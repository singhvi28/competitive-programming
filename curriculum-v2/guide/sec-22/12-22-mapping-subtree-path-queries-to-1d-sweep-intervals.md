# Mapping Subtree & Path Queries to 1D Sweep Intervals

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Trees are hierarchical, non-linear graphs. Sweep lines require an ordered, 1D domain.
- By assigning pre-order entry times (`in[u]`) and exit times (`out[u]`) during a single DFS, **subtrees become contiguous 1D subsegments**.

```
Tree Hierarchy:              Euler Tour Flattening (Pre-order):
       (1)                    Index:  0   1   2   3   4
      /   \                   Node:  [1] [2] [4] [5] [3]
    (2)   (3)                         |_________|
   /   \                              Subtree of 2:
 (4)   (5)                            in[2] = 1, out[2] = 4 -> [1, 3]
```

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

## 3. Core Intuition & Problem Framing

1. **Subtree of node $u$:** Exactly the 1D range $[in[u], out[u] - 1]$.
2. **Descendant Test in $O(1)$:** Node $v$ is inside subtree of $u \iff in[u] \le in[v] < out[u]$.
3. **Subtree-to-Subsegment Transformation:** Any tree query (e.g. "count distinct values in subtree of $u$", "find max duplicate in subtree of $u$") is transformed into a standard 1D range query $[L, R]$ on the flattened array.

---

## 3. The Circular Doubled Euler Tour ($A + A$) Trick

---

## 4. Proof Sketches & Recurrences

In an Euler tour DFS, every node in $u$'s subtree is visited after $tin[u]$ and before $tout[u]$. Therefore, $v \in \text{subtree}(u) \iff tin[u] \le tin[v] \le tout[u]$. Any subtree condition combined with an auxiliary parameter (depth, weight, time of activation) becomes a 2D box query $[tin[u], tout[u]] \times [d_{\min}, d_{\max}]$. Sorting vertices and queries by the auxiliary parameter allows a 1D Fenwick tree over $[1, N]$ to answer all queries in $\mathcal{O}((N + Q) \log N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Tree Subtree Queries via Euler Tour Linearization & Offline BIT Sweep
#include <bits/stdc++.h>
using namespace std;

struct TreeSweep {
    int n, timer = 0;
    vector<vector<int>> adj;
    vector<int> tin, tout;
    TreeSweep(int n_) : n(n_), adj(n_ + 1), tin(n_ + 1), tout(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void dfs(int u, int p) {
        tin[u] = ++timer;
        for (int v : adj[u]) if (v != p) dfs(v, u);
        tout[u] = timer;
    }
    // Subtree of u is strictly the range [tin[u], tout[u]]
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count nodes in subtree of $u$ with value $\ge X$ or depth $\le K$.
- Path queries where paths are converted to pairs of Euler tour updates.
- DSU on tree alternative for offline queries.
- Subtree distinct color counting (combine with previous occurrence sweep).

---

## 7. Contest WA / TLE / RE Traps

- Euler tour timer off-by-one: initializing timer to 0 vs 1; Fenwick tree requires 1-indexed positions.
- Visiting back-edges in undirected trees: must guard with `if (v != p)` during DFS.
- Tree path vs subtree: subtree is a single contiguous interval; paths between $u$ and $v$ require HLD or double-entry Euler tour ($tin[u]$ and $tout[u]$).
- Forgetting that $tout[u] = timer$ must be assigned AFTER all children have been traversed.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

## 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---
