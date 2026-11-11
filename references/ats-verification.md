# Checking whether a posting is live

Search results and job aggregators keep showing postings long after they close. In testing, about a third of search hits were already closed, and about 10% of verified roles closed within a day. Check every posting during the run.

## Ashby (`jobs.ashbyhq.com`)

- **Posting page:** a live posting shows the job title. A closed one shows "Job not found" and the page title becomes just "Jobs".
- **Company board** (`jobs.ashbyhq.com/<company>`): lists every live role. Reading its job links is the fastest way to confirm several roles at once and spot extra matching roles. Example in-page script:

  ```js
  await new Promise(r=>setTimeout(r,1500));
  [...document.querySelectorAll('a')]
    .map(a=>a.innerText.split('\n')[0]+' | '+a.href)
    .filter(t=>/<title keyword regex>/i.test(t))
  ```
- Pages render with JavaScript. Wait about 1.5–3 seconds before reading.

## Greenhouse (`job-boards.greenhouse.io`, `boards.greenhouse.io`)

- **Posting page:** a live posting shows the title in the page's main heading. A closed one redirects to `…/<company>?error=true`.
- **Company board pages paginate.** A role missing from the first page of the board is not proof it closed, so open the posting itself.
- Some companies send live postings to their own careers site with `?gh_jid=<id>` in the URL. Treat that as live, and use that URL as the apply link.

## Lever (`jobs.lever.co`)

- A closed posting returns a "Not found – 404" page. Live pages render fully, including without JavaScript.

## Wellfound and others

- Look for the job title plus an active Apply button. "No longer accepting applications" or a redirect to a search page means closed.

## LinkedIn

- Only if the person opted in, and in their own signed-in browser. Open `https://www.linkedin.com/jobs/view/<id>/`. A live posting shows the title and an Apply or Easy Apply button; "No longer accepting applications" means closed.
- If the posting points to a company job board (Ashby, Greenhouse, Lever), verify it there and use that link.
- Read only, at a normal pace. Stop at any sign-in wall, security check or warning.
- If LinkedIn isn't available, the person can paste a job id, and you build the direct link the same way.

## Doing this at volume

- Work in small batches (6–10 postings); long batches can drop the connection.
- Save each result as you go (in the browser's `localStorage`, or a local file) and read them back at the end.
- Record a status for every row: `Live (checked <date>)`, `Closed (<date>)` or `Not verified (<reason>)`.
- Recheck anything more than a day old before handing over the final list.
