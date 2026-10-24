# Circle Geometry Basics

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Vectors, quadratic equations, `long double`  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Vectors, quadratic equations, `long double`

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

Circles force floats (or careful algebraic rewriting). Core toolkit: circle–circle intersection, circle–line intersection, tangents from a point, power of a point, radical ideas lightly. Prefer solving with squared radii to delay `sqrt`. Treat EPS as part of the algorithm, not an afterthought.

---

## 4. Proof Sketches & Recurrences

Circle–circle: centers O1,O2, radii r1,r2, d=|O1O2|.
No intersect if d>r1+r2 or d<|r1-r2| (strict with EPS).
Intersect chord is perpendicular to O1O2 at distance
\[
a=\frac{r1^2-r2^2+d^2}{2d}
\]
from O1; half-chord \(h=\sqrt{\max(0,r1^2-a^2)}\).

Line–circle: project center to line, compare distance to r.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1) intersections
- Total: O(1) / O(n) for n circles pairwise locally
- Memory: O(1)`

### C++17 Template

```cpp
namespace geo {
const long double EPS = 1e-9L;
const long double PI = acosl(-1.0L);

struct Circle { Ptd o; long double r; };

int circleCircleIntersect(Circle a, Circle b, Ptd& p1, Ptd& p2) {
    long double d = sqrtl((a.o.x - b.o.x) * (a.o.x - b.o.x) +
                          (a.o.y - b.o.y) * (a.o.y - b.o.y));
    if (d < EPS) return 0; // coincident centers: 0 or infinitely many — treat as none
    if (d > a.r + b.r + EPS || d < fabsl(a.r - b.r) - EPS) return 0;
    long double aa = (a.r * a.r - b.r * b.r + d * d) / (2.0L * d);
    long double h2 = a.r * a.r - aa * aa;
    if (h2 < -EPS) return 0;
    long double h = sqrtl(max(0.0L, h2));
    Ptd mid = {a.o.x + aa * (b.o.x - a.o.x) / d,
               a.o.y + aa * (b.o.y - a.o.y) / d};
    if (h < EPS) { p1 = mid; return 1; } // tangent
    Ptd dx = {(b.o.y - a.o.y) / d, (a.o.x - b.o.x) / d}; // unit perpendicular
    p1 = {mid.x + h * dx.x, mid.y + h * dx.y};
    p2 = {mid.x - h * dx.x, mid.y - h * dx.y};
    return 2;
}

// line through A,B ; circle c
int lineCircleIntersect(Ptd A, Ptd B, Circle c, Ptd& p1, Ptd& p2) {
    Ptd d = {B.x - A.x, B.y - A.y};
    Ptd f = {A.x - c.o.x, A.y - c.o.y};
    long double aa = d.x * d.x + d.y * d.y;
    long double bb = 2 * (f.x * d.x + f.y * d.y);
    long double cc = f.x * f.x + f.y * f.y - c.r * c.r;
    long double disc = bb * bb - 4 * aa * cc;
    if (disc < -EPS) return 0;
    disc = sqrtl(max(0.0L, disc));
    long double t1 = (-bb - disc) / (2 * aa);
    long double t2 = (-bb + disc) / (2 * aa);
    p1 = {A.x + t1 * d.x, A.y + t1 * d.y};
    if (fabsl(disc) < EPS) return 1;
    p2 = {A.x + t2 * d.x, A.y + t2 * d.y};
    return 2;
}

// length of tangents from point p to circle; -1 if inside
long double tangentLength(Ptd p, Circle c) {
    long double d2 = (p.x - c.o.x) * (p.x - c.o.x) + (p.y - c.o.y) * (p.y - c.o.y);
    long double v = d2 - c.r * c.r;
    if (v < -EPS) return -1;
    return sqrtl(max(0.0L, v));
}
} // namespace geo
```

### Python 3 Template

```python
import math

def circle_circle_intersect(o1, r1, o2, r2, eps=1e-9):
    x1, y1 = o1
    x2, y2 = o2
    d = math.hypot(x2 - x1, y2 - y1)
    if d > r1 + r2 + eps or d < abs(r1 - r2) - eps or d < eps:
        if abs(d - (r1 + r2)) <= eps or abs(d - abs(r1 - r2)) <= eps:
            pass
        else:
            return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h2 = r1 * r1 - a * a
    if h2 < -eps:
        return []
    h = math.sqrt(max(0.0, h2))
    mx, my = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d
    if h < eps:
        return [(mx, my)]
    rx, ry = -(y2 - y1) * (h / d), (x2 - x1) * (h / d)
    return [(mx + rx, my + ry), (mx - rx, my - ry)]
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Intersection of circles / common area”
- Tangents, Apollonius-style (rare)
- Points at equal distance (perpendicular bisector → line, then circle)

---

## 7. Contest WA / TLE / RE Traps

- **One EPS does not fit all:** `1e-9` vs `1e-12` vs relative EPS; coordinates in 1e6 with radii 1e-3 break absolute EPS.
- Tangent vs disjoint: `d` vs `r1+r2` within EPS — decide inclusive policy matching the statement (“touch counts as intersect”).
- `h2` slightly negative from rounding — clamp with `max(0, h2)`, but if largely negative it’s truly separate.
- Using `float` / `double` when judge diffs need `long double` + `printf` precision (`setprecision(10)` / 15).
- Degenerate line A==B in line–circle.
- Angle formulas with `acos` arguments outside \([-1,1]\) — clamp before `acos`.
- Mixing exact integer predicates with float-constructed centers → inconsistent “point on circle.”
- Circle–circle with **nearly coincident centers** — division by `d` explodes; special-case `d < EPS`.
- Area of intersection (lens): formula uses `acos`; clamp and watch r=0.

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

## 10. Algorithmic Variants & Advanced Extensions

- Common area of two circles (lens formula).
- Minimum enclosing circle (randomized O(n) expected) — situational.
- Inversion geometry — niche.

---

## 11. Typical Problem Archetypes

1. Standard application: intersect two circles, output points.
2. Slightly disguised: find points at distance r1 from A and r2 from B.
3. Difficult: tangents + constructions chain with precision.
4. Very difficult / advanced: arrangements of circles, MEC with constraints.

---

## 12. Recognition & Identification Drills

1. Classify 0/1/2 intersection points for random circle pairs near tangency.
2. Line–circle with tangent line; ensure one point.
3. Power of a point: verify tangent length² = power.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: circles, equal-distance loci
- Key invariant: clamp tiny negative discriminants; special-case d≈0
- Key formula: \(a=(r1^2-r2^2+d^2)/(2d)\), \(h=\sqrt{r1^2-a^2}\)
- Complexity: O(1)
- Template to remember: circle–circle + line–circle + EPS policy

---

## Back to section hub

[Section 17 overview, comparisons, drills](17-computational-geometry.md)

---
