# Line Intersection

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation / cross, vector algebra  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation / cross, vector algebra

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

Two lines in 2D either intersect in one point, are parallel (no meet), or coincide. Parametric form \(P + t\,D\) turns intersection into solving a 2×2 linear system; the determinant is a cross product of directions. For predicates (do they meet?), stay integer; for the actual point, you usually need rationals or `long double`.

---

## 4. Proof Sketches & Recurrences

Line 1: \(P + t\,R\), line 2: \(Q + u\,S\).
\[
P + t R = Q + u S \implies t(R\times S)=(Q-P)\times S.
\]
If \(R\times S = 0\): parallel (and coincident if \((Q-P)\times R = 0\)).
Else \(t = ((Q-P)\times S)/(R\times S)\), point \(P + t R\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1)
- Total: O(1)
- Memory: O(1)`

### C++17 Template

```cpp
namespace geo {
struct Ptd { long double x, y; };

bool lineIntersect(Pt p, Pt r, Pt q, Pt s, Ptd& out) {
    // lines p + t r and q + u s  (r,s = direction vectors as Pts)
    __int128 crs = cross128(r, s);
    if (crs == 0) return false; // parallel or coincident — treat as no unique point
    __int128 t_num = cross128(q - p, s);
    long double t = (long double)t_num / (long double)crs;
    out = {p.x + t * r.x, p.y + t * r.y};
    return true;
}

// through points (a,b) and (c,d)
bool lineIntersectPts(Pt a, Pt b, Pt c, Pt d, Ptd& out) {
    return lineIntersect(a, b - a, c, d - c, out);
}

int lineRelation(Pt a, Pt b, Pt c, Pt d) {
    // 0 parallel distinct, 1 coincident, 2 intersect uniquely
    auto crs = cross128(b - a, d - c);
    if (crs != 0) return 2;
    if (cross128(a, b, c) == 0) return 1;
    return 0;
}
} // namespace geo
```

### Python 3 Template

```python
# Exact rational intersection when needed:
# t = ((Q-P)×S) / (R×S) as Fraction
from fractions import Fraction

def line_intersect_rational(p, r, q, s):
    crs = r.x * s.y - r.y * s.x
    if crs == 0:
        return None
    t = Fraction((q.x - p.x) * s.y - (q.y - p.y) * s.x, crs)
    return (p.x + t * r.x, p.y + t * r.y)
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Intersection of two infinite lines”
- Constructing a point defined as line∩line then continuing geometry
- Checking parallel / coincident before dividing

---

## 7. Contest WA / TLE / RE Traps

- Dividing by cross ≈ 0 with floats → huge wrong point (EPS: treat \|cross\| < EPS as parallel).
- Returning an intersection for **coincident** lines as if unique.
- Using `float` instead of `long double`.
- Direction vectors (0,0) — degenerate line.
- Integer overflow before cast to long double.

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

- Segment vs line: check t∈[0,1] or u∈[0,1] after solve.
- Perpendicular through point: rotate direction (dx,dy)→(-dy,dx).
- Intersection of many lines: usually pairwise or dualize to half-planes.

---

## 11. Typical Problem Archetypes

1. Standard application: find intersection coordinate, print with precision.
2. Slightly disguised: reflection — intersect with mirror line.
3. Difficult: arrangement of lines counting cells (sweep / incremental).
4. Very difficult / advanced: exact predicates + constructed points in cascade (precision death).

---

## 12. Recognition & Identification Drills

1. Given two lines as point+direction, classify parallel / coincident / intersect and output point.
2. Find intersection of diagonals of a convex quadrilateral (lines, not segments).
3. Count distinct intersection points among n lines (n ≤ 1e3).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: infinite lines, constructed points
- Key invariant: unique iff direction cross ≠ 0
- Key formula: \(t=((Q-P)\times S)/(R\times S)\)
- Complexity: O(1)
- Template to remember: parametric solve + parallel check

---

## 3. Segment intersection

---
