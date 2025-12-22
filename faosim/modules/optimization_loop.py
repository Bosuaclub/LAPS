"""
Optimization Loop

Implements the main feedback loop for campaign optimization.
Uses genetic algorithm principles to iteratively improve campaign performance.
"""

import time
from typing import List, Dict, Any, Optional
from loguru import logger

from faosim.core.schemas import (
    UserConstraints,
    CampaignParameters,
    ForecastResult,
    OptimizationResult,
    ParameterSpace,
)
from faosim.modules.campaign_generator import CampaignGenerator
from faosim.modules.forecasting_engine import ForecastingEngine
from faosim.modules.evaluation_engine import EvaluationEngine


class OptimizationLoop:
    """
    Main optimization loop for campaign generation and improvement.

    Implements a genetic algorithm-style optimization:
    1. Generate initial population
    2. Simulate & evaluate
    3. Select best performers
    4. Generate next generation via crossover/mutation
    5. Repeat until convergence or max loops
    """

    def __init__(
        self,
        user_constraints: UserConstraints,
        parameter_space: ParameterSpace,
        forecasting_engine: ForecastingEngine,
        evaluation_engine: EvaluationEngine,
    ):
        """
        Initialize optimization loop.

        Args:
            user_constraints: User-defined constraints and goals
            parameter_space: Available parameter space from RAG
            forecasting_engine: Engine for performance forecasting
            evaluation_engine: Engine for campaign evaluation
        """
        self.user_constraints = user_constraints
        self.parameter_space = parameter_space
        self.forecasting_engine = forecasting_engine
        self.evaluation_engine = evaluation_engine

        # Initialize campaign generator
        self.campaign_generator = CampaignGenerator(
            parameter_space=parameter_space,
            user_constraints=user_constraints,
        )

        # Optimization tracking
        self.convergence_history = []
        self.all_winners = []
        self.all_failures = []

        logger.info("Optimization Loop initialized")

    def run(self) -> OptimizationResult:
        """
        Run the full optimization loop.

        Returns:
            OptimizationResult with winning campaigns and statistics
        """
        logger.info("=" * 60)
        logger.info("Starting Campaign Optimization Loop")
        logger.info("=" * 60)

        start_time = time.time()

        # Generate initial population
        population = self.campaign_generator.generate_initial_population(
            population_size=self.user_constraints.population_size
        )

        best_roas = 0.0
        best_campaign = None
        generations_without_improvement = 0
        early_stop_threshold = 3  # Stop if no improvement for 3 generations

        # Main optimization loop
        for generation in range(self.user_constraints.max_loops):
            logger.info(f"\n{'='*60}")
            logger.info(f"GENERATION {generation + 1}/{self.user_constraints.max_loops}")
            logger.info(f"{'='*60}")

            # Step 1: Forecast performance for all campaigns
            forecasts = self.forecasting_engine.batch_forecast(
                historical_data=self.user_constraints.historical_data,
                campaign_variants=population,
                user_constraints=self.user_constraints,
            )

            # Step 2: Evaluate campaigns
            winners, failures = self.evaluation_engine.evaluate_batch(
                campaigns=population,
                forecasts=forecasts,
            )

            # Track results
            self.all_winners.extend(winners)
            self.all_failures.extend(failures)

            # Step 3: Track best performing campaign
            if winners:
                gen_best = winners[0]
                if gen_best.forecast_metrics.predicted_roas > best_roas:
                    best_roas = gen_best.forecast_metrics.predicted_roas
                    best_campaign = gen_best.campaign_params
                    generations_without_improvement = 0
                    logger.info(
                        f"🎉 New best ROAS: {best_roas:.2f} (Score: {gen_best.score:.4f})"
                    )
                else:
                    generations_without_improvement += 1

                # Log generation statistics
                self._log_generation_stats(generation, winners, failures, gen_best)

            else:
                logger.warning("No winning campaigns in this generation")
                generations_without_improvement += 1

            # Step 4: Record convergence history
            gen_stats = {
                "generation": generation + 1,
                "winners": len(winners),
                "failures": len(failures),
                "best_roas": best_roas,
                "best_score": winners[0].score if winners else 0,
                "avg_roas": (
                    sum(w.forecast_metrics.predicted_roas for w in winners) / len(winners)
                    if winners
                    else 0
                ),
            }
            self.convergence_history.append(gen_stats)

            # Step 5: Check for early stopping
            if generations_without_improvement >= early_stop_threshold:
                logger.info(
                    f"\n⏹️  Early stopping: No improvement for {early_stop_threshold} generations"
                )
                break

            # Step 6: Check if we have enough winners
            if len(winners) >= self.user_constraints.population_size // 2:
                logger.info(
                    f"✓ Strong convergence: {len(winners)} winning campaigns"
                )

            # Step 7: Generate next generation
            if generation < self.user_constraints.max_loops - 1:
                population = self._generate_next_generation(
                    winners=winners,
                    failures=failures,
                    generation=generation + 1,
                )

        # Finalize results
        end_time = time.time()
        execution_time = end_time - start_time

        # Get unique winners (deduplicate)
        unique_winners = self._get_unique_winners(self.all_winners)

        result = OptimizationResult(
            winning_campaigns=unique_winners,
            failed_campaigns=self.all_failures[-100:],  # Keep last 100 failures
            total_loops=len(self.convergence_history),
            best_roas=best_roas,
            best_campaign=best_campaign,
            convergence_history=self.convergence_history,
            execution_time_seconds=round(execution_time, 2),
        )

        self._log_final_summary(result)

        return result

    def _generate_next_generation(
        self,
        winners: List[ForecastResult],
        failures: List[ForecastResult],
        generation: int,
    ) -> List[CampaignParameters]:
        """
        Generate next generation of campaigns.

        Args:
            winners: Winning campaigns from current generation
            failures: Failed campaigns
            generation: Next generation number

        Returns:
            New population for next generation
        """
        logger.info(f"\nGenerating next generation from {len(winners)} winners...")

        if not winners:
            # No winners, generate completely new random population
            logger.warning("No winners available, generating random population")
            return self.campaign_generator.generate_initial_population(
                population_size=self.user_constraints.population_size
            )

        # Extract campaign parameters from winners
        winner_campaigns = [w.campaign_params for w in winners]

        # Select top performers for breeding
        top_count = max(3, len(winner_campaigns) // 2)
        top_performers = winner_campaigns[:top_count]

        # Generate new population
        new_population = self.campaign_generator.generate_from_winners(
            winning_campaigns=top_performers,
            population_size=self.user_constraints.population_size,
            generation=generation,
        )

        return new_population

    def _log_generation_stats(
        self,
        generation: int,
        winners: List[ForecastResult],
        failures: List[ForecastResult],
        best: ForecastResult,
    ) -> None:
        """Log statistics for current generation."""
        logger.info(f"\n📊 Generation {generation + 1} Statistics:")
        logger.info(f"  Winners: {len(winners)}")
        logger.info(f"  Failures: {len(failures)}")
        logger.info(f"  Win Rate: {len(winners) / (len(winners) + len(failures)) * 100:.1f}%")
        logger.info(f"\n🏆 Best Campaign:")
        logger.info(f"  Name: {best.campaign_params.campaign_name}")
        logger.info(f"  ROAS: {best.forecast_metrics.predicted_roas:.2f}")
        logger.info(f"  CPA: ${best.forecast_metrics.predicted_cpa:.2f}")
        logger.info(f"  CTR: {best.forecast_metrics.predicted_ctr * 100:.2f}%")
        logger.info(f"  CR: {best.forecast_metrics.predicted_cr * 100:.2f}%")
        logger.info(f"  Score: {best.score:.4f}")

    def _log_final_summary(self, result: OptimizationResult) -> None:
        """Log final optimization summary."""
        logger.info("\n" + "=" * 60)
        logger.info("OPTIMIZATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"\n⏱️  Execution Time: {result.execution_time_seconds:.2f}s")
        logger.info(f"🔄 Total Generations: {result.total_loops}")
        logger.info(f"✅ Winning Campaigns: {len(result.winning_campaigns)}")
        logger.info(f"❌ Failed Campaigns: {len(result.failed_campaigns)}")
        logger.info(f"\n🎯 Best Performance:")
        logger.info(f"  ROAS: {result.best_roas:.2f}")

        if result.best_campaign:
            logger.info(f"  Campaign: {result.best_campaign.campaign_name}")
            logger.info(f"  Budget: ${result.best_campaign.bidding.daily_budget:.2f}/day")

        logger.info("\n" + "=" * 60)

    def _get_unique_winners(
        self, winners: List[ForecastResult]
    ) -> List[ForecastResult]:
        """
        Get unique winning campaigns (deduplicate by parameters).

        Args:
            winners: All winning campaigns

        Returns:
            Unique winners sorted by score
        """
        # Sort by score
        sorted_winners = sorted(winners, key=lambda x: x.score, reverse=True)

        # Keep top unique campaigns
        unique = []
        seen_configs = set()

        for winner in sorted_winners:
            # Create a simple hash of key parameters
            config_hash = (
                winner.campaign_params.audience.age_min,
                winner.campaign_params.audience.age_max,
                winner.campaign_params.bidding.daily_budget,
                winner.campaign_params.bidding.bid_strategy,
                tuple(winner.campaign_params.placements),
            )

            if config_hash not in seen_configs:
                unique.append(winner)
                seen_configs.add(config_hash)

            # Limit to top 50 unique campaigns
            if len(unique) >= 50:
                break

        return unique

    def get_convergence_plot_data(self) -> Dict[str, List[Any]]:
        """
        Get data for plotting convergence over generations.

        Returns:
            Dictionary with plot data
        """
        generations = [h["generation"] for h in self.convergence_history]
        best_roas = [h["best_roas"] for h in self.convergence_history]
        avg_roas = [h["avg_roas"] for h in self.convergence_history]
        winners = [h["winners"] for h in self.convergence_history]

        return {
            "generations": generations,
            "best_roas": best_roas,
            "avg_roas": avg_roas,
            "winners": winners,
        }
