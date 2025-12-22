"""
CLI Interface for FAO-Sim

Command-line interface for running campaign optimization.
"""

import argparse
import json
import sys
from pathlib import Path
from loguru import logger

from faosim.core.schemas import UserConstraints
from faosim.core.orchestrator import FAOSimOrchestrator


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Set up logging configuration."""
    logger.remove()  # Remove default handler

    # Console handler
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    )

    # File handler
    if log_file:
        logger.add(
            log_file,
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            rotation="10 MB",
        )


def load_user_constraints(config_file: str) -> UserConstraints:
    """Load user constraints from JSON file."""
    with open(config_file, "r") as f:
        data = json.load(f)

    return UserConstraints(**data)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FAO-Sim: FB Ads Autonomous Optimization & Simulation Lab"
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to user constraints JSON configuration file",
    )

    parser.add_argument(
        "--knowledge-base",
        type=str,
        nargs="*",
        help="Paths to knowledge base documents (PDF, DOCX, TXT)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory for results (default: ./output)",
    )

    parser.add_argument(
        "--export-format",
        type=str,
        choices=["json", "csv", "both"],
        default="json",
        help="Export format (default: json)",
    )

    parser.add_argument(
        "--use-existing-kb",
        action="store_true",
        help="Use existing knowledge base if available",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        help="Log file path (optional)",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level, args.log_file)

    try:
        # Load user constraints
        logger.info(f"Loading configuration from {args.config}...")
        user_constraints = load_user_constraints(args.config)

        # Initialize orchestrator
        orchestrator = FAOSimOrchestrator(
            user_constraints=user_constraints,
            knowledge_base_docs=args.knowledge_base,
            use_existing_kb=args.use_existing_kb,
        )

        # Run complete workflow
        if args.export_format == "both":
            result = orchestrator.run_complete_workflow(
                output_dir=args.output_dir,
                export_format="json",
            )
            orchestrator.export_results(result, args.output_dir, "csv")
        else:
            result = orchestrator.run_complete_workflow(
                output_dir=args.output_dir,
                export_format=args.export_format,
            )

        logger.info(f"\n✅ Optimization completed successfully!")
        logger.info(f"📁 Results saved to: {args.output_dir}")
        logger.info(f"🏆 Best ROAS: {result.best_roas:.2f}")
        logger.info(f"✨ Total winning campaigns: {len(result.winning_campaigns)}")

        return 0

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.exception("Full traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
