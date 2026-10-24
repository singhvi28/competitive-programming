# Dimensional Reduction via Event Processing

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–1900 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Typical CF rating range: 1400–1900
- Core Concept: Transforming a static $D$-dimensional problem into a dynamic $(D-1)$-dimensional active state evolving along a sweeping axis.

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

In a static array or geometric setting, an interval $[L, R]$ with value $V$ is typically viewed as a contiguous block. The fundamental shift in the **Sweep Line** technique is deconstructing each interval into independent, atomic point **events** in time:
1. **Start Event at $L$:** Interval enters the active state ($+V$).
2. **End Event at $R + 1$:** Interval leaves the active state ($-V$).
3. **Query Event at $X$:** Inspect the active state at coordinate $X$.

By sorting all events chronologically along the sweep axis and processing them sequentially, the global state at any point $X$ is evaluated via a running prefix sum of deltas.

```
Interval [L, R]  ========================>
Events:          +-----------------------+
                 ^                       ^
            Start at L              End at R+1
            (Delta +V)              (Delta -V)
```

---

## 4. Proof Sketches & Recurrences

Consider $N$ 2D points or rectangles. Checking all pairs in 2D space takes $\mathcal{O}(N^2)$. By sorting the $2N$ boundary events along the $X$-axis in $\mathcal{O}(N \log N)$, the sweep line maintains only the currently active elements intersecting the line $x = X_{cur}$. The active set is maintained in a Fenwick or Segment Tree indexed by the $Y$-coordinate. Each event causes $\mathcal{O}(1)$ modifications to the 1D tree, leading to an overall runtime of $\mathcal{O}(N \log N)$ and $\mathcal{O}(N)$ space.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Dimensional Reduction via Sweep Line Event Processing
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Event {
    ll x;
    int type; // 0 = Add interval, 1 = Query point, 2 = Remove interval
    ll y1, y2;
    int id;
    bool operator<(const Event& o) const {
        if (x != o.x) return x < o.x;
        return type < o.type; // Process additions before queries before removals
    }
};

void sweep_line_events(vector<Event>& events) {
    sort(events.begin(), events.end());
    // Fenwick tree or active set over Y coordinates
    for (const auto& ev : events) {
        if (ev.type == 0) { /* insert [y1, y2] into active set */ }
        else if (ev.type == 1) { /* query y1 in active set */ }
        else if (ev.type == 2) { /* remove [y1, y2] from active set */ }
    }
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- 1. **Start Events (+1):** Processed **first** (intervals become active before queries evaluate).
- 2. **Query Events (0):** Processed **second** (reads the exact inclusive active state).
- 3. **End Events (-1):** Processed **third** (intervals that end at $X$ remain active for queries at $X$, and are removed only afterwards).
- 

---

## 7. Contest WA / TLE / RE Traps

- Event tie-breaking: when events share the exact same $X$-coordinate, processing order matters critically. If intervals are closed $[L, R]$, additions must be processed before queries, which must be processed before deletions.
- Coordinate compression omission: $Y$-coordinates up to $10^9$ must be mapped to $[0, K-1]$ before inserting into standard array-backed Fenwick/Segment trees.
- Forgetting to clear or un-insert expired elements on exit events, leaving stale entries in the active structure.
- Using 32-bit `int` for $X$ or $Y$ coordinates when products or sums exceed $2 \times 10^9$.

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
