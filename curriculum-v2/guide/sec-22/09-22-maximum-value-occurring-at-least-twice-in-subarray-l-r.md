# 9. Maximum Value Occurring At Least Twice in Subarray $[L, R]$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Sweep line, Offline Range Queries, Segment Tree, Previous Occurrence Map
- Tradeoff: Solves frequency-conditioned range queries offline in $\mathcal{O}((N + Q) \log N)$ instead of heavy online persistent trees.

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

To answer queries 'What is the maximum value that appears at least twice in subarray $[L, R]$?': process queries offline sorted by their right endpoint $R$. For each element $A[R]$, let $prev[R]$ be its previous occurrence index in the array. $A[R]$ appears at least twice in $[L, R]$ if and only if $L \le prev[R]$! Therefore, as the sweep line advances to $R$, we update the position $prev[R]$ in a Segment tree with value $A[R]$ (and remove the previous occurrence's older activation). To answer a query with left bound $L$, we simply query the maximum value in the segment tree on range $[L, R]$!

---

## 4. Proof Sketches & Recurrences

An element $v$ appears at least twice in $[L, R]$ iff the second-to-last occurrence of $v$ up to $R$ is $\ge L$. Let $p_1(v)$ be the last occurrence of $v$ and $p_2(v)$ be the second-to-last occurrence. When the sweep line is at $R = p_1(v)$, $v$ becomes an eligible candidate for any query with $L \le p_2(v)$. In the Segment Tree over array indices $1..N$, we activate index $p_2(v)$ with weight $v$. A query for subarray $[L, R]$ asks for $\max_{i \in [L, R]} tree[i]$. Each right-endpoint advance performs $\mathcal{O}(1)$ point updates on the Segment Tree, yielding $\mathcal{O}((N + Q) \log N)$ total time.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Maximum Duplicate Query via Offline Segment Tree Sweep
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int L, R, id;
    bool operator<(const Query& o) const { return R < o.R; }
};

struct MaxSegTree {
    int n;
    vector<int> tree;
    MaxSegTree(int n) : n(n), tree(2 * n, -1) {}
    
    void update(int p, int val) {
        for (p += n, tree[p] = max(tree[p], val); p > 1; p >>= 1) {
            tree[p >> 1] = max(tree[p], tree[p ^ 1]);
        }
    }
    
    int query(int l, int r) {
        int res = -1;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = max(res, tree[l++]);
            if (r & 1) res = max(res, tree[--r]);
        }
        return res;
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Query asks for max/min value appearing at least $K$ times (especially $K = 2$) in subarray $[L, R]$.
- Count of distinct elements in subarray $[L, R]$ (activate latest occurrence with $+1$, clear previous occurrence).
- Sum of elements appearing at least once / at least twice in range $[L, R]$.
- Offline range queries where eligibility depends on occurrence frequencies.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to clear older activations: when element $v$ appears for the 3rd time at $R$, the 2nd occurrence becomes the new threshold, and the 1st occurrence must be deactivated (set to 0) in the segment tree.
- 1-based vs 0-based indexing mismatch between array queries and segment tree.
- Queries with no valid duplicate: returning 0 or $-1$ correctly when no element appears twice.
- Sorting queries by $L$ instead of $R$ (requires reversing the sweep direction).

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
