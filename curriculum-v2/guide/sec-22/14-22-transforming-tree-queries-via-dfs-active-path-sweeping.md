# Transforming Tree Queries via DFS Active-Path Sweeping

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Tree DFS, Root-to-Node Active Path, Fenwick Tree / Stack Rollback
- Tradeoff: Solves ancestor-path queries in $\mathcal{O}((N + Q) \log N)$ with $\mathcal{O}(N)$ memory, eliminating heavy binary lifting tables or HLD.

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

To answer queries about ancestors on the path from root to node $u$ (e.g. 'How many ancestors of $u$ have weight $\le W$ and depth $\ge D$?'): attach all queries for node $u$ to an adjacency list `queries[u]`. Run a single DFS from the root. When entering node $u$, insert $u$'s value into a global data structure (Fenwick tree or monotone stack). While at $u$, answer all queries attached to $u$ by directly querying the data structure! When exiting node $u$ (backtracking), remove $u$'s value from the data structure. The data structure exclusively contains elements on the active path from root to $u$!

---

## 4. Proof Sketches & Recurrences

During a DFS traversal, the call stack corresponds exactly to the simple path from the root to the currently visited node $u$. By inserting node $u$ on entry and retracting node $u$ on exit, the active data structure maintains the multiset $\{v : v \text{ is an ancestor of } u\}$. Each node is inserted once and deleted once. If the data structure is a Fenwick Tree, total time spent across the entire tree is $2N \log N$, and answering $Q$ queries takes $\mathcal{O}(Q \log N)$. Memory is strictly $\mathcal{O}(N + Q)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// DFS Active-Path Sweeping Framework
#include <bits/stdc++.h>
using namespace std;

struct Query { int val, id; };

struct ActivePathSweep {
    int n;
    vector<vector<int>> adj;
    vector<vector<Query>> queries;
    vector<int> ans;
    ActivePathSweep(int n_, int q_) : n(n_), adj(n_ + 1), queries(n_ + 1), ans(q_) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void add_query(int u, int val, int qid) { queries[u].push_back({val, qid}); }
    void dfs(int u, int p) {
        // 1. Enter: Insert u into active path data structure (e.g. BIT)
        // ... bit.add(val[u], +1); ...
        // 2. Answer all queries for node u
        for (const auto& q : queries[u]) {
            // ans[q.id] = bit.query(q.val);
        }
        // 3. Recurse into children
        for (int v : adj[u]) if (v != p) dfs(v, u);
        // 4. Exit: Retract u from active path data structure
        // ... bit.add(val[u], -1); ...
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Query asks for properties of ancestors of $u$ (e.g. number of ancestors with property $P$).
- Finding the nearest ancestor satisfying a condition (maintain monotone stack on active path with binary search).
- Path queries where the path is strictly vertical (from node to root).
- Counting tree paths with sum $\le S$ starting from an ancestor.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to retract on exit: failing to remove node $u$ from the data structure on exit leaks its values into sibling subtrees.
- Stack overflow: deep skew trees ($N = 2 \times 10^5$) require `#pragma comment(linker, "/STACK:...")` or manual stack unwinding.
- Modifying query answers after backtracking: answers must be recorded immediately while visiting node $u$.
- Applying active path sweeping to arbitrary paths $u \leftrightarrow v$ without splitting the query at $\text{LCA}(u, v)$.

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
