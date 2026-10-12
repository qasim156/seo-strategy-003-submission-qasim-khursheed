#!/usr/bin/env python3
"""Builds the operating artifact: SEO_003_audit_and_refresh_model.xlsx (plain-language version).
Usage: python3 -I build_workbook.py <evidence-dir> <out.xlsx>
Every sheet: row 1 title, row 2 what the sheet tells you, row 4 table header, data from row 5.
"""
import csv, json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EV = Path(sys.argv[1]); OUT = Path(sys.argv[2])
rows = list(csv.DictReader(open(EV / "triage_table.csv", newline="")))
summary = json.loads((EV / "analysis_output.json").read_text())
serp = list(csv.DictReader(open(EV / "live_serp_observations_2026-10-12.csv", newline="")))
ramp = list(csv.DictReader(open(EV / "ramp_com_historical_rank_overview_2026-10-12.csv", newline="")))
links = list(csv.DictReader(open(EV / "competitor_link_velocity_2026-10-12.csv", newline="")))

F = "Arial"
BLUE = Font(name=F, color="0000FF", size=10); BLACK = Font(name=F, size=10); BOLD = Font(name=F, bold=True, size=10)
TITLE = Font(name=F, bold=True, size=13); NOTE = Font(name=F, italic=True, size=10, color="404040")
HDR_FILL = PatternFill("solid", fgColor="1F3864"); HDR_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
YELLOW = PatternFill("solid", fgColor="FFFF00"); GREY = PatternFill("solid", fgColor="F2F2F2")
DEC_FILL = {"Protect": "E2EFDA", "Refresh": "FFF2CC", "Consolidate": "DDEBF7", "Kill": "F8CBAD"}
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BFBFBF"); BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HR, DR = 4, 5  # header row, first data row

wb = Workbook(); wb.remove(wb.active)

def sheet(name, title, tells, widths):
    ws = wb.create_sheet(name)
    ws.cell(row=1, column=1, value=title).font = TITLE
    c = ws.cell(row=2, column=1, value="What this sheet tells you: " + tells); c.font = NOTE; c.alignment = WRAP
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(4, min(len(widths), 8)))
    ws.row_dimensions[2].height = 34
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws

def header(ws, r, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=r, column=i, value=c)
        cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.alignment = Alignment(wrap_text=True, vertical="center"); cell.border = BORDER
    ws.row_dimensions[r].height = 32

def put(ws, r, c, v, font=BLACK, fmt=None, fill=None, wrap=False):
    cell = ws.cell(row=r, column=c, value=v); cell.font = font; cell.border = BORDER
    if fmt: cell.number_format = fmt
    if fill: cell.fill = fill
    if wrap: cell.alignment = WRAP
    return cell

def note(ws, r, text, cols=8, height=48):
    c = ws.cell(row=r, column=1, value=text); c.font = BLACK; c.alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=cols); ws.row_dimensions[r].height = height

# ================================================================== Start_Here
ws = sheet("Start_Here", "SEO recovery plan: audit and refresh model", "how to read this workbook, in what order, and what the colors mean.", [118])
lines = [
    ("Beat Claude challenge SEO Strategy 003, brief version 2026-07. Prepared by Qasim Khursheed, October 2026.", BLACK),
    (f"Fixture: content_audit_sample.csv, SHA-256 {summary['fixture_sha256']}", BLACK),
    ("", BLACK),
    ("Read in this order", BOLD),
    ("1. Why_Traffic_Dropped: where the lost traffic went and what the data tested.", BLACK),
    ("2. Page_Triage: every page in the fixture with its decision (Protect, Refresh, Consolidate, Kill), the rule behind it, priority, what we do and what to watch out for.", BLACK),
    ("3. Triage_Rules: the eight rules in order. Change a threshold here if you disagree with it.", BLACK),
    ("4. Topics: which topics bring conversions, so new content and links go there first.", BLACK),
    ("5. Plan_90_Days: what happens each week, who owns it, what you can see at the end of it.", BLACK),
    ("6. Roadmap_12_Months: the four quarters and the five 90-day indicators with what we do if they do not move.", BLACK),
    ("7. Budget: the $15,000 a month split, and how many posts that buys.", BLACK),
    ("8. Targets_Month_12: low, base and stretch month-12 targets for traffic and conversions, every assumption in an editable cell.", BLACK),
    ("Evidence sheets, for when you want to check a number: Data_To_Request (what we ask for in week one), Live_SERPs (who ranks today), Competitors (Ramp and Brex footprint and link pace), Ref_CTR_Curve (the click-through curve used in Page_Triage).", BLACK),
    ("", BLACK),
    ("Colors", BOLD),
    ("Blue text = a number typed in from the fixture, the brief or a live tool pull. Black = a formula. Yellow fill = an assumption you can change. Green, yellow, blue and red row fills in Page_Triage = Protect, Refresh, Consolidate, Kill.", BLACK),
    ("", BLACK),
    ("Number labels", BOLD),
    ("[Observed] from the fixture, the brief or a live tool pull. [Estimated] my estimate with the reasoning next to it. [Benchmarked] a named outside source. [Assumed] a placeholder to make the plan concrete.", BLACK),
    ("", BLACK),
    ("Limits of the data", BOLD),
    ("18 pages is the top of the site, not a fair sample. Conversions cover 90 days while traffic is monthly. The fixture does not say whether traffic is GA4 sessions or a tool estimate. There are no last-year conversions, so we cannot see how conversions moved when rankings moved.", BLACK),
]
for i, (t, f) in enumerate(lines, 4):
    c = ws.cell(row=i, column=1, value=t); c.font = f; c.alignment = WRAP

# ================================================================== Ref_CTR_Curve (built early: Page_Triage formulas point here)
wc = sheet("Ref_CTR_Curve", "Click-through rate by Google position", "the share of clicks a page gets at each position. Page_Triage uses it to work out how much traffic a rank drop should have cost.", [12, 20, 16, 90])
header(wc, HR, ["Position", "Click rate", "Label", "Source"])
ctr = [(1, .398), (2, .187), (3, .102), (4, .072), (5, .051), (6, .044), (7, .030), (8, .021), (9, .019), (10, .016)]
r = DR
for p, v in ctr:
    put(wc, r, 1, p, BLUE); put(wc, r, 2, v, BLUE, "0.0%", YELLOW); put(wc, r, 3, "[Benchmarked]")
    put(wc, r, 4, "FirstPageSage curve as cited by Backlinko, backlinko.com/google-ctr-stats (updated April 2025). Backlinko's own #1 figure is 27.6%; the model uses the ratio between positions, so the curve choice shifts the numbers a little and the conclusions not at all." if p == 1 else "", wrap=True)
    r += 1
for p in range(11, 42):
    v = round(0.012 - (p - 11) * 0.0007, 4) if p <= 20 else (0.003 if p <= 30 else 0.0015)
    put(wc, r, 1, p, BLUE); put(wc, r, 2, v, BLUE, "0.00%", YELLOW); put(wc, r, 3, "[Assumed]")
    put(wc, r, 4, "Page 2 and beyond is assumed. Most studies stop at position 10. Change these cells if you have better data." if p == 11 else "", wrap=True)
    r += 1
CTR_LAST = r - 1
wc.freeze_panes = wc.cell(row=DR, column=1)

# ================================================================== Page_Triage
wt = sheet("Page_Triage", "Every page: what happened to it and what we do",
           "one row per fixture page. Blue columns are the fixture. Black columns are worked out. The Decision, Rule, Priority, What we do and Watch out columns are the plan for that page.",
           [36, 28, 10, 9, 10, 11, 11, 11, 10, 10, 10, 9, 10, 10, 11, 11, 26, 34, 12, 42, 8, 58, 58, 34, 14, 14])
put(wt, 3, 1, "Today, for the page-age calculation", BOLD); put(wt, 3, 2, "2026-07", BLUE, fill=YELLOW); put(wt, 3, 3, "[Assumed] the brief version date")
put(wt, 3, 5, "Site traffic now", BOLD); put(wt, 3, 6, 85000, BLUE, "#,##0", YELLOW); put(wt, 3, 7, "12 months ago", BOLD); put(wt, 3, 8, 140000, BLUE, "#,##0", YELLOW); put(wt, 3, 9, "[Observed] brief")
cols = ["URL", "Target keyword", "Position 12 months ago", "Position now", "Positions lost (+ means it fell)", "Traffic 12 months ago", "Traffic now (monthly)",
        "Traffic change", "Traffic change %", "Share of the sample's lost traffic", "Referring domains", "Published", "Last updated", "Months since last update",
        "Conversions (90 days)", "Conversions per 1,000 visits", "Topic", "Why it dropped", "Decision", "Rule that fired", "Priority", "What we do", "Watch out",
        "Fixture note", "Expected traffic at the new position (click curve)", "Traffic change the rank move does not explain"]
header(wt, HR, cols)
first = DR
for i, x in enumerate(rows):
    r = first + i
    put(wt, r, 1, x["url_slug"], BLUE); put(wt, r, 2, x["target_keyword"], BLUE)
    put(wt, r, 3, int(x["position_12mo_ago"]), BLUE); put(wt, r, 4, int(x["position_now"]), BLUE)
    put(wt, r, 5, f"=D{r}-C{r}")
    put(wt, r, 6, int(x["traffic_12mo_ago"]), BLUE, "#,##0"); put(wt, r, 7, int(x["traffic_now_monthly"]), BLUE, "#,##0")
    put(wt, r, 8, f"=G{r}-F{r}", fmt="#,##0;(#,##0);-"); put(wt, r, 9, f"=IF(F{r}=0,0,H{r}/F{r})", fmt="0.0%")
    put(wt, r, 10, f"=IF($H${first+len(rows)}=0,0,H{r}/$H${first+len(rows)})", fmt="0.0%")
    put(wt, r, 11, int(x["referring_domains"]), BLUE); put(wt, r, 12, str(x["publish_year"]), BLUE); put(wt, r, 13, x["last_updated"], BLUE)
    put(wt, r, 14, f'=(VALUE(LEFT($B$3,4))-VALUE(LEFT(M{r},4)))*12+(VALUE(RIGHT($B$3,2))-VALUE(RIGHT(M{r},2)))')
    put(wt, r, 15, int(x["conversions_90d"]), BLUE); put(wt, r, 16, f"=IF(G{r}=0,0,1000*O{r}/(3*G{r}))", fmt="0.00")
    put(wt, r, 17, x["topic"], wrap=True); put(wt, r, 18, x["cause_bucket"], wrap=True)
    put(wt, r, 19, x["triage_bucket"], BOLD, fill=PatternFill("solid", fgColor=DEC_FILL[x["triage_bucket"]]))
    put(wt, r, 20, x["triage_rule"], wrap=True); put(wt, r, 21, x["priority"])
    put(wt, r, 22, x["action"], wrap=True); put(wt, r, 23, x["face_value_flag"], wrap=True); put(wt, r, 24, x["notes"], BLUE, wrap=True)
    put(wt, r, 25, f"=ROUND(F{r}*INDEX(Ref_CTR_Curve!$B${DR}:$B${CTR_LAST},MATCH(D{r},Ref_CTR_Curve!$A${DR}:$A${CTR_LAST},0))/INDEX(Ref_CTR_Curve!$B${DR}:$B${CTR_LAST},MATCH(C{r},Ref_CTR_Curve!$A${DR}:$A${CTR_LAST},0)),0)", fmt="#,##0")
    put(wt, r, 26, f"=G{r}-Y{r}", fmt="#,##0;(#,##0);-")
    wt.row_dimensions[r].height = 80
tr = first + len(rows)
put(wt, tr, 1, "TOTAL (18 pages)", BOLD)
for c, letter in ((6, "F"), (7, "G"), (8, "H"), (15, "O")):
    put(wt, tr, c, f"=SUM({letter}{first}:{letter}{tr-1})", BOLD, "#,##0;(#,##0);-")
put(wt, tr, 9, f"=H{tr}/F{tr}", BOLD, "0.0%"); put(wt, tr, 10, f"=SUM(J{first}:J{tr-1})", BOLD, "0.0%"); put(wt, tr, 16, f"=1000*O{tr}/(3*G{tr})", BOLD, "0.00")
TF, TL, TT = first, tr - 1, tr
s0 = tr + 2
put(wt, s0, 1, "Quick checks", BOLD)
checks = [
    ("Sample traffic change", f"=I{tr}", "0.0%"), ("Site traffic change (brief)", "=(F3-H3)/H3", "0.0%"),
    ("Sample share of site traffic now", f"=G{tr}/F3", "0.0%"), ("Sample share of site traffic 12 months ago", f"=F{tr}/H3", "0.0%"),
    ("Sample change without the branded page", f'=(SUMIF(B{first}:B{tr-1},"<>company brand expense software",G{first}:G{tr-1})-SUMIF(B{first}:B{tr-1},"<>company brand expense software",F{first}:F{tr-1}))/SUMIF(B{first}:B{tr-1},"<>company brand expense software",F{first}:F{tr-1})', "0.0%"),
    ("Pages marked Protect", f'=COUNTIF(S{first}:S{tr-1},"Protect")', None), ("Pages marked Refresh", f'=COUNTIF(S{first}:S{tr-1},"Refresh")', None),
    ("Pages marked Consolidate", f'=COUNTIF(S{first}:S{tr-1},"Consolidate")', None), ("Pages marked Kill", f'=COUNTIF(S{first}:S{tr-1},"Kill")', None),
    ("Conversions on the two comparison pages", f'=SUMIF(A{first}:A{tr-1},"/compare/*",O{first}:O{tr-1})', None),
    ("Share of conversions from the top 4 pages", f"=(LARGE(O{first}:O{tr-1},1)+LARGE(O{first}:O{tr-1},2)+LARGE(O{first}:O{tr-1},3)+LARGE(O{first}:O{tr-1},4))/O{tr}", "0.0%"),
    ("Traffic lost on pages with zero conversions", f"=SUMIF(O{first}:O{tr-1},0,H{first}:H{tr-1})", "#,##0;(#,##0);-"),
    ("...as a share of all lost traffic", f"=SUMIF(O{first}:O{tr-1},0,H{first}:H{tr-1})/H{tr}", "0.0%"),
]
for i, (label, formula, fmt) in enumerate(checks, s0 + 1):
    put(wt, i, 1, label); put(wt, i, 2, formula, fmt=fmt)
note(wt, s0 + len(checks) + 2, "The last two columns (Y and Z) are the click-curve check: Y is what last year's traffic should have become at the new position; Z is traffic now minus Y. A big negative Z means the page lost clicks for a reason other than rank (an AI Overview, a changed SERP). Only receipt-scanning-app shows that.", cols=8, height=50)
wt.freeze_panes = wt.cell(row=DR, column=3)

# ================================================================== Why_Traffic_Dropped
wd = sheet("Why_Traffic_Dropped", "Where the lost traffic went, and what the data says caused it",
           "the sample's lost traffic split by cause, then the questions we tested on the data and what each one found, in plain words.",
           [46, 16, 12, 56, 60, 44])
header(wd, HR, ["Cause", "Lost traffic (sum of Page_Triage rows)", "Share", "Pages", "What it means", "Fix"])
causes = [
    ("A. Dated URL expired", "per-diem-rates-2022, quarterly-tax-deadlines-2023", "Two year-stamped URLs lost 12,510 visits between them. The year in the URL expired. This is not decay, competition or a penalty.", "Redirect to evergreen URLs. Refresh on a calendar. No other spend."),
    ("B. Head term", "what-is-expense-management, expense-management-guide, business-expense-categories, corporate-card-vs-credit-card", "The three head terms and the cannibal lost 16,500. Live SERPs show an AI Overview above every result and competitors updated in 2026. Our pages were last touched 2023-11 to 2024-08.", "Refresh for depth and citation, merge the cannibal, accept a ceiling where the AI Overview sits."),
    ("C. Off-core, outranked by aggregators / thin", "accounting-software-list, bookkeeping-basics", "Bookkeeping and accounting software lists. Zero conversions, under 10 referring domains each.", "Remove. Not our battle."),
    ("D. Stale rules content", "mileage-reimbursement-guide", "Mileage rules changed; the page was last updated 2022-11.", "Refresh with the current rate in a block that can be quoted."),
    ("E. SERP feature at stable rank", "receipt-scanning-app", "Held #5 and still lost 31%. The live SERP has an AI Overview and consumer cashback intent.", "Refresh for citation rather than rank. Accept lower traffic."),
    ("F. High-intent compare page slipping", "vs-ramp", "Slid 6 to 11. Small traffic, 22% of all conversions.", "Rebuild first. Highest conversion lever on the site."),
    ("G. Link asset drifting", "expense-fraud-statistics", "74 referring domains, statistics from 2023.", "Yearly stat refresh. Internal link source for the comparison pages."),
    ("H. Stable", "expense-report-template, what-is-an-invoice, vs-brex", "Within noise.", "Leave alone."),
    ("I. Gainers", "travel-expense-policy, what-is-spend-management, branded page", "Updated 2025-01, a new cluster, and branded demand.", "Build around them. Report the branded page separately."),
]
for i, (k, pages, meaning, fix) in enumerate(causes, DR):
    put(wd, i, 1, k); put(wd, i, 2, f'=SUMIF(Page_Triage!$R${TF}:$R${TL},"{k}*",Page_Triage!$H${TF}:$H${TL})', fmt="#,##0;(#,##0);-")
    put(wd, i, 3, f"=B{i}/Page_Triage!$H${TT}", fmt="0.0%"); put(wd, i, 4, pages, wrap=True); put(wd, i, 5, meaning, wrap=True); put(wd, i, 6, fix, wrap=True)
    wd.row_dimensions[i].height = 52
tot = DR + len(causes)
put(wd, tot, 1, "Check: adds up to", BOLD); put(wd, tot, 2, f"=SUM(B{DR}:B{tot-1})", BOLD, "#,##0;(#,##0);-"); put(wd, tot, 3, f"=SUM(C{DR}:C{tot-1})", BOLD, "0.0%")
note(wd, tot + 2, "Two kinds of drop. The head terms slid 2 to 5 positions: that is competition. Four pages fell 17 to 38 positions (per diem 5 to 29, tax deadlines 3 to 41, accounting list 10 to 34, bookkeeping 14 to 31): that is expiry and off-topic content, and links do not fix it.", cols=6, height=44)
q0 = tot + 4
put(wd, q0, 1, "What we tested on the 18 pages", BOLD)
header(wd, q0 + 1, ["Question", "Result (correlation, -1 to +1)", "Strength", "What it means", "Cross-check (Pearson, live formula on Page_Triage)", "Pair tested"])
C = summary["correlations"]
def strength(rho, p):
    a = abs(rho)
    return ("strong" if a >= 0.7 else "moderate" if a >= 0.4 else "weak") + (" and reliable" if p < 0.05 else ", could be chance")
tests = [
    ("Did the pages that dropped lose conversions?", "position_delta_vs_conversions_90d", "E", "O", "Pages that fell furthest have the fewest conversions, but they are the dated and off-topic pages that never converted. There are no last-year conversions in the fixture, so we cannot measure conversion change from this file. Needs GA4 by landing page for both years.", "positions lost vs conversions"),
    ("Do more referring domains mean a better position today?", "referring_domains_vs_position_now", "K", "D", "Yes. More links, better current position. Authority sets the floor.", "referring domains vs position now"),
    ("Did referring domains protect pages from falling?", "referring_domains_vs_position_delta", "K", "E", "No. The four pages with 50+ referring domains (84, 74, 61, 52) all fell, and they fell the least (2 to 5 places). The two gainers have 26 and 11. Once page age is held constant, link counts add nothing (partial correlation -0.07; age with links held constant: 0.80). What this file cannot see: link quality, links lost during the year, or competitors out-building us. Quietly neutralized links would look like the same slow slide on the head terms. The week-one audit (new and lost by month, anchors, DR spread, manual actions report) settles it and decides the order of Q1.", "referring domains vs positions lost"),
    ("Do referring domains bring conversions?", "referring_domains_vs_conversions_90d", "K", "O", "Only through traffic. Against conversions per 1,000 visits the link is 0.40 and could be chance. The best converting pages (comparisons) have 17 to 19 referring domains. Intent converts, links do not.", "referring domains vs conversions"),
    ("Does a better position mean more conversions?", "position_now_vs_conversions_90d", "D", "O", "Yes, through traffic. The exception is the comparison pages: #8 and #11 with 10 to 13 conversions per 1,000 visits.", "position now vs conversions"),
    ("Did older pages fall further?", "months_since_update_vs_position_delta", "N", "E", "Strongest signal in the file. The older the last update, the bigger the fall. Pages that fell: 39 months since update on average. Pages that held: 21. Nothing in the sample updated since 2025-01.", "months since update vs positions lost"),
    ("Did older pages lose more traffic?", "months_since_update_vs_traffic_change_pct", "N", "I", "Same story in traffic terms.", "months since update vs traffic change %"),
    ("Does traffic predict conversions?", "traffic_now_vs_conversions_90d", "G", "O", "Loosely. 2,900 visits on the invoice page produce 0. 1,100 on the Ramp comparison produce 44. Traffic is the wrong KPI.", "traffic now vs conversions"),
]
for i, (q, key, ca, cb, meaning, pair) in enumerate(tests, q0 + 2):
    put(wd, i, 1, q, wrap=True); put(wd, i, 2, C[key]["rho"], fmt="0.00"); put(wd, i, 3, strength(C[key]["rho"], C[key]["p"]), wrap=True)
    put(wd, i, 4, meaning, wrap=True); put(wd, i, 5, f"=CORREL(Page_Triage!{ca}{TF}:{ca}{TL},Page_Triage!{cb}{TF}:{cb}{TL})", fmt="0.00"); put(wd, i, 6, pair, wrap=True)
    wd.row_dimensions[i].height = 70
e = q0 + 2 + len(tests)
note(wd, e, "Method: Spearman rank correlation from scripts/analyze_fixture.py (included). A correlation of 1.0 is a perfect match, 0 is no relationship, negative means they move in opposite directions. With 18 pages, read these as direction and rough strength. 'Reliable' means a p-value under 0.05. Column E is a live Pearson cross-check that moves if you edit Page_Triage.", cols=6, height=50)
g0 = e + 2
put(wd, g0, 1, "Pages that fell vs pages that held", BOLD)
header(wd, g0 + 1, ["Group", "Pages", "Conversions (90 days)", "Traffic now", "Average months since update", ""])
G = summary["groups"]
put(wd, g0 + 2, 1, "Fell"); put(wd, g0 + 2, 2, f'=COUNTIF(Page_Triage!E{TF}:E{TL},">0")'); put(wd, g0 + 2, 3, f'=SUMIF(Page_Triage!E{TF}:E{TL},">0",Page_Triage!O{TF}:O{TL})'); put(wd, g0 + 2, 4, f'=SUMIF(Page_Triage!E{TF}:E{TL},">0",Page_Triage!G{TF}:G{TL})', fmt="#,##0"); put(wd, g0 + 2, 5, G["pages_that_fell"]["median_months_since_update"])
put(wd, g0 + 3, 1, "Held or gained"); put(wd, g0 + 3, 2, f'=COUNTIF(Page_Triage!E{TF}:E{TL},"<=0")'); put(wd, g0 + 3, 3, f'=SUMIF(Page_Triage!E{TF}:E{TL},"<=0",Page_Triage!O{TF}:O{TL})'); put(wd, g0 + 3, 4, f'=SUMIF(Page_Triage!E{TF}:E{TL},"<=0",Page_Triage!G{TF}:G{TL})', fmt="#,##0"); put(wd, g0 + 3, 5, G["pages_that_held_or_gained"]["median_months_since_update"])
put(wd, g0 + 4, 1, "Months since update is the median from the script.")

# ================================================================== Triage_Rules
wr = sheet("Triage_Rules", "The eight rules, in order", "how each page gets its decision. The first rule that fits wins. Yellow cells are thresholds you can change.", [8, 64, 14, 30, 10, 76])
header(wr, HR, ["Order", "Rule", "Decision", "Threshold", "Value", "Why"])
rules = [
    ("R1", "Two pages target the same keyword (cannibal)", "Consolidate", "", "", "Two URLs splitting one query never both win. Merge the unique parts and redirect the weaker one."),
    ("R2", "The URL has a year in it", "Consolidate", "", "", "The URL expires with the year. Redirect to an evergreen URL and refresh on a calendar. Refreshing the dated URL is wasted."),
    ("R3", "Off-topic AND zero conversions AND few referring domains AND lost many positions", "Kill", "Max referring domains / min positions lost", "10 / 15", "No revenue, no links, no rank. Remove it, or redirect to the nearest hub only if the links are from real sites."),
    ("R4", "Conversion page: conversions per 1,000 visits at or above the threshold, or a branded query", "Protect", "Min conversions per 1,000 visits", 2.0, "These pages pay for the program. Keep the URL, light update, stronger CTA, point internal links at it."),
    ("R5", "Holding or gaining rank AND updated recently", "Protect", "Max months since update", 24, "Working pages are left alone. Build the cluster around them."),
    ("R6", "Traffic with no product relevance", "Protect", "", "", "Keep it, spend nothing, test one CTA. Never report it as a win."),
    ("R7", "Lost positions, or old, on a core topic", "Refresh", "Max months since update", 18, "Full refresh, same URL, check intent and SERP format again. Pages with 70+ referring domains are never redirected."),
    ("R8", "Anything else", "Protect", "", "", "Check monthly."),
]
for i, (o, rule, b, th, val, why) in enumerate(rules, DR):
    put(wr, i, 1, o); put(wr, i, 2, rule, wrap=True); put(wr, i, 3, b, fill=PatternFill("solid", fgColor=DEC_FILL[b]))
    put(wr, i, 4, th, wrap=True); put(wr, i, 5, val, BLUE, fill=YELLOW if val != "" else None); put(wr, i, 6, why, wrap=True); wr.row_dimensions[i].height = 40
note(wr, DR + len(rules) + 1, "Running this on all 400 posts: export URL, target keyword, position now and 12 months ago, Search Console clicks, referring domains, last-modified date and GA4 conversions. Paste into Page_Triage. Apply R1 to R8 in order. A person reviews every Kill and Consolidate before any redirect goes live.", cols=6, height=48)

# ================================================================== Topics
wtp = sheet("Topics", "Which topics bring conversions", "traffic and conversions grouped by topic, so new content and links go to the topics that convert first.", [40, 8, 13, 16, 10, 14, 16, 14, 80])
header(wtp, HR, ["Topic", "Pages", "Traffic now", "Traffic 12 months ago", "Change %", "Conversions (90 days)", "Conversions per 1,000 visits", "Referring domains", "Where it sits in the plan"])
topic_plan = {
    "Comparisons and alternatives": "Fight. First priority for conversion. Rebuild vs-ramp, align vs-brex, add 2 comparison pages and an alternatives page. Links and internal links point here.",
    "Branded": "Report separately. This is branded demand.",
    "Corporate cards": "Fight for conversions rather than rank. Banks own the SERP. Protect the page and build the card decision content around it.",
    "Expense management core": "Fight on depth and freshness. The head terms, templates and policy pages. Refresh the fallen ones, extend the spend management cluster, put a template or tool on every page.",
    "Rates and deadlines (compliance utility)": "Flank cheaply. Evergreen URLs, refresh on a calendar, no new investment. Government owns the rates SERPs.",
    "Data and statistics (link assets)": "Flank. One data study a quarter from anonymized product data. Yearly refresh of the fraud page. This is where links come from.",
    "Off-core finance education": "Concede. Kill the thin pages, leave the invoice page alone. Aggregators and accounting software own these SERPs.",
}
order = ["Comparisons and alternatives", "Corporate cards", "Expense management core", "Data and statistics (link assets)", "Rates and deadlines (compliance utility)", "Off-core finance education", "Branded"]
for i, t in enumerate(order, DR):
    rng = lambda col: f"Page_Triage!${col}${TF}:${col}${TL}"
    put(wtp, i, 1, t); put(wtp, i, 2, f'=COUNTIF({rng("Q")},A{i})')
    put(wtp, i, 3, f'=SUMIF({rng("Q")},A{i},{rng("G")})', fmt="#,##0"); put(wtp, i, 4, f'=SUMIF({rng("Q")},A{i},{rng("F")})', fmt="#,##0")
    put(wtp, i, 5, f"=IF(D{i}=0,0,(C{i}-D{i})/D{i})", fmt="0.0%"); put(wtp, i, 6, f'=SUMIF({rng("Q")},A{i},{rng("O")})')
    put(wtp, i, 7, f"=IF(C{i}=0,0,1000*F{i}/(3*C{i}))", fmt="0.00"); put(wtp, i, 8, f'=SUMIF({rng("Q")},A{i},{rng("K")})')
    put(wtp, i, 9, topic_plan[t], wrap=True); wtp.row_dimensions[i].height = 45
tt = DR + len(order)
put(wtp, tt, 1, "Check", BOLD); put(wtp, tt, 2, f"=SUM(B{DR}:B{tt-1})", BOLD); put(wtp, tt, 3, f"=SUM(C{DR}:C{tt-1})", BOLD, "#,##0"); put(wtp, tt, 6, f"=SUM(F{DR}:F{tt-1})", BOLD)
note(wtp, tt + 2, "Two comparison pages with 2,000 visits produce 72 of the 200 conversions. Seven core expense management pages with 20,450 visits produce 42. Topic authority still matters (the core cluster carries 246 of the sample's referring domains), but the money is in comparisons, cards and templates. The missing piece is lead quality: 44 conversions on vs-ramp could be Ramp's own customers. Pipeline by landing page from the CRM decides the final order.", cols=9, height=60)

# ================================================================== Plan_90_Days
wp = sheet("Plan_90_Days", "The first 90 days, week by week", "what ships each week, who owns it, what you can look at when it is done, and what it depends on.", [8, 72, 24, 46, 36])
header(wp, HR, ["Week", "What ships", "Owner", "What you can see when it is done", "Depends on"])
plan = [
    ("1", "KPI conversation with the VP; all Data_To_Request items sent; rank tracking live; Page_Triage loaded with the fixture rules", "Head of SEO, SEO Specialist", "Agreed KPI definition; data requests logged; rank tracker screenshot", "VP availability"),
    ("2", "Search Console 16-month series lined up with the update calendar; link audit (new and lost by month, anchors, DR spread); branded page moved out of the SEO baseline", "SEO Specialist", "One-page diagnosis note: step change or slow slide, link problem yes or no", "Week 1 data"),
    ("3", "Redirect map for the two dated URLs and the cannibal; removal decisions for the two off-topic pages; a person reviews every Kill and Consolidate", "SEO Specialist, Content Manager", "Redirect map (old URL, new URL, reason, referring domains carried)", "Link audit (check the links on the kills)"),
    ("3-4", "vs-ramp rebuilt: pricing and feature table, honest tradeoffs, CTA; vs-brex aligned to the same format", "Content Manager, CRO contractor", "New page live; conversion tracking on the CTA verified", "Product marketing for pricing facts"),
    ("3-5", "what-is-expense-management refreshed for depth and AI Overview citation, brief built in Clearscope against the current top 10; cannibal merged and redirected", "Content Manager, freelancer", "Refreshed URL live; Clearscope score on the new draft; Search Console URL filter saved for the holdout", "Redirect map"),
    ("4", "Holdout chosen: 20 pages to refresh in weeks 5 to 12 and 20 similar pages left alone; the matching rule written down", "SEO Specialist", "Holdout list with the matching rule (similar traffic, position and age)", "Full 400-post export"),
    ("5-8", "P2 refreshes: business expense categories (plus downloadable sheet), mileage guide, corporate card light update and CTA, template page download-to-signup test; 4 new posts in the spend management cluster", "Content Manager, freelancers", "8 refreshes and 4 new posts live; CTA test running", "Sprint 1 for the download flow (or a plugin fallback)"),
    ("6-10", "Sprint 1 ships: blog template speed, redirect map deployed, related-posts and in-content link module", "Engineering, WordPress contractor", "PageSpeed lab LCP under 2.5s on the blog template; redirects returning 301; link module live", "Engineering sprint slot"),
    ("9-12", "P3 refreshes (receipt scanning for citation, fraud statistics yearly update); internal links from the two strongest blog pages into the comparison hub; first batch of relevant-domain outreach aimed at the refreshed guides; data study #1 scoped with product and legal", "Content Manager, SEO Specialist", "8 more refreshes live; internal link map; outreach list with relevance notes; data study brief", "Legal sign-off on anonymized spend data"),
    ("12-13", "90-day review: the five indicators in Roadmap_12_Months against their targets; continue, pivot or re-diagnose using the pre-agreed rules", "Head of SEO, VP Marketing", "90-day note with the indicator table and the decision", "8 weeks of indexed refresh data"),
]
for i, (w, s_, o, out, dep) in enumerate(plan, DR):
    put(wp, i, 1, w); put(wp, i, 2, s_, wrap=True); put(wp, i, 3, o, wrap=True); put(wp, i, 4, out, wrap=True); put(wp, i, 5, dep, wrap=True); wp.row_dimensions[i].height = 62
note(wp, DR + len(plan) + 1, "Throughout: 4 new posts a month minimum (the brief's floor), a weekly rank and Search Console check, and a monthly note on which pages lost, which gained, what changed on theirs and what changed on ours. Weeks are indicative [Assumed]; the last column says what moves them.", cols=5, height=45)
wp.freeze_panes = wp.cell(row=DR, column=1)

# ================================================================== Roadmap_12_Months
wro = sheet("Roadmap_12_Months", "The four quarters and the 90-day indicators", "what ships each quarter, which engineering sprint it needs, the milestone, then the five numbers we watch at 90 days and what we do if each one does not move.", [14, 70, 50, 60, 12])
header(wro, HR, ["Quarter", "Ships", "Engineering sprint (1 per quarter)", "Milestone", "Label"])
road = [
    ("Q1 (days 1 to 90)", "KPI reset with the VP; GA4 and CRM baseline by landing page; Search Console trend on the update calendar; link audit; P1 then P2 pages; 4 new posts a month in the spend management cluster; refresh holdout (20 refreshed vs 20 left alone).",
     "Sprint 1: blog template speed (hero image, fonts, lazy loading, caching), redirect map, related-posts and in-content link module. Cut: INP work, redesign, any framework change.",
     "vs-ramp back in the top 8. what-is-expense-management top 3. Refreshed pages beating the holdout on impressions within 8 weeks. Comparison page conversion rate up 25%. Blog LCP under 2.5s in lab. 24 refreshes, 3 consolidations, 2 removals live.", "[Estimated]"),
    ("Q2 (months 4 to 6)", "Rules run on all 400 posts. 8 refreshes a month, consolidations by cluster. Data study #1 with outreach. Contextual link placements from relevant domains running at 6 to 10 a month, aimed at the refreshed guides. Comparison hub: vs-ramp, vs-brex, 2 new comparison pages, 1 alternatives page. Template library with download-to-signup.",
     "Sprint 2: comparison page template (tables, schema, CTA components), template download flow, sitemap and removal handling.",
     "100+ posts actioned. Organic conversions +40% to +60% on the Q1 baseline. Traffic 100K to 110K.", "[Estimated]"),
    ("Q3 (months 7 to 9)", "Refresh pipeline at full pace. Data study #2. First hire decision (content strategist or editor) once the 6-month freeze ends, only if refresh throughput is the bottleneck. Spend management cluster complete.",
     "Sprint 3: internal linking automation built as a reverse silo (guides up to topic hubs, hubs to the comparison and product pages, every link reciprocated), hub pages.",
     "250+ posts actioned. Organic conversions about +80%. Traffic 110K to 120K.", "[Estimated]"),
    ("Q4 (months 10 to 12)", "All 400 posts actioned. Yearly refresh calendar for rate and deadline pages. Yearly stat refresh on the fraud page. Holdout results and conversion lift reported.",
     "Sprint 4: reserve for whatever the data says (field vitals, schema, the next template).",
     "Base case: organic conversions about 2x baseline, traffic about 117K (low about 101K, stretch about 136K). 140K sits above the stretch case: the AI Overview on the head terms and the two expired URLs cap what the old pages can return; anything above comes from new clusters and templates.", "[Estimated]"),
]
for i, (q, s_, e_, m, l) in enumerate(road, DR):
    put(wro, i, 1, q, BOLD, wrap=True); put(wro, i, 2, s_, wrap=True); put(wro, i, 3, e_, wrap=True); put(wro, i, 4, m, wrap=True); put(wro, i, 5, l); wro.row_dimensions[i].height = 130
i0 = DR + len(road) + 1
put(wro, i0, 1, "The five 90-day indicators", BOLD)
header(wro, i0 + 1, ["Indicator", "Where we read it", "Target by day 90", "If it does not move", "Label"])
ind = [
    ("Positions: what is expense management, business expense categories, corporate card vs credit card, vs-ramp", "Ahrefs rank tracker, weekly, US desktop and mobile", "+2 positions on the first two; vs-ramp top 8; corporate card holds #5", "If the head terms do not move after 8 weeks indexed: the problem is format and authority, not freshness. Move Q2 refresh budget to the data study and change the page format (tools and templates over prose).", "[Estimated]"),
    ("Impressions and clicks on refreshed pages vs the untouched holdout", "Search Console, URL filter, 8-week window", "Refreshed group up 20%+ on impressions relative to the holdout", "If refreshed pages do not beat the holdout: stop the refresh program at 24 and re-diagnose from Search Console and the update calendar.", "[Estimated]"),
    ("Organic conversions on the comparison pages", "GA4 landing page plus CRM source", "+25% conversion rate on vs-ramp and vs-brex", "If the rebuilt page converts no better: the CTA and offer are the problem. Product marketing owns the offer; SEO stays on traffic.", "[Estimated]"),
    ("Index hygiene", "Search Console pages report, Ahrefs site audit", "Dated URLs redirected, cannibal merged, one URL per target keyword", "Binary. If not done it is a process failure, not a strategy failure.", "[Observed]"),
    ("Blog template LCP", "PageSpeed Insights lab, then CrUX field after 28 days", "Under 2.5s lab by day 60", "If the contractor cannot get there on WordPress: escalate to the Q2 sprint; do not spend Q1 sprint time on it twice.", "[Benchmarked] Google's 2.5s threshold"),
]
for i, (a, b, c_, d, e_) in enumerate(ind, i0 + 2):
    put(wro, i, 1, a, wrap=True); put(wro, i, 2, b, wrap=True); put(wro, i, 3, c_, wrap=True); put(wro, i, 4, d, wrap=True); put(wro, i, 5, e_, wrap=True); wro.row_dimensions[i].height = 80

# ================================================================== Budget
wbud = sheet("Budget", "The $15,000 a month, and what it buys", "the monthly split by line with the reasoning, and how many posts the budget covers in a year.", [50, 16, 14, 90])
header(wbud, HR, ["Line", "Monthly $", "Label", "Basis"])
budget = [
    ("Tools (Ahrefs, Clearscope, rank tracking)", 1000, "[Assumed]", "Existing tool stack per the brief. Prices change, so confirm against invoices."),
    ("New posts: 4 a month x $300", "=4*300", "[Observed]", "Brief: 4 posts a month minimum, 3 freelancers at $300 a post."),
    ("Refreshes: 8 a month x $200", "=8*200", "[Assumed]", "A refresh at two-thirds of a new post. Confirm with the freelancers; a heavy rewrite is a $300 job."),
    ("Digital PR and data study (freelancer retainer)", 2500, "[Assumed]", "One original data asset a quarter from anonymized, aggregated product data, pitched to finance and business press. No paid links at any price."),
    ("Contextual link outreach to relevant domains", 1500, "[Assumed]", "Editorial placements on finance, accounting, B2B software and business operations sites, pointing at the refreshed guides and comparison pages. Target 6 to 10 a month. No networks, no directories, no paid placements."),
    ("WordPress speed and template contractor", 2500, "[Assumed]", "Front-loaded in Q1 (speed, image pipeline, caching, related-posts module). Drops to maintenance by Q3; the saving moves to refreshes."),
    ("CRO and design for the comparison pages", 1500, "[Assumed]", "Comparison tables, CTAs, template downloads. Mainly Q1 and Q2."),
    ("Automation and AI tooling, misc", 700, "[Assumed]", "Triage sheet automation, rank alerts, brief generation."),
    ("Reserve", 2500, "[Assumed]", "Held for the Q3 data study or a fix that cannot wait for the sprint."),
]
for i, (l, v, lab, basis) in enumerate(budget, DR):
    put(wbud, i, 1, l); put(wbud, i, 2, v, BLUE, "$#,##0", YELLOW); put(wbud, i, 3, lab); put(wbud, i, 4, basis, wrap=True); wbud.row_dimensions[i].height = 32
b_tot = DR + len(budget)
put(wbud, b_tot, 1, "Total", BOLD); put(wbud, b_tot, 2, f"=SUM(B{DR}:B{b_tot-1})", BOLD, "$#,##0")
put(wbud, b_tot + 1, 1, "Budget cap (brief)", BOLD); put(wbud, b_tot + 1, 2, 15000, BLUE, "$#,##0", YELLOW); put(wbud, b_tot + 1, 3, "[Observed]")
put(wbud, b_tot + 2, 1, "Headroom", BOLD); put(wbud, b_tot + 2, 2, f"=B{b_tot+1}-B{b_tot}", BOLD, "$#,##0;($#,##0);-")
c0 = b_tot + 4
put(wbud, c0, 1, "What the budget buys in a year", BOLD)
put(wbud, c0 + 1, 1, "New posts"); put(wbud, c0 + 1, 2, "=4*12")
put(wbud, c0 + 2, 1, "Refreshes"); put(wbud, c0 + 2, 2, "=8*12")
put(wbud, c0 + 3, 1, "Consolidations and removals (SEO Specialist time, no freelancer cost)"); put(wbud, c0 + 3, 2, 80, BLUE, fill=YELLOW); put(wbud, c0 + 3, 3, "[Estimated]")
put(wbud, c0 + 4, 1, "Posts actioned in 12 months"); put(wbud, c0 + 4, 2, f"=B{c0+1}+B{c0+2}+B{c0+3}")
put(wbud, c0 + 5, 1, "Ramp's publishing pace (brief): posts a year"); put(wbud, c0 + 5, 2, "=50*2"); put(wbud, c0 + 5, 3, "[Estimated]"); put(wbud, c0 + 5, 4, "50 posts in 6 months in the brief. We cannot match it on new posts (48 a year). Refreshes and consolidations are where our effort goes.", wrap=True)

# ================================================================== Targets_Month_12
wm = sheet("Targets_Month_12", "Month-12 targets: three scenarios", "a labeled projection, not a forecast. Low, base and stretch cases side by side. Every yellow cell is an assumption you can change and the three results update.", [60, 11, 11, 11, 14, 80])
note(wm, 3, "Caveat that applies to every row below: the head-term share of loss (46%) comes from an 18-page sample of the biggest pages, and the written answer says not to scale that sample to the site. This sheet does scale it, as a scenario input only, so the targets have a shape. Search Console data in week one replaces the scaled input with the real one.", cols=6, height=44)
header(wm, HR, ["Assumption", "Low", "Base", "Stretch", "Label", "Where it comes from"])
A = [
    ("Where we start: organic traffic a month", 85000, 85000, 85000, "[Observed]", "Brief. Source not stated."),
    ("Where we start: organic conversions a month (index)", 100, 100, 100, "[Assumed]", "Index = 100 so the VP can drop in the real GA4 or CRM number. The fixture shows 200 conversions in 90 days on 18 pages, about 67 a month, but that is a sample."),
    ("Traffic the head-term pages lost across the site in 12 months", 20000, 25000, 30000, "[Assumed]", "Scenario input. Base takes the sample's 46% head-term share of a 55,000 site loss (140K to 85K). Low and stretch bracket it. Replace with Search Console page data."),
    ("Share of that we can win back while an AI Overview sits above #1", 0.25, 0.40, 0.55, "[Estimated]", "Ahrefs, February 2026, 300,000 keywords: 58% lower click rate for the top result when an AI Overview appears. Winning back rank returns under half the old clicks in the base case."),
    ("Traffic lift on a refreshed non-head page, 6 months after the refresh", 0.15, 0.30, 0.45, "[Assumed]", "Placeholder until the Q1 holdout gives a measured number. Replace at day 90."),
    ("Share of non-head traffic on pages that get refreshed this year", 0.40, 0.45, 0.50, "[Estimated]", "96 refreshes plus consolidations against 400 posts, weighted to the top of the traffic curve."),
    ("Share of today's traffic on the head-term pages", 0.25, 0.25, 0.25, "[Estimated]", "Blog is 70% of traffic; the head terms are its biggest pages. Replace with Search Console page data."),
    ("Traffic won back by making the dated URLs evergreen (monthly, by month 12)", 2000, 4000, 6000, "[Estimated]", "Two URLs peaked at 12,900 combined. Government and IRS own both SERPs now."),
    ("Traffic from new content by month 12 (48 new posts plus the comparison hub)", 5000, 9000, 14000, "[Estimated]", "Base is about 190 visits a post at month 12, in line with the spend management page's 650 at under a year old."),
    ("Conversion lift from CTAs, the comparison hub and templates (multiplier on conversions per visit)", 1.3, 1.6, 1.9, "[Estimated]", "Comparison pages convert at 10 to 13 per 1,000 visits against a blended 1.85. Base moves a tenth of visits to that path and fixes CTAs on the top 6 pages."),
]
for i, (a, lo, ba, st, l, b) in enumerate(A, DR):
    put(wm, i, 1, a, wrap=True)
    for c, v in ((2, lo), (3, ba), (4, st)):
        put(wm, i, c, v, BLUE, "0.00" if isinstance(v, float) else "#,##0", YELLOW)
    put(wm, i, 5, l); put(wm, i, 6, b, wrap=True); wm.row_dimensions[i].height = 44
k = {name: DR + i for i, name in enumerate(["start_traffic", "start_conv", "head_lost", "head_share_back", "refresh_lift", "refresh_share", "head_share_now", "dated_back", "new_content", "conv_mult"])}
p0 = DR + len(A) + 1
put(wm, p0, 1, "Month-12 projection", BOLD)
header(wm, p0 + 1, ["", "Low", "Base", "Stretch", "Label", ""])
def row(r, label, f, lab, fmt="#,##0", bold=False):
    put(wm, r, 1, label, BOLD if bold else BLACK)
    for c, col in ((2, "B"), (3, "C"), (4, "D")):
        put(wm, r, c, f(col), BOLD if bold else BLACK, fmt)
    put(wm, r, 5, lab)
r0 = p0 + 2
row(r0, "Today's traffic (untouched pages assumed flat)", lambda c: f"={c}{k['start_traffic']}", "[Observed]")
row(r0 + 1, "Head-term traffic won back (lost x share we can win back)", lambda c: f"={c}{k['head_lost']}*{c}{k['head_share_back']}", "[Assumed]")
row(r0 + 2, "Lift on the refreshed non-head pages", lambda c: f"={c}{k['start_traffic']}*(1-{c}{k['head_share_now']})*{c}{k['refresh_share']}*{c}{k['refresh_lift']}", "[Estimated]")
row(r0 + 3, "Dated URLs made evergreen", lambda c: f"={c}{k['dated_back']}", "[Estimated]")
row(r0 + 4, "New content", lambda c: f"={c}{k['new_content']}", "[Estimated]")
row(r0 + 5, "Projected organic traffic, month 12", lambda c: f"=SUM({c}{r0}:{c}{r0+4})", "[Estimated]", bold=True)
put(wm, r0 + 6, 1, "Target in the brief"); put(wm, r0 + 6, 3, 140000, BLUE, "#,##0", YELLOW); put(wm, r0 + 6, 5, "[Observed]")
row(r0 + 7, "Gap to 140K", lambda c: f"=$C${r0+6}-{c}{r0+5}", "", fmt="#,##0;(#,##0);-")
row(r0 + 8, "Projected organic conversions, month 12 (index, start = 100)", lambda c: f"={c}{k['start_conv']}*({c}{r0+5}/{c}{k['start_traffic']})*{c}{k['conv_mult']}", "[Estimated]", fmt="0", bold=True)
note(wm, r0 + 10, "Reading: low about 101K, base about 117K, stretch about 136K. The brief's 140K sits above the stretch case, because the head-term pages sit under an AI Overview and the two expired URLs are government-owned queries now. Conversions land between about 1.5x and 3x, base about 2.2x, because the conversion path (comparison hub, templates, CTAs) is where the upside is. The base case is a scenario, not a promise: the Q1 holdout replaces the refresh lift, and week-one Search Console data replaces the scaled head-term loss.", cols=6, height=70)

# ================================================================== Data_To_Request
wdr = sheet("Data_To_Request", "What we ask for in week one", "the nine data pulls, who owns each, why it matters, and what changes in the plan if the data says something different.", [4, 46, 26, 18, 60, 60])
header(wdr, HR, ["#", "Data", "Source", "Owner", "Why it matters", "What changes if it says something different"])
reqs = [
    ("Search Console clicks, impressions and average position by page and by query, the full 16 months, weekly", "Search Console export or API", "SEO Specialist", "The only accurate record of clicks, and of rankings that bounced back. 90 days hides seasonality and update timing.", "If Search Console shows a different shape from the brief's numbers, the whole diagnosis is re-run on it before anything ships."),
    ("GA4 sessions and conversions by landing page, both 12-month periods, organic only", "GA4 explorations", "SEO Specialist", "Sets the real baseline and shows what conversions were before the decline.", "If conversions cannot be tied to landing pages, fix tracking first; no page-level KPI until then."),
    ("CRM stage by landing page and first-touch source (MQL, SQL, opportunity, closed-won)", "HubSpot or Salesforce report", "VP Marketing to unlock", "Lead quality. 44 conversions on vs-ramp may be Ramp customers browsing.", "Pages are re-weighted by pipeline rather than by raw conversions."),
    ("Ahrefs new and lost referring domains by month for the domain and the four fallen head pages; anchor text mix; DR spread", "Ahrefs Site Explorer", "SEO Specialist", "Tests the spam hypothesis and the timing of links.", "A spike before the drop, or exact-match anchors, moves the link audit ahead of refreshes and triggers a targeted disavow."),
    ("Last-modified and publish date for all 400 posts", "WordPress export", "Content Manager", "Freshness is the strongest signal in the fixture; this is the full-site version.", "If modified dates are missing: Wayback Machine for the top 100, publish date for the rest."),
    ("Google update calendar lined up with the weekly Search Console series", "Search Engine Journal update history", "SEO Specialist", "A step down in a core update means content quality; in a spam update, links; a slow slide, decay and competition.", "The order of Q1 work changes with the answer."),
    ("CrUX field data and PageSpeed lab data for the blog template, mobile and desktop", "PageSpeed Insights, CrUX", "WordPress contractor", "Sizes the Sprint 1 speed work and gives the before number.", "If field data already passes, Sprint 1 time moves to the redirect map and link module."),
    ("Rank tracking: head terms and comparison pages, US desktop and mobile, weekly", "Ahrefs rank tracker", "SEO Specialist", "The 90-day indicators need a weekly series from day one.", "None. This is the measurement."),
    ("What counts as a conversion, agreed in writing (demo request, signup, download?)", "VP Marketing", "VP Marketing", "The template page's 12 conversions may be downloads. The KPI needs one definition.", "Baseline numbers are restated under the agreed definition."),
]
for i, (d, src, own, why, change) in enumerate(reqs, DR):
    put(wdr, i, 1, i - DR + 1); put(wdr, i, 2, d, wrap=True); put(wdr, i, 3, src, wrap=True); put(wdr, i, 4, own, wrap=True); put(wdr, i, 5, why, wrap=True); put(wdr, i, 6, change, wrap=True); wdr.row_dimensions[i].height = 58
wdr.freeze_panes = wdr.cell(row=DR, column=1)

# ================================================================== Live_SERPs
wl = sheet("Live_SERPs", "Who ranks today for the fallen keywords", "the live Google US results pulled on 12 October 2026 for five fixture keywords: who is in the top 10, when their page was last updated, and whether an AI Overview sits on top.", [11, 28, 13, 9, 36, 10, 16, 8, 24, 70, 12])
scols = list(serp[0].keys())
nice = {"pulled_on": "Pulled on", "keyword": "Keyword", "location": "Location", "device": "Device", "dataforseo_task_id": "DataForSEO task id (for re-checking)", "ai_overview_present": "AI Overview present", "ai_overview_position": "AI Overview position", "organic_rank": "Organic rank", "domain": "Domain", "url": "URL", "snippet_date": "Page date Google shows"}
header(wl, HR, [nice[c] for c in scols])
for i, x in enumerate(serp, DR):
    for j, k in enumerate(scols, 1):
        put(wl, i, j, x[k], BLUE)
n = DR + len(serp) + 1
note(wl, n, "[Observed] Google US desktop via the DataForSEO SERP API. Task ids can be re-checked in a DataForSEO account. A blank page date means Google showed none.", cols=10, height=32)
obs = [
    "AI Overview on all 5 SERPs; on 4 of 5 it sits above the first organic result (per diem rates: below #3).",
    "what is expense management: NetSuite #1 (updated 2025-07), Medius #2, Ramp #3 (2026-07), Airwallex #4 (2026-05), Stripe #5 (2026-07). Our page: last updated 2024-01. The fixture blames a lost snippet to Ramp; the live SERP says the whole top 5 refreshed in 2025-26 and an AI Overview took the top.",
    "business expense categories: IRS #1, NetSuite #2 (2026-09), Ramp #3 (2026-05), Paychex #4 (2026-03). Related searches show PDF and spreadsheet demand. Our page: last updated 2023-11 with outdated IRS references.",
    "corporate card vs credit card: JPMorgan, Chase, Reddit, Amex, Investopedia. Banks own it. Ramp is not in the top 10. Holding #5 and converting is the realistic goal.",
    "per diem rates: GSA, State, DoD, Commerce. Government owns the SERP. Concede the rates query; keep a cheap evergreen page for the long tail.",
    "receipt scanning app: mixed intent (consumer cashback apps and business tools), AI Overview, video carousel, Reddit. A stable #5 losing 31% of clicks fits this layout.",
]
put(wl, n + 2, 1, "What it shows", BOLD)
for i, t in enumerate(obs):
    note(wl, n + 3 + i, t, cols=10, height=32)
wl.freeze_panes = wl.cell(row=DR, column=1)

# ================================================================== Competitors
wk = sheet("Competitors", "Ramp and Brex: footprint and link pace", "how big Ramp's organic footprint is, and how many referring domains Ramp and Brex gain each month, so we know what we are up against on links.", [11, 44, 36, 10, 18, 12, 12, 14, 14, 16, 16, 14])
put(wk, 3, 1, "Ramp's organic footprint (DataForSEO Labs, US)", BOLD)
rcols = list(ramp[0].keys())
rnice = {"pulled_on": "Pulled on", "source": "Source", "dataforseo_task_id": "Task id", "target": "Domain", "location": "Location", "year": "Year", "month": "Month", "organic_keywords_count": "Keywords ranking", "organic_pos_1": "At #1", "organic_pos_2_3": "At #2-3", "organic_pos_4_10": "At #4-10", "organic_pos_11_20": "At #11-20", "organic_etv_monthly": "Estimated monthly visits", "organic_is_new": "New keywords", "organic_is_lost": "Lost keywords"}
header(wk, HR, [rnice[c] for c in rcols])
for i, x in enumerate(ramp, DR):
    for j, k in enumerate(rcols, 1):
        v = x[k]; put(wk, i, j, int(v) if v.isdigit() else v, BLUE, "#,##0" if v.isdigit() and j > 5 else None)
r1 = DR + len(ramp)
note(wk, r1, "[Observed] Ramp ranks for roughly 34,000 to 41,000 US keywords with 420,000 to 474,000 estimated monthly visits: about 3x our keyword footprint and 5x our traffic (brief). Estimated visits are a tool estimate, not sessions. Ramp's own count softened from June to October 2026, so even the aggressive publisher is not immune to the same SERP changes.", cols=10, height=48)
l0 = r1 + 2
put(wk, l0, 1, "Referring domains gained and lost each month (DataForSEO backlinks index)", BOLD)
lcols = list(links[0].keys()) + ["net_new_main_domains"]
lnice = {"pulled_on": "Pulled on", "source": "Source", "dataforseo_task_id": "Task id", "target": "Domain", "month": "Month", "new_backlinks": "New backlinks", "lost_backlinks": "Lost backlinks", "new_referring_domains": "New referring domains", "lost_referring_domains": "Lost referring domains", "new_referring_main_domains": "New referring main domains", "lost_referring_main_domains": "Lost referring main domains", "net_new_main_domains": "Net new main domains"}
header(wk, l0 + 1, [lnice[c] for c in lcols])
lf = l0 + 2
for i, x in enumerate(links, lf):
    for j, k in enumerate(lcols[:-1], 1):
        v = x[k]; put(wk, i, j, int(v) if v.isdigit() else v, BLUE, "#,##0" if v.isdigit() else None)
    put(wk, i, len(lcols), f"=J{i}-K{i}", fmt="#,##0;(#,##0);-")
ll = lf + len(links) - 1
s1 = ll + 2
put(wk, s1, 1, "12 full months (October 2025 to September 2026)", BOLD)
header(wk, s1 + 1, ["Domain", "New main domains", "Lost main domains", "Net", "Net a month", "First half, net a month", "Second half, net a month"])
for i, (t, r0) in enumerate((("ramp.com", lf), ("brex.com", lf + 13)), s1 + 2):
    put(wk, i, 1, t); put(wk, i, 2, f"=SUM(J{r0}:J{r0+11})", fmt="#,##0"); put(wk, i, 3, f"=SUM(K{r0}:K{r0+11})", fmt="#,##0")
    put(wk, i, 4, f"=B{i}-C{i}", fmt="#,##0"); put(wk, i, 5, f"=D{i}/12", fmt="#,##0"); put(wk, i, 6, f"=SUM(L{r0}:L{r0+5})/6", fmt="#,##0"); put(wk, i, 7, f"=SUM(L{r0+6}:L{r0+11})/6", fmt="#,##0")
put(wk, s1 + 4, 1, "our domain (fill from Ahrefs in week one)", BLUE, fill=YELLOW)
note(wk, s1 + 6, "[Observed] Ramp nets about 340 new referring main domains a month and the pace roughly doubled from the first half to the second. Brex nets about 165. A $4,000 a month digital PR line will not match that on volume, so our links go to the handful of pages that convert or hold the head terms. The week-one link audit looks for spikes or drops in our own pace that line up with ranking changes, exact-match anchors, low-quality domains and any manual action. If it finds a problem, links move to the front of Q1 and the refresh program slows until it is dealt with.", cols=10, height=60)

# ================================================================== order and fonts
order = ["Start_Here", "Why_Traffic_Dropped", "Page_Triage", "Triage_Rules", "Topics", "Plan_90_Days", "Roadmap_12_Months", "Budget", "Targets_Month_12",
         "Data_To_Request", "Live_SERPs", "Competitors", "Ref_CTR_Curve"]
wb._sheets = [wb[n] for n in order]; wb.active = 0
for s_ in wb.worksheets:
    for row in s_.iter_rows():
        for c in row:
            if c.font.name != F:
                c.font = Font(name=F, size=c.font.size or 10, bold=c.font.bold, italic=c.font.italic, color=c.font.color)
wb.save(OUT)
print("saved", OUT, len(wb.sheetnames), "sheets")
