# Integer cross vs floats

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Universal in Computational Geometry
- Typical CF/ICPC rating range: 1400–2500
- Prerequisites: Vector cross product, dot product, orientation tests
- Tradeoff: Floating-point arithmetic suffers from precision breakdown, epsilon tuning nightmares, and `NaN` errors; integer cross products are 100% exact and deterministic.

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

In computational geometry, 95% of contest problems can and should be solved using pure 64-bit or 128-bit integer arithmetic. The cross product of vectors $\vec{u} = (x_1, y_1)$ and $\vec{v} = (x_2, y_2)$ is $\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1$. Its sign deterministically tells whether $\vec{v}$ turns counter-clockwise ($> 0$), clockwise ($< 0$), or is collinear ($= 0$) with $\vec{u}$. Never use `atan2`, slope division $y/x$, or `double` trigonometry to check orientation or sorting.

---

## 4. Proof Sketches & Recurrences

The 2D cross product equals the signed area of the parallelogram formed by $\vec{u}$ and $\vec{v}$. For integer coordinates bounded by $C = 10^9$, the cross product $x_1 y_2 - x_2 y_1$ reaches up to $2 \times 10^{18}$, which fits within signed 64-bit integer `long long`. For products of differences $(x_b - x_a)(y_c - y_a) - (y_b - y_a)(x_c - x_a)$, maximum magnitude is $4 \times 10^{18}$, comfortably within `long long` (or `__int128_t` for intermediate calculations to prevent any overflow).

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// 100% Exact Integer Geometry Point & Orientation Test
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    Point operator-(const Point& o) const { return {x - o.x, y - o.y}; }
    ll cross(const Point& o) const { return x * o.y - y * o.x; }
    ll dot(const Point& o) const { return x * o.x + y * o.y; }
};

// Returns: +1 for CCW (left turn), -1 for CW (right turn), 0 for Collinear
int orient(Point a, Point b, Point c) {
    __int128 val = (__int128)(b.x - a.x) * (c.y - a.y) - (__int128)(b.y - a.y) * (c.x - a.x);
    if (val > 0) return 1;
    if (val < 0) return -1;
    return 0;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Convex Hull construction (Monotone Chain / Graham Scan).
- Checking whether two line segments intersect.
- Testing if a point lies to the left or right of a directed line.
- Sorting points radially around a pivot (half-plane radial sorting without `atan2`).

---

## 7. Contest WA / TLE / RE Traps

- Using `float` or `double` slopes $m = (y_2 - y_1)/(x_2 - x_1)$, causing division by zero on vertical lines and rounding errors on nearly collinear points.
- 32-bit integer overflow: cross product of coordinates up to $10^5$ exceeds $2^{31} - 1$; always use `long long` or `__int128`.
- Using `acos` or `asin` without clamping argument to $[-1.0, 1.0]$, producing `NaN` due to slight floating point drift.
- Comparing floats with strict `== 0.0` instead of `std::abs(x) < 1e-9` when floats are unavoidable.

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
