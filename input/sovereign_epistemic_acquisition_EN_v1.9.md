> **SUPERSEDED / 已被取代：** This is a historical version, not the current authoritative manuscript. Current version: `input/sovereign_epistemic_acquisition_EN_v1.16.md`. See `archive/README.md`. Do not cite this version’s claims without checking v1.16.

# Sovereign Epistemic Acquisition: Conditional Design for Pull, Push, and Weighted Recall

**Wen Hu**<sup>1,2</sup>&nbsp;&nbsp;**Xutong Wang**<sup>1</sup>&nbsp;&nbsp;**Ya Yu**<sup>1</sup>

<sup>1</sup> College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China  
<sup>2</sup> Jiangsu Yunhefeng Intelligent Technology Co., Ltd., Jiangsu, China

Corresponding author: Wen Hu (huwen@nuaa.edu.cn)

November 2026 · Human–AI collaboration; independent human mathematical review remains pending

---

## Abstract

Information systems usually treat active retrieval and passive filtering as separate problems, while the authority to read, write, and audit the objective is often left implicit. Sovereign Epistemic Acquisition (SEA) instead formulates a Sovereign Acquisition Problem (SAP): pull and push operators share one cognitive budget and are constrained by user-authorized objective writes and audit trails. The contribution is a conditional integration, not a new general theory of submodular optimization, rational inattention, or recall estimation. Four formal results organize the paper. First, a single update kernel, possibly based on a misspecified credibility parameter, yields an expected-realized-value identity; correctly specified Bayesian updating is the nonnegative special case, and misspecification regret can exceed that value. Second, population threshold analysis is separated from finite top-$m$ selection: the Gaussian proposition-level example requires $d'=4.3893$ for 95% population recall, whereas the exact finite-pool expectation and its realized variability are computed separately. Third, end-to-end recall is expressed as weighted expected omission, with an exact coverage–delivery decomposition $m_e=1-\kappa_e\delta_e$ and dependence-robust bounds. Pooled class coverage is not a uniform proposition-conditional floor, and a Clopper–Pearson interval for a mean does not identify an infimum. Fourth, a fixed-capacity subset-choice model gives the correct zero-temperature top-$m$ limit, without confusing single-alternative logit with subset inclusion. Existing pilots are semi-oracle, retrospective mechanism checks: none establishes a 95% end-to-end deployment guarantee or superiority to end-to-end LLM, RAG, or welfare-recommender baselines. Negative and inconsistent recall/value results, time leakage, shared corpora, and the absence of human data are reported explicitly. SEA's defensible contribution is therefore a testable ownership and accounting framework whose deployment claims remain contingent on matched, leakage-resistant experiments.

**Keywords**: epistemic sovereignty; active acquisition; information filtering; misspecified learning; weighted recall; bounded agency

## Contents

# Part I Problem, Evidence Scope, and Framework

## 1 Introduction

### 1.1 The budget problem and the ownership problem

A bounded agent cannot consume every candidate. If 45 minutes are available and each substantive item requires at least four minutes, at most 11 items can be consumed. In a stylized stream of $10^4$ candidates, the discarded fraction is therefore at least

$$1-\frac{45}{4\times 10^4}=0.998875,$$

or 99.8875% (about 99.89%). The stream size is an illustrative scenario, not a measured universal constant; the inequality itself is arithmetic. Notification and personal-information-management research documents the practical burden of interruptions and digital organization, but it does not validate this particular daily count for every user (Pielot, Church & de Oliveira, 2014; Bergman & Whittaker, 2016).

Two design questions follow. First, how should active acquisition (queries, source exploration, monitoring) and passive filtering compete for the same limited attention? Second, who may read and change the objective against which candidates are selected, and who can audit those changes? The second question is not answered by replacing an engagement objective with a designer's conception of welfare. User-controlled recommenders, preference elicitation, contestability, and value-sensitive design already address important parts of it (Harper et al., 2015; Jugovac & Jannach, 2017; Hirsch et al., 2017; Friedman & Hendry, 2019).

SEA's narrower proposal is to make these components explicit in one conditional model:

- pull and push are operators in one Sovereign Acquisition Problem (SAP);
- objective parameters have authorized read, write, rollback, and audit semantics;
- source coverage is distinguished from ingestion, proposition linking, quota allocation, and actual consumption;
- empirical recall is reported for a declared target distribution and consumption unit, rather than treated as a context-free percentage.

### 1.2 Contributions and non-contributions

The paper makes four contributions.

1. **A behaviorally consistent value model.** A single update kernel is used for every observed signal. A reliability-mixture specialization separates the true credibility $c$ from the agent's assumed credibility $\hat c$, without allowing the update rule to depend on an unobserved genuine/adversarial branch.
2. **Aligned filtering calculations.** The paper distinguishes combinatorial capacity bounds, population threshold models, and finite top-$m$ order statistics. It also corrects the Pareto leakage expression by giving the exact Gamma sum and labeling the integral expression as an approximation.
3. **A weighted end-to-end recall theory.** The main object is weighted expected omission, not a pooled estimate inserted into a pointwise redundancy formula. Exact identities separate source noncoverage from delivery loss, support dependence-robust bounds, and clarify what an independent proposition sample can and cannot estimate.
4. **An evidence and validation audit.** The paper reports the limits of existing semi-oracle pilots, corrects their denominators and budget calibers, decomposes negative citation-weighted returns, and specifies the direct baselines and temporal controls required for structural identification.

The following are not claimed: a universal need for dual channels; a five-dimensional sufficient statistic for all decision value; a measured independence coefficient $k_{\mathrm{eff}}$; a pointwise 95% or 99.76% deployment guarantee; a new KKT, Hoeffding, Poisson-binomial, minimax-regret, or submodular-greedy theorem; or evidence that SEA improves human welfare.

### 1.3 Claim and evidence conventions

A **formal result** is a derivation under its stated assumptions. A **design rule** is a normative or engineering choice. A **descriptive pilot** summarizes a frozen retrospective artifact. A **confirmatory experiment** would require a time-stamped protocol, independent environments, matched baselines, and an immutable analysis package; no such complete experiment is reported here.

The word *recall* always requires four qualifiers: target set, probability measure or weighting, configuration, and consumption unit. In the empirical sections it means **retrospective proxy-opportunity recall**, with upstream conditioning stated explicitly. It never abbreviates “recall of every proposition that would have been critical ex ante to a person.” The authoritative evidence matrix appears once, in Section 9; later discussion interprets rather than reintroduces competing calibers.

## 2 Related Work and Precise Positioning

### 2.1 Review method

The literature update uses a targeted scoping search rather than a systematic review. Search concepts, inclusion and exclusion rules, access date, and representative publisher records are archived in `docs/LITERATURE_SEARCH_v1.9.md`. Databases and queries covered user-controlled recommendation, diversified retrieval and submodular summarization, misspecified learning, selective prediction and cascade retrieval, personal information management and notifications, meaningful human control and contestability, and agenda setting and common knowledge. Because the search is not exhaustive, the positioning claim is deliberately limited: among the literature identified by this search, we have not found one formal integration that simultaneously treats pull and push under one budget, explicit objective write/audit rights, end-to-end weighted omission, and joint counterfactual auditing. Each component has substantial prior work.

### 2.2 Acquisition, attention, and value of information

Search economics (Stigler, 1961), optimal stopping and Pandora's box (Weitzman, 1979), information foraging (Pirolli & Card, 1999), Bayesian experimental design (Lindley, 1956; Chaloner & Verdinelli, 1995), active learning (Settles, 2009), bandits (Gittins, 1979; Whittle, 1988), and rational inattention (Sims, 2003; Matějka & McKay, 2015; Maćkowiak, Matějka & Wiederholt, 2023) supply the pull-side foundations. Blackwell (1953) gives the correctly specified information-value benchmark. SAP uses these as components of a shared-budget control problem; it does not imply that their indices have the same units or that a layered solution is globally optimal.

Selective prediction and the reject option formalize the choice to abstain when confidence is inadequate (Chow, 1970; Geifman & El-Yaniv, 2017). Cascade ranking studies how cheap stages can preserve retrieval quality while reducing expensive computation (Wang, Lin & Metzler, 2011). Recall@k and relevance-judgment variability are established retrieval-evaluation concerns (Voorhees, 1998). These literatures motivate separate reporting of upstream candidate recall, judgment-layer recall, abstention, and final consumption. SEA adds no new retrieval metric; it requires these established stages not to be collapsed into one headline number.

### 2.3 User control, welfare, and contestability

User-controlled recommendation already allows people to alter recommendation objectives and trade-offs. Harper et al. (2015), for example, let users tune popularity and recency controls; Jugovac and Jannach (2017) review a broader interaction literature. Welfare-oriented recommenders study objectives other than raw engagement (Allcott et al., 2020; Stray et al., 2024). It would therefore be inaccurate to claim that prior research never asked who configures a recommender's objective.

SEA's narrower distinction is the combination of explicit machine-state write authorization, reversible change logs, a common pull–push budget, and an end-to-end actual-consumption estimand. This is adjacent to, not a replacement for, meaningful human control (Santoni de Sio & van den Hoven, 2018), contestability (Hirsch et al., 2017), and value-sensitive design (Friedman & Hendry, 2019). These traditions also warn that a readable interface or a signature alone does not establish meaningful control.

### 2.4 Diversified retrieval and submodular summarization

Maximal marginal relevance (Carbonell & Goldstein, 1998), xQuAD (Santos, Macdonald & Ounis, 2010), PM-2 (Dang & Croft, 2012), and submodular document summarization (Lin & Bilmes, 2011) directly address relevance, redundancy, and coverage. Facility-location objectives and classical monotone-submodular guarantees provide further foundations (Nemhauser, Wolsey & Fisher, 1978; Krause, Singh & Guestrin, 2008).

The SEA selection objective is an instance of this family, not an alternative invented independently of it. Weighted proposition coverage inherits diminishing returns; facility-location diversity is a standard submodular term. MMR is a sequential relevance–redundancy heuristic, xQuAD explicitly models subtopic coverage, and PM-2 targets proportional aspect representation. SEA differs mainly in its declared ownership constraints and its requirement to audit actual consumption. Its approximation ratios, when applicable, are inherited from standard algorithms and restricted to their certified domains (Leskovec et al., 2007; Sviridenko, 2004).

### 2.5 Misspecified learning and non-Bayesian realized value

The nonnegativity of correctly specified information value does not cover an agent acting on a wrong likelihood. Misspecified-statistics and misspecified-learning research studies exactly this divergence (Berk, 1966; Esponda & Pouzo, 2016; Fudenberg, Romanyuk & Strack, 2017). SEA uses this upstream directly: the environment generates signals under $c$, while one behaviorally implementable update kernel uses $\hat c$ for every signal. The resulting expected realized utility is not a Blackwell value unless the complete model, including the prior and posterior, is correctly specified.

### 2.6 Human measurement and public communication

Brier scores (Brier, 1950) combine calibration-related reliability, resolution, and outcome uncertainty (Murphy, 1973; Gneiting & Raftery, 2007). Strict propriety concerns expected-score minimization under a specified incentive model; it does not show that every participant in every scoring environment has no strategic reason to distort a report. Notification batching and digital-wellbeing research motivates time-budget interventions but does not validate long-term epistemic change (Fitz et al., 2019).

Agenda-setting research studies which issues become salient (McCombs & Shaw, 1972), while public rituals and common knowledge address the additional fact that participation is publicly visible (Aumann, 1976; Chwe, 2001). Public signals may also receive excessive weight in coordination problems (Morris & Shin, 2002). These are distinct mechanisms. A shared digest can change agenda overlap without producing common knowledge of truth.

### 2.7 Comparison matrix

| Tradition | What it already supplies | What SEA borrows | What SEA does not establish |
|---|---|---|---|
| Search, foraging, bandits, rational inattention | Acquisition and stopping rules | Pull operators and common-budget comparisons | Global optimality of the complete SAP |
| Controlled and welfare-oriented recommendation | User-configured objectives and welfare criteria | Explicit write/audit interface | First study of user objective control; superiority to those systems |
| MMR, xQuAD, PM-2, submodular summarization | Coverage/diversity objectives and greedy algorithms | Proposition coverage and facility-location diversity | A new submodularity or greedy theorem |
| Misspecified learning | Effects of acting on wrong models | One update kernel with $c\ne\hat c$ | General sufficiency of five semantic scoring coordinates |
| Retrieval evaluation and cascades | Stage-specific recall and judgment uncertainty | Upstream/downstream opportunity accounting | A leakage-free estimate from historical replay alone |
| Human control, contestability, VSD | Governance and recourse principles | Authorized, reversible, auditable changes | Proof that formal controls create meaningful human control |
| Agenda setting and common knowledge | Public salience and public visibility | Separate agenda-overlap and announcement conditions | Evidence that a private receipt creates common knowledge |

## 3 The Sovereign Acquisition Problem and Its Governance Constraints

### 3.1 Items, propositions, and actual consumption

An information item $x_i$ belongs to a source class $\mathcal C_i$ and is mapped to one or more propositions $e\in E$. A proposition is not automatically a document, a company–day, or an event: the target construction $\kappa:x_i\mapsto e$ is part of the estimand and must be versioned. For a target proposition $e$ and source class $i$, let $Z_i(e)$ indicate authentic source coverage. Coverage does not imply that the item was ingested, authenticated, linked correctly, selected, or actually consumed.

A policy $\pi=(\pi_{\mathrm{mon}},\pi_{\mathrm{pull}},\pi_{\mathrm{push}},\pi_{\mathrm{del}},\pi_{\mathrm{esc}})$ chooses a monitoring portfolio, acquisition operators, push selection, delivery, and any emergency action. Pull and push costs, reading time $T_{\mathrm{push}}$, reflection time $T_{\mathrm{ref}}$, and acquisition time $T_{\mathrm{pull}}$ obey

$$T_{\mathrm{pull}}+T_{\mathrm{push}}+T_{\mathrm{ref}}\le T.$$

The complete objective is a declared expected discounted sum of realized decision utility, reflection/learning utility, and harm terms. The full SAP is not solved globally in this paper. In particular, monotone-submodular selection, independent coverage bounds, and concave budget allocation address different restricted subproblems and do not compose automatically into a global approximation ratio.

### 3.2 A valid finite-horizon existence statement

The original reduced tuple $(K_t,\theta_t,\text{budget},\pi_{\mathrm{mon},t})$ is not assumed to be Markov. Authorization state, the second-order objective $g_t^{(2)}$, exposure and queue histories, public and emergency commitments, current candidate states, and producer/adversary states can all affect rewards, feasibility, or transitions. Latent producer/adversary states belong to the transition model, not automatically to the policy's information set.

**Proposition 3.1 (Optimal policy for a finite observable-history SAP).** *Suppose the SAP has finite horizon $H$ and bounded one-period rewards (including any reflection term). Primitive actions and observations have finite range; latent exogenous states also have finite range so that the model remains discrete. Let $h_t=(o_0,a_0,\ldots,a_{t-1},o_t)$ be the observable history, including every authorization and audit variable available to the policy. Latent states enter only transition and reward kernels and any belief formed from $h_t$; they are not inputs to the policy. Encode every budget, exposure, tolerance, authorization, audit, public, and emergency constraint into a nonempty finite feasible set $\mathcal A_t(h_t)$. Then an optimal deterministic history-dependent policy exists.*

**Proof.** Finite actions and observations generate finitely many observable histories at each finite time. Set $V_{H+1}=0$ and recursively compute

$$V_t(h)=\max_{a\in\mathcal A_t(h)}\left\{r_t(h,a)+\beta\sum_{o_{t+1}}P(o_{t+1}\mid h,a)V_{t+1}(h,a,o_{t+1})\right\}.$$

Every maximum is over a nonempty finite set and is attained. Choosing a maximizer with a fixed tie rule and concatenating the decisions proves the result without requiring latent-state knowledge. $\blacksquare$

This is not a proof that the reduced tuple is Markov or that a low-dimensional belief is sufficient. Continuous dwelling times or budget allocations require a separate Borel-MDP argument and are outside this proposition. The general SAP also remains computationally difficult; restless-bandit special cases are already PSPACE-hard (Papadimitriou & Tsitsiklis, 1999).

### 3.3 Sovereignty as structural constraints, not a mutual-information slogan

Let $\vartheta=(w,g^{(2)},\pi_{\mathrm{mon}},\text{thresholds})$ denote objective parameters and $\Psi^{\mathrm{plat}}$ third-party platform variables. The design requirements are:

- **S1, inspectability:** the implemented objective, parameters, defaults, and relevant data provenance are readable by the reflective principal $R$.
- **S2, authorized writes and rollback:** every change to $\vartheta$ requires an authorization record $\sigma_R$, old and new values, a timestamp, and a reversible implementation. Behavioral measurements may inform a proposal but cannot silently become a write.
- **S3, revenue exclusion and counterfactual invariance:** $U_\vartheta$ contains no third-party revenue term and platform variables cannot write $\vartheta$ without $\sigma_R$. For fixed candidate pool $C$, user state $\kappa$, and authorized $\vartheta$, the direct platform-side counterfactual satisfies
  $$\operatorname{Rank}_\vartheta(C,\kappa;\psi)=\operatorname{Rank}_\vartheta(C,\kappa;\psi')$$
  for tested $\psi,\psi'$. The audit also logs unauthorized write attempts.
- **S4, auditability and recourse:** admission, ranking, delivery, override, and rollback decisions leave append-only records with evidence pointers and a contestation channel.

No mutual-information equation is used. $I(U;\mathrm{Rev})=0$ would be neither necessary nor sufficient: a degenerate revenue variable can have zero mutual information even when revenue is an explicit objective term, while statistical dependence does not by itself identify an unauthorized causal write. The counterfactual test covers only tested variables and fixed supply; platform influence through the candidate ecology needs a separate audit. S1–S4 are therefore design constraints, not proof of complete social or psychological non-capture.

### 3.4 Declaration burden and human–AI asymmetry

A minimal onboarding declaration does not identify the complete SAP. The mapping must be explicit:

| Onboarding item | Formal object supplied | Objects still missing |
|---|---|---|
| Monitoring list | $\pi_{\mathrm{mon}}$ | Coverage and delivery probabilities; capacity feasibility |
| Time budget | $T$ | Allocation across pull, push, and reflection |
| One-sentence $g^{(2)}$ | Candidate topics for a human-reviewed decision template | Actions, utility/loss tables, horizons, harm thresholds, emergency permissions |
| Optional emergency sheet | $\mathcal A_{\mathrm{safe}}$, loss table, triggers, undo costs | Validation and calibration; otherwise override remains disabled |

Conservative defaults may support a feasibility demonstration, but they are not identified personal utilities and cannot support a personalized optimality claim. A full deployment declaration requires a decision–action map, horizon, loss/harm specification, monitoring and capacity checks, and either a pre-authorization table or an explicitly disabled override.

Finally, human and machine write isolation are not perfectly symmetric. A machine parameter store can be architecturally prevented from changing $\vartheta$ without authorization. Human emotion, learning, and preference formation mean that content can shape the very goals later endorsed by a person. S2 governs machine writes; it does not prove that human preferences are exogenous or untouched by exposure.

# Part II Conditional Formal Results

## 4 Expected Realized Value under One Misspecified Update Rule

### 4.1 Arbitrary update kernel

For decision $d$, let $P_{i,d}$ be the true joint distribution of $(\omega_d,Y_i)$, let $\mu_{i,d}$ be the agent's current prior, and let $\widehat\mu_{i,d}(\cdot\mid y)$ be **one arbitrary measurable update kernel used for every signal**. Time and deadline effects are included in $u^h_{i,d}$. Assume all displayed utilities are integrable and all required maxima are attained. Define

$$a^0_{i,d}\in\arg\max_a\mathbb E_{\mu_{i,d}}[u^h_{i,d}(a,\omega_d)],$$

$$\widehat a_{i,d}(y)\in\arg\max_a\mathbb E_{\widehat\mu_{i,d}(\cdot\mid y)}[u^h_{i,d}(a,\omega_d)].$$

**Definition 4.1 (Expected realized decision value).**

$$\mathcal W_{i,d}:=\mathbb E_{P_{i,d}}\!\left[u^h_{i,d}(\widehat a_{i,d}(Y_i),\omega_d)-u^h_{i,d}(a^0_{i,d},\omega_d)\right],\qquad v_i^*:=\sum_{d\in D}\pi_d(i)\mathcal W_{i,d}.$$

Only one update kernel appears. No genuine/adversarial branch label is observed or used to select an update rule. Gains and losses can be separated without imposing their signs: if $\Delta U_{i,d}$ is the utility increment inside the expectation and $G_{i,d}=\mathbb E[(\Delta U_{i,d})^+]$, $L_{i,d}=\mathbb E[(\Delta U_{i,d})^-]$, then $\mathcal W_{i,d}=G_{i,d}-L_{i,d}$.

### 4.2 Correctly specified special case and misspecification regret

If $\mu_{i,d}=P_{i,d,\omega}$ and $\widehat\mu_{i,d}(\cdot\mid y)=P_{i,d}(\cdot\mid Y_i=y)$, the standard tower argument gives

$$\mathcal W_{i,d}=\mathbb E_y\!\left[\max_a\mathbb E(u^h_{i,d}\mid y)\right]-\max_a\mathbb E_{\mu_{i,d}}u^h_{i,d}=\mathrm{VOI}_{i,d}\ge0.$$

The complete prior, likelihood, posterior, and evaluation distribution must agree; a “correct likelihood” attached to a wrong prior is not enough.

For a parametric reliability model, let $Q_c$ be the true joint law with prior $\mu=P_\omega$ and let $Q_{\hat c}$ be the agent's assumed law. The agent always uses the posterior induced by $Q_{\hat c}$. Let $a_c^*(y)$ be the Bayes action under $Q_c$ and $\widehat a_{\hat c}(y)$ the action under $Q_{\hat c}$. Define the correctly specified value $\mathrm{VOI}_c$ and realized value $W(c,\hat c)$ relative to the same no-signal baseline.

**Theorem 4.1 (Value minus misspecification regret).** *Under the integrability and attainment assumptions above,*

$$W(c,\hat c)=\mathrm{VOI}_c-\operatorname{Regret}_c(\hat c),$$

where

$$\operatorname{Regret}_c(\hat c):=\mathbb E_{Q_c}\!\left[u(a_c^*(Y),\omega)-u(\widehat a_{\hat c}(Y),\omega)\right]\ge0.$$

Consequently $W(c,\hat c)<0$ is possible exactly when the regret exceeds the correctly specified value.

**Proof.** Add and subtract $\mathbb E_{Q_c}u(a_c^*(Y),\omega)$. The regret is nonnegative because, conditional on each $y$, $a_c^*(y)$ maximizes expected utility under the true posterior $Q_c(\omega\mid y)$. $\blacksquare$

A reliability-mixture implementation is

$$\ell_{\hat c}(y\mid\omega)=\hat c\,\ell_G(y\mid\omega)+(1-\hat c)\ell_A(y\mid\omega),$$

with the corresponding single posterior $\widehat\mu(B\mid y)\propto\int_B\mu(d\omega)\ell_{\hat c}(y\mid\omega)$. The true environment may use $c\ne\hat c$, but the update rule never observes the latent $G/A$ branch. Credibility mismatch need not cause harm in every problem—different posteriors can induce the same actions—but it can cause strictly negative realized value.

### 4.3 Binary counterexample

Let $\omega\sim\operatorname{Bernoulli}(1/2)$, actions be $0,1$, and utility be one for a correct action and zero otherwise. A genuine mechanism is correct with probability $\eta>1/2$; an adversarial mechanism returns the opposite state with the same probability. Under reliability $c$, the observed signal is correct with probability

$$a_c=c\eta+(1-c)(1-\eta).$$

Take $c=0.2$, $\hat c=0.8$, and $\eta=0.9$. The agent uses only $Q_{0.8}$, perceives signal accuracy $a_{0.8}=0.74>1/2$, and therefore follows every signal. The true accuracy is $a_{0.2}=0.26$, so $W=-0.24$. With the correctly specified $Q_{0.2}$, the agent reverses the signal and obtains $\mathrm{VOI}=0.24$. Hence misspecification regret is $0.48$. The negative value arises from one implementable rule applied uniformly to all observations, not from branch-contingent updating.

### 4.4 Status of scoring features

Relevance, novelty, durability, actionability, and credibility can remain engineering coordinates $\phi_i$. They are not proved to be a universal sufficient statistic for value. An exact representation $W_i=F(\phi_i;K,D)$ holds only when such a map and its decision homogeneity assumptions are externally specified and validated. That is a conditional parameterization, close to a representability assumption—not evidence that the five semantic names exhaust decision value.

A useful restricted form is obtained only after additional assumptions. If $G_{i,d}=a_dG_i$, $L_{i,d}=a_dL_i$, and $A_i=\sum_d\pi_d(i)a_d$, then $v_i^*=A_i(G_i-L_i)$. If separately validated maps $G_i=\mathcal G(\phi_i)$, $L_i=\mathcal L(\phi_i)$, and $A_i=\mathcal A(\phi_i)$ exist, then

$$v_i^*=\mathcal A(\phi_i)\{\mathcal G(\phi_i)-\mathcal L(\phi_i)\}.$$

Outside those conditions the full update kernel, decision-specific utilities, and harm/loss terms remain necessary. Linear scoring on the five coordinates is a heuristic whose error must be measured, not a decision-theoretic identity.

## 5 Filtering: Capacity, Population Thresholds, and Finite Selection

### 5.1 Capacity and exact Pareto leakage

**Proposition 5.1 (Capacity and optimal unavoidable leakage).** *If $N$ items arrive, each costs at least $\underline\tau>0$, and the budget is $T$, then at most $T/\underline\tau$ items can be consumed. If $K$ critical propositions have nonnegative values $v_e$ and at most $m$ distinct propositions can be consumed, define $\mathcal D(\pi):=\mathbb E[\sum_{e=1}^Kv_e\mathbf 1\{e\text{ is not consumed by }\pi\}]$. Then*

$$\mathcal D(\pi)\ge\mathcal D^*:=\mathbb E\!\left[\sum_{r=m_0+1}^{K}V_{(r)}\right],\qquad m_0=\min(m,K),$$

*where $V_{(1)}\ge\cdots\ge V_{(K)}$ is the decreasing rearrangement. Equality holds exactly when the consumed critical value equals the top-$m_0$ critical value almost surely; ties are allowed.*

**Proof.** The consumed critical value cannot exceed the sum of the $m_0$ largest values. A policy attaining that sum reaches equality. $\blacksquare$

For $v_e\overset{iid}{\sim}\mathrm{Pareto}(\alpha,v_{\min})$, $\alpha>1$, the exact order-statistic expectation is

$$\mathbb E V_{(r)}=v_{\min}\frac{\Gamma(r-1/\alpha)\Gamma(K+1)}{\Gamma(r)\Gamma(K+1-1/\alpha)}.$$

Thus the exact expected aggregate leaked share is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}=1-\frac{\sum_{r=1}^{m_0}\mathbb E V_{(r)}}{Kv_{\min}\alpha/(\alpha-1)}.$$

As $K\to\infty$, $m\to\infty$, and $m/K\to\rho\in(0,1)$, the quantile-integral limit (Resnick, 1987) is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}\;\longrightarrow\;1-\rho^{(\alpha-1)/\alpha}.$$

At finite $K,m$, $1-(m/K)^{(\alpha-1)/\alpha}$ is therefore an approximation, not an equality. At $K=52,\alpha=1.5$, the exact/approximate pairs are 20.7999%/20.6299% for $m=26$ and 6.9191%/6.8716% for $m=42$. The latter approximation uses the actual ratio $42/52=0.807692$, not 0.8. Direct pass-through does not increase total consumption capacity; it changes how the same slots are allocated.

### 5.2 Population threshold model and boundary cases

Let noncritical and critical scores have continuous distributions $F_0,F_1$ and survival functions $\bar F_0,\bar F_1$, with critical mass $\pi\in(0,1)$. At a fixed threshold $t$, the population acceptance and recall are

$$\beta(t)=(1-\pi)\bar F_0(t)+\pi\bar F_1(t),\qquad R(t)=\bar F_1(t).$$

This is a population threshold identity. It is not an exact identity for the random threshold induced by finite top-$m$ selection.

**Theorem 5.2 (Threshold feasibility).** *For $0<R<1$ and $0<\beta<1$, a counting-necessary condition is $\beta\ge\pi R$. Let $\tau_R=Q_1(1-R)$, where $Q_1$ is the ordinary CDF quantile. Assuming the survival functions are continuous and strictly decreasing on their relevant supports, a threshold with acceptance $\beta$ and recall at least $R$ exists if and only if*

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

### 5.3 Finite top-$m$: exact formula evaluated by quadrature

Let $M$ be finite. All $M$ scores are mutually independent, with $K$ critical scores drawn from $F_1$ and $M-K$ noncritical scores drawn from $F_0$. Select exactly the $m$ largest scores, $1\le m<M$. The threshold is an order statistic, not the population threshold above.

**Proposition 5.2 (Finite-pool expected recall).** *For continuous scores and $K\ge1$, symmetry among critical items gives*

$$\mathbb E R_{M,K,m}=\int f_1(x)\Pr\{N_0(x)+N_1(x)\le m-1\}\,dx,$$

*where, conditional on one marked critical score $x$,*

$$N_0(x)\sim\operatorname{Binomial}(M-K,\bar F_0(x)),\qquad N_1(x)\sim\operatorname{Binomial}(K-1,\bar F_1(x)),$$

*independently. The marked critical item is selected exactly when at most $m-1$ other scores exceed it.*

For the Gaussian example $M=800,K=8,m=10$, deterministic Gauss–Legendre quadrature and 20,000 independent Monte Carlo realizations give:

| $d'$ | Population threshold recall | Exact-formula $\mathbb E R_{800,8,10}$ (converged quadrature) | Realized recall 2.5%, 50%, 97.5% quantiles |
|---:|---:|---:|---:|
| 1.5 | 0.209640 | 0.208661 | 0.000, 0.250, 0.500 |
| 2.5 | 0.523767 | 0.524234 | 0.250, 0.500, 0.875 |
| 4.389338 | 0.950000 | 0.952626 | 0.750, 1.000, 1.000 |

The Monte Carlo estimate at the required separation is 0.952825 with numerical 95% interval [0.951825, 0.953825]. That interval quantifies Monte Carlo error in the mean only. The predictive quantiles describe variation across finite pools; neither is an empirical confidence interval. The finite expectation is close to, but not identical with, the population value and should not be replaced by the random top-$m$ threshold in Theorem 5.2. Reproduction code and quadrature-convergence tests accompany the paper.

### 5.4 Coverage–diversity objectives: inherited guarantees and their limits

For candidate set $A$, consider

$$U(A)=\sum_{e\in E}v_e\mathbf 1\{A\cap D_e\ne\varnothing\}+\mu\sum_{\sigma\in\mathcal S}\max_{i\in A}\operatorname{sim}(\sigma,i)-\lambda\sum_{i\in A}\hat m_i\tau_i,$$

with nonnegative values, similarities, costs, and weights. The first term is weighted coverage and the second is facility-location diversity. Both are nonnegative, monotone, and submodular. The complete penalized objective remains submodular but need not be monotone.

Consequently, the usual cardinality ratio $1-1/e$ applies to the unpenalized objective or to a separately certified monotone restriction, not automatically to the full pool. One sufficient restriction $\mathcal C_M$ requires, for every $i\in\mathcal C_M$, the smallest positive-part coverage/diversity gain over all subcontexts to dominate $\lambda\hat m_i\tau_i$. All optima and ratios are then relative to that restricted ground set. Under positive unequal costs, density greedy plus the best feasible singleton has the standard $\tfrac12(1-1/e)$ guarantee, and depth-three partial enumeration has the standard $1-1/e$ guarantee (Leskovec et al., 2007; Sviridenko, 2004). Unaugmented density greedy is not assigned either ratio.

This is the same algorithmic lineage as diversified retrieval and submodular summarization. The engineering contribution is the audit requirement to log monotonicity certificates, algorithm variant, residual capacities, and restricted optimum—not a new approximation theorem.

### 5.5 Online thresholds with explicit boundaries

Suppose an item arrives independently with probability $a\in(0,1]$ in each period; conditional on arrival, its reward $R=r(S)$ is iid with $\mathbb E R^+<\infty$ and $r$ strictly increasing. At most $b$ items can be consumed over the remaining periods and discarding is irrevocable. Let $W_i(b)$ be optimal continuation value and $\Delta_i(b)=W_i(b)-W_i(b-1)$.

**Proposition 5.3 (Threshold policy).** *With $W_i(0)=W_0(b)=0$ and $g_a(\tau)=a\mathbb E[(R-\tau)^+]$,*

$$W_i(b)=W_{i-1}(b)+g_a(\Delta_{i-1}(b)).$$

*It is strictly optimal to consume when $r(s)>\Delta_{i-1}(b)$ and not optimal when $r(s)<\Delta_{i-1}(b)$; either action is optimal on ties. Moreover $\Delta_i(b)$ is nonnegative, nonincreasing in $b$, and nondecreasing in $i$.*

**Proof.** The Bellman equation follows by comparing consumption and discard. Subtracting $W_i(0)=0$ gives the distinct boundary recursion

$$\Delta_i(1)=\Delta_{i-1}(1)+g_a(\Delta_{i-1}(1)),$$

whereas for $b\ge2$,

$$\Delta_i(b)=\Delta_{i-1}(b)+g_a(\Delta_{i-1}(b))-g_a(\Delta_{i-1}(b-1)).$$

The function $g_a$ is nonnegative, nonincreasing, and $a$-Lipschitz with $a\le1$. I prove concavity by induction, with base $\Delta_0(b)=0$ for $b\ge1$. At $b=2$, write $y=\Delta_{i-1}(1)\ge z=\Delta_{i-1}(2)$. Then

$$\Delta_i(1)-\Delta_i(2)=(y-z)+g_a(y)+[g_a(y)-g_a(z)]\ge0.$$

For every $b\ge3$, write $x=\Delta_{i-1}(b-2)\ge y=\Delta_{i-1}(b-1)\ge z=\Delta_{i-1}(b)$. Then

$$\Delta_i(b-1)-\Delta_i(b)=(y-z)+[g_a(y)-g_a(x)]+[g_a(y)-g_a(z)]\ge0,$$

because $g_a(y)-g_a(x)\ge0$ and $(y-z)+[g_a(y)-g_a(z)]\ge0$ by the Lipschitz property. Nonnegativity and time monotonicity follow separately: at $b=1$, $\Delta_i(1)=\Delta_{i-1}(1)+g_a(\Delta_{i-1}(1))\ge\Delta_{i-1}(1)$; at $b\ge2$, the induction hypothesis $\Delta_{i-1}(b)\le\Delta_{i-1}(b-1)$ and monotonicity of $-g_a$ give $\Delta_i(b)\ge\Delta_{i-1}(b)$. $\blacksquare$

A finite cooling queue introduces occupancy, age, eviction, and decay states. The present proof does not establish a double-threshold queue policy, and no such structural claim is made here.

## 6 Recall as Weighted Expected Omission

### 6.1 Separate source coverage from end-to-end delivery

Fix a monitoring set $S$ and proposition $e$. Let $Z_i(e)$ denote authentic coverage by source class $i$, with $p_i(e)=P(Z_i(e)=1)$, and define

$$C_S(e)=\bigcup_{i\in S}Z_i(e),\qquad \kappa_e(S)=P(C_S(e)).$$

Let $D_S(e)$ be actual consumption of $e$ through the monitored channel, with $D_S(e)\subseteq C_S(e)$. When $\kappa_e(S)>0$, define the complete delivery conversion probability

$$\delta_e(S):=P(D_S(e)\mid C_S(e)).$$

It includes ingestion, authentication, proposition linking, deduplication, quota allocation, selection, and actual consumption. When $\kappa_e(S)=0$, actual delivery is zero and $\delta_e$ need not be defined; the convention $\kappa_e(S)\delta_e(S)=0$ is used in the identities below.

**Theorem 6.1 (Coverage–delivery identity and weighted omission).** *For each $e$, the actual miss probability is*

$$m_e(S):=P(\operatorname{miss}_S(e))=1-\kappa_e(S)\delta_e(S).$$

*For target weights $w_e\ge0$ with $W=\sum_ew_e>0$, define $\nu_e=w_e/W$. Then*

$$\mathcal M_\nu(S):=\sum_e\nu_em_e(S),\qquad \mathcal R_\nu(S):=1-\mathcal M_\nu(S)=\sum_e\nu_e\kappa_e(S)\delta_e(S).$$

*These are weighted mean recall and expected omission, not $\inf_e P(D_S(e))$.*

**Proof.** Since $D_S\subseteq C_S$, $P(D_S)=P(C_S)P(D_S\mid C_S)=\kappa_e\delta_e$. The weighted identities follow by linearity. $\blacksquare$

If $\{Z_i(e)\}_{i\in J_e}$ are mutually independent on a certified subset $J_e\subseteq S$, then

$$\kappa_e(S)\ge1-\prod_{i\in J_e}(1-p_i(e)),$$

Write $P_J:=\prod_{i\in J_e}(1-p_i(e))$. If $J_e=S$ and the full family is independent, then $\kappa_e(S)=1-P_J$ and the pointwise decomposition is exactly

$$m_e(S)=P_J+(1-P_J)(1-\delta_e(S)).$$

For a proper certified independent subset $J_e\subsetneq S$, the same expression is generally only an upper bound:

$$m_e(S)=1-\kappa_e(S)\delta_e(S)\le P_J+(1-P_J)(1-\delta_e(S)),$$

because $\kappa_e(S)\ge1-P_J$. In both cases the first term represents independent-subset noncoverage and the second discounts delivery loss. Perfect pass-through $\delta_e=1$ is only a special case, not an empirical default.

Without independence, the Fréchet bounds use only marginal coverage probabilities:

$$\max\left\{0,1-\sum_{i\in S}p_i(e)\right\}\le P\!\left(\bigcap_{i\in S}Z_i(e)^c\right)\le1-\max_{i\in S}p_i(e).$$

Both bounds are sharp when only the marginals are known. In particular, $\kappa_e(S)\ge\max_{i\in S}p_i(e)$ requires no independence certificate.

### 6.2 Certifiable average bounds and a counterexample to pooled products

**Corollary 6.1 (Weighted lower recall certificates).** *If logs or a structural model provide $\kappa_e(S)\ge\underline\kappa_e(S)\ge0$ and $\delta_e(S)\ge\underline\delta_e(S)\ge0$, then*

$$\mathcal R_\nu(S)\ge\sum_e\nu_e\underline\kappa_e(S)\underline\delta_e(S),\qquad
\mathcal M_\nu(S)\le1-\sum_e\nu_e\underline\kappa_e(S)\underline\delta_e(S).$$

*If $\mathcal M_\nu(S)\le\varepsilon$, then for every $\eta\in(0,1]$, the weight of propositions with pointwise miss probability above $\eta$ satisfies*

$$\nu\{e:m_e(S)>\eta\}\le\varepsilon/\eta.$$

The first statement follows from Theorem 6.1 and monotonicity. The tail statement is Markov's inequality for bounded $m_e$. It limits the weight of poorly covered propositions without pretending that every proposition has high recall.

A pooled class mean cannot be inserted into a proposition-wise product. Suppose two equally weighted propositions have class-coverages $p_i(e_1)=0.9$ and $p_i(e_2)=0.1$ for two classes, with independence within each proposition and perfect delivery. The correct weighted omission is

$$\tfrac12(0.1)^2+\tfrac12(0.9)^2=0.410.$$

The pooled class mean is 0.5, but $(1-0.5)^2=0.250$, which would overstate recall as 0.75 rather than the correct 0.59. Joint list coverage is already a union outcome; exponentiating it again would also count redundancy twice.

The former $(1-p_{\min})^{k_{\mathrm{eff}}}$ expression is therefore not used as the main estimand. If a uniform pointwise theorem is desired, it needs a genuine per-class, per-proposition floor and a certified independent subset. Degenerate floors also invalidate the old universal tightness statement: under its perfect-delivery assumption, omission one almost surely forces every coverage indicator to vanish almost surely; those degenerate indicators are mutually independent, so an arbitrary smaller effective independent-subset size cannot be constructed. The present Fréchet and weighted formulations avoid assigning an empirical value to $k_{\mathrm{eff}}$ altogether.

### 6.3 Two channels: failure-weighted recovery, not pooled recovery

Let $D_{\mathrm I}(e)$ and $D_{\mathrm II}(e)$ denote actual consumption by two channels, $q_e=P(D_{\mathrm I}(e)^c)$, and, when $q_e>0$,

$$R_{\mathrm{II}}(e):=P(D_{\mathrm II}(e)\mid D_{\mathrm I}(e)^c).$$

When $q_e=0$, omission is zero and the convention $q_e[1-R_{\mathrm{II}}(e)]=0$ is used without defining $R_{\mathrm{II}}(e)$.

**Proposition 6.1 (Total omission without cross-channel independence).**

$$P(\operatorname{miss}(e))=q_e[1-R_{\mathrm{II}}(e)],\qquad
\mathcal M_\nu^{\mathrm{tot}}=\sum_e\nu_eq_e[1-R_{\mathrm{II}}(e)].$$

If $Q_\nu=\sum_e\nu_eq_e>0$ and $\bar R_{\mathrm{II},q}:=Q_\nu^{-1}\sum_e\nu_eq_eR_{\mathrm{II}}(e)$, then

$$\mathcal M_\nu^{\mathrm{tot}}=(1-\bar R_{\mathrm{II},q})Q_\nu.$$

The recovery mean is weighted by Channel-I failure $q_e$, not by all opportunities and not by an unweighted pooled count. No independence between channels is assumed. A pooled recovery computed on a selected subpopulation does not identify a uniform per-proposition recovery floor.

### 6.4 An explicit availability–pipeline decomposition

The conversion probability can be audited through three stages. Let $A_i(e)$ indicate authentic availability, $L_i(e)$ successful ingestion/authentication/linkage, and $C_i(e)$ selection and actual consumption, with $D_i(e)=A_i(e)L_i(e)C_i(e)$. Define availability-only omission $M_A(e)=\cap_{i\in S}A_i(e)^c$ and total omission $M(e)=\cap_{i\in S}D_i(e)^c$. Then

$$M(e)=M_A(e)\;\dot\cup\;\big[M(e)\cap M_A(e)^c\big],$$

so

$$P(M(e))=P(M_A(e))+P\big(M(e)\cap M_A(e)^c\big).$$

The two terms are source-availability omission and loss after at least one authentic item was available. A weighted sum gives the corresponding $\nu$-decomposition. This makes the difficult engineering stages part of the estimand rather than assuming them away with probability one. A claim of zero filtering-induced omission applies only conditional on the specified availability, linkage, and actual-consumption events; it is not an unconditional zero-miss guarantee.

### 6.5 What Clopper–Pearson can and cannot certify

Freeze the monitoring set and the complete policy. Suppose $n$ independent target–environment–evaluation units are generated, with target $E_j$ sampled from $\nu$ and with an independent realization of the complete pipeline, including its environment, quotas, and implementation randomness. Observe the **end-to-end** omission indicators

$$X_j=\mathbf 1\{\text{no monitored channel actually consumes }E_j\},\qquad X=\sum_{j=1}^nX_j.$$

Under this independent-unit superpopulation model, $X_j\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(\mathcal M_\nu(S))$, so $X\sim\operatorname{Binomial}(n,\mathcal M_\nu(S))$ regardless of dependence among source classes within a proposition. Independent target labels alone are insufficient when units share a day, quota, seed, or global environment. Let $U=\operatorname{CP}^+(X,n;\alpha)$ be the one-sided Clopper–Pearson upper bound satisfying

$$\sum_{k=0}^{X}\binom nk U^k(1-U)^{n-k}=\alpha,$$

with $U=1$ when $X=n$. Then

$$\Pr\{\mathcal M_\nu(S)\le U\}\ge1-\alpha,\qquad
\Pr\{\mathcal R_\nu(S)\ge1-U\}\ge1-\alpha.$$

This statement estimates a weighted mean and automatically includes delivery failures. It does not estimate $\inf_{i,e}p_i(e)$ or $\inf_e m_e(S)$, and it requires no source-independence assumption.

By contrast, a CP interval for an average class-coverage proportion does not yield a uniform proposition-conditional lower bound. Nor does it identify a maximum independent-subset size, account for list selection on the same data, or supply simultaneous confidence across classes and propositions. A structural pointwise analysis would need fixed sampling units for every $(e,i)$, a pre-frozen independence model, simultaneous error allocation, and independent validation data. Time-replayed propositions require independent time blocks or an explicit superpopulation model. On one complete finite corpus, the proportion is descriptive; it should not be presented as a future-probability guarantee.

### 6.6 Monitoring-portfolio optimization

For realized coverage indicators $Z_i(e,\omega)$, define

$$U_{\mathrm{mon}}(S)=\sum_e w_e\,\mathbb E\!\left[\max_{i\in S}Z_i(e,\omega)\right],$$

with the empty-set maximum equal to zero. Each realized max-coverage function is monotone submodular, and expectation and nonnegative weighting preserve both properties. No independence is needed for this set-function result. Under a cardinality constraint, standard greedy inherits the $1-1/e$ ratio; under a knapsack constraint, the same algorithm-specific guarantees reviewed in Section 5.4 apply (Nemhauser et al., 1978; Leskovec et al., 2007; Sviridenko, 2004).

The independent-product expression is only one way to evaluate the objective under a joint model. For positively correlated pairs it need not be a conservative recall estimate, and for three or more classes even pairwise positive correlation alone gives no universal one-sided product interpretation. Monitoring selection and its evaluation should therefore use independent validation data and the realized joint coverage or a declared model, not a pooled proxy labeled as $p_{\min}$.

## 7 Pull Operators, Budget Prices, and Fixed-Capacity Choice

### 7.1 KKT prices with corner cases

Let $x_u\ge0$ be minutes allocated to use $u$, with differentiable, increasing, concave values $V_u$ and $\sum_ux_u=T$. If $V(x)=\sum_uV_u(x_u)$, a feasible allocation $x^*$ is optimal if and only if some $\nu\ge0$ satisfies

$$V_u'(x_u^*)=\nu\quad(x_u^*>0),\qquad V_u'(0)\le\nu\quad(x_u^*=0).$$

This is the standard concave KKT characterization. Funded uses share a marginal value; unfunded uses need not. Activating a previously unfunded use can produce first-order loss $(\nu-V_u'(0))\epsilon$, and a universal second-order statement is false. Pull query time, push reading, exploration, dwelling, and reflection can be compared through this price only after converting all values to the same utility-per-minute unit. Pandora's reservation index, a patch-cycle average, a slot threshold, and a Whittle index are not automatically the same scalar (Charnov, 1976; Weitzman, 1979; Whittle, 1988).

The KKT result does not solve interactions between retrieval and push novelty, stochastic path-dependent opening costs, or global knowledge-state coupling. Those remain outside the separable concave model.

### 7.2 Conditional EIG submodularity

Let $K$ be the current knowledge state and let $I_K(Q)=I(\omega;Y_Q\mid K)$ for a fixed nonadaptive query batch $Q$. For finite discrete variables, monotonicity follows from

$$I_K(Q\cup q)-I_K(Q)=I(Y_q;\omega\mid Y_Q,K)\ge0.$$

**Theorem 7.1 (Conditional-independence condition for EIG submodularity).** *If the full family $\{Y_q:q\in\mathcal Q\}$ is mutually conditionally independent given $(\omega,K)$, then $I_K$ is monotone submodular.*

**Proof.** For $q\notin Q$,

$$\Delta(q\mid Q)=H(Y_q\mid Y_Q,K)-H(Y_q\mid\omega,K).$$

For $Q'\subseteq Q$, conditioning reduces entropy, so $H(Y_q\mid Y_Q,K)\le H(Y_q\mid Y_{Q'},K)$ and $\Delta(q\mid Q)\le\Delta(q\mid Q')$. $\blacksquare$

Pairwise independence given only $\omega$ is insufficient. If $K$ is fixed, it may be suppressed; if queries adaptively change $K$, this static batch result does not automatically apply. Standard greedy guarantees are inherited only under the corresponding cardinality or knapsack algorithms and certified domain.

### 7.3 A correct fixed-capacity stochastic-choice limit

Single-alternative rational-inattention logit is not a probability law for overlapping events $\{i\in A\}$. To model selection of exactly $m$ items, the action itself must be a subset. Let $\mathcal A_m=\{A\subseteq[n]:|A|=m\}$, and consider the KL-regularized subset-choice problem

$$\max_{p\in\Delta(\mathcal A_m)}\left\{\sum_A p(A)U(A)-\lambda D_{\mathrm{KL}}(p\|\pi^0)\right\},\qquad \lambda>0,$$

where $\pi^0$ is a positive reference distribution over subsets. Equivalently, the objective is $\sum_Ap(A)U(A)+\lambda H(p)+\lambda\sum_Ap(A)\log\pi_A^0$.

**Proposition 7.2 (Subset logit and top-$m$ limit).** *The unique optimum is*

$$p_\lambda(A)=\frac{\pi^0_A\exp(U(A)/\lambda)}{\sum_{B\in\mathcal A_m}\pi^0_B\exp(U(B)/\lambda)},$$

*Inclusion probabilities are*

$$P_\lambda(i\in A)=\sum_{A\in\mathcal A_m:A\ni i}p_\lambda(A),$$

*not a single-item logit proportional to $\pi_i^0e^{u_i/\lambda}$. As $\lambda\downarrow0$, $p_\lambda$ concentrates on $\arg\max_{A\in\mathcal A_m}U(A)$, weighted by $\pi^0$ if several optima exist. If $U(A)=\sum_{i\in A}u_i$, this is the top-$m$ rule.*

**Proof.** The KKT conditions for maximizing the strictly concave KL-regularized objective over the simplex give the exponential family with reference weights $\pi_A^0$. As $\lambda\downarrow0$, exponents dominated by the maximal set utility determine the limit. $\blacksquare$

This proposition is a deliberate fixed-capacity subset model, not a consequence of Matějka–McKay single-alternative choice. It also does not identify the online opportunity-cost thresholds of Proposition 5.3 with a static information-cost parameter.

## 8 Normative Extensions: Measurement, Override, and Public Agenda

### 8.1 Measurement is not control validation

A three-dimensional state such as calibration, openness, and intellectual humility is a modeling choice, not an identified latent state from ten weekly prediction questions. Brier scores reflect reliability, resolution, and uncertainty, and their proper-scoring property is conditional on the participant's complete incentives. Bounded observations on $[0,1]^3$ also do not justify a homoskedastic Gaussian error model by default. A human measurement program needs validated instruments, test–retest reliability, longitudinal measurement-invariance checks, and a latent-variable model justified by sample size. No convergence theorem for human “virtue dynamics” is claimed in this paper.

The same limitation applies to LLM cohorts. Replaying a human paradigm can test an AI mechanism, but it does not establish human transfer. Model-specific Brier or persuasion results cannot identify human learning, welfare, or deskilling without a predeclared, passed transfer gate and ultimately direct human evidence.

### 8.2 Emergency authorization is a finite design table

An emergency override can be restricted to a nonempty finite whitelist $\mathcal A_{\mathrm{safe}}$, a finite uncertainty set $\Omega$, and a declared loss table $L(a,\omega)$. The standard minimax-regret action is

$$a^*\in\arg\min_{a\in\mathcal A_{\mathrm{safe}}}\max_{\omega\in\Omega}\left[L(a,\omega)-\min_{a'\in\mathcal A_{\mathrm{safe}}}L(a',\omega)\right].$$

Finite enumeration makes the value computable ex ante; this is Savage's standard criterion, not a new regret theorem (Savage, 1951). A valid implementation also needs explicit triggers, evidence authentication, a time-feasibility check, rollback, logging, and post hoc review. If those inputs are absent, the override is disabled rather than initialized with unvalidated defaults. No dominance claim over every alternative policy follows without specifying the loss model and audit costs.

### 8.3 Agenda overlap is not common knowledge

For consumption sets $C_i,C_j$, define the Jaccard agenda overlap $J(C_i,C_j)=|C_i\cap C_j|/|C_i\cup C_j|$. Suppose every member of a group actually consumes the same public set $S$, $|S|=s=\gamma m$, and each has a private part of size $d=(1-\gamma)m$ disjoint from $S$. Then, for every pair,

$$J(C_i,C_j)\ge\frac{s}{s+2d}=\frac{\gamma}{2-\gamma}.$$

The proof is only set accounting: the intersection contains at least $S$ and the union has size at most $s+2d$. The quantity is an **agenda-overlap index**, not a “fragmentation index” whose direction would be ambiguous. It does not require or establish truth, attention beyond actual consumption, or common knowledge.

Common knowledge of an announcement requires a self-evident public event: every member receives, attends to, and understands the same authenticated announcement, and the public character of that receipt is itself commonly observable. Private delivery receipts and ordinary audit logs do not satisfy this condition merely because everyone knows the mechanism. Even a genuine public announcement establishes common knowledge of membership in the announced set, not common knowledge that the proposition is true or important. Whether any real protocol achieves those strong conditions is an empirical question left open.

# Part III Evidence, Falsification, and Scope

## 9 Evidence Status and Controlled Reanalyses

### 9.1 Authoritative claim–assumption–evidence matrix

The table below is the single authoritative summary of empirical status. “Completed” refers only to the named retrospective artifact, not to validation of SEA as a whole. Detailed files are listed in Data and Code Availability.

| Claim or artifact | Estimand and critical assumptions | Evidence and status | What is not supported |
|---|---|---|---|
| Capacity and Gaussian calculations | Arithmetic; population threshold model; separate finite top-$m$ model | Formal derivations and numerical reproduction completed | Universal dual-channel necessity; measured ex-ante criticality |
| Weighted omission theory | Declared $\nu$, source-coverage law, delivery conversion, independent target sampling only for the CP statement | Formal result; deployment inputs not validated | A measured uniform $p_{\min}$, $k_{\mathrm{eff}}\ge2$, or 99.76% deployment recall |
| Academic parameter replay | Top-2%-citation retrospective proxy; semi-oracle citation-correlated scorer | Best semi-oracle proxy recall 0.28; separate supervised feature-scorer/list-optimization pilot maximum 0.135 (not paired or leakage-free); author-list coverage 1/52, institution lists 9/52–19/52, size-400 list 24/52 | Ex-ante decision relevance or per-proposition coverage probabilities |
| Financial historical configuration | Within-portfolio market proxy; realized labels enter selection score; seven agent/proxy configurations | Semi-oracle 120/126 agent–target evaluations = 0.952381; supervised feature-scorer 0.722222; 7/7 budget alarms; 150 monthly slots | R4-compliant 95% delivery; strict daily budget; 126 independent targets |
| Financial expanded configuration | Same semi-oracle design; 19 propositions on 18 company–days across 10 tickers | Semi-oracle 121/133 agent–target evaluations = 0.909774; post hoc 114/126 agent–company–day evaluations = 0.904762; supervised feature-scorer 0.789474; 7/7 alarms | A same-denominator or company–day interpretation of 18→19; causal news-expansion effect; point-in-time availability |
| Four-family judgment replay | Fixed digest after 2026-citation-dependent construction; citation-proxy opportunities; 80 model–seed configurations but 70 distinct digests | Controlled unique-key exploratory reanalysis; 71,914 valid keys, 86 gaps; results below | Whole-corpus recall, independent environments, modern RAG superiority, human value |
| O/G citation-return decomposition | Strict-singleton subset; retrospective $\log(1+\text{citation})$ return | Post hoc accounting: O/G critical-item return rises but noncritical-item return falls more | A causal explanation, welfare loss, or restored positive total return |
| H8/H9 transfer bridge | Family×version×task gate must be fixed before use | No family certified for human transfer; H8 directions inconsistent and H9 calibers non-commensurate | Human priors, human calibration, welfare, or virtue extrapolation |
| S2d, S4, S5, full battery | Matched model, raw input, retrieval access, and inference budget | Design only; not executed | Any claim that SEA outperforms end-to-end LLM, RAG, or welfare recommendation |
| Human evidence | HP-0 feasibility and future RCT protocols | No participant data; no recruitment | Every human-side effectiveness claim |

Two leakage channels must be distinguished. First, retrospective proxy dependence is **present by construction**: all four-family Channel-II digests use 2026 citation counts, and the financial semi-oracle score uses realized legal and market labels. Second, model memory and incomplete point-in-time availability remain unquantified. Titles and identifiers are shown to models; no memory ablation, post-cutoff replication, anonymized-title arm, or complete pre-availability filter has been performed.

### 9.2 Upstream opportunity and financial caliber audits

Across the frozen academic seed sets, 24–33 of the 52 proxy targets reach a run's digest. Family means are 28.37 (O), 28.40 (C), 27.70 (Q), and 28.70 (G), or 53.27%–55.19% upstream opportunity share. O and G share seeds 1–10 and therefore ten identical upstream digest pairs. The reported judgment recall is conditional on targets reaching this digest. The upstream share is not a legitimate multiplier for converting to end-to-end recall without a separately frozen joint estimand.

The financial audit reconstructs every current S2p selection and matches the stored proposition recall to $10^{-12}$. The historical semi-oracle headline is 120 hits over $7\times18$ recurring agent–target evaluations, not 126 independent targets. The expanded headline is 121 over $7\times19$ evaluations; those 19 propositions represent 18 company–days. The old and new $m=5$ arms use 150 monthly slots, not strict daily caps, and all seven configurations in each version trigger the budget-conflict alarm because supply 4.6/4.733 exceeds the Channel-I cap of three propositions per day. Thus even the earlier numerical crossing of 0.95 does not satisfy the claimed delivery assumptions.

The increase from 18 to 19 targets is valid in **proposition** units, but not in company–day units: the expanded 19 propositions represent 18 company–days. The configurations and target sets are non-paired, and the historical company–day denominator was not independently reconstructed. The supervised financial feature scorer is trained on day<15 realized labels and evaluated descriptively over the full month; its identical deterministic selection is repeated across seven agent rows, not seven independent feature experiments, and it is neither label-free nor a held-out estimate. The academic 0.135 route is a separate supervised feature-scorer/list-optimization pilot, not a paired replacement for the semi-oracle best arm, and its historical citation-derived features are not leakage-free.

Timestamp availability is also incomplete: among 19 expanded portfolio targets, seven have `acceptance_hour >= 13`, eight are news items without that timestamp, and only four satisfy the code's `<13` marker; the marker is a feature, not a filter. The class-by-proposition binary coverage matrix is released, but it is not repeated sampling for each proposition and cannot estimate a uniform pointwise floor or independence.

### 9.3 Four-family results: positive recall contrasts are not uniform value gains

The controlled rule-A reanalysis gives run-equal estimates and 10,000 run-bootstrap intervals. It remains post hoc, within one 30-day corpus, and exploratory.

| Family | Judgment recall | Parametric recall | $\Delta$recall [95% run CI] | $\Delta\log(1+\text{citation})$ return |
|---|---:|---:|---:|---:|
| O | 0.443790 | 0.413620 | +0.030170 [−0.003971, +0.064767] | −0.175016 [−0.293452, −0.053577] |
| C | 0.532600 | 0.403317 | +0.129283 [+0.098441, +0.158663] | +0.667380 [+0.539180, +0.802858] |
| Q | 0.516153 | 0.403265 | +0.112887 [+0.081432, +0.147666] | +0.426727 [+0.295044, +0.548216] |
| G | 0.519783 | 0.430371 | +0.089412 [+0.022924, +0.148522] | −0.219053 [−0.427112, −0.025626] |

O's run-cluster sign-flip $p=0.160128$. O has 19 positive and 11 negative within-run recall contrasts; C/Q/G have 28/2, 10/0, and 9/1, respectively. The evidence is therefore not a blanket cross-family benefit. Agent-day McNemar/CMH tails are nominal dependence approximations, not calibrated cross-corpus error rates. The honest feature value 0.241 is a fixed descriptive reference, not a paired arm. Family, backend, quantization, prompts, reasoning budgets, and runtime are confounded, while all configurations share labels and one corpus.

The previous “value” is a sum of $\log(1+\text{2026 citations})$, not decision utility or welfare. A new strict-singleton accounting decomposition, using 70,306 keys and no new model calls, gives:

| Family | $\Delta$critical-item citation return | $\Delta$noncritical-item citation return | Total citation return | $\Delta$selected count |
|---|---:|---:|---:|---:|
| O | +0.124007 | −0.299564 | −0.175557 | −0.044889 |
| C | +0.606797 | +0.056792 | +0.663589 | −0.009278 |
| Q | +0.510555 | −0.090163 | +0.420392 | −0.000936 |
| G | +0.410169 | −0.629270 | −0.219101 | −0.182926 |

For O, the critical-item component's run-bootstrap 95% interval is [−0.054770, +0.304276], so it crosses zero; G's is [+0.048621, +0.729638]. Noncritical-item intervals are [−0.403201, −0.186791] for O and [−0.781947, −0.459691] for G. C and Q's noncritical-item intervals also cross zero. Point estimates of critical-item citation return are positive for O/G, but the noncritical decline is larger in magnitude and total return remains negative. The negative selected-count contrasts show that the decomposition is consistent with both substitution and changed counts; it does not separate those mechanisms. The identity is accounting, not a psychological or structural causal explanation. Under the intentional favor-LLM endpoint, O/G total-return intervals include zero, so endpoint sensitivity must also remain visible. Most importantly, an objective based on ex-ante decision value must not be replaced by either recall or retrospective citations.

### 9.4 H8/H9: a failed or unadjudicated gate blocks human extrapolation

The transfer rule is family-, version-, and task-specific. Every required paradigm, direction, effect interval, sample minimum, and failure action must be fixed before a family is used for human-side conclusions. Any failed or unadjudicated component restricts that family to AI-mechanism description.

The existing H8 results do not pass such a gate: opposing-exposure directions reverse across families; accuracy-prompt effects are negative across the three named families, but one is near zero and outside the target effect interval; and one discrimination estimate exceeds the stated reference interval. All H8 outcomes are AI-task descriptions only, and the discrimination materials are not thereby certified as memory-free. Data completion for named tags is not the same as transfer validation.

H9 also cannot certify the gate as archived. On the agent's 40-question task, O/C/Q/G Brier scores are 0.17046/0.23206/0.23306/0.28480, with constant baseline 0.219375. O passes both the implemented Manifold-mean $\pm2\times$ rule and the separate 0.15–0.21 superforecaster reference interval; G falls in the report's distinct 0.24–0.30 layperson interval; C/Q lie between those literature intervals, and C/Q/G are worse than the agent task's constant baseline. The Manifold anchor has Brier 0.11169 on different questions and base rates and uses community terminal prices. These references are not one “human band,” do not implement the preregistered human-quantile criterion, and do not test monotone correctability on the incompletely archived per-question answers.

Accordingly, **no existing family is certified for human transfer**, even though O passes two descriptive numerical criteria. All replay findings in this paper are AI-task mechanism descriptions only.

## 10 A Proposed Minimum Protocol for the Next Matched Evaluation

A valid next experiment must start from raw candidate streams and include S2d end-to-end LLM screening, S4 RAG with safety filtering, S5 welfare-oriented recommendation, and full pull/push/budget/monitoring ablations. Arms must match model instance, raw inputs, retrieval permissions, index snapshots, context and reasoning budgets, and actual consumption limits. Family and backend cannot vary only with treatment.

At least three nonoverlapping time windows, two domains, and one post-cutoff or private corpus are required, with a final locked corpus untouched by design or tuning. Titles and authors should be anonymized in the decontamination arm, with exact/normalized string and semantic memory audits. Features require strict point-in-time timestamps. Ex-ante decision-relevance labels should be elicited independently of later citations and market outcomes; retrospective labels remain secondary proxies.

The inferential unit is the independent corpus or month, not agent-day. All numerators, denominators, missing records, conflicts, upstream omissions, and run-level aggregation rules must be released. These are design minima, not a guarantee that any completed implementation will identify every structural effect. A time-stamped public registry entry must precede unlocking the final corpus; an internally frozen document is not called public preregistration. The full protocol and missing/conflict rules are archived in `docs/MINIMAL_VALID_EXPERIMENT_v1.9.md`.

The future human protocol also needs one declared primary comparison and a longitudinal power model. For orientation only, the normal approximation at $d=0.35$, two-sided $\alpha=0.05$, and 80% power gives 128.145 analyzable participants per arm; 25% attrition gives 171 randomized participants per arm, or 513 across three arms. Two co-primary Bonferroni comparisons give approximately 207 per arm (621 total). Ceilings are applied independently to the unrounded $n$ and $n/(1-\text{attrition})$, not sequentially to an already rounded analyzable count. These are design calculations, not human data or a substitute for variance estimates from a feasibility study.

## 11 Limitations and Conclusion

The formal results are deliberately conditional. The update-value identity does not validate a credibility estimate. The Gaussian calculations do not describe every score distribution. Finite-pool expectations do not determine any one realized ranking. Submodular guarantees end at their certified ground sets and constraints. Weighted recall depends on the declared target distribution, joint source-coverage law, and actual delivery conversion; its mean confidence interval is not a pointwise guarantee. KKT prices require separability and concavity, EIG submodularity requires joint conditional independence given $(\omega,K)$, and subset logit is not a theory of every attention mechanism.

The empirical gaps are more consequential than the mathematical restrictions. Existing direct baselines are unexecuted; academic and financial scores contain retrospective information by construction; upstream and shared-corpus dependence prevent independent-environment interpretation; timestamp and model-memory audits are incomplete; negative and interval-crossing results preclude a robust-benefit narrative; and no human data or independent human mathematical sign-off exists. A working source tree and locally frozen protocol are not an immutable public release.

SEA nevertheless offers a useful discipline. It requires an information system to state who owns the objective, how it may be changed, which acquisition and filtering actions share a budget, what counts as a target, and where a candidate was lost between publication and actual consumption. Its near-term value is this explicit ownership, omission accounting, and audit structure, together with negative results that rule out overconfident deployment claims. Its comparative effectiveness and human consequences remain hypotheses for the matched, temporally valid experiments specified above.

## Data and Code Availability

The current public candidate snapshot is **`v1.9.0`**, maintained at <https://github.com/hurrywhen/sea-nuaa> and <https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa>. The tag, source files, and file-level hashes are recorded in `RELEASE_v1.9.md` and the artifact manifest linked from `docs/REPRODUCIBILITY_v1.9.md`. This is a public source-and-data release, not independent mathematical verification or a completed end-to-end experiment. The earlier v1.7 archive and DOI are real but do not include this revision or its new audits: version DOI <https://doi.org/10.5281/zenodo.23620920>; concept DOI <https://doi.org/10.5281/zenodo.23620919>. No v1.9-specific DOI is asserted here unless a separate persistent record is actually created. Internal frozen protocols are not called public preregistration without a registry URL.

The working tree contains the following read-only or independently regenerated checks:

- `tools/reproduce_v19_math.py` and `tools/test_v19_math.py`: population and finite-pool calculations, exact Pareto sums, the pooled-product counterexample, the unified-update binary example, and RCT design arithmetic;
- `sim/sea_pilot/audit_v19_financial_caliber.py`: financial selection reconstruction, agent–target and company–day accounting, supervised feature-scorer comparisons, budget alarms, timestamp counts, and the binary class-by-proposition coverage matrix;
- `sim/sea_pilot/audit_v19_upstream_digest.py`: upstream opportunity counts and complete-digest hashes for all 80 model–seed configurations;
- `sim/sea_pilot/audit_v19_recall_value_tradeoff.py`: strict-singleton decomposition of citation-weighted return, with recorded values checked against reconstructed selections;
- `sim/sea_pilot/recompute_replay_frozen.py`: the earlier controlled unique-key, 17-scenario reanalysis of 292 frozen shards;
- `sim/pilot/results/evidence_status_v1.9.json`: machine-readable evidence status;
- `docs/MINIMAL_VALID_EXPERIMENT_v1.9.md` and `docs/LITERATURE_SEARCH_v1.9.md`: the unexecuted validation protocol and scoped literature-search record.

Core commands are:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tools/test_v19_math.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v19.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v19_math.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_upstream_digest.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_recall_value_tradeoff.py --write --force
bash tools/build_review_pdf.sh en v1.9
python3 tools/check_pdf_textlayer.py latex/SEA_EN_v1.9_draft.pdf input/sovereign_epistemic_acquisition_EN_v1.9.md
```

Default audit behavior is read-only unless `--write` is supplied; replacement of a dedicated artifact set additionally requires `--force`. The financial historical comparison reads commit `8ffc7f5` through `git show` and does not change the worktree. The scripts make no LLM calls and create no human data. Live APIs and historical web pages can change, so bit-identical reproduction is claimed only for identified frozen inputs, not fresh downloads. Incomplete H9 raw-answer records, incomplete caches, shared corpus dependence, and the absence of direct baseline runs remain release-blocking limitations for any confirmatory claim.

## Human–AI Collaboration and Responsibility Statement

AI agents assisted with literature searching, mathematical re-derivation, code generation, numerical checks, and manuscript drafting. Model families studied in the replay are therefore both research instruments and research objects; shared prompts, infrastructure, corpora, and model biases remain conflict channels rather than independent replications.

The human authors retain responsibility for the research question, design decisions, treatment of negative results, authorship, and any submission decision. Computational tests and AI-assisted proof checks are not independent human mathematical verification. **Independent human mathematical review remains pending**, and no paper-wide Lean certification or completed independent reproduction is claimed. No AI system holds approval authority over objective writes, publication, or human-subject decisions.

## References

Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *American Economic Review, 110*(3), 629–676.

Aumann, R. J. (1976). Agreeing to disagree. *The Annals of Statistics, 4*(6), 1236–1239.

Bergman, O., & Whittaker, S. (2016). *The Science of Managing Our Digital Stuff*. MIT Press.

Berk, R. H. (1966). Limiting behavior of posterior distributions when the model is incorrect. *The Annals of Mathematical Statistics, 37*(1), 51–58. https://doi.org/10.1214/aoms/1177699597

Blackwell, D. (1953). Equivalent comparisons of experiments. *The Annals of Mathematical Statistics, 24*(2), 265–272.

Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review, 78*(1), 1–3.

Carbonell, J., & Goldstein, J. (1998). The use of MMR, diversity-based reranking for reordering documents and producing summaries. In *Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336).

Chaloner, K., & Verdinelli, I. (1995). Bayesian experimental design: A review. *Statistical Science, 10*(3), 273–304.

Charnov, E. L. (1976). Optimal foraging, the marginal value theorem. *Theoretical Population Biology, 9*(2), 129–136.

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Chwe, M. S.-Y. (2001). *Rational Ritual: Culture, Coordination, and Common Knowledge*. Princeton University Press.

Dang, V., & Croft, W. B. (2012). Diversity by proportionality: An election-based approach to search result diversification. In *Proceedings of the 35th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 65–74).

Esponda, I., & Pouzo, D. (2016). Berk–Nash equilibrium: A framework for modeling agents with misspecified models. *Econometrica, 84*(3), 1093–1130.

Fitz, N., Kushlev, K., Jagannathan, R., Lewis, T., Paliwal, D., & Ariely, D. (2019). Batching smartphone notifications can improve well-being. *Computers in Human Behavior, 101*, 84–94. https://doi.org/10.1016/j.chb.2019.07.016

Friedman, B., & Hendry, D. G. (2019). *Value Sensitive Design: Shaping Technology with Moral Imagination*. MIT Press.

Fudenberg, D., Romanyuk, G., & Strack, P. (2017). Active learning with a misspecified prior. *Theoretical Economics, 12*(3), 1155–1189.

Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30* (pp. 4878–4887).

Gittins, J. C. (1979). Bandit processes and dynamic allocation indices. *Journal of the Royal Statistical Society: Series B, 41*(2), 148–177.

Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association, 102*(477), 359–378.

Harper, F. M., Xu, F., Kaur, H., Condiff, K., Chang, S., & Terveen, L. G. (2015). Putting users in control of their recommendations. In *Proceedings of the 9th ACM Conference on Recommender Systems* (pp. 3–10). https://doi.org/10.1145/2792838.2800179

Hirsch, T., Merced, K., Narayanan, S., Imel, Z. E., & Atkins, D. C. (2017). Designing contestability: Interaction design, machine learning, and mental health. In *Proceedings of the 2017 Conference on Designing Interactive Systems* (pp. 95–99). https://doi.org/10.1145/3064663.3064703

Jugovac, M., & Jannach, D. (2017). Interacting with recommenders—Overview and research directions. *ACM Transactions on Interactive Intelligent Systems, 7*(3), Article 10, 1–46. https://doi.org/10.1145/3001837

Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research, 9*, 235–284.

Leskovec, J., Krause, A., Guestrin, C., Faloutsos, C., VanBriesen, J., & Glance, N. (2007). Cost-effective outbreak detection in networks. In *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 420–429).

Lin, H., & Bilmes, J. (2011). A class of submodular functions for document summarization. In *Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies* (pp. 510–520). https://aclanthology.org/P11-1052/

Lindley, D. V. (1956). On a measure of the information provided by an experiment. *The Annals of Mathematical Statistics, 27*(4), 986–1005.

Maćkowiak, B., Matějka, F., & Wiederholt, M. (2023). Rational inattention: A review. *Journal of Economic Literature, 61*(1), 226–273.

Matějka, F., & McKay, A. (2015). Rational inattention to discrete choices: A new foundation for the multinomial logit model. *American Economic Review, 105*(1), 272–298.

McCombs, M. E., & Shaw, D. L. (1972). The agenda-setting function of mass media. *Public Opinion Quarterly, 36*(2), 176–187. https://doi.org/10.1086/267990

Morris, S., & Shin, H. S. (2002). Social value of public information. *American Economic Review, 92*(5), 1521–1534.

Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology, 12*(4), 595–600.

Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming, 14*, 265–274.

Papadimitriou, C. H., & Tsitsiklis, J. N. (1999). The complexity of optimal queueing network control. *Mathematics of Operations Research, 24*(2), 293–305.

Pielot, M., Church, K., & de Oliveira, R. (2014). An in-situ study of mobile phone notifications. In *Proceedings of the 16th International Conference on Human-Computer Interaction with Mobile Devices & Services* (pp. 43–52).

Pirolli, P., & Card, S. K. (1999). Information foraging. *Psychological Review, 106*(4), 643–675.

Resnick, S. I. (1987). *Extreme Values, Regular Variation, and Point Processes*. Springer.

Santoni de Sio, F., & van den Hoven, J. (2018). Meaningful human control over autonomous systems: A philosophical account. *Frontiers in Robotics and AI, 5*, Article 15. https://doi.org/10.3389/frobt.2018.00015

Santos, R. L. T., Macdonald, C., & Ounis, I. (2010). Exploiting query reformulations for web search result diversification. In *Proceedings of the 19th International Conference on World Wide Web* (pp. 881–890). https://doi.org/10.1145/1772690.1772780

Savage, L. J. (1951). The theory of statistical decision. *Journal of the American Statistical Association, 46*(253), 55–67.

Settles, B. (2009). *Active Learning Literature Survey* (Computer Sciences Technical Report 1648). University of Wisconsin–Madison.

Sims, C. A. (2003). Implications of rational inattention. *Journal of Monetary Economics, 50*(3), 665–690.

Stigler, G. J. (1961). The economics of information. *Journal of Political Economy, 69*(3), 213–225.

Stray, J., Halevy, A., Assar, P., Hadfield-Menell, D., Boutilier, C., Ashar, A., et al. (2024). Building human values into recommender systems: An interdisciplinary synthesis. *ACM Transactions on Recommender Systems, 2*(3), Article 20, 1–57. https://doi.org/10.1145/3632297

Sviridenko, M. (2004). A note on maximizing a submodular set function subject to a knapsack constraint. *Operations Research Letters, 32*(1), 41–43.

Voorhees, E. M. (1998). Variations in relevance judgments and the measurement of retrieval effectiveness. In *Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 315–323). https://doi.org/10.1145/290941.291017

Wang, L., Lin, J., & Metzler, D. (2011). A cascade ranking model for efficient ranked retrieval. In *Proceedings of the 34th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 105–114). https://doi.org/10.1145/2009916.2009934

Weitzman, M. L. (1979). Optimal search for the best alternative. *Econometrica, 47*(3), 641–654.

Whittle, P. (1988). Restless bandits: Activity allocation in a changing world. *Journal of Applied Probability, 25*(A), 287–298.

## Appendix A Minimal Notation and Quantifier Guide

| Symbol | Meaning | Quantifier or scope |
|---|---|---|
| $T,N,\underline\tau$ | Cognitive budget, candidate count, minimum item cost | Per declared period |
| $h_t,\mathcal A_t(h_t)$ | Observable history and feasible actions | Proposition 3.1; latent states are not policy inputs and reduced state is not assumed Markov |
| $\mu,\widehat\mu$ | Prior and one actual update kernel | The same kernel for every observed signal |
| $c,\hat c$ | True and assumed reliability | Reliability-mixture specialization only |
| $\mathcal W,\mathrm{VOI}$ | Expected realized value and correctly specified information value | Distinct unless the whole model is correct |
| $F_0,F_1,Q_1$ | Noncritical/critical score laws and CDF quantile | $Q_1(1-R)$ captures upper-tail recall $R$ |
| $M,K,m,d'$ | Finite pool, critical count, selection size, Gaussian separation | Finite top-$m$ is not a population threshold |
| $Z_i(e),C_S(e)$ | Source coverage and union coverage | No delivery implied |
| $D_S(e),\delta_e(S)$ | Actual monitored consumption and conversion given coverage | Includes ingestion through actual reading |
| $\kappa_e(S),m_e(S)$ | Union-coverage probability and actual miss probability | $m_e=1-\kappa_e\delta_e$ |
| $w_e,\nu_e$ | Target weights and normalized target measure | $\nu_e=w_e/\sum_jw_j$ |
| $\mathcal M_\nu,\mathcal R_\nu$ | Weighted expected omission and weighted mean recall | Not a pointwise infimum |
| $q_e,R_{\mathrm{II}}(e)$ | Channel-I failure and conditional Channel-II recovery | Recovery uses failure weighting |
| $A_i,L_i,C_i$ | Availability, ingestion/linkage, selection/consumption stages | $D_i=A_iL_iC_i$ locally in Section 6.4 |
| $V_u,\nu$ | Concave value of time use and budget shadow price | KKT corner conditions required |
| $I_K(Q)$ | Conditional mutual information $I(\omega;Y_Q\mid K)$ | Submodular under joint conditional independence |
| $p_\lambda(A)$ | Distribution over $m$-subsets | Inclusion requires summing over subsets |
| $J(C_i,C_j)$ | Jaccard agenda overlap | Not common knowledge |

A probability statement about a fixed proposition must state whether it is conditional on that proposition, drawn from a superpopulation, or evaluated on one deterministic frozen corpus. A binary coverage matrix from one corpus supplies realized indicators, not repeated proposition-conditional Bernoulli experiments. A mean over propositions answers a different question from a lower bound over all propositions.

## Appendix B Regression Checks and Falsification Map

### B.1 Numerical identities

The reproduction script verifies the filtering ratio 0.998875, $d'=4.389337888$, AUC 0.999044514, population recalls 0.209639680 and 0.523766570, exact Pareto leakage 20.799886% and 6.919112%, their same-ratio approximations 20.629947% and 6.871634%, the weighted omission counterexample 0.410 versus 0.250, the binary update values $W=-0.24$ and $\mathrm{VOI}=0.24$, and the RCT design numbers 171 and 207 per arm. Finite-top-$m$ quadrature is checked for convergence and against 20,000 Monte Carlo realizations per separation. These are numerical checks of mathematical objects, not empirical validation.

### B.2 Falsification and audit map

| Formal object | Observation that would falsify its implementation or assumptions | Required report |
|---|---|---|
| Unified update model | Different update kernels selected using an unobserved branch label; wrong-prior nonnegative claim | Full joint model, prior, update kernel, and evaluation distribution |
| Population threshold model | Confusion of population threshold with finite top-$m$ order statistic; wrong quantile direction | Class-conditional laws, $\beta,\pi,R$, and boundary cases |
| Pareto approximation | Approximate expression written as an identity or compared using a different $m/K$ | Exact Gamma sum and same-ratio approximation |
| Weighted omission | Pooled class coverage inserted into a product; upstream/delivery losses omitted | $\nu$, per-target stages, $\kappa_e,\delta_e$, and actual consumption |
| CP mean bound | Mean interval described as an infimum interval; clustered targets treated as independent | Sampling design, cluster unit, one-sided CP definition, and target measure |
| Submodular guarantee | Ratio assigned to a nonmonotone full pool or unaugmented density greedy | Ground-set certificate and exact algorithm variant |
| EIG submodularity | Only pairwise independence given $\omega$ asserted | Joint conditional independence given $(\omega,K)$ |
| Subset-choice limit | Single-item logit used as an inclusion law | Subset action space, reference distribution, and capacity |
| Agenda overlap | Jaccard overlap interpreted as truth or common knowledge | Actual common consumption and, separately, public-announcement evidence |
| Empirical structure effect | Fixed digest, unmatched model/input/budget, or retrospective proxy used as deployment evidence | Raw-stream S2d/S4/S5 arms and independent temporal corpora |

### B.3 Deleted or demoted claims

No universal five-dimensional value summary, universal dual-channel necessity, measured $k_{\mathrm{eff}}$, CP-certified pointwise $p_{\min}$, degenerate-case tightness for arbitrary effective subset sizes, single-alternative logit inclusion probability, double-threshold cooling-queue theorem, mutual-information definition of non-capture, or human-virtue convergence result is asserted. These deletions are substantive scope corrections, not limitations that can be reversed by adding a disclaimer to the older formulas.

---

*(End of manuscript)*


