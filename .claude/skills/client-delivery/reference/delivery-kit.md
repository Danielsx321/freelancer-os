# The milestone delivery kit

When any milestone or contract is ready to deliver, produce all four pieces, without being asked, in the same response as "it's done and verified". Never offer it or ask permission for it.

## Before the kit: the pre-delivery checks

Run these first, and name what was checked in the delivery message:

- The work matches what the thread asked for (every promise and attachment, see `messages.md`, thread audit).
- Nothing else changed: styles against the original, the phone view, the cache cleared, forms and checkout still work, no server errors.
- The client can see it themselves without help (a link, a login, a before-and-after).

## The four pieces

**1. Pre-delivery message**, under 500 characters. Sent in the chat before the formal submission: the work is live, what changed in one line, how they can see it themselves, "submitting now with a report attached".

**2. Delivery message**, under 500 characters. Goes in the milestone submission: what was delivered, the same-look or no-risk reassurance, the checks done, a pointer to the report.

**3. The report**, a Word .docx with its .md source kept alongside. Sections, in order:
- Summary (three or four lines)
- Before and after (a table where there are numbers)
- What changed
- Where the changes live (pages, files, settings)
- Checks done
- How to undo
- Next milestone preview (what it fixes, what will be measured)

No name, no signature, no "prepared by". Generic greeting if any. Made with `node scripts/md2docx.js report.md report.docx`.

**4. Post-delivery message.** Value first (what the next milestone fixes, what will be measured), then the ask. If the next milestone is already part of an accepted contract, ask directly for it to be funded and say work starts the same day it is: "Once you fund Milestone 2, I'll start the same day." Never a soft "want me to start?", which gives the client time to drift. If the next step isn't agreed yet, ask for it once and lead with the value; after that, follow-ups carry value and easy questions, never the contract again.

**5. The review ask, last milestone only.** On the final milestone of a contract, the post-delivery message also asks once, in one easy line after the value, for a review on the platform when the contract closes. Once per contract, never chased. Nothing on mid-contract milestones.

## Format

Each message in its own fenced code block, with its character count beside it (count with `wc -m`). The report's .docx goes to the user as a file; the .md stays as the source.

## Example (invented client, invented job)

```
Pre-delivery (412 chars)

Hi Dana,

The new booking page is live at /book. It loads in under two seconds on a phone now and the form posts straight to your calendar.

You can try it from your phone: pick any slot, it will show on your calendar within a minute and you can delete the test.

Submitting the milestone now with a short report attached.
```

```
Post-delivery (388 chars)

Hi Dana,

Milestone 2 takes the same approach to the service pages: the three slowest get the same image and script fixes, and I'll measure each one before and after so you can see the change.

Once you fund Milestone 2, I'll start the same day. Shall I go ahead?
```
