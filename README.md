# JobSnatcher

**A Claude skill that snatches open job listings matching your résumé, checks every one is still live, ranks them by fit, and hands you a clean application tracker, plus a report of the résumé keywords employers want and you're missing.**

Built by [Kelly Reddington](https://kellyreddington.xyz). More AI marketing workflows at [brandsurf.ai](https://brandsurf.ai).

---

## What you get

1. **An application tracker** of live roles you can apply to directly:
   - Tier (A / B / C) and a 0–100 fit score
   - company, role and direct apply link
   - location, salary when listed, and company stage
   - a one-line angle from your résumé (or the gap to address) for every role
   - a Status dropdown (To apply / Applied / Interviewing / Skipped / Closed) to track your applications
2. **A "Not remote" tab**, if you only want remote roles. On-site and hybrid roles go here instead of being deleted.
3. **A keyword-gap report:** the skills and phrases that appear most across the postings, ranked, with a check against your résumé and tips on wording you can honestly use.

## How it works

You answer a short intake once (target titles, industry, location rules, and your résumé). Then JobSnatcher:

1. **Searches** the public applicant-tracking boards (Ashby, Greenhouse, Lever) with targeted `site:` queries, plus Wellfound, sector job boards and, if you opt in, LinkedIn in your own browser.
2. **Verifies** each posting is still open by opening it. About a third of search results are typically already closed.
3. **Scores** each role against your résumé (seniority, background match, location, recency, sector).
4. **Builds** your tracker in whatever your setup supports: a spreadsheet in Claude, a Google Sheet, Excel or CSV.
5. **Reads** the live postings and counts the keywords they use, then compares them with your résumé.

**LinkedIn is opt-in.** If you say yes and Claude can use your browser, JobSnatcher runs a few LinkedIn searches in your own signed-in session at a normal pace. It only reads; it never applies, messages or saves anything, and it stops if LinkedIn shows a security check. LinkedIn's terms restrict automated tools, so it's your call. If you say no, or no browser is connected, JobSnatcher skips LinkedIn and gives you search links to run yourself.

## What you need

- Claude with **Skills** enabled
- **Web search**
- **A browser Claude can control** (for example Claude in Chrome), or a page-fetch tool that can open job boards. Without one, JobSnatcher still finds roles but marks them "Not verified".
- Optional: signed in to LinkedIn in that browser, if you want LinkedIn included
- Optional: a Google Sheets connector, if you want the tracker in Google Sheets

## Install

1. Download `JobSnatcher.zip` from this repo's Releases (or clone the repo).
2. Add it as a skill:
   - **Claude apps:** upload the zip wherever your Claude app lets you add custom skills. See Anthropic's help center for current steps.
   - **Claude Code:** unzip into `~/.claude/skills/` so you have `~/.claude/skills/jobsnatcher/SKILL.md`.
3. Start a chat and say something like: *"Run JobSnatcher. I'm looking for remote Senior Product Manager roles in AI."* Attach your résumé.

## What's inside

```
jobsnatcher/
├── SKILL.md                     # The skill: intake, search, verify, score, build, keyword report
├── scripts/
│   ├── build_counter.py         # Builds the in-page keyword counter from a keyword set
│   └── aggregate.py             # Turns per-posting counts into the ranked keyword-gap report
├── references/
│   ├── search-queries.md        # Query templates for each job board, LinkedIn link format
│   ├── ats-verification.md      # How to tell a live posting from a closed one, per board
│   └── keywords/                # Keyword sets by role family
│       ├── general.json
│       ├── product-marketing.json
│       ├── product-management.json
│       ├── engineering.json
│       ├── design.json
│       └── sales.json
└── templates/
    └── tracker-template.csv     # Column layout for the CSV fallback
```

## Customize

- **A new role family:** copy `references/keywords/general.json`, add 20–30 terms typical for the field (`label` plus a regex `pattern`), and save it as `<family>.json`. JobSnatcher picks the closest set automatically.
- **Scoring:** the rubric is in `SKILL.md` under "Score fit". Change the weights to match what matters to you.
- **Search scope:** add sector boards or query variations in `references/search-queries.md`.

## Good to know

- Job postings close fast. Re-run JobSnatcher, or ask it to recheck your list, if it's more than a day or two old.
- The keyword tips only suggest wording for experience that's actually on your résumé. Anything it can't confirm is marked "only if true".
- JobSnatcher never applies to jobs or contacts anyone unless you explicitly ask it to.
- Your résumé stays in your Claude session; nothing is sent anywhere else.

## License

MIT. Free to use, adapt and share. See [LICENSE](LICENSE).

If JobSnatcher helps you land interviews, I'd love to hear about it. Find me at [kellyreddington.xyz](https://kellyreddington.xyz) or [brandsurf.ai](https://brandsurf.ai).
