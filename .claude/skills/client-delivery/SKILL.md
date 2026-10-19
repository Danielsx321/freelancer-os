---
name: client-delivery
description: >
  The client process from first reply to contract close. Use whenever the user pastes a client
  message (any platform or email), says a milestone or job is done or ready to deliver, asks for a
  report, says "end this contract", "what else can I sell them", "write the feedback", or asks what
  to say to a client. Covers: reply first then work, the milestone delivery kit (pre-delivery
  message, delivery message, Word report, post-delivery ask), per-client upsells.md and
  future-work.md, the other-needs ask, the closing-question rule, the contract close message and
  the client feedback text. Not for cold outreach (outreach skill) or proposals (proposals skill).
---

# Client delivery

The user talks to clients; Claude runs the process behind every message. Every rule here came from real jobs where the softer version lost time or money.

**Files**
- `reference/delivery-kit.md`: the four-piece kit for every milestone, the review ask, the pre-delivery checks
- `reference/messages.md`: reply-first, draft-after-edits, the closing question, the close message, feedback text, the thread audit
- `reference/client-folder.md`: `<clients_dir>/<slug>/` with `upsells.md`, `future-work.md`, `notes.md`; the other-needs ask

**Before anything:** read `config.yml`, `context/client-voice.md` and `context/proof-bank.md`. Open the client's folder if one exists; create it on the first message from a new client (`reference/client-folder.md`).

## On every pasted client message, in this order

1. **Reply first if the reply doesn't depend on the work.** An acknowledgement, confirming terms, answering a question, "starting now": the draft reply is the first thing in the response, in a code block, before any work starts. Then do the work.
2. **Hold a reply that reports finished work until every edit is done and verified.** No draft in progress updates. Finish, check, then one final reply.
3. **Stack silently.** Anything they hint at that they haven't asked for goes in `upsells.md`. Anything they say they want later goes in `future-work.md` with the date and their words. Don't announce it; show it when asked or when pitching.
4. **Hire-out mentions.** When they say they need, or will hire someone for, anything ("we'll need someone for our ads", "I have to find a designer"), note it in `future-work.md` tagged `hire-out mention` and give the user a drafted line offering to take it on, in the same response. It does not have to be the user's main service. Never promise a skill the user hasn't used hands-on; ask them first.
5. **Audit the thread before building and before delivering.** Before building from a client's document, check the thread for a later version. Before calling a milestone done, walk the whole thread for every promise and attachment and list promise vs live status.
6. **Closing question only when converting.** A message ends with one easy yes/no question only when the user is trying to convert: a prospect who hasn't hired, a follow-up, an upsell or future-work pitch, the post-delivery ask for the next milestone or a review. Working replies on an active job (status updates, answers, deliveries) end naturally; a question goes in only when there is something real to ask. When a closing question is used: no time or day in it, never "whenever you're ready", "just say" or "let me know", never "now" to a prospect who hasn't hired.
7. **Count and box.** Every client message goes in its own fenced code block with its character count (`wc -m`) beside it. Platform message fields often cap at 500 characters; the delivery kit messages always fit.
8. **Plain punctuation.** Commas, full stops, semicolons. No em dashes. The user's client voice from `context/client-voice.md`, never the chat register.

## When work is done

The moment a milestone or contract is verified, hand over the full delivery kit in the same response without being asked. Never "want me to write the kit?". See `reference/delivery-kit.md`.

## When a job wraps up

Order with every buyer: the specific upsell first, then the future work they named, then the open ask ("Is there anything else in the business you need a hand with, even outside the website?"). One at a time, never stacked in one message. Once per contract. See `reference/client-folder.md`.

## When a contract has run its course

"Let's end this contract" means the nudges went unanswered and nothing else is coming, not that the next milestone is starting. If it's unclear which they mean, ask. The close message in `reference/messages.md`: acknowledge, the work does its job, one low-effort offer, no pitch.

## Reports

Every client-facing report (milestone report, audit, handover) is a Word .docx made from a Markdown source: write the .md, then `node scripts/md2docx.js report.md report.docx`. No name, no signature, no "prepared by" line. Never a PDF or an HTML page. Save both next to the client's files.

## Ledger

If the workspace has a `ledger/` folder, write a row when a milestone ships (`<client>/ship`) and when a decision is made. No amounts in the ledger.
