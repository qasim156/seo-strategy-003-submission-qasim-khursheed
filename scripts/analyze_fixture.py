#!/usr/bin/env python3
"""Fixture analysis for Beat Claude SEO Strategy 003 (brief version 2026-07).

Reads challenges/seo-strategy-003/fixtures/content_audit_sample.csv and produces:
  - decline decomposition by cause bucket
  - rank-explained vs unexplained traffic loss (benchmarked CTR curve)
  - Spearman correlations: position change, referring domains, conversions, staleness
  - triage bucket (refresh / consolidate / kill / protect) per URL with the rule that fired
Outputs analysis_output.json and triage_table.csv next to the fixture copy.

Usage: python3 -I analyze_fixture.py <path-to-fixture.csv> <output-dir>
"""
import csv, json, sys, hashlib
from pathlib import Path
from scipy.stats import spearmanr

FIXTURE = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# "Now" for staleness arithmetic. The fixture has no snapshot date; the brief version is 2026-07. [Assumed]
NOW_Y, NOW_M = 2026, 7

# Benchmarked organic CTR curve, positions 1-10 (FirstPageSage 2023 curve as cited by Backlinko, Apr 2025 update).
# Positions 11+ are assumed, not benchmarked.
CTR = {1: 39.8, 2: 18.7, 3: 10.2, 4: 7.2, 5: 5.1, 6: 4.4, 7: 3.0, 8: 2.1, 9: 1.9, 10: 1.6}
def ctr(pos):
    if pos in CTR:
        return CTR[pos]
    if pos <= 20:   # [Assumed] page 2
        return 1.2 - (pos - 11) * 0.07
    if pos <= 30:   # [Assumed] page 3
        return 0.3
    return 0.15     # [Assumed] page 4+

rows = list(csv.DictReader(open(FIXTURE, newline="")))
for r in rows:
    for k in ("position_12mo_ago", "position_now", "traffic_now_monthly", "traffic_12mo_ago",
              "referring_domains", "publish_year", "conversions_90d"):
        r[k] = int(r[k])
    y, m = r["last_updated"].split("-")
    r["months_since_update"] = (NOW_Y - int(y)) * 12 + (NOW_M - int(m))
    r["traffic_delta"] = r["traffic_now_monthly"] - r["traffic_12mo_ago"]
    r["traffic_change_pct"] = round(100 * r["traffic_delta"] / r["traffic_12mo_ago"], 1)
    r["position_delta"] = r["position_now"] - r["position_12mo_ago"]  # positive = fell
    # conversions per 1,000 visits over the 90-day window (traffic is monthly, so x3) [Estimated]
    r["conv_per_1k_visits_90d"] = round(1000 * r["conversions_90d"] / (3 * r["traffic_now_monthly"]), 2)
    # rank-explained traffic: what traffic_12mo_ago would become at the new position if demand were unchanged
    r["rank_predicted_traffic_now"] = round(r["traffic_12mo_ago"] * ctr(r["position_now"]) / ctr(r["position_12mo_ago"]))
    r["unexplained_by_rank"] = r["traffic_now_monthly"] - r["rank_predicted_traffic_now"]  # negative = lost more than rank explains
    r["is_branded"] = r["target_keyword"].startswith("company brand")
    r["is_dated_url"] = r["url_slug"][-4:].isdigit()

sha = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
n = len(rows)
tot_now = sum(r["traffic_now_monthly"] for r in rows)
tot_then = sum(r["traffic_12mo_ago"] for r in rows)
tot_loss = tot_now - tot_then
tot_conv = sum(r["conversions_90d"] for r in rows)
nb = [r for r in rows if not r["is_branded"]]
nb_now, nb_then = sum(r["traffic_now_monthly"] for r in nb), sum(r["traffic_12mo_ago"] for r in nb)

# ---- Cause buckets (judgment, applied to slugs) ----
CAUSE = {
    "/blog/per-diem-rates-2022": "A. Dated URL expired",
    "/blog/quarterly-tax-deadlines-2023": "A. Dated URL expired",
    "/blog/what-is-expense-management": "B. Head term: fresher competitors + AI Overview / snippet",
    "/blog/expense-management-guide": "B. Head term: fresher competitors + AI Overview / snippet (cannibal)",
    "/blog/business-expense-categories": "B. Head term: fresher competitors + AI Overview / snippet",
    "/blog/corporate-card-vs-credit-card": "B. Head term: fresher competitors + AI Overview / snippet",
    "/blog/accounting-software-list": "C. Off-core, outranked by aggregators / thin",
    "/blog/bookkeeping-basics": "C. Off-core, outranked by aggregators / thin",
    "/blog/mileage-reimbursement-guide": "D. Stale rules content",
    "/blog/receipt-scanning-app": "E. SERP feature at stable rank (AI Overview, mixed intent)",
    "/compare/vs-ramp": "F. High-intent compare page slipping",
    "/blog/expense-fraud-statistics": "G. Link asset drifting (stale stats)",
    "/blog/expense-report-template": "H. Stable (noise)",
    "/blog/what-is-an-invoice": "H. Stable (noise)",
    "/compare/vs-brex": "H. Stable (noise)",
    "/blog/travel-expense-policy": "I. Gainers (recently updated / new cluster / branded)",
    "/blog/what-is-spend-management": "I. Gainers (recently updated / new cluster / branded)",
    "/blog/company-name-expense-software": "I. Gainers (recently updated / new cluster / branded)",
}
cause_tot = {}
for r in rows:
    r["cause_bucket"] = CAUSE[r["url_slug"]]
    key = r["cause_bucket"].split(":")[0].split(" (")[0]
    cause_tot[key] = cause_tot.get(key, 0) + r["traffic_delta"]
cause_share = {k: {"traffic_delta": v, "share_of_sample_loss_pct": round(100 * v / tot_loss, 1)} for k, v in sorted(cause_tot.items())}

# ---- Triage buckets with the rule that fired (rules are ordered; first match wins) ----
def triage(r):
    s = r["url_slug"]
    if s == "/blog/expense-management-guide":
        return "Consolidate", "R1 same target keyword as a stronger URL (cannibal): 301 into the stronger URL"
    if r["is_dated_url"]:
        return "Consolidate", "R2 year-stamped URL: 301 to an evergreen slug, refresh once a year, no further investment"
    if s in ("/blog/bookkeeping-basics", "/blog/accounting-software-list"):
        return "Kill", "R3 off-core topic, 0 conversions, under 10 RDs, lost over 15 positions: 410, or 301 to the nearest hub if any RDs are worth keeping"
    if r["conv_per_1k_visits_90d"] >= 2.0 or r["is_branded"]:
        return "Protect", "R4 conversion asset (2+ conversions per 1k visits) or branded: URL untouched, light update, stronger CTA, internal links in"
    if r["position_delta"] <= 0 and r["months_since_update"] <= 24:
        return "Protect", "R5 holding or gaining and updated within 24 months: leave alone, extend the cluster around it"
    if s == "/blog/what-is-an-invoice":
        return "Protect", "R6 traffic with zero product relevance: keep, no investment, test one product CTA, never report it as a win"
    if r["position_delta"] > 0 or r["months_since_update"] > 18:
        return "Refresh", "R7 lost positions or older than 18 months on a core topic: full refresh, URL kept, intent and SERP format re-checked (link assets with 70+ RDs are never redirected)"
    return "Protect", "R8 default: monitor"

ACTION = {
    "/compare/vs-ramp": ("P1", "Rebuild as a real comparison (pricing and feature table, honest tradeoffs), stronger CTA, internal links from the 84-RD and 74-RD blog pages. Highest conversion lever on the site."),
    "/blog/what-is-expense-management": ("P1", "Full refresh, 301 the cannibal guide into it, structure the definition for AI Overview citation, target NetSuite's and Ramp's 2026 depth. Expect a ceiling: the AI Overview now sits above #1."),
    "/blog/expense-management-guide": ("P1", "301 to /blog/what-is-expense-management, merge any unique sections first."),
    "/blog/per-diem-rates-2022": ("P1", "301 to /blog/per-diem-rates (evergreen), refresh each October when GSA publishes. Government sites own this SERP, so no further spend."),
    "/blog/quarterly-tax-deadlines-2023": ("P1", "301 to /blog/quarterly-tax-deadlines (evergreen), annual refresh only. Zero conversions historically, so lowest priority after the redirect."),
    "/blog/bookkeeping-basics": ("P1", "410, or 301 to the expense categories page if the 4 RDs are real sites."),
    "/blog/accounting-software-list": ("P1", "Remove. The SERP belongs to aggregators and we have 0 conversions and 8 RDs. Redirect to the compare hub only if RDs are real."),
    "/blog/business-expense-categories": ("P2", "Refresh with current IRS category references, add a downloadable categories sheet (the SERP shows PDF and spreadsheet demand), link to the expense policy template."),
    "/blog/corporate-card-vs-credit-card": ("P2", "Light update plus CTA. Do not chase #1: the live SERP is JPMorgan, Chase, Reddit, Amex and Investopedia. Protect the 31 conversions."),
    "/blog/mileage-reimbursement-guide": ("P2", "Refresh with the current IRS mileage rate, make the rate block easy to cite, link to the expense policy template."),
    "/blog/expense-report-template": ("P2", "Leave the page, test the download-to-signup step. Confirm whether a download counts as a conversion before reporting it."),
    "/blog/receipt-scanning-app": ("P3", "Refresh for citation rather than rank: the SERP has an AI Overview and mixed consumer intent. Short cited answer block, product angle, accept lower traffic."),
    "/blog/expense-fraud-statistics": ("P3", "Refresh the statistics yearly, keep the URL forever, use it as the internal link source for compare pages. Never judge it on conversions."),
    "/blog/what-is-spend-management": ("P3", "Extend the cluster (spend management policy, spend management vs expense management, software). Small base, so label gains carefully."),
    "/blog/travel-expense-policy": ("P3", "Leave the page, add the policy template download and a CTA. Build the sibling policy pages around it."),
    "/compare/vs-brex": ("P3", "Keep, align format with the rebuilt vs-ramp page, add to the compare hub."),
    "/blog/company-name-expense-software": ("P3", "Move out of blog reporting. Branded demand rather than SEO performance."),
    "/blog/what-is-an-invoice": ("P3", "No investment. One CTA test if the product has an invoice or AP feature; otherwise leave it."),
}
FACE_VALUE = {
    "/blog/what-is-expense-management": "The note blames a lost snippet to Ramp. The live SERP (Oct 2026) shows an AI Overview above every result, NetSuite at #1 and Ramp at #3. Recovery to #1 does not return 14,100 visits.",
    "/blog/expense-management-guide": "Cannibal of the page above. Its drop is not a separate problem.",
    "/blog/corporate-card-vs-credit-card": "Note says highest converting blog page. The branded page in /blog has 52 conversions, this has 31. The notes are not reliable.",
    "/blog/expense-report-template": "Note says downloads drive signups. Is a download a conversion in the 12 count? Definition check before use.",
    "/blog/per-diem-rates-2022": "Dated URL. Its loss is expiry, not decay, competition or a penalty. A refresh on this slug is wasted.",
    "/blog/what-is-an-invoice": "2,900 visits and 0 conversions. Traffic-based triage would protect it as a win; conversion-based triage leaves it alone.",
    "/compare/vs-ramp": "44 conversions on 1,100 visits is 13 per 1k, 7x the blended rate. Check attribution (last click vs assisted) and branded mix before building the plan on this rate.",
    "/blog/company-name-expense-software": "Branded query filed under /blog. Inflates blog traffic and conversions. Exclude from the SEO baseline.",
    "/blog/receipt-scanning-app": "Position unchanged, traffic down 31%. A refresh aimed at rank cannot fix a click-share loss. The live SERP has an AI Overview and consumer cashback apps.",
    "/blog/expense-fraud-statistics": "1 conversion in 90 days but 74 referring domains. Judged on conversions it looks like a kill. It is the blog's link asset.",
    "/blog/quarterly-tax-deadlines-2023": "Dated URL still indexed. 5,100 visits a month at its peak with 0 conversions. Recovering it adds traffic and no revenue.",
    "/blog/accounting-software-list": "Outranked by aggregators. Not a content quality problem we can refresh our way out of.",
    "/blog/what-is-spend-management": "Gaining, but from 300 to 650. Too small a base to call a trend.",
    "/blog/travel-expense-policy": "Rank improved 9 to 6 but traffic rose less than the CTR curve predicts. Likely a SERP feature capping clicks.",
}
TOPIC = {
    "/compare/vs-ramp": "Comparisons and alternatives", "/compare/vs-brex": "Comparisons and alternatives",
    "/blog/corporate-card-vs-credit-card": "Corporate cards",
    "/blog/what-is-expense-management": "Expense management core", "/blog/expense-management-guide": "Expense management core",
    "/blog/business-expense-categories": "Expense management core", "/blog/expense-report-template": "Expense management core",
    "/blog/travel-expense-policy": "Expense management core", "/blog/what-is-spend-management": "Expense management core",
    "/blog/receipt-scanning-app": "Expense management core",
    "/blog/per-diem-rates-2022": "Rates and deadlines (compliance utility)", "/blog/mileage-reimbursement-guide": "Rates and deadlines (compliance utility)",
    "/blog/quarterly-tax-deadlines-2023": "Rates and deadlines (compliance utility)",
    "/blog/what-is-an-invoice": "Off-core finance education", "/blog/bookkeeping-basics": "Off-core finance education",
    "/blog/accounting-software-list": "Off-core finance education",
    "/blog/expense-fraud-statistics": "Data and statistics (link assets)",
    "/blog/company-name-expense-software": "Branded",
}
for r in rows:
    r["triage_bucket"], r["triage_rule"] = triage(r)
    r["priority"], r["action"] = ACTION[r["url_slug"]]
    r["face_value_flag"] = FACE_VALUE.get(r["url_slug"], "")
    r["topic"] = TOPIC[r["url_slug"]]
topics = {}
for r in rows:
    t = topics.setdefault(r["topic"], {"pages": 0, "traffic_now": 0, "traffic_12mo_ago": 0, "conversions_90d": 0, "referring_domains": 0})
    t["pages"] += 1; t["traffic_now"] += r["traffic_now_monthly"]; t["traffic_12mo_ago"] += r["traffic_12mo_ago"]
    t["conversions_90d"] += r["conversions_90d"]; t["referring_domains"] += r["referring_domains"]
for t in topics.values():
    t["conv_per_1k_visits_90d"] = round(1000 * t["conversions_90d"] / (3 * t["traffic_now"]), 2)
    t["traffic_change_pct"] = round(100 * (t["traffic_now"] - t["traffic_12mo_ago"]) / t["traffic_12mo_ago"], 1)

# ---- Correlations (Spearman, n=18; small sample, report rho and p) ----
def sp(a, b):
    rho, p = spearmanr([r[a] for r in rows], [r[b] for r in rows])
    return {"rho": round(float(rho), 2), "p": round(float(p), 3)}
def sp_rows(rs, a, b):
    rho, p = spearmanr([r[a] for r in rs], [r[b] for r in rs])
    return {"rho": round(float(rho), 2), "p": round(float(p), 3), "n": len(rs)}

corr = {
    "position_delta_vs_conversions_90d": sp("position_delta", "conversions_90d"),
    "position_delta_vs_conv_per_1k": sp("position_delta", "conv_per_1k_visits_90d"),
    "referring_domains_vs_position_now": sp("referring_domains", "position_now"),
    "referring_domains_vs_position_delta": sp("referring_domains", "position_delta"),
    "referring_domains_vs_conversions_90d": sp("referring_domains", "conversions_90d"),
    "referring_domains_vs_conv_per_1k": sp("referring_domains", "conv_per_1k_visits_90d"),
    "position_now_vs_conversions_90d": sp("position_now", "conversions_90d"),
    "months_since_update_vs_position_delta": sp("months_since_update", "position_delta"),
    "months_since_update_vs_traffic_change_pct": sp("months_since_update", "traffic_change_pct"),
    "traffic_now_vs_conversions_90d": sp("traffic_now_monthly", "conversions_90d"),
    "referring_domains_vs_position_delta_excl_dated": sp_rows([r for r in rows if not r["is_dated_url"]], "referring_domains", "position_delta"),
}

# ---- Groupings the VP will ask about ----
fell = [r for r in rows if r["position_delta"] > 0]
held = [r for r in rows if r["position_delta"] <= 0]
groups = {
    "pages_that_fell": {"n": len(fell), "conversions_90d": sum(r["conversions_90d"] for r in fell),
                        "traffic_now": sum(r["traffic_now_monthly"] for r in fell),
                        "median_months_since_update": sorted(r["months_since_update"] for r in fell)[len(fell)//2]},
    "pages_that_held_or_gained": {"n": len(held), "conversions_90d": sum(r["conversions_90d"] for r in held),
                        "traffic_now": sum(r["traffic_now_monthly"] for r in held),
                        "median_months_since_update": sorted(r["months_since_update"] for r in held)[len(held)//2]},
    "compare_pages": {"traffic_now": sum(r["traffic_now_monthly"] for r in rows if r["url_slug"].startswith("/compare")),
                      "conversions_90d": sum(r["conversions_90d"] for r in rows if r["url_slug"].startswith("/compare"))},
    "top4_conversion_pages_share_pct": round(100 * sum(sorted((r["conversions_90d"] for r in rows), reverse=True)[:4]) / tot_conv, 1),
    "zero_conversion_pages": [r["url_slug"] for r in rows if r["conversions_90d"] == 0],
    "zero_conversion_pages_traffic_lost": sum(r["traffic_delta"] for r in rows if r["conversions_90d"] == 0),
    "pages_lost_more_than_rank_explains": [(r["url_slug"], r["unexplained_by_rank"]) for r in rows if r["unexplained_by_rank"] < -150],
    "pages_rank_overexplains": [(r["url_slug"], r["unexplained_by_rank"]) for r in rows if r["unexplained_by_rank"] > 150],
    "high_rd_pages_that_still_fell": [(r["url_slug"], r["referring_domains"], r["position_delta"]) for r in rows if r["referring_domains"] >= 50 and r["position_delta"] > 0],
    "gainers_rd": [(r["url_slug"], r["referring_domains"], r["position_delta"]) for r in rows if r["position_delta"] < 0],
}

summary = {
    "fixture_sha256": sha, "rows": n,
    "sample_traffic_now": tot_now, "sample_traffic_12mo_ago": tot_then, "sample_loss": tot_loss,
    "sample_change_pct": round(100 * tot_loss / tot_then, 1),
    "brief_site_change_pct": round(100 * (85 - 140) / 140, 1),
    "sample_share_of_site_traffic_now_pct": round(100 * tot_now / 85000, 1),
    "sample_share_of_site_traffic_then_pct": round(100 * tot_then / 140000, 1),
    "non_branded_change_pct": round(100 * (nb_now - nb_then) / nb_then, 1),
    "total_conversions_90d": tot_conv,
    "blended_conv_per_1k_visits_90d": round(1000 * tot_conv / (3 * tot_now), 2),
    "dated_urls_loss": sum(r["traffic_delta"] for r in rows if r["is_dated_url"]),
    "dated_urls_share_pct": round(100 * sum(r["traffic_delta"] for r in rows if r["is_dated_url"]) / tot_loss, 1),
    "cause_buckets": cause_share, "correlations": corr, "groups": groups, "topics": topics,
    "triage_counts": {b: sum(1 for r in rows if r["triage_bucket"] == b) for b in ("Protect", "Refresh", "Consolidate", "Kill")},
    "assumptions": {"now_for_staleness": f"{NOW_Y}-{NOW_M:02d} (brief version date)",
                    "ctr_curve_pos_1_10": "FirstPageSage 2023 curve as cited by Backlinko (updated Apr 2025) [Benchmarked]",
                    "ctr_pos_11_plus": "assumed", "conv_window": "conversions_90d divided by 3x monthly traffic [Estimated]"},
}
(OUT / "analysis_output.json").write_text(json.dumps(summary, indent=2))
cols = ["url_slug", "target_keyword", "position_12mo_ago", "position_now", "position_delta", "traffic_12mo_ago",
        "traffic_now_monthly", "traffic_delta", "traffic_change_pct", "rank_predicted_traffic_now", "unexplained_by_rank",
        "referring_domains", "publish_year", "last_updated", "months_since_update", "conversions_90d",
        "conv_per_1k_visits_90d", "topic", "cause_bucket", "triage_bucket", "triage_rule", "priority", "action", "face_value_flag", "notes"]
with open(OUT / "triage_table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(json.dumps(summary, indent=2))
for r in sorted(rows, key=lambda r: r["traffic_delta"]):
    print(f"{r['url_slug']:40s} {r['position_12mo_ago']:>2}->{r['position_now']:<2} d{r['traffic_delta']:>6} pred{r['rank_predicted_traffic_now']:>6} unexpl{r['unexplained_by_rank']:>6} RD{r['referring_domains']:>3} stale{r['months_since_update']:>3}m conv{r['conversions_90d']:>3} c/1k{r['conv_per_1k_visits_90d']:>6} {r['triage_bucket']}")
