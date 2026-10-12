// Client-facing strategy deck, Single Grain brand theme. Build: node build_deck.js
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "Qasim Khursheed"; pres.company = "Single Grain"; pres.title = "Organic search recovery plan";

// Brand (from singlegrain.com main-home-v3.css and logo.svg): no # prefix for pptxgenjs
const ORANGE = "F27038", GOLD = "EFB438", DARK = "232020", CHAR = "2F343A", GREY = "929194", LIGHT = "E9EFF4", WHITE = "FFFFFF", INK = "2C2F33", MID = "6C757D", PALE = "F8F8F8", BLUE = "0996C7";
const FONT = "Arial";
const W = 13.333, H = 7.5;

// ---------- helpers (factory functions: pptxgenjs mutates option objects) ----------
const wordmark = (s, x, y, size, color, onDark) => {
  s.addText([{ text: "Single", options: { bold: true, color: onDark ? WHITE : CHAR } }, { text: "Grain", options: { bold: true, color: ORANGE } }],
    { x, y, w: 2.2, h: 0.4, fontFace: FONT, fontSize: size, margin: 0, valign: "middle" });
};
let n = 0;
function contentSlide(tag, title, opts = {}) {
  const s = pres.addSlide(); n += 1;
  s.background = { color: WHITE };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.18, h: H, fill: { color: ORANGE }, line: { color: ORANGE } });
  s.addText(tag.toUpperCase(), { x: 0.6, y: 0.38, w: 8, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: ORANGE, charSpacing: 2, margin: 0 });
  s.addText(title, { x: 0.6, y: 0.7, w: 12.1, h: opts.titleH || 1.1, fontFace: FONT, fontSize: opts.titleSize || 26, bold: true, color: CHAR, margin: 0, valign: "top" });
  wordmark(s, 0.6, H - 0.55, 11, CHAR, false);
  s.addText(String(n), { x: W - 1.2, y: H - 0.55, w: 0.6, h: 0.4, fontFace: FONT, fontSize: 10, color: GREY, align: "right", margin: 0 });
  if (opts.source) s.addText(opts.source, { x: 3.0, y: H - 0.55, w: 8.9, h: 0.4, fontFace: FONT, fontSize: 8.5, color: GREY, align: "right", margin: 0, valign: "middle" });
  return s;
}
function takeaway(s, text, y = 6.15, h = 0.62) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 12.1, h, fill: { color: LIGHT }, line: { color: LIGHT } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 0.09, h, fill: { color: ORANGE }, line: { color: ORANGE } });
  s.addText(text, { x: 0.85, y, w: 11.7, h, fontFace: FONT, fontSize: 13, color: INK, margin: 0, valign: "middle" });
}
function stat(s, x, y, w, h, big, small, dark) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: dark ? CHAR : PALE }, line: { color: dark ? CHAR : LIGHT, width: 1 } });
  s.addText(big, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: h * 0.5, fontFace: FONT, fontSize: 30, bold: true, color: dark ? WHITE : ORANGE, margin: 0, valign: "middle" });
  s.addText(small, { x: x + 0.2, y: y + h * 0.55, w: w - 0.4, h: h * 0.4, fontFace: FONT, fontSize: 11.5, color: dark ? LIGHT : INK, margin: 0, valign: "top" });
}
function card(s, x, y, w, h, head, body, accent) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: PALE }, line: { color: LIGHT, width: 1 } });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.08, fill: { color: accent || ORANGE }, line: { color: accent || ORANGE } });
  s.addText(head, { x: x + 0.22, y: y + 0.2, w: w - 0.44, h: 0.5, fontFace: FONT, fontSize: 15, bold: true, color: CHAR, margin: 0, valign: "top" });
  s.addText(body, { x: x + 0.22, y: y + 0.85, w: w - 0.44, h: h - 0.98, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top" });
}
const axisOpts = () => ({
  catAxisLabelColor: INK, catAxisLabelFontFace: FONT, catAxisLabelFontSize: 11, valAxisLabelColor: GREY, valAxisLabelFontFace: FONT, valAxisLabelFontSize: 9,
  valGridLine: { color: "E6E6E6", style: "solid", size: 0.5 }, catGridLine: { style: "none" }, valAxisLineShow: false, catAxisLineColor: "D0D0D0",
  dataLabelFontFace: FONT, dataLabelFontSize: 11, dataLabelColor: INK, legendFontFace: FONT, legendFontSize: 10, legendColor: INK,
});

// ================================================================ 1. Cover
{
  const s = pres.addSlide(); n += 1;
  s.background = { color: DARK };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: H, fill: { color: ORANGE }, line: { color: ORANGE } });
  wordmark(s, 0.9, 0.6, 20, WHITE, true);
  s.addText("Organic search: why traffic fell, and the plan to grow what matters", { x: 0.9, y: 2.2, w: 11.4, h: 1.9, fontFace: FONT, fontSize: 38, bold: true, color: WHITE, margin: 0, valign: "top" });
  s.addText("A 12-month recovery plan, and a better way to measure it", { x: 0.9, y: 4.15, w: 11, h: 0.6, fontFace: FONT, fontSize: 20, color: LIGHT, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.9, y: 5.0, w: 1.6, h: 0.06, fill: { color: ORANGE }, line: { color: ORANGE } });
  s.addText([{ text: "Prepared for the marketing leadership team", options: { breakLine: true } }, { text: "Qasim Khursheed, Single Grain  |  October 2026" }],
    { x: 0.9, y: 5.25, w: 11, h: 0.9, fontFace: FONT, fontSize: 13, color: GREY, margin: 0, valign: "top" });
}

// ================================================================ 2. What happened
{
  const s = contentSlide("Where we are", "Organic traffic is down 40% in a year. A third of the keywords you ranked for are gone.", { source: "Source: your traffic and ranking figures, last 12 months" });
  s.addChart(pres.ChartType.bar, [{ name: "Monthly organic visits", labels: ["12 months ago", "Today"], values: [140000, 85000] }], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 6.2, h: 3.9, barDir: "col", barGapWidthPct: 80, chartColors: [GREY, ORANGE], showValue: true, dataLabelFormatCode: "#,##0", dataLabelPosition: "outEnd",
    valAxisMinVal: 0, valAxisMaxVal: 160000, valAxisLabelFormatCode: "#,##0", showTitle: true, title: "Monthly visits from Google", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR,
  });
  stat(s, 7.4, 2.1, 2.6, 1.6, "140K", "visits a month, 12 months ago", false);
  stat(s, 10.1, 2.1, 2.6, 1.6, "85K", "visits a month today", true);
  stat(s, 7.4, 3.9, 2.6, 1.6, "18,000", "keywords ranking, 12 months ago", false);
  stat(s, 10.1, 3.9, 2.6, 1.6, "12,000", "keywords ranking today", true);
  takeaway(s, "The number everyone is looking at is visits. The rest of this deck shows why visits are the wrong number to chase, and what to chase instead.");
}

// ================================================================ 3. Where the lost traffic went
{
  const s = contentSlide("What happened", "Almost all of the lost traffic came from two kinds of pages: old pages competitors overtook, and dated pages that expired.",
    { source: "Source: audit of your 18 biggest pages (42% of today's traffic). Shares are of the visits those pages lost." });
  s.addChart(pres.ChartType.bar, [{ name: "Share of lost visits", labels: ["Old guides that competitors overtook", "Pages with a year in the web address that expired", "Off-topic pages (bookkeeping, accounting lists)", "Pages where the rules changed but the page did not", "Everything else, net"], values: [46.2, 35.0, 9.1, 6.2, 3.5] }], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 8.2, h: 4.0, barDir: "bar", barGapWidthPct: 45, chartColors: [ORANGE], showValue: true, dataLabelFormatCode: '0.0"%"', dataLabelPosition: "outEnd",
    valAxisMinVal: 0, valAxisMaxVal: 60, valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 11, catAxisOrientation: "maxMin",
  });
  s.addText([
    { text: "Two different problems", options: { bold: true, color: CHAR, breakLine: true, fontSize: 14 } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "The big guides slipped 2 to 5 places. That is competition: the pages above you were rewritten in 2025 and 2026, yours were not.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "Four pages fell 17 to 38 places. Two of them have a year in their web address, so they expired. Two are off-topic. No amount of promotion brings those back; they need to be redirected or retired.", options: { breakLine: true } },
  ], { x: 9.1, y: 2.1, w: 3.6, h: 3.9, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top" });
  takeaway(s, "Fixing this is mostly updating and tidying what you already own. It is not a rebuild and it is not a promotion problem.");
}

// ================================================================ 4. Old pages fell, updated pages held
{
  const s = contentSlide("Why it happened", "The older the page, the further it fell. Pages updated in the last two years held or grew.",
    { source: "Source: last-updated dates and ranking change for your 18 biggest pages. Average is the median." });
  s.addChart(pres.ChartType.bar, [{ name: "Months since the page was last updated", labels: ["Pages that dropped (13 pages)", "Pages that held or grew (5 pages)"], values: [39, 21] }], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 6.0, h: 3.9, barDir: "col", barGapWidthPct: 90, chartColors: [ORANGE, CHAR], showValue: true, dataLabelFormatCode: '0" months"', dataLabelPosition: "outEnd",
    valAxisMinVal: 0, valAxisMaxVal: 48, valAxisHidden: true, valGridLine: { style: "none" }, showTitle: true, title: "Average time since last update", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR,
  });
  s.addText([
    { text: "What we saw", options: { bold: true, color: CHAR, breakLine: true, fontSize: 14 } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "None of your top pages has been touched since January 2025.", options: { bullet: true, breakLine: true } },
    { text: "The two pages that improved are the two most recently updated.", options: { bullet: true, breakLine: true } },
    { text: "For \"what is expense management\", every page now above you was updated between July 2025 and July 2026. Yours was last updated January 2024.", options: { bullet: true, breakLine: true } },
    { text: "For \"business expense categories\", the pages above you were updated in 2026. Yours still cites outdated IRS categories.", options: { bullet: true, breakLine: true } },
  ], { x: 7.0, y: 2.1, w: 5.7, h: 3.9, fontFace: FONT, fontSize: 12, color: INK, margin: 0, valign: "top", paraSpaceAfter: 4 });
  takeaway(s, "Google rewards the freshest, most complete answer. Your competitors have been rewriting; your pages have been standing still for 18 months.");
}

// ================================================================ 5. Google changed the page
{
  const s = contentSlide("Why it happened", "Google now answers the question before anyone clicks. Getting back to #1 will not bring back all the clicks.",
    { source: "Source: live Google results, 12 October 2026. Click-rate benchmark: Ahrefs, February 2026, 300,000 searches." });
  // mock search page
  const x0 = 0.6, y0 = 2.0, w0 = 6.4;
  s.addShape(pres.shapes.RECTANGLE, { x: x0, y: y0, w: w0, h: 4.0, fill: { color: PALE }, line: { color: LIGHT, width: 1 } });
  s.addText("Google   \"what is expense management\"", { x: x0 + 0.25, y: y0 + 0.12, w: w0 - 0.5, h: 0.35, fontFace: FONT, fontSize: 11, color: MID, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: x0 + 0.25, y: y0 + 0.55, w: w0 - 0.5, h: 1.05, fill: { color: "FFEAE1" }, line: { color: ORANGE, width: 1.5 } });
  s.addText([{ text: "AI Overview", options: { bold: true, color: ORANGE, breakLine: true } }, { text: "Expense management is the process a business uses to track, control, approve and reimburse employee spending...", options: { color: INK } }],
    { x: x0 + 0.4, y: y0 + 0.62, w: w0 - 0.8, h: 0.92, fontFace: FONT, fontSize: 10.5, margin: 0, valign: "top" });
  const results = [["1", "NetSuite", "updated Jul 2025"], ["2", "Medius", ""], ["3", "Ramp", "updated Jul 2026"], ["4", "Your page", "last updated Jan 2024"], ["5", "Airwallex", "updated May 2026"]];
  results.forEach((r, i) => {
    const yy = y0 + 1.75 + i * 0.44;
    const mine = r[1] === "Your page";
    s.addShape(pres.shapes.RECTANGLE, { x: x0 + 0.25, y: yy, w: w0 - 0.5, h: 0.38, fill: { color: mine ? LIGHT : WHITE }, line: { color: mine ? CHAR : LIGHT, width: mine ? 1.25 : 0.75 } });
    s.addText([{ text: r[0] + "   ", options: { color: GREY } }, { text: r[1], options: { bold: true, color: mine ? CHAR : INK } }, { text: r[2] ? "     " + r[2] : "", options: { color: mine ? ORANGE : GREY } }],
      { x: x0 + 0.4, y: yy, w: w0 - 0.8, h: 0.38, fontFace: FONT, fontSize: 11, margin: 0, valign: "middle" });
  });
  stat(s, 7.4, 2.0, 5.3, 1.25, "4 of 5", "of your key searches now show an AI answer above the first result", true);
  stat(s, 7.4, 3.4, 5.3, 1.25, "58% fewer clicks", "to the #1 result when an AI answer is present (industry benchmark)", false);
  s.addText("Your biggest page used to get 14,100 visits a month at #1. Even back at #1, with the AI answer sitting on top, it will not get there again. The recovery has to come from more pages, not from one page returning to its old number.",
    { x: 7.4, y: 4.8, w: 5.3, h: 1.2, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top" });
  takeaway(s, "This is the single biggest reason a target of \"back to 140K visits\" is the wrong promise. The page has changed under everyone, including Ramp.");
}

// ================================================================ 6. Not a penalty, not links
{
  const s = contentSlide("What it is not", "This is not a Google penalty and not a shortage of links. Your best-linked pages fell too.",
    { source: "Source: sites linking to each page (referring domains) and ranking change, your 18 biggest pages" });
  s.addChart(pres.ChartType.bar, [
    { name: "Pages that fell", labels: ["Expense mgmt guide", "Fraud statistics", "Corporate card guide", "Expense categories", "Travel policy", "Spend mgmt guide"], values: [84, 74, 61, 52, 0, 0] },
    { name: "Pages that grew", labels: ["Expense mgmt guide", "Fraud statistics", "Corporate card guide", "Expense categories", "Travel policy", "Spend mgmt guide"], values: [0, 0, 0, 0, 26, 11] },
  ], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 7.6, h: 3.95, barDir: "col", barGapWidthPct: 60, barGrouping: "clustered", barOverlapPct: 100, chartColors: [ORANGE, CHAR], showValue: true, dataLabelFormatCode: "0;;", dataLabelPosition: "outEnd",
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisHidden: true, valGridLine: { style: "none" }, showLegend: true, legendPos: "t", showTitle: true, title: "Number of websites linking to the page", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR, catAxisLabelFontSize: 10,
  });
  s.addText([
    { text: "Three signs this is not a penalty", options: { bold: true, color: CHAR, breakLine: true, fontSize: 14 } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "5 of your 18 top pages, on the same site and template, held or grew. A penalty drags everything down.", options: { bullet: true, breakLine: true } },
    { text: "The four pages with the most links all fell. The two that grew have far fewer. Links did not decide this.", options: { bullet: true, breakLine: true } },
    { text: "The drops match page age, not link counts.", options: { bullet: true, breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "We will still run a full check of your link profile in week one. If anything looks manufactured, we deal with it first. We do not expect to find it.", options: { color: MID } },
  ], { x: 8.5, y: 2.1, w: 4.2, h: 3.9, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top", paraSpaceAfter: 4 });
  takeaway(s, "Buying or chasing links would be money spent on the wrong problem. The fix is the content and the pages themselves.");
}

// ================================================================ 7. The traffic that left was not the traffic that paid
{
  const s = contentSlide("The real question", "Almost half of the lost visits came from pages that have never produced a lead.",
    { source: "Source: leads (conversions) in the last 90 days by page, your 18 biggest pages" });
  s.addChart(pres.ChartType.bar, [
    { name: "From pages with zero leads: 16,460", labels: ["Lost visits"], values: [16460] },
    { name: "From pages that produce leads: 19,250", labels: ["Lost visits"], values: [19250] },
  ], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 7.6, h: 2.0, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 30, chartColors: [ORANGE, CHAR], showValue: true, dataLabelFormatCode: "#,##0", dataLabelColor: WHITE,
    valAxisHidden: true, valGridLine: { style: "none" }, catAxisHidden: true, showLegend: true, legendPos: "b", showTitle: true, title: "The 35,710 monthly visits your top pages lost, split by whether the page ever produces a lead", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR,
  });
  stat(s, 0.6, 4.3, 3.6, 1.6, "46%", "of lost visits were on pages with zero leads in 90 days", false);
  stat(s, 4.4, 4.3, 3.8, 1.6, "4 pages", "produce 77.5% of all your leads from search", true);
  s.addText([
    { text: "Example", options: { bold: true, color: CHAR, breakLine: true, fontSize: 14 } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "Your \"per diem rates 2022\" page used to bring 7,800 visits a month. It brought zero leads. Winning that traffic back would make the traffic chart look better and change nothing for sales.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "Your \"vs Ramp\" comparison page brings 1,100 visits a month and 44 leads. It is the most valuable page on the site and it has slipped from 6th to 11th.", options: {} },
  ], { x: 8.5, y: 2.1, w: 4.2, h: 3.9, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top" });
  takeaway(s, "Chasing the old traffic number means spending the budget on pages that never paid. We would rather spend it on the ones that do.");
}

// ================================================================ 8. Which pages bring leads
{
  const s = contentSlide("The real question", "Comparison pages turn visitors into leads about 7 times better than your site average.",
    { source: "Source: leads in the last 90 days per 1,000 visits, grouped by topic. Site average across the 18 pages: 1.85." });
  s.addChart(pres.ChartType.bar, [{ name: "Leads per 1,000 visits", labels: ["Comparison pages (vs Ramp, vs Brex)", "Corporate card guide", "Core expense management guides and templates", "Rates and deadlines pages", "Off-topic finance pages"], values: [12.0, 2.5, 0.68, 0.61, 0] }], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 8.2, h: 4.0, barDir: "bar", barGapWidthPct: 45, chartColors: [ORANGE], showValue: true, dataLabelFormatCode: "0.0", dataLabelPosition: "outEnd",
    valAxisMinVal: 0, valAxisMaxVal: 14, valAxisHidden: true, valGridLine: { style: "none" }, catAxisOrientation: "maxMin", catAxisLabelFontSize: 11,
  });
  s.addText([
    { text: "What this means for the plan", options: { bold: true, color: CHAR, breakLine: true, fontSize: 14 } },
    { text: " ", options: { breakLine: true, fontSize: 6 } },
    { text: "The comparison pages are small in traffic and huge in leads. They get fixed first.", options: { bullet: true, breakLine: true } },
    { text: "The big guides still matter: they hold most of your authority and feed the comparison pages. They get refreshed, not abandoned.", options: { bullet: true, breakLine: true } },
    { text: "The rates, deadlines and off-topic pages get tidied up and no new investment.", options: { bullet: true, breakLine: true } },
  ], { x: 9.1, y: 2.1, w: 3.6, h: 3.9, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top", paraSpaceAfter: 4 });
  takeaway(s, "One caveat we will close in week one: a lead is only worth counting if sales can use it. We need your CRM data to confirm which pages bring the good ones.");
}

// ================================================================ 9. The KPI
{
  const s = contentSlide("The proposal", "Measure what reaches sales, not what reaches the site.", { source: "" });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.0, w: 5.8, h: 3.95, fill: { color: PALE }, line: { color: LIGHT, width: 1 } });
  s.addText("TODAY'S TARGET", { x: 0.9, y: 2.2, w: 5.2, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: GREY, charSpacing: 2, margin: 0 });
  s.addText("Back to 140,000 visits a month", { x: 0.9, y: 2.55, w: 5.2, h: 0.8, fontFace: FONT, fontSize: 22, bold: true, color: CHAR, margin: 0, valign: "top" });
  s.addText([
    { text: "The number has no stated source. If it came from a ranking tool it is an estimate, not real visits.", options: { bullet: true, breakLine: true } },
    { text: "46% of what was lost never produced a lead.", options: { bullet: true, breakLine: true } },
    { text: "The AI answer on your biggest searches means the old pages cannot return to their old numbers.", options: { bullet: true, breakLine: true } },
    { text: "Hitting it would prove traffic went up. It would not prove the business got anything.", options: { bullet: true } },
  ], { x: 0.9, y: 3.45, w: 5.2, h: 2.4, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top", paraSpaceAfter: 5 });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.9, y: 2.0, w: 5.8, h: 3.95, fill: { color: CHAR }, line: { color: CHAR } });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.9, y: 2.0, w: 5.8, h: 0.08, fill: { color: ORANGE }, line: { color: ORANGE } });
  s.addText("WHAT WE PROPOSE", { x: 7.2, y: 2.2, w: 5.2, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: ORANGE, charSpacing: 2, margin: 0 });
  s.addText("Qualified leads from search, by page, with pipeline value", { x: 7.2, y: 2.55, w: 5.2, h: 0.8, fontFace: FONT, fontSize: 22, bold: true, color: WHITE, margin: 0, valign: "top" });
  s.addText([
    { text: "Counted from your own analytics and CRM, not a third-party estimate.", options: { bullet: true, breakLine: true } },
    { text: "Only leads that sales accepts count. A download is not a lead.", options: { bullet: true, breakLine: true } },
    { text: "Reported by page, so we know which content pays and double down on it.", options: { bullet: true, breakLine: true } },
    { text: "Traffic stays on the dashboard as a health check, split into branded and non-branded.", options: { bullet: true } },
  ], { x: 7.2, y: 3.45, w: 5.2, h: 2.4, fontFace: FONT, fontSize: 11.5, color: LIGHT, margin: 0, valign: "top", paraSpaceAfter: 5 });
  takeaway(s, "Our 12-month commitment is to roughly double qualified leads from search. Traffic will recover too, and we will say exactly how far on slide 12.");
}

// ================================================================ 10. The plan in four moves
{
  const s = contentSlide("The plan", "Four moves, in this order. The first one starts in week one.", { source: "" });
  const cw = 2.9, gap = 0.17, y = 2.0, h = 2.75;
  card(s, 0.6, y, cw, h, "1. Fix the pages that make money", "Rebuild the \"vs Ramp\" comparison with a proper side-by-side table and a clear next step. Bring the \"vs Brex\" page to the same standard. Point your strongest pages at them.");
  card(s, 0.6 + (cw + gap), y, cw, h, "2. Refresh what is old", "Rewrite the big guides for 2026 with the current rules and a short, quotable answer at the top so Google's AI answer can cite you. Then work through the rest of the 400 posts, oldest and most valuable first.", CHAR);
  card(s, 0.6 + 2 * (cw + gap), y, cw, h, "3. Retire what is dead", "Redirect the two expired dated pages to permanent versions. Remove the off-topic pages. Merge the two pages competing for the same search into one.", CHAR);
  card(s, 0.6 + 3 * (cw + gap), y, cw, h, "4. Earn links to what sells", "No paid links. One original data report a quarter from your anonymized spend data, templates and tools people link to naturally, and your strongest pages linking to the comparison pages.", CHAR);
  s.addText([
    { text: "What ships in the first 30 days", options: { bold: true, color: CHAR, breakLine: true, fontSize: 13 } },
    { text: "The \"vs Ramp\" rebuild, the biggest guide refreshed, the two expired pages redirected, the two off-topic pages removed, the duplicate merged, and the measurement set up so every later change can be proven.", options: {} },
  ], { x: 0.6, y: 4.95, w: 12.1, h: 1.05, fontFace: FONT, fontSize: 11.5, color: INK, margin: 0, valign: "top" });
  takeaway(s, "Every one of the 400 posts gets one of four decisions: protect, refresh, merge or retire. About half get work; all of them get a decision.");
}

// ================================================================ 11. Ramp
{
  const s = contentSlide("The competition", "We will not out-publish Ramp. We win where they do not play.", { source: "Source: Ramp's publishing pace from your brief; linking sites gained per month from a public backlink index, 12 months to September 2026" });
  stat(s, 0.6, 2.0, 3.9, 1.3, "100 vs 48", "posts a year: Ramp's pace against yours", false);
  stat(s, 4.7, 2.0, 3.9, 1.3, "340", "new websites linking to Ramp every month", false);
  stat(s, 8.8, 2.0, 3.9, 1.3, "5x", "your traffic. Ramp is a much bigger site", true);
  const cw = 3.9, y = 3.5, h = 2.5;
  card(s, 0.6, y, cw, h, "Fight", "Comparison and alternatives pages (your highest-value traffic). The corporate card decision guide. The core expense management guides, on depth and freshness.", ORANGE);
  card(s, 4.7, y, cw, h, "Flank", "Templates and tools: policy templates, category sheets, a mileage calculator. Original data from your spend data. The spend management topic, where you are already growing.", GOLD);
  card(s, 8.8, y, cw, h, "Concede", "Generic finance education (invoicing, bookkeeping, accounting software lists). Per diem and tax deadline rate pages that government sites own. Consumer searches like receipt scanning apps.", GREY);
  takeaway(s, "Ramp is a volume publisher. Volume is the one game we cannot win on this budget, so we do not enter it.");
}

// ================================================================ 12. What to expect
{
  const s = contentSlide("What to expect", "By month 12: about twice the leads from search, and traffic back to roughly 117K. Not 140K, and here is why.",
    { source: "Projection, not a forecast. Every assumption is listed in the working model and gets replaced with measured numbers at day 90." });
  s.addChart(pres.ChartType.line, [{ name: "Monthly visits (projection)", labels: ["Today", "Month 3", "Month 6", "Month 9", "Month 12"], values: [85000, 92000, 105000, 113000, 117000] }], {
    ...axisOpts(), x: 0.6, y: 2.0, w: 6.0, h: 3.5, chartColors: [ORANGE], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 8, showValue: true, dataLabelFormatCode: "#,##0", dataLabelPosition: "t",
    valAxisMinVal: 60000, valAxisMaxVal: 150000, valAxisLabelFormatCode: "#,##0", showTitle: true, title: "Monthly visits from Google (projection)", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR,
  });
  s.addChart(pres.ChartType.line, [{ name: "Qualified leads (today = 100)", labels: ["Today", "Month 3", "Month 6", "Month 9", "Month 12"], values: [100, 115, 150, 180, 220] }], {
    ...axisOpts(), x: 6.8, y: 2.0, w: 5.9, h: 3.5, chartColors: [CHAR], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 8, showValue: true, dataLabelFormatCode: "0", dataLabelPosition: "t",
    valAxisMinVal: 0, valAxisMaxVal: 260, showTitle: true, title: "Qualified leads from search, indexed to today = 100 (projection)", titleFontFace: FONT, titleFontSize: 12, titleColor: CHAR,
  });
  s.addText("Why not 140K: your biggest searches now have an AI answer on top, and the two expired pages were queries that government sites now own. The old pages top out near 117K even if every refresh works. Anything above that comes from new comparison pages and templates. We would rather tell you this now than explain it in month 12.",
    { x: 0.6, y: 5.55, w: 12.1, h: 0.6, fontFace: FONT, fontSize: 11, color: MID, margin: 0, valign: "top" });
  takeaway(s, "The traffic line recovers. The leads line is the one we are accountable for, and it moves faster because the first fixes land on the pages that convert.", 6.25, 0.55);
}

// ================================================================ 13. First 90 days
{
  const s = contentSlide("The first 90 days", "You will see the first signals within 90 days, and we have agreed in advance what we do if they do not move.", { source: "" });
  const rows = [
    [{ text: "What we watch", options: { bold: true, color: WHITE, fill: { color: CHAR } } }, { text: "Target by day 90", options: { bold: true, color: WHITE, fill: { color: CHAR } } }, { text: "If it does not move", options: { bold: true, color: WHITE, fill: { color: CHAR } } }],
    ["Rankings for your four most important searches", "\"vs Ramp\" back in the top 8; the two big guides up 2 places", "The problem is page format and authority. We shift budget from rewriting to the data report and change the page format."],
    ["Refreshed pages against a matched set we leave alone", "Refreshed pages get 20% more impressions than the untouched set", "We stop at 24 refreshes and go back to the data before spending more."],
    ["Leads from the comparison pages", "Lead rate up 25% on the rebuilt pages", "The offer, not the page, is the problem. We hand it to product marketing."],
    ["Clean-up done", "Expired pages redirected, duplicate merged, off-topic pages removed", "This one is simply done or not done."],
    ["Page speed on the blog", "Blog loads under 2.5 seconds in testing", "We escalate to the next engineering sprint rather than spending the first one twice."],
  ];
  s.addTable(rows, { x: 0.6, y: 2.0, w: 12.1, colW: [3.4, 3.9, 4.8], fontFace: FONT, fontSize: 11, color: INK, border: { type: "solid", color: "D9DEE3", pt: 0.75 }, valign: "middle", rowH: 0.62, margin: 0.08, fill: { color: WHITE } });
  takeaway(s, "No waiting a year to find out. Each signal has a number attached and a pre-agreed response.", 6.15, 0.62);
}

// ================================================================ 14. What we need from you
{
  const s = contentSlide("What we need from you", "Three decisions and five pieces of data, all in week one.", { source: "" });
  card(s, 0.6, 2.0, 5.9, 3.95, "Decisions", "", ORANGE);
  s.addText([
    { text: "Sign off on the KPI: qualified leads from search, by page.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Agree in writing what counts as a lead. A demo request yes, a template download no.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Legal sign-off to publish anonymized, aggregated spend data as a research report.", options: { bullet: { type: "number" } } },
  ], { x: 0.85, y: 2.75, w: 5.4, h: 3.0, fontFace: FONT, fontSize: 12.5, color: INK, margin: 0, valign: "top", paraSpaceAfter: 8 });
  card(s, 6.8, 2.0, 5.9, 3.95, "Data", "", CHAR);
  s.addText([
    { text: "Search Console access, full history (16 months).", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "Analytics: visits and leads by landing page, this year and last.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "CRM: which leads became opportunities, by landing page.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "The last-modified date for every blog post from WordPress.", options: { bullet: { type: "number" }, breakLine: true } },
    { text: "One engineering sprint per quarter, confirmed in the calendar.", options: { bullet: { type: "number" } } },
  ], { x: 7.05, y: 2.75, w: 5.4, h: 3.0, fontFace: FONT, fontSize: 12.5, color: INK, margin: 0, valign: "top", paraSpaceAfter: 8 });
  takeaway(s, "With these in hand, the first fixes go live inside 30 days and the baseline is real, not estimated.");
}

// ================================================================ 15. Close
{
  const s = pres.addSlide(); n += 1;
  s.background = { color: DARK };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.35, h: H, fill: { color: ORANGE }, line: { color: ORANGE } });
  wordmark(s, 0.9, 0.6, 20, WHITE, true);
  s.addText("Next steps", { x: 0.9, y: 1.8, w: 11, h: 0.8, fontFace: FONT, fontSize: 34, bold: true, color: WHITE, margin: 0 });
  s.addText([
    { text: "This week: a 45-minute working session to agree the KPI and the lead definition.", options: { bullet: true, breakLine: true } },
    { text: "Week one: data access and the link check. You get a one-page diagnosis note.", options: { bullet: true, breakLine: true } },
    { text: "Day 30: the first seven fixes live and the measurement in place.", options: { bullet: true, breakLine: true } },
    { text: "Day 90: the five signals reviewed together, and the decision to continue, adjust or re-diagnose.", options: { bullet: true } },
  ], { x: 0.9, y: 2.8, w: 11.2, h: 2.6, fontFace: FONT, fontSize: 16, color: LIGHT, margin: 0, valign: "top", paraSpaceAfter: 10 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.9, y: 5.6, w: 1.6, h: 0.06, fill: { color: ORANGE }, line: { color: ORANGE } });
  s.addText([{ text: "Qasim Khursheed, Single Grain", options: { breakLine: true, color: WHITE, bold: true } }, { text: "khursheed-qasim@outlook.com", options: { color: GREY } }],
    { x: 0.9, y: 5.8, w: 8, h: 0.8, fontFace: FONT, fontSize: 13, margin: 0, valign: "top" });
}

pres.writeFile({ fileName: process.argv[2] || "SEO_recovery_plan_client_deck.pptx" }).then(f => console.log("written", f));
