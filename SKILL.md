---
name: jobsnatcher
description: Finds open jobs that match a person's résumé across public job boards, confirms each posting is still live, scores fit, and builds a clean application tracker plus a résumé keyword-gap report. Use when someone asks to find jobs, build a job list, or tailor their résumé to job postings.
---

# JobSnatcher

JobSnatcher snatches open job listings that fit a person's résumé, checks that every one is still accepting applications, ranks them by fit, and assembles them into a clean tracker. It can also read the postings to show which words employers use that the résumé is missing.

Rule that never bends: **every row must be a live posting the person can apply to directly.** A closed or unverifiable posting is left out or clearly marked, never presented as open.

## Step 1: Intake (ask everything in one message, then work without interrupting)

Ask these together, in plain language. Mark which are optional and say what the default is. If the person already gave an answer earlier in the conversation, don't ask again.

**Required**
1. **Target roles:** job titles and level (e.g. "Senior Product Manager, Group PM").
2. **Industry or sector:** e.g. AI, fintech, healthcare, climate, or "open to any".
3. **Location rules:** remote only / specific cities / hybrid OK. Include country if not US.
4. **Résumé:** ask them to upload it (PDF or Word), paste it, or share a link.

**Optional (use the default if they skip it)**
5. **Companies already applied to:** a list or a tracker link. Default: none excluded.
6. **Salary floor.** Default: none.
7. **Company stage:** startup / growth / public / any. Default: any.
8. **How many roles they want.** Default: 50.
9. **Where results go:** a spreadsheet in this app, a Google Sheet, or an Excel/CSV file. Default: the best spreadsheet option available in this session (see Step 6).
10. **Keyword-gap report:** yes/no. Default: yes.
11. **Include LinkedIn?** yes/no. Default: yes if a browser is connected. Tell them in one line: "LinkedIn's terms restrict automated tools. If you opt in, I'll run a few searches in your own signed-in browser at a normal pace and only read the results. I won't apply, message or change anything."

After they answer, read the résumé in full. Extract: current level, years of experience, industries, standout achievements with numbers, tools, and anything that signals a pivot. Restate the plan in 2–3 lines ("Looking for remote Senior PM roles in AI, excluding 12 companies, targeting 50 roles"), then start. If they're likely to step away, don't wait for confirmation.

Pick the keyword set that matches their roles from `references/keywords/` (`product-marketing.json`, `product-management.json`, `engineering.json`, `design.json`, `sales.json`, or `general.json` as a fallback). If none fits well, copy `general.json` and add 20–30 terms typical for their field.

## Step 2: Collect roles (wide net)

Build queries from their titles, level and sector. `references/search-queries.md` has templates and variations.

1. **Public applicant-tracking boards with web search**, one query per board, varying the qualifiers:
   - `site:jobs.ashbyhq.com ("<Title 1>" OR "<Title 2>" OR "<Title 3>") (remote OR "Remote (US)")`
   - the same for `site:job-boards.greenhouse.io`, `site:boards.greenhouse.io` and `site:jobs.lever.co`
   - Vary the second clause with sector terms, the city, and senior title variants (Staff, Principal, Head of, Director, Founding).
2. **Sector job boards** if one exists for their industry (search "<sector> startup jobs board"). These often list stage and location.
3. **Wellfound:** `site:wellfound.com/jobs "<title>" <sector>`.
4. **Each company's full job board.** When you open a company's board to verify one role, note any other matching roles there. This finds roles no search surfaced.
5. **LinkedIn (if they opted in).**
   - **Check for a browser.** It needs one Claude can control, where the person is signed in to LinkedIn (e.g. Claude in Chrome or a built-in browser).
     - If none is connected, ask them once to connect it and say why.
     - If they decline, or it still isn't available, skip LinkedIn, say so in the hand-over, and give them the search links to run themselves (format in `references/search-queries.md`).
   - **Run 2–4 searches** in a new tab, using the URL format in `references/search-queries.md`: past 7 days, their location filter, newest first. Vary the queries (core titles, senior/Director/Head-of titles, sector terms).
   - **Read each results page** with page-text reading. Wait about 3–4 seconds after each navigation; LinkedIn renders late.
   - **Pick the postings that match** their titles, sector and location. Open each one at `https://www.linkedin.com/jobs/view/<id>/`. The id is the `currentJobId` value in the URL once a result is selected, or comes from the result's link.
   - **Read the posting.** Take title, company, location and salary if shown. If the job is posted on the company's own job board (Ashby, Greenhouse, Lever), prefer that as the apply link. Otherwise use the `/jobs/view/<id>/` link.
   - **Limits:**
     - at most about 25 postings per run, opened one at a time at a normal reading pace
     - reading only: never click Apply, Easy Apply, Save, Message or Follow
     - stop and tell the person if LinkedIn shows a sign-in wall, a security check or a warning; don't try to get past it
   - **Close the tabs you opened** when done.
6. **Other sign-in sites** (Indeed accounts, etc.): don't automate them. Give the person search links to run themselves, and add any postings they paste back.

Dedupe by company + title. Remove companies they already applied to. **Search results are not proof a job is open.** Roughly a third of search hits turn out to be closed, so everything goes through Step 3.

## Step 3: Verify every role is live

This step needs a way to open web pages: a browser Claude can control (e.g. Claude in Chrome or a built-in browser) or a page-fetch tool. Use what the session has. If neither can open the job boards, say so plainly and mark rows "Not verified" rather than guessing.

How to tell open from closed (details in `references/ats-verification.md`):
- **Ashby:** a closed posting shows "Job not found". Opening the company board (`jobs.ashbyhq.com/<company>`) lists every live role at once.
- **Greenhouse:** a closed posting redirects to `…/<company>?error=true`. Boards paginate, so open each posting rather than trusting the board list. Some redirect live jobs to the company's own careers page with `gh_jid` in the URL; that counts as live, so use that URL.
- **Lever:** a closed posting is a 404 page.
- **LinkedIn:** a live posting at `/jobs/view/<id>/` shows the title and an Apply or Easy Apply button. "No longer accepting applications" means closed.
- **Anything else:** look for the job title and an Apply button on the page.

Working tips for browser sessions:
- Check several postings per batch, but keep batches small (6–10). Long batches can drop the connection.
- Save each result as you go (in the browser's `localStorage` or a local file), so a dropped connection doesn't lose work.
- Postings close fast: in testing, about 10% of verified roles closed within a day. If the list is more than a day old, recheck before handing it over.
- Confirm what each company actually does from its own page. Job boards sometimes mislabel the sector.

## Step 4: Score fit (0–100)

Use this rubric and show it in the tracker, so the person can see why a role ranks where it does:

| Factor | Points | High score when |
|---|---|---|
| Seniority match | 25 | Title matches their level; one level up or down scores lower |
| Background match | 25 | Their past industries and achievements map directly to the company's customers |
| Location fit | 20 | Meets their location rules exactly |
| Recency | 15 | Posted in the last 14 days |
| Sector fit | 15 | Core to their target sector, not adjacent |

Subtract 5 for a clear skills gap (e.g. a "Technical" title for a non-technical background). Apply their salary floor and stage filter if given.

Tiers: **A – apply first** (88+), **B – strong** (76–87), **C – volume** (below 76). Adjust the cut-offs so Tier A is roughly the top quarter.

For every row, write one sentence: the angle from their résumé to lead with, or the gap to address. Use only what's on the résumé. Never invent experience.

## Step 5: Location filter and cleanup

- If they asked for remote only: keep explicitly remote roles on the main list. Move on-site, hybrid and city-based roles to a separate "Not remote" tab (don't delete them, in case they change their mind). Flag roles listed as "Multiple locations" or just a country as "check if remote".
- Remove anything closed, at an already-applied company, or without a direct apply link.

## Step 6: Build the tracker

Pick the output in this order, unless they chose one:
1. A spreadsheet artifact type in this app, if available.
2. A Google Sheet, if a Google Sheets connector is connected.
3. An .xlsx file, if a spreadsheet skill or library is available.
4. A CSV based on `templates/tracker-template.csv`.

**Main tab columns (most important first):** Tier, Score, Company, Role, Apply link, Status, Location, Sector, Seniority, Company stage, Posted, Days open, What they do, Your angle / gap, Verified, Salary, Source.

- **Status:** a dropdown with To apply / Applied / Interviewing / Skipped / Closed, where the format supports dropdowns.
- **Summary at the top:** roles listed, Tier A count, applied so far and verified live, as formulas where supported.
- **Freeze** the header row and the Company column.
- **Salary:** record it whenever the posting shows one.

## Step 7: Keyword-gap report (if they said yes)

Find the words employers in this search use most, and which of them the résumé is missing.

1. Choose the keyword set from Step 1. Build the in-page counter: `python3 scripts/build_counter.py references/keywords/<set>.json > counter.js`.
2. On each verified posting page, run the contents of `counter.js` in the page (e.g. with a browser's JavaScript tool). It returns a compact line: `word_count|index:count,…|top phrases`. A word count under ~30 means the posting closed; verify it and drop it.
   - To avoid re-sending the script for every page, store it once per site (`localStorage.kw = <script>`), then run `await eval(localStorage.kw)` on each page. Some company career sites block scripts; skip those and say so.
   - If you can only fetch page text (no browser), apply the same regexes from the JSON to the fetched text yourself.
3. Save one line per posting to `hits.txt` as `posting_id|word_count|index:count,…`.
4. Run `python3 scripts/aggregate.py references/keywords/<set>.json hits.txt resume.txt > keywords.csv`. This gives each theme's rank, the postings using it, the % of postings, total mentions, the count on the résumé and a leverage rating (High – missing / Medium – missing / Medium – underused / Covered / Low).
5. Check the résumé column by hand for wording the matcher missed (e.g. "Owned" vs "own", "12 years" vs "5+ years"), and correct it.
6. Put it on a **Keywords** tab with a "How to use it" note for each High or Medium term. Tie every tip to something the person actually did. For anything you can't confirm from the résumé, say "only if true". Note that company boilerplate can inflate a few generic terms (e.g. "AI", "data").

## Step 8: Check, then hand over

- Re-read the tracker after writing it. Confirm the counts, that the links open, and that no closed or already-applied roles slipped in.
- Tell the person:
  - How many live roles they have, and how many are Tier A.
  - What closed during the search.
  - What couldn't be verified, and why.
  - The 5–7 highest-leverage résumé wording changes.
- Offer one next step: short tailored openers for the Tier A roles, résumé bullet rewrites, or a weekly re-run to refresh the list.

## Guardrails

- Never mark a role live from a search snippet or from memory, only from the posting page itself, checked during this run.
- Never invent résumé experience, metrics or skills in tips or openers.
- Use LinkedIn only if the person opted in, only in their own signed-in browser, within the limits in Step 2: read only, at a normal pace, and stop at any sign-in wall, security check or warning. Don't automate other sign-in sites.
- Don't apply to jobs, message recruiters or submit forms on the person's behalf unless they explicitly ask, and confirm each submission first.
- Keep the person's résumé and tracker private. Don't put personal details in URLs or share them outside the session.
