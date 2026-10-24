# 2. 2D Fenwick Tree

> **Section:** §01 Fenwick Tree (Binary Indexed Tree)  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** 1D Fenwick, coordinate compression, offline thinking  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: 1D Fenwick, coordinate compression, offline thinking

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

A Fenwick tree (Binary Indexed Tree) is a compact, cache-friendly data structure that maintains prefix sums of an array of $N$ numbers in $\mathcal{O}(N)$ space and supports $\mathcal{O}(\log N)$ point updates and prefix sum queries.

### Fundamental Theorems & Invariants

- **Lowest Set Bit Decomposition:** For any index $i \ge 1$, $\text{LSB}(i) = i \& (-i)$. The interval managed by index $i$ in a 1-indexed BIT is $(i - \text{LSB}(i), i]$.
- **Prefix Sum Invariant:** The prefix sum $S(r) = \sum_{i=1}^r A[i]$ is composed of at most $\lfloor \log_2 r \rfloor + 1$ disjoint canonical binary intervals.
- **Point Update Invariant:** Incrementing $A[i]$ by $v$ propagates strictly to ancestors $i \leftarrow i + \text{LSB}(i)$, visiting at most $\mathcal{O}(\log N)$ nodes.
- **Binary Lifting on BIT (Order Statistics):** Finding the smallest index $r$ such that $\sum_{i=1}^r A[i] \ge k$ can be solved in pure $\mathcal{O}(\log N)$ time without extra binary search factors by jumping power-of-two steps from MSB to LSB.

### Algorithmic Execution Blueprint

1. **Initialization:** Preallocate array `bit` of size $N+1$ initialized to $0$. Build in $\mathcal{O}(N)$ linear time by propagating each index $i$ to its immediate parent $i + (i \& -i)$.
2. **Point Update:** To add $v$ at index $i$: while $i \le N$, execute `bit[i] += v` and `i += i & -i`.
3. **Prefix Query:** To query $\sum_{j=1}^i A[j]$: initialize $S = 0$; while $i > 0$, execute `S += bit[i]` and `i -= i & -i`.
4. **Range Update & Range Sum:** Maintain two Fenwick trees $B_1$ and $B_2$. Adding $v$ to $[L, R]$ updates $B_1$ with $+v$ at $L$, $-v$ at $R+1$, and updates $B_2$ with $+v \cdot (L-1)$ at $L$, $-v \cdot R$ at $R+1$. The prefix sum at $r$ equals $r \cdot B_1(r) - B_2(r)$.

### Closed-Form Invariant Equations

$$\sum_{i=1}^r A[i] = (r+1)\sum_{j=1}^r d_j - \sum_{j=1}^r j \cdot d_j = (r+1)B_1(r) - B_2(r)$$

### Structural Edge Cases & Assumptions

- Fenwick trees MUST be 1-indexed. Passing index $0$ into $i \& -i$ causes an infinite loop ($0 \& -0 = 0$).
- Coordinate compression is required when coordinates exceed $10^7$ or are negative.
- Prefix sums on frequencies can exceed standard 32-bit integers; always use 64-bit `long long` for accumulators.

---

## 3. Core Intuition & Problem Framing

Nest Fenwicks: outer index walks rows with `i & -i`, inner walks columns. Point \((x,y)\) contributes to \(O(\log X\log Y)\) nodes; rectangle prefix is inclusion-exclusion of four prefixes. True online 2D segtrees are heavier; 2D BIT + compression is the contest default for “point updates + rectangle sums.”

---

## 4. Proof Sketches & Recurrences

\[
\mathrm{pref}(X,Y)=\sum_{x\le X}\sum_{y\le Y} a_{x,y}
\]
Rectangle \([x_1,x_2]\times[y_1,y_2]\):
\[
\mathrm{pref}(x_2,y_2)-\mathrm{pref}(x_1-1,y_2)-\mathrm{pref}(x_2,y_1-1)+\mathrm{pref}(x_1-1,y_1-1).
\]
Each update/query: \(O(\log X\log Y)\). Memory \(O(XY)\) dense, or sparse maps / offline dynamic — for contests usually compress to \(\le n\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) empty / \(O(n\log^2)\) for \(n\) points
- Per-query / per-operation: \(O(\log X\log Y)\)
- Total: \(O(q\log^2 n)\) after compression to \(n\)
- Memory: \(O(XY)\) dense; often \(O(n^2)\) worst after compression if careless — compress both axes to ranks \(\le n\)`

### C++17 Template

```cpp
namespace fenwick2d {
using ll = long long;

struct BIT2D {
    int n, m;
    vector<vector<ll>> bit;
    BIT2D(int n, int m) : n(n), m(m), bit(n + 1, vector<ll>(m + 1, 0)) {}
    void add(int x, int y, ll v) { // 1-indexed
        for (int i = x; i <= n; i += i & -i)
            for (int j = y; j <= m; j += j & -j)
                bit[i][j] += v;
    }
    ll sumPrefix(int x, int y) const {
        ll s = 0;
        for (int i = x; i > 0; i -= i & -i)
            for (int j = y; j > 0; j -= j & -j)
                s += bit[i][j];
        return s;
    }
    ll sumRect(int x1, int y1, int x2, int y2) const {
        if (x1 > x2 || y1 > y2) return 0;
        return sumPrefix(x2, y2) - sumPrefix(x1 - 1, y2)
             - sumPrefix(x2, y1 - 1) + sumPrefix(x1 - 1, y1 - 1);
    }
};
} // namespace fenwick2d
```

### Python 3 Template

```python
class BIT2D:
    def __init__(self, n: int, m: int):
        self.n, self.m = n, m
        self.bit = [[0] * (m + 1) for _ in range(n + 1)]
    def add(self, x: int, y: int, v: int) -> None:
        i = x
        while i <= self.n:
            j = y
            while j <= self.m:
                self.bit[i][j] += v
                j += j & -j
            i += i & -i
    def sum_prefix(self, x: int, y: int) -> int:
        s, i = 0, x
        while i > 0:
            j = y
            while j > 0:
                s += self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return s
```

---

## 6. Recognition Trigger Signals & Heuristics

- Points in a plane; rectangle sum / count queries
- “Add value at (x,y); query sum in \([x1,x2]\times[y1,y2]\)”
- Offline 2D counting after compressing coordinates
- Prefer this over naive 2D segtree when only sum/count + points matter

---

## 7. Contest WA / TLE / RE Traps

- Forgetting four-term inclusion-exclusion
- Using raw coordinates without compression → MLE/RE
- Updating only one copy when points are “set” not “add” (subtract old value first)
- Mixing 0/1-index on x and y independently

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1311F | Moving Points | 2000 | Fenwick, Line Sweep, Coordinate Compression | Sort by velocity, sweep with 2 Fenwicks for count and coordinate prefix sums. | [Solve Problem](https://codeforces.com/contest/1311/problem/F) |
| Codeforces | CF-1073D | Berland Fair | 1800 | Fenwick, Binary Search | Fenwick tree tracking active stalls and sum of costs for fast cycle simulation. | [Solve Problem](https://codeforces.com/contest/1073/problem/D) |
| Codeforces | CF-1208D | Restore Permutation | 1900 | Fenwick, Binary Lifting, Greedy | Reverse reconstruction using Fenwick binary lifting in O(log N). | [Solve Problem](https://codeforces.com/contest/1208/problem/D) |
| CSES | CSES-1648 | Dynamic Range Sum Queries | 1400 | Fenwick, Range Queries | Standard Fenwick tree 1-based prefix sums and point updates. | [Solve Problem](https://cses.fi/problemset/task/1648) |
| Codeforces | CF-1404C | Fixed Point Removal | 2300 | Fenwick, Binary Lifting, Offline Sweep | Offline query sweep with Fenwick binary lifting to find maximum active prefix. | [Solve Problem](https://codeforces.com/contest/1404/problem/C) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fenwick Tree (Binary Indexed Tree)](https://cp-algorithms.com/data_structures/fenwick.html)
- **[USACO Guide]** [USACO Guide: Point Update Range Sum (Fenwick)](https://usaco.guide/gold/purq)
- **[YouKn0wWho]** [YouKn0wWho Academy: Fenwick Tree Mastery](https://youkn0wwho.academy/topic-list#fenwick-tree)
- **[Codeforces]** [Codeforces Blog: Binary Lifting on Fenwick Tree](https://codeforces.com/blog/entry/61364)

---

## 10. Algorithmic Variants & Advanced Extensions

- Count-only (store 1 per point)
- Offline: process by x-sweep + 1D Fenwick on y (often faster / less memory than full 2D)
- Range add rectangle + point query: 2D difference + 2D BIT
- Dynamic sparse: `map` / segment tree of Fenwicks (heavier)

---

## 11. Typical Problem Archetypes

1. Standard application: point add, rectangle sum
2. Slightly disguised: number of points in rectangles offline
3. Difficult: rectangle add + rectangle sum (need more structure / segtree beats-style or lazy 2D — rare)
4. Very difficult / advanced: CDQ divide-conquer replacing 2D/3D structures

---

## 12. Recognition & Identification Drills

1. \(n\) weighted points; \(q\) axis-aligned rectangle sum queries (offline OK).
2. Grid \(n\times m\) (\(n,m\le 1000\)); point updates and sub-rectangle sums.
3. Count inversions in 2D: pairs \(i<j\), \(x_i<x_j\), \(y_i>y_j\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: 2D point updates + rectangle prefix sums/counts
- Key invariant: nested BIT covers
- Key formula: 4-prefix inclusion-exclusion
- Complexity: \(O(\log^2 n)\) per op after compression
- Template to remember: double `i += i & -i` loops + compress coords

---

## 3. Sparse table

---
