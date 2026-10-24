# Mapping Sparse $10^9$ Domains to Dense $[0, K-1]$ Ranks

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2000
- Prerequisites: Coordinate Compression, Sorting, Unique, Binary Search (`std::lower_bound`)
- Tradeoff: Compresses arbitrary $10^9$ coordinate domains into compact $[0, K-1]$ ranks with $K \le 2N$ to fit in array-based trees.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

## 3. Core Intuition & Problem Framing

Tree data structures like Fenwick Trees and basic Segment Trees require memory proportional to the coordinate domain size $M$. When problem coordinates lie in $[-10^9, 10^9]$, allocating a size $10^9$ array is impossible (MLE). Coordinate compression sorts all distinct coordinates appearing in inputs and queries, removes duplicates, and replaces each large coordinate with its 0-based or 1-based index rank via `std::lower_bound`. The relative order of all coordinates is preserved, while the domain size collapses from $10^9$ to at most $2N$!

---

## 4. Proof Sketches & Recurrences

Given $N$ query/event points $x_1, x_2, \dots, x_N \in \mathbb{R}$. Sorting and deduplicating produces unique array $U$ of size $K \le N$ in $\mathcal{O}(N \log N)$. For any $x_i$, its compressed rank is $rank(x_i) = \text{lower\_bound}(U, x_i) - U.\text{begin}()$. Order is preserved: $x_a < x_b \iff rank(x_a) < rank(x_b)$. For interval problems where intervals have length, remember to also compress $R_i + 1$ or track endpoint spans $U[i+1] - U[i]$ to preserve continuous measure.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Coordinate Compression Utility
#include <bits/stdc++.h>
using namespace std;

struct CoordinateCompressor {
    vector<long long> coords;
    
    void add(long long x) { coords.push_back(x); }
    
    void build() {
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());
    }
    
    int get_rank(long long x) const {
        return lower_bound(coords.begin(), coords.end(), x) - coords.begin();
    }
    
    long long get_val(int rank) const {
        return coords[rank];
    }
    
    int size() const { return coords.size(); }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Coordinates or values up to $10^9$ or $10^{18}$ where only relative comparisons matter.
- Range queries on offline data with sparse coordinate points.
- Fenwick tree or Segment tree indexing over large continuous domains.
- Interval sweep line where endpoints are floating point numbers or large integers.

---

## 7. Contest WA / TLE / RE Traps

- Calling `get_rank()` before calling `build()` (sorting and deduplicating), returning nonsensical ranks.
- Forgetting to add query endpoints into the compression vector: if queries test coordinates not in `vals`, `get_rank` might return inconsistent or out-of-bounds positions.
- Interval length corruption: mapping $[1, 2]$ and $[2, 100]$ to contiguous ranks $[0, 1]$ and $[1, 2]$ loses the physical length of intervals unless span weights $U[i+1] - U[i]$ are explicitly maintained.
- Off-by-one indexing: 0-based compressed ranks passed to 1-based Fenwick trees without `+ 1`.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

## 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---
