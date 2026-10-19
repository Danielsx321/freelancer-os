# The client folder

Every client, new or existing, gets `<clients_dir>/<slug>/` (slug: lower-case business or person name, hyphens). Created on the first message, kept for the life of the relationship. It is git-ignored; it never leaves the machine.

```
clients/northwind-bakery/
  notes.md          what the job is, access details, decisions, dates
  upsells.md        angles we noticed, not asked for
  future-work.md    work the client said they want later, and hire-out mentions
  reports/          .md and .docx per milestone
```

## upsells.md

Whenever a conversation, a pasted message or work on their site shows an angle they haven't asked for (something broken you noticed, something missing, something that would lift a number), add it. Don't announce it or ask; just stack it.

Each entry: date, what, where you saw it, rough size if obvious.

```
- 2026-10-09 · Product pages have no reviews block; theme supports one · seen on /shop · small
```

## future-work.md

Whenever the client themselves mentions something for later ("after this I also want...", "can you help with X next", "once this is done..."), add it with the date and their words in a short quote. This is work the client asked for, not something you spotted. If the client asked for it, it goes here even if you'd also noticed it; never duplicate between the two files.

Hire-out mentions go here too, tagged: when the client says they need or will hire someone for anything, web or not.

```
- 2026-10-12 · "once the shop is sorted I want a proper email list" · from their message
- 2026-10-14 · hire-out mention · "we need someone for the Google ads" · offer drafted, sent 14 Oct
```

## The three steps with every buyer

1. **During the work: hire-out mentions.** The moment a buyer says they need someone for anything, note it in `future-work.md` and give the user a drafted line offering to take it on, in the same response. If the need is outside what the user has done hands-on, bring it to them before the reply promises anything.

2. **At each delivery: the specific upsell.** Pitch the strongest entry from `upsells.md` in the post-delivery message, value first, one easy question. One per message.

3. **At wrap-up: the open ask.** When the job is wrapping up and the upsells were pitched and declined (or there are none) and the future work was taken up or turned down: the wrap-up message includes one open question, value first, along the lines of "Is there anything else in the business you need a hand with, even outside the website?" Record the answer in `future-work.md`.

Order: upsell, then the future work they named, then the open ask. One at a time, never stacked in one message. Ask once per contract. Skip the open ask on a thread in dispute or where the client is unhappy.

## notes.md

The job in two lines, access details the user shares (never passwords in chat; point to where they are kept), decisions with dates, what's promised and what's delivered. Read it before every reply.
