"""Shared UI helpers for the Streamlit dashboard."""

import html

import streamlit as st


STEP_NAMES = [
    "Task Selection", "Config Load", "Run Agent",
    "Collect Logs", "Compute Metrics", "ANOVA",
]


def render_pipeline_banner() -> None:
    """Show pipeline context banner at top of a tab."""
    active = st.session_state.get("active_condition", "---")
    step = st.session_state.get("pipeline_step", 0)
    step_label = STEP_NAMES[min(step, 5)] if step < 6 else "Complete"
    n_conds = len(st.session_state.get("selected_conditions", []))

    rm = st.session_state.get("run_manager")
    run_status = rm.get_status()["status"] if rm else "idle"

    parts = [f"Condition: `{html.escape(active)}`", f"Step {step+1}/6: {step_label}"]
    if n_conds > 1:
        parts.append(f"{n_conds} conditions selected")
    if run_status == "running":
        parts.append("Running...")

    st.caption(" | ".join(parts))


def escape_html(text: str) -> str:
    """Escape HTML special characters for safe rendering."""
    return html.escape(str(text))
