# Stage 1: identify the client behind the post

**Core principle:** this is an identity investigation, not a search. One query and a matching name is not an identification.

## Tools, in the order to reach for them

| Need | Tool |
|---|---|
| The post itself, client history (payment verified, spend, hires, reviews given), proposal count | If the user pastes a job link and the Upwork connector is connected, pull it (`get_job_posting`). If they paste text, use the text; don't go looking for the link |
| Web search, exact-phrase search, company sites, press, directories | A Firecrawl skill if the workspace has one; otherwise Claude's built-in web search and fetch |
| LinkedIn, Instagram, Facebook profiles | Web search on the platform domain first (`site:linkedin.com/in "Full Name" company`); an Apify actor only if a token is configured and that fails, and keep pulls small |
| Opening the site the job concerns | A fetch for content; a browser tab for what the page actually does (filters, forms, layout, console errors) |
| Speed jobs | PageSpeed Insights on the page named in the post (the public page, or the API if a key is configured) |

**Budget:** about 6 pages per lead. Past that, grade what you have.

## Step 0: the red-flag scan (before anything else)

Read the whole post, including screening questions and attachment text, for any sign the client doesn't want to be contacted outside the platform. The user may have missed it; this scan is the safety net. Examples, in any wording:

- "Do not contact me outside the platform", "communicate only through here", "all contact through the platform"
- "Do not email / call / message me", "don't DM me on LinkedIn", "no outside links or contact details"
- "Applicants who contact us directly will be disqualified / reported / blocked"
- Anything saying they will report off-platform contact

**If one is found: stop.** Don't run the duplicate check or open any page. Return only this, then wait:

```
RED FLAG: the client asks not to be contacted outside the platform.
"<the exact line from the post>"
Pitching this one directly risks a report on your account. Skip it, or bid on it through the platform instead?
```

Only a clear yes in chat continues the research, and the lead file then records the flag in Notes. A softer signal ("we prefer to keep everything on the platform") gets the same stop.

## Before researching: the duplicate check

Run `python3 scripts/leads_tool.py check "<company>" "<domain>" "<distinctive phrase>"`. A match means this company is already in the pipeline: re-open that file instead of making a new one. Its research is already done; the new post is the reason for the new message, and nothing about the old sequence is mentioned.

## Method

### 1. Extract clues from the post
Company name, location, industry, project or product name, URLs, brands, tools and platforms, people named, budget, timeline, client history, any deadline, event date or compliance date, and distinctive phrasing. **Distinctive phrasing matters most**: clients paste from their own site or brief, so an exact-phrase search is often the fastest route.

**Read the client's review history first.** A post copied from the platform page carries the client's past contracts and the feedback freelancers left. Those reviews routinely name the contact ("Thanks Sarah"), the company, the site or the product, and past job titles reveal the business ("Shopify store for XYZ Candles"). Mine every review and past contract title before any web search; it is usually the shortest route to the identification.

### 2. Search in combinations, never one broad query
At minimum: the exact phrase alone in quotes; the phrase plus industry or location; the project name plus organiser or founder; the company name plus LinkedIn. Narrow on what each pass returns.

### 3. Company before person
`job post → company → website → people behind it`. Never `job post → a person with a matching name`. Check About, Team and Contact pages, press, directories, event listings.

### 4. The decision-maker
The person tied to this project, not just to the company: founder, CEO, marketing or operations lead, project manager, web lead. Don't list the staff roster.

**Agency posts** ("our client", a services company as the poster, a site that doesn't match the company): record both, agency first. The agency hires and pays, so it's the contact. The end client is context only. Never approach the end client's founder; they didn't post it and going around the agency ends the opportunity.

### 5. Verify across independent sources
LinkedIn, the company site, Facebook, Instagram, X, plus whatever fits the industry (Crunchbase, Clutch, event directories, press, GitHub). A matching handle proves nothing on its own.

### 6. The email (the deliverable)
Everything above exists so you know whose address to look for. Run all the steps; stopping early is the failure this section exists to prevent.

**Personal inbox first, business address only as a fallback.** Most owners do not check their web mailbox; they live in Gmail. So the search target is the decision-maker's personal address (@gmail.com, @hotmail.com, @yahoo.com, @outlook.com, @icloud.com and the like), and the research is not finished until it has been looked for properly. Where to look, in order:
1. Their own site: contact, about, team, footer, privacy and terms pages, PDF flyers, vendor and press packs, older pages in the Wayback Machine (small businesses often started on a Gmail address and left it in the footer or the privacy policy).
2. Their social profiles: Facebook page About section and the "email" button, Instagram bio and the email button, LinkedIn contact info, event organizer pages, Etsy, Nextdoor, Yelp owner replies, YouTube channel About.
3. Public records and listings: domain registration history (historic WHOIS), state or national business filings, nonprofit filings, permit and licence records, event listings, press releases, podcast and interview bios, GoFundMe or Patreon pages.
4. Exact-phrase searches: `"Full Name" "@gmail.com"`, `"Full Name" gmail`, `"business name" "@gmail.com"`, and the same for hotmail, yahoo and outlook.

A personal address counts when a public page ties it to the person or the business by name, or when an unmasked snippet is backed by a second signal (same handle on another profile under the same name and city). Record the page it was found on.

**When no personal address turns up**, a business address may be used only when it is shown to be alive: it appears on the current site (not just an archived page) AND at least one of these holds: it is named in a dated post, listing, press item or event page from the last 12 months; a named person is attached to it on the site; a recent review or reply refers to contact by email. Record which signal proved it in the lead file's Email status line as `Business, active: <signal>`. A business address with no life signal is `Business, unproven`: write the message, send it only with a one-line warning after the message, and keep looking for the personal one in follow-up research.

Never guess a personal address from a pattern. Never use a masked aggregator (ZoomInfo, RocketReach, Apollo, ContactOut) as a source; an unmasked fragment can corroborate, and a masked hit means an address exists, so keep looking. A contact form is not an exhausted search.

Order of preference once found: (1) the personal inbox, (2) the person's own named work address shown to be active, (3) a shared mailbox shown to be active. State the pick and its status in one line, and record any other address in the lead file's Notes as the fallback if the first bounces.

| Status | Meaning |
|---|---|
| Personal, verified | A personal inbox tied to the person or business by a public page; the page is named |
| Verified | A named work address published on an official source and tied to the person |
| Business, active | No personal address found after the full search; business address on the current site plus a life signal from the last 12 months, named |
| Business, unproven | No personal address found; business address with no life signal. Send only with a warning line |
| Publicly listed | Third-party source, not independently confirmed |
| Pattern guess | Inferred from a naming convention. Never presented as confirmed |
| Not found | Every step above actually run. Record the queries in the Research section |

### 7. Contact type
Named personal (one person), Shared mailbox (hello@, info@), or Form only. This sets the touch budget, so record it explicitly.

### 8. Open the site
Open the page the job concerns. Record what was actually seen, in a line or two each; record a second thing if there is one, because touch 2 spends it. Name what is visibly wrong or visibly present; this is not an audit.

"Not inspected" is a valid answer (unreachable, behind a login, no page named) and produces a safer message. Never write "Inspected: Yes" unless the page was opened, and never describe the job post in that field. If you can't confirm the site you opened is the site the job concerns, say so: that forces a question in the opening instead of a diagnosis.

Every observation must be visible on the rendered page (a browser tab or rendered markdown), never taken from raw HTML, an HTML comment or a hidden element. A wrong observation costs the lead and the reputation; when in doubt, use the next one or skip.

### 9. Grade honestly
| Grade | Threshold |
|---|---|
| Strong | Name, company, location and project corroborate across two or more independent sources |
| Probable | Most signals align; one key link unconfirmed. Name the link |
| Not found | One line. Fill what the post supports and say the entry rests on the post alone |

Never upgrade a weak match. A false positive costs a wasted approach and a damaged first impression.

## Output: the research block

Shown in chat, and saved in full into the lead file's Research section with a source URL on every fact.

```
Ref:               Company + month, e.g. Northwind Bakery Oct 2026
Job:
Sourced:           date found, age of the post, proposal count
Identified:        Yes / No
Email (+ status):
Contact type:      Named personal / Shared mailbox / Form only
Posted by:         Direct client / Agency on behalf of a client
Person / Role:
Company:
End client:        (agency posts only)
Website:
Site inspected:    Yes / No; if yes, what was seen
Urgency signal:    deadline, event date, compliance date, or none stated
LinkedIn:
Facebook:
Instagram:
X:
Other:
Confidence:        Strong / Probable / Not found
Open doubt:        one line, or none
Evidence:          what corroborates, and what is still missing
Best outreach route:
```

Then **Notes for outreach**, facts only, no recommendation: competition (proposals, post age, last viewed), budget stated and the client's historical average rate, client history (payment verified, hires, spend, reviews given), contact risk, brief specificity, which service in `context/offer.md` it falls under (and which problem the client leads with if it spans two), any warning sign.

**Outside your services** (a platform or kind of work `context/offer.md` doesn't cover): say so in Notes as a fact. Check `context/proof-bank.md` before calling it uncovered.

## Before handing over, three questions
1. Did I pin down who posted this job, or only a plausible company? If the second, the entry says so.
2. If the email is "Not found", did I run step 6 in full, or check the site and stop?
3. Does "Site inspected" say what was seen, or does it say yes and then describe the post?
