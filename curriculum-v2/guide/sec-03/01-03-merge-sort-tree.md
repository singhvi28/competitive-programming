# Merge sort tree

> **Section:** §03 Merge Sort Trees & 2D Ranges  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Segment tree structure; binary search; sorted vectors; fenwick/PBDS alternatives awareness  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Segment tree structure; binary search; sorted vectors; fenwick/PBDS alternatives awareness

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

A Merge Sort Tree stores a sorted array of elements at each segment tree node, enabling static 2D range frequency queries (e.g., counting values in $[X_1, X_2]$ within index range $[L, R]$) in $\mathcal{O}(\log^2 N)$ time, or $\mathcal{O}(\log N)$ using Fractional Cascading.

### Fundamental Theorems & Invariants

- **Space Complexity:** Built in $\mathcal{O}(N \log N)$ time and $\mathcal{O}(N \log N)$ space, since each level of the segment tree stores exactly $N$ elements across all nodes.
- **Fractional Cascading Acceleration:** By precomputing pointers from each parent vector element to its lower-bound position in the left and right child vectors, binary search is executed only once at the root in $\mathcal{O}(\log N)$, reducing total query time from $\mathcal{O}(\log^2 N)$ to $\mathcal{O}(\log N)$.

### Algorithmic Execution Blueprint

1. **Build:** For leaf node $i$, `tree[node] = {A[i]}`. For internal nodes, merge sorted vectors of children using `std::merge`.
2. **Fractional Cascading Pointers:** For each element in `tree[node]`, record `to_left = lower_bound(tree[2*node])` and `to_right = lower_bound(tree[2*node+1])`.
3. **Range Count Query:** Decompose $[L, R]$ into $\mathcal{O}(\log N)$ canonical nodes. In each node, evaluate `upper_bound(X2) - lower_bound(X1)`.

### Closed-Form Invariant Equations

$$\text{Count}([L, R], [X_1, X_2]) = \sum_{u \in \text{canonical}([L, R])} \Big(\text{rank}(u.\text{vec}, X_2) - \text{rank}(u.\text{vec}, X_1 - 1)\Big)$$

### Structural Edge Cases & Assumptions

- Merge sort trees are static; point updates require 2D segment trees or Fenwick trees with coordinate compression.
- For dynamic $k$-th queries with updates, prefer a Persistent Segment Tree or PBDS Treap over Merge Sort Trees.

---

## 3. Core Intuition & Problem Framing

Each segtree node stores the **multiset of values** in its segment, usually as a **sorted vector** (static) or fenwick/policy BST (dynamic). Build merges child vectors like merge-sort — hence the name.

Query “how many values in `[L,R]` are `≤ x`” = sum over O(log n) nodes of `upper_bound` in each sorted vector → **O(log² n)**.

**Vs persistent segtree:** merge-sort tree is simpler for static arrays; updates are painful (need fenwick-in-nodes or rebuild). Persistent / fenwick-on-compressed-values often better for “k-th in range” with updates or for online versions.

**Vs fenwick of counts:** if coordinates compressed and you only need global order-stat, fenwick wins. Merge-sort tree shines for **range + value** 2D constraints on a static array.

---

## 4. Proof Sketches & Recurrences

Build: leaf `{a[i]}`; parent = merge(left_sorted, right_sorted) in linear time → total `O(n log n)` time and memory (each element appears in `O(log n)` nodes).

Count `≤ x` on `[ql,qr)`:
```
ans = 0
descend canonical nodes; ans += upper_bound(node.vec, x) - begin
```
Each of `O(log n)` nodes costs `O(log n)` binary search ⇒ `O(log² n)`.

K-th in range: binary search value `mid` counting ≤ mid, or walk tree comparing left-node counts (wavelet-style) for `O(log² n)`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n log n)` time and memory
- Per-query / per-operation: `O(log² n)` count; k-th `O(log³ n)` if binary search + count, or `O(log² n)` with tree walk on values
- Total: `O(n log n + q log² n)`
- Memory: `O(n log n)``

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace merge_sort_tree {
struct MST {
  int n;
  vector<vector<int>> t;
  explicit MST(const vector<int>& a) : n((int)a.size()), t(4 * max(1, n)) {
    build(1, 0, n, a);
  }
  void build(int v, int l, int r, const vector<int>& a) {
    if (r - l == 1) {
      t[v] = {a[l]};
      return;
    }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a);
    build(v << 1 | 1, m, r, a);
    t[v].resize(t[v << 1].size() + t[v << 1 | 1].size());
    merge(t[v << 1].begin(), t[v << 1].end(),
          t[v << 1 | 1].begin(), t[v << 1 | 1].end(),
          t[v].begin());
  }
  // count in [ql,qr) with value in [lo, hi] inclusive
  int count(int ql, int qr, int lo, int hi) const {
    return count(1, 0, n, ql, qr, lo, hi);
  }
  int count(int v, int l, int r, int ql, int qr, int lo, int hi) const {
    if (qr <= l || r <= ql) return 0;
    if (ql <= l && r <= qr) {
      auto L = lower_bound(t[v].begin(), t[v].end(), lo);
      auto R = upper_bound(t[v].begin(), t[v].end(), hi);
      return (int)(R - L);
    }
    int m = (l + r) >> 1;
    return count(v << 1, l, m, ql, qr, lo, hi)
         + count(v << 1 | 1, m, r, ql, qr, lo, hi);
  }
  // k-th smallest in [ql,qr), 0-based k; assumes 0 <= k < length
  int kth(int ql, int qr, int k) const {
    int lo = 0, hi = (int)t[1].size() ? t[1].back() : 0;
    // better: binary search on value using global min/max from t[1]
    if (!t[1].empty()) { lo = t[1].front(); hi = t[1].back(); }
    while (lo < hi) {
      int mid = lo + (hi - lo) / 2;
      int cnt = count(ql, qr, INT_MIN / 2, mid); // careful with bounds
      // use lo/hi from compressed coords in practice
      if (cnt <= k) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }
};

// Fractional cascading optional — rarely needed on CF; O(log^2) usually passes
} // namespace merge_sort_tree
```

### Python 3 Template

```python
# Usable for n ≲ 1e5, q ≲ 1e5 if careful; memory heavy
import bisect

class MergeSortTree:
    __slots__ = ("n", "t")

    def __init__(self, a: list[int]):
        self.n = len(a)
        self.t = [None] * (4 * max(1, self.n))
        self._build(1, 0, self.n, a)

    def _build(self, v, l, r, a):
        if r - l == 1:
            self.t[v] = [a[l]]
            return
        m = (l + r) // 2
        self._build(v << 1, l, m, a)
        self._build(v << 1 | 1, m, r, a)
        self.t[v] = sorted(self.t[v << 1] + self.t[v << 1 | 1])  # OK for clarity; merge better

    def count(self, ql, qr, lo, hi):
        return self._count(1, 0, self.n, ql, qr, lo, hi)

    def _count(self, v, l, r, ql, qr, lo, hi):
        if qr <= l or r <= ql:
            return 0
        if ql <= l and r <= qr:
            L = bisect.bisect_left(self.t[v], lo)
            R = bisect.bisect_right(self.t[v], hi)
            return R - L
        m = (l + r) // 2
        return self._count(v << 1, l, m, ql, qr, lo, hi) + self._count(
            v << 1 | 1, m, r, ql, qr, lo, hi
        )
```

---

## 6. Recognition Trigger Signals & Heuristics

- Static array; queries: count of elements in `[L,R]` with value in `[a,b]`.
- K-th smallest in subarray (static) — also wavelet / persistent; merge-sort tree is the “first idea.”
- “Number of inversions where …” offline with range structures.
- Updates present → prefer BIT of BITs, dynamic segtree, or policy PBDS + fenwick, not classic merge-sort tree.

---

## 7. Contest WA / TLE / RE Traps

- Using `merge` incorrectly / not sorting leaves.
- Memory MLE at `n=1e6` (`n log n` ints).
- Updates attempted on immutable vectors.
- Off-by-one in `lower_bound`/`upper_bound` for inclusive `hi`.
- k-th binary search on wrong value domain (must compress or use true min/max).

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| SPOJ | SPOJ-KQUERY | K-query | 1800 | Merge Sort Tree, Fractional Cascading | Count elements > k in [L, R] using Merge Sort Tree binary search or offline Fenwick. | [Solve Problem](https://www.spoj.com/problems/KQUERY/) |
| SPOJ | SPOJ-MKTHNUM | K-th Number | 2000 | Merge Sort Tree, Persistent SegTree | Binary search on answer + Merge Sort Tree count or Persistent SegTree walk. | [Solve Problem](https://www.spoj.com/problems/MKTHNUM/) |
| Codeforces | CF-990G | GCD Counting | 2200 | Merge Sort Tree, Number Theory, Tree DP | Multiples grouping with tree paths and sorted divisor vectors. | [Solve Problem](https://codeforces.com/contest/990/problem/G) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Merge Sort Tree & Range Frequency](https://cp-algorithms.com/data_structures/segment_tree.html#merge-sort-tree)
- **[Codeforces]** [Codeforces Blog: Fractional Cascading on Merge Sort Trees](https://codeforces.com/blog/entry/15890)
- **[USACO Guide]** [USACO Guide: Static 2D Range Queries](https://usaco.guide/plat/2d-range)

---

## 10. Algorithmic Variants & Advanced Extensions

- Fenwick/segtree of sorted lists with updates via BITs in nodes (heavy).
- Wavelet tree: similar queries, often faster constants, harder to code.
- Persistent segtree on value axis: better for k-th + updates via path copy.
- Mo’s algorithm + fenwick: alternative for some range frequency queries.

---

## 11. Typical Problem Archetypes

1. Standard application: count values in `[a,b]` on index range `[L,R]`.
2. Slightly disguised: number of pairs `i<j` in range with `a_i>a_j` offline.
3. Difficult: distinct values count — merge-sort tree alone insufficient; need other tricks (Mo, Hilbert, persistent + DSU).
4. Very difficult / advanced: with updates — migrate to dynamic/persistent structures.

---

## 12. Recognition & Identification Drills

1. Static array; `q` queries: how many `a_i ∈ [L,R]` have `a_i ≤ x`. Structure?
2. Same but point updates change `a_i`. Why is classic merge-sort tree a bad fit?
3. Only need global k-th after insertions (no index range). Merge-sort tree or fenwick/PBDS?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: static array; range + value rectangle counts.
- Key invariant: node vector = sorted multiset of segment.
- Key formula: count = Σ `upper-lower` over O(log n) nodes.
- Complexity: build `O(n log n)`, query `O(log² n)`, memory `O(n log n)`.
- Template to remember: merge children vectors; binary search per node.

---

---
