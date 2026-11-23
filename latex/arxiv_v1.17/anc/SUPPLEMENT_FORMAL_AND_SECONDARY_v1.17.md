# SEA v1.17 Supplementary Appendix: Deferred Proofs and Standard Technical Foundations

> **References:** all citations use the unified reference list in the v1.17 main manuscript.
>
> **Status:** supporting material for the conditional-component/audit paper. The proofs concern only their stated restrictions. This supplement keeps proofs, model-calculated numerical identities, and pointers only; all retrospective selected-proxy estimates (Rule A, strict-singleton, and 17-scenario tables) are retained in exactly one place, `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.17.md` §R5, regenerated from frozen data files. They are not actual-consumption, intention-to-treat, independent-environment, decision-value, or welfare results. No new model call, experiment, or historical imputation was performed.

## SA Deferred standard proofs

### SA.0 Finite observable-history existence proof (Proposition 3.1)

**Proof.** Finite actions and observations generate finitely many observable histories at each finite time. Fix a full-support behavioral reference policy $\beta$, for example the uniform distribution over each nonempty finite $\mathcal A_t(h)$. For every history $h$ with $\Pr^\beta(h)>0$ and every feasible $a$ (which has positive probability under $\beta$), condition the full generative model on $h,a$ to define $r_t(h,a)=\mathbb E[r_t\mid h,a]$ and the marginal next-observation kernel $P(y_{t+1}\mid h,a)$. Define $\bar\Phi(h)=\mathbb E[\Phi(x_{H+1})\mid h]$ at $t=H+1$ on terminal histories with positive $\beta$-probability. These conditionings integrate over latent states and do not make them policy inputs. Full support covers every history–action pair reachable under any policy. At a history with zero probability under $\beta$ (and therefore under every policy), no posterior quantity is needed: assign any fixed feasible action and arbitrary finite continuation value consistent with the recursion. Such assignments cannot change values or optimality on reachable histories. Set $V_{H+1}(h)=-\bar\Phi(h)$ on positive-probability terminal histories and recursively compute

$$V_t(h)=\max_{a\in\mathcal A_t(h)}\left\{r_t(h,a)+\gamma\sum_{y_{t+1}}P(y_{t+1}\mid h,a)V_{t+1}(h,a,y_{t+1})\right\}.$$

Every maximum is over a nonempty finite set and is attained. A fixed tie rule and concatenation prove the result without latent-state knowledge. $\blacksquare$

**Registry-version extension (main text, Section 3.2).** When the active registry $\rho_t$ and its frozen content are added to the state, the argument is unchanged provided the declared family $\mathfrak R$ is finite and each registry is frozen ex ante with a content hash: the registry component then takes values in a finite set and histories remain finite.

**Formal correspondence and scope.** Along every accepted run, the schedule position and active registry are determined by the frozen declaration and committed-period index: a due successor must be accepted before the old cohort can commit another period. Thus the schedule adds no policy-controlled or outcome-dependent branch. Proposition 3.1 concerns this finite decision abstraction, not an arbitrary wall-clock scheduler or an unlimited stream of external operator calls. Rejected transition diagnostics do not change the registry, objective, budget, or active path and add no policy action; if an application makes arbitrary exogenous calls decision-relevant, their finite observation/kernel model must be added explicitly rather than claimed to follow from this proof. Calendar windows and point-in-time availability are evaluation-design fields, not consequences of the finite-history existence argument.

**Strict actual-period boundary.** The reference control instance derives a read-only `next_period` from the committed result sequence, requiring that sequence to be exactly $0,\ldots,N-1$ and then returning $N$. `run_period(p)` accepts only integer $p=N$; duplicate, regressed, skipped, Boolean, and noninteger periods are rejected before any budget, ledger, history, or result mutation. Only a successfully committed result extends the sequence. A continuity transition shares the sequence and therefore preserves $N$ in both predecessor and successor views; a full-reset control instance starts with an empty sequence and $N=0$. For a successor declaring `switch_after_period` $=k$, acceptance requires $N=k+1$, equivalently completion of the unique actual periods $0,\ldots,k$. It therefore cannot be satisfied by repeating one period to manufacture result rows, and a manually writable counter cannot bypass it. Once that boundary is due, `run_period(k+1)` on the old cohort is rejected before any result, budget, history, or audit mutation; the scheduled transition must occur first. Every period commit also rechecks declaration integrity, so editing `switch_after_period` after seeing results cannot reopen the old cohort. Here `period` is an ordinal successful evaluation commit, not elapsed time, an attempt count, or evidence of independent/equal-duration windows. A real protocol separately freezes the period-to-observation-window/cohort map and point-in-time snapshots. The old cohort ends at $k$, the new cohort starts at $k+1$, and old outcomes are not retroactively relabeled. These are executable protocol-integrity rules; they add no policy action and leave the finite-history argument unchanged.

Registry-version transitions are **exogenous evaluation-protocol events following a fixed ex-ante schedule and frozen switch timing, not policy actions**: they add no primitive action to the attempt set, and the protocol event at each period is determined by the declared schedule position and its `switch_after_period` boundary, fixed before any arm result is read; a transition attempt outside that boundary is rejected, so the switch point cannot be selected after seeing interim results. The single-line lifecycle seals the predecessor control path at each transition, so exactly one active control path exists per control instance; sealing is a state transition, not a branching of the probability space, and no parallel control branches share a control identity. A full reset is an implementation-layer exception: it selects an allowlisted target from the finite family (backward or outside the parent schedule only if declared), starts a new control instance with a fresh single-version schedule, and seals the parent; it is not a registry rollback. The allowlist alone does not make reset exogenous, because trigger/timing and within-allowlist selection could still depend on interim outcomes. Confirmatory use requires those rules, a deterministic tie rule, and failure handling to be frozen before outcomes; otherwise reset starts an exploratory new experiment outside the primary analysis. Proposition 3.1 is per control instance and makes no global optimality or common-estimand claim across resets. Evaluation remains cohort-separated: each maximal constant-version interval along the single path uses its own $\nu^{(v)}$, and no cross-version pooling is performed. Objective rollback acts on the objective version history $\mathcal V_t$ only and never restores a registry version; continuity transitions are append-only forward along the schedule. A rejected transition leaves the registry, objective store, budget, and active path unchanged; because the audit ledger $L_t$ is part of the state, the precise statement is that only one rejection audit record is appended, with zero resource spend—not that the whole state is unmutated.

### SA.1 Online threshold recursion and monotonicity (Proposition SD.5)

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

### SA.2 Conditional EIG submodularity (Proposition SD.9)

For $q\notin Q$,

$$\Delta(q\mid Q)=H(Y_q\mid Y_Q,K)-H(Y_q\mid\omega,K).$$

For $Q'\subseteq Q$, conditioning reduces entropy, so

$$H(Y_q\mid Y_Q,K)\le H(Y_q\mid Y_{Q'},K),$$

and therefore $\Delta(q\mid Q)\le\Delta(q\mid Q')$. Monotonicity follows from nonnegativity of conditional mutual information. The proof uses joint conditional independence of the full query family given $(\omega,K)$; pairwise independence given only $\omega$ is insufficient. $\blacksquare$

### SA.3 Fixed-capacity KL subset choice (Proposition SD.10)

The KL-regularized objective is strictly concave over the simplex because $\lambda>0$ and $\pi^0$ is positive. Its simplex-KKT conditions give

$$p_\lambda(A)\propto\pi_A^0\exp(U(A)/\lambda),$$

and normalization yields the displayed exponential family. Inclusion probabilities are obtained by summing over every $m$-subset containing the item, not by applying a single-item logit. As $\lambda\downarrow0$, exponents dominated by the maximal subset utility determine the limit; positive reference weights determine mass among tied maximizers. For additive $U(A)=\sum_{i\in A}u_i$, every maximizer is a top-$m$ subset. $\blacksquare$

## SB Secondary historical calibers (single-source pointer)

The secondary Rule A, strict-singleton citation-return, and 17-scenario tables (Supplementary Tables SB1–SB3) are **not duplicated here**. Their single authoritative location is `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.17.md` §R5, which is regenerated from `sim/pilot/results/v110_consumption_caliber/scenario_effects.csv` and `sim/pilot/results/v19_recall_value_tradeoff/summary.json` by `tools/make_retrospective_tables.py` and checked for drift by the release audit. All intervals there are exploratory whole-run percentile bootstrap intervals (10,000 resamples, seed 42) that omit shared-corpus, retrospective-label, missingness, duplicate-arbitration, backend, and model dependence. Rule A and strict-singleton C have different populations and must not be subtracted cell by cell from each other or from the designated all-existing-record descriptive caliber in the main text.

## SC Onboarding declaration burden

**Supplementary Table SC1. What onboarding supplies and what remains unidentified.**

| Onboarding item | Formal object supplied | Objects still missing |
|---|---|---|
| Monitoring list | $\pi_{\mathrm{mon}}$ | Coverage/consumption laws and capacity feasibility |
| Time budget | $B^T$ | Compute, call, money, and risk budgets; allocation across uses |
| One-sentence $g^{(2)}$ | Candidate topics for human review | Actions, utilities/losses, horizon, harms, and emergency permissions |
| Optional emergency sheet | $\mathcal A_{\mathrm{safe}}$, triggers, undo costs | Validation; otherwise override remains disabled |

Machine writes can be architecturally guarded, while human preferences remain partly endogenous to exposure. S2 governs the machine store and does not prove that human goals are untouched by content.


## SD Standard technical foundations (independent supplement numbering)

The following material is retained as conditional technical foundations. It is not a collection of new general theorems. The v1.17 main text keeps only the framework-level statements and pointers.

**Numbering convention.** To avoid cross-reference ambiguity with the main manuscript, supplement results carry `SD`-prefixed numbers with the result type always stated (Definition, Proposition, Corollary); propositions and corollaries run SD.1–SD.10, and the single definition is Definition SD.1. Displayed equations carry `S`-prefixed tags. Supplementary tables carry `SC`/`SD` prefixes here; the `SB`-prefixed retrospective tables exist only in the retrospective audit supplement (§R5), which is their single source. Only Proposition 3.1 is numbered in the main text; its proof is SA.0 below. Symbol conventions follow the main text: $G_i(e)$ is source-class reference coverage, $Z_i(e)$ is operational attendance, $\Gamma_i/D$ is latent actual consumption, $c_e(S)$ is union coverage probability, $\lambda_B$ is the KKT budget shadow price, $\rho_t$ is the active frozen registry with family $\mathfrak R$ and initial law $\mu_0$ (the scalar $\rho$ in the SD.2.1 limit is a local bound ratio, not the registry), and $\mathcal V_t$ is objective version history only.

### SD.1 Expected realized value under one misspecified update rule

#### SD.1.1 Arbitrary update kernel

For decision $d$, let $P_{i,d}$ be the true joint distribution of $(\omega_d,Y_i)$, let $\mu_{i,d}$ be the agent's current prior, and let $\widehat\mu_{i,d}(\cdot\mid y)$ be **one arbitrary measurable update kernel used for every signal**. Time and deadline effects are included in $u^h_{i,d}$. Assume all displayed utilities are integrable and all required maxima are attained. Define

$$a^0_{i,d}\in\arg\max_a\mathbb E_{\mu_{i,d}}[u^h_{i,d}(a,\omega_d)],$$

$$\widehat a_{i,d}(y)\in\arg\max_a\mathbb E_{\widehat\mu_{i,d}(\cdot\mid y)}[u^h_{i,d}(a,\omega_d)].$$

**Definition SD.1 (Expected realized decision value).**

$$\mathcal W_{i,d}:=\mathbb E_{P_{i,d}}\!\left[u^h_{i,d}(\widehat a_{i,d}(Y_i),\omega_d)-u^h_{i,d}(a^0_{i,d},\omega_d)\right],\qquad v_i^*:=\sum_{d\in D}\pi_d(i)\mathcal W_{i,d}.$$

Only one update kernel appears. No genuine/adversarial branch label is observed or used to select an update rule. Gains and losses can be separated without imposing their signs: if $\Delta U_{i,d}$ is the utility increment inside the expectation and $\mathrm{Gain}_{i,d}=\mathbb E[(\Delta U_{i,d})^+]$, $\mathrm{Loss}_{i,d}=\mathbb E[(\Delta U_{i,d})^-]$, then $\mathcal W_{i,d}=\mathrm{Gain}_{i,d}-\mathrm{Loss}_{i,d}$. (Gain/loss symbols are spelled out to avoid collision with coverage $G_i(e)$ and linkage $L_i(e)$.)

#### SD.1.2 Correctly specified special case and misspecification regret

If $\mu_{i,d}=P_{i,d,\omega}$ and $\widehat\mu_{i,d}(\cdot\mid y)=P_{i,d}(\cdot\mid Y_i=y)$, the standard tower argument gives

$$\mathcal W_{i,d}=\mathbb E_y\!\left[\max_a\mathbb E(u^h_{i,d}\mid y)\right]-\max_a\mathbb E_{\mu_{i,d}}u^h_{i,d}=\mathrm{VOI}_{i,d}\ge0.$$

The complete prior, likelihood, posterior, and evaluation distribution must agree; a “correct likelihood” attached to a wrong prior is not enough.

For a parametric reliability model, let $Q_c$ be the true joint law with prior $\mu=P_\omega$ and let $Q_{\hat c}$ be the agent's assumed law. The agent always uses the posterior induced by $Q_{\hat c}$. Let $a_c^*(y)$ be the Bayes action under $Q_c$ and $\widehat a_{\hat c}(y)$ the action under $Q_{\hat c}$. Define the correctly specified value $\mathrm{VOI}_c$ and realized value $W(c,\hat c)$ relative to the same no-signal baseline.

**Proposition SD.1 (Value minus misspecification regret).** *Under the integrability and attainment assumptions above,*

$$W(c,\hat c)=\mathrm{VOI}_c-\operatorname{Regret}_c(\hat c),\tag{S4}$$

where

$$\operatorname{Regret}_c(\hat c):=\mathbb E_{Q_c}\!\left[u(a_c^*(Y),\omega)-u(\widehat a_{\hat c}(Y),\omega)\right]\ge0.$$

Consequently $W(c,\hat c)<0$ is possible exactly when the regret exceeds the correctly specified value.

**Proof.** Add and subtract $\mathbb E_{Q_c}u(a_c^*(Y),\omega)$. The regret is nonnegative because, conditional on each $y$, $a_c^*(y)$ maximizes expected utility under the true posterior $Q_c(\omega\mid y)$. $\blacksquare$

A reliability-mixture implementation is

$$\ell_{\hat c}(y\mid\omega)=\hat c\,\ell_G(y\mid\omega)+(1-\hat c)\ell_A(y\mid\omega),$$

with the corresponding single posterior $\widehat\mu(B\mid y)\propto\int_B\mu(d\omega)\ell_{\hat c}(y\mid\omega)$. The true environment may use $c\ne\hat c$, but the update rule never observes the latent $G/A$ branch. Credibility mismatch need not cause harm in every problem—different posteriors can induce the same actions—but it can cause strictly negative realized value.

#### SD.1.3 Binary counterexample

Let $\omega\sim\operatorname{Bernoulli}(1/2)$, actions be $0,1$, and utility be one for a correct action and zero otherwise. A genuine mechanism is correct with probability $\eta>1/2$; an adversarial mechanism returns the opposite state with the same probability. Under reliability $c$, the observed signal is correct with probability

$$a_c=c\eta+(1-c)(1-\eta).$$

Take $c=0.2$, $\hat c=0.8$, and $\eta=0.9$. The agent uses only $Q_{0.8}$, perceives signal accuracy $a_{0.8}=0.74>1/2$, and therefore follows every signal. The true accuracy is $a_{0.2}=0.26$, so $W=-0.24$. With the correctly specified $Q_{0.2}$, the agent reverses the signal and obtains $\mathrm{VOI}=0.24$. Hence misspecification regret is $0.48$. The negative value arises from one implementable rule applied uniformly to all observations, not from branch-contingent updating.

#### SD.1.4 Status of scoring features

Relevance, novelty, credibility, durability, and harm_avoidance can remain engineering coordinates $\phi_i$. They are not proved to be a universal sufficient statistic for value. An exact representation $W_i=F(\phi_i;K,D)$ holds only when such a map and its decision homogeneity assumptions are externally specified and validated. That is a conditional parameterization, close to a representability assumption—not evidence that the five semantic names exhaust decision value.

A useful restricted form is obtained only after additional assumptions. If $\mathrm{Gain}_{i,d}=a_d\,\mathrm{Gain}_i$, $\mathrm{Loss}_{i,d}=a_d\,\mathrm{Loss}_i$, and $A_i=\sum_d\pi_d(i)a_d$, then $v_i^*=A_i(\mathrm{Gain}_i-\mathrm{Loss}_i)$. If separately validated maps $\mathrm{Gain}_i=\mathcal U^+(\phi_i)$, $\mathrm{Loss}_i=\mathcal U^-(\phi_i)$, and $A_i=\alpha(\phi_i)$ exist, then

$$v_i^*=\alpha(\phi_i)\{\mathcal U^+(\phi_i)-\mathcal U^-(\phi_i)\}.$$

Outside those conditions the full update kernel, decision-specific utilities, and harm/loss terms remain necessary. Linear scoring on the five coordinates is a heuristic whose error must be measured, not a decision-theoretic identity.

### SD.2 Filtering: capacity, population thresholds, and finite selection

#### SD.2.1 Capacity and exact Pareto leakage

**Proposition SD.2 (Capacity and clairvoyant leakage relaxation).** *If $N$ items arrive, each costs at least $\underline\tau>0$, and the budget is $T$, then at most $T/\underline\tau$ items can be consumed. If $K$ critical propositions have nonnegative values $v_e$ and at most $m$ distinct propositions can be consumed, define $\mathcal D(\pi):=\mathbb E[\sum_{e=1}^Kv_e\mathbf 1\{e\text{ is not consumed by }\pi\}]$. Then*

$$\mathcal D(\pi)\ge\mathcal D^*:=\mathbb E\!\left[\sum_{r=m_0+1}^{K}V_{(r)}\right],\qquad m_0=\min(m,K),\tag{S5}$$

*where $V_{(1)}\ge\cdots\ge V_{(K)}$ is the decreasing rearrangement. Equality holds exactly when the consumed critical value equals the top-$m_0$ critical value almost surely; ties are allowed. The quantity $\mathcal D^*$ is a **clairvoyant/oracle relaxation**, computed using realized criticality and values. It is not generally attainable by a feasible non-anticipating SAP policy.*

**Proof.** The consumed critical value cannot exceed the sum of the $m_0$ largest values. A policy that actually attains that sum reaches equality; an oracle that sees the realization and consumes its top-$m_0$ values is one such non-implementable relaxation. $\blacksquare$

For $v_e\overset{iid}{\sim}\mathrm{Pareto}(\alpha,v_{\min})$, $\alpha>1$, the exact order-statistic expectation is

$$\mathbb E V_{(r)}=v_{\min}\frac{\Gamma(r-1/\alpha)\Gamma(K+1)}{\Gamma(r)\Gamma(K+1-1/\alpha)}.$$

Thus the **normalized expected leaked value**—a ratio of expectations, not the expectation $\mathbb E[\sum_{r>m_0}V_{(r)}/\sum_e v_e]$ of a per-realization leaked share—is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}=1-\frac{\sum_{r=1}^{m_0}\mathbb E V_{(r)}}{Kv_{\min}\alpha/(\alpha-1)}.\tag{S6}$$

As $K\to\infty$, $m\to\infty$, and $m/K\to\rho\in(0,1)$, the quantile-integral limit (Resnick, 1987) is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}\;\longrightarrow\;1-\rho^{(\alpha-1)/\alpha}.$$

At finite $K,m$, $1-(m/K)^{(\alpha-1)/\alpha}$ is therefore an approximation, not an equality. At $K=52,\alpha=1.5$, the exact/approximate pairs are 20.7999%/20.6299% for $m=26$ and 6.9191%/6.8716% for $m=42$. The latter approximation uses the actual ratio $42/52=0.807692$, not 0.8. Direct pass-through does not increase total consumption capacity; it changes how the same slots are allocated.

#### SD.2.2 Population threshold model and boundary cases

Let noncritical and critical scores have continuous distributions $F_0,F_1$ and survival functions $\bar F_0,\bar F_1$, with critical mass $\pi\in(0,1)$. At a fixed threshold $t$, the population acceptance and recall are

$$\beta(t)=(1-\pi)\bar F_0(t)+\pi\bar F_1(t),\qquad R(t)=\bar F_1(t).$$

This is a population threshold identity. It is not an exact identity for the random threshold induced by finite top-$m$ selection.

**Proposition SD.3 (Threshold feasibility).** *For $0<R<1$ and $0<\beta<1$, a counting-necessary condition is $\beta\ge\pi R$. Let $\tau_R=Q_1(1-R)$, where $Q_1$ is the ordinary CDF quantile. Assuming the survival functions are continuous and strictly decreasing on their relevant supports, a threshold with acceptance $\beta$ and recall at least $R$ exists if and only if*

$$\bar F_0(\tau_R)\le b,\qquad b:=\frac{\beta-\pi R}{1-\pi}.$$

*For equal-variance Gaussian scores separated by $d'\ge0$, the complete boundary-aware minimum is*

$$\underline d'=\begin{cases}
\text{infeasible},&b<0,\\
+\infty,&b=0,\\
\max\{0,\Phi^{-1}(1-b)+\Phi^{-1}(R)\},&0<b<1,\\
0,&b\ge1.
\end{cases}$$

**Proof.** At $\tau_R$, critical recall is $R$. If the displayed inequality holds, total acceptance there is at most $\beta$. Because $\beta<1$, lowering the threshold continuously fills the budget and cannot reduce critical recall. Conversely, any threshold with recall at least $R$ must satisfy $t\le\tau_R$, so the noncritical contribution is at least $\bar F_0(\tau_R)$; budget feasibility requires the inequality. For $0<b<1$, the Gaussian expression follows from $z=\Phi^{-1}(1-b)$ and $z-d'=-\Phi^{-1}(R)$. When $b\ge1$, the threshold condition is automatic and identical score distributions ($d'=0$) already give recall $\beta\ge R$. $\blacksquare$

The remaining boundaries are separate. If $\beta<\pi R$ (equivalently $b<0$), the target is impossible even for perfect ranking. For a nondegenerate finite Gaussian $d'$, $b=0$ (equivalently $\beta=\pi R$) requires infinite separation when $R>0$. Likewise $R=1$ with $\beta<1$ requires infinite separation; $\beta=1$ is handled outside the theorem as the trivial consume-everything rule with recall one for every $d'$. If $Q_1$ is a CDF quantile, 95% critical recall uses $Q_1(0.05)$, not $Q_1(0.95)$.

At the **proposition-level** parameters $\beta=0.0125,\pi=0.01,R=0.95$,

$$\underline d'=4.389337888,\qquad \mathrm{AUC}=\Phi(\underline d'/\sqrt2)=0.999044514.$$

Population recalls at $d'=1.5$ and $2.5$ are 0.209639680 and 0.523766570. By contrast, the illustrative document-level parameter $\beta=0.001$ gives $R\le\beta/\pi=0.1$, so 95% is capacity-infeasible irrespective of separation. These are model calculations, not evidence that dual channels are necessary for every retrieval architecture.

#### SD.2.3 Finite top-$m$: exact formula evaluated by quadrature

Let $M$ be finite. All $M$ scores are mutually independent, with $K$ critical scores drawn from $F_1$ and $M-K$ noncritical scores drawn from $F_0$. Select exactly the $m$ largest scores, $1\le m<M$. The threshold is an order statistic, not the population threshold above.

**Proposition SD.4 (Finite-pool expected recall).** *For continuous scores and $K\ge1$, symmetry among critical items gives*

$$\mathbb E R_{M,K,m}=\int f_1(x)\Pr\{N_0(x)+N_1(x)\le m-1\}\,dx,$$

*where, conditional on one marked critical score $x$,*

$$N_0(x)\sim\operatorname{Binomial}(M-K,\bar F_0(x)),\qquad N_1(x)\sim\operatorname{Binomial}(K-1,\bar F_1(x)),$$

*independently. The marked critical item is selected exactly when at most $m-1$ other scores exceed it.*

For the Gaussian example $M=800,K=8,m=10$, deterministic Gauss–Legendre quadrature and 20,000 independent Monte Carlo realizations give Supplementary Table SD1.

**Supplementary Table SD1. Population thresholds versus finite-pool top-$m$ selection.**

| $d'$ | Population threshold recall | Exact-formula $\mathbb E R_{800,8,10}$ (converged quadrature) | Realized recall 2.5%, 50%, 97.5% quantiles |
|---:|---:|---:|---:|
| 1.5 | 0.209640 | 0.208661 | 0.000, 0.250, 0.500 |
| 2.5 | 0.523767 | 0.524234 | 0.250, 0.500, 0.875 |
| 4.389338 | 0.950000 | 0.952626 | 0.750, 1.000, 1.000 |

The Monte Carlo estimate at the required separation is 0.952825 with numerical 95% interval [0.951825, 0.953825]. That interval quantifies Monte Carlo error in the mean only. The predictive quantiles describe variation across finite pools; neither is an empirical confidence interval. The finite expectation is close to, but not identical with, the population value and should not be replaced by the random top-$m$ threshold in Proposition SD.3. Reproduction code and quadrature-convergence tests accompany the paper.

#### SD.2.4 Coverage–diversity objectives: inherited guarantees and their limits

For candidate set $A$, consider

$$U(A)=\sum_{e\in E}v_e\mathbf 1\{A\cap D_e\ne\varnothing\}+\mu\sum_{\sigma\in\mathcal S}\max_{i\in A}\operatorname{sim}(\sigma,i)-\lambda\sum_{i\in A}\hat m_i\tau_i,$$

with nonnegative values, similarities, costs, and weights, and the convention $\max_{i\in\varnothing}\operatorname{sim}(\sigma,i)=0$. The first term is weighted coverage and the second is facility-location diversity. Both are nonnegative, monotone, and submodular. The complete penalized objective remains submodular but need not be monotone.

Write $f(A)$ for the sum of the coverage and diversity terms. One explicit sufficient restriction is a ground set $\mathcal C_M$ such that, **for every** $i\in\mathcal C_M$ and **every** $A\subseteq\mathcal C_M\setminus\{i\}$,

$$f(A\cup\{i\})-f(A)\ge\lambda\hat m_i\tau_i.$$

Then $U$ is nonnegative and monotone throughout the subsets of $\mathcal C_M$; the condition is not a minimum taken only over positive-gain contexts, and zero-gain contexts cannot be silently discarded. For a cardinality domain $\{A\subseteq\mathcal C_M:|A|\le m\}$, standard ordinary greedy on $U$ inherits $1-1/e$ relative to the optimum **within that restricted domain**. For a knapsack domain $\{A\subseteq\mathcal C_M:\sum_{i\in A}c_i\le B\}$ with $c_i>0$, the specific combination of density greedy on $U$ and the best feasible singleton inherits $\tfrac12(1-1/e)$; depth-three partial enumeration with greedy completion inherits $1-1/e$ under the corresponding standard conditions (Leskovec et al., 2007; Sviridenko, 2004). Unaugmented density greedy is assigned neither ratio. Without the displayed restriction, only the unpenalized monotone objective receives these statements automatically.

This is the same algorithmic lineage as diversified retrieval and submodular summarization. The engineering contribution is the audit requirement to log monotonicity certificates, algorithm variant, residual capacities, and restricted optimum—not a new approximation theorem.

#### SD.2.5 Online thresholds with explicit boundaries

Suppose an item arrives independently with probability $a\in(0,1]$ in each period; conditional on arrival, its reward $R=r(S)$ is iid with $\mathbb E R^+<\infty$ and $r$ strictly increasing. At most $b$ items can be consumed over the remaining periods and discarding is irrevocable. Let $W_i(b)$ be optimal continuation value and $\Delta_i(b)=W_i(b)-W_i(b-1)$.

**Proposition SD.5 (Threshold policy).** *With $W_i(0)=W_0(b)=0$ and $g_a(\tau)=a\mathbb E[(R-\tau)^+]$,*

$$W_i(b)=W_{i-1}(b)+g_a(\Delta_{i-1}(b)).$$

*It is strictly optimal to consume when $r(s)>\Delta_{i-1}(b)$ and not optimal when $r(s)<\Delta_{i-1}(b)$; either action is optimal on ties. Moreover $\Delta_i(b)$ is nonnegative, nonincreasing in $b$, and nondecreasing in $i$.*

The boundary-aware induction, including the distinct $b=1$ recursion and the Lipschitz argument, is deferred to Supplementary Appendix SA.1 (`docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.17.md`). A finite cooling queue introduces occupancy, age, eviction, and decay states; this result does not establish a double-threshold queue policy.

### SD.3 Recall as weighted expected omission

#### SD.3.1 Separate source coverage from end-to-end delivery

Fix a monitoring set $S$ and proposition $e$. Let $G_i(e)$ denote authentic coverage by source class $i$, with $p_i(e)=P(G_i(e)=1)$, and define

$$C_S(e)=\bigcup_{i\in S}G_i(e),\qquad c_e(S)=P(C_S(e)).$$

Let $D_S(e)$ be actual consumption of $e$ through the monitored channel, with $D_S(e)\subseteq C_S(e)$. When $c_e(S)>0$, define the complete delivery conversion probability

$$\delta_e(S):=P(D_S(e)\mid C_S(e)).$$

It includes ingestion, authentication, proposition linking, deduplication, quota allocation, selection, delivery, opening, and latent actual consumption (theoretical terminal). When $c_e(S)=0$, actual consumption is zero and $\delta_e$ need not be defined; the convention $c_e(S)\delta_e(S)=0$ is used in the identities below.

**Proposition SD.6 (Coverage–consumption identity and weighted omission).** *For each $e$, the actual miss probability is*

$$m_e(S):=P(\operatorname{miss}_S(e))=1-c_e(S)\delta_e(S).\tag{S7}$$

*For target weights $w_e\ge0$ with $W=\sum_ew_e>0$, define $\nu_e=w_e/W$. Then*

$$\mathcal M_\nu(S):=\sum_e\nu_em_e(S),\qquad \mathcal R_\nu(S):=1-\mathcal M_\nu(S)=\sum_e\nu_ec_e(S)\delta_e(S).\tag{S8}$$

*These are weighted mean recall and expected omission, not $\inf_e P(D_S(e))$.*

**Proof.** Since $D_S\subseteq C_S$, $P(D_S)=P(C_S)P(D_S\mid C_S)=c_e\delta_e$. The weighted identities follow by linearity. $\blacksquare$

If $\{G_i(e)\}_{i\in J_e}$ are mutually independent on a certified subset $J_e\subseteq S$, then

$$c_e(S)\ge1-\prod_{i\in J_e}(1-p_i(e)),$$

Write $P_J:=\prod_{i\in J_e}(1-p_i(e))$. If $J_e=S$ and the full family is independent, then $c_e(S)=1-P_J$ and the pointwise decomposition is exactly

$$m_e(S)=P_J+(1-P_J)(1-\delta_e(S)).$$

For a proper certified independent subset $J_e\subsetneq S$, the same expression is generally only an upper bound:

$$m_e(S)=1-c_e(S)\delta_e(S)\le P_J+(1-P_J)(1-\delta_e(S)),$$

because $c_e(S)\ge1-P_J$. In both cases the first term represents independent-subset noncoverage and the second discounts delivery loss. Perfect pass-through $\delta_e=1$ is only a special case, not an empirical default.

Without independence, the Fréchet bounds use only marginal coverage probabilities:

$$\max\left\{0,1-\sum_{i\in S}p_i(e)\right\}\le P\!\left(\bigcap_{i\in S}G_i(e)^c\right)\le1-\max_{i\in S}p_i(e).$$

Both bounds are sharp when only the marginals are known. In particular, $c_e(S)\ge\max_{i\in S}p_i(e)$ requires no independence certificate.

#### SD.3.2 Certifiable average bounds and a counterexample to pooled products

**Corollary SD.7 (Weighted lower recall certificates).** *If logs or a structural model provide $c_e(S)\ge\underline c_e(S)\ge0$ and $\delta_e(S)\ge\underline\delta_e(S)\ge0$, then*

$$\mathcal R_\nu(S)\ge\sum_e\nu_e\underline c_e(S)\underline\delta_e(S),\qquad
\mathcal M_\nu(S)\le1-\sum_e\nu_e\underline c_e(S)\underline\delta_e(S).$$

*If $\mathcal M_\nu(S)\le\varepsilon$, then for every $\eta\in(0,1]$, the weight of propositions with pointwise miss probability above $\eta$ satisfies*

$$\nu\{e:m_e(S)>\eta\}\le\varepsilon/\eta.$$

The first statement follows from Proposition SD.6 and monotonicity. The tail statement is Markov's inequality for bounded $m_e$. It limits the weight of poorly covered propositions without pretending that every proposition has high recall.

A pooled class mean cannot be inserted into a proposition-wise product. Suppose two equally weighted propositions have class-coverages $p_i(e_1)=0.9$ and $p_i(e_2)=0.1$ for two classes, with independence within each proposition and perfect delivery. The correct weighted omission is

$$\tfrac12(0.1)^2+\tfrac12(0.9)^2=0.410.$$

The pooled class mean is 0.5, but $(1-0.5)^2=0.250$, which would overstate recall as 0.75 rather than the correct 0.59. Joint list coverage is already a union outcome; exponentiating it again would also count redundancy twice.

The former $(1-p_{\min})^{k_{\mathrm{eff}}}$ expression is therefore not used as the main estimand. If a uniform pointwise theorem is desired, it needs a genuine per-class, per-proposition floor and a certified independent subset. Degenerate floors also invalidate the old universal tightness statement: under its perfect-delivery assumption, omission one almost surely forces every coverage indicator to vanish almost surely; those degenerate indicators are mutually independent, so an arbitrary smaller effective independent-subset size cannot be constructed. The present Fréchet and weighted formulations avoid assigning an empirical value to $k_{\mathrm{eff}}$ altogether.

#### SD.3.3 Two channels: failure-weighted recovery, not pooled recovery

Let $D_{\mathrm I}(e)$ and $D_{\mathrm II}(e)$ denote actual consumption by two channels, $q_e=P(D_{\mathrm I}(e)^c)$, and, when $q_e>0$,

$$R_{\mathrm{II}}(e):=P(D_{\mathrm II}(e)\mid D_{\mathrm I}(e)^c).$$

When $q_e=0$, omission is zero and the convention $q_e[1-R_{\mathrm{II}}(e)]=0$ is used without defining $R_{\mathrm{II}}(e)$.

**Proposition SD.8 (Total omission without cross-channel independence).**

$$P(\operatorname{miss}(e))=q_e[1-R_{\mathrm{II}}(e)],\qquad
\mathcal M_\nu^{\mathrm{tot}}=\sum_e\nu_eq_e[1-R_{\mathrm{II}}(e)].$$

If $Q_\nu=\sum_e\nu_eq_e>0$ and $\bar R_{\mathrm{II},q}:=Q_\nu^{-1}\sum_e\nu_eq_eR_{\mathrm{II}}(e)$, then

$$\mathcal M_\nu^{\mathrm{tot}}=(1-\bar R_{\mathrm{II},q})Q_\nu.$$

The recovery mean is weighted by Channel-I failure $q_e$, not by all opportunities and not by an unweighted pooled count. No independence between channels is assumed. A pooled recovery computed on a selected subpopulation does not identify a uniform per-proposition recovery floor.

#### SD.3.4 An explicit availability-to-consumption decomposition: two ledgers

Audit the nested indicators $A_i(e)$ (reference availability), $L_i(e)$ (ingestion/authentication/linkage), $Q_i(e)$ (quota selection), $\Delta_i(e)$ (delivery), $O_i(e)$ (opening), $Z_i(e)$ (operational attendance measurement), and $\Gamma_i(e)$ (latent actual consumption, not the operational measurement). The theoretical terminal item event is $D_i(e)=A_iL_iQ_i\Delta_iO_i\Gamma_i$, consistent with $D_S(e)$ in Proposition SD.6. `picked` identifies at most $Q_i$; it does not identify $\Delta_i,O_i,Z_i$, or $\Gamma_i$. Missing stage receipts must carry an explicit unknown status rather than being silently interpreted as either success or abstention.

Define availability-only omission $M_A(e)=\cap_{i\in S}A_i(e)^c$ and total omission $M(e)=\cap_{i\in S}D_i(e)^c$. Then

$$M(e)=M_A(e)\;\dot\cup\;\big[M(e)\cap M_A(e)^c\big],$$

so

$$P(M(e))=P(M_A(e))+P\big(M(e)\cap M_A(e)^c\big).$$

The terms are source-availability omission and loss after at least one authentic item was available. For multiple candidate items, an arbitrary item's first failure does **not** partition a target's omission. Define cumulative target successes $\widetilde A=\cup_iA_i$, $\widetilde L=\cup_i(A_iL_i)$, $\widetilde Q=\cup_i(A_iL_iQ_i)$, $\widetilde\Delta=\cup_i(A_iL_iQ_i\Delta_i)$, and $\widetilde O=\cup_i(A_iL_iQ_i\Delta_iO_i)$.

**Theoretical ledger.** With $D_S=\cup_iD_i$, the disjoint first-failed-stage events are $\widetilde A^c$, $\widetilde A\cap\widetilde L^c$, $\widetilde L\cap\widetilde Q^c$, $\widetilde Q\cap\widetilde\Delta^c$, $\widetilde\Delta\cap\widetilde O^c$, and $\widetilde O\cap D_S^c$; they partition total latent omission into availability, linkage, quota, delivery, opening, and latent-consumption losses. This ledger defines $\mathcal M_\nu$ and is **not executable from operational telemetry alone**, because $\Gamma_i$ is unobserved.

**Executable operational/FC ledger.** With valid positive operational attendance $Z_S^+=\cup_i(A_iL_iQ_i\Delta_iO_i\mathbf1\{Z_i=1\})$, the same construction ends with $\widetilde O\cap(Z_S^+)^c$; unknown terminal measurements are flagged inside that final event and are never rewritten as observed non-attendance. This ledger computes the failure-composite omission $\mathcal M_\nu^{FC}$ (main text, Section 4.3). The synthetic executor implements only this operational/FC partition; every `latent_actual_consumption` field remains null. The two ledgers coincide only under the additional measurement-consistency assumption that non-unknown $Z$ perfectly classifies $D$; otherwise they are different estimands, and the operational contrast bounds of main-text equation (6) do not bound the latent contrast.

**Sharp operational-attendance contrast bounds (main-text equation 6).** Let $U_a$ be the unknown-target set in arm $a$, with $u_a=\sum_{j\in U_a}\nu_j$. For any completion of those unknown operational outcomes,

$$\mathcal M_{\nu,a}^{FC}-\mathcal M_{\nu,a}^{Z}=\sum_{j\in U_a}\nu_j\mathbf 1\{Z_{aj}=1\}\in[0,u_a],$$

because the failure-composite rule counts every unknown as omission, whereas the completed operational estimand counts exactly the unknowns assigned to attendance as successes. Hence $\mathcal M_{\nu,sea}^{Z}\in[\mathcal M_{\nu,sea}^{FC}-u_{sea},\mathcal M_{\nu,sea}^{FC}]$ and $\mathcal M_{\nu,control}^{Z}\in[\mathcal M_{\nu,control}^{FC}-u_{control},\mathcal M_{\nu,control}^{FC}]$. Subtracting the control interval from the SEA interval gives equation (6). The lower endpoint is attained by assigning every SEA unknown to operational success and every control unknown to operational failure; reversing both assignments attains the upper endpoint. These joint assignments are feasible when, as stated, no cross-arm or missingness-mechanism restriction is imposed. The bounds are therefore sharp for the **operational** contrast, not merely conservative widths; additional cross-arm restrictions could change them, and neither endpoint is a latent-consumption bound without measurement assumptions. $\blacksquare$

**Conditional transport under an explicit measurement-error model.** If completed (non-unknown) measurements in arm $a$ have sensitivity $se_a=P(Z=1\mid D=1)$ and specificity $sp_a=P(Z=0\mid D=0)$ with $se_a+sp_a>1$, then the operational positive probability $q_a=P(Z=1)$ and latent consumption probability $\pi_a=P(D=1)$ satisfy $q_a=se_a\,\pi_a+(1-sp_a)(1-\pi_a)$, hence

$$m^{D}_a=\frac{m^{Z}_a-(1-se_a)}{se_a+sp_a-1},\tag{S12}$$

where $m^{Z}_a=1-q_a$ is operational omission among completed measurements and $m^{D}_a=1-\pi_a$ is latent omission. Perfect measurement ($se_a=sp_a=1$) gives $m^{D}_a=m^{Z}_a$; false negatives alone can make $m^{Z}_a>0$ while $m^{D}_a=0$. This is an explicit-error-model transport, not an assumption-free bound: it applies only to completed measurements (unknowns remain governed by the operational bounds), requires arm-specific error rates estimated on an independent blinded validation set, with uncertainty propagation for all three inputs and their dependence. Arm-differential error can move the latent contrast outside the operational bounds even with no unknowns, which is why the future protocol preregisters misclassification validation and arm-differential error comparison before outcome unlock.

**Validation-to-deployment transportability.** The rates $se_a,sp_a$ are estimated on an independent blinded validation set. Applying them to the final locked corpus requires, beyond the explicit error model, conditional stability of the error rates between the validation and deployment populations:

$$P_{\mathrm{validation}}(Z=1\mid D=1,a)=P_{\mathrm{deployment}}(Z=1\mid D=1,a),$$

$$P_{\mathrm{validation}}(Z=0\mid D=0,a)=P_{\mathrm{deployment}}(Z=0\mid D=0,a).$$

These are assumptions, not consequences of (S12). Differences in corpus domain, user population, or measurement-completion mechanism can break them, and the completed-measurement subset must itself be checked for representativeness against all assigned units by arm and stage. The assumptions must be examined, not merely declared: the reference helper `transportability_stratified_diagnostics` reports stratum-specific sensitivity/specificity, their denominators and counts, stratum-specific completion rates, completed-subset stratum-share shifts relative to all assigned units, and—when deployment records are supplied—validation-to-deployment completion-rate gaps and strata missing on either side. Sensitivity and specificity have separate estimability flags and reasons: a stratum with only truth-positive units can still inform sensitivity, but not specificity. For each rate separately, cross-stratum heterogeneity is constructed only when at least two strata and the pooled rate are estimable; one stratum's trivial zero deviation from the pool is not evidence of no heterogeneity. The overall maximum pools only the rate-specific deviations whose cross-stratum comparison is defined. These diagnostics support, but never prove, transportability: deployment error rates remain unobserved, and a large small-sample deviation is not by itself proof of transport failure. When comparability is doubtful, the protocol requires covariate standardization or stratified estimation of the error rates, or a preregistered error-rate sensitivity grid, rather than silently transporting point estimates.

**Small-sample and zero-completion semantics.** For $x$ successes among $n>0$ units and $z=1.959963984540054$, the helper reports the standard Wilson score interval (Wilson, 1927)

$$\frac{\hat p+z^2/(2n)\pm z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n},\qquad \hat p=x/n,$$

intersected with $[0,1]$ to guard only against floating-point boundary roundoff. Sensitivity uses $(x,n)=(tp,tp+fn)$, specificity uses $(tn,tn+fp)$, and completion uses completed/assigned counts. A zero denominator yields `None`, not a Wald zero-width interval. These are unit-level, marginal 95% intervals under a binomial approximation, not cluster-adjusted or simultaneous intervals; their Cartesian product is not a joint confidence region for (S12). Clustered designs require a design-consistent cluster method, and joint transported uncertainty still requires the covariance or joint-bootstrap analysis below. If multiple arms, strata, or metrics form an inferential reporting family, simultaneous confidence and multiplicity handling must be fixed before unlock; otherwise these marginal intervals are descriptive diagnostics. Small strata must retain their numerators, denominators, and non-estimability reasons alongside every interval.

If no measurements are complete, overall completion is exactly 0 and its Wilson interval remains defined, but completed-subset stratum shares are $0/0$. The helper therefore returns `complete_subset_share_shift_by_stratum= None` for every stratum, `max_share_shift=None`, `completion_subset_share_shift="not_estimable"`, `sensitivity_specificity_estimable=False`, `completion_warning=True`, `representativeness_warning=True`, and `reason="no_completed_measurements"`. Assigned, completed (explicit zeros), and unknown counts remain visible, and no pooled error-rate exception is allowed to suppress these completion diagnostics. Single-truth-class, single-completed-stratum, entirely unknown-stratum, and missing-deployment-stratum cases likewise return structured reasons. With no common validation/deployment strata, `max_completion_rate_gap=None`, not zero. None of these outputs establishes representativeness or measurement validity.

**Population feasibility and precision near a zero denominator.** Write $J_a=se_a+sp_a-1$ and $N_a=m_a^Z-1+se_a$. For **exact population values** with $J_a>0$, identity (S12) satisfies $0\le m_a^D\le1$ if and only if

$$1-se_a\le m_a^Z\le sp_a.$$

At $J_a=0$, $q_a=se_a$ independently of $\pi_a$: if $N_a=0$, every $\pi_a$ gives the same operational positive probability and latent omission is unidentified; if $N_a\ne0$, no compatible population $\pi_a$ exists. Negative $J_a$ lies outside this protocol's declared positive-Youden model and is not conflated with those two zero-denominator cases. The sensitivity grid therefore excludes nonpositive-$J_a$ cells **under that preregistered rule**, while returning separate zero-denominator reasons rather than silently dropping them.

For finite-sample plug-ins, an estimate outside $[0,1]$ flags violation of the exact population constraints by that estimated quadruple **or sampling instability**, potentially amplified by a small $J_a$; it does not by itself prove that the true error model is false. It must be reported without clipping. The reference implementation reports $J_a$, the common delta-scale factor $1/J_a^2$ qualified below, and a precision warning below a declared threshold (default 0.1). When the warning fires, the analysis uses the preregistered grid (`completed_measurement_transport_sensitivity_grid`) and reports its range and out-of-unit fraction instead of relying on one transported estimate or a normal-approximation interval.

**Dependent inputs: covariance terms or design-consistent resampling.** With $N=m^{Z}_a-1+se_a$, the delta-method partial derivatives are $\partial/\partial se_a=(J_a-N)/J_a^2$, $\partial/\partial sp_a=-N/J_a^2$, and $\partial/\partial m^{Z}_a=1/J_a$. Equivalently, writing $f=N/J_a$, the gradient is $J_a^{-1}(1-f,-f,1)$. The **first-order asymptotic approximation**, not an exact finite-sample variance, is

$$\widehat{\mathrm{Var}}_{\Delta}(\widehat m^{D}_a)\approx\frac{(1-f,-f,1)\Sigma(1-f,-f,1)^\top}{J_a^2},$$

or, expanded,

$$\widehat{\mathrm{Var}}_{\Delta}(\widehat m^{D}_a)\approx d_{se}^2\,\widehat{\mathrm{Var}}(se_a)+d_{sp}^2\,\widehat{\mathrm{Var}}(sp_a)+d_{m}^2\,\widehat{\mathrm{Var}}(m^{Z}_a)+2d_{se}d_{sp}\,\widehat{\mathrm{Cov}}(se_a,sp_a)+2d_{m}d_{se}\,\widehat{\mathrm{Cov}}(m^{Z}_a,se_a)+2d_{m}d_{sp}\,\widehat{\mathrm{Cov}}(m^{Z}_a,sp_a).$$

Thus $J_a^{-2}$ is a common factor, but it is the complete divergence order only when $f$ and the quadratic form remain stable. If $J_a\to0$ with fixed $N\ne0$, then $f=N/J_a$ itself diverges and the variance can be of order $J_a^{-4}$ (when its leading quadratic coefficient is nonzero). The helper's `variance_amplification_factor` denotes only the common delta-gradient scale, not a universal asymptotic rate or calibrated coverage claim.

The helper `completed_measurement_transport_delta_method` accepts all three covariance terms. Zero covariances encode a **zero-covariance approximation**, not independence: zero covariance does not imply independence, and shared-sample estimators can have zero empirical covariance by chance. Independence may be invoked only with separate sampling-design evidence; it is neither inferred nor required for the quadratic-form calculation. Shared or clustered units require all dependent covariance terms or design-consistent joint resampling of every dependent estimator. Manually supplied inputs must also be jointly feasible. In the order $(se_a,sp_a,m_a^Z)$, write

$$\Sigma=\begin{pmatrix}v_{se}&c_{se,sp}&c_{m,se}\\c_{se,sp}&v_{sp}&c_{m,sp}\\c_{m,se}&c_{m,sp}&v_m\end{pmatrix}.$$

The implementation checks that $\Sigma$ is positive semidefinite, rather than merely checking the scalar quadratic form along the S12 gradient. Every zero-variance coordinate must have exactly zero covariances; the remaining positive-variance principal submatrix is checked in normalized form. For three positive variances this requires every $|r_{ij}|\le1$ (all diagonal and $2\times2$ principal minors nonnegative) **and** $\det R=1+2r_{01}r_{02}r_{12}-r_{01}^2-r_{02}^2-r_{12}^2\ge0$; with zero-variance coordinates, the same principal-minor criterion is applied after their required zero rows/columns are established. Pairwise correlations use sequential division to avoid raw variance-product overflow/underflow. Acceptance therefore means **PSD according to the dimensionless $10^{-12}$ roundoff tolerance**, not exact arithmetic beyond that tolerance. Thus a large unrelated variance cannot hide an illegal small-variance subblock. For example, unit variances with correlations $(0.9,0.9,-0.9)$ have nonnegative pairwise minors but determinant $-2.888$ and are rejected even though the worked S12 direction has positive scalar variance. Materially negative or nonfinite transported variance is also rejected, never silently corrected. **PSD is only algebraic admissibility of the supplied matrix.** It does not show that its variance/covariance entries are accurately estimated, that the delta-method normal approximation is calibrated, that validation error rates transport to deployment, or that an interval has nominal coverage when $J_a$ is small or units are clustered. Those are separate sampling and calibration questions; a valid $\Sigma$ cannot substitute for design-consistent uncertainty estimation or a sensitivity analysis.

One limited alternative is `completed_measurement_transport_joint_bootstrap`: paired validation records (test result, reference truth) are resampled jointly, re-estimating **only** $se_a$ and $sp_a$ together in each replicate; with a cluster key, whole clusters are resampled. The helper holds $m^{Z}_a$ fixed and is therefore applicable only when that value is treated as externally fixed—for example, when it comes from a separate deployment operational sample whose uncertainty is explicitly left unmodeled. It is **not** a three-input joint bootstrap. If $se_a,sp_a,m^{Z}_a$ share sampling units, the analysis must jointly resample all three under the actual design or supply their full covariance; calling this two-input helper would omit their dependence.

Replicates with a nonpositive Youden denominator or a lost truth class are counted and reported, never silently dropped, but they are excluded from the percentile calculation. The reported percentile interval is consequently **conditional on nondegenerate replicates**, not an unconditional resampling distribution. Few clusters, unstable $J_a$, or a high degenerate-replicate fraction can make that conditional interval unrepresentative and preclude an automatic calibration claim; these conditions must be reported and the preregistered sensitivity grid used. Both helpers are method demonstrations on synthetic paired records, not completed measurement validation, and the transportability assumption still applies.

The worked example has one candidate per target, so its table is a special case. The stage figure below and main-text Figure 2 make clear why selected-proxy recall is an upper bound on terminal consumption for the same logged population, but not necessarily for an all-assigned population whose missing records were excluded upstream.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[font=\scriptsize,
 stage/.style={draw,rounded corners,minimum height=9mm,align=center,inner sep=2pt,text width=1.65cm},
 arr/.style={-{Latex[length=1.7mm]},thick}]
\node[stage] (a) at (0,0) {reference availability};
\node[stage] (l) at (2.4,0) {ingested and linked};
\node[stage] (q) at (4.8,0) {quota selected};
\node[stage] (d) at (7.2,0) {delivered};
\node[stage] (o) at (9.6,0) {opened};
\node[stage] (c) at (12,0) {operational attendance};
\draw[arr] (a)--(l); \draw[arr] (l)--(q); \draw[arr] (q)--(d);
\draw[arr] (d)--(o); \draw[arr] (o)--(c);
\node[draw,rounded corners,align=center,inner sep=4pt,text width=11.4cm] (loss) at (6,-2.2)
 {First-failed-stage ledger: availability; linkage; quota; delivery; opening; attendance. Latent consumption remains unobserved.};
\draw[arr] (a)--(loss.north -| a); \draw[arr] (l)--(loss.north -| l);
\draw[arr] (q)--(loss.north -| q); \draw[arr] (d)--(loss.north -| d);
\draw[arr] (o)--(loss.north -| o); \draw[arr] (c)--(loss.north -| c);
\end{tikzpicture}
\caption{Staged omission from reference availability to operational attendance. The executable ledger terminates in operational attendance; latent actual consumption is a separate theoretical terminal. Historical \texttt{picked} logs stop at selection.}
\label{fig:supplement-omission-stages}
\end{figure}

A claim of zero filtering-induced omission applies only conditional on the specified availability, linkage, and terminal events of the declared ledger; it is not an unconditional zero-miss guarantee.

#### SD.3.5 What Clopper–Pearson can and cannot certify

Freeze the monitoring set and the complete policy. Suppose $n$ independent target–environment–evaluation units are generated, with target $E_j$ sampled from $\nu$ and with an independent realization of the complete pipeline, including its environment, quotas, and implementation randomness. Independent corpora or months—not thousands of shared-corpus agent-days—are the relevant inferential units for temporal deployment. Observe the **end-to-end actual-consumption** omission indicators

$$X_j=\mathbf 1\{\text{no monitored channel actually consumes }E_j\},\qquad X=\sum_{j=1}^nX_j.$$

Under this independent-unit superpopulation model, $X_j\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(\mathcal M_\nu(S))$, so $X\sim\operatorname{Binomial}(n,\mathcal M_\nu(S))$ regardless of dependence among source classes within a proposition. This is a **theoretical-ledger** statement: $X_j$ requires observing latent actual consumption. Operational telemetry alone instantiates $X_j$ only under the measurement-consistency assumption that non-unknown attendance measurements perfectly classify $D$; without it, the same construction estimates the failure-composite mean $\mathcal M_\nu^{FC}$ (or operational attendance omission under a declared unknown assignment), not $\mathcal M_\nu$. Independent target labels alone are insufficient when units share a day, quota, seed, or global environment. Let $U=\operatorname{CP}^+(X,n;\alpha)$ be the one-sided Clopper–Pearson upper bound (Clopper & Pearson, 1934) satisfying

$$\sum_{k=0}^{X}\binom nk U^k(1-U)^{n-k}=\alpha,$$

with $U=1$ when $X=n$. Then

$$\Pr\{\mathcal M_\nu(S)\le U\}\ge1-\alpha,\qquad
\Pr\{\mathcal R_\nu(S)\ge1-U\}\ge1-\alpha.\tag{S9}$$

This statement estimates a weighted mean and automatically includes delivery failures. It does not estimate $\inf_{i,e}p_i(e)$ or $\inf_e m_e(S)$, and it requires no source-independence assumption.

By contrast, a CP interval for an average class-coverage proportion does not yield a uniform proposition-conditional lower bound. Nor does it identify a maximum independent-subset size, account for list selection on the same data, or supply simultaneous confidence across classes and propositions. A structural pointwise analysis would need fixed sampling units for every $(e,i)$, a pre-frozen independence model, simultaneous error allocation, and independent validation data. Time-replayed propositions require independent time blocks or an explicit superpopulation model. On one complete finite corpus, the proportion is descriptive; it should not be presented as a future-probability guarantee.

#### SD.3.6 Monitoring-portfolio optimization

For realized coverage indicators $G_i(e,\omega)$, define

$$U_{\mathrm{mon}}(S)=\sum_e w_e\,\mathbb E\!\left[\max_{i\in S}G_i(e,\omega)\right],$$

with the empty-set maximum equal to zero. Each realized max-coverage function is monotone submodular, and expectation and nonnegative weighting preserve both properties. No independence is needed for this set-function result. Under a cardinality constraint, standard greedy inherits the $1-1/e$ ratio; under a knapsack constraint, the same algorithm-specific guarantees reviewed in Section SD.2.4 apply (Nemhauser et al., 1978; Leskovec et al., 2007; Sviridenko, 2004).

The independent-product expression is only one way to evaluate the objective under a joint model. For positively correlated pairs it need not be a conservative recall estimate, and for three or more classes even pairwise positive correlation alone gives no universal one-sided product interpretation. Monitoring selection and its evaluation should therefore use independent validation data and the realized joint coverage or a declared model, not a pooled proxy labeled as $p_{\min}$.

### SD.4 Pull operators, budget prices, and fixed-capacity choice

#### SD.4.1 KKT prices with corner cases

Let $x_u\ge0$ be minutes allocated to use $u$, with differentiable, increasing, concave values $V_u$, $T>0$, and $\sum_ux_u=T$. If $V(x)=\sum_uV_u(x_u)$, the strictly positive feasible allocation supplies Slater's condition, and a feasible allocation $x^*$ is optimal if and only if some $\lambda_B\ge0$ satisfies the standard Karush–Kuhn–Tucker conditions (Karush, 1939; Kuhn & Tucker, 1951):

$$V_u'(x_u^*)=\lambda_B\quad(x_u^*>0),\qquad V_u'(0)\le\lambda_B\quad(x_u^*=0).\tag{S10}$$

This is the standard concave KKT characterization, not a new theorem. Funded uses share a marginal value; unfunded uses need not. Activating a previously unfunded use can produce first-order loss $(\lambda_B-V_u'(0))\epsilon$, and a universal second-order statement is false. Pull query time, push reading, exploration, dwelling, and reflection can be compared through this price only after converting all values to the same utility-per-minute unit. Pandora's reservation index, a patch-cycle average, a slot threshold, and a Whittle index are not automatically the same scalar (Charnov, 1976; Weitzman, 1979; Whittle, 1988).

The KKT result does not solve interactions between retrieval and push novelty, stochastic path-dependent opening costs, or global knowledge-state coupling. Those remain outside the separable concave model.

#### SD.4.2 Conditional EIG submodularity

Let $K$ be the current knowledge state and let $I_K(Q)=I(\omega;Y_Q\mid K)$ for a fixed nonadaptive query batch $Q$. For finite discrete variables, monotonicity follows from

$$I_K(Q\cup q)-I_K(Q)=I(Y_q;\omega\mid Y_Q,K)\ge0.$$

**Proposition SD.9 (Conditional-independence condition for EIG submodularity).** *If the full family $\{Y_q:q\in\mathcal Q\}$ is mutually conditionally independent given $(\omega,K)$, then $I_K$ is monotone submodular.*

The short entropy proof is deferred to Supplementary Appendix SA.2. Pairwise independence given only $\omega$ is insufficient. If $K$ is fixed, it may be suppressed; if queries adaptively change $K$, this static batch result does not automatically apply. Standard greedy guarantees are inherited only under the corresponding cardinality or knapsack algorithms and certified domain.

#### SD.4.3 A correct fixed-capacity stochastic-choice limit

Single-alternative rational-inattention logit is not a probability law for overlapping events $\{i\in A\}$. To model selection of exactly $m$ items, the action itself must be a subset. Let $\mathcal A_m=\{A\subseteq[n]:|A|=m\}$, and consider the KL-regularized subset-choice problem

$$\max_{p\in\Delta(\mathcal A_m)}\left\{\sum_A p(A)U(A)-\lambda D_{\mathrm{KL}}(p\|\pi^0)\right\},\qquad \lambda>0,$$

where $\pi^0$ is a positive reference distribution over subsets. Equivalently, the objective is $\sum_Ap(A)U(A)+\lambda H(p)+\lambda\sum_Ap(A)\log\pi_A^0$.

**Proposition SD.10 (Subset logit and top-$m$ limit).** *The unique optimum is*

$$p_\lambda(A)=\frac{\pi^0_A\exp(U(A)/\lambda)}{\sum_{B\in\mathcal A_m}\pi^0_B\exp(U(B)/\lambda)},\tag{S11}$$

*Inclusion probabilities are*

$$P_\lambda(i\in A)=\sum_{A\in\mathcal A_m:A\ni i}p_\lambda(A),$$

*not a single-item logit proportional to $\pi_i^0e^{u_i/\lambda}$. As $\lambda\downarrow0$, $p_\lambda$ concentrates on $\arg\max_{A\in\mathcal A_m}U(A)$, weighted by $\pi^0$ if several optima exist. If $U(A)=\sum_{i\in A}u_i$, this is the top-$m$ rule.*

The simplex-KKT and limiting argument appears in Supplementary Appendix SA.3. This proposition is a deliberate fixed-capacity subset model, not a consequence of Matějka–McKay single-alternative choice. It also does not identify the online opportunity-cost thresholds of Proposition SD.5 with a static information-cost parameter.
