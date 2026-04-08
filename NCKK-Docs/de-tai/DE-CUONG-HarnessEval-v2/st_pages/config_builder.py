"""Config Builder tab — Tab 1 of HarnessEval Dashboard.

Provides:
  1. 3-factor radio selectors (Tool Level, Context Strategy, Backend)
  2. Active condition summary with badge/chip rendering
  3. YAML config generation + download
  4. Run panel (dry-run, max_tasks, sweagent_dir, run/stop, progress, live log)
  5. 27-condition table with data status
"""

from __future__ import annotations

import time
from pathlib import Path

import streamlit as st
import yaml

from harness_eval.configs.backend_config import BackendConfig, BackendType
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.experiment import CRITICAL_CONDITIONS, ExperimentConfig
from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.harness.factory import create_harness_config
from st_utils.data_loader import scan_trajectories
from st_utils.run_manager import RunManager

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

# Tool radio: value -> display label
TOOL_OPTIONS: dict[str, str] = {
    "full": "Full (12 tools)",
    "medium": "Medium (8 tools)",
    "minimal": "Minimal (5 tools)",
}

# Context radio: value -> display label
CONTEXT_OPTIONS: dict[str, str] = {
    "full": "Full History (no truncation)",
    "sliding_window": "Sliding Window (50K tokens)",
    "summary": "Summary / ACC (2K tokens)",
}

# Backend radio: value -> display label (cost filled at render time)
BACKEND_LABEL_FMT: dict[str, str] = {
    "claude": "Claude Sonnet 4 (${cost}/eval)",
    "gpt": "GPT-4o (${cost}/eval)",
    "deepseek": "DeepSeek-V3 (${cost}/eval)",
}

# Full tool list for chip comparison
FULL_TOOLS = ToolConfig(ToolLevel.FULL).tools

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _backend_label(backend_val: str) -> str:
    """Return formatted backend radio label including cost."""
    cfg = BackendConfig(BackendType(backend_val))
    cost = cfg.cost_per_eval
    fmt = BACKEND_LABEL_FMT[backend_val]
    return fmt.replace("${cost}", f"{cost:.2f}")


def _build_yaml(tool: str, context: str, backend: str) -> str:
    """Generate YAML config dict for the selected condition."""
    tool_cfg = ToolConfig(ToolLevel(tool))
    ctx_cfg = ContextConfig(ContextStrategy(context))
    be_cfg = BackendConfig(BackendType(backend))

    data = {
        "condition_id": f"{tool}_{context}_{backend}",
        "tool": {
            "level": tool,
            "tools": tool_cfg.tools,
            "tool_count": tool_cfg.tool_count,
        },
        "context": {
            "strategy": context,
            "window_size_tokens": ctx_cfg.window_size_tokens,
            "summary_max_tokens": ctx_cfg.summary_max_tokens,
        },
        "backend": {
            "type": backend,
            "model_id": be_cfg.model_id,
            "provider": be_cfg.provider,
            "cost_per_eval_usd": be_cfg.cost_per_eval,
            "temperature": be_cfg.temperature,
        },
    }
    return yaml.dump(data, sort_keys=False, allow_unicode=True)


def _scan_data_counts() -> dict[str, int]:
    """Return mapping of condition_id -> file count in TRAJECTORIES_DIR."""
    counts: dict[str, int] = {}
    if not TRAJECTORIES_DIR.exists():
        return counts
    try:
        rows = scan_trajectories(TRAJECTORIES_DIR)
        for row in rows:
            cid = row["condition_id"]
            counts[cid] = counts.get(cid, 0) + 1
    except Exception:  # noqa: BLE001
        pass
    return counts


def _get_run_manager() -> RunManager:
    # Re-create if old instance lacks new methods (e.g., after code update)
    if "run_manager" not in st.session_state or not hasattr(st.session_state.run_manager, "_run_thread_ollama"):
        st.session_state.run_manager = RunManager()
    return st.session_state.run_manager


def _log_line_html(line: str) -> str:
    """Wrap a log line in the appropriate CSS class based on content."""
    import html
    safe = html.escape(line)
    upper = line.upper()
    if "PASS" in upper or "DONE" in upper:
        css = "log-line-pass"
    elif "FAIL" in upper or "ERROR" in upper:
        css = "log-line-fail"
    elif "CONDITION:" in upper or "INFO" in upper or upper.startswith("["):
        css = "log-line-info"
    else:
        css = "log-line"
    return f'<span class="{css}">{safe}</span>'


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _render_selectors() -> tuple[str, str, str]:
    """Render 3-column radio selectors. Returns (tool, context, backend) values."""
    col_tool, col_ctx, col_be = st.columns(3)

    with col_tool:
        st.markdown("**Tool Level**")
        tool_val = st.radio(
            "tool_level",
            options=list(TOOL_OPTIONS.keys()),
            format_func=lambda v: TOOL_OPTIONS[v],
            key="cb_tool",
            label_visibility="collapsed",
        )

    with col_ctx:
        st.markdown("**Context Strategy**")
        ctx_val = st.radio(
            "context_strategy",
            options=list(CONTEXT_OPTIONS.keys()),
            format_func=lambda v: CONTEXT_OPTIONS[v],
            key="cb_context",
            label_visibility="collapsed",
        )

    with col_be:
        st.markdown("**Backend**")
        be_val = st.radio(
            "backend",
            options=list(BACKEND_LABEL_FMT.keys()),
            format_func=_backend_label,
            key="cb_backend",
            label_visibility="collapsed",
        )

    return tool_val, ctx_val, be_val  # type: ignore[return-value]


def _render_condition_summary(tool: str, context: str, backend: str) -> None:
    """Render the active condition summary card."""
    condition_id = f"{tool}_{context}_{backend}"
    is_critical = (tool, context, backend) in CRITICAL_CONDITIONS

    exp = ExperimentConfig()
    from harness_eval.configs.experiment import Condition

    cond_obj = Condition(
        tool=ToolConfig(ToolLevel(tool)),
        context=ContextConfig(ContextStrategy(context)),
        backend=BackendConfig(BackendType(backend)),
    )
    runs = exp.runs_for_condition(cond_obj)
    num_tasks = exp.num_tasks
    be_cfg = BackendConfig(BackendType(backend))
    model_id = be_cfg.model_id
    cost_per_eval = be_cfg.cost_per_eval
    est_cost = runs * num_tasks * cost_per_eval

    badge_class = "badge-crit" if is_critical else "badge-norm"
    badge_label = "CRITICAL" if is_critical else "standard"

    # Tool chips
    current_tools = ToolConfig(ToolLevel(tool)).tools
    chips_html = ""
    for t in FULL_TOOLS:
        if t in current_tools:
            chips_html += f'<span class="chip-on">{t}</span>'
        else:
            chips_html += f'<span class="chip-off">{t}</span>'

    html = f"""
<div style="background:#1e2130;border-left:3px solid #4c8dff;border-radius:8px;padding:14px;margin-bottom:12px;">
  <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
    <span style="font-size:15px;font-weight:bold;font-family:monospace;">{condition_id}</span>
    <span class="{badge_class}">{badge_label}</span>
    <span style="color:#9ca0ad;font-size:13px;">runs: <b style="color:#e4e6ed;">{runs}</b></span>
    <span style="color:#9ca0ad;font-size:13px;">tasks: <b style="color:#e4e6ed;">{num_tasks}</b></span>
    <span style="color:#9ca0ad;font-size:13px;">est. cost: <b style="color:#e4e6ed;">${est_cost:,.0f}</b></span>
    <span style="color:#9ca0ad;font-size:13px;">model: <b style="color:#e4e6ed;">{model_id}</b></span>
  </div>
  <div style="margin-top:8px;">
    {chips_html}
  </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def _render_yaml_section(tool: str, context: str, backend: str) -> None:
    """Render YAML config display and download button."""
    yaml_text = _build_yaml(tool, context, backend)
    condition_id = f"{tool}_{context}_{backend}"

    with st.expander("YAML Config", expanded=False):
        st.code(yaml_text, language="yaml")
        st.download_button(
            label="Download config.yaml",
            data=yaml_text.encode("utf-8"),
            file_name=f"{condition_id}_config.yaml",
            mime="text/yaml",
            key="cb_yaml_download",
        )


def _render_run_panel(tool: str, context: str, backend: str) -> None:
    """Render the run control panel."""
    st.markdown("---")
    st.markdown("#### Run Panel")

    run_mgr = _get_run_manager()
    status = run_mgr.get_status()
    is_running = status["status"] == "running"

    # Controls (disabled while running)
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        run_mode = st.selectbox(
            "Run Mode",
            ["ollama", "dry-run", "real"],
            index=0,
            key="cb_run_mode",
            disabled=is_running,
            help="ollama = local LLM (free), dry-run = synthetic data, real = SWE-Agent + API",
        )
    with col_b:
        max_tasks = st.number_input(
            "Max tasks per condition",
            min_value=1,
            max_value=150,
            value=5,
            step=1,
            key="cb_max_tasks",
            disabled=is_running,
        )
    with col_c:
        parallel = st.toggle("Parallel Mode", value=False, key="cb_parallel", disabled=is_running,
                             help="Run conditions concurrently (faster for 27-condition runs)")
        if parallel:
            max_workers = st.number_input("Workers", min_value=2, max_value=16, value=4, key="cb_workers", disabled=is_running)
        else:
            max_workers = 1

    # Mode-specific settings
    ollama_model: str | None = None
    sweagent_dir: str | None = None

    if run_mode == "ollama":
        from st_utils.ollama_runner import list_models, check_ollama
        if check_ollama():
            models = list_models()
            model_names = [m["name"] for m in models]
            if model_names:
                ollama_model = st.selectbox(
                    "Ollama Model",
                    model_names,
                    key="cb_ollama_model",
                    disabled=is_running,
                    help="Local LLM model running on Ollama",
                )
            else:
                st.warning("Ollama is running but no models found. Run: `ollama pull qwen2.5:7b`")
        else:
            st.error("Ollama is not running. Start it with: `ollama serve`")

    elif run_mode == "real":
        sweagent_dir = st.text_input(
            "SWE-Agent directory",
            value="./SWE-agent",
            key="cb_sweagent_dir",
            disabled=is_running,
            help="Path to SWE-Agent installation.",
        )

    condition_id = f"{tool}_{context}_{backend}"

    # Run / Stop buttons
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])
    with btn_col1:
        run_clicked = st.button(
            "Run",
            key="cb_run_btn",
            disabled=is_running,
            type="primary",
        )
    with btn_col2:
        stop_clicked = st.button(
            "Stop",
            key="cb_stop_btn",
            disabled=not is_running,
        )

    if run_clicked and not is_running:
        try:
            run_mgr.start(
                conditions=[condition_id],
                mode=run_mode,
                max_tasks=int(max_tasks),
                output_dir=TRAJECTORIES_DIR,
                sweagent_dir=Path(sweagent_dir) if sweagent_dir else None,
                parallel=parallel,
                max_workers=int(max_workers) if parallel else 4,
                ollama_model=ollama_model if run_mode == "ollama" else None,
            )
            st.rerun()
        except RuntimeError as exc:
            st.error(str(exc))

    if stop_clicked:
        run_mgr.stop()
        st.rerun()

    # Progress + live log
    status = run_mgr.get_status()
    cur_status = status["status"]
    progress_tuple: tuple[int, int] = status["progress"]
    logs: list[str] = status["logs"]

    completed, total = progress_tuple
    if total > 0:
        frac = completed / total
    else:
        frac = 0.0

    if cur_status == "running":
        st.progress(frac, text=f"Running: {completed}/{total} — {status['current_condition']}")
    elif cur_status == "done":
        st.progress(1.0, text="Done")
        st.success("Run completed.")
    elif cur_status == "stopped":
        st.progress(frac, text=f"Stopped at {completed}/{total}")
        st.warning("Run was stopped.")
    elif cur_status == "failed":
        st.progress(frac, text=f"Failed at {completed}/{total}")
        st.error("Run failed — see logs.")
    elif cur_status == "idle" and total == 0:
        st.progress(0.0, text="Idle")

    if logs:
        lines_html = "<br>".join(_log_line_html(ln) for ln in logs[-80:])
        st.markdown(
            f'<div style="background:#0d1117;border-radius:6px;padding:10px;'
            f'max-height:220px;overflow-y:auto;font-family:monospace;">'
            f"{lines_html}</div>",
            unsafe_allow_html=True,
        )

    if cur_status == "running":
        time.sleep(1)
        st.rerun()


def _render_conditions_table(tool: str, context: str, backend: str) -> None:
    """Render the 27-condition table with sorting by match score and multi-select."""
    import pandas as pd

    st.markdown("---")
    st.markdown("#### All 27 Conditions")

    data_counts = _scan_data_counts()
    exp = ExperimentConfig()
    all_conditions = exp.generate_conditions()

    active_cid = f"{tool}_{context}_{backend}"

    # Get per-condition run status from RunManager
    run_mgr = _get_run_manager()
    run_st = run_mgr.get_status()
    cond_status_map = run_st.get("condition_status", {})

    rows = []
    for cond in all_conditions:
        cid = cond.condition_id
        tool_val = cond.tool.level.value
        ctx_val = cond.context.strategy.value
        be_val = cond.backend.backend.value
        is_crit = (tool_val, ctx_val, be_val) in CRITICAL_CONDITIONS
        runs = exp.runs_for_condition(cond)
        est_cost = runs * exp.num_tasks * cond.estimated_cost_per_task
        data_n = data_counts.get(cid, 0)

        # Determine how many of the 3 factors match the current selection
        matches_tool = tool_val == tool
        matches_ctx = ctx_val == context
        matches_be = be_val == backend
        match_score = int(matches_tool) + int(matches_ctx) + int(matches_be)
        is_active = cid == active_cid

        # Pipeline status for this condition
        cs = cond_status_map.get(cid)
        if cs:
            pipe_status = cs["status"].capitalize()
            if cs["status"] == "done":
                pipe_status = f"Done ({cs['resolved']}/{cs['total']})"
            elif cs["status"] == "running":
                pipe_status = f"Running ({cs['completed']}/{cs['total']})"
        elif data_n > 0:
            pipe_status = f"Data ({data_n})"
        else:
            pipe_status = "—"

        rows.append(
            {
                "Select": is_active,
                "Condition": cid,
                "Tool": tool_val,
                "Context": ctx_val,
                "Backend": be_val,
                "Critical": "Yes" if is_crit else "",
                "Pipeline": pipe_status,
                "Data": data_n,
                "_match_score": match_score,
                "_is_active": is_active,
            }
        )

    df = pd.DataFrame(rows)

    # Sort: active row first, then by match score descending, then by condition id
    df = df.sort_values(
        ["_is_active", "_match_score", "Condition"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    # Drop hidden helper columns before handing to data_editor
    display_df = df.drop(columns=["_match_score", "_is_active"])

    edited_df = st.data_editor(
        display_df,
        use_container_width=True,
        hide_index=True,
        disabled=["Condition", "Tool", "Context", "Backend", "Critical", "Pipeline", "Data"],
        column_config={
            "Select": st.column_config.CheckboxColumn("", default=False, width="small"),
            "Condition": st.column_config.TextColumn("Condition", width="medium"),
            "Tool": st.column_config.TextColumn("Tool", width="small"),
            "Context": st.column_config.TextColumn("Context", width="small"),
            "Backend": st.column_config.TextColumn("Backend", width="small"),
            "Critical": st.column_config.TextColumn("Crit", width="small"),
            "Pipeline": st.column_config.TextColumn("Pipeline", width="medium"),
            "Data": st.column_config.NumberColumn("Files", width="small"),
        },
        key="conditions_editor",
    )

    # Persist selected conditions; fall back to active condition if nothing ticked
    selected = edited_df[edited_df["Select"] == True]["Condition"].tolist()  # noqa: E712
    st.session_state.selected_conditions = selected if selected else [active_cid]

    n_selected = len(st.session_state.selected_conditions)

    # Auto-refresh table while running
    if run_st["status"] == "running":
        import time
        time.sleep(1)
        st.rerun()

    st.caption(f"{n_selected} condition(s) selected  |  active: `{active_cid}`")

    # Action buttons
    run_mgr = _get_run_manager()
    status = run_mgr.get_status()
    is_busy = status["status"] == "running"

    btn_col_active, btn_col_sel, btn_col_all, btn_col_spacer = st.columns([2, 2, 2, 2])

    # "Run Active" — quick single condition run
    with btn_col_active:
        run_active = st.button(
            f"Run Active",
            disabled=is_busy,
            key="run_active_btn",
            help=f"Run only the active condition: {active_cid}",
        )

    # "Run Selected" button
    with btn_col_sel:
        run_selected = st.button(
            f"Run {n_selected} Selected",
            type="primary",
            disabled=is_busy or n_selected == 0,
            key="run_selected_btn",
        )

    # "Run All 27" button
    with btn_col_all:
        run_all = st.button(
            "Run All 27",
            disabled=is_busy,
            key="run_all_btn",
            help="Auto-run all 27 conditions in parallel (4 workers)",
        )

    def _start_run(condition_list: list[str]) -> None:
        mode = st.session_state.get("cb_run_mode", "ollama")
        max_tasks = int(st.session_state.get("cb_max_tasks", 5))
        sweagent_dir_str = st.session_state.get("cb_sweagent_dir")
        is_parallel = st.session_state.get("cb_parallel", False)
        n_workers = int(st.session_state.get("cb_workers", 4))
        selected_ollama_model = st.session_state.get("cb_ollama_model", "qwen2.5:7b")

        # Validate real mode requirements
        if mode == "real" and not sweagent_dir_str:
            st.error("**Real mode requires SWE-Agent directory.**")
            return

        if mode == "ollama":
            from st_utils.ollama_runner import check_ollama
            if not check_ollama():
                st.error("**Ollama is not running.** Start with: `ollama serve`")
                return

        # Auto-enable parallel for large dry-run/real runs
        if mode != "ollama" and len(condition_list) >= 10 and not is_parallel:
            is_parallel = True
            n_workers = 4 if mode == "dry-run" else 3

        try:
            run_mgr.start(
                conditions=condition_list,
                mode=mode,
                max_tasks=max_tasks,
                output_dir=TRAJECTORIES_DIR,
                sweagent_dir=Path(sweagent_dir_str) if sweagent_dir_str else None,
                parallel=is_parallel,
                max_workers=n_workers,
                ollama_model=selected_ollama_model if mode == "ollama" else None,
            )
            st.rerun()
        except RuntimeError as exc:
            st.error(str(exc))

    if run_active:
        _start_run([active_cid])

    if run_selected:
        _start_run(st.session_state.selected_conditions)

    if run_all:
        all_27 = [
            f"{t}_{c}_{b}"
            for t in ["full", "medium", "minimal"]
            for c in ["full", "sliding_window", "summary"]
            for b in ["claude", "gpt", "deepseek"]
        ]
        st.session_state.selected_conditions = all_27
        _start_run(all_27)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def render_config_builder() -> None:
    """Render the Config Builder tab (Tab 1)."""
    st.markdown("### Config Builder")
    st.caption("Select a condition, generate its YAML config, and launch a run.")

    # 1. Factor selectors
    tool, context, backend = _render_selectors()

    st.markdown("---")

    # 2. Active condition summary
    _render_condition_summary(tool, context, backend)

    # 3. YAML config + download
    _render_yaml_section(tool, context, backend)

    # Store active condition in session state for cross-tab access
    st.session_state.active_condition = f"{tool}_{context}_{backend}"
    st.session_state.active_config = _build_yaml(tool, context, backend)

    # 4. Run panel
    _render_run_panel(tool, context, backend)

    # 5. 27-condition table (receives current selection for sorting/pre-check)
    _render_conditions_table(tool, context, backend)
