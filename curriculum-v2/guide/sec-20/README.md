# Section §20: Greedy Intermediate (Slope Trick, WQS)

> **Module ID:** `sec-20`  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Topic Count:** 92  

**Module Summary:** Decoupled dimension sweeps, Median cost minimization, Slope Trick with two priority queues, and WQS Binary Search / Aliens Trick.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | The Core Principle: Additive Independence | `B-tier` | 1600–2200 | Common | [01-20-the-core-principle-additive-independence.md](./01-20-the-core-principle-additive-independence.md) |
| 2 | The Master Transformation: Chebyshev to Manhattan | `B-tier` | 1600–2200 | Common | [02-20-the-master-transformation-chebyshev-to-manhattan.md](./02-20-the-master-transformation-chebyshev-to-manhattan.md) |
| 3 | Python Implementation: 2D Optimal Meeting Point | `B-tier` | 1600–2200 | Common | [03-20-python-implementation-2d-optimal-meeting-point.md](./03-20-python-implementation-2d-optimal-meeting-point.md) |
| 4 | Applying the "Sweep" to Decoupled Axes | `B-tier` | 1600–2200 | Common | [04-20-applying-the-sweep-to-decoupled-axes.md](./04-20-applying-the-sweep-to-decoupled-axes.md) |
| 5 | Identifying the Decoupling Pattern | `B-tier` | 1600–2200 | Common | [05-20-identifying-the-decoupling-pattern.md](./05-20-identifying-the-decoupling-pattern.md) |
| 6 | The Median Invariant: Why it Minimizes Absolute Cost | `B-tier` | 1600–2200 | Common | [06-20-the-median-invariant-why-it-minimizes-absolute-cost.md](./06-20-the-median-invariant-why-it-minimizes-absolute-cost.md) |
| 7 | Case Study: CSES Stick Lengths | `B-tier` | 1600–2200 | Common | [07-20-case-study-cses-stick-lengths.md](./07-20-case-study-cses-stick-lengths.md) |
| 8 | The "Sweep" Version: Sliding Window Median | `B-tier` | 1600–2200 | Common | [08-20-the-sweep-version-sliding-window-median.md](./08-20-the-sweep-version-sliding-window-median.md) |
| 9 | Python Implementation: Efficient Dynamic Median | `B-tier` | 1600–2200 | Common | [09-20-python-implementation-efficient-dynamic-median.md](./09-20-python-implementation-efficient-dynamic-median.md) |
| 10 | The Master Generalization: Weighted Median | `B-tier` | 1600–2200 | Common | [10-20-the-master-generalization-weighted-median.md](./10-20-the-master-generalization-weighted-median.md) |
| 11 | Prefix-Suffix Sweeps: The "Middle Man" Strategy | `B-tier` | 1600–2200 | Common | [11-20-prefix-suffix-sweeps-the-middle-man-strategy.md](./11-20-prefix-suffix-sweeps-the-middle-man-strategy.md) |
| 12 | Block Compression: Reducing State Space | `B-tier` | 1600–2200 | Common | [12-20-block-compression-reducing-state-space.md](./12-20-block-compression-reducing-state-space.md) |
| 13 | Python Implementation: The Master Toolkit | `B-tier` | 1600–2200 | Common | [13-20-python-implementation-the-master-toolkit.md](./13-20-python-implementation-the-master-toolkit.md) |
| 14 | The Core Concept: The "Penalty" Transformation | `B-tier` | 1600–2200 | Common | [14-20-the-core-concept-the-penalty-transformation.md](./14-20-the-core-concept-the-penalty-transformation.md) |
| 15 | The Convexity/Concavity Requirement | `B-tier` | 1600–2200 | Common | [15-20-the-convexity-concavity-requirement.md](./15-20-the-convexity-concavity-requirement.md) |
| 16 | Python Implementation: The $O(N \log V)$ Template | `B-tier` | 1600–2200 | Common | [16-20-python-implementation-the-o-n-log-v-template.md](./16-20-python-implementation-the-o-n-log-v-template.md) |
| 17 | Handling Tie-Breaking (LIP: Linear Interpolation) | `B-tier` | 1600–2200 | Common | [17-20-handling-tie-breaking-lip-linear-interpolation.md](./17-20-handling-tie-breaking-lip-linear-interpolation.md) |
| 18 | What Kind of Functions? | `B-tier` | 1600–2200 | Common | [18-20-what-kind-of-functions.md](./18-20-what-kind-of-functions.md) |
| 19 | The Representation: Two Heaps | `B-tier` | 1600–2200 | Common | [19-20-the-representation-two-heaps.md](./19-20-the-representation-two-heaps.md) |
| 20 | Operation: Adding $|x - a|$ | `B-tier` | 1600–2200 | Common | [20-20-operation-adding-x-a.md](./20-20-operation-adding-x-a.md) |
| 21 | Function Transformations | `B-tier` | 1600–2200 | Common | [21-20-function-transformations.md](./21-20-function-transformations.md) |
| 22 | Python Implementation Template | `B-tier` | 1600–2200 | Common | [22-20-python-implementation-template.md](./22-20-python-implementation-template.md) |
| 23 | Decoupled Sweeps & Chebyshev-Manhattan Equivalence | `A-tier` | 1900–2300 | Common in Div.1 A/B and Div.2 D/E | [23-20-decoupled-sweeps-chebyshev-manhattan-equivalence.md](./23-20-decoupled-sweeps-chebyshev-manhattan-equivalence.md) |
| 24 | Median as the $L_1$ Norm Minimizer | `S-tier` | 1600–2200 | High | [24-20-median-as-the-l-1-norm-minimizer.md](./24-20-median-as-the-l-1-norm-minimizer.md) |
| 25 | Simultaneous Past-Future Queries and State Space Reduction | `B-tier` | 1600–2200 | Common | [25-20-simultaneous-past-future-queries-and-state-space-reduction.md](./25-20-simultaneous-past-future-queries-and-state-space-reduction.md) |
| 26 | The Formal Definition of a Matroid | `B-tier` | 1600–2200 | Common | [26-20-the-formal-definition-of-a-matroid.md](./26-20-the-formal-definition-of-a-matroid.md) |
| 27 | Core Matroid Terminology | `B-tier` | 1600–2200 | Common | [27-20-core-matroid-terminology.md](./27-20-core-matroid-terminology.md) |
| 28 | The Rado-Edmonds Theorem (The Greedy Theorem) | `B-tier` | 1600–2200 | Common | [28-20-the-rado-edmonds-theorem-the-greedy-theorem.md](./28-20-the-rado-edmonds-theorem-the-greedy-theorem.md) |
| 29 | Classical Matroid Archetypes in CP | `B-tier` | 1600–2200 | Common | [29-20-classical-matroid-archetypes-in-cp.md](./29-20-classical-matroid-archetypes-in-cp.md) |
| 30 | Python Implementation: The Generic Matroid Greedy | `B-tier` | 1600–2200 | Common | [30-20-python-implementation-the-generic-matroid-greedy.md](./30-20-python-implementation-the-generic-matroid-greedy.md) |
| 31 | Why Bipartite Matching is NOT a Matroid | `B-tier` | 1600–2200 | Common | [31-20-why-bipartite-matching-is-not-a-matroid.md](./31-20-why-bipartite-matching-is-not-a-matroid.md) |
| 32 | The Rank Function and Submodularity | `B-tier` | 1600–2200 | Common | [32-20-the-rank-function-and-submodularity.md](./32-20-the-rank-function-and-submodularity.md) |
| 33 | The Dual Matroid ($M^*$) | `B-tier` | 1600–2200 | Common | [33-20-the-dual-matroid-m.md](./33-20-the-dual-matroid-m.md) |
| 34 | Cocycles and the "Reverse Greedy" Algorithm | `B-tier` | 1600–2200 | Common | [34-20-cocycles-and-the-reverse-greedy-algorithm.md](./34-20-cocycles-and-the-reverse-greedy-algorithm.md) |
| 35 | Python Implementation: The Matroid Rank Oracle | `B-tier` | 1600–2200 | Common | [35-20-python-implementation-the-matroid-rank-oracle.md](./35-20-python-implementation-the-matroid-rank-oracle.md) |
| 36 | Identifying Submodular / Dual Problems | `B-tier` | 1600–2200 | Common | [36-20-identifying-submodular-dual-problems.md](./36-20-identifying-submodular-dual-problems.md) |
| 37 | The Core Idea: Bipartite Swapping | `B-tier` | 1600–2200 | Common | [37-20-the-core-idea-bipartite-swapping.md](./37-20-the-core-idea-bipartite-swapping.md) |
| 38 | The Exchange Graph ($G_I$) | `B-tier` | 1600–2200 | Common | [38-20-the-exchange-graph-g-i.md](./38-20-the-exchange-graph-g-i.md) |
| 39 | The Augmenting Path | `B-tier` | 1600–2200 | Common | [39-20-the-augmenting-path.md](./39-20-the-augmenting-path.md) |
| 40 | Python Conceptual Implementation | `B-tier` | 1600–2200 | Common | [40-20-python-conceptual-implementation.md](./40-20-python-conceptual-implementation.md) |
| 41 | Weighted Matroid Intersection | `B-tier` | 1600–2200 | Common | [41-20-weighted-matroid-intersection.md](./41-20-weighted-matroid-intersection.md) |
| 42 | What is an Antimatroid? | `B-tier` | 1600–2200 | Common | [42-20-what-is-an-antimatroid.md](./42-20-what-is-an-antimatroid.md) |
| 43 | Lawler's Algorithm: The Reverse Greedy on Antimatroids | `B-tier` | 1600–2200 | Common | [43-20-lawler-s-algorithm-the-reverse-greedy-on-antimatroids.md](./43-20-lawler-s-algorithm-the-reverse-greedy-on-antimatroids.md) |
| 44 | Dilworth's Theorem and Posets | `B-tier` | 1600–2200 | Common | [44-20-dilworth-s-theorem-and-posets.md](./44-20-dilworth-s-theorem-and-posets.md) |
| 45 | Python Implementation: Kahn's Algorithm + Priority Queue | `B-tier` | 1600–2200 | Common | [45-20-python-implementation-kahn-s-algorithm-priority-queue.md](./45-20-python-implementation-kahn-s-algorithm-priority-queue.md) |
| 46 | Identifying Antimatroid / Scheduling Patterns | `B-tier` | 1600–2200 | Common | [46-20-identifying-antimatroid-scheduling-patterns.md](./46-20-identifying-antimatroid-scheduling-patterns.md) |
| 47 | The Mathematical Origin of WQS Binary Search | `S-tier in Grandmaster/IOI contests` | 1600–2200 | Essential for high-tier CF (2200–2600+) | [47-20-the-mathematical-origin-of-wqs-binary-search.md](./47-20-the-mathematical-origin-of-wqs-binary-search.md) |
| 48 | When Multiple Counts Share the Same Optimal Tangency | `B-tier` | 1600–2200 | Common | [48-20-when-multiple-counts-share-the-same-optimal-tangency.md](./48-20-when-multiple-counts-share-the-same-optimal-tangency.md) |
| 49 | Handling Two Simultaneous Constraints ($K$ and $L$) | `B-tier` | 1600–2200 | Common | [49-20-handling-two-simultaneous-constraints-k-and-l.md](./49-20-handling-two-simultaneous-constraints-k-and-l.md) |
| 50 | The Greedy Descent (Maximizing XOR) | `B-tier` | 1600–2200 | Common | [50-20-the-greedy-descent-maximizing-xor.md](./50-20-the-greedy-descent-maximizing-xor.md) |
| 51 | Python Implementation: The Flat Array Trie | `B-tier` | 1600–2200 | Common | [51-20-python-implementation-the-flat-array-trie.md](./51-20-python-implementation-the-flat-array-trie.md) |
| 52 | The Prefix XOR Invariant | `B-tier` | 1600–2200 | Common | [52-20-the-prefix-xor-invariant.md](./52-20-the-prefix-xor-invariant.md) |
| 53 | Maintaining Subtree Sizes & Dynamic MEX | `B-tier` | 1600–2200 | Common | [53-20-maintaining-subtree-sizes-dynamic-mex.md](./53-20-maintaining-subtree-sizes-dynamic-mex.md) |
| 54 | The Greedy Routing Logic | `B-tier` | 1600–2200 | Common | [54-20-the-greedy-routing-logic.md](./54-20-the-greedy-routing-logic.md) |
| 55 | Python Implementation: The Walkable SegTree | `B-tier` | 1600–2200 | Common | [55-20-python-implementation-the-walkable-segtree.md](./55-20-python-implementation-the-walkable-segtree.md) |
| 56 | Constrained Walking | `B-tier` | 1600–2200 | Common | [56-20-constrained-walking.md](./56-20-constrained-walking.md) |
| 57 | Advanced Applications: Resource Allocation | `B-tier` | 1600–2200 | Common | [57-20-advanced-applications-resource-allocation.md](./57-20-advanced-applications-resource-allocation.md) |
| 58 | The Theorem: The Bottleneck Test | `B-tier` | 1600–2200 | Common | [58-20-the-theorem-the-bottleneck-test.md](./58-20-the-theorem-the-bottleneck-test.md) |
| 59 | The CP Translation: Intervals on a Line | `B-tier` | 1600–2200 | Common | [59-20-the-cp-translation-intervals-on-a-line.md](./59-20-the-cp-translation-intervals-on-a-line.md) |
| 60 | The "Greedy + Hall's Oracle" Pattern | `B-tier` | 1600–2200 | Common | [60-20-the-greedy-hall-s-oracle-pattern.md](./60-20-the-greedy-hall-s-oracle-pattern.md) |
| 61 | Python Implementation: The Lazy Segment Tree Oracle | `B-tier` | 1600–2200 | Common | [61-20-python-implementation-the-lazy-segment-tree-oracle.md](./61-20-python-implementation-the-lazy-segment-tree-oracle.md) |
| 62 | Nim and the XOR Invariant | `B-tier` | 1600–2200 | Common | [62-20-nim-and-the-xor-invariant.md](./62-20-nim-and-the-xor-invariant.md) |
| 63 | The Sprague-Grundy Theorem | `B-tier` | 1600–2200 | Common | [63-20-the-sprague-grundy-theorem.md](./63-20-the-sprague-grundy-theorem.md) |
| 64 | Python Implementation: MEX & Grundy DP | `B-tier` | 1600–2200 | Common | [64-20-python-implementation-mex-grundy-dp.md](./64-20-python-implementation-mex-grundy-dp.md) |
| 65 | The Subgame Split Rule | `B-tier` | 1600–2200 | Common | [65-20-the-subgame-split-rule.md](./65-20-the-subgame-split-rule.md) |
| 66 | Periodicity in Grundy Sequences | `B-tier` | 1600–2200 | Common | [66-20-periodicity-in-grundy-sequences.md](./66-20-periodicity-in-grundy-sequences.md) |
| 67 | What is Slope Trick? | `S-tier (Turns $O(N^2)$ DP into $O(N \log N)$)` | 1600–2200 | Classic in Codeforces 2000–2600+ | [67-20-what-is-slope-trick.md](./67-20-what-is-slope-trick.md) |
| 68 | Adding an Absolute Penalty $|x - a|$ | `B-tier` | 1600–2200 | Common | [68-20-adding-an-absolute-penalty-x-a.md](./68-20-adding-an-absolute-penalty-x-a.md) |
| 69 | Prefix Minimum Transformation: $g(x) = \min_{y \le x} f(y)$ | `B-tier` | 1600–2200 | Common | [69-20-prefix-minimum-transformation-g-x-min-y-le-x-f-y.md](./69-20-prefix-minimum-transformation-g-x-min-y-le-x-f-y.md) |
| 70 | Suffix Minimum Transformation: $g(x) = \min_{y \ge x} f(y)$ | `B-tier` | 1600–2200 | Common | [70-20-suffix-minimum-transformation-g-x-min-y-ge-x-f-y.md](./70-20-suffix-minimum-transformation-g-x-min-y-ge-x-f-y.md) |
| 71 | Sliding / Infimal Convolution: $g(x) = \min_{y \in [x - d_R, x - d_L]} f(y)$ | `B-tier` | 1600–2200 | Common | [71-20-sliding-infimal-convolution-g-x-min-y-in-x-d-r-x-d-l-f-y.md](./71-20-sliding-infimal-convolution-g-x-min-y-in-x-d-r-x-d-l-f-y.md) |
| 72 | What is a Matroid? | `A-tier (Provides the ultimate structural proof for when greedy is globally optimal)` | 2200–2600+ | Common | [72-20-what-is-a-matroid.md](./72-20-what-is-a-matroid.md) |
| 73 | The Universal Greedy Algorithm | `B-tier` | 1600–2200 | Common | [73-20-the-universal-greedy-algorithm.md](./73-20-the-universal-greedy-algorithm.md) |
| 74 | Uniform Matroid $U_{k, n}$ | `B-tier` | 1600–2200 | Common | [74-20-uniform-matroid-u-k-n.md](./74-20-uniform-matroid-u-k-n.md) |
| 75 | Graphic Matroid $M(G)$ | `B-tier` | 1600–2200 | Common | [75-20-graphic-matroid-m-g.md](./75-20-graphic-matroid-m-g.md) |
| 76 | Vector (Linear) Matroid over $\mathbb{F}_2$ | `B-tier` | 1600–2200 | Common | [76-20-vector-linear-matroid-over-mathbb-f-2.md](./76-20-vector-linear-matroid-over-mathbb-f-2.md) |
| 77 | Partition Matroid | `B-tier` | 1600–2200 | Common | [77-20-partition-matroid.md](./77-20-partition-matroid.md) |
| 78 | Submodularity as Discrete Concavity | `B-tier` | 1600–2200 | Common | [78-20-submodularity-as-discrete-concavity.md](./78-20-submodularity-as-discrete-concavity.md) |
| 79 | The Dual Matroid $M^*$ | `B-tier` | 1600–2200 | Common | [79-20-the-dual-matroid-m.md](./79-20-the-dual-matroid-m.md) |
| 80 | Why Two Matroids Break Greedy, and How Augmenting Paths Fix It | `A-tier (The ultimate tool for multi-constraint combinatorial problems)` | 2400–2800 | Common | [80-20-why-two-matroids-break-greedy-and-how-augmenting-paths-fix-it.md](./80-20-why-two-matroids-break-greedy-and-how-augmenting-paths-fix-it.md) |
| 81 | Sources and Sinks | `B-tier` | 1600–2200 | Common | [81-20-sources-and-sinks.md](./81-20-sources-and-sinks.md) |
| 82 | Directed Swap Edges | `B-tier` | 1600–2200 | Common | [82-20-directed-swap-edges.md](./82-20-directed-swap-edges.md) |
| 83 | The Augmentation Step | `B-tier` | 1600–2200 | Common | [83-20-the-augmentation-step.md](./83-20-the-augmentation-step.md) |
| 84 | First Principles: What is an Antimatroid? | `B-tier` | 1600–2200 | Common | [84-20-first-principles-what-is-an-antimatroid.md](./84-20-first-principles-what-is-an-antimatroid.md) |
| 85 | Lawler's Algorithm ($1 \mid prec \mid f_{\max}$) | `B-tier` | 1600–2200 | Common | [85-20-lawler-s-algorithm-1-mid-prec-mid-f-max.md](./85-20-lawler-s-algorithm-1-mid-prec-mid-f-max.md) |
| 86 | Dilworth's Theorem for Posets | `B-tier` | 1600–2200 | Common | [86-20-dilworth-s-theorem-for-posets.md](./86-20-dilworth-s-theorem-for-posets.md) |
| 87 | The MSB Dominance Principle in Bitwise Optimization | `S-tier (Essential in Codeforces 1800–2300)` | 1600–2200 | Common | [87-20-the-msb-dominance-principle-in-bitwise-optimization.md](./87-20-the-msb-dominance-principle-in-bitwise-optimization.md) |
| 88 | Single-Pass $O(\log N)$ Binary Search on SegTrees | `B-tier` | 1600–2200 | Common | [88-20-single-pass-o-log-n-binary-search-on-segtrees.md](./88-20-single-pass-o-log-n-binary-search-on-segtrees.md) |
| 89 | Dynamic Verification of Bipartite Matchability | `B-tier` | 1600–2200 | Common | [89-20-dynamic-verification-of-bipartite-matchability.md](./89-20-dynamic-verification-of-bipartite-matchability.md) |
| 90 | MEX Evaluation and Independent Subgame Superposition | `B-tier` | 1600–2200 | Common | [90-20-mex-evaluation-and-independent-subgame-superposition.md](./90-20-mex-evaluation-and-independent-subgame-superposition.md) |
| 91 | Prerequisites & Relationship to Section 19 | `B-tier` | 1600–2200 | Common | [91-20-prerequisites-relationship-to-section-19.md](./91-20-prerequisites-relationship-to-section-19.md) |
| 92 | Prerequisites & Progression | `B-tier` | 1600–2200 | Common | [92-20-prerequisites-progression.md](./92-20-prerequisites-progression.md) |
