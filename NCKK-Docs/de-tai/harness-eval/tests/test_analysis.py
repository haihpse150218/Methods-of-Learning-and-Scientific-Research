"""Tests for statistical analysis module (RO4: ANOVA)."""

import pytest
import numpy as np
import pandas as pd

from harness_eval.pipeline.analysis import compute_cohens_d


class TestCohensD:
    def test_identical_groups(self):
        g1 = np.array([0.5, 0.6, 0.7, 0.5, 0.6])
        g2 = np.array([0.5, 0.6, 0.7, 0.5, 0.6])
        assert compute_cohens_d(g1, g2) == 0.0

    def test_large_effect(self):
        """Cohen's d > 0.8 is a large effect (H1 hypothesis)."""
        g1 = np.array([0.8, 0.9, 0.85, 0.75, 0.88])  # full tools
        g2 = np.array([0.3, 0.4, 0.35, 0.25, 0.38])  # minimal tools
        d = compute_cohens_d(g1, g2)
        assert d > 0.8, f"Expected large effect, got d={d:.2f}"

    def test_medium_effect(self):
        """Cohen's d 0.3-0.5 is medium (H2 hypothesis)."""
        g1 = np.array([0.7, 0.72, 0.68, 0.71, 0.69])  # full context
        g2 = np.array([0.55, 0.58, 0.52, 0.56, 0.54])  # summary context
        d = compute_cohens_d(g1, g2)
        assert d > 0.2  # reasonable positive effect

    def test_small_groups(self):
        """Groups with fewer than 2 elements return 0."""
        g1 = np.array([0.5])
        g2 = np.array([0.3])
        assert compute_cohens_d(g1, g2) == 0.0

    def test_zero_variance(self):
        g1 = np.array([0.5, 0.5, 0.5])
        g2 = np.array([0.5, 0.5, 0.5])
        assert compute_cohens_d(g1, g2) == 0.0

    def test_sign_direction(self):
        """Positive d means group1 > group2."""
        g1 = np.array([0.8, 0.9, 0.85])
        g2 = np.array([0.3, 0.4, 0.35])
        assert compute_cohens_d(g1, g2) > 0
        assert compute_cohens_d(g2, g1) < 0


class TestANOVAIntegration:
    """Integration test: verify ANOVA runs on synthetic data."""

    @pytest.fixture
    def synthetic_data(self):
        """Create synthetic experimental data mimicking 27 conditions."""
        np.random.seed(42)
        rows = []
        tool_effect = {"full": 0.15, "medium": 0.05, "minimal": -0.10}
        ctx_effect = {"full": 0.10, "sliding_window": 0.02, "summary": -0.05}
        backend_effect = {"claude": 0.08, "gpt": 0.03, "deepseek": -0.05}

        for tool in ["full", "medium", "minimal"]:
            for ctx in ["full", "sliding_window", "summary"]:
                for backend in ["claude", "gpt", "deepseek"]:
                    base = 0.50
                    rate = base + tool_effect[tool] + ctx_effect[ctx] + backend_effect[backend]
                    # 10 tasks per condition
                    for _ in range(10):
                        resolved = 1 if np.random.random() < rate else 0
                        rows.append({
                            "tool_config": tool,
                            "context_strategy": ctx,
                            "backend": backend,
                            "resolve_rate": resolved,
                        })
        return pd.DataFrame(rows)

    def test_anova_runs(self, synthetic_data):
        """ANOVA should complete without errors on valid data."""
        from harness_eval.pipeline.analysis import compute_three_way_anova

        results = compute_three_way_anova(synthetic_data)
        assert len(results) > 0

        # Should have sources for main effects, interactions, and error
        sources = {r.source for r in results}
        assert "Tool" in sources
        assert "Context" in sources
        assert "Backend" in sources
        assert "Error" in sources

    def test_eta_squared_sums_to_one(self, synthetic_data):
        """All eta-squared values should sum to approximately 1.0."""
        from harness_eval.pipeline.analysis import compute_three_way_anova

        results = compute_three_way_anova(synthetic_data)
        total_eta = sum(r.eta_squared for r in results)
        assert abs(total_eta - 1.0) < 0.01, f"Eta-squared sum = {total_eta:.4f}"

    def test_eta_squared_non_negative(self, synthetic_data):
        """All eta-squared values should be non-negative."""
        from harness_eval.pipeline.analysis import compute_three_way_anova

        results = compute_three_way_anova(synthetic_data)
        for r in results:
            assert r.eta_squared >= 0, f"{r.source} has negative eta-squared: {r.eta_squared}"

    def test_tool_has_effect(self, synthetic_data):
        """With synthetic data, tool config should show an effect."""
        from harness_eval.pipeline.analysis import compute_three_way_anova

        results = compute_three_way_anova(synthetic_data)
        tool_result = next(r for r in results if r.source == "Tool")
        # With added effects, tool should explain some variance
        assert tool_result.eta_squared > 0.0


class TestGLMM:
    """Tests for GLMM robustness analysis."""

    @pytest.fixture
    def glmm_data(self):
        """Create continuous data with task_id for random effects.

        Uses continuous resolve_rate (not binary) so GLMM converges reliably.
        """
        np.random.seed(42)
        rows = []
        task_ids = [f"task-{i}" for i in range(30)]
        # Task difficulty varies (random intercept)
        task_difficulty = {tid: np.random.normal(0, 0.05) for tid in task_ids}

        tool_effect = {"full": 0.15, "medium": 0.05, "minimal": -0.10}
        ctx_effect = {"full": 0.10, "sliding_window": 0.02, "summary": -0.05}
        backend_effect = {"claude": 0.08, "gpt": 0.03, "deepseek": -0.05}

        for tool in ["full", "medium", "minimal"]:
            for ctx in ["full", "sliding_window", "summary"]:
                for backend in ["claude", "gpt", "deepseek"]:
                    for tid in task_ids:
                        base = 0.50 + task_difficulty[tid]
                        rate = base + tool_effect[tool] + ctx_effect[ctx] + backend_effect[backend]
                        # Add noise but keep as continuous rate
                        resolve_rate = np.clip(rate + np.random.normal(0, 0.08), 0, 1)
                        rows.append({
                            "task_id": tid,
                            "tool_config": tool,
                            "context_strategy": ctx,
                            "backend": backend,
                            "resolve_rate": resolve_rate,
                        })
        return pd.DataFrame(rows)

    def test_glmm_runs(self, glmm_data):
        """GLMM should complete without errors."""
        from harness_eval.pipeline.analysis import compute_glmm

        result = compute_glmm(glmm_data)
        assert result.converged is True
        assert result.n_observations == len(glmm_data)
        assert result.n_groups == 30

    def test_glmm_fixed_effects(self, glmm_data):
        """GLMM should produce fixed effects for all factors."""
        from harness_eval.pipeline.analysis import compute_glmm

        result = compute_glmm(glmm_data)
        assert "Intercept" in result.fixed_effects
        assert len(result.fixed_effects) > 1

    def test_glmm_random_effect_variance(self, glmm_data):
        """Random effect variance should be non-negative."""
        from harness_eval.pipeline.analysis import compute_glmm

        result = compute_glmm(glmm_data)
        assert result.random_effect_variance >= 0.0

    def test_glmm_model_fit(self, glmm_data):
        """GLMM should produce log-likelihood (AIC/BIC may be NaN with REML)."""
        from harness_eval.pipeline.analysis import compute_glmm

        result = compute_glmm(glmm_data)
        assert isinstance(result.aic, float)
        assert isinstance(result.bic, float)
        assert isinstance(result.log_likelihood, float)
        # log-likelihood should be finite
        assert not np.isnan(result.log_likelihood)

    def test_glmm_missing_columns(self):
        """GLMM should raise ValueError for missing columns."""
        from harness_eval.pipeline.analysis import compute_glmm

        df = pd.DataFrame({"x": [1, 2, 3]})
        with pytest.raises(ValueError, match="Missing required columns"):
            compute_glmm(df)

    def test_glmm_insufficient_groups(self):
        """GLMM should raise ValueError with < 2 task groups."""
        from harness_eval.pipeline.analysis import compute_glmm

        df = pd.DataFrame({
            "task_id": ["t1"] * 9,
            "tool_config": ["full"] * 3 + ["medium"] * 3 + ["minimal"] * 3,
            "context_strategy": ["full", "sliding_window", "summary"] * 3,
            "backend": ["claude"] * 9,
            "resolve_rate": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
        })
        with pytest.raises(ValueError, match="at least 2 unique task_ids"):
            compute_glmm(df)

    def test_fixed_effect_significance(self, glmm_data):
        """FixedEffect.is_significant uses Bonferroni correction."""
        from harness_eval.pipeline.analysis import FixedEffect

        sig = FixedEffect("test", 0.5, 0.1, 5.0, 0.001)
        assert sig.is_significant is True

        not_sig = FixedEffect("test", 0.1, 0.1, 1.0, 0.10)
        assert not_sig.is_significant is False
