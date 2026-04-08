"""
Chart generation helpers for the HarnessEval Streamlit dashboard.

Plotly functions return interactive go.Figure objects.
Matplotlib functions (mpl_ prefix) return publication-quality Figure objects
and use lazy imports to avoid loading matplotlib at module level.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

DARK_COLORS: dict[str, str] = {
    "bg": "#0f1117",
    "surface": "#1e2130",
    "text": "#e4e6ed",
    "text2": "#9ca0ad",
    "blue": "#4c8dff",
    "green": "#22c55e",
    "orange": "#f59e0b",
    "red": "#ef4444",
    "purple": "#a78bfa",
    "cyan": "#22d3ee",
}

LIGHT_COLORS: dict[str, str] = {
    "bg": "#ffffff",
    "surface": "#f8f9fa",
    "text": "#1a1d29",
    "text2": "#6c757d",
    "blue": "#4c8dff",
    "green": "#22c55e",
    "orange": "#f59e0b",
    "red": "#ef4444",
    "purple": "#a78bfa",
    "cyan": "#22d3ee",
}

METRIC_COLORS: list[str] = [
    "#4c8dff",
    "#a78bfa",
    "#22d3ee",
    "#f59e0b",
    "#22c55e",
    "#ef4444",
]

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_palette(theme: str) -> dict[str, str]:
    """Return the color palette dict for *theme* ('dark' or 'light')."""
    return LIGHT_COLORS if theme == "light" else DARK_COLORS


def _apply_theme(fig: go.Figure, theme: str) -> go.Figure:
    """Apply background, font, margin and grid colors to *fig* in-place."""
    p = _get_palette(theme)
    grid_color = "rgba(255,255,255,0.08)" if theme != "light" else "rgba(0,0,0,0.08)"
    fig.update_layout(
        paper_bgcolor=p["bg"],
        plot_bgcolor=p["surface"],
        font_color=p["text"],
        margin=dict(l=60, r=30, t=50, b=50),
    )
    fig.update_xaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    return fig


# ---------------------------------------------------------------------------
# Plotly chart functions
# ---------------------------------------------------------------------------


def plotly_metrics_bar(metrics: dict[str, Any], theme: str = "dark") -> go.Figure:
    """Horizontal bar chart of evaluation metrics.

    Parameters
    ----------
    metrics:
        Dict whose values are dicts with ``"label"`` (str) and ``"value"``
        (float 0-1). Keys are metric ids like ``m11``, ``m12``, etc.
    theme:
        ``"dark"`` (default) or ``"light"``.

    Returns
    -------
    go.Figure
    """
    p = _get_palette(theme)

    labels: list[str] = []
    values: list[float] = []
    colors: list[str] = []

    for i, (_, meta) in enumerate(metrics.items()):
        labels.append(meta.get("label", ""))
        values.append(round(float(meta.get("value", 0)) * 100, 2))
        colors.append(METRIC_COLORS[i % len(METRIC_COLORS)])

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition="outside",
            cliponaxis=False,
        )
    )
    fig.update_layout(
        title=dict(text="Evaluation Metrics", font_color=p["text"]),
        xaxis=dict(title="Score (%)", range=[0, 110]),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    _apply_theme(fig, theme)
    return fig


def plotly_grouped_comparison(
    logs: list[dict],
    metric_keys: list[str],
    labels: list[str],
    theme: str = "dark",
) -> go.Figure:
    """Grouped bar chart comparing metrics across multiple experiment logs.

    Parameters
    ----------
    logs:
        Each element is a dict whose keys include the metric keys. Values are
        expected to be floats in 0-1 range and will be displayed as %.
    metric_keys:
        Subset of metric keys to compare (e.g. ``["m11", "m21"]``).
    labels:
        Human-readable names for each log in *logs* (same length as *logs*).
    theme:
        ``"dark"`` or ``"light"``.

    Returns
    -------
    go.Figure
    """
    p = _get_palette(theme)
    fig = go.Figure()

    for i, (log, label) in enumerate(zip(logs, labels)):
        y_vals = [round(float(log.get(k, 0)) * 100, 2) for k in metric_keys]
        fig.add_trace(
            go.Bar(
                name=label,
                x=metric_keys,
                y=y_vals,
                marker_color=METRIC_COLORS[i % len(METRIC_COLORS)],
                text=[f"{v:.1f}%" for v in y_vals],
                textposition="outside",
            )
        )

    fig.update_layout(
        title=dict(text="Metric Comparison", font_color=p["text"]),
        barmode="group",
        yaxis=dict(title="Score (%)"),
        xaxis=dict(title="Metric"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    _apply_theme(fig, theme)
    return fig


def plotly_variance_pie(anova_results: list, theme: str = "dark") -> go.Figure:
    """Doughnut chart showing variance explained by each ANOVA source.

    Parameters
    ----------
    anova_results:
        List of objects with ``.source`` (str) and ``.eta_squared`` (float)
        attributes.
    theme:
        ``"dark"`` or ``"light"``.

    Returns
    -------
    go.Figure
    """
    p = _get_palette(theme)

    sources = [r.source for r in anova_results]
    eta_sq = [float(r.eta_squared) for r in anova_results]

    fig = go.Figure(
        go.Pie(
            labels=sources,
            values=eta_sq,
            hole=0.45,
            marker_colors=METRIC_COLORS[: len(sources)],
            textinfo="label+percent",
            hovertemplate="%{label}: eta²=%{value:.4f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Variance Explained (eta²)", font_color=p["text"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    _apply_theme(fig, theme)
    return fig


def plotly_effect_size_bar(anova_results: list, theme: str = "dark") -> go.Figure:
    """Horizontal bar chart of eta-squared effect sizes.

    Bars are colored green if ``p_value < 0.05 / 7`` (Bonferroni-corrected),
    gray otherwise. The ``"Error"`` source is excluded.

    Parameters
    ----------
    anova_results:
        List of objects with ``.source`` (str), ``.eta_squared`` (float), and
        ``.p_value`` (float) attributes.
    theme:
        ``"dark"`` or ``"light"``.

    Returns
    -------
    go.Figure
    """
    p = _get_palette(theme)
    threshold = 0.05 / 7  # Bonferroni correction for 7 comparisons

    sources: list[str] = []
    eta_values: list[float] = []
    colors: list[str] = []

    for r in anova_results:
        if r.source == "Error":
            continue
        sources.append(r.source)
        eta_values.append(float(r.eta_squared))
        sig_color = p["green"] if float(r.p_value) < threshold else p["text2"]
        colors.append(sig_color)

    fig = go.Figure(
        go.Bar(
            x=eta_values,
            y=sources,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.4f}" for v in eta_values],
            textposition="outside",
            cliponaxis=False,
        )
    )
    fig.update_layout(
        title=dict(text="Effect Size (eta²) — green = significant", font_color=p["text"]),
        xaxis=dict(title="eta²"),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    _apply_theme(fig, theme)
    return fig


# ---------------------------------------------------------------------------
# Matplotlib chart functions (publication quality)
# ---------------------------------------------------------------------------


def mpl_variance_pie(anova_results: list):
    """Publication-quality doughnut chart of ANOVA variance explained.

    Parameters
    ----------
    anova_results:
        List of objects with ``.source`` (str) and ``.eta_squared`` (float).

    Returns
    -------
    matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt

    sources = [r.source for r in anova_results]
    eta_sq = [float(r.eta_squared) for r in anova_results]
    colors = METRIC_COLORS[: len(sources)]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        eta_sq,
        labels=sources,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=1.5),
        pctdistance=0.75,
    )
    for t in texts:
        t.set_fontsize(10)
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")

    ax.set_title("Variance Explained (eta²)", fontsize=13, fontweight="bold", pad=16)
    fig.tight_layout()
    return fig


def mpl_effect_forest(pairwise_results: list[dict]):
    """Forest plot of pairwise Cohen's d effect sizes.

    Parameters
    ----------
    pairwise_results:
        List of dicts with keys:

        - ``"comparison"`` (str) — label for the row
        - ``"cohens_d"`` (float) — effect size
        - ``"interpretation"`` (str) — e.g. "large", "medium", etc.

    Bar color is determined by ``abs(cohens_d)``:

    - >= 0.8 → blue
    - >= 0.5 → green
    - >= 0.2 → orange
    - else   → gray

    Reference lines are drawn at ±0.2, ±0.5, ±0.8.

    Returns
    -------
    matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    def _color(d: float) -> str:
        a = abs(d)
        if a >= 0.8:
            return DARK_COLORS["blue"]
        if a >= 0.5:
            return DARK_COLORS["green"]
        if a >= 0.2:
            return DARK_COLORS["orange"]
        return "#888888"

    comparisons = [r["comparison"] for r in pairwise_results]
    ds = [float(r["cohens_d"]) for r in pairwise_results]
    colors = [_color(d) for d in ds]

    n = len(comparisons)
    fig, ax = plt.subplots(figsize=(9, max(4, n * 0.55 + 1.5)))

    y_pos = list(range(n))
    ax.barh(y_pos, ds, color=colors, height=0.55, edgecolor="white", linewidth=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(comparisons, fontsize=9)
    ax.invert_yaxis()

    # Reference lines
    for ref in (0.2, 0.5, 0.8):
        for sign in (1, -1):
            ax.axvline(
                sign * ref,
                color="gray",
                linestyle="--",
                linewidth=0.8,
                alpha=0.7,
            )
    ax.axvline(0, color="black", linewidth=1.0)

    ax.set_xlabel("Cohen's d", fontsize=11)
    ax.set_title("Pairwise Effect Sizes (Cohen's d)", fontsize=13, fontweight="bold")

    # Legend patches
    legend_entries = [
        mpatches.Patch(color=DARK_COLORS["blue"], label="|d| ≥ 0.8 (large)"),
        mpatches.Patch(color=DARK_COLORS["green"], label="0.5 ≤ |d| < 0.8 (medium)"),
        mpatches.Patch(color=DARK_COLORS["orange"], label="0.2 ≤ |d| < 0.5 (small)"),
        mpatches.Patch(color="#888888", label="|d| < 0.2 (negligible)"),
    ]
    ax.legend(handles=legend_entries, loc="lower right", fontsize=8, framealpha=0.6)

    fig.tight_layout()
    return fig
