# Section §19: Greedy Fundamentals & Invariants

> **Module ID:** `sec-19`  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Topic Count:** 162  

**Module Summary:** Greedy exchange arguments, Sorting criteria derivation, Priority queue regret/undo maintenance, and structural invariants.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | What is Greedy? (The Master's Definition) | `B-tier` | 1600–2200 | Common | [01-19-what-is-greedy-the-master-s-definition.md](./01-19-what-is-greedy-the-master-s-definition.md) |
| 2 | The Guess-and-Prove Workflow | `B-tier` | 1600–2200 | Common | [02-19-the-guess-and-prove-workflow.md](./02-19-the-guess-and-prove-workflow.md) |
| 3 | When Greedy Fails | `B-tier` | 1600–2200 | Common | [03-19-when-greedy-fails.md](./03-19-when-greedy-fails.md) |
| 4 | Python Implementation: Efficiency at the Master Level | `B-tier` | 1600–2200 | Common | [04-19-python-implementation-efficiency-at-the-master-level.md](./04-19-python-implementation-efficiency-at-the-master-level.md) |
| 5 | Master-Level Practice | `B-tier` | 1600–2200 | Common | [05-19-master-level-practice.md](./05-19-master-level-practice.md) |
| 6 | The Formal Exchange Workflow | `B-tier` | 1600–2200 | Common | [06-19-the-formal-exchange-workflow.md](./06-19-the-formal-exchange-workflow.md) |
| 7 | Case Study: Weighted Completion Time (Smith's Rule) | `B-tier` | 1600–2200 | Common | [07-19-case-study-weighted-completion-time-smith-s-rule.md](./07-19-case-study-weighted-completion-time-smith-s-rule.md) |
| 8 | Python Implementation: Custom Comparators | `B-tier` | 1600–2200 | Common | [08-19-python-implementation-custom-comparators.md](./08-19-python-implementation-custom-comparators.md) |
| 9 | Finding Counter-Examples | `B-tier` | 1600–2200 | Common | [09-19-finding-counter-examples.md](./09-19-finding-counter-examples.md) |
| 10 | Red Flag: Non-Local Dependencies | `B-tier` | 1600–2200 | Common | [10-19-red-flag-non-local-dependencies.md](./10-19-red-flag-non-local-dependencies.md) |
| 11 | The "Choice Independence" Test | `B-tier` | 1600–2200 | Common | [11-19-the-choice-independence-test.md](./11-19-the-choice-independence-test.md) |
| 12 | Greedy vs. DP vs. Network Flow | `B-tier` | 1600–2200 | Common | [12-19-greedy-vs-dp-vs-network-flow.md](./12-19-greedy-vs-dp-vs-network-flow.md) |
| 13 | Python Comparison: Greedy Trap | `B-tier` | 1600–2200 | Common | [13-19-python-comparison-greedy-trap.md](./13-19-python-comparison-greedy-trap.md) |
| 14 | Breaking the "Expert" Intuition | `B-tier` | 1600–2200 | Common | [14-19-breaking-the-expert-intuition.md](./14-19-breaking-the-expert-intuition.md) |
| 15 | The Core Intuition: "Deepen the Light, Shallow the Heavy" | `B-tier` | 1600–2200 | Common | [15-19-the-core-intuition-deepen-the-light-shallow-the-heavy.md](./15-19-the-core-intuition-deepen-the-light-shallow-the-heavy.md) |
| 16 | The Proof: Why it works | `B-tier` | 1600–2200 | Common | [16-19-the-proof-why-it-works.md](./16-19-the-proof-why-it-works.md) |
| 17 | Python Implementation: The $O(N \log N)$ Pattern | `B-tier` | 1600–2200 | Common | [17-19-python-implementation-the-o-n-log-n-pattern.md](./17-19-python-implementation-the-o-n-log-n-pattern.md) |
| 18 | Beyond Compression: "Merge Problems" | `B-tier` | 1600–2200 | Common | [18-19-beyond-compression-merge-problems.md](./18-19-beyond-compression-merge-problems.md) |
| 19 | Dijkstra’s Algorithm: The "Shortest Path" Greedy | `B-tier` | 1600–2200 | Common | [19-19-dijkstra-s-algorithm-the-shortest-path-greedy.md](./19-19-dijkstra-s-algorithm-the-shortest-path-greedy.md) |
| 20 | Minimum Spanning Trees (MST) | `B-tier` | 1600–2200 | Common | [20-19-minimum-spanning-trees-mst.md](./20-19-minimum-spanning-trees-mst.md) |
| 21 | Python Implementation: The $O(E \log V)$ Dijkstra | `B-tier` | 1600–2200 | Common | [21-19-python-implementation-the-o-e-log-v-dijkstra.md](./21-19-python-implementation-the-o-e-log-v-dijkstra.md) |
| 22 | Master-Level Nuance: The "State Space" Dijkstra | `B-tier` | 1600–2200 | Common | [22-19-master-level-nuance-the-state-space-dijkstra.md](./22-19-master-level-nuance-the-state-space-dijkstra.md) |
| 23 | Kruskal’s with DSU (Python Template) | `B-tier` | 1600–2200 | Common | [23-19-kruskal-s-with-dsu-python-template.md](./23-19-kruskal-s-with-dsu-python-template.md) |
| 24 | The Problem: Maximum Disjoint Intervals | `B-tier` | 1600–2200 | Common | [24-19-the-problem-maximum-disjoint-intervals.md](./24-19-the-problem-maximum-disjoint-intervals.md) |
| 25 | Formal Proof: Greedy Stays Ahead | `B-tier` | 1600–2200 | Common | [25-19-formal-proof-greedy-stays-ahead.md](./25-19-formal-proof-greedy-stays-ahead.md) |
| 26 | Python Implementation: $O(N \log N)$ | `B-tier` | 1600–2200 | Common | [26-19-python-implementation-o-n-log-n.md](./26-19-python-implementation-o-n-log-n.md) |
| 27 | Master-Level Variations | `B-tier` | 1600–2200 | Common | [27-19-master-level-variations.md](./27-19-master-level-variations.md) |
| 28 | The Problem: Minimum Interval Coverage | `B-tier` | 1600–2200 | Common | [28-19-the-problem-minimum-interval-coverage.md](./28-19-the-problem-minimum-interval-coverage.md) |
| 29 | The Proof: Greedy Stays Ahead | `B-tier` | 1600–2200 | Common | [29-19-the-proof-greedy-stays-ahead.md](./29-19-the-proof-greedy-stays-ahead.md) |
| 30 | Variations & Master Logic | `B-tier` | 1600–2200 | Common | [30-19-variations-master-logic.md](./30-19-variations-master-logic.md) |
| 31 | The Core Logic: The Lexicographical Greedy | `B-tier` | 1600–2200 | Common | [31-19-the-core-logic-the-lexicographical-greedy.md](./31-19-the-core-logic-the-lexicographical-greedy.md) |
| 32 | The Proof: Stays Ahead with Tie-Breaking | `B-tier` | 1600–2200 | Common | [32-19-the-proof-stays-ahead-with-tie-breaking.md](./32-19-the-proof-stays-ahead-with-tie-breaking.md) |
| 33 | Python Implementation: $O(N^2)$ vs $O(N)$ | `B-tier` | 1600–2200 | Common | [33-19-python-implementation-o-n-2-vs-o-n.md](./33-19-python-implementation-o-n-2-vs-o-n.md) |
| 34 | Master Insight: The "Reachable" Greedy | `B-tier` | 1600–2200 | Common | [34-19-master-insight-the-reachable-greedy.md](./34-19-master-insight-the-reachable-greedy.md) |
| 35 | The Theoretical Framework: The Neighbor Swap | `B-tier` | 1600–2200 | Common | [35-19-the-theoretical-framework-the-neighbor-swap.md](./35-19-the-theoretical-framework-the-neighbor-swap.md) |
| 36 | Establishing a Total Ordering | `B-tier` | 1600–2200 | Common | [36-19-establishing-a-total-ordering.md](./36-19-establishing-a-total-ordering.md) |
| 37 | Case Study: The "Monster" Problem | `B-tier` | 1600–2200 | Common | [37-19-case-study-the-monster-problem.md](./37-19-case-study-the-monster-problem.md) |
| 38 | Python Implementation: Using `cmp_to_key` | `B-tier` | 1600–2200 | Common | [38-19-python-implementation-using-cmp-to-key.md](./38-19-python-implementation-using-cmp-to-key.md) |
| 39 | Identifying the "Comparator" Pattern | `B-tier` | 1600–2200 | Common | [39-19-identifying-the-comparator-pattern.md](./39-19-identifying-the-comparator-pattern.md) |
| 40 | The Algebra of the Swap | `B-tier` | 1600–2200 | Common | [40-19-the-algebra-of-the-swap.md](./40-19-the-algebra-of-the-swap.md) |
| 41 | Common Master-Level Formulas | `B-tier` | 1600–2200 | Common | [41-19-common-master-level-formulas.md](./41-19-common-master-level-formulas.md) |
| 42 | Python Implementation: The Cross-Multiplication Rule | `B-tier` | 1600–2200 | Common | [42-19-python-implementation-the-cross-multiplication-rule.md](./42-19-python-implementation-the-cross-multiplication-rule.md) |
| 43 | The Transitivity Warning | `B-tier` | 1600–2200 | Common | [43-19-the-transitivity-warning.md](./43-19-the-transitivity-warning.md) |
| 44 | The Core Scenario: Resource Management | `B-tier` | 1600–2200 | Common | [44-19-the-core-scenario-resource-management.md](./44-19-the-core-scenario-resource-management.md) |
| 45 | Deriving Phase 1: The "Low Barrier" Strategy | `B-tier` | 1600–2200 | Common | [45-19-deriving-phase-1-the-low-barrier-strategy.md](./45-19-deriving-phase-1-the-low-barrier-strategy.md) |
| 46 | Deriving Phase 2: The "Safety First" Strategy | `B-tier` | 1600–2200 | Common | [46-19-deriving-phase-2-the-safety-first-strategy.md](./46-19-deriving-phase-2-the-safety-first-strategy.md) |
| 47 | Python Implementation: Handling the Partition | `B-tier` | 1600–2200 | Common | [47-19-python-implementation-handling-the-partition.md](./47-19-python-implementation-handling-the-partition.md) |
| 48 | Why One Sort Fails | `B-tier` | 1600–2200 | Common | [48-19-why-one-sort-fails.md](./48-19-why-one-sort-fails.md) |
| 49 | The Sweep Line Philosophy | `B-tier` | 1600–2200 | Common | [49-19-the-sweep-line-philosophy.md](./49-19-the-sweep-line-philosophy.md) |
| 50 | Invariants: The Greedy Guardrail | `B-tier` | 1600–2200 | Common | [50-19-invariants-the-greedy-guardrail.md](./50-19-invariants-the-greedy-guardrail.md) |
| 51 | The "Active Set" Data Structure | `B-tier` | 1600–2200 | Common | [51-19-the-active-set-data-structure.md](./51-19-the-active-set-data-structure.md) |
| 52 | Python Implementation: The "Meeting Rooms" Invariant | `B-tier` | 1600–2200 | Common | [52-19-python-implementation-the-meeting-rooms-invariant.md](./52-19-python-implementation-the-meeting-rooms-invariant.md) |
| 53 | Master Technique: Coordinate Compression | `B-tier` | 1600–2200 | Common | [53-19-master-technique-coordinate-compression.md](./53-19-master-technique-coordinate-compression.md) |
| 54 | Maintaining "Sanity" in 2D | `B-tier` | 1600–2200 | Common | [54-19-maintaining-sanity-in-2d.md](./54-19-maintaining-sanity-in-2d.md) |
| 55 | The Constructive Mindset: "Small to Large" | `B-tier` | 1600–2200 | Common | [55-19-the-constructive-mindset-small-to-large.md](./55-19-the-constructive-mindset-small-to-large.md) |
| 56 | Key Strategy: The "Snake" and "Parity" Patterns | `B-tier` | 1600–2200 | Common | [56-19-key-strategy-the-snake-and-parity-patterns.md](./56-19-key-strategy-the-snake-and-parity-patterns.md) |
| 57 | Invariants: The "Checklist" Method | `B-tier` | 1600–2200 | Common | [57-19-invariants-the-checklist-method.md](./57-19-invariants-the-checklist-method.md) |
| 58 | Python Implementation: Building Patterns | `B-tier` | 1600–2200 | Common | [58-19-python-implementation-building-patterns.md](./58-19-python-implementation-building-patterns.md) |
| 59 | The "Greedy Guess" in Construction | `B-tier` | 1600–2200 | Common | [59-19-the-greedy-guess-in-construction.md](./59-19-the-greedy-guess-in-construction.md) |
| 60 | The Core Pattern: The "Greedy Choice" in Flux | `B-tier` | 1600–2200 | Common | [60-19-the-core-pattern-the-greedy-choice-in-flux.md](./60-19-the-core-pattern-the-greedy-choice-in-flux.md) |
| 61 | Case Study: Optimal Job Scheduling (Profit vs. Deadline) | `B-tier` | 1600–2200 | Common | [61-19-case-study-optimal-job-scheduling-profit-vs-deadline.md](./61-19-case-study-optimal-job-scheduling-profit-vs-deadline.md) |
| 62 | Python Implementation: `heapq` and $O(N \log N)$ | `B-tier` | 1600–2200 | Common | [62-19-python-implementation-heapq-and-o-n-log-n.md](./62-19-python-implementation-heapq-and-o-n-log-n.md) |
| 63 | Advanced Dynamic Constraint: "The Refill" | `B-tier` | 1600–2200 | Common | [63-19-advanced-dynamic-constraint-the-refill.md](./63-19-advanced-dynamic-constraint-the-refill.md) |
| 64 | Formal Invariant | `B-tier` | 1600–2200 | Common | [64-19-formal-invariant.md](./64-19-formal-invariant.md) |
| 65 | The Core Philosophy: "Buy Now, Refund Later" | `B-tier` | 1600–2200 | Common | [65-19-the-core-philosophy-buy-now-refund-later.md](./65-19-the-core-philosophy-buy-now-refund-later.md) |
| 66 | Case Study: The Potions Problem | `B-tier` | 1600–2200 | Common | [66-19-case-study-the-potions-problem.md](./66-19-case-study-the-potions-problem.md) |
| 67 | Python Implementation: Potions (Hard Version) | `B-tier` | 1600–2200 | Common | [67-19-python-implementation-potions-hard-version.md](./67-19-python-implementation-potions-hard-version.md) |
| 68 | Advanced Regret: Stock Trading | `B-tier` | 1600–2200 | Common | [68-19-advanced-regret-stock-trading.md](./68-19-advanced-regret-stock-trading.md) |
| 69 | Identifying "Regret" Problems | `B-tier` | 1600–2200 | Common | [69-19-identifying-regret-problems.md](./69-19-identifying-regret-problems.md) |
| 70 | The Problem: The "Optimal" Buy-Sell | `B-tier` | 1600–2200 | Common | [70-19-the-problem-the-optimal-buy-sell.md](./70-19-the-problem-the-optimal-buy-sell.md) |
| 71 | The "Regret" Logic: The Two-Push Strategy | `B-tier` | 1600–2200 | Common | [71-19-the-regret-logic-the-two-push-strategy.md](./71-19-the-regret-logic-the-two-push-strategy.md) |
| 72 | Connection to Slope Trick | `B-tier` | 1600–2200 | Common | [72-19-connection-to-slope-trick.md](./72-19-connection-to-slope-trick.md) |
| 73 | Identifying the Pattern | `B-tier` | 1600–2200 | Common | [73-19-identifying-the-pattern.md](./73-19-identifying-the-pattern.md) |
| 74 | The Core Principle: Additive Independence | `B-tier` | 1600–2200 | Common | [74-19-the-core-principle-additive-independence.md](./74-19-the-core-principle-additive-independence.md) |
| 75 | The Master Transformation: Chebyshev to Manhattan | `B-tier` | 1600–2200 | Common | [75-19-the-master-transformation-chebyshev-to-manhattan.md](./75-19-the-master-transformation-chebyshev-to-manhattan.md) |
| 76 | Python Implementation: 2D Optimal Meeting Point | `B-tier` | 1600–2200 | Common | [76-19-python-implementation-2d-optimal-meeting-point.md](./76-19-python-implementation-2d-optimal-meeting-point.md) |
| 77 | Applying the "Sweep" to Decoupled Axes | `B-tier` | 1600–2200 | Common | [77-19-applying-the-sweep-to-decoupled-axes.md](./77-19-applying-the-sweep-to-decoupled-axes.md) |
| 78 | Identifying the Decoupling Pattern | `B-tier` | 1600–2200 | Common | [78-19-identifying-the-decoupling-pattern.md](./78-19-identifying-the-decoupling-pattern.md) |
| 79 | The Median Invariant: Why it Minimizes Absolute Cost | `B-tier` | 1600–2200 | Common | [79-19-the-median-invariant-why-it-minimizes-absolute-cost.md](./79-19-the-median-invariant-why-it-minimizes-absolute-cost.md) |
| 80 | Case Study: CSES Stick Lengths | `B-tier` | 1600–2200 | Common | [80-19-case-study-cses-stick-lengths.md](./80-19-case-study-cses-stick-lengths.md) |
| 81 | The "Sweep" Version: Sliding Window Median | `B-tier` | 1600–2200 | Common | [81-19-the-sweep-version-sliding-window-median.md](./81-19-the-sweep-version-sliding-window-median.md) |
| 82 | Python Implementation: Efficient Dynamic Median | `B-tier` | 1600–2200 | Common | [82-19-python-implementation-efficient-dynamic-median.md](./82-19-python-implementation-efficient-dynamic-median.md) |
| 83 | The Master Generalization: Weighted Median | `B-tier` | 1600–2200 | Common | [83-19-the-master-generalization-weighted-median.md](./83-19-the-master-generalization-weighted-median.md) |
| 84 | Median in 2D (Revisiting Manhattan) | `B-tier` | 1600–2200 | Common | [84-19-median-in-2d-revisiting-manhattan.md](./84-19-median-in-2d-revisiting-manhattan.md) |
| 85 | Prefix-Suffix Sweeps: The "Middle Man" Strategy | `B-tier` | 1600–2200 | Common | [85-19-prefix-suffix-sweeps-the-middle-man-strategy.md](./85-19-prefix-suffix-sweeps-the-middle-man-strategy.md) |
| 86 | Block Compression: Reducing State Space | `B-tier` | 1600–2200 | Common | [86-19-block-compression-reducing-state-space.md](./86-19-block-compression-reducing-state-space.md) |
| 87 | Python Implementation: The Master Toolkit | `B-tier` | 1600–2200 | Common | [87-19-python-implementation-the-master-toolkit.md](./87-19-python-implementation-the-master-toolkit.md) |
| 88 | Case Study: The "Remove Peak" Problem | `B-tier` | 1600–2200 | Common | [88-19-case-study-the-remove-peak-problem.md](./88-19-case-study-the-remove-peak-problem.md) |
| 89 | The Core Concept: The "Penalty" Transformation | `B-tier` | 1600–2200 | Common | [89-19-the-core-concept-the-penalty-transformation.md](./89-19-the-core-concept-the-penalty-transformation.md) |
| 90 | The Convexity/Concavity Requirement | `B-tier` | 1600–2200 | Common | [90-19-the-convexity-concavity-requirement.md](./90-19-the-convexity-concavity-requirement.md) |
| 91 | Python Implementation: The $O(N \log V)$ Template | `B-tier` | 1600–2200 | Common | [91-19-python-implementation-the-o-n-log-v-template.md](./91-19-python-implementation-the-o-n-log-v-template.md) |
| 92 | Handling Tie-Breaking (LIP: Linear Interpolation) | `B-tier` | 1600–2200 | Common | [92-19-handling-tie-breaking-lip-linear-interpolation.md](./92-19-handling-tie-breaking-lip-linear-interpolation.md) |
| 93 | The Grand Link: WQS, Undo, and Slope Trick | `B-tier` | 1600–2200 | Common | [93-19-the-grand-link-wqs-undo-and-slope-trick.md](./93-19-the-grand-link-wqs-undo-and-slope-trick.md) |
| 94 | What Kind of Functions? | `B-tier` | 1600–2200 | Common | [94-19-what-kind-of-functions.md](./94-19-what-kind-of-functions.md) |
| 95 | The Representation: Two Heaps | `B-tier` | 1600–2200 | Common | [95-19-the-representation-two-heaps.md](./95-19-the-representation-two-heaps.md) |
| 96 | Operation: Adding $|x - a|$ | `B-tier` | 1600–2200 | Common | [96-19-operation-adding-x-a.md](./96-19-operation-adding-x-a.md) |
| 97 | Python Conceptual Snippet | `B-tier` | 1600–2200 | Common | [97-19-python-conceptual-snippet.md](./97-19-python-conceptual-snippet.md) |
| 98 | Why is this Greedy? | `B-tier` | 1600–2200 | Common | [98-19-why-is-this-greedy.md](./98-19-why-is-this-greedy.md) |
| 99 | The "Shift" Transformation ($f(x) \to f(x - c)$) | `B-tier` | 1600–2200 | Common | [99-19-the-shift-transformation-f-x-to-f-x-c.md](./99-19-the-shift-transformation-f-x-to-f-x-c.md) |
| 100 | The "Prefix Minimum" ($f(x) \to \min_{y \le x} f(y)$) | `B-tier` | 1600–2200 | Common | [100-19-the-prefix-minimum-f-x-to-min-y-le-x-f-y.md](./100-19-the-prefix-minimum-f-x-to-min-y-le-x-f-y.md) |
| 101 | Full Python Implementation Template | `B-tier` | 1600–2200 | Common | [101-19-full-python-implementation-template.md](./101-19-full-python-implementation-template.md) |
| 102 | Complexity Analysis | `B-tier` | 1600–2200 | Common | [102-19-complexity-analysis.md](./102-19-complexity-analysis.md) |
| 103 | Master's Secret: Handling Slopes $> 1$ | `B-tier` | 1600–2200 | Common | [103-19-master-s-secret-handling-slopes-1.md](./103-19-master-s-secret-handling-slopes-1.md) |
| 104 | The Shared Foundation: Convexity | `B-tier` | 1600–2200 | Common | [104-19-the-shared-foundation-convexity.md](./104-19-the-shared-foundation-convexity.md) |
| 105 | The Three Perspectives | `B-tier` | 1600–2200 | Common | [105-19-the-three-perspectives.md](./105-19-the-three-perspectives.md) |
| 106 | The Geometric Unification | `B-tier` | 1600–2200 | Common | [106-19-the-geometric-unification.md](./106-19-the-geometric-unification.md) |
| 107 | Python Synthesis: Solving the Same Problem Three Ways | `B-tier` | 1600–2200 | Common | [107-19-python-synthesis-solving-the-same-problem-three-ways.md](./107-19-python-synthesis-solving-the-same-problem-three-ways.md) |
| 108 | The "Master" Decision Tree | `B-tier` | 1600–2200 | Common | [108-19-the-master-decision-tree.md](./108-19-the-master-decision-tree.md) |
| 109 | The Conflict Graph Logic | `B-tier` | 1600–2200 | Common | [109-19-the-conflict-graph-logic.md](./109-19-the-conflict-graph-logic.md) |
| 110 | Bipartite DSU (Weighted DSU) | `B-tier` | 1600–2200 | Common | [110-19-bipartite-dsu-weighted-dsu.md](./110-19-bipartite-dsu-weighted-dsu.md) |
| 111 | Python Implementation: Bipartite DSU Template | `B-tier` | 1600–2200 | Common | [111-19-python-implementation-bipartite-dsu-template.md](./111-19-python-implementation-bipartite-dsu-template.md) |
| 112 | Why This is "Greedy"? | `B-tier` | 1600–2200 | Common | [112-19-why-this-is-greedy.md](./112-19-why-this-is-greedy.md) |
| 113 | Defining the State | `B-tier` | 1600–2200 | Common | [113-19-defining-the-state.md](./113-19-defining-the-state.md) |
| 114 | 0-1 BFS: The Hybrid Greedy | `B-tier` | 1600–2200 | Common | [114-19-0-1-bfs-the-hybrid-greedy.md](./114-19-0-1-bfs-the-hybrid-greedy.md) |
| 115 | Python Implementation: The "Implicit" Dijkstra Template | `B-tier` | 1600–2200 | Common | [115-19-python-implementation-the-implicit-dijkstra-template.md](./115-19-python-implementation-the-implicit-dijkstra-template.md) |
| 116 | Master Insight: Multi-Stage Dijkstra | `B-tier` | 1600–2200 | Common | [116-19-master-insight-multi-stage-dijkstra.md](./116-19-master-insight-multi-stage-dijkstra.md) |
| 117 | Pruning: The Greedy Guardrail | `B-tier` | 1600–2200 | Common | [117-19-pruning-the-greedy-guardrail.md](./117-19-pruning-the-greedy-guardrail.md) |
| 118 | The Tree Diameter: The 2-BFS Greedy Strategy | `B-tier` | 1600–2200 | Common | [118-19-the-tree-diameter-the-2-bfs-greedy-strategy.md](./118-19-the-tree-diameter-the-2-bfs-greedy-strategy.md) |
| 119 | The Tree Centroid: The Balance Point | `B-tier` | 1600–2200 | Common | [119-19-the-tree-centroid-the-balance-point.md](./119-19-the-tree-centroid-the-balance-point.md) |
| 120 | Greedy Tree DP: The "Leaf-to-Root" Pattern | `B-tier` | 1600–2200 | Common | [120-19-greedy-tree-dp-the-leaf-to-root-pattern.md](./120-19-greedy-tree-dp-the-leaf-to-root-pattern.md) |
| 121 | Python Implementation: Diameter and Centroid | `B-tier` | 1600–2200 | Common | [121-19-python-implementation-diameter-and-centroid.md](./121-19-python-implementation-diameter-and-centroid.md) |
| 122 | Identifying Tree Greedy Patterns | `B-tier` | 1600–2200 | Common | [122-19-identifying-tree-greedy-patterns.md](./122-19-identifying-tree-greedy-patterns.md) |
| 123 | The Formal Definition of a Matroid | `B-tier` | 1600–2200 | Common | [123-19-the-formal-definition-of-a-matroid.md](./123-19-the-formal-definition-of-a-matroid.md) |
| 124 | Core Matroid Terminology | `B-tier` | 1600–2200 | Common | [124-19-core-matroid-terminology.md](./124-19-core-matroid-terminology.md) |
| 125 | The Rado-Edmonds Theorem (The Greedy Theorem) | `B-tier` | 1600–2200 | Common | [125-19-the-rado-edmonds-theorem-the-greedy-theorem.md](./125-19-the-rado-edmonds-theorem-the-greedy-theorem.md) |
| 126 | Classical Matroid Archetypes in CP | `B-tier` | 1600–2200 | Common | [126-19-classical-matroid-archetypes-in-cp.md](./126-19-classical-matroid-archetypes-in-cp.md) |
| 127 | Python Implementation: The Generic Matroid Greedy | `B-tier` | 1600–2200 | Common | [127-19-python-implementation-the-generic-matroid-greedy.md](./127-19-python-implementation-the-generic-matroid-greedy.md) |
| 128 | Why Bipartite Matching is NOT a Matroid | `B-tier` | 1600–2200 | Common | [128-19-why-bipartite-matching-is-not-a-matroid.md](./128-19-why-bipartite-matching-is-not-a-matroid.md) |
| 129 | The Rank Function and Submodularity | `B-tier` | 1600–2200 | Common | [129-19-the-rank-function-and-submodularity.md](./129-19-the-rank-function-and-submodularity.md) |
| 130 | The Dual Matroid ($M^*$) | `B-tier` | 1600–2200 | Common | [130-19-the-dual-matroid-m.md](./130-19-the-dual-matroid-m.md) |
| 131 | Cocycles and the "Reverse Greedy" Algorithm | `B-tier` | 1600–2200 | Common | [131-19-cocycles-and-the-reverse-greedy-algorithm.md](./131-19-cocycles-and-the-reverse-greedy-algorithm.md) |
| 132 | Python Implementation: The Matroid Rank Oracle | `B-tier` | 1600–2200 | Common | [132-19-python-implementation-the-matroid-rank-oracle.md](./132-19-python-implementation-the-matroid-rank-oracle.md) |
| 133 | Identifying Submodular / Dual Problems | `B-tier` | 1600–2200 | Common | [133-19-identifying-submodular-dual-problems.md](./133-19-identifying-submodular-dual-problems.md) |
| 134 | The Core Idea: Bipartite Swapping | `B-tier` | 1600–2200 | Common | [134-19-the-core-idea-bipartite-swapping.md](./134-19-the-core-idea-bipartite-swapping.md) |
| 135 | The Exchange Graph ($G_I$) | `B-tier` | 1600–2200 | Common | [135-19-the-exchange-graph-g-i.md](./135-19-the-exchange-graph-g-i.md) |
| 136 | The Augmenting Path | `B-tier` | 1600–2200 | Common | [136-19-the-augmenting-path.md](./136-19-the-augmenting-path.md) |
| 137 | Python Conceptual Implementation | `B-tier` | 1600–2200 | Common | [137-19-python-conceptual-implementation.md](./137-19-python-conceptual-implementation.md) |
| 138 | Weighted Matroid Intersection | `B-tier` | 1600–2200 | Common | [138-19-weighted-matroid-intersection.md](./138-19-weighted-matroid-intersection.md) |
| 139 | What is an Antimatroid? | `B-tier` | 1600–2200 | Common | [139-19-what-is-an-antimatroid.md](./139-19-what-is-an-antimatroid.md) |
| 140 | Lawler's Algorithm: The Reverse Greedy on Antimatroids | `B-tier` | 1600–2200 | Common | [140-19-lawler-s-algorithm-the-reverse-greedy-on-antimatroids.md](./140-19-lawler-s-algorithm-the-reverse-greedy-on-antimatroids.md) |
| 141 | Dilworth's Theorem and Posets | `B-tier` | 1600–2200 | Common | [141-19-dilworth-s-theorem-and-posets.md](./141-19-dilworth-s-theorem-and-posets.md) |
| 142 | Python Implementation: Kahn's Algorithm + Priority Queue | `B-tier` | 1600–2200 | Common | [142-19-python-implementation-kahn-s-algorithm-priority-queue.md](./142-19-python-implementation-kahn-s-algorithm-priority-queue.md) |
| 143 | Identifying Antimatroid / Scheduling Patterns | `B-tier` | 1600–2200 | Common | [143-19-identifying-antimatroid-scheduling-patterns.md](./143-19-identifying-antimatroid-scheduling-patterns.md) |
| 144 | The Greedy Descent (Maximizing XOR) | `B-tier` | 1600–2200 | Common | [144-19-the-greedy-descent-maximizing-xor.md](./144-19-the-greedy-descent-maximizing-xor.md) |
| 145 | Python Implementation: The Flat Array Trie | `B-tier` | 1600–2200 | Common | [145-19-python-implementation-the-flat-array-trie.md](./145-19-python-implementation-the-flat-array-trie.md) |
| 146 | The Prefix XOR Invariant | `B-tier` | 1600–2200 | Common | [146-19-the-prefix-xor-invariant.md](./146-19-the-prefix-xor-invariant.md) |
| 147 | Maintaining Subtree Sizes & Dynamic MEX | `B-tier` | 1600–2200 | Common | [147-19-maintaining-subtree-sizes-dynamic-mex.md](./147-19-maintaining-subtree-sizes-dynamic-mex.md) |
| 148 | The Greedy Routing Logic | `B-tier` | 1600–2200 | Common | [148-19-the-greedy-routing-logic.md](./148-19-the-greedy-routing-logic.md) |
| 149 | Python Implementation: The Walkable SegTree | `B-tier` | 1600–2200 | Common | [149-19-python-implementation-the-walkable-segtree.md](./149-19-python-implementation-the-walkable-segtree.md) |
| 150 | Constrained Walking | `B-tier` | 1600–2200 | Common | [150-19-constrained-walking.md](./150-19-constrained-walking.md) |
| 151 | Advanced Applications: Resource Allocation | `B-tier` | 1600–2200 | Common | [151-19-advanced-applications-resource-allocation.md](./151-19-advanced-applications-resource-allocation.md) |
| 152 | The Theorem: The Bottleneck Test | `B-tier` | 1600–2200 | Common | [152-19-the-theorem-the-bottleneck-test.md](./152-19-the-theorem-the-bottleneck-test.md) |
| 153 | The CP Translation: Intervals on a Line | `B-tier` | 1600–2200 | Common | [153-19-the-cp-translation-intervals-on-a-line.md](./153-19-the-cp-translation-intervals-on-a-line.md) |
| 154 | The "Greedy + Hall's Oracle" Pattern | `B-tier` | 1600–2200 | Common | [154-19-the-greedy-hall-s-oracle-pattern.md](./154-19-the-greedy-hall-s-oracle-pattern.md) |
| 155 | Python Implementation: The Lazy Segment Tree Oracle | `B-tier` | 1600–2200 | Common | [155-19-python-implementation-the-lazy-segment-tree-oracle.md](./155-19-python-implementation-the-lazy-segment-tree-oracle.md) |
| 156 | Nim and the XOR Invariant | `B-tier` | 1600–2200 | Common | [156-19-nim-and-the-xor-invariant.md](./156-19-nim-and-the-xor-invariant.md) |
| 157 | The Sprague-Grundy Theorem | `B-tier` | 1600–2200 | Common | [157-19-the-sprague-grundy-theorem.md](./157-19-the-sprague-grundy-theorem.md) |
| 158 | Python Implementation: MEX & Grundy DP | `B-tier` | 1600–2200 | Common | [158-19-python-implementation-mex-grundy-dp.md](./158-19-python-implementation-mex-grundy-dp.md) |
| 159 | The Subgame Split Rule | `B-tier` | 1600–2200 | Common | [159-19-the-subgame-split-rule.md](./159-19-the-subgame-split-rule.md) |
| 160 | Periodicity in Grundy Sequences | `B-tier` | 1600–2200 | Common | [160-19-periodicity-in-grundy-sequences.md](./160-19-periodicity-in-grundy-sequences.md) |
| 161 | The Greedy Basics Curriculum | `B-tier` | 1600–2200 | Common | [161-19-the-greedy-basics-curriculum.md](./161-19-the-greedy-basics-curriculum.md) |
| 162 | Continuing the Greedy Curriculum | `B-tier` | 1600–2200 | Common | [162-19-continuing-the-greedy-curriculum.md](./162-19-continuing-the-greedy-curriculum.md) |
