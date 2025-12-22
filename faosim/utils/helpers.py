"""
Helper utility functions for FAO-Sim system.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


def ensure_dir_exists(directory: str) -> Path:
    """
    Ensure directory exists, create if not.

    Args:
        directory: Directory path

    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data
    """
    with open(file_path, "r") as f:
        return json.load(f)


def save_json(data: Any, file_path: str, indent: int = 2) -> None:
    """
    Save data as JSON file.

    Args:
        data: Data to save
        file_path: Output file path
        indent: JSON indentation
    """
    ensure_dir_exists(Path(file_path).parent)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent, default=str)


def format_currency(amount: float) -> str:
    """Format number as currency."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format decimal as percentage."""
    return f"{value * 100:.2f}%"


def generate_timestamp() -> str:
    """Generate current timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def calculate_metrics_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics from results.

    Args:
        results: List of result dictionaries

    Returns:
        Summary statistics
    """
    if not results:
        return {}

    def safe_avg(values):
        return sum(values) / len(values) if values else 0

    roas_values = [r.get("predicted_roas", 0) for r in results]
    cpa_values = [r.get("predicted_cpa", 0) for r in results]
    ctr_values = [r.get("predicted_ctr", 0) for r in results]

    return {
        "count": len(results),
        "avg_roas": safe_avg(roas_values),
        "max_roas": max(roas_values) if roas_values else 0,
        "min_roas": min(roas_values) if roas_values else 0,
        "avg_cpa": safe_avg(cpa_values),
        "avg_ctr": safe_avg(ctr_values),
    }
