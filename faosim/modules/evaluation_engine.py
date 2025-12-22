"""
Simulation & Evaluation Engine

Evaluates campaign variants against goals and constraints.
Determines which campaigns are winners based on forecasted performance.
"""

from typing import List, Tuple, Optional
from loguru import logger

from faosim.core.schemas import (
    CampaignParameters,
    ForecastMetrics,
    ForecastResult,
    UserConstraints,
    MetricType,
)


class EvaluationEngine:
    """
    Evaluates campaign performance against user goals.

    Determines winners and assigns fitness scores for optimization.
    """

    def __init__(self, user_constraints: UserConstraints):
        """
        Initialize evaluation engine.

        Args:
            user_constraints: User-defined goals and constraints
        """
        self.user_constraints = user_constraints
        self.goal_metric = user_constraints.goal.metric
        self.target_value = user_constraints.goal.target_value
        self.tolerance = user_constraints.goal.tolerance

        logger.info(
            f"Evaluation Engine initialized (Target: {self.goal_metric.value} = {self.target_value})"
        )

    def evaluate_campaign(
        self,
        campaign: CampaignParameters,
        forecast: ForecastMetrics,
    ) -> ForecastResult:
        """
        Evaluate a single campaign against goals.

        Args:
            campaign: Campaign parameters
            forecast: Forecasted metrics

        Returns:
            ForecastResult with evaluation details
        """
        # Get the metric value based on goal type
        metric_value = self._get_metric_value(forecast)

        # Check if campaign meets target
        is_winner = self._check_if_winner(metric_value)

        # Calculate fitness score
        score = self._calculate_fitness_score(forecast, metric_value)

        # Generate notes
        notes = self._generate_notes(forecast, metric_value, is_winner)

        result = ForecastResult(
            campaign_params=campaign,
            forecast_metrics=forecast,
            is_winner=is_winner,
            score=score,
            notes=notes,
        )

        return result

    def evaluate_batch(
        self,
        campaigns: List[CampaignParameters],
        forecasts: List[ForecastMetrics],
    ) -> Tuple[List[ForecastResult], List[ForecastResult]]:
        """
        Evaluate multiple campaigns and separate winners from failures.

        Args:
            campaigns: List of campaign parameters
            forecasts: List of corresponding forecasts

        Returns:
            Tuple of (winning_campaigns, failed_campaigns)
        """
        logger.info(f"Evaluating {len(campaigns)} campaigns...")

        winners = []
        failures = []

        for campaign, forecast in zip(campaigns, forecasts):
            result = self.evaluate_campaign(campaign, forecast)

            if result.is_winner:
                winners.append(result)
            else:
                failures.append(result)

        # Sort winners by score (descending)
        winners.sort(key=lambda x: x.score, reverse=True)
        failures.sort(key=lambda x: x.score, reverse=True)

        logger.info(
            f"Evaluation complete: {len(winners)} winners, {len(failures)} failures"
        )

        return winners, failures

    def _get_metric_value(self, forecast: ForecastMetrics) -> float:
        """Extract the target metric value from forecast."""
        metric_map = {
            MetricType.ROAS: forecast.predicted_roas,
            MetricType.ROI: forecast.predicted_roi,
            MetricType.CPA: forecast.predicted_cpa,
            MetricType.CTR: forecast.predicted_ctr,
            MetricType.CR: forecast.predicted_cr,
        }

        return metric_map.get(self.goal_metric, 0.0)

    def _check_if_winner(self, metric_value: float) -> bool:
        """
        Check if campaign meets target criteria.

        Args:
            metric_value: Actual metric value

        Returns:
            True if campaign meets or exceeds target (within tolerance)
        """
        # For metrics where lower is better (like CPA)
        if self.goal_metric == MetricType.CPA:
            threshold = self.target_value * (1 + self.tolerance)
            return metric_value <= threshold

        # For metrics where higher is better (ROAS, ROI, CTR, CR)
        threshold = self.target_value * (1 - self.tolerance)
        return metric_value >= threshold

    def _calculate_fitness_score(
        self, forecast: ForecastMetrics, metric_value: float
    ) -> float:
        """
        Calculate overall fitness score for ranking campaigns.

        Combines multiple factors:
        - Primary metric performance
        - ROAS (always important)
        - Confidence level
        - Risk factors

        Args:
            forecast: Forecasted metrics
            metric_value: Primary metric value

        Returns:
            Fitness score (higher is better)
        """
        # Base score from primary metric
        if self.goal_metric == MetricType.CPA:
            # For CPA, lower is better
            metric_score = self.target_value / max(metric_value, 0.01)
        else:
            # For others, higher is better
            metric_score = metric_value / max(self.target_value, 0.01)

        # Weight primary metric heavily
        score = metric_score * 0.6

        # Always consider ROAS (profitability)
        roas_score = min(forecast.predicted_roas / 2.0, 1.0)  # Normalize around 2.0
        score += roas_score * 0.3

        # Consider confidence
        score += forecast.confidence_score * 0.1

        # Penalty for very high CPA (risk management)
        if forecast.predicted_cpa > self.user_constraints.selling_price:
            score *= 0.5  # Heavy penalty for unprofitable campaigns

        return round(score, 4)

    def _generate_notes(
        self, forecast: ForecastMetrics, metric_value: float, is_winner: bool
    ) -> str:
        """Generate evaluation notes and warnings."""
        notes = []

        if is_winner:
            notes.append(f"✓ Meets target {self.goal_metric.value} ({metric_value:.2f})")
        else:
            notes.append(
                f"✗ Below target {self.goal_metric.value} ({metric_value:.2f} vs {self.target_value:.2f})"
            )

        # Add warnings
        if forecast.predicted_cpa > self.user_constraints.selling_price:
            notes.append("⚠️ CPA exceeds selling price (unprofitable)")

        if forecast.predicted_roas < 1.0:
            notes.append("⚠️ ROAS below 1.0 (losing money)")

        if forecast.predicted_ctr < 0.005:
            notes.append("⚠️ Very low CTR (< 0.5%)")

        if forecast.predicted_cr < 0.01:
            notes.append("⚠️ Very low conversion rate (< 1%)")

        if forecast.confidence_score < 0.5:
            notes.append("⚠️ Low confidence in forecast")

        return " | ".join(notes)

    def get_top_campaigns(
        self,
        results: List[ForecastResult],
        n: int = 10,
        winners_only: bool = True,
    ) -> List[ForecastResult]:
        """
        Get top N campaigns by fitness score.

        Args:
            results: List of evaluation results
            n: Number of top campaigns to return
            winners_only: Only return winning campaigns

        Returns:
            Top N campaigns sorted by score
        """
        if winners_only:
            filtered = [r for r in results if r.is_winner]
        else:
            filtered = results

        # Sort by score (descending)
        sorted_results = sorted(filtered, key=lambda x: x.score, reverse=True)

        return sorted_results[:n]

    def analyze_performance_distribution(
        self, results: List[ForecastResult]
    ) -> dict:
        """
        Analyze the distribution of performance metrics.

        Args:
            results: List of evaluation results

        Returns:
            Dictionary with statistical analysis
        """
        if not results:
            return {}

        roas_values = [r.forecast_metrics.predicted_roas for r in results]
        cpa_values = [r.forecast_metrics.predicted_cpa for r in results]
        scores = [r.score for r in results]

        analysis = {
            "total_campaigns": len(results),
            "winners": sum(1 for r in results if r.is_winner),
            "win_rate": sum(1 for r in results if r.is_winner) / len(results),
            "roas": {
                "min": min(roas_values),
                "max": max(roas_values),
                "avg": sum(roas_values) / len(roas_values),
            },
            "cpa": {
                "min": min(cpa_values),
                "max": max(cpa_values),
                "avg": sum(cpa_values) / len(cpa_values),
            },
            "score": {
                "min": min(scores),
                "max": max(scores),
                "avg": sum(scores) / len(scores),
            },
        }

        return analysis

    def compare_against_baseline(
        self, forecast: ForecastMetrics, baseline_data
    ) -> dict:
        """
        Compare forecasted performance against baseline (historical data).

        Args:
            forecast: Forecasted metrics
            baseline_data: Historical baseline data

        Returns:
            Comparison metrics
        """
        comparison = {
            "cpm_change_pct": (
                (forecast.predicted_cpm - baseline_data.cpm) / baseline_data.cpm * 100
            ),
            "ctr_change_pct": (
                (forecast.predicted_ctr - baseline_data.ctr) / baseline_data.ctr * 100
            ),
            "cpc_change_pct": (
                (forecast.predicted_cpc - baseline_data.cpc) / baseline_data.cpc * 100
            ),
            "cr_change_pct": (
                (forecast.predicted_cr - baseline_data.cr) / baseline_data.cr * 100
            ),
        }

        return comparison
