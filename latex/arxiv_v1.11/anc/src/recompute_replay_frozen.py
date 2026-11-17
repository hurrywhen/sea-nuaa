#!/usr/bin/env python3
"""Controlled four-family unique-key reanalysis of the frozen replay snapshot.

The only replay outcomes read are the 292 top-level ``llm_replay_*.jsonl``
shards accepted by :func:`audit_replay_integrity.load_runs`.  The fixed replay
corpus is read solely to construct scenario J's all-corpus daily value ceiling.
No replay shard, legacy analysis, integrity audit, three-family artifact, or
manuscript is modified.

Default behavior is stdout only.  ``--write`` emits the independent artifact
set under ``sim/pilot/results/frozen_reanalysis_v1/``; replacement of any target
requires ``--force`` as well.

Run from the repository root::

    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/recompute_replay_frozen.py

Dependencies: Python >= 3.10 and NumPy.  The result status is always
CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY.  This is not a
prospective preregistration or a cross-corpus confirmatory analysis.
"""
from __future__ import annotations

import argparse
import collections
import csv
import dataclasses
import functools
import gzip
import hashlib
import io
import json
import math
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

import numpy as np

try:  # Support both ``python -m sea_pilot...`` and direct script execution.
    from . import corpus as cp
    from .analyze_families import mcnemar_exact as _mcnemar_exact
    from .audit_replay_integrity import (
        EXPECTED_RUNS,
        FAMILY_ORDER,
        TAG_RE,
        is_valid,
        load_runs,
    )
except ImportError:  # pragma: no cover - exercised by the CLI, not unit imports
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sea_pilot import corpus as cp
    from sea_pilot.analyze_families import mcnemar_exact as _mcnemar_exact
    from sea_pilot.audit_replay_integrity import (
        EXPECTED_RUNS,
        FAMILY_ORDER,
        TAG_RE,
        is_valid,
        load_runs,
    )

VERSION = "1.0.0"
SCHEMA = "sea.controlled_unique_key_reanalysis/v1"
STATUS = "CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY"
LEGACY_STATUS = "LEGACY_EXPLORATORY_NOT_DEDUPLICATED"
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = ROOT / "sim" / "pilot" / "results"
DEFAULT_OUTPUT_DIR = DEFAULT_RESULTS_DIR / "frozen_reanalysis_v1"
SPEC_PATH = ROOT / "docs" / "主验证唯一键处置与重分析规约.md"
NOMINAL_PER_RUN = 900
NOMINAL_TOTAL = 72000
EXPECTED_SHARDS = 292
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 42
SIGN_FLIP_N = 100000
SIGN_FLIP_SEED = 42
HONEST_DESCRIPTION_REFERENCE = 0.241
PARAM_FIELDS = ("hits_param", "n_crit", "value_param")
FIVE_FIELDS = ("hits_llm", "hits_param", "n_crit", "value_llm", "value_param")
SIX_FIELDS = FIVE_FIELDS + ("picked",)
METRICS = ("recall_llm", "recall_param", "delta_recall", "delta_value")
EXPECTED_STRUCTURE = {
    "expected_keys": 72000,
    "valid_unique_keys": 71914,
    "empty_only_keys": 56,
    "no_surviving_row_keys": 30,
    "empty_records_on_valid_keys": 101,
    "raw_rows": 73704,
    "valid_records": 73547,
    "recall_conflicts_A": 341,
    "value_conflicts_A": 1238,
    "sign_conflicts_A": 296,
    "resolved_recall_A": 71573,
    "resolved_value_A": 70676,
    "resolved_sign_A": 71618,
    "resolved_B": 70676,
    "resolved_C": 70306,
    "resolved_D": 70525,
    "resolved_E": 71914,
}

# ``id`` is used in JSON/CSV; ``rule`` preserves the specification's labels.
SCENARIOS: tuple[dict[str, str], ...] = (
    {"id": "A", "family": "A", "rule": "metric_resolved"},
    {"id": "B", "family": "B", "rule": "common_cohort"},
    {"id": "C", "family": "C", "rule": "strict_singleton"},
    {"id": "D", "family": "D", "rule": "audit_six_consistent"},
    {"id": "E", "family": "E", "rule": "attempt_mean"},
    *({"id": f"F{i:02d}", "family": "F", "rule": f"hash_salt{i:02d}",
       "salt": f"salt{i:02d}"} for i in range(5)),
    {"id": "G", "family": "G", "rule": "empty_only_zero"},
    {"id": "H", "family": "H", "rule": "all_gap_zero"},
    {"id": "I_favor_param", "family": "I", "rule": "favor_param"},
    {"id": "I_favor_llm", "family": "I", "rule": "favor_llm"},
    {"id": "I_unresolved_tie", "family": "I", "rule": "unresolved_tie"},
    {"id": "J_lower_value", "family": "J", "rule": "lower_value"},
    {"id": "J_upper_value", "family": "J", "rule": "upper_value"},
)
SCENARIO_BY_ID = {item["id"]: item for item in SCENARIOS}
ARTIFACT_NAMES = (
    "summary.json",
    "REPORT.md",
    "run_metrics.csv",
    "key_ledger.jsonl.gz",
    "input_manifest.json",
    "SPECIFICATION.md",
    "environment.json",
)


@dataclass(frozen=True, slots=True)
class CanonicalDay:
    hits_param: int
    n_crit: int
    value_param: float


@dataclass(frozen=True, slots=True)
class Cell:
    """One key under one scenario; recall/value/sign cohorts may differ."""

    recall: tuple[float, float, float] | None  # hits_llm, hits_param, n_crit
    delta_value: float | None
    sign: int | None
    recall_status: str
    value_status: str
    sign_status: str


@dataclass(slots=True)
class KeyState:
    family: str
    run: int
    agent: int
    sim_day: int
    n_rows: int
    n_empty: int
    records: list[dict[str, Any]]  # nonempty-picked attempts only
    provenance: list[tuple[str, int, bool]]
    canonical: CanonicalDay
    value_upper: float
    recall: tuple[float, float, float] | None
    delta_value: float | None
    sign: int | None
    common: Cell | None
    audit_six: Cell | None
    attempt_mean: Cell | None
    hash_cells: dict[str, Cell]
    hash_meta: dict[str, dict[str, Any]]

    @property
    def gap(self) -> str | None:
        if self.records:
            return None
        return "EMPTY_ONLY" if self.n_rows else "NO_SURVIVING_ROW"

    @property
    def valid_unique(self) -> bool:
        return bool(self.records)


def _json_value(value: Any) -> str:
    """Type-preserving JSON equality, matching the integrity audit's semantics."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return _sha256_bytes(data)


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric, got {value!r}")
    answer = float(value)
    if not math.isfinite(answer):
        raise ValueError(f"{label} must be finite, got {value!r}")
    return answer


def _integer_field(record: dict[str, Any], field: str, label: str) -> int:
    value = _finite_number(record.get(field), f"{label}.{field}")
    if not value.is_integer():
        raise ValueError(f"{label}.{field} must be an integer, got {value!r}")
    answer = int(value)
    if answer < 0:
        raise ValueError(f"{label}.{field} must be nonnegative")
    return answer


def _validate_valid_record(record: dict[str, Any], label: str) -> None:
    hl = _integer_field(record, "hits_llm", label)
    hp = _integer_field(record, "hits_param", label)
    nc = _integer_field(record, "n_crit", label)
    vl = _finite_number(record.get("value_llm"), f"{label}.value_llm")
    vp = _finite_number(record.get("value_param"), f"{label}.value_param")
    if hl > nc or hp > nc:
        raise ValueError(f"{label}: hits exceed n_crit ({hl=}, {hp=}, {nc=})")
    if vl < 0 or vp < 0:
        raise ValueError(f"{label}: values must be nonnegative")


def canonical_daily_parameters(
    runs: dict[tuple[str, int], list[dict[str, Any]]],
) -> dict[tuple[str, int, int], CanonicalDay]:
    """Recover one parameter triple per run/day, or fail on any nonuniqueness.

    All rows, including empty-picked rows, participate.  No valid/empty, line,
    day, mtime, reason, or outcome-based arbitration is permitted here.
    """
    answer: dict[tuple[str, int, int], CanonicalDay] = {}
    for (family, run), records in sorted(runs.items()):
        by_day: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
        for record in records:
            day = record.get("sim_day")
            if isinstance(day, bool) or not isinstance(day, int) or not 0 <= day < 30:
                raise ValueError(f"Invalid sim_day in {family}/run {run}: {day!r}")
            by_day[day].append(record)
        if set(by_day) != set(range(30)):
            missing = sorted(set(range(30)) - set(by_day))
            raise ValueError(f"Cannot recover canonical parameters for {family}/run {run}; "
                             f"days without any record: {missing}")
        for day in range(30):
            group = by_day[day]
            values: dict[str, Any] = {}
            for field in PARAM_FIELDS:
                unique = {_json_value(record.get(field)) for record in group}
                if len(unique) != 1:
                    locations = [f"{r.get('_source_file')}:{r.get('_source_line')}"
                                 for r in group]
                    raise ValueError(
                        f"Non-unique daily parameter {field} at {family}/run {run}/day {day}; "
                        f"refusing arbitration; locations={locations}"
                    )
                values[field] = group[0].get(field)
            label = f"canonical {family}/run {run}/day {day}"
            hp = _integer_field(values, "hits_param", label)
            nc = _integer_field(values, "n_crit", label)
            vp = _finite_number(values["value_param"], f"{label}.value_param")
            if hp > nc or vp < 0:
                raise ValueError(f"Invalid canonical parameter triple at {label}")
            answer[(family, run, day)] = CanonicalDay(hp, nc, vp)
    return answer


def daily_value_upper(universe: Sequence[dict[str, Any]]) -> dict[int, float]:
    """Top three log1p(cit) values over *all* papers on each simulation day."""
    by_day: dict[int, list[float]] = collections.defaultdict(list)
    for record in universe:
        day = cp.day_index(record)
        cit = _finite_number(record.get("cit"), f"corpus {record.get('arxiv_id')}.cit")
        if cit < 0:
            raise ValueError("Citation counts must be nonnegative")
        by_day[day].append(math.log1p(cit))
    if set(by_day) != set(range(30)):
        raise ValueError(f"Expected all 30 corpus days, got {sorted(by_day)}")
    return {day: math.fsum(sorted(by_day[day], reverse=True)[:3]) for day in range(30)}


def _consistent(records: Sequence[dict[str, Any]], function: Callable[[dict[str, Any]], Any]) -> Any | None:
    if not records:
        return None
    first = function(records[0])
    return first if all(function(record) == first for record in records[1:]) else None


def _fields_consistent(records: Sequence[dict[str, Any]], fields: Sequence[str]) -> bool:
    signatures = {_json_value([record.get(field) for field in fields]) for record in records}
    return len(signatures) == 1


def selection_hash(salt: str, family: str, run: int, agent: int, sim_day: int,
                   source_file: str, source_line: int) -> str:
    """Outcome-blind F hash; its byte string contains only frozen provenance."""
    material = (f"SEA-80run-dedup-v1\0{salt}{family}/{run}/{agent}/{sim_day}/"
                f"{source_file}/{source_line}").encode("utf-8")
    return _sha256_bytes(material)


def _cell_from_record(record: dict[str, Any], canonical: CanonicalDay,
                      recall_status: str, value_status: str | None = None,
                      sign_status: str | None = None) -> Cell:
    hl = float(record["hits_llm"])
    hp = float(canonical.hits_param)
    nc = float(canonical.n_crit)
    dv = float(record["value_llm"]) - float(record["value_param"])
    sign = (hl > hp) - (hl < hp)
    return Cell((hl, hp, nc), dv, sign, recall_status,
                value_status or recall_status, sign_status or recall_status)


def _build_common_cell(records: list[dict[str, Any]], canonical: CanonicalDay,
                       fields: Sequence[str], label: str) -> Cell | None:
    if not records or not _fields_consistent(records, fields):
        return None
    return _cell_from_record(records[0], canonical, label)


def _attempt_mean_cell(records: list[dict[str, Any]], canonical: CanonicalDay) -> Cell | None:
    if not records:
        return None
    n = len(records)
    hl = math.fsum(float(record["hits_llm"]) for record in records) / n
    # Per-attempt mean of (value_llm-value_param), not a mean of selected keys.
    dv = math.fsum(float(record["value_llm"]) - float(record["value_param"])
                   for record in records) / n
    return Cell((hl, float(canonical.hits_param), float(canonical.n_crit)),
                dv, None, "ATTEMPT_MEAN", "ATTEMPT_MEAN", "NOT_APPLICABLE_FRACTIONAL")


def build_key_states(
    runs: dict[tuple[str, int], list[dict[str, Any]]],
    canonical: dict[tuple[str, int, int], CanonicalDay],
    value_upper: dict[int, float],
) -> list[KeyState]:
    """Materialize the complete 80 x 30 x 30 grid without copying first/last rows."""
    states: list[KeyState] = []
    for family in FAMILY_ORDER:
        for run in sorted(EXPECTED_RUNS[family]):
            records = runs[(family, run)]
            grouped: dict[tuple[int, int], list[dict[str, Any]]] = collections.defaultdict(list)
            for record in records:
                agent, day = record.get("agent"), record.get("sim_day")
                if (isinstance(agent, bool) or not isinstance(agent, int)
                        or not 0 <= agent < 30 or not 0 <= day < 30):
                    raise ValueError(f"Out-of-grid key at {family}/run {run}: {(agent, day)!r}")
                grouped[(agent, day)].append(record)
            for agent in range(30):
                for day in range(30):
                    rows = grouped.get((agent, day), [])
                    valid = [record for record in rows if is_valid(record)]
                    for record in valid:
                        _validate_valid_record(
                            record, f"{record.get('_source_file')}:{record.get('_source_line')}")
                    day_parameters = canonical[(family, run, day)]
                    recall_pair = _consistent(
                        valid, lambda r: (r["hits_llm"], r["n_crit"])) if valid else None
                    recall = ((float(recall_pair[0]), float(day_parameters.hits_param),
                               float(day_parameters.n_crit))) if recall_pair is not None else None
                    delta_value = _consistent(
                        valid, lambda r: float(r["value_llm"]) - float(r["value_param"])
                    ) if valid else None
                    sign = _consistent(
                        valid, lambda r: ((r["hits_llm"] > r["hits_param"])
                                          - (r["hits_llm"] < r["hits_param"]))
                    ) if valid else None
                    common = _build_common_cell(valid, day_parameters, FIVE_FIELDS, "COMMON_COHORT")
                    audit_six = _build_common_cell(valid, day_parameters, SIX_FIELDS,
                                                   "AUDIT_SIX_CONSISTENT")
                    attempt_mean = _attempt_mean_cell(valid, day_parameters)
                    hash_cells: dict[str, Cell] = {}
                    hash_meta: dict[str, dict[str, Any]] = {}
                    for scenario in SCENARIOS:
                        if scenario["family"] != "F" or not valid:
                            continue
                        salt = scenario["salt"]
                        ranked: list[tuple[str, dict[str, Any]]] = []
                        for record in valid:
                            digest = selection_hash(
                                salt, family, run, agent, day,
                                record["_source_file"], int(record["_source_line"]))
                            ranked.append((digest, record))
                        ranked.sort(key=lambda item: item[0])
                        if len(ranked) > 1 and ranked[0][0] == ranked[1][0]:
                            raise ValueError(f"Cryptographic hash tie at {family}/{run}/{agent}/{day}")
                        digest, selected = ranked[0]
                        sid = scenario["id"]
                        hash_cells[sid] = _cell_from_record(selected, day_parameters, "HASH_SELECTED")
                        hash_meta[sid] = {
                            "sha256": digest,
                            "source_file": selected["_source_file"],
                            "source_line": int(selected["_source_line"]),
                        }
                    states.append(KeyState(
                        family=family, run=run, agent=agent, sim_day=day,
                        n_rows=len(rows), n_empty=len(rows) - len(valid), records=valid,
                        provenance=[(r["_source_file"], int(r["_source_line"]), is_valid(r))
                                    for r in rows],
                        canonical=day_parameters, value_upper=value_upper[day],
                        recall=recall, delta_value=delta_value, sign=sign,
                        common=common, audit_six=audit_six, attempt_mean=attempt_mean,
                        hash_cells=hash_cells, hash_meta=hash_meta,
                    ))
    if len(states) != NOMINAL_TOTAL:
        raise AssertionError(f"Expected {NOMINAL_TOTAL} states, got {len(states)}")
    return states


def _gap_cell(state: KeyState) -> Cell:
    gap = state.gap
    assert gap is not None
    return Cell(None, None, None, gap, gap, gap)


def scenario_cell(state: KeyState, scenario_id: str) -> Cell:
    """Apply one frozen scenario to one key; no source-row order is consulted."""
    scenario = SCENARIO_BY_ID[scenario_id]
    family = scenario["family"]
    rule = scenario["rule"]
    if family == "A":
        if not state.valid_unique:
            return _gap_cell(state)
        return Cell(state.recall, state.delta_value, state.sign,
                    "RESOLVED" if state.recall is not None else "UNRESOLVED_CONFLICT",
                    "RESOLVED" if state.delta_value is not None else "UNRESOLVED_CONFLICT",
                    "RESOLVED" if state.sign is not None else "UNRESOLVED_CONFLICT")
    if family == "B":
        return state.common or _gap_or_conflict(state, "FIVE_FIELD_CONFLICT")
    if family == "C":
        if not state.valid_unique:
            return _gap_cell(state)
        if len(state.records) != 1:
            conflict = Cell(None, None, None, "NOT_STRICT_SINGLETON",
                            "NOT_STRICT_SINGLETON", "NOT_STRICT_SINGLETON")
            return conflict
        return _cell_from_record(state.records[0], state.canonical, "STRICT_SINGLETON")
    if family == "D":
        return state.audit_six or _gap_or_conflict(state, "AUDIT_SIX_CONFLICT")
    if family == "E":
        return state.attempt_mean or _gap_cell(state)
    if family == "F":
        return state.hash_cells.get(scenario_id) or _gap_cell(state)
    if family in {"G", "H"}:
        base = scenario_cell(state, "A")
        is_gap = not state.valid_unique
        fill = is_gap and (family == "H" or state.gap == "EMPTY_ONLY")
        if not fill:
            return base
        hp = float(state.canonical.hits_param)
        nc = float(state.canonical.n_crit)
        zero_sign = (0.0 > hp) - (0.0 < hp)
        gap_status = "EMPTY_ONLY_ZERO" if state.gap == "EMPTY_ONLY" else "NO_SURVIVING_ROW_ZERO"
        return Cell((0.0, hp, nc), -float(state.canonical.value_param), zero_sign,
                    gap_status, gap_status, gap_status)
    if family in {"I", "J"}:
        # I's directional assignments and J's partial-identification endpoints
        # deliberately share the same protocol-extreme numeric assignments.
        # I adds the unresolved-tie sign/value scenario; J names the two endpoints.
        if family == "I":
            mode = rule
        else:
            mode = "favor_param" if rule == "lower_value" else "favor_llm"
        prefix = "A_RESOLVED"
        imputed = f"{family}_{rule.upper()}"
        if state.recall is not None:
            recall = state.recall
            recall_status = prefix
        else:
            hp = float(state.canonical.hits_param)
            nc = float(state.canonical.n_crit)
            hl = 0.0 if mode == "favor_param" else nc if mode == "favor_llm" else hp
            recall = (hl, hp, nc)
            recall_status = imputed
        if state.delta_value is not None:
            delta_value = state.delta_value
            value_status = prefix
        else:
            if mode == "favor_param":
                delta_value = -float(state.canonical.value_param)
            elif mode == "favor_llm":
                delta_value = state.value_upper - float(state.canonical.value_param)
            else:
                delta_value = 0.0
            value_status = imputed
        if state.sign is not None:
            sign = state.sign
            sign_status = prefix
        else:
            assert recall is not None
            sign = (recall[0] > recall[1]) - (recall[0] < recall[1])
            sign_status = imputed
        return Cell(recall, delta_value, sign, recall_status, value_status, sign_status)
    raise AssertionError(f"Unknown scenario {scenario_id}")


def _gap_or_conflict(state: KeyState, conflict_status: str) -> Cell:
    if not state.valid_unique:
        return _gap_cell(state)
    return Cell(None, None, None, conflict_status, conflict_status, conflict_status)


def structure_counts(states: Sequence[KeyState]) -> dict[str, Any]:
    valid = [state for state in states if state.valid_unique]
    counts: dict[str, Any] = {
        "expected_keys": len(states),
        "valid_unique_keys": len(valid),
        "empty_only_keys": sum(state.gap == "EMPTY_ONLY" for state in states),
        "no_surviving_row_keys": sum(state.gap == "NO_SURVIVING_ROW" for state in states),
        "empty_records_on_valid_keys": sum(state.n_empty for state in valid),
        "raw_rows": sum(state.n_rows for state in states),
        "valid_records": sum(len(state.records) for state in states),
        "empty_records": sum(state.n_empty for state in states),
        "duplicate_excess_records": sum(len(state.records) - 1 for state in valid),
        "recall_conflicts_A": sum(state.valid_unique and state.recall is None for state in states),
        "value_conflicts_A": sum(state.valid_unique and state.delta_value is None for state in states),
        "sign_conflicts_A": sum(state.valid_unique and state.sign is None for state in states),
        "resolved_recall_A": sum(state.recall is not None for state in states),
        "resolved_value_A": sum(state.delta_value is not None for state in states),
        "resolved_sign_A": sum(state.sign is not None for state in states),
        "resolved_B": sum(state.common is not None for state in states),
        "resolved_C": sum(len(state.records) == 1 for state in states),
        "resolved_D": sum(state.audit_six is not None for state in states),
        "resolved_E": sum(state.attempt_mean is not None for state in states),
        "resolved_each_F": len(valid),
    }
    by_family: dict[str, Any] = {}
    for family in FAMILY_ORDER:
        subset = [state for state in states if state.family == family]
        by_family[family] = {
            "expected_keys": len(subset),
            "valid_unique_keys": sum(state.valid_unique for state in subset),
            "empty_only_keys": sum(state.gap == "EMPTY_ONLY" for state in subset),
            "no_surviving_row_keys": sum(state.gap == "NO_SURVIVING_ROW" for state in subset),
            "recall_conflicts_A": sum(state.valid_unique and state.recall is None for state in subset),
            "value_conflicts_A": sum(state.valid_unique and state.delta_value is None for state in subset),
            "sign_conflicts_A": sum(state.valid_unique and state.sign is None for state in subset),
            "resolved_recall_A": sum(state.recall is not None for state in subset),
            "resolved_value_A": sum(state.delta_value is not None for state in subset),
            "resolved_sign_A": sum(state.sign is not None for state in subset),
        }
    counts["by_family"] = by_family
    return counts


def validate_structure(counts: dict[str, Any]) -> None:
    failures = {key: {"expected": expected, "observed": counts.get(key)}
                for key, expected in EXPECTED_STRUCTURE.items() if counts.get(key) != expected}
    if failures:
        raise ValueError(f"Frozen structural expectations failed: {failures}")
    if counts["empty_only_keys"] + counts["no_surviving_row_keys"] != 86:
        raise AssertionError("The two gap classes must sum to 86")
    if counts["valid_unique_keys"] + 86 != NOMINAL_TOTAL:
        raise AssertionError("Valid unique keys plus gaps must equal 72,000")


RUN_COLUMNS = (
    "scenario", "rule", "family", "run", "expected_keys", "raw_rows", "valid_records",
    "valid_unique_keys", "empty_only_keys", "no_surviving_row_keys",
    "empty_records_on_valid_keys", "n_resolved_recall", "n_resolved_value", "n_resolved_sign",
    "coverage_recall", "coverage_value", "coverage_sign",
    "conflict_recall_A", "conflict_value_A", "conflict_sign_A",
    "excluded_valid_recall", "excluded_valid_value", "excluded_valid_sign",
    "sum_hits_llm", "sum_hits_param", "sum_n_crit", "sum_delta_value",
    "recall_llm", "recall_param", "delta_recall", "delta_value",
    "mcnemar_b", "mcnemar_c", "mcnemar_tie",
)


def compute_run_row(state_group: Sequence[KeyState], scenario_id: str) -> dict[str, Any]:
    if not state_group:
        raise ValueError("Empty run")
    scenario = SCENARIO_BY_ID[scenario_id]
    family, run = state_group[0].family, state_group[0].run
    recall_values: list[tuple[float, float, float]] = []
    deltas: list[float] = []
    signs: list[int] = []
    excluded = {"recall": 0, "value": 0, "sign": 0}
    for state in state_group:
        cell = scenario_cell(state, scenario_id)
        if cell.recall is not None:
            recall_values.append(cell.recall)
        elif state.valid_unique:
            excluded["recall"] += 1
        if cell.delta_value is not None:
            deltas.append(cell.delta_value)
        elif state.valid_unique:
            excluded["value"] += 1
        if cell.sign is not None:
            signs.append(cell.sign)
        elif state.valid_unique and scenario["family"] != "E":
            excluded["sign"] += 1
    sum_hl = math.fsum(item[0] for item in recall_values)
    sum_hp = math.fsum(item[1] for item in recall_values)
    sum_nc = math.fsum(item[2] for item in recall_values)
    rllm = sum_hl / sum_nc if sum_nc else None
    rparam = sum_hp / sum_nc if sum_nc else None
    dr = rllm - rparam if rllm is not None and rparam is not None else None
    sum_dv = math.fsum(deltas)
    dv = sum_dv / len(deltas) if deltas else None
    sign_applicable = scenario["family"] != "E"
    b = sum(sign > 0 for sign in signs) if sign_applicable else None
    c = sum(sign < 0 for sign in signs) if sign_applicable else None
    tie = sum(sign == 0 for sign in signs) if sign_applicable else None
    valid = [state for state in state_group if state.valid_unique]
    row: dict[str, Any] = {
        "scenario": scenario_id,
        "rule": scenario["rule"],
        "family": family,
        "run": run,
        "expected_keys": len(state_group),
        "raw_rows": sum(state.n_rows for state in state_group),
        "valid_records": sum(len(state.records) for state in state_group),
        "valid_unique_keys": len(valid),
        "empty_only_keys": sum(state.gap == "EMPTY_ONLY" for state in state_group),
        "no_surviving_row_keys": sum(state.gap == "NO_SURVIVING_ROW" for state in state_group),
        "empty_records_on_valid_keys": sum(state.n_empty for state in valid),
        "n_resolved_recall": len(recall_values),
        "n_resolved_value": len(deltas),
        "n_resolved_sign": len(signs) if sign_applicable else None,
        "coverage_recall": len(recall_values) / len(state_group),
        "coverage_value": len(deltas) / len(state_group),
        "coverage_sign": len(signs) / len(state_group) if sign_applicable else None,
        "conflict_recall_A": sum(state.valid_unique and state.recall is None for state in state_group),
        "conflict_value_A": sum(state.valid_unique and state.delta_value is None for state in state_group),
        "conflict_sign_A": sum(state.valid_unique and state.sign is None for state in state_group),
        "excluded_valid_recall": excluded["recall"],
        "excluded_valid_value": excluded["value"],
        "excluded_valid_sign": excluded["sign"] if sign_applicable else None,
        "sum_hits_llm": sum_hl,
        "sum_hits_param": sum_hp,
        "sum_n_crit": sum_nc,
        "sum_delta_value": sum_dv,
        "recall_llm": rllm,
        "recall_param": rparam,
        "delta_recall": dr,
        "delta_value": dv,
        "mcnemar_b": b,
        "mcnemar_c": c,
        "mcnemar_tie": tie,
    }
    if len(state_group) != NOMINAL_PER_RUN:
        raise ValueError(f"Expected 900 keys in {family}/run {run}, got {len(state_group)}")
    return row


def compute_all_run_rows(states: Sequence[KeyState]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[tuple[str, int], list[KeyState]] = collections.defaultdict(list)
    for state in states:
        grouped[(state.family, state.run)].append(state)
    answer: dict[str, list[dict[str, Any]]] = {}
    for scenario in SCENARIOS:
        rows: list[dict[str, Any]] = []
        for family in FAMILY_ORDER:
            for run in sorted(EXPECTED_RUNS[family]):
                rows.append(compute_run_row(grouped[(family, run)], scenario["id"]))
        answer[scenario["id"]] = rows
    return answer


def bootstrap_indices(n_runs: int, resamples: int = BOOTSTRAP_B,
                      seed: int = BOOTSTRAP_SEED) -> np.ndarray:
    if n_runs <= 0:
        raise ValueError("Bootstrap requires at least one run")
    rng = np.random.default_rng(seed)
    return rng.integers(0, n_runs, size=(resamples, n_runs))


def run_bootstrap(values: Sequence[float | None], indices: np.ndarray) -> dict[str, Any]:
    """Unweighted run estimate and percentile CI; never drops an undefined run."""
    if any(value is None for value in values):
        raise ValueError("A run has no defined estimate; available-case analysis may not delete a run")
    array = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(array)) or len(array) != indices.shape[1]:
        raise ValueError("Bootstrap values do not match the fixed run-resampling plan")
    means = array[indices].mean(axis=1)
    return {
        "estimate": float(array.mean()),
        "ci95": [float(x) for x in np.percentile(means, [2.5, 97.5])],
        "n_runs": len(array),
    }


@functools.lru_cache(maxsize=8)
def _bootstrap_plan(n_runs: int) -> np.ndarray:
    return bootstrap_indices(n_runs)


def equal_run_and_pooled(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: (FAMILY_ORDER.index(row["family"]), row["run"]))
    indices = _bootstrap_plan(len(ordered))
    equal = {metric: run_bootstrap([row[metric] for row in ordered], indices)
             for metric in METRICS}
    hl = math.fsum(row["sum_hits_llm"] for row in ordered)
    hp = math.fsum(row["sum_hits_param"] for row in ordered)
    nc = math.fsum(row["sum_n_crit"] for row in ordered)
    dv_sum = math.fsum(row["sum_delta_value"] for row in ordered)
    n_value = sum(row["n_resolved_value"] for row in ordered)
    pooled_rllm = hl / nc if nc else None
    pooled_rparam = hp / nc if nc else None
    pooled = {
        "recall_llm": pooled_rllm,
        "recall_param": pooled_rparam,
        "delta_recall": (pooled_rllm - pooled_rparam
                         if pooled_rllm is not None and pooled_rparam is not None else None),
        "delta_value": dv_sum / n_value if n_value else None,
        "n_resolved_recall": sum(row["n_resolved_recall"] for row in ordered),
        "n_resolved_value": n_value,
        "sum_n_crit": nc,
    }
    return {"equal_run": equal, "pooled_agent_day_sensitivity": pooled}


def cmh_formulas(strata: Sequence[tuple[int, int]]) -> dict[str, Any]:
    """The three declared pooled CMH-style nominal approximations."""
    B = sum(int(b) for b, _ in strata)
    C = sum(int(c) for _, c in strata)
    n = B + C
    if n == 0:
        uncorrected = corrected = legacy = 0.0
    else:
        uncorrected = (B - C) ** 2 / n
        corrected = max(0, abs(B - C) - 1) ** 2 / n
        legacy = (abs(B - C) - 1) ** 2 / n
    def result(chi2: float) -> dict[str, float]:
        return {"chi2": float(chi2), "p_nominal": float(math.erfc(math.sqrt(chi2 / 2)))}
    return {
        "B": B, "C": C, "discordant": n,
        "uncorrected": result(uncorrected),
        "continuity_corrected": result(corrected),
        "legacy_unbounded_correction": result(legacy),
        "note": "Nominal agent-day independence approximation; not cross-corpus error calibration.",
    }


@functools.lru_cache(maxsize=256)
def exact_mcnemar(b: int, c: int) -> float:
    # Reuse the established implementation, including n=0 -> 1 and two-sided tail.
    return float(_mcnemar_exact(int(b), int(c)))


def _exact_sign_matrix(n_runs: int) -> np.ndarray:
    integers = np.arange(2 ** n_runs, dtype=np.uint64)[:, None]
    bits = (integers >> np.arange(n_runs, dtype=np.uint64)) & 1
    return (bits * 2 - 1).astype(np.int8)


@functools.lru_cache(maxsize=8)
def _monte_carlo_sign_matrix(n_runs: int, n_draws: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return (rng.integers(0, 2, size=(n_draws, n_runs), dtype=np.int8) * 2 - 1).astype(np.int8)


def run_cluster_sign_flip(discordance: Sequence[int], exact: bool,
                          n_draws: int = SIGN_FLIP_N,
                          seed: int = SIGN_FLIP_SEED) -> dict[str, Any]:
    """Whole-run label flips of T=sum_r(b_r-c_r), including |T| ties as extreme."""
    d = np.asarray(discordance, dtype=np.int64)
    if d.ndim != 1 or not len(d):
        raise ValueError("Sign-flip requires one b-c value per run")
    observed = int(d.sum())
    if exact:
        signs = _exact_sign_matrix(len(d))
        statistics = signs @ d
        extreme = int(np.count_nonzero(np.abs(statistics) >= abs(observed)))
        return {
            "method": "exact_2^n", "n_runs": len(d), "T_observed": observed,
            "enumerations": int(2 ** len(d)), "extreme": extreme,
            "p": extreme / (2 ** len(d)),
        }
    signs = _monte_carlo_sign_matrix(len(d), n_draws, seed)
    statistics = signs @ d
    extreme = int(np.count_nonzero(np.abs(statistics) >= abs(observed)))
    return {
        "method": "monte_carlo_run_cluster", "n_runs": len(d), "T_observed": observed,
        "draws": int(n_draws), "seed": int(seed), "extreme": extreme,
        "p": (1 + extreme) / (1 + n_draws),
    }


def bh_adjust(pvalues: Sequence[float]) -> list[float]:
    if len(pvalues) != 4:
        raise ValueError("The one and only McNemar BH family has four tests")
    order = sorted(range(4), key=lambda index: pvalues[index])
    adjusted = [1.0] * 4
    running = 1.0
    for rank, index in reversed(list(enumerate(order, start=1))):
        running = min(running, pvalues[index] * 4 / rank)
        adjusted[index] = min(1.0, running)
    return adjusted


def _run_metrics_for_group(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "expected_keys": sum(row["expected_keys"] for row in rows),
        "raw_rows": sum(row["raw_rows"] for row in rows),
        "valid_records": sum(row["valid_records"] for row in rows),
        "valid_unique_keys": sum(row["valid_unique_keys"] for row in rows),
        "empty_only_keys": sum(row["empty_only_keys"] for row in rows),
        "no_surviving_row_keys": sum(row["no_surviving_row_keys"] for row in rows),
        "n_resolved_recall": sum(row["n_resolved_recall"] for row in rows),
        "n_resolved_value": sum(row["n_resolved_value"] for row in rows),
        "n_resolved_sign": (sum(row["n_resolved_sign"] for row in rows)
                            if rows[0]["n_resolved_sign"] is not None else None),
        "conflict_recall_A": sum(row["conflict_recall_A"] for row in rows),
        "conflict_value_A": sum(row["conflict_value_A"] for row in rows),
        "conflict_sign_A": sum(row["conflict_sign_A"] for row in rows),
    }


def aggregate_scenario(scenario_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    scenario = SCENARIO_BY_ID[scenario_id]
    output: dict[str, Any] = {
        **scenario,
        "status": STATUS,
        "families": {},
        "estimand_note": _scenario_note(scenario_id),
    }
    for family in FAMILY_ORDER:
        selected = [row for row in rows if row["family"] == family]
        family_output: dict[str, Any] = {
            **_run_metrics_for_group(selected),
            **equal_run_and_pooled(selected),
        }
        if scenario["family"] == "E":
            family_output["paired_inference"] = None
        else:
            b = sum(int(row["mcnemar_b"]) for row in selected)
            c = sum(int(row["mcnemar_c"]) for row in selected)
            tie = sum(int(row["mcnemar_tie"]) for row in selected)
            family_output["paired_inference"] = {
                "mcnemar": {"b": b, "c": c, "tie": tie,
                            "p_exact_two_sided": exact_mcnemar(b, c)},
                "run_cluster_sign_flip": run_cluster_sign_flip(
                    [int(row["mcnemar_b"]) - int(row["mcnemar_c"]) for row in selected],
                    exact=family in {"Q", "G"}),
            }
        output["families"][family] = family_output
    output["all_80_runs"] = {
        **_run_metrics_for_group(rows),
        **equal_run_and_pooled(rows),
    }
    if scenario["family"] == "E":
        output["all_80_runs"]["paired_inference"] = None
        output["inference_omission"] = "Fractional attempt-mean hits: no exact McNemar, CMH, or sign flip."
    else:
        strata = [(int(row["mcnemar_b"]), int(row["mcnemar_c"])) for row in rows]
        output["all_80_runs"]["paired_inference"] = {
            "pooled_cmh_three_formulas": cmh_formulas(strata),
            "run_cluster_sign_flip": run_cluster_sign_flip(
                [b - c for b, c in strata], exact=False),
        }
    return output


def _scenario_note(scenario_id: str) -> str:
    family = SCENARIO_BY_ID[scenario_id]["family"]
    return {
        "A": "Available resolved cases; metric-specific cohorts; 86 gaps are not zero-imputed.",
        "B": "Common five-field consistent cohort; all metrics use the same keys.",
        "C": "Exactly one valid attempt per retained key; strongest source conservatism.",
        "D": "Audit six fields (five outcome fields plus picked) must be consistent.",
        "E": "Equal-weight mean of recorded attempts per key; a different estimand, not a recovered run truth.",
        "F": "Outcome-blind mechanical hash sensitivity; not identification of the historically correct attempt.",
        "G": "A plus zero LLM consumption for 56 EMPTY_ONLY keys; 30 no-row keys remain missing.",
        "H": "A plus zero LLM consumption for all 86 gaps; changes the estimand.",
        "I": "Directional/sign scenario, not a point estimate and not an exhaustive p-value bound.",
        "J": "Partial-identification endpoint using all-corpus daily top-three log1p(cit) value ceilings.",
    }[family]


def apply_a_bh(scenarios: dict[str, dict[str, Any]]) -> None:
    raw = [scenarios["A"]["families"][family]["paired_inference"]["mcnemar"]["p_exact_two_sided"]
           for family in FAMILY_ORDER]
    adjusted = bh_adjust(raw)
    for family, p_raw, p_adjusted in zip(FAMILY_ORDER, raw, adjusted):
        mcnemar = scenarios["A"]["families"][family]["paired_inference"]["mcnemar"]
        mcnemar["p_bh4"] = p_adjusted
        mcnemar["bh_family"] = "A only: O,C,Q,G exact two-sided McNemar"
    scenarios["A"]["mcnemar_bh4"] = {
        "family_order": list(FAMILY_ORDER), "raw": raw, "adjusted": adjusted,
        "scope": "Only A's four family exact McNemar tests; CIs and pooled CMH are not BH-adjusted.",
    }


def build_input_manifest(results_dir: Path, root: Path = ROOT) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    for path in sorted(results_dir.glob("llm_replay_*.jsonl")):
        tag = path.name[len("llm_replay_"):-len(".jsonl")]
        if not TAG_RE.match(tag):
            continue
        data = path.read_bytes()
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            relative = path.name
        manifest.append({
            "path": relative,
            "file": path.name,
            "size_bytes": len(data),
            "line_count": sum(bool(line.strip()) for line in data.splitlines()),
            "line_count_definition": "nonblank JSONL records",
            "sha256": _sha256_bytes(data),
        })
    if len(manifest) != EXPECTED_SHARDS:
        raise ValueError(f"Expected {EXPECTED_SHARDS} manifest entries, got {len(manifest)}")
    return manifest


def environment_info(spec_path: Path, manifest: list[dict[str, Any]],
                     corpus_path: Path | None = None) -> dict[str, Any]:
    script_path = Path(__file__).resolve()
    answer = {
        "python_version": sys.version,
        "python_version_info": list(sys.version_info[:3]),
        "python_executable": sys.executable,
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "analysis_script": str(script_path.relative_to(ROOT)),
        "analysis_script_sha256": _sha256_file(script_path),
        "specification": str(spec_path.resolve().relative_to(ROOT)),
        "specification_sha256": _sha256_file(spec_path),
        "input_manifest_entries": len(manifest),
        "input_manifest_sha256": _sha256_json(manifest),
        "bootstrap": {"unit": "run", "resamples": BOOTSTRAP_B,
                      "seed": BOOTSTRAP_SEED, "interval": "percentile 95%"},
        "sign_flip": {"monte_carlo_draws": SIGN_FLIP_N, "seed": SIGN_FLIP_SEED,
                      "Q_G": "exact 2^10", "O_C_and_80_run": "Monte Carlo (1+extreme)/(1+N)"},
    }
    if corpus_path is not None:
        answer["fixed_corpus_for_J_value_ceiling"] = {
            "path": str(corpus_path.resolve().relative_to(ROOT)),
            "sha256": _sha256_file(corpus_path),
            "role": "Only scenario J daily all-corpus top-three log1p(cit) ceilings; no extra replay outcomes.",
        }
    return answer


def _clean_csv_value(value: Any) -> Any:
    return "" if value is None else value


def run_metrics_csv(run_rows: dict[str, list[dict[str, Any]]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=RUN_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for scenario in SCENARIOS:
        for row in run_rows[scenario["id"]]:
            writer.writerow({key: _clean_csv_value(row.get(key)) for key in RUN_COLUMNS})
    return buffer.getvalue()


def ledger_rows(states: Sequence[KeyState]) -> Iterator[dict[str, Any]]:
    for state in states:
        scenario_dispositions: dict[str, list[str]] = {}
        for scenario in SCENARIOS:
            cell = scenario_cell(state, scenario["id"])
            scenario_dispositions[scenario["id"]] = [
                cell.recall_status, cell.value_status, cell.sign_status]
        yield {
            "key": [state.family, state.run, state.agent, state.sim_day],
            "n_rows": state.n_rows,
            "n_valid": len(state.records),
            "n_empty": state.n_empty,
            "gap": state.gap,
            "canonical": dataclasses.asdict(state.canonical),
            "daily_all_corpus_value_upper": state.value_upper,
            "source_records": [
                {"source_file": file, "source_line": line, "valid_nonempty_picked": valid}
                for file, line, valid in state.provenance
            ],
            "A_values": {
                "recall_hits_llm_hits_param_n_crit": state.recall,
                "delta_value": state.delta_value,
                "sign": state.sign,
            },
            "hash_selection_provenance_only": state.hash_meta,
            "scenario_disposition_order": ["recall", "delta_value", "paired_sign"],
            "scenario_dispositions": scenario_dispositions,
        }


def _fmt(value: float | None, digits: int = 6, signed: bool = False) -> str:
    if value is None:
        return "NA"
    format_spec = f"{'+' if signed else ''}.{digits}f"
    return format(value, format_spec)


def _estimate_ci(item: dict[str, Any], signed: bool = False) -> str:
    lo, hi = item["ci95"]
    return f"{_fmt(item['estimate'], signed=signed)} [{_fmt(lo, signed=signed)}, {_fmt(hi, signed=signed)}]"


def _p(value: float) -> str:
    return f"{value:.3e}"


def direction_summary(scenarios: dict[str, dict[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for family in FAMILY_ORDER:
        family_answer: dict[str, Any] = {}
        for metric in ("delta_recall", "delta_value"):
            estimates = {sid: scenarios[sid]["families"][family]["equal_run"][metric]["estimate"]
                         for sid in scenarios}
            signs = {sid: (value > 0) - (value < 0) for sid, value in estimates.items()}
            family_answer[metric] = {
                "estimate_by_scenario": estimates,
                "sign_by_scenario": signs,
                "same_strict_sign_all_17_scenarios": len(set(signs.values())) == 1 and 0 not in signs.values(),
            }
        answer[family] = family_answer
    return answer


def render_report(summary: dict[str, Any]) -> str:
    structure = summary["structure"]
    scenarios = summary["scenarios"]
    lines = [
        "# 四家族唯一键全量重算（frozen_reanalysis_v1）",
        "",
        f"**状态：`{STATUS}`。** 本工作是已查看旧结果后的受控语料内探索性重分析，"
        "不是 prospective preregistration，也不构成跨语料确证。所有场景一次性完整报告，不按效应或 p 值筛选。",
        "",
        "## 1. 输入、完整性与不可变边界",
        "",
        f"- 输入：**{summary['input_manifest_count']}** 个主审计 tag JSONL，80 run（O/C 各 30，Q/G 各 10）；"
        f"原始行 {structure['raw_rows']}，非空 `picked` 记录 {structure['valid_records']}。",
        f"- 期望唯一键 **{structure['expected_keys']}**；有效唯一键 **{structure['valid_unique_keys']}**；"
        f"`EMPTY_ONLY` **{structure['empty_only_keys']}**；`NO_SURVIVING_ROW` **{structure['no_surviving_row_keys']}**。",
        f"- 与有效记录共键的空记录 **{structure['empty_records_on_valid_keys']}**，不属于 86 缺口；"
        f"重复超额有效记录 {structure['duplicate_excess_records']}。",
        "- 日级 `hits_param,n_crit,value_param` 任一不唯一即失败；本快照已通过该闸门。"
        "文件行号只用于 F 的盲哈希来源标识，绝不用于推断正确 attempt。",
        f"- 旧 {structure['valid_records']} 行非去重结果继续标为 `{LEGACY_STATUS}`，不改名为本冻结重分析。",
        "",
        "| Family | Expected | Valid unique | EMPTY_ONLY | NO_SURVIVING_ROW | A recall conflicts | A value conflicts | A sign conflicts |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for family in FAMILY_ORDER:
        item = structure["by_family"][family]
        lines.append(f"| {family} | {item['expected_keys']} | {item['valid_unique_keys']} | "
                     f"{item['empty_only_keys']} | {item['no_surviving_row_keys']} | "
                     f"{item['recall_conflicts_A']} | {item['value_conflicts_A']} | {item['sign_conflicts_A']} |")
    lines += [
        "",
        "A 的解析人口分别由充分统计量决定：recall/Δrecall 71,573，Δvalue 70,676，配对符号 71,618。"
        "B/C/D/E/F 的键数分别见下表；不同指标人口不被强行合并，B 另提供共同 cohort。",
        "",
        "## 2. 主规则 A：run 等权点估计与 95% percentile run-bootstrap CI",
        "",
        "10,000 次、seed=42，以整个 run 为重抽样单位。区间只含 run 间变异，不含仲裁/缺失不确定性。",
        "",
        "| Family | Rllm [CI] | Rparam [CI] | Δrecall [CI] | Δvalue [CI] | n recall / value / sign |",
        "|---|---|---|---|---|---:|",
    ]
    for family in FAMILY_ORDER:
        item = scenarios["A"]["families"][family]
        eq = item["equal_run"]
        lines.append(f"| {family} | {_estimate_ci(eq['recall_llm'])} | {_estimate_ci(eq['recall_param'])} | "
                     f"{_estimate_ci(eq['delta_recall'], True)} | {_estimate_ci(eq['delta_value'], True)} | "
                     f"{item['n_resolved_recall']} / {item['n_resolved_value']} / {item['n_resolved_sign']} |")
    lines += ["", "Pooled agent-day 加权敏感性（不替代 run 等权主口径）：", "",
              "| Family | Rllm | Rparam | Δrecall | Δvalue |", "|---|---:|---:|---:|---:|"]
    for family in FAMILY_ORDER:
        pooled = scenarios["A"]["families"][family]["pooled_agent_day_sensitivity"]
        lines.append(f"| {family} | {_fmt(pooled['recall_llm'])} | {_fmt(pooled['recall_param'])} | "
                     f"{_fmt(pooled['delta_recall'], signed=True)} | {_fmt(pooled['delta_value'], signed=True)} |")
    lines += ["", "A 的精确 McNemar 与唯一 BH(4) 检验族：", "",
              "| Family | b | c | tie | exact two-sided p | BH(4) p | run-cluster flip p |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for family in FAMILY_ORDER:
        paired = scenarios["A"]["families"][family]["paired_inference"]
        mc = paired["mcnemar"]
        flip = paired["run_cluster_sign_flip"]
        method = "exact" if flip["method"] == "exact_2^n" else "MC"
        lines.append(f"| {family} | {mc['b']} | {mc['c']} | {mc['tie']} | {_p(mc['p_exact_two_sided'])} | "
                     f"{_p(mc['p_bh4'])} | {_p(flip['p'])} ({method}) |")
    cmh = scenarios["A"]["all_80_runs"]["paired_inference"]["pooled_cmh_three_formulas"]
    flip80 = scenarios["A"]["all_80_runs"]["paired_inference"]["run_cluster_sign_flip"]
    lines += [
        "",
        f"80-run 汇总 B={cmh['B']}, C={cmh['C']}：未校正 χ²={cmh['uncorrected']['chi2']:.6f} "
        f"(p={_p(cmh['uncorrected']['p_nominal'])})；修正 χ²={cmh['continuity_corrected']['chi2']:.6f} "
        f"(p={_p(cmh['continuity_corrected']['p_nominal'])})；旧式 χ²={cmh['legacy_unbounded_correction']['chi2']:.6f} "
        f"(p={_p(cmh['legacy_unbounded_correction']['p_nominal'])})。"
        f"80-run cluster MC flip p={_p(flip80['p'])}（100,000，seed=42）。三种 CMH 均只是名义 agent-day 独立近似。",
        "",
        "## 3. 全场景 run 等权结果（全部 17 个场景）",
        "",
        "每格均为点估计 [95% run-bootstrap CI]。E 是 attempt 均值估计量；G/H 是零消费运维情景；"
        "I/J 是方向/端点而非新点估计。",
        "",
        "| Scenario | Family | n recall/value | Rllm [CI] | Rparam [CI] | Δrecall [CI] | Δvalue [CI] |",
        "|---|---|---:|---|---|---|---|",
    ]
    for scenario in SCENARIOS:
        sid = scenario["id"]
        for family in FAMILY_ORDER:
            item = scenarios[sid]["families"][family]
            eq = item["equal_run"]
            lines.append(f"| {sid} `{scenario['rule']}` | {family} | "
                         f"{item['n_resolved_recall']}/{item['n_resolved_value']} | "
                         f"{_estimate_ci(eq['recall_llm'])} | {_estimate_ci(eq['recall_param'])} | "
                         f"{_estimate_ci(eq['delta_recall'], True)} | {_estimate_ci(eq['delta_value'], True)} |")
    lines += ["", "### 全场景 pooled agent-day 敏感性", "",
              "| Scenario | Family | pooled Rllm | pooled Rparam | pooled Δrecall | pooled Δvalue |",
              "|---|---|---:|---:|---:|---:|"]
    for scenario in SCENARIOS:
        sid = scenario["id"]
        for family in FAMILY_ORDER:
            pooled = scenarios[sid]["families"][family]["pooled_agent_day_sensitivity"]
            lines.append(f"| {sid} | {family} | {_fmt(pooled['recall_llm'])} | {_fmt(pooled['recall_param'])} | "
                         f"{_fmt(pooled['delta_recall'], signed=True)} | {_fmt(pooled['delta_value'], signed=True)} |")
    lines += ["", "## 4. 全场景配对符号、CMH 与 run-cluster 敏感性", "",
              "E 不做精确 McNemar/CMH，也不做符号翻转。其余场景下列 p 均为情景描述；只有 A 四家族进入 BH(4)。"
              "Q/G 为精确 2^10；O/C 与 80-run 为 100,000 次 seed=42 Monte Carlo。", "",
              "| Scenario | Family | b | c | tie | exact McNemar p | run-cluster flip p |",
              "|---|---|---:|---:|---:|---:|---:|"]
    for scenario in SCENARIOS:
        if scenario["family"] == "E":
            continue
        sid = scenario["id"]
        for family in FAMILY_ORDER:
            paired = scenarios[sid]["families"][family]["paired_inference"]
            mc, flip = paired["mcnemar"], paired["run_cluster_sign_flip"]
            lines.append(f"| {sid} | {family} | {mc['b']} | {mc['c']} | {mc['tie']} | "
                         f"{_p(mc['p_exact_two_sided'])} | {_p(flip['p'])} |")
    lines += ["", "### 80-run 三种 CMH 公式与整体 run-cluster 翻转", "",
              "| Scenario | B | C | χ² uncorrected | χ² corrected | χ² legacy | 80-run flip p |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for scenario in SCENARIOS:
        if scenario["family"] == "E":
            continue
        paired = scenarios[scenario["id"]]["all_80_runs"]["paired_inference"]
        cmh = paired["pooled_cmh_three_formulas"]
        flip = paired["run_cluster_sign_flip"]
        lines.append(f"| {scenario['id']} | {cmh['B']} | {cmh['C']} | "
                     f"{cmh['uncorrected']['chi2']:.6f} | {cmh['continuity_corrected']['chi2']:.6f} | "
                     f"{cmh['legacy_unbounded_correction']['chi2']:.6f} | {_p(flip['p'])} |")
    lines += ["", "## 5. 方向是否依赖处置规则", "",
              "下表列出所有 17 个场景的 run 等权 Δ 符号（`+`/`-`/`0`；顺序为 "
              + ", ".join(item["id"] for item in SCENARIOS) + "）。I/J 含刻意方向与端点，不能拿来挑选结论。", "",
              "| Family | Δrecall signs | same nonzero sign? | Δvalue signs | same nonzero sign? |",
              "|---|---|---|---|---|"]
    direction = summary["direction_summary"]
    for family in FAMILY_ORDER:
        cells = []
        for metric in ("delta_recall", "delta_value"):
            item = direction[family][metric]
            symbols = "".join("+" if sign > 0 else "-" if sign < 0 else "0"
                              for sign in item["sign_by_scenario"].values())
            cells += [f"`{symbols}`", "yes" if item["same_strict_sign_all_17_scenarios"] else "no"]
        lines.append(f"| {family} | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |")
    lines += [
        "",
        "因此，A/B/E、五个 F 盐、G/H 与 I/J 是否同向必须逐族逐项读取，而不能用一个‘总体稳健’标签替代。"
        "`same nonzero sign=no` 即表示结论对至少一个预定规则敏感；即使为 yes，也仅限本语料内方向一致。",
        "",
        "## 6. J 的每日全语料价值上界",
        "",
        "上界为当日**全部论文**最高三项 `log1p(cit)` 之和，而非 digest 内上界；仅赋给 A 未解析的冲突/缺口。"
        "已解析键保持原值。J lower/upper 的 recall 与 value 逐键有序，因此端点保持方向顺序。",
        "",
        "| sim_day | upper | sim_day | upper | sim_day | upper |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    upper = summary["daily_all_corpus_value_upper"]
    for day in range(10):
        lines.append(f"| {day} | {_fmt(upper[str(day)])} | {day + 10} | {_fmt(upper[str(day + 10)])} | "
                     f"{day + 20} | {_fmt(upper[str(day + 20)])} |")
    env = summary["environment"]
    lines += [
        "",
        "## 7. 可复现性与解释限制",
        "",
        f"- 规约 SHA-256：`{env['specification_sha256']}`；分析脚本 SHA-256：`{env['analysis_script_sha256']}`。",
        f"- 292 输入 manifest SHA-256：`{env['input_manifest_sha256']}`；逐文件路径/大小/行数/SHA-256 见 `input_manifest.json`。",
        f"- Python `{env['python_version_info']}`，NumPy `{env['numpy_version']}`；完整环境见 `environment.json`。",
        "- F 哈希字节串只含 salt、family/run/agent/sim_day、source_file/source_line，绝不含任何结果或理由字段。"
        "五种盐全部报告，哈希不是历史真相。",
        "- 缺失与冲突不假定随机；available-resolved-case 可能有选择偏倚。86 缺口在 A 不按零、不按名义 900 强补分母，也不删除整个 run。",
        "- run 推断不消除 run 内相关、共享语料/标签/上游 digest、模型记忆或缺失非随机。Q/G 仅 10 run，CI 为小样本探索描述。",
        f"- honest={HONEST_DESCRIPTION_REFERENCE:.3f} 仅保留为固定描述参照；它不是本 80-run 同 digest 配对臂，未进入新的配对推断。",
        "- 时间外无泄漏复制、point-in-time 特征、记忆消融、S2d/S4/S5、公共层独立确认、HP-0 与后续人类研究仍未完成。",
        "",
        "默认执行只打印本报告，不写文件。只有显式 `--write` 才生成独立目录中的 summary、REPORT、run CSV、压缩逐键账本、292 输入 manifest、规约快照与环境信息；覆盖还需 `--force`。",
        "",
    ]
    return "\n".join(lines)


def build_analysis(results_dir: Path = DEFAULT_RESULTS_DIR,
                   spec_path: Path = SPEC_PATH) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], list[KeyState]]:
    """Run the entire frozen analysis in memory; this function never writes files."""
    if not spec_path.is_file():
        raise FileNotFoundError(f"Missing frozen specification: {spec_path}")
    # Reuse the immutable audit loader and its exact tag/run/shard gates.
    runs, _shards, skipped = load_runs(results_dir)
    manifest = build_input_manifest(results_dir)
    canonical = canonical_daily_parameters(runs)

    # build_all is the same corpus constructor used by run_llm_replay.  It is
    # needed only for J's wider-than-digest, all-corpus daily value ceiling.
    universe, _critical, _watchlists, corpus_stats = cp.build_all()
    upper = daily_value_upper(universe)
    raw_corpus = ROOT / "sim" / "pilot" / "data" / "raw" / "arxiv_2019-09.jsonl"
    lite_corpus = ROOT / "sim" / "pilot" / "data" / "corpus_lite.json"
    corpus_path = lite_corpus if corpus_stats.get("_source") == "corpus_lite.json" else raw_corpus
    states = build_key_states(runs, canonical, upper)
    # Raw records are now represented by compact states; release duplicate containers.
    del runs
    structure = structure_counts(states)
    validate_structure(structure)
    run_rows = compute_all_run_rows(states)
    scenarios = {scenario["id"]: aggregate_scenario(scenario["id"], run_rows[scenario["id"]])
                 for scenario in SCENARIOS}
    apply_a_bh(scenarios)
    env = environment_info(spec_path, manifest, corpus_path)
    summary: dict[str, Any] = {
        "schema": SCHEMA,
        "script_version": VERSION,
        "status": STATUS,
        "legacy_result_status": LEGACY_STATUS,
        "not_prospective_preregistration": True,
        "cross_corpus_confirmatory": False,
        "read_only_inputs": True,
        "default_behavior": "stdout only; --write required for frozen_reanalysis_v1; --force required to overwrite",
        "unique_key": "(family, run, agent, sim_day)",
        "scenario_order": [scenario["id"] for scenario in SCENARIOS],
        "scenario_definitions": list(SCENARIOS),
        "skipped_non_main_tags": skipped,
        "input_manifest_count": len(manifest),
        "input_manifest": manifest,
        "structure": structure,
        "structural_expectations": EXPECTED_STRUCTURE,
        "structural_expectations_validated": True,
        "bootstrap_plan": {
            "unit": "whole run", "resamples": BOOTSTRAP_B, "seed": BOOTSTRAP_SEED,
            "interval": "percentile 95%", "same_indices_within_each_run_count": True,
            "run_counts": {"O": 30, "C": 30, "Q": 10, "G": 10, "all": 80},
        },
        "honest_fixed_descriptive_reference": {
            "recall": HONEST_DESCRIPTION_REFERENCE,
            "paired_80_run_inference": False,
            "reason": "Replay proxy seed changes by run; legacy honest reconstruction fixed seed=99.",
        },
        "daily_all_corpus_value_upper": {str(day): value for day, value in sorted(upper.items())},
        "scenarios": scenarios,
        "direction_summary": direction_summary(scenarios),
        "artifacts": {
            "summary": "summary.json", "report": "REPORT.md", "run_metrics": "run_metrics.csv",
            "compressed_key_ledger": "key_ledger.jsonl.gz", "input_manifest": "input_manifest.json",
            "specification_snapshot": "SPECIFICATION.md", "environment": "environment.json",
            "run_metric_rows": len(SCENARIOS) * 80,
            "key_ledger_rows": NOMINAL_TOTAL,
        },
        "environment": env,
        "limitations": [
            "Within-corpus exploratory reanalysis after legacy results were seen.",
            "Run-level resampling does not eliminate within-run dependence, shared corpus/labels/digests, model memory, or nonrandom missingness.",
            "Available resolved cases may be selected; attempt means estimate a different estimand.",
            "Hash selection is outcome-blind mechanics, not historical truth; zero-gap scenarios are operational scenarios.",
            "J values are partial-identification endpoints, not new point estimates.",
        ],
    }
    return summary, run_rows, states


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(output_dir: Path, force: bool, summary: dict[str, Any], report: str,
         csv_text: str, states: Sequence[KeyState], spec_path: Path) -> None:
    """Write only the seven dedicated artifacts; never remove unrelated files."""
    targets = {name: output_dir / name for name in ARTIFACT_NAMES}
    existing = [str(path) for path in targets.values() if path.exists()]
    if existing and not force:
        raise FileExistsError(f"Refusing to overwrite existing artifacts without --force: {existing}")
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_json = json.dumps(summary["input_manifest"], ensure_ascii=False,
                               indent=1, allow_nan=False) + "\n"
    environment_json = json.dumps(summary["environment"], ensure_ascii=False,
                                  indent=1, allow_nan=False) + "\n"
    summary_json = json.dumps(summary, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    _atomic_write_bytes(targets["input_manifest.json"], manifest_json.encode("utf-8"))
    _atomic_write_bytes(targets["environment.json"], environment_json.encode("utf-8"))
    _atomic_write_bytes(targets["SPECIFICATION.md"], spec_path.read_bytes())
    _atomic_write_bytes(targets["run_metrics.csv"], csv_text.encode("utf-8"))
    _atomic_write_bytes(targets["REPORT.md"], report.encode("utf-8"))

    ledger_path = targets["key_ledger.jsonl.gz"]
    temporary = ledger_path.with_name(f".{ledger_path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("xb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                for row in ledger_rows(states):
                    line = json.dumps(row, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":"), allow_nan=False) + "\n"
                    compressed.write(line.encode("utf-8"))
        os.replace(temporary, ledger_path)
    finally:
        if temporary.exists():
            temporary.unlink()
    _atomic_write_bytes(targets["summary.json"], summary_json.encode("utf-8"))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR,
                        help="Top-level directory containing the immutable 292 replay shards")
    parser.add_argument("--spec", type=Path, default=SPEC_PATH,
                        help="Frozen specification to hash and snapshot")
    parser.add_argument("--write", action="store_true",
                        help="Write only sim/pilot/results/frozen_reanalysis_v1; default is stdout only")
    parser.add_argument("--force", action="store_true",
                        help="With --write, permit replacement of the seven dedicated output artifacts")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.force and not args.write:
        raise SystemExit("--force is meaningful only together with --write")
    summary, run_rows, states = build_analysis(args.results_dir, args.spec)
    report = render_report(summary)
    if args.write:
        # Deliberately fixed: no CLI option can redirect writes into immutable inputs or legacy artifacts.
        emit(DEFAULT_OUTPUT_DIR, args.force, summary, report,
             run_metrics_csv(run_rows), states, args.spec)
        print(f"Wrote {len(ARTIFACT_NAMES)} controlled exploratory artifacts to {DEFAULT_OUTPUT_DIR}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
