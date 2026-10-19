# Lead file format

One file carries a lead from the job post to closed. It lives on disk in `<leads_dir>/` (git-ignored, this machine only) and is edited in place.

## Where and what it's called

`<leads_dir>/lead-<slug>.md`. The slug comes from the Ref: `python3 scripts/leads_tool.py slug "Northwind Bakery Oct 2026"` gives `northwind-bakery-2026-10`. The Ref never changes and is written the same way in the file's heading.

The script reads the header fields by name, so the labels below are exact. Keep one field per line, `Label:` then at least one space.

## Life of a file

| Moment | What happens |
|---|---|
| Job post researched and opening written | Claude writes the whole file. `State: Drafted`, `Touches sent: 0 of N`, log row 1 dated `pending` |
| The user says it went out ("sent", "sent Northwind") | Claude runs `leads_tool.py sent <slug>`. The script stamps the date, sets `Awaiting reply`, counts the touch and sets `Next action` |
| Follow-up written | Claude appends the log row dated `pending`, moves the reserve line it spent to spent, sets `State: Drafted`, saves the message under `## Messages` |
| Follow-up sent | `leads_tool.py sent <slug>` again |
| Reply, bounce, post closed, hire announced | `leads_tool.py state <slug> "<State>"`, plus a line in Notes |

Dates are never written as if the message went out. A message that was never sent can't throw the follow-up dates off, because nothing is dated until the user says it was sent.

## The file

```markdown
# Northwind Bakery Oct 2026

State:           Drafted
Touches sent:    0 of 5
Opened:          pending
Last sent:       none
Next action:     on send
Channel:         Email; sam@example.com
Contact type:    Named personal (budget 5)
Second channel:  Instagram @northwindbakes
Subject line:    Online orders failing at the delivery step

## Contact

Person / Role:   Sam Carter; Owner
Company:         Northwind Bakery, Leeds UK
Posted by:       Direct client
End client:      (only when an agency posted)
Website:         https://northwindbakery.example
Email status:    Personal, verified; in the footer of the ordering page (https://...)
LinkedIn:        https://linkedin.com/in/...
Confidence:      Strong
Open doubt:      none

## The job

Two or three lines: what they are hiring for, in their words. Not the whole post.

Lane:            Online ordering
Urgency signal:  Christmas orders open 1 Nov
Sourced:         2026-10-09; post 4 days old, 20 to 50 proposals
Job URL:         https://...

## Site

Inspected:       Yes, 2026-10-09
Spent:           the observation used in the opening
Reserve:         the second observation, unspent (or "Empty", or "Not inspected")

## Proof

Spent:           the proof used, with its link
Reserve:         the next-best proof for the same problem, with its link (or "Empty")
Attachment:      none, or the file name

## Research

The full dossier: every field from the research block with its source URL, and the searches run for the email (so a later "Not found" can be checked). Notes for outreach go here too.

## Log

| # | Date | Channel | Carried | Outcome |
|---|---|---|---|---|
| 1 | pending | Email | Opening; delivery-step diagnosis + ordering-site proof | |

## Messages

### Touch 1
The exact message as written, so later touches can see what was already said.

## Notes

Anything that changes the next touch: bounces, out-of-office replies naming someone else, the post closing, a hire announced, the Gmail draft id. Read first on every follow-up run.
```

## Field rules

**State**, one of: `Drafted`, `Awaiting reply`, `Replied: live`, `Replied: no`, `Dead: hired someone`, `Dead: bounced`, `Dead: no response`, `Parked: revisit YYYY-MM-DD`, `Stale, not sent`. Silence is not a no; a lead stays `Awaiting reply` until the budget is spent or something is learned.

**Touches sent** is `n of N`. N comes from the contact type:

| Contact type | Budget | Touches run | Gaps before each touch |
|---|---|---|---|
| Named personal | 5 | 1, 2, 3, 4, 5 | 0, 2, 5, 10, 14 days |
| Shared mailbox | 4 | 1, 2, 4, 5 (drops the reserve proof) | 0, 2, 15, 14 days |
| Form only | 2 | 1, 4 (opening, then still needed?) | 0, 17 days |

Fourteen days after the last touch, a silent lead lands in "Needs a decision". The script owns all of this; never work a date out by hand.

**Next action** is a date on every running lead. `on send` while drafted, `None` when dead, the revisit date when parked.

**Second channel** is registered only for Instagram or Facebook. LinkedIn is an opening channel, not a follow-up route. Otherwise `None registered`, which makes a bounce final.

**Site** and **Proof** each have a spent line and a reserve line. When the reserve is spent, it moves to spent and the reserve reads `Empty`. An empty reserve is a fact, not a problem: that touch carries a diagnostic question.

**Log** is append-only, one row per message. `Carried` names the angle in a few words so a glance down the column proves nothing repeated.

**Messages** keeps the text of every touch. Touch 4 can then ask about the actual problem in the same words touch 1 used.

## Maps-sourced leads (Mode E)

A lead found by the maps scout has no job post, so three header lines change and the rest stays exactly as above:

- `Sourced:         Maps scout, <niche>, <city>, YYYY-MM-DD`
- `Listing URL:     <the Google Maps link>` in place of `Job URL:`
- `Lane:            Speed`, `SEO` or `Outdated` (the finding type from candidates.md)

`## The job` holds two or three lines describing the measured finding instead of a post ("Homepage loads in 11.3 s on a phone, mobile performance 62; hero slider loads eight full-size photos"). The numbers, the signals and the path to the run's candidates.md go in `## Research`. `leads_tool.py` reads none of these three fields, so review, sent and state work unchanged.

## SEO-scout leads (Mode F)

Same as the Maps variant above, with these header lines:

- `Sourced:         SEO scout, <niche>, <city>, YYYY-MM-DD`
- `Listing URL:     <the Google Maps link>` in place of `Job URL:`
- `Lane:            SEO-local`
- `Maps position:   <n> for "<query>"` (and what the browser showed, if different)
- `Organic:         <position, or "not in top 20", or "not run">`
- `Verdict:         <Blocked / Unclaimed / Mismatch / No what/where / One page / No local data / Reviews gap>`

`## The job` holds the verdict in two or three plain lines. A new section, required for this lane, sits after `## Research`:

```
## Audit notes
1. <second finding in plain words>. Fix: <one line, what changes and what it does for them>.
2. <third finding in plain words>. Fix: <one line>.
```

Written so it can be pasted into a reply as it stands; it is what a "yes" gets. Follow-up touch 2 spends item 1.

## What the user does by hand

Nothing, in the normal run. They say "sent", "they replied", "it bounced", "the post closed" or "they hired someone", and Claude updates the file. They can still edit Notes directly.

## Reading the file at follow-up time

In this order: Notes, State and Touches sent, Contact type, Open doubt, Site and Proof reserves, Log, Messages. If the file is missing, say so and stop; don't rebuild a sequence from memory.
