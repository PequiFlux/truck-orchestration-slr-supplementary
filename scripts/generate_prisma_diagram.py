from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
DOCS_DIR = ROOT / "docs"


def add_box(ax, xy, width, height, title, lines, fc="#ffffff", ec="#1f2937", title_fc="#0f172a"):
    x, y = xy
    rect = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.6,
    )
    ax.add_patch(rect)
    ax.text(
        x + width / 2,
        y + height * 0.78,
        title,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=title_fc,
    )
    line_y = y + height * 0.53
    step = height * 0.16
    for line in lines:
        ax.text(
            x + width / 2,
            line_y,
            line,
            ha="center",
            va="center",
            fontsize=10.8,
            color="#334155",
        )
        line_y -= step


def add_arrow(ax, start, end):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=16,
        linewidth=1.6,
        color="#475569",
        connectionstyle="arc3,rad=0.0",
    )
    ax.add_patch(arrow)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 180})

    fig, ax = plt.subplots(figsize=(10.0, 8.2))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15.2)
    ax.axis("off")

    add_box(
        ax,
        (2.1, 12.2),
        5.8,
        1.7,
        "Identification",
        ["Database-search records from IEEE, WoS, and Scopus = 60"],
        fc="#eef4ff",
    )
    add_box(
        ax,
        (2.1, 9.85),
        5.8,
        1.8,
        "Deduplication",
        ["Duplicates removed = 18", "Records remaining after deduplication = 42"],
        fc="#f3f8ff",
    )
    add_box(
        ax,
        (2.1, 7.3),
        5.8,
        1.95,
        "Screening",
        ["Abstract-based inclusion and exclusion screening applied", "Full-text unavailable records excluded = 13", "Records remaining = 29"],
        fc="#f5fbf2",
    )
    add_box(
        ax,
        (7.95, 4.6),
        1.75,
        1.65,
        "Backward Snowballing",
        ["Additional records", "identified from", "references = 8"],
        fc="#fff7ed",
    )
    add_box(
        ax,
        (2.1, 4.55),
        5.8,
        1.65,
        "Quality Assessment Input",
        ["Studies entering quality assessment = 37"],
        fc="#fffaf0",
    )
    add_box(
        ax,
        (2.1, 2.15),
        5.8,
        1.85,
        "Quality Assessment",
        ["Scoring rule: Yes = 1, Partially = 0.5, No = 0", "Studies with score <= 7.5 excluded = 3"],
        fc="#fdf2f8",
    )
    add_box(
        ax,
        (2.1, 0.15),
        5.8,
        1.55,
        "Included",
        ["Final review corpus = 34 studies"],
        fc="#ecfeff",
    )

    add_arrow(ax, (5.0, 12.2), (5.0, 11.7))
    add_arrow(ax, (5.0, 9.85), (5.0, 9.25))
    add_arrow(ax, (5.0, 7.3), (5.0, 6.45))
    add_arrow(ax, (7.9, 5.37), (7.15, 5.37))
    add_arrow(ax, (5.0, 4.55), (5.0, 4.02))
    add_arrow(ax, (5.0, 2.15), (5.0, 1.72))

    ax.text(
        5.0,
        14.55,
        "PRISMA Flow Diagram for the Review Corpus",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#111827",
    )
    ax.text(
        5.0,
        -0.35,
        "Flow reconstructed from the review protocol, abstract screening records, snowballing additions, and the final quality threshold.",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#475569",
    )

    png = FIG_DIR / "prisma_flow_diagram.png"
    pdf = FIG_DIR / "prisma_flow_diagram.pdf"
    fig.savefig(png, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
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
