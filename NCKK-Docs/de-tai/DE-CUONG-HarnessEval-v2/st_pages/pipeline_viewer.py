"""Pipeline Viewer tab — Tab 2 of HarnessEval Dashboard.

Shows 6-step pipeline flow with state tracking. Receives config from
Config Builder tab via session_state. Controls Run/Load lifecycle.

Phase 7.3: YAML flow from Config → Pipeline
Phase 7.4: Pipeline step tracking with auto-advance
"""

import streamlit as st
from pathlib import Path

from st_utils.run_manager import RunManager
from st_utils.data_loader import scan_trajectories

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

PIPELINE_STEPS = [
    {"title": "Task Selection", "detail": "Select conditions from Config Builder", "icon": "1"},
    {"title": "Config Load", "detail": "Load YAML config + SWE-Agent command", "icon": "2"},
    {"title": "Run Agent", "detail": "Execute pipeline (dry-run or real)", "icon": "3"},
    {"title": "Collect Logs", "detail": "Scan trajectory JSON files", "icon": "4"},
    {"title": "Compute Metrics", "detail": "Calculate 7 metrics (M1.1-M3.2)", "icon": "5"},
    {"title": "ANOVA Analysis", "detail": "Three-way ANOVA on results", "icon": "6"},
]


def _get_step_state(step_index: int) -> str:
    """Determine state of a pipeline step: 'done', 'active', 'running', or 'pending'."""
    pipeline_step = st.session_state.get("pipeline_step", 0)
    rm: RunManager | None = st.session_state.get("run_manager")
    run_status = rm.get_status()["status"] if rm else "idle"

    # Step 3 (index 2) special: running state from run_manager
    if step_index == 2 and run_status == "running":
        return "running"

    if step_index < pipeline_step:
        return "done"
    elif step_index == pipeline_step:
        return "active"
    else:
        return "pending"


def _step_color(state: str) -> str:
    colors = {
        "done": "#22c55e",
        "active": "#4c8dff",
        "running": "#f59e0b",
        "pending": "#636879",
    }
    return colors.get(state, "#636879")


def render_pipeline_viewer():
    st.subheader("Pipeline")

    # -----------------------------------------------------------------------
    # Session state defaults
    # -----------------------------------------------------------------------
    if "pipeline_step" not in st.session_state:
        st.session_state.pipeline_step = 0

    # -----------------------------------------------------------------------
    # Read shared state
    # -----------------------------------------------------------------------
    active_cond: str = st.session_state.get("active_condition", "not set")
    selected_conds: list[str] = st.session_state.get("selected_conditions", [])
    pipeline_step: int = st.session_state.get("pipeline_step", 0)
    rm: RunManager | None = st.session_state.get("run_manager")

    run_status: dict = (
        rm.get_status()
        if rm
        else {"status": "idle", "progress": (0, 0), "logs": [], "current_condition": ""}
    )

    # -----------------------------------------------------------------------
    # Context banner
    # -----------------------------------------------------------------------
    n_conds = len(selected_conds)
    step_label = (
        PIPELINE_STEPS[min(pipeline_step, 5)]["title"]
        if pipeline_step < 6
        else "Complete"
    )
    banner_parts = [
        f"Active: **{active_cond}**",
        (
            f"Step: **{pipeline_step + 1}/6 — {step_label}**"
            if pipeline_step < 6
            else "**Pipeline Complete**"
        ),
        f"Conditions: **{n_conds}**",
    ]
    if run_status["status"] == "running":
        cur, total = run_status["progress"]
        banner_parts.append(f"Progress: **{cur}/{total}**")
    st.markdown(" | ".join(banner_parts))

    st.divider()

    # -----------------------------------------------------------------------
    # Pipeline step indicators (visual bubbles)
    # -----------------------------------------------------------------------
    cols = st.columns(len(PIPELINE_STEPS))
    for i, (col, step) in enumerate(zip(cols, PIPELINE_STEPS)):
        state = _get_step_state(i)
        color = _step_color(state)
        label = state.upper()
        with col:
            st.markdown(
                f'<div style="text-align:center;">'
                f'<div style="width:40px;height:40px;border-radius:50%;background:{color};'
                f'color:white;display:inline-flex;align-items:center;justify-content:center;'
                f'font-weight:bold;font-size:18px;margin-bottom:8px;">{step["icon"]}</div>'
                f'<div style="font-weight:bold;font-size:13px;">{step["title"]}</div>'
                f'<div style="font-size:11px;color:#9ca0ad;">{step["detail"]}</div>'
                f'<div style="font-size:11px;margin-top:4px;color:{color};">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # -----------------------------------------------------------------------
    # Step content panels
    # -----------------------------------------------------------------------

    # --- STEP 1: Task Selection ---
    with st.expander(
        f"Step 1: Task Selection {'[DONE]' if pipeline_step > 0 else ''}",
        expanded=(pipeline_step == 0),
    ):
        if selected_conds:
            st.success(f"{len(selected_conds)} condition(s) selected from Config Builder:")
            for c in selected_conds[:10]:
                st.markdown(f"- `{c}`")
            if len(selected_conds) > 10:
                st.caption(f"... and {len(selected_conds) - 10} more")
            if pipeline_step == 0:
                if st.button("Confirm Selection", key="confirm_selection"):
                    st.session_state.pipeline_step = 1
                    st.rerun()
        else:
            st.info("Go to the **Config Builder** tab and select conditions first.")

    # --- STEP 2: Config Load (Phase 7.3) ---
    with st.expander(
        f"Step 2: Config Load {'[DONE]' if pipeline_step > 1 else ''}",
        expanded=(pipeline_step == 1),
    ):
        active_config_yaml: str = st.session_state.get("active_config", "")
        if active_config_yaml:
            st.markdown("**YAML Config:**")
            st.code(active_config_yaml, language="yaml")

            # Compose SWE-Agent command from active_condition parts
            st.markdown("**SWE-Agent Composed Command:**")
            cmd_lines = ["python -m sweagent run \\", "  --config config/harness_eval/base.yaml \\"]
            parts = active_cond.split("_")
            if len(parts) >= 3:
                tool_val = parts[0]
                ctx_val = "_".join(parts[1:-1])
                be_val = parts[-1]
                cmd_lines.append(f"  --config config/harness_eval/tool_{tool_val}.yaml \\")
                cmd_lines.append(f"  --config config/harness_eval/ctx_{ctx_val}.yaml \\")
                cmd_lines.append(f"  --config config/harness_eval/be_{be_val}.yaml")
            else:
                # Fallback when condition format differs
                cmd_lines.append(f"  # condition: {active_cond}")
            st.code("\n".join(cmd_lines), language="bash")

            if pipeline_step == 1:
                if st.button("Load Config", type="primary", key="load_config_btn"):
                    st.session_state.pipeline_step = 2
                    st.session_state.loaded_config = active_config_yaml
                    st.rerun()
        else:
            st.info("No config available. Go to **Config Builder** to generate one.")
            if pipeline_step == 1:
                st.caption(
                    "Tip: In Config Builder, select a condition and click 'Generate Config YAML'."
                )

    # --- STEP 3: Run Agent ---
    _run_step_label = "[DONE]" if pipeline_step > 2 else (
        "[RUNNING]" if run_status["status"] == "running" else ""
    )
    with st.expander(
        f"Step 3: Run Agent {_run_step_label}",
        expanded=(pipeline_step == 2),
    ):
        if pipeline_step >= 2:
            status_val = run_status["status"]

            if status_val == "idle" and pipeline_step == 2:
                st.info(
                    "Config loaded. Use the **Run Selected** button in the Config Builder tab "
                    "to start execution."
                )
                st.caption("The run panel in Config Builder controls pipeline execution.")

            elif status_val == "running":
                cur, total = run_status["progress"]
                st.progress(cur / total if total > 0 else 0)
                st.info(
                    f"Running: `{run_status['current_condition']}` — "
                    f"Task {cur}/{total}"
                )
                if run_status["logs"]:
                    with st.container():
                        for line in run_status["logs"][-15:]:
                            st.text(line)
                # Auto-refresh while running
                import time
                time.sleep(1)
                st.rerun()

            elif status_val == "done":
                st.success("Run complete!")
                if pipeline_step == 2:
                    st.session_state.pipeline_step = 3
                    st.rerun()

            elif status_val == "failed":
                st.error("Run failed. Check logs in the Config Builder tab.")

            elif status_val == "stopped":
                st.warning("Run was stopped manually.")

        else:
            st.info("Load config first (Step 2).")

    # --- STEP 4: Collect Logs ---
    with st.expander(
        f"Step 4: Collect Logs {'[DONE]' if pipeline_step > 3 else ''}",
        expanded=(pipeline_step == 3),
    ):
        if pipeline_step >= 3:
            entries = scan_trajectories(TRAJECTORIES_DIR)
            if entries:
                relevant = [
                    e for e in entries if e["condition_id"] in set(selected_conds)
                ]
                if relevant:
                    resolved = sum(1 for e in relevant if e["resolved"])
                    pct = resolved / len(relevant)
                    st.success(
                        f"Found **{len(relevant)}** trajectory file(s) for selected conditions. "
                        f"**{resolved}/{len(relevant)}** resolved ({pct:.0%})."
                    )
                    # Show mini-table of first few
                    import pandas as pd
                    preview_df = pd.DataFrame(
                        [
                            {
                                "condition": e["condition_id"],
                                "task": e["task_id"],
                                "resolved": "yes" if e["resolved"] else "no",
                                "turns": e["num_turns"],
                                "cost ($)": f"{e['total_cost']:.4f}",
                            }
                            for e in relevant[:20]
                        ]
                    )
                    st.dataframe(preview_df, use_container_width=True)
                    if len(relevant) > 20:
                        st.caption(f"... and {len(relevant) - 20} more entries")
                else:
                    st.info(
                        f"Found {len(entries)} total file(s), "
                        "but none match the selected conditions."
                    )

                if pipeline_step == 3:
                    if st.button("Continue to Metrics", key="continue_metrics"):
                        st.session_state.pipeline_step = 4
                        st.rerun()
            else:
                st.warning(
                    "No trajectory files found in `trajectories/` directory. "
                    "Ensure the run completed and output was written there."
                )
        else:
            st.info("Run agent first (Step 3).")

    # --- STEP 5: Compute Metrics ---
    with st.expander(
        f"Step 5: Compute Metrics {'[DONE]' if pipeline_step > 4 else ''}",
        expanded=(pipeline_step == 4),
    ):
        if pipeline_step >= 4:
            st.success("Metrics are computed on-the-fly from trajectory files.")
            st.markdown(
                "- Go to **Log Viewer** tab to see per-task metrics (M1.1, M1.2, M1.3, M2.2)\n"
                "- Go to **Compare** tab to compare conditions side-by-side\n"
                "- Metrics span 3 dimensions: Tool Dispatch (D1), Context Utilization (D2), "
                "Backend Efficiency (D3)"
            )
            if pipeline_step == 4:
                if st.button("Continue to ANOVA", key="continue_anova"):
                    st.session_state.pipeline_step = 5
                    st.rerun()
        else:
            st.info("Collect logs first (Step 4).")

    # --- STEP 6: ANOVA Analysis ---
    with st.expander(
        f"Step 6: ANOVA Analysis {'[DONE]' if pipeline_step >= 6 else ''}",
        expanded=(pipeline_step == 5),
    ):
        if pipeline_step >= 5:
            st.success("Ready for ANOVA analysis. Go to the **ANOVA** tab.")
            st.markdown(
                "- Three-way ANOVA table with effect sizes (η²)\n"
                "- Variance decomposition charts\n"
                "- Hypothesis evaluation (H1–H4)\n"
                "- GLMM robustness check\n"
                "- Paper-quality figure export"
            )
        else:
            st.info("Compute metrics first (Step 5).")
