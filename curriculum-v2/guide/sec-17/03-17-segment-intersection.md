# 3. Segment Intersection

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, on-segment  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, on-segment

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

Proper intersection: endpoints of each segment are on opposite sides of the other. Improper: share an endpoint or overlap collinearly. The classic 4-orientation test handles general position; collinear overlap needs interval overlap on the line.

---

## 4. Proof Sketches & Recurrences

Segments AB, CD. Let
\[
o1=\mathrm{orient}(A,B,C),\; o2=\mathrm{orient}(A,B,D),\;
o3=\mathrm{orient}(C,D,A),\; o4=\mathrm{orient}(C,D,B).
\]
Proper: \(o1\neq o2\) and \(o3\neq o4\) with all nonzero.
General (including touch): also true if a point lies on the other segment when some orient is 0.
Collinear overlap: all oriients 0 and projections overlap on x (and y).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1)
- Total: O(1) pairwise; O(n²) all pairs
- Memory: O(1)`

### C++17 Template

```cpp
namespace geo {
bool segmentsIntersect(Pt a, Pt b, Pt c, Pt d) {
    int o1 = orient(a, b, c), o2 = orient(a, b, d);
    int o3 = orient(c, d, a), o4 = orient(c, d, b);
    if (o1 != o2 && o3 != o4) return true; // general (includes proper)
    // collinear touching / overlap
    if (o1 == 0 && onSegment(a, b, c)) return true;
    if (o2 == 0 && onSegment(a, b, d)) return true;
    if (o3 == 0 && onSegment(c, d, a)) return true;
    if (o4 == 0 && onSegment(c, d, b)) return true;
    return false;
}

bool segmentsProperIntersect(Pt a, Pt b, Pt c, Pt d) {
    int o1 = orient(a, b, c), o2 = orient(a, b, d);
    int o3 = orient(c, d, a), o4 = orient(c, d, b);
    return o1 && o2 && o3 && o4 && (o1 != o2) && (o3 != o4);
}

// optional: actual intersection point (long double); assumes intersect exists
bool segmentIntersectionPoint(Pt a, Pt b, Pt c, Pt d, Ptd& out) {
    Pt r = b - a, s = d - c;
    __int128 crs = cross128(r, s);
    __int128 t_num = cross128(c - a, s);
    if (crs == 0) {
        // collinear: return any shared point if needed by problem
        if (onSegment(a, b, c)) { out = {(long double)c.x, (long double)c.y}; return true; }
        if (onSegment(a, b, d)) { out = {(long double)d.x, (long double)d.y}; return true; }
        if (onSegment(c, d, a)) { out = {(long double)a.x, (long double)a.y}; return true; }
        if (onSegment(c, d, b)) { out = {(long double)b.x, (long double)b.y}; return true; }
        return false;
    }
    long double t = (long double)t_num / (long double)crs;
    out = {a.x + t * r.x, a.y + t * r.y};
    return true;
}
} // namespace geo
```

### Python 3 Template

```python
def segments_intersect(a, b, c, d) -> bool:
    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(a, b, c): return True
    if o2 == 0 and on_segment(a, b, d): return True
    if o3 == 0 and on_segment(c, d, a): return True
    if o4 == 0 and on_segment(c, d, b): return True
    return False
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Do these two sticks cross?”
- Map / planar graph edges
- Geometry + graph: segments as obstacles
- Prelude to sweep-line segment intersection

---

## 7. Contest WA / TLE / RE Traps

- **Collinear overlap:** forgotten → WA on “touching sticks.”
- Endpoint touch: problem says “intersect” vs “strictly cross” — read statement.
- Zero-length segments (a==b): `onSegment` still works if careful.
- Using float EPS for orientation on integer inputs.
- Overflow in cross.

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

- Closed vs open segments (exclude endpoints).
- Count intersections among n segments → sweep (§8) if n large.
- Intersection point uniqueness vs segment overlap (continuum).

---

## 11. Typical Problem Archetypes

1. Standard application: yes/no two segments intersect.
2. Slightly disguised: edges of polygons intersect ⇒ not simple.
3. Difficult: build intersection graph of segments.
4. Very difficult / advanced: Bentley–Ottmann reporting all k intersections.

---

## 12. Recognition & Identification Drills

1. Handle collinear overlapping segments correctly for YES/NO.
2. Detect if a polygon is simple (no two non-adjacent edges intersect).
3. Given n≤2e3 segments, count intersecting pairs.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: pairwise segment tests, n small or inner check in sweep
- Key invariant: opposite orientations ⇒ cross
- Key formula: four `orient` + collinear `onSegment`
- Complexity: O(1)
- Template to remember: `segmentsIntersect` including collinear cases

---

## 4. Point-in-polygon

---
