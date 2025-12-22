"""
Quick Start Example for FAO-Sim

This script demonstrates how to use FAO-Sim programmatically.
"""

import os
from dotenv import load_dotenv

from faosim.core.schemas import (
    UserConstraints,
    HistoricalData,
    Goal,
)
from faosim.core.orchestrator import FAOSimOrchestrator

# Load environment variables
load_dotenv()


def main():
    """Run a quick optimization example."""

    # Define historical data
    historical_data = HistoricalData(
        cpm=15.0,
        ctr=0.02,
        cpc=0.75,
        cr=0.03,
        daily_budget=100.0,
        impressions=10000,
        clicks=200,
        conversions=6,
    )

    # Define optimization goal
    goal = Goal(
        metric="ROAS",
        target_value=2.5,
        tolerance=0.1,
    )

    # Define user constraints
    user_constraints = UserConstraints(
        product_cost=100.0,
        selling_price=300.0,
        historical_data=historical_data,
        goal=goal,
        max_loops=5,  # Quick test with 5 generations
        population_size=10,  # Smaller population for quick test
        min_daily_budget=50.0,
        max_daily_budget=500.0,
    )

    # Initialize orchestrator
    print("🚀 Initializing FAO-Sim...")
    orchestrator = FAOSimOrchestrator(
        user_constraints=user_constraints,
        knowledge_base_docs=["examples/fb_ads_guide.txt"],
        use_existing_kb=False,
    )

    # Run optimization
    print("\n🎯 Starting optimization...\n")
    result = orchestrator.run_complete_workflow(
        output_dir="./output",
        export_format="both",
    )

    # Print summary
    print("\n" + "="*60)
    print("OPTIMIZATION SUMMARY")
    print("="*60)
    print(f"Best ROAS: {result.best_roas:.2f}")
    print(f"Winning Campaigns: {len(result.winning_campaigns)}")
    print(f"Total Generations: {result.total_loops}")
    print(f"Execution Time: {result.execution_time_seconds:.2f}s")

    if result.best_campaign:
        print(f"\nBest Campaign: {result.best_campaign.campaign_name}")
        print(f"Daily Budget: ${result.best_campaign.bidding.daily_budget:.2f}")

    print("\n📁 Results saved to ./output/")
    print("="*60)


if __name__ == "__main__":
    main()
