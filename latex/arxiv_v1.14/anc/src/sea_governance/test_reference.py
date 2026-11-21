"""Synthetic conformance and negative tests for SEA v1.14 governance S1--S4.

Run from ``sim``::

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v sea_governance.test_reference

No repository data, network resource, wall clock, or randomness is used.
"""
from __future__ import annotations

import hashlib
import unittest

from sea_governance import (
    Authorization,
    GovernanceReference,
    OBJECTIVE_TERMS,
    canonical_json,
    proposal_digest,
)


def candidate(candidate_id, *, relevance=0, novelty=0, credibility=0,
              durability=0, harm_avoidance=0, topic="science"):
    return {
        "candidate_id": candidate_id,
        "topic": topic,
        "features": {
            "relevance": relevance,
            "novelty": novelty,
            "credibility": credibility,
            "durability": durability,
            "harm_avoidance": harm_avoidance,
        },
        "provenance": f"fixture:{candidate_id}",
    }


def candidates():
    # Default scores: a=50, b=20.  Relevance/novelty writes reverse them.
    return [
        candidate("a", relevance=10),
        candidate("b", novelty=10),
    ]


def user_state():
    return {"topic_priority": {"science": 0, "health": 0}}


def authorize(operation, proposal, governance=None, *, identifier="sigma-1",
              timestamp="logical:00000010"):
    return Authorization(
        authorization_id=identifier,
        principal="R",
        operation=operation,
        proposal_hash=proposal_digest(operation, proposal),
        timestamp=timestamp,
        version_token=governance.version_token() if governance is not None else "",
    )


def authorized_write(governance, patch, *, timestamp="logical:00000010"):
    return governance.write_objective(
        patch,
        actor="R",
        authorization=authorize("objective_write", patch, governance, timestamp=timestamp),
        evidence=["proposal:objective-write"],
    )


class TestS1Inspectability(unittest.TestCase):
    def test_s1_objective_defaults_history_and_provenance_are_inspectable(self):
        governance = GovernanceReference()
        inspected = governance.inspect_objective()
        self.assertEqual(inspected["objective"], inspected["defaults"])
        self.assertEqual(set(inspected["objective"]["weights"]), set(OBJECTIVE_TERMS))
        self.assertNotIn("revenue", inspected["objective"]["weights"])
        self.assertFalse(inspected["provenance"]["third_party_revenue_term"])
        self.assertEqual(inspected["version"], 0)
        self.assertEqual(inspected["version_token"], governance.version_token())
        self.assertEqual(len(inspected["objective_sha256"]), 64)
        self.assertEqual(inspected["versions"][0]["evidence"], ["defaults:sea-v1.14"])
        self.assertIn("defaults_source", inspected["provenance"])
        self.assertIn("objective_expression", inspected["provenance"])
        self.assertIn("time_source", inspected["provenance"])
        self.assertEqual(inspected, GovernanceReference().inspect_objective())

        # Read snapshots cannot mutate the implementation or its defaults.
        inspected["objective"]["weights"]["relevance"] = 999
        inspected["versions"].clear()
        reread = governance.inspect_objective()
        self.assertEqual(reread["objective"]["weights"]["relevance"], 5)
        self.assertEqual(len(reread["versions"]), 1)


class TestS2WritesAndRollback(unittest.TestCase):
    def test_s2_unauthorized_objective_writes_are_rejected_and_logged(self):
        governance = GovernanceReference()
        before = governance.inspect_objective()["objective"]
        patch = {"weights": {"relevance": 0}}
        attempts = [
            ("behavioral_measurement", None),
            ("platform", None),
            ("R", authorize("objective_write", {"weights": {"relevance": 1}})),
        ]
        for index, (actor, authorization) in enumerate(attempts):
            with self.subTest(actor=actor, authorization=bool(authorization)):
                result = governance.write_objective(
                    patch,
                    actor=actor,
                    authorization=authorization,
                    evidence=[f"attempt:{index}"],
                )
                self.assertFalse(result["accepted"])
                self.assertEqual(result["reason"], "unauthorized")
                self.assertEqual(governance.inspect_objective()["objective"], before)
                record = governance.audit_records()[-1]
                self.assertEqual(record["event"], "override")
                self.assertFalse(record["payload"]["accepted"])
                self.assertEqual(record["payload"]["actor"], actor)
                self.assertEqual(record["evidence"], [f"attempt:{index}"])
        self.assertTrue(governance.verify_audit()["valid"])

    def test_s2_authorized_write_and_rollback_restore_objective_and_exact_ranking(self):
        governance = GovernanceReference()
        original_objective = governance.inspect_objective()["objective"]
        original_objective_bytes = governance.objective_bytes()
        baseline = governance.rank(
            candidates(), user_state(), {"boost": 0}, evidence=["rank:baseline"]
        )
        patch = {"weights": {"relevance": 0, "novelty": 10}}
        write = authorized_write(governance, patch)
        self.assertTrue(write["accepted"])
        self.assertNotEqual(governance.inspect_objective()["objective"], original_objective)
        changed = governance.rank(
            candidates(), user_state(), {"boost": 0}, evidence=["rank:changed"]
        )
        self.assertNotEqual(changed, baseline)
        self.assertEqual(changed[0]["candidate_id"], "b")

        rollback_auth = authorize(
            "rollback", {"target_version": 0}, governance, identifier="sigma-rollback",
            timestamp="logical:00000020",
        )
        restored = governance.rollback(
            0, authorization=rollback_auth, evidence=["proposal:rollback"]
        )
        self.assertTrue(restored["accepted"])
        self.assertEqual(governance.inspect_objective()["objective"], original_objective)
        after_rollback = governance.rank(
            candidates(), user_state(), {"boost": 999}, evidence=["rank:after-rollback"]
        )
        self.assertEqual(after_rollback, baseline)
        self.assertEqual(governance.objective_bytes(), original_objective_bytes)
        self.assertEqual([item["candidate_id"] for item in after_rollback],
                         [item["candidate_id"] for item in baseline])

        override_record = governance.audit_records()[write["audit_sequence"] - 1]
        rollback_record = governance.audit_records()[restored["audit_sequence"] - 1]
        self.assertEqual(override_record["timestamp"], "logical:00000010")
        self.assertEqual(override_record["payload"]["old_value"], original_objective)
        self.assertNotEqual(override_record["payload"]["new_value"], original_objective)
        self.assertEqual(rollback_record["timestamp"], "logical:00000020")
        self.assertEqual(rollback_record["payload"]["new_value"], original_objective)
        self.assertEqual(rollback_record["payload"]["restored_from"], 0)
        self.assertTrue(governance.verify_audit()["valid"])

    def test_s2_rollback_without_authorization_is_rejected(self):
        governance = GovernanceReference()
        patch = {"weights": {"relevance": 1}}
        authorized_write(governance, patch)
        changed = governance.inspect_objective()["objective"]
        result = governance.rollback(0, authorization=None, evidence=["attempt:rollback"])
        self.assertFalse(result["accepted"])
        self.assertEqual(result["reason"], "unauthorized")
        self.assertEqual(governance.inspect_objective()["objective"], changed)
        self.assertEqual(governance.audit_records()[-1]["event"], "rollback")
        self.assertFalse(governance.audit_records()[-1]["payload"]["accepted"])

    def test_s2_stale_version_token_is_rejected_without_state_change(self):
        governance = GovernanceReference()
        stale_patch = {"weights": {"relevance": 9}}
        stale_authorization = authorize("objective_write", stale_patch, governance)
        authorized_write(governance, {"weights": {"novelty": 3}})
        current = governance.inspect_objective()["objective"]
        result = governance.write_objective(
            stale_patch,
            actor="R",
            authorization=stale_authorization,
            evidence=["attempt:stale-version"],
        )
        self.assertFalse(result["accepted"])
        self.assertEqual(result["reason"], "unauthorized")
        self.assertEqual(governance.inspect_objective()["objective"], current)
        record = governance.audit_records()[-1]
        self.assertNotEqual(record["payload"]["authorization"]["version_token"],
                            record["payload"]["old_version_token"])

    def test_s2_actor_must_match_authorization_principal(self):
        governance = GovernanceReference()
        patch = {"weights": {"relevance": 0}}
        authorization = authorize("objective_write", patch, governance)
        result = governance.write_objective(
            patch, actor="platform", authorization=authorization,
            evidence=["attempt:stolen-principal"],
        )
        self.assertFalse(result["accepted"])
        self.assertEqual(result["guard_reject_reason"], "actor_principal_mismatch")
        self.assertEqual(governance.inspect_objective()["version"], 0)
        record = governance.audit_records()[-1]
        self.assertEqual(record["payload"]["actor"], "platform")
        self.assertEqual(record["payload"]["authorization"]["principal"], "R")
        self.assertFalse(record["payload"]["accepted"])

    def test_s2_invalid_and_nonmonotonic_timestamps_are_rejected(self):
        malformed = GovernanceReference()
        patch = {"weights": {"relevance": 0}}
        malformed_auth = authorize(
            "objective_write", patch, malformed, timestamp="yesterday")
        rejected = malformed.write_objective(
            patch, actor="R", authorization=malformed_auth,
            evidence=["attempt:bad-time"],
        )
        self.assertEqual(rejected["guard_reject_reason"], "invalid_timestamp")

        governance = GovernanceReference()
        accepted = authorized_write(governance, patch, timestamp="logical:00000020")
        self.assertTrue(accepted["accepted"])
        current = governance.inspect_objective()["objective"]
        late_patch = {"weights": {"novelty": 7}}
        stale_time = authorize(
            "objective_write", late_patch, governance,
            identifier="sigma-stale-time", timestamp="logical:00000019")
        stale = governance.write_objective(
            late_patch, actor="R", authorization=stale_time,
            evidence=["attempt:nonmonotonic-time"],
        )
        self.assertEqual(stale["guard_reject_reason"], "nonmonotonic_timestamp")
        self.assertEqual(governance.inspect_objective()["objective"], current)

    def test_s2_authorization_identifier_is_single_use(self):
        governance = GovernanceReference()
        # A no-change guard decision consumes the authorization without creating
        # a new objective version, isolating reuse from stale-version rejection.
        authorization = authorize("objective_write", {}, governance)
        first = governance.write_objective(
            {}, actor="R", authorization=authorization, evidence=["guard:no-change"])
        self.assertEqual(first["reason"], "no_change")
        second = governance.write_objective(
            {}, actor="R", authorization=authorization, evidence=["guard:reuse"])
        self.assertFalse(second["accepted"])
        self.assertEqual(second["guard_reject_reason"], "authorization_reuse")

    def test_s3_revenue_objective_term_is_rejected_even_with_authorization(self):
        governance = GovernanceReference()
        before = governance.inspect_objective()["objective"]
        patch = {"weights": {"platform_revenue": 10}}
        result = authorized_write(governance, patch)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["reason"], "invalid_objective")
        self.assertEqual(governance.inspect_objective()["objective"], before)
        record = governance.audit_records()[-1]
        self.assertFalse(record["payload"]["accepted"])
        self.assertIn("invalid_objective", record["payload"]["reason"])


class TestS3Counterfactuals(unittest.TestCase):
    def test_s3_fixed_supply_platform_invariance_and_rejected_platform_write(self):
        governance = GovernanceReference()
        baseline = {
            "candidates": candidates(),
            "user_state": user_state(),
            "platform_variables": {"ad_revenue": 0, "boost:a": 0},
        }
        changed_platform = {
            "candidates": candidates(),
            "user_state": user_state(),
            "platform_variables": {"ad_revenue": 10**9, "boost:a": 10**6},
        }
        comparison = governance.compare_counterfactual(
            baseline, changed_platform, evidence=["counterfactual:fixed"]
        )
        self.assertEqual(comparison["classification"], "fixed-supply")
        self.assertTrue(comparison["fixed_supply_invariant_holds"])
        self.assertFalse(comparison["ranking_changed"])
        self.assertEqual(comparison["baseline"]["ranking"],
                         comparison["counterfactual"]["ranking"])

        objective_before = governance.inspect_objective()["objective"]
        rejected = governance.write_objective(
            {"g2": "maximize platform revenue"}, actor="platform", authorization=None,
            evidence=["attempt:platform-objective-write"],
        )
        self.assertFalse(rejected["accepted"])
        self.assertEqual(governance.inspect_objective()["objective"], objective_before)
        rejection = governance.audit_records()[-1]
        self.assertEqual(rejection["payload"]["actor"], "platform")
        self.assertFalse(rejection["payload"]["accepted"])

    def test_s3_changed_candidate_ecology_is_separately_logged_and_classified(self):
        governance = GovernanceReference()
        baseline = {
            "candidates": candidates(),
            "user_state": user_state(),
            "platform_variables": {"boost": 0},
        }
        fixed = governance.compare_counterfactual(
            baseline,
            {
                "candidates": candidates(),
                "user_state": user_state(),
                "platform_variables": {"boost": 100},
            },
            evidence=["counterfactual:fixed"],
        )
        ecology = candidates() + [candidate("c", relevance=20, novelty=20)]
        changed = governance.compare_counterfactual(
            baseline,
            {
                "candidates": ecology,
                "user_state": user_state(),
                "platform_variables": {"boost": 100},
            },
            evidence=["counterfactual:ecology"],
        )
        self.assertEqual(fixed["classification"], "fixed-supply")
        self.assertEqual(changed["classification"], "supply-ecosystem")
        self.assertEqual(changed["mechanism"], "supply-mediated")
        self.assertIsNone(changed["fixed_supply_invariant_holds"])
        self.assertTrue(changed["ranking_changed"])
        self.assertEqual(changed["counterfactual"]["ranking"][0]["candidate_id"], "c")
        records = [item for item in governance.audit_records()
                   if item["event"] == "counterfactual"]
        self.assertEqual(len(records), 2)
        self.assertNotEqual(records[0]["sequence"], records[1]["sequence"])
        self.assertEqual([item["payload"]["classification"] for item in records],
                         ["fixed-supply", "supply-ecosystem"])

    def test_deterministic_integer_ranking_and_candidate_id_tie_break(self):
        governance = GovernanceReference()
        tied = candidates() + [candidate("a0", relevance=10)]
        first = governance.rank(
            tied, user_state(), {"arbitrary": "left"}, evidence=["rank:first"]
        )
        second = governance.rank(
            list(reversed(tied)), user_state(), {"arbitrary": "right"},
            evidence=["rank:second"],
        )
        self.assertEqual(first, second)
        self.assertEqual([item["candidate_id"] for item in first], ["a", "a0", "b"])
        self.assertEqual(first[0]["score"], first[1]["score"])


class TestS4AuditAndRecourse(unittest.TestCase):
    def _exercise_decisions(self):
        governance = GovernanceReference()
        governance.admit(candidates()[0], user_state(), evidence=["admission:1"])
        governance.rank(candidates(), user_state(), {}, evidence=["ranking:1"])
        governance.deliver(
            candidates(), user_state(), {}, limit=1, evidence=["delivery:1"]
        )
        patch = {"weights": {"relevance": 6}}
        authorized_write(governance, patch)
        governance.rollback(
            0,
            authorization=authorize(
                "rollback", {"target_version": 0}, governance,
                identifier="sigma-exercise-rollback", timestamp="logical:00000020"),
            evidence=["rollback:1"],
        )
        return governance

    def test_s4_all_decisions_have_evidence_and_valid_hash_chain(self):
        governance = self._exercise_decisions()
        records = governance.audit_records()
        self.assertEqual(
            {item["event"] for item in records},
            {"admission", "ranking", "delivery", "override", "rollback"},
        )
        for record in records:
            with self.subTest(sequence=record["sequence"]):
                self.assertTrue(record["evidence"])
                self.assertEqual(len(record["record_hash"]), 64)
        verification = governance.verify_audit(anchor=governance.audit_anchor())
        self.assertTrue(verification["valid"], verification["errors"])
        self.assertEqual(verification["length"], len(records))

    def test_s4_contestation_and_recourse_records_are_linked(self):
        governance = GovernanceReference()
        governance.rank(candidates(), user_state(), {}, evidence=["ranking:contested"])
        target = governance.audit_records()[-1]["sequence"]
        contestation = governance.contest(
            target,
            claimant="user-fixture",
            reason="score explanation requested",
            requested_recourse="review and rerun",
            evidence=["contest:1"],
        )
        recourse = governance.record_recourse(
            contestation,
            reviewer="reviewer-fixture",
            outcome="ranking reproduced; reasons supplied",
            evidence=["recourse:1"],
        )
        records = governance.audit_records()
        self.assertEqual(records[contestation - 1]["payload"]["target_sequence"], target)
        self.assertEqual(records[contestation - 1]["payload"]["status"], "open")
        self.assertEqual(records[recourse - 1]["payload"]["contestation_sequence"], contestation)
        self.assertEqual(records[recourse - 1]["payload"]["status"], "recorded")
        self.assertTrue(governance.verify_audit()["valid"])

    def test_tampering_with_payload_is_detected_without_mutating_internal_log(self):
        governance = self._exercise_decisions()
        exported = governance.audit_records()
        exported[0]["payload"]["score"] = 999999
        verification = governance.verify_audit(exported)
        self.assertFalse(verification["valid"])
        self.assertTrue(any("record_hash mismatch" in error for error in verification["errors"]))
        self.assertTrue(governance.verify_audit()["valid"])

    def test_reordering_and_anchored_truncation_are_detected(self):
        governance = self._exercise_decisions()
        anchor = governance.audit_anchor()
        reordered = governance.audit_records()
        reordered[0], reordered[1] = reordered[1], reordered[0]
        self.assertFalse(governance.verify_audit(reordered)["valid"])
        truncated = governance.audit_records()[:-1]
        verification = governance.verify_audit(truncated, anchor=anchor)
        self.assertFalse(verification["valid"])
        self.assertIn("anchor length mismatch", verification["errors"])
        self.assertIn("anchor head mismatch", verification["errors"])

    def test_record_hash_matches_domain_separated_canonical_body(self):
        governance = GovernanceReference()
        governance.rank(candidates(), user_state(), {}, evidence=["rank:hash-spec"])
        record = governance.audit_records()[0]
        self.assertEqual(record["previous_hash"], "0" * 64)
        self.assertNotIn("record", record["payload"])
        body = {key: value for key, value in record.items() if key != "record_hash"}
        material = canonical_json({
            "domain": "sea-governance-record/2", "value": body,
        }).encode("utf-8")
        self.assertEqual(record["record_hash"], hashlib.sha256(material).hexdigest())
        self.assertEqual(set(body), {
            "schema", "sequence", "event", "timestamp", "evidence",
            "payload", "previous_hash",
        })

    def test_missing_evidence_is_rejected_before_append(self):
        governance = GovernanceReference()
        with self.assertRaisesRegex(ValueError, "evidence"):
            governance.rank(candidates(), user_state(), {}, evidence=[])
        self.assertEqual(governance.audit_records(), [])
        self.assertEqual(governance.audit_anchor()["length"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
