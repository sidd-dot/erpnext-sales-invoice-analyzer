# ERPNext Sales Invoice Code Analyzer

## Overview
This project is a lightweight code intelligence tool built to analyze
a legacy ERPNext module (Sales Invoice). The goal is to quickly extract
structural information from a large, unfamiliar codebase.

## Why ERPNext Sales Invoice?
The Sales Invoice module is a critical part of ERPNext and contains
complex business logic related to billing, taxes, and accounting.
Its size and complexity make it a good candidate for automated analysis.

## What the Tool Does
- Scans Python files in a given directory
- Extracts class and function names
- Generates structured output (JSON)
- Produces a simple relationship diagram (Mermaid)
- Summarizes findings in Markdown

## How to Run
```bash
python src/analyzer.py erpnext/accounts/doctype/sales_invoice
