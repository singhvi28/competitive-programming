# Section §01: Fenwick Tree (Binary Indexed Tree)

> **Module ID:** `sec-01`  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Topic Count:** 2  

**Module Summary:** Prefix invertible operations, binary lifting on BIT in O(log N), 2D Fenwick trees, range adds/range sums, and offline contribution counting.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Fenwick Tree (Binary Indexed Tree)](#topic-1) | `S-tier` | 1400–2000 | Very Common | [01-01-fenwick-tree-binary-indexed-tree.md](./01-01-fenwick-tree-binary-indexed-tree.md) |
| 2 | [2D Fenwick Tree](#topic-2) | `A-tier` | 1800–2400 | Occasional | [02-01-2d-fenwick-tree.md](./02-01-2d-fenwick-tree.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Fenwick Tree (Binary Indexed Tree)

> **Section:** §01 Fenwick Tree (Binary Indexed Tree)  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Very Common  
> **Prerequisites:** Prefix sums, bit tricks (`i & -i`), associative invertible ops (usually `+` / XOR)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Prefix sums, bit tricks (`i & -i`), associative invertible ops (usually `+` / XOR)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Fenwick tree (Binary Indexed Tree) is a compact, cache-friendly data structure that maintains prefix sums of an array of $N$ numbers in $\mathcal{O}(N)$ space and supports $\mathcal{O}(\log N)$ point updates and prefix sum queries.

##### Fundamental Theorems & Invariants

- **Lowest Set Bit Decomposition:** For any index $i \ge 1$, $\text{LSB}(i) = i \& (-i)$. The interval managed by index $i$ in a 1-indexed BIT is $(i - \text{LSB}(i), i]$.
- **Prefix Sum Invariant:** The prefix sum $S(r) = \sum_{i=1}^r A[i]$ is composed of at most $\lfloor \log_2 r \rfloor + 1$ disjoint canonical binary intervals.
- **Point Update Invariant:** Incrementing $A[i]$ by $v$ propagates strictly to ancestors $i \leftarrow i + \text{LSB}(i)$, visiting at most $\mathcal{O}(\log N)$ nodes.
- **Binary Lifting on BIT (Order Statistics):** Finding the smallest index $r$ such that $\sum_{i=1}^r A[i] \ge k$ can be solved in pure $\mathcal{O}(\log N)$ time without extra binary search factors by jumping power-of-two steps from MSB to LSB.

##### Algorithmic Execution Blueprint

1. **Initialization:** Preallocate array `bit` of size $N+1$ initialized to $0$. Build in $\mathcal{O}(N)$ linear time by propagating each index $i$ to its immediate parent $i + (i \& -i)$.
2. **Point Update:** To add $v$ at index $i$: while $i \le N$, execute `bit[i] += v` and `i += i & -i`.
3. **Prefix Query:** To query $\sum_{j=1}^i A[j]$: initialize $S = 0$; while $i > 0$, execute `S += bit[i]` and `i -= i & -i`.
4. **Range Update & Range Sum:** Maintain two Fenwick trees $B_1$ and $B_2$. Adding $v$ to $[L, R]$ updates $B_1$ with $+v$ at $L$, $-v$ at $R+1$, and updates $B_2$ with $+v \cdot (L-1)$ at $L$, $-v \cdot R$ at $R+1$. The prefix sum at $r$ equals $r \cdot B_1(r) - B_2(r)$.

##### Closed-Form Invariant Equations

$$\sum_{i=1}^r A[i] = (r+1)\sum_{j=1}^r d_j - \sum_{j=1}^r j \cdot d_j = (r+1)B_1(r) - B_2(r)$$

##### Structural Edge Cases & Assumptions

- Fenwick trees MUST be 1-indexed. Passing index $0$ into $i \& -i$ causes an infinite loop ($0 \& -0 = 0$).
- Coordinate compression is required when coordinates exceed $10^7$ or are negative.
- Prefix sums on frequencies can exceed standard 32-bit integers; always use 64-bit `long long` for accumulators.

---

#### 3. Core Intuition & Problem Framing

Index `i` stores the sum of a contiguous block ending at `i` whose length is the lowest set bit of `i`. Walking `i += i & -i` climbs to parents for updates; walking `i -= i & -i` folds a prefix for queries. You never store “arbitrary segments” — only a canonical binary partition of prefixes — which is why Fenwick is smaller/faster than a segtree for the ops it supports.

---

#### 4. Proof Sketches & Recurrences

Let \(\ell(i) = i \& -i\). Node `i` covers \((i-\ell(i), i]\).  
Prefix sum \(S(r) = \sum_{i=1}^{r} a_i\) is the sum of \(O(\log r)\) such blocks.  
Range \(S(l..r) = S(r) - S(l-1)\) needs an inverse. Update of \(a_i\) touches \(O(\log n)\) ancestors.  
**Range add, point query:** store differences \(d_i = a_i - a_{i-1}\) in a Fenwick; point \(a_i =\) prefix of \(d\).  
**Range add, range sum:** maintain two Fenwicks for \(\sum d\) and \(\sum i\cdot d\) so  
\[
\sum_{i=1}^{r} a_i = (r+1)B_1(r) - B_2(r)
\]
after range-add on \([l,r]\) updates \(B_1,B_2\) at \(l\) and \(r+1\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) build from array (sequential adds) or \(O(n)\) linear build
- Per-query / per-operation: \(O(\log n)\)
- Total: \(O((n+q)\log n)\) typical
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace fenwick {
using ll = long long;

struct BIT {
    int n;
    vector<ll> bit;
    BIT(int n = 0) : n(n), bit(n + 1, 0) {}
    void add(int i, ll v) { // 1-indexed
        for (; i <= n; i += i & -i) bit[i] += v;
    }
    ll sumPrefix(int i) const {
        ll s = 0;
        for (; i > 0; i -= i & -i) s += bit[i];
        return s;
    }
    ll sumRange(int l, int r) const { // inclusive
        if (l > r) return 0;
        return sumPrefix(r) - sumPrefix(l - 1);
    }
    // smallest idx with sumPrefix(idx) >= k (array as frequencies); n+1 if none
    int lower_bound(ll k) const {
        int idx = 0;
        int pw = 1;
        while ((pw << 1) <= n) pw <<= 1;
        for (int d = pw; d; d >>= 1) {
            int ni = idx + d;
            if (ni <= n && bit[ni] < k) {
                idx = ni;
                k -= bit[ni];
            }
        }
        return idx + 1;
    }
};

// Range add + range sum via two BITs
struct RangeBIT {
    int n;
    BIT b1, b2;
    RangeBIT(int n) : n(n), b1(n), b2(n) {}
    void addRange(int l, int r, ll v) { // 1-indexed inclusive
        auto upd = [&](int i, ll x) {
            if (i < 1 || i > n) return;
            b1.add(i, x);
            b2.add(i, x * i);
        };
        upd(l, v);
        upd(r + 1, -v);
    }
    ll pref(int r) const {
        if (r <= 0) return 0;
        return (r + 1) * b1.sumPrefix(r) - b2.sumPrefix(r);
    }
    ll sumRange(int l, int r) const { return pref(r) - pref(l - 1); }
};
} // namespace fenwick
```

##### Python 3 Template

```python
class BIT:
    __slots__ = ("n", "bit")
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, i: int, v: int) -> None:
        while i <= self.n:
            self.bit[i] += v
            i += i & -i
    def sum_prefix(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s
    def sum_range(self, l: int, r: int) -> int:
        return self.sum_prefix(r) - self.sum_prefix(l - 1)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Point update, prefix/range sum (or XOR)” with \(n,q \le 10^5\)–\(10^6\)
- Frequency array + “how many ≤ x” after coordinate compression
- Offline inversions / contribution counting with a running Fenwick
- Need something lighter than a segment tree and the op has an inverse

---

#### 7. Contest WA / TLE / RE Traps

- 0-index vs 1-index: `i & -i` formulas assume 1-based indices
- Forgetting `long long` on sums
- Range sum with XOR: use `sumPrefix(r) ^ sumPrefix(l-1)`, not minus
- `lower_bound` on Fenwick assumes non-negative frequencies
- Off-by-one at `r+1` in range-update difference arrays when \(r=n\)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1311F | Moving Points | 2000 | Fenwick, Line Sweep, Coordinate Compression | Sort by velocity, sweep with 2 Fenwicks for count and coordinate prefix sums. | [Solve Problem](https://codeforces.com/contest/1311/problem/F) |
| Codeforces | CF-1073D | Berland Fair | 1800 | Fenwick, Binary Search | Fenwick tree tracking active stalls and sum of costs for fast cycle simulation. | [Solve Problem](https://codeforces.com/contest/1073/problem/D) |
| Codeforces | CF-1208D | Restore Permutation | 1900 | Fenwick, Binary Lifting, Greedy | Reverse reconstruction using Fenwick binary lifting in O(log N). | [Solve Problem](https://codeforces.com/contest/1208/problem/D) |
| CSES | CSES-1648 | Dynamic Range Sum Queries | 1400 | Fenwick, Range Queries | Standard Fenwick tree 1-based prefix sums and point updates. | [Solve Problem](https://cses.fi/problemset/task/1648) |
| Codeforces | CF-1404C | Fixed Point Removal | 2300 | Fenwick, Binary Lifting, Offline Sweep | Offline query sweep with Fenwick binary lifting to find maximum active prefix. | [Solve Problem](https://codeforces.com/contest/1404/problem/C) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fenwick Tree (Binary Indexed Tree)](https://cp-algorithms.com/data_structures/fenwick.html)
- **[USACO Guide]** [USACO Guide: Point Update Range Sum (Fenwick)](https://usaco.guide/gold/purq)
- **[YouKn0wWho]** [YouKn0wWho Academy: Fenwick Tree Mastery](https://youkn0wwho.academy/topic-list#fenwick-tree)
- **[Codeforces]** [Codeforces Blog: Binary Lifting on Fenwick Tree](https://codeforces.com/blog/entry/61364)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **XOR Fenwick:** same code with `^=` / `^`
- **Range update, point query:** one BIT on differences
- **Range update, range query:** `RangeBIT` above
- **2D Fenwick:** next topic
- **Fenwick on Euler tour:** subtree add / path tricks with entry-exit
- **Compression:** map values to ranks before counting

---

#### 11. Typical Problem Archetypes

1. Standard application: point updates + range sums
2. Slightly disguised: count inversions / “elements ≤ x in prefix”
3. Difficult: range add + range sum online; k-th by frequency Fenwick
4. Very difficult / advanced: Fenwick + CDQ for 3D partial order; dynamic 2D offline

---

#### 12. Recognition & Identification Drills

1. Array of size \(n\); \(q\) ops: set \(a_i \leftarrow x\) or print \(\sum_{i=l}^{r} a_i\).
2. Process updates “add \(v\) on \([l,r]\)” and queries “value at index \(i\)”.
3. Multiset of numbers in \([1,n]\); support insert/delete and “k-th smallest”.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: invertible prefix structure + updates; prefer over segtree for sum/XOR
- Key invariant: node `i` = sum of last `i&-i` elements
- Key formula: range = prefix(r) − prefix(l−1); range-add via diffs
- Complexity: \(O(\log n)\) per op, \(O(n)\) memory
- Template to remember: `for (; i <= n; i += i & -i)` / `for (; i > 0; i -= i & -i)`

---

## 2. 2D Fenwick

---


---

<a id="topic-2"></a>
### 2. 2D Fenwick Tree

> **Section:** §01 Fenwick Tree (Binary Indexed Tree)  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** 1D Fenwick, coordinate compression, offline thinking  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: 1D Fenwick, coordinate compression, offline thinking

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Fenwick tree (Binary Indexed Tree) is a compact, cache-friendly data structure that maintains prefix sums of an array of $N$ numbers in $\mathcal{O}(N)$ space and supports $\mathcal{O}(\log N)$ point updates and prefix sum queries.

##### Fundamental Theorems & Invariants

- **Lowest Set Bit Decomposition:** For any index $i \ge 1$, $\text{LSB}(i) = i \& (-i)$. The interval managed by index $i$ in a 1-indexed BIT is $(i - \text{LSB}(i), i]$.
- **Prefix Sum Invariant:** The prefix sum $S(r) = \sum_{i=1}^r A[i]$ is composed of at most $\lfloor \log_2 r \rfloor + 1$ disjoint canonical binary intervals.
- **Point Update Invariant:** Incrementing $A[i]$ by $v$ propagates strictly to ancestors $i \leftarrow i + \text{LSB}(i)$, visiting at most $\mathcal{O}(\log N)$ nodes.
- **Binary Lifting on BIT (Order Statistics):** Finding the smallest index $r$ such that $\sum_{i=1}^r A[i] \ge k$ can be solved in pure $\mathcal{O}(\log N)$ time without extra binary search factors by jumping power-of-two steps from MSB to LSB.

##### Algorithmic Execution Blueprint

1. **Initialization:** Preallocate array `bit` of size $N+1$ initialized to $0$. Build in $\mathcal{O}(N)$ linear time by propagating each index $i$ to its immediate parent $i + (i \& -i)$.
2. **Point Update:** To add $v$ at index $i$: while $i \le N$, execute `bit[i] += v` and `i += i & -i`.
3. **Prefix Query:** To query $\sum_{j=1}^i A[j]$: initialize $S = 0$; while $i > 0$, execute `S += bit[i]` and `i -= i & -i`.
4. **Range Update & Range Sum:** Maintain two Fenwick trees $B_1$ and $B_2$. Adding $v$ to $[L, R]$ updates $B_1$ with $+v$ at $L$, $-v$ at $R+1$, and updates $B_2$ with $+v \cdot (L-1)$ at $L$, $-v \cdot R$ at $R+1$. The prefix sum at $r$ equals $r \cdot B_1(r) - B_2(r)$.

##### Closed-Form Invariant Equations

$$\sum_{i=1}^r A[i] = (r+1)\sum_{j=1}^r d_j - \sum_{j=1}^r j \cdot d_j = (r+1)B_1(r) - B_2(r)$$

##### Structural Edge Cases & Assumptions

- Fenwick trees MUST be 1-indexed. Passing index $0$ into $i \& -i$ causes an infinite loop ($0 \& -0 = 0$).
- Coordinate compression is required when coordinates exceed $10^7$ or are negative.
- Prefix sums on frequencies can exceed standard 32-bit integers; always use 64-bit `long long` for accumulators.

---

#### 3. Core Intuition & Problem Framing

Nest Fenwicks: outer index walks rows with `i & -i`, inner walks columns. Point \((x,y)\) contributes to \(O(\log X\log Y)\) nodes; rectangle prefix is inclusion-exclusion of four prefixes. True online 2D segtrees are heavier; 2D BIT + compression is the contest default for “point updates + rectangle sums.”

---

#### 4. Proof Sketches & Recurrences

\[
\mathrm{pref}(X,Y)=\sum_{x\le X}\sum_{y\le Y} a_{x,y}
\]
Rectangle \([x_1,x_2]\times[y_1,y_2]\):
\[
\mathrm{pref}(x_2,y_2)-\mathrm{pref}(x_1-1,y_2)-\mathrm{pref}(x_2,y_1-1)+\mathrm{pref}(x_1-1,y_1-1).
\]
Each update/query: \(O(\log X\log Y)\). Memory \(O(XY)\) dense, or sparse maps / offline dynamic — for contests usually compress to \(\le n\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) empty / \(O(n\log^2)\) for \(n\) points
- Per-query / per-operation: \(O(\log X\log Y)\)
- Total: \(O(q\log^2 n)\) after compression to \(n\)
- Memory: \(O(XY)\) dense; often \(O(n^2)\) worst after compression if careless — compress both axes to ranks \(\le n\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Points in a plane; rectangle sum / count queries
- “Add value at (x,y); query sum in \([x1,x2]\times[y1,y2]\)”
- Offline 2D counting after compressing coordinates
- Prefer this over naive 2D segtree when only sum/count + points matter

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting four-term inclusion-exclusion
- Using raw coordinates without compression → MLE/RE
- Updating only one copy when points are “set” not “add” (subtract old value first)
- Mixing 0/1-index on x and y independently

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1311F | Moving Points | 2000 | Fenwick, Line Sweep, Coordinate Compression | Sort by velocity, sweep with 2 Fenwicks for count and coordinate prefix sums. | [Solve Problem](https://codeforces.com/contest/1311/problem/F) |
| Codeforces | CF-1073D | Berland Fair | 1800 | Fenwick, Binary Search | Fenwick tree tracking active stalls and sum of costs for fast cycle simulation. | [Solve Problem](https://codeforces.com/contest/1073/problem/D) |
| Codeforces | CF-1208D | Restore Permutation | 1900 | Fenwick, Binary Lifting, Greedy | Reverse reconstruction using Fenwick binary lifting in O(log N). | [Solve Problem](https://codeforces.com/contest/1208/problem/D) |
| CSES | CSES-1648 | Dynamic Range Sum Queries | 1400 | Fenwick, Range Queries | Standard Fenwick tree 1-based prefix sums and point updates. | [Solve Problem](https://cses.fi/problemset/task/1648) |
| Codeforces | CF-1404C | Fixed Point Removal | 2300 | Fenwick, Binary Lifting, Offline Sweep | Offline query sweep with Fenwick binary lifting to find maximum active prefix. | [Solve Problem](https://codeforces.com/contest/1404/problem/C) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fenwick Tree (Binary Indexed Tree)](https://cp-algorithms.com/data_structures/fenwick.html)
- **[USACO Guide]** [USACO Guide: Point Update Range Sum (Fenwick)](https://usaco.guide/gold/purq)
- **[YouKn0wWho]** [YouKn0wWho Academy: Fenwick Tree Mastery](https://youkn0wwho.academy/topic-list#fenwick-tree)
- **[Codeforces]** [Codeforces Blog: Binary Lifting on Fenwick Tree](https://codeforces.com/blog/entry/61364)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Count-only (store 1 per point)
- Offline: process by x-sweep + 1D Fenwick on y (often faster / less memory than full 2D)
- Range add rectangle + point query: 2D difference + 2D BIT
- Dynamic sparse: `map` / segment tree of Fenwicks (heavier)

---

#### 11. Typical Problem Archetypes

1. Standard application: point add, rectangle sum
2. Slightly disguised: number of points in rectangles offline
3. Difficult: rectangle add + rectangle sum (need more structure / segtree beats-style or lazy 2D — rare)
4. Very difficult / advanced: CDQ divide-conquer replacing 2D/3D structures

---

#### 12. Recognition & Identification Drills

1. \(n\) weighted points; \(q\) axis-aligned rectangle sum queries (offline OK).
2. Grid \(n\times m\) (\(n,m\le 1000\)); point updates and sub-rectangle sums.
3. Count inversions in 2D: pairs \(i<j\), \(x_i<x_j\), \(y_i>y_j\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: 2D point updates + rectangle prefix sums/counts
- Key invariant: nested BIT covers
- Key formula: 4-prefix inclusion-exclusion
- Complexity: \(O(\log^2 n)\) per op after compression
- Template to remember: double `i += i & -i` loops + compress coords

---

## 3. Sparse table

---


---
