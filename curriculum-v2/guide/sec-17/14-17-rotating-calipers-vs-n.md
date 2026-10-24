# 14. Rotating calipers vs N²

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Convex Hull, Antipodal Pairs, Cross Product, Two Pointers
- Tradeoff: Reduces polygon diameter / minimum bounding box from $\mathcal{O}(N^2)$ brute force to $\mathcal{O}(N)$ after $\mathcal{O}(N \log N)$ convex hull.

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

To find the maximum distance between any two points in a 2D set of $N$ points (the polygon diameter), checking all pairs takes $\mathcal{O}(N^2)$, which TLEs for $N = 2 \times 10^5$. The two furthest points must both lie on the vertices of the Convex Hull. Furthermore, the distance from an edge $(P_i, P_{i+1})$ to hull vertices is unimodal: as we advance along hull edges, the furthest opposite vertex (antipodal point) advances monotonically in the same direction. Rotating Calipers maintains an antipodal pointer with two pointers, traversing the entire convex hull in $\mathcal{O}(N)$ total steps!

---

## 4. Proof Sketches & Recurrences

The distance from a point $C$ to the line through $A$ and $B$ is proportional to the triangle area $|(B - A) \times (C - A)|$. Because the polygon is convex, the area function is strictly unimodal. When we advance the base edge from $(P_i, P_{i+1})$ to $(P_{i+1}, P_{i+2})$, the peak of the triangle area also advances counter-clockwise. Thus, the antipodal pointer index $j$ only advances forward and never retreats, wrapping around $N$ vertices in at most $2N$ steps.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Rotating Calipers: Convex Polygon Diameter in O(N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    ll dist_sq(const Point& o) const { return (x - o.x) * (x - o.x) + (y - o.y) * (y - o.y); }
};

ll cross_product(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Returns maximum squared Euclidean distance between any pair of points on convex hull
ll rotating_calipers_diameter(const vector<Point>& hull) {
    int n = hull.size();
    if (n < 2) return 0;
    if (n == 2) return hull[0].dist_sq(hull[1]);
    ll max_dist = 0;
    int j = 1;
    for (int i = 0; i < n; ++i) {
        Point next_i = hull[(i + 1) % n];
        while (cross_product(hull[i], next_i, hull[(j + 1) % n]) >
               cross_product(hull[i], next_i, hull[j])) {
            j = (j + 1) % n;
        }
        max_dist = max({max_dist, hull[i].dist_sq(hull[j]), next_i.dist_sq(hull[j])});
    }
    return max_dist;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Find the maximum Euclidean distance between any two points among $N \le 2 \times 10^5$ points.
- Minimum enclosing bounding box (minimum area or perimeter rectangle enclosing point set).
- Maximum area triangle inscribed in a convex polygon.
- Widest empty corridor between two disjoint convex point sets.

---

## 7. Contest WA / TLE / RE Traps

- Running Rotating Calipers on raw points without computing the Convex Hull first.
- Handling collinear edges on the convex hull: strictly greater `>` vs `>=` in cross product area comparison.
- Degenerate hull size: $N = 1$ or $N = 2$ causes infinite while loop if modular indexing is not guarded.
- Using floating-point sqrt when the problem asks for squared distance, losing precision on large coordinates.

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
