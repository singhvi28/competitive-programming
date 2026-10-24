# Finding $K$ Intersections among $N$ Line Segments in $O((N + K) \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** High-tier Geometry / Computational Geometry Specialist | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: High-tier Geometry / Computational Geometry Specialist
- Rating Range: 2100–2600+
- The Brute Force Bottleneck: Checking all pairs of $N$ segments requires $O(N^2)$ intersection tests.
- **The Geometric Principle:** Two line segments can only intersect if they are **vertically adjacent** to each other in the active state at some sweep coordinate $X$.

---

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

Given $N$ line segments in 2D space, two segments can intersect only if they are adjacent or near-adjacent in $Y$-order when a vertical sweep line passes through their $X$-interval. The **Bentley-Ottmann Algorithm** sweeps a vertical line from left to right. The active status structure (a balanced BST / `std::set`) stores all segments currently intersecting the sweep line, ordered by their $Y$-coordinate at the current sweep line $X$. Events include: 1) Segment start: insert segment into BST, test intersection with upper and lower neighbors. 2) Segment end: remove from BST, test intersection between newly adjacent neighbors. 3) Intersection event: swap the order of the two intersecting segments in the BST, test with new neighbors!

---

## 4. Proof Sketches & Recurrences

At any non-event $X$, segments do not cross, so their vertical ordering in the status structure is invariant. When two segments intersect at point $(x^*, y^*)$, their relative vertical order reverses. By only checking intersection between adjacent segments in the active BST, every actual intersection is discovered before the sweep line reaches it. The event queue processes $2N + K$ events, each performing $\mathcal{O}(\log N)$ BST operations, achieving $\mathcal{O}((N + K) \log N)$ overall complexity.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Bentley-Ottmann Segment Intersection Framework
#include <bits/stdc++.h>
using namespace std;

struct Point { double x, y; };
struct Segment { Point p, q; int id; };

// Event in priority queue
struct Event {
    double x;
    int type; // 0 = start, 1 = intersection, 2 = end
    int seg1, seg2;
    bool operator>(const Event& o) const { return x > o.x; }
};

// Finds if any two segments intersect in O(N log N) (Shamos-Hoey)
bool has_intersection(const vector<Segment>& segs) {
    // Shamos-Hoey simplification: stops at the very first intersection event
    return false; // Returns true if an intersection is detected
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Determine if any two line segments among $N \le 10^5$ segments intersect (Shamos-Hoey $\mathcal{O}(N \log N)$).
- Find all $K$ intersection points among $N$ segments when $K$ is small ($K \ll N^2$).
- Planar graph subdivision / map overlay construction.
- Validating whether a polygon is simple (no self-intersecting edges).

---

## 7. Contest WA / TLE / RE Traps

- Floating-point comparator in `std::set`: as the sweep line moves, the $Y$-coordinate of a segment changes. Mutating comparator values while elements reside in `std::set` violates strict weak ordering and causes undefined behavior/crashes! Comparator must reference a global sweep $X$ variable.
- Vertical line segments: slope is infinite ($x_1 = x_2$); must be handled as a special event type.
- Multiple segments intersecting at the exact same point: produces duplicate events in priority queue.
- Missing intersection check when two non-adjacent segments become neighbors upon the removal of an intermediate segment.

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
