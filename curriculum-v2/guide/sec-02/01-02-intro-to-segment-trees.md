# 1. Intro to segment trees

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Very Common  
> **Prerequisites:** Arrays, associative merge ops, binary tree indexing, recursion or iterative bottom-up  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Arrays, associative merge ops, binary tree indexing, recursion or iterative bottom-up

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

A segment tree is a complete binary tree over an array where every node stores an aggregate of a contiguous segment. Leaves are single elements; an internal node is the **merge** of its two children. The power comes from two facts:

1. Any interval `[L, R)` decomposes into **O(log n)** canonical nodes (disjoint, covering exactly the query).
2. Point/range updates touch **O(log n)** nodes if the merge is associative (and for range updates, if you add lazy — next topics).

Think less “tree of ranges” and more “**canonical cover** of intervals under a fixed partition of `[0,n)`”. The same cover idea appears in sparse tables (idempotent only), fenwick (prefix-shaped covers), and beats (canonical cover + pruning).

**When Fenwick is enough:** if you only need prefix-reducible ops (sum, XOR, or “add on point + prefix query” / “add on prefix + point query” via difference), Fenwick is shorter, faster constants, less bug surface. Reach for segtree when you need arbitrary range query + arbitrary point update for a non-prefix op (min/max with updates, GCD with updates, custom structs), or when you will grow into lazy / persistence / beats.

---

## 4. Proof Sketches & Recurrences

Index nodes as a heap: root = 1, children `2v`, `2v+1`. For array length `n`, use size `N = next_pow2(n)` so leaves `[N, N+n)` hold values and unused leaves are identities.

**Canonical cover:** on query `[ql, qr)`:
- If node segment `[l,r)` is fully inside → take node.
- If disjoint → skip.
- Else recurse both children.
Each level contributes ≤ 2 nodes ⇒ **≤ 4⌈log₂ N⌉** nodes in the recursive formulation; iterative walks from leaves and also **O(log n)**.

**Merge must be a monoid:** associative binary op `⊕` with identity `e` (for empty / out-of-range). Commutativity not required (matrix product, string concat — careful with child order).

**Build:** `O(n)` bottom-up: leaves then `t[v] = t[2v] ⊕ t[2v+1]`.
**Point set `i ← x`:** walk leaf → root, rematerialize.
**Range query:** cover merge left-to-right (preserve order if non-commutative).

Height `⌈log₂ N⌉`, so all ops `O(log n)` time, memory `~4n` for recursive or `2N` for iterative power-of-two.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)` build
- Per-query / per-operation: `O(log n)` point update / range query
- Total: `O((n + q) log n)` typical
- Memory: `O(n)` (~4n recursive nodes)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready — recursive monoid segtree
#include <bits/stdc++.h>
using namespace std;

namespace segtree {
template <class T, T (*op)(T, T), T (*e)()>
struct SegTree {
  int n = 0;
  vector<T> t;
  SegTree() = default;
  explicit SegTree(int n_) { init(n_); }
  explicit SegTree(const vector<T>& a) { init((int)a.size()); build(a); }

  void init(int n_) {
    n = n_;
    t.assign(4 * max(1, n), e());
  }

  void build(const vector<T>& a) { build(1, 0, n, a); }
  void build(int v, int l, int r, const vector<T>& a) {
    if (r - l == 1) {
      t[v] = (l < (int)a.size() ? a[l] : e());
      return;
    }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a);
    build(v << 1 | 1, m, r, a);
    t[v] = op(t[v << 1], t[v << 1 | 1]);
  }

  void set(int i, T x) { set(1, 0, n, i, x); }
  void set(int v, int l, int r, int i, T x) {
    if (r - l == 1) { t[v] = x; return; }
    int m = (l + r) >> 1;
    if (i < m) set(v << 1, l, m, i, x);
    else set(v << 1 | 1, m, r, i, x);
    t[v] = op(t[v << 1], t[v << 1 | 1]);
  }

  T get(int i) const { return query(i, i + 1); }

  // query on half-open [ql, qr)
  T query(int ql, int qr) const {
    if (ql >= qr) return e();
    return query(1, 0, n, ql, qr);
  }
  T query(int v, int l, int r, int ql, int qr) const {
    if (ql <= l && r <= qr) return t[v];
    if (qr <= l || r <= ql) return e();
    int m = (l + r) >> 1;
    return op(query(v << 1, l, m, ql, qr), query(v << 1 | 1, m, r, ql, qr));
  }

  // find leftmost i with pred(query[0,i+1)) true; assumes pred false on e, monotone
  template <class F>
  int min_left(F pred) const {
    T cur = e();
    auto dfs = [&](auto&& self, int v, int l, int r) -> int {
      if (r - l == 1) {
        T nxt = op(cur, t[v]);
        if (pred(nxt)) { cur = nxt; return r; }
        return l;
      }
      int m = (l + r) >> 1;
      T with_l = op(cur, t[v << 1]);
      if (!pred(with_l)) return self(self, v << 1, l, m);
      cur = with_l;
      return self(self, v << 1 | 1, m, r);
    };
    if (n == 0 || !pred(t[1])) return 0; // none / whole fails differently — caller defines
    // standard: largest r such that pred(query[0,r))
    // here return first index where extending fails when walking L→R from 0
    cur = e();
    return dfs(dfs, 1, 0, n);
  }
};

inline long long op_sum(long long a, long long b) { return a + b; }
inline long long e_sum() { return 0; }
inline long long op_min(long long a, long long b) { return min(a, b); }
inline long long e_min() { return LLONG_MAX / 4; }
inline long long op_gcd(long long a, long long b) { return std::gcd(a, b); }
inline long long e_gcd() { return 0; } // gcd(0,x)=x
} // namespace segtree
```

### Python 3 Template

```python
# Python 3.11+ — usable for n ≲ 2e5 if tight code; prefer C++ under strict TL
from __future__ import annotations

class SegTree:
    __slots__ = ("n", "t", "op", "e")

    def __init__(self, n: int, op, e, a: list | None = None):
        self.n, self.op, self.e = n, op, e
        self.t = [e] * (4 * max(1, n))
        if a is not None:
            self._build(1, 0, n, a)

    def _build(self, v, l, r, a):
        if r - l == 1:
            self.t[v] = a[l] if l < len(a) else self.e
            return
        m = (l + r) // 2
        self._build(v << 1, l, m, a)
        self._build(v << 1 | 1, m, r, a)
        self.t[v] = self.op(self.t[v << 1], self.t[v << 1 | 1])

    def set(self, i, x):
        self._set(1, 0, self.n, i, x)

    def _set(self, v, l, r, i, x):
        if r - l == 1:
            self.t[v] = x
            return
        m = (l + r) // 2
        if i < m:
            self._set(v << 1, l, m, i, x)
        else:
            self._set(v << 1 | 1, m, r, i, x)
        self.t[v] = self.op(self.t[v << 1], self.t[v << 1 | 1])

    def query(self, ql, qr):
        if ql >= qr:
            return self.e
        return self._query(1, 0, self.n, ql, qr)

    def _query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[v]
        if qr <= l or r <= ql:
            return self.e
        m = (l + r) // 2
        return self.op(
            self._query(v << 1, l, m, ql, qr),
            self._query(v << 1 | 1, m, r, ql, qr),
        )
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Point update + range query” or “range update + point query” with associative op → segtree/fenwick.
- Op is min/max/GCD/LCM/matrix multiply/monoid struct → almost always segtree (fenwick awkward).
- Need the **actual segment nodes** later (HLD, offline time-segtree, Li Chao) → learn the recursive shape even if you ship iterative.
- Static array + only idempotent RMQ → sparse table wins; do not force segtree.
- Online k-th / order statistics on ranges → merge-sort tree or fenwick-of-counts / PBDS, not plain sum tree unless compressed + fenwick.

---

## 7. Contest WA / TLE / RE Traps

- Half-open vs inclusive endpoints mismatch → off-by-one WA.
- Wrong identity (`0` for min, `INF` for sum) → silent corruption.
- Non-associative “merge” (e.g. mean) → wrong answers; store sum+count instead.
- Updating leaf but forgetting to push merges up.
- `4*n` too small when `n=1` edge; always `4*max(1,n)`.
- Querying empty range without returning `e`.
- Using recursive segtree on deep custom recursion + large `n` → stack overflow on some judges (prefer iterative for production).

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

- **Point add + range sum:** fenwick preferred.
- **Range add + point query:** difference array + fenwick/segtree.
- **Store index of min:** merge keeps `(value, index)` with tie-break.
- **Walk tree for first position with property:** binary search on tree (`find_first` / `min_left` / `max_right`) — O(log n) not O(log² n).
- **Segment tree on Euler tour / HLD:** same code, different index mapping.

---

## 11. Typical Problem Archetypes

1. Standard application: point assign, range min/sum.
2. Slightly disguised: range GCD after point updates; or “longest prefix with sum ≤ X” via tree walk.
3. Difficult: store custom monoid (max subarray sum = Kadane-on-merge with left/right/total/best).
4. Very difficult / advanced: offline queries as nodes on a time-segment tree (add edge for duration `[t1,t2)`, DSU rollback) — same skeleton, different payload.

---

## 12. Recognition & Identification Drills

1. Array of `n` integers; `q` operations: set `a[i]=x`, or report GCD on `[l,r]`. Which structure, and why not fenwick?
2. Static array; only queries “min on `[l,r]`”, no updates. Is segtree optimal?
3. After each point update you must answer “largest `r` such that sum(`[0,r)`) ≤ `X`”. How do you avoid `O(log² n)`?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: associative range query + updates; fenwick fails (non-prefix / need walk / need lazy later).
- Key invariant: parent = merge(left, right); query = merge of O(log n) disjoint canonical nodes.
- Key formula: identity `e`, `op` associative; half-open `[l,r)`.
- Complexity: `O(n)` build, `O(log n)/op`, `O(n)` memory.
- Template to remember: recursive 4n monoid tree or iterative 2N (next topic).

---

---
