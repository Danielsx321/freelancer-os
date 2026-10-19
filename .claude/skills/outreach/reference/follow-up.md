# Stage 3: follow-ups

Voice, proof matching, do-not-claim, banned wording and the sign-off are in `outreach.md` and apply in full.

## What this is

The opening email is the first of five, and most replies don't come from the first. A follow-up isn't a reminder; it's one more thing worth saying about the same problem. If a message has nothing new in it, it doesn't go out. Everything a follow-up says was recorded in the lead file at research time; nothing is invented on the day.

**Never write a follow-up without reading that lead's file first.** If the file is missing, say so and stop.

## Standing rules

- **Named means write.** No assessment of whether the lead is still worth it.
- **Reply in the thread.** No subject line; the thread carries it.
- **The attachment went with the opening.** Never again.
- **No price, no timeline.**
- **The portfolio link closes every message.** Same link as the opening.
- **Sent as `sender_name`.**
- **Plain punctuation.** Semicolons and commas, no em dashes.
- **Two proofs across the whole sequence, never two in one message.** The opening spent one; touch 3 spends the reserve.
- **No breakup email.** Touch 5 does that job without the theatre.
- **No opt-out line.** Don't add one.

## "Follow up time"

1. If Gmail is connected, search it for replies from each running lead's address since its last send, record any with `state`, then run `python3 scripts/leads_tool.py review`.
2. **Open check, if your mail tool shows opens.** A running lead with 4 or more opens gets its next touch now, even if the script says not due. Ignore anyone who already replied, live conversations, and opens within minutes of sending (security scanners and image proxies fire one open straight away). Clicks are a weaker signal than they look: several clicks with one open is a link scanner, not a person. Opens are a hint, not interest.
3. Return the script's list exactly (Due now, Not due, Needs a decision, Drafted but not sent), then a short **Opened 4+** list if there is one. Don't recount or re-date anything.
4. Stop. The user names which to write. Due now plus Opened 4+ is the default set.

"Drafted, not sent" is new: a message was written and nobody said it went out. Ask whether it went, and don't write the next touch on top of it.

## Writing a named follow-up

1. Read the whole lead file, in the order in `lead-file.md`. If it has a `Job URL` and the Upwork connector is connected, re-read the post: if it's closed or shows a hire, don't write the touch; say so and suggest `Dead: hired someone` (or touch 4's question if it's unclear).
2. Write the touch the script said is next.
3. Update the file: append the log row dated `pending`, move the spent reserve line to spent (reserve becomes `Empty`), add the message under `## Messages`, set `State: Drafted`.
4. Return the message in a code block, then the file path. When they say it went: `python3 scripts/leads_tool.py sent <slug>`.

## The sequence

| Touch | Day | Carries |
|---|---|---|
| 1 | 0 | The opening (`outreach.md`) |
| 2 | 2 | The second site observation |
| 3 | 7 | The reserve proof |
| 4 | 17 | Whether they still need it done |
| 5 | 31 | The A/B/C reply |

The ask shrinks each time: an observation, then proof, then a yes or no, then a single letter. A touch sent late keeps its place; the script counts gaps from the actual send date.

**Touch 2: the second observation.** Three or four lines. Spend the site reserve, specifically, because it was actually seen. If the file says `Not inspected` or the reserve is `Empty`, ask a **real diagnostic question** instead: which builder the template runs on, whether the errors started after an update, whether there's a staging copy. Observation or question, never both.

SEO-scout leads (Mode F): touch 2 gives `## Audit notes` item 1 away in two sentences (the finding and what fixing it does) and asks the same kind of yes/no question; never repeat the reason from touch 1.

**Touch 3: the reserve proof.** The only place it can be spent. Named, linked, the same inline shape as the opening. If the reserve is `Empty`, ask a diagnostic question and leave the proof unspent.

**Touch 4: still needed?** The whole message is the question, using the problem in the words from touch 1 (it's in `## Messages`). *"Is the checkout still giving you trouble, or has that been sorted?"* *"Did you end up finding someone for it? If it's covered, no problem at all."* A reply saying they hired someone is a good outcome.

**Touch 5: A/B/C.** Readable in ten seconds. Say plainly they're busy and this is quick, then three letters adapted to the job: A, not a priority right now; B, went with someone else; C, still meaning to get to it. No guilt, no "last email", no door closing.

## Budget by contact type

Named personal 5 touches. Shared mailbox 4 (drops touch 3; the reserve proof is the most expendable). Form only 2 (the opening, then touch 4's question). The script applies this.

## Second channel

Email carries the sequence. A second channel exists only where research found Instagram or Facebook; LinkedIn isn't a follow-up route. Use it only when the email bounced, or when the file has an Open doubt about the contact and two email touches went unanswered (the script flags this at touch 3). A second-channel message is shorter still: the work, and a way to reach you, the portfolio link only. Never both channels in one touch.

## Referencing the hiring, again

By touch 4 there's an unspoken question about why you're still writing. Don't answer it by explaining. They have a problem, and it looks like it's still there. The platform and the trail stay unmentioned, however long the sequence runs.

## Tone

Shorter each time. Never wounded: no "I haven't heard back", no "I know you're busy but", no counting previous emails. Silence is normal and gets treated as normal.

## When a lead ends

| State | When |
|---|---|
| Replied: live | Any reply that keeps the conversation going. Outreach stops; it's a conversation now |
| Replied: no | Not interested. Record why in Notes |
| Dead: hired someone | From a reply, or the post visibly closed |
| Dead: bounced | Dead address, no second channel |
| Dead: no response | Budget spent (the review list puts these under Needs a decision first) |
| Parked: revisit YYYY-MM-DD | Hired someone cheap; worth one revisit in three to six months. The user's call |
| Stale, not sent | A draft went past its stale date without going out |

Set with `python3 scripts/leads_tool.py state <slug> "<State>"`. A lead that dies of silence isn't finished: when the company posts again, re-open the same file. The new post is the reason for the new message, and the old sequence is never mentioned.

## Never in a follow-up

Price or timeline. A second proof in one message, or any proof after touch 3. The platform, or the trail. A count of emails, or any mention of not hearing back. "Final email". A re-attached resume. A service list. A subheading.
