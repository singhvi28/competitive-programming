# 11. B. FIRST PRINCIPLES & ALGORITHM MECHANICS

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Meta-Methodology for all Sweep Line Problems
- Typical CF/ICPC rating range: 1500–2400
- Prerequisites: Invariants, Event Queues, Active Status Structures
- Blueprint: The 3 invariant laws governing all sweep line algorithms.

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

Every sweep-line algorithm without exception consists of exactly three fundamental components: 1) **The Sweep Space**: A continuous dimension (time, $X$-axis, tree depth) along which execution advances monotonically. 2) **The Event Queue**: A priority queue or sorted array of discrete points where the topological state of the system changes. 3) **The Active Status Structure**: A dynamic data structure (Fenwick, Segment Tree, Treap, `std::set`) that maintains the cross-section of objects currently active at the sweep frontier. The invariant is that the status structure is 100% accurate for the current sweep frontier position.

---

## 4. Proof Sketches & Recurrences

Let the continuous state space be $\Omega$. If state transitions only occur at discrete coordinates $E = \{e_1, e_2, \dots, e_M\}$, then for any $x \in (e_i, e_{i+1})$, the active state is static. Hence, the continuous problem $\int_\Omega f(x) dx$ is discretized into $\sum_{i=1}^{M-1} f(e_i) \cdot (e_{i+1} - e_i)$. The time complexity is bounded by $\mathcal{O}(M \log M + M \cdot T_{\text{update}})$, converting continuous geometry into discrete algebra.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++ Contest Template — Bentley-Ottmann Concept & Segment Intersection
#include <bits/stdc++.h>
using namespace std;

struct Point {
    double x, y;
    bool operator<(const Point& o) const {
        if (abs(x - o.x) > 1e-9) return x < o.x;
        return y < o.y;
    }
};

struct Segment {
    Point p1, p2; // p1.x <= p2.x
    int id;
    
    double get_y(double current_x) const {
        if (abs(p1.x - p2.x) < 1e-9) return p1.y;
        return p1.y + (p2.y - p1.y) * (current_x - p1.x) / (p2.x - p1.x);
    }
};

double sweep_x = 0;

struct SegmentComparator {
    bool operator()(const Segment& a, const Segment& b) const {
        double ya = a.get_y(sweep_x);
        double yb = b.get_y(sweep_x);
        if (abs(ya - yb) > 1e-9) return ya < yb;
        return a.id < b.id;
    }
};

// Check if two line segments intersect and return intersection point
bool get_intersection(const Segment& a, const Segment& b, Point& inter) {
    double x1 = a.p1.x, y1 = a.p1.y, x2 = a.p2.x, y2 = a.p2.y;
    double x3 = b.p1.x, y3 = b.p1.y, x4 = b.p2.x, y4 = b.p2.y;
    
    double denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
    if (abs(denom) < 1e-9) return false; // Parallel or collinear
    
    double px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom;
    double py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom;
    
    // Check if (px, py) lies within bounding boxes of both segments
    if (px < min(x1, x2) - 1e-9 || px > max(x1, x2) + 1e-9) return false;
    if (px < min(x3, x4) - 1e-9 || px > max(x3, x4) + 1e-9) return false;
    if (py < min(y1, y2) - 1e-9 || py > max(y1, y2) + 1e-9) return false;
    if (py < min(y3, y4) - 1e-9 || py > max(y3, y4) + 1e-9) return false;
    
    inter = {px, py};
    return true;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Any geometric problem with $N$ static 2D objects.
- Static offline queries on an array that can be processed in sorted order of $R$.
- Tree problems transformed into 1D interval sweeps via Euler tour linearization.
- Interval union, intersection, or coverage metrics.

---

## 7. Contest WA / TLE / RE Traps

- Violating the monotonicity invariant: inserting an event whose coordinate is in the past.
- Imprecise event tie-breaking order leading to phantom state discrepancies.
- Memory explosion: generating dynamic events without deleting expired events.
- Failing to handle empty intervals or points with $L > R$.

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
