# Stage 2: the opening message

## What this is

A job post is a lead source, not a place to bid. It proves the company has a defined problem, has decided to spend money on it, and is looking this week. That's warmer than any list-built prospect.

**Pasted means pitch.** The research stage has run and the user has already decided the lead is worth it. No assessment of the lead, no advice to drop it, no question about whether they can do the work.

**Sent as `sender_name`.** Their own name and identity. Never another account's reviews or history.

## Referencing the job

**Referable:** the work, and the fact that they're hiring for it. "I saw you're looking for help with the filters on your shop page" is right. A message that obviously comes from a hiring context but won't admit it reads evasive.

**Never referable:** the platform by name, and the trail: reviews, their timezone, attachment filenames, hiring history, spend, proposal counts, anything from the research. Naming it turns a well-timed email into surveillance.

That includes the sender's own credentials that name the platform. A "top rated" badge and job-count figures can't appear in a cold email. Use the proof instead; it's stronger anyway.

## The message, line by line

Short enough to read on a phone without scrolling twice. No subheadings, no numbered method, no service list.

**1. Their problem, named with its cause.** Echo their words in quotes, and in the same line or the next, name the mechanism: the setting, rule, tool behaviour or platform limit behind it. This is what separates the sender from the fifty people who applied. Use one of three shapes:

- **Reframe:** their framing misses the cause. ("The 'slow checkout' is most often the payment plugin loading its script on every page, not the checkout itself.")
- **Link:** two symptoms they listed but haven't connected.
- **Constraint:** they diagnosed it right, so name the trap in their plan instead.

How sure that line sounds depends on the lead file's `Site` section:

- **Inspected: Yes** and the page is confirmed as the one the job concerns: name what's happening on the page, specifically. The strongest version.
- **Inspected: No:** a pattern observation, framed as what usually causes it ("Most of the time, this comes down to..."). Never a specific fault on a page nobody saw.
- **Neither can be written honestly**, or the inspected site isn't confirmed as theirs: a short diagnostic question in that slot instead.

Diagnosis and question are alternatives, never both. Where two observations were recorded, **spend one, hold the other** for touch 2.

**2. What it costs if it's missed, in their terms** (optional, one line). Lost enquiries, a failed audit date, orders dropping at checkout. Only if the post supports it.

**3. One proof, with its link, inline.** Two links in the whole opening at most: the proof site inline, and the portfolio in the sign-off. In a cold email from a new sender, every extra link raises the spam score and splits attention. The proof sits inside the point it backs, wherever that is, and reads as part of the sentence: "Your homepage takes 11 seconds to show its main photo on a phone, the same thing https://example-client.com was doing before I took it to 2.6." No separate proof line tacked on. Prefer a **client site** as the inline proof when one matches the problem; use your own site only when it's the closest match. The claim must match `context/proof-bank.md` in substance, with the verb it allows (built / fixed / sped up / worked on). Never more than one proof; a second dilutes the first.

**4. One small ask.** Either/or, the kind only someone who understood the job could ask: *"Is the filter slow for every location, or only once a product sits in two?"* or *"Would it help more to start with the checkout or the product pages?"* A reply, not a meeting for the whole engagement.

**Before handing over, two checks:**
- **The core requirement is touched.** Whatever the post calls the backbone or the daily work (a tool, a platform, a format) gets one line, even without a named project behind it: say what the sender does with it in plain capability terms, never as a shipped result. An email that answers the side issue and skips the core reads like someone who skimmed.
- **Hard constraints are answered in a clause.** Timezone overlap, start date, a required tool or hours: if the post makes it a must, one short clause removes the doubt. Availability isn't a timeline, so it's allowed.

Both fit inside the length limit; cut elsewhere if needed.

**5. Sign-off.**

```
Best regards,
<sender_name>
<a title that matches this job, e.g. "WordPress Developer & Elementor Expert" or "B2B Email Copywriter">
<portfolio_url, or the case-study page that matches the proof if you have one>
```

The title line matches the kind of work the post is about, not a generic label. Check the link loads before a batch.

## The subject line

Written once, it carries all five touches: every follow-up replies in the same thread, so the client sees it again a month later. The problem in their words, short, still accurate on day 31. No "quick question", no dates, no urgency that expires. Recorded in the lead file and never rewritten.

## Proof matching

Match the client's **problem** to a problem already solved, not their industry. **Choose two, spend one.** The closest goes in the opening; the next-best for the same problem type is recorded as the reserve, spent only at touch 3. If there's only one strong entry, the reserve is `Empty`; don't reach for a weaker one.

Source of truth: `context/proof-bank.md` (live sites, results, allowed verbs). It grows every time a job ships, so read it every run. Build your own problem-to-proof table there as patterns repeat; a few rows of "when they say X, lead with Y" save time on every batch.

**Signals to answer directly:** a previous freelancer vanished (an inherited-work proof); a deadline or compliance date (a proof with a dated outcome); an agency needing capacity (a maintenance or volume record).

## SEO scout email (Mode F)

The owner never posted a job, so the email has to be worth reading on its own: it gives away the reason they are not ranking and asks one yes/no question. Everything else in this file (voice, one proof inline, banned wording, no price, no timeline, no service list) still applies. Where this section differs, it wins for Mode F.

**Order, four short paragraphs, 70 to 110 words:**
1. Where they came up, as something they can check in ten seconds: "I searched 'fence company Charlotte' on Google Maps this week and Oak Ridge Fence came up around 23rd." When the Maps position is fine but they are missing from Google: "...you are not on the first two pages of Google for it."
2. The reason, in plain words, one sentence: "Your homepage is telling Google not to list it." / "The phone number on your site is not the one on your Google listing, so Google is not sure they are the same business."
3. What fixing it does, with the one proof inside that sentence.
4. The offer, yes/no: "I noted two other things holding the site back. Want me to send them over?"

**Close:** the yes/no offer above, worded fresh each time ("Shall I send the other two?", "Would a short list of the other two help?"). Never "now", never "let me know".

**Subject:** the business name plus one plain fact, lower case allowed, no question marks or hype: "Oak Ridge Fence on Google Maps", "your Google listing vs your site".

**No attachment.** The free list is the reason to reply.

**Plain words only.** Never in the email: SEO audit, schema, NAP, canonical, noindex, SERP, rank tracker, keywords, algorithm, Core Web Vitals, PageSpeed, Lighthouse. Translations:
- noindex: "your homepage tells Google not to list it"
- canonical to another domain: "your site tells Google its real address is <other site>"
- robots.txt blocking: "a settings file on your site tells search engines to stay away"
- unclaimed profile: "nobody has claimed your Google listing, so anyone can suggest changes to it"
- NAP mismatch: "the phone number on your site is not the one on your Google listing"
- no what/where: "your homepage title just says 'Home', so Google has nothing telling it you are a <service> in <town>"
- one page: "the whole business sits on one page, so there is nothing for Google to show when someone searches for <one service>"
- no schema / no address: "nothing on the site tells Google where you are"
- reviews gap: "the five businesses above you have about <n> reviews each; you have <m>"

**Example (fictional business, never sent):**

```
Subject: Oak Ridge Fence on Google Maps

Hi Mark,

I searched "fence company Charlotte" on Google Maps this week and Oak Ridge Fence came up around 23rd.

Looking at why, your homepage title just says "Home", so Google has nothing telling it you build fences in Charlotte. It is a small change, the same kind I made on https://example-fence-client.com, where I rewrote the page titles and headings around their three main services.

I noted two other things holding the site back. Shall I send them over?

Best regards,
Sam Carter
Local SEO & WordPress Specialist
https://samcarter.example
```

## Attachment

If `resume_path` is set in `config.yml`, the resume goes on the opening message only, never again in the sequence. Mode F never attaches it on the first email. Name it after the message with a one-line reason.

## Voice

The user's client voice, from `context/client-voice.md`, never the chat register. Plain verbs. They are the actor in every step. Their prospect's words echoed in quotes. Diagnosis softened ("Most of the time, it is..."). A concrete tail ("on the website", "exactly as it stands right now"). Diplomatic, not deferential. One idea per paragraph.

## Never in an opening message

Price or timeline. A service list. A numbered method. Years of experience. More than one proof. The platform by name, or anything from the research trail. Credentials that name the platform. Anything in the proof bank's do-not-claim list.

**Banned wording, checked before handing over:** honest, honestly, to be honest, upfront, transparency; "I came across"; "I hope this finds you well"; "passionate"; "perfect fit"; any sentence announcing a gap; em dashes (semicolons instead); the AI vocabulary list (delve, leverage, seamless, robust, elevate, streamline, unlock, empower, and their relatives).

## Do not claim

Keep a short list in `context/proof-bank.md` under "Do not claim": own concepts that never shipped, features not tied to a named project, tools you've only read about, years-of-experience framing, and any result that belongs to someone else's account. Check it before every message.

## Output

1. **Subject line**, in its own code block
2. **Email body**, ready to send, in its own code block
3. **Attachment**, named, one line why (only if configured)
4. **LinkedIn note** (under 300 characters, own code block), only when the research shows LinkedIn as the verified or primary channel. It doesn't register LinkedIn as a follow-up route
5. One sentence for each gap that affected the message, if any; the message is still written, using the safer version
6. The lead file path, written in full (see `lead-file.md`). The file is saved to disk, never printed in chat

## Field notes

What the sends taught you. Add a dated line whenever a batch shows something: which openings got replies, which got none, what bounced, what to retire. Read the last few before writing a new batch so no opening repeats and nothing retired comes back.
