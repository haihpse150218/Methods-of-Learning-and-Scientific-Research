import streamlit as st

st.set_page_config(
    page_title="HarnessEval Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme state ──────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── CSS definitions ──────────────────────────────────────────────────────────
DARK_CSS = """
<style>
.metric-card {
    background: #1e2130;
    border-left: 3px solid #4c8dff;
    border-radius: 8px;
    padding: 12px;
}
.metric-label {
    color: #9ca0ad;
    font-size: 13px;
}
.metric-value {
    color: #e4e6ed;
    font-size: 20px;
    font-weight: bold;
}
.badge-crit {
    background: #22c55e;
    color: #000;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-norm {
    background: #636879;
    color: #e4e6ed;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-pass {
    background: #22c55e22;
    color: #22c55e;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-fail {
    background: #ef444422;
    color: #ef4444;
    padding: 2px 8px;
    border-radius: 10px;
}
.chip-on {
    background: #22c55e22;
    color: #22c55e;
    display: inline-block;
    margin: 2px;
    padding: 2px 8px;
    border-radius: 10px;
}
.chip-off {
    background: #1e2130;
    color: #636879;
    display: inline-block;
    margin: 2px;
    padding: 2px 8px;
    border-radius: 10px;
    text-decoration: line-through;
}
.turn-card {
    background: #1e2130;
    border-radius: 8px;
    padding: 12px;
}
.log-line {
    font-family: monospace;
    font-size: 12px;
    color: #9ca0ad;
}
.log-line-pass {
    font-family: monospace;
    font-size: 12px;
    color: #22c55e;
}
.log-line-fail {
    font-family: monospace;
    font-size: 12px;
    color: #ef4444;
}
.log-line-info {
    font-family: monospace;
    font-size: 12px;
    color: #4c8dff;
}
.hyp-supported {
    background: #22c55e22;
    color: #22c55e;
    padding: 2px 8px;
    border-radius: 4px;
}
.hyp-not-supported {
    background: #ef444422;
    color: #ef4444;
    padding: 2px 8px;
    border-radius: 4px;
}
</style>
"""

LIGHT_CSS = """
<style>
.metric-card {
    background: #f8f9fa;
    border-left: 3px solid #2563eb;
    border-radius: 8px;
    padding: 12px;
}
.metric-label {
    color: #6b7280;
    font-size: 13px;
}
.metric-value {
    color: #1a1d29;
    font-size: 20px;
    font-weight: bold;
}
.badge-crit {
    background: #16a34a;
    color: #fff;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-norm {
    background: #d1d5db;
    color: #1a1d29;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-pass {
    background: #dcfce7;
    color: #16a34a;
    padding: 2px 8px;
    border-radius: 10px;
}
.badge-fail {
    background: #fee2e2;
    color: #dc2626;
    padding: 2px 8px;
    border-radius: 10px;
}
.chip-on {
    background: #dcfce7;
    color: #16a34a;
    display: inline-block;
    margin: 2px;
    padding: 2px 8px;
    border-radius: 10px;
}
.chip-off {
    background: #f8f9fa;
    color: #9ca3af;
    display: inline-block;
    margin: 2px;
    padding: 2px 8px;
    border-radius: 10px;
    text-decoration: line-through;
}
.turn-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 12px;
}
.log-line {
    font-family: monospace;
    font-size: 12px;
    color: #6b7280;
}
.log-line-pass {
    font-family: monospace;
    font-size: 12px;
    color: #16a34a;
}
.log-line-fail {
    font-family: monospace;
    font-size: 12px;
    color: #dc2626;
}
.log-line-info {
    font-family: monospace;
    font-size: 12px;
    color: #2563eb;
}
.hyp-supported {
    background: #dcfce7;
    color: #16a34a;
    padding: 2px 8px;
    border-radius: 4px;
}
.hyp-not-supported {
    background: #fee2e2;
    color: #dc2626;
    padding: 2px 8px;
    border-radius: 4px;
}
</style>
"""

# Inject CSS based on current theme
css = DARK_CSS if st.session_state.theme == "dark" else LIGHT_CSS
st.markdown(css, unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
header_left, header_right = st.columns([10, 1])
with header_left:
    st.markdown("### HarnessEval Dashboard")
    st.caption("v0.1.0 — Modular Harness Evaluation Toolkit")
with header_right:
    icon = "Light" if st.session_state.theme == "dark" else "Dark"
    if st.button(icon, key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Config Builder", "Pipeline", "Log Viewer", "Compare", "ANOVA"]
)

with tab1:
    from st_pages.config_builder import render_config_builder
    render_config_builder()

with tab2:
    from st_pages.pipeline_viewer import render_pipeline_viewer
    render_pipeline_viewer()

with tab3:
    from st_pages.log_viewer import render_log_viewer
    render_log_viewer()

with tab4:
    from st_pages.compare import render_compare
    render_compare()

with tab5:
    from st_pages.anova import render_anova
    render_anova()
