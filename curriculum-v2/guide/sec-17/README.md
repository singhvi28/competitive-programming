# Section §17: Computational Geometry & Polygons

> **Module ID:** `sec-17`  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Topic Count:** 17  

**Module Summary:** Vector cross/dot products, Orientation tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-polygon, Half-plane intersection, and Circle geometry.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Orientation / Cross Product](#topic-1) | `A-tier` | 1600–2200 | Occasional (but foundational whenever geometry appears) | [01-17-orientation-cross-product.md](./01-17-orientation-cross-product.md) |
| 2 | [Line Intersection](#topic-2) | `B-tier` | 1800–2400 | Occasional | [02-17-line-intersection.md](./02-17-line-intersection.md) |
| 3 | [Segment Intersection](#topic-3) | `B-tier` | 1800–2400 | Occasional | [03-17-segment-intersection.md](./03-17-segment-intersection.md) |
| 4 | [Point-in-Polygon](#topic-4) | `B-tier` | 1800–2400 | Occasional | [04-17-point-in-polygon.md](./04-17-point-in-polygon.md) |
| 5 | [Convex Hull (Andrew Monotone Chain)](#topic-5) | `A-tier` | 1800–2400 | Occasional | [05-17-convex-hull-andrew-monotone-chain.md](./05-17-convex-hull-andrew-monotone-chain.md) |
| 6 | [Rotating Calipers](#topic-6) | `B-tier` | 2000–2600 | Occasional | [06-17-rotating-calipers.md](./06-17-rotating-calipers.md) |
| 7 | [Closest Pair of Points](#topic-7) | `B-tier` | 1900–2500 | Occasional | [07-17-closest-pair-of-points.md](./07-17-closest-pair-of-points.md) |
| 8 | [Sweep Line](#topic-8) | `A-tier` | 2000–2700 | Occasional | [08-17-sweep-line.md](./08-17-sweep-line.md) |
| 9 | [Half-Plane Intersection (Concepts)](#topic-9) | `C-tier / Niche (rarely worth early)` | 2400–3000 | Rare | [09-17-half-plane-intersection-concepts.md](./09-17-half-plane-intersection-concepts.md) |
| 10 | [Circle Geometry Basics](#topic-10) | `B-tier` | 1800–2500 | Occasional | [10-17-circle-geometry-basics.md](./10-17-circle-geometry-basics.md) |
| 11 | [Ternary Search for Unimodal Functions](#topic-11) | `A-tier` | 1400–2100 | Occasional | [11-17-ternary-search-for-unimodal-functions.md](./11-17-ternary-search-for-unimodal-functions.md) |
| 12 | [Integer cross vs floats](#topic-12) | `B-tier` | 1600–2200 | Common | [12-17-integer-cross-vs-floats.md](./12-17-integer-cross-vs-floats.md) |
| 13 | [Ray casting vs winding (point-in-polygon)](#topic-13) | `B-tier` | 1600–2200 | Common | [13-17-ray-casting-vs-winding-point-in-polygon.md](./13-17-ray-casting-vs-winding-point-in-polygon.md) |
| 14 | [Rotating calipers vs N²](#topic-14) | `B-tier` | 1600–2200 | Common | [14-17-rotating-calipers-vs-n.md](./14-17-rotating-calipers-vs-n.md) |
| 15 | [High-ROI (learn early in this section)](#topic-15) | `B-tier` | 1600–2200 | Common | [15-17-high-roi-learn-early-in-this-section.md](./15-17-high-roi-learn-early-in-this-section.md) |
| 16 | [Situational (learn when recognition hits)](#topic-16) | `B-tier` | 1600–2200 | Common | [16-17-situational-learn-when-recognition-hits.md](./16-17-situational-learn-when-recognition-hits.md) |
| 17 | [Rarely worth early / Niche](#topic-17) | `B-tier` | 1600–2200 | Common | [17-17-rarely-worth-early-niche.md](./17-17-rarely-worth-early-niche.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Orientation / Cross Product

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Occasional (but foundational whenever geometry appears)  
> **Prerequisites:** Vectors, 2D coordinates  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional (but foundational whenever geometry appears)
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Vectors, 2D coordinates

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

The 2D cross product \(a_x b_y - a_y b_x\) is the signed parallelogram area. Sign tells orientation: positive = CCW turn from \(\vec{a}\) to \(\vec{b}\) (under standard math coords with y up — same formula works in screen coords; only “which sign is left” flips with axis conventions, not the algebra). Almost every geometry predicate collapses to “sign of one cross.”

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: O(1)
- Total: O(1) per predicate
- Memory: O(1)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Is C left/right of directed line AB?”
- “Collinear / turn direction for hull”
- “Do three points form a left turn?” (Andrew / Graham)
- Polar angle sorting around a point (via cross, not `atan2` when possible)

---

#### 7. Contest WA / TLE / RE Traps

- **`long long` overflow:** on cross when coords are 1e9 — silent WA. Use `__int128`.
- Mixing `atan2` sort with cross predicates → inconsistent order near axes.
- Assuming “left = positive” without matching the problem’s coordinate system (rarely an issue if you stay consistent).
- Using `== 0` with floats for collinearity — never for integer geometry.
- Forgetting collinear points are “on line” but may be outside the segment.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Dot product:** acute/obtuse angles, projection length squared.
- **Squared distances:** avoid `sqrt` until output.
- **3-point area / polygon shoelace:** sum of crosses.

---

#### 11. Typical Problem Archetypes

1. Standard application: count left turns along a path.
2. Slightly disguised: “can the robot turn without crossing?” → orientation.
3. Difficult: polar sort + unique rays for angular sweep.
4. Very difficult / advanced: exact predicates for higher geometry (still built on cross).

---

#### 12. Recognition & Identification Drills

1. Given directed line AB and point C, output LEFT / RIGHT / ON.
2. Sort points by angle around the lowest point; break ties by distance.
3. Detect whether polyline is strictly convex (all turns same sign, no collinear).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any turn / side / collinearity test
- Key invariant: sign(cross) is orientation
- Key formula: \((B-A)\times(C-A)\)
- Complexity: O(1)
- Template to remember: `orient(o,a,b)` + `__int128` cross

---

## 2. Line intersection

---


---

<a id="topic-2"></a>
### 2. Line Intersection

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation / cross, vector algebra  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation / cross, vector algebra

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Two lines in 2D either intersect in one point, are parallel (no meet), or coincide. Parametric form \(P + t\,D\) turns intersection into solving a 2×2 linear system; the determinant is a cross product of directions. For predicates (do they meet?), stay integer; for the actual point, you usually need rationals or `long double`.

---

#### 4. Proof Sketches & Recurrences

Line 1: \(P + t\,R\), line 2: \(Q + u\,S\).
\[
P + t R = Q + u S \implies t(R\times S)=(Q-P)\times S.
\]
If \(R\times S = 0\): parallel (and coincident if \((Q-P)\times R = 0\)).
Else \(t = ((Q-P)\times S)/(R\times S)\), point \(P + t R\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1)
- Total: O(1)
- Memory: O(1)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Intersection of two infinite lines”
- Constructing a point defined as line∩line then continuing geometry
- Checking parallel / coincident before dividing

---

#### 7. Contest WA / TLE / RE Traps

- Dividing by cross ≈ 0 with floats → huge wrong point (EPS: treat \|cross\| < EPS as parallel).
- Returning an intersection for **coincident** lines as if unique.
- Using `float` instead of `long double`.
- Direction vectors (0,0) — degenerate line.
- Integer overflow before cast to long double.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Segment vs line: check t∈[0,1] or u∈[0,1] after solve.
- Perpendicular through point: rotate direction (dx,dy)→(-dy,dx).
- Intersection of many lines: usually pairwise or dualize to half-planes.

---

#### 11. Typical Problem Archetypes

1. Standard application: find intersection coordinate, print with precision.
2. Slightly disguised: reflection — intersect with mirror line.
3. Difficult: arrangement of lines counting cells (sweep / incremental).
4. Very difficult / advanced: exact predicates + constructed points in cascade (precision death).

---

#### 12. Recognition & Identification Drills

1. Given two lines as point+direction, classify parallel / coincident / intersect and output point.
2. Find intersection of diagonals of a convex quadrilateral (lines, not segments).
3. Count distinct intersection points among n lines (n ≤ 1e3).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: infinite lines, constructed points
- Key invariant: unique iff direction cross ≠ 0
- Key formula: \(t=((Q-P)\times S)/(R\times S)\)
- Complexity: O(1)
- Template to remember: parametric solve + parallel check

---

## 3. Segment intersection

---


---

<a id="topic-3"></a>
### 3. Segment Intersection

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, on-segment  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, on-segment

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Proper intersection: endpoints of each segment are on opposite sides of the other. Improper: share an endpoint or overlap collinearly. The classic 4-orientation test handles general position; collinear overlap needs interval overlap on the line.

---

#### 4. Proof Sketches & Recurrences

Segments AB, CD. Let
\[
o1=\mathrm{orient}(A,B,C),\; o2=\mathrm{orient}(A,B,D),\;
o3=\mathrm{orient}(C,D,A),\; o4=\mathrm{orient}(C,D,B).
\]
Proper: \(o1\neq o2\) and \(o3\neq o4\) with all nonzero.
General (including touch): also true if a point lies on the other segment when some orient is 0.
Collinear overlap: all oriients 0 and projections overlap on x (and y).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1)
- Total: O(1) pairwise; O(n²) all pairs
- Memory: O(1)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Do these two sticks cross?”
- Map / planar graph edges
- Geometry + graph: segments as obstacles
- Prelude to sweep-line segment intersection

---

#### 7. Contest WA / TLE / RE Traps

- **Collinear overlap:** forgotten → WA on “touching sticks.”
- Endpoint touch: problem says “intersect” vs “strictly cross” — read statement.
- Zero-length segments (a==b): `onSegment` still works if careful.
- Using float EPS for orientation on integer inputs.
- Overflow in cross.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Closed vs open segments (exclude endpoints).
- Count intersections among n segments → sweep (§8) if n large.
- Intersection point uniqueness vs segment overlap (continuum).

---

#### 11. Typical Problem Archetypes

1. Standard application: yes/no two segments intersect.
2. Slightly disguised: edges of polygons intersect ⇒ not simple.
3. Difficult: build intersection graph of segments.
4. Very difficult / advanced: Bentley–Ottmann reporting all k intersections.

---

#### 12. Recognition & Identification Drills

1. Handle collinear overlapping segments correctly for YES/NO.
2. Detect if a polygon is simple (no two non-adjacent edges intersect).
3. Given n≤2e3 segments, count intersecting pairs.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: pairwise segment tests, n small or inner check in sweep
- Key invariant: opposite orientations ⇒ cross
- Key formula: four `orient` + collinear `onSegment`
- Complexity: O(1)
- Template to remember: `segmentsIntersect` including collinear cases

---

## 4. Point-in-polygon

---


---

<a id="topic-4"></a>
### 4. Point-in-Polygon

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, on-segment, ray or winding idea  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, on-segment, ray or winding idea

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

**Ray casting:** shoot a ray to +∞; odd crossings ⇒ inside (for simple polygons). Vertices and edges parallel to the ray are landmines — use a careful crossing rule (e.g., count only edges straddling the ray with an upward/downward convention).

**Winding number:** sum signed crossings / angle; nonzero ⇒ inside for closed curves. Cleaner with orientation; still need an explicit boundary test.

Always decide **BOUNDARY** as a third answer when problems ask IN/ON/OUT.

---

#### 4. Proof Sketches & Recurrences

Ray casting (half-open edge rule): for edge (xi,yi)–(xj,yj), count a crossing if the edge straddles y = py and the x-intersect is strictly to the right of px, using a consistent endpoint rule so vertices are not double-counted:
\[
\text{cross if } (y_i > p_y) \neq (y_j > p_y) \text{ and } p_x < \text{xinterp}.
\]
Winding (integer version via crosses): for each edge, add +1/−1 when a ray crosses upward/downward.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (or O(n) store)
- Per-query / per-operation: O(n) general; O(log n) convex
- Total: O(n) / O(q log n) convex
- Memory: O(n)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Is the point inside the fence?”
- Lattice points in polygon (combine with Pick — separate)
- Geofencing / regions on plane

---

#### 7. Contest WA / TLE / RE Traps

- **Vertex grazing:** double-count or miss — use strict half-open y-rule.
- Horizontal edges: must not break parity; winding rule above handles via y-straddle.
- Forgetting ON-boundary as separate case.
- Assuming CCW input when using signed area tests inconsistently.
- Ray casting with floats through a vertex → classic WA.
- Self-intersecting polygons: “inside” ill-defined; winding still defined.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Multiple queries static polygon: preprocess trapezoids / triangulation (rare in CF).
- Polygon with holes: winding per ring or even-odd per component.
- Lattice-only: still geometry, or Pick’s theorem for area/counts.

---

#### 11. Typical Problem Archetypes

1. Standard application: IN/ON/OUT for one polygon.
2. Slightly disguised: points strictly inside convex hull.
3. Difficult: many queries + large polygon → O(log n) convex or offline.
4. Very difficult / advanced: point location in planar subdivision.

---

#### 12. Recognition & Identification Drills

1. Classify points for a non-convex simple polygon including edge cases on vertices.
2. Implement O(log n) for convex CCW polygon; stress vs O(n).
3. Decide even-odd vs nonzero winding for a self-touching ring.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: membership tests; prefer winding + onSegment
- Key invariant: boundary first, then wn ≠ 0
- Key formula: upward/downward cross signs
- Complexity: O(n) or O(log n) convex
- Template to remember: ON check + winding loop

---

## 5. Convex hull

---


---

<a id="topic-5"></a>
### 5. Convex Hull (Andrew Monotone Chain)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Orientation, sorting  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Orientation, sorting

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Sort points by (x, y). Build lower hull left→right keeping only CCW turns; build upper hull right→left similarly. Concatenate. Collinear-on-edge policy is a single comparison change (`<=` vs `<`). Andrew’s chain is the contest default: short, robust, O(n log n).

---

#### 4. Proof Sketches & Recurrences

Lower hull invariant: stack is a CCW chain. When adding p, while last turn is not CCW (or not strictly CCW), pop. Same for upper with the reversed pass. Correctness: after sort, each point is considered once per chain; extreme points remain. Complexity: sort O(n log n) + amortized O(n) pops.

**Strict vs non-strict:**  
- Keep collinear on hull: pop while `orient <= 0` becomes pop while `orient < 0` (depending on CCW convention).  
- Standard “no unnecessary collinear”: while `cross <= 0` pop (for CCW lower hull).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: —
- Total: O(n log n) time
- Memory: O(n)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Smallest convex set containing points”
- Diameter / width of a set (hull first)
- Gift wrapping only if h tiny and you know it
- “Vertices of the fence”

---

#### 7. Contest WA / TLE / RE Traps

- **All collinear:** hull should be 2 endpoints if dropping collinear middles — check `<= 0` pops correctly.
- Duplicates not removed → zero edges / degenerate crosses.
- Off-by-one when concatenating upper/lower (duplicate endpoints).
- CW vs CCW mismatch with later calipers code.
- Using `long long` cross with 1e9 coords → overflow WA.
- Integer points with same x: sort by y matters for stability of lower/upper.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Keep collinear boundary points: use `< 0` instead of `<= 0` in while (for CCW).
- Lower hull only (for CHT geometry dual — related but different section).
- Dynamic hull (set of upper/lower tangents) — harder, rare.
- 3D convex hull — niche.

---

#### 11. Typical Problem Archetypes

1. Standard application: output hull vertices in order.
2. Slightly disguised: minimum perimeter fence / wrapping.
3. Difficult: hull tricks + binary search tangents from external point.
4. Very difficult / advanced: offline dynamic hull, layers of onion peeling.

---

#### 12. Recognition & Identification Drills

1. Build hull; verify all input points have orient ≤ 0 (or ≥ 0) vs each edge.
2. Stress all-collinear and duplicate-heavy inputs.
3. Compute hull area via shoelace; match triangle fan from interior point.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: extreme points, prelude to calipers/diameter
- Key invariant: monotone chain CCW turns
- Key formula: while cross ≤ 0 pop
- Complexity: O(n log n)
- Template to remember: Andrew lower+upper

---

Next: [17-b — Rotating calipers → Circles](17-b-computational-geometry.md)

---


---

<a id="topic-6"></a>
### 6. Rotating Calipers

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Convex hull, orientation / cross, distances  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Convex hull, orientation / cross, distances

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

On a convex polygon, antipodal pairs (supporting parallel lines) march monotonically. After building the hull, diameter (farthest pair), minimum width, maximum distance between parallel supports, and similar metrics are **O(h)** by advancing a pointer — not O(h²). Calipers beat N² when h is large; for n≤2e3 brute on all pairs of the hull (or all points) is acceptable and less buggy.

---

#### 4. Proof Sketches & Recurrences

**Diameter:** for convex polygon, the farthest pair is realized by an antipodal pair (vertices with parallel supporting lines). Start with a point and the farthest in one direction; rotate the caliper: when the next edge’s outward direction “wins” the cross comparison, advance the opposite pointer. Each pointer moves O(h) total ⇒ O(h).

Distance compare with squared distances to avoid `sqrt`. Area/width use absolute cross / edge length.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n log n) hull
- Per-query / per-operation: O(h) calipers
- Total: O(n log n)
- Memory: O(n)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Maximum distance among points” (diameter of set)
- “Minimum width strip covering points”
- “Farthest opposite buildings” on a convex shape
- After hull, need antipodal structure

---

#### 7. Contest WA / TLE / RE Traps

- Running calipers on **non-convex** input — wrong. Hull first.
- Off-by-one when `j` wraps; infinite loop if while condition wrong on parallel edges.
- Comparing distances with `sqrt` + EPS instead of `dist2`.
- Minimum width: dividing by zero on duplicate hull points.
- Using N² on full set when only hull extremes matter (correct but slower); or wrongly assuming diameter endpoints are hull vertices — they are, so hull is required and sufficient.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Maximum distance between two convex polygons (antipodal dual pointers).
- All antipodal pairs enumeration.
- Minimum area / perimeter bounding rectangle with rotating calipers (rotate by edge directions).

---

#### 11. Typical Problem Archetypes

1. Standard application: diameter of n points.
2. Slightly disguised: farthest pair after Manhattan↔rotated coords (still hull+calipers or transform).
3. Difficult: min-width strip covering.
4. Very difficult / advanced: rotating calipers + binary search on geometric predicates.

---

#### 12. Recognition & Identification Drills

1. Diameter via calipers; verify vs O(h²) on random convex polygons.
2. Min width of a convex polygon; check against all edge–vertex distances.
3. Decide calipers vs N² given n=3e3 vs n=1e5.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: convex metrics after hull; n large
- Key invariant: antipodal pointer only advances
- Key formula: advance while next cross larger
- Complexity: O(n log n)
- Template to remember: hull + two-pointer antipodes

---

## 7. Closest pair

---


---

<a id="topic-7"></a>
### 7. Closest Pair of Points

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Sorting, divide-and-conquer or sweep + set  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Sorting, divide-and-conquer or sweep + set

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Brute O(n²) dies at n~1e5. Divide-and-conquer: sort by x, recurse left/right, then only points within δ of the midline can beat δ, and in the strip each point only needs to check a constant number of neighbors by y (classic ≤ 7). Sweep-line variant: maintain points in a y-ordered set within a δ-width window.

---

#### 4. Proof Sketches & Recurrences

Let δ = min(δL, δR). Strip width 2δ. Claim: for a point, candidates in the strip sorted by y lie in a δ×2δ box packing argument ⇒ O(1) checks each ⇒ strip O(n), total T(n)=2T(n/2)+O(n)=O(n log n).

Use squared distances until the end.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort O(n log n)
- Per-query / per-operation: —
- Total: O(n log n)
- Memory: O(n)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Minimum distance between any two points”
- Collision / nearest neighbor among static points
- Geometry + “must be O(n log n)”

---

#### 7. Contest WA / TLE / RE Traps

- Comparing with `sqrt` and EPS: two close distances may mis-order — keep `dist2` in `ll` / `__int128` if needed.
- Overflow: dx*dx with dx~2e9 needs `__int128` or careful `ll` (2e9²=4e18 fits signed 64).
- Forgetting to merge by y (or resort strip) → strip checks wrong / TLE.
- Duplicate points ⇒ distance 0 — handle if problem forbids.
- Strip condition using `|x-midx| < δ` with float δ after sqrt — prefer `dx*dx < d` with d = δ².

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Sweep + `std::set` by y: O(n log n), often shorter to code for some.
- Closest pair among two sets (bichromatic) — harder.
- Approximate closest pair — rare in CP.

---

#### 11. Typical Problem Archetypes

1. Standard application: print minimum distance.
2. Slightly disguised: “any two cities closer than D?” — early exit when d < D².
3. Difficult: closest pair with Manhattan distance (rotate 45°).
4. Very difficult / advanced: dynamic closest pair.

---

#### 12. Recognition & Identification Drills

1. Implement D&C; match brute on n=2e3 random.
2. Force duplicate points and coords at ±1e9.
3. Rewrite strip with `dx*dx < d` only (no sqrt).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: min distance, n large
- Key invariant: strip + O(1) y-neighbors
- Key formula: δ² comparisons
- Complexity: O(n log n)
- Template to remember: recurse + merge by y + strip

---

## 8. Sweep line

---


---

<a id="topic-8"></a>
### 8. Sweep Line

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Sorting events, ordered set / fenwick, segment intersection predicates  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Sorting events, ordered set / fenwick, segment intersection predicates

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Replace a 2D problem with a 1D structure that evolves over “time” (usually x). Critical moments are **events** (start/end of segment, intersection, point query). The active set is ordered by the other coordinate (y). Same pattern appears outside geometry: scheduling, rectangle union, offline 2D counting.

---

#### 4. Proof Sketches & Recurrences

**Rectangle union area (axis-aligned):** vertical sweep; events = left/right edges. Active y-intervals in a segment tree on compressed y; measure covered length × Δx. O(n log n).

**Segment intersection existence:** horizontal sweep; status = segments ordered by y at current x; when inserting, test neighbors for intersect; at intersections swap order (Bentley–Ottmann). Full reporting is heavy; contest often needs only specialized sweeps.

Event order must be total and consistent; ties (same x) need a policy: e.g. process verticals carefully, left endpoints before right, etc.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: coordinate compress O(n log n)
- Per-query / per-operation: O(log n) status updates
- Total: typically O(n log n) or O((n+k) log n)
- Memory: O(n)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Segments on a plane / report intersections”
- Union area of axis-aligned rectangles
- “Closest pair” sweep variant
- Anytime: sort events + maintain ordered active structure

---

#### 7. Contest WA / TLE / RE Traps

- Event tie-breaking** wrong (process remove before add at same x) → empty active set / missed cover. **EPS-heavy when sweep coordinate is float** (intersection x): never trust `==` on floats; use exact predicates or rational x, or snap with disciplined order keys.
- Compressing y incorrectly (off-by-one on half-open `[y1,y2)`).
- Segment tree `cnt` vs `len` pull bugs when partial cover.
- Assuming general position (no overlapping endpoints) when tests have them.
- For geometric segment sweep: recomputing y-order with floats at current x → **neighbor order flips spuriously from EPS** → false intersections / infinite event loops. Prefer integer geometry problems or exact orientation tests between adjacent segments.
- Vertical segments: special-case; they don’t define a unique y(x).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Union perimeter of rectangles.
- Sweep for closest pair.
- Discrete sweep on grid / fenwick instead of segtree.
- Angular sweep around a point (sort by polar angle) — cousin technique.

---

#### 11. Typical Problem Archetypes

1. Standard application: area of union of rectangles.
2. Slightly disguised: count overlapping intervals while scanning x.
3. Difficult: report whether any two open segments intersect (status + neighbors).
4. Very difficult / advanced: full Bentley–Ottmann with numeric robustness.

---

#### 12. Recognition & Identification Drills

1. Union area of n≤1e5 axis-aligned rectangles.
2. Design event order for “add vertical chord, query active count.”
3. Explain why float intersection events are dangerous without exact predicates.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: 2D → events + 1D DS
- Key invariant: active set correct between events
- Key formula: ans += measure × Δx
- Complexity: O(n log n)
- Template to remember: compress + sweep + segtree coverage

---

## 9. Half-plane concepts

---


---

<a id="topic-9"></a>
### 9. Half-Plane Intersection (Concepts)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** C-tier / Niche (rarely worth early) | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** Lines, convex polygons, polar/deque techniques, robust geometry  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier / Niche (rarely worth early)
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Lines, convex polygons, polar/deque techniques, robust geometry

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

A half-plane is “one side of a directed line” (`cross >= 0`). Intersection of half-planes is a convex (possibly unbounded) polygon. Algorithmically: sort lines by angle, maintain a deque of bounding lines, pop from both ends when the new intersection violates the new constraint — similar spirit to convex hull / CHT dual. Implementation is long and EPS-sensitive; **postpone until forced**.

---

#### 4. Proof Sketches & Recurrences

Each constraint: \(a_i x + b_i y + c_i \ge 0\). Normalize direction angle \(\theta=\mathrm{atan2}(b,a)\). Process in angle order; keep deque of lines whose consecutive intersections form the boundary. When inserting line L, while deque size ≥ 2 and intersection of last two not in L’s half-plane, pop back; similarly pop front. Unbounded regions: add large box half-planes if problem asks for a bounded answer, or handle infinite rays carefully.

Complexity O(n log n) from sort + amortized pops.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort O(n log n)
- Per-query / per-operation: —
- Total: O(n log n)
- Memory: O(n)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Feasible region of linear inequalities in 2D
- “Intersection of half-planes / kernel of polygon”
- Convex polygon as ∩ of edge half-planes (inside poly)

---

#### 7. Contest WA / TLE / RE Traps

- **EPS everywhere:** parallel detection, `atan2` ties, intersection division by near-zero cross, “is point outside?” — tiny EPS changes flip emptiness. Prefer problems with integer half-planes / dualize to hull when possible.
- Forgetting bounding box → “correct” unbounded intersection but empty vertex list.
- Duplicate angles: must keep the tighter constraint.
- Numerically unstable intersection of nearly parallel lines → garbage vertices.
- Using this early in practice instead of learning hull/orientation — poor ROI.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Polygon kernel = ∩ half-planes of edges (for convex is itself; for concave may be empty).
- Linear programming in 2D (Seidel / randomized) — related niche.
- Dual: some half-plane problems ↔ convex hull of points.

---

#### 11. Typical Problem Archetypes

1. Standard application: intersect n half-planes, output area.
2. Slightly disguised: feasible (x,y) for inequality system.
3. Difficult: kernel of a polygon.
4. Very difficult / advanced: robust exact arithmetic half-planes.

---

#### 12. Recognition & Identification Drills

1. Represent a convex polygon as intersection of half-planes.
2. Manually intersect 4 half-planes forming a triangle + redundant constraint.
3. Decide: is this problem half-planes or “just convex hull of something”?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: ∩ linear inequalities in 2D; rare
- Key invariant: deque of angularly sorted lines
- Key formula: pop while intersection outside new half-plane
- Complexity: O(n log n)
- Template to remember: sort by angle + deque (niche)

---

## 10. Circle geometry basics

---


---

<a id="topic-10"></a>
### 10. Circle Geometry Basics

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Vectors, quadratic equations, `long double`  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Vectors, quadratic equations, `long double`

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Circles force floats (or careful algebraic rewriting). Core toolkit: circle–circle intersection, circle–line intersection, tangents from a point, power of a point, radical ideas lightly. Prefer solving with squared radii to delay `sqrt`. Treat EPS as part of the algorithm, not an afterthought.

---

#### 4. Proof Sketches & Recurrences

Circle–circle: centers O1,O2, radii r1,r2, d=|O1O2|.
No intersect if d>r1+r2 or d<|r1-r2| (strict with EPS).
Intersect chord is perpendicular to O1O2 at distance
\[
a=\frac{r1^2-r2^2+d^2}{2d}
\]
from O1; half-chord \(h=\sqrt{\max(0,r1^2-a^2)}\).

Line–circle: project center to line, compare distance to r.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: O(1) intersections
- Total: O(1) / O(n) for n circles pairwise locally
- Memory: O(1)`

##### C++17 Template

```cpp
namespace geo {
const long double EPS = 1e-9L;
const long double PI = acosl(-1.0L);

struct Circle { Ptd o; long double r; };

int circleCircleIntersect(Circle a, Circle b, Ptd& p1, Ptd& p2) {
    long double d = sqrtl((a.o.x - b.o.x) * (a.o.x - b.o.x) +
                          (a.o.y - b.o.y) * (a.o.y - b.o.y));
    if (d < EPS) return 0; // coincident centers: 0 or infinitely many — treat as none
    if (d > a.r + b.r + EPS || d < fabsl(a.r - b.r) - EPS) return 0;
    long double aa = (a.r * a.r - b.r * b.r + d * d) / (2.0L * d);
    long double h2 = a.r * a.r - aa * aa;
    if (h2 < -EPS) return 0;
    long double h = sqrtl(max(0.0L, h2));
    Ptd mid = {a.o.x + aa * (b.o.x - a.o.x) / d,
               a.o.y + aa * (b.o.y - a.o.y) / d};
    if (h < EPS) { p1 = mid; return 1; } // tangent
    Ptd dx = {(b.o.y - a.o.y) / d, (a.o.x - b.o.x) / d}; // unit perpendicular
    p1 = {mid.x + h * dx.x, mid.y + h * dx.y};
    p2 = {mid.x - h * dx.x, mid.y - h * dx.y};
    return 2;
}

// line through A,B ; circle c
int lineCircleIntersect(Ptd A, Ptd B, Circle c, Ptd& p1, Ptd& p2) {
    Ptd d = {B.x - A.x, B.y - A.y};
    Ptd f = {A.x - c.o.x, A.y - c.o.y};
    long double aa = d.x * d.x + d.y * d.y;
    long double bb = 2 * (f.x * d.x + f.y * d.y);
    long double cc = f.x * f.x + f.y * f.y - c.r * c.r;
    long double disc = bb * bb - 4 * aa * cc;
    if (disc < -EPS) return 0;
    disc = sqrtl(max(0.0L, disc));
    long double t1 = (-bb - disc) / (2 * aa);
    long double t2 = (-bb + disc) / (2 * aa);
    p1 = {A.x + t1 * d.x, A.y + t1 * d.y};
    if (fabsl(disc) < EPS) return 1;
    p2 = {A.x + t2 * d.x, A.y + t2 * d.y};
    return 2;
}

// length of tangents from point p to circle; -1 if inside
long double tangentLength(Ptd p, Circle c) {
    long double d2 = (p.x - c.o.x) * (p.x - c.o.x) + (p.y - c.o.y) * (p.y - c.o.y);
    long double v = d2 - c.r * c.r;
    if (v < -EPS) return -1;
    return sqrtl(max(0.0L, v));
}
} // namespace geo
```

##### Python 3 Template

```python
import math

def circle_circle_intersect(o1, r1, o2, r2, eps=1e-9):
    x1, y1 = o1
    x2, y2 = o2
    d = math.hypot(x2 - x1, y2 - y1)
    if d > r1 + r2 + eps or d < abs(r1 - r2) - eps or d < eps:
        if abs(d - (r1 + r2)) <= eps or abs(d - abs(r1 - r2)) <= eps:
            pass
        else:
            return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h2 = r1 * r1 - a * a
    if h2 < -eps:
        return []
    h = math.sqrt(max(0.0, h2))
    mx, my = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d
    if h < eps:
        return [(mx, my)]
    rx, ry = -(y2 - y1) * (h / d), (x2 - x1) * (h / d)
    return [(mx + rx, my + ry), (mx - rx, my - ry)]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Intersection of circles / common area”
- Tangents, Apollonius-style (rare)
- Points at equal distance (perpendicular bisector → line, then circle)

---

#### 7. Contest WA / TLE / RE Traps

- **One EPS does not fit all:** `1e-9` vs `1e-12` vs relative EPS; coordinates in 1e6 with radii 1e-3 break absolute EPS.
- Tangent vs disjoint: `d` vs `r1+r2` within EPS — decide inclusive policy matching the statement (“touch counts as intersect”).
- `h2` slightly negative from rounding — clamp with `max(0, h2)`, but if largely negative it’s truly separate.
- Using `float` / `double` when judge diffs need `long double` + `printf` precision (`setprecision(10)` / 15).
- Degenerate line A==B in line–circle.
- Angle formulas with `acos` arguments outside \([-1,1]\) — clamp before `acos`.
- Mixing exact integer predicates with float-constructed centers → inconsistent “point on circle.”
- Circle–circle with **nearly coincident centers** — division by `d` explodes; special-case `d < EPS`.
- Area of intersection (lens): formula uses `acos`; clamp and watch r=0.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Common area of two circles (lens formula).
- Minimum enclosing circle (randomized O(n) expected) — situational.
- Inversion geometry — niche.

---

#### 11. Typical Problem Archetypes

1. Standard application: intersect two circles, output points.
2. Slightly disguised: find points at distance r1 from A and r2 from B.
3. Difficult: tangents + constructions chain with precision.
4. Very difficult / advanced: arrangements of circles, MEC with constraints.

---

#### 12. Recognition & Identification Drills

1. Classify 0/1/2 intersection points for random circle pairs near tangency.
2. Line–circle with tangent line; ensure one point.
3. Power of a point: verify tangent length² = power.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: circles, equal-distance loci
- Key invariant: clamp tiny negative discriminants; special-case d≈0
- Key formula: \(a=(r1^2-r2^2+d^2)/(2d)\), \(h=\sqrt{r1^2-a^2}\)
- Complexity: O(1)
- Template to remember: circle–circle + line–circle + EPS policy

---

## Back to section hub

[Section 17 overview, comparisons, drills](17-computational-geometry.md)

---


---

<a id="topic-11"></a>
### 11. Ternary Search for Unimodal Functions

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2100 | **Frequency:** Occasional  
> **Prerequisites:** Binary search  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1400–2100
- Prerequisites: Binary search

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

While Binary Search is for monotonic functions, **Ternary Search** is for unimodal functions (functions that strictly increase then decrease, or strictly decrease then increase). We pick two midpoints $m_1 = L + (R-L)/3$ and $m_2 = R - (R-L)/3$. By comparing $f(m_1)$ and $f(m_2)$, we can discard one third of the search space.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Finding the minimum time to reach a point when speed varies.
- Finding the optimal angle to shoot a projectile.
- Minimizing a cost function that forms a parabola.

---

#### 7. Contest WA / TLE / RE Traps

- Flat plateaus: if $f(x)$ is constant on an interval ($f(m_1) == f(m_2)$), ternary search cannot determine which side holds the optimum. Strict unimodality is required.
- Integer mid calculation: integer division `(r - l) / 3` can produce $m_1 = m_2$ when $r - l \le 2$, leading to infinite loops; always stop discrete search at $r - l \le 3$ and brute force the rest.
- Maximizing vs minimizing: flipping inequality `<` vs `>` flips search direction.
- Too few iterations: using `r - l > 1e-9` as loop condition can loop forever due to floating point precision limits; use a fixed loop `for (int iter = 0; iter < 100; ++iter)` instead.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-12"></a>
### 12. Integer cross vs floats

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Universal in Computational Geometry
- Typical CF/ICPC rating range: 1400–2500
- Prerequisites: Vector cross product, dot product, orientation tests
- Tradeoff: Floating-point arithmetic suffers from precision breakdown, epsilon tuning nightmares, and `NaN` errors; integer cross products are 100% exact and deterministic.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

In computational geometry, 95% of contest problems can and should be solved using pure 64-bit or 128-bit integer arithmetic. The cross product of vectors $\vec{u} = (x_1, y_1)$ and $\vec{v} = (x_2, y_2)$ is $\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1$. Its sign deterministically tells whether $\vec{v}$ turns counter-clockwise ($> 0$), clockwise ($< 0$), or is collinear ($= 0$) with $\vec{u}$. Never use `atan2`, slope division $y/x$, or `double` trigonometry to check orientation or sorting.

---

#### 4. Proof Sketches & Recurrences

The 2D cross product equals the signed area of the parallelogram formed by $\vec{u}$ and $\vec{v}$. For integer coordinates bounded by $C = 10^9$, the cross product $x_1 y_2 - x_2 y_1$ reaches up to $2 \times 10^{18}$, which fits within signed 64-bit integer `long long`. For products of differences $(x_b - x_a)(y_c - y_a) - (y_b - y_a)(x_c - x_a)$, maximum magnitude is $4 \times 10^{18}$, comfortably within `long long` (or `__int128_t` for intermediate calculations to prevent any overflow).

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// 100% Exact Integer Geometry Point & Orientation Test
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    Point operator-(const Point& o) const { return {x - o.x, y - o.y}; }
    ll cross(const Point& o) const { return x * o.y - y * o.x; }
    ll dot(const Point& o) const { return x * o.x + y * o.y; }
};

// Returns: +1 for CCW (left turn), -1 for CW (right turn), 0 for Collinear
int orient(Point a, Point b, Point c) {
    __int128 val = (__int128)(b.x - a.x) * (c.y - a.y) - (__int128)(b.y - a.y) * (c.x - a.x);
    if (val > 0) return 1;
    if (val < 0) return -1;
    return 0;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Convex Hull construction (Monotone Chain / Graham Scan).
- Checking whether two line segments intersect.
- Testing if a point lies to the left or right of a directed line.
- Sorting points radially around a pivot (half-plane radial sorting without `atan2`).

---

#### 7. Contest WA / TLE / RE Traps

- Using `float` or `double` slopes $m = (y_2 - y_1)/(x_2 - x_1)$, causing division by zero on vertical lines and rounding errors on nearly collinear points.
- 32-bit integer overflow: cross product of coordinates up to $10^5$ exceeds $2^{31} - 1$; always use `long long` or `__int128`.
- Using `acos` or `asin` without clamping argument to $[-1.0, 1.0]$, producing `NaN` due to slight floating point drift.
- Comparing floats with strict `== 0.0` instead of `std::abs(x) < 1e-9` when floats are unavoidable.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-13"></a>
### 13. Ray casting vs winding (point-in-polygon)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Point in Polygon, Ray Casting, Winding Number, Cross Product
- Tradeoff: Ray casting is simple parity counting but has tricky boundary edge cases; winding number is robust against complex/self-intersecting polygons.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

To determine whether a query point $P$ lies inside a polygon: 1) **Ray Casting Algorithm** shoots a horizontal ray from $P$ to $(+\infty, y_P)$ and counts intersections with polygon edges. If the number of crossings is odd, $P$ is inside; if even, $P$ is outside. 2) **Winding Number Algorithm** computes the total number of counter-clockwise revolutions made by the polygon boundaries around $P$. Non-zero winding number $\implies$ inside. Winding number handles self-intersecting polygons and is immune to vertex-grazing ambiguities when implemented with cross product signs.

---

#### 4. Proof Sketches & Recurrences

Jordan Curve Theorem: Any continuous simple closed curve divides the plane into an 'inside' and an 'outside'. A ray starting from infinity (outside) alternates between inside and outside with each boundary crossing. For winding number, edge $(A, B)$ contributes $+1$ to the winding count if it crosses the horizontal ray upwards and $P$ is to the left of the edge, and $-1$ if it crosses downwards and $P$ is to the right.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Robust Point in Polygon via Winding Number (Integer Precision)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point { ll x, y; };
ll cross_product(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Returns: 1 if inside, 0 if outside, -1 if strictly on boundary
int point_in_polygon(Point p, const vector<Point>& poly) {
    int n = poly.size();
    int wn = 0;
    for (int i = 0; i < n; ++i) {
        Point a = poly[i], b = poly[(i + 1) % n];
        // Check if p is on segment ab
        if (cross_product(a, b, p) == 0 &&
            min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
            min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y)) return -1;
        if (a.y <= p.y) {
            if (b.y > p.y && cross_product(a, b, p) > 0) wn++;
        } else {
            if (b.y <= p.y && cross_product(a, b, p) < 0) wn--;
        }
    }
    return wn != 0 ? 1 : 0;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Query asks whether a point lies strictly inside, outside, or on the boundary of an arbitrary polygon.
- Geofencing or territorial containment queries in computational geometry.
- Polygon triangulation or ear clipping preprocessing.
- Testing point containment in non-convex polygons where binary search on angle cannot be used.

---

#### 7. Contest WA / TLE / RE Traps

- Ray passes exactly through a polygon vertex: standard ray casting double-counts or misses the intersection unless half-open vertical intervals $[y_1, y_2)$ are strictly enforced.
- Horizontal polygon edges: ray overlaps collinear horizontal edges; ensure horizontal segments are ignored or explicitly handled.
- Forgetting boundary check: query point lies exactly on an edge or vertex, but the algorithm reports strictly inside or outside.
- Polygon vertices not oriented in consistent order (CCW or CW).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-14"></a>
### 14. Rotating calipers vs N²

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Convex Hull, Antipodal Pairs, Cross Product, Two Pointers
- Tradeoff: Reduces polygon diameter / minimum bounding box from $\mathcal{O}(N^2)$ brute force to $\mathcal{O}(N)$ after $\mathcal{O}(N \log N)$ convex hull.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

To find the maximum distance between any two points in a 2D set of $N$ points (the polygon diameter), checking all pairs takes $\mathcal{O}(N^2)$, which TLEs for $N = 2 \times 10^5$. The two furthest points must both lie on the vertices of the Convex Hull. Furthermore, the distance from an edge $(P_i, P_{i+1})$ to hull vertices is unimodal: as we advance along hull edges, the furthest opposite vertex (antipodal point) advances monotonically in the same direction. Rotating Calipers maintains an antipodal pointer with two pointers, traversing the entire convex hull in $\mathcal{O}(N)$ total steps!

---

#### 4. Proof Sketches & Recurrences

The distance from a point $C$ to the line through $A$ and $B$ is proportional to the triangle area $|(B - A) \times (C - A)|$. Because the polygon is convex, the area function is strictly unimodal. When we advance the base edge from $(P_i, P_{i+1})$ to $(P_{i+1}, P_{i+2})$, the peak of the triangle area also advances counter-clockwise. Thus, the antipodal pointer index $j$ only advances forward and never retreats, wrapping around $N$ vertices in at most $2N$ steps.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Rotating Calipers: Convex Polygon Diameter in O(N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    ll dist_sq(const Point& o) const { return (x - o.x) * (x - o.x) + (y - o.y) * (y - o.y); }
};

ll cross_product(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Returns maximum squared Euclidean distance between any pair of points on convex hull
ll rotating_calipers_diameter(const vector<Point>& hull) {
    int n = hull.size();
    if (n < 2) return 0;
    if (n == 2) return hull[0].dist_sq(hull[1]);
    ll max_dist = 0;
    int j = 1;
    for (int i = 0; i < n; ++i) {
        Point next_i = hull[(i + 1) % n];
        while (cross_product(hull[i], next_i, hull[(j + 1) % n]) >
               cross_product(hull[i], next_i, hull[j])) {
            j = (j + 1) % n;
        }
        max_dist = max({max_dist, hull[i].dist_sq(hull[j]), next_i.dist_sq(hull[j])});
    }
    return max_dist;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Find the maximum Euclidean distance between any two points among $N \le 2 \times 10^5$ points.
- Minimum enclosing bounding box (minimum area or perimeter rectangle enclosing point set).
- Maximum area triangle inscribed in a convex polygon.
- Widest empty corridor between two disjoint convex point sets.

---

#### 7. Contest WA / TLE / RE Traps

- Running Rotating Calipers on raw points without computing the Convex Hull first.
- Handling collinear edges on the convex hull: strictly greater `>` vs `>=` in cross product area comparison.
- Degenerate hull size: $N = 1$ or $N = 2$ causes infinite while loop if modular indexing is not guarded.
- Using floating-point sqrt when the problem asks for squared distance, losing precision on large coordinates.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-15"></a>
### 15. High-ROI (learn early in this section)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: 2D Point struct, 2D cross product, sorting

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Master Andrew's Monotone Chain algorithm for Convex Hull in $\mathcal{O}(N \log N)$ and 2D cross product turn tests (`cross(B-A, C-A)`). These two primitives solve the vast majority of geometric contest problems.

---

#### 4. Proof Sketches & Recurrences

Cross product $(B - A) \times (C - A) = (B_x - A_x)(C_y - A_y) - (B_y - A_y)(C_x - A_x)$. Positive $\implies$ Counter-Clockwise (left turn); negative $\implies$ Clockwise (right turn); zero $\implies$ collinear.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Andrew Monotone Chain Convex Hull in O(N log N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    bool operator<(const Point& o) const { return x < o.x || (x == o.x && y < o.y); }
};

ll cross(Point o, Point a, Point b) {
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

vector<Point> convex_hull(vector<Point>& pts) {
    int n = pts.size(), k = 0;
    if (n <= 2) return pts;
    vector<Point> h(2 * n);
    sort(pts.begin(), pts.end());
    for (int i = 0; i < n; ++i) {
        while (k >= 2 && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    for (int i = n - 2, t = k + 1; i >= 0; --i) {
        while (k >= t && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    h.resize(k - 1);
    return h;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Enclosing a set of points with minimal perimeter or area.
- Sorting points radially around an origin to detect angular intervals.

---

#### 7. Contest WA / TLE / RE Traps

- Collinear points: strictly `< 0` vs `<= 0` pop condition in convex hull depending on whether collinear points on edges must be preserved.
- Floating point inaccuracies; always use 64-bit integer cross products when coordinates are integers.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-16"></a>
### 16. Situational (learn when recognition hits)

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Convex Hull, Two Pointers, Half-Plane Intersection

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Situational Geometry: (1) Rotating Calipers for polygon diameter and minimum bounding box in $\mathcal{O}(N)$, (2) Half-Plane Intersection in $\mathcal{O}(N \log N)$ using sorted polar angles, and (3) Point-in-Convex-Polygon binary search in $\mathcal{O}(\log N)$.

---

#### 4. Proof Sketches & Recurrences

Rotating calipers advances two antipodal pointers around the convex hull based on triangle area maximization using cross products.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Rotating Calipers Polygon Diameter in O(N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
// Advances pointer j around hull while cross product area increases
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Maximum distance between any two points in a 2D cloud.
- Finding the kernel of a polygon or region satisfying a set of linear half-plane constraints.

---

#### 7. Contest WA / TLE / RE Traps

- Antipodal pointer cycle wrap-around off-by-one.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---

<a id="topic-17"></a>
### 17. Rarely worth early / Niche

> **Section:** §17 Computational Geometry & Polygons  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Minkowski Sum, Delaunay Triangulation, 3D Convex Hull

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Computational Geometry implements 2D geometric algorithms with exact integer arithmetic: Vector cross and dot products, Orientation Tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-Polygon, and Half-Plane Intersection.

##### Fundamental Theorems & Invariants

- **Cross Product Orientation Invariant:** For vectors $\vec{u} = B - A$ and $\vec{v} = C - A$, the 2D cross product $\vec{u} \times \vec{v} = u_x v_y - u_y v_x$ is positive for counter-clockwise turns (left), negative for clockwise turns (right), and zero for collinear points.
- **Monotone Chain Convex Hull (Andrew's Algorithm):** Sorting $N$ points by $(x, y)$ coordinates and building lower and upper hulls via cross-product orientation tests runs in strictly $\mathcal{O}(N \log N)$ time.
- **Rotating Calipers Diameter Theorem:** The maximum distance between any pair of points in a set equals the distance between two antipodal vertices on its convex hull, computable in $\mathcal{O}(N)$ linear time using a rotating caliper pointer.

##### Algorithmic Execution Blueprint

1. **Orientation Test:** `orient(A, B, C) = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)`.
2. **Monotone Chain Hull:** Sort points by $x$, then $y$. Build lower hull by popping while `orient(hull[k-2], hull[k-1], p) <= 0`. Repeat in reverse for upper hull.
3. **Point in Convex Polygon:** Binary search for the wedge containing the query point using cross products from the origin vertex in $\mathcal{O}(\log N)$ time.

##### Closed-Form Invariant Equations

$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \cdot \text{SignedArea}(\triangle), \quad \text{Area} = \frac{1}{2}\Big|\sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i)\Big|$$

##### Structural Edge Cases & Assumptions

- Never use floating-point divisions (`double` slope) for line intersection or orientation when coordinates are integer $\le 10^9$; always use 64-bit or 128-bit cross products.
- In Convex Hull, decide strictly whether collinear points on the hull edge should be included (`< 0` vs `<= 0`).
- Check for duplicate points before running rotating calipers to prevent infinite pointer loops.

---

#### 3. Core Intuition & Problem Framing

Niche geometry constructs: Minkowski Sum of convex polygons in $\mathcal{O}(N + M)$ for collision detection and 3D Convex Hull in $\mathcal{O}(N^2)$ or $\mathcal{O}(N \log N)$.

---

#### 4. Proof Sketches & Recurrences

Minkowski Sum $A + B = \{a + b : a \in A, b \in B\}$ is computed by merging the edge vectors of both convex hulls sorted by polar angle.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Minkowski Sum of Convex Polygons
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Shortest distance between two moving convex polygons over time.
- Point location in Voronoi diagrams.

---

#### 7. Contest WA / TLE / RE Traps

- Cyclic ordering of edge vectors during Minkowski merge.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-166B | Polygons | 2000 | Convex Hull, Point in Polygon | Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks. | [Solve Problem](https://codeforces.com/contest/166/problem/B) |
| Codeforces | CF-70D | Professor's task | 2400 | Dynamic Convex Hull, Geometry | Dynamic online convex hull maintenance using std::map for upper and lower envelopes. | [Solve Problem](https://codeforces.com/contest/70/problem/D) |
| CSES | CSES-2195 | Convex Hull | 1700 | Convex Hull, Monotone Chain | Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests. | [Solve Problem](https://cses.fi/problemset/task/2195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: 2D Geometry Primitives & Cross Products](https://cp-algorithms.com/geometry/basic-geometry.html)
- **[CP-Algorithms]** [CP-Algorithms: Convex Hull (Monotone Chain)](https://cp-algorithms.com/geometry/convex-hull.html)
- **[USACO Guide]** [USACO Guide: Computational Geometry](https://usaco.guide/adv/geometry)

---


---
