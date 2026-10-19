# Freelancer OS

A Claude Code add-on pack for solo freelancers. It finds work, writes the cold email, wins the proposal, delivers the job and keeps the client. Five skills, one setup command, and the scripts behind them. You talk, Claude runs the process.

## Who this is for

One person selling their own work: web, copy, design, video, consulting, anything where you find clients, pitch them, deliver and get paid. It was built in a working web freelance practice and the web-specific parts (slow-site checks, local SEO audits) are switches you can leave off.

## Two ways to install

**1. On top of Liam Ottley's AI Makeover template (recommended).** The template gives Claude a full picture of your business and a daily rhythm; this pack plugs into that.

1. Watch the video: https://youtu.be/ulJqlCPNGKI
2. Download his template and run `/install` the way the video shows.
3. Download this repo and copy `.claude/`, `scripts/`, `templates/`, `config.example.yml` and `package.json` into your workspace folder. Existing folders merge; none of his files are overwritten (the pack's skills and command have their own names). Don't copy this repo's `.gitignore` or `requirements.txt` over his; `/activate` adds the ignore lines it needs, and the two Python packages (`requests`, `python-dotenv`) are already in his template.
4. Open the workspace in Claude Code and type `/activate`.

`/activate` reads what `/install` already learned about your business and only asks what is missing.

**2. On its own.** Download this repo, open the folder in Claude Code, type `/activate`. It explains what the pack does, asks about ten minutes of questions to personalise it, writes the few context files it needs, and offers a first job to run.

Either way, nothing sends an email or submits a proposal without your word.

## What you get

**Outreach.** Paste a job post or a job link. Claude works out the real business behind it, finds a verified email for the decision-maker, opens their site, writes a short cold email in your voice with one piece of proof, and saves a lead file. "Follow up time" reads the lead files and tells you who is due; follow-ups run a five-touch sequence with dates from a script, never from Claude's head. Optional lanes: Claude finding fresh job posts itself, a Google Maps lane that measures every site in a niche and city and pitches the slowest, and a local SEO lane that pitches the businesses that aren't ranking.

**Client delivery.** Paste a client message and the reply comes first, before any work starts. When a milestone is done, Claude hands over the delivery kit unasked: the pre-delivery message, the delivery message, a Word report, and the post-delivery message that asks for the next milestone. Every client gets an `upsells.md` and a `future-work.md` that fill up silently as the conversation goes. When a job wraps up, one open question asks what else they need. When a contract has run its course, the close message leaves the door open without a pitch.

**Auto-apply (optional, scheduled).** Every 20 minutes, Claude finds the fresh posts on your own Upwork account that fit your lanes, writes a full proposal for each by the proposals rules, notes the Connects cost, and saves them. Nothing is submitted until you say "submit the drafts". A Connects floor stops it when the balance can't carry the next one.

**Auto-reply (optional, scheduled).** Every 20 minutes, Claude reads the Upwork rooms you haven't opened and drafts a reply to each waiting client message from the thread and the client folder. Anything that needs a decision gets a holding draft and a line in a needs-you file. Nothing is sent until you say "send the drafts".

**Proposals.** Paste a post you want to bid on. Claude opens the client's site, names one real fault, writes a letter under 5,000 characters with at least three proof links woven into the points they back, prices against the real scope (including the case where the posted budget is a placeholder), formats the screening answers so they paste cleanly, and waits for your approval.

## What it needs

- Claude Code (the desktop app or CLI) on a paid Claude plan.
- Python 3.10 or newer for the scripts: `pip install -r requirements.txt`.
- Optional: the Gmail connector in the Claude app, so cold emails land as drafts in your inbox. Without it, the email shows in chat for you to paste.
- Optional: a free Google PageSpeed Insights API key and a free Apify account, for the Maps and SEO lanes.
- Optional: Node.js with `npm install`, for Word reports (`scripts/md2docx.js`).
- Optional: the Upwork connector, for pulling job links, the job-scout lane, auto-apply and auto-reply.

## Built on

This pack sits on top of Liam Ottley's AI Makeover workspace template (youtube.com/@LiamOttley). His template is not included here; get it from the video above. Everything in this repo was written for a working freelance practice and generalised so you can run it on yours.

## By

Daniel Dada, Dada Daniels. Web designer and developer, Top Rated on Upwork, building sites, web apps and event tech, and the AI systems that run the business around them. https://dadadaniels.vercel.app

## Licence

MIT. Use it, change it, ship it. Keep the copyright line.
