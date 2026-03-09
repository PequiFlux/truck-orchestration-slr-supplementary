from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT.parent / "data_extraction.xls"
BIB_FILE = ROOT.parent / "Artigos ICPR.bib"
DOCS_DIR = ROOT / "docs"


def parse_bib_entries(text):
    chunks = re.split(r"(?=@\w+\{)", text)
    entries = []
    for chunk in chunks:
        if not chunk.strip().startswith("@"):
            continue
        doi = ""
        title = ""
        key = ""
        mkey = re.match(r"@(\w+)\{([^,]+),", chunk)
        if mkey:
            key = mkey.group(2)
        mdoi = re.search(r"\bdoi\s*=\s*\{([^}]+)\}", chunk, re.I)
        if mdoi:
            doi = mdoi.group(1).strip().lower()
        mtitle = re.search(r"\btitle\s*=\s*\{(.+?)\},\n", chunk, re.I | re.S)
        if mtitle:
            title = re.sub(r"\s+", " ", mtitle.group(1)).strip().lower()
        entries.append({"key": key, "doi": doi, "title": title, "raw": chunk.strip()})
    return entries


def sanitize_key(text, fallback):
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return cleaned[:40] or fallback


def build_manual_bib_entry(row, idx):
    title = str(row["article"]).replace("{", "").replace("}", "")
    authors_year = str(row["Authors (Year)"])
    year_match = re.search(r"(19|20)\d{2}", authors_year)
    year = year_match.group(0) if year_match else "0000"
    authors = re.sub(r"\s*\(\d{4}\)", "", authors_year).strip()
    doi = str(row["DOI/ISBN"]).strip()
    key = sanitize_key(authors + year, f"manual{idx}")
    return "\n".join(
        [
            f"@misc{{{key},",
            f"  title = {{{title}}},",
            f"  author = {{{authors}}},",
            f"  year = {{{year}}},",
            f"  doi = {{{doi}}},",
            "}",
        ]
    )


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(DATA_FILE, sheet_name="Articles")
    bib_entries = parse_bib_entries(BIB_FILE.read_text(encoding="utf-8"))
    doi_map = {entry["doi"]: entry["raw"] for entry in bib_entries if entry["doi"]}
    title_map = {entry["title"]: entry["raw"] for entry in bib_entries if entry["title"]}

    exported = []
    markdown_lines = [
        "# Full Reference List",
        "",
        "This file provides a readable reference list for the extracted studies.",
        "",
    ]

    for idx, row in df.iterrows():
        doi = str(row["DOI/ISBN"]).strip().lower()
        title = str(row["article"]).strip().lower()
        raw = doi_map.get(doi) or title_map.get(title)
        if raw is None:
            raw = build_manual_bib_entry(row, idx + 1)
        exported.append(raw)
        markdown_lines.append(
            f"{idx + 1}. {row['Authors (Year)']}. *{row['article']}*. DOI/ISBN: {row['DOI/ISBN']}."
        )

    (DOCS_DIR / "full_references.bib").write_text("\n\n".join(exported) + "\n", encoding="utf-8")
    (DOCS_DIR / "full_references.md").write_text("\n".join(markdown_lines) + "\n", encoding="utf-8")
    print(f"Exported {len(exported)} references.")


if __name__ == "__main__":
    main()
