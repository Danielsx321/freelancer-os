#!/usr/bin/env python3
"""Lead tracker for the outreach skill.

Reads and updates the lead files in the leads folder (leads_dir in config.yml). Every date the
follow-up system relies on comes from here, never from Claude's own arithmetic.

Commands:
  slug "<Ref>"                     filename slug for a Ref, e.g. "PPC Geeks Sep 2026" -> ppc-geeks-2026-09
  review [--today YYYY-MM-DD]      the follow-up review list (due now / not due / needs a decision / drafted)
  sent <slug> [--date YYYY-MM-DD]  mark the pending touch as sent; stamps dates, advances the count, sets next action
  state <slug> "<State>"           set State (Replied: live, Replied: no, Dead: hired someone, Dead: bounced,
                                   Dead: no response, Parked: revisit YYYY-MM-DD)
  check <term> [<term> ...]        has this company, domain or person been pitched already?
  list                             one line per lead

Standard library only. The LEADS_DIR env var overrides the folder (used by tests).
"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = config.ROOT
LEADS_DIR = Path(os.environ["LEADS_DIR"]) if os.environ.get("LEADS_DIR") else config.path_for("leads_dir")

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

# Which touches each contact type runs, and the gap in days before each one.
# Named personal: full sequence. Shared mailbox drops touch 3 (the reserve proof).
# Form only: the opening, then the still-needed question.
SEQUENCES = {
    "named personal": [1, 2, 3, 4, 5],
    "shared mailbox": [1, 2, 4, 5],
    "form only": [1, 4],
}
DAY_OF_TOUCH = {1: 0, 2: 2, 3: 7, 4: 17, 5: 31}
DECIDE_AFTER_LAST = 14  # days after the final touch before a silent lead needs a decision

TOUCH_CARRIES = {
    1: "opening",
    2: "second observation (or diagnostic question)",
    3: "reserve proof (or diagnostic question if empty)",
    4: "still needed?",
    5: "A/B/C",
}

FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z /()]*?):[ \t]+(.*)$")


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_date(s: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(s.strip()[:10])
    except ValueError:
        return None


def slugify(ref: str) -> str:
    words = ref.strip().split()
    if len(words) >= 3 and words[-2].lower()[:3] in MONTHS and re.fullmatch(r"\d{4}", words[-1]):
        name = " ".join(words[:-2])
        suffix = f"{words[-1]}-{MONTHS[words[-2].lower()[:3]]:02d}"
    else:
        name, suffix = ref, ""
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{base}-{suffix}" if suffix else base


class Lead:
    def __init__(self, path: Path):
        self.path = path
        self.text = path.read_text()
        self.fields: dict[str, str] = {}
        section = ""
        for line in self.text.splitlines():
            if line.startswith("# ") and "ref" not in self.fields:
                self.fields["ref"] = line[2:].strip()
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            m = FIELD_RE.match(line)
            if m:
                key = m.group(1).strip().lower()
                if section in ("site", "proof") and key in ("spent", "reserve"):
                    key = f"{section} {key}"
                self.fields.setdefault(key, m.group(2).strip())

    def get(self, key: str) -> str:
        return self.fields.get(key, "")

    @property
    def slug(self) -> str:
        return self.path.stem.removeprefix("lead-")

    @property
    def contact_type(self) -> str:
        ct = self.get("contact type").lower()
        for k in SEQUENCES:
            if ct.startswith(k):
                return k
        return "named personal"

    @property
    def sequence(self) -> list[int]:
        return SEQUENCES[self.contact_type]

    @property
    def sent_count(self) -> int:
        m = re.match(r"(\d+)", self.get("touches sent"))
        return int(m.group(1)) if m else 0

    @property
    def state(self) -> str:
        return self.get("state")

    def set_field(self, key: str, value: str) -> None:
        pat = re.compile(rf"^({re.escape(key)}:[ \t]+).*$", re.M | re.I)
        if not pat.search(self.text):
            die(f"{self.path.name} has no '{key}:' line")
        self.text = pat.sub(lambda m: m.group(1) + value, self.text, count=1)

    def save(self) -> None:
        self.path.write_text(self.text)


def load_leads() -> list[Lead]:
    if not LEADS_DIR.exists():
        return []
    return [Lead(p) for p in sorted(LEADS_DIR.glob("lead-*.md"))]


def find_lead(slug: str) -> Lead:
    slug = slug.removeprefix("lead-").removesuffix(".md")
    p = LEADS_DIR / f"lead-{slug}.md"
    if p.exists():
        return Lead(p)
    hits = [l for l in load_leads() if slug in l.slug]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        die(f"no lead file matches '{slug}' in {LEADS_DIR}")
    die(f"'{slug}' matches several leads: " + ", ".join(l.slug for l in hits))


def next_touch(lead: Lead) -> int | None:
    seq, n = lead.sequence, lead.sent_count
    return seq[n] if n < len(seq) else None


def next_action_after(lead: Lead, sent_touch: int, sent_on: dt.date) -> dt.date:
    """Gap from the touch just sent to the next one in this lead's sequence."""
    seq = lead.sequence
    i = seq.index(sent_touch)
    if i + 1 < len(seq):
        gap = DAY_OF_TOUCH[seq[i + 1]] - DAY_OF_TOUCH[sent_touch]
    else:
        gap = DECIDE_AFTER_LAST
    return sent_on + dt.timedelta(days=gap)


def cmd_review(today: dt.date) -> None:
    due, not_due, decide, drafted, closed = [], [], [], [], 0
    for l in load_leads():
        ref, st = l.get("ref") or l.slug, l.state.lower()
        total = len(l.sequence)
        if st.startswith("drafted"):
            nt = next_touch(l)
            label = f"touch {l.sent_count + 1} of {total} ({TOUCH_CARRIES[nt]})" if nt else "a message"
            drafted.append(f"- {ref}: {label} written, not marked sent (say \"sent {l.slug}\")")
            continue
        if st.startswith("parked"):
            d = parse_date(re.sub(r"^.*?revisit\s*", "", l.state, flags=re.I))
            if d and d <= today:
                decide.append(f"- {ref}: parked, revisit date {d.isoformat()} has arrived")
            else:
                closed += 1
            continue
        if not st.startswith("awaiting"):
            closed += 1
            continue
        last = parse_date(l.get("last sent"))
        nxt = parse_date(l.get("next action"))
        days = (today - last).days if last else None
        since = f"{days} days since last send" if days is not None else "last send date missing"
        t = next_touch(l)
        if t is None:
            if nxt is None or nxt <= today:
                decide.append(f"- {ref}: touch budget spent ({l.sent_count} of {total}), no reply, {since}")
            else:
                not_due.append(f"- {ref}: budget spent, decision due {nxt.isoformat()}")
            continue
        if nxt is None:
            decide.append(f"- {ref}: no next action date on file")
            continue
        extra = []
        doubt = l.get("open doubt").lower()
        second = l.get("second channel").lower()
        if doubt and doubt not in ("none", "-") and l.sent_count == 2:
            if second and not second.startswith("none"):
                extra.append(f"open doubt unresolved after two silent emails; move to {l.get('second channel')}")
            else:
                decide.append(f"- {ref}: open doubt unresolved after two silent emails, no second channel")
                continue
        if t == 3 and l.get("proof reserve").lower().startswith("empty"):
            extra.append("proof reserve empty, carries a diagnostic question")
        if t == 2 and l.get("site reserve").lower().startswith(("empty", "not inspected")):
            extra.append("no site reserve, carries a diagnostic question")
        line = f"- {ref}: touch {l.sent_count + 1} of {total} ({TOUCH_CARRIES[t]}), {since}"
        if extra:
            line += "; " + "; ".join(extra)
        if nxt <= today:
            due.append(line)
        else:
            not_due.append(f"- {ref}: touch {l.sent_count + 1} of {total} ({TOUCH_CARRIES[t]}) due {nxt.isoformat()}")
    for title, rows in (("Due now", due), ("Not due", not_due), ("Needs a decision", decide),
                        ("Drafted, not sent", drafted)):
        print(title)
        print("\n".join(rows) if rows else "- none")
        print()
    print(f"Closed or parked (not shown): {closed}")


def cmd_sent(slug: str, on: dt.date) -> None:
    l = find_lead(slug)
    st = l.state.lower()
    if not (st.startswith("drafted") or st.startswith("awaiting")):
        die(f"{l.slug} is '{l.state}', not running; nothing to mark sent")
    t = next_touch(l)
    if t is None:
        die(f"{l.slug} has already spent its budget ({l.sent_count} of {len(l.sequence)})")
    if "| pending |" not in l.text:
        die(f"{l.slug} has no log row marked 'pending'; write the touch before marking it sent")
    l.text = l.text.replace("| pending |", f"| {on.isoformat()} |", 1)
    n = l.sent_count + 1
    l.set_field("Touches sent", f"{n} of {len(l.sequence)}")
    l.set_field("Last sent", on.isoformat())
    l.set_field("Next action", next_action_after(l, t, on).isoformat())
    l.set_field("State", "Awaiting reply")
    if t == 1 and re.search(r"^Opened:[ \t]+", l.text, re.M):
        l.set_field("Opened", on.isoformat())
    l.save()
    after = Lead(l.path)
    nt = next_touch(after)
    what = f"next is touch {after.sent_count + 1} ({TOUCH_CARRIES[nt]}), due {after.get('next action')}" if nt else f"budget spent; decision due {after.get('next action')}"
    print(f"{after.get('ref')}: {TOUCH_CARRIES[t]} marked sent {on.isoformat()}. {after.get('touches sent')} sent; {what}.")


def cmd_state(slug: str, state: str) -> None:
    l = find_lead(slug)
    l.set_field("State", state)
    s = state.lower()
    if s.startswith(("replied", "dead")):
        l.set_field("Next action", "None")
    elif s.startswith("parked"):
        d = parse_date(re.sub(r"^.*?revisit\s*", "", state, flags=re.I))
        l.set_field("Next action", d.isoformat() if d else "None")
    l.save()
    print(f"{l.get('ref')}: State set to '{state}'.")


def cmd_check(terms: list[str]) -> None:
    terms = [t.lower() for t in terms if t.strip()]
    found = False
    for folder, label in ((LEADS_DIR, "outreach lead"),):
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.md")):
            text = p.read_text().lower()
            hit = [t for t in terms if t in text]
            if hit:
                found = True
                print(f"{label}: {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} (matched: {', '.join(hit)})")
    if not found:
        print("No match in the lead files.")


def cmd_list() -> None:
    leads = load_leads()
    if not leads:
        print("No lead files yet.")
    for l in leads:
        print(f"{l.slug}: {l.state} · {l.get('touches sent')} · next {l.get('next action')}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]

    def opt(name: str) -> dt.date:
        if name in rest:
            i = rest.index(name)
            d = parse_date(rest[i + 1]) if i + 1 < len(rest) else None
            if not d:
                die(f"{name} needs a YYYY-MM-DD date")
            del rest[i:i + 2]
            return d
        return dt.date.today()

    if cmd == "slug":
        print(slugify(" ".join(rest)))
    elif cmd == "review":
        cmd_review(opt("--today"))
    elif cmd == "sent":
        on = opt("--date")
        if not rest:
            die("sent needs a lead slug")
        cmd_sent(rest[0], on)
    elif cmd == "state":
        if len(rest) < 2:
            die('state needs a slug and a state, e.g. state ppc-geeks-2026-09 "Replied: live"')
        cmd_state(rest[0], " ".join(rest[1:]))
    elif cmd == "check":
        cmd_check(rest)
    elif cmd == "list":
        cmd_list()
    else:
        die(f"unknown command '{cmd}'")


if __name__ == "__main__":
    main(sys.argv[1:])
