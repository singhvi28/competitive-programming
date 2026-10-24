# 5. Point Dominance

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Sweep line, Fenwick Tree, CDQ Divide and Conquer, 2D/3D Dominance
- Tradeoff: Solves 2D point dominance in $\mathcal{O}(N \log N)$ and 3D point dominance in $\mathcal{O}(N \log^2 N)$.

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

Point $A = (x_a, y_a)$ dominates point $B = (x_b, y_b)$ if $x_a \ge x_b$ and $y_a \ge y_b$. Counting how many points each point dominates (or finding the longest chain of dominated points) is 2D Point Dominance. Sorting all points primarily by $X$ ascending eliminates the $X$-coordinate constraint: any point processed earlier automatically has $x_b \le x_a$. The remaining problem is 1D: count how many previously processed points have $y_b \le y_a$, which is a single prefix sum query on a Fenwick tree over $Y$-coordinates!

---

## 4. Proof Sketches & Recurrences

In 2D: sort points by $(x_i, y_i)$. Iterate $i$ from 1 to $N$: query Fenwick for prefix sum up to $y_i$, then insert $y_i$ into Fenwick. Total time is $\mathcal{O}(N \log N)$. In 3D ($x_a \ge x_b, y_a \ge y_b, z_a \ge z_b$): sort by $X$, then apply CDQ Divide and Conquer on $Y$, using a Fenwick tree on $Z$ during the merge step, running in $\mathcal{O}(N \log^2 N)$ without 2D segment trees.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// 2D Point Dominance Counting in O(N log N)
#include <bits/stdc++.h>
using namespace std;

struct Point { int x, y, id; };

vector<int> count_dominated_points(vector<Point>& pts) {
    int n = pts.size();
    vector<int> ans(n, 0);
    // Coordinate compress Y coordinates
    vector<int> ys;
    for (auto& p : pts) ys.push_back(p.y);
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    
    // Sort points: X ascending, Y ascending for ties
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
    });
    
    // Fenwick tree over compressed Y
    int m = ys.size();
    vector<int> bit(m + 1, 0);
    auto add = [&](int i) { for (; i <= m; i += i & -i) bit[i]++; };
    auto query = [&](int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; };
    
    for (const auto& p : pts) {
        int y_rank = lower_bound(ys.begin(), ys.end(), p.y) - ys.begin() + 1;
        ans[p.id] = query(y_rank);
        add(y_rank);
    }
    return ans;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Partial order queries: count pairs $(i, j)$ such that $a_i \le a_j$ and $b_i \le b_j$.
- Longest chain of bounding boxes that can be nested inside one another.
- Skyline / Pareto frontier computation in multi-objective optimization.
- 3D Partial order / Elementary particles problem (CF 1093E, etc.).

---

## 7. Contest WA / TLE / RE Traps

- Strict vs non-strict dominance: if dominance requires $x_a > x_b$ and $y_a > y_b$, identical coordinates require careful tie-breaking (e.g. process identical $X$ points in batch or reverse $Y$ order).
- Coordinate compression forgetting duplicate entries in $Y$.
- Incorrect Fenwick sizing when compressed $Y$ ranks reach $N$.
- Applying 2D sweep directly to 3D without CDQ divide-and-conquer.

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
