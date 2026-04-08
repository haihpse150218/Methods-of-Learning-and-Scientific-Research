"""HarnessEval Flask App — Interactive Config, Pipeline, Log Viewer, Compare, ANOVA, Run."""

import json
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load .env
load_dotenv(Path(__file__).parent / ".env")

# Add parent to path so we can import harness_eval
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness_eval.configs.tool_config import ToolConfig, ToolLevel, FULL_TOOLS, MEDIUM_TOOLS, MINIMAL_TOOLS
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType, BACKEND_REGISTRY
from harness_eval.configs.experiment import ExperimentConfig, CRITICAL_CONDITIONS
from harness_eval.metrics.tool_dispatch import ToolCall, correct_selection_rate, redundant_call_rate, utilization_breadth
from harness_eval.metrics.context_utilization import info_retention_score, effective_token_ratio, TokenSegment
from harness_eval.metrics.backend_portability import cross_backend_stddev, min_max_ratio
from harness_eval.pipeline.analysis import compute_three_way_anova, compute_cohens_d, ANOVAResult
from harness_eval.parsers.trajectory import parse_sweagent_traj, convert_traj_to_json

app = Flask(__name__)
APP_DIR = Path(__file__).parent
TRAJECTORIES_DIR = APP_DIR / "trajectories"
TRAJECTORIES_DIR.mkdir(exist_ok=True)
SWEAGENT_DIR = Path(os.getenv("SWEAGENT_DIR", str(APP_DIR.parent / "SWE-agent"))).resolve()

# ──────────────────────────────────────────────
# Run state (in-memory, single concurrent run)
# ──────────────────────────────────────────────
run_state = {
    "run_id": None,
    "state": "idle",       # idle | running | done | stopped
    "total": 0,
    "completed": 0,
    "current": None,
    "results": [],         # [{condition_id, status, turns, error}]
    "logs": [],            # [{time, msg, type}] — live log lines
    "stop_requested": False,
    "thread": None,
    "process": None,       # current subprocess.Popen
}
MAX_LOGS = 200  # keep last N log lines

# ──────────────────────────────────────────────
# Data helpers
# ──────────────────────────────────────────────

TOOL_LEVELS = {
    "full": {"tools": FULL_TOOLS, "count": 12, "label": "Full"},
    "medium": {"tools": MEDIUM_TOOLS, "count": 8, "label": "Medium"},
    "minimal": {"tools": MINIMAL_TOOLS, "count": 5, "label": "Minimal"},
}

CTX_STRATEGIES = {
    "full": {"label": "Full Context", "detail": "No truncation"},
    "sliding_window": {"label": "Sliding Window", "detail": "50,000 tokens"},
    "summary": {"label": "Summary", "detail": "Compress old context"},
}

BACKENDS = {}
for bt in BackendType:
    reg = BACKEND_REGISTRY[bt]
    BACKENDS[bt.value] = {
        "label": f"{bt.value.title()} ({reg['model_id']})",
        "model_id": reg["model_id"],
        "provider": reg["provider"],
        "cost": reg["cost_per_eval_usd"],
    }


def scan_trajectories():
    """Scan trajectories/ folder, return list of log entries."""
    entries = []
    for condition_dir in sorted(TRAJECTORIES_DIR.iterdir()):
        if not condition_dir.is_dir():
            continue
        condition_id = condition_dir.name
        for json_file in sorted(condition_dir.glob("*.json")):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                entries.append({
                    "condition_id": condition_id,
                    "task_id": data.get("task_id", json_file.stem),
                    "resolved": data.get("resolved", False),
                    "turns": len(data.get("trajectory", [])),
                    "cost": data.get("total_cost", 0),
                    "model": data.get("model", "—"),
                    "path": str(json_file.relative_to(TRAJECTORIES_DIR)).replace("\\", "/"),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return entries


def load_log(rel_path):
    """Load a trajectory JSON file."""
    full_path = TRAJECTORIES_DIR / rel_path
    if not full_path.exists():
        return None
    return json.loads(full_path.read_text(encoding="utf-8"))


def compute_metrics_from_log(log):
    """Compute all available metrics from a trajectory log."""
    traj = log.get("trajectory", [])
    tool_level = log.get("config", {}).get("tool_level", "full")
    available = TOOL_LEVELS.get(tool_level, TOOL_LEVELS["full"])["tools"]

    # Build ToolCall objects
    tool_calls = []
    for t in traj:
        tc = ToolCall(
            turn_index=t.get("turn", 0),
            tool_name=t.get("action", ""),
            output=t.get("output", ""),
            acceptable_tools=t.get("acceptable_tools"),
        )
        tool_calls.append(tc)

    # M1.1
    m11 = correct_selection_rate(tool_calls)
    annotated = [tc for tc in tool_calls if tc.acceptable_tools]
    correct_count = sum(1 for tc in annotated if tc.tool_name in tc.acceptable_tools)

    # M1.2
    m12 = redundant_call_rate(tool_calls)
    evaluable = max(len(tool_calls) - 1, 0)
    redundant_count = int(round(m12 * evaluable))

    # M1.3
    m13 = utilization_breadth(tool_calls, available)
    used = {tc.tool_name for tc in tool_calls} & set(available)

    # M2.2 (simplified)
    total_tokens = sum(len((t.get("output", "") or "").split()) for t in traj)
    relevant_tokens = sum(
        len((t.get("output", "") or "").split())
        for t in traj
        if not t.get("acceptable_tools") or t.get("action", "") in t.get("acceptable_tools", [])
    )
    m22 = relevant_tokens / total_tokens if total_tokens > 0 else 0

    return {
        "m11": {"value": m11, "label": "Correct Selection", "dim": "D1", "detail": f"{correct_count}/{len(annotated)} correct"},
        "m12": {"value": m12, "label": "Redundant Calls", "dim": "D1", "detail": f"{redundant_count}/{evaluable} redundant", "invert": True},
        "m13": {"value": m13, "label": "Utilization Breadth", "dim": "D1", "detail": f"{len(used)}/{len(available)} tools"},
        "m21": {"value": None, "label": "Info Retention", "dim": "D2", "detail": "Requires paired runs"},
        "m22": {"value": m22, "label": "Effective Tokens", "dim": "D2", "detail": f"{relevant_tokens}/{total_tokens} tokens"},
        "m31": {"value": None, "label": "Cross-Backend StdDev", "dim": "D3", "detail": "Requires multiple backends"},
        "m32": {"value": None, "label": "Min/Max Ratio", "dim": "D3", "detail": "Requires multiple backends"},
    }


def get_condition_info(tool, ctx, be):
    """Get condition summary info."""
    cond_id = f"{tool}_{ctx}_{be}"
    is_critical = (tool, ctx, be) in CRITICAL_CONDITIONS
    runs = 3 if is_critical else 1
    cost_per = BACKENDS[be]["cost"]
    return {
        "id": cond_id,
        "is_critical": is_critical,
        "runs": runs,
        "evals": runs * 150,
        "cost": round(runs * 150 * cost_per, 2),
        "cost_per_eval": cost_per,
    }


def build_anova_dataframe():
    """Build DataFrame from all trajectory files for ANOVA analysis."""
    entries = scan_trajectories()
    if not entries:
        return None

    rows = []
    for e in entries:
        parts = e["condition_id"].split("_")
        # Parse condition_id: tool_ctx_backend
        # Handle sliding_window (has underscore)
        if "sliding_window" in e["condition_id"]:
            tool = parts[0]
            ctx = "sliding_window"
            backend = parts[-1]
        else:
            tool = parts[0]
            ctx = parts[1]
            backend = parts[2] if len(parts) > 2 else parts[-1]

        rows.append({
            "task_id": e["task_id"],
            "condition_id": e["condition_id"],
            "tool_config": tool,
            "context_strategy": ctx,
            "backend": backend,
            "resolve_rate": 1.0 if e["resolved"] else 0.0,
        })

    return pd.DataFrame(rows)


def generate_sample_anova_data():
    """Generate synthetic ANOVA data for demonstration (27 conditions x 50 tasks)."""
    np.random.seed(42)
    rows = []
    tools = ["full", "medium", "minimal"]
    contexts = ["full", "sliding_window", "summary"]
    backends = ["claude", "gpt", "deepseek"]

    # Base resolve rate + effects
    base_rate = 0.60
    tool_effects = {"full": 0.12, "medium": 0.03, "minimal": -0.15}
    ctx_effects = {"full": 0.06, "sliding_window": 0.01, "summary": -0.07}
    be_effects = {"claude": 0.04, "gpt": 0.02, "deepseek": -0.06}

    for tool in tools:
        for ctx in contexts:
            for be in backends:
                n_tasks = 50
                prob = base_rate + tool_effects[tool] + ctx_effects[ctx] + be_effects[be]
                prob = max(0.1, min(0.95, prob))  # clamp
                outcomes = np.random.binomial(1, prob, n_tasks)
                for i, resolved in enumerate(outcomes):
                    rows.append({
                        "task_id": f"task_{i:03d}",
                        "condition_id": f"{tool}_{ctx}_{be}",
                        "tool_config": tool,
                        "context_strategy": ctx,
                        "backend": be,
                        "resolve_rate": float(resolved),
                    })

    return pd.DataFrame(rows)


def evaluate_hypotheses(results):
    """Evaluate H1-H4 from ANOVA results."""
    # Build lookup
    lookup = {r.source: r for r in results}

    tool_eta = lookup.get("Tool", ANOVAResult("Tool", 0, 0, 0, 0, 1, 0)).eta_squared
    ctx_eta = lookup.get("Context", ANOVAResult("Context", 0, 0, 0, 0, 1, 0)).eta_squared
    be_eta = lookup.get("Backend", ANOVAResult("Backend", 0, 0, 0, 0, 1, 0)).eta_squared
    txb_p = lookup.get("Tool x Backend", ANOVAResult("", 0, 0, 0, 0, 1, 0)).p_value

    harness_eta = tool_eta + ctx_eta
    # Include interactions for total harness contribution
    txc_eta = lookup.get("Tool x Context", ANOVAResult("", 0, 0, 0, 0, 1, 0)).eta_squared

    hypotheses = [
        {
            "id": "H1",
            "text": "Tool configuration has the largest effect among harness components",
            "evidence": f"eta_tool={tool_eta:.3f} vs eta_ctx={ctx_eta:.3f}",
            "supported": tool_eta > ctx_eta,
        },
        {
            "id": "H2",
            "text": "Context management has medium effect (eta > 1%)",
            "evidence": f"eta_ctx={ctx_eta:.3f} ({ctx_eta*100:.1f}%)",
            "supported": ctx_eta > 0.01,
        },
        {
            "id": "H3",
            "text": "Harness components explain >= 10% of variance",
            "evidence": f"Tool+Context = {harness_eta*100:.1f}% (TxC={txc_eta*100:.1f}%)",
            "supported": (harness_eta + txc_eta) >= 0.10,
        },
        {
            "id": "H4",
            "text": "Tool x Backend interaction is significant",
            "evidence": f"p={txb_p:.4f}",
            "supported": txb_p < 0.05,
        },
    ]
    return hypotheses


def compute_pairwise_effects(df):
    """Compute Cohen's d for key pairwise comparisons."""
    comparisons = []

    def add_comparison(label, g1, g2):
        d = compute_cohens_d(np.array(g1), np.array(g2))
        abs_d = abs(d)
        if abs_d >= 0.8:
            interp = "Large effect"
        elif abs_d >= 0.5:
            interp = "Medium-large effect"
        elif abs_d >= 0.2:
            interp = "Small-medium effect"
        else:
            interp = "Negligible"
        comparisons.append({"label": label, "d": round(d, 3), "abs_d": round(abs_d, 3), "interpretation": interp})

    # Tool comparisons
    for t1, t2 in [("full", "minimal"), ("full", "medium"), ("medium", "minimal")]:
        g1 = df[df["tool_config"] == t1]["resolve_rate"].values
        g2 = df[df["tool_config"] == t2]["resolve_rate"].values
        if len(g1) >= 2 and len(g2) >= 2:
            add_comparison(f"Tool: {t1} vs {t2}", g1, g2)

    # Context comparisons
    for c1, c2 in [("full", "summary"), ("full", "sliding_window")]:
        g1 = df[df["context_strategy"] == c1]["resolve_rate"].values
        g2 = df[df["context_strategy"] == c2]["resolve_rate"].values
        if len(g1) >= 2 and len(g2) >= 2:
            add_comparison(f"Context: {c1} vs {c2}", g1, g2)

    # Backend comparisons
    for b1, b2 in [("claude", "deepseek"), ("claude", "gpt")]:
        g1 = df[df["backend"] == b1]["resolve_rate"].values
        g2 = df[df["backend"] == b2]["resolve_rate"].values
        if len(g1) >= 2 and len(g2) >= 2:
            add_comparison(f"Backend: {b1} vs {b2}", g1, g2)

    return comparisons


# ──────────────────────────────────────────────
# Page routes
# ──────────────────────────────────────────────

@app.route("/")
def page_config():
    tool = request.args.get("tool", "full")
    ctx = request.args.get("ctx", "full")
    be = request.args.get("be", "claude")
    cond = get_condition_info(tool, ctx, be)
    all_conditions, completed = build_condition_table()
    return render_template("config.html",
        active_tab="config",
        tool_levels=TOOL_LEVELS, ctx_strategies=CTX_STRATEGIES, backends=BACKENDS,
        all_tools=FULL_TOOLS,
        sel_tool=tool, sel_ctx=ctx, sel_be=be,
        cond=cond, tools_active=TOOL_LEVELS[tool]["tools"],
        all_conditions=all_conditions, completed=completed,
        models=RUN_MODELS, sel_model="ollama_1.5b",
        repo_url=os.getenv("HARNESS_REPO_URL", "https://github.com/SWE-agent/test-repo"),
        issue_url=os.getenv("HARNESS_ISSUE_URL", "https://github.com/SWE-agent/test-repo/issues/1"),
    )


@app.route("/pipeline")
def page_pipeline():
    tool = request.args.get("tool", "full")
    ctx = request.args.get("ctx", "full")
    be = request.args.get("be", "claude")
    cond = get_condition_info(tool, ctx, be)
    return render_template("pipeline.html", active_tab="pipeline",
        sel_tool=tool, sel_ctx=ctx, sel_be=be, cond=cond, backends=BACKENDS,
        models=RUN_MODELS,
        repo_url=os.getenv("HARNESS_REPO_URL", "https://github.com/SWE-agent/test-repo"),
        issue_url=os.getenv("HARNESS_ISSUE_URL", "https://github.com/SWE-agent/test-repo/issues/1"),
    )


@app.route("/logs")
def page_logs():
    entries = scan_trajectories()
    conditions = {}
    for e in entries:
        conditions.setdefault(e["condition_id"], []).append(e)
    return render_template("logs.html", active_tab="logs", conditions=conditions, total=len(entries))


@app.route("/logs/<path:log_path>")
def page_log_detail(log_path):
    log = load_log(log_path)
    if not log:
        return "Log not found", 404
    metrics = compute_metrics_from_log(log)
    tool_level = log.get("config", {}).get("tool_level", "full")
    available = TOOL_LEVELS.get(tool_level, TOOL_LEVELS["full"])["tools"]
    # Get all log paths for "Add to Compare" links
    all_entries = scan_trajectories()
    return render_template("log_detail.html", active_tab="logs",
        log=log, metrics=metrics, log_path=log_path, available_tools=available,
        all_entries=all_entries)


@app.route("/compare")
def page_compare():
    paths = request.args.getlist("p")
    items = []
    for p in paths:
        log = load_log(p)
        if log:
            m = compute_metrics_from_log(log)
            items.append({"path": p, "log": log, "metrics": m})

    # Also compute cross-backend metrics if items span multiple backends
    backend_rates = {}
    for item in items:
        be = item["log"].get("config", {}).get("backend", "unknown")
        resolved = 1.0 if item["log"].get("resolved") else 0.0
        backend_rates.setdefault(be, []).append(resolved)

    cross_be = None
    if len(backend_rates) >= 2:
        avg_rates = {be: np.mean(rates) for be, rates in backend_rates.items()}
        rates_list = list(avg_rates.values())
        cross_be = {
            "stddev": round(float(np.std(rates_list)), 4),
            "min_max": round(min(rates_list) / max(rates_list), 4) if max(rates_list) > 0 else 0,
            "backends": avg_rates,
        }

    # Get available logs for the selector
    all_entries = scan_trajectories()

    return render_template("compare.html", active_tab="compare",
        items=items, cross_be=cross_be, all_entries=all_entries)


@app.route("/anova")
def page_anova():
    run_mode = request.args.get("run")

    if run_mode == "sample":
        df = generate_sample_anova_data()
        source = "Synthetic sample (27 cond x 50 tasks)"
    elif run_mode == "trajectories":
        df = build_anova_dataframe()
        source = "Trajectory files"
        if df is None or len(df) < 10:
            return render_template("anova.html", active_tab="anova", results=None)
    else:
        return render_template("anova.html", active_tab="anova", results=None)

    # Check we have enough factor levels
    n_tools = df["tool_config"].nunique()
    n_ctx = df["context_strategy"].nunique()
    n_be = df["backend"].nunique()
    n_conditions = n_tools * n_ctx * n_be

    # Run ANOVA
    results = compute_three_way_anova(df)

    # Convert to dicts for template
    results_dicts = []
    for r in results:
        results_dicts.append({
            "source": r.source,
            "sum_sq": float(r.sum_sq) if not np.isnan(r.sum_sq) else 0.0,
            "df": int(r.df),
            "mean_sq": float(r.mean_sq) if not np.isnan(r.mean_sq) else 0.0,
            "f_statistic": float(r.f_statistic) if not np.isnan(r.f_statistic) else 0.0,
            "p_value": float(r.p_value) if not np.isnan(r.p_value) else 1.0,
            "eta_squared": float(r.eta_squared) if not np.isnan(r.eta_squared) else 0.0,
            "is_significant": bool(r.is_significant),
        })

    hypotheses = evaluate_hypotheses(results)
    pairwise = compute_pairwise_effects(df)

    return render_template("anova.html", active_tab="anova",
        results=results_dicts,
        results_json=json.dumps(results_dicts),
        hypotheses=hypotheses,
        pairwise=pairwise,
        source=source,
        n_conditions=n_conditions,
        n_observations=len(df))


# ──────────────────────────────────────────────
# API routes
# ──────────────────────────────────────────────

@app.route("/api/logs")
def api_logs():
    return jsonify(scan_trajectories())


@app.route("/api/metrics/<path:log_path>")
def api_metrics(log_path):
    log = load_log(log_path)
    if not log:
        return jsonify({"error": "not found"}), 404
    return jsonify(compute_metrics_from_log(log))


@app.route("/api/config", methods=["POST"])
def api_config():
    data = request.json or {}
    tool = data.get("tool", "full")
    ctx = data.get("ctx", "full")
    be = data.get("be", "claude")
    be_info = BACKENDS[be]
    tools = TOOL_LEVELS[tool]["tools"]

    ctx_processors = {
        "full": "[]  # keep all history",
        "sliding_window": "\n    - type: LastNObservations\n      n: 15",
        "summary": "\n    - type: LastNObservations\n      n: 5\n    - type: RemoveRegex\n      pattern: \"(.{500}).*\"\n      replacement: \"\\\\1... [truncated]\"",
    }

    yaml = f"""# HarnessEval condition: {tool}_{ctx}_{be}
# Factor A: Tool Configuration ({tool})
tools:
  bundles:
{chr(10).join(f'    - {t}' for t in tools)}
  enable_bash_tool: true

# Factor B: Context Strategy ({ctx})
agent:
  history_processors: {ctx_processors[ctx]}

# Factor C: LLM Backend ({be})
model:
  name: {be_info['model_id']}
  temperature: 0.0
  provider: {be_info['provider']}
"""
    return jsonify({"yaml": yaml, "condition": get_condition_info(tool, ctx, be)})


@app.route("/api/anova", methods=["POST"])
def api_anova():
    """Run ANOVA on trajectory data or uploaded CSV."""
    source = (request.json or {}).get("source", "trajectories")
    if source == "sample":
        df = generate_sample_anova_data()
    else:
        df = build_anova_dataframe()
    if df is None:
        return jsonify({"error": "No data available"}), 400

    results = compute_three_way_anova(df)
    return jsonify([{
        "source": r.source,
        "sum_sq": float(r.sum_sq) if not np.isnan(r.sum_sq) else 0.0,
        "df": int(r.df),
        "mean_sq": float(r.mean_sq) if not np.isnan(r.mean_sq) else 0.0,
        "f_statistic": float(r.f_statistic) if not np.isnan(r.f_statistic) else 0.0,
        "p_value": float(r.p_value) if not np.isnan(r.p_value) else 1.0,
        "eta_squared": float(r.eta_squared) if not np.isnan(r.eta_squared) else 0.0,
        "is_significant": bool(r.is_significant),
    } for r in results])


@app.route("/api/summary")
def api_summary():
    """Get summary statistics per condition from trajectory files."""
    entries = scan_trajectories()
    conditions = {}
    for e in entries:
        cid = e["condition_id"]
        if cid not in conditions:
            conditions[cid] = {"total": 0, "resolved": 0, "cost": 0}
        conditions[cid]["total"] += 1
        conditions[cid]["resolved"] += 1 if e["resolved"] else 0
        conditions[cid]["cost"] += e["cost"]

    summary = []
    for cid, stats in sorted(conditions.items()):
        summary.append({
            "condition_id": cid,
            "total_tasks": stats["total"],
            "resolved": stats["resolved"],
            "resolve_rate": round(stats["resolved"] / stats["total"], 3) if stats["total"] > 0 else 0,
            "total_cost": round(stats["cost"], 2),
        })
    return jsonify(summary)


# ──────────────────────────────────────────────
# Run page + API
# ──────────────────────────────────────────────

RUN_MODELS = {
    "ollama_1.5b": {
        "label": "Ollama qwen2.5:1.5b",
        "detail": "Local — free — 986MB RAM",
        "config": "be_ollama.yaml",
        "cost": 0,
    },
    "ollama_7b": {
        "label": "Ollama qwen2.5-coder:7b",
        "detail": "Local — free — 4.7GB RAM",
        "config": "be_ollama_7b.yaml",
        "cost": 0,
    },
    "claude": {
        "label": "Claude Sonnet 4",
        "detail": "$0.35/eval — needs ANTHROPIC_API_KEY",
        "config": "be_claude.yaml",
        "cost": 0.35,
    },
    "gpt": {
        "label": "GPT-4o",
        "detail": "$0.30/eval — needs OPENAI_API_KEY",
        "config": "be_gpt.yaml",
        "cost": 0.30,
    },
    "deepseek": {
        "label": "DeepSeek-V3",
        "detail": "$0.15/eval — needs DEEPSEEK_API_KEY",
        "config": "be_deepseek.yaml",
        "cost": 0.15,
    },
}


def build_condition_table():
    """Build the 27-condition table for the Run page."""
    from itertools import product
    tools = ["full", "medium", "minimal"]
    contexts = ["full", "sliding_window", "summary"]
    backends_list = ["claude", "gpt", "deepseek"]

    # Check which conditions already have trajectories
    entries = scan_trajectories()
    completed = {e["condition_id"] for e in entries}

    conditions = []
    for t, c, b in product(tools, contexts, backends_list):
        cid = f"{t}_{c}_{b}"
        is_crit = (t, c, b) in CRITICAL_CONDITIONS
        runs = 3 if is_crit else 1
        cost_per = BACKENDS.get(b, {}).get("cost", 0)
        conditions.append({
            "id": cid,
            "tool": t,
            "ctx": c,
            "backend": b,
            "is_critical": is_crit,
            "runs": runs,
            "cost": round(runs * cost_per, 2),
        })
    return conditions, completed


@app.route("/run")
def page_run():
    """Redirect to Config tab (run controls are now in Tab 1)."""
    from flask import redirect
    return redirect("/")


@app.route("/api/run", methods=["POST"])
def api_run_start():
    """Start running selected conditions."""
    global run_state
    if run_state["state"] == "running" and run_state.get("thread") and run_state["thread"].is_alive():
        return jsonify({"error": "A run is already in progress"}), 409
    # Reset stale state
    run_state["state"] = "idle"

    data = request.json or {}
    conditions = data.get("conditions", [])
    model = data.get("model", "ollama")
    repo_url = data.get("repo_url", os.getenv("HARNESS_REPO_URL", ""))
    issue_url = data.get("issue_url", os.getenv("HARNESS_ISSUE_URL", ""))

    if not conditions:
        return jsonify({"error": "No conditions selected"}), 400
    if not repo_url or not issue_url:
        return jsonify({"error": "Repo URL and Issue URL required"}), 400

    rid = str(uuid.uuid4())[:8]
    run_state.update({
        "run_id": rid,
        "state": "running",
        "total": len(conditions),
        "completed": 0,
        "current": None,
        "results": [],
        "logs": [],
        "stop_requested": False,
        "process": None,
    })

    # Start background thread
    t = threading.Thread(
        target=_run_conditions_thread,
        args=(rid, conditions, model, repo_url, issue_url),
        daemon=True,
    )
    run_state["thread"] = t
    t.start()

    return jsonify({"run_id": rid, "total": len(conditions)})


@app.route("/api/run/status")
def api_run_status():
    """Poll run status. Use ?since=N to get only new logs."""
    since = int(request.args.get("since", 0))
    new_logs = run_state["logs"][since:]
    return jsonify({
        "run_id": run_state["run_id"],
        "state": run_state["state"],
        "total": run_state["total"],
        "completed": run_state["completed"],
        "current": run_state["current"],
        "results": run_state["results"],
        "logs": new_logs,
        "log_offset": len(run_state["logs"]),
    })


@app.route("/api/run/clear", methods=["POST"])
def api_run_clear():
    """Reset run state to idle."""
    run_state.update({
        "run_id": None, "state": "idle", "total": 0, "completed": 0,
        "current": None, "results": [], "logs": [], "stop_requested": False, "process": None,
    })
    return jsonify({"ok": True})


@app.route("/api/run/stop", methods=["POST"])
def api_run_stop():
    """Request stop of current run."""
    run_state["stop_requested"] = True
    proc = run_state.get("process")
    if proc and proc.poll() is None:
        proc.kill()
    return jsonify({"ok": True})


def _add_log(msg, log_type="info"):
    """Thread-safe: push a log line to run_state."""
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    run_state["logs"].append({"time": ts, "msg": msg, "type": log_type})
    # Trim old logs
    if len(run_state["logs"]) > MAX_LOGS:
        run_state["logs"] = run_state["logs"][-MAX_LOGS:]


def _run_conditions_thread(rid, conditions, model, repo_url, issue_url):
    """Background thread: run each condition via SWE-Agent subprocess with live output."""
    global run_state
    cfg_dir = SWEAGENT_DIR / "config" / "harness_eval"

    _add_log(f"Run {rid}: {len(conditions)} conditions, model={model}")

    for i, cond_id in enumerate(conditions):
        if run_state["stop_requested"]:
            _add_log("Stop requested — aborting", "error")
            run_state["state"] = "stopped"
            return

        run_state["current"] = cond_id
        _add_log(f"[{i+1}/{len(conditions)}] Starting {cond_id}...")

        # Parse condition_id -> tool, ctx, backend
        parts = cond_id.split("_")
        if "sliding_window" in cond_id:
            tool = parts[0]
            ctx = "sliding_window"
            backend = parts[-1]
        else:
            tool, ctx, backend = parts[0], parts[1], parts[-1]

        # Build config list — override backend with selected model
        model_cfg = RUN_MODELS.get(model, RUN_MODELS.get("ollama_1.5b", {})).get("config", "be_ollama.yaml")
        config_files = [
            str(cfg_dir / "base.yaml"),
            str(cfg_dir / f"tool_{tool}.yaml"),
            str(cfg_dir / f"ctx_{ctx}.yaml"),
            str(cfg_dir / model_cfg),
        ]

        # Verify all configs exist
        missing = [f for f in config_files if not Path(f).exists()]
        if missing:
            _add_log(f"  SKIP — missing config: {missing}", "error")
            run_state["results"].append({
                "condition_id": cond_id, "status": "failed",
                "error": f"Missing configs: {missing}", "turns": 0,
            })
            run_state["completed"] = i + 1
            continue

        _add_log(f"  Tool: {tool}, Context: {ctx}, Model: {model_cfg}")

        # Output dir
        output_dir = SWEAGENT_DIR / "trajectories" / "harness_runs" / cond_id

        # Build command
        cmd = [
            sys.executable, "-m", "sweagent", "run",
            "--env.repo.github_url", repo_url,
            "--problem_statement.github_url", issue_url,
            "--output_dir", str(output_dir),
        ]
        for cf in config_files:
            cmd.extend(["--config", cf])

        # Run subprocess with live output streaming
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        timeout = int(os.getenv("HARNESS_TIMEOUT", "300"))
        success = False
        step_count = 0

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(SWEAGENT_DIR),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
            )
            run_state["process"] = proc

            start_time = time.time()
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue

                # Parse interesting lines from SWE-Agent output
                if "STEP" in line:
                    step_count += 1
                    _add_log(f"  Step {step_count}...", "info")
                elif "ACTION" in line:
                    # Extract action name
                    action = line.split("ACTION")[-1].strip()[:80]
                    if action:
                        _add_log(f"    {action}", "info")
                elif "Trajectory saved" in line:
                    _add_log(f"  Trajectory saved", "done")
                elif "ERROR" in line.upper() or "Error" in line:
                    _add_log(f"  {line[:120]}", "error")
                elif "INFO" in line and ("Starting" in line or "Done" in line or "Pulling" in line or "Exiting" in line):
                    _add_log(f"  {line.split('INFO')[-1].strip()[:100]}", "info")

                # Check timeout
                if time.time() - start_time > timeout:
                    proc.kill()
                    _add_log(f"  TIMEOUT after {timeout}s", "error")
                    break

                # Check stop request
                if run_state["stop_requested"]:
                    proc.kill()
                    _add_log("  Killed by stop request", "error")
                    break

            proc.wait(timeout=10)
            success = proc.returncode == 0
            run_state["process"] = None

        except Exception as e:
            _add_log(f"  Exception: {str(e)[:100]}", "error")
            success = False
            run_state["process"] = None

        # Convert .traj to our JSON format
        turns = 0
        if success and output_dir.exists():
            traj_files = list(output_dir.rglob("*.traj"))
            for tf in traj_files:
                try:
                    parsed = parse_sweagent_traj(tf)
                    turns = parsed.metadata.num_turns
                    out_cond = f"{tool}_{ctx}_{model}"
                    out_path = TRAJECTORIES_DIR / out_cond / f"{parsed.metadata.task_id}.json"
                    convert_traj_to_json(tf, out_path)
                    _add_log(f"  Converted: {out_cond}/{parsed.metadata.task_id}.json ({turns} turns)", "done")
                except Exception as e:
                    _add_log(f"  Convert error: {str(e)[:80]}", "error")

        status = "done" if success else "failed"
        _add_log(f"[{i+1}/{len(conditions)}] {cond_id} — {status} ({turns} turns, {step_count} steps)", status)

        run_state["results"].append({
            "condition_id": cond_id, "status": status, "turns": turns, "error": "",
        })
        run_state["completed"] = i + 1

    run_state["state"] = "done"
    run_state["current"] = None
    _add_log(f"Run complete: {run_state['completed']}/{run_state['total']}", "done")


if __name__ == "__main__":
    print(f"Trajectories dir: {TRAJECTORIES_DIR}")
    print(f"SWE-Agent dir: {SWEAGENT_DIR}")
    print(f"Found {len(scan_trajectories())} trajectory files")
    app.run(debug=True, port=5000)
