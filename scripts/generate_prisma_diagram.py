from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
DOCS_DIR = ROOT / "docs"


def add_box(ax, xy, width, height, title, body, fc="#f6f7fb", ec="#334155"):
    x, y = xy
    rect = Rectangle((x, y), width, height, facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + width / 2, y + height * 0.72, title, ha="center", va="center", fontsize=11, fontweight="bold")
    ax.text(x + width / 2, y + height * 0.35, body, ha="center", va="center", fontsize=10)


def add_arrow(ax, start, end):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.4, color="#475569")
    ax.add_patch(arrow)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "serif", "figure.dpi": 180})

    fig, ax = plt.subplots(figsize=(8.5, 7.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    add_box(ax, (2.2, 11.7), 5.6, 1.45, "Identification", "Database-search records\\nIEEE + WoS + Scopus = 60")
    add_box(ax, (2.2, 9.7), 5.6, 1.45, "Deduplication", "Duplicates removed = 18\\nRecords remaining = 42", fc="#eef6ff")
    add_box(ax, (2.2, 7.7), 5.6, 1.45, "Screening", "Abstract screening applied\\nFull-text unavailable = 13\\nRecords remaining = 29", fc="#f6fbef")
    add_box(ax, (2.2, 5.7), 5.6, 1.45, "Additional Identification", "Backward snowballing added = 8\\nStudies entering QA = 37", fc="#fff7ed")
    add_box(ax, (2.2, 3.7), 5.6, 1.45, "Quality Assessment", "Threshold rule: retain if score > 7.5\\nExcluded with score <= 7.5 = 3", fc="#fdf2f8")
    add_box(ax, (2.2, 1.7), 5.6, 1.45, "Included", "Final review base = 34 studies", fc="#ecfeff")

    add_arrow(ax, (5.0, 11.7), (5.0, 11.15))
    add_arrow(ax, (5.0, 9.7), (5.0, 9.15))
    add_arrow(ax, (5.0, 7.7), (5.0, 7.15))
    add_arrow(ax, (5.0, 5.7), (5.0, 5.15))
    add_arrow(ax, (5.0, 3.7), (5.0, 3.15))

    ax.text(5.0, 13.55, "PRISMA Flow Diagram for the Review Corpus", ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(
        5.0,
        0.7,
        "Flow reconstructed from the review protocol and manuscript-consistent screening counts.",
        ha="center",
        va="center",
        fontsize=9,
    )

    png = FIG_DIR / "prisma_flow_diagram.png"
    pdf = FIG_DIR / "prisma_flow_diagram.pdf"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)

    catalog = DOCS_DIR / "figure_catalog.md"
    if catalog.exists():
        text = catalog.read_text(encoding="utf-8")
        line = "- `prisma_flow_diagram.png` / `prisma_flow_diagram.pdf`: Visual PRISMA flow diagram for identification, screening, snowballing, quality assessment, and final inclusion.\n"
        if line not in text:
            catalog.write_text(text.rstrip() + "\n" + line, encoding="utf-8")

    print("Generated PRISMA flow diagram.")


if __name__ == "__main__":
    main()
