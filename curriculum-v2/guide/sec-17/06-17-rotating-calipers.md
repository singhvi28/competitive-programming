# Rotating Calipers

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Convex hull, orientation / cross, distances  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Convex hull, orientation / cross, distances

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

On a convex polygon, antipodal pairs (supporting parallel lines) march monotonically. After building the hull, diameter (farthest pair), minimum width, maximum distance between parallel supports, and similar metrics are **O(h)** by advancing a pointer — not O(h²). Calipers beat N² when h is large; for n≤2e3 brute on all pairs of the hull (or all points) is acceptable and less buggy.

---

## 4. Proof Sketches & Recurrences

**Diameter:** for convex polygon, the farthest pair is realized by an antipodal pair (vertices with parallel supporting lines). Start with a point and the farthest in one direction; rotate the caliper: when the next edge’s outward direction “wins” the cross comparison, advance the opposite pointer. Each pointer moves O(h) total ⇒ O(h).

Distance compare with squared distances to avoid `sqrt`. Area/width use absolute cross / edge length.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n log n) hull
- Per-query / per-operation: O(h) calipers
- Total: O(n log n)
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
ll dist2(Pt a, Pt b) {
    ll dx = a.x - b.x, dy = a.y - b.y;
    return dx * dx + dy * dy;
}

// diameter squared of point set; O(n log n)
ll convexDiameter2(vector<Pt> pts) {
    auto h = convexHull(std::move(pts));
    int n = (int)h.size();
    if (n <= 1) return 0;
    if (n == 2) return dist2(h[0], h[1]);
    ll best = 0;
    int j = 1;
    for (int i = 0; i < n; i++) {
        int ni = (i + 1) % n;
        while (true) {
            int nj = (j + 1) % n;
            // advance j while area of triangle grows (j farther from edge i->ni)
            __int128 now = abs(cross128(h[i], h[ni], h[j]));
            __int128 nxt = abs(cross128(h[i], h[ni], h[nj]));
            if (nxt > now) j = nj;
            else break;
        }
        best = max(best, dist2(h[i], h[j]));
        best = max(best, dist2(h[ni], h[j]));
    }
    return best;
}

// minimum width squared *related*: min over edges of max height to antipode
// returns (min width)^2 if you compare height^2 = cross^2 / |edge|^2 carefully with doubles,
// or keep as pair (cross^2, edge_len^2) for comparisons.
long double minWidth(const vector<Pt>& h_in) {
    auto h = h_in;
    int n = (int)h.size();
    if (n <= 2) return 0;
    int j = 1;
    long double ans = 1e300L;
    for (int i = 0; i < n; i++) {
        int ni = (i + 1) % n;
        while (true) {
            int nj = (j + 1) % n;
            if (abs(cross128(h[i], h[ni], h[nj])) > abs(cross128(h[i], h[ni], h[j]))) j = nj;
            else break;
        }
        __int128 cr = abs(cross128(h[i], h[ni], h[j]));
        long double edge = sqrtl((long double)dist2(h[i], h[ni]));
        ans = min(ans, (long double)cr / edge);
    }
    return ans;
}
} // namespace geo
```

### Python 3 Template

```python
def convex_diameter2(pts):
    h = convex_hull(pts)
    n = len(h)
    if n <= 1: return 0
    if n == 2:
        d = h[0] - h[1]
        return d.x * d.x + d.y * d.y
    best, j = 0, 1
    def d2(a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
    for i in range(n):
        ni = (i + 1) % n
        while True:
            nj = (j + 1) % n
            if abs(cross(h[ni] - h[i], h[nj] - h[i])) > abs(cross(h[ni] - h[i], h[j] - h[i])):
                j = nj
            else:
                break
        best = max(best, d2(h[i], h[j]), d2(h[ni], h[j]))
    return best
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Maximum distance among points” (diameter of set)
- “Minimum width strip covering points”
- “Farthest opposite buildings” on a convex shape
- After hull, need antipodal structure

---

## 7. Contest WA / TLE / RE Traps

- Running calipers on **non-convex** input — wrong. Hull first.
- Off-by-one when `j` wraps; infinite loop if while condition wrong on parallel edges.
- Comparing distances with `sqrt` + EPS instead of `dist2`.
- Minimum width: dividing by zero on duplicate hull points.
- Using N² on full set when only hull extremes matter (correct but slower); or wrongly assuming diameter endpoints are hull vertices — they are, so hull is required and sufficient.

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

- Maximum distance between two convex polygons (antipodal dual pointers).
- All antipodal pairs enumeration.
- Minimum area / perimeter bounding rectangle with rotating calipers (rotate by edge directions).

---

## 11. Typical Problem Archetypes

1. Standard application: diameter of n points.
2. Slightly disguised: farthest pair after Manhattan↔rotated coords (still hull+calipers or transform).
3. Difficult: min-width strip covering.
4. Very difficult / advanced: rotating calipers + binary search on geometric predicates.

---

## 12. Recognition & Identification Drills

1. Diameter via calipers; verify vs O(h²) on random convex polygons.
2. Min width of a convex polygon; check against all edge–vertex distances.
3. Decide calipers vs N² given n=3e3 vs n=1e5.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: convex metrics after hull; n large
- Key invariant: antipodal pointer only advances
- Key formula: advance while next cross larger
- Complexity: O(n log n)
- Template to remember: hull + two-pointer antipodes

---

## 7. Closest pair

---
