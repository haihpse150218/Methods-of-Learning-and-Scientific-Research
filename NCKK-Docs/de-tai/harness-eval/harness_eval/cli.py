"""CLI entry point for HarnessEval toolkit."""

from pathlib import Path

import click

from harness_eval import __version__
from harness_eval.configs.experiment import ExperimentConfig


@click.group()
@click.version_option(version=__version__)
def main():
    """HarnessEval: Evaluate coding agent scaffolds through ablation-driven analysis."""
    pass


@main.command()
def info():
    """Show experiment design summary."""
    config = ExperimentConfig()
    conditions = config.generate_conditions()

    click.echo(f"HarnessEval v{__version__}")
    click.echo(f"{'='*50}")
    click.echo(f"Total conditions:     {config.total_conditions}")
    click.echo(f"Tasks per condition:  {config.num_tasks}")
    click.echo(f"Total evaluations:   {config.total_evaluations:,}")
    click.echo(f"Pilot evaluations:   {config.pilot_evaluations}")
    click.echo(f"Estimated cost:      ${config.estimated_total_cost:,.0f}")
    click.echo()
    click.echo("Conditions:")
    for c in conditions:
        runs = config.runs_for_condition(c)
        click.echo(f"  {c.condition_id:40s} runs={runs}")


@main.command()
@click.option("--output", "-o", default="trajectories", help="Output directory for trajectory files")
@click.option("--dry-run", is_flag=True, default=False, help="Generate synthetic data instead of calling SWE-Agent")
@click.option("--max-tasks", type=int, default=None, help="Override number of tasks per condition")
@click.option("--sweagent-dir", type=click.Path(exists=True, path_type=Path), default=None, help="Path to SWE-Agent installation")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable verbose logging")
def pilot(output: str, dry_run: bool, max_tasks: int | None, sweagent_dir: Path | None, verbose: bool):
    """Run pilot study (5 critical conditions x 20 tasks x 2 runs = 200 evals).

    Use --dry-run to generate synthetic data for testing the pipeline.
    """
    from harness_eval.pipeline.runner import run_pilot

    output_dir = Path(output)

    if not dry_run and sweagent_dir is None:
        raise click.UsageError(
            "Real mode requires --sweagent-dir pointing to SWE-Agent installation. "
            "Use --dry-run for synthetic data."
        )

    mode = "DRY-RUN (synthetic)" if dry_run else "REAL (SWE-Agent)"
    tasks_label = max_tasks if max_tasks else "20 (default)"
    click.echo(f"HarnessEval Pilot Study")
    click.echo(f"{'='*50}")
    click.echo(f"Mode:       {mode}")
    click.echo(f"Tasks/cond: {tasks_label}")
    click.echo(f"Output:     {output_dir.resolve()}")
    if sweagent_dir:
        click.echo(f"SWE-Agent:  {sweagent_dir.resolve()}")
    click.echo()

    import logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(name)s %(message)s")

    results = run_pilot(
        output_dir=output_dir,
        dry_run=dry_run,
        sweagent_dir=sweagent_dir,
        max_tasks=max_tasks,
    )

    click.echo()
    click.echo(f"{'='*50}")
    click.echo(f"Pilot complete: {len(results)} condition runs")
    total_cost = sum(cr.total_cost for cr in results)
    avg_resolve = sum(cr.resolve_rate for cr in results) / len(results) if results else 0
    click.echo(f"Total cost:     ${total_cost:.2f}")
    click.echo(f"Avg resolve:    {avg_resolve:.1%}")
    click.echo()
    for cr in results:
        click.echo(
            f"  {cr.condition_id:40s} "
            f"resolve={cr.resolve_rate:.1%}  "
            f"cost=${cr.total_cost:.2f}  "
            f"tasks={len(cr.task_results)}"
        )


@main.command()
@click.option("--output", "-o", default="trajectories", help="Output directory for trajectory files")
@click.option("--dry-run", is_flag=True, default=False, help="Generate synthetic data instead of calling SWE-Agent")
@click.option("--max-tasks", type=int, default=None, help="Override number of tasks per condition")
@click.option("--sweagent-dir", type=click.Path(exists=True, path_type=Path), default=None, help="Path to SWE-Agent installation")
@click.option("--conditions", "-c", multiple=True, help="Filter to specific condition IDs (can specify multiple)")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable verbose logging")
def run(output: str, dry_run: bool, max_tasks: int | None, sweagent_dir: Path | None, conditions: tuple, verbose: bool):
    """Run full experiment (27 conditions x 150 tasks = 7,050 evals).

    Use --dry-run to generate synthetic data for testing.
    Use -c to filter to specific conditions.
    """
    from harness_eval.pipeline.runner import run_full, PipelineRunner, RunConfig

    output_dir = Path(output)

    if not dry_run and sweagent_dir is None:
        raise click.UsageError(
            "Real mode requires --sweagent-dir pointing to SWE-Agent installation. "
            "Use --dry-run for synthetic data."
        )

    mode = "DRY-RUN (synthetic)" if dry_run else "REAL (SWE-Agent)"
    click.echo(f"HarnessEval Full Experiment")
    click.echo(f"{'='*50}")
    click.echo(f"Mode:       {mode}")
    click.echo(f"Tasks/cond: {max_tasks or '150 (default)'}")
    click.echo(f"Output:     {output_dir.resolve()}")
    if conditions:
        click.echo(f"Conditions: {', '.join(conditions)}")
    if sweagent_dir:
        click.echo(f"SWE-Agent:  {sweagent_dir.resolve()}")
    click.echo()

    import logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(name)s %(message)s")

    if conditions:
        # Use PipelineRunner directly for filtered conditions
        exp = ExperimentConfig()
        config = RunConfig(
            output_dir=output_dir,
            dry_run=dry_run,
            max_tasks=max_tasks,
            conditions=list(conditions),
            sweagent_dir=sweagent_dir,
            verbose=verbose,
        )
        runner = PipelineRunner(exp, config)
        results = runner.run_all()
    else:
        results = run_full(
            output_dir=output_dir,
            dry_run=dry_run,
            sweagent_dir=sweagent_dir,
            max_tasks=max_tasks,
        )

    click.echo()
    click.echo(f"{'='*50}")
    click.echo(f"Experiment complete: {len(results)} condition runs")
    total_cost = sum(cr.total_cost for cr in results)
    avg_resolve = sum(cr.resolve_rate for cr in results) / len(results) if results else 0
    click.echo(f"Total cost:     ${total_cost:.2f}")
    click.echo(f"Avg resolve:    {avg_resolve:.1%}")
    click.echo()
    for cr in results:
        click.echo(
            f"  {cr.condition_id:40s} "
            f"resolve={cr.resolve_rate:.1%}  "
            f"cost=${cr.total_cost:.2f}  "
            f"tasks={len(cr.task_results)}"
        )


@main.command()
@click.argument("traj_path", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), default=None, help="Output JSON path (default: print to stdout)")
def convert(traj_path: Path, output: Path | None):
    """Convert a SWE-Agent .traj file to HarnessEval JSON format."""
    from harness_eval.parsers.trajectory import convert_traj_to_json
    import json

    result = convert_traj_to_json(traj_path, output)

    if output:
        click.echo(f"Converted: {traj_path} -> {output}")
    else:
        click.echo(json.dumps(result, indent=2))


@main.command()
@click.argument("results_dir", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), default=None, help="Output CSV path for ANOVA results")
def analyze(results_dir: Path, output: Path | None):
    """Run ANOVA analysis on trajectory results.

    RESULTS_DIR should contain condition subdirectories with trajectory JSON files.
    """
    from harness_eval.parsers.trajectory import parse_condition_dir
    from harness_eval.pipeline.analysis import compute_three_way_anova, compute_cohens_d
    import pandas as pd

    # Scan condition directories
    condition_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
    if not condition_dirs:
        raise click.UsageError(f"No condition directories found in {results_dir}")

    click.echo(f"Analyzing {len(condition_dirs)} conditions in {results_dir}")
    click.echo()

    # Parse all trajectories and build DataFrame
    rows = []
    for cond_dir in sorted(condition_dirs):
        try:
            trajectories = parse_condition_dir(cond_dir)
        except (FileNotFoundError, ValueError) as e:
            click.echo(f"  Skipping {cond_dir.name}: {e}", err=True)
            continue

        for traj in trajectories:
            m = traj.metadata
            rows.append({
                "task_id": m.task_id,
                "condition_id": m.condition_id,
                "tool_config": m.tool_level,
                "context_strategy": m.context_strategy,
                "backend": m.backend,
                "resolve_rate": 1.0 if m.resolved else 0.0,
                "total_cost": m.total_cost,
            })

    if not rows:
        raise click.UsageError("No valid trajectory data found")

    df = pd.DataFrame(rows)
    click.echo(f"Loaded {len(df)} task results across {df['condition_id'].nunique()} conditions")
    click.echo()

    # Run ANOVA
    try:
        anova_results = compute_three_way_anova(df)
    except Exception as e:
        raise click.ClickException(f"ANOVA failed: {e}")

    click.echo(f"{'Source':<30s} {'eta²':>8s} {'F':>10s} {'p-value':>10s} {'Sig?':>6s}")
    click.echo("-" * 70)
    for r in anova_results:
        sig = "***" if r.p_value < 0.001 else "**" if r.p_value < 0.01 else "*" if r.is_significant else ""
        click.echo(
            f"  {r.source:<28s} {r.eta_squared:>8.4f} {r.f_statistic:>10.3f} {r.p_value:>10.4f} {sig:>6s}"
        )

    if output:
        import csv as csv_mod
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv_mod.DictWriter(f, fieldnames=["source", "sum_sq", "df", "mean_sq", "f_statistic", "p_value", "eta_squared", "is_significant"])
            writer.writeheader()
            for r in anova_results:
                writer.writerow({
                    "source": r.source,
                    "sum_sq": f"{r.sum_sq:.6f}",
                    "df": r.df,
                    "mean_sq": f"{r.mean_sq:.6f}",
                    "f_statistic": f"{r.f_statistic:.4f}",
                    "p_value": f"{r.p_value:.6f}",
                    "eta_squared": f"{r.eta_squared:.6f}",
                    "is_significant": r.is_significant,
                })
        click.echo(f"\nANOVA results saved to {output}")


if __name__ == "__main__":
    main()
