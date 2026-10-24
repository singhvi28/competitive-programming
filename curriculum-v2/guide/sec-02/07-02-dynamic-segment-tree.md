# 7. Dynamic segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Segtree; pointers/indices pool; coordinate ranges up to 1e9/1e18  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Segtree; pointers/indices pool; coordinate ranges up to 1e9/1e18

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

When the index universe is huge (`[1, 1e18]`) but you only touch `q` positions/segments, allocate nodes **on demand**. Same recursive logic; children start null. Memory `O(q log U)` not `O(U)`.

**Vs compression:** if all coordinates known offline, **compress to 1..m** and use dense segtree/fenwick — simpler and faster. Dynamic wins when online (coordinates appear live) or when compression awkward (ranges as indices with splits).

**Vs fenwick:** fenwick needs dense 1..n; dynamic segtree is the sparse analogue for arbitrary associative ops / lazy on large universe.

---

## 4. Proof Sketches & Recurrences

Each node covers `[l,r]` mid `(l+r)/2` carefully with `int128` or `long long` mid to avoid overflow: `m = l + (r-l)/2`.

On update, if node null create it. Descend only needed side(s). Query skips null (treat as identity).

With lazy: store tag on sparse node; push creates children if needed.

Node count: each update creates ≤ `2 log U` new nodes worst case.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(1)` empty tree
- Per-query / per-operation: `O(log U)` time; `O(log U)` new nodes per update worst-case
- Total: `O(q log U)`
- Memory: `O(q log U)``

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace dynamic_segtree {
using ll = long long;

struct DynSumAdd {
  struct Node {
    ll sum = 0, add = 0;
    int L = -1, R = -1;
  };
  vector<Node> t;
  ll U0, U1; // inclusive universe [U0, U1]
  int root = -1;

  DynSumAdd(ll lo, ll hi) : U0(lo), U1(hi) { t.reserve(1 << 20); }

  int neo() {
    t.push_back(Node{});
    return (int)t.size() - 1;
  }

  void apply(int v, ll len, ll x) {
    t[v].sum += x * len;
    t[v].add += x;
  }
  void push(int v, ll l, ll r) {
    if (t[v].add == 0 || l == r) return;
    ll m = l + (r - l) / 2;
    if (t[v].L == -1) t[v].L = neo();
    if (t[v].R == -1) t[v].R = neo();
    apply(t[v].L, m - l + 1, t[v].add);
    apply(t[v].R, r - m, t[v].add);
    t[v].add = 0;
  }

  void range_add(ll ql, ll qr, ll x) { // inclusive
    if (root == -1) root = neo();
    range_add(root, U0, U1, ql, qr, x);
  }
  void range_add(int v, ll l, ll r, ll ql, ll qr, ll x) {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
      apply(v, r - l + 1, x);
      return;
    }
    push(v, l, r);
    ll m = l + (r - l) / 2;
    if (t[v].L == -1) t[v].L = neo();
    if (t[v].R == -1) t[v].R = neo();
    range_add(t[v].L, l, m, ql, qr, x);
    range_add(t[v].R, m + 1, r, ql, qr, x);
    t[v].sum = t[t[v].L].sum + t[t[v].R].sum;
  }

  ll query(ll ql, ll qr) {
    if (root == -1) return 0;
    return query(root, U0, U1, ql, qr);
  }
  ll query(int v, ll l, ll r, ll ql, ll qr) {
    if (v == -1 || qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return t[v].sum;
    push(v, l, r);
    ll m = l + (r - l) / 2;
    return query(t[v].L, l, m, ql, qr) + query(t[v].R, m + 1, r, ql, qr);
  }
};
} // namespace dynamic_segtree
```

### Python 3 Template

```python
# Light educational dynamic sum (point add, range sum), universe [0,U)
class DynPointSum:
    __slots__ = ("U", "s", "L", "R", "root")

    def __init__(self, U: int):
        self.U = U
        self.s = [0]
        self.L = [-1]
        self.R = [-1]
        self.root = 0

    def _neo(self):
        self.s.append(0)
        self.L.append(-1)
        self.R.append(-1)
        return len(self.s) - 1

    def add(self, pos, delta):
        self._add(self.root, 0, self.U, pos, delta)

    def _add(self, v, l, r, pos, delta):
        self.s[v] += delta
        if r - l == 1:
            return
        m = (l + r) // 2
        if pos < m:
            if self.L[v] == -1:
                self.L[v] = self._neo()
            self._add(self.L[v], l, m, pos, delta)
        else:
            if self.R[v] == -1:
                self.R[v] = self._neo()
            self._add(self.R[v], m, r, pos, delta)
```

---

## 6. Recognition Trigger Signals & Heuristics

- Indices up to `1e9`/`1e18`, only `q ≤ 1e5` updates.
- Online coordinates; cannot compress ahead.
- Range add/sum on huge line (coverage of segments).
- “Implicit segtree” / “sparse segtree” wording in blogs.

---

## 7. Contest WA / TLE / RE Traps

- Mid overflow: `(l+r)/2` for `l,r ~ 1e18` → use `l + (r-l)/2`.
- Inclusive vs half-open confusion on huge ranges.
- Forgetting to create children on push with lazy.
- Using dynamic when offline compression would be trivial.
- MLE from not reserving / leaking nodes on wrong recursion.

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

- Point update / range query sparse.
- Lazy range add / range sum on `[1,1e18]`.
- Dynamic on two axes → “2D dynamic” (next topic) — usually prefer alternatives.
- Persistent + dynamic combined (node pool versions).

---

## 11. Typical Problem Archetypes

1. Standard application: range coverage on coordinate line `1e9`.
2. Slightly disguised: store segments as +1/-1 on compressed ends — sometimes fenwick enough.
3. Difficult: dynamic lazy + walking for first true predicate.
4. Very difficult / advanced: dynamic Li Chao on `1e18` x-axis.

---

## 12. Recognition & Identification Drills

1. Online: add point `(x,v)` with `x∈[1,1e18]`; query sum on `[L,R]`. Compress or dynamic?
2. All `x` given in input before queries. Preferred approach?
3. Range add on `[L,R] ⊆ [1,1e18]`, query point. Difference array ideas vs dynamic lazy?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: huge universe, few touches, especially online.
- Key invariant: null child = identity segment; allocate on write.
- Key formula: mid = `l+(r-l)/2`; memory `O(q log U)`.
- Complexity: `O(log U)` per op.
- Template to remember: index pool with `L,R` child ints + lazy optional.

---

---
