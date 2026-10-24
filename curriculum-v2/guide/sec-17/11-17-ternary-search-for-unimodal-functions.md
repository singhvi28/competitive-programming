# Ternary Search for Unimodal Functions

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2100 | **Frequency:** Occasional  
> **Prerequisites:** Binary search  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1400–2100
- Prerequisites: Binary search

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

While Binary Search is for monotonic functions, **Ternary Search** is for unimodal functions (functions that strictly increase then decrease, or strictly decrease then increase). We pick two midpoints $m_1 = L + (R-L)/3$ and $m_2 = R - (R-L)/3$. By comparing $f(m_1)$ and $f(m_2)$, we can discard one third of the search space.

---

## 4. Proof Sketches & Recurrences

```cpp
// Continuous Ternary Search (Finding Minimum of convex function)
double ternary_search_continuous(double L, double R) {
    for (int iter = 0; iter < 100; ++iter) { // 100 iterations is enough for double
        double m1 = L + (R - L) / 3.0;
        double m2 = R - (R - L) / 3.0;
        if (f(m1) < f(m2)) { 
            R = m2;
        } else {
            L = m1;
        }
    }
    return f(L);
}

// Discrete Ternary Search (Finding Minimum of convex sequence)
long long ternary_search_discrete(long long L, long long R) {
    while (R - L > 2) {
        long long m1 = L + (R - L) / 3;
        long long m2 = R - (R - L) / 3;
        if (f(m1) < f(m2)) R = m2;
        else L = m1;
    }
    long long ans = f(L);
    for(long long i = L + 1; i <= R; ++i) ans = min(ans, f(i));
    return ans;
}
```

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Continuous Ternary Search (Finding Minimum of convex function)
double ternary_search_continuous(double L, double R) {
    for (int iter = 0; iter < 100; ++iter) { // 100 iterations is enough for double
        double m1 = L + (R - L) / 3.0;
        double m2 = R - (R - L) / 3.0;
        if (f(m1) < f(m2)) { 
            R = m2;
        } else {
            L = m1;
        }
    }
    return f(L);
}

// Discrete Ternary Search (Finding Minimum of convex sequence)
long long ternary_search_discrete(long long L, long long R) {
    while (R - L > 2) {
        long long m1 = L + (R - L) / 3;
        long long m2 = R - (R - L) / 3;
        if (f(m1) < f(m2)) R = m2;
        else L = m1;
    }
    long long ans = f(L);
    for(long long i = L + 1; i <= R; ++i) ans = min(ans, f(i));
    return ans;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Finding the minimum time to reach a point when speed varies.
- Finding the optimal angle to shoot a projectile.
- Minimizing a cost function that forms a parabola.

---

## 7. Contest WA / TLE / RE Traps

- Flat plateaus: if $f(x)$ is constant on an interval ($f(m_1) == f(m_2)$), ternary search cannot determine which side holds the optimum. Strict unimodality is required.
- Integer mid calculation: integer division `(r - l) / 3` can produce $m_1 = m_2$ when $r - l \le 2$, leading to infinite loops; always stop discrete search at $r - l \le 3$ and brute force the rest.
- Maximizing vs minimizing: flipping inequality `<` vs `>` flips search direction.
- Too few iterations: using `r - l > 1e-9` as loop condition can loop forever due to floating point precision limits; use a fixed loop `for (int iter = 0; iter < 100; ++iter)` instead.

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
