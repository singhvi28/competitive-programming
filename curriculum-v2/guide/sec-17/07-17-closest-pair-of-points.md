# 7. Closest Pair of Points

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Sorting, divide-and-conquer or sweep + set  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Sorting, divide-and-conquer or sweep + set

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

Brute O(n²) dies at n~1e5. Divide-and-conquer: sort by x, recurse left/right, then only points within δ of the midline can beat δ, and in the strip each point only needs to check a constant number of neighbors by y (classic ≤ 7). Sweep-line variant: maintain points in a y-ordered set within a δ-width window.

---

## 4. Proof Sketches & Recurrences

Let δ = min(δL, δR). Strip width 2δ. Claim: for a point, candidates in the strip sorted by y lie in a δ×2δ box packing argument ⇒ O(1) checks each ⇒ strip O(n), total T(n)=2T(n/2)+O(n)=O(n log n).

Use squared distances until the end.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort O(n log n)
- Per-query / per-operation: —
- Total: O(n log n)
- Memory: O(n)`

### C++17 Template

```cpp
namespace geo {
ll closestPair2(vector<Pt> a) {
    int n = (int)a.size();
    if (n < 2) return 0;
    sort(a.begin(), a.end()); // by x, then y
    const ll INF = 4e18;
    vector<Pt> t(n);
    function<ll(int,int)> rec = [&](int l, int r) -> ll {
        if (r - l <= 3) {
            ll d = INF;
            for (int i = l; i < r; i++)
                for (int j = i + 1; j < r; j++)
                    d = min(d, dist2(a[i], a[j]));
            sort(a.begin() + l, a.begin() + r, [](Pt p, Pt q){ return p.y < q.y; });
            return d;
        }
        int m = (l + r) / 2;
        ll midx = a[m].x;
        ll d = min(rec(l, m), rec(m, r));
        merge(a.begin() + l, a.begin() + m, a.begin() + m, a.begin() + r, t.begin(),
              [](Pt p, Pt q){ return p.y < q.y; });
        copy(t.begin(), t.begin() + (r - l), a.begin() + l);
        vector<Pt> strip;
        strip.reserve(r - l);
        for (int i = l; i < r; i++) {
            ll dx = a[i].x - midx;
            if (dx * dx < d) strip.push_back(a[i]);
        }
        for (int i = 0; i < (int)strip.size(); i++) {
            for (int j = i + 1; j < (int)strip.size(); j++) {
                ll dy = strip[j].y - strip[i].y;
                if (dy * dy >= d) break;
                d = min(d, dist2(strip[i], strip[j]));
            }
        }
        return d;
    };
    return rec(0, n);
}
} // namespace geo
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Minimum distance between any two points”
- Collision / nearest neighbor among static points
- Geometry + “must be O(n log n)”

---

## 7. Contest WA / TLE / RE Traps

- Comparing with `sqrt` and EPS: two close distances may mis-order — keep `dist2` in `ll` / `__int128` if needed.
- Overflow: dx*dx with dx~2e9 needs `__int128` or careful `ll` (2e9²=4e18 fits signed 64).
- Forgetting to merge by y (or resort strip) → strip checks wrong / TLE.
- Duplicate points ⇒ distance 0 — handle if problem forbids.
- Strip condition using `|x-midx| < δ` with float δ after sqrt — prefer `dx*dx < d` with d = δ².

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

- Sweep + `std::set` by y: O(n log n), often shorter to code for some.
- Closest pair among two sets (bichromatic) — harder.
- Approximate closest pair — rare in CP.

---

## 11. Typical Problem Archetypes

1. Standard application: print minimum distance.
2. Slightly disguised: “any two cities closer than D?” — early exit when d < D².
3. Difficult: closest pair with Manhattan distance (rotate 45°).
4. Very difficult / advanced: dynamic closest pair.

---

## 12. Recognition & Identification Drills

1. Implement D&C; match brute on n=2e3 random.
2. Force duplicate points and coords at ±1e9.
3. Rewrite strip with `dx*dx < d` only (no sqrt).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: min distance, n large
- Key invariant: strip + O(1) y-neighbors
- Key formula: δ² comparisons
- Complexity: O(n log n)
- Template to remember: recurse + merge by y + strip

---

## 8. Sweep line

---
