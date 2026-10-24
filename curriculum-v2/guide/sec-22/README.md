# Section §22: Line Sweep Algorithms & Reductions

> **Module ID:** `sec-22`  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Topic Count:** 15  

**Module Summary:** Event abstraction, coordinate compression, 1D/2D difference arrays, 2D Fenwick dominance, Klee's Measure rectangle union area, and Bentley-Ottmann line sweep.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | Dimensional Reduction via Event Processing | `S-tier` | 1400–1900 | Common | [01-22-dimensional-reduction-via-event-processing.md](./01-22-dimensional-reduction-via-event-processing.md) |
| 2 | Mapping Sparse $10^9$ Domains to Dense $[0, K-1]$ Ranks | `B-tier` | 1600–2200 | Common | [02-22-mapping-sparse-10-9-domains-to-dense-0-k-1-ranks.md](./02-22-mapping-sparse-10-9-domains-to-dense-0-k-1-ranks.md) |
| 3 | Maximum Overlapping Intervals in $O(N \log N)$ | `B-tier` | 1600–2200 | Common | [03-22-maximum-overlapping-intervals-in-o-n-log-n.md](./03-22-maximum-overlapping-intervals-in-o-n-log-n.md) |
| 4 | Dynamic Time-Series Projection via Binary Indexed Trees | `S-tier` | 1600–2200 | Common | [04-22-dynamic-time-series-projection-via-binary-indexed-trees.md](./04-22-dynamic-time-series-projection-via-binary-indexed-trees.md) |
| 5 | Point Dominance | `B-tier` | 1600–2200 | Common | [05-22-point-dominance.md](./05-22-point-dominance.md) |
| 6 | Multi-Pass / 3-Element Inversions (e.g., Codeforces 61E) | `B-tier` | 1600–2200 | Common | [06-22-multi-pass-3-element-inversions-e-g-codeforces-61e.md](./06-22-multi-pass-3-element-inversions-e-g-codeforces-61e.md) |
| 7 | When Fenwick Trees Fail | `S-tier (The foundation of 2D computational geometry and advanced offline range querying)` | 1900–2400+ | Common | [07-22-when-fenwick-trees-fail.md](./07-22-when-fenwick-trees-fail.md) |
| 8 | Computing Overlapping 2D Rectangle Area in $O(N \log N)$ | `B-tier` | 1600–2200 | Common | [08-22-computing-overlapping-2d-rectangle-area-in-o-n-log-n.md](./08-22-computing-overlapping-2d-rectangle-area-in-o-n-log-n.md) |
| 9 | Maximum Value Occurring At Least Twice in Subarray $[L, R]$ | `B-tier` | 1600–2200 | Common | [09-22-maximum-value-occurring-at-least-twice-in-subarray-l-r.md](./09-22-maximum-value-occurring-at-least-twice-in-subarray-l-r.md) |
| 10 | Finding $K$ Intersections among $N$ Line Segments in $O((N + K) \log N)$ | `High-tier Geometry / Computational Geometry Specialist` | 1600–2200 | Common | [10-22-finding-k-intersections-among-n-line-segments-in-o-n-k-log-n.md](./10-22-finding-k-intersections-among-n-line-segments-in-o-n-k-log-n.md) |
| 11 | B. FIRST PRINCIPLES & ALGORITHM MECHANICS | `B-tier` | 1600–2200 | Common | [11-22-b-first-principles-algorithm-mechanics.md](./11-22-b-first-principles-algorithm-mechanics.md) |
| 12 | Mapping Subtree & Path Queries to 1D Sweep Intervals | `B-tier` | 1600–2200 | Common | [12-22-mapping-subtree-path-queries-to-1d-sweep-intervals.md](./12-22-mapping-subtree-path-queries-to-1d-sweep-intervals.md) |
| 13 | Edge-Cut Tree Component Splitting in $O((N + Q) \log N)$ | `B-tier` | 1600–2200 | Common | [13-22-edge-cut-tree-component-splitting-in-o-n-q-log-n.md](./13-22-edge-cut-tree-component-splitting-in-o-n-q-log-n.md) |
| 14 | Transforming Tree Queries via DFS Active-Path Sweeping | `B-tier` | 1600–2200 | Common | [14-22-transforming-tree-queries-via-dfs-active-path-sweeping.md](./14-22-transforming-tree-queries-via-dfs-active-path-sweeping.md) |
| 15 | Prerequisites | `B-tier` | 1600–2200 | Common | [15-22-prerequisites.md](./15-22-prerequisites.md) |
