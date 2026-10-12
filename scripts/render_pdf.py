#!/usr/bin/env python3
"""Render the submission Markdown to a compact PDF and report the page count.
Usage: python3 render_pdf.py in.md out.pdf"""
import sys, subprocess, markdown
from pathlib import Path
from pypdf import PdfReader

src, out = Path(sys.argv[1]), Path(sys.argv[2])
body = markdown.markdown(src.read_text(), extensions=["tables", "fenced_code"])
css = """
@page { size: A4; margin: 12mm 14mm 12mm 14mm; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; line-height: 1.27; color: #111; }
h1 { font-size: 15pt; margin: 0 0 4pt 0; }
h2 { font-size: 11.5pt; margin: 9pt 0 3pt 0; border-bottom: 1px solid #999; padding-bottom: 1pt; page-break-after: avoid; }
tr { page-break-inside: avoid; }
h3 { font-size: 10.3pt; margin: 7pt 0 2pt 0; }
p { margin: 0 0 4pt 0; }
ol, ul { margin: 0 0 4pt 0; padding-left: 16pt; }
li { margin: 0 0 1.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0 6pt 0; font-size: 9.2pt; }
th, td { border: 1px solid #bbb; padding: 2pt 4pt; vertical-align: top; text-align: left; }
th { background: #eef1f6; }
code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 8.9pt; }
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
tmp = out.with_suffix(".html"); tmp.write_text(html)
subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "--page-size", "A4",
                "-T", "12mm", "-B", "12mm", "-L", "14mm", "-R", "14mm", str(tmp), str(out)], check=True)
print("pages:", len(PdfReader(str(out)).pages))
