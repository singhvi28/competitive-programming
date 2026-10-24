# Orientation / Cross Product

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Occasional (but foundational whenever geometry appears)  
> **Prerequisites:** Vectors, 2D coordinates  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional (but foundational whenever geometry appears)
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Vectors, 2D coordinates

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

The 2D cross product \(a_x b_y - a_y b_x\) is the signed parallelogram area. Sign tells orientation: positive = CCW turn from \(\vec{a}\) to \(\vec{b}\) (under standard math coords with y up — same formula works in screen coords; only “which sign is left” flips with axis conventions, not the algebra). Almost every geometry predicate collapses to “sign of one cross.”

---

## 4. Proof Sketches & Recurrences

For \(\vec{u}=A\to B\), \(\vec{v}=A\to C\):
\[
\mathrm{cross}(u,v)=u_x v_y - u_y v_x = |u||v|\sin\theta.
\]
- `> 0`: CCW (left turn if traveling A→B then to C)
- `= 0`: collinear
- `< 0`: CW (right turn)

Area of triangle ABC: \(\frac{1}{2}|\mathrm{cross}(B-A,C-A)|\).

Overflow: if coordinates are in \([-10^9,10^9]\), differences fit in 32-bit signed range roughly 2e9, products need 64-bit carefully — prefer `__int128` for cross when \(|x|,|y|\le 10^9\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: O(1)
- Total: O(1) per predicate
- Memory: O(1)`

### C++17 Template

```cpp
namespace geo {
int sgn128(__int128 v) { return (v > 0) - (v < 0); }
// returns 1 if O->A->B is CCW, -1 if CW, 0 if collinear
int orient(Pt o, Pt a, Pt b) { return sgn128(cross128(o, a, b)); }

bool onSegment(Pt a, Pt b, Pt p) { // p on segment ab (inclusive), assumes collinear check separate or included
    if (orient(a, b, p) != 0) return false;
    return p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x)
        && p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y);
}

// polar compare around origin o: smaller angle first; ties by distance
bool polarLess(Pt o, Pt a, Pt b) {
    int oa = (a.y > o.y || (a.y == o.y && a.x >= o.x)) ? 0 : 1; // half-plane trick optional
    int ob = (b.y > o.y || (b.y == o.y && b.x >= o.x)) ? 0 : 1;
    if (oa != ob) return oa < ob;
    auto cr = cross128(o, a, b);
    if (cr != 0) return cr > 0;
    // same ray: nearer first
    auto da = (__int128)(a.x - o.x) * (a.x - o.x) + (__int128)(a.y - o.y) * (a.y - o.y);
    auto db = (__int128)(b.x - o.x) * (b.x - o.x) + (__int128)(b.y - o.y) * (b.y - o.y);
    return da < db;
}
} // namespace geo
```

### Python 3 Template

```python
from typing import NamedTuple

class Pt(NamedTuple):
    x: int
    y: int
    def __sub__(self, p: "Pt") -> "Pt":
        return Pt(self.x - p.x, self.y - p.y)

def cross(a: Pt, b: Pt) -> int:
    return a.x * b.y - a.y * b.x

def orient(o: Pt, a: Pt, b: Pt) -> int:
    v = cross(a - o, b - o)
    return (v > 0) - (v < 0)

def on_segment(a: Pt, b: Pt, p: Pt) -> bool:
    if orient(a, b, p) != 0:
        return False
    return min(a.x, b.x) <= p.x <= max(a.x, b.x) and min(a.y, b.y) <= p.y <= max(a.y, b.y)
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Is C left/right of directed line AB?”
- “Collinear / turn direction for hull”
- “Do three points form a left turn?” (Andrew / Graham)
- Polar angle sorting around a point (via cross, not `atan2` when possible)

---

## 7. Contest WA / TLE / RE Traps

- **`long long` overflow:** on cross when coords are 1e9 — silent WA. Use `__int128`.
- Mixing `atan2` sort with cross predicates → inconsistent order near axes.
- Assuming “left = positive” without matching the problem’s coordinate system (rarely an issue if you stay consistent).
- Using `== 0` with floats for collinearity — never for integer geometry.
- Forgetting collinear points are “on line” but may be outside the segment.

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

- **Dot product:** acute/obtuse angles, projection length squared.
- **Squared distances:** avoid `sqrt` until output.
- **3-point area / polygon shoelace:** sum of crosses.

---

## 11. Typical Problem Archetypes

1. Standard application: count left turns along a path.
2. Slightly disguised: “can the robot turn without crossing?” → orientation.
3. Difficult: polar sort + unique rays for angular sweep.
4. Very difficult / advanced: exact predicates for higher geometry (still built on cross).

---

## 12. Recognition & Identification Drills

1. Given directed line AB and point C, output LEFT / RIGHT / ON.
2. Sort points by angle around the lowest point; break ties by distance.
3. Detect whether polyline is strictly convex (all turns same sign, no collinear).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: any turn / side / collinearity test
- Key invariant: sign(cross) is orientation
- Key formula: \((B-A)\times(C-A)\)
- Complexity: O(1)
- Template to remember: `orient(o,a,b)` + `__int128` cross

---

## 2. Line intersection

---
