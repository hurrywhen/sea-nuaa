> **SUPERSEDED / 已被取代：** This is a historical version, not the current authoritative manuscript. Current version: `input/sovereign_epistemic_acquisition_EN_v1.13.md`. See `archive/README.md`. Do not cite this version’s claims without checking v1.13.

# Sovereign Epistemic Acquisition:\newline Conditional Components, Governance Audits, and Weighted Omission

**Wen Hu**<sup>1,2</sup>&nbsp;&nbsp;**Xutong Wang**<sup>1</sup>&nbsp;&nbsp;**Ya Yu**<sup>1</sup>

<sup>1</sup> College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China  
<sup>2</sup> Jiangsu Yunhefeng Intelligent Technology Co., Ltd., Jiangsu, China

Corresponding author: Wen Hu (huwen@nuaa.edu.cn)

November 2026 · Human–AI collaboration; independent human mathematical review remains pending

---

## Abstract

Active retrieval, passive filtering, and authority over the recommendation objective are usually modeled separately. This paper instead specifies a finite-horizon Sovereign Acquisition Problem (SAP) with explicit latent state, observable histories, monitoring/pull/push/delivery/override actions, authorized objective writes and rollback, multi-resource budgets, and consumption-based rewards. The paper is a **conditional-component and audit study**, not a globally solved SAP or a validated algorithm system. Its contributions are fivefold. First, the SAP tuple is mapped to restricted update, filtering, recall, and budget models; a worked example follows candidates through updating, linkage, quota allocation, delivery, opening, attendance, and weighted omission, and an executable guarded-step algorithm states its implementation complexity without claiming joint optimality. Second, S1–S4 governance requirements become deterministic conformance tests for unauthorized-write rejection, state-and-ranking rollback, fixed-supply platform invariance, supply-ecology logging, and audit-tamper detection. Third, one misspecified update kernel yields a value-minus-regret identity; population thresholds, finite top-$m$ selection, oracle capacity relaxations, and normalized expected leaked value are kept distinct. Fourth, end-to-end recall is expressed as weighted expected omission, $m_e=1-\kappa_e\delta_e$, with dependence-robust bounds and an explicit selected-to-consumed measurement chain. Fifth, retrospective audits show how nonempty-selection conditioning, retrospective labels, shared corpora, and unmatched model families can overturn strong effectiveness interpretations. Historical `picked` records are only selection proxies: they contain no delivered/opened/attended observations. All-existing-record zero-empty calculations are therefore retrospective descriptive sensitivities, not recovered consumption. No 95% deployment guarantee, end-to-end superiority, or human-welfare effect is claimed. The defensible contribution is an executable ownership interface, omission accounting, and falsification discipline; matched raw-stream evaluation on independent corpora remains future work.

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

The paper makes five contributions, all within the conditional-design/audit route.

1. **A closed problem statement without a joint-optimality claim.** Section 3 defines the SAP state, observations, actions, transition and reward kernels, resource budgets, authorization transitions, and observable histories. A component map, a numerical pipeline example, and a guarded-step algorithm make the interfaces executable; a counterexample shows why component guarantees do not compose into global optimality.
2. **Executable governance conformance.** S1–S4 are instantiated as inspectable state, authorized and reversible writes, fixed-supply counterfactual invariance, separate supply-ecology audits, hash-chained records, tamper detection, and recourse. These are software consistency tests, not evidence of meaningful human control or security against a malicious host.
3. **Behaviorally consistent conditional calculations.** One update kernel is used for every signal; value is separated from misspecification regret. Population thresholds, finite top-$m$ order statistics, clairvoyant capacity relaxations, and normalized expected leaked value are not interchanged. Standard KKT, submodular, and KL-choice results are explicitly inherited rather than presented as new general theorems.
4. **Consumption-aligned omission accounting.** The main object is weighted expected omission, not a pooled estimate inserted into a pointwise redundancy formula. Selection, delivery, opening, and attendance are separate events; only the last is actual consumption in the formal estimand.
5. **Evidence and reproduction audits.** The paper freezes every required historical financial input inside the public snapshot, distinguishes the designated retrospective descriptive caliber from nonempty-selection secondary analyses, publishes metric-specific denominators and all-scenario ranges, decomposes negative citation-weighted returns, and specifies one primary future matched comparison.

The following are not claimed: a globally optimal SAP algorithm; a universal need for dual channels; a five-dimensional sufficient statistic for all decision value; a measured independence coefficient $k_{\mathrm{eff}}$; a pointwise 95% or 99.76% deployment guarantee; a new KKT, Hoeffding, Poisson-binomial, minimax-regret, or submodular-greedy theorem; actual-consumption observations in the historical replay; or evidence that SEA improves human welfare.

### 1.3 Claim and evidence conventions

A **formal result** is a derivation under its stated assumptions. A **design rule** is a normative or engineering choice. A **descriptive pilot** summarizes a frozen retrospective artifact. A **confirmatory experiment** would require a time-stamped protocol, independent environments, matched baselines, and an immutable analysis package; no such complete experiment is reported here.

The word *recall* always requires four qualifiers: target set, probability measure or weighting, configuration, and consumption unit. In the formal model the terminal unit is attended/consumed; in the historical replay only `picked` is observed, so the empirical quantity is **retrospective selected-proxy opportunity recall**, never actual-consumption recall. The designated retrospective descriptive caliber includes every parseable existing policy key with empty selections set to selected-proxy zero; nonempty-selection and strict-singleton analyses are secondary. Missing keys and unresolved conflicts remain separate rather than being silently converted into observed abstentions. The authoritative evidence matrix appears once, in Section 9.

## 2 Related Work and Precise Positioning

### 2.1 Review method

The literature update is a **structured narrative positioning with targeted bibliographic verification**, not a systematic or formally logged scoping review. Search concepts, full representative queries, publisher/ACL/NeurIPS/arXiv/Crossref records, inclusion and exclusion rules, and access dates are archived in `docs/LITERATURE_SEARCH_v1.11.md`. AI-assisted search and author revision selected the sources; there was no independent dual screening. Earlier searches did not preserve complete hit and deduplication counts, so none are invented here and no PRISMA-style completeness is implied. Within this nonexhaustive search, we have not identified one formal integration that simultaneously treats pull and push under one multi-resource budget, explicit objective write/rollback/audit rights, consumption-weighted omission, and separate fixed-supply and supply-ecology counterfactual audits. This is not a claim that no such system exists, and each component has substantial prior work.

### 2.2 Acquisition, attention, and value of information

Search economics (Stigler, 1961), optimal stopping and Pandora's box (Weitzman, 1979), information foraging (Pirolli & Card, 1999), Bayesian experimental design (Lindley, 1956; Chaloner & Verdinelli, 1995), active learning (Settles, 2009), bandits (Gittins, 1979; Whittle, 1988), and rational inattention (Sims, 2003; Matějka & McKay, 2015; Maćkowiak, Matějka & Wiederholt, 2023) supply the pull-side foundations. Blackwell (1953) gives the correctly specified information-value benchmark. SAP uses these as components of a shared-budget control problem; it does not imply that their indices have the same units or that a layered solution is globally optimal.

Selective prediction and the reject option formalize the choice to abstain when confidence is inadequate (Chow, 1970; Geifman & El-Yaniv, 2017). Cascade ranking studies how cheap stages can preserve retrieval quality while reducing expensive computation (Wang, Lin & Metzler, 2011). Recall@k and relevance-judgment variability are established retrieval-evaluation concerns (Voorhees, 1998). Lewis et al. (2020) introduced retrieval-augmented generation (RAG), combining parametric generation with a nonparametric dense index; it is therefore a direct architectural comparator, not a name to invoke without citation. RAGAs and ARES separately evaluate context relevance, faithfulness, and answer quality (Es et al., 2024; Saad-Falcon et al., 2024), but neither turns those proxies into consumption, serving-cost, or latency measurements. These literatures motivate separate reporting of upstream candidate recall, judgment-layer recall, abstention, final consumption, and efficiency. SEA adds no new retrieval metric; it requires these established stages not to be collapsed into one headline number.

### 2.3 User control, welfare, and contestability

User-controlled recommendation already allows people to alter recommendation objectives and trade-offs. Harper et al. (2015), for example, let users tune popularity and recency controls; Jugovac and Jannach (2017) review a broader interaction literature. Welfare-oriented recommenders study objectives other than raw engagement (Allcott et al., 2020; Stray et al., 2024). It would therefore be inaccurate to claim that prior research never asked who configures a recommender's objective.

SEA's narrower distinction is the combination of explicit machine-state write authorization, reversible change logs, a common pull–push budget, and an end-to-end actual-consumption estimand. This is adjacent to, not a replacement for, meaningful human control (Santoni de Sio & van den Hoven, 2018), contestability (Hirsch et al., 2017), and value-sensitive design (Friedman & Hendry, 2019). These traditions also warn that a readable interface or a signature alone does not establish meaningful control.

### 2.4 Agentic recommendation and autonomous information seeking

Peng et al. (2025) review LLM-powered recommender agents across recommender-oriented, interaction-oriented, and simulation-oriented paradigms, with profile, memory, planning, and action modules. Lin et al. (2026), a verified arXiv roadmap rather than a peer-reviewed survey, covers retrieval-grounded assistance, tool orchestration, single- and multi-agent planning, reactive/proactive/mixed-initiative behavior, and layered evaluation including latency and token cost. These adjacent roadmaps substantially weaken any broad novelty claim about integrating acquisition, proactivity, planning, and evaluation. The checked roadmap does not use SEA's literal pull/push unified cognitive-budget formulation; SAP's narrower positioning is the conjunction of guarded objective writes, multi-resource pull/push accounting, terminal-consumption omission, and the two supply counterfactuals.

### 2.5 Diversified retrieval and submodular summarization

Maximal marginal relevance (Carbonell & Goldstein, 1998), xQuAD (Santos, Macdonald & Ounis, 2010), PM-2 (Dang & Croft, 2012), and submodular document summarization (Lin & Bilmes, 2011) directly address relevance, redundancy, and coverage. Facility-location objectives and classical monotone-submodular guarantees provide further foundations (Nemhauser, Wolsey & Fisher, 1978; Krause, Singh & Guestrin, 2008).

The SEA selection objective is an instance of this family, not an alternative invented independently of it. Weighted proposition coverage inherits diminishing returns; facility-location diversity is a standard submodular term. MMR is a sequential relevance–redundancy heuristic, xQuAD explicitly models subtopic coverage, and PM-2 targets proportional aspect representation. SEA differs mainly in its declared ownership constraints and its requirement to audit actual consumption. Its approximation ratios, when applicable, are inherited from standard algorithms and restricted to their certified domains (Leskovec et al., 2007; Sviridenko, 2004).

### 2.6 Misspecified learning and non-Bayesian realized value

The nonnegativity of correctly specified information value does not cover an agent acting on a wrong likelihood. Misspecified-statistics and misspecified-learning research studies exactly this divergence (Berk, 1966; Esponda & Pouzo, 2016; Fudenberg, Romanyuk & Strack, 2017). SEA uses this upstream directly: the environment generates signals under $c$, while one behaviorally implementable update kernel uses $\hat c$ for every signal. The resulting expected realized utility is not a Blackwell value unless the complete model, including the prior and posterior, is correctly specified.

### 2.7 Comparison matrix

**Table 1. Prior traditions, borrowed components, and remaining non-claims.**

| Tradition | What it already supplies | What SEA borrows | What SEA does not establish |
|---|---|---|---|
| Search, foraging, bandits, rational inattention | Acquisition and stopping rules | Pull operators and common-budget comparisons | Global optimality of the complete SAP |
| Controlled and welfare-oriented recommendation | User-configured objectives and welfare criteria | Explicit write/audit interface | First study of user objective control; superiority to those systems |
| MMR, xQuAD, PM-2, submodular summarization | Coverage/diversity objectives and greedy algorithms | Proposition coverage and facility-location diversity | A new submodularity or greedy theorem |
| Misspecified learning | Effects of acting on wrong models | One update kernel with $c\ne\hat c$ | General sufficiency of five semantic scoring coordinates |
| RAG, retrieval evaluation, and agentic recommendation | Retrieval–generation architectures, component evaluation, planning and proactive-agent roadmaps | Stage-specific opportunity, grounding, and efficiency accounting | First integration of proactivity or tools; superiority to RAG/agents |
| Human control, contestability, VSD | Governance and recourse principles | Authorized, reversible, auditable changes | Proof that formal controls create meaningful human control |

## 3 The Sovereign Acquisition Problem and Its Governance Constraints

### 3.1 Items, propositions, and the terminal consumption event

An information item $x_i$ belongs to a source class $\mathcal C_i$ and is mapped to one or more propositions $e\in E$. A proposition is not automatically a document, company–day, or event: the target construction $\kappa:x_i\mapsto e$ is versioned as part of the estimand. For each item and period, the implementation must distinguish the nested events

$$\mathrm{selected}\supseteq\mathrm{delivered}\supseteq\mathrm{opened}\supseteq\mathrm{attended/consumed}.$$

The last event, abbreviated $C_i$, is the terminal consumption unit used by the formal reward and recall definitions. An opening receipt is not sufficient for attention. If no attendance instrument exists, the appropriate value is *unobserved*, not “consumed” and not automatically zero. Section 9 therefore calls the historical `picked` field a selection proxy only.

### 3.2 Complete finite-horizon SAP tuple

A conditional SAP instance is the tuple

$$\mathrm{SAP}=\langle H,\gamma,\mathcal X,\mathcal Y,\widetilde{\mathcal A},\{\mathcal A_t\},P,r,\Phi,\rho_0,\mathcal G,\nu\rangle.\tag{1}$$

Its elements are as follows.

- **Horizon and discount.** $t=0,\ldots,H$, $H<\infty$, and $\gamma\in(0,1]$; $\rho_0(x_0,y_0)$ is the joint initial state–observation distribution and $h_0=(y_0)$. Conditional history laws are used only on positive-probability support; zero-probability histories are handled explicitly in Proposition 3.1.
- **Controlled state.** $x_t=(s_t,\vartheta_t,\mathcal V_t,Q_t,B_t,L_t,\chi_t)\in\mathcal X$. Here $s_t$ contains observable and latent environment, candidate, user, and producer states; $\vartheta_t=(w,g^{(2)},\pi_{\mathrm{mon}},\mathrm{thresholds})$ is the objective store; $\mathcal V_t$ is its append-only rollback version history; $Q_t$ contains ingestion, selection, delivery, exposure, and commitment queues; $L_t$ is the audit ledger; and $\chi_t$ contains public and emergency states.
- **Observation and history.** $y_t\in\mathcal Y$ contains source/query responses, candidate and budget observations, authorization receipts, delivery/opening/attendance receipts when measured, and audit observations. The policy information is $h_t=(y_0,a_0,\ldots,a_{t-1},y_t)$. Latent states are never policy inputs.
- **Attempted actions and feasible sets.** $a_t=(a_t^{\mathrm{mon}},a_t^{\mathrm{pull}},a_t^{\mathrm{push}},a_t^{\mathrm{del}},a_t^{\mathrm{write}},a_t^{\mathrm{ovr}})\in\widetilde{\mathcal A}$. Monitoring chooses sources; pull chooses queries/tools; push chooses a candidate subset; delivery chooses schedule/channel; write proposes $\vartheta^+$ or rollback; override chooses from a finite preauthorized safe whitelist or is disabled. The nonempty resource-feasible subset is $\mathcal A_t(h_t)$. Invalid writes remain observable *attempts* so that rejection can be logged; they do not silently change state.
- **Transition and observation kernel.** $P(x_{t+1},y_{t+1}\mid x_t,a_t)$ includes candidate ecology, producer behavior, user response, consumption, queue evolution, and the guarded store/ledger transitions below. No Markov assumption is imposed on the reduced vector $(K_t,\theta_t,B_t,\pi_{\mathrm{mon},t})$.
- **Budgets.** $B_t=(B_t^T,B_t^{\mathrm{cmp}},B_t^{\mathrm{call}},B_t^{\$},B_t^{\mathrm{risk}})$ records remaining time, computation, model/tool calls, money, and authorized risk. A resource-feasible action satisfies $0\le c(x_t,a_t)\le B_t$ componentwise and $B_{t+1}=B_t-c(x_t,a_t)+\zeta_t$, where $\zeta_t$ is a declared exogenous replenishment vector. The familiar $T_{\mathrm{pull}}+T_{\mathrm{push}}+T_{\mathrm{ref}}\le T$ is only the time coordinate. Tokens, fees, latency, and retries are logged resource uses, not hidden free operations.
- **Reward and target measure.** For authorized $\vartheta_t$,

  $$r_t=r^{\mathrm{dec}}_{\vartheta_t}(s_t,a_t,C_t)+r^{\mathrm{ref}}_{\vartheta_t}(s_t,a_t)-\sum_{\ell=1}^{L}\lambda_{\ell,t}h_{\ell,t}(s_t,a_t),$$

  with declared terminal cost $\Phi(x_{H+1})$. Decision reward uses actual consumption $C_t$, not selection. The target measure $\nu$ and its weights are part of $\vartheta$ and of the estimand. A policy $\pi_t(a_t\mid h_t)$ induces

  $$J(\pi)=\mathbb E^\pi\!\left[\sum_{t=0}^{H}\gamma^t r_t-\gamma^{H+1}\Phi(x_{H+1})\right].\tag{2}$$

The tuple closes the problem statement; it does not make the problem tractable or identify any personal utility. Figure 1 shows the information and authorization flow.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[font=\small,
 box/.style={draw,rounded corners,align=center,inner sep=4pt,text width=3.15cm},
 arr/.style={-{Latex[length=2mm]},thick}]
\node[box] (store) at (0,0) {Objective $\vartheta_t$ and rollback versions $\mathcal V_t$};
\node[box] (auth) at (4.5,0) {Authorization and rollback guard $\mathcal G$};
\node[box] (principal) at (9,0) {Reflective principal $R$: read, write, contest};
\node[box] (policy) at (0,-2.7) {History policy $\pi_t$: monitor, pull, push, deliver};
\node[box] (env) at (4.5,-2.7) {Action $a_t$ in environment and candidate ecology $s_t$};
\node[box] (obs) at (9,-2.7) {Observation $y_t$ and consumption receipts};
\node[box,text width=11cm] (ledger) at (4.5,-5.5) {Hash-chained ledger $L_t$: admission, ranking, delivery, override, rollback, evidence, and recourse};
\draw[arr] (principal) -- (auth);
\draw[arr] (auth) -- (store);
\draw[arr] (store) -- (policy);
\draw[arr] (policy) -- (env);
\draw[arr] (env) -- (obs);
\draw[arr] (obs.south) -- ++(0,-0.45) -| (policy.south);
\draw[arr] (policy.south) -- (ledger.north -| policy);
\draw[arr] (env.south) -- (ledger.north -| env);
\end{tikzpicture}
\caption{SAP information flow. Platform variables may affect the candidate ecology, but objective changes pass through the authorization guard. The ledger records both paths separately.}
\label{fig:sap-flow}
\end{figure}

### 3.3 Guarded objective transitions and finite-history existence

For a write proposal $(\vartheta^+,\sigma_R)$, the guard $\mathcal G$ checks the principal, scope, timestamp, schema, and rollback token. Period-$t$ ranking, delivery, and reward use the pre-write $\vartheta_t$; guard processing occurs after those decisions. If accepted, it appends $\vartheta_t$ to $\mathcal V_t$ and sets $\vartheta_{t+1}=\vartheta^+$; otherwise $\vartheta_{t+1}=\vartheta_t$ and a rejection event is appended. A valid rollback restores the identified version as a **newly appended current version**, preserving the append-only history. Every canonical guard-admitted attempt with a valid evidence envelope appends

$$\ell_{t+1}=(\ell_t,\mathrm{event},\mathrm{evidence\ pointer},H_{\mathrm{prev}}),\qquad
H_{t+1}=\mathrm{SHA256}(H_t\,\|\,\mathrm{canonical}(\ell_{t+1})).\tag{3}$$

Malformed requests rejected before guard admission may raise without a ledger append and are not counted as governed write attempts. Unauthorized guard-admitted writes leave the objective and version history unchanged apart from the appended rejection record; the full SAP state still advances through that ledger event. Hash chaining provides tamper evidence for the logged bytes; it is not a claim of consensus, secure key management, or protection against a host that can replace the entire store and verifier.

**Proposition 3.1 (Optimal policy for a finite observable-history SAP).** *Suppose the SAP has finite horizon $H$ and bounded one-period rewards (including reflection and harm terms) and bounded terminal cost. Primitive actions and observations have finite range; latent exogenous states also have finite range so that the model remains discrete. Let every authorization and audit variable available to the policy be included in $h_t$. Encode every resource, exposure, tolerance, authorization, audit, public, and emergency constraint into a nonempty finite feasible set $\mathcal A_t(h_t)$. Then an optimal deterministic history-dependent policy exists.*

**Proof.** Finite actions and observations generate finitely many observable histories at each finite time. Fix a full-support behavioral reference policy $\beta$, for example the uniform distribution over each nonempty finite $\mathcal A_t(h)$. For every history $h$ with $\Pr^\beta(h)>0$ and every feasible $a$ (which has positive probability under $\beta$), condition the full generative model on $h,a$ to define $r_t(h,a)=\mathbb E[r_t\mid h,a]$ and the marginal next-observation kernel $P(y_{t+1}\mid h,a)$. Define $\bar\Phi(h)=\mathbb E[\Phi(x_{H+1})\mid h]$ at $t=H+1$ on terminal histories with positive $\beta$-probability. These conditionings integrate over latent states and do not make them policy inputs. Full support covers every history–action pair reachable under any policy. At a history with zero probability under $\beta$ (and therefore under every policy), no posterior quantity is needed: assign any fixed feasible action and arbitrary finite continuation value consistent with the recursion. Such assignments cannot change values or optimality on reachable histories. Set $V_{H+1}(h)=-\bar\Phi(h)$ on positive-probability terminal histories and recursively compute

$$V_t(h)=\max_{a\in\mathcal A_t(h)}\left\{r_t(h,a)+\gamma\sum_{y_{t+1}}P(y_{t+1}\mid h,a)V_{t+1}(h,a,y_{t+1})\right\}.$$

Every maximum is over a nonempty finite set and is attained. A fixed tie rule and concatenation prove the result without latent-state knowledge. $\blacksquare$

This is an existence statement, not a tractable algorithm or a proof that a low-dimensional belief is sufficient. Continuous dwelling times require a separate Borel-space argument. Restless-bandit special cases are already PSPACE-hard (Papadimitriou & Tsitsiklis, 1999).

### 3.4 Component map and a non-composition counterexample

**Table 2. SAP components, additional restrictions, and the conclusions actually obtained.**

| SAP object or component | Additional restriction | Conclusion used | Why it does not solve the full SAP |
|---|---|---|---|
| Update and decision (Section 4) | One signal, one decision kernel, integrable utilities | $W=\mathrm{VOI}-\mathrm{Regret}$ | No multi-stage retrieval or quota optimization |
| Capacity and filtering (Sections 5.1–5.3) | Fixed values or fixed score laws; finite independent pool | Oracle relaxation, threshold feasibility, finite top-$m$ mean | Does not choose sources or learn scores |
| Coverage/diversity and online choice (Sections 5.4–5.5, 6.6) | Certified ground set, exact algorithm, iid online rewards | Inherited approximation or threshold result | Certificates stop at their feasible domains |
| Weighted omission (Section 6) | Frozen $\nu$, complete stage events, declared joint law | Coverage–consumption identity and mean bounds | Does not estimate missing stage observations |
| Pull prices and subset choice (Section 7) | Separable concavity, conditional independence, or fixed $m$ | KKT corners, EIG submodularity, subset logit | Adaptive knowledge and cross-channel coupling remain |
| Governance guard (Section 3.7) | Deterministic reference store, candidates, and verifier | Executable consistency and tamper tests | No psychological control or malicious-host security |

Component guarantees need not compose even when every later choice is optimal conditional on earlier choices. For a two-source monitoring problem, assign weight 3 to items $a,b,c,d$ and weight 2.5 to $g,h,i,j$. Let

$$A=\{a,b,c,d\},\quad B=\{a,b,g,h\},\quad C=\{c,d,i,j\},\quad D=\{c,d,g,h\}.$$

Their values are 12, 11, 11, and 11. Greedy chooses $A$; every second set adds 5, so a tie rule may choose $D$, yielding 17. The pair $B\cup C$ covers all eight items and yields 22. If all covered items can be consumed, subsequent optimal delivery cannot repair the earlier monitoring choice. The realized ratio $17/22\approx77.27\%$ **exceeds** the 75% worst-case two-step greedy guarantee $1-(1-1/2)^2=0.75$ but remains below the optimum 22. Thus the guarantee is not violated, yet greedy monitoring followed by optimal delivery is not jointly optimal.

### 3.5 One numerical pipeline from update to omission

Consider six equally weighted target propositions, $\nu_e=1/6$. Each has one raw candidate with declared ranking values $v=(6,5,4,3,2,1)$. The binary relevance prior is $1/2$, and the single correctly specified update kernel is a **symmetric binary channel**, $P(Y=1\mid\omega=1)=P(Y=0\mid\omega=0)=0.8$. A positive signal therefore gives posterior $q_e=0.8$ for every candidate. The provisional score is $q_ev_e$. Authentic availability holds for $e_1,\ldots,e_5$ but not $e_6$. The candidate for $e_5$ fails ingestion/authentication/linkage. Three quota slots select $e_1,e_2,e_3$; $e_4$ is linked but omitted by the quota. Delivery reaches $e_1,e_2$ only; both are opened. Attendance is instrumented for both opened items: $e_1$ attends and $e_2$ is measured as not attending. These are declared example events and measurements, not experimental data.

**Table 3. Worked pipeline; terminal consumption means observed attendance.**

| Target | Authentic | Linked | Score | Selected | Delivered | Opened | Consumed | First omission stage |
|---|---|---|---:|---|---|---|---|---|
| $e_1$ | yes | yes | 4.8 | yes | yes | yes | yes | none |
| $e_2$ | yes | yes | 4.0 | yes | yes | yes | no | attendance |
| $e_3$ | yes | yes | 3.2 | yes | no | no | no | delivery |
| $e_4$ | yes | yes | 2.4 | no | no | no | no | quota |
| $e_5$ | yes | no | 1.6 | no | no | no | no | linkage |
| $e_6$ | no | no | 0.8 | no | no | no | no | availability |

Consequently selected-proxy recall is $3/6$, delivered-proxy and opened-proxy recall are $2/6$, and actual-consumption recall is $1/6$. Total weighted omission is $5/6$, decomposed into $1/6$ availability omission plus $4/6$ post-availability omission. This arithmetic is the estimand template for Algorithm 1; it is not a performance estimate for SEA.

### 3.6 Algorithm 1: guarded SAP step and omission ledger

```text
Input: history h, current θ, version history, budgets B,
       raw candidates X, target map κ
1  Observe y and append it to h;
   inspect objective, defaults, and provenance.
2  Apply the SAME update kernel to every observed signal;
   log calls, tokens, cost, latency, and retries.
3  Ingest, authenticate, deduplicate, and link candidates
   to versioned propositions.
4  Rank the fixed linked pool using CURRENT θ and user state;
   platform revenue is not an input.
5  Choose a resource-feasible subset under
   time/compute/call/money/risk budgets.
6  Record selected, delivered, opened, and attended as
   DIFFERENT events with missingness flags.
7  Compute omission by target and first failed stage;
   evaluate period-t reward under the pre-write θ.
8  Process write/rollback attempts through G for period t+1;
   log every canonical guard-admitted attempt.
9  Append all decision and guard events to the hash chain;
   roll forward B and the observable history.
Output: next state, consumption receipts,
        resource ledger, target omission ledger
```

The complexity claim is decomposed rather than assigned to the whole guarded step. Let $L_\kappa=\sum_{i=1}^n|\kappa(x_i)|$ be the number of candidate–proposition associations and $B_{\mathrm{audit}}$ the total number of canonical audit bytes written in the period.

- **Ranking:** comparison sorting costs $O(n\log n)$ time and $O(n)$ working memory for candidate references, excluding score evaluation.
- **Linking and target accounting:** traversing already computed associations and initializing target ledgers costs $O(L_\kappa+|E|)$ time; materializing the associations requires $O(L_\kappa)$ additional memory, or they may be streamed. Candidate ingestion, authentication, deduplication, and computation of $\kappa$ have implementation-dependent cost $C_{\mathrm{link}}$ and are not bounded by $O(|E|)$.
- **Feasible-subset selection:** report $T_{\mathrm{select}}$ separately for the algorithm actually used. Exact $m$-subset enumeration considers $\binom nm$ subsets; ordinary cardinality greedy uses at most $m$ scans with implementation-dependent marginal-evaluation cost; knapsack and partial-enumeration variants have their own bounds. None follows automatically from the sorting bound.
- **Audit, updating, and scoring:** canonicalization and hash chaining are linear in $B_{\mathrm{audit}}$, with persistent storage additional. Update/scoring cost $C_{\mathrm{score}}$, model/tool calls, tokens, latency, fees, and retries must be measured rather than inferred from $n$.

Thus $O(n\log n)$ is only the comparison-sorting bound, and $O(n\log n+L_\kappa+|E|+B_{\mathrm{audit}}+C_{\mathrm{link}}+C_{\mathrm{score}}+T_{\mathrm{select}})$ is an accounting template under the stated implementations, not a universal running-time theorem. In the reference API, a `write_objective()` followed by `rank()` represents guard completion at $t$ followed by ranking at $t+1$. Algorithm 1 is an executable interface and audit schedule, not a globally optimal SAP solver.

### 3.7 S1–S4 as executable conformance properties

Let $\Psi^{\mathrm{plat}}$ denote third-party platform variables. The reference implementation in `sim/sea_governance/` instantiates the following checks; it does not infer them from a mutual-information slogan.

- **S1, inspectability:** the objective, defaults, parameters, and data provenance are readable by $R$.
- **S2, authorized writes and rollback:** every write needs $\sigma_R$, old/new values, timestamp, and version token. Unauthorized guard-admitted writes raise a rejection and leave the objective and version history unchanged apart from the rejection record; authorized rollback appends a restored objective and reproduces both its canonical bytes and the ranking.
- **S3, revenue exclusion and two counterfactuals:** $U_\vartheta$ contains no revenue term. For fixed candidate pool $C$, user state $\kappa$, and authorized $\vartheta$, tested $\psi,\psi'$ satisfy
  $$\operatorname{Rank}_\vartheta(C,\kappa;\psi)=\operatorname{Rank}_\vartheta(C,\kappa;\psi').$$
  A second test changes the candidate ecology. Any resulting ranking change is logged as **supply-mediated**, not misreported as a fixed-supply violation or as proof of direct objective capture.
- **S4, auditability and recourse:** admission, ranking, delivery, override, and rollback produce hash-linked evidence records. Modifying a logged event is detected; a contestation references the relevant record and receives a recourse outcome.

**Table 4. Minimum governance conformance evidence.**

| Property | Executable assertion | Scope boundary |
|---|---|---|
| Inspectability | Exported objective/default/provenance equals stored canonical state | Readability is not comprehension or meaningful control |
| Write guard | Missing/invalid authorization is rejected and logged | Host/key security is outside the test |
| Rollback | Objective bytes and ordered candidate IDs equal their pre-write values | Restoration of the external world is not claimed |
| Fixed-supply S3 | Platform-variable perturbation leaves ranking unchanged | Only tested variables and fixed supply |
| Supply-ecology S3 | Changed candidate supply and resulting rank delta are separately logged | No causal attribution beyond the constructed intervention |
| Audit S4 | Hash verification detects edited event; contest/recourse is replayable | Hash chaining is not distributed consensus |

No equation $I(U;\mathrm{Rev})=0$ is used: it would be neither necessary nor sufficient for non-capture. Passing Table 4 is a software consistency result, not a deployment or human-autonomy certificate.

### 3.8 Declaration burden and human–AI asymmetry

The onboarding declaration table is deferred to Supplementary Appendix SC. Conservative defaults support feasibility demonstrations, not identified personal utilities. S2 governs the machine store; it does not prove that human goals are untouched by content.

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

**Proposition 4.1 (Value minus misspecification regret).** *Under the integrability and attainment assumptions above,*

$$W(c,\hat c)=\mathrm{VOI}_c-\operatorname{Regret}_c(\hat c),\tag{4}$$

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

**Proposition 5.1 (Capacity and clairvoyant leakage relaxation).** *If $N$ items arrive, each costs at least $\underline\tau>0$, and the budget is $T$, then at most $T/\underline\tau$ items can be consumed. If $K$ critical propositions have nonnegative values $v_e$ and at most $m$ distinct propositions can be consumed, define $\mathcal D(\pi):=\mathbb E[\sum_{e=1}^Kv_e\mathbf 1\{e\text{ is not consumed by }\pi\}]$. Then*

$$\mathcal D(\pi)\ge\mathcal D^*:=\mathbb E\!\left[\sum_{r=m_0+1}^{K}V_{(r)}\right],\qquad m_0=\min(m,K),\tag{5}$$

*where $V_{(1)}\ge\cdots\ge V_{(K)}$ is the decreasing rearrangement. Equality holds exactly when the consumed critical value equals the top-$m_0$ critical value almost surely; ties are allowed. The quantity $\mathcal D^*$ is a **clairvoyant/oracle relaxation**, computed using realized criticality and values. It is not generally attainable by a feasible non-anticipating SAP policy.*

**Proof.** The consumed critical value cannot exceed the sum of the $m_0$ largest values. A policy that actually attains that sum reaches equality; an oracle that sees the realization and consumes its top-$m_0$ values is one such non-implementable relaxation. $\blacksquare$

For $v_e\overset{iid}{\sim}\mathrm{Pareto}(\alpha,v_{\min})$, $\alpha>1$, the exact order-statistic expectation is

$$\mathbb E V_{(r)}=v_{\min}\frac{\Gamma(r-1/\alpha)\Gamma(K+1)}{\Gamma(r)\Gamma(K+1-1/\alpha)}.$$

Thus the **normalized expected leaked value**—a ratio of expectations, not the expectation $\mathbb E[\sum_{r>m_0}V_{(r)}/\sum_e v_e]$ of a per-realization leaked share—is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}=1-\frac{\sum_{r=1}^{m_0}\mathbb E V_{(r)}}{Kv_{\min}\alpha/(\alpha-1)}.\tag{6}$$

As $K\to\infty$, $m\to\infty$, and $m/K\to\rho\in(0,1)$, the quantile-integral limit (Resnick, 1987) is

$$\frac{\mathcal D^*}{\mathbb E[\sum_e v_e]}\;\longrightarrow\;1-\rho^{(\alpha-1)/\alpha}.$$

At finite $K,m$, $1-(m/K)^{(\alpha-1)/\alpha}$ is therefore an approximation, not an equality. At $K=52,\alpha=1.5$, the exact/approximate pairs are 20.7999%/20.6299% for $m=26$ and 6.9191%/6.8716% for $m=42$. The latter approximation uses the actual ratio $42/52=0.807692$, not 0.8. Direct pass-through does not increase total consumption capacity; it changes how the same slots are allocated.

### 5.2 Population threshold model and boundary cases

Let noncritical and critical scores have continuous distributions $F_0,F_1$ and survival functions $\bar F_0,\bar F_1$, with critical mass $\pi\in(0,1)$. At a fixed threshold $t$, the population acceptance and recall are

$$\beta(t)=(1-\pi)\bar F_0(t)+\pi\bar F_1(t),\qquad R(t)=\bar F_1(t).$$

This is a population threshold identity. It is not an exact identity for the random threshold induced by finite top-$m$ selection.

**Proposition 5.2 (Threshold feasibility).** *For $0<R<1$ and $0<\beta<1$, a counting-necessary condition is $\beta\ge\pi R$. Let $\tau_R=Q_1(1-R)$, where $Q_1$ is the ordinary CDF quantile. Assuming the survival functions are continuous and strictly decreasing on their relevant supports, a threshold with acceptance $\beta$ and recall at least $R$ exists if and only if*

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

**Proposition 5.3 (Finite-pool expected recall).** *For continuous scores and $K\ge1$, symmetry among critical items gives*

$$\mathbb E R_{M,K,m}=\int f_1(x)\Pr\{N_0(x)+N_1(x)\le m-1\}\,dx,$$

*where, conditional on one marked critical score $x$,*

$$N_0(x)\sim\operatorname{Binomial}(M-K,\bar F_0(x)),\qquad N_1(x)\sim\operatorname{Binomial}(K-1,\bar F_1(x)),$$

*independently. The marked critical item is selected exactly when at most $m-1$ other scores exceed it.*

For the Gaussian example $M=800,K=8,m=10$, deterministic Gauss–Legendre quadrature and 20,000 independent Monte Carlo realizations give Table 5.

**Table 5. Population thresholds versus finite-pool top-$m$ selection.**

| $d'$ | Population threshold recall | Exact-formula $\mathbb E R_{800,8,10}$ (converged quadrature) | Realized recall 2.5%, 50%, 97.5% quantiles |
|---:|---:|---:|---:|
| 1.5 | 0.209640 | 0.208661 | 0.000, 0.250, 0.500 |
| 2.5 | 0.523767 | 0.524234 | 0.250, 0.500, 0.875 |
| 4.389338 | 0.950000 | 0.952626 | 0.750, 1.000, 1.000 |

The Monte Carlo estimate at the required separation is 0.952825 with numerical 95% interval [0.951825, 0.953825]. That interval quantifies Monte Carlo error in the mean only. The predictive quantiles describe variation across finite pools; neither is an empirical confidence interval. The finite expectation is close to, but not identical with, the population value and should not be replaced by the random top-$m$ threshold in Proposition 5.2. Reproduction code and quadrature-convergence tests accompany the paper.

### 5.4 Coverage–diversity objectives: inherited guarantees and their limits

For candidate set $A$, consider

$$U(A)=\sum_{e\in E}v_e\mathbf 1\{A\cap D_e\ne\varnothing\}+\mu\sum_{\sigma\in\mathcal S}\max_{i\in A}\operatorname{sim}(\sigma,i)-\lambda\sum_{i\in A}\hat m_i\tau_i,$$

with nonnegative values, similarities, costs, and weights, and the convention $\max_{i\in\varnothing}\operatorname{sim}(\sigma,i)=0$. The first term is weighted coverage and the second is facility-location diversity. Both are nonnegative, monotone, and submodular. The complete penalized objective remains submodular but need not be monotone.

Write $f(A)$ for the sum of the coverage and diversity terms. One explicit sufficient restriction is a ground set $\mathcal C_M$ such that, **for every** $i\in\mathcal C_M$ and **every** $A\subseteq\mathcal C_M\setminus\{i\}$,

$$f(A\cup\{i\})-f(A)\ge\lambda\hat m_i\tau_i.$$

Then $U$ is nonnegative and monotone throughout the subsets of $\mathcal C_M$; the condition is not a minimum taken only over positive-gain contexts, and zero-gain contexts cannot be silently discarded. For a cardinality domain $\{A\subseteq\mathcal C_M:|A|\le m\}$, standard ordinary greedy on $U$ inherits $1-1/e$ relative to the optimum **within that restricted domain**. For a knapsack domain $\{A\subseteq\mathcal C_M:\sum_{i\in A}c_i\le B\}$ with $c_i>0$, the specific combination of density greedy on $U$ and the best feasible singleton inherits $\tfrac12(1-1/e)$; depth-three partial enumeration with greedy completion inherits $1-1/e$ under the corresponding standard conditions (Leskovec et al., 2007; Sviridenko, 2004). Unaugmented density greedy is assigned neither ratio. Without the displayed restriction, only the unpenalized monotone objective receives these statements automatically.

This is the same algorithmic lineage as diversified retrieval and submodular summarization. The engineering contribution is the audit requirement to log monotonicity certificates, algorithm variant, residual capacities, and restricted optimum—not a new approximation theorem.

### 5.5 Online thresholds with explicit boundaries

Suppose an item arrives independently with probability $a\in(0,1]$ in each period; conditional on arrival, its reward $R=r(S)$ is iid with $\mathbb E R^+<\infty$ and $r$ strictly increasing. At most $b$ items can be consumed over the remaining periods and discarding is irrevocable. Let $W_i(b)$ be optimal continuation value and $\Delta_i(b)=W_i(b)-W_i(b-1)$.

**Proposition 5.4 (Threshold policy).** *With $W_i(0)=W_0(b)=0$ and $g_a(\tau)=a\mathbb E[(R-\tau)^+]$,*

$$W_i(b)=W_{i-1}(b)+g_a(\Delta_{i-1}(b)).$$

*It is strictly optimal to consume when $r(s)>\Delta_{i-1}(b)$ and not optimal when $r(s)<\Delta_{i-1}(b)$; either action is optimal on ties. Moreover $\Delta_i(b)$ is nonnegative, nonincreasing in $b$, and nondecreasing in $i$.*

The boundary-aware induction, including the distinct $b=1$ recursion and the Lipschitz argument, is deferred to Supplementary Appendix SA.1 (`docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md`). A finite cooling queue introduces occupancy, age, eviction, and decay states; this result does not establish a double-threshold queue policy.

## 6 Recall as Weighted Expected Omission

### 6.1 Separate source coverage from end-to-end delivery

Fix a monitoring set $S$ and proposition $e$. Let $Z_i(e)$ denote authentic coverage by source class $i$, with $p_i(e)=P(Z_i(e)=1)$, and define

$$C_S(e)=\bigcup_{i\in S}Z_i(e),\qquad \kappa_e(S)=P(C_S(e)).$$

Let $D_S(e)$ be actual consumption of $e$ through the monitored channel, with $D_S(e)\subseteq C_S(e)$. When $\kappa_e(S)>0$, define the complete delivery conversion probability

$$\delta_e(S):=P(D_S(e)\mid C_S(e)).$$

It includes ingestion, authentication, proposition linking, deduplication, quota allocation, selection, delivery, opening, and actual attendance/consumption. When $\kappa_e(S)=0$, actual consumption is zero and $\delta_e$ need not be defined; the convention $\kappa_e(S)\delta_e(S)=0$ is used in the identities below.

**Proposition 6.1 (Coverage–consumption identity and weighted omission).** *For each $e$, the actual miss probability is*

$$m_e(S):=P(\operatorname{miss}_S(e))=1-\kappa_e(S)\delta_e(S).\tag{7}$$

*For target weights $w_e\ge0$ with $W=\sum_ew_e>0$, define $\nu_e=w_e/W$. Then*

$$\mathcal M_\nu(S):=\sum_e\nu_em_e(S),\qquad \mathcal R_\nu(S):=1-\mathcal M_\nu(S)=\sum_e\nu_e\kappa_e(S)\delta_e(S).\tag{8}$$

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

**Corollary 6.2 (Weighted lower recall certificates).** *If logs or a structural model provide $\kappa_e(S)\ge\underline\kappa_e(S)\ge0$ and $\delta_e(S)\ge\underline\delta_e(S)\ge0$, then*

$$\mathcal R_\nu(S)\ge\sum_e\nu_e\underline\kappa_e(S)\underline\delta_e(S),\qquad
\mathcal M_\nu(S)\le1-\sum_e\nu_e\underline\kappa_e(S)\underline\delta_e(S).$$

*If $\mathcal M_\nu(S)\le\varepsilon$, then for every $\eta\in(0,1]$, the weight of propositions with pointwise miss probability above $\eta$ satisfies*

$$\nu\{e:m_e(S)>\eta\}\le\varepsilon/\eta.$$

The first statement follows from Proposition 6.1 and monotonicity. The tail statement is Markov's inequality for bounded $m_e$. It limits the weight of poorly covered propositions without pretending that every proposition has high recall.

A pooled class mean cannot be inserted into a proposition-wise product. Suppose two equally weighted propositions have class-coverages $p_i(e_1)=0.9$ and $p_i(e_2)=0.1$ for two classes, with independence within each proposition and perfect delivery. The correct weighted omission is

$$\tfrac12(0.1)^2+\tfrac12(0.9)^2=0.410.$$

The pooled class mean is 0.5, but $(1-0.5)^2=0.250$, which would overstate recall as 0.75 rather than the correct 0.59. Joint list coverage is already a union outcome; exponentiating it again would also count redundancy twice.

The former $(1-p_{\min})^{k_{\mathrm{eff}}}$ expression is therefore not used as the main estimand. If a uniform pointwise theorem is desired, it needs a genuine per-class, per-proposition floor and a certified independent subset. Degenerate floors also invalidate the old universal tightness statement: under its perfect-delivery assumption, omission one almost surely forces every coverage indicator to vanish almost surely; those degenerate indicators are mutually independent, so an arbitrary smaller effective independent-subset size cannot be constructed. The present Fréchet and weighted formulations avoid assigning an empirical value to $k_{\mathrm{eff}}$ altogether.

### 6.3 Two channels: failure-weighted recovery, not pooled recovery

Let $D_{\mathrm I}(e)$ and $D_{\mathrm II}(e)$ denote actual consumption by two channels, $q_e=P(D_{\mathrm I}(e)^c)$, and, when $q_e>0$,

$$R_{\mathrm{II}}(e):=P(D_{\mathrm II}(e)\mid D_{\mathrm I}(e)^c).$$

When $q_e=0$, omission is zero and the convention $q_e[1-R_{\mathrm{II}}(e)]=0$ is used without defining $R_{\mathrm{II}}(e)$.

**Proposition 6.3 (Total omission without cross-channel independence).**

$$P(\operatorname{miss}(e))=q_e[1-R_{\mathrm{II}}(e)],\qquad
\mathcal M_\nu^{\mathrm{tot}}=\sum_e\nu_eq_e[1-R_{\mathrm{II}}(e)].$$

If $Q_\nu=\sum_e\nu_eq_e>0$ and $\bar R_{\mathrm{II},q}:=Q_\nu^{-1}\sum_e\nu_eq_eR_{\mathrm{II}}(e)$, then

$$\mathcal M_\nu^{\mathrm{tot}}=(1-\bar R_{\mathrm{II},q})Q_\nu.$$

The recovery mean is weighted by Channel-I failure $q_e$, not by all opportunities and not by an unweighted pooled count. No independence between channels is assumed. A pooled recovery computed on a selected subpopulation does not identify a uniform per-proposition recovery floor.

### 6.4 An explicit availability-to-consumption decomposition

Audit the nested indicators $A_i(e)$ (authentic availability), $L_i(e)$ (ingestion/authentication/linkage), $Q_i(e)$ (quota selection), $\Delta_i(e)$ (delivery), $O_i(e)$ (opening), and $\Gamma_i(e)$ (attendance/actual consumption). The terminal item event is $D_i(e)=A_iL_iQ_i\Delta_iO_i\Gamma_i$, consistent with $D_S(e)$ in Proposition 6.1. `picked` identifies at most $Q_i$; it does not identify $\Delta_i,O_i$, or $\Gamma_i$. Missing stage receipts must carry an explicit unknown status rather than being silently interpreted as either success or abstention.

Define availability-only omission $M_A(e)=\cap_{i\in S}A_i(e)^c$ and total omission $M(e)=\cap_{i\in S}D_i(e)^c$. Then

$$M(e)=M_A(e)\;\dot\cup\;\big[M(e)\cap M_A(e)^c\big],$$

so

$$P(M(e))=P(M_A(e))+P\big(M(e)\cap M_A(e)^c\big).$$

The terms are source-availability omission and loss after at least one authentic item was available. For multiple candidate items, an arbitrary item's first failure does **not** partition a target's omission. Define cumulative target successes $\widetilde A=\cup_iA_i$, $\widetilde L=\cup_i(A_iL_i)$, $\widetilde Q=\cup_i(A_iL_iQ_i)$, $\widetilde\Delta=\cup_i(A_iL_iQ_i\Delta_i)$, $\widetilde O=\cup_i(A_iL_iQ_i\Delta_iO_i)$, and $D_S=\cup_iD_i$. The disjoint first-failed-stage events are then $\widetilde A^c$, $\widetilde A\cap\widetilde L^c$, $\widetilde L\cap\widetilde Q^c$, $\widetilde Q\cap\widetilde\Delta^c$, $\widetilde\Delta\cap\widetilde O^c$, and $\widetilde O\cap D_S^c$; they partition total omission into availability, linkage, quota, delivery, opening, and attendance losses. The worked example has one candidate per target, so its table is a special case. Figure 2 makes clear why selected-proxy recall is an upper bound on terminal consumption for the same logged population, but not necessarily for an all-assigned population whose missing records were excluded upstream.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[font=\scriptsize,
 stage/.style={draw,rounded corners,minimum height=9mm,align=center,inner sep=2pt,text width=1.65cm},
 arr/.style={-{Latex[length=1.7mm]},thick}]
\node[stage] (a) at (0,0) {authentic availability};
\node[stage] (l) at (2.4,0) {ingested and linked};
\node[stage] (q) at (4.8,0) {quota selected};
\node[stage] (d) at (7.2,0) {delivered};
\node[stage] (o) at (9.6,0) {opened};
\node[stage] (c) at (12,0) {attended / consumed};
\draw[arr] (a)--(l); \draw[arr] (l)--(q); \draw[arr] (q)--(d);
\draw[arr] (d)--(o); \draw[arr] (o)--(c);
\node[draw,rounded corners,align=center,inner sep=4pt,text width=11.4cm] (loss) at (6,-2.2)
 {First-failed-stage omission ledger: unavailable; linkage; quota; delivery; opening; attendance};
\draw[arr] (a)--(loss.north -| a); \draw[arr] (l)--(loss.north -| l);
\draw[arr] (q)--(loss.north -| q); \draw[arr] (d)--(loss.north -| d);
\draw[arr] (o)--(loss.north -| o); \draw[arr] (c)--(loss.north -| c);
\end{tikzpicture}
\caption{Staged omission from authentic availability to actual consumption. Each box is a different event and estimand. Historical \texttt{picked} logs stop at the third box.}
\label{fig:omission-stages}
\end{figure}

A claim of zero filtering-induced omission applies only conditional on the specified availability, linkage, and actual-consumption events; it is not an unconditional zero-miss guarantee.

### 6.5 What Clopper–Pearson can and cannot certify

Freeze the monitoring set and the complete policy. Suppose $n$ independent target–environment–evaluation units are generated, with target $E_j$ sampled from $\nu$ and with an independent realization of the complete pipeline, including its environment, quotas, and implementation randomness. Independent corpora or months—not thousands of shared-corpus agent-days—are the relevant inferential units for temporal deployment. Observe the **end-to-end actual-consumption** omission indicators

$$X_j=\mathbf 1\{\text{no monitored channel actually consumes }E_j\},\qquad X=\sum_{j=1}^nX_j.$$

Under this independent-unit superpopulation model, $X_j\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(\mathcal M_\nu(S))$, so $X\sim\operatorname{Binomial}(n,\mathcal M_\nu(S))$ regardless of dependence among source classes within a proposition. Independent target labels alone are insufficient when units share a day, quota, seed, or global environment. Let $U=\operatorname{CP}^+(X,n;\alpha)$ be the one-sided Clopper–Pearson upper bound (Clopper & Pearson, 1934) satisfying

$$\sum_{k=0}^{X}\binom nk U^k(1-U)^{n-k}=\alpha,$$

with $U=1$ when $X=n$. Then

$$\Pr\{\mathcal M_\nu(S)\le U\}\ge1-\alpha,\qquad
\Pr\{\mathcal R_\nu(S)\ge1-U\}\ge1-\alpha.\tag{9}$$

This statement estimates a weighted mean and automatically includes delivery failures. It does not estimate $\inf_{i,e}p_i(e)$ or $\inf_e m_e(S)$, and it requires no source-independence assumption.

By contrast, a CP interval for an average class-coverage proportion does not yield a uniform proposition-conditional lower bound. Nor does it identify a maximum independent-subset size, account for list selection on the same data, or supply simultaneous confidence across classes and propositions. A structural pointwise analysis would need fixed sampling units for every $(e,i)$, a pre-frozen independence model, simultaneous error allocation, and independent validation data. Time-replayed propositions require independent time blocks or an explicit superpopulation model. On one complete finite corpus, the proportion is descriptive; it should not be presented as a future-probability guarantee.

### 6.6 Monitoring-portfolio optimization

For realized coverage indicators $Z_i(e,\omega)$, define

$$U_{\mathrm{mon}}(S)=\sum_e w_e\,\mathbb E\!\left[\max_{i\in S}Z_i(e,\omega)\right],$$

with the empty-set maximum equal to zero. Each realized max-coverage function is monotone submodular, and expectation and nonnegative weighting preserve both properties. No independence is needed for this set-function result. Under a cardinality constraint, standard greedy inherits the $1-1/e$ ratio; under a knapsack constraint, the same algorithm-specific guarantees reviewed in Section 5.4 apply (Nemhauser et al., 1978; Leskovec et al., 2007; Sviridenko, 2004).

The independent-product expression is only one way to evaluate the objective under a joint model. For positively correlated pairs it need not be a conservative recall estimate, and for three or more classes even pairwise positive correlation alone gives no universal one-sided product interpretation. Monitoring selection and its evaluation should therefore use independent validation data and the realized joint coverage or a declared model, not a pooled proxy labeled as $p_{\min}$.

## 7 Pull Operators, Budget Prices, and Fixed-Capacity Choice

### 7.1 KKT prices with corner cases

Let $x_u\ge0$ be minutes allocated to use $u$, with differentiable, increasing, concave values $V_u$, $T>0$, and $\sum_ux_u=T$. If $V(x)=\sum_uV_u(x_u)$, the strictly positive feasible allocation supplies Slater's condition, and a feasible allocation $x^*$ is optimal if and only if some $\nu\ge0$ satisfies the standard Karush–Kuhn–Tucker conditions (Karush, 1939; Kuhn & Tucker, 1951):

$$V_u'(x_u^*)=\nu\quad(x_u^*>0),\qquad V_u'(0)\le\nu\quad(x_u^*=0).\tag{10}$$

This is the standard concave KKT characterization, not a new theorem. Funded uses share a marginal value; unfunded uses need not. Activating a previously unfunded use can produce first-order loss $(\nu-V_u'(0))\epsilon$, and a universal second-order statement is false. Pull query time, push reading, exploration, dwelling, and reflection can be compared through this price only after converting all values to the same utility-per-minute unit. Pandora's reservation index, a patch-cycle average, a slot threshold, and a Whittle index are not automatically the same scalar (Charnov, 1976; Weitzman, 1979; Whittle, 1988).

The KKT result does not solve interactions between retrieval and push novelty, stochastic path-dependent opening costs, or global knowledge-state coupling. Those remain outside the separable concave model.

### 7.2 Conditional EIG submodularity

Let $K$ be the current knowledge state and let $I_K(Q)=I(\omega;Y_Q\mid K)$ for a fixed nonadaptive query batch $Q$. For finite discrete variables, monotonicity follows from

$$I_K(Q\cup q)-I_K(Q)=I(Y_q;\omega\mid Y_Q,K)\ge0.$$

**Proposition 7.1 (Conditional-independence condition for EIG submodularity).** *If the full family $\{Y_q:q\in\mathcal Q\}$ is mutually conditionally independent given $(\omega,K)$, then $I_K$ is monotone submodular.*

The short entropy proof is deferred to Supplementary Appendix SA.2. Pairwise independence given only $\omega$ is insufficient. If $K$ is fixed, it may be suppressed; if queries adaptively change $K$, this static batch result does not automatically apply. Standard greedy guarantees are inherited only under the corresponding cardinality or knapsack algorithms and certified domain.

### 7.3 A correct fixed-capacity stochastic-choice limit

Single-alternative rational-inattention logit is not a probability law for overlapping events $\{i\in A\}$. To model selection of exactly $m$ items, the action itself must be a subset. Let $\mathcal A_m=\{A\subseteq[n]:|A|=m\}$, and consider the KL-regularized subset-choice problem

$$\max_{p\in\Delta(\mathcal A_m)}\left\{\sum_A p(A)U(A)-\lambda D_{\mathrm{KL}}(p\|\pi^0)\right\},\qquad \lambda>0,$$

where $\pi^0$ is a positive reference distribution over subsets. Equivalently, the objective is $\sum_Ap(A)U(A)+\lambda H(p)+\lambda\sum_Ap(A)\log\pi_A^0$.

**Proposition 7.2 (Subset logit and top-$m$ limit).** *The unique optimum is*

$$p_\lambda(A)=\frac{\pi^0_A\exp(U(A)/\lambda)}{\sum_{B\in\mathcal A_m}\pi^0_B\exp(U(B)/\lambda)},\tag{11}$$

*Inclusion probabilities are*

$$P_\lambda(i\in A)=\sum_{A\in\mathcal A_m:A\ni i}p_\lambda(A),$$

*not a single-item logit proportional to $\pi_i^0e^{u_i/\lambda}$. As $\lambda\downarrow0$, $p_\lambda$ concentrates on $\arg\max_{A\in\mathcal A_m}U(A)$, weighted by $\pi^0$ if several optima exist. If $U(A)=\sum_{i\in A}u_i$, this is the top-$m$ rule.*

The simplex-KKT and limiting argument appears in Supplementary Appendix SA.3. This proposition is a deliberate fixed-capacity subset model, not a consequence of Matějka–McKay single-alternative choice. It also does not identify the online opportunity-cost thresholds of Proposition 5.4 with a static information-cost parameter.

## 8 Measurement, Missingness, and Efficiency Audit Interfaces

### 8.1 Consumption, abstention, and measurement failure are different states

Every future policy run must use one versioned target–run key and record each stage as 0, 1, or unknown with timestamp and evidence pointer. An empty `selected` set is not a sufficient reason code. Valid abstention requires an explicit policy decision and a frozen reason such as `no_authorized_value` or `no_feasible_candidate`; parser, transport, retry-pending, execution, and attendance-instrument failures are different states. Valid abstention remains in the all-assigned denominator and implies no consumption. A failure is not retroactively reclassified as abstention.

**Table 6. Minimum event, attendance-measurement, and efficiency schema for a future matched run.**

| Field group | Required fields | Aggregation rule |
|---|---|---|
| Identity | corpus/month, locked arm, model/seed, target, candidate, attempt | Independent corpus/month is the inferential unit |
| Stages | available, linked, selected, delivered, opened, attended; each 0/1/unknown | Report every transition and first failed stage |
| Attendance instrument | domain/instrument/version, raw-event pointer, threshold, validation-set hash, assessor-blinding status | Positive and negative attendance require a valid completed measurement; instrument failure is unknown |
| Missingness and outcome | explicit abstention, parse/transport/execution/instrument failure, conflict, unknown | All-assigned failure-composite primary; alternative missing-data analyses are sensitivity only |
| Resources | model/tool calls, input/output tokens, compute, fee, wall latency, retries | Per run and per successfully consumed target |
| Governance | objective version, authorization, rollback, evidence pointer, contest outcome | Fixed-supply and supply-ecology audits separate |

For a resource total $Z$ and $n_{\mathrm{cons}}>0$ successfully consumed targets, report $Z/n_{\mathrm{cons}}$ alongside the run total; if $n_{\mathrm{cons}}=0$, the ratio is undefined. Higher selected-proxy recall with greater resource use is not a budget advantage. Historical logs lack this schema, so no historical efficiency or consumption values are imputed.

### 8.2 Preregistered attendance instruments and the primary missing-outcome rule

Before unlocking arm outcomes, each corpus domain must freeze an **instrument registry** containing the instrument, decision rule, thresholds, validation data and code, raw-event schema, and sensitivity versions. For digital text, the default primary instrument is a combination of (i) a valid reading event using focused visibility, elapsed engaged time, and content-coverage signals and (ii) an active content-linked confirmation or task-related operation. Opening or dwell time alone is insufficient. For machine-to-machine private corpora, a content-addressed receipt showing that the complete item entered a declared downstream task context, plus a task operation referencing that receipt, may measure *machine consumption*; it must be reported separately and never called human attention.

Thresholds must be estimated on an independent measurement-validation set with blinded reference annotation, then frozen before comparative outcomes are inspected. The registry must report validation error and threshold sensitivity (including prespecified alternative instruments), not claim that a universal seconds cutoff measures attention. Human adjudicators and validation annotators must be blind to arm, model family, and comparative outcomes; automated adjudication code is frozen with the registry. Any failed, incomplete, invalid, or non-adjudicable measurement yields `attended=unknown`, never an automatic zero.

The primary endpoint uses one rule for every assigned target–run. It is omission ($Y_j=1$) unless at least one channel has a valid positive attendance/consumption measurement ($Y_j=0$). Thus explicit abstention, observed non-attendance, and missing terminal outcomes caused by parse, transport, execution, or instrument failure all enter the **all-assigned failure-composite weighted omission** as $Y_j=1$. This estimand measures failure to obtain confirmed actual consumption; it does not recover latent consumption when measurement fails. Failure coding is conservative for an arm's omission level but need not be conservative for a between-arm contrast, so missingness is reported by arm and stage.

Prespecified sensitivity analyses code unknown terminal outcomes as consumed, use inverse-probability weighting with a frozen arm-aware missingness model, and, if separately justified, multiple imputation; none replaces the primary rule after seeing results. The analysis must publish assignment, instrument validity, missingness reasons, and all sensitivity results before unblinding interpretation. No post-hoc choice between “missing” and “valid abstention” is permitted.

### 8.3 Governance and demoted material

The 14 deterministic S1–S4 tests check software conformance only; they do not identify treatment effects, establish comprehension, or secure a production host. Emergency override, agenda/common-knowledge, human-measurement, and H8/H9 material remains in `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.11.md`, and deferred proofs and secondary tables in `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md`; none supplies effectiveness or welfare evidence.

# Part III Evidence, Falsification, and Scope

## 9 Evidence Status and Controlled Reanalyses

### 9.1 Authoritative claim–assumption–evidence matrix

Table 7 is the single authoritative summary of empirical status. “Completed” refers only to the named retrospective or synthetic artifact, not to validation of SEA as a whole. Detailed files are listed in Data and Code Availability.

**Table 7. Claim–assumption–evidence matrix.**

| Claim or artifact | Estimand and critical assumptions | Evidence and status | What is not supported |
|---|---|---|---|
| S1–S4 governance reference | Deterministic synthetic candidates, structural authorization fixtures, retained audit anchor | 14/14 conformance and negative tests pass; fixed-supply and supply-ecology counterfactuals separate | Authenticated identity, malicious-host security, meaningful human control, or end-to-end effectiveness |
| Capacity and Gaussian calculations | Arithmetic; population threshold model; separate finite top-$m$ model | Formal derivations and numerical reproduction completed | Universal dual-channel necessity; measured ex-ante criticality |
| Weighted omission theory | Declared $\nu$, source-coverage law, consumption conversion, independent target sampling only for the CP statement | Formal result; deployment inputs not validated | A measured uniform $p_{\min}$, $k_{\mathrm{eff}}\ge2$, or 99.76% deployment recall |
| Academic parameter replay | Top-2%-citation retrospective proxy; semi-oracle citation-correlated scorer | Best semi-oracle selected-proxy recall 0.28; separate supervised feature-scorer/list-optimization pilot maximum 0.135 (not paired or leakage-free); author-list coverage 1/52, institution lists 9/52–19/52, size-400 list 24/52 | Ex-ante decision relevance, actual consumption, or per-proposition coverage probabilities |
| Financial historical configuration | Frozen historical rows; within-portfolio market proxy; realized labels enter selection score; seven agent/proxy configurations | Frozen-row aggregate 120/126 = 0.952381; supervised feature-scorer 0.722222; 7/7 budget alarms; 150 monthly slots; public CSV SHA-256 80e953d1…b495024 | Independent reconstruction of historical selections or company–day denominator; R4-compliant 95% delivery; 126 independent targets |
| Financial expanded configuration | Same semi-oracle design; 19 propositions on 18 company–days across 10 tickers | Semi-oracle 121/133 agent–target evaluations = 0.909774; post hoc 114/126 agent–company–day evaluations = 0.904762; supervised feature-scorer 0.789474; 7/7 alarms | A same-denominator or company–day interpretation of 18→19; causal news-expansion effect; point-in-time availability |
| Four-family judgment replay | Fixed digest after 2026-citation-dependent construction; citation-proxy opportunities; 80 model–seed configurations but 70 distinct digests; `picked` is selected only | 71,970 existing keys and 30 no-row keys; all-record zero-empty selected-proxy sensitivity, metric-resolved G, nonempty Rule A, strict singleton, and 17 scenarios below | Actual delivery/opening/attendance, valid versus failed abstention, whole-corpus recall, independent environments, RAG superiority, human value |
| O/G citation-return decomposition | Strict-singleton subset; retrospective $\log(1+\text{citation})$ return | Post hoc accounting: O/G critical-item return rises but noncritical-item return falls more | A causal explanation, welfare loss, or restored positive total return |
| H8/H9 transfer bridge | Family×version×task gate must be fixed before use | No family certified for human transfer; H8 directions inconsistent and H9 calibers non-commensurate | Human priors, human calibration, welfare, or virtue extrapolation |
| S2d, S4, S5, full battery | Matched model, raw input, retrieval access, and inference budget | Design only; not executed | Any claim that SEA outperforms end-to-end LLM, RAG, or welfare recommendation |
| Human evidence | HP-0 feasibility and future RCT protocols | No participant data; no recruitment | Every human-side effectiveness claim |

Two leakage channels must be distinguished. First, retrospective proxy dependence is **present by construction**: all four-family Channel-II digests use 2026 citation counts, and the financial semi-oracle score uses realized legal and market labels. Second, model memory and incomplete point-in-time availability remain unquantified. Titles and identifiers are shown to models; no memory ablation, post-cutoff replication, anonymized-title arm, or complete pre-availability filter has been performed.

### 9.2 Upstream opportunity and financial caliber audits

Across the frozen academic seed sets, 24–33 of the 52 proxy targets reach a run's digest. Family means are 28.37 (O), 28.40 (C), 27.70 (Q), and 28.70 (G), or 53.27%–55.19% upstream opportunity share. O and G share seeds 1–10 and therefore ten identical upstream digest pairs. The reported judgment recall is conditional on targets reaching this digest. The upstream share is not a legitimate multiplier for converting to end-to-end recall without a separately frozen joint estimand.

The financial audit reconstructs every **expanded-configuration parametric S2p** selection to $10^{-12}$; S2p-feat values remain frozen-row aggregates. The historical comparison aggregates the public 1,260-row `historical_p2_rows_8ffc7f5.csv`; default reproduction verifies its bytes and row count without reading Git history, while historical selections and the company–day denominator remain unreconstructed. Historical 120 hits over $7\times18$ recurring agent–target evaluations are not 126 independent targets. Expanded 121 hits over $7\times19$ evaluations concern 19 propositions on 18 company–days. The non-paired arms use 150 monthly slots and trigger 7/7 budget alarms: inherited historical supply 4.6 (not verified from the pinned CSV) and reconstructed expanded supply 4.733 exceed the Channel-I cap of three per day. Thus crossing 0.95 does not satisfy the claimed delivery assumptions.

The supervised financial scorer trains on day<15 realized labels and is evaluated over the full month; its deterministic selection repeats across seven agent rows, not seven independent or held-out experiments. The academic 0.135 route is likewise a separate, non-paired supervised pilot with leakage-prone citation features. Among 19 expanded targets, seven have `acceptance_hour >= 13`, eight lack that timestamp, and only four meet the code's `<13` marker—a feature, not a filter. The class-by-proposition binary matrix is not repeated sampling and identifies neither a uniform pointwise floor nor independence.

### 9.3 Four-family selected-proxy results and calibers

All intervals in this section are **exploratory run-level descriptive intervals**: 10,000 whole-run percentile bootstrap resamples within family (Efron, 1979; seed 42). Q/G have only 10 runs. Resampling does not include shared-corpus, label, missingness, duplicate-arbitration, backend, or model dependence. The 30-day corpus—not the agent-day count—is the effective independent environment.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[font=\scriptsize,
 box/.style={draw,rounded corners,align=center,inner sep=3pt,text width=2.55cm},
 conf/.style={draw,dashed,align=center,inner sep=3pt,text width=3.1cm},
 arr/.style={-{Latex[length=1.7mm]},thick}]
\node[box] (label) at (0,0) {2026 citations and realized labels};
\node[box] (digest) at (3.6,0) {Fixed 30-day digest};
\node[box] (pick) at (7.2,0) {Model \texttt{picked}: selected proxy};
\node[box] (proxy) at (10.8,0) {Recall and citation-return proxies};
\node[conf] (shared) at (0,-2.4) {One shared corpus and labels; upstream opportunity 53.27--55.19\%};
\node[conf] (family) at (7.2,-2.4) {Family, backend, prompt, quantization, and inference budget};
\node[conf] (missing) at (7.2,2.1) {Delivered, opened, attended: UNOBSERVED};
\draw[arr] (label)--(digest); \draw[arr] (digest)--(pick); \draw[arr] (pick)--(proxy);
\draw[arr,dashed] (shared)--(digest);
\draw[arr,dashed] (family)--(pick); \draw[arr,dashed] (missing)--(proxy);
\node[box] (raw) at (0,-5.4) {Future locked raw streams and independent corpora/months};
\node[box] (arms) at (3.6,-5.4) {Same model, input, access, and budget: SEA versus end-to-end screening};
\node[box] (stages) at (7.2,-5.4) {Selected $\rightarrow$ delivered $\rightarrow$ opened $\rightarrow$ attended; efficiency};
\node[box] (primary) at (10.8,-5.4) {Primary: all-assigned failure-composite omission};
\draw[arr] (raw)--(arms); \draw[arr] (arms)--(stages); \draw[arr] (stages)--(primary);
\end{tikzpicture}
\caption{Identification structure. The historical upper path conditions on a fixed digest, shares labels and corpus, confounds family with infrastructure, and stops at selection. The lower path is an unexecuted matched design, not new evidence.}
\label{fig:identification}
\end{figure}

The snapshot has 73,704 structurally parseable records on **71,970 existing keys**: 71,914 nonempty-selection keys plus 56 empty-only keys. Thirty no-row keys remain missing. There are 157 empty records, including 154 stored `parse-error` records; historical logs cannot distinguish valid abstention from other silent execution failures. No delivered/opened/attended fields exist. Table 8 therefore uses explicit **retrospective descriptive** names: these are selected-proxy calculations on observed records, not intention-to-treat analyses and not recovered actual consumption.

\Needspace{16em}

**Table 8. Analysis populations and aggregation rules; R/V/S = recall/citation-return/paired-sign resolved keys.**

| Caliber | R/V/S keys | Empty selections and conflicts | Role |
|---|---|---|---|
| `ALL_EXISTING_`\allowbreak `RECORD_MEAN_`\allowbreak `ZERO_EMPTY` | 71,970 / 71,970 / NA | Every existing key once; equal-weight all records within key; `picked=[]` is selected-proxy zero; conflicts retained as attempt means; 30 no-row keys missing | Designated retrospective descriptive caliber; recorded-attempt mean |
| `METRIC_RESOLVED_`\allowbreak `ZERO_EMPTY` (G) | 71,629 / 70,732 / 71,674 | Empty-only keys zero; metric-inconsistent duplicates and no-row keys excluded | Conflict-refusing zero-empty sensitivity |
| Rule A (nonempty) | 71,573 / 70,676 / 71,618 | Nonempty records only; each metric uses its own consistent-record cohort | Secondary historical caliber |
| Strict singleton (C) | 70,306 / 70,306 / 70,306 | Exactly one nonempty valid record per existing key | Secondary common-cohort caliber |

Table 9 reports the designated all-existing-key retrospective descriptive caliber. If $\bar h_k$ is the record-averaged selected-hit numerator for key $k$, a run's recall is $\sum_k\bar h_k/\sum_k n^{\mathrm{crit}}_k$, a ratio of sums—not $|\mathcal K|^{-1}\sum_k(\bar h_k/n^{\mathrm{crit}}_k)$. Keys with more critical opportunities therefore weigh more in that run. Citation return is the equal-key mean of within-key attempt-mean contrasts, and family estimates are unweighted run means. Key counts are denominators, not independent-sample claims.

\Needspace{12em}

**Table 9. `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`: all existing keys, selected-proxy zero for empty picks, exploratory run-level intervals.**

| Family | R/V keys | Selected recall | Parametric recall | $\Delta$recall [interval] | $\Delta$citation return [interval] |
|---|---:|---:|---:|---:|---:|
| O | 26,996 | 0.443161 | 0.413441 | +0.029720 [−0.004409, +0.064360] | −0.181292 [−0.297932, −0.062012] |
| C | 26,987 | 0.532275 | 0.403215 | +0.129060 [+0.098475, +0.158255] | +0.662236 [+0.534883, +0.796727] |
| Q | 8,998 | 0.513909 | 0.403200 | +0.110709 [+0.080555, +0.144612] | +0.396418 [+0.258508, +0.521986] |
| G | 8,989 | 0.517008 | 0.430937 | +0.086071 [+0.019272, +0.144873] | −0.251347 [−0.457599, −0.062888] |

Raw recomputation of the conflict-refusing G caliber matches frozen scenario G for 80/80 runs (maximum absolute discrepancy $9.71\times10^{-17}$). The complete Rule A and strict-singleton tables are deferred to Supplementary Appendix SB.1–SB.2 rather than mixed with Table 9's population.

O's run-cluster sign-flip $p=0.160128$; O has 19 positive and 11 negative within-run recall contrasts, while C/Q/G have 28/2, 10/0, and 9/1. Agent-day McNemar and Cochran–Mantel–Haenszel calculations (McNemar, 1947; Cochran, 1954; Mantel & Haenszel, 1959) are nominal dependence approximations, not calibrated cross-corpus error rates. The honest feature value 0.241 is a fixed descriptive reference, not a paired arm.

All 68 scenario-by-family estimates and denominators are consolidated in `scenario_effects.csv` and Supplementary Table SB3. Recall point estimates stay positive in all 17 scenarios; citation return stays positive for C/Q and negative for O/G. Zero point-estimate sign changes do not make every interval exclude zero and do not identify a structural effect. Full scenario-by-family denominators and intervals are in `scenario_effects.csv`.

The previous “value” is a sum of $\log(1+\text{2026 citations})$, not decision utility or welfare. The strict-singleton citation-return decomposition uses a different 70,306-key cohort and is reported in Supplementary Appendix SB.2. Positive O/G critical-item point estimates are outweighed by noncritical declines; O's critical-item interval crosses zero, and the favor-LLM endpoint lets O/G total-return intervals include zero. This is accounting, not a causal explanation or ex-ante decision value.

Finally, the historical shards contain zero archived call, token, fee, latency, or retry fields in the required schema. Section 8 defines prospective efficiency reporting; no retrospective efficiency advantage is inferred. Family, backend, quantization, prompts, reasoning budgets, and runtime remain confounded.

### 9.4 Human-transfer boundary

No model family is certified for human transfer. The H8/H9 details remain in `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.11.md` as AI-task descriptions only, not evidence for human learning, welfare, or the selected-proxy effects above.

## 10 A Proposed Minimum Protocol for the Next Matched Evaluation

The **one primary comparison** is SEA's guarded staged pipeline versus the same model performing end-to-end screening. The **one primary outcome** is the all-assigned failure-composite weighted omission of confirmed actual consumption from the raw candidate stream, using Section 8.2's frozen rule: unknown terminal outcomes count as failure, while alternative missing-data methods are sensitivity analyses. RAG with safety filtering (S4), welfare-oriented recommendation (S5), hierarchical secondary outcomes, and pull/push/budget/monitoring ablations use prespecified gatekeeping; there are not multiple primary outcomes. Arms must match model instance, raw inputs, retrieval permissions, index snapshots, context and reasoning budgets, and consumption limits. S2d, S4, S5, and the full ablations remain unexecuted.

At least three nonoverlapping time windows, two domains, and one post-cutoff or private corpus are design minima, not a claim of adequate power. A final locked corpus remains untouched by design or tuning. Titles and authors require anonymized memory-diagnostic arms, exact/normalized string and semantic memory audits, strict point-in-time features, and ex-ante labels independent of later outcomes. Domain-specific attendance instruments, thresholds, validation sets, assessor blinding, and sensitivity versions must be registered before outcome unblinding.

The inferential unit is the independent corpus or month, not agent-day. Simulation-based power must address between-corpus/month variance, within-cluster correlation, missingness, and the primary endpoint. All numerators, denominators, valid abstentions, unknown outcomes, conflicts, upstream omissions, resource totals, and aggregation rules must be released, including per-run and per-successfully-consumed-target efficiency outcomes.

A time-stamped public registry entry must precede unlocking the final corpus; an internally frozen document is not public preregistration. The complete protocol is `docs/MINIMAL_VALID_EXPERIMENT_v1.11.md`. No human RCT is a precondition for the present conditional-design/audit contribution; direct human evidence becomes necessary only for human learning, welfare, or transfer claims.

## 11 Limitations and Conclusion

The SAP is closed as a conditional controlled model, not jointly solved: the monitoring counterexample shows why component guarantees need not compose, and Algorithm 1 has no global approximation claim. Update, capacity, filtering, and submodular results remain restricted to their stated models and certified domains. Weighted recall requires a declared target law and terminal consumption; a mean interval is not a pointwise guarantee.

Fourteen deterministic tests establish reference write/rollback/ranking/audit conformance, not identity authentication, malicious-host security, or meaningful human control. The hash-pinned public CSV removes the financial reproduction blocker, but historical selections remain frozen-row aggregates. Historical `picked` records measure neither delivery/opening/attendance nor efficiency. The all-existing-key zero-empty analysis is a designated retrospective selected-proxy descriptive caliber, not an intention-to-treat or actual-consumption analysis. Retrospective labels, one shared corpus, upstream conditioning, unmatched infrastructure, and negative or interval-crossing results preclude a robust-benefit narrative.

SEA's defensible contribution is an executable ownership interface and falsifiable accounting discipline: who may write and roll back the objective, which resources actions consume, what counts as a target, and where disappearance occurs before confirmed consumption. Comparative effectiveness and human consequences remain hypotheses for the preregistered matched protocol; direct baselines, independent environments, human data, third-party reproduction, and independent human mathematical sign-off remain absent.

## Data and Code Availability

The current public candidate snapshot is **`v1.11.0`**, maintained at <https://github.com/hurrywhen/sea-nuaa> and <https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa>. Entry points are `RELEASE_v1.11.md`, `docs/REPRODUCIBILITY_v1.11.md`, `sim/pilot/results/evidence_status_v1.11.json`, and the versioned artifact manifest. This is a source-and-data prerelease, not independent mathematical verification or a completed end-to-end experiment. The historical v1.7 version DOI <https://doi.org/10.5281/zenodo.23620920> and concept DOI <https://doi.org/10.5281/zenodo.23620919> do not cover v1.9, v1.10, or v1.11. No v1.11-specific DOI or public experimental preregistration is asserted without a persistent record.

The snapshot provides the S1–S4 reference and 14 tests (`sim/sea_governance/`); the worked SAP and non-composition checks (`tools/reproduce_v110_sap.py`, stable historical filename); retained mathematical regressions (`tools/reproduce_v19_math.py`); the renamed retrospective calibers, 72,000-key ledger, 17 scenarios, and prospective schema (`sim/sea_pilot/audit_v110_consumption_caliber.py`, stable script/result paths); financial, upstream, and citation-return audits (`sim/sea_pilot/`); and the unexecuted protocol, literature record, and two supplements listed in Section 8.3. Exact wrapped commands, dependencies, frozen-input hashes, and clean-snapshot checks are consolidated in `docs/REPRODUCIBILITY_v1.11.md` rather than duplicated here.

Analyses are read-only by default; writing dedicated artifacts requires `--write`, and replacement requires `--force`. The historical financial source commit is provenance only. The scripts make no LLM calls and create no human data. Bit-identical reproduction is claimed only for identified frozen inputs, and author-run clean-snapshot checks are not third-party reproduction.

## Human–AI Collaboration and Responsibility Statement

AI agents assisted with literature searching, mathematical re-derivation, code generation, numerical checks, and manuscript drafting. Model families studied in the replay are therefore both research instruments and research objects; shared prompts, infrastructure, corpora, and model biases remain conflict channels rather than independent replications.

The human authors retain responsibility for the research question, design decisions, treatment of negative results, authorship, and any submission decision. Computational tests and AI-assisted proof checks are not independent human mathematical verification. **Independent human mathematical review remains pending**, and no paper-wide Lean certification or completed independent reproduction is claimed. No AI system holds approval authority over objective writes, publication, or human-subject decisions.

## References

Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *American Economic Review, 110*(3), 629–676.

Bergman, O., & Whittaker, S. (2016). *The Science of Managing Our Digital Stuff*. MIT Press.

Berk, R. H. (1966). Limiting behavior of posterior distributions when the model is incorrect. *The Annals of Mathematical Statistics, 37*(1), 51–58. https://doi.org/10.1214/aoms/1177699597

Blackwell, D. (1953). Equivalent comparisons of experiments. *The Annals of Mathematical Statistics, 24*(2), 265–272.

Carbonell, J., & Goldstein, J. (1998). The use of MMR, diversity-based reranking for reordering documents and producing summaries. In *Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336).

Chaloner, K., & Verdinelli, I. (1995). Bayesian experimental design: A review. *Statistical Science, 10*(3), 273–304.

Charnov, E. L. (1976). Optimal foraging, the marginal value theorem. *Theoretical Population Biology, 9*(2), 129–136.

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Clopper, C. J., & Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika, 26*(4), 404–413. https://doi.org/10.1093/biomet/26.4.404

Cochran, W. G. (1954). Some methods for strengthening the common $\chi^2$ tests. *Biometrics, 10*(4), 417–451. https://doi.org/10.2307/3001616

Dang, V., & Croft, W. B. (2012). Diversity by proportionality: An election-based approach to search result diversification. In *Proceedings of the 35th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 65–74).

Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics, 7*(1), 1–26. https://doi.org/10.1214/aos/1176344552

Es, S., James, J., Espinosa Anke, L., & Schockaert, S. (2024). RAGAs: Automated evaluation of retrieval augmented generation. In *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations* (pp. 150–158). https://doi.org/10.18653/v1/2024.eacl-demo.16

Esponda, I., & Pouzo, D. (2016). Berk–Nash equilibrium: A framework for modeling agents with misspecified models. *Econometrica, 84*(3), 1093–1130.

Friedman, B., & Hendry, D. G. (2019). *Value Sensitive Design: Shaping Technology with Moral Imagination*. MIT Press.

Fudenberg, D., Romanyuk, G., & Strack, P. (2017). Active learning with a misspecified prior. *Theoretical Economics, 12*(3), 1155–1189.

Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30* (pp. 4878–4887).

Gittins, J. C. (1979). Bandit processes and dynamic allocation indices. *Journal of the Royal Statistical Society: Series B, 41*(2), 148–177.

Harper, F. M., Xu, F., Kaur, H., Condiff, K., Chang, S., & Terveen, L. G. (2015). Putting users in control of their recommendations. In *Proceedings of the 9th ACM Conference on Recommender Systems* (pp. 3–10). https://doi.org/10.1145/2792838.2800179

Hirsch, T., Merced, K., Narayanan, S., Imel, Z. E., & Atkins, D. C. (2017). Designing contestability: Interaction design, machine learning, and mental health. In *Proceedings of the 2017 Conference on Designing Interactive Systems* (pp. 95–99). https://doi.org/10.1145/3064663.3064703

Jugovac, M., & Jannach, D. (2017). Interacting with recommenders—Overview and research directions. *ACM Transactions on Interactive Intelligent Systems, 7*(3), Article 10, 1–46. https://doi.org/10.1145/3001837

Karush, W. (1939). *Minima of Functions of Several Variables with Inequalities as Side Conditions* [Master's thesis, University of Chicago]. Reprinted in *Traces and Emergence of Nonlinear Programming* (2014, pp. 217–245). https://doi.org/10.1007/978-3-0348-0439-4_10

Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research, 9*, 235–284.

Kuhn, H. W., & Tucker, A. W. (1951). Nonlinear programming. In *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability* (pp. 481–492). University of California Press. https://doi.org/10.1525/9780520411586-036

Leskovec, J., Krause, A., Guestrin, C., Faloutsos, C., VanBriesen, J., & Glance, N. (2007). Cost-effective outbreak detection in networks. In *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 420–429).

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. In *Advances in Neural Information Processing Systems 33* (pp. 9459–9474). https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

Lin, H., & Bilmes, J. (2011). A class of submodular functions for document summarization. In *Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies* (pp. 510–520). https://aclanthology.org/P11-1052/

Lin, X., Deldjoo, Y., Dai, S., Bao, H., Ye, X., Nazary, F., Wang, W., Di Noia, T., Xu, J., & Chua, T.-S. (2026). Autonomous information seeking: A roadmap for agentic recommender systems. *arXiv:2607.04433v1*. https://doi.org/10.48550/arXiv.2607.04433

Lindley, D. V. (1956). On a measure of the information provided by an experiment. *The Annals of Mathematical Statistics, 27*(4), 986–1005.

Maćkowiak, B., Matějka, F., & Wiederholt, M. (2023). Rational inattention: A review. *Journal of Economic Literature, 61*(1), 226–273.

Mantel, N., & Haenszel, W. (1959). Statistical aspects of the analysis of data from retrospective studies of disease. *Journal of the National Cancer Institute, 22*(4), 719–748. https://doi.org/10.1093/jnci/22.4.719

Matějka, F., & McKay, A. (2015). Rational inattention to discrete choices: A new foundation for the multinomial logit model. *American Economic Review, 105*(1), 272–298.

McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika, 12*(2), 153–157. https://doi.org/10.1007/BF02295996

Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming, 14*, 265–274.

Papadimitriou, C. H., & Tsitsiklis, J. N. (1999). The complexity of optimal queueing network control. *Mathematics of Operations Research, 24*(2), 293–305.

Peng, Q., Liu, H., Huang, H., Yang, J., Yang, Q., & Shao, M. (2025). A survey on LLM-powered agents for recommender systems. In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 11574–11583). https://doi.org/10.18653/v1/2025.findings-emnlp.620

Pielot, M., Church, K., & de Oliveira, R. (2014). An in-situ study of mobile phone notifications. In *Proceedings of the 16th International Conference on Human-Computer Interaction with Mobile Devices & Services* (pp. 43–52).

Pirolli, P., & Card, S. K. (1999). Information foraging. *Psychological Review, 106*(4), 643–675.

Resnick, S. I. (1987). *Extreme Values, Regular Variation, and Point Processes*. Springer.

Saad-Falcon, J., Khattab, O., Potts, C., & Zaharia, M. (2024). ARES: An automated evaluation framework for retrieval-augmented generation systems. In *Proceedings of NAACL-HLT 2024 (Volume 1: Long Papers)* (pp. 338–354). https://doi.org/10.18653/v1/2024.naacl-long.20

Santoni de Sio, F., & van den Hoven, J. (2018). Meaningful human control over autonomous systems: A philosophical account. *Frontiers in Robotics and AI, 5*, Article 15. https://doi.org/10.3389/frobt.2018.00015

Santos, R. L. T., Macdonald, C., & Ounis, I. (2010). Exploiting query reformulations for web search result diversification. In *Proceedings of the 19th International Conference on World Wide Web* (pp. 881–890). https://doi.org/10.1145/1772690.1772780

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

**Table 10. Stable notation and scope.**

| Symbol | Meaning | Quantifier or scope |
|---|---|---|
| $x_t,y_t,a_t,h_t$ | Full controlled state, observation, attempted action, observable history | Latent components of $x_t$ are not policy inputs |
| $\vartheta_t,\mathcal V_t,L_t$ | Objective store, rollback versions, audit ledger | Writes and rollback pass through $\mathcal G$ |
| $B^T,B^{cmp},B^{call},B^{\$},B^{risk}$ | Time, computation, call, money, and risk budgets | Resource feasibility is componentwise; all uses are logged |
| $T,N,\underline\tau$ | Cognitive budget, candidate count, minimum item cost | Per declared period |
| $h_t,\mathcal A_t(h_t)$ | Observable history and feasible actions | Proposition 3.1; latent states are not policy inputs and reduced state is not assumed Markov |
| $\mu,\widehat\mu$ | Prior and one actual update kernel | The same kernel for every observed signal |
| $c,\hat c$ | True and assumed reliability | Reliability-mixture specialization only |
| $\mathcal W,\mathrm{VOI}$ | Expected realized value and correctly specified information value | Distinct unless the whole model is correct |
| $F_0,F_1,Q_1$ | Noncritical/critical score laws and CDF quantile | $Q_1(1-R)$ captures upper-tail recall $R$ |
| $M,K,m,d'$ | Finite pool, critical count, selection size, Gaussian separation | Finite top-$m$ is not a population threshold |
| $Z_i(e),C_S(e)$ | Source coverage and union coverage | No delivery implied |
| $D_S(e),\delta_e(S)$ | Actual monitored consumption and conversion given coverage | Includes linkage, selection, delivery, opening, and attendance |
| $\kappa_e(S),m_e(S)$ | Union-coverage probability and actual miss probability | $m_e=1-\kappa_e\delta_e$ |
| $w_e,\nu_e$ | Target weights and normalized target measure | $\nu_e=w_e/\sum_jw_j$ |
| $\mathcal M_\nu,\mathcal R_\nu$ | Weighted expected omission and weighted mean recall | Not a pointwise infimum |
| $q_e,R_{\mathrm{II}}(e)$ | Channel-I failure and conditional Channel-II recovery | Recovery uses failure weighting |
| $A_i,L_i,Q_i,\Delta_i,O_i,\Gamma_i$ | Availability, linkage, selection, delivery, opening, attendance | $D_i=A_iL_iQ_i\Delta_iO_i\Gamma_i$ locally in Section 6.4 |
| $V_u,\nu$ | Concave value of time use and budget shadow price | KKT corner conditions required |
| $I_K(Q)$ | Conditional mutual information $I(\omega;Y_Q\mid K)$ | Submodular under joint conditional independence |
| $p_\lambda(A)$ | Distribution over $m$-subsets | Inclusion requires summing over subsets |

A probability statement about a fixed proposition must state whether it is conditional on that proposition, drawn from a superpopulation, or evaluated on one deterministic frozen corpus. A binary coverage matrix from one corpus supplies realized indicators, not repeated proposition-conditional Bernoulli experiments. A mean over propositions answers a different question from a lower bound over all propositions.

## Appendix B Regression Checks and Falsification Map

### B.1 Numerical identities

The retained mathematical script verifies the filtering ratio 0.998875, $d'=4.389337888$, AUC 0.999044514, population recalls 0.209639680 and 0.523766570, exact normalized expected leaked values 20.799886% and 6.919112%, their same-ratio approximations 20.629947% and 6.871634%, the weighted omission counterexample 0.410 versus 0.250, and the binary update values $W=-0.24$ and $\mathrm{VOI}=0.24$. Finite-top-$m$ quadrature is checked for convergence and against 20,000 Monte Carlo realizations per separation. The new SAP script separately verifies selected/delivered/opened/consumed recalls 3/6, 2/6, 2/6, and 1/6, total omission 5/6 = 1/6 + 4/6, and the non-composition values 17, 22, and 0.75. The former RCT arithmetic remains only in the supplement. These are numerical checks of mathematical objects, not empirical validation.

### B.2 Falsification and audit map

**Table 11. Implementation and assumption falsification map.**

| Formal object | Observation that would falsify its implementation or assumptions | Required report |
|---|---|---|
| SAP composition | Component approximation described as joint optimality | Full tuple, component restrictions, and the 17/22 counterexample |
| S1–S4 governance | Unauthorized write changes the objective or version history; rollback changes ranking; platform variable changes fixed-supply rank; edit escapes hash verification | 14 synthetic tests, retained anchor, fixed-supply and supply-ecology records |
| Unified update model | Different update kernels selected using an unobserved branch label; wrong-prior nonnegative claim | Full joint model, prior, update kernel, and evaluation distribution |
| Population threshold model | Confusion of population threshold with finite top-$m$ order statistic; wrong quantile direction | Class-conditional laws, $\beta,\pi,R$, and boundary cases |
| Pareto approximation | Approximate expression written as an identity or compared using a different $m/K$ | Exact Gamma sum and same-ratio approximation |
| Weighted omission | Pooled class coverage inserted into a product; upstream/delivery losses omitted | $\nu$, per-target stages, $\kappa_e,\delta_e$, and actual consumption |
| CP mean bound | Mean interval described as an infimum interval; clustered targets treated as independent | Sampling design, cluster unit, one-sided CP definition, and target measure |
| Submodular guarantee | Ratio assigned to a nonmonotone full pool or unaugmented density greedy | Ground-set certificate and exact algorithm variant |
| EIG submodularity | Only pairwise independence given $\omega$ asserted | Joint conditional independence given $(\omega,K)$ |
| Subset-choice limit | Single-item logit used as an inclusion law | Subset action space, reference distribution, and capacity |
| Retrospective selected-proxy descriptive caliber | Empty rows dropped without label; no-row keys silently zero-filled; selected called consumed or the caliber given an intention-to-treat label | 72,000-key ledger, 71,970 existing keys, 30 missing, per-metric denominators and missingness reasons |
| Financial public reproduction | Historical audit requests a Git object absent from the public snapshot | Hash-pinned 1,260-row CSV, no-Git execution, expanded versus historical reconstruction status |
| Empirical structure effect | Fixed digest, unmatched model/input/budget, or retrospective proxy used as deployment evidence | Raw-stream S2d primary comparison and independent temporal corpora |

### B.3 Deleted or demoted claims

No global SAP optimality, universal five-dimensional value summary, universal dual-channel necessity, non-oracle attainability of $\mathcal D^*$, ratio-of-realizations interpretation of normalized leaked value, measured $k_{\mathrm{eff}}$, CP-certified pointwise $p_{\min}$, degenerate-case tightness for arbitrary effective subset sizes, single-alternative logit inclusion probability, double-threshold cooling-queue theorem, mutual-information definition of non-capture, selected-equals-consumed identity, historical efficiency measurement, or human-virtue convergence result is asserted. These deletions are substantive scope corrections, not limitations that can be reversed by adding a disclaimer to older formulas.

---

*(End of manuscript)*


