# Quality-Assessment Data Note

The review protocol used a ten-question quality-assessment checklist with the following rule:

- `Yes = 1`
- `Partially = 0.5`
- `No = 0`
- retain study if total score `> 7.5`
- exclude study if total score `<= 7.5`

## Preservation Status of the Raw QA Matrix

The current local workspace preserves:

- the scoring rule,
- the threshold rule,
- the fact that 37 studies entered quality assessment,
- the fact that 3 studies were excluded by the threshold,
- and the final set of 34 retained studies in the extraction spreadsheet.

However, the exported `.docx`, `.md`, and extraction spreadsheet available in this workspace do **not** preserve the study-by-study responses to the 10 individual quality-assessment questions. For this reason, the CSV file `data/raw/quality_assessment_scores.csv` records all information that is currently recoverable from the local materials, while explicitly flagging fields that were not preserved in the export.

If the original Parsifal project is later exported with the full QA worksheet, this file should be replaced by the complete per-question score matrix for the 37 studies.
