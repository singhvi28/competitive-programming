# Lazy propagation

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Very Common  
> **Prerequisites:** Segment tree monoid; composition of updates  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Segment tree monoid; composition of updates

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

Range updates would touch `Θ(n)` leaves if applied naively. Lazy propagation stores a **pending update** on a node meaning “this update applies to the whole segment, but children are not yet materialized.” When you need to go deeper, you **push** the tag to children and clear it.

Two algebraic objects:
1. **Data monoid** `(S, ⊕, e)` — what queries return.
2. **Update monoid** `(F, ∘, id)` — how updates compose; each `f ∈ F` is an affine action on `S`: applying `f` to a node’s aggregate must be doable in `O(1)` from the tag + node length / stored aux.

Classic: range add on sum → tag `add`; `sum += add * len`. Range assign → tag `set` with priority over add. Composition order matters: usually “new update applied **after** old” or the reverse — pick one and stick to it in `compose` and `push`.

---

## 4. Proof Sketches & Recurrences

Maintain `t[v]` = true aggregate of segment (as if all tags pushed), and `lz[v]` = pending update for children.

**Apply tag `f` to node `v` covering length `len`:**
`t[v] ← f · t[v]` (action), `lz[v] ← f ∘ lz[v]` (compose onto pending).

**Push:** if `lz[v] ≠ id`, apply `lz[v]` to both children, then `lz[v] ← id`.

**Range update on `[ql,qr)`:** same canonical descent as query; before branching, `push(v)`. On full cover, `apply` only.

**Correctness:** after every public op, root’s `t[1]` is correct; tags mean “children stale relative to parent.” Parent always reflects applied tags.

Composition associativity: `(f ∘ g) · s = f · (g · s)`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: `O(log n)` amortized/worst for standard tags
- Total: `O((n+q) log n)`
- Memory: `O(n)` data + `O(n)` tags`

### C++17 Template

```cpp
// C++17 — lazy segtree: range add + range min (common starter)
#include <bits/stdc++.h>
using namespace std;

namespace lazy_segtree {
struct Tag {
  long long add = 0;
  bool empty() const { return add == 0; }
  void compose(const Tag& o) { add += o.add; } // apply o then this? here: accumulate adds
};

struct Node {
  long long mn = LLONG_MAX / 4;
};

inline Node merge(const Node& a, const Node& b) {
  return Node{min(a.mn, b.mn)};
}

struct LazySeg {
  int n;
  vector<Node> t;
  vector<Tag> lz;
  explicit LazySeg(int n_) : n(n_), t(4 * max(1, n_)), lz(4 * max(1, n_)) {}
  explicit LazySeg(const vector<long long>& a) : LazySeg((int)a.size()) { build(1, 0, n, a); }

  void build(int v, int l, int r, const vector<long long>& a) {
    if (r - l == 1) { t[v].mn = a[l]; return; }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a);
    build(v << 1 | 1, m, r, a);
    pull(v);
  }
  void pull(int v) { t[v] = merge(t[v << 1], t[v << 1 | 1]); }

  void apply(int v, const Tag& tag, int /*len*/) {
    t[v].mn += tag.add;
    lz[v].compose(tag);
  }
  void push(int v, int l, int r) {
    if (lz[v].empty() || r - l == 1) return;
    int m = (l + r) >> 1;
    apply(v << 1, lz[v], m - l);
    apply(v << 1 | 1, lz[v], r - m);
    lz[v] = Tag{};
  }

  void range_add(int ql, int qr, long long x) { range_add(1, 0, n, ql, qr, Tag{x}); }
  void range_add(int v, int l, int r, int ql, int qr, Tag tag) {
    if (qr <= l || r <= ql) return;
    if (ql <= l && r <= qr) { apply(v, tag, r - l); return; }
    push(v, l, r);
    int m = (l + r) >> 1;
    range_add(v << 1, l, m, ql, qr, tag);
    range_add(v << 1 | 1, m, r, ql, qr, tag);
    pull(v);
  }

  Node query(int ql, int qr) { return query(1, 0, n, ql, qr); }
  Node query(int v, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql) return Node{}; // identity for min: +inf — fix below
    if (ql <= l && r <= qr) return t[v];
    push(v, l, r);
    int m = (l + r) >> 1;
    return merge(query(v << 1, l, m, ql, qr), query(v << 1 | 1, m, r, ql, qr));
  }
};

// Fix identity: use optional merge with sentinel
struct LazySegMin {
  int n;
  vector<long long> t, lz;
  static constexpr long long INF = LLONG_MAX / 4;
  explicit LazySegMin(int n_) : n(n_), t(4 * max(1, n_), INF), lz(4 * max(1, n_), 0) {}
  explicit LazySegMin(const vector<long long>& a) : LazySegMin((int)a.size()) {
    build(1, 0, n, a);
  }
  void build(int v, int l, int r, const vector<long long>& a) {
    if (r - l == 1) { t[v] = a[l]; return; }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a); build(v << 1 | 1, m, r, a);
    t[v] = min(t[v << 1], t[v << 1 | 1]);
  }
  void apply(int v, long long x) { t[v] += x; lz[v] += x; }
  void push(int v) {
    if (lz[v] == 0) return;
    apply(v << 1, lz[v]); apply(v << 1 | 1, lz[v]); lz[v] = 0;
  }
  void add(int ql, int qr, long long x) { add(1, 0, n, ql, qr, x); }
  void add(int v, int l, int r, int ql, int qr, long long x) {
    if (qr <= l || r <= ql) return;
    if (ql <= l && r <= qr) { apply(v, x); return; }
    push(v);
    int m = (l + r) >> 1;
    add(v << 1, l, m, ql, qr, x); add(v << 1 | 1, m, r, ql, qr, x);
    t[v] = min(t[v << 1], t[v << 1 | 1]);
  }
  long long query(int ql, int qr) { return query(1, 0, n, ql, qr); }
  long long query(int v, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql) return INF;
    if (ql <= l && r <= qr) return t[v];
    push(v);
    int m = (l + r) >> 1;
    return min(query(v << 1, l, m, ql, qr), query(v << 1 | 1, m, r, ql, qr));
  }
};
} // namespace lazy_segtree
```

### Python 3 Template

```python
# Usable for n,q ≲ 1e5 with PyPy; C++ preferred for 2e5+ tight limits
class LazyMinAdd:
    __slots__ = ("n", "t", "lz")
    INF = 10**18

    def __init__(self, a: list[int]):
        self.n = len(a)
        self.t = [self.INF] * (4 * max(1, self.n))
        self.lz = [0] * (4 * max(1, self.n))
        self._build(1, 0, self.n, a)

    def _build(self, v, l, r, a):
        if r - l == 1:
            self.t[v] = a[l]
            return
        m = (l + r) // 2
        self._build(v << 1, l, m, a)
        self._build(v << 1 | 1, m, r, a)
        self.t[v] = min(self.t[v << 1], self.t[v << 1 | 1])

    def _apply(self, v, x):
        self.t[v] += x
        self.lz[v] += x

    def _push(self, v):
        if self.lz[v] == 0:
            return
        self._apply(v << 1, self.lz[v])
        self._apply(v << 1 | 1, self.lz[v])
        self.lz[v] = 0

    def add(self, ql, qr, x):
        self._add(1, 0, self.n, ql, qr, x)

    def _add(self, v, l, r, ql, qr, x):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            self._apply(v, x)
            return
        self._push(v)
        m = (l + r) // 2
        self._add(v << 1, l, m, ql, qr, x)
        self._add(v << 1 | 1, m, r, ql, qr, x)
        self.t[v] = min(self.t[v << 1], self.t[v << 1 | 1])

    def query(self, ql, qr):
        return self._query(1, 0, self.n, ql, qr)

    def _query(self, v, l, r, ql, qr):
        if qr <= l or r <= ql:
            return self.INF
        if ql <= l and r <= qr:
            return self.t[v]
        self._push(v)
        m = (l + r) // 2
        return min(self._query(v << 1, l, m, ql, qr), self._query(v << 1 | 1, m, r, ql, qr))
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Add `v` on `[l,r]`, query sum/min/max on `[L,R]`” → lazy add.
- “Set all on `[l,r]` to `x`, then query” → lazy assign (often with add mixed).
- Updates are **uniform** on a segment and query aggregate has closed form under that update.
- If updates are arbitrary per index inside range → not plain lazy; need different model.
- Only range add + range sum → fenwick with difference tricks sometimes; min/max after add still wants lazy segtree.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `push` before recursing → WA.
- Composing tags in wrong order (assign vs add).
- Applying add to min OK; applying add to sum needs `* len`.
- Pushing on leaves unnecessarily / not clearing tag.
- Query identity wrong when merging partials.
- Mixing 0-index/1-index in `ql,qr`.
- Recursion stack with lazy on large `n` (rare but real).

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

- Add on sum / min / max / (min,max,sum) jointly.
- Affine `x ↦ a*x+b` on range with sum query (compose matrices / pairs `(a,b)`).
- Lazy on HLD paths / Euler subtours — same tags, mapped indices.
- Beats: “lazy chmin” that only sometimes fully covers — see Segment tree beats.

---

## 11. Typical Problem Archetypes

1. Standard: range add, range min.
2. Slightly disguised: range add, then “count of minima” — store `(min, cnt)`.
3. Difficult: affine updates + sum; or assign+add with two-tag composition.
4. Very difficult: lazy on dynamic tree indices; or beats-style chmin.

---

## 12. Recognition & Identification Drills

1. Ops: add `v` on `[l,r]`; query max on `[L,R]`. Fenwick or lazy segtree?
2. Ops: set every element in `[l,r]` to `x`; query sum. What tags do you need?
3. Range add on an array of matrices; query product. What must be true for lazy to work?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: uniform range updates + range queries with O(1) tag action.
- Key invariant: `t[v]` correct; `lz[v]` means children not yet updated.
- Key formula: push before descend; compose tags associatively.
- Complexity: `O(log n)` per update/query.
- Template to remember: `apply` / `push` / `pull` trio.

---

---
