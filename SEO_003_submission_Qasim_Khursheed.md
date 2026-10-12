# SEO recovery plan: 12 months for a declining fintech blog

**Qasim Khursheed** · **Brief version:** 2026-07 · **Date:** 12 October 2026 · **Fixture SHA-256:** `fa691abc31b14093230657d17674ab0120449c54d20cef54bfe73686fe9b99c6`
**Workbook:** `SEO_003_audit_and_refresh_model.xlsx`, open the Start_Here sheet first. **Number labels:** [Observed] = from the fixture, the brief or a live tool pull · [Estimated] = my estimate · [Benchmarked] = a named source · [Assumed] = a placeholder. A label at the start of a paragraph covers every number in it unless a number carries its own.

**The short version.** Traffic dropped because the pages that used to rank have not been updated in two to five years, the competitors above them have, and an AI Overview now sits on top of the big head terms. A third of the lost traffic in the sample was two dated URLs that simply expired. Links are not the problem and the site does not look penalized. The plan: agree a conversion KPI with the VP, fix the seven highest-value pages in the first 30 days, run all 400 posts through one set of rules, and build links only to pages that make money. [Estimated] At 12 months I expect about 117K visits and roughly double the organic conversions. I am not promising 140K. Section 8 says why.

How this maps to the brief: diagnosis and competitive response are sections 1 to 4, content and technical are sections 5 to 7, the roadmap is section 8.

## Written answer

### 1. Agree the KPI with the VP before anything else

[Observed] The brief gives 85K and 140K visits with no source. If those are Ahrefs or Semrush numbers they are estimates built from rankings and an assumed click rate, blind to AI Overviews and seasonality. I report on GA4 sessions and Search Console clicks and set goals on revenue, never on a tool estimate.

[Observed] Traffic and revenue point in different directions in this data. Of the 35,710 visits the sample lost, 16,460 (46%) were on six pages with zero conversions. Four pages produce 77.5% of the 200 conversions. The two comparison pages get 2,000 visits a month and 72 conversions, 12 per 1,000 visits, against 1.85 for the sample as a whole. Getting the dated per diem page back would add 7,500 visits and nothing to pipeline.

[Observed] The conversion numbers need a quality check too. The 44 on the Ramp comparison page could be Ramp customers browsing, and the 12 on the template page may be downloads rather than signups. Until the CRM says which leads became opportunities, 50 conversions on one page can be worth less than 5 on another.

So the KPI I propose is organic conversions that reach SQL, by landing page, with pipeline value, monthly. Traffic stays as a health metric, split branded and non-branded and by page type. Week one is data collection: [Observed] the full 16 months Search Console keeps (90 days hides seasonality and rankings that bounced back), GA4 conversions by landing page for both years, CRM stage by landing page, Ahrefs new and lost referring domains by month, last-modified dates for all 400 posts, and CrUX field data. The Data_To_Request sheet in `SEO_003_audit_and_refresh_model.xlsx` lists each one with an owner.

### 2. Why the traffic dropped

[Observed] The fixture is 18 pages, down 49.7% against 39.3% for the site. Those 18 pages are 42% of today's traffic, so this is the top of the site rather than a fair sample. I use it to rank the causes. I would not use it to size them for the whole site.

| Cause [Observed] | Share of lost traffic | Pages | Fix |
|---|---|---|---|
| Dated URLs expired | 35.0% | `per-diem-rates-2022`, `quarterly-tax-deadlines-2023` | Redirect to evergreen URLs, refresh yearly |
| Head terms lost to fresher pages and an AI Overview, plus one cannibal | 46.2% | `what-is-expense-management`, `expense-management-guide`, `business-expense-categories`, `corporate-card-vs-credit-card` | Refresh, merge the cannibal |
| Off-topic pages outranked by aggregators | 9.1% | `accounting-software-list`, `bookkeeping-basics` | Remove |
| Rules changed, page did not | 6.2% | `mileage-reimbursement-guide` | Refresh |
| Lost clicks without losing rank (AI Overview, mixed intent) | 2.2% | `receipt-scanning-app` (#5 then and now, traffic down 31%) | Refresh for citation, accept lower traffic |
| Comparison page slipping | 2.2% | `vs-ramp` (6 to 11) | Rebuild first |
| Pages that grew | -3.8% | `travel-expense-policy`, `what-is-spend-management`, branded page | Build around them |

**Two kinds of drop.** [Observed] The head terms slid 2 to 5 positions. That is competition. Four pages fell 17 to 38 positions (per diem 5 to 29, tax deadlines 3 to 41, accounting list 10 to 34, bookkeeping 14 to 31). That is expiry and off-topic content, and no amount of links fixes it.

**Old pages dropped, updated pages held.** [Observed] The older the last update, the bigger the fall. On a scale where 1.0 is a perfect match, the correlation between months since update and positions lost is 0.83. Pages that fell were last updated 39 months ago on average; pages that held, 21. Nothing in the sample has been touched since January 2025, which is the 18-month audit gap in the brief. The two pages that improved are the two most recently updated.

**Rankings explain the lost clicks.** I took a standard click-through curve ([Benchmarked] FirstPageSage via Backlinko for positions 1 to 10, page 2 and beyond [Assumed]) and checked what each page's old traffic should have become at its new position. On every head term the rank drop alone accounts for the lost clicks. Only the receipt scanning page lost clicks without moving, and the live SERP shows why.

**Who took the positions.** [Observed] I pulled the live US SERPs on 12 October 2026. An AI Overview sits above the first result on four of the five terms. "What is expense management": NetSuite (updated July 2025), Medius, Ramp (July 2026), Airwallex (May 2026), Stripe (July 2026); our page was last updated January 2024. "Business expense categories": IRS, NetSuite (September 2026), Ramp (May 2026), Paychex (March 2026); ours is from November 2023 with outdated IRS references. "Corporate card vs credit card": JPMorgan, Chase, Reddit, Amex, Investopedia, and Ramp is not in the top 10. "Per diem rates": GSA, State, DoD, Commerce. "Receipt scanning app": an AI Overview, consumer cashback apps, a video carousel, Reddit. The fixture note says we lost a featured snippet to Ramp. That is half of it. Everyone in the top five refreshed in 2025 or 2026 and the AI Overview took the top. [Benchmarked] Ahrefs measured a 58% lower click rate for the first result when an AI Overview is present (February 2026, 300,000 keywords), so getting back to #1 does not bring back 14,100 visits.

**Links show where pages sit. They do not explain why pages moved.** [Observed] Pages with more referring domains rank higher today (correlation -0.77 with position). But links did not protect pages from falling: the four pages with 50+ referring domains (84, 74, 61, 52) all dropped, and the two pages that grew have 26 and 11. This is not a decline we can link our way out of. The spam question cannot be answered from counts; 84 referring domains say nothing about relevance, anchors or timing. In week one I run the Ahrefs new and lost report by month for the domain and the four fallen pages, check anchors and DR spread, and line that up with the update calendar. A spike in links before the drop, or exact-match anchors, means a link problem and a targeted disavow. Otherwise no disavow. I have done this once on an ecommerce collection that kept dropping in and out because of exact-match anchor links. A fresh URL and natural links fixed it, and the page still ranks a year later.

**Google updates.** [Benchmarked] In the 12 months to the brief date (Search Engine Journal's update history): spam August 2025, core December 2025, core and spam March 2026, core May 2026, spam June 2026. The brief has no monthly trend, so I cannot line the drop up yet. The rule for the Search Console export: a step down inside a core update means content quality, a step down inside a spam update means the link profile, a slow slide means decay and competition. [Observed] The fixture argues against a sitewide hit: 5 of 18 pages on the same template held or grew.

**Ramp's footprint and link pace.** [Observed] Ramp ranks for about 34,000 to 41,000 US keywords with 420,000 to 474,000 estimated monthly visits, roughly 3x our keywords and 5x our traffic, and even that softened between June and October 2026. Over the 12 months to September 2026 Ramp gained a net 340 referring domains a month, with the pace doubling in the second half. Brex gained 165. Our own pace goes into the Competitors sheet in week one.

**Core Web Vitals.** [Observed] LCP of 3.2s and failing mobile vitals are real, but the pages that held rank share the same slow template. Vitals are a tiebreaker: between two pages with similar authority and content, the faster one tends to win, but they do not lift a page that is losing on freshness or authority. Content and links first, speed next. It still gets the first sprint because it is cheap and helps mobile conversion.

Where to look: `SEO_003_audit_and_refresh_model.xlsx`, sheets Why_Traffic_Dropped, Live_SERPs and Competitors.

### 3. Seven things in the data I would not take at face value

1. **The traffic numbers.** Source unknown, monthly, against conversions counted over 90 days.
2. **The notes column.** [Observed] "Highest converting blog page" on the corporate card page is wrong. The branded page sitting under /blog has 52 conversions to its 31, and it inflates every blog total. It comes out of the SEO baseline.
3. **Referring domain counts.** [Observed] The fraud statistics page has 74 and 1 conversion. The Ramp comparison page has 19 and 44. Quality and relevance decide, and the fixture has neither.
4. **Conversions without lead quality.** [Observed] 44 on the Ramp comparison and 12 on the template need CRM stages before they set priorities.
5. **The receipt scanning drop.** [Observed] Same position, 31% fewer clicks. A refresh aimed at rank cannot fix that.
6. **The spend management "win".** [Observed] 300 to 650 visits is too small to call a trend.
7. **The sample itself.** [Observed] 18 rows, 42% of site traffic, down 50% against the site's 39%. I would not scale any of these shares to the full site.

Where to look: the "Watch out" column in the Page_Triage sheet of `SEO_003_audit_and_refresh_model.xlsx`.

### 4. Ramp: fight, flank, concede

[Observed] Ramp published 50 posts in six months, about 100 a year at that pace [Estimated], against our 48, and gains 340 referring domains a month. We do not out-publish them.

[Observed] **Fight** where we convert or already hold: the comparison and alternatives pages (12 conversions per 1,000 visits), the corporate card decision content (hold #5 against the banks and convert; do not chase #1 against JPMorgan), and the expense management head terms on depth and freshness, with the definition written so the AI Overview can cite it. **Flank** with formats Ramp's volume does not cover: templates and tools (expense policy, categories sheet, report template, mileage calculator; the categories SERP shows PDF and spreadsheet demand), original data from anonymized product spend (the fraud page already has 74 referring domains), and the spend management cluster where we are growing on our own. **Concede** generic finance education (invoicing, bookkeeping, best accounting software), the per diem and tax deadline rate queries that government sites own, and consumer SERPs like receipt scanning. Keep a cheap evergreen page for the long tail and spend nothing else there.

Where to look: `SEO_003_audit_and_refresh_model.xlsx`, Topics sheet.

### 5. The 400 posts: four decisions, eight rules

Every page gets one of four decisions: Protect, Refresh, Consolidate or Kill. The rules run in order and the first one that fits wins.

- R1 Two pages targeting the same keyword → Consolidate the weaker one into the stronger.
- R2 Year in the URL → Consolidate into an evergreen URL, refresh on a calendar.
- R3 Off-topic, zero conversions, under 10 referring domains, lost 15+ positions ([Assumed] thresholds, editable in the sheet) → Kill.
- R4 Two or more conversions per 1,000 visits, or a branded page → Protect. Light update, stronger CTA, links pointed in.
- R5 Holding or gaining and updated in the last 24 months → Protect and build around it.
- R6 Traffic with no product relevance → Protect, spend nothing, test one CTA.
- R7 Lost rank, or older than 18 months on a core topic → Refresh. Keep the URL. Pages with 70+ referring domains are never redirected.
- R8 Anything else → monitor.

[Observed] On the fixture that gives 8 Protect, 5 Refresh, 3 Consolidate, 2 Kill. Priority is traffic lost times conversion relevance, conversion pages first, and the free fixes (redirects, removals) go in the same month because they cost nothing. Refresh beats new wherever a URL already has links and a ranking history; an 84-referring-domain page at #4 beats a new post every time. New posts only go where a converting topic has no URL yet, which is the comparison hub and the spend management cluster.

| Priority | Page | Decision | What we do |
|---|---|---|---|
| P1 | `/compare/vs-ramp` | Protect | Rebuild as a real comparison with a pricing and feature table, stronger CTA, internal links from the two strongest blog pages [Observed] |
| P1 | `/blog/what-is-expense-management` | Refresh | Full refresh for depth and AI Overview citation; redirect `/blog/expense-management-guide` into it |
| P1 | `/blog/per-diem-rates-2022`, `/blog/quarterly-tax-deadlines-2023` | Consolidate | Redirect to evergreen URLs, refresh yearly, no other spend |
| P1 | `/blog/bookkeeping-basics`, `/blog/accounting-software-list` | Kill | Remove, or redirect to a hub if the few links are from real sites |
| P2 | `/blog/business-expense-categories` | Refresh | Current IRS references plus a downloadable categories sheet |
| P2 | `/blog/corporate-card-vs-credit-card`, `/blog/expense-report-template` | Protect | Light update, CTA, download-to-signup test; agree what counts as a conversion |
| P2 | `/blog/mileage-reimbursement-guide` | Refresh | Current IRS rate in a block that can be quoted |
| P3 | `/blog/receipt-scanning-app`, `/blog/expense-fraud-statistics` | Refresh | Write for citation; refresh the statistics yearly; never redirect the fraud page |
| P3 | `/compare/vs-brex`, `/blog/travel-expense-policy`, `/blog/what-is-spend-management` | Protect | Build the clusters around them |
| P3 | `/blog/company-name-expense-software`, `/blog/what-is-an-invoice` | Protect | Report the branded page separately; no spend on the invoice page |

**Scaling to 400.** Export URL, target keyword, position now and 12 months ago, Search Console clicks, referring domains, last-modified date and GA4 conversions. The sheet works out the rest. Apply R1 to R8. A person reviews every Kill and Consolidate before a redirect goes live. Redirects ship in the sprint, refreshes through the freelancers, and refreshed pages are measured against a holdout. Capacity for the year: 48 new posts ([Observed] the brief's 4 a month), 96 refreshes ([Assumed] 8 a month) and about 80 consolidations or removals ([Estimated] SEO Specialist time). Every post gets a decision, about half get work.

**Topics and page types.** [Observed] By topic, comparison pages convert at 12 per 1,000 visits, corporate cards at 2.5, the seven core expense management pages at 0.68, rates and deadlines at 0.61, off-topic finance at 0. The topical map still matters because the core cluster holds 246 of the sample's referring domains, but new content and links go to the converting topics first, and the final order waits for CRM pipeline by landing page. Product pages are 15% of traffic and comparison pages 10%, with no conversion data in the brief. I assume they convert best and treat the blog as the feeder: internal links from the strongest blog pages into the comparison hub and product pages, commercial queries moved onto product pages, and templates and tools as the download-to-signup path.

Where to look: `SEO_003_audit_and_refresh_model.xlsx`, sheets Page_Triage, Triage_Rules and Topics.

### 6. Technical: one sprint a quarter

Sprint 1: blog template speed (hero image, fonts, lazy loading, caching), the redirect map, and a related-posts and in-content link module. Sprint 2: the comparison page template with tables, schema and CTAs, plus the template download flow. Sprint 3: internal linking automation from the strongest pages to the comparison and product pages. Sprint 4: held for whatever the data says. Cut from the plan: INP work, redesign, any framework change. Most speed work on WordPress is contractor work (images, caching, hosting), so the sprint is spent on template changes only.

### 7. Links on $15K a month

No paid links at any price; one bad batch on a DR 62 domain costs more than a year of PR. [Assumed] $4,000 a month goes to a digital PR freelancer and one data study a quarter built from anonymized, aggregated product spend data. Reclaim what we have: unlinked brand mentions, broken links to the dated URLs, and redirects so the [Observed] 22 and 9 referring domains on the expired pages pass to the evergreen ones. Templates and tools earn links without outreach; the finance team's quotes go out through journalist request platforms. Internal links are the cheapest links we have, so the two strongest blog pages point into the comparison hub. Links go to pages that convert or hold the head terms, never to volume.

Where to look: `SEO_003_audit_and_refresh_model.xlsx`, Competitors sheet, and `evidence/triage_table.csv` for the referring domain counts.

### 8. The 12-month plan, budget and targets

**Budget and team.** [Assumed] unless marked: tools $1,000; 4 new posts $1,200 [Observed]; 8 refreshes $1,600; digital PR $4,000; WordPress speed contractor $2,500 (front-loaded, drops by Q3); CRO and design $1,500; automation $700; reserve $2,500; total $15,000. The SEO Specialist owns the triage sheet, Search Console monitoring, internal linking and the sprint tickets. The Content Manager owns refresh briefs, freelancer QA, CTAs and templates. Three freelancers carry 4 new posts and 8 refreshes a month. No hire for six months; at month seven, a content strategist or editor only if refresh throughput is the bottleneck.

| When | What ships | Sprint | Target [Estimated] |
|---|---|---|---|
| Days 1 to 30 | KPI agreed and baselined; Search Console trend lined up with the update calendar; link audit; all P1 pages live; holdout set ([Assumed] 20 refreshed vs 20 untouched) | Sprint 1 scoped | Redirects and removals live; Ramp comparison rebuilt |
| Days 31 to 90 | P2 pages; 4 new posts a month in the spend management cluster; first data study scoped | Sprint 1 ships | The 90-day targets below |
| Q2 | Rules run on all 400; data study #1; comparison hub (two more comparisons, one alternatives page); template library | Sprint 2 | 100+ posts actioned; conversions +40% to +60% on the Q1 baseline; traffic 100K to 110K |
| Q3 | Refresh pipeline at full pace; data study #2; hiring decision | Sprint 3 | 250+ posts actioned; conversions about +80%; traffic 110K to 120K |
| Q4 | All 400 actioned; yearly refresh calendar; holdout results reported | Sprint 4 (reserve) | Conversions about 2x; traffic 115K to 120K |

**90 days.** [Estimated] The Ramp comparison back in the top 8; the two head terms up 2 positions; refreshed pages beating the holdout on impressions; comparison page conversion rate up 25%; blog LCP under 2.5s in lab ([Benchmarked] Google's threshold). **6 months:** 100+ posts actioned, conversions up 40% to 60%, traffic 100K to 110K. **12 months:** conversions about 2x, traffic 115K to 120K.

**Why not 140K.** [Estimated] The head terms now sit under an AI Overview and the two expired URLs are government-owned queries, so the old pages top out around 117K even if every refresh works. Anything beyond that comes from new clusters and templates. The Targets_Month_12 sheet has every assumption as an editable cell, and the Q1 holdout replaces the assumed refresh uplift with a measured one.

**If the 90-day numbers do not move.** Head terms flat after 8 weeks indexed ([Assumed] window): the problem is format and authority, so Q2 refresh money moves to the data study and the page formats change to tools and templates. Refreshed pages not beating the holdout: stop at 24 refreshes and go back to the Search Console data and the update calendar. The rebuilt comparison page not converting: the offer is the problem, product marketing owns it, SEO stays on traffic.

**Also worth setting up.** [Observed] Track who the AI Overview cites on the head terms (today NetSuite, Procurify, Workday, Airwallex and Ramp; we are absent). Compare year on year, because the tax deadline page is seasonal. Track mobile rankings separately, since mobile vitals are failing. Write down what counts as a conversion before the first report. Run a monthly check: which pages lost, which gained, what changed on theirs, what changed on ours. Happy to walk through the sheet live and run the rules on a messy sample of real posts.

Where to look: `SEO_003_audit_and_refresh_model.xlsx`, sheets Plan_90_Days, Roadmap_12_Months, Budget and Targets_Month_12.

## Operating artifact

`SEO_003_audit_and_refresh_model.xlsx`, 13 sheets. Start_Here gives the reading order and color legend. Working sheets: Why_Traffic_Dropped, Page_Triage, Triage_Rules, Topics, Plan_90_Days, Roadmap_12_Months, Budget, Targets_Month_12. Evidence sheets: Data_To_Request, Live_SERPs, Competitors, Ref_CTR_Curve. Page_Triage holds the [Observed] 18 fixture pages with decision, rule, priority, action and watch-out, with the derived numbers as live formulas. `scripts/analyze_fixture.py` reproduces every fixture number; `scripts/build_workbook.py` rebuilds the file.

## Evidence log

| Claim | Proof | Tier |
|---|---|---|
| Decline breakdown, correlations, page decisions | `scripts/analyze_fixture.py` on the fixture; outputs in `evidence/analysis_output.json` and `evidence/triage_table.csv`; workbook recalculates from inputs [Observed] | Tier 3 |
| Who ranks now, AI Overview presence, competitor update dates | `evidence/live_serp_observations_2026-10-12.csv`, DataForSEO task ids included | Tier 3 |
| Ramp footprint, Ramp and Brex link pace | `evidence/ramp_com_historical_rank_overview_2026-10-12.csv`, `evidence/competitor_link_velocity_2026-10-12.csv`, task ids included | Tier 3 |
| Click-through curve, AI Overview click impact, update dates | backlinko.com/google-ctr-stats; ahrefs.com/blog/ai-overviews-reduce-clicks-update; searchenginejournal.com/google-algorithm-history | Tier 3 (named sources) |
| The audit and refresh model | `SEO_003_audit_and_refresh_model.xlsx` | Tier 2 |
| Budget, roadmap, month-12 targets | Labeled assumptions in the workbook | Tier 0 |
| Past work reversing a link-driven drop and reporting on GA4 and CRM | Stated here; sanitized exports available in a walkthrough | Tier 0 as submitted |

## Number source labels

Every paragraph with numbers opens with [Observed], [Estimated], [Benchmarked] or [Assumed], and a number with a different source carries its own label. Workbook cells carry the same labels in a column next to them. Numbers in the page table are [Observed] from the fixture, `evidence/content_audit_sample.csv`.

## AI usage disclosure

Tools: Claude (Anthropic) in Claude Code with the DataForSEO connector. What AI did: read the fixture and wrote the analysis script, worked out the decline breakdown and correlations, pulled the live SERPs and the Ramp and Brex data, built the workbook, and drafted this document from my framing and corrections, in my voice. What I decided: conversions as the KPI, the order of the diagnosis, the eight rules and thresholds, each page's decision and priority, where to fight Ramp, the budget split, and not promising 140K. What I checked: every fixture number in the workbook against `evidence/content_audit_sample.csv`, the correlations against the script output, the SERP results against my own searches, and the workbook recalculation ([Observed] all formulas, zero errors). Known weak spots: the click curve past position 10 is assumed, a correlation on 18 rows shows direction rather than precision, and the month-12 target is an estimate until the holdout gives a measured uplift.

## What breaks it (failure handling)

Traffic numbers turn out to be tool estimates and Search Console shows a different shape: re-run the diagnosis on Search Console in week one before anything ships. A step down inside a spam update window: the link audit goes ahead of the refreshes and a targeted disavow is considered. No last-modified dates in the export: Wayback Machine for the top 100 ([Assumed] cut-off), publish date for the rest. Conversions cannot be tied to landing pages: fix GA4 and the CRM first, no page-level KPI until then. Refreshed pages do not beat the holdout: stop at 24 and go back to the data. The sprint slips: redirects go live through a plugin, speed work stays with the contractor, the comparison template waits. Lead quality shows the Ramp comparison conversions are Ramp customers: the page keeps its SEO priority and loses its conversion weight. Detection is the weekly check of the five indicators in Roadmap_12_Months.

## What stays human

Agreeing the KPI with the VP and telling leadership that 140K [Observed] is the wrong number (the Targets_Month_12 sheet in `SEO_003_audit_and_refresh_model.xlsx` shows why). Every Kill and Consolidate before a redirect goes live. Any disavow. Which Ramp battles to fight. Publishing anything built on customer spend data (legal and privacy sign-off). Hiring. Reading the holdout and deciding whether the refresh program continues. AI drafts, scores and monitors. It does not decide what gets removed or what we promise.

## Artifact access

Everything is in the submission folder, no login needed. [Observed] Files: `SEO_003_audit_and_refresh_model.xlsx` (Excel or LibreOffice, yellow cells are inputs); the fixture `evidence/content_audit_sample.csv` (checksum above); the outputs and pulls listed in the evidence log; `scripts/analyze_fixture.py` and `scripts/build_workbook.py`. To reproduce: `python3 -I scripts/analyze_fixture.py evidence/content_audit_sample.csv evidence/` then `python3 -I scripts/build_workbook.py evidence/ out.xlsx` (needs scipy and openpyxl). DataForSEO task ids can be re-checked in any DataForSEO account.
