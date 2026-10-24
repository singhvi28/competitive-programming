# 2D segment tree / alternatives

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** Segtree; 2D fenwick; CDQ divide-conquer; offline thinking  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Segtree; 2D fenwick; CDQ divide-conquer; offline thinking

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

## 3. Core Intuition & Problem Framing

Naive 2D segtree: segtree on `x`, each node holds a segtree on `y` of points in that `x`-segment. Build/memory `O(n log² n)` for points; query rectangle `O(log² n)`; updates painful.

**Early ROI is low** because almost every “2D range” CF problem has a better tool:
- **2D fenwick** on compressed grid — if point add + rectangle sum.
- **CDQ / D&C on time** — offline 3D partial order.
- **Sweep + 1D fenwick/segtree** — classic.
- **Merge-sort tree** — static `x` as index, `y` as value.
- **Persistent segtree** — insert by `x`, query `y`-range on version difference.

Use true 2D segtree only when online 2D with ops that don’t fit fenwick and offline is impossible.

---

## 4. Proof Sketches & Recurrences

For `n` points: outer tree sorts by `x` (or builds on compressed `x`). Node’s inner structure stores all points with that `x`-range sorted by `y` (merge-sort style) or a balanced BST/fenwick of `y`.

Rectangle query `[x1,x2] × [y1,y2]`: O(log n) outer nodes × O(log n) inner = O(log² n).

Memory: if each outer node stores fenwick of size = points in node, total `O(n log n)`.

Segment-of-segment-of-arrays without care → `O(n log² n)` memory easy MLE.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: 2D fenwick `O(nm)` or `O(n log² n)` sparse builds; naive 2D seg `O(n log² n)`
- Per-query / per-operation: `O(log² n)` typical rectangle
- Total: depends; CDQ often `O(n log² n)` offline
- Memory: fenwick2D dense `O(nm)`; sparse `O(n log n)` — 2D seg easy MLE`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace fenwick2d {
// Prefer this over 2D segtree when possible
struct Fenwick2D {
  int n, m;
  vector<vector<long long>> bit;
  Fenwick2D(int n_, int m_) : n(n_), m(m_), bit(n + 1, vector<long long>(m + 1)) {}
  void add(int x, int y, long long v) {
    for (int i = x; i <= n; i += i & -i)
      for (int j = y; j <= m; j += j & -j) bit[i][j] += v;
  }
  long long sum(int x, int y) const {
    long long r = 0;
    for (int i = x; i > 0; i -= i & -i)
      for (int j = y; j > 0; j -= j & -j) r += bit[i][j];
    return r;
  }
  long long rect(int x1, int y1, int x2, int y2) const {
    return sum(x2, y2) - sum(x1 - 1, y2) - sum(x2, y1 - 1) + sum(x1 - 1, y1 - 1);
  }
};
} // namespace fenwick2d

namespace segtree_2d_points {
// Static points: outer merge-sort by x-index, inner sorted y + fenwick on build order
// Simpler practical pattern: compress x,y; use Fenwick2D after mapping points to grid
struct PointAddRectSumOffline {
  // placeholder pattern: compress, then fenwick2d — full 2D segtree omitted as low-ROI
};
} // namespace segtree_2d_points

namespace segtree_of_fenwicks {
// Dynamic points with compressed y per x-node — advanced; sketch only
struct SegFenwick {
  int n;
  vector<vector<int>> ys; // sorted y coords per seg node
  vector<vector<long long>> bit;
  vector<int> X; // compressed x of points
  vector<long long> Yv;
  // build ys by merging; bit sized ys[v].size()
  // update: walk x-path, add into each node's fenwick at y-rank
  // query: walk x-canonical, sum fenwicks for y-range
};
} // namespace segtree_of_fenwicks
```

---

## 6. Recognition Trigger Signals & Heuristics

- Rectangle sum with point updates on grid → 2D fenwick first.
- Offline “add point / query rectangle” → sweep or CDQ.
- Static points, query count in rectangle → merge-sort / persistent / fenwick2D build.
- Online arbitrary 2D range chmin — suffering; rethink problem.

---

## 7. Contest WA / TLE / RE Traps

- Reaching for 2D segtree when 2D fenwick suffices.
- MLE from `vector` of full inner trees sized to global `m`.
- Off-by-one in rectangle inclusion-exclusion.
- Compressing x/y inconsistently between updates and queries.
- Online 2D with deletes without invertible op → stuck.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

## 10. Algorithmic Variants & Advanced Extensions

- 2D fenwick (invertible).
- Segtree of fenwicks / fenwick of segtrees.
- Persistent segtree as 2D count.
- CDQ for 3-sided/4-sided offline.
- Quadtrees (rare in CF).

---

## 11. Typical Problem Archetypes

1. Standard application: point add, rectangle sum → 2D fenwick.
2. Slightly disguised: static points rectangle count → compress + fenwick2D or merge-sort tree.
3. Difficult: online 2D with set (non-invertible) — seg of policy BST.
4. Very difficult / advanced: 2D lazy — almost never; reformulate.

---

## 12. Recognition & Identification Drills

1. `n≤2000` grid, point add, rectangle sum. Best structure?
2. `n≤1e5` static points, many rectangle counts. List two approaches that beat naive 2D segtree coding time.
3. Offline: add point, query “points with `x≤X, y≤Y, time≤T`”. Name the technique family.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: only if simpler 2D fenwick / sweep / CDQ / persistent fail.
- Key invariant: outer canonical x-nodes × inner y-structure.
- Key formula: rectangle = inclusion-exclusion on 2D prefixes when invertible.
- Complexity: usually `O(log² n)` query; watch memory.
- Template to remember: **prefer fenwick2D**; seg-of-fenwicks if forced dynamic.

---

---
