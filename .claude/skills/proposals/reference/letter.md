# The letter

## Shape

Short paragraphs of one to three sentences, a blank line between each. No headings, no bullet lists in the letter, no greeting longer than "Hi <name>," (or none if no name).

**1. Opening line: the core requirement plus one thing seen.** The first sentence touches what the post is about, in their words, and names one real thing from their own site or brief. "Your product filters reload the whole page on every click, which is the ajax setting in the theme's shop template, not the filter plugin." The comparison to a client site where the same fault was fixed can sit in this line when it fits.

**2. Diagnosis before plan.** One short paragraph on the cause, in plain words. Reframe it if their framing misses the cause; link two symptoms they listed separately; or name the trap in a plan they've already decided on.

**3. The plan.** Three to five numbered steps at most, each one line, each saying what the client gets. No method lecture. Where a step matches a proof, the link goes in that step's line.

**4. Must-haves answered.** Timezone overlap, start date, tools, hours, anything the post made a condition: one clause each, early, so the reader stops wondering. Availability is allowed; a delivery timeline is only promised when the user set one.

**5. The price line.** Per `pricing.md`. A number and what it covers, or milestones with a number each. No apology, no comment on their budget.

**6. Sign-off.** One easy, fast-to-answer question tied to the outcome the buyer wants from the job (no time or day in it), then exactly three lines:

```
<a title written for this job, e.g. "Website Security Specialist" or "Product Launch Copywriter">
<portfolio_url>
<sender_name>
```

The title names the job's own specialism, so the letter reads as from someone who does exactly this. Never a generic "Freelancer".

## Proof links, woven in

Minimum three links per letter, no maximum. Each one sits inside the point it backs and reads as part of the sentence: "Your site is serving spam posts the same way https://example-client.com was before I audited it and cleaned it out." Never a separate "similar work" block, never a list of links, never the same link twice.

Where the letter has fewer than three points with a matching site, find more angles in the job (a plan step, the price line, the close) rather than dropping below three. Live client sites beat case-study pages on your own site; use a case-study page only for work with no public URL, and at most one per letter.

Every claim matches `context/proof-bank.md` in substance and verb (built / fixed / sped up / worked on). A "top rated" badge or job counts from the platform may appear in a proposal (the client is on the platform), but the proof is stronger; use it.

## Length

Under 5,000 characters, the platform's field limit; aim for 3,000 to 4,000. Count with `wc -m` before showing it and print the count beside the block. The sign-off counts.

## Reading between the lines

- A post that lists symptoms without a cause wants the cause named.
- A post that names a cause wants the trap in the fix named.
- A post with a tight budget and a wide scope is either a real small job or a placeholder budget; `pricing.md` decides.
- A post that says "the last developer disappeared" wants reliability shown, not promised: a repeat-client proof.
- A post with a deadline wants the deadline acknowledged and a first step that lands before it.

## Banned wording, checked before showing

honest, honestly, to be honest, upfront, transparency; "I came across"; "I hope this finds you well"; "passionate"; "perfect fit"; "I have X years of experience"; "I am confident"; any sentence announcing a gap; em dashes; the AI vocabulary (delve, leverage, seamless, robust, elevate, streamline, unlock, empower, cutting-edge, tailored, comprehensive, and their relatives); "I'd love to"; "feel free"; "let me know".

## Example skeleton (invented job, invented proof)

```
Hi Dana,

Your booking page takes about nine seconds to show the calendar on a phone, and the cause is the three slider images loading at full size before anything else, the same thing https://example-venue.com was doing before I took it to under three seconds.

The booking plugin itself is fine; it's waiting on the images. Swapping the slider for one compressed hero and loading the calendar script first fixes it without touching the booking setup.

1. Measure the page as it stands and send you the numbers.
2. Compress and lazy-load the hero images, as on https://example-client-two.com.
3. Move the calendar script ahead of the theme scripts.
4. Re-measure and send a before-and-after, the same report format I used for https://example-client-three.com.

I'm available from Monday and overlap your afternoon (Eastern) through my working day.

$450 fixed, in two milestones: $150 for the measurement and image work, $300 for the script order and final report.

Would you rather I start with the booking page or the homepage?

Website Performance Specialist
https://your-portfolio.example
Sam Carter
```
