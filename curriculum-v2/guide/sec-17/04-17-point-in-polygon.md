# 4. Point-in-Polygon

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, on-segment, ray or winding idea  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, on-segment, ray or winding idea

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

**Ray casting:** shoot a ray to +∞; odd crossings ⇒ inside (for simple polygons). Vertices and edges parallel to the ray are landmines — use a careful crossing rule (e.g., count only edges straddling the ray with an upward/downward convention).

**Winding number:** sum signed crossings / angle; nonzero ⇒ inside for closed curves. Cleaner with orientation; still need an explicit boundary test.

Always decide **BOUNDARY** as a third answer when problems ask IN/ON/OUT.

---

## 4. Proof Sketches & Recurrences

Ray casting (half-open edge rule): for edge (xi,yi)–(xj,yj), count a crossing if the edge straddles y = py and the x-intersect is strictly to the right of px, using a consistent endpoint rule so vertices are not double-counted:
\[
\text{cross if } (y_i > p_y) \neq (y_j > p_y) \text{ and } p_x < \text{xinterp}.
\]
Winding (integer version via crosses): for each edge, add +1/−1 when a ray crosses upward/downward.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (or O(n) store)
- Per-query / per-operation: O(n) general; O(log n) convex
- Total: O(n) / O(q log n) convex
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
// polygon p[0..n-1], not necessarily closed in array (we wrap)
enum class Loc { OUT, ON, IN };

Loc pointInPolygon(const vector<Pt>& poly, Pt p) {
    int n = (int)poly.size();
    for (int i = 0; i < n; i++) {
        Pt a = poly[i], b = poly[(i + 1) % n];
        if (onSegment(a, b, p)) return Loc::ON;
    }
    // winding via ray crossings (integer-safe)
    ll wn = 0;
    for (int i = 0; i < n; i++) {
        Pt a = poly[i], b = poly[(i + 1) % n];
        if (a.y <= p.y) {
            if (b.y > p.y && cross128(a, b, p) > 0) ++wn; // upward cross
        } else {
            if (b.y <= p.y && cross128(a, b, p) < 0) --wn; // downward
        }
    }
    return wn == 0 ? Loc::OUT : Loc::IN;
}

// convex polygon O(log n): binary search fans from poly[0] (CCW convex)
Loc pointInConvex(const vector<Pt>& poly, Pt p) {
    int n = (int)poly.size();
    for (int i = 0; i < n; i++)
        if (onSegment(poly[i], poly[(i + 1) % n], p)) return Loc::ON;
    if (orient(poly[0], poly[1], p) < 0) return Loc::OUT;
    if (orient(poly[0], poly[n - 1], p) > 0) return Loc::OUT;
    int l = 1, r = n - 1;
    while (r - l > 1) {
        int m = (l + r) / 2;
        if (orient(poly[0], poly[m], p) >= 0) l = m;
        else r = m;
    }
    // p in triangle poly[0], poly[l], poly[r]
    return orient(poly[l], poly[r], p) >= 0 ? Loc::IN : Loc::OUT;
}
} // namespace geo
```

### Python 3 Template

```python
def point_in_polygon(poly, p):
    n = len(poly)
    for i in range(n):
        if on_segment(poly[i], poly[(i + 1) % n], p):
            return "ON"
    wn = 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if a.y <= p.y:
            if b.y > p.y and cross(b - a, p - a) > 0:
                wn += 1
        else:
            if b.y <= p.y and cross(b - a, p - a) < 0:
                wn -= 1
    return "IN" if wn != 0 else "OUT"
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Is the point inside the fence?”
- Lattice points in polygon (combine with Pick — separate)
- Geofencing / regions on plane

---

## 7. Contest WA / TLE / RE Traps

- **Vertex grazing:** double-count or miss — use strict half-open y-rule.
- Horizontal edges: must not break parity; winding rule above handles via y-straddle.
- Forgetting ON-boundary as separate case.
- Assuming CCW input when using signed area tests inconsistently.
- Ray casting with floats through a vertex → classic WA.
- Self-intersecting polygons: “inside” ill-defined; winding still defined.

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

- Multiple queries static polygon: preprocess trapezoids / triangulation (rare in CF).
- Polygon with holes: winding per ring or even-odd per component.
- Lattice-only: still geometry, or Pick’s theorem for area/counts.

---

## 11. Typical Problem Archetypes

1. Standard application: IN/ON/OUT for one polygon.
2. Slightly disguised: points strictly inside convex hull.
3. Difficult: many queries + large polygon → O(log n) convex or offline.
4. Very difficult / advanced: point location in planar subdivision.

---

## 12. Recognition & Identification Drills

1. Classify points for a non-convex simple polygon including edge cases on vertices.
2. Implement O(log n) for convex CCW polygon; stress vs O(n).
3. Decide even-odd vs nonzero winding for a self-touching ring.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: membership tests; prefer winding + onSegment
- Key invariant: boundary first, then wn ≠ 0
- Key formula: upward/downward cross signs
- Complexity: O(n) or O(log n) convex
- Template to remember: ON check + winding loop

---

## 5. Convex hull

---
