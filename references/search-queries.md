# Search query templates

Replace `<T1>`, `<T2>` and `<T3>` with the person's target titles (three or four variants work best), `<SECTOR>` with their industry term, and `<CITY>` with their city.

## Applicant-tracking boards (run each with web search)

Run every pattern on each board:

| Board | `site:` prefix |
|---|---|
| Ashby | `site:jobs.ashbyhq.com` |
| Greenhouse (new) | `site:job-boards.greenhouse.io` |
| Greenhouse (old) | `site:boards.greenhouse.io` |
| Lever | `site:jobs.lever.co` |

Patterns:

```
<prefix> ("<T1>" OR "<T2>" OR "<T3>") (remote OR "Remote (US)")
<prefix> ("<T1>" OR "<T2>" OR "<T3>") <SECTOR>
<prefix> ("<T1>" OR "<T2>" OR "<T3>") "<CITY>"
<prefix> ("Senior <T1>" OR "Staff <T1>" OR "Principal <T1>") <SECTOR>
<prefix> ("Director of <FUNCTION>" OR "Head of <FUNCTION>" OR "Founding <T1>") <SECTOR>
```

Useful second clauses for AI roles: `AI`, `agentic`, `"AI agents"`, `LLM`, `"generative AI"`. For fintech: `fintech OR "financial services" OR payments`.

Example (product marketing, remote, AI):

```
site:jobs.ashbyhq.com ("Product Marketing Manager" OR "Senior Product Marketing Manager" OR "Director of Product Marketing") (remote OR "Remote (US)")
```

## Wellfound

```
site:wellfound.com/jobs "<T1>" <SECTOR> remote
```

## Sector boards

Search `<SECTOR> startup jobs board <FUNCTION>`. Many sectors have curated boards (AI, climate, crypto, health tech) with stage and location filters.

## LinkedIn

Use these in the person's signed-in browser if they opted in (see SKILL.md Step 2 for the limits). Otherwise, give them the links to run themselves.

```
https://www.linkedin.com/jobs/search/?keywords=<URL-encoded title + sector>&location=United%20States&f_TPR=r604800&f_WT=2&sortBy=DD
```

- `f_TPR=r604800` = posted in the past 7 days (`r86400` = 24 hours)
- `f_WT=2` = remote (`1` = on-site, `3` = hybrid)
- `sortBy=DD` = newest first

When a posting is open, its URL contains `currentJobId=<id>`. The direct link is `https://www.linkedin.com/jobs/view/<id>/`; store that in the tracker.

Reading tips:
- Wait 3–4 seconds after each navigation before reading. Results and job details load late.
- Results pages: read the page text and pick matching title / company / location entries.
- Posting pages (`/jobs/view/<id>/`): the description sits between "About the job" and "About the company". The keyword counter already slices to that part.
- If the results page has no job ids in its links, select a result and read `currentJobId` from the address bar.

Example searches (remote, past week, newest first):

```
https://www.linkedin.com/jobs/search/?keywords=%22product%20marketing%22%20AI&location=United%20States&f_TPR=r604800&f_WT=2&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=%22director%20of%20product%20marketing%22%20AI&location=United%20States&f_TPR=r604800&sortBy=DD
```
