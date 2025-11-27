"""
RRA Utility Functions
=====================

Utility modules for data aggregation and analysis.

Available Modules:
------------------
- rra_aggregator: Multi-form aggregation and portfolio analysis

Usage:
------
    from python_scripts.utils import RRADataAggregator
    aggregator = RRADataAggregator('synthetic_data/')
    summary = aggregator.get_portfolio_summary()
"""

from .rra_aggregator import RRADataAggregator

__all__ = [
    'RRADataAggregator',
]
