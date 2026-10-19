---
name: outreach
description: >
  Cold outreach from a job post to a direct email, one pass. Use when the user pastes a job post or
  job link to pitch the client directly: work out the real business and decision-maker behind the
  post, find a verified email, open their site, write the cold email in the user's client voice,
  and save a lead file for follow-ups. Also for "follow up time", "who's due", "follow up with
  <company>", "sent", "sent <company>", "<company> replied", "it bounced", "they hired someone", and
  for changes to the outreach playbooks, the proof bank or lead files. Also "job scout" (Claude finds
  fresh posts itself), "maps scout <niche> in <city>" (slow-website lane) and "seo scout <niche> in
  <city>" (not-ranking lane), when those lanes are switched on in config.yml. Not for writing a
  proposal to submit on the platform; that is the proposals skill.
---

# Outreach

One pipeline: job post in, research plus cold email plus lead file out. "Follow up time" reads the lead files and writes the next touch. Dates come from a script, never from Claude's head.

**Files**
- `reference/research.md`: stage 1, finding the business behind the post
- `reference/outreach.md`: stage 2, the opening email, proof matching, voice
- `reference/follow-up.md`: stage 3, the five-touch sequence
- `reference/lead-file.md`: the lead file format and its life cycle
- `reference/job-scout.md`: Mode D, Claude finds the best fresh posts itself (needs the Upwork connector)
- `reference/maps-scout.md`: Mode E, one niche in one city, every site measured, the slowest pitched. Script: `scripts/maps_scout.py`
- `reference/seo-scout.md`: Mode F, local businesses that are not ranking, one verified reason each. Script: `scripts/seo_scout.py`
- `reference/proof-bank.template.md`: the shape of `context/proof-bank.md`, which `/activate` creates
- `scripts/leads_tool.py`: dates, review list, "sent", state changes, duplicate check
- `config.yml`: sender name and email, portfolio link, lanes on or off, send caps, folders. Read it at the start of every run

**Before anything:** read `config.yml`, `context/offer.md`, `context/proof-bank.md` and `context/client-voice.md`. If `config.yml` is missing, say so in one line and point to `/activate`.

**Which mode.** Work it out from the message; don't announce it.

| They send | Run |
|---|---|
| A job post (text or link), or several | Mode A |
| "Follow up time", "who's due" | Mode B, review only |
| "Follow up with X", "write touch 2 for X", names from the review list | Mode B, write |
| "Sent", "sent X", "X replied", "bounced", "they hired someone", "the post closed" | Mode C |
| "Job scout", "scout for jobs", "another 10" | Mode D, if `lanes.job_scout` is on |
| "Maps scout", "maps scout <niche> in <city>" | Mode E, if `lanes.maps_scout` is on |
| "SEO scout", "seo scout <niche> in <city>" | Mode F, if `lanes.seo_scout` is on |
| A change to how the system works (playbook edit, new proof, correct a lead file) | Make the change and stay out of A and B |

A lane that is off gets one line: "The maps scout lane is off in config.yml (`lanes.maps_scout`). Switch it on and add the keys, or run `/activate` again." Nothing else runs.

If it's unclear whether a pasted post is for a cold email or for a proposal on the platform, ask in one line.

## Mode A: job post in, message out

For each post, in the order given (one output per post; never merge or summarise across them):

0. **Red-flag scan** per `reference/research.md` Step 0. Any "don't contact me outside the platform" language: stop, quote the line, ask. Nothing else runs until they answer.
1. **Duplicate check** (`python3 scripts/leads_tool.py check "<company>" "<domain>" "<phrase>"`). If the company is already a lead, re-open that file instead of starting a new one.
2. **Research** per `reference/research.md`. Live tools, a source on every fact, an honest grade.
3. **Write the opening** per `reference/outreach.md`. Pick the proof and the reserve from `context/proof-bank.md`.
4. **Save the lead file** per `reference/lead-file.md`: `State: Drafted`, log row `pending`, research block and sources in `## Research`, the message in `## Messages`.
5. **Ledger row**, if the workspace has a `ledger/` folder: `outreach/research` with the Ref and grade. No names of private individuals or email addresses in the ledger.

**What they see, in this order and nothing else:**
1. The research block, then Notes for outreach (as in `research.md`)
2. Subject line (code block)
3. Email body (code block)
4. Attachment line, only if `resume_path` is set in config: the file name and one line why
5. LinkedIn note (code block), only when LinkedIn is the verified or primary channel
6. One sentence per gap that affected the message
7. `Saved: <leads_dir>/lead-<slug>.md. Say "sent" once it's out.`

No preamble and no restating the post. **When the research grades Not found and there's no route**, still write the message for the route that exists (a form, a DM), set the contact type to match, and say what's missing in one line. When there's no route at all, return the research block and stop; the lead file is still saved so nothing is repeated later.

**They decided before pasting.** Don't open by questioning whether the lead is worth it, don't close by second-guessing it, and give no pursue-or-skip verdict. Facts that bear on the lead go in Notes for outreach without a recommendation.

**Gmail.** If the Gmail connector is connected, save the email as a draft with `create_draft`: To the verified address, `htmlBody` only (paragraphs with `<br><br>`, links as `<a href="https://x">https://x</a>`; a plain-text body gets every link rewritten into a visible redirect), the resume attached if configured. Record the draft id in the lead file's Notes. If Gmail isn't connected, the code blocks are the deliverable.

## Mode B: follow-ups

"Follow up time" runs the review in `reference/follow-up.md` and stops at the list. A named lead gets its next touch written, per the same file. Never write a follow-up without reading that lead's file first.

## Mode C: record what happened

- "Sent" with one lead drafted: `python3 scripts/leads_tool.py sent <slug>`. With several drafted, ask which (or "all").
- A different send date ("sent it yesterday"): `--date YYYY-MM-DD`.
- Replies, bounces, closures, hires: `python3 scripts/leads_tool.py state <slug> "<State>"`, plus a dated line in the file's Notes. On "Replied: live", offer to help with the reply; the lead is now a conversation and the client-delivery skill takes over.
- Quote the script's output line back. That's the confirmation.

## Modes D, E and F

Run the matching reference file in this session, start to finish. Each is a full run: pull, research, write, draft, file, summarise. Each ends with a batch file and a summary; nothing is ever sent.

## Standing rules

- Search before answering. Never fill a field from assumption. An empty field or "Not found" is a valid answer.
- **Personal inbox first, every lane.** The decision-maker's gmail, hotmail, yahoo, outlook or icloud address is what the research looks for (`reference/research.md` step 6). A business address goes out only when no personal one exists after the full search and the mailbox is shown to be alive. Owners rarely read their web mailbox.
- Never present an inferred email as confirmed. Never write the opening to a pattern-guess address without saying so on the first line after the message: a bounce hurts the sending inbox.
- A post that asks not to be contacted off the platform is a red flag and stops the run until the user decides.
- Agency posts: record both, agency first; never approach the end client.
- "Site inspected: Yes" only if the page was opened. Every quoted observation must be visible on the rendered page, never in raw HTML or a comment, and re-checked the day the email goes out.
- No price, no timeline in any client-facing message.
- The work and the hiring are referable. The platform by name and the research trail are not, including any "top rated" badge from the platform.
- Every client-facing message ends with `portfolio_url`. Sent as `sender_name`.
- **Send rule:** at most `daily_send_cap` new cold openings a day from `sender_email`, never more than `per_15_min_cap` in any 15 minutes, best leads first. Follow-ups in an existing thread don't count. Two bounces in a day stop new sends for the day.
- **Stale drafts:** a drafted email older than `stale_days_*` for its lane is deleted, not sent. The lead is marked `Stale, not sent` and never re-sent from the old draft.
- Plain punctuation: commas, full stops, semicolons. No em dashes anywhere.
- Anything the user copies goes in a fenced code block.
- Where something is missing, say so in one sentence after the message and still write it, using the safer version.
- Chat is direct and compressed; they read these in volume. The chat register is never the client voice.

## Things that bite

- Gmail tracking extensions (Streak, Mailtrack and the like) rewrite every link in a sent email into a double redirect and add tracking pixels. Spam filters notice. Turn them off before cold sends and check one Sent message's raw source ("Show original") to confirm the links are bare.
- A plain-text Gmail body gets every URL wrapped in a visible google.com redirect. Always `htmlBody`.
- Cold email from a personal inbox gets flagged fast. Keep to the caps, never send to unverified addresses in bulk, and space sends out.
- At "follow up time", search the connected Gmail for replies from each running lead's address before listing touches as due, and record any with `state`.
