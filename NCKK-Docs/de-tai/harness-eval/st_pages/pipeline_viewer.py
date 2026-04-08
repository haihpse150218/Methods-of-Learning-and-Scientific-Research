"""Run Monitor tab — Tab 2 of HarnessEval Dashboard.

Dedicated run monitoring: live per-condition status table, full scrollable log,
run summary stats. No config selection here — that's in Config Builder.
"""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import streamlit as st

from st_utils.run_manager import RunManager
from st_utils.data_loader import scan_trajectories

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


def _get_run_manager() -> RunManager | None:
    return st.session_state.get("run_manager")


def render_pipeline_viewer():
    st.markdown("### Run Monitor")

    rm = _get_run_manager()
    if rm is None:
        st.info("No run manager initialized. Go to **Config Builder** to start a run.")
        return

    status = rm.get_status()
    run_status = status["status"]
    cur, total = status["progress"]
    cond_status = status.get("condition_status", {})
    logs = status.get("logs", [])

    # ── Status Header ────────────────────────────────────────────────────────
    if run_status == "idle":
        st.info("No active run. Go to **Config Builder** → select conditions → click Run.")
        _render_data_summary()
        return
    elif run_status == "running":
        st.progress(cur / total if total > 0 else 0, text=f"Running: {cur}/{total} tasks")
    elif run_status == "done":
        st.success(f"Run complete! {cur}/{total} tasks finished.")
    elif run_status == "failed":
        st.error("Run failed. See logs below.")
    elif run_status == "stopped":
        st.warning(f"Run stopped at {cur}/{total} tasks.")

    # ── Controls ─────────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 6])
    with ctrl1:
        if st.button("Stop", disabled=run_status != "running", key="monitor_stop"):
            rm.stop()
            st.rerun()
    with ctrl2:
        if st.button("Clear", disabled=run_status == "running", key="monitor_clear"):
            rm.clear()
            st.rerun()

    # ── Per-Condition Status Table ───────────────────────────────────────────
    if cond_status:
        st.markdown("#### Condition Status")

        cond_rows = []
        for cid, cs in cond_status.items():
            resolve_rate = cs["resolved"] / cs["total"] if cs["total"] > 0 and cs["completed"] > 0 else 0
            cond_rows.append({
                "Condition": cid,
                "Status": cs["status"].capitalize().replace("Running", "Running..."),
                "Progress": f"{cs['completed']}/{cs['total']}",
                "Resolved": cs["resolved"],
                "Failed": cs["failed"],
                "Resolve %": f"{resolve_rate:.0%}" if cs["completed"] > 0 else "—",
            })

        # Sort: running first, done second, pending last
        order = {"Running...": 0, "Done": 1, "Pending": 2, "Stopped": 3}
        cond_rows.sort(key=lambda r: (order.get(r["Status"], 9), r["Condition"]))

        df = pd.DataFrame(cond_rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(400, 35 * len(cond_rows) + 38),
            column_config={
                "Condition": st.column_config.TextColumn("Condition", width="large"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Progress": st.column_config.TextColumn("Progress", width="small"),
                "Resolved": st.column_config.NumberColumn("Resolved", width="small"),
                "Failed": st.column_config.NumberColumn("Failed", width="small"),
                "Resolve %": st.column_config.TextColumn("Resolve %", width="small"),
            },
        )

        # Summary stats
        n_done = sum(1 for cs in cond_status.values() if cs["status"] == "done")
        n_running = sum(1 for cs in cond_status.values() if cs["status"] == "running")
        n_pending = sum(1 for cs in cond_status.values() if cs["status"] == "pending")
        total_resolved = sum(cs["resolved"] for cs in cond_status.values())
        total_failed = sum(cs["failed"] for cs in cond_status.values())

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Conditions", f"{n_done} done / {n_running} running / {n_pending} pending")
        m2.metric("Total Tasks", f"{cur}/{total}")
        m3.metric("Resolved", total_resolved)
        m4.metric("Failed", total_failed)

    # ── Full Log ─────────────────────────────────────────────────────────────
    if logs:
        st.markdown("#### Run Log")
        log_text = "\n".join(logs[-200:])
        st.code(log_text, language="text", line_numbers=False)
        if len(logs) > 200:
            st.caption(f"Showing last 200 of {len(logs)} log lines")

    # ── Data Summary (when done) ─────────────────────────────────────────────
    if run_status in ("done", "stopped"):
        _render_data_summary()

    # ── Auto-refresh ─────────────────────────────────────────────────────────
    if run_status == "running":
        time.sleep(1)
        st.rerun()


def _render_data_summary():
    """Show summary of existing trajectory data."""
    st.markdown("#### Trajectory Data")
    entries = scan_trajectories(TRAJECTORIES_DIR)
    if not entries:
        st.caption("No trajectory files in `trajectories/` yet.")
        return

    conditions = set(e["condition_id"] for e in entries)
    resolved = sum(1 for e in entries if e["resolved"])
    st.caption(
        f"{len(entries)} files across {len(conditions)} conditions "
        f"| {resolved}/{len(entries)} resolved ({resolved/len(entries):.0%})"
    )

    # Per-condition summary
    from collections import Counter
    cond_counts = Counter(e["condition_id"] for e in entries)
    cond_resolved = Counter(e["condition_id"] for e in entries if e["resolved"])
    summary_rows = []
    for cid in sorted(conditions):
        n = cond_counts[cid]
        r = cond_resolved.get(cid, 0)
        summary_rows.append({
            "Condition": cid,
            "Files": n,
            "Resolved": r,
            "Failed": n - r,
            "Resolve %": f"{r/n:.0%}" if n > 0 else "—",
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
