from pathlib import Path
from collections import Counter
import re
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "data_extraction.xls"
FIG_DIR = ROOT / "figures"
DOCS_DIR = ROOT / "docs"


def setup_style():
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 180,
        }
    )


def wrap_labels(labels, width=18):
    return [textwrap.fill(str(label), width=width) for label in labels]


def split_multi(value):
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def count_multilabel(series):
    counter = Counter()
    for value in series:
        parts = split_multi(value)
        if parts:
            for part in parts:
                counter[part] += 1
        elif pd.notna(value) and str(value).strip():
            counter[str(value).strip()] += 1
    return counter


def save_figure(fig, stem):
    png = FIG_DIR / f"{stem}.png"
    pdf = FIG_DIR / f"{stem}.pdf"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return png.name, pdf.name


def horizontal_bar(counter, stem, title, xlabel="Count", top_n=None, color="#3d6f8e"):
    items = counter.most_common(top_n)
    labels = [item[0] for item in items][::-1]
    values = [item[1] for item in items][::-1]
    fig, ax = plt.subplots(figsize=(8.2, max(4.0, 0.42 * len(labels) + 1.2)))
    ax.barh(wrap_labels(labels, 28), values, color=color)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", linestyle=":", alpha=0.35)
    ax.set_axisbelow(True)
    for idx, value in enumerate(values):
        ax.text(value + 0.1, idx, str(value), va="center", fontsize=9)
    return save_figure(fig, stem)


def vertical_bar(counter, stem, title, xlabel="", ylabel="Count", color="#567d46"):
    labels = list(counter.keys())
    values = list(counter.values())
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.bar(wrap_labels(labels, 14), values, color=color)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle=":", alpha=0.35)
    ax.set_axisbelow(True)
    for idx, value in enumerate(values):
        ax.text(idx, value + 0.1, str(value), ha="center", fontsize=9)
    return save_figure(fig, stem)


def heatmap(df, index, columns, stem, title, cmap="YlGnBu"):
    matrix = df.to_numpy()
    fig, ax = plt.subplots(figsize=(8.8, max(4.6, 0.55 * len(index) + 1.5)))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(len(columns)))
    ax.set_yticks(np.arange(len(index)))
    ax.set_xticklabels(wrap_labels(columns, 16))
    ax.set_yticklabels(wrap_labels(index, 22))
    ax.set_title(title, loc="left", fontweight="bold")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = int(matrix[i, j])
            color = "white" if value >= max(1, matrix.max() * 0.55) else "#1f1f1f"
            ax.text(j, i, str(value), ha="center", va="center", fontsize=9, color=color)
    ax.set_xticks(np.arange(len(columns) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(index) + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    return save_figure(fig, stem)


def classify_pain_point(row):
    title = str(row["article"]).lower()
    focus = str(row["Logistic focus"]).lower()
    text = f"{title} {focus}"
    if "cold chain" in text or "perishable" in text:
        return "Cold chain"
    if "gate operations" in text or "queue / congestion management" in text:
        return "Gate / queue"
    if "reactive rescheduling" in text:
        return "Rescheduling"
    if "intermodal terminal transfer" in text or "truck routing" in text:
        return "Integrated flow decisions"
    if (
        "truck-crane joint scheduling" in text
        or "inbound-outbound synchronization" in text
        or "truck dispatching" in text
    ):
        return "Truck-resource synchronization"
    if (
        "yard operations" in text
        or "yard resource scheduling" in text
        or "cross-docking operations" in text
    ):
        return "Internal balancing"
    return "Truck scheduling core"


def classify_dynamic(value):
    text = str(value).lower()
    if "real-time online" in text:
        return "Real-time online"
    if "rolling horizon" in text or "periodic update" in text:
        return "Rolling horizon"
    if "event-driven" in text:
        return "Event-driven"
    return "Static"


def classify_validation(value):
    text = str(value).lower()
    if "real data" in text:
        return "Real data involved"
    if "synthetic data" in text:
        return "Synthetic data"
    if "simulation" in text:
        return "Simulation-based"
    if "computational experiment" in text:
        return "Computational only"
    return "Other / unclear"


def extract_year(author_year):
    match = re.search(r"(19|20)\d{2}", str(author_year))
    return int(match.group(0)) if match else None


def main():
    setup_style()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(DATA_FILE, sheet_name="Articles")

    generated = []

    generated.extend([
        horizontal_bar(
            Counter(df["Application environment"].fillna("not specified")),
            "01_application_environment_distribution",
            "Application environment distribution",
            color="#2f6b8a",
        ),
        horizontal_bar(
            count_multilabel(df["Logistic focus"]),
            "02_logistic_focus_distribution",
            "Logistic focus frequency",
            top_n=12,
            color="#7a8f35",
        ),
        horizontal_bar(
            count_multilabel(df["Technical artifact delivered"]),
            "03_technical_artifact_distribution",
            "Technical artifact frequency",
            color="#8c5a2b",
        ),
        horizontal_bar(
            count_multilabel(df["Uncertainty treatment"]),
            "04_uncertainty_treatment_distribution",
            "Uncertainty-treatment frequency",
            color="#8a3d66",
        ),
        horizontal_bar(
            Counter(df["Real-time/dynamic feature"].fillna("not specified")),
            "05_dynamic_feature_distribution",
            "Dynamic-feature distribution",
            color="#5f6f9c",
        ),
        horizontal_bar(
            count_multilabel(df["Validation type"]),
            "06_validation_type_distribution",
            "Validation-type frequency",
            color="#aa6f39",
        ),
        horizontal_bar(
            count_multilabel(df["Events/disruptions tested"]),
            "07_disruption_frequency",
            "Disruptions tested across studies",
            top_n=10,
            color="#a14d4d",
        ),
        horizontal_bar(
            count_multilabel(df["Performance metrics reported"]),
            "08_metric_frequency",
            "Performance-metric frequency",
            top_n=10,
            color="#4a8f86",
        ),
    ])

    years = [year for year in df["Authors (Year)"].map(extract_year) if year]
    year_counts = Counter(sorted(years))
    generated.append(
        vertical_bar(
            year_counts,
            "09_publication_year_distribution",
            "Publication-year distribution",
            xlabel="Year",
            color="#6d6aa8",
        )
    )

    env_focus = pd.DataFrame(0, index=sorted(df["Application environment"].fillna("not specified").unique()), columns=sorted(count_multilabel(df["Logistic focus"]).keys()))
    for _, row in df.iterrows():
        env = row["Application environment"] if pd.notna(row["Application environment"]) else "not specified"
        for focus in split_multi(row["Logistic focus"]):
            env_focus.loc[env, focus] += 1
    env_focus = env_focus.loc[:, env_focus.sum().sort_values(ascending=False).index[:10]]
    generated.append(
        heatmap(
            env_focus,
            list(env_focus.index),
            list(env_focus.columns),
            "10_environment_vs_focus_heatmap",
            "Application environment versus logistic focus",
            cmap="YlGnBu",
        )
    )

    art_unc = pd.DataFrame(0, index=sorted(count_multilabel(df["Technical artifact delivered"]).keys()), columns=sorted(count_multilabel(df["Uncertainty treatment"]).keys()))
    for _, row in df.iterrows():
        arts = split_multi(row["Technical artifact delivered"])
        uncs = split_multi(row["Uncertainty treatment"])
        for art in arts:
            for unc in uncs:
                art_unc.loc[art, unc] += 1
    art_unc = art_unc.loc[art_unc.sum(axis=1).sort_values(ascending=False).index[:8], art_unc.sum(axis=0).sort_values(ascending=False).index[:8]]
    generated.append(
        heatmap(
            art_unc,
            list(art_unc.index),
            list(art_unc.columns),
            "11_artifact_vs_uncertainty_heatmap",
            "Technical artifact versus uncertainty treatment",
            cmap="YlOrBr",
        )
    )

    df["Pain point"] = df.apply(classify_pain_point, axis=1)
    df["Dynamic class"] = df["Real-time/dynamic feature"].map(classify_dynamic)
    df["Validation class"] = df["Validation type"].map(classify_validation)

    env_pain = (
        df.groupby(["Application environment", "Pain point"])
        .size()
        .unstack(fill_value=0)
    )
    generated.append(
        heatmap(
            env_pain,
            list(env_pain.index),
            list(env_pain.columns),
            "12_environment_vs_painpoint_heatmap",
            "Application environment versus dominant pain point",
            cmap="PuBuGn",
        )
    )

    dyn_val = (
        df.groupby(["Dynamic class", "Validation class"])
        .size()
        .unstack(fill_value=0)
    )
    generated.append(
        heatmap(
            dyn_val,
            list(dyn_val.index),
            list(dyn_val.columns),
            "13_dynamic_vs_validation_heatmap",
            "Dynamic sophistication versus validation maturity",
            cmap="YlOrRd",
        )
    )

    catalog_lines = [
        "# Figure Catalog",
        "",
        "This catalog lists the figures generated from the extraction matrix.",
        "",
    ]
    for png_name, pdf_name in generated:
        title = png_name.replace(".png", "").split("_", 1)[1].replace("_", " ").title()
        catalog_lines.append(f"- `{png_name}` / `{pdf_name}`: {title}.")

    (DOCS_DIR / "figure_catalog.md").write_text("\n".join(catalog_lines) + "\n", encoding="utf-8")
    print(f"Generated {len(generated)} figures and updated figure catalog.")


if __name__ == "__main__":
    main()
