"""Tab 5: ANOVA Analysis — Three-way ANOVA, Cohen's d, GLMM robustness, and paper exports."""

from __future__ import annotations

import io
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from harness_eval.pipeline.analysis import (
    ANOVAResult,
    compute_cohens_d,
    compute_three_way_anova,
    tukey_hsd_pairwise,
)
from st_utils.ui_helpers import render_pipeline_banner
from st_utils.charts import (
    mpl_effect_forest,
    mpl_variance_pie,
    plotly_effect_size_bar,
    plotly_variance_pie,
)
from st_utils.data_loader import build_anova_dataframe

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


# ---------------------------------------------------------------------------
# Sample data generator
# ---------------------------------------------------------------------------

def _generate_sample_data() -> pd.DataFrame:
    np.random.seed(42)
    rows = []
    tool_effect = {"full": 0.15, "medium": 0.05, "minimal": -0.10}
    ctx_effect = {"full": 0.10, "sliding_window": 0.02, "summary": -0.05}
    backend_effect = {"claude": 0.08, "gpt": 0.03, "deepseek": -0.05}
    for tool in ["full", "medium", "minimal"]:
        for ctx in ["full", "sliding_window", "summary"]:
            for backend in ["claude", "gpt", "deepseek"]:
                for i in range(50):
                    base = 0.50
                    rate = base + tool_effect[tool] + ctx_effect[ctx] + backend_effect[backend]
                    rows.append(
                        {
                            "task_id": f"task-{i}",
                            "condition_id": f"{tool}_{ctx}_{backend}",
                            "tool_config": tool,
                            "context_strategy": ctx,
                            "backend": backend,
                            "resolve_rate": 1 if np.random.random() < rate else 0,
                        }
                    )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Significance label helper
# ---------------------------------------------------------------------------

def _sig_label(r: ANOVAResult) -> str:
    if r.p_value < 0.001:
        return "***"
    if r.p_value < 0.01:
        return "**"
    if r.is_significant:
        return "*"
    return "ns"


# ---------------------------------------------------------------------------
# Cohen's d interpretation
# ---------------------------------------------------------------------------

def _interpret_d(d: float) -> str:
    a = abs(d)
    if a >= 0.8:
        return "Large"
    if a >= 0.5:
        return "Medium"
    if a >= 0.2:
        return "Small"
    return "Negligible"


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------

def render_anova() -> None:
    theme = st.session_state.get("theme", "dark")

    st.subheader("ANOVA — Three-way Factorial Analysis")
    render_pipeline_banner()
    st.caption(
        "Decomposes resolve-rate variance across Tool Config x Context Strategy x Backend. "
        "Bonferroni-corrected significance threshold: p < 0.05/7 ≈ 0.0071."
    )

    # ── Section 1: Data Source ────────────────────────────────────────────────
    data_source = st.radio(
        "Data Source",
        ["Trajectory Data", "Sample Data"],
        horizontal=True,
        key="anova_data_source",
    )

    df: pd.DataFrame
    if data_source == "Trajectory Data":
        with st.spinner("Loading trajectory files…"):
            df = build_anova_dataframe(TRAJECTORIES_DIR)
        if df.empty:
            st.warning(
                "No trajectory files found in `trajectories/`. "
                "Switch to **Sample Data** to explore the analysis with synthetic data."
            )
            return
        st.success(f"Loaded {len(df):,} observations from trajectory files.")
    else:
        df = _generate_sample_data()
        st.info(
            f"Using synthetic sample data: {len(df):,} observations, "
            "27 conditions (3 tools x 3 contexts x 3 backends), 50 obs each."
        )

    with st.expander("Preview DataFrame", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.caption(f"Shape: {df.shape[0]} rows x {df.shape[1]} cols")
        with col_b:
            mean_rr = df["resolve_rate"].mean() if "resolve_rate" in df.columns else float("nan")
            st.caption(f"Mean resolve rate: {mean_rr:.3f}")

    st.divider()

    # ── Section 2: Run ANOVA ──────────────────────────────────────────────────
    run_col, _ = st.columns([2, 6])
    with run_col:
        run_clicked = st.button("Run ANOVA", type="primary", use_container_width=True)

    if run_clicked:
        with st.spinner("Fitting three-way ANOVA (statsmodels OLS)…"):
            try:
                results = compute_three_way_anova(df)
                st.session_state["anova_results"] = results
                st.session_state["anova_df"] = df.copy()
                st.success("ANOVA complete.")
            except ImportError as exc:
                st.error(f"Missing dependency: {exc}")
                return
            except Exception as exc:
                st.error(f"ANOVA failed: {exc}")
                return

    anova_results: list[ANOVAResult] | None = st.session_state.get("anova_results")
    anova_df: pd.DataFrame = st.session_state.get("anova_df", df)

    if not anova_results:
        st.info("Press **Run ANOVA** to start the analysis.")
        return

    st.divider()

    # ── Section 3: ANOVA Table ────────────────────────────────────────────────
    st.markdown("#### ANOVA Table")

    table_rows = []
    for r in anova_results:
        table_rows.append(
            {
                "Source": r.source,
                "SS": round(r.sum_sq, 4),
                "df": r.df,
                "MS": round(r.mean_sq, 4),
                "F": round(r.f_statistic, 3) if r.f_statistic else "",
                "p-value": f"{r.p_value:.4f}" if r.p_value < 1.0 else "—",
                "eta²": round(r.eta_squared, 4),
                "Sig": _sig_label(r),
            }
        )
    anova_table_df = pd.DataFrame(table_rows)
    st.dataframe(anova_table_df, use_container_width=True, hide_index=True)

    st.caption("Sig: *** p<0.001 | ** p<0.01 | * Bonferroni-corrected significant | ns not significant")

    st.divider()

    # ── Section 4: Charts ─────────────────────────────────────────────────────
    st.markdown("#### Variance & Effect Size Charts")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(
            plotly_variance_pie(anova_results, theme),
            use_container_width=True,
            key="anova_pie",
        )
    with chart_col2:
        st.plotly_chart(
            plotly_effect_size_bar(anova_results, theme),
            use_container_width=True,
            key="anova_bar",
        )

    st.divider()

    # ── Section 5: Hypothesis Evaluation ─────────────────────────────────────
    st.markdown("#### Hypothesis Evaluation")

    # Look up tool / context / backend results by source name
    def _find(source_name: str) -> ANOVAResult | None:
        for r in anova_results:
            if r.source == source_name:
                return r
        return None

    tool_r = _find("Tool")
    context_r = _find("Context")
    backend_r = _find("Backend")

    # H1: Tool has largest effect
    if tool_r and context_r:
        h1_supported = tool_r.eta_squared > context_r.eta_squared
        h1_detail = (
            f"Tool eta²={tool_r.eta_squared:.4f} "
            f"{'>' if h1_supported else '<='} "
            f"Context eta²={context_r.eta_squared:.4f}"
        )
    else:
        h1_supported = False
        h1_detail = "Could not find Tool or Context in ANOVA results."

    # H2: Context medium effect — Cohen's d(full vs summary) in [0.3, 0.8]
    if "context_strategy" in anova_df.columns:
        full_ctx = anova_df.loc[anova_df["context_strategy"] == "full", "resolve_rate"].values
        summary_ctx = anova_df.loc[anova_df["context_strategy"] == "summary", "resolve_rate"].values
        h2_d = compute_cohens_d(full_ctx, summary_ctx)
        h2_abs = abs(h2_d)
        h2_supported = 0.3 <= h2_abs <= 0.8
        h2_detail = f"Cohen's d (full vs summary context) = {h2_d:.3f} (abs={h2_abs:.3f})"
    else:
        h2_supported = False
        h2_detail = "context_strategy column not found."
        h2_d = 0.0

    # H3: Harness (tool + context) >= 10% variance
    harness_eta = 0.0
    if tool_r:
        harness_eta += tool_r.eta_squared
    if context_r:
        harness_eta += context_r.eta_squared
    h3_supported = harness_eta * 100 >= 10.0
    h3_detail = f"Tool eta² + Context eta² = {harness_eta*100:.1f}% (threshold: 10%)"

    # H4: Any interaction is significant
    interaction_sources = [r for r in anova_results if "x" in r.source.lower()]
    h4_supported = any(r.is_significant for r in interaction_sources)
    if interaction_sources:
        sig_ixns = [r.source for r in interaction_sources if r.is_significant]
        h4_detail = (
            f"Significant interactions: {', '.join(sig_ixns) if sig_ixns else 'none'}"
        )
    else:
        h4_detail = "No interaction terms found in ANOVA results."

    hypotheses = [
        {
            "id": "H1",
            "label": "Tool config has the largest main effect",
            "supported": h1_supported,
            "detail": h1_detail,
        },
        {
            "id": "H2",
            "label": "Context strategy has a medium effect (Cohen's d 0.3–0.8, full vs summary)",
            "supported": h2_supported,
            "detail": h2_detail,
        },
        {
            "id": "H3",
            "label": "Harness factors (tool + context) explain ≥ 10% of total variance",
            "supported": h3_supported,
            "detail": h3_detail,
        },
        {
            "id": "H4",
            "label": "At least one interaction term is statistically significant",
            "supported": h4_supported,
            "detail": h4_detail,
        },
    ]

    hyp_cols = st.columns(len(hypotheses))
    for col, hyp in zip(hyp_cols, hypotheses):
        with col:
            badge_class = "hyp-supported" if hyp["supported"] else "hyp-not-supported"
            badge_text = "Supported" if hyp["supported"] else "Not supported"
            st.markdown(
                f"<div style='margin-bottom:8px;'>"
                f"<strong>{hyp['id']}</strong><br>"
                f"<span style='font-size:13px;'>{hyp['label']}</span><br>"
                f"<span class='{badge_class}'>{badge_text}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.caption(hyp["detail"])

    st.divider()

    # ── Section 6: Pairwise Comparisons ──────────────────────────────────────
    st.markdown("#### Pairwise Comparisons (Cohen's d)")

    factors = {
        "tool_config": "Tool Config",
        "context_strategy": "Context Strategy",
        "backend": "Backend",
    }

    all_pairwise_rows: list[dict] = []

    for factor_col, factor_label in factors.items():
        if factor_col not in anova_df.columns:
            continue
        groups = anova_df[factor_col].unique().tolist()
        for g1, g2 in combinations(sorted(groups), 2):
            arr1 = anova_df.loc[anova_df[factor_col] == g1, "resolve_rate"].values
            arr2 = anova_df.loc[anova_df[factor_col] == g2, "resolve_rate"].values
            d = compute_cohens_d(arr1, arr2)
            all_pairwise_rows.append(
                {
                    "Factor": factor_label,
                    "Group A": g1,
                    "Group B": g2,
                    "Cohen's d": round(d, 4),
                    "Interpretation": _interpret_d(d),
                    "comparison": f"{factor_label}: {g1} vs {g2}",
                    "cohens_d": d,
                    "interpretation": _interpret_d(d),
                }
            )

    if all_pairwise_rows:
        display_cols = ["Factor", "Group A", "Group B", "Cohen's d", "Interpretation"]
        st.dataframe(
            pd.DataFrame(all_pairwise_rows)[display_cols],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No pairwise comparisons could be computed (check factor columns in DataFrame).")

    st.divider()

    # ── Section 7: GLMM Robustness Check ─────────────────────────────────────
    st.markdown("#### GLMM Robustness Check")

    run_glmm = st.toggle(
        "Run GLMM Robustness Check",
        key="anova_glmm_toggle",
        help="Fits a Generalized Linear Mixed Model with task_id as random intercept.",
    )

    if run_glmm:
        if "task_id" not in anova_df.columns:
            st.error("GLMM requires a `task_id` column in the DataFrame.")
        else:
            with st.spinner("Fitting GLMM (mixed effects model)… this may take 30–60 s."):
                try:
                    from harness_eval.pipeline.analysis import compute_glmm

                    glmm_result = compute_glmm(anova_df)

                    # Model summary
                    status_text = "Converged" if glmm_result.converged else "Did not converge"
                    status_color = "#22c55e" if glmm_result.converged else "#ef4444"
                    st.markdown(
                        f"<span style='color:{status_color};font-weight:bold;'>"
                        f"Status: {status_text}</span>",
                        unsafe_allow_html=True,
                    )

                    glmm_meta_cols = st.columns(4)
                    with glmm_meta_cols[0]:
                        st.metric("Log-Likelihood", f"{glmm_result.log_likelihood:.3f}")
                    with glmm_meta_cols[1]:
                        st.metric("AIC", f"{glmm_result.aic:.3f}")
                    with glmm_meta_cols[2]:
                        st.metric("Random Effect Var.", f"{glmm_result.random_effect_variance:.4f}")
                    with glmm_meta_cols[3]:
                        st.metric("Observations", glmm_result.n_observations)

                    # Fixed effects table
                    st.markdown("**Fixed Effects**")
                    fe_rows = []
                    for name, fe in glmm_result.fixed_effects.items():
                        fe_rows.append(
                            {
                                "Effect": fe.name,
                                "Coefficient": round(fe.coefficient, 4),
                                "Std Error": round(fe.std_error, 4),
                                "z": round(fe.z_value, 3),
                                "p-value": f"{fe.p_value:.4f}",
                                "Sig": "***" if fe.p_value < 0.001 else ("**" if fe.p_value < 0.01 else ("*" if fe.is_significant else "ns")),
                            }
                        )
                    st.dataframe(pd.DataFrame(fe_rows), use_container_width=True, hide_index=True)

                    if not glmm_result.converged:
                        st.warning(
                            "GLMM did not fully converge. Results may be unreliable. "
                            "Consider increasing sample size or simplifying the model."
                        )

                except ImportError as exc:
                    st.error(f"Missing dependency: {exc}")
                except ValueError as exc:
                    st.error(f"GLMM error: {exc}")
                except Exception as exc:
                    st.error(f"GLMM failed: {exc}")

    st.divider()

    # ── Section 8: Export ─────────────────────────────────────────────────────
    st.markdown("#### Export")

    export_col1, export_col2 = st.columns(2)

    # CSV download
    with export_col1:
        csv_bytes = anova_table_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download ANOVA Table (CSV)",
            data=csv_bytes,
            file_name="anova_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Paper figures
    with export_col2:
        if st.button("Generate Paper Figures", use_container_width=True):
            with st.spinner("Rendering publication-quality figures…"):
                try:
                    # Variance pie
                    pie_fig = mpl_variance_pie(anova_results)
                    pie_buf = io.BytesIO()
                    pie_fig.savefig(pie_buf, format="png", dpi=300, bbox_inches="tight")
                    pie_buf.seek(0)

                    # Effect forest
                    forest_fig = mpl_effect_forest(all_pairwise_rows)
                    forest_buf = io.BytesIO()
                    forest_fig.savefig(forest_buf, format="png", dpi=300, bbox_inches="tight")
                    forest_buf.seek(0)

                    fig_col1, fig_col2 = st.columns(2)
                    with fig_col1:
                        st.download_button(
                            label="Download Variance Pie (PNG)",
                            data=pie_buf,
                            file_name="fig_variance_pie.png",
                            mime="image/png",
                            use_container_width=True,
                        )
                    with fig_col2:
                        st.download_button(
                            label="Download Effect Forest (PNG)",
                            data=forest_buf,
                            file_name="fig_effect_forest.png",
                            mime="image/png",
                            use_container_width=True,
                        )
                    st.success("Figures ready for download.")
                except Exception as exc:
                    st.error(f"Figure generation failed: {exc}")

    st.markdown("---")
    st.caption("Pipeline complete! Review results above, export paper figures, or return to **Config Builder** to run more conditions.")
