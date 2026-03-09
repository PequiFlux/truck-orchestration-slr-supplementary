# Supplementary Material for the SLR on Truck and Physical Resource Orchestration

This repository provides the supplementary material associated with the systematic literature review on computational methods for truck and physical resource orchestration in logistics terminals.

## Contents

- `data/raw/data_extraction.xls`: original extraction spreadsheet used during the review.
- `data/raw/data_extraction.csv`: CSV export of the extraction matrix for easier reuse.
- `data/raw/quality_assessment_scores.csv`: recoverable quality-assessment matrix and status notes.
- `data/derived/included_studies_list.csv`: cleaned list of the 34 extracted studies with core metadata.
- `docs/full_references.bib`: BibTeX reference list for the extracted studies.
- `docs/full_references.md`: readable reference list for the extracted studies.
- `docs/review_protocol_summary.md`: concise summary of the protocol, PRISMA flow, and quality-assessment rule.
- `docs/search_strings.md`: exact preserved Boolean query and source notes.
- `docs/quality_assessment_note.md`: transparency note about the currently recoverable QA data.
- `docs/figure_catalog.md`: index of the generated figures.
- `figures/`: visual summaries generated from the extraction matrix.
- `figures/prisma_flow_diagram_tikz.tex`: native LaTeX/TikZ source for the PRISMA flow diagram.
- `scripts/generate_all_figures.py`: reproducible script that regenerates the figure set.
- `scripts/generate_prisma_diagram.py`: reproducible script for the PRISMA flow diagram.
- `scripts/build_reference_exports.py`: script that exports the reference list files.

## Review Flow Used in the Manuscript

- Database searches (`IEEE Xplore`, `Web of Science`, `Scopus`): 60 records
- Deduplication removed: 18 records
- Records remaining after deduplication: 42
- Records excluded for inaccessible full text: 13
- Records added by backward snowballing: 8
- Studies entering quality assessment: 37
- Studies excluded with score `<= 7.5`: 3
- Final review base: 34 studies

## Quality Assessment Rule

- `Yes = 1`
- `Partially = 0.5`
- `No = 0`
- Studies were retained only when total score was `> 7.5`.

## Purpose

The repository is intended to improve transparency, auditability, and reuse of the review corpus by making the extracted-study list, raw matrix, and complementary notes openly available.
