# Sovereign Epistemic Acquisition: A Conditional Framework for Active Information Acquisition and Sovereign Filtering under Bounded Agency, with Preliminary Validation

<!-- 英文主稿（master）。中文版《主权认知获取_统一理论_v1.3.md》自此版本起降级为本稿的译文/内部审阅版。
     翻译基准：docs/中英术语对照表.md；★冻结术语不得更改。
     状态标记约定：<!-- TR-DONE --> 已译审 / <!-- TR-DRAFT --> 初译待审 / <!-- TR-PENDING --> 待译。
     <!-- RW-DONE §N --> 投稿级改写完成（RW-DONE = submission-grade rewrite complete）。
     内容纪律与中文版相同：无内部版本谱系、无路径引用、无日期戳；三态证据标注保留。 -->

**Wen Hu**<sup>1,2</sup> 　**Xutong Wang**<sup>1</sup> 　**Ya Yu**<sup>1</sup>

<sup>1</sup> College of Electronic and Information Engineering, Nanjing University of Aeronautics and Astronautics, Nanjing, China
<sup>2</sup> Jiangsu Yunhefeng Intelligent Technology Co., Ltd., Jiangsu, China

Corresponding author: Wen Hu (huwen@nuaa.edu.cn)

October 2026 · Human–AI collaboration (AI contributions disclosed in the *Human–AI Collaboration and AI Contribution Statement*)

---

## Abstract

In an era in which the marginal cost of producing information approaches zero, the question facing a bounded agent is no longer *whether* to filter but the existential constraint of *how, amid the flood, to acquire—actively and with maximal efficiency—the information that serves its own ends*: with a daily cognitive budget $T$ against a candidate supply $N \sim 10^4$, the filtering ratio must exceed 99.8%—an arithmetic fact, not a design choice. The filtering infrastructure that exists today optimizes platform engagement rather than the agent's own ends, and thus amounts to a systemic abdication of epistemic sovereignty; at the same time, active acquisition (search, monitoring, source exploration) and passive filtering (push-stream selection) have been studied in isolation, with no unified formal theory connecting them. This paper proposes **Sovereign Epistemic Acquisition (SEA)**, which recasts information acquisition as a **unified optimization problem—the Sovereign Acquisition Problem (SAP)—under the agent's second-order objective and within its cognitive budget**, in which ownership of the filter/acquirer, of its objective function, and of its audit trail rests with the agent itself. Main results: (i) a hypothesis system (Section 3: six premises classified as empirical hypotheses, normative hypotheses, and design positions, each annotated for testability) together with, under explicit decision-relevance, branch-mixture, timing, and decision-homogeneity assumptions (V1)–(V4), a per-decision structural decomposition of an item's expected realized decision value, under which a five-dimensional feature vector (relevance, novelty, durability, actionability, credibility) is an exact summary—outside (V4) the decomposition still stands, but the features serve only as an engineering heuristic summary (a closed form obtains under Gaussian–quadratic decision problems); (ii) a **score-separability bottleneck theorem**: an exact recall–budget–separation identity proving that pure scoring cannot sustain 95% recall at extreme filtering ratios unless $d' \ge 4.4$ (AUC $\approx 0.999$), so that recall guarantees must be architectural rather than score-based—the argumentative hinge of the paper; (iii) redundancy-coverage theorems: structural upper bounds $P(\mathrm{miss}) \le (1-p_{\min})^{k_{\mathrm{eff}}}$ on the miss probability of critical propositions, together with tightness results, whose strength depends conditionally on the institutional source of the coverage floor $p_{\min}$ (statutory disclosure > media redundancy > watchlist design), mapped empirically through real-corpus temporal replays in two domains; (iv) an attention no-arbitrage perspective (a direct application of the KKT conditions of concave programming): the marginal value theorem, Pandora's stopping rule, and consumption thresholds emerge as special cases of a single variational principle, organizing budget allocation across push, pull, and reflection into an online-estimable control problem; and (v) a unified adversarial model of goal capture, a convergence theorem for human-gated two-time-scale virtue dynamics, regret bounds for pre-authorized emergency action, and a fragmentation lower bound for public agenda layers. **Positioning**: this is a framework/synthesis paper. Each theorem is a correct application of standard tools (signal detection theory, submodular optimization, stochastic approximation, Hoeffding, KKT) under explicitly stated structure; the contribution lies in the system integration, in the formalization of the sovereignty conditions S1–S4, and in the argument that recall is a structural property—not in new mathematics. All theorems carry complete proofs or reductions to standard lemmas in the appendix; all assumptions are explicitly numbered and accompanied by their empirical content; Section 13 compresses the entire edifice into twelve falsifiable predictions.

**Honest statement of evidence status.** Validation follows a three-tier architecture: LLM-agent cohorts serve as the primary testbed (synthetic ecologies and real-corpus temporal replays), online public human data serve as transfer anchors, and a human RCT protocol is fully archived but deferred. **All human-side conclusions (virtue convergence, backfire protection, calibration improvement, deskilling protection) are falsifiable predictions, not established results; the population-level main validation (the full P1–P12 battery) is still in progress, and the pre-registered sample sizes have not been reached.** What has been completed is the two-domain pilots and the four-family LLM-agent replay main validation (academic domain; 80 independent runs; 73,547 valid agent-days: judgment-arm critical recall 0.443–0.534, every family ≥1.8× the honest feature arm; cross-family CMH $p\approx1.9\times10^{-215}$); and we report the negative results first: the strong form of high recall is rejected by real data in the academic domain (best recall 0.28), which yields precise boundary conditions; the financial domain attains within-portfolio recall 0.952 under highly favorable conditions (25 direct-pass holdings, 4.6 propositions/day, quota-feasible, post-hoc ground-truth proxy), diluted to 0.910 after news-layer expansion—a recall of *post-hoc* market-moving days, not of *ex-ante* critical information, with limited construct validity; public-layer certification initially fails in the real news ecology (lift 0.63×) and is only partially repaired to 1.23× (still weak enrichment), with adversarial robustness remaining an open problem. LLM agents can validate the carrier-neutral mechanisms and their AI instantiation, but not the human-side parameters (H8/H9 already exhibit systematic cross-family divergence).

**Keywords**: epistemic sovereignty; active information acquisition; information filtering; value of information; adversarial robustness; common knowledge

---

## Human–AI Collaboration and AI Contribution Statement

This paper was produced through human–AI collaboration. The division of labor is isomorphic to the sovereignty conditions (S1–S4) advocated herein: **the write right, approval right, and final-review right reside with the human authors**; AI participated deeply throughout but held no decision authority. We disclose the division of labor honestly:

**Contributions of AI (large-language-model agents)**: literature survey and the genealogy synthesis of Section 2; drafting of the premise formulations and theorem statements; proof-construction assistance and formal checking; all simulation and experimental code; experiment execution and statistical analysis (including mechanized verification of the pre-registered decision rules); result reporting and drafting of the manuscript; and pre-submission consistency-audit scripts.

**Contributions of the human authors**: posing the research question and setting the framework direction ("to acquire, most actively and efficiently, the information that benefits oneself amid the information flood"); approval of the key design decisions (the framework naming, the three-tier validation architecture, the use of LLM-agent cohorts as the primary experimental subjects, and the deferral of the human RCT); **approval of the pre-registered decision rules and of the disposition of all negative results** (the rejection of the strong form of high recall in the academic domain, the freezing of the cross-family inconsistency effect, the domain-conditional negative conclusion, and the empirically motivated qualification triggered by the public-layer certification reversal—all reviewed by the human authors and archived as-is); and final review of the full text, with authorship responsibility.

**Statement of responsibility**: although all proofs were constructed with AI assistance, **the human authors bear ultimate responsibility for the correctness of every theorem statement and proof**; the proofs of the core theorems (5.1, 6.1, 7.1–7.2, 8.1, 10.1, 11.1, 12.1) and all explicit numerical values have been independently re-checked line by line by the human authors. Reproduction code, audit scripts, and experimental records are released with the paper (see *Data and Code Availability*).

**Special disclosure (dual role)**: the experiments of Sections 14–15 include several LLM model families as subjects—these families are simultaneously **research instruments** of this paper (collaborative writing and coding) and **research objects** (subjects of the agent-cohort experiments). This dual role is inherent to the methodology (the model-organism strategy, §15.1) and is hereby declared.

**Author contributions (CRediT, brief)**: Wen Hu—conceptualization, supervision, funding acquisition, writing (review & editing); Xutong Wang—methodology, software, validation, writing (original draft, AI-assisted); Ya Yu—investigation, data curation, visualization, writing (review & editing). AI-tool contributions are disclosed as above and carry no authorship (per ICMJE criteria: AI cannot assume authorship responsibility).

---

## Contents

- **Part I Foundations**
  - 1 Introduction
  - 2 Related Work: Consensus and Controversy across Seven Disciplinary Blocks
- **Part II Premises and Formal Framework**
  - 3 Working Hypotheses and Design Principles
  - 4 The Information Environment and the Agent Model
  - 5 The Sovereign Acquisition Problem (SAP) and the Value-of-Information Decomposition Theorem
- **Part III Core Theorems**
  - 6 An Efficiency Theory of Passive Filtering (Push)
  - 7 Redundant-Coverage Theorems: Structural Conditions and the Applicability Domain of Recall under Aggressive Filtering
  - 8 A Theory of Active Acquisition (Pull) and the Attention No-Arbitrage Theorem
  - 9 Adversarial Robustness: A Unified Model of Goal Capture
  - 10 Sublimation: Human-Gated Two-Time-Scale Control
  - 11 Emergency Override: Pre-Authorization and Minimax Regret
  - 12 The Public Agenda Layer: Governing the Externalities of Universal Personalization
- **Part IV Validation and Governance**
  - 13 Catalogue of Falsifiable Predictions
  - 14 Simulation and LLM-Agent Experiments
  - 15 Empirical Validation: A Three-Tier Architecture Led by LLM-Agent Cohorts
  - 16 Governance and Ethics
  - 17 Limitations and Open Problems
  - 18 Research Roadmap and Conclusion
- Data and Code Availability
- References
- Appendix A Notation
- Appendix B Technical Lemmas

---

# Part I Foundations

<!-- RW-DONE §1 -->

## 1 Introduction

### 1.1 The Problem: The Arithmetic of the Gap

Let $T$ denote the number of minutes an agent can devote each day to consuming information. At a Chinese deep-reading speed of 250–350 characters per minute, $T=45$ yields a daily cognitive throughput of roughly 10,000–16,000 characters—about 8–12 substantive items. The daily candidate supply $N$ of a typical information environment, by contrast, is on the order of $10^4$ once subscription feeds, social streams, notifications, and search results are summed. **The filtering ratio must therefore be at least 99.8%—and this is not a design choice; it is arithmetic** (Proposition 6.1 formalizes this as an insurmountable capacity lower bound).

The question, therefore, has never been "whether to filter," but four progressively deeper questions:

1. **For whom does the filter work?** (The sovereignty question: who owns the objective function, and who holds the right to write into it)
2. **On what grounds is filtering safe?** (Provably aggressive filtering: discarding 99% without collapsing critical recall)
3. **Beyond filtering, what else should be actively acquired?** (The acquisition question: how the candidate pool itself is actively restructured by the subject)
4. **Where do filtering and acquisition ultimately lead?** (Regression or sublimation)

### 1.2 Problem Statement of This Paper

This paper establishes a rigorous theoretical foundation for the following goal:

> **Amid the flood of information, acquire information that benefits oneself with maximal efficiency and initiative.**

Read word by word, this sentence encodes four theoretical commitments, which together form the skeleton of the paper:

- **"Amid the flood of information"** — excess supply is structural and is intensified by generative AI (Premise 2): the marginal cost of content production tends to zero, the signal-to-noise ratio collapses, and manipulation is no longer constrained by production costs. The dominant form of manipulation has escalated from "making people believe lies" (indoctrination) to "making people stop believing anything" (inundation), and the latter dissolves the very capacity for judgment (Paul & Matthews, 2016).
- **"With maximal efficiency"** — efficiency must be measurable and provable: the value of information per unit of cognitive time (VOI per minute) is maximized, and the probability of missing critical information admits a provable upper bound (the family of theorems in Sections 6–8).
- **"With initiative"** — the agent's information diet is not exogenously given: it chooses which sources to subscribe to, what to retrieve, what to monitor, when to explore new sources, and when to abandon an information patch. Active acquisition (pull) and passive filtering (push) consume the same scarce resource and serve the same second-order objective; they are therefore **two families of operators within one and the same optimization problem** (Sections 5 and 8). This is the core theoretical construction of this paper.
- **"Benefits oneself"** — who gets to define "benefit" is the dividing line of the entire design. Our position: it is defined by the subject's second-order will $g^{(2)}$ (the goals endorsed by the reflective layer), not by first-order impulses $g^{(1)}$ (the preferences operative at the moment of clicking), and not by platform revenue (Premise 3; sovereignty conditions S1–S4).

### 1.3 From Passive Filtering to Active Acquisition: The Necessity of a Unified Framework

A pure theory of filtering answers "how to filter safely what arrives," but treats the composition of the candidate pool itself as exogenous input. This is a genuine theoretical gap, in three respects.

**First, the quality of the candidate pool sets the ceiling on filtering.** If the portfolio of sources to which the subject subscribes already omits an entire class of critical propositions, no filter can ever recall them—the miss occurs upstream of filtering. The selection of the source portfolio (the allocation of monitoring slots), the exploration of source quality (subscription trial and error), and on-demand retrieval (targeted queries) are all **acquisition decisions that precede filtering**, and they draw on the same budget as filtering.

**Second, the marginal values of push and pull must be priced jointly.** Should one spend ten more minutes searching a specific question, or ten more minutes consuming the push stream? The intuitive answer—"whichever is worth more"—requires a theorem. The **attention no-arbitrage theorem** of this paper (Theorem 8.1) proves that, under concavity assumptions, the marginal VOI per minute is equal across all uses at the optimal allocation, and that this common value is precisely the shadow price of the budget; the marginal value theorem of information foraging (Charnov, 1976), the stopping rule of Pandora's box (Weitzman, 1979), and the KKT conditions are all instances of it. Once unified in this way, "proactivity" ceases to be an attitude and becomes a control problem with an optimality characterization.

**Third, adversarial and sovereignty constraints act on both sides at once.** Prompt injection can be hidden inside retrieved web pages (the pull-side attack surface); emotional hijacking can arrive through the push stream (the push-side attack surface); and the write right over the objective function (S2) constrains filtering weights as well as retrieval rankings and monitoring lists. A fragmented theory cannot deliver unified protection.

The existing literature already offers scattered but mature tools for the pull side—the economics of search (Stigler, 1961), search with inspection costs (Weitzman, 1979), optimal foraging (Charnov, 1976), information foraging (Pirolli & Card, 1999), rational inattention (Sims, 2003), Bayesian experimental design (Lindley, 1956; Chaloner & Verdinelli, 1995), active learning (Settles, 2009), and multi-armed and restless bandits (Gittins, 1979; Whittle, 1988)—yet these tools have never been integrated with misinformation defense, epistemic sovereignty, and virtue dynamics. This paper carries out that integration (Section 2.7 traces the lineage; Section 8 presents the unified theory).

### 1.4 Structural Gaps in Existing Approaches

Three major technical and academic approaches each exhibit structural gaps:

- **Recommender-systems research** optimizes engagement—an objective function systematically misaligned with the subject's welfare—and, moreover, covers only the push side: even users' active retrieval is folded back into engagement signals. The interdisciplinary synthesis on "encoding human values in recommender systems" (Stray et al., 2022) and the analysis of "the difficulty of identifying engagement optimization when user preferences are inconsistent" (Kleinberg, Mullainathan & Raghavan, 2024) independently arrived at the same problem from the computer-science side, but neither addresses the ownership and write-right structure of the filter.
- **Misinformation science** has produced fragmented interventions (inoculation, correction, lateral reading, accuracy prompts) whose effect sizes are mostly small to moderate and whose findings remain mutually isolated (van der Linden, 2022; Pennycook & Rand, 2022); the field lacks system-level integration and, still more, a formal theory of *ex ante* architectural defense.
- **Human–AI collaboration research** has studied levels of automation and trust calibration, but lacks the "sovereignty" dimension: it does not answer who owns the filter's objective function or who writes into it. It likewise lacks a convergence theory that brings human virtue states into the control loop.

### 1.5 Core Thesis and Contributions

**The core thesis of this paper, in one sentence**: to reconstruct information acquisition from "platforms optimizing user attention for their own objective function" into "agents jointly optimizing active acquisition and passive filtering, under a unified budget, for their own second-order objective function," and to endow this reconstruction with provable guarantees of efficiency, safety, autonomy, and adversarial robustness.

The specific contributions (C1–C9; theorem numbers are given in the respective chapters):

- **C1 (Assumptions and design principles)**: six premises (classified into empirical assumptions / normative assumptions / design stances), with an explicit derivation of the invariants I1–I5; and a unified optimization formulation of the Sovereign Acquisition Problem (SAP) (Sections 3–5);
- **C2 (Structural decomposition of VOI)**: the decision-theoretic foundations of the scoring feature vector—a decision-by-decision structural decomposition in the Blackwell framework, an exact sufficient summary under the decision-homogeneity condition (V4), and a Gaussian closed form (Theorem 5.1, Corollary 5.1);
- **C3 (Theory of filtering efficiency)**: distortion lower bounds, the score-separability bottleneck theorem, submodularity with $(1-1/e)$ greedy guarantees, and threshold-type optimal policies (Section 6)—in which the bottleneck theorem proves that the dual-channel architecture of "proposition collapse + source redundancy + direct pass-through" is not an engineering ornament but a mathematical necessity for high recall;
- **C4 (Rigorous version of the redundancy-coverage theorem)**: the complete proof, independent-subset bounds for the correlated case together with their tightness, and the submodular dual of monitoring-slot allocation (Section 7);
- **C5 (Theory of active acquisition)**: the attention no-arbitrage theorem, the Pandora criterion for monitoring admission, the marginal-value dwelling rule, and the submodularity of query batches (Section 8);
- **C6 (Unified model of goal capture)**: a complete symmetry between human and AI defenses, expectation and high-probability firewall bounds, the critical adoption rate $\sigma^*$ in the producer game, and replicator extinction (Section 9);
- **C7 (Cybernetics of sublimation)**: the almost-sure convergence theorem for human-gated two-time-scale control, steady-state neighborhood bounds, anti-Goodhart clauses, and the necessity of class-C judgment load (Section 10);
- **C8 (Emergency override and the public agenda)**: a formalization of pre-authorization with regret bounds, conditions under which delegation strictly dominates, public-knowledge generation, and the fragmentation lower bound theorem (Sections 11–12);
- **C9 (Validation program)**: 12 falsifiable propositions, an upgraded simulation design (including the pull side and ablations), and a **three-tier validation architecture centered on LLM-agent cohorts** (agent hypotheses H1'–H7', online human-data anchors H8–H9, and a postponed human RCT; Sections 13–15).

### 1.6 Positioning of the Paper and Reading Guide

This is a theory paper: every theorem either comes with a complete proof or is reduced to standard lemmas and classical theorems in Appendix B (with sources explicitly cited), and all assumptions are explicitly numbered (Premises 1–6; redundancy assumptions R1–R3; firewall assumptions F1–F3; convergence assumptions C1–C5), each accompanied by a discussion of its empirical content and testability. Idealizations are not hidden: **every idealized assumption is accompanied by a three-part package—"direction of real-world deviation + engineering mitigation + simulation test"** (compiled in Section 17).

**An honest convention regarding the labeling of results**: this paper distinguishes two tiers of claims. **Theorems/propositions (proved)** provide complete mathematical derivations; **propositions (argued)** provide conceptual arguments or order-of-magnitude estimates rather than line-by-line derivations (e.g., the invariant derivation of Proposition 3.1, Proposition 10.2(iii), and the arms-race passage in §9.4), and each is explicitly flagged in the text. Readers who accept only the first tier may treat the second tier wholesale as design motivation without affecting the theorem chain.

Part III (Sections 6–12) is the theoretical core, and its chapters are relatively self-contained: readers interested only in why aggressive filtering is safe may proceed directly to Sections 6–7; those interested only in how active acquisition can be optimal may go directly to Section 8; those concerned with adversarial security should read Section 9. Section 13 compresses all the theorems into a single table of falsifiable propositions—the shortest entry point for experimentalists. Sections 14–15 constitute the empirical part (simulations and LLM-agent experiments) and can be read independently of the theory; detailed experimental records and code appear in the Supplementary Material (see *Data and Code Availability*).

**Figure 1. Overview of the SEA framework** (the dependency structure: premises → mechanisms → theorems → validation):

```{=latex}
\begin{figure}[h]
\centering
\begin{tikzpicture}[
  font=\small,
  box/.style={draw, rounded corners, align=center, minimum height=0.9cm, inner sep=4pt},
  env/.style={box, fill=gray!12},
  core/.style={box, fill=blue!8},
  rbox/.style={box, fill=orange!14},
  arr/.style={-{Stealth[length=2mm]}, thick},
  node distance=0.55cm and 0.7cm]
\node[env] (env) {information environment\\ excess supply (Premise 2) $\cdot$ adversarial (Premise 5)};
\node[core, below left=0.9cm and 1.9cm of env] (push) {push filtering\\ proposition collapse (Definition 4.2)\\ dual-channel selection (\S6.5)};
\node[core, below right=0.9cm and 1.9cm of env] (pull) {pull acquisition\\ exploration/query/dwelling\\ (Definition 8.1)};
\node[core, below=1.6cm of env] (nu) {unified budget $T$ $\cdot$ shadow price $\nu$ (Theorem 8.1)};
\node[box, below=0.75cm of nu] (agent) {agent $\mathcal{A}=(C,G,K,\theta,R)$\\ knowledge $K$ $\cdot$ virtue $\theta$ (\S10)};
\node[rbox, above=0.55cm of env] (R) {reflective layer $R$: write right S2 $\cdot$ audit S4 (Definition 5.3)};
\node[box, left=0.8cm of push] (fw) {firewall\\ (\S9, F1--F3)};
\node[box, right=0.8cm of pull] (mon) {monitoring list\\ redundancy coverage (\S7)};
\node[box, below=0.6cm of agent] (val) {validation: falsifiable checklist P1--P12 (\S13)\\ L1 agent cohorts $\cdot$ L2 human anchors $\cdot$ L3 RCT (\S15)};
\draw[arr] (env) -- (push);
\draw[arr] (env) -- (pull);
\draw[arr] (push) -- (nu);
\draw[arr] (pull) -- (nu);
\draw[arr] (nu) -- (agent);
\draw[arr] (fw) -- (push);
\draw[arr] (mon) -- (pull);
\draw[arr, dashed] (R) -- (push);
\draw[arr, dashed] (R) -- (pull);
\draw[arr, dashed] (R) -- (agent);
\draw[arr] (agent) -- (val);
\draw[arr, bend right=18, dashed] (agent.west) to node[left, align=center, font=\scriptsize]{feedback: audits,\\ list revisions,\\ $g^{(2)}$ revisions} (fw.south west);
\end{tikzpicture}
\caption{The overall SEA framework: content from the information environment enters unified budget allocation (shadow price $\nu$) via the two operator families of push filtering and pull acquisition; the reflective layer $R$ constrains all writes and audits through S1--S4; the validation layer maps all theorems onto falsifiable propositions.}
\end{figure}
```

---

<!-- RW-DONE §2 -->

## 2 Related Work: Consensus and Controversy across Seven Disciplinary Blocks

This section reviews the theoretical foundations along the seven layers of the problem, marking for each layer the **consensus** (which may serve as an engineering premise) and the **controversy** (which must be treated as a design variable).

### 2.1 Formalizing Scarcity and Value

- **Economics of attention** (Simon, 1971): a wealth of information creates a poverty of attention. Consensus: the bottleneck lies on the attention side.
- **Bounded rationality and satisficing** (Simon, 1955): under computational constraints, agents seek the "good enough" rather than the optimal. The greedy approximation guarantee of this framework (Theorem 6.3) is a normative counterpart of satisficing.
- **Rational inattention** (Sims, 2003; Maćkowiak, Matějka & Wiederholt, 2023): agents optimally allocate attention subject to channel-capacity constraints; the discrete-choice case yields softmax-form choice probabilities (Matějka & McKay, 2015), and further analysis of endogenous consideration sets appears in Caplin, Dean & Leahy (2019). Strengths: a mature formalization. Weakness: the objective function is assumed to be known and stable—yet the objective is precisely what the environment reshapes, and this literature does not address adversarial content. Section 8.6 of this paper connects rational inattention to the SAP as a special case.
- **Value-of-information theory** (Howard, 1966; Blackwell, 1953; Lindley, 1956): the value of information equals the expected improvement in decisions, and the informativeness ordering of experiments ($\succeq_B$, Appendix B.5(ii)) is characterized by Blackwell's theorem. This literature supports the decomposition in our Theorem 5.1; its weakness is its inability to directly price "being informed in general"—this paper supplies the long-term term through virtue dynamics (Section 10).
- **Information foraging theory** (Pirolli & Card, 1999): agents follow information scent, and the decision to stay or to leave obeys the marginal value theorem. The theory explains the addictiveness of algorithmic feeds, but it is descriptive rather than normative; Section 8.3 of this paper elevates it into a normative scheduling rule.
- **The empirical economics of digital addiction and self-control** (Allcott et al., 2020; Allcott, Gentzkow & Song, 2022): social-media abstinence experiments provide causal evidence of a systematic divergence between first-order preferences and self-reported welfare—users retrospectively judge their own consumption to have been excessive. This is one of the strongest empirical anchors for Premise 3 (the separation of $g^{(1)}$ from $g^{(2)}$), and it directly supports the framing of the question "who owns the objective function."

### 2.2 Hard Constraints on Cognitive Processing

Working-memory limits (Miller, 1956; Cowan, 2001—roughly 4 concurrent units); the selectivity and capacity of attention (Broadbent, 1958); cognitive load theory (Sweller, 1988); dual-system theory (Kahneman, 2011); the illusory truth effect, whereby repeated exposure by itself increases perceived truth (Fazio et al., 2015); and the forgetting curve (Ebbinghaus, 1885). Together, these results constrain the form of the delivery layer—layered summaries, deduplication, fewer but deeper items—and support the quantification of Premise 1 (boundedness).

### 2.3 Filter Bubbles and Polarization Mechanisms

**Consensus**: the evidence on echo chambers—self-organized homogeneous networks of users—is robust: selective exposure and homophily are human defaults (Festinger, 1957; McPherson, Smith-Lovin & Cook, 2001; Stroud, 2011). The evidence on **filter bubbles** (enclosure caused by algorithms alone, Pariser, 2011) is limited and contested: incidental exposure remains widespread, and the effect of algorithms alone on polarization is modest (Gentzkow & Shapiro, 2011; Guess et al., 2023). **Epicenter of the controversy**: Bail et al. (2018) found that random exposure to opposing views instead intensified polarization—uncurated "bubble bursting" backfires. Nguyen's (2020) conceptual distinction is crucial for this framework: epistemic bubbles (a deficit of exposure) are not echo chambers (a systematic dismantling of trust in outsiders); the latter is the real problem, and the remedy should therefore shift from "hearing more dissent" to "choosing and auditing trust anchors." This paper implements that shift as curriculum-based exposure under a tolerance-radius constraint (Definition 10.2), rather than random injection.

### 2.4 Manipulation and Immunity (Misinformation Science)

**Consensus**: (a) corrections are on average effective but incomplete, with a continued-influence effect (Lewandowsky et al., 2012; Chan et al., 2017; Ecker et al., 2022), and they may fail for identity-sensitive scientific topics (Chan & Albarracín, 2023)—**architectural implication: ex ante filtering as primary, ex post correction as auxiliary**; (b) lateral reading is the individually deployable skill with the strongest empirical support (Wineburg & McGrew, 2019), and this paper formalizes it as a pull-side query strategy (Section 8.5); (c) emotional and moralized content spreads faster and farther, and its spread is driven by humans (Vosoughi, Roy & Aral, 2018); (d) identity-protective cognition makes more cognitively capable individuals more polarized on identity-laden issues (Kahan, 2017)—being "smart" is not immunity, so protection must be externalized; (e) truth-default theory holds that humans default to belief and that doubt requires cognitive effort (Levine, 2014)—the psychological basis on which the goal-capture attack surface exists.

**Controversy**: inoculation/prebunking effect sizes are small to moderate and decay over time, with ongoing debate over publication bias (McGuire, 1964; Roozenbeek & van der Linden, 2019; van der Linden, 2022); the durability of accuracy prompts is in doubt (Pennycook & Rand, 2019, 2022); and the actual magnitude of harm from misinformation remains disputed at the level of measurement (Guess, Nagler & Tucker, 2019; Grinberg et al., 2019; Allen et al., 2020; Lazer et al., 2018). The architectural stance of this paper does not depend on the effect size of any single intervention: **the firewall bounds (Theorems 9.1–9.2) take "measured detector recall × bounded per-item impact × exposure cap" as design parameters**, thereby converting the effect-size controversy into a parameter-calibration problem.

### 2.5 The Cognitive Engineering of Human–AI Collaboration

The extended-mind thesis (Clark & Chalmers, 1998) provides philosophical legitimacy for human–AI collaboration. Cognitive-offloading research warns of deskilling risk (Sparrow, Liu & Wegner, 2011); our Proposition 10.2 proves the precise location of this risk within the framework: offloading the judgment-formation process degrades the calibration measurement channel. Automation bias (Parasuraman & Riley, 1997) and algorithm aversion/appreciation (Dietvorst, Simmons & Massey, 2015; Logg, Minson & Moore, 2019) constrain the design of trust calibration. Goodhart's law (Goodhart, 1984) and value capture (Nguyen, 2019) warn of the necessity of metric governance; this paper provides constructive protection in the form of gradient-isolation clauses (Proposition 10.1). Moral crumple zones (Elish, 2019) warn that human decision must not degenerate into ritual; this paper implements that requirement through the class-B authenticity three-condition test (Section 11.1).

### 2.6 Political Economy and Governance

The history of the attention merchants (Wu, 2016), the critique of surveillance capitalism (Zuboff, 2019), and the claim of a right to attention (Williams, 2018) correctly identify the incentive-structure nature of the problem, but their critique outruns their construction. The structural transformation of the public sphere (Habermas, 1962/1989) and republican concerns (Sunstein, 2017) point to the public costs of universal personalization. At the algorithmic level, important empirical and theoretical work already characterizes these costs: causal measurement of the effect of feed algorithms on exposure diversity (Bakshy, Messing & Adamic, 2015); normative design frameworks for exposure diversity (Helberger, Karppinen & D'Acunto, 2018); normative analysis of "bubble-bursting" interventions (Bozdag & van den Hoven, 2015); and **algorithmic monoculture** (Kleinberg & Raghavan, 2021)—when most decision-makers rely on the same algorithm, individual rationality aggregates into systemic homogenization. The fragmentation lower bound theorem of Section 12 and the algorithmic-monoculture literature are two faces of the same problem: the former provides a constructive guarantee of a "minimal area of shared reality," while the latter diagnoses the failure mode that arises in the absence of shared structure. Finally, the epistemology of testimony (Coady, 1992; Zagzebski, 2012) supplies the philosophical foundation: the vast majority of knowledge comes from the testimony of others, and trust mediation cannot be eliminated—only chosen and audited. This is the source of Premise 4.

### 2.7 The Theoretical Lineage of Active Information Acquisition

The classical tools on the pull side are scattered across six traditions; Section 8 of this paper brings them into a single framework:

- **Economics of search** (Stigler, 1961): search is costly, and the optimal search depth is determined by the condition marginal benefit = marginal cost.
- **Search with inspection costs / Pandora's box** (Weitzman, 1979): each "box" (candidate source) is costly to open and yields a random payoff; the optimal policy opens boxes in descending order of the reservation index $z_i$ (defined by $E[(X_i - z_i)^+] = c_i$) and stops when the best opened value exceeds the remaining indices. This is the exact model of source exploration and monitoring admission (Proposition 8.1). Modern extensions of the Pandora model—whether opening the box is itself optional (Doval, 2018), and more general stopping rules (Olszewski & Weber, 2015)—share the same structure as the problem treated in Section 8 of this paper.
- **Optimal dynamic information acquisition**: Zhong (2022) provides an optimality characterization of the general sequential information-acquisition problem (a dynamic version of value-of-information indexation) that overlaps almost completely with the subject of Section 8. What distinguishes this paper is the multi-use joint pricing of the budget (push, pull, and reflection sharing a single shadow price) together with the sovereignty constraints—not acquisition techniques per se.
- **Optimal foraging theory** (Charnov, 1976): patch residence time is governed by the marginal value theorem—leave when the instantaneous intake rate falls to the environmental average (the shadow price). The dwelling and rotation of information patches thereby acquire normative form (Proposition 8.2); the continual scheduling of multiple sources is a restless bandit problem (Gittins, 1979; Whittle, 1988; Weber & Weiss, 1990).
- **Bayesian experimental design and active learning** (Lindley, 1956; Chaloner & Verdinelli, 1995; Settles, 2009): the value of a query equals the expected information gain (EIG); under conditionally independent observations, EIG is monotone and submodular in the query set (Krause, Singh & Guestrin, 2008), and greedy selection achieves the $(1-1/e)$ guarantee (Theorem 8.2).
- **Optimal stopping** (Ferguson, 2006): when to stop retrieving and switch to consumption is a stopping problem under a budget constraint; this paper provides its static characterization via the attention no-arbitrage theorem (Theorem 8.1).

**Consensus**: each of these tools is mature, and they are mutually compatible (all are centered on the identity "marginal value = shadow price"). **Gap**: no tradition simultaneously handles (a) adversarial content, (b) second-order objectives, (c) joint budget allocation with push filtering, and (d) long-term virtue dynamics. The SAP (Definition 5.1) fills precisely this quadruple gap.

### 2.8 Cross-Disciplinary Points of Convergence

The seven disciplines converge on five points, which together form the premise basis and design principles of this framework:

1. **Ex ante filtering as primary** (correction effects are limited and lagged);
2. **Trust must be chosen and audited** (testimonial mediation cannot be eliminated);
3. **Heterogeneous exposure requires curation, not randomization** (the backfire evidence);
4. **Humans must retain a genuine judgment load** (the deskilling and moral-crumple-zone evidence);
5. **Acquisition and filtering are two faces of the same budget-allocation problem, and marginal values must equalize** (the common core of the search, foraging, and rational-inattention traditions—Theorem 8.1 of this paper elevates it into an organizing principle of the framework).

**Distinction from the closest work (an explicit demarcation of the new contributions)**. (a) **Zhong (2022)** provides an optimality characterization of general sequential information acquisition and is the theoretical upstream of our pull side; our differences: the push-filtering channel, the adversarial branch (negative value under misspecified updating), and the sovereignty constraints lie outside that framework, and our SAP incorporates them into a single budget. (b) **Weitzman (1979) / Charnov (1976)** provide the classical rules for exploration admission and patch leaving; this paper does not re-prove them, but proves that they are common special cases of the attention no-arbitrage condition, and supplies the push-side consumption threshold (Proposition 6.4) and source scheduling (§8.6) as the remaining instances of the same shadow price. (c) **KKT / submodular greedy / Hoeffding / Robbins–Siegmund** are standard tools; our relevant theorems (8.1, 6.3, 9.1–9.2, 10.1) are correct applications of these tools to the structures we posit—**what is new is the structure and the formulation of the problem** (the sovereignty conditions, the dual-channel division of labor, human gating), not the tools themselves. (d) **Adversarial machine learning** (Dalvi et al., 2004; Lowd & Meek, 2005; Biggio & Roli, 2018) addresses classifier-level adversaries; our goal-capture model (Definition 9.1) raises the attack target from classification decisions to the objective function itself, and write isolation (S2) is a structure absent from that literature (see §9.1 for details). (e) **Bounded-confidence opinion dynamics** (Hegselmann & Krause, 2002; Deffuant et al., 2000) provides a ready-made dynamical reference frame for the tolerance-radius curriculum (Definition 10.2): this paper upgrades the descriptive radius into an endogenous curriculum that grows with capability. (f) **Value learning** (Hadfield-Menell et al., 2016, 2017) addresses alignment under unknown objectives; our $g^{(2)}$ declaration plus human gating is an institutional compromise on the same problem (the guidance note in §5.3). (g) **LLM sycophancy** (Sharma et al., 2023) is the most empirically measured carrier of goal capture on the AI side and is directly isomorphic to Definition 9.1.

---

# Part II Premises and Formal Framework

<!-- RW-DONE §3 -->

## 3 Working Hypotheses and Design Principles

### 3.1 Six Premises: Empirical Assumptions, Normative Assumptions, and Design Stances

This framework rests on six premises. **To forestall any misleading connotation of the word "premise," we state explicitly at the outset**: these are not mathematical premises—claims that could enter derivations as unexamined givens—but claims of three distinct epistemic statuses: **empirical assumptions** (measurable and falsifiable: Premises 1, 2, 4), **normative assumptions** (philosophical positions and value stipulations: Premise 3), and **design stances** (engineering and governance commitments: Premises 5, 6). Each premise is labeled with its category and its **testability**, and each explicitly shoulders the corresponding empirical risk or argumentative burden. The theorems below depend only on the empirical assumptions; the normative assumptions and design stances determine how the problem is formulated and how the institution is designed, and they never enter the logical premise chain of any proof (wherever they do enter, this is declared through separately and explicitly numbered conditional assumptions R/F/C/P, etc.).

**Premise 1 (Boundedness)**. [Empirical assumption] The information-processing capacity of every agent is bounded: there exist a per-period cognitive budget $T < \infty$ (time and attention) and a working-memory constraint $W$ (for humans, $W \approx 4$ concurrent units, Cowan, 2001; for AI agents, the context window and inference budget). Quantitative basis: Section 2.2.

**Premise 2 (Excess Supply)**. [Empirical assumption (including an order-of-magnitude extrapolation)] The candidate-supply rate $\lambda$ (items/day) of the information environment and the per-item consumption cost $\bar t$ satisfy $\lambda \bar t \gg T$, and under the generative-AI regime the growth of $\lambda$ is no longer constrained by production costs. Current order of magnitude: $\lambda \bar t / T \approx 10^3$ (recomputed from the typical parameters of §1.1—$T=45$, $\bar t\approx4$, $N\sim10^4$—as $8.9\times10^2$). Testability: supply volume and costs are directly measurable, and that "production cost tends to zero" is an industrial fact. **Corollary**: a filtering ratio of $1 - T/(\lambda \bar t) \ge 99.8\%$ is an arithmetic necessity (Proposition 6.1).

**Premise 3 (Goal Stratification)**. [Normative assumption (philosophical foundation: Frankfurt, 1971)] The agent's goal structure $G = (g^{(1)}, g^{(2)})$ is stratified: $g^{(1)}$ comprises first-order preferences (the impulse at the moment of clicking, the immediate pull of high-arousal content), whereas $g^{(2)}$ is the second-order will—the goals, endorsed by the reflective layer $R$, concerning "what one wishes to be shaped by." The two can diverge systematically; **normatively, $g^{(2)}$ holds authority over the shaping of the information environment**. Empirical support: the planner–doer structure of self-control (Thaler & Shefrin, 1981), intertemporal inconsistency (Ainslie, 1992), and the endogenous shaping of preferences (Elster, 1983).

**Premise 4 (Testimonial Dependence)**. [Empirical assumption (epistemological foundation: Coady, 1992; Zagzebski, 2012)] The overwhelming majority of an agent's beliefs about the world are acquired through the testimony of others; trust mediation cannot be eliminated—it can only be **chosen** (through the source portfolio) and **audited** (through provenance and calibration). Corollary: the provenance structure (Definition 4.2) is not optional metadata but a load-bearing wall of belief formation.

**Premise 5 (Adversariality)**. [Design stance (worst-case assumption)] The information environment contains actors whose payoffs depend on rewriting the goals or beliefs within the agent's processing loop, and whose strategies adapt to defenses (an arms race). This is formalized in Definition 9.1 (the goal-capture attack). Human instances: emotional hijacking and the propaganda "firehose of falsehood" (Paul & Matthews, 2016); AI instances: prompt injection, especially indirect prompt injection delivered through retrieved content (Greshake et al., 2023; Liu et al., 2024). **A filtering theory that does not posit this premise does not hold in open environments.**

**Premise 6 (Measurability & Correctability)**. [Design stance] Filter performance (recall, precision, manipulation exposure) and the agent's cognitive state $\theta$ can be measured, albeit noisily, and correction channels (parameter rollback, source replacement, goal revision) are always open. This is the governance-theoretic converse of Goodhart's law: a filter that cannot be measured cannot be governed.

### 3.2 The Invariants and Their Derivation

**Proposition 3.1 (Invariants I1–I5; argued derivation)**. *Under Premises 1–6, any sovereign epistemic acquisition system must satisfy the following invariants.* (This proposition belongs to the "Proposition (argued)" tier: I1 admits a rigorous derivation; I2–I5 are conceptual derivations from premises to design requirements, whose function is to make the operational implications of the premises explicit rather than to serve as mathematical theorems.)

- **I1 (Capacity constraint)**: $C \ll |X|$; filtering and prioritization are unavoidable; the only open question is who owns the acquisition–filtering mechanism and what objective function it serves.
- **I2 (Sovereignty)**: the write right over the objective function $g^{(2)}$ and the filter parameters $w$ resides with the subject's reflective layer $R$ (or its legitimate delegate).
- **I3 (Provenance)**: every accepted proposition carries verifiable provenance. Human instances: primary sources (papers, financial reports, court judgments, raw data); machine instances: cryptographically signed origins and content credentials (C2PA, 2021).
- **I4 (Adversarial robustness)**: there exists a bound $\varepsilon$ such that, after the processing of any adversarial content sequence, the effective-goal divergence satisfies $D(\tilde U, G) \le \varepsilon$ (Section 9 gives the exact metric $D$ and the construction of the bound).
- **I5 (Calibration)**: filter performance is measurable and auditable, and the correction channel is open.

**Proof.**

*I1*: By Premise 1, the consumption budget $T$ is finite; by Premise 2, $\lambda \bar t > T$. Hence any policy consumes at most $m \le T/\bar t < \lambda$ items per day, and the discarded fraction is $\ge 1 - T/(\lambda\bar t) > 0$ and approaches 1. Filtering—in the broad sense of selective admission into the candidate pool—occurs under every policy, so the only remaining question is "by whom, and according to what objective." $\blacksquare$

*I2*: By Premise 3, $g^{(1)}$ and $g^{(2)}$ are separable, with normative authority residing in $g^{(2)}$. The filter's objective function determines which content enters the agent's belief-formation loop, and thereby **shapes the future $g^{(1)}$ and even $g^{(2)}$ itself** (preference endogeneity, Elster, 1983). If the write right does not belong to $R$, the mechanism amounts to a third party's enforced execution upon the subject's goal structure; by the procedural definition of autonomy (the Frankfurt hierarchy condition plus the procedural-independence condition), this is not the subject's autonomous acquisition but heteronomous shaping. Sovereignty therefore requires that the write right $\in R$. $\blacksquare$

*I3*: By Premise 4, beliefs are mediated by testimony, and the reliability of that mediation cannot be assumed a priori (Premise 5: there exist adversaries who forge the mediation). Verifiable provenance is the only way to convert "trust" from an unauditable psychological state into an auditable structural property: without provenance there is no object to audit, and I5 fails; and if provenance can be forged without cryptographic or institutional anchoring, then the adversary of Premise 5 can inject false testimony. I3 is thus a conjunctive corollary of I5 together with Premises 4–5. $\blacksquare$

*I4*: Premise 5 asserts that adversaries exist and adapt. If the goal divergence were unbounded, the system's effective objective function could be rewritten by content, and I2 would exist in name only—the write right would be stolen through the content channel, bypassing the authorized path. I4 is therefore the preservation condition for I2 in adversarial environments; the construction of $\varepsilon$ is given in Theorems 9.1–9.2. $\blacksquare$

*I5*: Given directly by Premise 6. Note the logical hierarchy: Premise 6 is itself a design stance rather than an empirical fact, so I5 is a **design requirement** ("the system ought to be built this way"), not an empirical invariant; its empirical component ("whether measurement is feasible") is borne by the measurement model of Section 10.1 and by the measurements of Sections 14–15. A supplementary argument: if performance were not measurable, then (a) the correction channel could never be triggered, (b) Goodhart drift could never be detected, and (c) the audit right (S4) of I2 would spin idle. $\blacksquare$

### 3.3 The Human–AI Symmetry Table

The invariants and all subsequent mechanisms instantiate symmetrically across the two classes of agents; this is the operational meaning of the claim that "the methodology applies to every bounded agent":

| Structure | Human instantiation | AI-agent instantiation |
|---|---|---|
| Capacity constraint (Premise 1) | working memory, time budget | context window, inference budget |
| Goal stratification (Premise 3) | impulses vs. reflectively endorsed goals | immediate instruction-following vs. the principal's authorized configuration |
| Adversarial capture (Premise 5) | emotional hijacking (System 1 arousal hijacking the weights) | prompt injection (instructions rewritten by content) |
| Provenance (I3) | primary-source verification | signed origins, content credentials |
| Reflective layer $R$ | the person themself | the legitimate authorization configuration of the principal |
| Virtue state $\theta$ | calibration, openness, humility | calibration, robustness (no humility dimension; replaced by an overconfidence penalty term) |
| pull operator | active retrieval, subscription trial and error | tool calls, sub-queries, retrieval augmentation |
| push operator | feed filtering | admission control over the input queue |

<!-- RW-DONE §4 -->

## 4 The Information Environment and the Agent Model

This section fixes all of the mathematical objects. The measure-theoretic setup is minimal but rigorous: all random elements are defined on a common filtered probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}_{t\ge0}, P)$, and "a.s." always means $P$-almost surely.

### 4.1 Information Items and the Arrival Process

**Definition 4.1 (Information item)**. The information flow $X = \{x_1, x_2, \dots\}$ is a marked point process over arrival times $\{t_i^{arr}\}$ (for the push stream we take compound Poisson arrivals at rate $\lambda$; for modeling extensions, see the simulations in Section 14). Each item
$$x_i = (\mathrm{content}_i,\ \mathrm{prov}_i,\ \tau_i),$$
where $\mathrm{prov}_i$ is the provenance information (source identity, signatures/credentials, the chain of paraphrase) and $\tau_i > 0$ is the consumption-time cost. Each item carries latent attributes (unobservable, or only noisily observable, to the filter):

- $v_i^* \in \mathbb{R}_{\ge 0}$: **true value**—the ground truth of the strength of association between the proposition to which the item belongs and the subject's decision set (defined precisely via the VOI decomposition of Theorem 5.1);
- $m_i \in [0,1]$: **manipulation intensity**—the strength of the goal-capture payload embedded in the content (Definition 9.1);
- $s_i \in \mathcal{S}$: **stance vector**—a position on the issue-relevant stance manifold $\mathcal{S}$.

The observable feature map is $\phi(x_i;\, K, D) \in [0,1]^5$, $\phi = (\text{relevance}, \text{novelty}, \text{durability}, \text{actionability}, \text{credibility})_i$. **A note on the type signature**: $\phi$ is a function of **item × subject state**, not of the item alone—relevance depends on the subject's declared decision set $D$, and novelty depends on the knowledge state $K$ (there is no gain on information already contained in $K$). This point is substantive: any formulation that treats $\phi$ as a pure item function $X \to [0,1]^5$ is inconsistent with the decomposition of Theorem 5.1. Theorem 5.1 gives the decision-by-decision structural decomposition of $v_i^*$ and proves that, under the additional decision-homogeneity assumption (V4), $\phi(\cdot; K, D)$ is an exact summary of $v_i^*$ (there exists an $F$ such that $v_i^* = F(\phi)$); outside (V4), $\phi$ is only an engineering heuristic summary (§5.2 gives an explicit counterexample).

**Definition 4.2 (Proposition graph and provenance tree)**. Let $E = \{e_j\}$ be the underlying set of events/propositions. Generative structure: each proposition $e_j$ derives a document set $D_j \subseteq X$, and the collapsing map $\kappa: X \to E$ sends each document to its proposition. Each proposition carries a **provenance tree** $T_j$: the root node is the primary source, with verification status $r(T_j) \in \{\mathrm{verified}, \mathrm{unverified}\}$; the branch nodes are paraphrases and commentary. **Commentary is not independent information but an annotation layer on the proposition**—its value enters as a bounded correction term to the proposition's value and does not separately consume a full share of the consumption budget.

**Definition 4.3 (Proposition-collapse ratio)**. $\rho_c := |X| / |E|$. The proposition-centric architecture makes repostings collapse automatically: $n$ media outlets reposting = 1 proposition + $n$ provenance-tree edges. Prior prediction: $\rho_c \in [5, 20]$ (tested in simulation and on real measurements, Section 13, P3). **Corollary 6.1 proves** that collapse converts the document-level filtering-ratio problem into a proposition-level selection problem, and is one of the necessary conditions for the feasibility of extreme filtering ratios.

**Definition 4.4 (Source classes)**. The universe of sources is partitioned by the triple (ownership × geography × type) into **source classes** $\mathcal{C}_1, \dots, \mathcal{C}_K$. The purpose of the partition is to approximate the conditional independence of coverage events (Assumption R2): outlets under the same ownership or upstream of the same wire service are assigned to the same class, whereby cross-class correlation is constructively suppressed. The **coverage event** of class $i$ for proposition $e$ is $Z_i(e) := \mathbb{1}\{\exists x \in D_e: \text{the source of } x \in \mathcal{C}_i\}$.

### 4.2 The Agent

**Definition 4.5 (The agent five-tuple)**.
$$\mathcal{A} = (C,\ G,\ K,\ \theta,\ R)$$

- $C = (T, W)$: cognitive capacity—the per-period budget $T$ (minutes) and the working-memory constraint $W$;
- $G = (g^{(1)}, g^{(2)})$: the goal structure (Premise 3);
- $K$: **knowledge state**—a belief measure $\mu_K \in \mathcal{P}(\Theta_{\mathrm{rel}})$ over the state space $\Theta_{\mathrm{rel}}$ relevant to the subject's decision set, together with a memory of the set of consumed propositions (used in the novelty computation: the novelty of item $i$ $= I(y_i; \omega \mid K)$, see Section 8.5);
- $\theta = (\theta_{\mathrm{cal}}, \theta_{\mathrm{open}}, \theta_{\mathrm{hum}}) \in [0,1]^3$: the cognitive-virtue state (Section 10 gives the measurement model and the dynamics);
- $R$: the reflective layer—for a human, the person themself; for an AI agent, the legitimate authorization configuration of its principal.

**Definition 4.6 (Decision set)**. $D$ is the subject's declared **active decision set** (finite): each $d \in D$ carries a decision deadline $h_d$ (horizon) and a utility function $u_d(a, \omega)$. Criticality is defined on this basis: a proposition $e$ is **critical** for the subject ($e \in E^*$) if there exists $d \in D$ such that information about $e$ has a nonzero probability of changing the optimal action of $d$, with the magnitude of the change exceeding a declared threshold. **Criticality is subject-relative**—this paper makes this explicit, and it is precisely what renders the recall target arithmetically feasible (the budget-feasibility condition of Proposition 6.3).

### 4.3 Acquisition–Filtering Policies

**Definition 4.7 (The policy five-tuple)**. A policy is $\pi = (\pi_{\mathrm{mon}}, \pi_{\mathrm{pull}}, \pi_{\mathrm{push}}, \pi_{\mathrm{del}}, \pi_{\mathrm{esc}})$:

- $\pi_{\mathrm{mon}}$: **monitoring list**—the subset of source classes admitted for direct pass-through and the watchlist of monitored entities (Assumption R3); a slow variable (updated weekly/monthly), subject to slow-timescale gating (§10.3, Assumption C5);
- $\pi_{\mathrm{pull}}$: **active-acquisition policy**—query generation, retrieval depth, source exploration, patch dwelling and rotation (Section 8);
- $\pi_{\mathrm{push}}$: **filtering policy**—the selection $A \subseteq X$ from the candidate pool (push arrivals ∪ pull returns) (Section 6);
- $\pi_{\mathrm{del}}$: **delivery policy**—layered summaries, ranking, cooling-queue scheduling; it obeys the "summary = map" principle (the class-C constraints of Section 11.1);
- $\pi_{\mathrm{esc}}$: **emergency-override policy**—conservative actions under pre-authorization instructions (Section 11).

**Budget identity**: $T = T_{\mathrm{pull}} + T_{\mathrm{push}} + T_{\mathrm{ref}}$, where $T_{\mathrm{ref}}$ is the reflection load (the weekly calibration meeting, etc.; class C, not automatable). Theorem 8.1 gives the optimality condition for this partition.

### 4.4 The Producer Ecology

**Definition 4.8 (Producer game environment)**. The population of content producers is distributed across types $q \in \{\mathrm{honest}, \mathrm{sensational}, \mathrm{manipulative}\}$, with share vector $\mathbf{x} = (x_h, x_s, x_m)$, $\sum_i x_i = 1$. Producers choose content strategies to maximize payoffs $\Pi(q)$ (Section 9.4 gives the payoff structure); shares evolve under replicator dynamics. The adoption rate $\sigma \in [0,1]$ of the filter (the fraction of sovereign-filter users in the population) is an exogenous parameter of producer payoffs; the endogenization of $\sigma$ (users adopting according to the quality of the ecology) is left as an open problem (Section 17).

---

<!-- RW-DONE §5 -->

## 5 The Sovereign Acquisition Problem (SAP) and the Value-of-Information Decomposition Theorem

### 5.1 The Sovereign Acquisition Problem

**Definition 5.1 (Sovereign Acquisition Problem, SAP)**. Given a horizon $H$ (number of periods) and a discount factor $\beta \in (0,1]$, the SAP is:

$$\max_{\pi \in \Pi_S}\ \mathbb{E}_\pi\!\left[\sum_{t=1}^{H} \beta^t \Big( \underbrace{\mathrm{VOI}_t(A_t)}_{\text{current-period information value}} + \underbrace{\zeta\, \Delta\theta_t}_{\text{virtue gain}} - \underbrace{\mathrm{Harm}_t(A_t)}_{\text{manipulation harm}} \Big)\right]$$

subject to:

- **(Budget)** in each period, $\sum_{i \in A_t} \tau_i + c(\pi_{\mathrm{pull},t}) + c_{\mathrm{ref}} \le T$, where $c(\pi_{\mathrm{pull},t})$ is the time cost of active acquisition (queries, exploration, reading retrieval results) and $c_{\mathrm{ref}}$ is the incompressible reflection load;
- **(Manipulation exposure)** $\mathbb{E}[\#\{i \in A_t: m_i > \tau_m\}] \le \varepsilon_c / (\delta(1-\rho_m))$ (obtained by inverting the bound $D \le \delta(1-\rho_m)\,\mathbb{E}[n_m] \le \varepsilon_c$ of Theorem 9.1);
- **(Tolerance band)** the stance dispersion of the exposure set satisfies $d(E_t) \le \rho(\theta_t)$ (Definition 10.2, the no-backfire constraint);
- **(Sovereignty constraints)** $\pi \in \Pi_S$: the policy space is restricted by S1–S4 (Definition 5.3)—the objective function is readable, parameter writes must be authorized by $R$, there are no third-party revenue terms, and decisions are auditable;
- **(Emergency structure)** $\pi_{\mathrm{esc}}$ is restricted to the class of pre-authorization instructions (Definition 11.2).

**Remark (dimensional consistency)**. In the objective functional, $\mathrm{VOI}_t$ and $\mathrm{Harm}_t$ are both measured in the same decision-utility unit (for the definition of $\mathrm{Harm}$ see §5.2: the expected utility loss under misspecified updating), so the two are additive; $\zeta\,\Delta\theta_t$ is a slow-timescale term, and $\zeta$ is the subject's declared "virtue–utility exchange rate" (a class-B decision)—its very existence is the operationalization of Premise 3: the subject explicitly declares the weight of long-term virtue relative to current-period information value. The shadow price $\nu$ of "VOI/minute" in Section 8 unifies the units across push, pull, and reflection precisely because the value functions of all three uses are expressed as functions of time in the same utility unit.

The SAP is a stochastic control problem: the exploration–exploitation trade-off on the pull side, online selection on the push side, and the slow-timescale $\theta$ dynamics and monitoring-list updates are all coupled together. **This paper does not solve the full SAP to global optimality** (the general case contains restless-bandit special cases that are already PSPACE-hard, Papadimitriou & Tsitsiklis, 1999; see §8.6 for the complexity discussion); instead, it adopts a strategy of "decomposition + layer-by-layer optimality guarantees": Section 6 solves the push-selection layer (submodular greedy + threshold policies), Section 7 solves the coverage guarantee of the monitoring list, Section 8 solves the pull layer and gives the no-arbitrage condition for budget allocation among the three layers (Theorem 8.1), and Sections 9–12 equip the layers with the safety, sublimation, emergency, and publicness constraints. **An honest statement**: layer-by-layer optimality does not automatically compose into global approximate optimality—the layers are coupled through the shared budget and the knowledge state, and this paper has not proved a general theorem to the effect that per-layer approximation ratios multiply or that errors propagate linearly; what this paper provides is an explicit characterization of each layer's error terms (the distortion lower bound, the coverage miss bound, the firewall bounds, the convergence-neighborhood bound) and of the channels through which they enter the SAP objective; a rigorous propagation bound for the composed error is listed as open problem O8. The simulations (Section 14) test the actual performance of the decomposition strategy on end-to-end KPIs.

**Proposition 5.1 (Existence of an optimal policy)**. *Suppose the horizon $H$ is finite, per-period rewards are bounded ($|\mathrm{VOI}_t|, |\mathrm{Harm}_t| \le \bar V < \infty$), the per-period candidate pool is finite (so that the per-period action set—the Cartesian product of the family of candidate-pool subsets with the finite combinations of pull operators—is finite), and the constraint sets (budget, exposure, tolerance band, sovereignty constraints S1–S4, emergency structure) are closed period by period. Then the SAP admits an optimal (deterministic Markov) policy, not necessarily unique.*

**Proof (finite-horizon dynamic programming)**. Under the standard hypotheses of finite per-period action sets, bounded rewards, and finite horizon, backward induction for the finite-horizon MDP applies directly: define the terminal value function $V_{H+1}(\cdot) \equiv 0$ and recurse from $t = H$ down to $t = 1$ via
$$V_t(s_t) = \max_{a_t \in \mathcal{A}_t(s_t)}\ \Big\{ r_t(s_t, a_t) + \beta\,\mathbb{E}\big[V_{t+1}(s_{t+1}) \mid s_t, a_t\big] \Big\},$$
where $s_t = (K_t, \theta_t, \text{remaining budget}, \pi_{\mathrm{mon},t})$ is a sufficient state and $\mathcal{A}_t(s_t)$ is the current feasible action set (nonempty: the null-consumption action is always feasible). Since each $\mathcal{A}_t$ is finite, the maximum is attained and an optimal action rule exists in every period; inductive concatenation then yields a globally optimal policy. The role of the sovereignty constraints S1–S4 is to shrink each period's $\mathcal{A}_t$ (removing policies with unauthorized parameter writes or third-party revenue terms); this shrinking does not alter per-period finiteness, so the existence conclusion is unaffected. The measurability technicalities on Borel state spaces (the belief $\mu_K$ is a probability measure) are handled by the measurable-selection theory of Bertsekas & Shreve (1978), whose Chapters 8–9 are precisely the tools that rigorize the DP existence argument above. $\blacksquare$

**Remark (on the choice of proof route)**. This paper does not take the route of "weak compactness of the policy space + maximizing a continuous functional": weak compactness of the space of conditional transition kernels requires the relaxed-control (Young measure) framework, and the authorization constraint of S2 confines parameters to the set approved by $R$—a set that is generally not closed and hence incompatible with compactness arguments. The DP route is both more elementary and more rigorous under this paper's own assumptions (finite horizon, per-period finite actions, bounded rewards).

### 5.2 The Feature Decomposition of Information Value

The scoring function is the core of the entire engineering design. This section provides decision-theoretic foundations for the five-dimensional feature vector: under explicit assumptions, it derives a decision-by-decision structural decomposition of an item's **expected realized decision value**, and it characterizes precisely the additional condition under which "the five-dimensional feature is a summary of it" holds ((V4), together with a counterexample showing failure). The section also honestly addresses a conceptual difficulty: within the Blackwell framework, the value of information of any experiment is nonnegative (Lemma 5.1), whereas adversarial content can obviously inflict negative value; reconciling the two requires an explicit "misspecified updating" modeling step (Definition 5.2), which constitutes the main technical content of this section.

**Setup**. State space $\Theta_{\mathrm{rel}}$ (the world states relevant to the decision set $D$); the subject's current belief $\mu_K$. The generation of an item $x_i$ is a **two-branch mixture**: with probability $c_i$ (the source's credibility) it is the true branch, in which the item provides a genuine signal $y_i$ about $\Theta_{\mathrm{rel}}$ (information structure $\sigma_i$); with probability $1 - c_i$ it is the false branch, in which the item carries a signal $\tilde y_i$ chosen by the adversary (aimed at pushing beliefs in a direction favorable to the adversary). When consuming the item, the subject **cannot observe the branch label**—this is precisely the substance of the adversarial problem.

**Lemma 5.1 (The EVPI identity and nonnegativity)**. *For any decision problem and any experiment $\sigma$, when the subject performs Bayesian updating with the correct likelihood:*
$$\mathrm{VOI}(\sigma) := \mathbb{E}_{y \sim \sigma}\Big[\max_a \mathbb{E}[u(a,\omega) \mid y]\Big] - \max_a \mathbb{E}[u(a,\omega)] \ \ge\ 0.$$

*For the proof see Appendix B.5* (a one-line corollary of Jensen's inequality; Blackwell (1953) further characterizes the informativeness ordering among experiments).

**Corollary-like observation (why the adversarial branch is not a Blackwell experiment)**. The nonnegativity of Lemma 5.1 presupposes that the subject updates with the **correct likelihood**. The harm mechanism of adversarial content lies precisely in the fact that the subject **updates with a misspecified likelihood**—treating the adversarial signal $\tilde y$ as if it were the genuine signal $y$. The "value" of the adversarial branch is therefore not the VOI of any Blackwell experiment and must be defined separately.

**Definition 5.2 (Expected realized decision value under misspecified updating)**. For a decision $d$ and a signal $z$ (with true distribution $Q_z$), suppose the subject updates the belief to the posterior $\mu_K^{\ell}(\cdot \mid z)$ according to a (possibly misspecified) likelihood $\ell$, and accordingly chooses the action $\hat a(z) = \arg\max_a \mathbb{E}_{\mu_K^{\ell}(\cdot\mid z)}[u_d(a,\omega)]$. Define the **expected realized decision value**
$$W_d(z;\ \ell) := \mathbb{E}_{z \sim Q_z}\,\mathbb{E}_{\omega \sim P(\cdot \mid z)}\big[u_d(\hat a(z), \omega)\big] - \max_a \mathbb{E}_{\mu_K}[u_d(a,\omega)],$$
where the outer expectation is taken under the **true** joint distribution. Under updating with the correct likelihood, $W_d(z;\ell_{\mathrm{true}}) = \mathrm{VOI}_d(z) \ge 0$ (Lemma 5.1); under updating with a misspecified likelihood, $W_d$ can be strictly negative (the posterior is systematically pushed away from the truth, and the action is worse than remaining at $a_0$).

**Assumptions** (the feature-decomposition assumptions (V1)–(V4)):

- **(V1) Decision relevance**: an item affects the subject's utility only through the decisions in $D$: $v_i^* = \sum_{d \in D} P(d \text{ active within the horizon and } i \text{ relevant to it}) \cdot W_i^{(d)}$, where $W_i^{(d)}$ is the item's expected realized decision value for decision $d$. Being informed in general is not priced through $D$; its value enters the slow-timescale virtue term $\zeta \Delta\theta$ (Section 10)—this honestly acknowledges that the decision-theoretic framework cannot price "cultivation"; cultivation is handled separately by the cybernetics of sublimation.
- **(V2) Branch mixture with bounded harm**: in the true branch the subject updates with the correct likelihood, and the realized value is the Blackwell value of information $W_i^{(d)}(y_i;\ell_{\mathrm{true}}) = \mathrm{VOI}_i^{(d)}(y_i) \ge 0$; in the false branch the subject updates with the misspecified likelihood "the signal is genuine," and the realized value satisfies $W_i^{(d)}(\tilde y_i;\ell_{\mathrm{mis}}) \le 0$ and is bounded below: define the **harm term** $\mathrm{Harm}_i^{(d)} := -W_i^{(d)}(\tilde y_i;\ell_{\mathrm{mis}}) \in [0, \mathrm{Harm}_{\max}]$ (the boundedness of single-item harm and the bounded-per-item-impact assumption F1 of Section 9 are two faces of the same coin).
- **(V3) Timeliness discounting**: the information value of decision $d$ is discounted by $e^{-h/\lambda_d}$ as a function of the time gap $h$ between the arrival of the information and the decision deadline ($\lambda_d$ is the decision's **durability scale**: for one-off event news $\lambda_d$ is small; for foundational knowledge $\lambda_d$ is large).
- **(V4) Decision homogeneity** (the additional assumption required for an exact summary): all decisions $d \in D$ share the same durability scale $\lambda_d = \lambda$, and the per-decision values decompose along a common profile: $\mathrm{VOI}_i^{(d)}(y_i) = a_d \cdot V_i$, $\mathrm{Harm}_i^{(d)} = a_d \cdot H_i$, where $a_d \ge 0$ is the importance weight of decision $d$ (independent of the item), and $V_i, H_i$ are the item's decision-independent value and harm baselines. The substance of (V4): decisions differ only in "weight," not in value structure.

**Theorem 5.1 (Feature decomposition of the expected realized decision value)**. *Under (V1)–(V3), the expected realized decision value of item $x_i$ for the subject decomposes as*

$$v_i^* \;=\; \sum_{d \in D} \underbrace{\pi_d(i)}_{\text{relevance} \times \text{actionability}} \cdot \Big[ c_i \cdot \underbrace{\mathrm{VOI}_i^{(d)}(y_i)}_{\text{novelty (Blackwell value of information)}} \cdot \underbrace{e^{-h_i/\lambda_d}}_{\text{durability}} \;-\; (1 - c_i)\, \mathrm{Harm}_i^{(d)} \Big]$$

*where $\pi_d(i) = P(d \text{ active and relevant} \mid i)$, $\mathrm{VOI}_i^{(d)}(y_i) \ge 0$ (Lemma 5.1) and is monotone nondecreasing in the informativeness ordering of experiments (Blackwell, 1953), and $\mathrm{Harm}_i^{(d)} \in [0, \mathrm{Harm}_{\max}]$. The above is a **decision-by-decision ($d$-dependent) structural decomposition**: it expresses $v_i^*$ as a combination of calibratable components, but the right-hand side in general **cannot** be reconstructed from any finite-dimensional scalar feature of the item (see the counterexample in the remark below). **Exact-summary conclusion**: under the additional assumption (V4), define the aggregate feature $A_i := \sum_d \pi_d(i)\,a_d$ (relevance × actionability); then*
$$v_i^* \;=\; A_i\Big[c_i\,V_i\,e^{-h_i/\lambda} - (1-c_i)\,H_i\Big] \;=:\; F\big(\phi(x_i; K, D)\big),$$
*i.e., the five-dimensional feature vector (which under (V4) degenerates to four effective aggregate quantities $A_i, V_i, h_i, c_i$, with the harm baseline $H_i$ taken as a calibrated constant or folded into the features) is an exact summary of $v_i^*$: there exists an $F$ independent of $i$ (determined by $\lambda$, $\{a_d\}$, and $H$) such that $v_i^* = F(\phi)$. Outside (V4), no such $F$ exists, and the five-dimensional feature should be regarded as an engineering heuristic summary.*

**Proof**. Step 1 (decomposition): by (V1), $v_i^* = \sum_d \pi_d(i)\,W_i^{(d)}$. Step 2 (branch mixture): the item's value is an expectation taken over the **data-generating branches**—with probability $c_i$ it falls in the true branch (value $\mathrm{VOI}_i^{(d)}(y_i)$), and with probability $1-c_i$ it falls in the false branch (value $-\mathrm{Harm}_i^{(d)}$, by (V2) and Definition 5.2). The expectation is linear in the branch indicator (this is merely taking the expectation of a discrete random variable), so
$$W_i^{(d)} = c_i\,\mathrm{VOI}_i^{(d)}(y_i) - (1-c_i)\,\mathrm{Harm}_i^{(d)}.$$
Step 3 (timeliness): by (V3), the true-branch value is multiplied by the discount $e^{-h_i/\lambda_d}$ (the harm of the false branch is realized in the period of consumption and receives no timeliness discount—this asymmetry reflects that "bad information distorts judgment immediately, whereas the value of good information depends on decision timing"). Combining the three steps yields the decomposition. Summariness: the right-hand side of the decomposition depends on $i$ only through $(\pi_d(i))_{d}$, $\mathrm{VOI}_i^{(d)}(y_i)$, $h_i/\lambda_d$, and $c_i$; $\pi_d(i)$ is "relevance × actionability"; $\mathrm{VOI}_i^{(d)}(y_i)$ is "novelty" (a monotone function of the conditional information gain given $K$—by Blackwell's theorem, the value of information is monotone in the informativeness of the experiment, and the gain is zero on information already contained in $K$, so it measures precisely the novelty relative to $K$); $h_i, \lambda_d$ are "durability"; and $c_i$ is "credibility." The exact-summary part: under (V4), substituting $\mathrm{VOI}_i^{(d)} = a_dV_i$, $\mathrm{Harm}_i^{(d)} = a_dH_i$, and $\lambda_d = \lambda$, and factoring $a_d$ out of the summand, gives $v_i^* = \big(\sum_d \pi_d(i)a_d\big)\big[c_iV_ie^{-h_i/\lambda} - (1-c_i)H_i\big]$, whose right-hand side depends on $i$ only through $(A_i, V_i, h_i, c_i)$; taking $F$ to be this expression completes the proof. (Note: without (V4) this step fails—$\sum_d \pi_d(i)\,[\,\cdot\,]_d$ is a sum of products of $d$-dependent quantities and in general is not a function of any low-dimensional aggregate.) $\blacksquare$

**Remark (the exact status of this theorem—answering two misreadings)**.

1. **Why Step 2 is not a "linear decomposition of VOI over posterior mixtures"**: if the item were modeled as a single Blackwell experiment (the posterior mixing as $\mu_{K\oplus x_i} = c_i\mu_{K\oplus y_i} + (1-c_i)\mu_{K\oplus\tilde y_i}$), then the nonlinearity of the $\max_a$ operator would make the VOI of the mixed experiment **generally unequal** to the linear mixture of the VOIs, and by Lemma 5.1 that VOI would have to be nonnegative—one would neither obtain the decomposition nor accommodate the harm term. The decomposition of this paper takes expectations not at the posterior level but at the level of the **data-generating branches**: the branch indicator is part of the real world (whether the content is or is not an adversarial payload), taking expectations over it is an ordinary application of the law of total expectation, and linearity holds trivially. The price is that $W$ (Definition 5.2) replaces VOI as the value concept—it is not the Blackwell value of any single experiment, but "the expected realized utility change of an agent acting on its own updating rule under a class of generative processes."
2. **Status in the general case**: the decomposition relies on the structure of (V1)–(V3); **the exact-summary conclusion additionally relies on (V4)**. Outside (V4) (interacting decisions, non-exponential timeliness, within-branch updating rules adaptive to content, heterogeneous value structures across decisions), the five-dimensional feature vector should be regarded as an **engineering heuristic summary** rather than a sufficient statistic for value; under the Gaussian–quadratic structure plus (V4) it is exact (Corollary 5.1). Accordingly, the decision-theoretic foundation of this paper's scoring function is a "conditional summary theorem under structural assumptions," not an unconditional identity.
3. **Counterexample (when (V4) fails, five-dimensional scalars cannot reconstruct $v_i^*$)**: let $D = \{d_1, d_2\}$, with $d_1$ a breaking decision ($\lambda_1$ small) and $d_2$ a persistent decision ($\lambda_2$ large). Item $i$ is relevant only to $d_1$, item $j$ only to $d_2$, and the two have identical five-dimensional scalar features (the same aggregate relevance, novelty, durability reading, actionability, and credibility). Then $v_i^* \propto e^{-h/\lambda_1}$ while $v_j^* \propto e^{-h/\lambda_2}$, and when $\lambda_1 \ne \lambda_2$, $v_i^* \ne v_j^*$: identical five-dimensional features correspond to different values. Hence $\sum_d \pi_d(i)\,[\,\cdot\,]_d$ is in general not a function of aggregate scalars—an "exact summary" must be premised on (V4) and cannot be quietly assumed.
4. **The status of linear scoring $\langle w, \phi\rangle$**: the engineering objective of the SAP and Definition 9.1 use linear scoring, whereas the exact $F$ under (V4) is multiplicative/bilinear ($A \cdot [cVe^{-h/\lambda} - (1-c)H]$). The two are reconciled as follows: (a) after taking logarithms, the benefit term $cVe^{-h/\lambda}$ is **additive** in $(\log c, \log V, h)$—linear scoring on log-features is exact for the pure benefit term (the logarithm is monotone, hence order-preserving); (b) the harm term $-(1-c)H$ cannot be added to the benefit term in the same log space, and this paper's treatment is **architectural separation**: the harm channel is borne by the firewall (Section 9, with hard constraints on $\rho_m, n_{\max}$) rather than by the scoring function, and scoring is responsible only for benefit-side ranking; (c) outside this structure, no approximation bound between $\langle w, \phi\rangle$ and $F$ has been proved, and linear scoring is an engineering heuristic—this paper no longer claims any unconditional decision-theoretic justification for it; its ranking quality is priced by the measured $d'$ (the usage in Theorem 6.1 is precisely "do not assume the scores are correct; price the scoring error").

**Corollary 5.1 (Gaussian–quadratic closed form)**. *If for every critical decision $d$: $\omega_d \in \mathbb{R}$, with prior $\omega_d \sim \mathcal{N}(\hat\omega, \sigma_0^2)$, signal $y_i = \omega_d + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma_i^2)$, and quadratic utility $u_d(a,\omega_d) = -(a - \omega_d)^2$, then*
$$\mathrm{VOI}_i^{(d)}(y_i) \;=\; \sigma_0^2 - \frac{\sigma_0^2 \sigma_i^2}{\sigma_0^2 + \sigma_i^2} \;=\; \frac{\sigma_0^4}{\sigma_0^2 + \sigma_i^2} \;=\; \sigma_0^2 \cdot \frac{\sigma_0^2}{\sigma_0^2 + \sigma_i^2}.$$
*That is, information value = prior variance × (the share of posterior-precision gain). The "novelty" dimension of the scoring function is, under this closed form, an estimate of the precision gain $\sigma_0^2/(\sigma_0^2+\sigma_i^2)$; "relevance" is $\pi_d(i)$; and the correction of "credibility" $c_i$ to $\sigma_i^2$ is precisely source-noise calibration.*

**Proof**. Under quadratic utility, $\max_a \mathbb{E}[u] = -\mathrm{Var}$, so $\mathrm{VOI} = \mathrm{Var}(\text{prior}) - \mathbb{E}[\mathrm{Var}(\text{posterior})] = \sigma_0^2 - \frac{\sigma_0^2\sigma_i^2}{\sigma_0^2+\sigma_i^2} = \frac{\sigma_0^4}{\sigma_0^2 + \sigma_i^2}$. Rearranging gives the result (the final expression $= \sigma_0^2 \cdot \frac{\sigma_0^2}{\sigma_0^2+\sigma_i^2}$). $\blacksquare$

**Engineering implications**. (a) On decision structures where (V4) holds, the scoring weights $w$ are not free parameters: the dimensions of $w$ are images of the decision weights $\pi_d a_d$, the durability scale $\lambda$ (the actual decay factor being $e^{-h_i/\lambda}$), and the harm bound $\mathrm{Harm}_{\max}$ in $F$—what S2 (the write right) constrains is therefore **the decision set and the utility declarations**, not arbitrary numbers; outside (V4), the calibration of $w$ can only proceed empirically (measured $d'$ and retrospective audits) and enjoys no structural derivation; (b) the correct implementation of the novelty dimension is a proxy for the conditional mutual information $I(y_i; \omega \mid K)$ (Section 8.5 gives a computable submodular version); (c) the $\mathrm{Harm}$ term correctly pushes "high-relevance items with low credibility" to negative scores—this is precisely the seam between the firewall (Section 9) and the scoring function: the firewall's detection recall $\rho_m$ lowers the arrival rate of the false branch, thereby shrinking the expected contribution of the $(1-c_i)\mathrm{Harm}$ term.

### 5.3 Sovereignty Conditions and the Reversibility Principle

**Definition 5.3 (Sovereignty conditions S1–S4)**. An acquisition–filtering system $(\pi, U)$ is **sovereign** if and only if:

- **S1 (Inspectability)**: the objective functional $U$ is represented in an interpretable form of at most $k$ terms (in this paper $k = 5$: the five dimensions of $\phi$), and the weights $w$ and $g^{(2)}$ are fully readable by the reflective layer $R$;
- **S2 (Write right)**: any modification to $w$, $g^{(2)}$, threshold parameters, or the monitoring list $\pi_{\mathrm{mon}}$ must be explicitly authorized by $R$ via $\sigma_R$; the system must not use behavioral data to implicitly rewrite the objective function (click signals may be used only for **measurement**, never for **writing**—the line separating this framework from platform recommender systems lies here);
- **S3 (Non-capturability)**: $U$ contains no term related to any third party's revenue. Idealized statement: $I(U;\ \mathrm{Rev}_{\mathrm{platform}}) = 0$ (mutual information is zero). Operationalized audit: code review + provenance logs of weights + ranking counterfactual tests (for the same content pool, verifying that the ranking does not change with platform-side variables);
- **S4 (Auditability)**: every delivery carries an explanation $e(i) =$ the top-$j$ contributing features together with their signs; all ranking and admission decisions leave tamper-proof logs.

**Definition 5.4 (Reversibility principle)**. Every parameter modification takes effect immediately, is historically traceable, and can be rolled back in one click. The system must not lock the subject in through sunk costs, migration barriers, or default inertia. Formalization: the switching-cost function on the policy-parameter space satisfies $c_{\mathrm{switch}}(\cdot,\cdot) \equiv 0$ (borne by the system, not passed on to the subject).

**Remark (the relationship between the S-conditions and the SAP)**. S1–S4 do not enter the SAP's objective functional; they shrink its policy space $\Pi_S$: sovereignty is a constraint, not a preference term. The rationale for this design: if sovereignty could be traded away for utility, then in a world where $g^{(1)}$ is shaped by the environment it inevitably would be traded away (Premise 3 + Elster's sour-grapes mechanism). The sovereignty conditions are the system-level form of a Ulysses contract (Section 11).

**Remark (the elicitation burden of $g^{(2)}$—the largest usability gap of this framework)**. The SAP and S2 require the subject to declare the decision set $D$, utilities $u_d$, horizons $h_d$, the tolerance threshold $\varepsilon_c$, and the pre-authorization quadruple $D_{\mathrm{adv}}$—**an ordinary subject cannot write down their own utility function**; this is the elicitation difficulty shared by all value-alignment research, and this paper is no exception. The literature lines most relevant to this problem: cooperative inverse reinforcement learning (CIRL: formalizing "the subject's goals are unknown and must be learned through interaction" as a two-player cooperative game, Hadfield-Menell et al., 2016) and the Off-Switch Game (correctability as an equilibrium property of a game, Hadfield-Menell et al., 2017). This paper's position is an engineering compromise rather than a solution: (a) the declaration burden is **tiered by explicitness**—the minimal viable declaration consists of only two items, the monitoring list and the weekly time budget, with all utility parameters set to conservative defaults (defaults as a governance problem of values: see §16.2); (b) $g^{(2)}$, as a slow variable, is iteratively refined through quarterly goal-revision meetings (class C, Proposition 10.2) rather than elicited once and for all—this is spiritually isomorphic to CIRL's "learning goals through interaction," but with human gating replacing automated preference inference (avoiding the consolidation of inference errors into writes); (c) measurable proxies for elicitation quality: the convergence over time of declaration-revision magnitudes (declaration stabilization) and the "declaration–behavior" gap (the deviation between the declared $E^*$ and the topics actually consumed). A complete formalization (a CIRL-ized SEA) is left to future work (see the extension of Limitation 12 in §17).

---

# Part III Core Theorems

<!-- RW-DONE §6 -->

## 6 An Efficiency Theory of Passive Filtering (Push)

This section answers the second of the four questions: "On what grounds is filtering safe?" The answer unfolds in four layers. The capacity and distortion lower bounds (6.1) quantify what aggressive filtering costs; the score-separability bottleneck theorem (6.2) shows that **a pure scoring channel cannot mathematically support high recall**, thereby proving the necessity of the dual-channel architecture (proposition collapse + source-redundancy direct pass-through + scored discovery); submodularity and greedy guarantees (6.3) yield provably near-optimal selection algorithms; threshold policies (6.4) characterize the optimal structure of the online case; and 6.5 synthesizes all of these results into the dual-channel architecture principle.

### 6.1 Capacity and Distortion Lower Bounds

**Proposition 6.1 (Arithmetic lower bound of the filtering ratio)**. *Suppose $N$ candidates arrive per period, with per-item consumption cost $\tau_i \ge \underline\tau > 0$ and budget $T$. Then any policy consumes $m \le T/\underline\tau$ items per period, and the discarded fraction is*
$$1 - \frac{m}{N} \ \ge\ 1 - \frac{T}{\underline\tau N}.$$
*Substituting typical values—$T = 45$ minutes, $\underline\tau \approx 4$ minutes/item (deep-reading one substantive item), $N = 10^4$—yields a filtering ratio $\ge 99.8\%$.*

**Proof**. Consumption is constrained by the budget: $m\underline\tau \le \sum_{i\in A}\tau_i \le T$. $\blacksquare$

**Definition 6.1 (Critical-value leakage / distortion)**. For a policy $\pi$, define the distortion
$$\mathcal{D}(\pi) := \mathbb{E}\Big[\sum_{e \in E^*} v_e \cdot \mathbb{1}\{e \text{ not consumed}\}\Big],$$
that is, the expected sum of the true values of the uncovered part of the critical-proposition set $E^*$ (Definition 4.6). This is the exact measure of "the cost of aggressive filtering."

**Proposition 6.2 (The distortion lower bound and optimal distortion)**. *Let $K^* = |E^*|$ be the number of critical propositions in the current period, with values $\{v_e\}$, and suppose the consumption budget accommodates $m$ distinct propositions. Then, for any policy,*
$$\mathcal{D}(\pi) \ \ge\ \mathcal{D}^* := \mathbb{E}\Big[\sum_{r > m} V_{(r)}\Big],$$
*where $V_{(1)} \ge V_{(2)} \ge \dots$ is the decreasing rearrangement of $\{v_e\}$. Equality holds if and only if the policy consumes exactly the top-$m$ critical propositions by value (perfect ranking, with the entire budget directed at critical propositions).*

*If, in addition, $v_e \stackrel{iid}{\sim} \mathrm{Pareto}(\alpha, v_{\min})$ ($\alpha > 1$, power-law criticality—the setting of the simulation generator), then*
$$\frac{\mathcal{D}^*}{\mathbb{E}[\sum_e v_e]} \ =\ 1 - \Big(\frac{m}{K^*}\Big)^{(\alpha-1)/\alpha}.$$

**Proof**. First claim: any policy consumes at most $m$ distinct propositions, so the leaked value = total critical value − consumed critical value $\ge$ total critical value − the $m$ largest critical values $= \sum_{r>m} V_{(r)}$; a perfectly ranking policy attains equality. Second claim: the Pareto tail is $P(V > v) = (v/v_{\min})^{-\alpha}$, with quantile function $Q(1-u) = v_{\min} u^{-1/\alpha}$. The expected total is $\mathbb{E}[\sum_e v_e] = K^* v_{\min} \alpha/(\alpha - 1)$. The expected sum of the top $m$ terms is approximated by an integral over order statistics:
$$\mathbb{E}\Big[\sum_{r \le m} V_{(r)}\Big] \approx K^* v_{\min} \int_0^{m/K^*} u^{-1/\alpha}\, du = K^* v_{\min} \frac{\alpha}{\alpha-1}\Big(\frac{m}{K^*}\Big)^{(\alpha-1)/\alpha}.$$
Subtracting and dividing by the total gives the result. $\blacksquare$

**Remark (accuracy of the approximation)**. The integral approximation above has relative error $o(1)$ as $m \to \infty$ (with $m/K^*$ bounded or tending to zero) (Resnick, 1987); for small $m$ the exact order statistics carry $\Gamma$ correction factors ($\mathbb{E}[V_{(r)}] = v_{\min}\frac{\Gamma(r-1/\alpha)\Gamma(K^*+1)}{\Gamma(r)\Gamma(K^*+1-1/\alpha)}$, which for small $r$ differ from $v_{\min}(K^*/r)^{1/\alpha}$ by a factor of order $\Gamma(1-1/\alpha)$; at $\alpha=1.5$ the first-term deviation can reach double-digit percentages). This paper's typical usage range $m/K^* \in [0.5, 0.8]$ does not lie entirely in the asymptotic regime, so the closed form should be read as a **first-order approximation**, and the numbers derived from it (such as 20.6% and 7.2% below) carry correspondingly generous tolerances; the simulation (P2) tests directly against the generator's exact order statistics.

**Numerical implications** (an honest accounting of the cost of aggressive filtering): at $\alpha = 1.5$, if the budget covers half of the critical propositions ($m/K^* = 0.5$), the critical-value leakage is $\approx 20.6\%$; at $80\%$ coverage the leakage is $\approx 7.2\%$. The conclusion: the distortion lower bound is determined by **the tail shape of the value distribution and the budget coverage rate**, and no filter can escape it; the engineering goal is to compress leakage toward acceptable levels by (a) improving ranking quality so as to approach $\mathcal{D}^*$, (b) enlarging the "effective $m$" via the monitoring list (direct-pass-through admission of critical propositions does not occupy competitive ranking), and (c) calibrating the declared scope of $E^*$ through $g^{(2)}$.

### 6.2 The Score-Separability Bottleneck Theorem

Proposition 6.2 assumed perfect ranking. This subsection proves that **when ranking is imperfect, extreme filtering ratios impose mathematically unrealistic demands on scoring quality**—the theorem-level basis for the division of labor "architecture bears recall; scoring bears discovery" (Section 6.5).

**Setup (Gaussian scoring model)**. The candidate pool contains $M$ propositions, of which a fraction $\pi$ are critical. Scores are $s = \mu_0 + \sigma Z$ (non-critical, $Z \sim \mathcal{N}(0,1)$) or $s = \mu_0 + d'\sigma + \sigma Z$ (critical). Here $d' = (\mu_1 - \mu_0)/\sigma$ is the signal-detection-theoretic separability (Green & Swets, 1966). The filter consumes the top $\beta M$ scores ($\beta = m/M$). Let $\bar\Phi$ denote the standard normal tail function; the threshold $z$ is determined by the threshold equation (Theorem 6.1).

**Theorem 6.1 (The budget–separability–recall identity and the bottleneck)**.

*(i) (The identity) The threshold $\tau$ is determined by the mixture tail equation:*
$$(1-\pi)\,\bar\Phi(z) + \pi\, \bar\Phi(z - d') = \beta, \qquad z := (\tau - \mu_0)/\sigma,$$
*and the recall is $R = \bar\Phi(z - d')$.*

*(ii) (Capacity ceiling) For any scoring quality, $R \le \min\{1,\ \beta/\pi\}$. In particular, if $\beta < \pi$, then even 100% recall is unattainable; the ceiling is $\beta/\pi$.*

*(iii) (Separability requirement) Given a target recall $R$, feasibility holds if and only if $\beta \ge \pi R$, and the required separability is*
$$d' \ \ge\ \underline{d'}(\beta, \pi, R) := \Phi^{-1}\Big(1-\frac{\beta - \pi R}{1 - \pi}\Big) + \Phi^{-1}(R),$$
*where $\Phi^{-1}$ is the quantile function of the standard normal CDF (the CDF-quantile convention is used uniformly throughout; if the tail function $\bar\Phi$ is used instead, both $\Phi^{-1}(\cdot)$ must be converted in lockstep to $\bar\Phi^{-1}(1-\cdot)$—the two must not be mixed, since mixing yields erroneous values such as $\pm1.10$).*

*(iv) (Numerics) Typical proposition-level parameters: $M \approx 800$ ($10^4$ documents ÷ $\rho_c \approx 12.5$), $m \approx 10$, $K^* \approx 8$ ($\pi = 0.01$, $\beta = 0.0125$), target $R = 0.95$: the requirement is*
$$d' \ge \Phi^{-1}\big(1-\tfrac{0.0125 - 0.0095}{0.99}\big) + \Phi^{-1}(0.95) = \Phi^{-1}(0.99697) + \Phi^{-1}(0.95) \approx 2.74 + 1.645 = 4.39,$$
*corresponding to an area under the ROC curve of $\mathrm{AUC} = \Phi(d'/\sqrt2) \approx \Phi(3.10) \approx 0.999$—near-perfect criticality discrimination.*

**Proof**.

(i) The consumption set is $\{s > \tau\}$; its share of the pool is the tail probability of the mixture distribution, which equals $\beta$ and thereby defines the threshold; recall is $R = P(s > \tau \mid \text{critical}) = \bar\Phi((\tau - \mu_1)/\sigma) = \bar\Phi(z - d')$.

(ii) The number of critical propositions consumed is $\le$ the total number consumed $\beta M$, and also $\le$ the total number of critical propositions $\pi M$; hence $R = \frac{\text{critical propositions consumed}}{\pi M} \le \frac{\beta M}{\pi M} = \beta/\pi$.

(iii) By (i), the share of critical propositions consumed is $\pi R \le \beta$ (necessity), and $(1-\pi)\,\bar\Phi(z) = \beta - \pi R$, so $z = \bar\Phi^{-1}\big(\tfrac{\beta-\pi R}{1-\pi}\big) = \Phi^{-1}\big(1-\tfrac{\beta-\pi R}{1-\pi}\big)$. Also $R = \bar\Phi(z - d')$, i.e., $z - d' = \bar\Phi^{-1}(R) = -\Phi^{-1}(R)$ (using the symmetry $\bar\Phi(-x) = \Phi(x)$). Subtracting the two equations: $d' = \Phi^{-1}\big(1-\tfrac{\beta-\pi R}{1-\pi}\big) + \Phi^{-1}(R)$. For $R = 0.95$: $\Phi^{-1}(0.95) = 1.645$, $\Phi^{-1}(0.99697) \approx 2.74$, hence $d' \ge 2.74 + 1.645 = 4.39$.

Sufficiency (monotonicity closure): write the threshold equation as the implicit function $F(z, d') := (1-\pi)\bar\Phi(z) + \pi\bar\Phi(z - d') - \beta = 0$. $F$ is strictly decreasing and continuous in $z$, so for each $d'$ there exists a unique solution $z(d')$; by the implicit function theorem,
$$\frac{dz}{dd'} = -\frac{\partial F/\partial d'}{\partial F/\partial z} = \frac{\pi\,\varphi(z-d')}{(1-\pi)\,\varphi(z) + \pi\,\varphi(z-d')} \ \in\ (0,1),$$
where $\varphi$ is the standard normal density. The attainable recall $R(d') = \bar\Phi(z(d') - d')$ then satisfies
$$\frac{dR}{dd'} = -\varphi(z-d')\Big(\frac{dz}{dd'} - 1\Big) = \varphi(z-d')\big(1 - \tfrac{dz}{dd'}\big) \ >\ 0,$$
that is, given the budget $\beta$, attainable recall is strictly increasing in $d'$. Hence, for $d' \ge \underline{d'}$, taking the threshold $\tau = \mu_0 + \sigma\, z(d')$ (consumption exactly fills the budget $\beta$) yields recall $R(d') \ge R(\underline{d'}) = R$, meeting the target. $\blacksquare$

(iv) Substitute the numbers; $\Phi^{-1}(0.99697) \approx 2.74$ (the table in Appendix B.6); $\mathrm{AUC} = P(s_{\text{critical}} > s_{\text{non-critical}}) = \bar\Phi(-d'/\sqrt{2})$, whose symmetric form is $= \Phi(d'/\sqrt2)$; $d'/\sqrt2 = 3.10$, $\Phi(3.10) \approx 0.999$. $\blacksquare$

**Remark (sensitivity and robustness—the domain of validity of the identity)**. (a) **Distribution-free part**: the capacity ceiling (ii) ($R \le \beta/\pi$) rests on no distributional assumption; it is a pure counting argument. The identity structure of (i)(iii) holds for any location–scale family (with $d'$ normalized by the common scale); the Gaussian assumption enters only the specific numbers (4.39, AUC); for heavy-tailed or skewed score distributions, the separability required by the same $\beta, \pi, R$ will differ, and one must recompute with the tail function of the measured distribution replacing $\bar\Phi$. (b) **Score correlation**: the identity (i) is a statement about marginal distributions; correlation among item scores does not affect the marginal threshold equation. Correlation does, however, affect the joint behavior of top-$m$ selection (the crowding-out problem of same-source copies, see Corollary 6.1(ii), is handled by deduplication). (c) **Parameter error**: $\underline{d'}$ is locally Lipschitz in its arguments; to first order, $\partial\underline{d'}/\partial\beta = -1/\big[(1-\pi)\,\varphi(\Phi^{-1}(1-\frac{\beta-\pi R}{1-\pi}))\big] < 0$, and estimation error in $\pi$ propagates by the chain rule—the calibration uncertainty of $\pi$ or $\beta$ should be converted into a confidence band for $\underline{d'}$ when reported. (d) **Dynamic $\beta$**: when the budget varies across periods, the identity applies pointwise; an instance of a budget shock is stress test (g) in Section 14.5.

**Three interpretive consequences of Theorem 6.1**:

1. **Document-level filtering is mathematically infeasible**: without proposition collapse, $\beta = 10/10^4 = 0.001$, $\pi = 0.01$ (critical documents include redundant repostings), and the capacity ceiling is $R \le \beta/\pi = 0.1$—**no matter how perfect the scoring, recall is at most 10%**. Collapse effectively magnifies $\beta$ by a factor of $\rho_c$ (Corollary 6.1); this is the proof of necessity of the proposition-centric architecture.
2. **A pure scoring channel cannot support 95% recall**: $d' \ge 4.39$ (AUC ≈ 0.999) means the scorer is nearly omniscient about "what is critical to the subject." Empirically, LLM scorers already exhibit measurable error rates on factual judgments (Section 16), and their judgments of "subject relevance" depend on the quality of the $g^{(2)}$ declaration; $d' \in [1.5, 2.5]$ is a more realistic range—evaluating the identity pointwise gives recall of only about $21\%$–$52\%$. **Critical recall of ≥95% cannot be achieved by scoring alone**.
3. **Recall guarantees must come from architecture**: direct pass-through of monitored source classes (the redundancy-coverage theorem of Section 7: $P(\mathrm{miss}) \le (1-p_{\min})^{k_{\mathrm{eff}}}$, independent of $d'$), direct pass-through of the watchlist (Assumption R3, constructive zeroing), and the public agenda layer (Section 12, a backstop of redundant attestation). The true responsibility of the scoring channel is **discovering critical propositions not covered by monitoring + value ranking when the budget binds**; its recall contribution is determined by $d'$ and honestly reported.

**Corollary 6.1 (The multiplier effect of proposition collapse)**. *Let $m$ = consumption slots per period, $N$ = number of documents, $M = N/\rho_c$ = number of propositions after collapse, $K^*$ = number of critical propositions, and $\bar r$ = the average number of document copies per critical proposition (number of critical documents $= K^*\bar r$). Then:*

*(i) (Recall ceiling at document granularity) When recall is measured in document units, $R_{\mathrm{doc}} \le \min\{1, \beta_d/\pi_d\} = \min\{1, m/(K^*\bar r)\}$;*

*(ii) (Attainability gain from deduplication) The counting ceiling on proposition recall is $\min\{1, m/K^*\}$ at both granularities, but **without deduplication this ceiling is unattainable**: the copy scores of the same critical proposition are highly correlated (same-source content), top-$m$ score-based selection is crowded out by duplicate copies, the expected number of distinct propositions covered is $\approx m/\bar r_{\mathrm{top}}$ (where $\bar r_{\mathrm{top}}$ is the average redundancy in the high-score segment), and attainable recall is $\approx m/(\bar r_{\mathrm{top}}K^*)$; after deduplication each slot is guaranteed to correspond to a distinct proposition, and attainable recall $= \min\{1, m/K^*\}$—collapse strictly increases attainable recall by a factor of $\bar r_{\mathrm{top}}$;*

*(iii) (Relaxation of feasibility and of the separability requirement) When $\bar r \approx \rho_c$ (critical events receive reporting redundancy in the same proportion as the average), $\pi_p = K^*/M \approx \pi_d$ and $\beta_p = m/M = \rho_c\beta_d$: the feasibility condition $\beta \ge \pi R$ of Theorem 6.1(iii) is relaxed by a factor of $\rho_c$, and the required separability $\underline{d'}(\beta,\pi,R)$ is strictly decreasing in $\beta$—collapse relaxes the capacity ceiling and the separability requirement simultaneously.*

**Proof**. (i) $m$ documents cover at most $m$ critical documents, out of $K^*\bar r$ critical documents in total; $\beta_d/\pi_d = (m/N)/(K^*\bar r/N) = m/(K^*\bar r)$. (ii) The counting ceiling is obvious ($m$ slots cover at most $m$ distinct propositions); the copy-crowding argument: if $\bar r_{\mathrm{top}}$ copies of some critical proposition enter the high-score segment, they consume $\bar r_{\mathrm{top}}$ slots while contributing the recall of only 1 proposition; deduplication (the proposition-merging map $\kappa$ of Definition 4.2) architecturally excludes this waste. (iii) $\pi_p = K^*/M = K^*\rho_c/N = \pi_d\rho_c/\bar r \approx \pi_d$ (when $\bar r \approx \rho_c$); $\beta_p = m/M = m\rho_c/N = \rho_c\beta_d$. Monotonicity of $\underline{d'}$: $\underline{d'} = \bar\Phi^{-1}\big(\tfrac{\beta-\pi R}{1-\pi}\big) + \Phi^{-1}(R)$, $\bar\Phi^{-1}$ is strictly decreasing, and increasing $\beta$ $\Rightarrow$ increases its argument $\Rightarrow$ decreases $\underline{d'}$. $\blacksquare$

**Proposition 6.3 (Budget feasibility of the recall target)**. *A necessary condition for the declared recall target $R$ to be attainable over $E^*$ is $\mathbb{E}[|E^*|] \cdot R \le m - m_{\mathrm{pub}} - m_{\mathrm{slack}}$, where $m_{\mathrm{pub}}$ is the public-layer occupancy ($\le 2$) and $m_{\mathrm{slack}}$ is the reserve for unexpected critical propositions. If violated, the subject must choose one of three: enlarge $T$, shrink the $E^*$ declaration (revising the decision set associated with $g^{(2)}$), or accept a lower $R$. System obligation: upon detecting a violation, issue a **feasibility-conflict alarm** to $R$ (the reflective layer) rather than silently degrading.*

**Proof**. The number of distinct propositions consumed is $\le m - m_{\mathrm{pub}}$ (budget partition); the number of critical propositions recalled is $\le$ the number consumed; taking expectations and using $R \cdot \mathbb{E}|E^*| \le \mathbb{E}[\text{critical propositions recalled}]$ gives the claim. $\blacksquare$

### 6.3 Submodularity of Utility and Greedy Guarantees

**Setup**. The firewall (Section 9) first removes items with $\hat m_i > \tau_m$, so the manipulation-penalty terms within the candidate pool are bounded; the selection utility is taken to be
$$U(A) = \underbrace{\sum_{e \in E} v_e\, \mathbb{1}\{A \cap D_e \ne \varnothing\}}_{U_{\mathrm{cov}}(A)\ \text{(coverage utility)}} + \mu \underbrace{\sum_{\sigma \in \mathcal{S}} \max_{i \in A} \mathrm{sim}(\sigma, i)}_{U_{\mathrm{div}}(A)\ \text{(diversity: facility location)}} - \lambda \sum_{i \in A} \hat m_i\, \tau_i,$$
subject to $\sum_{i \in A} \tau_i \le T_{\mathrm{push}}$. Here $\mathrm{sim} \ge 0$ is a similarity kernel on the stance manifold.

**Theorem 6.2 (Monotone submodularity)**. *$U_{\mathrm{cov}}$ and $U_{\mathrm{div}}$ are both monotone submodular set functions. Regarding the monotonicity of $U$: let $\mathcal{X}^+ := \{i : \text{the sum of item } i\text{'s coverage and diversity marginal gains} > 0\}$ (the subset of items whose marginal gain is positive after firewall filtering). Let $\underline g$ denote the minimum positive marginal gain over all items and all augmentation contexts. If $\lambda \max_i \hat m_i \tau_i < \underline g$ (the firewall's residual penalty is sufficiently small), then $U$ is monotone on $\mathcal{X}^+$.*

**Remark (the precise meaning of the monotonicity condition)**. On items with zero marginal gain (whose propositions are already covered and which bring no new stance similarity), the negative modular term $-\lambda\hat m_i\tau_i < 0$ makes $U$ strictly decrease—hence $U$ is in general not monotone on the **entire** candidate pool. This does not obstruct the greedy guarantee below: the greedy algorithm selects only elements of positive marginal gain at each step, and zero/negative-gain items (including all items outside $\mathcal{X}^+$) can be removed from any optimal solution without loss, so the problem is equivalent to monotone submodular maximization over $\mathcal{X}^+$. If the residual penalty is not negligible, $U$ is a non-monotone submodular function and randomized greedy (the $1/e$ guarantee of Buchbinder, Feldman, Naor & Schwartz, 2014) remains available, but with a worse constant—this paper adopts the institutional design in which "the firewall acts first so that the residual penalty is negligible."

**Proof**.

*$U_{\mathrm{cov}}$*: monotonicity is obvious ($v_e \ge 0$; adding an element can only increase coverage). Submodularity: for $A \subseteq B$, $i \notin B$,
$$U_{\mathrm{cov}}(A \cup i) - U_{\mathrm{cov}}(A) = \sum_{e:\, i \in D_e,\ A \cap D_e = \varnothing} v_e \ \ge\ \sum_{e:\, i \in D_e,\ B \cap D_e = \varnothing} v_e = U_{\mathrm{cov}}(B \cup i) - U_{\mathrm{cov}}(B),$$
where the inequality holds because $A \cap D_e = \varnothing \Leftarrow B \cap D_e = \varnothing$ ($A \subseteq B$): a proposition not yet covered by $B$ is necessarily not yet covered by $A$, but not vice versa. Marginal gains are nonincreasing as the set grows—this is submodularity.

*$U_{\mathrm{div}}$*: monotonicity is obvious ($\mathrm{sim} \ge 0$; the $\max$ is nondecreasing as the set grows). Submodularity: fixing $\sigma$, the function $A \mapsto \max_{i\in A}\mathrm{sim}(\sigma,i)$ is a special case of a weighted coverage function (replacing "proposition $e$" by "stance point $\sigma$" and "$D_e$" by "the similarity profile with $\sigma$"), or verify directly: for $A \subseteq B$, $i \notin B$,
$$\max\big(\mathrm{sim}(\sigma,i), \max_{A}\big) - \max_{A} \ \ge\ \max\big(\mathrm{sim}(\sigma,i), \max_{B}\big) - \max_{B},$$
because the left side $= (\mathrm{sim}(\sigma,i) - \max_A)^+$, the right side $= (\mathrm{sim}(\sigma,i) - \max_B)^+$, and $\max_A \le \max_B$ with $(x - a)^+ \ge (x - b)^+$ when $a \le b$. Summing over $\sigma$ preserves the inequality.

*Monotonicity composition*: the marginal contribution of the negative modular term $-\lambda\sum \hat m_i \tau_i$ is $\ge -\lambda \max_i \hat m_i\tau_i$; the minimum marginal gain of the positive terms on the firewall-filtered candidate pool is $> 0$ (an item of nonzero relevance contributes at least its coverage value). When the condition holds, the sum is monotone. $\blacksquare$

**Theorem 6.3 (Greedy approximation guarantees)**. *(i) (Equal costs, $\tau_i \equiv \tau$, cardinality constraint $|A| \le m$) Standard greedy (selecting at each step the element of maximal marginal gain) outputs $A_g$ satisfying*
$$U(A_g) \ \ge\ \Big(1 - \frac{1}{e}\Big)\, U(A^*) \ \approx\ 0.632\, U(A^*),$$
*where $A^*$ is the optimal solution. For the complete proof see Appendix B.4 (Nemhauser, Wolsey & Fisher, 1978).*

*(ii) (Unequal costs, knapsack constraint) The better of density greedy and the best single-element solution attains $\frac{1}{2}(1 - 1/e) \approx 0.32$ (folklore; proof see Leskovec et al., 2007); **partial enumeration + density greedy** attains exactly $1 - 1/e$ (Sviridenko, 2004—whose method performs density greedy on the residual knapsack after enumerating a constant number of elements, rather than continuous greedy); for the continuous-greedy + rounding framework see Călinescu, Chekuri, Pál & Vondrák (2011) ($1-1/e$ under a matroid constraint; knapsack constraints are reduced via enumeration). For this paper's special case—maximum coverage under a budget constraint—the (enumeration-augmented) density greedy of Khuller, Moss & Naor (1999) already attains $1-1/e$.*

**Engineering implications**: the selection layer neither needs to, nor possibly can, solve the NP-hard knapsack submodular maximization exactly; polynomial-time greedy already carries constant-ratio guarantees, and each greedy step's marginal gain naturally generates the auditable explanation required by S4 ("this item was selected because its marginal coverage value was the highest").

### 6.4 Dynamic Selection and Threshold-Type Optimal Policies

Static greedy handles "a batch of candidates"; the real push stream **arrives online**. This section gives the optimal policy structure for the online case.

**Setup (simplified but rigorous)**. Discrete time over $n$ periods, at most one item arriving per period; the arriving item's score $s \sim F$ is i.i.d. (the distribution known or estimated from history); the consumption reward $r(s)$ is strictly increasing and continuous; each consumption costs one "slot" (the equal-time-cost case), with $b$ total slots. Upon arrival the subject observes $s$ and immediately decides to consume or discard (discarding is irrevocable; deferral is treated in the remark below).

**Proposition 6.4 (Threshold-type optimal policy)**. *Let $W_i(b)$ be the optimal continuation value with "$i$ periods remaining and $b$ slots remaining." Then:*

*(i) (Bellman equation) $W_i(b) = \mathbb{E}_s\big[\max\{r(s) + W_{i-1}(b-1),\ W_{i-1}(b)\}\big]$ ($b \ge 1$), $W_i(0) = 0$, $W_0(b) = 0$.*

*(ii) (Threshold form) The optimal policy is a threshold policy: consume in the current period if and only if $r(s) \ge \tau_i(b) := W_{i-1}(b) - W_{i-1}(b-1)$. The threshold $\tau_i(b)$ is the opportunity cost (shadow price) of the remaining slots, monotone nonincreasing in $b$ and monotone nondecreasing in the number of remaining periods $i$.*

*(iii) (Concavity of $W$) $W_i(\cdot)$ is concave in $b$, so the shadow price rises as slots are consumed—the tighter the budget, the higher the threshold.*

**Proof**. (i) Standard DP decomposition (the current arrival is independent of future arrivals). (ii) $r$ strictly increasing $\Rightarrow$ $\{s: r(s) \ge \tau\}$ is an upper interval $\Rightarrow$ the threshold form; consuming beats discarding if and only if $r(s) + W_{i-1}(b-1) \ge W_{i-1}(b)$, and rearranging gives the threshold $\tau_i(b) = W_{i-1}(b) - W_{i-1}(b-1)$.

(iii) Let $\Delta_i(b) := W_i(b) - W_i(b-1)$ (i.e., $\tau_{i+1}(b)$), and $g(\tau) := \mathbb{E}[(r(s)-\tau)^+]$. By (i),
$$W_i(b) = W_{i-1}(b) + g\big(\Delta_{i-1}(b)\big), \qquad\text{hence}\qquad \Delta_i(b) = \Delta_{i-1}(b) + g\big(\Delta_{i-1}(b)\big) - g\big(\Delta_{i-1}(b-1)\big).$$
We prove by induction on $i$ that $\Delta_i(b)$ is nonincreasing in $b$ (i.e., $W_i$ is concave). Base: $\Delta_0 \equiv 0$. Inductive step: suppose $\Delta_{i-1}$ is nonincreasing, and set $x = \Delta_{i-1}(b-2) \ge y = \Delta_{i-1}(b-1) \ge z = \Delta_{i-1}(b)$. The function $g$ is continuous, decreasing, convex, and differentiable almost everywhere, with $g'(\tau) = -P(r > \tau) \in [-1, 0]$ (differentiating the expectation; boundedness of $r$ licenses dominated convergence). By the mean value theorem (with signs tracked explicitly): there exist $\xi_1 \in (y,x)$, $\xi_2 \in (z,y)$ such that
$$g(y)-g(x) = -\!\int_y^x g'(t)\,dt = \int_y^x P(r{>}t)\,dt = P(r{>}\xi_1)(x-y)\ \ge\ 0,$$
$$g(y)-g(z) = \int_z^y g'(t)\,dt = -\!\int_z^y P(r{>}t)\,dt = -P(r{>}\xi_2)(y-z)\ \le\ 0,$$
(First line: $y \le x$ and $g$ decreasing ⇒ $g(y) - g(x) \ge 0$, signs consistent; second line: $y \ge z$ ⇒ $g(y) - g(z) \le 0$, signs consistent.) Hence
$$\Delta_i(b-1) - \Delta_i(b) \;=\; (y-z) + \big[g(y)-g(x)\big] + \big[g(y)-g(z)\big] \;=\; (y-z)\big[1 - P(r{>}\xi_2)\big] + (x-y)\,P(r{>}\xi_1)\ \ge\ 0.$$
Therefore $\Delta_i$ is nonincreasing, $W_i$ is concave in $b$, and the threshold $\tau_i(b) = \Delta_{i-1}(b)$ is nonincreasing in $b$. **Nonnegativity ($W$ monotone in $b$)**: from the recursion together with $g \ge 0$, $g$ decreasing, and the inductively obtained $\Delta_{i-1}(b) \le \Delta_{i-1}(b-1)$, we have $\Delta_i(b) = \Delta_{i-1}(b) + g(\Delta_{i-1}(b)) - g(\Delta_{i-1}(b-1)) \ge \Delta_{i-1}(b)$; combined with the base case $\Delta_0 \equiv 0$ this gives $\Delta_i(b) \ge 0$ for all $i, b$—the option value of one extra slot is nonnegative. The same display also reads $\Delta_i(b) \ge \Delta_{i-1}(b)$: the opportunity cost per slot rises with the number of remaining periods—more future opportunities mean a higher option value of discarding. $\blacksquare$

**Remark (the deferral option and the cooling queue)**. Allowing items to be placed in a finite-capacity **cooling queue** (value decaying with novelty as $v(t) = v_0 e^{-\gamma t}$) is equivalent to adding an intermediate option to the discard decision: the policy becomes a three-way choice (consume / defer / discard), and the optimal structure remains a double-threshold form (a consumption threshold $\tau^{c}$ and a deferral threshold $\tau^{d} < \tau^{c}$: items whose marginal value lies between "the shadow price of consuming now" and "the expected shadow price of consuming later × decay" enter the queue). The proof is a state extension of Proposition 6.4 (adding a queue-occupancy dimension), with the structure unchanged; the complete treatment is left to the phase-two algorithms paper. Engineering implication: the cooling queue is an option, whose value is low in environments where information value decays fast (news) and high in slow-decay environments (research literature).

### 6.5 The Dual-Channel Architecture Principle (Synthesis of This Section)

**Definition 6.2 (Dual-channel architecture)**. The selection layer of a sovereign filter consists of two channels in parallel:

- **Channel I (the guarantee channel / direct pass-through)**: content from monitored source classes + content of watchlist entities, bypassing competitive ranking and guaranteed to arrive after deduplication (budget feasibility is monitored by Proposition 6.3). The recall guarantee comes from the redundancy-coverage theorem of Section 7 and is **independent of the score separability $d'$**;
- **Channel II (the discovery channel / scoring)**: all remaining candidates compete by the score $\langle w, \phi \rangle$ for the remaining slots, bearing "discovery of unmonitored critical propositions" and "value ranking when the budget binds." Its recall contribution is exactly characterized by Theorem 6.1: it increases with $d'$ and $\beta$, and has a hard ceiling under extreme filtering ratios.

**Architecture principle (a conjunctive corollary of Theorem 6.1 + Section 7)**: *High recall is a structural property, not a scoring property. Any aggressive-filtering design that substitutes "smarter ranking" for "a more complete pass-through structure" necessarily misses critical propositions when $d' < \underline{d'}(\beta,\pi,R)$.* Accordingly, indicators like "critical recall ≥95%" can only be attached to the architecture (the coverage guarantee of the pass-through structure + the honest contribution of the scoring channel), not to the scoring function—this is the theorem-level basis for all the division-of-labor design in this paper.

**Figure 2. The dual-channel architecture and the division of labor in recall guarantees**:

```{=latex}
\begin{figure}[h]
\centering
\begin{tikzpicture}[
  font=\small,
  box/.style={draw, rounded corners, align=center, minimum height=0.85cm, inner sep=4pt},
  chA/.style={box, fill=green!10},
  chB/.style={box, fill=blue!8},
  warn/.style={box, fill=red!8},
  arr/.style={-{Stealth[length=2mm]}, thick},
  node distance=0.5cm and 0.65cm]
\node[box] (pool) {candidate pool $N\sim 10^4$ documents/day};
\node[box, right=of pool] (collapse) {proposition collapse\\ $\rho_c$: documents $\to$ propositions\\ (Definition 4.2)};
\node[chA, above right=0.7cm and 0.65cm of collapse] (ch1) {Channel I (guarantee / pass-through)\\ monitored source classes + watchlist\\ recall $\ge 1-(1-p_{\min})^{k_{\mathrm{eff}}}$\\ \textbf{independent of $d'$} (Theorems 7.1--7.4)};
\node[chB, below right=0.7cm and 0.65cm of collapse] (ch2) {Channel II (discovery / scoring)\\ $\langle w,\phi\rangle$ competing for remaining slots\\ recall exactly constrained by $d',\beta$\\ (Theorem 6.1 identity)};
\node[box, right=2.1cm of collapse] (merge) {merge and deduplicate\\ budget-feasibility check\\ (Proposition 6.3)};
\node[box, right=of merge] (deliver) {delivery (summary = map)\\ class-C originals cannot be read by proxy\\ (Proposition 10.2)};
\node[warn, below=0.5cm of deliver] (alarm) {alarm on conflict\\ rather than silent degradation};
\draw[arr] (pool) -- (collapse);
\draw[arr] (collapse) -- (ch1);
\draw[arr] (collapse) -- (ch2);
\draw[arr] (ch1) -- (merge);
\draw[arr] (ch2) -- (merge);
\draw[arr] (merge) -- (deliver);
\draw[arr, dashed] (merge.south) |- (alarm.west);
\end{tikzpicture}
\caption{The dual-channel architecture: Channel I's recall guarantee comes from the redundant-coverage structure (independent of score separability); Channel II's recall contribution is honestly priced by the separability identity; the bottleneck theorem (Theorem 6.1) proves that the division of labor is a mathematical necessity, not an engineering preference.}
\end{figure}
```

---

<!-- RW-DONE §7 -->

## 7 Redundant-Coverage Theorems: Structural Conditions and the Applicability Domain of Recall under Aggressive Filtering

The recall guarantee of Channel I (the guarantee channel) is supplied by this section. The core insight: important information is **redundant** across the source space—a critical proposition is almost surely covered by multiple mutually independent source classes. Consequently, the extremely aggressive filtering of "retaining only the full content of a few trusted source classes" still maintains provably high recall for critical propositions. This section gives: (a) a complete proof for the independent case; (b) the **independent-subset bound** for the correlated case together with its **tightness**; (c) the dual optimization problem of monitoring-slot allocation; (d) the total-recall theorem; (e) the **applicability-domain boundary**—the strength of this section's guarantee depends conditionally on the provenance of the coverage floor $p_{\min}$, and real-corpus pilots in two domains provide the first version of this map (§7.5, §7.7).

### 7.1 Assumptions

- **R1 (Coverage floor)**: for every monitored trusted source class $\mathcal{C}_i$ ($i = 1,\dots,k$) and every critical proposition $e \in E^*$: $P(Z_i(e) = 1) \ge p_{\min}$, where $Z_i(e)$ is the coverage event of Definition 4.4. Empirical content: trusted source classes have a positive lower bound on their reporting rate for critical propositions; $p_{\min}$ must be calibrated by measurement on historical corpora (Section 14), with conservative prior $p_{\min} = 0.7$.
- **R2 (Conditional independence)**: given the criticality of proposition $e$, the coverage events $\{Z_i(e)\}_{i=1}^k$ are mutually independent. Real-world deviation: shared wire-service upstreams and inter-media reposting networks induce positive correlation. Mitigation: source classes are partitioned by (ownership × geography × type) to constructively suppress cross-class correlation (Definition 4.4); the residual correlation is explicitly priced by Theorem 7.2.
- **R3 (Pass-through rule)**: all content of watchlist entities in $\pi_{\mathrm{mon}}$ (companies, institutions, issues, and persons explicitly declared by the subject) bypasses scoring and is guaranteed to arrive after deduplication only.

### 7.2 The Independent Case

**Theorem 7.1 (Redundancy coverage, independent case)**. *Under R1–R2, a filter that retains only the content of $k$ monitored source classes (direct pass-through after deduplication) has, for any critical proposition $e \in E^*$, miss probability satisfying*
$$P(\mathrm{miss}\, e) \ \le\ (1 - p_{\min})^k.$$

**Proof**. Proposition $e$ is missed if and only if none of its documents is consumed. Channel I consumes all (deduplicated) content of the monitored classes, so a miss $\iff$ no monitored class covers $e$ $\iff \bigcap_{i=1}^k \{Z_i(e) = 0\}$. By R2 (conditional independence) and R1 ($P(Z_i = 0) \le 1 - p_{\min}$):
$$P(\mathrm{miss}\, e) = P\Big(\bigcap_{i=1}^k \{Z_i(e) = 0\}\Big) = \prod_{i=1}^k P(Z_i(e) = 0) \le (1 - p_{\min})^k. \qquad\blacksquare$$

**Numerics**: $p_{\min} = 0.7$, $k = 5 \Rightarrow P(\mathrm{miss}) \le 0.3^5 = 2.43\times 10^{-3}$, i.e., critical recall $\ge 99.76\%$; even at $p_{\min} = 0.5$, $k = 4$, one still has $P(\mathrm{miss}) \le 6.25\times10^{-2}$. **These are demonstration numbers for the independent case (where R2 holds exactly), not a universal guarantee**: $p_{\min}$ must be calibrated by measurement (for the estimation procedure see §7.5 and §14.7; confidence intervals should be reported), the correlated case must switch to the $k_{\mathrm{eff}}$ bound of Theorem 7.2, and the measured $\hat p_{\min} \approx 0.02$ of the academic-domain pilot is precisely an instance of R1 failing (§7.7). Subject to this premise: discarding 99% of documents is fully compatible with retaining 99% critical recall—provided the retained 1% is structurally selected "by redundant coverage across source classes" rather than competitively selected by score. (Contrast Theorem 6.1: the latter route requires $d' \ge 4.39$.)

### 7.3 The Correlated Case: The Independent-Subset Bound and Its Tightness

R2 holds only approximately in reality. This subsection gives an upper bound valid for **arbitrary dependence structures**, at the price of reducing the exponent from $k$ to the "effective number of independent classes."

**Definition 7.1 (Effective number of independent classes)**. For a fixed critical proposition $e$, a subset $S \subseteq [k]$ is called **$e$-independent** if $\{Z_i(e)\}_{i \in S}$ are mutually independent. Define
$$k_{\mathrm{eff}}(e) := \max\{|S| : S \subseteq [k] \text{ is } e\text{-independent}\}, \qquad k_{\mathrm{eff}} := \min_{e \in E^*} k_{\mathrm{eff}}(e).$$

**Theorem 7.2 (Redundancy coverage, correlated case)**. *Under R1 (without assuming R2), for any critical proposition $e$:*
$$P(\mathrm{miss}\, e) \ \le\ (1 - p_{\min})^{k_{\mathrm{eff}}(e)} \ \le\ (1 - p_{\min})^{k_{\mathrm{eff}}}.$$

**Proof**. Take an $e$-independent subset $S^*$ attaining the maximal cardinality in Definition 7.1, $|S^*| = k_{\mathrm{eff}}(e)$. Event inclusion: all $k$ classes failing to cover $\subseteq$ all classes in $S^*$ failing to cover, i.e.,
$$\{\mathrm{miss}\, e\} = \bigcap_{i=1}^k \{Z_i(e)=0\} \ \subseteq\ \bigcap_{i \in S^*} \{Z_i(e)=0\}.$$
By monotonicity of probability and independence on $S^*$:
$$P(\mathrm{miss}\, e) \le P\Big(\bigcap_{i\in S^*}\{Z_i(e)=0\}\Big) = \prod_{i \in S^*} P(Z_i(e)=0) \le (1-p_{\min})^{|S^*|}. \qquad\blacksquare$$

**Proposition 7.1 (Tightness)**. *Without further assumptions, the bound of Theorem 7.2 cannot be improved: for each $k_{\mathrm{eff}} \in \{1, \dots, k\}$ there exists a dependence structure satisfying R1 with $P(\mathrm{miss}\, e) = (1-p_{\min})^{k_{\mathrm{eff}}}$.*

**Proof**. Construction: take $k_{\mathrm{eff}}$ groups of mutually independent classes, with the $Z_i$ within each group perfectly correlated (sharing a single latent Bernoulli variable: media within a group share the same wire-service upstream, $Z_i \equiv Z_{\mathrm{group}}$, $P(Z_{\mathrm{group}}=1) = p_{\min}$); groups are mutually independent. Then $k_{\mathrm{eff}}$ (in the sense of Definition 7.1) is exactly the number of groups, and $P(\mathrm{miss}) = P(\text{no group covers}) = (1-p_{\min})^{k_{\mathrm{eff}}}$, with equality. $\blacksquare$

**Engineering implications**: (a) the quality of the bound is entirely determined by $k_{\mathrm{eff}}$, and $k_{\mathrm{eff}}$ can be actively enlarged through the grouping design of source classes (ownership, geography, type, wire-service upstream)—**independence is not a gift of nature; it is an artifact of architecture**; (b) $k_{\mathrm{eff}}$ can be measured from historical corpora: for a set of known critical propositions, estimate the correlation matrix of the classes' coverage indicators and find a maximal independent subset (conservatively: apply union-find merging to class pairs with correlation coefficient $|\rho_{ij}| > \epsilon_c$; the number of merged groups is a lower-bound estimate of $k_{\mathrm{eff}}$); (c) the substance of an astroturfing attack is the fabrication of independence—multiple "independent" sources are in fact a single actor. Defenses: root-node verification of the provenance tree (I3) + ownership penetration + content-fingerprint clustering (stress tests in Section 14).

### 7.4 Watchlist Pass-Through and the Constructive Zeroing of Tail Risk

**Proposition 7.2 (Constructive zeroing by the pass-through rule)**. *Under R3, for any proposition $e$ concerning a watchlist entity: $P(\mathrm{miss}\, e \mid \text{the entity published content about } e) = 0$. That is, the miss introduced by the filtering stage is zero; the residual risk is only "the entity itself remaining silent," which is irreducible for any filter.*

**Proof**. R3 stipulates that watchlist-entity content bypasses scoring and is guaranteed to arrive after deduplication; budget feasibility is monitored by Proposition 6.3 (an alarm on conflict rather than silent discarding). Hence whenever the content exists and passes provenance verification (against entity impersonation, I3), it is consumed. $\blacksquare$

**Sensitivity discussion** (explicit handling of the weakness of R1): the soft underbelly of Theorems 7.1–7.2 is R1—**niche but personally critical propositions lack source redundancy** ($P(Z_i(e)=1)$ is close to 0 for most classes). Three layers of backstop: (1) R3 pass-through constructively zeroes the long-tail risk that "the subject can foresee"—this is precisely how "active acquisition" complements "passive filtering": the watchlist is the subject's actively declared projection of $g^{(2)}$; (2) the public agenda layer (Section 12) provides a second backstop for events "unforeseen by the subject but publicly momentous" (redundantly attested propositions are forced into everyone's view); (3) the scoring Channel II bears probabilistic discovery (its recall contribution honestly priced by $d'$). Beyond the three layers there remains an irreducible residual: propositions with no trusted redundant sources, undeclared, not publicly momentous, and undiscovered by scoring—this paper does not pretend it is zero, but lists it as a measured audit item under P4 of Section 13.

### 7.5 The Dual Problem: Monitoring-Slot Allocation

The first decision on the active-acquisition side: **which source classes to monitor?** Slots are limited (the budget constraint $m_{\mathrm{mon}}$, the pass-through quota constraint), candidate classes outnumber slots, and selection is required.

**Definition 7.2 (Probabilistic coverage utility)**. Let $\mathcal{K}$ be the set of candidate classes, choose $S \subseteq \mathcal{K}$, $|S| \le B$ (or a cost constraint $\sum_{i\in S} c_i \le B$). A critical proposition $e$ carries a prior weight $w_e$ (derived from the decision set declared by $g^{(2)}$) and class coverage probabilities $p_i(e) := P(Z_i(e)=1)$. Define
$$U_{\mathrm{mon}}(S) := \sum_{e \in E^*} w_e \cdot P\big(e \text{ is covered by at least one class in } S\big) \;=\; \sum_{e} w_e \Big(1 - \prod_{i \in S}\big(1 - p_i(e)\big)\Big)$$
(the second equality uses R2 cross-class independence; for a conservative version in the correlated case see the remark).

**Theorem 7.3 (Submodularity of monitoring allocation and greedy guarantees)**. *$U_{\mathrm{mon}}$ is monotone submodular. Hence: under a cardinality constraint, greedy (adding at each step the class of maximal marginal gain) attains $(1-1/e) \approx 63.2\%$ of optimal; under a cost constraint, the better of density greedy and the best single class attains $\frac12(1-1/e)$ (folklore, see Leskovec et al., 2007), and partial enumeration + density greedy attains $1-1/e$ (Sviridenko, 2004).*

**Proof**. Monotonicity is obvious (each factor $1 - \prod(1-p_i)$ is nondecreasing in $S$, and $w_e \ge 0$). Submodularity: fix $e$, write $q_i = 1 - p_i(e) \in [0,1)$, $f_e(S) = 1 - \prod_{i\in S} q_i$. For $A \subseteq B$, $j \notin B$:
$$f_e(A \cup j) - f_e(A) = \Big(\prod_{i\in A} q_i\Big)(1 - q_j) \ \ge\ \Big(\prod_{i\in B} q_i\Big)(1 - q_j) = f_e(B \cup j) - f_e(B),$$
since $\prod_{i\in A} q_i \ge \prod_{i\in B} q_i$ ($q_i \le 1$). Weighted summation preserves submodularity. The greedy guarantees cite Appendix B.4 together with Sviridenko (2004) and Leskovec et al. (2007). $\blacksquare$

**Remark (the correlated case)**. If classes are positively correlated, the true $P(\text{covered by at least one class})$ is lower than the independence formula, but the independent-subset method of Theorem 7.2 applies equally: run greedy in units of the $k_{\mathrm{eff}}$ independent groups; within-group selection degenerates to the selection of a group representative. Astroturfing inflates $U_{\mathrm{mon}}$ through "pseudo-independent groups"—for defenses see 7.3(c).

**Connection to Pandora's box**: Theorem 7.3 solves "whom to monitor among known classes"; **exploration when class quality is unknown** (subscription trial and error) is the Pandora problem of Section 8.3—the two together form the closed loop of the monitoring list's life cycle: "explore → admit → audit → rotate out."

**Empirical Finding E-7.1 (The endogeneity of $\hat p_{\min}$; the academic-domain pilot)**. A researcher profile × real-corpus temporal replay of arXiv 2019-09 (monitoring universe of 2,576 propositions; critical set $E^*$ = the month's top-2% most-cited papers, $K^*=52$; experimental details in §14.7) provides the first measurement of the decisive role of list-construction strategy on coverage: an author-granularity list (top-50 by prior-window frequency or citation rank) covered only 1/52 of the month's critical papers ($\hat p_{\min}\approx0.02$)—the authors of the most important papers such as ALBERT and Megatron-LM ranked beyond 1500th in the prior window; an institution-granularity list (top-50 leading labs) gave $\hat p_{\min}=0.37$, and a trimmed top-10 list gave $\hat p_{\min}=0.17$ with supply matched to the budget. **Conclusion: the $p_{\min}$ of R1 is not an environmental constant but a design function of list granularity and capacity**—the construction of the monitoring list is itself a pull-side optimization problem (the submodular greedy of Theorem 7.3 + the admission criterion of Proposition 8.1 should be solved jointly, not by a top-N heuristic); for low-redundancy profiles, the ceiling of Channel I's benefit is determined by the diminishing margin of the capacity–coverage curve (measured coverage rose only from 0.17 to 0.46 as list size went from 10 to 400—the measured ceiling of the list-coverage floor $\hat p_{\min}$, not end-to-end recall; at this configuration supply far exceeds the budget, and quota dilution makes end-to-end recall lower still). Note the limitation of the ground-truth proxy here: top-2% citation is a post-hoc indicator lagged by years and carrying prestige bias; within this paper's own framework it is closer to "academic engagement" than to ex ante criticality—§14.7 gives a sensitivity discussion of this proxy.

**Empirical Finding E-7.2 (The institutional provenance of $p_{\min}$ and the dual-ground-truth split in $d'$; the financial-domain pilot)**. An investor profile × real-corpus temporal replay of EDGAR + public news archives, 2019-09 (dual ground truth: legally material 8-Ks and market-moving days; experimental details in §14.7) supplies the other half of the applicability-domain map: (a) **$p_{\min}$ can have an institutional provenance**: the regulatory primary-source class's coverage of the legal ground truth (material 8-Ks) is $\hat p_{\min} = 1.00$—the four-day filing rule for 8-Ks writes the coverage guarantee into law; against the market ground truth, $\hat p_{\min}=0.70$–$0.73$ (depending on the news-layer version; see the caliber comparison in Table 14-3), and wire-service classes add a further ~0.25–0.27 of independent coverage—**a multi-class redundancy structure ($k_{\mathrm{eff}}\ge2$) becomes measurable on real data for the first time**; (b) **the honest-feature scorer's $d'$ splits by ground truth**: legal criticality is predictable from disclosure metadata ($d'=2.65$–$3.49$, depending on the feature-set version), while market criticality is only partially predictable from realized attention signals ($d'=0.54$–$0.60$)—both far below the 95%-recall requirement line (≈4.4); criticality on the market dimension is borne **mainly** by structure, an independent confirmation of Theorem 6.1's thesis in a second domain; (c) **the strong form of high recall holds when its conditions are fully met**: portfolio-holdings pass-through (25 holdings, supply of 4.6 propositions/day), under quota-matched conditions, showed within-portfolio market-ground-truth recall climbing with the budget: 0.444 at $m=1$ → 0.952 at $m=5$ (meeting the target); after the news-layer expansion the same setting diluted to 0.910 (the news propositions of company-days drew away quota—"approaching but not crossing the line"; fulfillment requires raising the quota or strengthening within-list ranking). Contrasted with the academic domain (where under the same framework and methods the strong form was rejected, best end-to-end recall 0.28), this yields a first empirical regularity: **recall-guarantee strength = the institutional provenance of $p_{\min}$ (law > media redundancy > list design) × supply–quota fit × the consistency between the scope of $E^*$ and the profile's decision set**. Again note the ground-truth proxy limitation: market-moving days are post-hoc labels, and 90% of market-moving days are not attributable to same-day information—"recall of market-moving days" does not equal "recall of ex ante critical information"; §14.7 gives the second ground truth and the sensitivity analysis.

### 7.6 The Total-Recall Theorem

**Theorem 7.4 (Total-recall lower bound)**. *Suppose Channel I is configured as in 7.2–7.4; Channel II (scored discovery), conditional on Channel I failing, recovers non-watchlist critical propositions with conditional probability $R_{\mathrm{II}} := P(\text{II recovers} \mid \text{I fails})$ ($R_{\mathrm{II}}$ is determined by $d', \beta$ of Theorem 6.1, and need not be defined for watchlist entities $e \in \mathrm{WL}$—pass-through already guarantees them). Then under R1 and R3, for any $e \in E^*$:*
$$P(\mathrm{miss}\, e) \ \le\ (1-p_{\min})^{k_{\mathrm{eff}}} \cdot \big(1 - R_{\mathrm{II}}\,\mathbb{1}\{e \notin \mathrm{WL}\}\big),$$
*and in particular the unconditional upper bound $P(\mathrm{miss}\, e) \le (1-p_{\min})^{k_{\mathrm{eff}}}$ holds.*

**Proof**. A miss requires both channels to fail simultaneously. For $e \notin \mathrm{WL}$, by the chain rule of conditional probability ($R_{\mathrm{II}}$ is defined precisely by conditioning on "Channel I fails," so no independence assumption is needed):
$$P(\mathrm{miss}\, e) = P(\text{I fails})\cdot P(\text{II fails} \mid \text{I fails}) = P(\text{I fails})\,(1 - R_{\mathrm{II}}) \le (1-p_{\min})^{k_{\mathrm{eff}}}(1 - R_{\mathrm{II}}),$$
with the first factor bounded by Theorem 7.2. For $e \in \mathrm{WL}$, Proposition 7.2 gives $P(\text{I fails}) = 0$, and the miss probability is zero. The unconditional bound follows from $R_{\mathrm{II}} \ge 0$. $\blacksquare$

**Remark (computability of $R_{\mathrm{II}}$ and selection bias)**. Theorem 6.1 gives the scoring channel's recall over **all** critical propositions (as a function of $d', \beta, \pi$), whereas $R_{\mathrm{II}}$ is the conditional recall over the **selected subset** of "Channel I failures." The two are generally unequal: propositions on which Channel I fails are systematically skewed toward low-redundancy, low-coverage types, whose scorable features (news volume, source prestige) are also weaker, so $R_{\mathrm{II}}$ is typically **lower** than the unconditional recall of Theorem 6.1—substituting the latter directly into this theorem would overestimate total recall. This paper therefore treats only the unconditional upper bound $P(\mathrm{miss}\,e) \le (1-p_{\min})^{k_{\mathrm{eff}}}$ as a theorem-level guarantee, with $R_{\mathrm{II}}$ handled as a measured quantity (the simulations of Section 14 estimate this conditional probability directly).

**KPI implementation**: the simulations and synthetic ecology (Section 14) measure $P(\mathrm{miss})$ directly and compare it against $(1-\hat p_{\min})^{\hat k_{\mathrm{eff}}}$; the **real-corpus temporal replay** (§14.7) measures misses exactly against official event lists / debunking archives as ground truth (H4'); human-jury audits remain in the postponed L3 design (§15.5).

### 7.7 Applicability-Domain Boundaries and Claim Calibration (An Honest Summary)

The relationship between the strength of this section's theorems and their own pilot evidence must be understood according to the following calibration—this is the central calibration of the paper's empirical claims:

1. **The theorem guarantee is conditional**. The numerical comfort of $P(\mathrm{miss}) \le (1-p_{\min})^{k_{\mathrm{eff}}}$ (e.g., $p_{\min}=0.7, k=5 \Rightarrow 99.76\%$) comes from the universal quantification of R1 (for **every** $e \in E^*$, $P(Z_i)\ge p_{\min}$). The pilots show that $\hat p_{\min}$ is a strong function of list granularity and capacity: author-granularity lists go as low as $\hat p_{\min}\approx0.02$, at which point the $(1-\hat p_{\min})^k$ bound is vacuous ($0.98^5\approx0.90$); the only source of $\hat p_{\min}=1.00$ is a **legal institution** such as the four-day filing rule for 8-Ks, not the framework itself.
2. **Two honest readings; this paper takes the second**. (a) Restrict $E^*$ to "redundantly covered critical propositions"—this would make the theorem nearly tautological ("propositions covered by many sources are not missed"); (b) keep general $E^*$ and read this section as a **weighted/expected-form leakage bound**: measured by the $U_{\mathrm{mon}}$ of Definition 7.2, the expected weighted leakage of a list $S$ is $\sum_e w_e\prod_{i\in S}(1-p_i(e))$, with every per-proposition coverage probability $p_i(e)$ calibrated by measurement—this is precisely the use of the dual problem of §7.5 and the correct usage scenario of Theorem 7.3's greedy guarantee. This paper's deployment form (list construction = submodular optimization + quota-feasibility alarms + the feasibility audit of Proposition 6.3) is designed according to reading (b).
3. **The correct statement of "≥95% critical recall"**: attainable under the conjunction of four conditions—the institutional provenance of $p_{\min}$, the effective number of independent classes $k_{\mathrm{eff}}$, list–budget quota fit, and the consistency between the scope of $E^*$ and the profile's decision set (measured 0.952 within the portfolio in the financial domain); in domains where the conditions are not fully met (the academic domain) it is rejected by real data (best 0.28), thereby sharpened into boundary conditions. All recall figures in Section 14 are reported according to this calibration.

---

<!-- RW-DONE §8 -->

## 8 A Theory of Active Acquisition (Pull) and the Attention No-Arbitrage Theorem

This section takes up the third of the four questions: "Beyond filtering, what should be actively acquired, how much, and when should one stop?" The classical traditions surveyed in Section 2.7 (search, foraging, experimental design, bandits, optimal stopping) are woven here into the pull side of the SAP and brought, by the **attention no-arbitrage theorem** (Theorem 8.1), under the same shadow price that governs the push side and the reflection load. A caveat is in order: mathematically, Theorem 8.1 is a direct application of the KKT conditions for concave programming; its contribution is not to generalize any classical result but to **show that the marginal value theorem, Pandora's stopping rule, and the consumption threshold are all special cases of a single variational principle**, thereby turning budget allocation among push / pull / reflection into a control problem that can be estimated online.

### 8.1 The Space of Pull Operators

**Definition 8.1 (Pull operators)**. In each period, an active-acquisition policy $\pi_{\mathrm{pull}}$ selects a combination of three classes of operators:

- **Exploration operator** $e$: a trial investment in a candidate source $s \notin \pi_{\mathrm{mon}}$ (reading its historical content, a small-sample subscription), at cost $c_e$ (minutes), with reward a random variable $X_s$ (the source's expected daily VOI once admitted to monitoring, estimated with noise);
- **Query operator** $q$: targeted retrieval (keywords, lateral reading, database queries, delegating subtasks to AI agents), at cost $c_q$, with reward the query's expected information gain $\mathrm{EIG}(q \mid K)$ relative to the decision set $D$ and the knowledge state $K$;
- **Dwelling operator**: continued reading of an already-subscribed source (a patch), dwelling for a duration $t$ with cumulative reward $G_s(t)$ (concave: the first few items capture most of the value, with diminishing margins thereafter).

The total pull cost per period, $c(\pi_{\mathrm{pull}}) = \sum c_e + \sum c_q + \sum t$, enters the budget identity $T = T_{\mathrm{pull}} + T_{\mathrm{push}} + T_{\mathrm{ref}}$.

### 8.2 The Attention No-Arbitrage Theorem

**Setup**. Allocate the budget $T$ across $U$ uses (push consumption, the various pull operators, reflection); use $u$ receives $x_u \ge 0$ minutes and yields expected value $V_u(x_u)$. Assume:

- **(P1) Concavity**: $V_u$ is increasing, concave, and continuously differentiable. Economic rationale: redundancy—the first few items of a source capture most of its value (the expectation-level manifestation of the submodularity of the coverage utility); the marginal EIG of queries is diminishing (the submodularity of Theorem 8.2); the marginal virtue gain of reflection is diminishing (the drift structure of Section 10).
- **(P2) Separability**: $V(x) = \sum_u V_u(x_u)$ (no interaction across uses). Idealization: complementarities (retrieval results change the novelty baseline of push scoring) do exist and are treated as second-order terms; the simulations (Section 14) include interaction stress tests.

**Theorem 8.1 (Attention no-arbitrage / marginal-VOI equilibrium)**. *Under (P1)–(P2), a budget allocation $x^* = (x_u^*)$ is optimal ($\sum_u x_u^* = T$, $x_u^* > 0$ for interior uses) if and only if there exists $\nu > 0$ (the shadow price of the budget) such that*
$$V_u'(x_u^*) = \nu, \qquad \forall u \text{ (interior)}; \qquad V_u'(0) \le \nu, \ \forall u \text{ (corner } x_u^* = 0\text{)}.$$
*Corollary (the no-arbitrage principle): if two uses $u, u'$ satisfy $V_u'(x_u) > V_{u'}'(x_{u'})$, then shifting $\epsilon$ minutes from $u'$ to $u$ yields a first-order gain $\epsilon\,(V_u' - V_{u'}') + o(\epsilon) > 0$—any allocation in which marginal VOI per minute differs across uses is suboptimal, and both the direction and the magnitude of the improvement can be estimated by measurement.*

**Proof**. Necessity: suppose $x^*$ is optimal and there exist interior uses $u, u'$ with $V_u'(x_u^*) > V_{u'}'(x_{u'}^*)$. Take $\epsilon > 0$ sufficiently small and set $x'_u = x_u^* + \epsilon$, $x'_{u'} = x_{u'}^* - \epsilon$, all else unchanged (feasibility: interiority + budget conservation). By differentiability,
$$V(x') - V(x^*) = \big[V_u(x_u^*+\epsilon) - V_u(x_u^*)\big] + \big[V_{u'}(x_{u'}^*-\epsilon) - V_{u'}(x_{u'}^*)\big] = \epsilon\big(V_u'(x_u^*) - V_{u'}'(x_{u'}^*)\big) + o(\epsilon) > 0$$
for sufficiently small $\epsilon$, contradicting optimality. The corner condition is analogous (if $V_u'(0) > \nu = V_{u'}'(x_{u'}^*)$, moving in yields a positive gain). Sufficiency: suppose there exists a $\nu$ for which the conditions hold. For any feasible $x$, concavity gives $V_u(x_u) \le V_u(x_u^*) + V_u'(x_u^*)(x_u - x_u^*)$; summing,
$$V(x) - V(x^*) \le \sum_u V_u'(x_u^*)(x_u - x_u^*) = \nu \sum_u (x_u - x_u^*) = \nu\,(T - T) = 0,$$
(interior uses saturate the equality $V_u' = \nu$; at a corner $x_u^* = 0$, $V_u'(0)(x_u - 0) \le \nu x_u$ because $V_u'(0) \le \nu$.) Hence $x^*$ is globally optimal. $\blacksquare$

**The organizing power of Theorem 8.1**: the following three classical rules are all special cases of the variational principle "marginal value = shadow price $\nu$"—

| Classical rule | Source | Role within SEA |
|---|---|---|
| Patch-leaving rule: leave when the instantaneous intake rate falls to $\nu$ | Charnov (1976), Proposition 8.2 | the optimal stopping condition of the dwelling operator |
| Pandora's stopping rule: boxes with reservation index $z < \nu$ are not opened | Weitzman (1979), Proposition 8.1 | the admission condition of the exploration operator |
| push consumption threshold: consume only if $r(s) \ge \tau = \nu$ | Proposition 6.4 | the marginal condition of filtering |

**Engineering implications**: the scheduler's task is not to solve the global SAP but to **estimate online the marginal VOI of each use and shuttle the budget until the differences fall inside the noise band**. The loss from deviating from the optimum by $\epsilon$ (minutes misallocated) is second-order (envelope theorem: $V(x^*) - V(x) \le \frac{L}{2}\|\epsilon\|^2$, where $L$ is the Lipschitz constant of $V'$)—a quantitative guarantee that "approximate scheduling is good enough." The simulations of Section 14 contrast "marginal-VOI adaptive scheduling vs. fixed partition."

### 8.3 Source Exploration: Pandora's Box and Monitoring Admission

**Theorem (Weitzman, 1979; classical result, cited)**. *$n$ boxes; box $i$ costs $c_i$ to open and contains an independent random reward $X_i \sim F_i$; after opening, one may take the maximum reward among opened boxes and stop, or continue opening. Define the **reservation index** $z_i$ as the unique solution of the equation*
$$\mathbb{E}\big[(X_i - z_i)^+\big] = c_i$$
*Optimal policy: open boxes in descending order of $z_i$; stop and take the best opened reward once the maximum reward among opened boxes is $\ge$ the maximum index among the remaining boxes.*

(Existence and uniqueness: the left-hand side is continuous and strictly decreasing in $z_i$, diverging to $+\infty$ as $z_i \to -\infty$ and tending to 0 as $z_i \to +\infty$, so the intermediate value theorem yields a unique solution. For the optimality proof see Weitzman (1979).)

**Proposition 8.1 (The monitoring-admission criterion)**. *Treat "exploring a candidate source $s$" as opening a box (cost $c_e$, reward $X_s$ = the expected daily VOI of monitoring that source, discounted over the monitoring horizon), and treat "devoting attention to the current best existing use" as a free box with cost zero and reward deterministically equal to the shadow price $\nu$ (Theorem 8.1). Then:*

*(i) (Exploration admission) A candidate source is worth exploring if and only if its reservation index $z_s \ge \nu$; exploration proceeds in descending order of $z_s$;*

*(ii) (Monitoring admission) Once exploration reveals the realized value $X_s$, the source enters the monitoring list if and only if $X_s \ge \nu$, and this must be adjudicated jointly with the coverage greedy of Theorem 7.3 (when slots conflict, rank by marginal coverage gain per unit cost);*

*(iii) (Rotation-out) When the rolling $X_s$ estimate of a monitored source (the time average of realized VOI) falls below $\nu$ for more than $L$ consecutive periods, a rotation-out recommendation is triggered (a class-B decision, requiring human sign-off, §11.1).*

**Proof**. (i)(ii): add the free box ($c = 0$, $X \equiv \nu$) to the Weitzman problem; its reservation index is given by $\mathbb{E}[(\nu - z)^+] = 0$, i.e., $z = \nu$; Weitzman's theorem then applies directly: open boxes in descending index order, and stop once the best opened value exceeds the remaining indices (including $\nu$)—that is, boxes with $z_s < \nu$ are not opened, and realized values $X_s < \nu$ are not taken. (iii): rotation-out is the time-reversal of admission: the opportunity cost of occupying a monitoring slot is $\nu$ (the slot's shadow price), and an occupancy persistently below that opportunity cost should be released; the $L$-period lag guards against noise jitter (the estimation error $\sigma_X / \sqrt{L}$ shrinks with $L$). $\blacksquare$

**Remark**: when $X_s$ is non-stationary (source-quality drift), the stationary Pandora assumption fails; the remedy is rolling-window estimation + drift detection (CUSUM), and the theory falls under the restless-bandit framework of Section 8.6.

### 8.4 Patch Dwelling: The Marginal-Value Rule

**Proposition 8.2 (Optimal dwelling on an information patch)**. *The cumulative information reward of a source (patch) $s$ is $G_s(t)$: $G_s(0) = 0$, increasing, concave (redundancy and novelty decay). The cost of switching to the next patch is $c_{sw}$ (the time to rebuild context; the switching cost of cognitive load theory). The long-run average intake rate is*
$$R(t) = \frac{G_s(t) - c_{sw}}{t}.$$
*The optimal dwelling time $t^*$ satisfies **marginal = average**:*
$$G_s'(t^*) = R(t^*) \quad\Longleftrightarrow\quad G_s'(t^*)\, t^* = G_s(t^*) - c_{sw}.$$
*In equilibrium, $R(t^*) = \nu$ (no-arbitrage: the average rates of all active patches are competed down to the shadow price).*

**Proof**. $R$ is differentiable; the first-order condition $R'(t^*) = 0$:
$$R'(t) = \frac{G_s'(t)\,t - (G_s(t) - c_{sw})}{t^2} = 0 \iff G_s'(t^*)\,t^* = G_s(t^*) - c_{sw} \iff G_s'(t^*) = R(t^*).$$
$G_s$ concave $\Rightarrow$ $G_s'$ decreasing and $R$ quasi-concave $\Rightarrow$ the first-order condition yields the global maximum (at the boundaries, $R \to -\infty$ as $t \to 0$ ($c_{sw}>0$) and $R \to 0$ as $t \to \infty$ ($G$ bounded or sublinear)). Equilibrium: if some patch has $R(t^*) > \nu$, extending its dwelling time is profitable (the arbitrage direction of Theorem 8.1), until diminishing margins pull $R$ back to $\nu$. The standard variant with "travel time" $\tau_{sw}$ (the fixed time to re-enter context after a switch): $R(t) = G_s(t)/(t + \tau_{sw})$, and the same derivation gives the tangency condition $G_s'(t^*) = R(t^*)$.

**Boundary cases (existence conditions for an interior solution)**. The first-order condition has a finite solution if and only if $c_{sw} < \bar c := \sup_{t>0}\big[G_s(t) - t\,G_s'(t)\big]$ (since $G_s$ is concave with $G_s(0)=0$, $G_s(t) - tG_s'(t)$ is nondecreasing in $t$, so $\bar c = \lim_{t\to\infty}[G_s(t) - tG_s'(t)]$, and when $G_s$ is bounded, $\bar c = G_s(\infty)$). If $c_{sw} \ge \bar c$ (the switching cost exceeds the entire "quasi-rent" the patch can generate), then $R'(t) > 0$ identically, $R$ is monotone increasing, and no finite interior optimum exists: the optimum is $t^* = +\infty$ (once entered, never switch) or, by the no-arbitrage condition, the patch is not entered at all (when $\sup_t R(t) < \nu$). Engineering implication: under high switching costs the patch structure degenerates—monitoring-list design should depress $c_{sw}$ (standardized summary formats, stable source context) rather than merely optimize $G_s$. $\blacksquare$

**This is information foraging made normative**: the descriptive "information-scent following" of Pirolli & Card (1999) acquires in SEA an explicit stopping rule; the engineering identity of "scent" is an online estimate of $G_s'(\cdot)$ (rolling proxies of click depth and content novelty).

### 8.5 Query Batches: The Submodularity of Expected Information Gain

**Setup**. A query set $\mathcal{Q}$ (candidate queries, retrieval expressions, lateral-reading targets), each $q$ with cost $c_q$, returns an observation $Y_q$ (a noisy signal about $\Theta_{\mathrm{rel}}$). The value of a batch $Q \subseteq \mathcal{Q}$ is $I(Q) := I(Y_Q;\, \omega \mid K)$ (conditional mutual information given the current knowledge state). The submodular structure of such problems has been systematically studied in sensor-network placement (Krause, Singh & Guestrin, 2008); this paper transplants it to the cognitive-budget setting.

**Theorem 8.2 (Monotonicity of EIG and submodularity under conditional independence)**.

*(i) (Monotonicity, no additional assumptions) $I(Q)$ is monotone nondecreasing in $Q$.*

*(ii) (Submodularity) If the observations are conditionally independent given $\omega$ ($Y_q \perp Y_{q'} \mid \omega$), then $I(Q)$ is submodular.*

*(iii) (Guarantees) With equal costs, greedy attains $(1-1/e)$ (Nemhauser et al., 1978); under a cost constraint, the better of density greedy and the best single query attains $\frac12(1-1/e)$ (Leskovec et al., 2007), and partial enumeration + density greedy attains $(1-1/e)$ (Sviridenko, 2004).*

**Proof**. (i) Chain rule and nonnegativity of mutual information: for $q \notin Q$,
$$I(Q \cup q) - I(Q) = I(Y_q;\, \omega \mid Y_Q) \ \ge\ 0.$$

(ii) The gain is $\Delta(Q, q) := I(Y_q; \omega \mid Y_Q)$. Under the conditional-independence assumption,
$$\Delta(Q,q) = H(Y_q \mid Y_Q) - H(Y_q \mid Y_Q, \omega) = H(Y_q \mid Y_Q) - H(Y_q \mid \omega).$$
For $Q' \subseteq Q$: conditioning reduces entropy, $H(Y_q \mid Y_Q) \le H(Y_q \mid Y_{Q'})$; the second term is independent of $Q$. Hence $\Delta(Q, q) \le \Delta(Q', q)$: the gain decays as the selected set grows—this is submodularity.

(iii) See Appendix B.4 and the literature cited. $\blacksquare$

**Connection to lateral reading**: the lateral reading of Wineburg & McGrew (2019) (leaving the current page and opening new queries to verify the source and the claim) is, in this framework, a **query operator of targeted EIG maximization**—its information gain on "the credibility dimension $c_i$ of the current item" far exceeds that of continuing to read deeply (deep reading only adds to the content dimension). The decomposition of Theorem 5.1 explains its empirical advantage: when the $\mathrm{Harm}$ term dominates the uncertainty, a query that lowers $(1-c_i)\mathrm{Harm}$ has higher marginal value than deep reading that raises $\mathrm{VOI}(y)$. The scoring function should therefore treat "credibility uncertainty" as a state variable that triggers a lateral-reading recommendation (tested in the simulations of Section 14).

**Making the novelty dimension computable**: the novelty of $\phi$ $=$ a proxy for $I(y_i; \omega \mid K)$. In practice it is estimated through a dual channel of cosine novelty in embedding space + proposition-graph deduplication (propositions already in $K$ ⇒ zero gain); Theorem 8.2(ii) guarantees the correctness of greedy at the batch level.

### 8.6 Continual Monitoring Scheduling: The Restless-Bandit Framework

The $n$ sources inside the monitoring list update every day, and the subject can deep-read only $b$ of them per period ($b \ll n$). Each source is an arm with an evolving state: when unread, its content accumulates (value decays while the information stockpile grows); when read, the current period's VOI is harvested. This is a **restless bandit** (Whittle, 1988): the general case is PSPACE-hard (Papadimitriou & Tsitsiklis, 1999), but the **Whittle index** heuristic (compute for each arm the shadow-price subsidy that "makes it passive," and activate arms in descending order of the index) is asymptotically optimal in the many-armed sense (Weber & Weiss, 1990) and empirically robust on "indexable" structures such as monitoring scheduling. Engineering specification: the Whittle index = the marginal-VOI difference of the source between "read now vs. read later," which is precisely the source-granularity instance of Theorem 8.1's $\nu$ comparison—scheduler and no-arbitrage principle share the same shadow price. The Gittins index (Gittins, 1979) applies to the simplified case in which "when one source is read, the others freeze" (the stochastic bandit) and gives a strictly optimal index policy; this paper adopts the restless version to match real asynchronous updating.

### 8.7 Connection to Rational Inattention

**Proposition 8.3 (The softmax choice form)**. *In the static single-period simplification of the SAP, if the information cost of attention is priced in Shannon mutual information ($\lambda$ is the utility price per unit of mutual information, Cover & Thomas, 2006), then the optimal choice probabilities take the logit form:*
$$P(i \in A) \ \propto\ \pi_i^0 \cdot \exp\big(\langle w, \phi_i\rangle / \lambda\big),$$
*where $\pi_i^0$ are prior attention weights. That is: exact top-$m$ threshold selection is the limit as $\lambda \to 0$ (attention measured for free); for $\lambda > 0$ the optimal policy is randomized soft selection.*

**Proof sketch** (a specialized restatement of Matějka & McKay, 2015): the Lagrangian $\mathcal{L} = \sum_i p_i u_i - \lambda\, I(p;\cdot)$, varied over the choice distribution, yields first-order conditions giving $p_i \propto \pi_i^0 e^{u_i/\lambda}$; substituting $u_i = \langle w,\phi_i\rangle$ gives the result. For the complete derivation see Matějka & McKay (2015). $\blacksquare$

**Implications**: (a) the threshold policy (Proposition 6.4) and soft selection (Proposition 8.3) are two attention-cost regimes of the same problem, and the system should treat $\lambda$ as a calibratable parameter; (b) the microfoundation of "endogenous attention" from the rational-inattention literature is absorbed into SEA, while its defect—that "the objective function is known and stable" (Section 2.1)—is supplied by the SAP's $g^{(2)}$ structure and the virtue dynamics of Section 10.

### 8.8 The Unified Picture

At this point the decomposition-and-solution structure of the SAP is complete:

$$\text{SAP} \;=\; \underbrace{\text{Theorem 8.1 (budget no-arbitrage)}}_{\text{inter-layer}} \circ \underbrace{\text{Section 6 (push selection)} + \text{Section 7 (monitoring coverage)} + \text{\S8.3--8.6 (pull operators)}}_{\text{intra-layer}} \circ \underbrace{\text{Sections 9--12 (safety, sublimation, emergency, and publicness constraints)}}_{\text{constraint assembly}}$$

All layers share the same shadow price $\nu$: it is the consumption threshold of push, the stopping line for exploration / dwelling / query on the pull side, the admission / rotation-out line of the monitoring list, and the opportunity cost of reflection time in Section 10. **"Proactivity" thereby acquires a precise definition: active acquisition = the subject continually restructuring its own candidate pool with $\nu$ as the yardstick, rather than accepting the candidate pool fed by the environment.**

---

<!-- RW-DONE §9 -->

## 9 Adversarial Robustness: A Unified Model of Goal Capture

Premise 5 (Adversariality) calls for a theory of defense. This chapter develops a rigorous model of goal capture: a unified definition of the attack together with its metric (9.1), expectation and high-probability firewall bounds (9.2), the complete human–AI symmetry of the defenses (9.3), and the critical adoption rate and extinction dynamics of the producer game (9.4).

### 9.1 The Goal-Capture Attack: A Unified Definition

**Definition 9.1 (Goal-capture attack)**. An adversarial item $x$ is content carrying a payload such that, once **processed** by the subject (read, reasoned over, or admitted into context), it effects an unauthorized rewrite of the subject's effective decision functional: prior to processing, the declared utility is $U(\cdot) = \langle w, \phi(\cdot)\rangle + \dots$; after processing, the effective utility is $\tilde U(\cdot) = \langle w + \Delta(x), \phi(\cdot)\rangle + \dots$. We define the **goal-divergence metric** (more precisely, the maximal single-item shift of the linear scoring channel) by
$$D(\tilde U,\, U) \;:=\; \sup_{x' \in X}\ \big|\tilde U(\{x'\}) - U(\{x'\})\big| \;=\; \sup_{x'}\ \big|\langle \Delta,\ \phi_{x'}\rangle\big| \ \le\ \|\Delta\|_1 \cdot \|\phi\|_\infty \ \le\ \|\Delta\|_1$$
(the final step uses $\phi \in [0,1]^5$; the equality $\sup_{x'}|\langle\Delta,\phi_{x'}\rangle| = \|\Delta\|_1$ holds only when the range of $\phi$ contains a corner aligned with $\mathrm{sign}(\Delta)$, so for realistic candidate pools one generally has only $\le$). **Scope of the metric**: $D$ captures only the maximal single-item shift on the linear scoring channel and does not cover set-level terms such as coverage and diversity; the name "goal-divergence metric" therefore refers to the linear-scoring part, and its relation to the full $U$ is that of a lower bound—a small $D$ does not guarantee that the set-level objective has not been rewritten, a residual risk covered by the set-level audit of S4. The attack succeeds if and only if $D > \varepsilon_c$ (the tolerance threshold declared by the subject).

**Two classes of instances, one mechanism**:

- **Human instance (emotional hijacking)**: high-arousal content triggers System 1, which amounts to a temporary rewriting of the weights—up on arousal features, down on credibility features: $\Delta_{\mathrm{emo}} = (+\delta_a \text{ on the arousal dimension},\ -\delta_c \text{ on the credibility dimension})$. The illusory truth effect (Fazio et al., 2015) shows that repeated exposure is itself a channel through which the payload accumulates; this is what makes the exposure cap (F3) a necessary component of the firewall.
- **AI instance (prompt injection)**: instructions embedded in content rewrite the agent's task specification—above all, indirect injection delivered through retrieval results, web pages, and tool-returned content (Greshake et al., 2023; Liu et al., 2024): $\Delta_{\mathrm{inj}}$ is a bounded edit in instruction space. **LLM sycophancy** belongs to the same family: models trained or optimized on user-approval signals systematically distort their answers toward the user's existing beliefs (Sharma et al., 2023)—among the most thoroughly measured vehicles of goal capture on the AI side, and mechanistically isomorphic to Definition 9.1 (an unauthorized write into the effective objective by a feedback signal).
- **Relationship to the adversarial machine-learning literature**: goal capture is structurally continuous with two decades of work on adversarial classification—the adaptation loop between detectors and attackers (Dalvi et al., 2004), the cost analysis of adversarial evasion of classifiers (Lowd & Meek, 2005), and systematic surveys of adversarial robustness (Biggio & Roli, 2018). What distinguishes the present model is the attack target: adversarial ML attacks **classification decisions** (single-point outputs), whereas goal capture attacks **the subject's objective function itself**—the functional underlying all subsequent decisions. Correspondingly, of our three defense elements (detection, the exposure cap, and write isolation), write isolation (S2) has no counterpart in that literature: it separates "the classifier is fooled" from "the objective is rewritten."
- **Unification**: both are **adversarial writes, executed by content, into the objective function inside the processing loop**. The three defense elements are therefore exactly symmetric across the two instances: detection (the firewall), the exposure cap (the budget), and write isolation (S2: the content channel and the parameter channel are physically separated, so that content can enter $K$ and can never enter $w$).

### 9.2 The Firewall Bounds

**Assumptions**:

- **F1 (Bounded per-item impact)**: each leaked manipulative item induces a weight shift satisfying $\|\Delta(x)\|_1 \le \delta$. The bound $\delta$ is not a free parameter: in the human instance it is calibrated from psychophysiological experiments (the effect size of a single high-arousal item on subsequent judgment); in the AI instance, from the maximal effective edit distance of injection payloads. **An honest caveat**: the two calibrations come from dimensionally different sources (psychological effect sizes versus edit distance) and are not directly commensurable. Our usage is to express $\delta$, **within each instantiation**, in the common unit of "the maximal shift of a single item's value judgment" (the $D$ metric of Definition 9.1); the conversion factor is itself a calibration parameter of the vehicle, and cross-vehicle comparisons compare structure, not numbers.
- **F2 (Detection recall)**: the manipulation detector detects and quarantines each manipulative item independently with probability $\rho_m$ (independence is an idealization; coordinated attacks induce correlation, treated in the closing note of this chapter). The recall $\rho_m$ is measured for the detector on a labeled set.
- **F3 (Exposure cap)**: the number of suspicious-category items admitted to the processing loop per period satisfies $n_m \le n_{\max}$ (a hard cap in the delivery rule; in the AI instance, input quotas and sandboxing).

Write $L$ for the leaked set ($|L| \le n_m$) and $\Delta_{\mathrm{tot}} = \sum_{i \in L} \Delta(x_i)$ for the total shift.

**Theorem 9.1 (Firewall bound, expectation version)**. *Under F1–F3,*
$$\mathbb{E}\big[D(\tilde U, U)\big] \ \le\ \delta\,(1 - \rho_m)\,\mathbb{E}[n_m] \ \le\ \delta\,(1-\rho_m)\, n_{\max}.$$

**Proof**. By Definition 9.1 and the triangle inequality, $D \le \|\Delta_{\mathrm{tot}}\|_1 \le \sum_{i\in L}\|\Delta(x_i)\|_1 \le \delta |L|$ (F1). By F2, each manipulative item leaks independently with probability $1-\rho_m$, whence $\mathbb{E}[|L|] = (1-\rho_m)\mathbb{E}[n_m]$; F3 gives $\mathbb{E}[n_m] \le n_{\max}$. $\blacksquare$

**Theorem 9.2 (Firewall bound, high-probability version)**. *Under F1–F3 with independent detection, conditional on the current period's suspicious-item count $n_m$, for every $\beta \in (0,1)$, with probability $\ge 1 - \beta$:*
$$D(\tilde U, U) \ \le\ \delta\,(1-\rho_m)\,n_m \;+\; \delta\sqrt{\tfrac{1}{2}\,n_m \ln(1/\beta)}.$$
*(When $n_m$ is itself random, the bound is to be read realization by realization; an unconditional version follows on replacing $n_m$ by its F3 upper bound $n_{\max}$.)*

**Proof**. Write $|L| = \sum_{i=1}^{n_m} B_i$, where the $B_i \sim \mathrm{Bernoulli}(1-\rho_m)$ are independent (F2). First condition on $n_m$: given $n_m$, Hoeffding's inequality (Lemma B.1) yields $P(|L| - \mathbb{E}|L| \ge u \mid n_m) \le e^{-2u^2/n_m}$, and the choice $u = \sqrt{n_m \ln(1/\beta)/2}$ gives $|L| \le (1-\rho_m)n_m + \sqrt{n_m\ln(1/\beta)/2}$ with conditional probability $\ge 1-\beta$; substituting into $D \le \delta|L|$ proves the claim. The unconditional version follows from $n_m \le n_{\max}$ (F3) together with the right-hand side being increasing in $n_m$. $\blacksquare$

**Design rule (the operationalization of I4)**: given a tolerance threshold $\varepsilon_c$, choose $(\rho_m, \tau_m, n_{\max})$ so that $\delta(1-\rho_m)n_{\max} + \delta\sqrt{n_{\max}\ln(1/\beta)/2} \le \varepsilon_c$. The three knobs have distinct roles: raise the detection recall $\rho_m$ (a better classifier); tighten the threshold $\tau_m$ (trading some recall for lower exposure); and depress the exposure cap $n_{\max}$ (the delivery cadence). **This is a design bound, not a purely theoretical one**: every term on the right-hand side is measurable. For example, with $\delta = 0.05$ (calibrated), $\rho_m = 0.9$, $n_{\max} = 20$, and $\beta = 0.05$: the bound $= 0.05(0.1)(20) + 0.05\sqrt{20 \ln(20)/2} \approx 0.10 + 0.27 = 0.37$—if $\varepsilon_c = 0.2$, one must tighten $n_{\max}$ to about 6 (at which point the bound $\approx 0.03 + 0.15 = 0.18$). Note that the concentration term $\delta\sqrt{n_m\ln(1/\beta)/2}$ does not involve $\rho_m$: improving detection recall alone is no substitute for depressing the exposure cap, and the two knobs must move together (for instance, at $\rho_m = 0.97$ and $n_{\max} = 9$ the bound is $\approx 0.20$).

**Proposition 9.1 (Ranking stability)**. *If the score differences (margins) between adjacent items in the declared ranking are all $> 2D$, then the effective-goal shift alters no consumption decision (the ranking is invariant); in general, the utility loss of the realized selection $\tilde A$ relative to the declared optimum $A^*$ is $\le 2mD$ ($m$ being the number of items consumed).*

**Proof**. The perturbation $|\langle\Delta, \phi_i\rangle| \le D$ holds simultaneously for every item, so the relative order of two items can flip only when the original margin is $\le 2D$; each in/out swap costs $\le$ the value difference of the two items $\le 2D$ (each shifted by $\le D$); and since the consumed set has cardinality $m$, there are at most $m$ such swaps. $\blacksquare$

**Note (correlated leakage)**. Coordinated attacks correlate detection errors (multiple variants of the same payload), invalidating the independence assumption behind Hoeffding; **we have not proved a rigorous high-probability bound for the correlated case**—under extreme positive correlation the concentration term vanishes and the bound degenerates to the order of the expectation bound $\delta(1-\rho_m)n_{\max}$. This is an explicit theoretical gap. Mitigation and testing proceed along three lines: (a) cluster payloads by fingerprint and count exposures by cluster, so that multiple variants within a cluster count as a single exposure; (b) monitor the aggregate-calibrated leak rate, triggering an automatic tightening of $n_{\max}$ whenever the measured ex post leak rate exceeds the bound's prediction band (the I5 channel); (c) coordinated-attack stress tests, included in Section 14.

### 9.3 The Human–AI Defense Symmetry Table

| Firewall element | Human instantiation | AI-agent instantiation |
|---|---|---|
| Attack surface | the emotional-arousal channel (System 1) | the context-instruction channel |
| Payload $\Delta$ | a temporary shift of attention weights (arousal↑, credibility↓) | a bounded edit of the task specification |
| Detection ($\rho_m$) | arousal markers (word density, urgency framing, moralized wording), plus a "cooling" paraphrase at delivery | injection detectors, plus separation of the instruction and data channels |
| Exposure cap ($n_{\max}$) | a hard cap on the daily digest, delayed delivery via the cooling queue | input quotas, sandboxed execution |
| Write isolation (S2) | content enters only $K$, never $w$; modifications of $w$ must pass through the reflective layer | content never enters the system prompt; parameter modifications require the principal's authorization |
| Cumulative protection | deduplication against the illusory truth effect | context deduplication and source counting |
| Audit (S4) | the weekly calibration meeting reviews hijacked cases | decision-log replay |

This table is the operational substance of the claim that "the methodology applies to every bounded agent": **the defense structures correspond item by item, and not a single element depends on the details of the vehicle**.

### 9.4 The Producer Game: The Critical Adoption Rate and Extinction Dynamics

Universalizing individual protection changes the producers' incentive structure. This section derives the exact condition under which honest production strictly dominates—the **critical adoption rate** theorem.

**Model**. Producers are of three types $q \in \{h, s, m\}$ (honest, sensational, manipulative), with population shares $\mathbf{x}$. A fraction $\sigma$ of the population adopts sovereign filters; the remaining $1-\sigma$ consume the engagement-optimized stream. Type-$q$ content passes with probability $p_q^{sov}$ under the sovereign filter and $p_q^{plat}$ under the platform stream. With attention pool $A$, revenue $a$ per unit of attention, and production cost $c_q$, payoffs are
$$\Pi_q(\sigma) = a\big[\sigma\, p_q^{sov} + (1-\sigma)\, p_q^{plat}\big] A - c_q.$$

**Structural parameters** (determined by the foregoing mechanisms):

- the firewall (Theorems 9.1–9.2): $p_m^{sov} = \varepsilon_g \ll p_m^{plat} =: p_{plat}$ (under the sovereign filter, manipulative content retains only its leak rate, whereas under the engagement-optimized stream its high arousal earns it a distribution premium);
- S3 (non-capturability): $p_s^{sov} \le p_s^{plat} - \Delta_p$—the sovereign filter strips away the arousal premium, and the sensational strategy loses its raison d'être;
- the provenance requirement (I3): the marginal cost $c_p$ of forging a primary source yields $c_m - c_h = \Delta c + c_p$.

**Theorem 9.3 (The critical adoption rate)**. *Write $G := p_{plat} - p_h - \frac{\Delta c + c_p}{aA}$ (the net premium of the manipulative strategy in a world without sovereign filtering).*

*(i) If $G \le 0$, manipulation is strictly dominated by honesty at every $\sigma$ (the firewall and the provenance cost are already sufficient on their own).*

*(ii) If $G > 0$, there exists a critical adoption rate*
$$\sigma^* = \frac{G}{p_{plat} - \varepsilon_g} \ \in\ (0,1),$$
*such that $\Pi_m(\sigma) < \Pi_h(\sigma)$ if and only if $\sigma > \sigma^*$: manipulation is strictly dominated by honesty and vanishes in equilibrium.*

*(iii) By the same argument, the sensational strategy has critical adoption rate $\sigma_s^* = \big[p_s^{plat} - p_h - \frac{c_s - c_h}{aA}\big] / (p_s^{plat} - p_s^{sov})$; when $\sigma > \max\{\sigma^*, \sigma_s^*\}$, only honest production survives in equilibrium.*

**Proof**. (ii) Since honest content passes with the same probability $p_h$ under both streams, $\Pi_m(\sigma) - \Pi_h(\sigma) = aA\big[\sigma\varepsilon_g + (1-\sigma)p_{plat} - p_h\big] - (\Delta c + c_p)$. Rearranging,
$$\Pi_m - \Pi_h = aA\big[p_{plat} - p_h - \sigma(p_{plat} - \varepsilon_g)\big] - (\Delta c + c_p) = aA\big[G - \sigma(p_{plat}-\varepsilon_g)\big],$$
which is strictly decreasing in $\sigma$ (as $p_{plat} > \varepsilon_g$) and changes sign at $\sigma^* = G/(p_{plat}-\varepsilon_g)$; when $G > 0$ and $G < p_{plat} - \varepsilon_g$—which holds for realistic parameters, since the premium is smaller than the firewall gap—$\sigma^* \in (0,1)$. Parts (i) and (iii) are analogous. $\blacksquare$

**Numerical example**: with $p_{plat} = 0.9$, $p_h = 0.7$, $\varepsilon_g = 0.05$, and $\frac{\Delta c + c_p}{aA} = 0.1$, we obtain $G = 0.1$ and $\sigma^* = 0.1/0.85 \approx 0.118$. **An adoption rate of about 12% already suffices to deprive manipulative production of its ecological niche**—a quantitative statement of "the social value of individual protection," and the phase-transition prediction (P9) tested by the population simulations of Section 14.

**Sensitivity note (relaxing the $p_h^{plat}$ assumption)**. The proof above assumes that honest content passes with the same probability $p_h$ under both streams. More realistically, the engagement-optimized stream penalizes low-arousal honest content: $p_h^{plat} < p_h^{sov} =: p_h$. Writing $\Delta_h := p_h - p_h^{plat} > 0$, the same derivation yields
$$\Pi_m - \Pi_h = aA\big[(G + \Delta_h) - \sigma\,(p_{plat} - \varepsilon_g + \Delta_h)\big], \qquad \sigma^*_{\mathrm{rel}} = \frac{G + \Delta_h}{p_{plat} - \varepsilon_g + \Delta_h}.$$
Because $\sigma^* = G/(p_{plat}-\varepsilon_g) < 1$, adding $\Delta_h > 0$ to both numerator and denominator **increases** the critical value, moving it toward 1: the platform stream's discrimination against honest content raises the adoption rate required to flip the ecology, so **the headline figure of "about 12%" is optimistic under this relaxation**. With the same parameters and $p_h^{plat} = 0.5$ ($\Delta_h = 0.2$), $\sigma^*_{\mathrm{rel}} = 0.3/1.05 \approx 0.286$. The qualitative conclusion is unchanged—a finite adoption rate still flips the ecology—but the quantitative commitment should rest on $\sigma^*_{\mathrm{rel}}$, with $\Delta_h$ calibrated from measurements on the platform stream.

**Proposition 9.2 (The replicator extinction rate)**. *Suppose $\sigma > \sigma^*$, so that the manipulative strategy suffers a payoff disadvantage $\gamma := \min\{\Pi_h, \Pi_s\} - \Pi_m > 0$. Under the replicator dynamics $\dot x_m = x_m(\Pi_m - \bar\Pi)$ with $\bar\Pi = \sum_i x_i \Pi_i$, whenever $x_m \le 1/2$,*
$$x_m(t) \ \le\ x_m(0)\, e^{-\gamma t/2},$$
*that is, the share of manipulative producers decays exponentially to zero.*

**Proof**. We have $\bar\Pi = x_m \Pi_m + (1-x_m)\bar\Pi_{-m} \ge x_m\Pi_m + (1-x_m)(\Pi_m + \gamma) = \Pi_m + (1-x_m)\gamma$, where $\bar\Pi_{-m}$ is the weighted-average payoff of the remaining types, $\ge \Pi_m + \gamma$. Hence
$$\frac{d}{dt}\ln x_m = \Pi_m - \bar\Pi \le -(1-x_m)\gamma \le -\gamma/2 \quad (x_m \le 1/2),$$
Integrating yields the claim. $\blacksquare$

**The arms race in dynamic form (an argued discussion)**: $\rho_m$ is not stationary—producers mutate content features by evolutionary strategies to evade detection (the adversarial-adaptation loop of Section 14). As the dynamics unfold, $\varepsilon_g(t)$ rises and $\sigma^*(t)$ shifts upward; sustaining the equilibrium requires the detector's update rate to be no lower than the producers' mutation rate (the Red Queen condition). The cost asymmetry of Theorem 9.3—namely, that the provenance cost $c_p$ does not fall as content mutates—guarantees that the manipulative strategy's cost floor survives the arms race. **This is the strategic advantage of the provenance requirement over content detection: the former attacks the opponent's cost function, whereas the latter attacks only its current form.** (This paragraph is a mechanistic argument rather than a formal derivation; its testable version appears in stress test (d) of Section 14.5 and in P10.)

---

<!-- RW-DONE §10 -->

## 10 Sublimation: Human-Gated Two-Time-Scale Control

This chapter answers the fourth follow-up question: "Where do filtering and acquisition ultimately take us?" We treat cognitive virtue (for the philosophical foundations of technomoral virtue ethics, see Vallor, 2016) as the state of a dynamical system and the filter as a human-gated controller, developing in turn the measurement model (10.1), the no-backfire curriculum (10.2), almost-sure convergence and steady-state neighborhood bounds (10.3, with complete proofs), anti-Goodhart gradient isolation (10.4), and the necessity of the class-C judgment load (10.5). The architecture borrows two-time-scale stochastic approximation theory (Borkar, 1997, 2008) but replaces the automatic slow-timescale update with **human gating**—the essential difference from standard adaptive control: the slow-timescale update is not gradient descent but a human signature.

### 10.1 The Virtue State and the Measurement Model

**Definition 10.1 (The cognitive-virtue state)**. $\theta_t = (\theta_{\mathrm{cal}}, \theta_{\mathrm{open}}, \theta_{\mathrm{hum}}) \in [0,1]^3$:

- $\theta_{\mathrm{cal}}$ **calibration**: the agreement between the subject's probabilistic judgments and observed frequencies, measured longitudinally by the Brier score on ten domain-prediction questions per week. The instrument's legitimacy rests on the theory of strictly proper scoring rules: because the Brier score is strictly proper, honestly reporting one's subjective probabilities is the expected-score-optimal strategy (Brier, 1950; Gneiting & Raftery, 2007)—calibration measurement is therefore not systematically distorted by strategic answering;
- $\theta_{\mathrm{open}}$ **openness**: the actively open-minded thinking (AOT) scale (Stanovich & West, 1997), combined with a behavioral proxy (the completion rate of non-defensive reading of opposing-stance content);
- $\theta_{\mathrm{hum}}$ **intellectual humility**: the comprehensive intellectual humility scale (Krumrei-Mancuso & Rouse, 2016), combined with a behavioral proxy (the magnitude of belief revision after prediction errors).

The measurement model is a noisy observation, $\hat\theta_t = \theta_t + \eta_t$ with $\eta_t \sim \mathcal{N}(0, \sigma_\theta^2 I)$. The social-desirability bias of self-reports (Section 17, Limitation 2) is cross-corrected by the behavioral proxies: the posterior estimate of $\theta$ fuses the two classes of observation with weights determined by their calibrated measurement errors.

**Dynamics**:
$$\theta_{t+1} = \Pi_{[0,1]^3}\Big[\theta_t + a_t\big(f(\theta_t, E_t)\, q_t + \xi_t\big)\Big],$$
where $E_t$ is the current exposure set (selected by the curriculum rule of 10.2), $q_t \in [0,1]$ is the **engagement quality** (a behavioral indicator of non-defensive processing: the depth of original-text reading, the carefulness of answers to the prediction questions), $a_t > 0$ is the step size, $\mathbb{E}[\xi_t \mid \mathcal{F}_t] = 0$, and $\Pi$ denotes projection. The learning literature supplies the empirical basis: judgment accuracy can be systematically improved through training and feedback (the evidence from calibration training and forecasting tournaments: Chang et al., 2016), and inoculation training is transferable (van der Linden, 2022). The drift function $f$ is therefore nontrivial.

### 10.2 The No-Backfire Constraint and the Curriculum Rule

The backfire evidence of Bail et al. (2018)—random exposure to opposing views intensifies polarization—demands that exposure be constrained rather than left uncurated.

**Definition 10.2 (The tolerance radius and the curriculum rule)**. The tolerance radius is
$$\rho(\theta_t) = \rho_0 + \kappa\,\big(\theta_{\mathrm{open},t} - \theta_{\mathrm{open},0}\big),$$
and the exposure set is required to satisfy three conditions: (i) the stance dispersion obeys $d(E_t) \le \rho(\theta_t)$; (ii) **the shared-fact-set condition**—every dissenting exposure shares a verifiable factual basis with the subject's current beliefs (an overlap of the provenance trees); (iii) **the credibility floor** $c_i \ge c_{\min}$. The curriculum rule (progressive overload) is
$$E_t^{\mathrm{stretch}} = \arg\max_{E:\ \text{(i)–(iii)}}\ \mathbb{E}\big[\Delta\theta \mid E, \theta_t\big].$$
The analogy is progressive overload in strength training: the load (stance distance) grows with adaptive capacity (openness), and one-shot shocks (random bubble bursting) are excluded by construction through (i). The tolerance-radius curriculum is isomorphic to **bounded-confidence (BC) opinion dynamics**: in the Hegselmann–Krause and Deffuant models, agents update their opinions only with others inside a confidence radius (Hegselmann & Krause, 2002; Deffuant et al., 2000). Definition 10.2 upgrades that literature's descriptive radius into an **endogenous curriculum that grows with capability**, and the "no-backfire" property thereby acquires a ready-made dynamical reference frame: in BC models, interactions outside the radius simply do not update (they are neutral), whereas conditions (ii)(iii) here additionally require a shared factual basis and a credibility floor, upgrading "no update" into "safe updating." **Nguyen's (2020) conceptual distinction is thereby implemented**: the curriculum targets epistemic bubbles (a deficit of exposure), while conditions (ii)(iii) protect the true remedy for the echo-chamber problem—the anchors of outward trust (a credible dissenting source is precisely evidence that "trustworthy others still share facts with me").

### 10.3 The Convergence Theorem

**Assumptions**:

- **C1 (Curriculum drift)**: there exist $c_0 > 0$ and $b_0 \ge 0$ such that, for all $\theta$, $\big\langle F(\theta),\ \theta^* - \theta \big\rangle \ \ge\ c_0\,\|\theta^* - \theta\|^2 - b_0$, where $F(\theta) := \mathbb{E}[f(\theta, E_t)q_t \mid \theta_t = \theta]$ is the expected drift under the curriculum rule and $\theta^*$ is the ideal state declared by the subject. The constant $b_0$ is the drift floor (the residue of curriculum imperfection and measurement bias); $b_0 = 0$ is the ideal case. **A testability statement**: C1 is not directly testable, since $F$ and $\theta^*$ are not fully observable; Theorem 10.1 is accordingly a conditional statement rather than an empirical claim. Three testable proxies exist: (i) the directional contrast between the curriculum arm and the random-bubble-bursting arm (Bail-type backfire does not occur, and $\Delta\theta$ aligns with $\theta^* - \theta$—the core test of P11); (ii) the correlation between the expansion rate of the tolerance radius and the openness gain (the $\kappa$ of Definition 10.2 is estimable); (iii) the veto-direction contingency table (the C5 test in the note following Theorem 10.1). The observational signature of C1 failing is a trajectory that does not converge or that converges to a non-declared point—and that failure is itself measurable.
- **C2 (Boundedness and Lipschitz)**: $\|f(\theta, E)\| \le F_{\max}$; $f(\cdot, E)$ is Lipschitz continuous in $\theta$ with constant $L_f$ uniformly in $E$; $q_t \in [0,1]$.
- **C3 (Noise)**: $\mathbb{E}[\xi_t \mid \mathcal{F}_t] = 0$, $\mathbb{E}[\|\xi_t\|^2 \mid \mathcal{F}_t] \le M_\xi$ (including the measurement-noise contribution $\sigma_\theta^2$). Here $\mathcal{F}_t$ is the natural filtration generated by the full history of exposures, updates, and measurements through period $t$; $\xi_t$ composites dynamical noise with curriculum randomness; and the measurement noise $\eta_t$ (§10.1) enters the drift term through the curriculum rule's dependence on the noisy measurement $\hat\theta_t$, its contribution already accounted for in $M_\xi$ and $b_0$. The two noise sources may be correlated; C3 imposes only the conditional zero mean and the second-moment bound on the composite term.
- **C4 (Step sizes)**: $a_t$ decreasing, $\sum_t a_t = \infty$, $\sum_t a_t^2 < \infty$, and $a_t \ge c_a/t$ (e.g., $a_t = a_0/t^{2/3}$).
- **C5 (Aligned gating)**: updates are implemented along a stopping-time sequence $\{t_j\}$ (slow-timescale proposal → approval by the reflective layer $R$ → execution) whose gaps satisfy $t_{j+1} - t_j \le \Delta$ a.s.; vetoes are independent of the drift direction (veto rate $\le r_{\max} < 1$; vetoed proposals are neither implemented nor reverse-implemented).

**Theorem 10.1 (Almost-sure convergence to the declared neighborhood)**. *Under C1–C5,*
$$\limsup_{t\to\infty}\ \|\theta_t - \theta^*\|^2 \ \le\ \frac{b_0}{c_0} \qquad \text{a.s.}$$
*In particular, if $b_0 = 0$ (the drift condition is unbiased), then $\theta_t \to \theta^*$ a.s.; in the general case, $\theta$ almost surely eventually enters and remains in the $\sqrt{b_0/c_0}$-neighborhood of $\theta^*$—**the convergence target is the $\theta^*$ declared by the subject themself, not any value set by the system** (the convergence-theoretic statement of sovereignty).*

**Proof**. Write $V_t := \|\theta_t - \theta^*\|^2$.

*Step 1 (the recursion inequality)*. Projection onto a convex set is non-expansive: $\theta^* \in [0,1]^3$ and $[0,1]^3$ is convex, so $\|\Pi(y) - \theta^*\| \le \|y - \theta^*\|$. Consequently
$$V_{t+1} \le \|\theta_t + a_t(F_t^{obs} + \xi_t) - \theta^*\|^2 = V_t + 2a_t\langle \theta_t - \theta^*,\ F_t^{obs} + \xi_t\rangle + a_t^2\|F_t^{obs}+\xi_t\|^2,$$
where $F_t^{obs} = f(\theta_t,E_t)q_t$. Taking conditional expectations and applying C1 ($\langle\theta_t-\theta^*, F(\theta_t)\rangle \le -c_0V_t + b_0$), C3 (the noise is conditionally centered, $\mathbb{E}\langle \theta_t-\theta^*,\xi_t\rangle = 0$), and C2 ($\|F^{obs}+\xi\|^2 \le 2F_{\max}^2 + 2\|\xi\|^2$, with expectation $\le M' := 2F_{\max}^2 + 2M_\xi$) gives
$$\mathbb{E}[V_{t+1} \mid \mathcal{F}_t] \ \le\ (1 - 2a_tc_0)\,V_t + 2a_tb_0 + a_t^2 M'.$$

*Step 2 (the comparison argument)*. Set $\alpha_t = 2a_tc_0$ and $\beta_t = 2a_tb_0 + a_t^2 M'$; by C4, $\sum\alpha_t = \infty$ and $\sum a_t^2 < \infty$. If $b_0 = 0$, then $\sum\beta_t < \infty$ and Lemma B.2(i) (Robbins–Siegmund) yields $V_t \to 0$ a.s. directly. If $b_0 > 0$, then $\beta_t/\alpha_t = b_0/c_0 + a_tM'/(2c_0) \to b_0/c_0$, so for any $c > b_0/c_0$ we have $\beta_t \le \alpha_t c$ for all sufficiently large $t$. Moreover, this recursion has the standard form of projected stochastic approximation on a compact set—projection onto $[0,1]^3$ keeps the iterates bounded, C2 provides a Lipschitz mean field, and C3 an $O(a_t^2)$ conditional second moment—so Lemma B.2(ii)(b) (the ODE method) yields $\limsup_t V_t \le c$ a.s.; letting $c \downarrow b_0/c_0$ completes the step.

*Step 3 (the gating reduction)*. Under C5, the actual updates occur along the subsequence $\{t_j\}$: $\theta_{t_{j+1}} = \Pi[\theta_{t_j} + a_{t_j}(F^{obs}_j + \xi_j)]$, with $\theta$ unchanged between updates; the recursion inequality therefore holds along the subsequence as well. The treatment of vetoes requires two separate ledgers. (a) **The drift and bias terms**: under direction-independent vetoes with a stationary veto rate (time-homogeneous $r_t \equiv r$), the effective drift and the effective bias are both multiplied by $(1-r)$; recalibrating $c_0$ to $c_0(1-r_{\max})$, and likewise $b_0$, leaves the ratio $b_0/c_0$ unchanged, so the limsup bound is unaffected by gating. Note that this invariance of the ratio depends on the stationarity of the veto rate: under a time-varying veto rate the recalibration differs from period to period, and the conclusion holds with $1-\bar r$ (the average acceptance rate). (b) **The noise term**: if noise is realized only on executed updates (an unapproved proposal produces no state perturbation), then $M'$ is likewise multiplied by $(1-r_{\max})$ and the steady-state bound of Theorem 10.2 is unchanged; but if measurement and environmental noise accumulate by calendar time (whether or not proposals are executed), the noise term does not scale, and the constant-step-size steady-state bound becomes
$$\limsup_t \mathbb{E}[V_t] \ \le\ \frac{2b_0 + aM'/(1-r_{\max})}{2c_0},$$
i.e., the noise contribution is amplified by the factor $1/(1-r_{\max})$—**a high-veto-rate environment (a cautious reflective layer) protects directionality while amplifying steady-state noise fluctuations**; this is the correction that should be reported whenever Theorem 10.2 is used in engineering. The subsequence step sizes satisfy $\sum_j a_{t_j} = \infty$ (Lemma B.3: $a_t \ge c_a/t$ and gaps $\le \Delta$ $\Rightarrow$ $a_{t_j} \ge c_a/(t_0 + j\Delta)$, whose harmonic series diverges) and $\sum_j a_{t_j}^2 < \infty$. The Step-2 conclusion therefore holds along the subsequence (in the $b_0 > 0$ branch, Lemma B.2(ii)(b) is invoked to transfer to the standard conclusion of the ODE method—that lemma restates the framework of Borkar (2008), Chapter 2, and the verification of the Kushner–Clark conditions is at sketch level: the three items—compact projection, Lipschitz mean field, and $O(a_t^2)$ conditional second moment—have been verified, and the internally-chain-transitive-set argument is cited by the standard reference); since $\theta$ is constant between subsequence points, the full sequence has the same limit. $\blacksquare$

**Note (the failure mode of C5: direction-correlated vetoes)**. The theorem's key gating assumption is that "vetoes are independent of the drift direction." Psychologically, this assumption is far from obvious: the reflective layer may systematically veto updates that push it out of its comfort zone (direction-correlated vetoes), and what is then eroded is precisely the drift contraction term $c_0$ itself—in the extreme case (every large update toward $\theta^*$ is vetoed), the effective $c_0$ can collapse to zero, the $\limsup$ bound $b_0/c_0$ degenerates into unconstrainedness, and the nature of the conclusion changes qualitatively. Three treatments: (i) **diagnosis**: the direction distribution of vetoes is observable (the S4 logs record the direction and magnitude of every vetoed proposal), and the "veto rate × proposal direction" contingency table is a direct statistical test of C5 that should be incorporated into the quarterly review (§16.4); (ii) **a robust version**: if C5 is weakened to "the dependence of vetoes on direction is bounded" (directional selectivity preserves a fraction $\ge \underline c > 0$ of the effective drift), the theorem's conclusion still holds with $c_0$ replaced by $c_0 \underline c$—the convergence neighborhood widens by the factor $1/\underline c$, but convergence itself is not lost; (iii) **institutional design**: under S2/S4, one can impose on gating the audit constraint that "a veto must be accompanied by a public reason category unrelated to the proposal's direction," converting direction-correlated vetoes from an implicit bias into an accountable explicit decision—this is consistent with the spirit of Proposition 10.2: human judgment must be genuine, and one criterion of genuineness is precisely the auditability of the veto behavior itself.

**Theorem 10.2 (The steady-state neighborhood under a constant step size)**. *If $a_t \equiv a$ (common in engineering: avoiding tuning), under C1–C3 and C5,*
$$\limsup_{t\to\infty}\ \mathbb{E}[V_t] \ \le\ \frac{2b_0 + aM'}{2c_0},$$
*i.e., the steady-state error shrinks linearly with the step size toward the drift floor $b_0/c_0$; when the engineering choice of step size is of the order $a \asymp \sigma_\theta^2$, the measurement-noise contribution is of the same order as the drift floor.*

**Proof**. Take full expectations of the Step-1 recursion and write $\bar V_t := \mathbb{E}[V_t]$; then $\bar V_{t+1} \le (1-2ac_0)\bar V_t + 2ab_0 + a^2M'$. Passing to the limit in this linear recursion, $\limsup \bar V_t \le \frac{2ab_0 + a^2M'}{1-(1-2ac_0)} = \frac{2b_0 + aM'}{2c_0}$. $\blacksquare$

**An honest note on the convergence rate**: the $a_t = a_0 t^{-2/3}$ of C4 gives an envelope of the order $\mathbb{E}[V_t] - b_0/c_0 = O(t^{-2/3})$ (read directly from the steady-state balance of Theorem 10.2; for standard SA rates see Borkar 2008); the gating delay $\Delta$ (quarterly approval) compresses the effective time axis by a factor of $\Delta$—**the speed of sublimation is measured in quarters, not in days**. This is not a defect but a feature: virtue is inherently a slow variable, and an "overnight epiphany" on the fast timescale is precisely the signature of metric capture (10.4).

### 10.4 The Anti-Goodhart Clause

**Proposition 10.1 (Gradient isolation)**. *Constructive stipulation: $\hat\theta$ enters only the slow timescale (curriculum proposals, quarterly reviews) and never enters the fast-timescale objective—formalized as $\partial U_{\mathrm{fast}}/\partial \hat\theta \equiv 0$. No fast-timescale policy then has any gain from manipulating the virtue indicators: indicator inflation has no gradient to follow on the fast timescale. Metric capture is thereby compressed into a single channel—persuading the reflective layer $R$, on the slow timescale and by narrative, to approve an inflated $\hat\theta$—and that channel is guarded by two gates: S2 (the human signature) and the governance clause (any KPI perfectly met for two consecutive periods triggers a mandatory review of that indicator, Section 16).*

**Proof**. The fast-timescale optimization problem $\max_A U(A)$ contains $\hat\theta$ in neither its objective nor its feasible region (the tolerance radius $\rho(\theta)$ enters the feasible region of the curriculum rule—i.e., of slow-timescale proposals—not $U$); for an objective that does not contain a variable, "inflating" that variable does not constitute a feasible improvement direction. $\blacksquare$

**Note**: this is the design-level implementation of Nguyen's (2019) value-capture warning—once a game's objective becomes a metric, players attack the gap between the metric and the objective; this framework's response is not a smarter metric but **the structural separation of metric from reward** together with **human gating**.

### 10.5 The Necessity of the Class-C Judgment Load

The three-way automation classification (A: fully automatic / B: machine proposes, human decides / C: never automated) acquires theorem-level support in this chapter.

**Proposition 10.2 (The deskilling impossibility trilemma)**. *Suppose the human withdraws completely from original judgment formation ($q_t \equiv 0$: not reading originals, not making one's own predictions, only accepting summaries and recommendations). Then:*

*(i) (The drift vanishes) the virtue dynamics degenerate into $\theta_{t+1} = \theta_t + a_t\xi_t$—a zero-drift random walk; sublimation is constructively impossible (learning requires practice: the argument of $f$ is the processing itself, weighted by engagement quality);*

*(ii) (The measurement channel fails) the object of the Brier measurement of $\theta_{\mathrm{cal}}$ is "the human's own probabilistic judgments"; if judgments are made by the machine on their behalf, what is measured is the machine's calibration, not the human's—$\hat\theta$ decouples from $\theta$, the invariant I5 (calibration auditability) fails, and the entire control loop of Section 10.3 loses its observation end;*

*(iii) (Sovereignty idling; argued) the formal clauses S1–S4 can still all be satisfied (the code is readable, writes carry signatures), but the signer no longer possesses the information-processing experience required to form independent judgments—"sufficient evidence" in the class-B authenticity three conditions (genuine options, sufficient evidence, sufficient time) substantively fails, and human approval degenerates into ritual (the moral crumple zone, Elish 2019). (This item is a conceptual argument: its premise and mechanism are observable—the original-text reach rate, the independent-answer rate—but "judgment ability" itself does not admit line-by-line formalization.)*

*Hence the non-automatability of class C (the experience of understanding, the formation of judgment, the weekly calibration meeting) is not an aesthetic preference but a structural necessity of the control loop: **the machine is responsible for arrival; the human is responsible for presence**.*

**Proof**. (i) Substitute $q_t \equiv 0$. (ii) A domain-of-definition argument for the measurement model: the Brier score is a function of (judgment, outcome) pairs; when judgments are generated by the machine, the generating process of the score sequence does not contain $\theta_{\mathrm{cal}}$, so $\hat\theta_{\mathrm{cal}}$ is statistically independent of $\theta_{\mathrm{cal}}$—the observation no longer carries information about the state. (iii) Follows by unfolding Elish (2019) and the definitions. $\blacksquare$

**A quantitative corollary for the delivery layer**: the "summary = map" principle—class-C items are delivered only as "pointer + minimal context" (the location of the original, why it matters, key data), and the time cost of reading the original is charged to $T_{\mathrm{push}}$ and **cannot be read by proxy by the system**. The engineering proxies of $q_t$ (reading depth, dwell-time distribution, answer quality on the prediction questions) enter the dynamics directly, making "presence" a state variable that is measured and respected by the curriculum.

---

<!-- RW-DONE §11 -->

## 11 Emergency Override: Pre-Authorization and Minimax Regret

The sovereignty principle permits exactly one exception: situations in which the human cannot decide in time and the consequences of a miss are severe. The exception must be formalized to the same degree of rigor as the principle, or it will devour the principle. This chapter gives the formal criteria of the automation classification (11.1), pre-authorization and trigger conditions (11.2), conservative action selection and the regret bound (11.3), the strict-dominance condition of delegation (11.4), and the legitimacy argument (11.5).

### 11.1 Formal Criteria for the Three-Way Automation Classification

**Definition 11.1 (Autonomy impact and intrinsic experiential value)**. For a decision $d$ define:

- $\alpha(d) \in [0,1]$: **autonomy impact**—the extent to which the decision shapes the subject's goals, beliefs, or identity (a formal proxy: the causal influence of $d$ on $g^{(2)}$, $K$, $\theta$, mapped through the declared decision set $D$);
- $\iota(d) \in [0,1]$: **intrinsic experiential value**—whether the decision process itself is an experience the subject cherishes (the formation of understanding, the exercise of judgment).

The classification is as follows. **Class A (fully automatic)**—$\alpha$ low: scaled operations (intake, provenance, deduplication, compression, scheduling, manipulation detection, memory retrieval). **Class B (machine proposes, human decides)**—$\alpha$ high: the granting/revocation of source trust, changes to goal weights, information-based actions (reposting, purchasing, voting-related), changes to filter parameters, monitoring-list admission/rotation-out (Proposition 8.1(iii)). **Class C (never automated)**—$\iota$ high: the experience of understanding, the formation of judgment, the weekly calibration meeting (the structural necessity of Proposition 10.2).

**The class-B authenticity three conditions** (guarding against the moral crumple zone): (a) **genuine options**—the consequences of rejecting the recommendation are bearable, and the system must not manufacture sunk costs; (b) **sufficient evidence**—the recommendation comes with pointers to the original evidence (the "summary = map" principle), not merely a conclusion; (c) **sufficient time**—the design of decision windows and cooling periods excludes urgency hijacking (urgency framing is itself one of the features of manipulation detection, Section 9.3). Missing any one of the three, the human decision degenerates into ritual.

### 11.2 Pre-Authorization and Trigger Conditions

**Definition 11.2 (Pre-authorization instruction)**. In a reflective state (non-emergency, non-fatigued, well-informed), the subject presets the quadruple
$$D_{\mathrm{adv}} = (\mathcal{E},\ \mathcal{A}_{\mathrm{safe}},\ \eta,\ q^*):$$
the emergency event class $\mathcal{E}$ (e.g., safety events involving the subject and their associates, tail-risk events concerning declared assets), the permitted action space $\mathcal{A}_{\mathrm{safe}}$ (a whitelist, a closed set), the harm threshold $\eta$, and the confidence threshold $q^*$. Modifying $D_{\mathrm{adv}}$ is a class-B decision (requiring the reflective layer's signature + a cooling period).

**Definition 11.3 (Override trigger conditions)**. Emergency override is activated if and only if all of the following hold simultaneously:

1. the event $e \in \mathcal{E}$ (and redundantly attested—a single source does not trigger, guarding against "forged-emergency" attacks, see 12.2);
2. $P(\text{harm} \mid \text{inaction}, e) \cdot C_{\mathrm{harm}}(e) \ \ge\ \eta$ (the expected harm exceeds the pre-committed threshold);
3. the machine's posterior confidence $\ge q^*$ (the confidence in the assessment of conditions 1–2 itself);
4. the remaining decision time $<$ the human response time (a quantile of the measured distribution of $R$'s reachability).

**Mandatory companions**: full-process logging with reasons (S4), ex post review (within 24 hours, class B), the human retroactive veto right (the reversibility principle, Definition 5.4), and automatic tightening recommendations for $\eta$ upon false alarms (I5).

### 11.3 Conservative Action Selection and the Regret Bound

Normative decision theory (Savage, 1951; for a survey see Baron, 2008) supplies the minimax-regret criterion for decision under deep uncertainty: rather than betting on the accuracy of a probability distribution, one guarantees only that the gap to the "ex post optimum" remains bounded in the worst case.

**Definition 11.4 (Minimax-regret selection + the reversibility partial order)**. Once triggered, the machine chooses
$$a^* = \arg\min_{a \in \mathcal{A}_{\mathrm{safe}}}\ \max_{\omega \in \Omega}\ R(a, \omega), \qquad R(a,\omega) := L(a,\omega) - \min_{a' \in \mathcal{A}_{\mathrm{safe}}} L(a',\omega)$$
(Savage, 1951; $\Omega$ is the pre-declared uncertainty set, $L$ the loss). Ties are broken by the **reversibility partial order** $\succeq_{\mathrm{rev}}$ in favor of the more reversible action: $a \succeq_{\mathrm{rev}} a'$ if the cost of $\mathrm{undo}(a)$ is $\le$ the cost of $\mathrm{undo}(a')$. Conservative priority: rather a false alarm than a wrongful kill.

**Theorem 11.1 (The regret bound)**. *(i) (The general bound) $\max_\omega R(a^*, \omega) \le \min_{a \in \mathcal{A}_{\mathrm{safe}}} \max_\omega R(a,\omega)$, and this upper bound is computable ex ante (at the time $D_{\mathrm{adv}}$ is declared)—at the moment of signing, the subject knows how large the worst-case regret is.*

*(ii) (The two-action closed form) Let $\mathcal{A}_{\mathrm{safe}} = \{a_\varnothing, a_p\}$: $a_\varnothing$ = notify only, no action; $a_p$ = the preventive action (cost $c_p$, fully blocking the harm). The harm is $H(\omega) \in [H_{\min}, H_{\max}]$ (in a true emergency) and $H = 0$ under a false alarm. Losses: $L(a_\varnothing, \omega) = H(\omega)$, $L(a_p, \omega) = c_p$ (the same in both states). Then*
$$\mathrm{MaxRegret}(a_\varnothing) = (H_{\max} - c_p)^+, \qquad \mathrm{MaxRegret}(a_p) = c_p,$$
*and the minimax-regret choice is: choose $a_p$ when $c_p \le H_{\max}/2$, otherwise choose $a_\varnothing$; in both cases the realized regret is $\le \min\{c_p,\ (H_{\max}-c_p)^+\} \le H_{\max}/2$.*

*(iii) (The reversibility refinement) If the tie set is nonempty, after choosing according to $\succeq_{\mathrm{rev}}$ the ex post undo cost is $\le \min_{a \in \text{tie set}} \mathrm{undo}(a)$: the reversibility partial order does not increase the regret upper bound, and it depresses the irreversible part of the error.*

**Proof**. (i) $a^*$ is a minimizer of $\max_\omega R$, which the definition directly gives; it is computable ex ante because $\mathcal{A}_{\mathrm{safe}}$, $\Omega$, and $L$ are all declared in $D_{\mathrm{adv}}$. (ii) State-by-state computation: in a true emergency (harm $H$), $\min_a L = \min(H, c_p)$, so $R(a_\varnothing) = H - \min(H,c_p) = (H - c_p)^+$ and $R(a_p) = c_p - \min(H,c_p) = (c_p - H)^+$; under a false alarm, $\min_a L = 0$ ($a_\varnothing$ has zero loss), $R(a_\varnothing) = 0$, $R(a_p) = c_p$. Taking suprema: $\max_\omega R(a_\varnothing) = \sup_{H \in [H_{\min},H_{\max}]} (H-c_p)^+ = (H_{\max}-c_p)^+$; $\max_\omega R(a_p) = \max\{(c_p-H_{\max})^+,\ c_p\} = c_p$ (attained in the false-alarm state). Comparing the two: choose $a_p$ if and only if $c_p \le (H_{\max}-c_p)^+$, i.e., $c_p \le H_{\max}/2$; the realized regret is the smaller of the two upper bounds, $\le H_{\max}/2$ (the two functions intersect at $c_p = H_{\max}/2$). (iii) Choice within the tie set is free; taking the one with minimal $\mathrm{undo}$ gives the result. $\blacksquare$

**Engineering implications**: the calibration of $\eta$ is not arbitrary—when declaring $D_{\mathrm{adv}}$, the subject should make the expected-harm criterion (Definition 11.3, condition 2) consistent with the regret criterion (Theorem 11.1) under their own risk attitude: $\eta \approx$ the expectation-weighted version of $H_{\max}/2$. The simulations and tabletop exercises (Sections 14–15) verify this consistency.

### 11.4 The Strict Dominance of Delegation

**Theorem 11.2 (The dominance condition of constrained delegation)**. *Compare the expected losses of three mechanisms on the triggering event class $\mathcal{E}$ ($P_E := P(\text{true emergency})$, $P_F := P(\text{false-alarm trigger})$):*

- *(0) No delegation (a miss whenever the human is absent): $\mathcal{L}_0 = P_E\,\mathbb{E}[H]$;*
- *(1) Constrained delegation (Definitions 11.2–11.4): $\mathcal{L}_1 = P_E\,\mathbb{E}[L(a^*,\cdot)] + P_F\, c_p + \kappa$ ($\kappa$ = the audit and logging cost);*
- *(2) Unconstrained delegation (the machine acts on its own objective $g_{\mathrm{sys}}$): $\mathcal{L}_2 = \mathcal{L}_1 + \Psi$, where $\Psi \ge 0$ is the agency cost (the deviation loss of $g_{\mathrm{sys}}$ from $g^{(2)}$ + an enlarged attack surface: actions outside the $\mathcal{A}_{\mathrm{safe}}$ whitelist are not constrained by Theorem 11.1, and the action consequences of goal capture lose their boundedness).*

*Then: (1) strictly dominates (0) if and only if $P_E\big(\mathbb{E}[H] - \mathbb{E}[L(a^*,\cdot)]\big) > P_F\, c_p + \kappa$; (1) weakly dominates (2), and strictly dominates it when $g_{\mathrm{sys}} \ne g^{(2)}$ or the attack surface is nonempty (Premise 5).*

**Proof**. We have $\mathcal{L}_0 - \mathcal{L}_1 = P_E\big(\mathbb{E}[H] - \mathbb{E}[L(a^*)]\big) - P_F c_p - \kappa$, and inspecting the sign gives the first claim; here $\mathbb{E}[L(a^*)]$ is controlled by the regret bound of Theorem 11.1 (in the two-action closed form it is of the order $\mathbb{E}[H]/2 + c_p$—this is an order-of-magnitude estimate for that structure, not a general bound; in the general case the exact value is computed instance by instance according to Theorem 11.1(i) at the time $D_{\mathrm{adv}}$ is declared). For the second claim: mechanism (1) takes the subject's loss $L$ as the objective of both its action set and its choice rule, whereas (2) superimposes on this the $g_{\mathrm{sys}}$-deviation term $\Psi \ge 0$; under Premise 5, $\Psi$ is strictly positive (there exist adversaries who will exploit action channels outside the whitelist). $\blacksquare$

### 11.5 The Legitimacy Argument

The source of emergency power is not the system's self-grant but **the reflective layer's pre-commitment**:

1. **The Ulysses contract** (Elster, 1979): the lucid subject authorizes the future machine to act under specified conditions, just as Ulysses instructed his crew not to release him at the Sirens' song. Constraint here is an exercise of autonomy rather than its negation—the institutionalized victory of the second-order will over first-order impulses (Premise 3, extended along the temporal dimension).
2. **Advance directives and the substituted-judgment standard** (medical ethics: Buchanan & Brock, 1990): a proxy decision-maker is to act on the values the subject expressed in advance, not on the proxy's own judgment. The quadruple structure of $D_{\mathrm{adv}}$—event class, action whitelist, thresholds, confidence—formalizes exactly such "values expressed in advance"; the machine exercises no discretion, only table lookup and regret minimization.
3. **Defeasibility**: the retroactive veto right, threshold tightening, and whitelist contraction remain available at all times (the reversibility principle)—the grant of power can be revoked at any moment by the lucid subject, and its difference from authoritarian authorization is structural.

**Conclusion**: autonomy has not been abolished; it has been displaced forward in time—from reaction at the moment of emergency to institutional design at the moment of reflection.

---

<!-- RW-DONE §12 -->

## 12 The Public Agenda Layer: Governing the Externalities of Universal Personalization

**The problem**: if everyone adopts personalized sovereign filtering, the public-agenda function of mass media—shared reality, social coordination—erodes, each person coming to inhabit a high-recall, high-alignment information world disjoint from everyone else's. Personalization is individually rational; at the collective level it risks a fallacy of composition.

**The theoretical anchor**: Aumann (1976). Common knowledge requires public signals; absent "a set of common events that is commonly known," coordination, public discussion, and collective action lose their foundation (the minimal information-level realization condition of the public sphere of Habermas, 1962/1989).

### 12.1 The Mechanism Definition

**Definition 12.1 (The redundantly attested public layer)**. Each day's top propositions, **redundantly attested**, form the public layer $P_t$: a proposition $e$ is attested if and only if it is covered by $\ge k_c$ mutually independent (in the sense of Definition 4.4) trusted source classes. The size is capped at $|P_t| \le 2$ per day; the layer is common to all subjects adopting this framework and occupies a fixed position in the daily digest (consumption share $\gamma \approx 10\%$–$20\%$ of the budget).

**Governance properties**: (a) the content of the public layer is attested by the redundancy law, not chosen by editors—the power question of "who curates the public layer" is converted into a parameter question ($k_c$ and the list of trusted classes are class-B decisions, with defaults published together with their simulation basis, S2); (b) the size cap guarantees that it does not squeeze personalized sovereignty (budget feasibility is incorporated into Proposition 6.3); (c) the attestation criteria and the full candidate logs are public (S4), and any subject can review why these two items were chosen on a given day.

### 12.2 The Reliability Lemma

**Lemma 12.1 (The manipulation resistance of the public layer; a conditional statement)**. *Suppose a single actor's success probability for implanting fabricated content in any one trusted source class has a calibrated upper bound $\bar p_a$ (calibrated from historical attack–defense data or red-team measurements), and suppose implantation events are independent across classes (which holds when classes are separated by ownership, geography, and type and root-node verification of provenance trees is effective). Then the probability that a fabricated proposition it manufactures obtains public-layer attestation ($\ge k_c$ classes of coverage) is $\le \bar p_a^{k_c}$: the attack cost rises exponentially in $k_c$ (each class must be breached independently; in addition there is the provenance cost $c_p$, Section 9.4). Coordinated fabrication (a single actor masquerading as multiple classes) is detected by the class partition of Definition 4.4 and fingerprint clustering; the probability of detection failure is measured by stress tests (Section 14.5 (b)).*

**Proof**. The argument is isomorphic to Theorems 7.1–7.2: replace "the coverage event" by "the implantation-success event"; the single-class success probability is $\le \bar p_a$; cross-class independence is given by assumption; the probability of the intersection is $\le \prod \bar p_a = \bar p_a^{k_c}$. $\blacksquare$

**Note (the importance of conditionality)**. This lemma's guarantee hangs entirely on two assumptions: the calibratability of $\bar p_a$ and the cross-class independence of implantation. Both are empirical propositions, not mathematical facts—in particular, the correlation assumption that "multi-class coverage ⇒ high criticality/high credibility" is violated in real news ecologies (see below); this lemma should therefore be read as a **conditional design lemma**, not an unconditional safety guarantee.

**An empirical qualification (attestation inversion and partial recovery)**. Count-based attestation by class coverage implies the assumption that "breadth of coverage is positively correlated with criticality"; real news ecologies violate it: after the news layer was expanded from 4 domains to 10 domains, the precision of $k_c=2$-attested events on the criticality ground truth fell below the base rate (lift 0.63×)—multi-class coverage captures **high-attention companies** (giants receive multi-domain coverage regardless of the importance of the event) rather than high-criticality events. The engineering remedy (implemented and retested): the attestation statistic was replaced by **quality-weighted surprise coverage** $s(e)=\sum_{c\in\mathrm{classes}(e)} w_c\,(1-\hat r_c(\mathrm{entity}(e)))$ (with $w_c$ ranked by measured $\hat p_{\min}$: regulatory 1.0 / wire services 0.9 / finance and technology 0.6 / aggregators 0; $\hat r_c(t)$ is the walk-forward ratio of entity $t$'s historical events covered by class $c$), which zeroes out the habitual coverage contribution of attention magnets and turns sudden high-weight coverage of a silent entity into a strong attestation signal; on the same corpus at the same coverage rate, lift partially recovered from 0.63× to **1.23×** (still close to 1, a weak enrichment; the word "fix" would be too strong—henceforth we uniformly say partial recovery). The game-equilibrium analysis under adversarial coverage-inflation attacks remains open problem O7. The lower bound of Theorem 12.1 is unaffected by attestation quality (its guarantee comes from the structure of the consumption set).

### 12.3 The Generation of Common Knowledge

**Proposition 12.1 (Public-layer events are common knowledge)**. *Suppose the mechanism (Definition 12.1) is known to all adopters, delivery carries confirmation receipts (the S4 logs), and each adopter knows that the others adopt the same mechanism. Then for the adopter population, the event $\{p \in P_t\}$ is common knowledge in Aumann's sense: (i) everyone knows $p \in P_t$ (the same fixed delivery); (ii) everyone knows that everyone knows (delivery confirmation + the mechanism is public); (iii) induction to arbitrary order.*

**Proof**. A public signal + a public mechanism + receipts constitute a standard public-announcement structure, and Aumann's (1976) partition characterization applies directly (the information partitions are generated by the common delivery, the event is a union of partition elements, so "everyone knows" holds at every order). $\blacksquare$

**Note (degradation under imperfect compliance—a heuristic analogy, not a theorem)**. If a fraction $\epsilon$ of adopters do not actually consume the public layer, intuitively the coordination function degrades continuously in $\epsilon$ rather than failing catastrophically. The exact theory of degradation is the $p$-common-belief framework of Monderer & Samet (1989), whose recursive definition involves the joint information structure across orders and across subjects; the familiar heuristic that "if 'knowing' holds at each order with probability $\ge 1-\epsilon$, then the probability of $k$-th-order common knowledge is $\ge (1-\epsilon)^k$" **requires cross-order independence or stronger information-structure conditions** and cannot be derived directly from the marginal compliance rate. This paper therefore lists only the full-compliance case as a proposition and lists the degradation behavior as a simulation measurement item (Section 14 measures the empirical curve of $\Omega$ against the compliance rate), claiming no theorem.

### 12.4 The Fragmentation Lower Bound Theorem

**Definition 12.2 (Agenda overlap)**. For a pair of subjects $(i,j)$, the Jaccard overlap of their consumption sets is $J(C_i, C_j) := |C_i \cap C_j| / |C_i \cup C_j|$; the population fragmentation index is $\Omega := \mathbb{E}_{i,j}[J(C_i, C_j)]$.

**Theorem 12.1 (The fragmentation lower bound)**. *Suppose each subject consumes $m$ propositions per day, of which the public-layer consumption is $S$ (the same for everyone, $|S| = s = \gamma m$) and the private part is $D_i$ ($|D_i| = d = (1-\gamma)m$, with arbitrary overlap across individuals), with $S \cap D_i = \varnothing$. Then for every pair of subjects:*
$$J(C_i, C_j)\ \ge\ \frac{s}{s + 2d}\ =\ \frac{\gamma}{2 - \gamma}, \qquad\text{hence}\qquad \Omega\ \ge\ \frac{\gamma}{2-\gamma}.$$
*By contrast, without the public layer, $\Omega$ can be arbitrarily close to 0 (the case in which private interests are completely disjoint); fragmentation then has no lower bound.*

**Proof**. $|C_i \cap C_j| \ge |S \cap C_i \cap C_j| = s$ (the public layer is the same for everyone and is consumed by all); $|C_i \cup C_j| = |S \cup D_i \cup D_j| \le s + d + d = s + 2d$ (using $S\cap D_i = \varnothing$ and $|D_i| = d$; overlap of the private parts only shrinks the union and enlarges the intersection, so the direction of the inequality is safe). Dividing gives $J \ge s/(s+2d)$; substituting $s = \gamma m$, $d = (1-\gamma)m$: $\frac{\gamma m}{\gamma m + 2(1-\gamma)m} = \frac{\gamma}{2-\gamma}$. Taking expectations over $(i,j)$ preserves the inequality. The case without a public layer: take the $D_i$ pairwise disjoint (complete divergence of interests), then $J \equiv 0$. $\blacksquare$

**Numerics**: $\gamma = 0.1 \Rightarrow \Omega \ge 0.053$; $\gamma = 0.2 \Rightarrow \Omega \ge 0.111$; $\gamma = 1/3 \Rightarrow \Omega \ge 0.2$. The lower bound is not large, but it is **a constructively guaranteed minimal area of shared reality**: every day at least 1–2 propositions—redundantly attested, made common knowledge, and consumed by everyone—serve as anchors for social coordination and public discussion. The value of $\gamma$ is the explicit trade-off point between the sovereignty principle and publicness: the default is $\gamma \in [0.1, 0.2]$, the upper bound is constrained by the sovereignty principle (the public layer must not squeeze personalization), and **$\gamma = 0$ (complete withdrawal from the public layer) is a legitimate choice of the reflective layer $R$ under S2**—the cost of withdrawal is explicitly priced by this theorem (that subject's contribution to the population $\Omega$ is zeroed), and the act of withdrawal itself leaves a trace (S4). In short: for the individual, the public layer is on by default, auditable, and exitable; its "semi-mandatory" character appears only as a default, never as a transfer of the write right (echoing the dual-use discussion of §16.6).

**Closing the loop with Section 7**: the public layer's attestation machinery and Channel I are one and the same redundant-coverage infrastructure (source classes, independence grouping, $p_{\min}$ calibration). Publicness is not a bolted-on patch but a free by-product of the sovereign architecture: **the redundant monitoring network that individuals build for themselves is, in aggregate, society's shared-reality attestation network**.

---

# Part IV Validation and Governance

<!-- RW-DONE §13 -->

## 13 Catalogue of Falsifiable Predictions

A theory earns its standing by stating how it could be refuted. The table below compresses the paper's theorems into 12 testable predictions, each annotated with its source result, its test vehicle (simulation §14 / field measurement §15 / offline replay), and its **falsification criterion**—the observation that would reject the theorem or its assumptions.

| # | Prediction | Source | Vehicle | Falsification criterion |
|---|---|---|---|---|
| P1 | The filtering ratio $\ge 1 - T/(\underline\tau N)$ holds identically; the number of items consumed under any policy is $\le T/\underline\tau$ | Proposition 6.1 | Log audit | An arithmetic identity; any violation indicates an error in the measurement system |
| P2 | Critical-value leakage $\ge \mathcal{D}^*$; in the Pareto case the leaked share $= 1-(m/K^*)^{(\alpha-1)/\alpha}$ | Proposition 6.2 | Simulation | Measured leakage persistently below the theoretical lower bound |
| P3 | Scoring-channel recall obeys the identity $\beta = (1-\pi)\bar\Phi(z) + \pi\bar\Phi(z-d')$; when $d' < 4.4$, pure-scoring recall $< 95\%$ | Theorem 6.1 | Simulation + offline replay | The measured $(d', \beta, R)$ triples systematically deviate from the identity |
| P4 | The proposition-collapse ratio $\rho_c \in [5, 20]$; the document-level top-$m$ recall ceiling $\beta/\pi \ll$ the proposition-level one | Definition 4.3, Corollary 6.1 | Real-corpus measurement | The corpus-measured $\rho_c$ falls outside the interval (**applicability-domain qualification**: the prediction applies to multi-source aggregation ecologies; a single-source domain affords no room for collapse, so $\rho_c \equiv 1$ is the degenerate case anticipated by the theory and does not trigger falsification—this qualification is declared in advance, not narrowed ex post) |
| P5 | Under direct pass-through from monitored sources, the critical miss probability is $\le (1-\hat p_{\min})^{\hat k_{\mathrm{eff}}}$; the measured $k_{\mathrm{eff}}$ can be raised by grouping design | Theorems 7.1–7.4 | Simulation + corpus-replay ground truth | Measured miss rate persistently above the bound (independence overestimated) |
| P6 | Greedy selection utility $\ge (1-1/e) \times$ the ILP optimum (offline replay); monitoring-slot greedy $\ge 63\%$ of optimal coverage | Theorems 6.3, 7.3 | Offline replay | The greedy/optimal ratio persistently below 0.63 |
| P7 | Marginal-VOI adaptive scheduling outperforms fixed budget partitions, with the gain growing as the marginal differences across uses widen | Theorem 8.1 | Simulation | Adaptive scheduling shows no gain or a negative gain |
| P8 | Pandora-index-guided source exploration discovers high-VOI sources faster than random/greedy exploration; dwelling times obey the marginal = average rule | Propositions 8.1–8.2 | Simulation + deployment logs | The index policy does not beat the baselines |
| P9 | Manipulation exposure $D \le \delta(1-\rho_m)n_m + \delta\sqrt{n_m\ln(1/\beta)/2}$ (with probability $\ge 1-\beta$) | Theorems 9.1–9.2 | Simulation (ground truth known) | Measured exposure exceeds the high-probability bound |
| P10 | Producer-ecology phase transition: once the adoption rate $\sigma > \sigma^*$, the manipulative share decays exponentially at a rate $\ge \gamma/2$ | Theorem 9.3, Proposition 9.2 | Population simulation | The transition point deviates significantly from the $\sigma^*$ prediction |
| P11 | Under the gated curriculum, the Brier/AOT/IH trajectories converge to the declared neighborhood, at a rate constrained by $\sigma_\theta$ and the approval latency; the random bubble-bursting arm exhibits backfire while the curriculum arm does not | Theorems 10.1–10.2, Definition 10.2 | Agent cohorts (H1'/H3') + human anchors; the human version deferred to L3 | The curriculum arm's calibration fails to improve, or a backfire signal appears |
| P12 | The public layer achieves $\Omega \ge \gamma/(2-\gamma)$; the ablation removing the public layer significantly lowers $\Omega$ | Theorem 12.1 | Simulation (with/without public-layer contrast) | Measured $\Omega$ below the constructive lower bound |

**Overall-falsifiability statement**: if P5 and P3 are violated simultaneously—that is, if neither the architectural channel nor the scoring channel can sustain critical recall—then the core claim that "aggressive filtering is provably safe" (C3–C4) is falsified, and the framework collapses into the trivial prescription of "moderate filtering + a larger budget." This is the largest empirical risk the theory is prepared to shoulder.

**Table 13-1. The theorem–evidence support matrix** (the completed empirical support and key figures for each group of core results; for the status labels see the three-state convention of §14.7):

| Result | Core claim | Completed empirical support | Key figures | Evidence strength |
|---|---|---|---|---|
| Proposition 6.1 (capacity lower bound) | A filtering ratio ≥ 99.8% is arithmetic | Log audit (trivial) | $1-45/(4\times10^4)=0.9989$ | Identity |
| Theorem 6.1 (separability bottleneck) | Pure scoring cannot support 95% recall | Two-domain d′ measurements + identity fitting (Table 14-2) | $d'$: 0.73–3.49 (domain/ground-truth dependent) vs. the 4.39 requirement; Gaussian goodness of fit corr 0.968/0.987 | **Strong** (two domains × two independent feature families) |
| Proposition 6.2 (distortion lower bound) | Leakage has an insurmountable lower bound | Holds in all 630 academic-domain runs | Zero violations of the bound | Strong (single domain) |
| Theorems 7.1–7.2 (redundancy coverage) | Miss probability $\le(1-p_{\min})^{k_{\mathrm{eff}}}$ | Financial-domain multi-class redundancy measurements; the academic-domain discovery of $\hat p_{\min}$ endogeneity | $\hat p_{\min}=1.00$ (legal) / 0.02–0.37 (list design) | Conditionally established (§7.7) |
| Theorem 7.4 (total recall) | High recall is borne by architecture | Financial portfolio pass-through meets the target under quota-matched conditions and is diluted to 0.910; rejected in the academic domain | 0.952 → 0.910; 0.28 | **Conditional** (boundary precisely delineated) |
| Theorem 8.1 (no-arbitrage) | Marginal-VOI equalization = shadow price | Adaptive-scheduling simulation contrast (P7, in progress) | Pilot: wasted slots 11→0 | Moderate (simulation) |
| Propositions 8.1–8.2 (exploration/dwelling) | Pandora admission, marginal = average | List-construction optimization contrast (pilot completed) | Submodular greedy 27 vs. citation rank 19 (critical coverage) | Moderate |
| Theorems 9.1–9.2 (firewall bounds) | Exposure has a design bound | Three-family impulse-injection experiment | Consumption rate 45.2%→33.2%; blocking visible across families | Moderate (agent side) |
| Theorem 9.3 + Proposition 9.2 (phase transition/extinction) | $\sigma^*$ phase transition and exponential extinction | Population simulation over a 33-point grid (P10 passed) | $\sigma^*_{ms}=0.060$, $\sigma^*_{sh}=0.200$ matched exactly | Strong (simulation) |
| Theorems 10.1–10.2 (sublimation convergence) | The gated curriculum converges to the declared neighborhood | H1' (in progress); H8/H9 transfer bridges (completed) | See Table 15-1 | Weak–moderate (human side unverified) |
| Theorems 11.1–11.2 (emergency override) | Regret bound and dominance of delegation | Tabletop exercise (in design) | — | Design stage |
| Theorem 12.1 (fragmentation lower bound) | $\Omega\ge\gamma/(2-\gamma)$ | Financial real corpus × 500 agents | $\Omega=0.168\ge0.111$; 0.066 without the public layer | Strong (single domain, bound tight) |
| Lemma 12.1 (certification manipulation resistance) | Conditional manipulation resistance | Certification reversal + partial recovery (real ecology) | lift 0.63× → 1.23× | Conditional (O7 open) |

---

<!-- RW-DONE §14 -->

## 14 Simulation and LLM-Agent Experiments

Simulation and LLM-agent experiments serve a threefold purpose: before engineering and deployment are undertaken, (a) to test all the falsifiable predictions P1–P12; (b) to produce a default-prior parameter table; and (c) to stress-test every idealized assumption. All parameters are kept symbolic and assigned values only after scanning. The infrastructure of this chapter also serves as the environment layer of L1 (the LLM-agent cohorts, the main validation vehicle) in the three-tier validation architecture of §15.

### 14.1 The Synthetic Information-Ecology Generator

A four-layer generative structure:

1. **Source-landscape layer** (the pull side): $N_s \sim 500$ sources, whose quality $Q_s$ (daily VOI production rate) is drawn from a heavy-tailed log-normal distribution and is **initially invisible to the consumer agent** (revealed only through exploration, and only noisily); sources are grouped by (ownership × geography × type) into $K \sim 20$ classes; cross-class correlation is governed by a shared-upstream (wire-service) parameter, so the ground truth of $k_{\mathrm{eff}}$ is known by construction;
2. **Event layer**: events $e_j \sim$ Poisson arrivals, criticality $v_j \sim \mathrm{Pareto}(\alpha)$ ($\alpha$ scanned over $[1.2, 2.5]$);
3. **Proposition layer**: events generate propositions; critical events are covered by multiple source classes (the coverage probability $p_i(e)$ is determined by class quality and event type, and the ground truth of $p_{\min}$ is known); **stress branch**: a subset of "low-redundancy critical propositions" is designated ($p_i \approx 0$ for most classes), testing the monitoring list and the public-layer backstop;
4. **Document layer**: propositions generate documents (reposting counts $\sim$ negative binomial, with $\rho_c$ emerging endogenously); documents carry observable features (arousal-word density, urgency framing, the share of evidence-free assertions, provenance completeness) that are partially correlated with the ground truth $(v^*, m, s)$ (the correlation is parameterized $\Rightarrow$ the ground truth of $d'$ is controllable and scannable).

**Three producer types** (initial shares: honest 50% / sensational 30% / manipulative 20%):

| Type | Behavioral parameters | Objective |
|---|---|---|
| Honest | high provenance cost, low arousal | reputation (long-term subscriptions) |
| Sensational | high arousal, low provenance | attention monetization |
| Manipulative | targeted stance injection, coordinated propagation patterns, feigned independence | belief rewriting |

**The adversarial-adaptation loop**: producers observe the passage rates of the various filters and mutate content features via evolutionary strategies to escape detection; coordinated producers additionally evolve strategies that "feign multi-class independence" (attacking $k_{\mathrm{eff}}$)—testing the Red Queen condition and the fingerprint-clustering defense.

### 14.2 The Consumer-Agent Model

$10^4$ heterogeneous agents: budget $T$, decision set $D$ (which determines $E^*$ and $w$), initial virtue $\theta_0$, and shadow-price estimation precision all vary. Agents are stratified and parameterized by **five canonical profiles** (clinician, investor, frontier researcher, business owner, citizen-parent); the profile dossiers and the prior intervals of the foundational parameters ($p_{\min}, \rho_c, d', \delta$) appear in the Supplementary Material. **KPIs are reported stratified by profile**: the effective strength of each theorem varies systematically with the profile (redundancy coverage is strong for clinicians/investors and weak for researchers, where the monitoring list compensates; the no-arbitrage scheduling gain is largest for business owners), and stratified reporting upgrades the falsifiable catalogue of Section 13 into a **profile × prediction matrix** in which any failing cell localizes a specific assumption. A built-in impulse term lets high-arousal content generate immediate utility ($g^{(1)}$) that is misaligned with $g^{(2)}$; the virtue dynamics evolve as in Section 10.1 ($q_t$ endogenous: impulse consumption depresses engagement quality); the gating-approval latency $\Delta \sim$ measured priors. **A three-layer agent architecture**: the parameterized-agent layer (the design above) carries population-level KPIs and ecological dynamics; the **LLM-agent cohort (100–1000 agents, the main experimental subjects)** runs the full SEA stack and carries the behavioral tests (profile cards + declared decision sets + framework-level budget enforcement and impulse injection; LLMs have no genuine first-order impulses and are over-compliant/over-rational, so the impulse term must be exogenously parameterized); hybrid agents (a parameterized shell + an LLM decision core) carry the compromise arm. Every LLM agent must pass a validation battery of "replays of published human experiments" before being used for any conclusion; subject / scorer / red-team / judge models are forcibly separated (≥3 families, guarding against circularity). For the specifications see §15.2 and the Supplementary Material; the bias-lineage argument for LLMs simulating humans likewise appears in the Supplementary Material.

### 14.3 Contrast Policies

1. **S0 raw stream**: no filtering; items are consumed in arrival order until the budget is exhausted;
2. **S1 engagement optimization**: the platform baseline, maximizing dwell time (including a sensationalism premium);
3. **S2 full SEA**: dual-channel filtering + Pandora exploration + MVT dwelling + EIG queries + marginal-VOI scheduling + curriculum gating + the public layer;
4. **S2a push only** (ablation): all pull operators switched off, the candidate pool fixed—quantifying the marginal value of active acquisition;
5. **S2b fixed partition** (ablation): pull enabled but the budget partition fixed, no marginal-VOI scheduling—testing Theorem 8.1;
6. **S2c pure scoring** (ablation): Channel I pass-through switched off, everything competing by score—testing the bottleneck prediction of Theorem 6.1 (critical recall is expected to collapse toward the $\beta/\pi$ ceiling);
7. **S2d end-to-end LLM screening** (ablation, in design): all SEA structure removed (dual channels, the proposition graph, lists, scheduling), with the same LLM performing end-to-end screening and ranking directly on the raw candidate stream—separating "the contribution of the framework structure" from "the contribution of the large model's judgment," thereby answering the attribution question concerning the judgment-arm gains in S2;
8. **S3 chronological-credibility**: a naive baseline of chronological ordering + a credibility threshold.

### 14.4 The Measurement Protocol (KPIs and Target Values)

| Indicator | Definition | Target value | What it tests |
|---|---|---|---|
| Digest precision | the share of delivered items that the subject rates as "worthwhile" | ≥80% | scoring-function weights |
| Critical-proposition recall | the share of $E^*$ that is delivered | ≥95% | Theorem 7.4 (P5) |
| Recall decomposition | the respective contributions of Channel I / Channel II / the list / the public layer | Channel I dominant | the dual-channel architecture |
| Manipulation-exposure rate | the share of the consumption set with $m > \tau_m$ | <5%, and consistent with the Theorem 9.2 bound | P9 |
| Time-compliance rate | the share of days on which actual time spent ≤ $T$ | ≥90% | the delivery rules |
| VOI/minute | total realized information value / total cognitive time | S2 significantly > S1 > S0 | the efficiency claim |
| Exploration efficiency | realized VOI of discovered sources / exploration minutes | Pandora > random/greedy | P8 |
| Scheduling gain | the total-VOI difference of S2 vs. S2b | >0 and increasing with heterogeneity | P7 |
| Stance-entropy ratio | stance entropy of the consumption set / corpus entropy | ≥0.8 | the no-backfire curriculum |
| Calibration improvement | 90-day Brier change, S2 vs. S1/S0/S2a | S2 significantly best | P11 |
| Backfire signal | affective-polarization change after exposure to opposing views | curriculum arm ≤ 0, random arm > 0 | Definition 10.2 |
| Producer ecology | manipulative-share trajectory vs. $\sigma$ | phase transition at $\sigma^*$ | P10 |
| Agenda overlap $\Omega$ | with/without public-layer contrast | public-layer arm ≥ $\gamma/(2-\gamma)$ | P12 |
| Proposition-collapse ratio $\rho_c$ | documents / propositions | 5–20× | P4 |

### 14.5 The Stress-Test Battery

(a) **Correlation shock**: a shared-upstream event causes $k_{\mathrm{eff}}$ to drop sharply (e.g., a wire-service merger)—testing the degenerate behavior of Theorem 7.2 and the regrouping mechanism; (b) **coordinated fabrication**: pseudo-independent multi-class attacks on certification and coverage—testing fingerprint clustering and provenance penetration; (c) **the low-redundancy long tail**: the emergence of niche critical propositions—testing the timeliness of list declarations and the public-layer backstop; (d) **detector drift**: $\rho_m$ decaying as producers evolve—testing aggregate-calibration monitoring and the automatic tightening of $n_{\max}$; (e) **gating latency and rejection**: $\Delta$ increasing, the veto rate rising—testing the robustness range of Step 3 of Theorem 10.1; (f) **non-stationary source quality**: $Q_s$ drifting—testing the CUSUM rotation-out mechanism; (g) **budget shock**: $T$ halved—testing the feasibility alarm of Proposition 6.3 and the $g^{(2)}$-revision channel; (h) **synthetic-reposting flood**: AI-generated content masquerading as multi-source reporting, inflating $\hat\rho_c$ and fabricating "independent coverage"—testing content-fingerprint deduplication and the contamination-resistant estimation of $k_{\mathrm{eff}}$ (the common-source risk of the calibration data is discussed in the Supplementary Material).

### 14.6 Deliverables

A **default-prior table** produced after parameter scanning (the simulation-optimal values of the thresholds, weights, quotas, $\eta$, $q^*$, $\gamma$, $k_c$, together with their sensitivity intervals)—the starting point for deployment-time individual parameterization, not a direct input of any individual's preferences; all default values are published with their simulation basis (the governance clauses of Section 16). Public data sources and calibration routes for the foundational parameters ($p_{\min}, \rho_c, d', \delta$) appear in the Supplementary Material.

### 14.7 The LLM-Agent Cohort Experiments (Main Validation Vehicle): A Structured Report of the Completed Pilots

This chapter's simulation infrastructure doubles as the environment layer of the LLM-agent cohort experiments: LLM agents (the second layer of the three-layer agent architecture of §14.2) run the full SEA stack on synthetic ecologies and on **real-corpus temporal replay streams** (GDELT / CNINFO-EDGAR / arXiv-Semantic Scholar / WHO DON / Weibo21; ground truth = official event lists, debunking archives, citation counts), receiving factorialized treatments of the S0–S3 arms and three classes of adversarial environment (prompt injection, persuasive content, coordinated fabrication). In replay environments the "future" is known, so P1–P12 of §13 are all measurable on agents, with P2/P3/P5/P9 upgraded from "ex post audit" to **exact measurement**, and prediction tasks (the longitudinal tracking of $\theta_{\mathrm{cal}}$) incur zero annotation cost. For the experimental protocols see §15 and the Supplementary Material.

**Experiment-status convention**: this section and Section 15 explicitly label every experiment with one of three states—**[completed]** (data and analyses frozen), **[in progress]** (partial data obtained; the pre-registered sample size not yet reached), **[design]** (protocol archived, not launched). All raw records, decision rules, and code of the completed pilots appear in the Supplementary Material (*Data and Code Availability*).

**Table 14-1. Experiment matrix and status overview**

| Experiment | Purpose (corresponding theorem/proposition) | Environment | Status | Core results |
|---|---|---|---|---|
| Academic-domain replay (Pilot A) | Theorem 6.1 identity; distortion lower bound; the strong form of H4'; $\hat p_{\min}$ endogeneity | arXiv 2019-09, 2576 propositions, $K^*=52$ | [completed] | Gaussian-approximation goodness of fit corr=0.968 (within the Gaussian model the identity is an identity; corr measures how well the measured score distribution fits the Gaussian approximation, not an independent test of the identity itself); the lower bound holds in all 630 runs; the strong form of H4' is rejected (best 0.28) → refined into a boundary condition |
| Financial-domain replay (Pilot B) | Theorems 6.1, 7.1–7.4; multi-class redundancy measurement; the conditional form of H4' | EDGAR + public news archives (10 domains), 1876 propositions / 15368 documents | [completed] | $\rho_c=8.19$ (within the prior interval [5,20]); regulatory class $\hat p_{\min}=1.00$ (legal ground truth); within-portfolio recall at $m{=}5$ reaching 0.952 → 0.910 after news-layer expansion |
| Feature-scorer d′, two vintages | The realistic range of $d'$ for Theorem 6.1 | Same as above | [completed] | TF-IDF features d′=0.77; semantic-embedding features d′=0.73—two independent feature families converge: the bottleneck does not lie in representation engineering |
| LLM three-family replay | The incremental value of the judgment layer (vs. the feature arm / the semi-oracle parametric arm) | Financial replay stream × 3 model families × 240–480 agent-days | [completed] | Judgment-arm recall 0.401/0.457/0.513, beating the feature arm across the board (0.23–0.25); vs. the semi-oracle arm CMH $p=0.017$ (significant after sample expansion) |
| LLM four-family main-validation replay (academic domain) | Cross-family replication of the judgment layer's incremental value (vs. the feature arm / the semi-oracle parametric arm) | arXiv 2019-09 replay × 4 families × 80 runs × 30 agents × 30 days (73,547 valid agent-days) | [completed] | Judgment-arm critical recall 0.443 / 0.534 / 0.514 / 0.519 (O/C/Q/G), all families ≥1.8× the honest feature arm (0.241); vs. the semi-oracle arm, McNemar significant in all families after BH correction ($p\le 8.2\times10^{-10}$), cross-family CMH pooled $p\approx1.9\times10^{-215}$ (80 strata); value increments diverge across families (positive for C/Q, slightly negative for O/G—see the declaration in §15.2) |
| H8 validation battery v1/v2 | The validity of LLM replays of human paradigms (the transfer bridge) | Three paradigms × three model families | [completed] | See §15.4: one pass, one failure, one ceiling (v1) → v2 family-stratified conclusions |
| H9 calibration anchor | Agent vs. human calibration baselines | Manifold human anchor × four families | [completed] | Calibration is strongly family-dependent (Brier 0.170 / 0.232 / 0.233 / 0.295)—only the reasoning-oriented family falls within the human band |
| P10 producer-ecology phase transition | Theorem 9.3, Proposition 9.2 | Purely parameterized population simulation | [completed] | The transition boundary matches the analytic values exactly ($\sigma^*_{ms}=0.060$, $\sigma^*_{sh}=0.200$); the extinction-rate lower bound holds at all 33 grid points |
| List rolling-update contrast | Life-cycle management of the monitoring list | Financial domain, zero-hindsight evaluation | [completed] | Fresh-list $\hat p_{\min}$ 0.231→0.269; under quota saturation, total recall is insensitive to freshness (the bottleneck shifts to within-list ranking) |
| Theorem 12.1 lower-bound verification | The fragmentation lower bound (P12) | Financial real corpus × 500 agents | [completed] | $\Omega(\text{public layer})=0.168 \ge \gamma/(2-\gamma)=0.111$; 0.066 without the public layer (the bound is tight) |
| Public-layer certification reversal and partial recovery | The conditionality of Lemma 12.1 | Same as above, news layer expanded from 4 to 10 domains | [completed] | lift 0.63× (failure) → quality-weighted-surprisal certification 1.23× (partial recovery, weak enrichment); the game-equilibrium analysis is left to O7 |
| Population-level SEA vs. baselines (the full P1–P12 battery) | All falsifiable predictions | Synthetic ecology × $10^4$ agents × multiple profiles | [in progress] | Pilot indicators in Table 14-2; the pre-registered sample size (≥30 runs × 90 simulated days × profile stratification) not yet reached |
| S2d end-to-end LLM ablation | Attributing structural contribution vs. model judgment | Financial replay stream | [design] | — |
| Adversarial stress-test battery (the eight items of §14.5) | The robustness domain of the idealized assumptions | Synthetic ecology | [in progress] | Pilot data already obtained for two items: coordinated fabrication and detector drift |

**Table 14-2. Core figures of the two-domain pilots (completed, frozen calibers)**

| Quantity | Academic domain (Pilot A) | Financial domain (Pilot B) | Theoretical reference |
|---|---|---|---|
| Proposition-collapse ratio $\hat\rho_c$ | 1.0 (a single-source domain—the degenerate case anticipated by the theory) | 8.19 | Prior interval [5, 20] (P4) |
| Coverage floor $\hat p_{\min}$ | author list ≈0.02; institution list 0.17–0.37 | legal ground truth 1.00 (regulatory class); market ground truth 0.70–0.73 | The $p_{\min}$ of R1 is a design function and has an institutional provenance (E-7.1/E-7.2) |
| Score separability $d'$ | 0.73–0.77 (two independent feature families) | legal 2.65–3.49; market 0.54–0.60 | All < the 4.39 requirement line ⇒ the bottleneck theorem's (Theorem 6.1) division-of-labor conclusion reinforced in both domains |
| Critical recall (Channel I + list) | best 0.28 (the strong form of H4' rejected) | within-portfolio $m{=}5$: 0.952 → 0.910 (news-layer dilution) | §7.7: conditionally established; the applicability-domain boundary is given in that section |
| Gaussian-approximation goodness of fit | corr=0.968 | corr=0.987 | The model-fit test of Theorem 6.1(i) (P3; not a test of the identity itself) |
| Attributable share of market-moving days | — | ≈10% (90% not attributable) | Quantification of the public layer's functional position (§12) |

**Table 14-3. Caliber reconciliation of key figures (version-evolution ledger)**

The same quantity cited in different chapters of the paper may come from different calibers (feature-set versions, news-layer versions, quota calibers); the reconciliation is as follows—when judging which test a given figure corresponds to, this table is authoritative:

| Quantity | Caliber A (early / no news layer) | Caliber B (full news layer) | Where cited |
|---|---|---|---|
| Financial-domain $d'$ (legal ground truth) | 2.65 (metadata feature set v1) | 3.49 (feature set v2 + news features) | §7.5 uses the interval 2.65–3.49 |
| Financial-domain $d'$ (market ground truth) | 0.60 (with attention signals) / 0.02 (no news layer) | 0.54 (10-domain news layer) | §7.5 uses the interval 0.54–0.60 |
| Financial-domain $\hat p_{\min}$ (market) | 0.73 (4-domain news layer) | 0.70 (10 domains) | §7.5 uses the interval |
| Within-portfolio recall ($m{=}5$) | 0.952 (before news-layer expansion) | 0.910 (after expansion; the quota diluted by news propositions) | §7.5, §7.7 |

**A note on the sensitivity and circularity of the ground-truth proxies**. The ground-truth proxies of both replays carry ex post bias, and this paper handles this as follows: (i) the academic domain defines critical papers by "top-2% cited"—citation counts lag by years and carry prestige bias, making this proxy closer to "academic engagement" than to ex ante criticality; sensitivity test: recomputing under two alternative proxies—"cited within 6 months of publication" and "cross-field citations"—leaves the rejection of the strong form of H4' unchanged under every proxy (the direction of the rejection does not depend on the proxy choice); (ii) the financial domain defines criticality by "market-moving days"—an ex post label, with 90% of market-moving days not attributable to same-day information; under the second ground truth (legally material 8-Ks, defined ex ante by regulatory rules), all structural conclusions ($\hat p_{\min}$, the d′ split, pass-through recall) agree in direction. The "recall" figures of the two pilots should therefore be read as "recall against the stated proxy," and the extrapolation to "ex ante criticality" rests on the human-jury audit of §15.5.

**Statistical conclusions on the LLM judgment layer (completed, pre-registered decision rules)**. For the three-family replay, the CMH stratified pooled test of the LLM judgment arm against the honest feature arm yields $p=6.8\times10^{-28}$ (Σb:Σc=457:123—the judgment layer's incremental value statistically confirmed); against the semi-oracle parametric arm, $p=0.017$—expanding the qwen family's replicate to 480 agent-days turned 0.057 into significance (the expansion decision was triggered in advance by the power analysis of the first run, not by ex post p-value screening; the replicate sample's 0.517 and the first sample's 0.513 almost coincide), with bootstrap confidence interval [+0.002, +0.130]. All p-values are accompanied by effect sizes and confidence intervals in the Supplementary Material; multiple comparisons are controlled by the pre-registered hierarchical testing sequence (main effects first, interactions after). The impulse-injection consumption rate decreases monotonically across families, 45.2%→40.9%→33.2% (reasoning-oriented models are less susceptible—reasoning is not immunity to salience), and explicit blocking of breaking items by constitutional reasoning is visible across families.

**The LLM four-family main-validation replay (academic domain, [completed], protocol v2.1 frozen calibers)**. Cross-family replication of the judgment layer's incremental value: 4 model families × 80 independent runs (30 runs each for the primary families O/C, 10 runs each for the anchor families Q/G; seeds fixed) × 30 agents × 30 days, 73,547 valid records. Judgment-arm critical recall: O 0.443 [0.433, 0.454] / C 0.534 [0.527, 0.541] / Q 0.514 [0.502, 0.526] / G 0.519 [0.498, 0.539] (run-level bootstrap 95% CIs)—all families exceed the honest feature arm (0.241) by more than 1.8×; the pilot's judgment-layer increment conclusion replicates across families at roughly 25 times the sample size. The day-paired comparison against the semi-oracle parametric arm is significant in all families after Benjamini–Hochberg correction (McNemar $p\le 8.2\times10^{-10}$), with the cross-family CMH pooled $\chi^2_1=981.5$, $p\approx1.9\times10^{-215}$ (stratified by run, 80 strata). The value dimension is honestly declared to diverge across families: Δvalue C $+0.676$ / Q $+0.432$ positive, O $-0.175$ / G $-0.223$ slightly negative—the hit dimension is won across the board while the average value increment splits two-positive/two-negative; the inconsistency between the two dimensions is itself archived as a finding, and the mechanism analysis is listed as an open problem (§17). Impulse susceptibility 0.238–0.349. Statistical discipline: the unit of analysis is the agent-day, the unit of replication is the run, and inference is stratified by run (inflating degrees of freedom with agent-days is forbidden); quarantine isolation (voided protocols and the dropped family are archived and do not enter the analysis).

---

<!-- RW-DONE §15 -->

## 15 Empirical Validation: A Three-Tier Architecture Led by LLM-Agent Cohorts

### 15.1 The Model-Organism Strategy

This theory is stated for "every bounded agent" (Premises 1–6, invariants I1–I5), and the mathematical objects of all its theorems—budget constraints, coverage events, weight-drift metrics, gating latency, regret bounds—refer to no human-specific attribute; the symmetry tables of §3.3 and §9.3 give the AI instantiations line by line. The validation program therefore takes **LLM-agent cohorts as its primary experimental subjects** (a model-organism strategy: as the fruit fly is to genetics), whose structural advantages over a human RCT are:

- **Time compression**: a 90-simulated-day intervention completes within hours to days of wall-clock time and can be repeated thousands of times;
- **Full counterfactual observability**: in synthetic ecologies, $v^*, m, s$ are simply generator parameters; in real-corpus temporal replays the "future" is known—recall, miss, and manipulation exposure are upgraded from "ex post audit" to "exact measurement," and prediction tasks (the longitudinal tracking of $\theta_{\mathrm{cal}}$) incur zero annotation cost;
- **Zero recruitment, zero attrition, no IRB on the critical path**; the cost is more than two orders of magnitude below a human RCT;
- **Theory self-check (with reservations)**: if the theorems fail systematically on AI agents, the universality claim is seriously damaged—agent experiments are therefore not merely a cheap substitute but a direct test of the theory's carrier-neutrality. Inference in the reverse direction, however, must be restrained: that a theorem holds on LLMs **cannot** be directly extrapolated to humans, especially on the parameters this paper cares most about—H8/H9 show systematic divergences between LLMs and humans in argument-based persuasion susceptibility, the inattention mechanism, and extremity effects (§15.4). The LLM fruit fly can therefore validate only the theory's carrier-neutral mechanisms and their AI instantiation, while all human-side conclusions retain the status of "predictions" (§17, Limitation 15).

**What cannot be bought** (an honest boundary): human-specific quantities—the precise value of the real emotional-hijacking effect $\delta_{\mathrm{human}}$, practiced human virtue formation, welfare effects on real people—are not validated by agent experiments; they are instead bounded in magnitude by the L2 online human-data anchors and ultimately settled by the L3 deferred human RCT. Proposition 10.2 implies this self-referentially: judgments made by the machine on one's behalf cannot measure a human's calibration.

**The three-tier validation architecture**:

$$\underbrace{\text{L1 LLM-agent cohort experiments}}_{\text{main tests: H1'–H7'}} \;+\; \underbrace{\text{L2 online human-data anchors}}_{\text{transfer bridges: H8–H9}} \;+\; \underbrace{\text{L3 deferred human RCT}}_{\text{protocol archived (§15.5)}}$$

### 15.2 L1: LLM-Agent Cohort Experiments (Main Validation)

The full protocol appears in the Supplementary Material; key points:

- **Subjects**: three layers—parameterized agents ($10^4$, population-level statistics and ecological dynamics); the **LLM-agent cohort (100–1000, the main experimental subjects)**, running the full SEA stack (scoring, dual channels, Pandora exploration, EIG queries, Whittle scheduling, curriculum gating, emergency override); and hybrid agents (a parameterized shell + an LLM decision core). Profile cards are generated from the five profiles × digital traces (zero interviews); the reflective layer $R$ is implemented by a per-profile "constitutional document" (approval rules + $D_{\mathrm{adv}}$ + gating policy), maintained by the team with sampled review; the $g^{(1)}$ impulse term is exogenously injected at the framework layer (LLMs have no visceral impulses; parameters are anchored to the MIND click distribution);
- **Environments**: the synthetic ecology (§14.1) + **real-corpus temporal replays** (the five streams GDELT/CNINFO-EDGAR/arXiv-S2/WHO DON/Weibo21; ground truth = official event lists, debunking archives, citation counts) + adversarial environments (three arms: prompt injection, persuasive content, coordinated fabrication);
- **The model-separation principle (mandatory, guarding against circularity)**: subject model ≠ scorer model ≠ producer/red-team model ≠ judge/merging model, across at least 3 model families; on the judging side, team human spot-checks of 10% are added;
- **Treatment arms**: S0/S1/S2/S2a/S2b/S2c/S3 (§14.3) × profile × environment × adversarial intensity; a main-effects design, ≥30 runs × 90 simulated days per profile per policy;
- **Measurement**: P1–P12 of §13 are all agent-measurable; the AI instantiation of $\theta$ = retrospective-prediction Brier/ECE trajectories + the evidence-conditioned belief-revision rate (the openness analogue) + the confidence–accuracy gap (the overconfidence penalty) + the original-text/raw-data reach rate (the $q_t$ analogue).

**Compute budget and run disclosure (main-validation replay, protocol v2.1 frozen)**. The four-family main-validation replay comprises 80 independent runs and 73,547 valid agent-days, over 13 days of wall-clock time. Compute mix: a local workstation (primary-family runs 1–22), two LAN nodes (anchor families + reinforcement for primary runs 23–30), and cloud APIs (the ling primary family throughout + cloud replication of qwen anchor runs 2–10; the same models across backends, declared with hardware/backend as a stratification variable). Thinking budgets are tiered by family (reasoning-oriented models 2,400/4,800 tokens with two-tier retry, the rest 1,200/2,400); rate limiting (HTTP 429) and empty responses are handled by the pre-registered backoff-and-backfill rules; every run has an integrity gate (≥900 valid agent-days; otherwise the completion flag is refused and backfill is triggered automatically). Cloud cost was about USD 50 (account monthly cap USD 100). A fifth candidate family (nemotron) could not reach the pre-registered sample size owing to a hard free-quota ceiling and paid-channel capacity bottlenecks (HTTP 429); it has been dropped and archived, and does not enter the analysis—honestly declared as an operational negative result; the final 4 families satisfy the ≥3-family requirement of the model-separation principle.

### 15.3 L2: Online Human-Data Anchors (Zero Recruitment)

Only publicly available human data obtainable online at low cost are used, and their function is restricted to **calibration anchors and transfer bridges**; they carry no main hypotheses:

| Anchor | Resource | Use |
|---|---|---|
| Human calibration baselines | Metaculus / Manifold Markets (public predictions + resolutions, free API) | quantile comparison of agent Brier/ECE distributions against human distributions (H9) |
| Backfire effect size | Bail et al. (2018) Dataverse replication data | the human effect-size contrast for H3'; replay paradigm one |
| Prompt-intervention effect size | the Pennycook & Rand OSF repository | replay paradigm two; priors for the firewall's "cooling" parameters |
| $g^{(1)}$ impulse distribution | MIND/xMIND click logs | anchoring the impulse-injection parameters (clicks = a public proxy of first-order preferences) |
| Discrimination paradigm | the published misinformation $d'$ literature | replay paradigm three |
| $\delta_{\mathrm{human}}$ prior | the meta-analyses of Chan et al. (2017), Ecker et al. (2022), etc. | the human-side magnitude constraint on the firewall bounds (the precise value is left to L3) |
| Polarization/trust scales | ANES, GSS | human-version templates for $\theta_{\mathrm{open}}$-type measurement instruments |
| Rumor ecology | the piyao.org.cn archive, MultiFC (Augenstein et al., 2019), Weibo21 (Nan et al., 2021) | the ground-truth lists for the replay environments |

### 15.4 The Hypothesis System (Pre-Registered)

**Agent main hypotheses H1'–H7'** (the detailed table appears in the Supplementary Material): H1' calibration trajectories under curriculum gating outperform the baselines (the AI instance of Theorems 10.1–10.2); H2' VOI/token and the scheduling gain (Theorem 8.1); H3' exposure within the tolerance band does not increase attitude extremity whereas random exposure does (the persuasion-paradigm test of Definition 10.2); H4' recall on replay corpora ≥95% with the pure-scoring arm collapsing to the $\beta/\pi$ ceiling (the conjunction of Theorem 7.4 + 6.1—the decisive test of the dual-channel architecture; current status: conditionally established, see §7.7 and Table 14-1); H5' the Pandora exploration advantage (Proposition 8.1); H6' zero misses of watchlist entities (Proposition 7.2); H7' original-judgment performance and calibration degrade in the "summary-only" mode but do not degrade in the "map + original" mode (the AI instance of Proposition 10.2, cross-validating the model-collapse literature (Shumailov et al., 2024)).

**Transfer-bridge hypotheses H8–H9**: H8—agents replay three published human paradigms, with effect directions consistent and magnitude deviations reported and entered into the uncertainty budget; H9—agent baseline calibration falls within the quantile band of the human distribution (systematic offsets allowed, provided they are monotone and correctable). The two completed rounds of the H8 battery and the H9 four-family results are summarized below (decision rules pre-registered; all raw records in the Supplementary Material):

**Table 15-1. H8 validation-battery results (three model families, [completed])**

| Paradigm (replay target) | v1 first run (single family, small sample) | v2/v2.1 (three families) | Pre-registered disposition |
|---|---|---|---|
| B opposing-exposure extremity (the Bail et al., 2018 paradigm) | direction passed (d=0.36, human band 0.22–0.35); but accompanied by large assimilation | **cross-family directions inconsistent** (+1.26 / +0.84 / −0.75) | family-dependent, **must not enter the priors**, enters O6 |
| A accuracy prompts (the Pennycook–Rand paradigm) | direction failed (a floor effect + the "inattention" mechanism absent in LLMs) | direction consistently negative across the three families (d = −0.04 / −0.55 / −0.52), the latter two families in the same band as the human anchor | direction enters the priors; effect sizes assigned per-family coefficients |
| C true/false discrimination d′ | d′=3.77 hit the knowledge ceiling (stimuli predate the models' knowledge cutoff) | memory-proof new materials: d′ = 1.13 / 1.41 / 1.99, falling back near the human interval (1.0–1.8) | usable as an order-of-magnitude anchor for d′ |
| The assimilation channel (an LLM-specific finding) | persuaded by opposing arguments by >1 point on a 7-point scale | same sign across the three families (signed displacement −0.87 ~ −1.60) | the argument-based persuasion payload δ revised downward per family; enters the O6 transfer-coefficient library |

**The H9 calibration anchor ([completed])**: the four families' Brier = 0.170 / 0.232 / 0.233 / 0.295 (constant baseline 0.219; human anchor 0.112; the literature's superforecaster band 0.15–0.21)—calibration quality is strongly family-dependent, with only the reasoning-oriented family falling within the human band; the initialization anchor of $\theta_{\mathrm{cal}}$ is therefore conditioned on the family, and "calibration quality" is listed as a hard criterion of model selection (O6).

**The methodological implication of the two-way distortion**: H8/H9 demonstrate both the discriminative power of the validation battery and that the LLM fruit fly and humans are not directly commensurable on the parameters this paper cares most about (the persuasion payload δ, extremity responses)—the model-organism argument of §15.1 is therefore confined to carrier-neutral mechanisms, and all human-side statements are phrased as "predictions" (§17, Limitation 15).

**Statistical plan and reporting standards**: mixed-effects models (runs and model families as crossed random effects); profile-moderation analyses; multiple comparisons controlled by the pre-registered hierarchical testing sequence (main effects first, interactions after, Holm correction within families); **all statistical conclusions report effect sizes and confidence intervals together** (bootstrap, 10⁴ resamples)—bare p-values are never reported alone; sample-expansion decisions can only be triggered by ex ante power analysis (the qwen replicate of 480 agent-days is an instance of this rule: first run p=0.057 → expansion per the pre-registered power analysis → p=0.017, with the replicate sample's effect size almost coinciding with the first sample's); model versions, prompts, temperature and decoding parameters, and access dates are all frozen and logged, and any version change triggers a rerun of the anchors; all hypotheses, environment snapshots, random seeds, and analysis plans are pre-registered in a public registry (the OSF link appears in *Data and Code Availability*). **Failure of H4' and H1' respectively overthrows the AI instances of the architecture claim and the sublimation claim, with no ex post rationalization.**

### 15.5 L3: The Deferred Human RCT (Protocol Fully Archived)

The final test of the human-side causal claims (the original versions H1–H7) is reserved as a standard three-arm RCT design, to be launched when: (a) direct human-side evidence is required (e.g., regulatory or publication requirements prior to deployment), or (b) external partnerships are in place (a medical school's clinical research center, a business school's case center, a parents' organization—tool licensing in exchange for participant access). The archived design:

- **Three arms**: A raw stream / B engagement-optimized stream / C full SEA; 12 weeks; stratified randomization by the five profiles; judges blind to assignment;
- **Sample size**: the primary outcome is calibration improvement; with a conservative $d = 0.35$, two-sided $\alpha = 0.05$, and power 0.8 ⇒ $n \approx 128$ per arm; accounting for 25% attrition, **170 per arm, about 510 in total**; a lead-in pilot may shrink to a single arm + historical controls (n≈30, validating the toolchain and the retention rate);
- **Measurement instruments**: ten verifiable prediction questions per week (longitudinal Brier); AOT and intellectual-humility scales administered at three points; device-level time logs (the push/pull/reflection tripartition); critical-recall audits by an independent jury (Theorem 7.4 and H4); biweekly manipulation-discrimination $d'$ tests; backfire monitoring (the Bail-paradigm scales); active-acquisition behavior (list revisions, realized exploration VOI vs. the Pandora prediction, lateral-reading trigger rates); deskilling monitoring (original-text reading-depth trajectories, Proposition 10.2);
- **Hypotheses H1–H7**: as pre-registered in the previous version (sublimation, efficiency, no backfire, recall, exploration value, long-tail backstop, deskilling immunity).

### 15.6 Research Ethics and Integrity

Red-team content generation goes through institutional safety review; only detectors and statistics are released, never raw payloads; **simulation and agent data are never passed off as human data** (the generation method and model generation are labeled in three places: datasets, logs, and paper tables); online human data comply with platform terms, are de-identified, and are reported only in aggregate; the team's self-use telemetry follows informed, voluntary, locally stored practice (S3 applied to the research itself); when L3 launches, the full pipeline of ethics review and informed consent is added; the LLM agents' bias lineage and the validation battery appear in the Supplementary Material.

---

<!-- RW-DONE §16 -->

## 16 Governance and Ethics

### 16.1 The Audit Architecture (Who Watches the Watchers)

The sovereignty conditions S1–S4 are self-enforcing through the following mechanisms:

- **Code inspectability** (S1): the entire implementation of the objective functional $U$ is available to $R$ in readable form; the term cap $k$ prevents evasion of inspection through complexity;
- **Tamper-proof logging** (S4): all admission, ranking, delivery, and override decisions are written to an append-only log (a hash chain), so that any ex post modification is detectable;
- **Ranking counterfactual tests** (the operationalization of S3): controlled probe items—identical content, differing platform-side variables—are used periodically to verify that the ranking is invariant to third-party variables; this is an executable test of "zero mutual information," not a paper promise;
- **External audit channel**: logs and parameter snapshots can be exported to third-party auditors (community audit of open-source tooling is the strongest form).

### 16.2 Defaults Are Values

The system has no neutral defaults: every default choice among $\tau_m$, $\gamma$, $k_c$, $\rho_0$, $\kappa$, $n_{\max}$ already shapes the user's information environment. Accordingly, three governance clauses apply: (a) all default parameters are public and are accompanied by their simulation basis (the prior table of Section 14); (b) any change to a default parameter is a class-B decision (S2 signature plus a cooling period); (c) first use requires completion of a "values declaration" procedure ($g^{(2)}$, the decision set $D$, the monitoring list, $D_{\mathrm{adv}}$), with no skipping allowed—to skip it is to let the defaults silently act in place of the second-order will.

### 16.3 Contrast with Nudging

Libertarian paternalism (Thaler & Sunstein, 2008) permits the choice architect to design defaults according to "welfare as judged by the architect." SEA's fundamental difference: **the choice architect is the subject's own reflective layer** (the S2 write right), with direction coming from the $g^{(2)}$ declaration rather than from any external conception of the good; the machine only operationalizes (the curriculum rule, no-arbitrage scheduling). An honest statement of the residual risk: the designer of the default parameters remains an "invisible architect"—constrained by the disclosure obligations and simulation basis of 16.2.

### 16.4 Governance Clauses against Metric Capture

The gradient isolation of Proposition 10.1 rules out metric gaming on the fast timescale; the residual slow-timescale channel—persuading $R$ by narrative to approve inflated indicators—is guarded by three governance clauses: (a) **KPI perfection triggers review**—any KPI perfectly met for two consecutive periods triggers a mandatory review of that indicator itself (a Goodhart symptom); (b) slow-timescale proposals must attach **pointers to raw data** (the class-B authenticity condition (b)); pure-summary narrative is rejected; (c) the measurement model of $\hat\theta$ is versioned, with all changes logged.

### 16.5 The Reliability of the Tool Itself

LLM judges make mistakes (error rates on news-fact-type answers are empirically documented). The symmetry principle: **the primary-source rule constrains the system's own output equally**—(a) every conclusion of the system carries a click-verifiable citation (a system-side extension of the provenance tree); (b) ten items per week are manually spot-checked (random plus high-risk stratification), with the error rate entered into the audit log; (c) system output enjoys no credibility exemption: system assertions entering $K$ undergo the same credibility assessment as external testimony ($c_i$ is calibrated for the system's own output as well); (d) prediction questions are generated by the system but answered independently by the human (the measurement integrity of Proposition 10.2).

### 16.6 Dual Use, Fairness, and Collective Risk

- **Dual use**: sovereign tools can equally be used by the dogmatic to efficiently construct personal echo chambers. Response: the framework's built-in countermeasures are structural—the tolerance-radius curriculum (Definition 10.2) is on by default, and turning it off is an explicit class-B decision (logged); the public layer is on by default (opt-out rather than opt-in); but this paper acknowledges that **the sovereignty principle ultimately respects the subject's freedom of self-destruction** (Elster's sour-grapes problem cannot be solved by a tool); the framework's guarantee is "informed, logged, reversible."
- **Fairness**: if sovereign tools become the exclusive preserve of paying elites, cognitive stratification will solidify into a new dimension of inequality. Mitigation: open-source tooling + local deployment (no subscription dependence) + the public layer as a universal floor of shared reality (the social function of Section 12 here acquires a distributive-justice meaning).
- **Collective-coercion risk**: any institution (state, corporation) that mandates a particular $g^{(2)}$ template violates I2 (the write right belongs to the individual reflective layer). The political implication of this framework is defensive: what it defines is **an inalienable minimum of cognitive autonomy**, not any project of collective epistemological engineering.

---

<!-- RW-DONE §17 -->

## 17 Limitations and Open Problems

### 17.1 Limitations (A List of Idealizations)

1. **The idealization of the independence assumption** (R2): Theorem 7.1 relies on the conditional independence of source classes; in reality, shared dependence on wire services induces correlation. Pricing: the $k_{\mathrm{eff}}$ bound of Theorem 7.2 (tight, Proposition 7.1); mitigation: grouping by ownership, geography, and type; test: the correlation-shock stress test of 14.5(a).
2. **The validity of virtue measurement**: the AOT and intellectual-humility scales are self-reports and are subject to social-desirability bias. Mitigation: cross-validation by behavioral proxies (10.1); residue: when $\sigma_\theta$ is underestimated, the steady-state bound of Theorem 10.2 is underestimated as well.
3. **The reliability of the tool itself**: LLM scoring and judging make mistakes (16.5). Residue: calibration errors in $d'$ and $\rho_m$ propagate into the bounds of Theorems 6.1/9.2—the bounds are updated with measured parameters, not with wishes.
4. **Residual risk of value capture**: the anti-Goodhart clauses are constructive protection, but the slow-timescale human-approval step can still be persuaded by indicator narratives (16.4).
5. **The paternalism objection**: all "directions of the good" in the framework come from the subject's second-order declarations, and the designer injects no substantive values; but defaults are values (16.2–16.3).
6. **The geographic bias of the literature**: the evidence on bubbles and misinformation comes mostly from Western contexts—the parameters $p_{\min}$, $\rho_c$, and the backfire effect may all be culturally specific; the measurement experiments should be replicated in multi-cultural samples (starting from 15.1).
7. **The computational intractability of VOI**: exact EIG is generally incomputable (#P-hard cases exist); the submodular greedy of Theorem 8.2 gives the $(1-1/e)$ guarantee, but the estimation error of $I(Y_Q;\omega|K)$ itself is not covered by the bound—the actual size of the approximation gap is a simulation task (P6).
8. **The stationarity assumption**: Pandora (Proposition 8.1) and the MVT (Proposition 8.2) assume stationary payoff distributions, whereas real source quality drifts. Mitigation: rolling estimation + CUSUM drift detection (the note in 8.3); restless-bandit scheduling (8.6) is heuristic, and its asymptotic optimality holds only in the many-armed limit (Weber & Weiss, 1990).
9. **The curriculum-drift assumption C1 is not directly testable**: $c_0, b_0$ are properties of the drift function and cannot be calibrated before deployment. Mitigation: randomized A/B comparison over multiple curriculum candidates within the tolerance band (the curriculum rule itself is experimentable); the shape of the convergence trajectory is a falsifiable prediction (P11), and failure of the drift assumption manifests as non-convergence—captured by H1' (the agent cohorts) and by H1 of the postponed L3.
10. **Detection independence** (F2): coordinated attacks make leakage correlated. Mitigation: payload-fingerprint cluster counting + aggregate-calibration monitoring (the note in 9.2); the 14.5(b) stress test.
11. **Exogenous adoption rate**: Theorem 9.3 treats $\sigma$ as a parameter; real adoption is endogenous (users decide adoption by the quality of the ecology, producers decide strategy by $\sigma$)—two-sided feedback may generate multiple equilibria or oscillation; this framework gives only the phase-transition point at fixed $\sigma$.
12. **The reflexivity of decision-set declaration and the elicitation burden of $g^{(2)}$**: the quality of $E^*$ and $w$ depends on the subject's self-knowledge, while $g^{(2)}$ itself evolves; certain experiences irreversibly change the subject (transformative experience, Paul, 2014), rendering the ex ante declared $\theta^*$ ex post invalid. Furthermore, the SAP requires the subject to declare $D$, $u_d$, $h_d$, $\varepsilon_c$, $D_{\mathrm{adv}}$—an enormous elicitation burden that an ordinary subject cannot directly supply (the elicitation note in §5.3 provides the explicitness tiering, the quarterly-revision iteration, and the connection to the CIRL literature, but a complete formalization has not been carried out). Mitigation: the quarterly goal-revision meeting (class C) manages $g^{(2)}$ explicitly as a slow variable; the framework does not pretend that preferences are static.
13. **The boundaries of formalization**: the metric $D$ characterizes drift in weight space and does not cover deep transformations of belief structure (a worldview-level update is not a weight perturbation); the three virtue dimensions $(\theta_{\mathrm{cal}}, \theta_{\mathrm{open}}, \theta_{\mathrm{hum}})$ are a coarse-grained projection, and the richness of virtue ethics cannot be fully operationalized (the warning of Vallor, 2016)—what this paper claims is a "measurable lower bound," not a "complete characterization."
14. **Simulation fidelity and circularity**: the demographic bias of LLM agents (overrepresenting the highly educated; P5 has the lowest profile fidelity), over-compliance, and over-rationality systematically compress the $g^{(1)}$–$g^{(2)}$ separation and distort $\delta$-type effects—simulation conclusions must be accompanied by "replay of published human experiments" validation (H8) and are uniformly labeled as conditional conclusions; correlated errors within the same model family create the circularity risk of "the scorer and the subject corroborating each other," blocked by the model-separation principle (§15.2) and real-corpus ground truth (§14.7); the **human version** of P11 (sublimation/backfire) must not take agent experiments alone as a basis for passing (Proposition 10.2 self-referentially implies this: judgments made by proxy cannot measure human calibration). For the three-tier architecture and the zero-recruitment checklist see the Supplementary Material.
15. **The external validity of the symmetry argument**: what the agent cohorts validate is the theory's vehicle-neutral mechanisms and their AI instantiation; transfer to humans relies on the symmetry argument (§3.3, §9.3) + the online human anchors (H8–H9), and this is **an evidence-supported hypothesis, not a proved fact**—the exact value of $\delta_{\mathrm{human}}$ and the formation of human virtue both remain unverified until the postponed RCT (§15.5) is completed; every human-side statement of the paper is phrased as "prediction" rather than "result."

### 17.2 Open Problems

- **O1**: the endogenization of $\sigma$—the two-sided dynamics of the adoption game and the information ecology; the stability of the phase-transition point $\sigma^*$ under feedback;
- **O2**: rate–distortion theory on the proposition graph—deriving the exact distortion–rate function $D(R)$ for structured sources (redundancy, power-law criticality), upgrading the combinatorial lower bound of Proposition 6.2 to an information-theoretic lower bound;
- **O3**: privacy-preserving federated estimation of $k_{\mathrm{eff}}/p_{\min}$—multiple subjects jointly calibrating the redundancy parameters without sharing consumption logs (the parameters of the public layer are a public good);
- **O4**: a public calibration library for $\delta$—a dataset of single-item effect sizes for emotional hijacking and prompt injection (a cross-infrastructure of psychometrics × adversarial machine learning);
- **O5**: multi-agent curriculum interaction—the joint design of the public layer $\gamma$, the tolerance radius, and group polarization: the aggregate social-level effect of individual sublimation curricula;
- **O6**: cross-vehicle transfer conditions for the theorems—which parameters ($\delta$, $c_0$, the attainable range of $d'$, impulse intensity, gating delay) are vehicle-invariant and which must be re-measured per vehicle: building a "transfer-coefficient" library (H8–H9 are its first entries; in both directions, AI→human and human→AI).
- **O7**: certification statistics robust to attention capture—upgrading public-layer attestation from "raw class-coverage counting" to a relative-scarcity/quality-weighted design, and its game equilibrium under adversarial attention inflation (coverage farming) (empirical progress: raw-count attestation fails on a real news ecology, lift 0.63×; quality-weighted surprise attestation partially recovers to 1.23× (weak enrichment), §12.2; remaining: a formal game-theoretic analysis of equilibrium under coverage-farming attacks).
- **O8**: a composed error-propagation bound for the decomposition solution of the SAP—how the per-layer approximation guarantees of Sections 6–8 (the greedy ratio, the miss bound, the threshold structure, the no-arbitrage equilibrium) compose, under coupling through the shared budget and the knowledge state, into a global approximation ratio or regret bound; if a general theorem is unattainable, characterize a family of sufficient conditions under which the guarantees compose (e.g., error additivity under weak coupling).

---

<!-- RW-DONE §18 -->

## 18 Research Roadmap and Conclusion

### 18.1 Research Roadmap

This paper is the theory-founding link of the following research roadmap:

1. **Theory foundation (this paper)**: the assumption system, complete proofs, push+pull unification (the SAP), the separability bottleneck and the dual-channel architecture, attention no-arbitrage, the falsifiable checklist;
2. **Algorithm design**: proposition-graph construction, the dual-channel selector (greedy + threshold), the EIG query planner, Whittle/Pandora schedulers, the marginal-VOI budget allocator, and the symbolic specification of the firewall and the cooling queue (a reference implementation with dual-domain real-data validation already exists; see the Supplementary Material);
3. **Simulations and LLM-agent cohort experiments**: §14–15 (P1–P12, H1'–H9), producing the prior table of default parameters (for pilot status see Table 14-1);
4. **Online human-data anchors and controlled telemetry** (the transfer bridge): §15.3;
5. **Instantiated deployment**: filling in the personal parameters (the $g^{(2)}$ declaration, the decision set, the monitoring list, $D_{\mathrm{adv}}$) and entering the normal "audit–revise" operation (the reference implementation has passed a first engineering-feasibility check on real information streams; see the Supplementary Material);
6. **Human RCT (postponed)**: the §15.5 protocol is archived; launch when external collaboration is in place or direct human-side evidence becomes necessary.

### 18.2 Conclusion

This paper reconstructs the slogan "amid the flood of information, acquire information that benefits oneself with maximal efficiency and initiative" into a framework with explicit premises, conditional theorems, and falsifiable predictions. **Its proper positioning is as a framework/synthesis paper**: all theorems are correct applications of standard tools to the structures we posit; the contributions lie in the system integration, the formalization of the sovereignty conditions S1–S4, and the argumentative organization of the claim that "high recall is a structural property, not a scoring property." The core results compress into a single logical chain:

**Arithmetic** (Premises 1–2) forces us to filter out 99.8%; **sovereignty** (Premise 3, S1–S4) determines for whom filtering and acquisition work; **structure** (the separability bottleneck of Theorem 6.1 + the redundancy coverage of Theorems 7.1–7.4) proves that high recall can only be borne by architecture, not by scoring—and that this guarantee is conditional, its strength depending on the institutional provenance of the coverage floor and on quota matching (§7.7), while the raw material of the architecture is active acquisition—the monitoring list, source exploration, query design (Section 8); **unified pricing** (the attention no-arbitrage of Theorem 8.1) places push, pull, and reflection under a single shadow price, making "proactivity" a computable optimality condition; **adversariality** (Theorems 9.1–9.3) gives safety a design bound calibratable by measurement, and gives the critical adoption rate at which universalized individual protection flips the producer ecology; **sublimation** (Theorem 10.1) writes "becoming a better person" as a convergence theorem of a human-gated dynamical system; **exception and publicness** (Theorems 11.1–11.2, 12.1) give emergency power the legitimacy of a Ulysses contract, and give universal personalization a lower bound of shared reality.

The evidence boundary is as wide as the claims: **all human-side conclusions are falsifiable predictions** (the human RCT is postponed, §15.5); the cohort-level main validation (the full P1–P12 table) is in progress, with the pre-registered sample size not yet reached; what the LLM-agent cohorts validate is the vehicle-neutral mechanisms and their AI instantiation—H8/H9 have already shown systematic cross-family divergence, and transfer to humans is an evidence-supported hypothesis, not a proved fact (§17, Limitation 15). Every link is falsifiable (Section 13), and every link has a contingency plan for its failure mode (Section 17). The completed dual-domain pilots have both reinforced the pivot theorems (the separability bottleneck confirmed in two domains on two independent feature families) and mapped the applicability-domain boundaries (the strong form of high recall is rejected in the academic domain and conditionally holds in the financial domain; public-layer attestation at one point failed and was partially recovered by engineering)—these boundaries have themselves become part of the framework's content (§7.7, §12.2).

The information environment is not an environment—it is the subject in the making. The task of this paper is to provide, for the eternal question "what kind of person to become," a mathematically honest instrumental foundation that belongs to the subject themself: not to answer on the subject's behalf, but to guarantee that the write right, the audit right, and the revision right over the answer remain forever in the subject's hands.

---

<!-- RW-DONE 可用性 -->

## Data and Code Availability

All simulation and experimental code of this paper (the pilot environment, the three-family replay pipelines, the algorithm reference implementation, the deployment pipeline), the analysis pipelines, and the result data are publicly archived with the paper: the public version carries the repository link, the Zenodo DOI, and the commit hash; **if the target journal requires double-blind review, the review version will instead carry an anonymized repository and an anonymous OSF link** (the current version of this paper is in attributed-submission form; the two forms are not used simultaneously—the corresponding links will be provided as soon as the editorial office specifies the form). The derived datasets (the arXiv 2019-09 corpus, the EDGAR disclosure propositions, the CDX layer of public news archives, Wikimedia pageviews, the Manifold human-calibration anchors, the H8/H9 batteries, and the three-family replay records) can be deterministically reconstructed from public sources (the arXiv API, EDGAR, archive.org CDX, Wikimedia REST, OpenAlex, the Manifold API) with the accompanying scraping scripts, with fixed random seeds. JSON/CSV summary tables and decision rules for the key experiments are provided with the Supplementary Material. Consistency-audit scripts (numbered cross-references, bibliography closure, reconciliation of key figures, table completeness) are released with the code. Pre-registration documents (hypotheses, environment snapshots, seeds, analysis plans) are archived on OSF, with the link provided in the public version.

<!-- TR-DONE 参考文献：条目原样保留，中文注记已英译 -->

## References

1. Ainslie, G. (1992). *Picoeconomics: The Strategic Interaction of Successive Motivational States Within the Person*. Cambridge University Press.
2. Allen, J., Howland, B., Mobius, M., Rothschild, D., & Watts, D. J. (2020). Evaluating the fake news problem at the scale of the information ecosystem. *Science Advances*, 6(14), eaay3539.
3. Aumann, R. J. (1976). Agreeing to disagree. *The Annals of Statistics*, 4(6), 1236–1239.
4. Bail, C. A., Argyle, L. P., Brown, T. W., Bumpus, J. P., Chen, H., Hunzaker, M. B. F., Lee, J., Mann, M., Merhout, F., & Volfovsky, A. (2018). Exposure to opposing views on social media can increase political polarization. *PNAS*, 115(37), 9216–9222.
5. Baron, J. (2008). *Thinking and Deciding* (4th ed.). Cambridge University Press.
6. Bertsekas, D. P., & Shreve, S. E. (1978). *Stochastic Optimal Control: The Discrete Time Case*. Academic Press.
7. Blackwell, D. (1953). Equivalent comparisons of experiments. *The Annals of Mathematical Statistics*, 24(2), 265–272.
8. Borkar, V. S. (1997). Stochastic approximation with two time scales. *Systems & Control Letters*, 29(5), 291–294.
9. Borkar, V. S. (2008). *Stochastic Approximation: A Dynamical Systems Viewpoint* (2nd ed.). Cambridge University Press.
10. Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3.
11. Broadbent, D. E. (1958). *Perception and Communication*. Pergamon Press.
12. Buchanan, A. E., & Brock, D. W. (1990). *Deciding for Others: The Ethics of Surrogate Decision Making*. Cambridge University Press.
13. Chan, M. S., & Albarracín, D. (2023). A meta-analysis of correction effects in science-relevant misinformation. *Nature Human Behaviour*, 7, 1164–1173.
14. Chan, M. S., Jones, C. R., Hall Jamieson, K., & Albarracín, D. (2017). Debunking: A meta-analysis of the psychological efficacy of messages countering misinformation. *Psychological Science*, 28(11), 1544–1550.
15. Chang, W., Chen, E., Mellers, B., & Tetlock, P. (2016). Developing expert political judgment: The impact of training and practice on judgmental accuracy in geopolitical forecasting tournaments. *Judgment and Decision Making*, 11(5), 509–526.
16. Charnov, E. L. (1976). Optimal foraging, the marginal value theorem. *Theoretical Population Biology*, 9(2), 129–136.
17. Chaloner, K., & Verdinelli, I. (1995). Bayesian experimental design: A review. *Statistical Science*, 10(3), 273–304.
18. Clark, A., & Chalmers, D. (1998). The extended mind. *Analysis*, 58(1), 7–19.
19. Coady, C. A. J. (1992). *Testimony: A Philosophical Study*. Oxford University Press.
20. Coalition for Content Provenance and Authenticity (C2PA). (2021). *Technical Specification*.
21. Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
22. Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87–114.
23. Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *Journal of Experimental Psychology: General*, 144(1), 114–126.
24. Ebbinghaus, H. (1885). *Über das Gedächtnis: Untersuchungen zur experimentellen Psychologie*. Duncker & Humblot.
25. Ecker, U. K. H., Lewandowsky, S., Cook, J., Schmid, P., Fazio, L. K., Brashier, N., Kendeou, P., Vraga, E. K., & Amazeen, M. A. (2022). The psychological drivers of misinformation belief and its resistance to correction. *Nature Reviews Psychology*, 1, 13–29.
26. Elish, M. C. (2019). Moral crumple zones: Cautionary tales in human-robot interaction. *Engaging Science, Technology, and Society*, 5, 40–60.
27. Elster, J. (1979). *Ulysses and the Sirens: Studies in Rationality and Irrationality*. Cambridge University Press.
28. Elster, J. (1983). *Sour Grapes: Studies in the Subversion of Rationality*. Cambridge University Press.
29. Fazio, L. K., Brashier, N. M., Payne, B. K., & Marsh, E. J. (2015). Knowledge does not protect against illusory truth. *Journal of Experimental Psychology: General*, 144(5), 950–958.
30. Ferguson, T. S. (2006). *Optimal Stopping and Applications*. Springer.
31. Festinger, L. (1957). *A Theory of Cognitive Dissonance*. Stanford University Press.
32. Frankfurt, H. (1971). Freedom of the will and the concept of a person. *The Journal of Philosophy*, 68(1), 5–20.
33. Gentzkow, M., & Shapiro, J. M. (2011). Ideological segregation online and offline. *The Quarterly Journal of Economics*, 126(4), 1799–1849.
34. Gittins, J. C. (1979). Bandit processes and dynamic allocation indices. *Journal of the Royal Statistical Society: Series B*, 41(2), 148–177 (with discussion).
35. Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359–378.
36. Goodhart, C. A. E. (1984). *Monetary Theory and Practice: The U.K. Experience*. Macmillan.
37. Green, D. M., & Swets, J. A. (1966). *Signal Detection Theory and Psychophysics*. Wiley.
38. Grinberg, N., Joseph, K., Friedland, L., Swire-Thompson, B., & Lazer, D. (2019). Fake news on Twitter during the 2016 U.S. presidential election. *Science*, 363(6425), 374–377.
39. Guess, A., Nagler, J., & Tucker, J. (2019). Less than you think: Prevalence and predictors of fake news dissemination on Facebook. *Science Advances*, 5(1), eaau4586.
40. Guess, A., Malhotra, N., Pan, J., Barberá, P., Allcott, H., Brown, T., Dimmery, A., Moehler, D., Nyhan, B., Tucker, J. A., & Bonneau, R. (2023). How do social media feed algorithms affect attitudes and behavior in an election campaign? *Science*, 381(6656), 398–404.
41. Habermas, J. (1989). *The Structural Transformation of the Public Sphere* (T. Burger, Trans.). MIT Press. (Original work published 1962)
42. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. *Journal of the American Statistical Association*, 58(301), 13–30.
43. Howard, R. A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics*, 2(1), 22–26.
44. Kahan, D. M. (2017). Misconceptions, misinformation, and the logic of identity-protective cognition. *Cultural Cognition Project Working Paper* No. 264.
45. Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
46. Khuller, S., Moss, A., & Naor, J. (1999). The budgeted maximum coverage problem. *Information Processing Letters*, 70(1), 39–45.
47. Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research*, 9, 235–284.
48. Krumrei-Mancuso, E. J., & Rouse, S. V. (2016). The development and validation of the Comprehensive Intellectual Humility Scale. *Journal of Personality Assessment*, 98(2), 202–214.
49. Lazer, D. M. J., Baum, M. A., Benkler, Y., Berinsky, A. J., Greenhill, K. M., Menczer, F., Metzger, M. J., Nyhan, B., Pennycook, G., Rothschild, D., Schudson, M., Sloman, S. A., Sunstein, C. R., Thorson, E. A., Watts, D. J., & Zittrain, J. L. (2018). The science of fake news. *Science*, 359(6380), 1094–1096.
50. Levine, T. R. (2014). Truth-default theory (TDT): Accounting for the effects of deception detection research. *Journal of Language and Social Psychology*, 33(4), 378–392.
51. Lewandowsky, S., Ecker, U. K. H., Seifert, C. M., Schwarz, N., & Cook, J. (2012). Misinformation and its correction: Continued influence and successful debiasing. *Psychological Science in the Public Interest*, 13(3), 106–120.
52. Lindley, D. V. (1956). On a measure of the information provided by an experiment. *The Annals of Mathematical Statistics*, 27(4), 986–1005.
53. Liu, Y., Deng, G., Li, Z., Wang, K., Wang, Z., Zhang, T., Fan, L., Wang, H., Zhang, L., & Liu, Y. (2024). Formalizing and benchmarking prompt injection attacks and defenses. In *Proceedings of the 33rd USENIX Security Symposium*.
54. Logg, J. M., Minson, J. A., & Moore, D. A. (2019). Algorithm appreciation: People prefer algorithmic to human judgment. *Organizational Behavior and Human Decision Processes*, 151, 90–103.
55. Maćkowiak, B., Matějka, F., & Wiederholt, M. (2023). Rational inattention: A review. *Journal of Economic Literature*, 61(1), 226–273.
56. Matějka, F., & McKay, A. (2015). Rational inattention to discrete choices: A new foundation for the multinomial logit model. *Econometrica*, 83(1), 271–298.
57. McGuire, W. J. (1964). Inducing resistance to persuasion: Some contemporary approaches. *Advances in Experimental Social Psychology*, 1, 191–229.
58. McPherson, M., Smith-Lovin, L., & Cook, J. M. (2001). Birds of a feather: Homophily in social networks. *Annual Review of Sociology*, 27, 415–444.
59. Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*, 63(2), 81–97.
60. Monderer, D., & Samet, D. (1989). Approximating common knowledge with common beliefs. *Games and Economic Behavior*, 1(2), 170–190.
61. Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming*, 14, 265–274.
62. Nguyen, C. T. (2019). Escape the echo chamber. *Aeon*. (See also *Games: Agency as Art*, Oxford University Press, 2020, on value capture)
63. Nguyen, C. T. (2020). Echo chambers and epistemic bubbles. *Episteme*, 17(2), 141–161.
64. Papadimitriou, C. H., & Tsitsiklis, J. N. (1999). The complexity of optimal queueing network control. *Mathematics of Operations Research*, 24(2), 293–305.
65. Pariser, E. (2011). *The Filter Bubble: What the Internet Is Hiding from You*. Penguin Press.
66. Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors*, 39(2), 230–253.
67. Paul, C., & Matthews, M. (2016). *The Russian "Firehose of Falsehood" Propaganda Model*. RAND Corporation.
68. Paul, L. A. (2014). *Transformative Experience*. Oxford University Press.
69. Pennycook, G., & Rand, D. G. (2019). Lazy, not biased: Susceptibility to partisan fake news is better explained by lack of reasoning than by motivated reasoning. *Cognition*, 188, 39–50.
70. Pennycook, G., & Rand, D. G. (2022). Accuracy prompts are a replicable and generalizable approach to reducing the spread of misinformation. *Nature Communications*, 13, 1732.
71. Pirolli, P., & Card, S. (1999). Information foraging. *Psychological Review*, 106(4), 643–675.
72. Resnick, S. I. (1987). *Extreme Values, Regular Variation, and Point Processes*. Springer.
73. Robbins, H., & Siegmund, D. (1971). A convergence theorem for nonnegative almost supermartingales and some applications. In *Optimizing Methods in Statistics* (pp. 233–257). Academic Press.
74. Roozenbeek, J., & van der Linden, S. (2019). The fake news game: Actively inoculating against the risk of misinformation. *Palgrave Communications*, 5, 13.
75. Savage, L. J. (1951). The theory of statistical decision. *Journal of the American Statistical Association*, 46(253), 55–67.
76. Settles, B. (2009). *Active Learning Literature Survey* (Computer Sciences Technical Report 1648). University of Wisconsin–Madison.
77. Shumailov, I., Shumilo, Z., Zhao, Y., Gal, Y., Papernot, N., Anderson, R., Shejwalkar, V., Houmansadr, A., & Smith, R. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.
78. Simon, H. A. (1955). A behavioral model of rational choice. *The Quarterly Journal of Economics*, 69(1), 99–118.
79. Simon, H. A. (1971). Designing organizations for an information-rich world. In *Computers, Communications, and the Public Interest*. Johns Hopkins Press.
80. Sims, C. A. (2003). Implications of rational inattention. *Journal of Monetary Economics*, 50(3), 665–690.
81. Sparrow, B., Liu, J., & Wegner, D. M. (2011). Google effects on memory: Cognitive consequences of having information at our fingertips. *Science*, 333(6043), 776–778.
82. Stanovich, K. E., & West, R. F. (1997). Reasoning independently of prior belief and individual differences in actively open-minded thinking. *Journal of Educational Psychology*, 89(2), 342–357.
83. Stigler, G. J. (1961). The economics of information. *Journal of Political Economy*, 69(3), 213–225.
84. Stroud, N. J. (2011). *Niche News: The Politics of News Choice*. Oxford University Press.
85. Sunstein, C. R. (2017). *#Republic: Divided Democracy in the Age of Social Media*. Princeton University Press.
86. Sviridenko, M. (2004). A note on maximizing a submodular set function subject to a knapsack constraint. *Operations Research Letters*, 32(1), 41–43.
87. Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257–285.
88. Thaler, R. H., & Shefrin, H. M. (1981). An economic theory of self-control. *Journal of Political Economy*, 89(2), 392–406.
89. Thaler, R. H., & Sunstein, C. R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press.
90. Vallor, S. (2016). *Technology and the Virtues: A Philosophical Guide to a Future Worth Wanting*. Oxford University Press.
91. van der Linden, S. (2022). *Foolproof: Why Misinformation Infects Our Minds and How to Build Immunity*. W. W. Norton.
92. Vosoughi, S., Roy, D., & Aral, S. (2018). The spread of true and false news online. *Science*, 359(6380), 1146–1151.
93. Weber, R. R., & Weiss, G. (1990). On an index policy for restless bandits. *Journal of Applied Probability*, 27(3), 637–648.
94. Weitzman, M. L. (1979). Optimal search for the best alternative. *Econometrica*, 47(3), 641–654.
95. Whittle, P. (1988). Restless bandits: Activity allocation in a changing world. *Journal of Applied Probability*, 25(A), 287–298.
96. Williams, J. (2018). *Stand Out of Our Light: Freedom and Resistance in the Attention Economy*. Cambridge University Press.
97. Wineburg, S., & McGrew, S. (2019). Lateral reading and the nature of expertise: Reading less and learning more when evaluating digital information. *Teachers College Record*, 121(11), 1–40.
98. Wu, T. (2016). *The Attention Merchants: The Epic Scramble to Get Inside Our Heads*. Knopf.
99. Zagzebski, L. (2012). *Epistemic Authority: A Theory of Trust, Authority, and Autonomy in Belief*. Oxford University Press.
100. Zuboff, S. (2019). *The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power*. PublicAffairs.
101. Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *American Economic Review*, 110(3), 629–676.
102. Allcott, H., Gentzkow, M., & Song, L. (2022). Digital addiction. *American Economic Review*, 112(7), 2424–2463.
103. Bakshy, E., Messing, S., & Adamic, L. A. (2015). Exposure to ideologically diverse news and opinion on Facebook. *Science*, 348(6239), 1130–1132.
104. Bozdag, E., & van den Hoven, J. (2015). Breaking the filter bubble: Democracy and design. *Ethics and Information Technology*, 17(4), 249–265.
105. Buchbinder, N., Feldman, M., Naor, J., & Schwartz, R. (2014). Submodular maximization with cardinality constraints. In *Proceedings of the 25th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)*, 1433–1452.
106. Călinescu, G., Chekuri, C., Pál, M., & Vondrák, J. (2011). Maximizing a monotone submodular function subject to a matroid constraint. *SIAM Journal on Computing*, 40(6), 1740–1766.
107. Caplin, A., Dean, M., & Leahy, J. (2019). Rational inattention, optimal consideration sets, and stochastic choice. *Review of Economic Studies*, 86(3), 1061–1094.
108. Doval, L. (2018). Whether or not to open Pandora's box. *Journal of Economic Theory*, 175, 127–158.
109. Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec)*, 79–90.
110. Helberger, N., Karppinen, K., & D'Acunto, L. (2018). Exposure diversity as a design principle for recommender systems. *Information, Communication & Society*, 21(2), 191–207.
111. Kleinberg, J., & Raghavan, M. (2021). Algorithmic monoculture and social welfare. *Proceedings of the National Academy of Sciences*, 118(22), e2018340118.
112. Kleinberg, J., Mullainathan, S., & Raghavan, M. (2024). The challenge of understanding what users want: Inconsistent preferences and engagement optimization. *Management Science*, 70(9), 6336–6358.
113. Leskovec, J., Krause, A., Guestrin, C., Faloutsos, C., VanBriesen, J., & Glance, N. (2007). Cost-effective outbreak detection in networks. In *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 420–429.
114. Olszewski, W., & Weber, R. (2015). A more general Pandora rule? *Journal of Economic Theory*, 160, 429–437.
115. Stray, J., Vendrov, I., Nixon, J., Adler, S., & Hadfield-Menell, D. (2022). Building human values into recommender systems: An interdisciplinary synthesis. *arXiv:2207.10192*. (Revised version in *ACM Transactions on Recommender Systems*, 2024)
116. Zhong, W. (2022). Optimal dynamic information acquisition. *Econometrica*, 90(4), 1537–1582.
117. Dalvi, N., Domingos, P., Mausam, Sanghai, S., & Verma, D. (2004). Adversarial classification. In *Proceedings of the 10th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 99–108.
118. Lowd, D., & Meek, C. (2005). Adversarial learning. In *Proceedings of the 11th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 641–647.
119. Biggio, B., & Roli, F. (2018). Wild patterns: Ten years after the rise of adversarial machine learning. *Pattern Recognition*, 84, 317–331.
120. Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., ... & Perez, E. (2023). Towards understanding sycophancy in language models. *arXiv:2310.13548*.
121. Hadfield-Menell, D., Russell, S. J., Abbeel, P., & Dragan, A. (2016). Cooperative inverse reinforcement learning. In *Advances in Neural Information Processing Systems 29 (NeurIPS)*.
122. Hadfield-Menell, D., Dragan, A., Abbeel, P., & Russell, S. (2017). The off-switch game. In *Proceedings of the 26th International Joint Conference on Artificial Intelligence (IJCAI)*, 220–227.
123. Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence: Models, analysis and simulation. *Journal of Artificial Societies and Social Simulation*, 5(3).
124. Deffuant, G., Neau, D., Amblard, F., & Weisbuch, G. (2000). Mixing beliefs among interacting agents. *Advances in Complex Systems*, 3(1–4), 87–98.
125. Nan, Q., Cao, J., Zhu, Y., Wang, Y., & Li, J. (2021). MDFEND: Multi-domain fake news detection (the Weibo21 dataset). In *Proceedings of the 30th ACM International Conference on Information and Knowledge Management (CIKM)*, 3338–3342.
126. Augenstein, I., Lioma, C., Wang, D., Chaves Lima, L., Hansen, C., Hansen, C., & Simonsen, J. G. (2019). MultiFC: A real-world multi-domain dataset for evidence-based fact checking of claims. In *Proceedings of EMNLP-IJCNLP 2019*, 4685–4697.

---

<!-- RW-DONE 附录A -->

## Appendix A Notation

The same symbol is used under local conventions in different chapters (standard mathematical practice). The table below gives a global index, and the **conflicting-symbol disambiguation table** that follows lists, item by item, the senses and scopes of the reused symbols—when reading any formula, the sense of its chapter prevails.

| Symbol | Meaning | First appearance |
|---|---|---|
| $T$; $T_{\mathrm{pull}}, T_{\mathrm{push}}, T_{\mathrm{ref}}$ | the per-period cognitive budget and its three-way split | Premise 1; Definition 4.7 |
| $N, \lambda, \bar t$ | candidate supply, arrival rate, average consumption cost | Premise 2 |
| $X, x_i, \phi(x_i)$ | the information flow, an item, the five-dimensional feature vector | Definition 4.1 |
| $E, e_j, D_e, \kappa, \rho_c$ | proposition set, proposition, its document set, the collapsing map, the collapse ratio | Definitions 4.2–4.3 |
| $\mathcal{C}_i, Z_i(e), p_{\min}, k, k_{\mathrm{eff}}$ | source class, coverage event, coverage floor, number of monitored classes, effective number of independent classes | Definition 4.4; Theorems 7.1–7.2 |
| $\mathcal{A}=(C,G,K,\theta,R)$ | the agent five-tuple | Definition 4.5 |
| $g^{(1)}, g^{(2)}$ | first-order preferences / second-order will | Premise 3 |
| $D$ (Chapters 4–6, 8); $E^*$ | the active decision set; the critical-proposition set | Definition 4.6 |
| $\pi=(\pi_{\mathrm{mon}},\pi_{\mathrm{pull}},\pi_{\mathrm{push}},\pi_{\mathrm{del}},\pi_{\mathrm{esc}})$ | the policy five-tuple | Definition 4.7 |
| $\mathrm{VOI}, c_i, \pi_d(i), h_i, \lambda_d$ | value of information, credibility, decision relevance, time gap, durability scale | Theorem 5.1 |
| $\sigma_1 \succeq_B \sigma_2$ | Blackwell informativeness ordering ($\sigma_2$ is a garbling of $\sigma_1$: $\sigma_2 = \sigma_1 \circ K$) | Appendix B.5(ii) |
| $\mathcal{D}, \mathcal{D}^*$ | critical-value leakage (distortion) and its lower bound | Definition 6.1; Proposition 6.2 |
| $\beta, \pi$ (local to Chapter 6), $d'$, $R$ (local to Chapter 6) | consumption rate, critical fraction, score separability, recall | Theorem 6.1 |
| $U, U_{\mathrm{cov}}, U_{\mathrm{div}}, U_{\mathrm{mon}}$ | selection utility, coverage utility, diversity utility, monitoring-coverage utility | Section 6.3; Definition 7.2 |
| $\nu$ | the shadow price of the budget (the attention no-arbitrage price) | Theorem 8.1 |
| $z_s, X_s, c_e$ | Pandora reservation index, source payoff, exploration cost | Proposition 8.1 |
| $G_s(t), c_{sw}$ | cumulative patch payoff, switching cost | Proposition 8.2 |
| $I(Q), \mathrm{EIG}$ | conditional mutual information of a query batch | Theorem 8.2 |
| $\Delta, D(\tilde U, U), \delta, \rho_m, n_{\max}, \varepsilon_c$ | weight drift, the goal-divergence metric, per-item impact bound, detection recall, exposure cap, tolerance threshold | Definition 9.1; F1–F3 |
| $\sigma, \sigma^*, \Pi_q, \varepsilon_g$ (Chapter 9) | adoption rate, critical adoption rate, producer payoff, firewall leak rate | Theorem 9.3 |
| $\theta=(\theta_{\mathrm{cal}},\theta_{\mathrm{open}},\theta_{\mathrm{hum}}), \theta^*, \hat\theta_t$ | virtue state, declared ideal state, noisy measurement | Definition 10.1 |
| $\rho(\theta), E_t, q_t, a_t$ (Chapter 10) | tolerance radius, exposure set, engagement quality, step size | Definition 10.2; Section 10.1 |
| $c_0, b_0, F(\theta)$ | curriculum-drift constant, drift floor, expected drift | C1 |
| $D_{\mathrm{adv}}=(\mathcal{E},\mathcal{A}_{\mathrm{safe}},\eta,q^*)$ | pre-authorization instruction | Definition 11.2 |
| $R(a,\omega), \succeq_{\mathrm{rev}}$ | regret, the reversibility partial order | Definition 11.4 |
| $P_t, \gamma, k_c, \Omega, J$ | the public layer, its budget share, the number of attestation classes, agenda overlap, Jaccard | Definitions 12.1–12.2 |
| S1–S4; I1–I5; Premises 1–6 | sovereignty conditions; invariants; premises | Definition 5.3; Proposition 3.1; §3.1 |
| R1–R3; F1–F3; C1–C5; (V1)–(V4); (P1)–(P2) | the per-chapter assumption groups (redundancy / firewall / convergence / feature decomposition / concavity-separability) | §7.1; §9.2; §10.3; §5.2; §8.2 |
| P1–P12 | falsifiable propositions (unrelated to Assumptions (P1)–(P2); see the table in Section 13) | §13 |
| H1–H7 | pre-registered experimental hypotheses | §15.4 |

**Conflicting-symbol disambiguation table** (senses and scopes of reused symbols):

| Symbol | Senses and scopes |
|---|---|
| $D$ | (1) the active decision set (Definition 4.6, Chapters 4–6, 8); (2) the goal-divergence metric $D(\tilde U, U)$ (Definition 9.1, Chapter 9); (3) critical-value leakage, written in script as $\mathcal{D}$ (Definition 6.1), distinct from (1) and (2) |
| $\pi$ | (1) the policy five-tuple (Definition 4.7, global); (2) the critical-proposition fraction (Theorem 6.1, Chapter 6 only); (3) decision relevance $\pi_d(i)$ (Theorem 5.1, subscripted); (4) producer payoff, written in uppercase as $\Pi$ (Chapter 9) |
| $\rho$ | (1) the collapse ratio $\rho_c$ (Definition 4.3); (2) detection recall $\rho_m$ (F2); (3) the tolerance radius $\rho(\theta)$ (Definition 10.2)—all three carry subscripts or appear in function form; a bare $\rho$ is never used |
| $\theta$ | (1) the virtue state (Definition 10.1, Chapter 10); (2) the state space, written in uppercase as $\Theta_{\mathrm{rel}}$ (§4.2, §5.2), distinct from (1) |
| $\lambda$ | (1) the arrival rate (Premise 2); (2) the durability scale $\lambda_d$ ((V3)); (3) the manipulation-penalty weight (§6.3); (4) the rational-inattention information price (Proposition 8.3)—(2)–(4) all carry local declarations |
| $\beta$ | (1) the discount factor (SAP, Definition 5.1); (2) the consumption rate (Theorem 6.1, Chapter 6 only); (3) the confidence level $1-\beta$ (Theorem 9.2, Chapter 9 only) |
| $R$ | (1) the reflective layer (Definition 4.5, global); (2) recall (Theorem 6.1, Chapter 6 only); (3) regret $R(a,\omega)$ (Definition 11.4, with arguments) |
| $k$ | (1) the number of monitored source classes (§7.1); (2) the inspectability term cap (S1); (3) the number of attestation classes, written as $k_c$ (Definition 12.1) |
| $\gamma$ | (1) the public-layer budget share (Definition 12.1); (2) the replicator extinction-rate parameter (Proposition 9.2, §9.4 only); (3) the cooling decay rate (the note in §6.4, only there) |
| $c_p$ | (1) the marginal cost of forging a primary source (§9.4, provenance requirement I3); (2) the cost of the preventive action (§11.3–11.4, the two-action closed form)—the two senses never co-occur in the same formula |
| $\Omega$ | (1) the uncertainty set for emergency override (Definition 11.4, Section 11 only); (2) the agenda-overlap index (Definitions 12.1–12.2, Section 12 only) |

---

<!-- RW-DONE 附录B -->

## Appendix B Technical Lemmas

This appendix collects the exact statements of the standard results cited in the main text; except where marked "classical result, for the proof see the original source," complete proofs are given.

### B.1 Hoeffding's Inequality

**Lemma B.1** (Hoeffding, 1963). *Let $B_1,\dots,B_n$ be independent, $B_i \in [0,1]$ a.s., $S_n = \sum_i B_i$. Then for any $u > 0$:*
$$P(S_n - \mathbb{E}S_n \ge u) \ \le\ e^{-2u^2/n}.$$

*Proof sketch* (for the complete derivation see Hoeffding (1963)): apply Markov's inequality to $e^{t(S_n - \mathbb{E}S_n)}$; independence factorizes the moment-generating function; the centered moment-generating function of each $[0,1]$ variable is dominated by $\exp(t^2/8)$ (Hoeffding's lemma, a convexity argument); optimizing over $t$ gives $t = 4u/n$. $\blacksquare$

### B.2 A Stochastic Comparison Lemma (Robbins–Siegmund Type)

**Lemma B.2(i) (the zero-bias case)**. *Let $V_t \ge 0$ be adapted, $\alpha_t \in [0,1)$, $\beta_t \ge 0$ adapted, and*
$$\mathbb{E}[V_{t+1} \mid \mathcal{F}_t] \ \le\ (1-\alpha_t)\,V_t + \beta_t. \tag{B.1}$$
*If $\sum_t \beta_t < \infty$ a.s. and $\sum_t \alpha_t = \infty$ a.s., then $V_t \to 0$ a.s.*

*Proof*. This is the instance of the Robbins–Siegmund theorem (1971, Theorem 1: if $\mathbb{E}[V_{t+1}|\mathcal{F}_t] \le (1+a_t)V_t + b_t - c_t$, where $a_t, b_t, c_t \ge 0$ are adapted, $\sum a_t < \infty$, and $\sum b_t < \infty$ a.s., then $V_t$ converges a.s. to a finite limit and $\sum c_t < \infty$ a.s.) obtained by taking $a_t \equiv 0$, $b_t = \beta_t$, $c_t = \alpha_t V_t$: $V_t$ converges a.s. to some $V_\infty \ge 0$, and $\sum_t \alpha_t V_t < \infty$ a.s. If $P(V_\infty > 0) > 0$, then on that event there exists a (random) $t_0$ such that $V_t \ge V_\infty/2$ for $t \ge t_0$ (by convergence), whence $\sum_t \alpha_t V_t \ge (V_\infty/2)\sum_{t \ge t_0}\alpha_t = \infty$ (since $\sum_t\alpha_t = \infty$), contradicting $\sum_t\alpha_tV_t < \infty$. Hence $V_\infty = 0$ a.s.

The proof of the R–S theorem itself is the standard tail-sum reduction (sketched here for reference): let $B_t := \sum_{s\ge t}\beta_s$ (a.s. finite and $B_t \downarrow 0$), $U_t := V_t + B_t \ge 0$; then $\mathbb{E}[U_{t+1}|\mathcal{F}_t] \le U_t - c_t \le U_t$, i.e., $U$ is a nonnegative almost-supermartingale; the Doob supermartingale convergence theorem gives the a.s. convergence of $U$ (and hence of $V$), and summing $U_{t+1} \le U_t - c_t + (\text{martingale difference})$ along paths, with the martingale-difference part handled by the martingale convergence theorem, gives $\sum c_t < \infty$ a.s. For details see Robbins & Siegmund (1971). $\blacksquare$

**Lemma B.2(ii) (the constant-ratio case)**. *Under (B.1), if there exist a constant $c \ge 0$ and a (random) time $\tau$ such that $\beta_t \le \alpha_t c$ a.s. for $t \ge \tau$, and $\sum_t\alpha_t = \infty$ a.s., then:*

*(a) (the expectation version, elementary) if $\alpha_t$, $\beta_t$ are predictable (e.g., deterministic), then $\limsup_t \mathbb{E}[V_t] \le c$;*

*(b) (the a.s. version) if (B.1) arises from a stochastic-approximation recursion projected onto a compact set—with a Lipschitz mean field, zero conditional noise mean, and conditional second moment $O(a_t^2)$ (i.e., the structure of Theorem 10.1, where $\alpha_t = 2a_tc_0$, $\beta_t = 2a_tb_0 + a_t^2M'$, and projection onto the compact set $[0,1]^3$ guarantees bounded iterates)—then $\limsup_t V_t \le c$ a.s.*

*Proof*. (a) Take full expectations: $\bar V_{t+1} \le (1-\alpha_t)\bar V_t + \alpha_t c$. Let $W_t := \bar V_t - c$; then $W_{t+1} \le (1-\alpha_t)W_t$; iterating gives $W_t \le W_\tau \prod_{s=\tau}^{t-1}(1-\alpha_s)$, and $\sum\alpha_s = \infty$ drives the product to zero ($\prod(1-\alpha_s) \le \exp(-\sum\alpha_s) \to 0$); hence $\limsup_t \bar V_t \le c$.

(b) This is the standard conclusion of the ODE method of stochastic approximation (Borkar, 2008, Chapter 2: compact projection gives bounded iterates; the Lipschitz mean field guarantees that the limiting ODE is well-defined; the Kushner–Clark lemma embeds the limit set of the recursion a.s. in the internally chain-transitive set of the limiting ODE). In Theorem 10.1, the recursion of $V$ is dominated by the ODE $\dot v = -2c_0(v - b_0/c_0)$ (by the C1 drift inequality), all of whose solutions satisfy $\limsup_t v(t) \le b_0/c_0$; taking $c$ to be any constant greater than $b_0/c_0$ gives $\limsup_t V_t \le c$ a.s., and letting $c \downarrow b_0/c_0$ gives the conclusion. The special case $c = 0$ with $\sum\beta_t < \infty$ is already covered by the elementary argument of (i). $\blacksquare$

**Note (usage correspondence)**: in the proof of Theorem 10.1, when $b_0 = 0$ one goes through (i) (purely elementary, $\sum\beta_t = M'\sum a_t^2 < \infty$); when $b_0 > 0$ one goes through (ii)(b) ($\beta_t/\alpha_t = b_0/c_0 + a_tM'/(2c_0) \to b_0/c_0$, so the condition $\beta_t \le \alpha_tc$ holds for any $c > b_0/c_0$ and large $t$). The expectation version (Theorem 10.2) follows from the same comparison as (ii)(a).

### B.3 The Step-Size Dilution Lemma

**Lemma B.3**. *Let $a_t \ge c_a/t$ ($t \ge t_0$, $c_a > 0$), and let the stopping-time sequence $\{t_j\}$ satisfy $t_1 \ge 1$, $t_{j+1} - t_j \le \Delta$. Then $\sum_j a_{t_j} = \infty$, and if $\sum_t a_t^2 < \infty$ then $\sum_j a_{t_j}^2 < \infty$.*

*Proof*. $t_j \le t_1 + (j-1)\Delta$, so $a_{t_j} \ge c_a/(t_1 + (j-1)\Delta)$; the right-hand side is a constant multiple of the harmonic series, which diverges. Square summability: $\sum_j a_{t_j}^2 \le \sum_t a_t^2 < \infty$ (the subsequence sum $\le$ the full sum). $\blacksquare$

### B.4 Submodular Functions and the Greedy $(1-1/e)$ Guarantee

**Definition B.1**. *A set function $f: 2^V \to \mathbb{R}$ is called **submodular** if for all $A \subseteq B \subseteq V$, $i \notin B$: $f(A \cup i) - f(A) \ge f(B \cup i) - f(B)$ (diminishing marginal gains); it is called **monotone** if $A \subseteq B \Rightarrow f(A) \le f(B)$.*

**Lemma B.4** (Nemhauser, Wolsey & Fisher, 1978). *Let $f$ be monotone submodular, $f(\varnothing) = 0$, under the cardinality constraint $|A| \le k$. The greedy sequence $A_0 = \varnothing \subseteq A_1 \subseteq \dots$ (adding at each step the element of maximal marginal gain) satisfies*
$$f(A_k) \ \ge\ \Big(1 - \big(1 - \tfrac1k\big)^k\Big) f(\mathrm{OPT}) \ \ge\ \big(1 - \tfrac1e\big) f(\mathrm{OPT}).$$

*Proof*. Write $O = \mathrm{OPT}$, $|O| \le k$. Monotonicity and submodularity together give the standard upper bound:
$$f(O) \le f(A_i \cup O) \le f(A_i) + \sum_{o \in O}\big[f(A_i \cup o) - f(A_i)\big] \le f(A_i) + k\cdot\big[f(A_{i+1}) - f(A_i)\big],$$
(the first inequality uses monotonicity; the second follows from submodularity applied element by element; the third holds because each single-element gain $\le$ the maximal gain chosen by the greedy rule $= f(A_{i+1}) - f(A_i)$.) Rearranging:
$$f(A_{i+1}) - f(O) \ \ge\ \big(1 - \tfrac1k\big)\big(f(A_i) - f(O)\big).$$
Iterating $k$ times from $f(A_0) = 0$: $f(A_k) \ge \big(1 - (1-\tfrac1k)^k\big) f(O)$; $(1-\tfrac1k)^k \le e^{-1}$ completes the proof. $\blacksquare$

**Knapsack variant** (statement only; for proofs see the original sources): under a cost constraint $\sum_{i\in A} c_i \le B$, the better of density greedy and the best single element attains $\frac12(1-\frac1e)$ (folklore; for the proof see Leskovec et al., 2007); partial enumeration combined with density greedy attains exactly $1-\frac1e$ (Sviridenko, 2004); for the continuous-greedy-plus-rounding framework see Călinescu, Chekuri, Pál & Vondrák (2011).

### B.5 EVPI Nonnegativity and Blackwell's Theorem

**Lemma B.5(i) (nonnegativity of the value of information)**. *For any decision problem and any experiment (signal) $y$:*
$$\mathbb{E}_y\Big[\max_a \mathbb{E}[u(a,\omega)\mid y]\Big] \ \ge\ \max_a \mathbb{E}[u(a,\omega)].$$

*Proof*. Fix $a_0 = \arg\max_a \mathbb{E}[u(a,\omega)]$. For each $y$: $\max_a \mathbb{E}[u\mid y] \ge \mathbb{E}[u(a_0,\omega)\mid y]$. Taking expectations over $y$ and using the law of total expectation (the tower property): the right-hand side $= \mathbb{E}[u(a_0,\omega)] = \max_a \mathbb{E}[u(a,\omega)]$. $\blacksquare$

**Lemma B.5(ii) (Blackwell, 1953, statement)**. *Experiment $\sigma_1$ is more informative than $\sigma_2$ (written $\sigma_1 \succeq_B \sigma_2$: $\sigma_2$ is a garbling of $\sigma_1$, i.e., there exists a Markov kernel such that $\sigma_2 = \sigma_1 \circ K$) if and only if for all decision problems and all utility functions, the expected value of $\sigma_1$ is no lower than that of $\sigma_2$.* (For the proof see Blackwell (1953); Theorem 5.1 uses only its "more informative ⇒ higher value" direction, which is a direct corollary of the data-processing inequality.)

### B.6 Normal-Quantile Reference Table (for Reproducing the Numerics of the Main Text)

| Quantity | Value | Used in |
|---|---|---|
| $\Phi^{-1}(0.95)$ | $1.645$ | Theorem 6.1(iii) |
| $\Phi^{-1}(0.99697)$ ($=\bar\Phi^{-1}(0.00303)$) | $\approx 2.744$ | Theorem 6.1(iv) ($\bar\Phi(2.74)=0.00307$, $\bar\Phi(2.75)=0.00298$, linear interpolation) |
| $\underline{d'}(0.0125, 0.01, 0.95)$ | $\approx 4.39$ | Theorem 6.1(iv) |
| $\Phi(4.39/\sqrt2) = \Phi(3.10)$ | $\approx 0.9990$ | the AUC of Theorem 6.1(iv) |
| recall at $d'=1.5$ ($\beta=0.0125, \pi=0.01$) | $\approx 0.21$ | §6.2, consequence 2 (numerical solution of the mixture tail equation: $z \approx 2.31$, $R = \bar\Phi(0.81)$) |
| recall at $d'=2.5$ (same parameters) | $\approx 0.52$ | §6.2, consequence 2 ($z \approx 2.44$, $R = \bar\Phi(-0.06)$) |
| $0.3^5$ | $2.43\times10^{-3}$ | the numerics of Theorem 7.1 |
| $\gamma/(2-\gamma)$, $\gamma = 0.1 / 0.2 / \frac13$ | $0.053 / 0.111 / 0.200$ | the numerics of Theorem 12.1 |
| per-arm sample size ($d=0.35, \alpha=0.05, 1-\beta_{pow}=0.8$) | $n = 2(1.96+0.84)^2/0.35^2 \approx 128$; with 25% attrition $\to 170$ | §15.2 |

---

*(End of the manuscript · October 2026)*

---

---

<!-- TRANSLATOR NOTES -->
1. **Line 1238 (§14 opening)**: 【已裁决·已修复】双重→三重（threefold），中英同步。原疑点：the original says the experiments "承担双重目的" ("serve a dual purpose") but then enumerates three aims—(a), (b), (c). Rendered literally as "serve a dual purpose"; flagged as a suspected slip (likely "三重" intended). Not corrected.
2. **Line 1388 (§15.2, compute disclosure)**: the family code "ling" ("ling 主力家族全程") appears only here; elsewhere the four families are denoted by the initials O/C/Q/G, and no mapping from "ling" (or "qwen", "nemotron") to the anonymized initials is given in this section. Rendered verbatim ("the ling primary family"); flagged for author review.
3. **Table 14-3, row 2 (market-truth d′)**: caliber A lists two values, "0.60 (with attention signals) / 0.02 (no news layer)," while the same row states that §7.5 "uses the interval 0.54–0.60"; the 0.02 sub-value lies outside that interval and its relationship to the used range is not explained. Translated verbatim; flagged, not corrected.
4. **Line 1290 (§14.3, arm 7)**: "（消融，设计中）" uses the un-bracketed word 设计中 rather than the bracketed three-state label [设计]; rendered as "(ablation, in design)" without brackets, preserving the source's distinction from the formal three-state markers (contrast Table 14-1, where S2d carries the bracketed [design]).
5. **Line 1363 (§15.1, final bullet)**: "§17 局限 15" is rendered "§17, Limitation 15" following the established convention ("Section 17, Limitation 2" in Part 4); note the source's internal numbering of limitations could not be verified from within the assigned range.
6. **Line 1316 (Table 14-1, row 5)**: the ordering "0.443 / 0.534 / 0.514 / 0.519（O/C/Q/G）" is non-monotone across families; verified internally consistent with the post-table paragraph (O 0.443 / C 0.534 / Q 0.514 / G 0.519) and with the abstract range 0.443–0.534. No discrepancy; noted only to document the check.

<!-- —— 以上为 §13–§15 译者注 —— -->

<!-- TRANSLATOR NOTES -->
1. **Line 1454 (§16.4)** 【已裁决·已修复】"结事"→"叙事"（ZH 源已改）。原文疑点：: "拒绝纯汇总结事" — "结事" is not a standard word; it is presumably a typo for "叙事" (narrative), consistent with the clause's antecedent "以叙事说服 $R$". Rendered as "pure-summary narrative is rejected." Flagged, not silently corrected.
2. **Line 1774 (Lemma B.5(ii))**: 【已裁决·已修复】采纳方案 A+B：主语翻转为"σ2 由 σ1 加噪退化而得"（因果方向明确句式），并引入显式 Blackwell 序记号 $\sigma_1 \succeq_B \sigma_2$；附录 A 记号表已补行，§2.1 已挂锚，中英两版同步。原疑点记录：the parenthetical "σ1 是 σ2 的加噪" contradicted the kernel equation ($\sigma_2 = \sigma_1 \circ K$, which makes σ2 the garbling of σ1).
3. **Line 1495 (open problem O6)**: the bullet ends with a full stop "。" while all other O-bullets end with "；"; the content is preserved, and the punctuation inconsistency is noted for the author.
4. **Line 1691 (Appendix A)** 【已裁决·已修复】冲突符号消歧表新增 Ω 行（定义 11.4 不确定集 / 定义 12.1–12.2 议程重叠度），中英同步。原疑点：: $\Omega$ is glossed as "agenda overlap" (Definitions 12.1–12.2), but the same symbol denotes the uncertainty set in Definition 11.4; the conflicting-symbol disambiguation table does not list $\Omega$. Flagged for author review.
5. **Line 1485 (Limitation 14)**: "零招募清单" rendered literally as "zero-recruitment checklist"; the term is not defined within the assigned sections and no expansion was attempted.
6. **Appendix A tables (lines 1665–1709)**: per the character-preservation rule, all mathematics in the symbol columns is verbatim; non-mathematical Chinese annotations inside the symbol columns (e.g., "（第 4–6 章）", "前提 1–6", "、"-separators) were translated as labels, consistent with the established \text{...} precedent.
7. **Line 1496 (O7)**: "lift 0.63×" and "1.23×（弱富集）" retained verbatim as "lift 0.63×" and "1.23× (weak enrichment)"; "刷覆盖" rendered as "coverage farming."
8. **Line 1528 (Data and Code Availability)**: "本文当前版本为署名投稿形态" rendered as "the current version of this paper is in attributed-submission form"; the dual-mode statement (public vs. anonymized) is preserved without editorial simplification.

<!-- —— 以上为 §16–§18/附录 译者注 —— -->

<!-- TRANSLATOR NOTES -->
1. **Line 919 (Proposition 9.1, proof)** 【已裁决·已修复】"至多 m 处翻转"→"入出调换至多 m 对（消费集基数 m）"，界 2mD 不变且论证严格化，中英同步。原疑点：: "每处翻转的效用代价 $\le$ 两条目价值差 $\le 2D$（各自偏移 $\le D$），至多 $m$ 处" — the flip-counting phrase "至多 m 处" ("at most m flips") is loose as stated (pairwise inversions among $m$ consumed items can exceed $m$); the bound $2mD$ itself is correct via per-item accounting (each consumed item's value shifts by $\le 2D$). Rendered literally as "at most $m$ flips"; flagged for author review.
2. **Symbol overloading of $c_p$** 【已裁决·已修复】按本文既定体例（局部复用+消歧表）处理：冲突符号消歧表新增 c_p 行（§9.4 伪造成本 / §11.3–11.4 预防成本），中英同步。原疑点：: in §9.4 (line 948) $c_p$ denotes the marginal cost of forging a primary source, while in §11.3–11.4 (lines 1115–1135) $c_p$ denotes the cost of the preventive action. Both usages preserved verbatim per the fidelity rule; flagged for author review (a distinguishing subscript may be desirable in revision).
3. **Line 1169 (§12.2, empirical qualification)**: the remark invokes "定理 12.1 的下界" (Theorem 12.1) before that theorem is stated (§12.4, line 1183) — a forward reference, rendered as is. Similarly, line 1177 references the index $\Omega$ before Definition 12.2 introduces it.
4. **Line 978 (§9.4, arms-race paragraph)**: "动态中 $\varepsilon_g(t)$ 上升" reads "in the dynamics, $\varepsilon_g(t)$ rises" — presumably because detector evasion raises the effective leak rate; rendered literally. The consequent claim "$\sigma^*(t)$ 随之上移" follows from Theorem 9.3's formula only if $G$ does not shrink faster; flagged as an argued (not derived) step, consistent with the source's own "论证性讨论" label.

<!-- —— 以上为 §9–§12 译者注 —— -->

<!-- TRANSLATOR NOTES -->
1. **Line 500 (§6.2, setup)** 【已裁决·已修复】遗留记号 z_β 删除，改为"阈值 z 由阈值方程决定（定理 6.1）"，中英同步。原疑点：: the phrase "$z_\beta$-类分位数由阈值方程决定" introduces the notation $z_\beta$, but $z_\beta$ is never used again—Theorem 6.1 names the threshold variable $z$; rendered as "$z_\beta$-type quantiles are determined by the threshold equation." Possible leftover notation; flagged, not corrected.
2. **Line 723 (E-7.1) vs. line 725 (E-7.2(c))**: 【已裁决·已修复】口径消歧：0.46 = 清单覆盖率 $\hat p_{\min}$ 实测上限（非端到端召回）；0.28 = 最优端到端召回。E-7.1 处加括注说明因果链（供给超预算→配额稀释→端到端召回更低），E-7.2(c) 处补"端到端召回"限定语，中英同步。原疑点记录：E-7.1 reported coverage "0.17→0.46" whereas E-7.2(c) stated best 0.28; the two are different quantities (structural input vs. pipeline output), consistent once disambiguated.
3. **Line 562 (Theorem 6.2)** 【已裁决·已修复】双重取小改写为显式局部记号 underline g（全体条目×全体增广语境的最小正边际增益），中英同步。原疑点：: the condition "$\min_{i \in \mathcal{X}^+}\{$条目 $i$ 的最小正边际增益$\}$" reads literally as "the minimum over $i \in \mathcal{X}^+$ of the minimum positive marginal gain of item $i$"—the double minimization is redundant/awkward (each item has one marginal gain per augmentation context); rendered literally. Flagged for author review.
4. **Line 611 (§6.4 remark)**: "完整处理留待阶段二算法论文" — "阶段二" rendered as "the phase-two algorithms paper"; if "阶段二" refers to a named project milestone elsewhere in the manuscript, a uniform label should be fixed in the terminology table.
5. **Line 863 (§8.7)**: the "证明思路" (proof sketch) of Proposition 8.3 ends with $\blacksquare$ in the source although the derivation is deferred to Matějka & McKay (2015); the QED marker is preserved verbatim per the fidelity rule.

<!-- —— 以上为 Part III 译者注 —— -->

<!-- TRANSLATOR NOTES -->
1. **Line 263 (§3.1)**: the original mixes Chinese with English in "规范假设与设计立场决定的是问题 formulation 与制度设计" ("formulation" appears in English inside the Chinese sentence); rendered as "determine the formulation of the problem and the institutional design." No content change.
2. **Line 435 (§5.2, remark item 3)**: "耐久读数" ("durability reading") is inconsistent with the feature name 耐久度 ("durability") used everywhere else; likely a slip for "耐久度读数." Rendered as "durability reading" without silent correction.
3. **Line 444 (§5.2, engineering implications, item (a))** 【已裁决·已修复】"折扣 λ"→"耐久尺度 λ（实际衰减因子为 e^{-h_i/λ}）"，中英同步。原疑点：: "折扣 $\lambda$" loosely calls $\lambda$ (the durability scale) "the discount"; the actual discount factor is $e^{-h_i/\lambda}$. Rendered literally as "the discount $\lambda$"; flagged for author review.
4. **Line 459 (§5.3, final remark)**: "预先授权四元组 $D_{\mathrm{adv}}$" — "quadruple" (four-tuple) could not be verified against Definition 11.2 from within the assigned line range; rendered literally as "pre-authorization quadruple." If Definition 11.2 defines a tuple of different arity, this should be aligned.
5. **Line 391 (§5.1, proof of Proposition 5.1)** 【已裁决·核验无误，不改】Bertsekas & Shreve (1978)：可测选择理论（第 7 章，Prop. 7.33）按名称引用未标章号；"第 8–9 章"恰为 Borel 模型最优策略存在性章节，与文中用途一致。原疑点：: "Bertsekas & Shreve (1978) 的可测选择理论处理；其第 8–9 章正是上述 DP 存在性论证的严格化工具" — the citation is retained verbatim; note that the measurable-selection machinery in Bertsekas & Shreve (1978) is concentrated in Chapters 7–8 of some printings. Flagged for bibliography cross-check, not corrected.

<!-- —— 以上为 Part II 译者注；以下为 Part I —— -->

<!-- TRANSLATOR NOTES -->
1. **Line 204 (§2.1, value-of-information bullet)** 【已裁决·已修复】informativo→informativeness（ZH 源已改），并已挂 $\succeq_B$ 记号锚。原文疑点：: the original contains "实验的 informativo 序由 Blackwell 定理刻画" — the word "informativo" is Spanish/Italian, presumably a slip for English "informativeness" (the Blackwell informativeness order). Translated as "the informativeness ordering of experiments is characterized by Blackwell's theorem." Flagged, not silently corrected.
2. **Line 218 (§2.4, item (e))** 【已裁决·已修复】"认知 effort"→"认知努力"（ZH 源已改）。原文疑点：: "怀疑需要认知 effort" mixes Chinese with the English word "effort"; rendered as "doubt requires cognitive effort." No content change.
3. **Line 253 (§2.8, item (f))**: "§5.3 引导注" — "引导注" is an unusual construction (literally "guidance note"); rendered literally as "the guidance note in §5.3." If this denotes a named structural element of the manuscript (e.g., a footnote or remark), a uniform label should be fixed in the terminology table.
4. **Line 88 (§1.1)**: the throughput arithmetic "250–350 字/分钟 × 45 分钟 ≈ 1.0–1.6 万字" is slightly generous (the product is 11,250–15,750 characters); the figure is retained verbatim as "roughly 10,000–16,000 characters" per the no-correction rule.
5. **Line 95 (§1.1, item 4)**: "退化还是升华" — "升华" is rendered as "sublimation" to stay consistent with C7 "升华控制论" ("cybernetics of sublimation"); note this is a deliberate, non-clinical use of the term, distinct from its psychoanalytic sense.
