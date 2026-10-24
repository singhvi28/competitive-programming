# Section §21: Greedy Advanced (Matroids & Oracles)

> **Module ID:** `sec-21`  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Topic Count:** 20  

**Module Summary:** Axiomatic Matroid theory, Rado-Edmonds greedy optimality, Matroid Intersection augmenting paths in O(R^3 Q), Antimatroids, and Dynamic Verification Oracles.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | What is a Matroid? | `A-tier (Provides the ultimate structural proof for when greedy is globally optimal)` | 2200–2600+ | Common | [01-21-what-is-a-matroid.md](./01-21-what-is-a-matroid.md) |
| 2 | The Universal Greedy Algorithm | `B-tier` | 1600–2200 | Common | [02-21-the-universal-greedy-algorithm.md](./02-21-the-universal-greedy-algorithm.md) |
| 3 | Uniform Matroid $U_{k, n}$ | `B-tier` | 1600–2200 | Common | [03-21-uniform-matroid-u-k-n.md](./03-21-uniform-matroid-u-k-n.md) |
| 4 | Graphic Matroid $M(G)$ | `B-tier` | 1600–2200 | Common | [04-21-graphic-matroid-m-g.md](./04-21-graphic-matroid-m-g.md) |
| 5 | Vector (Linear) Matroid over $\mathbb{F}_2$ | `B-tier` | 1600–2200 | Common | [05-21-vector-linear-matroid-over-mathbb-f-2.md](./05-21-vector-linear-matroid-over-mathbb-f-2.md) |
| 6 | Partition Matroid | `B-tier` | 1600–2200 | Common | [06-21-partition-matroid.md](./06-21-partition-matroid.md) |
| 7 | Submodularity as Discrete Concavity | `B-tier` | 1600–2200 | Common | [07-21-submodularity-as-discrete-concavity.md](./07-21-submodularity-as-discrete-concavity.md) |
| 8 | The Dual Matroid $M^*$ | `B-tier` | 1600–2200 | Common | [08-21-the-dual-matroid-m.md](./08-21-the-dual-matroid-m.md) |
| 9 | Why Two Matroids Break Greedy, and How Augmenting Paths Fix It | `A-tier (The ultimate tool for multi-constraint combinatorial problems)` | 2400–2800 | Common | [09-21-why-two-matroids-break-greedy-and-how-augmenting-paths-fix-it.md](./09-21-why-two-matroids-break-greedy-and-how-augmenting-paths-fix-it.md) |
| 10 | Sources and Sinks | `B-tier` | 1600–2200 | Common | [10-21-sources-and-sinks.md](./10-21-sources-and-sinks.md) |
| 11 | Directed Swap Edges | `B-tier` | 1600–2200 | Common | [11-21-directed-swap-edges.md](./11-21-directed-swap-edges.md) |
| 12 | The Augmentation Step | `B-tier` | 1600–2200 | Common | [12-21-the-augmentation-step.md](./12-21-the-augmentation-step.md) |
| 13 | First Principles: What is an Antimatroid? | `B-tier` | 1600–2200 | Common | [13-21-first-principles-what-is-an-antimatroid.md](./13-21-first-principles-what-is-an-antimatroid.md) |
| 14 | Lawler's Algorithm ($1 \mid prec \mid f_{\max}$) | `B-tier` | 1600–2200 | Common | [14-21-lawler-s-algorithm-1-mid-prec-mid-f-max.md](./14-21-lawler-s-algorithm-1-mid-prec-mid-f-max.md) |
| 15 | Dilworth's Theorem for Posets | `B-tier` | 1600–2200 | Common | [15-21-dilworth-s-theorem-for-posets.md](./15-21-dilworth-s-theorem-for-posets.md) |
| 16 | The MSB Dominance Principle in Bitwise Optimization | `S-tier (Essential in Codeforces 1800–2300)` | 1600–2200 | Common | [16-21-the-msb-dominance-principle-in-bitwise-optimization.md](./16-21-the-msb-dominance-principle-in-bitwise-optimization.md) |
| 17 | Single-Pass $O(\log N)$ Binary Search on SegTrees | `B-tier` | 1600–2200 | Common | [17-21-single-pass-o-log-n-binary-search-on-segtrees.md](./17-21-single-pass-o-log-n-binary-search-on-segtrees.md) |
| 18 | Dynamic Verification of Bipartite Matchability | `B-tier` | 1600–2200 | Common | [18-21-dynamic-verification-of-bipartite-matchability.md](./18-21-dynamic-verification-of-bipartite-matchability.md) |
| 19 | MEX Evaluation and Independent Subgame Superposition | `B-tier` | 1600–2200 | Common | [19-21-mex-evaluation-and-independent-subgame-superposition.md](./19-21-mex-evaluation-and-independent-subgame-superposition.md) |
| 20 | Prerequisites | `B-tier` | 1600–2200 | Common | [20-21-prerequisites.md](./20-21-prerequisites.md) |
