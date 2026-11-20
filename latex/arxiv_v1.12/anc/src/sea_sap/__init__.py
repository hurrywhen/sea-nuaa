"""SEA v1.12 minimal longitudinal SAP executor and synthetic fixtures."""

from .executor import (
    SAPExecutor,
    failure_composite_contrast_bounds,
    load_fixture,
    machine_ingestion_and_task_reference,
    run_longitudinal_fixture,
    run_matched_implementation_demo,
)

__all__ = [
    "SAPExecutor",
    "failure_composite_contrast_bounds",
    "load_fixture",
    "machine_ingestion_and_task_reference",
    "run_longitudinal_fixture",
    "run_matched_implementation_demo",
]
