"""SEA v1.15 minimal longitudinal SAP executor and synthetic fixtures."""

from .executor import (
    SAPExecutor,
    completed_measurement_transport,
    completed_measurement_transport_delta_method,
    failure_composite_contrast_bounds,
    load_fixture,
    machine_ingestion_and_task_reference,
    operational_attendance_contrast_bounds,
    run_longitudinal_fixture,
    run_matched_implementation_demo,
    run_protocol_registry_switch_demo,
)

__all__ = [
    "SAPExecutor",
    "completed_measurement_transport",
    "completed_measurement_transport_delta_method",
    "failure_composite_contrast_bounds",
    "load_fixture",
    "machine_ingestion_and_task_reference",
    "operational_attendance_contrast_bounds",
    "run_longitudinal_fixture",
    "run_matched_implementation_demo",
    "run_protocol_registry_switch_demo",
]
