# SEO Strategy 003: 12-month recovery plan for a declining fintech blog

Submission for the Beat Claude challenge, SEO Strategy 003. Brief version 2026-07.
Qasim Khursheed, October 2026.

## Start here

1. **`SEO_003_submission_Qasim_Khursheed.pdf`** is the written answer (4 pages). The same content is in `SEO_003_submission_Qasim_Khursheed.md`.
2. **`SEO_003_audit_and_refresh_model.xlsx`** is the operating artifact. Open the Start_Here sheet first; it gives the reading order and what the colors mean.
3. **`evidence/`** holds the fixture, the analysis outputs and the live data pulls referenced in the evidence log.
4. **`scripts/`** reproduces every fixture number and rebuilds the workbook.

## Fixture

`evidence/content_audit_sample.csv`, SHA-256 `fa691abc31b14093230657d17674ab0120449c54d20cef54bfe73686fe9b99c6`

## Files

| File | What it is |
|---|---|
| `evidence/content_audit_sample.csv` | The fixture, unchanged |
| `evidence/triage_table.csv` | Every fixture page with derived metrics, decision, rule, priority, action and watch-out |
| `evidence/analysis_output.json` | Decline breakdown, correlations, topic totals, group views |
| `evidence/live_serp_observations_2026-10-12.csv` | Live Google US SERPs for five fixture keywords, with DataForSEO task ids |
| `evidence/ramp_com_historical_rank_overview_2026-10-12.csv` | Ramp's organic footprint, May to October 2026 |
| `evidence/competitor_link_velocity_2026-10-12.csv` | Ramp and Brex new and lost referring domains by month |
| `scripts/analyze_fixture.py` | Reads the fixture, writes the two outputs above |
| `scripts/build_workbook.py` | Builds the workbook from the outputs |
| `scripts/render_pdf.py` | Renders the Markdown to the PDF |

## Reproduce

```
python3 -I scripts/analyze_fixture.py evidence/content_audit_sample.csv evidence/
python3 -I scripts/build_workbook.py evidence/ SEO_003_audit_and_refresh_model.xlsx
```

Needs Python 3 with `scipy` and `openpyxl`. The workbook has 304 formulas; open it in Excel or LibreOffice and it recalculates from the blue input cells.

## Number labels used throughout

[Observed] from the fixture, the brief or a live tool pull. [Estimated] my estimate with the reasoning shown. [Benchmarked] a named outside source. [Assumed] a placeholder to make the plan concrete.
