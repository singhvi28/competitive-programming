# 9. Half-Plane Intersection (Concepts)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** C-tier / Niche (rarely worth early) | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** Lines, convex polygons, polar/deque techniques, robust geometry  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier / Niche (rarely worth early)
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Lines, convex polygons, polar/deque techniques, robust geometry

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

A half-plane is “one side of a directed line” (`cross >= 0`). Intersection of half-planes is a convex (possibly unbounded) polygon. Algorithmically: sort lines by angle, maintain a deque of bounding lines, pop from both ends when the new intersection violates the new constraint — similar spirit to convex hull / CHT dual. Implementation is long and EPS-sensitive; **postpone until forced**.

---

## 4. Proof Sketches & Recurrences

Each constraint: \(a_i x + b_i y + c_i \ge 0\). Normalize direction angle \(\theta=\mathrm{atan2}(b,a)\). Process in angle order; keep deque of lines whose consecutive intersections form the boundary. When inserting line L, while deque size ≥ 2 and intersection of last two not in L’s half-plane, pop back; similarly pop front. Unbounded regions: add large box half-planes if problem asks for a bounded answer, or handle infinite rays carefully.

Complexity O(n log n) from sort + amortized pops.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort O(n log n)
- Per-query / per-operation: —
- Total: O(n log n)
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
// CONCEPT TEMPLATE — use long double; treat as niche.
// Line: through point p with direction d (left side is inside half-plane).
struct Line {
    Ptd p, d; // point + direction; inside = left of directed line
};
const long double HPI_EPS = 1e-12L;

int sgnD(long double v) {
    if (fabsl(v) < HPI_EPS) return 0;
    return v > 0 ? 1 : -1;
}
long double crossD(Ptd a, Ptd b) { return a.x * b.y - a.y * b.x; }
Ptd operator+(Ptd a, Ptd b) { return {a.x + b.x, a.y + b.y}; }
Ptd operator-(Ptd a, Ptd b) { return {a.x - b.x, a.y - b.y}; }
Ptd operator*(Ptd a, long double s) { return {a.x * s, a.y * s}; }

Ptd lineIntersectD(Line a, Line b) {
    // a.p + t a.d = b.p + u b.d
    long double crs = crossD(a.d, b.d);
    long double t = crossD(b.p - a.p, b.d) / crs;
    return a.p + a.d * t;
}
bool out(Line l, Ptd q) { // q strictly right of l
    return sgnD(crossD(l.d, q - l.p)) < 0;
}

// Returns CCW vertices of intersection; empty if empty region.
// Assumes caller added a huge bounding box if a bounded polygon is required.
vector<Ptd> halfplaneIntersection(vector<Line> lines) {
    sort(lines.begin(), lines.end(), [](const Line& a, const Line& b){
        long double A = atan2l(a.d.y, a.d.x), B = atan2l(b.d.y, b.d.x);
        if (fabsl(A - B) > HPI_EPS) return A < B;
        // same angle: keep the tighter parallel half-plane
        return crossD(a.d, b.p - a.p) < 0;
    });
    // unique parallel directions: keep most restrictive
    vector<Line> nlines;
    for (auto &L : lines) {
        if (!nlines.empty() && fabsl(atan2l(nlines.back().d.y, nlines.back().d.x)
            - atan2l(L.d.y, L.d.x)) < HPI_EPS) continue;
        nlines.push_back(L);
    }
    deque<Line> dq;
    deque<Ptd> pts;
    auto check = [&](Line L) {
        while (pts.size() && out(L, pts.back())) { pts.pop_back(); dq.pop_back(); }
        while (pts.size() && out(L, pts.front())) { pts.pop_front(); dq.pop_front(); }
    };
    for (auto &L : nlines) {
        check(L);
        if (dq.size()) pts.push_back(lineIntersectD(dq.back(), L));
        dq.push_back(L);
    }
    check(dq.front());
    if (dq.size() <= 2) return {};
    pts.push_back(lineIntersectD(dq.back(), dq.front()));
    // optional: cleanup near-duplicate vertices with EPS
    vector<Ptd> poly(pts.begin(), pts.end());
    return poly;
}
} // namespace geo
```

---

## 6. Recognition Trigger Signals & Heuristics

- Feasible region of linear inequalities in 2D
- “Intersection of half-planes / kernel of polygon”
- Convex polygon as ∩ of edge half-planes (inside poly)

---

## 7. Contest WA / TLE / RE Traps

- **EPS everywhere:** parallel detection, `atan2` ties, intersection division by near-zero cross, “is point outside?” — tiny EPS changes flip emptiness. Prefer problems with integer half-planes / dualize to hull when possible.
- Forgetting bounding box → “correct” unbounded intersection but empty vertex list.
- Duplicate angles: must keep the tighter constraint.
- Numerically unstable intersection of nearly parallel lines → garbage vertices.
- Using this early in practice instead of learning hull/orientation — poor ROI.

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

- Polygon kernel = ∩ half-planes of edges (for convex is itself; for concave may be empty).
- Linear programming in 2D (Seidel / randomized) — related niche.
- Dual: some half-plane problems ↔ convex hull of points.

---

## 11. Typical Problem Archetypes

1. Standard application: intersect n half-planes, output area.
2. Slightly disguised: feasible (x,y) for inequality system.
3. Difficult: kernel of a polygon.
4. Very difficult / advanced: robust exact arithmetic half-planes.

---

## 12. Recognition & Identification Drills

1. Represent a convex polygon as intersection of half-planes.
2. Manually intersect 4 half-planes forming a triangle + redundant constraint.
3. Decide: is this problem half-planes or “just convex hull of something”?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: ∩ linear inequalities in 2D; rare
- Key invariant: deque of angularly sorted lines
- Key formula: pop while intersection outside new half-plane
- Complexity: O(n log n)
- Template to remember: sort by angle + deque (niche)

---

## 10. Circle geometry basics

---
