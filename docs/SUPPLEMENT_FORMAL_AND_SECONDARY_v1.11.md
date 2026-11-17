# SEA v1.11 Supplementary Appendix: Deferred Proofs and Secondary Historical Tables

> **Status:** supporting material for the conditional-component/audit paper. The proofs concern only their stated restrictions. The tables are unchanged retrospective selected-proxy calculations on one shared corpus; they are not actual-consumption, intention-to-treat, independent-environment, decision-value, or welfare results. No new model call, experiment, or historical imputation was performed.

## SA Deferred standard proofs

### SA.1 Online threshold recursion and monotonicity (Proposition 5.4)

The Bellman equation follows by comparing consumption and discard. Subtracting $W_i(0)=0$ gives the distinct boundary recursion

$$\Delta_i(1)=\Delta_{i-1}(1)+g_a(\Delta_{i-1}(1)),$$

whereas for $b\ge2$,

$$\Delta_i(b)=\Delta_{i-1}(b)+g_a(\Delta_{i-1}(b))-g_a(\Delta_{i-1}(b-1)).$$

The function $g_a$ is nonnegative, nonincreasing, and $a$-Lipschitz with $a\le1$. Concavity is proved by induction, with base $\Delta_0(b)=0$ for $b\ge1$. At $b=2$, write $y=\Delta_{i-1}(1)\ge z=\Delta_{i-1}(2)$. Then

$$\Delta_i(1)-\Delta_i(2)=(y-z)+g_a(y)+[g_a(y)-g_a(z)]\ge0.$$

For every $b\ge3$, write $x=\Delta_{i-1}(b-2)\ge y=\Delta_{i-1}(b-1)\ge z=\Delta_{i-1}(b)$. Then

$$\Delta_i(b-1)-\Delta_i(b)=(y-z)+[g_a(y)-g_a(x)]+[g_a(y)-g_a(z)]\ge0,$$

because $g_a(y)-g_a(x)\ge0$ and $(y-z)+[g_a(y)-g_a(z)]\ge0$ by the Lipschitz property. Nonnegativity and time monotonicity follow separately: at $b=1$,

$$\Delta_i(1)=\Delta_{i-1}(1)+g_a(\Delta_{i-1}(1))\ge\Delta_{i-1}(1);$$

at $b\ge2$, the induction hypothesis $\Delta_{i-1}(b)\le\Delta_{i-1}(b-1)$ and monotonicity of $-g_a$ give $\Delta_i(b)\ge\Delta_{i-1}(b)$. This completes the proof. $\blacksquare$

### SA.2 Conditional EIG submodularity (Proposition 7.1)

For $q\notin Q$,

$$\Delta(q\mid Q)=H(Y_q\mid Y_Q,K)-H(Y_q\mid\omega,K).$$

For $Q'\subseteq Q$, conditioning reduces entropy, so

$$H(Y_q\mid Y_Q,K)\le H(Y_q\mid Y_{Q'},K),$$

and therefore $\Delta(q\mid Q)\le\Delta(q\mid Q')$. Monotonicity follows from nonnegativity of conditional mutual information. The proof uses joint conditional independence of the full query family given $(\omega,K)$; pairwise independence given only $\omega$ is insufficient. $\blacksquare$

### SA.3 Fixed-capacity KL subset choice (Proposition 7.2)

The KL-regularized objective is strictly concave over the simplex because $\lambda>0$ and $\pi^0$ is positive. Its simplex-KKT conditions give

$$p_\lambda(A)\propto\pi_A^0\exp(U(A)/\lambda),$$

and normalization yields the displayed exponential family. Inclusion probabilities are obtained by summing over every $m$-subset containing the item, not by applying a single-item logit. As $\lambda\downarrow0$, exponents dominated by the maximal subset utility determine the limit; positive reference weights determine mass among tied maximizers. For additive $U(A)=\sum_{i\in A}u_i$, every maximizer is a top-$m$ subset. $\blacksquare$

## SB Secondary historical calibers

All intervals below are exploratory whole-run percentile bootstrap intervals (10,000 resamples, seed 42). They omit shared-corpus, retrospective-label, missingness, duplicate-arbitration, backend, and model dependence. Rule A and strict-singleton C have different populations and must not be subtracted cell by cell from each other or from the designated all-existing-record descriptive caliber in the main text.

### SB.1 Rule A: nonempty selections with metric-specific cohorts

**Supplementary Table SB1. Secondary Rule A: 71,573 recall, 70,676 citation-return, and 71,618 paired-sign resolved keys.**

| Family | R/V/S keys | Selected recall | Parametric recall | $\Delta$recall [interval] | $\Delta$citation return [interval] |
|---|---|---:|---:|---:|---:|---:|
| O | 26,908 / 26,668 / 26,918 | 0.443790 | 0.413620 | +0.030170 [−0.003971, +0.064767] | −0.175016 [−0.293452, −0.053577] |
| C | 26,851 / 26,577 / 26,869 | 0.532600 | 0.403317 | +0.129283 [+0.098441, +0.158663] | +0.667380 [+0.539180, +0.802858] |
| Q | 8,916 / 8,733 / 8,926 | 0.516153 | 0.403265 | +0.112887 [+0.081432, +0.147666] | +0.426727 [+0.295044, +0.548216] |
| G | 8,898 / 8,698 / 8,905 | 0.519783 | 0.430371 | +0.089412 [+0.022924, +0.148522] | −0.219053 [−0.427112, −0.025626] |

### SB.2 Strict-singleton citation-return accounting

**Supplementary Table SB2. Strict-singleton C: 70,306 common keys; selected citation-return accounting decomposition.**

| Family | Keys | $\Delta$critical-item return | $\Delta$noncritical-item return | Total return | $\Delta$selected count |
|---|---:|---:|---:|---:|---:|
| O | 26,592 | +0.124007 | −0.299564 | −0.175557 | −0.044889 |
| C | 26,499 | +0.606797 | +0.056792 | +0.663589 | −0.009278 |
| Q | 8,641 | +0.510555 | −0.090163 | +0.420392 | −0.000936 |
| G | 8,574 | +0.410169 | −0.629270 | −0.219101 | −0.182926 |

For O, the critical-item component's exploratory interval is [−0.054770, +0.304276], crossing zero; G's is [+0.048621, +0.729638]. Noncritical-item intervals are [−0.403201, −0.186791] for O and [−0.781947, −0.459691] for G. C/Q noncritical intervals also cross zero. Positive O/G critical-item point estimates are outweighed by noncritical declines. Under the intentional favor-LLM endpoint, O/G total-return intervals include zero. The identity is accounting, not a causal explanation of substitution or changed counts. Retrospective $\log(1+\text{2026 citations})$ is not ex-ante decision utility or welfare.

### SB.3 All 17 frozen missing/conflict/endpoint scenarios

**Supplementary Table SB3. Run-equal point-estimate ranges across all 17 scenarios.**

| Family | $\Delta$recall min–max | Recall sign changes | $\Delta$citation return min–max | Return sign changes |
|---|---:|---:|---:|---:|
| O | +0.027697 to +0.033656 | 0 | −0.277317 to −0.103091 | 0 |
| C | +0.124652 to +0.133596 | 0 | +0.522966 to +0.749538 | 0 |
| Q | +0.104956 to +0.120525 | 0 | +0.159403 to +0.587765 | 0 |
| G | +0.079407 to +0.097947 | 0 | −0.507806 to −0.027918 | 0 |

Recall point estimates stay positive in all 17 scenarios; citation return stays positive for C/Q and negative for O/G. Zero point-estimate sign changes do not make every interval exclude zero and do not identify a structural effect. Exact per-scenario denominators and intervals remain in `scenario_effects.csv`.

## SC Onboarding declaration burden

**Supplementary Table SC1. What onboarding supplies and what remains unidentified.**

| Onboarding item | Formal object supplied | Objects still missing |
|---|---|---|
| Monitoring list | $\pi_{\mathrm{mon}}$ | Coverage/consumption laws and capacity feasibility |
| Time budget | $B^T$ | Compute, call, money, and risk budgets; allocation across uses |
| One-sentence $g^{(2)}$ | Candidate topics for human review | Actions, utilities/losses, horizon, harms, and emergency permissions |
| Optional emergency sheet | $\mathcal A_{\mathrm{safe}}$, triggers, undo costs | Validation; otherwise override remains disabled |

Machine writes can be architecturally guarded, while human preferences remain partly endogenous to exposure. S2 governs the machine store and does not prove that human goals are untouched by content.
