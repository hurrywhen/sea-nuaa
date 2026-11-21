#!/usr/bin/env python3
"""Deterministic and Monte-Carlo checks for the SEA v1.9 mathematical revision.

No experimental records are created.  The finite top-m calculation uses the exact
order-statistic probability in integral form; Monte Carlo is used only for a
predictive distribution and an independent numerical cross-check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sim" / "theory_v1.9"
N = NormalDist()
SQRT2PI = math.sqrt(2 * math.pi)


def cdf(x: float) -> float:
    return N.cdf(x)


def sf(x: float) -> float:
    # erfc avoids both 1-CDF cancellation and NormalDist's lower-tail underflow.
    return math.erfc(x / math.sqrt(2.0)) / 2.0


def pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / SQRT2PI


def population_recall(beta: float, pi: float, dprime: float) -> float:
    """Recall at the population mixture threshold, found by monotone bisection."""
    if not (0 < pi < 1 and 0 < beta <= 1 and dprime >= 0):
        raise ValueError("Require 0<pi<1, 0<beta<=1, dprime>=0")
    if beta == 1:
        return 1.0
    lo, hi = -12.0, 12.0 + dprime
    for _ in range(200):
        z = (lo + hi) / 2
        tail = (1 - pi) * sf(z) + pi * sf(z - dprime)
        if tail > beta:
            lo = z
        else:
            hi = z
    z = (lo + hi) / 2
    return sf(z - dprime)


def required_dprime(beta: float, pi: float, recall: float) -> float:
    """Population Gaussian requirement, including the exact-capacity boundary."""
    if not (0 < pi < 1 and 0 < beta <= 1 and 0 < recall < 1):
        raise ValueError("Require 0<pi<1, 0<beta<=1, 0<recall<1")
    b = (beta - pi * recall) / (1 - pi)
    if b < 0:
        return math.inf
    if math.isclose(b, 0.0, rel_tol=0, abs_tol=1e-15):
        return math.inf
    if b >= 1:
        return 0.0
    return max(0.0, N.inv_cdf(1 - b) + N.inv_cdf(recall))


def _log_binom_pmf(k: int, n: int, p: float) -> float:
    if k < 0 or k > n:
        return -math.inf
    if p <= 0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1:
        return 0.0 if k == n else -math.inf
    return ((math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))
            + k * math.log(p) + (n - k) * math.log1p(-p))


def _at_most_m_joint(m: int, n0: int, p0: float, n1: int, p1: float) -> float:
    """P[Bin(n0,p0)+Bin(n1,p1) <= m], computed without SciPy."""
    terms = []
    for k1 in range(0, min(m, n1) + 1):
        logp1 = _log_binom_pmf(k1, n1, p1)
        for k0 in range(0, min(m - k1, n0) + 1):
            logp0 = _log_binom_pmf(k0, n0, p0)
            terms.append(logp0 + logp1)
    if not terms:
        return 0.0
    peak = max(terms)
    if peak == -math.inf:
        return 0.0
    return min(1.0, math.exp(peak) * math.fsum(math.exp(x - peak) for x in terms))


def finite_topm_expected_recall(M: int, K: int, m: int, dprime: float,
                                nodes: int = 384) -> dict[str, float]:
    """Exact expected recall for continuous iid Gaussian scores and finite top-m.

    Conditional on one marked critical score x=d'+z, that item is selected iff at
    most m-1 of the other M-1 scores exceed x.  Those exceedances are the sum of
    independent Binomial(M-K, sf(x)) and Binomial(K-1, sf(x-d')) variables.
    Gauss-Legendre quadrature over z in [-9,9] leaves normal tail mass <2e-18.
    """
    if not (1 <= K <= M and 1 <= m < M and dprime >= 0):
        raise ValueError("Require 1<=K<=M, 1<=m<M, dprime>=0")
    x, w = np.polynomial.legendre.leggauss(nodes)
    total = 0.0
    for zi, wi in zip(x, w):
        z = 9.0 * float(zi)  # leggauss nodes are on [-1,1]; map them to [-9,9].
        threshold = dprime + z
        prob = _at_most_m_joint(m - 1, M - K, sf(threshold), K - 1, sf(z))
        total += float(wi) * pdf(z) * prob
    # dz = 9 dx under the [-1,1] -> [-9,9] mapping.
    answer = 9.0 * total
    return {
        "expected_recall": answer,
        "quadrature_nodes": nodes,
        "normal_tail_mass_outside_grid": 2 * sf(9.0),
    }


def monte_carlo_topm(M: int, K: int, m: int, dprime: float,
                     repetitions: int, seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    values = np.empty(repetitions, dtype=float)
    for r in range(repetitions):
        scores = np.concatenate((rng.standard_normal(M - K),
                                 dprime + rng.standard_normal(K)))
        # argpartition is O(M); ties have probability zero.
        selected = np.argpartition(scores, M - m)[M - m:]
        values[r] = np.sum(selected >= M - K) / K
    mean = float(values.mean())
    se = float(values.std(ddof=1) / math.sqrt(repetitions))
    return {
        "repetitions": repetitions,
        "seed": seed,
        "mean_recall": mean,
        "monte_carlo_standard_error": se,
        "monte_carlo_mean_95ci": [mean - 1.96 * se, mean + 1.96 * se],
        "realized_recall_predictive_quantiles_2.5_50_97.5": [
            float(x) for x in np.quantile(values, [0.025, 0.5, 0.975])
        ],
        "mean_absolute_error_vs_quadrature": None,
    }


def subset_choice_distribution(utilities: list[float], m: int, temperature: float,
                               reference: list[float] | None = None) -> dict[tuple[int, ...], float]:
    """KL-regularized distribution over m-subsets, with optional reference weights."""
    import itertools
    if not (1 <= m <= len(utilities) and temperature > 0):
        raise ValueError("Require 1<=m<=n and temperature>0")
    subsets = list(itertools.combinations(range(len(utilities)), m))
    if reference is None:
        reference = [1.0] * len(subsets)
    if len(reference) != len(subsets) or any(x <= 0 for x in reference):
        raise ValueError("Reference must contain one positive weight per subset")
    logw = [math.log(reference[j]) + sum(utilities[i] for i in subsets[j]) / temperature
            for j in range(len(subsets))]
    peak = max(logw)
    weights = [math.exp(x - peak) for x in logw]
    total = math.fsum(weights)
    return {subsets[j]: weights[j] / total for j in range(len(subsets))}


def online_delta_constant_reward(periods: int, b: int, reward: float = 1.0,
                                 arrival_probability: float = 1.0) -> float:
    """Evaluate Delta_i(b) with the separate b=1 and b>=2 recursions."""
    if not (periods >= 0 and b >= 1 and reward >= 0 and 0 < arrival_probability <= 1):
        raise ValueError("Require periods>=0, b>=1, reward>=0, 0<a<=1")
    previous = [0.0] * (b + 1)  # Delta_0(b)=0 for every b>=1.
    for _ in range(periods):
        current = [0.0] * (b + 1)
        a = arrival_probability
        current[1] = previous[1] + a * max(reward - previous[1], 0.0)
        for slots in range(2, b + 1):
            g_b = a * max(reward - previous[slots], 0.0)
            g_bm1 = a * max(reward - previous[slots - 1], 0.0)
            current[slots] = previous[slots] + g_b - g_bm1
        previous = current
    return previous[b]


def pareto_leakage(K: int, m: int, alpha: float) -> dict[str, float]:
    """Exact Gamma order-statistic sum and its quantile-integral approximation."""
    if not (1 <= m < K and alpha > 1):
        raise ValueError("Require 1<=m<K and alpha>1")
    vmin = 1.0
    log_terms = [
        math.log(vmin) + math.lgamma(r - 1 / alpha) + math.lgamma(K + 1)
        - math.lgamma(r) - math.lgamma(K + 1 - 1 / alpha)
        for r in range(1, m + 1)
    ]
    peak = max(log_terms)
    expected_top = math.exp(peak) * math.fsum(math.exp(x - peak) for x in log_terms)
    expected_total = K * vmin * alpha / (alpha - 1)
    exact = 1 - expected_top / expected_total
    approximation = 1 - (m / K) ** ((alpha - 1) / alpha)
    return {
        "exact_leakage_share": exact,
        "quantile_integral_approximation_using_actual_m_over_K": approximation,
        "approximation_minus_exact_percentage_points": 100 * (approximation - exact),
        "m_over_K": m / K,
    }


def weighted_coverage_counterexample() -> dict[str, float]:
    # Two equally weighted propositions, two independent classes within each proposition.
    p1, p2 = 0.9, 0.1
    exact_weighted_miss = 0.5 * (1 - p1) ** 2 + 0.5 * (1 - p2) ** 2
    pooled_mean = 0.5 * p1 + 0.5 * p2
    naive = (1 - pooled_mean) ** 2
    return {
        "weighted_expected_miss": exact_weighted_miss,
        "weighted_expected_recall": 1 - exact_weighted_miss,
        "invalid_product_of_pooled_mean_coverages": naive,
        "naive_recall_that_would_be_overstated": 1 - naive,
        "difference_in_miss": exact_weighted_miss - naive,
    }


def misspecified_binary_example(c: float = 0.2, chat: float = 0.8,
                                eta: float = 0.9) -> dict[str, float]:
    """One update rule Q_chat for every signal; latent branches are never observed."""
    if not (0 <= c <= 1 and 0 <= chat <= 1 and 0.5 < eta <= 1):
        raise ValueError("Require c,chat in [0,1], eta in (0.5,1]")
    true_accuracy = c * eta + (1 - c) * (1 - eta)
    perceived_accuracy = chat * eta + (1 - chat) * (1 - eta)
    # With equal prior and symmetric utilities, baseline expected utility is 1/2.
    # If perceived_accuracy>.5 the agent follows y, otherwise reverses it.
    realized_accuracy = true_accuracy if perceived_accuracy > 0.5 else 1 - true_accuracy
    correct_accuracy = max(true_accuracy, 1 - true_accuracy)
    W = realized_accuracy - 0.5
    VOI = correct_accuracy - 0.5
    return {
        "true_mixture_signal_accuracy": true_accuracy,
        "agent_assumed_mixture_signal_accuracy": perceived_accuracy,
        "expected_realized_value_W": W,
        "correct_model_VOI": VOI,
        "misspecification_regret": VOI - W,
    }


def rct_sizes(d: float = 0.35, alpha: float = 0.05, power: float = 0.8,
              attrition: float = 0.25) -> dict[str, Any]:
    zalpha = N.inv_cdf(1 - alpha / 2)
    zpower = N.inv_cdf(power)
    raw = 2 * (zalpha + zpower) ** 2 / d ** 2
    one_primary = math.ceil(raw)
    attrition_adjusted = math.ceil(raw / (1 - attrition))
    zalpha_two = N.inv_cdf(1 - alpha / 4)  # Bonferroni for two co-primary comparisons
    raw_two = 2 * (zalpha_two + zpower) ** 2 / d ** 2
    two_primary = math.ceil(raw_two)
    attrition_two = math.ceil(raw_two / (1 - attrition))
    return {
        "one_declared_primary_comparison": {
            "unrounded_n_per_arm": raw,
            "ceiling_before_attrition": one_primary,
            "ceiling_after_25_percent_attrition": attrition_adjusted,
            "three_arm_total": 3 * attrition_adjusted,
        },
        "two_coprimary_bonferroni_sensitivity": {
            "unrounded_n_per_arm": raw_two,
            "ceiling_before_attrition": two_primary,
            "ceiling_after_25_percent_attrition": attrition_two,
            "three_arm_total": 3 * attrition_two,
        },
        "note": ("Normal-approximation two-sample calculation, not a completed clinical "
                 "power analysis. A future protocol must declare the primary comparison "
                 "before recruitment and consider a mixed-model analysis of repeated outcomes."),
    }


def run(repetitions: int, seed: int) -> dict[str, Any]:
    beta, pi, target = 0.0125, 0.01, 0.95
    dreq = required_dprime(beta, pi, target)
    finite = []
    for j, d in enumerate((1.5, 2.5, dreq)):
        exact = finite_topm_expected_recall(800, 8, 10, d)
        mc = monte_carlo_topm(800, 8, 10, d, repetitions, seed + j)
        mc["mean_absolute_error_vs_quadrature"] = abs(mc["mean_recall"] - exact["expected_recall"])
        finite.append({
            "M": 800, "K": 8, "m": 10, "dprime": d,
            "population_threshold_recall": population_recall(beta, pi, d),
            "finite_topm": exact,
            "monte_carlo": mc,
            "expected_finite_minus_population": exact["expected_recall"] - population_recall(beta, pi, d),
        })
    result = {
        "schema": "sea.v19.math-reproduction/v1",
        "seed": seed,
        "filtering_example": {
            "ratio": 1 - 45 / (4 * 10000),
            "percent": 100 * (1 - 45 / (4 * 10000)),
        },
        "gaussian_population": {
            "beta": beta, "pi": pi, "target_recall": target,
            "required_dprime": dreq,
            "auc_at_required_dprime": cdf(dreq / math.sqrt(2)),
            "recall_dprime_1.5": population_recall(beta, pi, 1.5),
            "recall_dprime_2.5": population_recall(beta, pi, 2.5),
            "boundary_rules": {
                "beta_less_than_pi_R": "infeasible",
                "beta_equals_pi_R_with_positive_R": "infinite Gaussian separation required",
                "R_equals_1_and_beta_less_than_1": "infinite Gaussian separation required",
                "beta_equals_1": "consume everything; recall one for every dprime",
                "b_ge_1": "zero minimum separation; identical score distributions already meet the target",
            },
            "high_budget_regression": {
                "required_dprime_beta_0.9999": required_dprime(0.9999, pi, target),
                "required_dprime_beta_1": required_dprime(1.0, pi, target),
                "population_recall_beta_1": population_recall(1.0, pi, 0.0),
            },
        },
        "online_threshold_constant_reward": {
            "delta_1_1": online_delta_constant_reward(1, 1),
            "delta_1_2": online_delta_constant_reward(1, 2),
            "delta_2_1": online_delta_constant_reward(2, 1),
            "delta_2_2": online_delta_constant_reward(2, 2),
        },
        "finite_topm_examples": finite,
        "pareto_alpha_1.5_K_52": {
            "m_26": pareto_leakage(52, 26, 1.5),
            "m_42": pareto_leakage(52, 42, 1.5),
        },
        "weighted_coverage_counterexample": weighted_coverage_counterexample(),
        "misspecified_binary_example": misspecified_binary_example(),
        "rct_sample_size": rct_sizes(),
    }
    return result


def render(result: dict[str, Any]) -> str:
    g = result["gaussian_population"]
    lines = [
        "# v1.9 mathematical reproduction report",
        "",
        "All population threshold values and Pareto sums are deterministic. "
        "Finite-top-m means use quadrature; Monte Carlo intervals quantify only "
        "simulation error, not empirical uncertainty.",
        "",
        "## Population Gaussian model",
        "",
        f"- Filtering arithmetic: {result['filtering_example']['ratio']:.9f} "
        f"({result['filtering_example']['percent']:.4f}%).",
        f"- Required separation: {g['required_dprime']:.9f}; AUC {g['auc_at_required_dprime']:.9f}.",
        f"- Population recall at d'=1.5 / 2.5: {g['recall_dprime_1.5']:.9f} / "
        f"{g['recall_dprime_2.5']:.9f}.",
        "- With fixed CDF-quantile notation, a critical recall R uses Q1(1-R), "
        "hence Q1(0.05) at R=0.95. Boundary cases are recorded in summary.json.",
        "",
        "## Finite top-m selection (M=800, K=8, m=10)",
        "",
        "| d' | Population recall | Exact-formula E[finite recall] (converged quadrature) | Finite−population | MC mean [MC 95% CI] | Realized 2.5%, 50%, 97.5% quantiles |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["finite_topm_examples"]:
        mc = row["monte_carlo"]
        qs = mc["realized_recall_predictive_quantiles_2.5_50_97.5"]
        lines.append(
            f"| {row['dprime']:.7f} | {row['population_threshold_recall']:.9f} | "
            f"{row['finite_topm']['expected_recall']:.9f} | "
            f"{row['expected_finite_minus_population']:+.9f} | "
            f"{mc['mean_recall']:.9f} [{mc['monte_carlo_mean_95ci'][0]:.9f}, "
            f"{mc['monte_carlo_mean_95ci'][1]:.9f}] | "
            f"{qs[0]:.3f}, {qs[1]:.3f}, {qs[2]:.3f} |")
    lines += [
        "",
        "The finite expected recall is not obtained by plugging the empirical top-m "
        "threshold into the population identity. Predictive quantiles describe "
        "between-realization variability; the MC CI describes only numerical error "
        "in the estimated expectation.",
        "",
        "## Pareto leakage",
        "",
        "| K,m | Exact | Integral approximation at actual m/K | Approx−exact (pp) |",
        "|---|---:|---:|---:|",
    ]
    for label, row in result["pareto_alpha_1.5_K_52"].items():
        lines.append(f"| 52,{label.split('_')[1]} | {100*row['exact_leakage_share']:.6f}% | "
                     f"{100*row['quantile_integral_approximation_using_actual_m_over_K']:.6f}% | "
                     f"{row['approximation_minus_exact_percentage_points']:+.6f} |")
    w = result["weighted_coverage_counterexample"]
    b = result["misspecified_binary_example"]
    r = result["rct_sample_size"]
    lines += [
        "",
        "## Counterexamples and design calculations",
        "",
        f"- Weighted-miss example: exact {w['weighted_expected_miss']:.6f}; invalid pooled-product "
        f"{w['invalid_product_of_pooled_mean_coverages']:.6f}. A pooled class mean cannot be "
        "inserted into a proposition-wise product.",
        f"- Unified-update binary example: W={b['expected_realized_value_W']:.6f}, "
        f"correct-model VOI={b['correct_model_VOI']:.6f}, regret={b['misspecification_regret']:.6f}. "
        "The same assumed mixture likelihood is used for every observed signal.",
        f"- RCT normal approximation with one declared primary comparison: ceil before attrition "
        f"{r['one_declared_primary_comparison']['ceiling_before_attrition']}/arm; after 25% attrition "
        f"{r['one_declared_primary_comparison']['ceiling_after_25_percent_attrition']}/arm "
        f"(total {r['one_declared_primary_comparison']['three_arm_total']}).",
        f"- Two co-primary Bonferroni sensitivity: {r['two_coprimary_bonferroni_sensitivity']['ceiling_after_25_percent_attrition']}/arm "
        f"(total {r['two_coprimary_bonferroni_sensitivity']['three_arm_total']}). These are future-design calculations only.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=20261116)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.repetitions < 1000:
        raise SystemExit("Use at least 1000 Monte Carlo repetitions")
    result = run(args.repetitions, args.seed)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if not args.write:
        print(text)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    targets = [OUT / "math_results.json", OUT / "MATH_REPORT.md"]
    if any(p.exists() for p in targets) and not args.force:
        raise SystemExit("Artifacts exist; use --force to replace them")
    (OUT / "math_results.json").write_text(text + "\n", encoding="utf-8")
    (OUT / "MATH_REPORT.md").write_text(render(result), encoding="utf-8")
    source = Path(__file__).read_bytes()
    (OUT / "script_sha256.txt").write_text(hashlib.sha256(source).hexdigest() + "  reproduce_v19_math.py\n",
                                             encoding="utf-8")
    print(f"Wrote mathematical reproduction artifacts to {OUT}")


if __name__ == "__main__":
    main()
