# /activate

> Turns the Freelancer OS pack on for this workspace. About ten minutes. A conversation, not a script: explain, confirm, act, verify, stop, for every step.

## Variables

args: $ARGUMENTS (usually empty)

**Always check `.activate-state` first.** If it exists and isn't marked complete, greet them back by name and resume at the first step that isn't done. Never re-ask something that's already answered; check the files on disk and let reality win.

---

## FOR CLAUDE, how to run this

- Assume a smart person who may never have used Claude Code. No jargon without a plain-English translation in the same sentence.
- The pattern for every step: explain → confirm → act → verify → stop.
- No error dumps, ever. Name the problem simply, fix it together, or park it without blocking the rest.
- Keys never go into chat. Open `.env` in the editor, point to the empty line, and have them paste the value there themselves. Wait until they say it's saved. Never quote, print or repeat a key.
- Write `.activate-state` after each step, in this shape:

  ```
  format: 1
  name: <their first name>
  mode: template | standalone
  steps:
    0: done | pending
    1: done | pending
    2: done | skipped | pending
    3: done | pending
    4: done | pending
    5: done | skipped | pending
  lanes: <the lanes switched on>
  keys: <key names present in .env, never values>
  notes: <anything a resuming session needs>
  ```

  When Step 5 lands, add `complete: yes`.
- All prose follows plain-writing rules: contractions, short paragraphs, no em dashes, no AI vocabulary.
- If the workspace has a `ledger/` folder (Liam Ottley's template), append one row per step to `ledger/<name>.md`: `- YYYY-MM-DD HH:MM · <name> · workspace/build · Freelancer OS: <what landed>`.

---

## STEP 0, Detect (1 min)

Look, don't ask:
- Does `CLAUDE.md` exist and mention `/prime`? Does `context/offer.md` exist? Both yes: **template mode**. Read `context/offer.md`, `context/you.md` and, if present, `context/proof-bank.md`. Say in two lines what you learned ("You're a freelance copywriter for B2B software companies, working from Leeds. I'll only ask what the setup didn't cover.").
- Otherwise: **standalone mode**. Say so in one line and that the questions take about ten minutes.
- Does `config.yml` exist already? Read it; those answers are done.
- Is `python3` available (`python3 --version`)? Is `requests` installed (`python3 -c "import requests"`)? If not, offer `pip3 install -r requirements.txt` and run it on their yes. Is `node` available? Only needed for Word reports; note it and move on.

Write `.activate-state` with mode and name (ask the name if standalone and nothing on disk gives it).

---

## STEP 1, The interview (5 to 8 min)

Only what's missing. In template mode most of this comes from `context/`; confirm it in one line each rather than re-asking.

1. **What you sell, in one line.** ("WordPress sites and fixes for small businesses", "B2B email copy".) Goes in `config.yml` as `business_one_line` and, standalone, into `context/offer.md`.
2. **Who buys it.** Two or three kinds of client, with the problem each one has when they come looking.
3. **Where work comes from.** Job boards (which), Google Maps businesses, referrals, LinkedIn. This decides the lanes in Step 3.
4. **Proof.** Three to six links to work they can put their name to, with one line each on what they did and any number that came out of it (load time, enquiries, revenue, whatever they measured). Verb matters: built, fixed, sped up, worked on. If they have fewer than three, that's fine; the pack works with what's there and the proof bank grows as jobs ship.
5. **Their client voice.** Ask them to paste one message they've sent a client that sounds like them. Read it and write five to eight observed traits (sentence length, greeting style, how they soften a diagnosis, how they close, words they use, words they'd never use). Never copy the message itself into the file.
6. **Sender details.** Name as it should appear on emails, the email address they send client mail from, their portfolio or site URL. Optional: a path to a one-page resume to attach to cold emails.

Confirm each answer back in one line before writing anything. Then stop.

---

## STEP 2, Keys and connectors (2 to 5 min, only for lanes that need them)

Explain in one line what each one unlocks, then let them choose:

- **Gmail connector** (Claude app, Settings → Connectors). With it, cold emails land as drafts in their inbox. Without it, the email shows in chat for them to paste. Check whether it's connected by calling the Gmail tool to list drafts; if it's missing, say how to connect it and carry on.
- **PageSpeed Insights API key** (free from Google's console; needed for the Maps and SEO lanes). Give the sign-up page first on its own; when they confirm they're in, the key page. They paste it into `.env` as `PAGESPEED_API_KEY=`. Test: `python3 -c "import config; print(bool(config.get_key('PAGESPEED_API_KEY')))"` from `scripts/`.
- **Apify token** (free tier; needed for the Maps and SEO lanes). Same pattern, `APIFY_API_TOKEN=`.
- **Upwork connector** (Claude app) for pulling job links and the job-scout lane. Check with `list_accounts`; if it's missing, say how to connect it.

Skip anything they don't want; a skipped lane stays off in `config.yml`. Mark the step `skipped` if nothing was added.

---

## STEP 3, Wire it in (2 min)

Explain what's about to be written, confirm, then:

1. Write `config.yml` from `config.example.yml` with their answers. Lanes: `job_post: on` always; `job_scout` on only with the Upwork connector; `maps_scout` and `seo_scout` on only with both keys and if they sell to local businesses.
2. Create the folders from config: `leads/`, `clients/`, `runs/`.
3. Write `context/proof-bank.md` from `templates/context/proof-bank.md` with their proof rows, and `context/client-voice.md` from `templates/context/client-voice.md` with the observed traits. In template mode, only create these if missing; never overwrite a file that's already there.
4. Standalone only: write `context/offer.md` from `templates/context/offer.md`, and a minimal `CLAUDE.md` if none exists: who they are in two lines, the pack's three skills, the writing rule.
5. Append `templates/claude-md-section.md` to `CLAUDE.md` (skip if the marker line is already there).
6. Add the ignore lines from the pack's `.gitignore` to the workspace `.gitignore` if the workspace has git (`leads/`, `clients/`, `runs/`, `config.yml`, `.env`, `.activate-state`). Private data never gets committed.

Verify: read `config.yml` back and say what's on. Stop.

---

## STEP 4, The tour (1 min)

Three short paragraphs, one per skill, each ending with the phrase that triggers it:

- **Outreach.** Paste a job post and you get the research, a cold email in your voice and a lead file. "Follow up time" tells you who's due. Say: paste any job post.
- **Client delivery.** Paste a client message and the reply comes first. Say "milestone done" and the delivery kit arrives: two messages, a Word report, the ask for the next one. Say: paste a client message.
- **Proposals.** Paste a post you want to bid on and you get a letter with your proof woven in, a price with the reasoning, and the screening answers ready to paste. Say: "write a proposal for this".

Then: "Nothing sends or submits without your word."

---

## STEP 5, First win (3 to 10 min)

Offer one of these and run the one they pick:

(a) Paste a job post → the outreach skill, Mode A, start to finish.
(b) Paste a client message → the client-delivery skill, the reply first.
(c) If `maps_scout` is on: "maps scout <their niche> in <a city they sell into>" → the outreach skill, Mode E.

If they'd rather stop here, mark the step `skipped`; the pack is live either way.

Close with one line: the pack is on, where their files live (`leads/`, `clients/`), and that `/activate` can be run again any time to change lanes or keys. Mark `complete: yes`.
