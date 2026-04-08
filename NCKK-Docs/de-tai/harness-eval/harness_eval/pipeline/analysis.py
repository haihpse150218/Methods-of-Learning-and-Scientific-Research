"""Statistical analysis for RO4: Three-way ANOVA and GLMM.

Decomposes variance contributions of harness vs. LLM:
  Total Variance = V_Tool + V_Context + V_Backend + V_TxB + V_CxB + V_TxC + V_TxCxB + V_Error
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class ANOVAResult:
    """Result from a three-way ANOVA analysis."""

    source: str
    sum_sq: float
    df: int
    mean_sq: float
    f_statistic: float
    p_value: float
    eta_squared: float  # effect size

    @property
    def is_significant(self) -> bool:
        """Significant at p < 0.05 after Bonferroni correction (7 tests)."""
        return self.p_value < (0.05 / 7)


def compute_three_way_anova(df: pd.DataFrame) -> list[ANOVAResult]:
    """Three-way ANOVA: Tool (3) x Context (3) x Backend (3).

    Args:
        df: DataFrame with columns:
            - tool_config: str ("full", "medium", "minimal")
            - context_strategy: str ("full", "sliding_window", "summary")
            - backend: str ("claude", "gpt", "deepseek")
            - resolve_rate: float (0 or 1 per task, or aggregated)

    Returns:
        List of ANOVAResult for each source of variation.
    """
    try:
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
    except ImportError:
        raise ImportError("statsmodels is required: pip install statsmodels")

    model = ols(
        "resolve_rate ~ C(tool_config) * C(context_strategy) * C(backend)",
        data=df,
    ).fit()

    anova_table = sm.stats.anova_lm(model, typ=2)
    total_ss = anova_table["sum_sq"].sum()

    results = []
    source_names = {
        "C(tool_config)": "Tool",
        "C(context_strategy)": "Context",
        "C(backend)": "Backend",
        "C(tool_config):C(context_strategy)": "Tool x Context",
        "C(tool_config):C(backend)": "Tool x Backend",
        "C(context_strategy):C(backend)": "Context x Backend",
        "C(tool_config):C(context_strategy):C(backend)": "Tool x Context x Backend",
        "Residual": "Error",
    }

    for idx, row in anova_table.iterrows():
        name = source_names.get(idx, idx)
        ss = row["sum_sq"]
        dof = int(row["df"])
        ms = ss / dof if dof > 0 else 0
        f_val = row.get("F", 0) or 0
        p_val = row.get("PR(>F)", 1.0) or 1.0
        eta_sq = ss / total_ss if total_ss > 0 else 0

        results.append(
            ANOVAResult(
                source=name,
                sum_sq=ss,
                df=dof,
                mean_sq=ms,
                f_statistic=f_val,
                p_value=p_val,
                eta_squared=eta_sq,
            )
        )

    return results


def compute_cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Cohen's d effect size for pairwise comparison.

    d > 0.8: large effect
    d = 0.5: medium effect
    d = 0.2: small effect

    Returns:
        Float (can be negative if group2 > group1).
    """
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0

    mean_diff = np.mean(group1) - np.mean(group2)
    pooled_std = np.sqrt(
        ((n1 - 1) * np.var(group1, ddof=1) + (n2 - 1) * np.var(group2, ddof=1))
        / (n1 + n2 - 2)
    )
    if pooled_std == 0:
        return 0.0
    return float(mean_diff / pooled_std)


def tukey_hsd_pairwise(df: pd.DataFrame, factor: str, value: str = "resolve_rate") -> pd.DataFrame:
    """Tukey HSD post-hoc pairwise comparisons for a given factor.

    Args:
        df: DataFrame with the factor column and value column.
        factor: Column name for the grouping factor.
        value: Column name for the dependent variable.

    Returns:
        DataFrame with pairwise comparison results.
    """
    from statsmodels.stats.multicomp import pairwise_tukeyhsd

    result = pairwise_tukeyhsd(df[value], df[factor], alpha=0.05)
    return pd.DataFrame(
        data=result._results_table.data[1:],
        columns=result._results_table.data[0],
    )


@dataclass
class FixedEffect:
    """A single fixed effect from GLMM."""

    name: str
    coefficient: float
    std_error: float
    z_value: float
    p_value: float

    @property
    def is_significant(self) -> bool:
        """Significant at p < 0.05 after Bonferroni correction (7 tests)."""
        return self.p_value < (0.05 / 7)


@dataclass
class GLMMResult:
    """Result from a Generalized Linear Mixed Model analysis."""

    fixed_effects: dict[str, FixedEffect]
    random_effect_variance: float  # Variance of random intercept (task_id)
    converged: bool
    log_likelihood: float
    aic: float
    bic: float
    n_observations: int
    n_groups: int  # Number of unique task_ids


def compute_glmm(df: pd.DataFrame) -> GLMMResult:
    """Generalized Linear Mixed Model with task_id as random intercept.

    Model: resolve_rate ~ Tool + Context + Backend + Tool:Context + Tool:Backend
                          + Context:Backend + (1 | task_id)

    This accounts for the fact that some tasks are inherently harder than others,
    providing a robustness check for the ANOVA results.

    Args:
        df: DataFrame with columns:
            - task_id: str (random effect grouping)
            - tool_config: str ("full", "medium", "minimal")
            - context_strategy: str ("full", "sliding_window", "summary")
            - backend: str ("claude", "gpt", "deepseek")
            - resolve_rate: float (0 or 1 per task, or aggregated)

    Returns:
        GLMMResult with fixed effects, random effect variance, and model fit stats.

    Raises:
        ImportError: If statsmodels is not installed.
        ValueError: If data is insufficient for GLMM fitting.
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        raise ImportError("statsmodels is required: pip install statsmodels")

    required_cols = {"task_id", "tool_config", "context_strategy", "backend", "resolve_rate"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    n_groups = df["task_id"].nunique()
    if n_groups < 2:
        raise ValueError(
            f"GLMM requires at least 2 unique task_ids (groups), got {n_groups}"
        )

    # Fit mixed model: fixed effects for factors + random intercept for task_id
    formula = (
        "resolve_rate ~ C(tool_config) + C(context_strategy) + C(backend)"
        " + C(tool_config):C(context_strategy)"
        " + C(tool_config):C(backend)"
        " + C(context_strategy):C(backend)"
    )

    model = smf.mixedlm(
        formula,
        data=df,
        groups=df["task_id"],
    )
    try:
        result = model.fit(reml=True)
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            f"Singular matrix — too little variance in the data. "
            f"Try running with more tasks or more conditions. Original: {exc}"
        )

    # Extract fixed effects
    fixed_effects = {}
    fe_params = result.fe_params
    fe_bse = result.bse_fe
    fe_tvalues = result.tvalues
    fe_pvalues = result.pvalues

    for name in fe_params.index:
        # Clean up statsmodels naming for readability
        clean_name = (
            name.replace("C(tool_config)", "Tool")
            .replace("C(context_strategy)", "Context")
            .replace("C(backend)", "Backend")
            .replace("[T.", "[")
        )
        fixed_effects[clean_name] = FixedEffect(
            name=clean_name,
            coefficient=float(fe_params[name]),
            std_error=float(fe_bse[name]) if name in fe_bse.index else 0.0,
            z_value=float(fe_tvalues[name]) if name in fe_tvalues.index else 0.0,
            p_value=float(fe_pvalues[name]) if name in fe_pvalues.index else 1.0,
        )

    # Random effect variance
    re_variance = float(result.cov_re.iloc[0, 0]) if hasattr(result, "cov_re") else 0.0

    return GLMMResult(
        fixed_effects=fixed_effects,
        random_effect_variance=re_variance,
        converged=result.converged,
        log_likelihood=float(result.llf),
        aic=float(result.aic) if not np.isnan(result.aic) else float("nan"),
        bic=float(result.bic) if not np.isnan(result.bic) else float("nan"),
        n_observations=len(df),
        n_groups=n_groups,
    )
