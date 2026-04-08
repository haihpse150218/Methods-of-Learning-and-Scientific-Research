import streamlit as st
from st_utils.run_manager import RunManager

PIPELINE_STEPS = [
    {"title": "Task Selection", "detail": "Load 150 tasks from SWE-Bench Verified", "icon": "1"},
    {"title": "Config Load", "detail": "Compose YAML: base + tool + context + backend", "icon": "2"},
    {"title": "Run Agent", "detail": "Execute SWE-Agent on each task", "icon": "3"},
    {"title": "Collect Logs", "detail": "Parse .traj output to JSON trajectories", "icon": "4"},
    {"title": "Compute Metrics", "detail": "Calculate 7 metrics (M1.1-M3.2)", "icon": "5"},
    {"title": "ANOVA Analysis", "detail": "Three-way ANOVA + Cohen's d + GLMM", "icon": "6"},
]

def render_pipeline_viewer():
    st.subheader("Pipeline Overview")
    condition = st.session_state.get("active_condition", "full_full_claude")
    st.markdown(f"**Active Condition:** `{condition}`")

    # Pipeline steps as 6 columns
    cols = st.columns(len(PIPELINE_STEPS))
    rm = st.session_state.get("run_manager")
    status = rm.get_status() if rm else {"status": "idle", "progress": (0, 0)}

    for i, (col, step) in enumerate(zip(cols, PIPELINE_STEPS)):
        with col:
            # Determine step color based on run status
            if status["status"] == "idle":
                color = "#636879"
                step_status = "pending"
            elif status["status"] == "running":
                if i < 2: color, step_status = "#22c55e", "done"
                elif i == 2: color, step_status = "#4c8dff", "running"
                else: color, step_status = "#636879", "pending"
            elif status["status"] == "done":
                color, step_status = "#22c55e", "done"
            else:
                color, step_status = "#636879", "pending"

            st.markdown(
                f'<div style="text-align:center;">'
                f'<div style="width:40px;height:40px;border-radius:50%;background:{color};'
                f'color:white;display:inline-flex;align-items:center;justify-content:center;'
                f'font-weight:bold;font-size:18px;margin-bottom:8px;">{step["icon"]}</div>'
                f'<div style="font-weight:bold;font-size:14px;">{step["title"]}</div>'
                f'<div style="font-size:12px;color:#9ca0ad;">{step["detail"]}</div>'
                f'<div style="font-size:11px;margin-top:4px;color:{color};">{step_status.upper()}</div>'
                f'</div>', unsafe_allow_html=True)

    st.divider()

    # Run status
    if status["status"] == "running":
        current, total = status["progress"]
        st.progress(current / total if total > 0 else 0)
        st.info(f"Running: {status.get('current_condition', '')} — Task {current}/{total}")
        if status.get("logs"):
            with st.expander("Live Log", expanded=True):
                for line in status["logs"][-15:]:
                    st.text(line)
        import time; time.sleep(1); st.rerun()
    elif status["status"] == "done":
        st.success("Pipeline complete! Check the Log Viewer and ANOVA tabs for results.")
    elif status["status"] == "failed":
        st.error("Pipeline failed. Check logs in the Config Builder tab.")
    else:
        st.info("No active run. Go to Config Builder to start a pipeline run.")

    st.divider()
    st.markdown("""**Pipeline Flow:**
1. **Task Selection** — Load task IDs from SWE-Bench Verified dataset (150 tasks default)
2. **Config Load** — Compose SWE-Agent YAML config from selected factors
3. **Run Agent** — Execute SWE-Agent on each task with composed config
4. **Collect Logs** — Parse `.traj` output files, convert to HarnessEval JSON format
5. **Compute Metrics** — Calculate 7 metrics across 3 dimensions
6. **ANOVA Analysis** — Three-way ANOVA decomposing variance: Tool x Context x Backend""")
