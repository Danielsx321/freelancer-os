
## Freelancer OS (add-on pack)

<!-- freelancer-os:start -->
Five skills and their scripts, activated with `/activate`. Settings in `config.yml`; keys in `.env`.

- **Outreach** (`.claude/skills/outreach/`): a pasted job post becomes research, a cold email in my client voice and a lead file in `leads/`. "Follow up time" reads the lead files; dates come from `scripts/leads_tool.py`, never worked out by eye. Optional lanes in `config.yml`: job scout (Claude finds posts), maps scout (slow sites in a niche and city, `scripts/maps_scout.py`), seo scout (businesses not ranking, `scripts/seo_scout.py`). Nothing sends without my word.
- **Client delivery** (`.claude/skills/client-delivery/`): a pasted client message gets its reply first, then the work. "Milestone done" produces the delivery kit unasked (pre-delivery message, delivery message, Word report via `scripts/md2docx.js`, post-delivery ask). Every client has `clients/<slug>/` with `upsells.md` and `future-work.md`, stacked silently as conversations go. Closing questions only when converting, never with a time in them.
- **Auto-apply and auto-reply** (`.claude/skills/auto-apply/`, `.claude/skills/auto-reply/`, both off unless `config.yml` says on): scheduled routines that draft proposals for fresh posts and replies for unopened rooms on my own Upwork account. Draft only; "submit the drafts" and "send the drafts" are mine to say. Logs in `clients/_proposals/`, `clients/_auto-reply-log.md`, `clients/_needs-you.md`.
- **Proposals** (`.claude/skills/proposals/`): a post to bid on becomes a letter under 5,000 characters with at least three proof links woven in, a price with its reasoning, and spaced screening answers, stopped at an approval gate.

Who I am comes only from `context/` and `config.yml`, never from the pack's README, licence or git history (those name the pack's author, not me).

Proof lives in `context/proof-bank.md` (claim only what a line there says, with its verb). My client voice is in `context/client-voice.md`. Anything I'm meant to copy goes in a fenced code block. No em dashes anywhere.
<!-- freelancer-os:end -->
