# 13. Ray casting vs winding (point-in-polygon)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Point in Polygon, Ray Casting, Winding Number, Cross Product
- Tradeoff: Ray casting is simple parity counting but has tricky boundary edge cases; winding number is robust against complex/self-intersecting polygons.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

## 3. Core Intuition & Problem Framing

To determine whether a query point $P$ lies inside a polygon: 1) **Ray Casting Algorithm** shoots a horizontal ray from $P$ to $(+\infty, y_P)$ and counts intersections with polygon edges. If the number of crossings is odd, $P$ is inside; if even, $P$ is outside. 2) **Winding Number Algorithm** computes the total number of counter-clockwise revolutions made by the polygon boundaries around $P$. Non-zero winding number $\implies$ inside. Winding number handles self-intersecting polygons and is immune to vertex-grazing ambiguities when implemented with cross product signs.

---

## 4. Proof Sketches & Recurrences

Jordan Curve Theorem: Any continuous simple closed curve divides the plane into an 'inside' and an 'outside'. A ray starting from infinity (outside) alternates between inside and outside with each boundary crossing. For winding number, edge $(A, B)$ contributes $+1$ to the winding count if it crosses the horizontal ray upwards and $P$ is to the left of the edge, and $-1$ if it crosses downwards and $P$ is to the right.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Robust Point in Polygon via Winding Number (Integer Precision)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point { ll x, y; };
ll cross_product(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Returns: 1 if inside, 0 if outside, -1 if strictly on boundary
int point_in_polygon(Point p, const vector<Point>& poly) {
    int n = poly.size();
    int wn = 0;
    for (int i = 0; i < n; ++i) {
        Point a = poly[i], b = poly[(i + 1) % n];
        // Check if p is on segment ab
        if (cross_product(a, b, p) == 0 &&
            min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
            min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y)) return -1;
        if (a.y <= p.y) {
            if (b.y > p.y && cross_product(a, b, p) > 0) wn++;
        } else {
            if (b.y <= p.y && cross_product(a, b, p) < 0) wn--;
        }
    }
    return wn != 0 ? 1 : 0;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Query asks whether a point lies strictly inside, outside, or on the boundary of an arbitrary polygon.
- Geofencing or territorial containment queries in computational geometry.
- Polygon triangulation or ear clipping preprocessing.
- Testing point containment in non-convex polygons where binary search on angle cannot be used.

---

## 7. Contest WA / TLE / RE Traps

- Ray passes exactly through a polygon vertex: standard ray casting double-counts or misses the intersection unless half-open vertical intervals $[y_1, y_2)$ are strictly enforced.
- Horizontal polygon edges: ray overlaps collinear horizontal edges; ensure horizontal segments are ignored or explicitly handled.
- Forgetting boundary check: query point lies exactly on an edge or vertex, but the algorithm reports strictly inside or outside.
- Polygon vertices not oriented in consistent order (CCW or CW).

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---
