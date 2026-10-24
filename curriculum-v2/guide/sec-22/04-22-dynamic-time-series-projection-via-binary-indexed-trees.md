# 4. Dynamic Time-Series Projection via Binary Indexed Trees

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Rating Range: 1600–2200
- Core Invariant: Sweeping along the $X$-axis satisfies the $X$-coordinate constraint for free, allowing an auxiliary **Fenwick Tree** to maintain and query the dynamic distribution of active $Y$-coordinates in $O(\log N)$.

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

To count points lying strictly inside a 2D bounding box $[x_1, x_2] \times [y_1, y_2]$:
1. Deconstruct the query into two 1D events:
   - **Left Query at $x_1 - 1$:** Query $\text{count}(y_1, y_2)$ and subtract from result.
   - **Right Query at $x_2$:** Query $\text{count}(y_1, y_2)$ and add to result.
2. Sort all point insertions and query events along the $X$-axis.
3. As the sweep line moves right, insert point $y$-coordinates into the Fenwick Tree.
4. When reaching a query event at $X$, query the Fenwick tree for the range $[y_1, y_2]$.

```
          Y ^
            |          [ Point (x, y) inserted into Fenwick ]
            |              +-----------------------+ (x2, y2)
            |              |                       |
            |              |   Active 2D Region    |
            |              |                       |
            |              +-----------------------+
            |        (x1, y1)
            +----------------------------------------------------> X
                      ^                             ^
                 Query at x1-1                 Query at x2
                 (Subtract)                    (Add)
```

---

## 2. 2D Point Dominance & Inversion Counting

---

## 4. Proof Sketches & Recurrences

A 2D query $(x \in [x_1, x_2], y \in [y_1, y_2])$ can be decomposed into two prefix queries via linearity: $Q(x_2) - Q(x_1 - 1)$. By grouping and sorting queries by their $X$-threshold, elements with $x_i \le X$ are inserted into the Fenwick tree monotonically. The Fenwick tree maintains frequency counts over $Y$ coordinates. Point updates and prefix queries both run in $\mathcal{O}(\log |Y|)$ time with cache-friendly contiguous array memory.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Dynamic Time-Series Projection via Offline BIT Sweep
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<ll> tree;
    Fenwick(int n_) : n(n_), tree(n_ + 1, 0) {}
    void add(int i, ll delta) { for (; i <= n; i += i & -i) tree[i] += delta; }
    ll query(int i) { ll sum = 0; for (; i > 0; i -= i & -i) sum += tree[i]; return sum; }
    ll query_range(int l, int r) { return query(r) - query(l - 1); }
};

struct Query { int l, r, k, id; };

// Count elements in subarray [l, r] with value >= k
vector<int> count_elements_ge_k(vector<int>& a, vector<Query>& queries) {
    int n = a.size(), q = queries.size();
    vector<int> ans(q);
    // Sort elements and queries by value descending
    // ... (Sweep elements into Fenwick indexed by position 1..n) ...
    return ans;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Queries ask for number of elements in range $[L, R]$ satisfying value constraints $A_i \ge K$.
- Counting inversions dynamically as a sequence is built.
- Offline range distinct elements (SPOJ DQUERY): sweep right endpoint $R$, insert current position, remove previous occurrence.
- Prefix sums on a dynamically activated subset of points.

---

## 7. Contest WA / TLE / RE Traps

- 0-based indexing in Fenwick: `i += i & -i` loops infinitely if $i = 0$; Fenwick trees must always be 1-indexed.
- Fenwick tree size: `tree` must be sized to the maximum possible compressed coordinate, not the number of queries.
- Off-by-one in prefix difference: querying range $[L, R]$ requires `query(R) - query(L - 1)`, not `query(L)`.
- Mixing up offline sorting order: queries sorted in opposite direction to elements.

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
