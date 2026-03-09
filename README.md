# Supplementary Material for the SLR on Truck and Physical Resource Orchestration

This repository provides the supplementary material associated with the systematic literature review on computational methods for truck and physical resource orchestration in logistics terminals.

## Contents

- `data/raw/data_extraction.xls`: original extraction spreadsheet used during the review.
- `data/raw/data_extraction.csv`: CSV export of the extraction matrix for easier reuse.
- `data/derived/included_studies_list.csv`: cleaned list of the 34 extracted studies with core metadata.
- `docs/review_protocol_summary.md`: concise summary of the protocol, PRISMA flow, and quality-assessment rule.
- `figures/corpus_evidence_maps.png`: evidence map used in the manuscript.

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
