# 8. Sweep Line

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Sorting events, ordered set / fenwick, segment intersection predicates  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Sorting events, ordered set / fenwick, segment intersection predicates

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

Replace a 2D problem with a 1D structure that evolves over “time” (usually x). Critical moments are **events** (start/end of segment, intersection, point query). The active set is ordered by the other coordinate (y). Same pattern appears outside geometry: scheduling, rectangle union, offline 2D counting.

---

## 4. Proof Sketches & Recurrences

**Rectangle union area (axis-aligned):** vertical sweep; events = left/right edges. Active y-intervals in a segment tree on compressed y; measure covered length × Δx. O(n log n).

**Segment intersection existence:** horizontal sweep; status = segments ordered by y at current x; when inserting, test neighbors for intersect; at intersections swap order (Bentley–Ottmann). Full reporting is heavy; contest often needs only specialized sweeps.

Event order must be total and consistent; ties (same x) need a policy: e.g. process verticals carefully, left endpoints before right, etc.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: coordinate compress O(n log n)
- Per-query / per-operation: O(log n) status updates
- Total: typically O(n log n) or O((n+k) log n)
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
// Axis-aligned rectangle union area. Rect = [x1,x2] x [y1,y2], x1<x2, y1<y2.
struct SegTree {
    int n;
    vector<int> cnt;
    vector<ll> len, ys; // ys compressed unique boundaries
    SegTree(vector<ll> y) : ys(std::move(y)) {
        n = (int)ys.size() - 1;
        cnt.assign(4 * n, 0);
        len.assign(4 * n, 0);
    }
    void pull(int v, int l, int r) {
        if (cnt[v] > 0) len[v] = ys[r + 1] - ys[l];
        else if (l == r) len[v] = 0;
        else len[v] = len[v << 1] + len[v << 1 | 1];
    }
    void add(int v, int l, int r, int ql, int qr, int d) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { cnt[v] += d; pull(v, l, r); return; }
        int m = (l + r) >> 1;
        add(v << 1, l, m, ql, qr, d);
        add(v << 1 | 1, m + 1, r, ql, qr, d);
        pull(v, l, r);
    }
    void add(int ql, int qr, int d) { if (ql <= qr) add(1, 0, n - 1, ql, qr, d); }
    ll covered() const { return len[1]; }
};

ll rectangleUnionArea(vector<array<ll,4>> rects) {
    // each: x1,x2,y1,y2
    struct Ev { ll x; int y1, y2, typ; }; // typ +1 left, -1 right
    vector<ll> ys;
    for (auto &r : rects) { ys.push_back(r[2]); ys.push_back(r[3]); }
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    vector<Ev> ev;
    for (auto &r : rects) {
        int y1 = (int)(lower_bound(ys.begin(), ys.end(), r[2]) - ys.begin());
        int y2 = (int)(lower_bound(ys.begin(), ys.end(), r[3]) - ys.begin());
        ev.push_back({r[0], y1, y2, +1});
        ev.push_back({r[1], y1, y2, -1});
    }
    sort(ev.begin(), ev.end(), [](const Ev& a, const Ev& b){
        if (a.x != b.x) return a.x < b.x;
        return a.typ > b.typ; // +1 before -1 at same x
    });
    if (ev.empty()) return 0;
    SegTree st(ys);
    ll ans = 0, prevX = ev[0].x;
    int idx = 0;
    while (idx < (int)ev.size()) {
        ll x = ev[idx].x;
        ans += st.covered() * (x - prevX);
        while (idx < (int)ev.size() && ev[idx].x == x) {
            // cover [y1, y2) in compressed boundary indices
            st.add(ev[idx].y1, ev[idx].y2 - 1, ev[idx].typ);
            idx++;
        }
        prevX = x;
    }
    return ans;
}
} // namespace geo
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Segments on a plane / report intersections”
- Union area of axis-aligned rectangles
- “Closest pair” sweep variant
- Anytime: sort events + maintain ordered active structure

---

## 7. Contest WA / TLE / RE Traps

- Event tie-breaking** wrong (process remove before add at same x) → empty active set / missed cover. **EPS-heavy when sweep coordinate is float** (intersection x): never trust `==` on floats; use exact predicates or rational x, or snap with disciplined order keys.
- Compressing y incorrectly (off-by-one on half-open `[y1,y2)`).
- Segment tree `cnt` vs `len` pull bugs when partial cover.
- Assuming general position (no overlapping endpoints) when tests have them.
- For geometric segment sweep: recomputing y-order with floats at current x → **neighbor order flips spuriously from EPS** → false intersections / infinite event loops. Prefer integer geometry problems or exact orientation tests between adjacent segments.
- Vertical segments: special-case; they don’t define a unique y(x).

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

- Union perimeter of rectangles.
- Sweep for closest pair.
- Discrete sweep on grid / fenwick instead of segtree.
- Angular sweep around a point (sort by polar angle) — cousin technique.

---

## 11. Typical Problem Archetypes

1. Standard application: area of union of rectangles.
2. Slightly disguised: count overlapping intervals while scanning x.
3. Difficult: report whether any two open segments intersect (status + neighbors).
4. Very difficult / advanced: full Bentley–Ottmann with numeric robustness.

---

## 12. Recognition & Identification Drills

1. Union area of n≤1e5 axis-aligned rectangles.
2. Design event order for “add vertical chord, query active count.”
3. Explain why float intersection events are dangerous without exact predicates.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: 2D → events + 1D DS
- Key invariant: active set correct between events
- Key formula: ans += measure × Δx
- Complexity: O(n log n)
- Template to remember: compress + sweep + segtree coverage

---

## 9. Half-plane concepts

---
