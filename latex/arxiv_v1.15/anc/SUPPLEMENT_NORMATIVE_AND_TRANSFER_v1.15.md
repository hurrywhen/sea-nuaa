# Supplement: Normative Extensions and AI-to-Human Transfer Boundaries (v1.15)

Sections are numbered N1–N5 to avoid collision with the governance conformance properties S1–S4 of the main text.

**References:** all citations use the unified reference list in the v1.15 main manuscript.

**Status:** historical design and AI-task material moved out of the v1.15 main line. This supplement contains no participant data, no new model calls, and no evidence of human welfare or transfer. It does not strengthen the main paper's empirical identification.

## N1 Measurement is not control validation

A three-dimensional state such as calibration, openness, and intellectual humility is a modeling choice, not an identified latent state from ten weekly prediction questions. Brier scores reflect reliability, resolution, and uncertainty, and their proper-scoring property is conditional on the participant's complete incentives. Bounded observations on $[0,1]^3$ also do not justify a homoskedastic Gaussian error model by default. A human measurement program needs validated instruments, test–retest reliability, longitudinal measurement-invariance checks, and a latent-variable model justified by sample size. No convergence theorem for human “virtue dynamics” is claimed.

The same limitation applies to LLM cohorts. Replaying a human paradigm can test an AI mechanism, but it does not establish human transfer. Model-specific Brier or persuasion results cannot identify human learning, welfare, or deskilling without a predeclared, passed transfer gate and ultimately direct human evidence.

## N2 Emergency authorization is a finite design table

An emergency override can be restricted to a nonempty finite whitelist $\mathcal A_{\mathrm{safe}}$, a finite uncertainty set $\Omega$, and a declared loss table $L(a,\omega)$. The standard minimax-regret action is

$$a^*\in\arg\min_{a\in\mathcal A_{\mathrm{safe}}}\max_{\omega\in\Omega}\left[L(a,\omega)-\min_{a'\in\mathcal A_{\mathrm{safe}}}L(a',\omega)\right].$$

Finite enumeration makes the value computable ex ante; this is Savage's standard criterion, not a new regret theorem (Savage, 1951). A valid implementation also needs explicit triggers, evidence authentication, a time-feasibility check, rollback, logging, and post hoc review. If those inputs are absent, the override is disabled rather than initialized with unvalidated defaults. No dominance claim over every alternative policy follows without specifying the loss model and audit costs.

## N3 Agenda overlap is not common knowledge

For consumption sets $C_i,C_j$, define the Jaccard agenda overlap $J(C_i,C_j)=|C_i\cap C_j|/|C_i\cup C_j|$. Suppose every member of a group actually consumes the same public set $S$, $|S|=s=\gamma m$, and each has a private part of size $d=(1-\gamma)m$ disjoint from $S$. Then, for every pair,

$$J(C_i,C_j)\ge\frac{s}{s+2d}=\frac{\gamma}{2-\gamma}.$$

The proof is only set accounting: the intersection contains at least $S$ and the union has size at most $s+2d$. The quantity is an **agenda-overlap index**, not a fragmentation index whose direction would be ambiguous. It does not require or establish truth, attention beyond actual consumption, or common knowledge.

Common knowledge of an announcement requires a self-evident public event: every member receives, attends to, and understands the same authenticated announcement, and the public character of that receipt is itself commonly observable. Private delivery receipts and ordinary audit logs do not satisfy this condition merely because everyone knows the mechanism. Even a genuine public announcement establishes common knowledge of membership in the announced set, not common knowledge that the proposition is true or important. Whether any real protocol achieves those strong conditions is an empirical question left open.

## N4 H8/H9: a failed or unadjudicated gate blocks human extrapolation

The transfer rule is family-, version-, and task-specific. Every required paradigm, direction, effect interval, sample minimum, and failure action must be fixed before a family is used for human-side conclusions. Any failed or unadjudicated component restricts that family to AI-mechanism description.

The existing H8 results do not pass such a gate: opposing-exposure directions reverse across families; accuracy-prompt effects are negative across the three named families, but one is near zero and outside the target effect interval; and one discrimination estimate exceeds the stated reference interval. All H8 outcomes are AI-task descriptions only, and the discrimination materials are not thereby certified as memory-free. Data completion for named tags is not the same as transfer validation.

H9 also cannot certify the gate as archived. On the agent's 40-question task, O/C/Q/G Brier scores are 0.17046/0.23206/0.23306/0.28480, with constant baseline 0.219375. O passes both the implemented Manifold-mean $\pm2\times$ rule and the separate 0.15–0.21 superforecaster reference interval; G falls in the report's distinct 0.24–0.30 layperson interval; C/Q lie between those literature intervals, and C/Q/G are worse than the agent task's constant baseline. The Manifold anchor has Brier 0.11169 on different questions and base rates and uses community terminal prices. These references are not one “human band,” do not implement the preregistered human-quantile criterion, and do not test monotone correctability on the incompletely archived per-question answers.

Accordingly, **no existing family is certified for human transfer**, even though O passes two descriptive numerical criteria. All replay findings are AI-task mechanism descriptions only.

## N5 Orientation-only human sample-size arithmetic

The former future human protocol used a longitudinal power model. For orientation only, the normal approximation at $d=0.35$, two-sided $\alpha=0.05$, and 80% power gives 128.145 analyzable participants per arm; 25% attrition gives 171 randomized participants per arm, or 513 across three arms. Two co-primary Bonferroni comparisons give approximately 207 per arm (621 total). Ceilings are applied independently to the unrounded $n$ and $n/(1-\text{attrition})$, not sequentially to an already rounded analyzable count. These are design calculations, not human data or a substitute for variance estimates from a feasibility study. No human RCT is a precondition for the present conditional-design/audit contribution; it would be necessary only for future human-effectiveness claims.
