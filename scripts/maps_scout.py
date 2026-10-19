#!/usr/bin/env python3
"""Google Maps scouting: the mechanical half of the outreach skill's Mode E ("maps scout").

Part of Freelancer OS.

Pulls one niche in one city from Google Maps (Apify, compass/crawler-google-places), measures every
homepage with the PageSpeed Insights API on mobile, checks a few outdated-site signals, and writes a
ranked candidate table. Claude takes it from there (email verification, the message, drafts, lead files).

Run: python3 scripts/maps_scout.py <command> ...

Commands:
  pull    --niche "wedding venues" --city "Austin, TX" [--max 60] [--cap-usd 1.00] [--dry-run] [--run-id ID]
          start the Apify run, wait for it, save raw.json and places.csv in the run folder
  measure --dir <run folder> [--limit 60]
          open each homepage (mobile user agent), read signals, one PSI mobile run each; writes measured.csv
  rank    --dir <run folder>
          apply the keep rules and the score; writes candidates.md (ranked table + filtered-out table)
  all     --niche ... --city ... [--max 60] [--cap-usd 1.00]
          pull, measure, rank in one go

Run folders: <runs_dir>/maps/YYYY-MM-DD-<niche-slug>-<city-slug>/ (runs_dir from config.yml, git-ignored).
Keys: APIFY_API_TOKEN and PAGESPEED_API_KEY from .env (or config.yml).
Cost: the Maps actor measured about $0.008 a place, so a 60-place run is about $0.50.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html as html_lib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = config.ROOT
MAPS_DIR = config.path_for("runs_dir") / "maps"
ACTOR = "compass~crawler-google-places"
APIFY = "https://api.apify.com/v2"
PSI = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
MOBILE_UA = ("Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/126.0 Mobile Safari/537.36")

# Links that are not a site of their own. A listing pointing here is "not own site".
NOT_OWN_SITE = (
    "facebook.com", "instagram.com", "linktr.ee", "yelp.com", "theknot.com", "weddingwire.com",
    "zola.com", "eventective.com", "peerspace.com", "tripadvisor.", "google.com", "business.site",
    "wixsite.com", "squarespace.com", "godaddysites.com", "weebly.com", "carrd.co", "linkedin.com",
    "venuereport.com", "partyslate.com", "airbnb.", "vrbo.com", "opentable.com", "yellowpages.",
)
# Hotel groups and chains: the listing's site is the brand's corporate domain, not the venue's own.
CHAIN_HOSTS = (
    "marriott.com", "hilton.com", "ihg.com", "intercontinental.com", "hyatt.com", "kimptonhotels.com",
    "fairmont.com", "fourseasons.com", "omnihotels.com", "auberge.com", "aubergeresorts.com", "wyndhamhotels.com",
    "choicehotels.com", "bestwestern.com", "radissonhotels.com", "accor.com", "loewshotels.com", "ritzcarlton.com",
    "hotelindigo.com", "sonesta.com", "drury", "legion.org", "ymca.org", "hilton", "marriott",
)
BUILDER_RE = re.compile(r"(wix\.com|squarespace|weebly|godaddy website builder|duda|webflow|shopify|"
                        r"wordpress|elementor|divi|joomla|drupal|hubspot|showit|site123|jimdo)", re.I)
THIS_YEAR = dt.date.today().year


def log(msg: str) -> None:
    print(msg, flush=True)


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def run_dir(niche: str, city: str, today: dt.date | None = None) -> Path:
    d = (today or dt.date.today()).isoformat()
    return MAPS_DIR / f"{d}-{slug(niche)}-{slug(city)}"


# ----------------------------------------------------------------------------- pull

def actor_input(niche: str, city: str, max_places: int) -> dict:
    return {
        "searchStringsArray": [niche],
        "locationQuery": city,
        "maxCrawledPlacesPerSearch": max_places,
        "language": "en",
        "website": "withWebsite",
        "skipClosedPlaces": True,
        "scrapeContacts": True,
        "scrapePlaceDetailPage": False,
        "maxReviews": 0,
        "maxImages": 0,
    }


def cmd_pull(niche: str, city: str, max_places: int, cap_usd: float, dry_run: bool,
             run_id: str = "") -> Path:
    payload = actor_input(niche, city, max_places)
    out = run_dir(niche, city)
    if dry_run:
        log(f"Would run {ACTOR} with input:\n{json.dumps(payload, indent=2)}\n"
            f"Cap: ${cap_usd:.2f}. Output folder: {out}")
        return out
    token = config.get_key("APIFY_API_TOKEN")
    out.mkdir(parents=True, exist_ok=True)
    if run_id:
        # Reattach to a run already started (a poll that dropped its connection), no second charge.
        run = {"id": run_id, "status": "RUNNING"}
        log(f"Reattached to Apify run {run_id} for '{niche}' in '{city}'.")
    else:
        r = requests.post(f"{APIFY}/acts/{ACTOR}/runs", params={"token": token}, json=payload, timeout=60)
        if r.status_code >= 300:
            die(f"Apify refused the run ({r.status_code}): {r.text[:400]}")
        run = r.json()["data"]
        run_id = run["id"]
        log(f"Apify run {run_id} started for '{niche}' in '{city}', up to {max_places} places, cap ${cap_usd:.2f}.")
    deadline = time.time() + 15 * 60
    status = run.get("status")
    usage = 0.0
    while time.time() < deadline:
        time.sleep(10)
        try:
            s = requests.get(f"{APIFY}/actor-runs/{run_id}", params={"token": token}, timeout=30).json()["data"]
        except requests.RequestException as e:
            log(f"  status check failed ({type(e).__name__}), retrying")
            continue
        status = s.get("status")
        usage = float(s.get("usageTotalUsd") or 0)
        log(f"  {status}, ${usage:.3f} so far")
        if usage > cap_usd and status in {"RUNNING", "READY"}:
            requests.post(f"{APIFY}/actor-runs/{run_id}/abort", params={"token": token}, timeout=30)
            log(f"Aborted: usage ${usage:.3f} passed the cap of ${cap_usd:.2f}. Partial results are kept.")
            break
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            break
    else:
        die("Apify run did not finish inside 15 minutes; check it in the Apify console.")
    dataset = s.get("defaultDatasetId")
    items = requests.get(f"{APIFY}/datasets/{dataset}/items", params={"token": token, "clean": "true"},
                         timeout=120).json()
    (out / "raw.json").write_text(json.dumps(items, indent=1))
    (out / "run.json").write_text(json.dumps({"runId": run_id, "status": status, "usageUsd": usage,
                                              "input": payload, "pulled": len(items),
                                              "at": dt.datetime.now().isoformat(timespec="minutes")}, indent=1))
    rows = []
    for it in items:
        emails = it.get("emails") or []
        socials = []
        for k in ("instagrams", "facebooks", "linkedIns", "twitters", "tiktoks", "youtubes"):
            socials += it.get(k) or []
        rows.append({
            "title": html_lib.unescape(it.get("title", "") or ""),
            "website": it.get("website", "") or "",
            "phone": it.get("phone", "") or "",
            "address": it.get("address", "") or "",
            "city": it.get("city", "") or "",
            "state": it.get("state", "") or "",
            "country": it.get("countryCode", "") or "",
            "reviews": it.get("reviewsCount") or 0,
            "rating": it.get("totalScore") or "",
            "category": it.get("categoryName", "") or "",
            "maps_url": it.get("url", "") or "",
            "emails": ";".join(emails),
            "socials": ";".join(socials),
            "closed": "yes" if (it.get("permanentlyClosed") or it.get("temporarilyClosed")) else "",
        })
    write_csv(out / "places.csv", rows)
    with_site = sum(1 for r_ in rows if r_["website"])
    log(f"Pulled {len(rows)} places, {with_site} with a website, cost ${usage:.3f}. Saved to {out}")
    return out


# ----------------------------------------------------------------------------- measure

def homepage(url: str) -> str:
    u = url.strip()
    if not u:
        return ""
    if not u.startswith("http"):
        u = "https://" + u
    p = urlparse(u)
    return f"{p.scheme}://{p.netloc}/"


def not_own_site(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(m in host for m in NOT_OWN_SITE)


def read_signals(url: str) -> dict:
    sig = {"final_url": "", "http_status": "", "https": "", "page_title": "", "viewport": "", "generator": "",
           "wordpress": "", "copyright_year": "", "coming_soon": "", "noindex": "", "fetch_error": ""}
    try:
        r = requests.get(url, headers={"User-Agent": MOBILE_UA, "Accept-Language": "en"}, timeout=20,
                         allow_redirects=True)
    except Exception as e:  # noqa: BLE001
        sig["fetch_error"] = type(e).__name__
        return sig
    html = r.text[:600_000]
    sig["final_url"] = r.url
    sig["http_status"] = r.status_code
    sig["https"] = "yes" if r.url.startswith("https://") else "no"
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    sig["page_title"] = html_lib.unescape(re.sub(r"\s+", " ", m.group(1))).strip()[:120] if m else ""
    sig["viewport"] = "yes" if re.search(r'<meta[^>]+name=["\']viewport', html, re.I) else "no"
    m = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', html, re.I)
    gen = m.group(1) if m else ""
    if not gen:
        m = BUILDER_RE.search(html[:200_000])
        gen = m.group(1) if m else ""
    sig["generator"] = gen[:60]
    sig["wordpress"] = "yes" if ("wp-content" in html or "wordpress" in gen.lower()) else "no"
    years = [int(y) for y in re.findall(r"(?:©|&copy;|&#169;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20\d{2})", html, re.I)]
    years += [int(y) for y in re.findall(r"(20\d{2})\s*(?:©|&copy;|&#169;)", html, re.I)]
    sig["copyright_year"] = max(years) if years else ""
    text = re.sub(r"<[^>]+>", " ", html[:300_000]).lower()
    sig["coming_soon"] = "yes" if ("coming soon" in text or "under construction" in text) else ""
    m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', html, re.I)
    sig["noindex"] = "yes" if (m and "noindex" in m.group(1).lower()) else ""
    return sig


SEO_AUDITS = ("document-title", "meta-description", "is-crawlable", "font-size", "tap-targets",
              "viewport", "link-text", "image-alt", "hreflang", "canonical", "robots-txt")


def psi(url: str, key: str) -> dict:
    out = {"psi_perf": "", "lcp_s": "", "cls": "", "tbt_ms": "", "speed_index_s": "", "psi_seo": "",
           "seo_fails": "", "psi_error": ""}
    params = [("url", url), ("strategy", "mobile"), ("category", "performance"), ("category", "seo"), ("key", key)]
    for attempt in (1, 2):
        try:
            r = requests.get(PSI, params=params, timeout=120)
            if r.status_code >= 500 and attempt == 1:
                time.sleep(5)
                continue
            d = r.json()
            if "error" in d:
                out["psi_error"] = d["error"].get("message", "error")[:120]
                return out
            lr = d["lighthouseResult"]
            a = lr["audits"]
            cats = lr["categories"]
            v = lambda k: a[k]["numericValue"]  # noqa: E731
            out["psi_perf"] = round(cats["performance"]["score"] * 100) if cats["performance"]["score"] is not None else ""
            out["lcp_s"] = round(v("largest-contentful-paint") / 1000, 1)
            out["cls"] = round(v("cumulative-layout-shift"), 3)
            out["tbt_ms"] = round(v("total-blocking-time"))
            out["speed_index_s"] = round(v("speed-index") / 1000, 1)
            if "seo" in cats and cats["seo"]["score"] is not None:
                out["psi_seo"] = round(cats["seo"]["score"] * 100)
            fails = [k for k in SEO_AUDITS if k in a and a[k].get("score") is not None and a[k]["score"] < 1]
            out["seo_fails"] = ";".join(fails)
            return out
        except Exception as e:  # noqa: BLE001
            out["psi_error"] = f"{type(e).__name__}"[:60]
            if attempt == 2:
                return out
            time.sleep(5)
    return out


def cmd_measure(d: Path, limit: int) -> None:
    places = read_csv(d / "places.csv")
    key = config.get_key("PAGESPEED_API_KEY")
    out_rows = []
    done = 0
    last_url = None
    for p in places:
        row = dict(p)
        hp = homepage(p["website"])
        row["homepage"] = hp
        if not hp:
            row["skip"] = "no site"
            out_rows.append(row)
            continue
        if not_own_site(hp):
            row["skip"] = "not own site"
            out_rows.append(row)
            continue
        if done >= limit:
            row["skip"] = "over limit"
            out_rows.append(row)
            continue
        log(f"[{done + 1}] {p['title']} -> {hp}")
        row.update(read_signals(hp))
        blocked = bool(row.get("fetch_error")) or (row.get("http_status") and int(row["http_status"]) >= 400)
        target = (row.get("final_url") if not blocked else "") or hp
        if target == last_url:
            time.sleep(3)
        row.update(psi(target, key))
        if blocked:
            row["fetch_note"] = f"direct fetch blocked ({row.get('fetch_error') or row.get('http_status')}); page signals unknown"
            if row.get("psi_error"):
                row["skip"] = f"site unreachable ({row.get('fetch_error') or row.get('http_status')}) and PSI failed"
        last_url = target
        if row.get("psi_error"):
            log(f"    PSI: {row['psi_error']}")
        else:
            log(f"    perf {row['psi_perf']}, LCP {row['lcp_s']}s, SEO {row['psi_seo']}, "
                f"gen {row['generator'] or '-'}, © {row['copyright_year'] or '-'}")
        out_rows.append(row)
        done += 1
        time.sleep(2)
    write_csv(d / "measured.csv", out_rows)
    log(f"Measured {done} sites. Saved {d / 'measured.csv'}")


# ----------------------------------------------------------------------------- rank

def chain_domains(rows: list[dict]) -> set[str]:
    seen: dict[str, int] = {}
    for r in rows:
        h = urlparse(r.get("homepage") or "").netloc.lower()
        if h:
            seen[h] = seen.get(h, 0) + 1
    return {h for h, n in seen.items() if n > 1}


def evaluate(r: dict, chains: set[str]) -> tuple[str, int, str, list[str]]:
    """Return (finding_type or '', score, measured line, signals). Empty finding type = filtered out."""
    if r.get("skip"):
        return "", 0, r["skip"], []
    host = urlparse(r.get("homepage") or "").netloc.lower()
    if host in chains:
        return "", 0, "chain (same site on several listings)", []
    if any(c in host for c in CHAIN_HOSTS):
        return "", 0, "chain or hotel group (corporate domain)", []
    if r.get("psi_error") and r.get("fetch_note"):
        return "", 0, f"PSI failed ({r['psi_error']}) and the page could not be read", []
    perf = int(r["psi_perf"]) if str(r.get("psi_perf", "")).strip() != "" else None
    lcp = float(r["lcp_s"]) if str(r.get("lcp_s", "")).strip() != "" else None
    seo = int(r["psi_seo"]) if str(r.get("psi_seo", "")).strip() != "" else None
    year = int(r["copyright_year"]) if str(r.get("copyright_year", "")).strip() != "" else None
    signals: list[str] = []
    score = 0
    speed = perf is not None and (perf < 50 or (lcp is not None and lcp > 6.0))
    if perf is not None and perf < 50:
        score += (50 - perf) // 5
        signals.append(f"mobile performance {perf}")
    if lcp is not None and lcp > 6.0:
        signals.append(f"loads in {lcp}s on a phone (LCP)")
        if lcp > 10.0:
            score += 2
    seo_bad = seo is not None and seo < 80
    if seo_bad:
        signals.append(f"SEO {seo}: {r.get('seo_fails') or 'see PSI'}")
        score += 1
    outdated = []
    fetched = not r.get("fetch_note")
    if fetched and year is not None and year <= THIS_YEAR - 3:
        outdated.append(f"copyright {year}")
    if fetched and r.get("https") == "no":
        outdated.append("no HTTPS")
    if fetched and r.get("viewport") == "no":
        outdated.append("no viewport meta (not built for phones)")
    t = (r.get("page_title") or "").strip().lower()
    if fetched and (t in {"", "home", "homepage", "welcome"} or t == host or t == host.replace("www.", "")):
        outdated.append(f"page title '{r.get('page_title') or '(none)'}'")
    if fetched and r.get("noindex") == "yes":
        signals.append("homepage carries a noindex robots meta (tells Google not to list it)")
        score += 3
        seo_bad = True
    if fetched and r.get("coming_soon") == "yes":
        outdated.append("'coming soon' text on the homepage")
    score += len(outdated)
    signals += outdated
    if not (speed or seo_bad or outdated):
        return "", 0, f"scores fine (perf {perf}, SEO {seo}, © {year or '-'})", []
    try:
        if int(r.get("reviews") or 0) >= 50:
            score += 1
    except ValueError:
        pass
    if r.get("wordpress") == "yes":
        score += 1
    if speed:
        ftype = "Speed"
    elif len(outdated) >= 2 or (outdated and not seo_bad):
        ftype = "Outdated"
    else:
        ftype = "SEO"
    if ftype == "Speed":
        line = f"Homepage loads in {lcp}s on a phone, mobile performance {perf}"
    elif ftype == "Outdated":
        line = "; ".join(outdated)
    else:
        line = f"SEO {seo}: {r.get('seo_fails') or 'see PSI'}"
    if r.get("fetch_note"):
        signals.append("direct fetch blocked; check the page by eye")
    return ftype, score, line, signals


def cmd_rank(d: Path) -> None:
    rows = read_csv(d / "measured.csv")
    chains = chain_domains(rows)
    kept, dropped = [], []
    for r in rows:
        ftype, score, line, signals = evaluate(r, chains)
        if ftype:
            kept.append((score, int(r.get("reviews") or 0), ftype, line, signals, r))
        else:
            dropped.append((line, r))
    kept.sort(key=lambda k: (-k[0], -k[1]))
    run = json.loads((d / "run.json").read_text()) if (d / "run.json").exists() else {}
    lines = [f"# Candidates: {d.name}", "",
             f"Pulled {run.get('pulled', len(rows))} places (Apify ${run.get('usageUsd', 0):.3f}); "
             f"{sum(1 for r in rows if not r.get('skip'))} measured; {len(kept)} kept; {len(dropped)} filtered out. "
             f"Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}.", "",
             "## Ranked, worst measured first", "",
             "| # | Score | Type | Business | Website | Measured | Signals | Reviews | Platform | Emails found | Maps |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (score, rev, ftype, line, signals, r) in enumerate(kept, 1):
        lines.append(f"| {i} | {score} | {ftype} | {r['title']} | {r.get('homepage', '')} | {line} | "
                     f"{'; '.join(signals)} | {rev} | {r.get('generator') or ('WordPress' if r.get('wordpress') == 'yes' else '-')} | "
                     f"{r.get('emails') or '-'} | {r.get('maps_url', '')} |")
    lines += ["", "## Filtered out", "", "| Business | Website | Reason |", "|---|---|---|"]
    for line, r in dropped:
        lines.append(f"| {r['title']} | {r.get('homepage') or r.get('website') or '-'} | {line} |")
    (d / "candidates.md").write_text("\n".join(lines) + "\n")
    log(f"Kept {len(kept)}, filtered {len(dropped)}. Saved {d / 'candidates.md'}")
    log("")
    log(f"{'#':>2}  {'sc':>2}  {'type':8} {'business':40} measured")
    for i, (score, rev, ftype, line, signals, r) in enumerate(kept[:15], 1):
        log(f"{i:>2}  {score:>2}  {ftype:8} {r['title'][:40]:40} {line}")


# ----------------------------------------------------------------------------- io

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    keys: list[str] = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        die(f"{path} not found; run the earlier stage first")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


# ----------------------------------------------------------------------------- main

def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def pull_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--niche", required=True)
        p.add_argument("--city", required=True)
        p.add_argument("--max", type=int, default=60)
        p.add_argument("--cap-usd", type=float, default=1.00)
        p.add_argument("--run-id", default="", help="reattach to an Apify run already started")

    p = sub.add_parser("pull")
    pull_args(p)
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("measure")
    p.add_argument("--dir", required=True)
    p.add_argument("--limit", type=int, default=60)
    p = sub.add_parser("rank")
    p.add_argument("--dir", required=True)
    p = sub.add_parser("all")
    pull_args(p)
    p.add_argument("--limit", type=int, default=60)
    a = ap.parse_args(argv)

    if a.cmd == "pull":
        cmd_pull(a.niche, a.city, a.max, a.cap_usd, a.dry_run, a.run_id)
    elif a.cmd == "measure":
        cmd_measure(Path(a.dir), a.limit)
    elif a.cmd == "rank":
        cmd_rank(Path(a.dir))
    elif a.cmd == "all":
        d = cmd_pull(a.niche, a.city, a.max, a.cap_usd, False, a.run_id)
        cmd_measure(d, a.limit)
        cmd_rank(d)


if __name__ == "__main__":
    main(sys.argv[1:])
