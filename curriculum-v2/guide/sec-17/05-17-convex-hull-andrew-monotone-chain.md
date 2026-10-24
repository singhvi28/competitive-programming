# 5. Convex Hull (Andrew Monotone Chain)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, sorting  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, sorting

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

Sort points by (x, y). Build lower hull left→right keeping only CCW turns; build upper hull right→left similarly. Concatenate. Collinear-on-edge policy is a single comparison change (`<=` vs `<`). Andrew’s chain is the contest default: short, robust, O(n log n).

---

## 4. Proof Sketches & Recurrences

Lower hull invariant: stack is a CCW chain. When adding p, while last turn is not CCW (or not strictly CCW), pop. Same for upper with the reversed pass. Correctness: after sort, each point is considered once per chain; extreme points remain. Complexity: sort O(n log n) + amortized O(n) pops.

**Strict vs non-strict:**  
- Keep collinear on hull: pop while `orient <= 0` becomes pop while `orient < 0` (depending on CCW convention).  
- Standard “no unnecessary collinear”: while `cross <= 0` pop (for CCW lower hull).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: —
- Total: O(n log n) time
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
// returns CCW hull, starting from leftmost-lowest; no duplicate consecutive;
// keeps only extreme points (drops middle collinear). n>=1
vector<Pt> convexHull(vector<Pt> pts) {
    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    int n = (int)pts.size();
    if (n <= 1) return pts;
    vector<Pt> h(2 * n);
    int k = 0;
    for (int i = 0; i < n; i++) {
        while (k >= 2 && cross128(h[k - 2], h[k - 1], pts[i]) <= 0) --k;
        h[k++] = pts[i];
    }
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross128(h[k - 2], h[k - 1], pts[i]) <= 0) --k;
        h[k++] = pts[i];
    }
    h.resize(k - 1); // drop duplicated start point
    return h;
}

// shoelace; CCW positive. returns 2*area
ll twiceArea(const vector<Pt>& poly) {
    __int128 a = 0;
    int n = (int)poly.size();
    for (int i = 0; i < n; i++) {
        Pt p = poly[i], q = poly[(i + 1) % n];
        a += (__int128)p.x * q.y - (__int128)p.y * q.x;
    }
    if (a < 0) a = -a;
    return (ll)a;
}
} // namespace geo
```

### Python 3 Template

```python
def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 1:
        return pts
    def build(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and cross(h[-1] - h[-2], p - h[-2]) <= 0:
                h.pop()
            h.append(p)
        return h
    lower = build(pts)
    upper = build(reversed(pts))
    return lower[:-1] + upper[:-1]
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Smallest convex set containing points”
- Diameter / width of a set (hull first)
- Gift wrapping only if h tiny and you know it
- “Vertices of the fence”

---

## 7. Contest WA / TLE / RE Traps

- **All collinear:** hull should be 2 endpoints if dropping collinear middles — check `<= 0` pops correctly.
- Duplicates not removed → zero edges / degenerate crosses.
- Off-by-one when concatenating upper/lower (duplicate endpoints).
- CW vs CCW mismatch with later calipers code.
- Using `long long` cross with 1e9 coords → overflow WA.
- Integer points with same x: sort by y matters for stability of lower/upper.

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

- Keep collinear boundary points: use `< 0` instead of `<= 0` in while (for CCW).
- Lower hull only (for CHT geometry dual — related but different section).
- Dynamic hull (set of upper/lower tangents) — harder, rare.
- 3D convex hull — niche.

---

## 11. Typical Problem Archetypes

1. Standard application: output hull vertices in order.
2. Slightly disguised: minimum perimeter fence / wrapping.
3. Difficult: hull tricks + binary search tangents from external point.
4. Very difficult / advanced: offline dynamic hull, layers of onion peeling.

---

## 12. Recognition & Identification Drills

1. Build hull; verify all input points have orient ≤ 0 (or ≥ 0) vs each edge.
2. Stress all-collinear and duplicate-heavy inputs.
3. Compute hull area via shoelace; match triangle fan from interior point.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: extreme points, prelude to calipers/diameter
- Key invariant: monotone chain CCW turns
- Key formula: while cross ≤ 0 pop
- Complexity: O(n log n)
- Template to remember: Andrew lower+upper

---

Next: [17-b — Rotating calipers → Circles](17-b-computational-geometry.md)

---
