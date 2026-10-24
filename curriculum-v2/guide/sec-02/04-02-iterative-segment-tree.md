# Iterative segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** Monoid segment tree idea; bit tricks helpful  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Monoid segment tree idea; bit tricks helpful

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

Pad `n` to `N = 2^{⌈log2 n⌉}` (or use non-pow2 size carefully). Store leaves at `[N, N+n)`, parents at `i>>1`. Point updates climb parents. Range queries walk from `l+=N`, `r+=N` toward root, consuming complete segments when endpoints are odd/even — **no recursion, no lazy in the classic form**.

Why contestants love it: ~2× less constant than recursive, no stack, tiny code for point-update range-query. Why not always: classic iterative form does **not** support lazy range updates cleanly (possible but ugly); non-commutative ops need careful left/right accumulation; find-first walks differ slightly.

**Vs recursive:** same asymptotics; iterative wins on TL; recursive wins on clarity for lazy / beats / persistence / dynamic nodes.

---

## 4. Proof Sketches & Recurrences

Leaves at `N+i`. Parent of `i` is `i>>1`, left child `i<<1`, right `i<<1|1`.

Query `[l,r)` half-open:
```
l += N; r += N;
L = e; R = e;
while (l < r) {
  if (l & 1) L = op(L, t[l++]);
  if (r & 1) R = op(t[--r], R);
  l >>= 1; r >>= 1;
}
return op(L, R);
```
Odd `l` means `t[l]` is a complete segment to include; odd `r` means previous node `t[r-1]` is complete.

Update: `t[p]=x; while(p>>=1) t[p]=op(t[p<<1], t[p<<1|1])`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)` after padding
- Per-query / per-operation: `O(log n)`
- Total: `O((n+q) log n)`
- Memory: `O(N) = O(n)``

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace iter_segtree {
template <class S, S (*op)(S, S), S (*e)()>
struct Seg {
  int n, N;
  vector<S> t;
  Seg() : n(0), N(0) {}
  explicit Seg(int n_) { init(n_); }
  explicit Seg(const vector<S>& a) { init((int)a.size()); for (int i = 0; i < n; ++i) t[N + i] = a[i]; build(); }

  void init(int n_) {
    n = n_;
    N = 1;
    while (N < n) N <<= 1;
    t.assign(2 * N, e());
  }
  void build() {
    for (int i = N - 1; i >= 1; --i) t[i] = op(t[i << 1], t[i << 1 | 1]);
  }
  void set(int p, S x) {
    for (t[p += N] = x; p >>= 1;) t[p] = op(t[p << 1], t[p << 1 | 1]);
  }
  S get(int p) const { return t[p + N]; }
  S all_prod() const { return t[1]; }
  S query(int l, int r) const { // [l, r)
    S L = e(), R = e();
    for (l += N, r += N; l < r; l >>= 1, r >>= 1) {
      if (l & 1) L = op(L, t[l++]);
      if (r & 1) R = op(t[--r], R);
    }
    return op(L, R);
  }
  // max r such that pred(query(l,r)) is true, assuming monoid pred monotone
  template <class F>
  int max_right(int l, F pred) const {
    if (l == n) return n;
    l += N;
    S cur = e();
    do {
      while ((l & 1) == 0) l >>= 1;
      if (!pred(op(cur, t[l]))) {
        while (l < N) {
          l <<= 1;
          if (pred(op(cur, t[l]))) cur = op(cur, t[l++]);
        }
        return l - N;
      }
      cur = op(cur, t[l++]);
    } while ((l & -l) != l);
    return n;
  }
};

inline int op_min(int a, int b) { return a < b ? a : b; }
inline int e_min() { return INT_MAX; }
} // namespace iter_segtree
```

### Python 3 Template

```python
# Excellent in Python — iterative is the preferred Py segtree
class IterSeg:
    __slots__ = ("n", "N", "t", "op", "e")

    def __init__(self, n, op, e, a=None):
        self.n, self.op, self.e = n, op, e
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.t = [e] * (2 * self.N)
        if a is not None:
            for i, x in enumerate(a):
                self.t[self.N + i] = x
            for i in range(self.N - 1, 0, -1):
                self.t[i] = op(self.t[i << 1], self.t[i << 1 | 1])

    def set(self, p, x):
        p += self.N
        self.t[p] = x
        p >>= 1
        while p:
            self.t[p] = self.op(self.t[p << 1], self.t[p << 1 | 1])
            p >>= 1

    def query(self, l, r):
        l += self.N
        r += self.N
        L = R = self.e
        while l < r:
            if l & 1:
                L = self.op(L, self.t[l])
                l += 1
            if r & 1:
                r -= 1
                R = self.op(self.t[r], R)
            l >>= 1
            r >>= 1
        return self.op(L, R)
```

---

## 6. Recognition Trigger Signals & Heuristics

- Point update + range query only → iterative is default ship choice.
- Need maximum speed for monoid queries in HLD (many segops) → iterative.
- Lazy / assign → stay recursive (or specialized).
- Non-commutative merge → must merge `left_acc = op(node, left_acc)` vs `right_acc = op(right_acc, node)` correctly.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to pad / using `n` not `N` as leaf base.
- Non-commutative: swapping `L`/`R` combine order.
- Inclusive `r` passed into half-open API.
- `max_right`/`min_left` bit conditions wrong (`l & -l`).
- Building without initializing unused leaves to `e`.

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

- Non-power-of-two size with `size = n` leaves at `size` and parents still `i/2` (AtCoder style) — works if `query` same.
- Dual fenwick-like for only invertible ops — not general.
- Iterative lazy exists (segment tree beats blogs) but rarely worth vs recursive.

---

## 11. Typical Problem Archetypes

1. Standard: point set, range min/sum.
2. Slightly disguised: HLD path aggregates with many queries.
3. Difficult: `max_right` for first prefix failing a predicate.
4. Very difficult: combine with Mo / offline — usually overkill vs recursive clarity.

---

## 12. Recognition & Identification Drills

1. Point updates, range products modulo prime. Iterative or fenwick?
2. You need range add later in the same problem. Start iterative or recursive?
3. Non-commutative matrix product on ranges, point set. What must query preserve?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: point update + range query; speed/clarity without lazy.
- Key invariant: `t[i] = op(t[2i], t[2i+1])`; leaves at `N+i`.
- Key formula: while-loop odd-endpoint consumption.
- Complexity: `O(log n)`, memory `2N`.
- Template to remember: AtCoder-style iterative monoid tree.

---

---
