"""
FAO-Sim: FB Ads Autonomous Optimization & Simulation Lab

An AI-powered system for automated Facebook Ads campaign creation,
simulation, and optimization using RAG and TimesFM forecasting.
"""

__version__ = "0.1.0"
__author__ = "FAO-Sim Team"

from faosim.core.schemas import (
    HistoricalData,
    Goal,
    UserConstraints,
    CampaignParameters,
    ForecastResult,
    OptimizationResult,
)

__all__ = [
    "HistoricalData",
    "Goal",
    "UserConstraints",
    "CampaignParameters",
    "ForecastResult",
    "OptimizationResult",
]
