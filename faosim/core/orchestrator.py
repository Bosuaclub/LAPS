"""
Main Orchestrator

Coordinates all modules to run the complete optimization workflow.
"""

import json
import os
from pathlib import Path
from typing import Optional, List
from loguru import logger

from faosim.core.schemas import (
    UserConstraints,
    OptimizationResult,
    ParameterSpace,
)
from faosim.modules.rag_knowledge_base import RAGKnowledgeBase
from faosim.modules.forecasting_engine import ForecastingEngine
from faosim.modules.evaluation_engine import EvaluationEngine
from faosim.modules.optimization_loop import OptimizationLoop


class FAOSimOrchestrator:
    """
    Main orchestrator for FAO-Sim system.

    Coordinates all modules to run the complete campaign optimization workflow.
    """

    def __init__(
        self,
        user_constraints: UserConstraints,
        knowledge_base_docs: Optional[List[str]] = None,
        use_existing_kb: bool = True,
    ):
        """
        Initialize FAO-Sim orchestrator.

        Args:
            user_constraints: User-defined constraints and goals
            knowledge_base_docs: Paths to knowledge base documents
            use_existing_kb: Use existing knowledge base if available
        """
        self.user_constraints = user_constraints
        self.knowledge_base_docs = knowledge_base_docs or []
        self.use_existing_kb = use_existing_kb

        logger.info("Initializing FAO-Sim Orchestrator...")

        # Initialize modules
        self.rag_kb: Optional[RAGKnowledgeBase] = None
        self.parameter_space: Optional[ParameterSpace] = None
        self.forecasting_engine: Optional[ForecastingEngine] = None
        self.evaluation_engine: Optional[EvaluationEngine] = None
        self.optimization_loop: Optional[OptimizationLoop] = None

    def setup(self) -> None:
        """Set up all modules."""
        logger.info("\n" + "="*60)
        logger.info("SETUP PHASE")
        logger.info("="*60)

        # Step 1: Initialize RAG Knowledge Base
        self._setup_knowledge_base()

        # Step 2: Extract Parameter Space
        self._extract_parameter_space()

        # Step 3: Initialize Forecasting Engine
        self._setup_forecasting_engine()

        # Step 4: Initialize Evaluation Engine
        self._setup_evaluation_engine()

        # Step 5: Initialize Optimization Loop
        self._setup_optimization_loop()

        logger.info("\n✅ All modules initialized successfully\n")

    def _setup_knowledge_base(self) -> None:
        """Initialize and build RAG knowledge base."""
        logger.info("\n📚 Setting up Knowledge Base...")

        self.rag_kb = RAGKnowledgeBase()

        # Check if knowledge base exists
        kb_exists = (
            os.path.exists(self.rag_kb.persist_directory)
            and os.listdir(self.rag_kb.persist_directory)
        )

        if self.use_existing_kb and kb_exists:
            logger.info("Loading existing knowledge base...")
            # Load existing vector store
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import OpenAIEmbeddings

            self.rag_kb.vectorstore = Chroma(
                persist_directory=self.rag_kb.persist_directory,
                embedding_function=OpenAIEmbeddings(),
                collection_name=self.rag_kb.collection_name,
            )
            self.rag_kb.retriever = self.rag_kb.vectorstore.as_retriever()

        elif self.knowledge_base_docs:
            logger.info(f"Building knowledge base from {len(self.knowledge_base_docs)} documents...")
            self.rag_kb.build_knowledge_base(self.knowledge_base_docs)
        else:
            logger.warning("No knowledge base documents provided. Using default parameter space.")

    def _extract_parameter_space(self) -> None:
        """Extract parameter space from knowledge base."""
        logger.info("\n🔍 Extracting Parameter Space...")

        if self.rag_kb and self.rag_kb.vectorstore:
            self.parameter_space = self.rag_kb.extract_parameter_space()
            logger.info(f"Extracted parameter space:")
            logger.info(f"  - {len(self.parameter_space.targeting_strategies)} targeting strategies")
            logger.info(f"  - {len(self.parameter_space.creative_formats)} creative formats")
            logger.info(f"  - {len(self.parameter_space.bidding_strategies)} bidding strategies")
            logger.info(f"  - {len(self.parameter_space.placement_combinations)} placement combinations")
        else:
            logger.warning("Using default parameter space")
            self.parameter_space = ParameterSpace()

    def _setup_forecasting_engine(self) -> None:
        """Initialize forecasting engine."""
        logger.info("\n📈 Setting up Forecasting Engine...")
        self.forecasting_engine = ForecastingEngine()

    def _setup_evaluation_engine(self) -> None:
        """Initialize evaluation engine."""
        logger.info("\n⚖️  Setting up Evaluation Engine...")
        self.evaluation_engine = EvaluationEngine(self.user_constraints)

    def _setup_optimization_loop(self) -> None:
        """Initialize optimization loop."""
        logger.info("\n🔄 Setting up Optimization Loop...")
        self.optimization_loop = OptimizationLoop(
            user_constraints=self.user_constraints,
            parameter_space=self.parameter_space,
            forecasting_engine=self.forecasting_engine,
            evaluation_engine=self.evaluation_engine,
        )

    def run_optimization(self) -> OptimizationResult:
        """
        Run the complete optimization workflow.

        Returns:
            OptimizationResult with winning campaigns
        """
        if not self.optimization_loop:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")

        logger.info("\n" + "="*60)
        logger.info("STARTING OPTIMIZATION")
        logger.info("="*60)

        # Run optimization loop
        result = self.optimization_loop.run()

        return result

    def export_results(
        self,
        result: OptimizationResult,
        output_dir: str = "./output",
        format: str = "json",
    ) -> None:
        """
        Export optimization results to files.

        Args:
            result: Optimization result to export
            output_dir: Output directory
            format: Export format (json, csv)
        """
        logger.info(f"\n💾 Exporting results to {output_dir}...")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if format == "json":
            self._export_json(result, output_path)
        elif format == "csv":
            self._export_csv(result, output_path)
        else:
            logger.warning(f"Unsupported format: {format}")

        logger.info("✅ Export complete")

    def _export_json(self, result: OptimizationResult, output_path: Path) -> None:
        """Export results as JSON."""
        # Export full results
        results_file = output_path / "optimization_results.json"
        with open(results_file, "w") as f:
            json.dump(result.model_dump(), f, indent=2, default=str)
        logger.info(f"  ✓ Full results: {results_file}")

        # Export winning campaigns only
        winners_file = output_path / "winning_campaigns.json"
        winners_data = [
            {
                "campaign_id": w.campaign_params.campaign_id,
                "campaign_name": w.campaign_params.campaign_name,
                "audience": w.campaign_params.audience.model_dump(),
                "creative": w.campaign_params.creative.model_dump(),
                "bidding": w.campaign_params.bidding.model_dump(),
                "placements": w.campaign_params.placements,
                "forecast": {
                    "predicted_roas": w.forecast_metrics.predicted_roas,
                    "predicted_cpa": w.forecast_metrics.predicted_cpa,
                    "predicted_ctr": w.forecast_metrics.predicted_ctr,
                    "predicted_cr": w.forecast_metrics.predicted_cr,
                },
                "score": w.score,
            }
            for w in result.winning_campaigns
        ]

        with open(winners_file, "w") as f:
            json.dump(winners_data, f, indent=2)
        logger.info(f"  ✓ Winning campaigns: {winners_file}")

        # Export convergence history
        convergence_file = output_path / "convergence_history.json"
        with open(convergence_file, "w") as f:
            json.dump(result.convergence_history, f, indent=2)
        logger.info(f"  ✓ Convergence history: {convergence_file}")

    def _export_csv(self, result: OptimizationResult, output_path: Path) -> None:
        """Export results as CSV."""
        import pandas as pd

        # Export winning campaigns as CSV
        winners_data = []
        for w in result.winning_campaigns:
            winners_data.append({
                "campaign_id": w.campaign_params.campaign_id,
                "campaign_name": w.campaign_params.campaign_name,
                "age_min": w.campaign_params.audience.age_min,
                "age_max": w.campaign_params.audience.age_max,
                "genders": ",".join(w.campaign_params.audience.genders),
                "locations": ",".join(w.campaign_params.audience.locations),
                "creative_format": w.campaign_params.creative.format,
                "cta": w.campaign_params.creative.call_to_action,
                "daily_budget": w.campaign_params.bidding.daily_budget,
                "bid_strategy": w.campaign_params.bidding.bid_strategy,
                "placements": ",".join(w.campaign_params.placements),
                "predicted_roas": w.forecast_metrics.predicted_roas,
                "predicted_cpa": w.forecast_metrics.predicted_cpa,
                "predicted_ctr": w.forecast_metrics.predicted_ctr,
                "predicted_cr": w.forecast_metrics.predicted_cr,
                "score": w.score,
            })

        df = pd.DataFrame(winners_data)
        csv_file = output_path / "winning_campaigns.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"  ✓ CSV export: {csv_file}")

    def run_complete_workflow(
        self,
        output_dir: str = "./output",
        export_format: str = "json",
    ) -> OptimizationResult:
        """
        Run complete workflow: setup, optimize, and export.

        Args:
            output_dir: Directory for output files
            export_format: Export format (json, csv)

        Returns:
            OptimizationResult
        """
        # Setup
        self.setup()

        # Run optimization
        result = self.run_optimization()

        # Export results
        self.export_results(result, output_dir, export_format)

        return result
