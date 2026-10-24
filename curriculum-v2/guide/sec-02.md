# Section §02: Segment Trees & Range Invariants

> **Module ID:** `sec-02`  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Topic Count:** 10  

**Module Summary:** Monoid segment trees, lazy propagation tags, range assign/add, iterative bottom-up trees, segment tree beats, persistent, and dynamic trees.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Intro to segment trees](#topic-1) | `S-tier` | 1400–2000 | Very Common | [01-02-intro-to-segment-trees.md](./01-02-intro-to-segment-trees.md) |
| 2 | [Lazy propagation](#topic-2) | `S-tier` | 1600–2200 | Very Common | [02-02-lazy-propagation.md](./02-02-lazy-propagation.md) |
| 3 | [Range assign/add/query](#topic-3) | `S-tier` | 1600–2200 | Common | [03-02-range-assign-add-query.md](./03-02-range-assign-add-query.md) |
| 4 | [Iterative segment tree](#topic-4) | `A-tier` | 1400–2000 | Common | [04-02-iterative-segment-tree.md](./04-02-iterative-segment-tree.md) |
| 5 | [Segment tree beats](#topic-5) | `Niche` | 2400–3200 | Rare | [05-02-segment-tree-beats.md](./05-02-segment-tree-beats.md) |
| 6 | [Persistent segment tree](#topic-6) | `A-tier` | 1900–2600 | Occasional | [06-02-persistent-segment-tree.md](./06-02-persistent-segment-tree.md) |
| 7 | [Dynamic segment tree](#topic-7) | `B-tier` | 2000–2600 | Occasional | [07-02-dynamic-segment-tree.md](./07-02-dynamic-segment-tree.md) |
| 8 | [2D segment tree / alternatives](#topic-8) | `C-tier` | 2200–2800 | Rare | [08-02-2d-segment-tree-alternatives.md](./08-02-2d-segment-tree-alternatives.md) |
| 9 | [When each variant is actually useful](#topic-9) | `S-tier (as decision skill)` | 1400–2800 | Very Common (every segtree problem is a choice) | [09-02-when-each-variant-is-actually-useful.md](./09-02-when-each-variant-is-actually-useful.md) |
| 10 | [Typical CF patterns](#topic-10) | `S-tier` | 1400–2600 | Very Common | [10-02-typical-cf-patterns.md](./10-02-typical-cf-patterns.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Intro to segment trees

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Very Common  
> **Prerequisites:** Arrays, associative merge ops, binary tree indexing, recursion or iterative bottom-up  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Arrays, associative merge ops, binary tree indexing, recursion or iterative bottom-up

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

A segment tree is a complete binary tree over an array where every node stores an aggregate of a contiguous segment. Leaves are single elements; an internal node is the **merge** of its two children. The power comes from two facts:

1. Any interval `[L, R)` decomposes into **O(log n)** canonical nodes (disjoint, covering exactly the query).
2. Point/range updates touch **O(log n)** nodes if the merge is associative (and for range updates, if you add lazy — next topics).

Think less “tree of ranges” and more “**canonical cover** of intervals under a fixed partition of `[0,n)`”. The same cover idea appears in sparse tables (idempotent only), fenwick (prefix-shaped covers), and beats (canonical cover + pruning).

**When Fenwick is enough:** if you only need prefix-reducible ops (sum, XOR, or “add on point + prefix query” / “add on prefix + point query” via difference), Fenwick is shorter, faster constants, less bug surface. Reach for segtree when you need arbitrary range query + arbitrary point update for a non-prefix op (min/max with updates, GCD with updates, custom structs), or when you will grow into lazy / persistence / beats.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)` build
- Per-query / per-operation: `O(log n)` point update / range query
- Total: `O((n + q) log n)` typical
- Memory: `O(n)` (~4n recursive nodes)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Point update + range query” or “range update + point query” with associative op → segtree/fenwick.
- Op is min/max/GCD/LCM/matrix multiply/monoid struct → almost always segtree (fenwick awkward).
- Need the **actual segment nodes** later (HLD, offline time-segtree, Li Chao) → learn the recursive shape even if you ship iterative.
- Static array + only idempotent RMQ → sparse table wins; do not force segtree.
- Online k-th / order statistics on ranges → merge-sort tree or fenwick-of-counts / PBDS, not plain sum tree unless compressed + fenwick.

---

#### 7. Contest WA / TLE / RE Traps

- Half-open vs inclusive endpoints mismatch → off-by-one WA.
- Wrong identity (`0` for min, `INF` for sum) → silent corruption.
- Non-associative “merge” (e.g. mean) → wrong answers; store sum+count instead.
- Updating leaf but forgetting to push merges up.
- `4*n` too small when `n=1` edge; always `4*max(1,n)`.
- Querying empty range without returning `e`.
- Using recursive segtree on deep custom recursion + large `n` → stack overflow on some judges (prefer iterative for production).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Point add + range sum:** fenwick preferred.
- **Range add + point query:** difference array + fenwick/segtree.
- **Store index of min:** merge keeps `(value, index)` with tie-break.
- **Walk tree for first position with property:** binary search on tree (`find_first` / `min_left` / `max_right`) — O(log n) not O(log² n).
- **Segment tree on Euler tour / HLD:** same code, different index mapping.

---

#### 11. Typical Problem Archetypes

1. Standard application: point assign, range min/sum.
2. Slightly disguised: range GCD after point updates; or “longest prefix with sum ≤ X” via tree walk.
3. Difficult: store custom monoid (max subarray sum = Kadane-on-merge with left/right/total/best).
4. Very difficult / advanced: offline queries as nodes on a time-segment tree (add edge for duration `[t1,t2)`, DSU rollback) — same skeleton, different payload.

---

#### 12. Recognition & Identification Drills

1. Array of `n` integers; `q` operations: set `a[i]=x`, or report GCD on `[l,r]`. Which structure, and why not fenwick?
2. Static array; only queries “min on `[l,r]`”, no updates. Is segtree optimal?
3. After each point update you must answer “largest `r` such that sum(`[0,r)`) ≤ `X`”. How do you avoid `O(log² n)`?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: associative range query + updates; fenwick fails (non-prefix / need walk / need lazy later).
- Key invariant: parent = merge(left, right); query = merge of O(log n) disjoint canonical nodes.
- Key formula: identity `e`, `op` associative; half-open `[l,r)`.
- Complexity: `O(n)` build, `O(log n)/op`, `O(n)` memory.
- Template to remember: recursive 4n monoid tree or iterative 2N (next topic).

---

---


---

<a id="topic-2"></a>
### 2. Lazy propagation

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Very Common  
> **Prerequisites:** Segment tree monoid; composition of updates  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Segment tree monoid; composition of updates

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

Range updates would touch `Θ(n)` leaves if applied naively. Lazy propagation stores a **pending update** on a node meaning “this update applies to the whole segment, but children are not yet materialized.” When you need to go deeper, you **push** the tag to children and clear it.

Two algebraic objects:
1. **Data monoid** `(S, ⊕, e)` — what queries return.
2. **Update monoid** `(F, ∘, id)` — how updates compose; each `f ∈ F` is an affine action on `S`: applying `f` to a node’s aggregate must be doable in `O(1)` from the tag + node length / stored aux.

Classic: range add on sum → tag `add`; `sum += add * len`. Range assign → tag `set` with priority over add. Composition order matters: usually “new update applied **after** old” or the reverse — pick one and stick to it in `compose` and `push`.

---

#### 4. Proof Sketches & Recurrences

Maintain `t[v]` = true aggregate of segment (as if all tags pushed), and `lz[v]` = pending update for children.

**Apply tag `f` to node `v` covering length `len`:**
`t[v] ← f · t[v]` (action), `lz[v] ← f ∘ lz[v]` (compose onto pending).

**Push:** if `lz[v] ≠ id`, apply `lz[v]` to both children, then `lz[v] ← id`.

**Range update on `[ql,qr)`:** same canonical descent as query; before branching, `push(v)`. On full cover, `apply` only.

**Correctness:** after every public op, root’s `t[1]` is correct; tags mean “children stale relative to parent.” Parent always reflects applied tags.

Composition associativity: `(f ∘ g) · s = f · (g · s)`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: `O(log n)` amortized/worst for standard tags
- Total: `O((n+q) log n)`
- Memory: `O(n)` data + `O(n)` tags`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Add `v` on `[l,r]`, query sum/min/max on `[L,R]`” → lazy add.
- “Set all on `[l,r]` to `x`, then query” → lazy assign (often with add mixed).
- Updates are **uniform** on a segment and query aggregate has closed form under that update.
- If updates are arbitrary per index inside range → not plain lazy; need different model.
- Only range add + range sum → fenwick with difference tricks sometimes; min/max after add still wants lazy segtree.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `push` before recursing → WA.
- Composing tags in wrong order (assign vs add).
- Applying add to min OK; applying add to sum needs `* len`.
- Pushing on leaves unnecessarily / not clearing tag.
- Query identity wrong when merging partials.
- Mixing 0-index/1-index in `ql,qr`.
- Recursion stack with lazy on large `n` (rare but real).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Add on sum / min / max / (min,max,sum) jointly.
- Affine `x ↦ a*x+b` on range with sum query (compose matrices / pairs `(a,b)`).
- Lazy on HLD paths / Euler subtours — same tags, mapped indices.
- Beats: “lazy chmin” that only sometimes fully covers — see Segment tree beats.

---

#### 11. Typical Problem Archetypes

1. Standard: range add, range min.
2. Slightly disguised: range add, then “count of minima” — store `(min, cnt)`.
3. Difficult: affine updates + sum; or assign+add with two-tag composition.
4. Very difficult: lazy on dynamic tree indices; or beats-style chmin.

---

#### 12. Recognition & Identification Drills

1. Ops: add `v` on `[l,r]`; query max on `[L,R]`. Fenwick or lazy segtree?
2. Ops: set every element in `[l,r]` to `x`; query sum. What tags do you need?
3. Range add on an array of matrices; query product. What must be true for lazy to work?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: uniform range updates + range queries with O(1) tag action.
- Key invariant: `t[v]` correct; `lz[v]` means children not yet updated.
- Key formula: push before descend; compose tags associatively.
- Complexity: `O(log n)` per update/query.
- Template to remember: `apply` / `push` / `pull` trio.

---

---


---

<a id="topic-3"></a>
### 3. Range assign/add/query

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Lazy propagation; tag composition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Lazy propagation; tag composition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

The “kitchen sink” lazy problem: support **range assign**, **range add**, and **range sum** (often also min/max). Assign annihilates previous adds on that segment; subsequent adds apply on top of the assigned value.

Model each tag as: optional assignment `set` + additive `add`. Semantics for a value `x`:
- If `has_set`: value becomes `set + add` (or apply set then add).
- Else: `x ← x + add`.

Composition of tags `f` after `g` (first `g`, then `f`):
- If `f` has set: result = `f` (ignore `g`).
- Else: result keeps `g`’s set (if any) and `add = g.add + f.add`.

For sums: assignment sets `sum = value * len`; add does `sum += delta * len`. Same for min/max with assign/add.

This is the workhorse for AtCoder library–style problems and many CF Div.2 D/E.

---

#### 4. Proof Sketches & Recurrences

Tag `(has_set, set_val, add)` acting on node aggregate `(sum, mn, mx, len)`:

```
apply_set(v, x): sum=x*len; mn=mx=x; has_set=1; set_val=x; add=0
apply_add(v, d): sum+=d*len; mn+=d; mx+=d; add+=d  (set_val+=d if has_set)
```

Composition `f ∘ g` (g first):
```
if f.has_set: return f
else: g.add += f.add; if g.has_set: g.set_val += f.add; return g
```

Push applies tag to children then clears. Pull merges children sums/mins/maxes.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: `O(log n)`
- Total: `O((n+q) log n)`
- Memory: `O(n)``

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace range_assign_add {
struct Tag {
  bool has_set = false;
  long long set_val = 0, add = 0;
  static Tag Set(long long x) { return {true, x, 0}; }
  static Tag Add(long long x) { return {false, 0, x}; }
  // compose: apply `o` first, then `*this`
  void compose(const Tag& o) {
    if (has_set) {
      // this already overwrites o entirely if we apply this after... 
      // We want: result = this ∘ o  meaning apply o then this.
      // If this has set, result is this (o ignored).
      return;
    }
    // this is pure add
    if (o.has_set) {
      has_set = true;
      set_val = o.set_val + add;
      add = 0;
    } else {
      add += o.add;
    }
  }
  // Better explicit: combine old pending with new update
};

// Cleaner API: apply new tag ON TOP of existing lz
inline void put_tag(Tag& lz, const Tag& neu) {
  if (neu.has_set) {
    lz = neu;
  } else {
    if (lz.has_set) lz.set_val += neu.add;
    else lz.add += neu.add;
    // if lz was empty pure add, accumulate
    if (!lz.has_set) { /* lz.add already */ }
  }
}

struct Info {
  long long sum = 0, mn = 0, mx = 0;
  int len = 0;
};

inline Info merge(Info a, Info b) {
  if (a.len == 0) return b;
  if (b.len == 0) return a;
  return {a.sum + b.sum, min(a.mn, b.mn), max(a.mx, b.mx), a.len + b.len};
}

struct Seg {
  int n;
  vector<Info> t;
  vector<Tag> lz;
  explicit Seg(int n_) : n(n_), t(4 * max(1, n_)), lz(4 * max(1, n_)) {}
  explicit Seg(const vector<long long>& a) : Seg((int)a.size()) { build(1, 0, n, a); }

  void build(int v, int l, int r, const vector<long long>& a) {
    if (r - l == 1) {
      long long x = a[l];
      t[v] = {x, x, x, 1};
      return;
    }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a);
    build(v << 1 | 1, m, r, a);
    pull(v);
  }
  void pull(int v) { t[v] = merge(t[v << 1], t[v << 1 | 1]); }

  void apply_node(int v, const Tag& tag) {
    if (tag.has_set) {
      long long x = tag.set_val + tag.add; // allow set+add in one tag
      t[v].sum = x * t[v].len;
      t[v].mn = t[v].mx = x;
      lz[v] = Tag::Set(x);
    } else if (tag.add) {
      t[v].sum += tag.add * t[v].len;
      t[v].mn += tag.add;
      t[v].mx += tag.add;
      if (lz[v].has_set) lz[v].set_val += tag.add;
      else lz[v].add += tag.add;
    }
  }

  void push(int v) {
    Tag& z = lz[v];
    if (!z.has_set && z.add == 0) return;
    apply_node(v << 1, z);
    apply_node(v << 1 | 1, z);
    z = Tag{};
  }

  void range_set(int ql, int qr, long long x) { upd(1, 0, n, ql, qr, Tag::Set(x)); }
  void range_add(int ql, int qr, long long x) { upd(1, 0, n, ql, qr, Tag::Add(x)); }
  void upd(int v, int l, int r, int ql, int qr, Tag tag) {
    if (qr <= l || r <= ql) return;
    if (ql <= l && r <= qr) { apply_node(v, tag); return; }
    push(v);
    int m = (l + r) >> 1;
    upd(v << 1, l, m, ql, qr, tag);
    upd(v << 1 | 1, m, r, ql, qr, tag);
    pull(v);
  }

  Info query(int ql, int qr) { return query(1, 0, n, ql, qr); }
  Info query(int v, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql) return Info{};
    if (ql <= l && r <= qr) return t[v];
    push(v);
    int m = (l + r) >> 1;
    return merge(query(v << 1, l, m, ql, qr), query(v << 1 | 1, m, r, ql, qr));
  }
};
} // namespace range_assign_add
```

##### Python 3 Template

```python
# Practical for moderate n; prefer C++ for assign+add+sum at 2e5 with heavy constants
class RangeAssignAddSum:
    __slots__ = ("n", "sum", "mn", "mx", "has_set", "set_val", "add")

    def __init__(self, a: list[int]):
        self.n = len(a)
        z = 4 * max(1, self.n)
        self.sum = [0] * z
        self.mn = [0] * z
        self.mx = [0] * z
        self.has_set = [False] * z
        self.set_val = [0] * z
        self.add = [0] * z
        self._build(1, 0, self.n, a)

    def _build(self, v, l, r, a):
        if r - l == 1:
            x = a[l]
            self.sum[v] = self.mn[v] = self.mx[v] = x
            return
        m = (l + r) // 2
        self._build(v << 1, l, m, a)
        self._build(v << 1 | 1, m, r, a)
        self._pull(v)

    def _pull(self, v):
        self.sum[v] = self.sum[v << 1] + self.sum[v << 1 | 1]
        self.mn[v] = min(self.mn[v << 1], self.mn[v << 1 | 1])
        self.mx[v] = max(self.mx[v << 1], self.mx[v << 1 | 1])

    def _apply_set(self, v, l, r, x):
        self.sum[v] = x * (r - l)
        self.mn[v] = self.mx[v] = x
        self.has_set[v] = True
        self.set_val[v] = x
        self.add[v] = 0

    def _apply_add(self, v, l, r, d):
        self.sum[v] += d * (r - l)
        self.mn[v] += d
        self.mx[v] += d
        if self.has_set[v]:
            self.set_val[v] += d
        else:
            self.add[v] += d

    def _push(self, v, l, r):
        m = (l + r) // 2
        if self.has_set[v]:
            self._apply_set(v << 1, l, m, self.set_val[v])
            self._apply_set(v << 1 | 1, m, r, self.set_val[v])
            self.has_set[v] = False
        if self.add[v]:
            d = self.add[v]
            self._apply_add(v << 1, l, m, d)
            self._apply_add(v << 1 | 1, m, r, d)
            self.add[v] = 0

    def range_set(self, ql, qr, x):
        self._upd_set(1, 0, self.n, ql, qr, x)

    def range_add(self, ql, qr, d):
        self._upd_add(1, 0, self.n, ql, qr, d)

    def _upd_set(self, v, l, r, ql, qr, x):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            self._apply_set(v, l, r, x)
            return
        self._push(v, l, r)
        m = (l + r) // 2
        self._upd_set(v << 1, l, m, ql, qr, x)
        self._upd_set(v << 1 | 1, m, r, ql, qr, x)
        self._pull(v)

    def _upd_add(self, v, l, r, ql, qr, d):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            self._apply_add(v, l, r, d)
            return
        self._push(v, l, r)
        m = (l + r) // 2
        self._upd_add(v << 1, l, m, ql, qr, d)
        self._upd_add(v << 1 | 1, m, r, ql, qr, d)
        self._pull(v)

    def query_sum(self, ql, qr):
        return self._query(1, 0, self.n, ql, qr)[0]

    def _query(self, v, l, r, ql, qr):
        if qr <= l or r <= ql:
            return (0, 10**18, -10**18)
        if ql <= l and r <= qr:
            return (self.sum[v], self.mn[v], self.mx[v])
        self._push(v, l, r)
        m = (l + r) // 2
        a = self._query(v << 1, l, m, ql, qr)
        b = self._query(v << 1 | 1, m, r, ql, qr)
        return (a[0] + b[0], min(a[1], b[1]), max(a[2], b[2]))
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Statement lists both “paint range to x” and “increment range” plus sum/min queries.
- “Reset segment then keep adding” stories (timelines, coverage with rebuild).
- Need length-aware aggregates under both ops.
- If only assign (no add): single set-tag suffices.
- If only add: pure add-tag; don’t overbuild.

---

#### 7. Contest WA / TLE / RE Traps

- Assign not clearing pending add (or vice versa).
- Double-counting: set tag stores `set_val` and also `add` inconsistently.
- `len` wrong on partial nodes after bad pull.
- Composition: “new set should wipe old add” forgotten → WA on mixed ops.
- Min/max not updated on add.
- Using int for sum when `x * len` overflows → use `int64`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Assign + sum only.
- Assign + add + min/max/sum (full).
- Affine `a*x+b` with composition `(a1,b1)∘(a2,b2)=(a1*a2, a1*b2+b1)`.
- Modulo arithmetic on sums.
- History: persistent lazy is rarely needed; usually offline or beats instead.

---

#### 11. Typical Problem Archetypes

1. Standard: paint / increment / sum.
2. Slightly disguised: “set range to 0 then add 1 on subranges” coverage rebuilds.
3. Difficult: maintain sum of `f(a_i)` under assign/add when `f` is polynomial — store power sums.
4. Very difficult: assign/add plus chmin (forces beats or casesplit).

---

#### 12. Recognition & Identification Drills

1. Support range set, range add, range sum. Sketch tag composition when set follows add.
2. Same ops but query “number of zeros in range”. What extra info do nodes store under assign/add?
3. Only range set + range sum — can you use a fenwick? When yes/no?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: mixed paint + increment + aggregates.
- Key invariant: set dominates; add stacks; `sum`/`mn`/`mx` always consistent with tags.
- Key formula: set ⇒ `sum=x*len`; add ⇒ `sum+=d*len`.
- Complexity: `O(log n)` per op.
- Template to remember: two-field tag `(set?, add)` with wipe-on-set.

---

---


---

<a id="topic-4"></a>
### 4. Iterative segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** Monoid segment tree idea; bit tricks helpful  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Monoid segment tree idea; bit tricks helpful

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

Pad `n` to `N = 2^{⌈log2 n⌉}` (or use non-pow2 size carefully). Store leaves at `[N, N+n)`, parents at `i>>1`. Point updates climb parents. Range queries walk from `l+=N`, `r+=N` toward root, consuming complete segments when endpoints are odd/even — **no recursion, no lazy in the classic form**.

Why contestants love it: ~2× less constant than recursive, no stack, tiny code for point-update range-query. Why not always: classic iterative form does **not** support lazy range updates cleanly (possible but ugly); non-commutative ops need careful left/right accumulation; find-first walks differ slightly.

**Vs recursive:** same asymptotics; iterative wins on TL; recursive wins on clarity for lazy / beats / persistence / dynamic nodes.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)` after padding
- Per-query / per-operation: `O(log n)`
- Total: `O((n+q) log n)`
- Memory: `O(N) = O(n)``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Point update + range query only → iterative is default ship choice.
- Need maximum speed for monoid queries in HLD (many segops) → iterative.
- Lazy / assign → stay recursive (or specialized).
- Non-commutative merge → must merge `left_acc = op(node, left_acc)` vs `right_acc = op(right_acc, node)` correctly.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to pad / using `n` not `N` as leaf base.
- Non-commutative: swapping `L`/`R` combine order.
- Inclusive `r` passed into half-open API.
- `max_right`/`min_left` bit conditions wrong (`l & -l`).
- Building without initializing unused leaves to `e`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Non-power-of-two size with `size = n` leaves at `size` and parents still `i/2` (AtCoder style) — works if `query` same.
- Dual fenwick-like for only invertible ops — not general.
- Iterative lazy exists (segment tree beats blogs) but rarely worth vs recursive.

---

#### 11. Typical Problem Archetypes

1. Standard: point set, range min/sum.
2. Slightly disguised: HLD path aggregates with many queries.
3. Difficult: `max_right` for first prefix failing a predicate.
4. Very difficult: combine with Mo / offline — usually overkill vs recursive clarity.

---

#### 12. Recognition & Identification Drills

1. Point updates, range products modulo prime. Iterative or fenwick?
2. You need range add later in the same problem. Start iterative or recursive?
3. Non-commutative matrix product on ranges, point set. What must query preserve?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: point update + range query; speed/clarity without lazy.
- Key invariant: `t[i] = op(t[2i], t[2i+1])`; leaves at `N+i`.
- Key formula: while-loop odd-endpoint consumption.
- Complexity: `O(log n)`, memory `2N`.
- Template to remember: AtCoder-style iterative monoid tree.

---

---


---

<a id="topic-5"></a>
### 5. Segment tree beats

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** Niche | **Rating Range:** 2400–3200 | **Frequency:** Rare  
> **Prerequisites:** Lazy segtree fluency; chmin/chmax intuition; amortized analysis comfort  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3200
- Prerequisites: Lazy segtree fluency; chmin/chmax intuition; amortized analysis comfort

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

Classic lazy fails for **range chmin** (`a_i ← min(a_i, x)`) because the update is not a uniform affine tag on arbitrary child values — unless the whole segment’s maximum is `≤ x` (tag is no-op) or you know enough structure to update aggregates in O(1).

**Beats** stores at each node: `mx`, `se` (strict second max), `mx_cnt`, often `sum`, and maybe `mn`/`se_min` for chmax. On chmin(`x`):
- If `mx ≤ x`: break (nothing changes).
- If `se < x < mx`: you can **beat** the node — only the maximums drop to `x`; update `sum`, `mx`, tags; **do not descend**.
- Else (`x ≤ se`): must push and recurse both children.

Amortized potential on “number of distinct values / tight maxima” gives **O(log² n)** per op typical (sometimes O(log n) amortized depending on proof). Extremely powerful on the right problem; **terrible early ROI** — learn after lazy mastery, ignore until ~2400+.

---

#### 4. Proof Sketches & Recurrences

Node invariants: `mx` = maximum; `se` = max among strictly `< mx` (or `-inf`); `cnt` = count of `mx`.

Chmin tag `x` when `se < x < mx`:
```
sum -= (mx - x) * cnt
mx = x
```
Push chmin to children with same rules.

Potential Φ = Σ_nodes (number of “distinct maximum chains”) — each failed beat (recurse) decreases global potential enough to amortize. Practical bound used in contests: treat as `O(log² n)` per update/query.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: amortized `O(log² n)` typical for chmin/chmax/add/sum suite
- Total: ~`O(q log² n)` 
- Memory: `O(n)` with large constant (~10–20 fields/node)`

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace segtree_beats {
using ll = long long;
const ll INF = (1LL << 60);

struct Beats {
  struct Node {
    ll sum, mx, se, mn, se_n;
    int cn_mx, cn_mn, len;
    ll add, fl, fg; // add tag; lazy chmin fl; lazy chmax fg
  };
  int n;
  vector<Node> t;
  explicit Beats(const vector<ll>& a) : n((int)a.size()), t(4 * max(1, n)) {
    build(1, 0, n, a);
  }

  Node make_leaf(ll x) {
    Node u{};
    u.sum = u.mx = u.mn = x;
    u.se = -INF; u.se_n = INF;
    u.cn_mx = u.cn_mn = 1; u.len = 1;
    u.add = 0; u.fl = INF; u.fg = -INF;
    return u;
  }
  Node merge(const Node& a, const Node& b) {
    Node c{};
    c.len = a.len + b.len;
    c.sum = a.sum + b.sum;
    c.add = 0; c.fl = INF; c.fg = -INF;
    // max / second max
    if (a.mx > b.mx) {
      c.mx = a.mx; c.cn_mx = a.cn_mx; c.se = max(a.se, b.mx);
    } else if (a.mx < b.mx) {
      c.mx = b.mx; c.cn_mx = b.cn_mx; c.se = max(b.se, a.mx);
    } else {
      c.mx = a.mx; c.cn_mx = a.cn_mx + b.cn_mx; c.se = max(a.se, b.se);
    }
    // min / second min
    if (a.mn < b.mn) {
      c.mn = a.mn; c.cn_mn = a.cn_mn; c.se_n = min(a.se_n, b.mn);
    } else if (a.mn > b.mn) {
      c.mn = b.mn; c.cn_mn = b.cn_mn; c.se_n = min(b.se_n, a.mn);
    } else {
      c.mn = a.mn; c.cn_mn = a.cn_mn + b.cn_mn; c.se_n = min(a.se_n, b.se_n);
    }
    return c;
  }

  void build(int v, int l, int r, const vector<ll>& a) {
    if (r - l == 1) { t[v] = make_leaf(a[l]); return; }
    int m = (l + r) >> 1;
    build(v << 1, l, m, a); build(v << 1 | 1, m, r, a);
    t[v] = merge(t[v << 1], t[v << 1 | 1]);
  }

  void apply_add(int v, ll x) {
    t[v].sum += x * t[v].len;
    t[v].mx += x; t[v].mn += x;
    if (t[v].se > -INF) t[v].se += x;
    if (t[v].se_n < INF) t[v].se_n += x;
    t[v].add += x;
    if (t[v].fl < INF) t[v].fl += x;
    if (t[v].fg > -INF) t[v].fg += x;
  }
  void apply_chmin(int v, ll x) {
    if (t[v].mx <= x) return;
    t[v].sum -= (t[v].mx - x) * t[v].cn_mx;
    t[v].mx = x;
    t[v].fl = x;
    if (t[v].mn > x) { // all equal after
      t[v].mn = x; t[v].se_n = INF; t[v].cn_mn = t[v].len;
      t[v].se = -INF; t[v].cn_mx = t[v].len;
    }
  }
  void apply_chmax(int v, ll x) {
    if (t[v].mn >= x) return;
    t[v].sum += (x - t[v].mn) * t[v].cn_mn;
    t[v].mn = x;
    t[v].fg = x;
    if (t[v].mx < x) {
      t[v].mx = x; t[v].se = -INF; t[v].cn_mx = t[v].len;
      t[v].se_n = INF; t[v].cn_mn = t[v].len;
    }
  }

  void push(int v) {
    if (t[v].add) {
      apply_add(v << 1, t[v].add);
      apply_add(v << 1 | 1, t[v].add);
      t[v].add = 0;
    }
    if (t[v].fl < INF) {
      apply_chmin(v << 1, t[v].fl);
      apply_chmin(v << 1 | 1, t[v].fl);
      t[v].fl = INF;
    }
    if (t[v].fg > -INF) {
      apply_chmax(v << 1, t[v].fg);
      apply_chmax(v << 1 | 1, t[v].fg);
      t[v].fg = -INF;
    }
  }

  void range_chmin(int ql, int qr, ll x) { chmin(1, 0, n, ql, qr, x); }
  void chmin(int v, int l, int r, int ql, int qr, ll x) {
    if (qr <= l || r <= ql || t[v].mx <= x) return;
    if (ql <= l && r <= qr && t[v].se < x) { apply_chmin(v, x); return; }
    push(v);
    int m = (l + r) >> 1;
    chmin(v << 1, l, m, ql, qr, x);
    chmin(v << 1 | 1, m, r, ql, qr, x);
    t[v] = merge(t[v << 1], t[v << 1 | 1]);
  }

  void range_add(int ql, int qr, ll x) { add(1, 0, n, ql, qr, x); }
  void add(int v, int l, int r, int ql, int qr, ll x) {
    if (qr <= l || r <= ql) return;
    if (ql <= l && r <= qr) { apply_add(v, x); return; }
    push(v);
    int m = (l + r) >> 1;
    add(v << 1, l, m, ql, qr, x);
    add(v << 1 | 1, m, r, ql, qr, x);
    t[v] = merge(t[v << 1], t[v << 1 | 1]);
  }

  ll query_sum(int ql, int qr) { return qsum(1, 0, n, ql, qr); }
  ll qsum(int v, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql) return 0;
    if (ql <= l && r <= qr) return t[v].sum;
    push(v);
    int m = (l + r) >> 1;
    return qsum(v << 1, l, m, ql, qr) + qsum(v << 1 | 1, m, r, ql, qr);
  }
  ll query_max(int ql, int qr) { return qmax(1, 0, n, ql, qr); }
  ll qmax(int v, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql) return -INF;
    if (ql <= l && r <= qr) return t[v].mx;
    push(v);
    int m = (l + r) >> 1;
    return max(qmax(v << 1, l, m, ql, qr), qmax(v << 1 | 1, m, r, ql, qr));
  }
};
} // namespace segtree_beats
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Range `a_i = min(a_i, x)` / `max(a_i, x)` plus sum or max queries.
- “Cap all values in range above threshold” repeatedly.
- Not plain assign/add; not invertible fenwick.
- If offline and only chmin + sum, sometimes CDQ / divide-conquer on time beats beats — consider alternatives first.

---

#### 7. Contest WA / TLE / RE Traps

- Wrong second-max after partial beat.
- Not handling all-equal segment (`se = -inf`) when chmin collapses.
- Forgetting to push add before chmin tags (tag order).
- Using beats when assign would suffice.
- TLE from missing break `mx ≤ x` → descends like O(n).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Chmin + sum only (lighter node).
- Chmin + chmax + add + sum (full “beats”).
- Historic beats on CF (jiupeng / angel) tutorials — stick to one verified template.
- Alternative: sqrt decomposition on values for some chmin problems.

---

#### 11. Typical Problem Archetypes

1. Standard application: range chmin, query sum.
2. Slightly disguised: repeatedly replace `a_i` with `min(a_i, x)` offline online mix.
3. Difficult: chmin/chmax/add together with max and sum queries.
4. Very difficult / advanced: beats on trees via HLD (constants brutal).

---

#### 12. Recognition & Identification Drills

1. Range operation `a_i ← min(a_i, x)`, query sum. Why classic lazy assign fails?
2. Same problem offline with all `x` known — name one alternative to beats.
3. Node stores `mx` but not `se`. Can you still beat in O(1) on a full cover?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: range chmin/chmax (+ add/sum) when forced online; else consider offline.
- Key invariant: second extremum enables O(1) partial update when only maxima change.
- Key formula: if `se < x < mx`, drop maxima to `x` and stop.
- Complexity: amortized ~`O(log² n)`.
- Template to remember: break / beat / recurse trichotomy + push order add→chmin→chmax.

---

---


---

<a id="topic-6"></a>
### 6. Persistent segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** Segtree; path-copying persistence; coordinate compression  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: Segtree; path-copying persistence; coordinate compression

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

Each update creates a **new root**; unchanged subtrees are **shared**. An update copies `O(log n)` nodes. You keep `roots[0..q]` representing versions of the array / frequency tree.

Killer application: **k-th smallest on `[L,R]`** — build persistent frequency tree over compressed values, version `i` = after inserting `a[0..i)`. Then k-th on `[L,R]` = walk on `roots[R] - roots[L]` (subtract counts on the fly) in `O(log V)`.

**Vs merge-sort tree:** persistent usually less memory (`O((n+q) log V)` nodes vs `O(n log n)` full vectors), faster k-th, supports “versions.” Merge-sort tree easier for arbitrary `[lo,hi]` counts without thinking in roots.

**Vs Mo + fenwick:** Mo is offline only; persistent is online-friendly for prefix versions.

---

#### 4. Proof Sketches & Recurrences

Node `{left_ptr, right_ptr, sum}`. Update at leaf index `p` (value coord):
```
new_node = copy(old)
if leaf: sum += delta
else: recurse to child, replace child ptr with new child, sum = L.sum+R.sum
```
`O(log V)` new nodes per update.

Query k-th between two roots `u,v` (v = right prefix, u = left prefix):
```
walk from top:
  left_cnt = v.left.sum - u.left.sum
  if k < left_cnt: go left
  else: k -= left_cnt; go right
```

Space: `O(n log V)` for n insertions.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n log V)` to insert n points
- Per-query / per-operation: `O(log V)` update or k-th / range count
- Total: `O((n+q) log V)`
- Memory: `O((n+q) log V)` nodes (~2 ints + sum each)`

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace persistent_segtree {
struct Persist {
  struct Node {
    int l = 0, r = 0; // child indices
    int sum = 0;
  };
  int N; // value domain [0, N)
  vector<Node> t;
  vector<int> roots; // roots[0]=empty
  Persist() : N(0) { t.reserve(1); t.push_back(Node{}); roots = {0}; }

  explicit Persist(int N_) : N(N_) {
    t.reserve(20 * (N_ + 5));
    t.push_back(Node{});
    roots = {0};
  }

  int copy(int v) {
    t.push_back(t[v]);
    return (int)t.size() - 1;
  }

  int add(int v, int l, int r, int pos, int delta) {
    v = copy(v);
    t[v].sum += delta;
    if (r - l == 1) return v;
    int m = (l + r) >> 1;
    if (pos < m) t[v].l = add(t[v].l, l, m, pos, delta);
    else t[v].r = add(t[v].r, m, r, pos, delta);
    return v;
  }

  // append new version = old version with +delta at pos
  int upd(int root, int pos, int delta) {
    int nr = add(root, 0, N, pos, delta);
    roots.push_back(nr);
    return nr;
  }

  int kth(int u, int v, int k) const { // k-th in v-u, 0-based
    return kth(u, v, 0, N, k);
  }
  int kth(int u, int v, int l, int r, int k) const {
    if (r - l == 1) return l;
    int m = (l + r) >> 1;
    int left = t[t[v].l].sum - t[t[u].l].sum;
    if (k < left) return kth(t[u].l, t[v].l, l, m, k);
    return kth(t[u].r, t[v].r, m, r, k - left);
  }

  int range_sum(int u, int v, int ql, int qr) const {
    return range_sum(u, v, 0, N, ql, qr);
  }
  int range_sum(int u, int v, int l, int r, int ql, int qr) const {
    if (qr <= l || r <= ql) return 0;
    if (ql <= l && r <= qr) return t[v].sum - t[u].sum;
    int m = (l + r) >> 1;
    return range_sum(t[u].l, t[v].l, l, m, ql, qr)
         + range_sum(t[u].r, t[v].r, m, r, ql, qr);
  }
};

// Build for array a[0..n): compress values first
inline vector<int> build_prefix_versions(vector<int> a, Persist& pst, vector<int>& comp) {
  comp = a;
  sort(comp.begin(), comp.end());
  comp.erase(unique(comp.begin(), comp.end()), comp.end());
  for (int& x : a) x = (int)(lower_bound(comp.begin(), comp.end(), x) - comp.begin());
  pst = Persist((int)comp.size());
  vector<int> ver(a.size() + 1);
  ver[0] = pst.roots[0];
  for (int i = 0; i < (int)a.size(); ++i) {
    ver[i + 1] = pst.upd(ver[i], a[i], 1);
  }
  return ver; // ver[i] = after first i elements; kth on [L,R) uses ver[L], ver[R]
}
} // namespace persistent_segtree
```

##### Python 3 Template

```python
# Educational only — expect TLE/MLE on tight CF
class Persist:
    __slots__ = ("N", "l", "r", "s", "roots")

    def __init__(self, N: int):
        self.N = N
        self.l = [0]
        self.r = [0]
        self.s = [0]
        self.roots = [0]

    def _copy(self, v):
        self.l.append(self.l[v])
        self.r.append(self.r[v])
        self.s.append(self.s[v])
        return len(self.s) - 1

    def _add(self, v, L, R, pos, delta):
        v = self._copy(v)
        self.s[v] += delta
        if R - L == 1:
            return v
        m = (L + R) // 2
        if pos < m:
            self.l[v] = self._add(self.l[v], L, m, pos, delta)
        else:
            self.r[v] = self._add(self.r[v], m, R, pos, delta)
        return v

    def upd(self, root, pos, delta):
        nr = self._add(root, 0, self.N, pos, delta)
        self.roots.append(nr)
        return nr
```

---

#### 6. Recognition Trigger Signals & Heuristics

- K-th in subarray `[L,R]` (static).
- “How array looked after update `t`” queries.
- Count of values in `[a,b]` on `[L,R]` via version difference.
- Functional graph / DFS timestamps with historical queries.
- Need true mutable persistence with range lazy — rare and hard; usually avoid.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting compression; `N` too large → MLE.
- Using `roots[R]-roots[L-1]` indexing off-by-one on half-open.
- Not reserving vector capacity → slow realloc.
- Recursing with null child `0` incorrectly (ensure `t[0]` is empty identity).
- Persistent **lazy** without care → exponential copies; avoid unless expert.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Persistent on index axis with point set (historical arrays).
- Persistent + segment tree on time for rollback-like queries.
- Chairman tree = persistent frequency tree nickname.
- Fully persistent vs partial (only update latest) — contests almost always partial.

---

#### 11. Typical Problem Archetypes

1. Standard application: k-th smallest in `[L,R]`.
2. Slightly disguised: count distinct in `[L,R]` with last-occurrence persistent trick.
3. Difficult: persistent + HLD / trees.
4. Very difficult / advanced: persistent Li Chao; persistent lazy (rare).

---

#### 12. Recognition & Identification Drills

1. Static `a[1..n]`; query k-th in `[L,R]`. Merge-sort tree vs persistent — tradeoffs?
2. After each update you must answer queries on **past** versions. Which property do you need?
3. Count values in `[x,y]` on index `[L,R]` with persistent freq tree — how, in one walk?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: versions / k-th on subarrays / rectangle counts via roots.
- Key invariant: path copy O(log); shared unchanged subtrees.
- Key formula: `kth(roots[L], roots[R], k)` on value tree.
- Complexity: `O(log V)` per op, `O(n log V)` memory.
- Template to remember: node pool + copy-on-write add.

---

---


---

<a id="topic-7"></a>
### 7. Dynamic segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Segtree; pointers/indices pool; coordinate ranges up to 1e9/1e18  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Segtree; pointers/indices pool; coordinate ranges up to 1e9/1e18

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

When the index universe is huge (`[1, 1e18]`) but you only touch `q` positions/segments, allocate nodes **on demand**. Same recursive logic; children start null. Memory `O(q log U)` not `O(U)`.

**Vs compression:** if all coordinates known offline, **compress to 1..m** and use dense segtree/fenwick — simpler and faster. Dynamic wins when online (coordinates appear live) or when compression awkward (ranges as indices with splits).

**Vs fenwick:** fenwick needs dense 1..n; dynamic segtree is the sparse analogue for arbitrary associative ops / lazy on large universe.

---

#### 4. Proof Sketches & Recurrences

Each node covers `[l,r]` mid `(l+r)/2` carefully with `int128` or `long long` mid to avoid overflow: `m = l + (r-l)/2`.

On update, if node null create it. Descend only needed side(s). Query skips null (treat as identity).

With lazy: store tag on sparse node; push creates children if needed.

Node count: each update creates ≤ `2 log U` new nodes worst case.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(1)` empty tree
- Per-query / per-operation: `O(log U)` time; `O(log U)` new nodes per update worst-case
- Total: `O(q log U)`
- Memory: `O(q log U)``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Indices up to `1e9`/`1e18`, only `q ≤ 1e5` updates.
- Online coordinates; cannot compress ahead.
- Range add/sum on huge line (coverage of segments).
- “Implicit segtree” / “sparse segtree” wording in blogs.

---

#### 7. Contest WA / TLE / RE Traps

- Mid overflow: `(l+r)/2` for `l,r ~ 1e18` → use `l + (r-l)/2`.
- Inclusive vs half-open confusion on huge ranges.
- Forgetting to create children on push with lazy.
- Using dynamic when offline compression would be trivial.
- MLE from not reserving / leaking nodes on wrong recursion.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Point update / range query sparse.
- Lazy range add / range sum on `[1,1e18]`.
- Dynamic on two axes → “2D dynamic” (next topic) — usually prefer alternatives.
- Persistent + dynamic combined (node pool versions).

---

#### 11. Typical Problem Archetypes

1. Standard application: range coverage on coordinate line `1e9`.
2. Slightly disguised: store segments as +1/-1 on compressed ends — sometimes fenwick enough.
3. Difficult: dynamic lazy + walking for first true predicate.
4. Very difficult / advanced: dynamic Li Chao on `1e18` x-axis.

---

#### 12. Recognition & Identification Drills

1. Online: add point `(x,v)` with `x∈[1,1e18]`; query sum on `[L,R]`. Compress or dynamic?
2. All `x` given in input before queries. Preferred approach?
3. Range add on `[L,R] ⊆ [1,1e18]`, query point. Difference array ideas vs dynamic lazy?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: huge universe, few touches, especially online.
- Key invariant: null child = identity segment; allocate on write.
- Key formula: mid = `l+(r-l)/2`; memory `O(q log U)`.
- Complexity: `O(log U)` per op.
- Template to remember: index pool with `L,R` child ints + lazy optional.

---

---


---

<a id="topic-8"></a>
### 8. 2D segment tree / alternatives

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** Segtree; 2D fenwick; CDQ divide-conquer; offline thinking  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Segtree; 2D fenwick; CDQ divide-conquer; offline thinking

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

Naive 2D segtree: segtree on `x`, each node holds a segtree on `y` of points in that `x`-segment. Build/memory `O(n log² n)` for points; query rectangle `O(log² n)`; updates painful.

**Early ROI is low** because almost every “2D range” CF problem has a better tool:
- **2D fenwick** on compressed grid — if point add + rectangle sum.
- **CDQ / D&C on time** — offline 3D partial order.
- **Sweep + 1D fenwick/segtree** — classic.
- **Merge-sort tree** — static `x` as index, `y` as value.
- **Persistent segtree** — insert by `x`, query `y`-range on version difference.

Use true 2D segtree only when online 2D with ops that don’t fit fenwick and offline is impossible.

---

#### 4. Proof Sketches & Recurrences

For `n` points: outer tree sorts by `x` (or builds on compressed `x`). Node’s inner structure stores all points with that `x`-range sorted by `y` (merge-sort style) or a balanced BST/fenwick of `y`.

Rectangle query `[x1,x2] × [y1,y2]`: O(log n) outer nodes × O(log n) inner = O(log² n).

Memory: if each outer node stores fenwick of size = points in node, total `O(n log n)`.

Segment-of-segment-of-arrays without care → `O(n log² n)` memory easy MLE.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: 2D fenwick `O(nm)` or `O(n log² n)` sparse builds; naive 2D seg `O(n log² n)`
- Per-query / per-operation: `O(log² n)` typical rectangle
- Total: depends; CDQ often `O(n log² n)` offline
- Memory: fenwick2D dense `O(nm)`; sparse `O(n log n)` — 2D seg easy MLE`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Rectangle sum with point updates on grid → 2D fenwick first.
- Offline “add point / query rectangle” → sweep or CDQ.
- Static points, query count in rectangle → merge-sort / persistent / fenwick2D build.
- Online arbitrary 2D range chmin — suffering; rethink problem.

---

#### 7. Contest WA / TLE / RE Traps

- Reaching for 2D segtree when 2D fenwick suffices.
- MLE from `vector` of full inner trees sized to global `m`.
- Off-by-one in rectangle inclusion-exclusion.
- Compressing x/y inconsistently between updates and queries.
- Online 2D with deletes without invertible op → stuck.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- 2D fenwick (invertible).
- Segtree of fenwicks / fenwick of segtrees.
- Persistent segtree as 2D count.
- CDQ for 3-sided/4-sided offline.
- Quadtrees (rare in CF).

---

#### 11. Typical Problem Archetypes

1. Standard application: point add, rectangle sum → 2D fenwick.
2. Slightly disguised: static points rectangle count → compress + fenwick2D or merge-sort tree.
3. Difficult: online 2D with set (non-invertible) — seg of policy BST.
4. Very difficult / advanced: 2D lazy — almost never; reformulate.

---

#### 12. Recognition & Identification Drills

1. `n≤2000` grid, point add, rectangle sum. Best structure?
2. `n≤1e5` static points, many rectangle counts. List two approaches that beat naive 2D segtree coding time.
3. Offline: add point, query “points with `x≤X, y≤Y, time≤T`”. Name the technique family.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: only if simpler 2D fenwick / sweep / CDQ / persistent fail.
- Key invariant: outer canonical x-nodes × inner y-structure.
- Key formula: rectangle = inclusion-exclusion on 2D prefixes when invertible.
- Complexity: usually `O(log² n)` query; watch memory.
- Template to remember: **prefer fenwick2D**; seg-of-fenwicks if forced dynamic.

---

---


---

<a id="topic-9"></a>
### 9. When each variant is actually useful

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier (as decision skill) | **Rating Range:** 1400–2800 | **Frequency:** Very Common (every segtree problem is a choice)  
> **Prerequisites:** Exposure to the variants above; fenwick fluency  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (as decision skill)
- Frequency: Very Common (every segtree problem is a choice)
- Typical CF/ICPC rating range: 1400–2800
- Prerequisites: Exposure to the variants above; fenwick fluency

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

The highest-ROI skill is **not** coding beats — it is picking the lightest structure that fits:

| Need | First reach |
|------|-------------|
| Point add + prefix/range sum | Fenwick |
| Point set + range min/max/GCD | Iterative segtree |
| Range add + range min/sum | Lazy segtree |
| Range set + add + sum | Assign/add lazy |
| Range chmin + sum online | Beats (or offline alt) |
| K-th in subarray static | Persistent / wavelet / MST |
| Huge index universe online | Dynamic segtree |
| Rectangle sum invertible | 2D fenwick / sweep |
| Historical versions | Persistent |

Wrong choice costs more than wrong constant factor.

---

#### 4. Proof Sketches & Recurrences

Decision tree (contest speed):
1. No updates → sparse table / prefix / sort + BS.
2. Updates but prefix-shaped → fenwick (± difference).
3. Point update, range monoid → iterative segtree.
4. Range update uniform → lazy; classify add vs set vs affine vs chmin.
5. Value-index 2D static → MST / persistent / fenwick2D.
6. Versions → persistent.
7. Universe huge online → dynamic.
8. True online 2D non-invertible → rare heavy artillery.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: N/A (decision O(1) with practice)
- Per-query / per-operation: whatever chosen structure
- Total: minimizing implement + debug time is the real objective
- Memory: prefer `O(n)` fenwick/iterative over `O(n log n)` MST when possible`

##### C++17 Template

```cpp
// Not a data structure — a comment block to paste into mental checklist
namespace segtree_choice {
/*
1. Fenwick? (sum/xor/prefix)
2. Sparse table? (static idempotent)
3. Iterative monoid seg? (point upd)
4. Lazy add/set/affine?
5. Persistent / MST? (kth, versions, rectangle count)
6. Dynamic? (1e18 online)
7. Beats? (chmin/chmax online) — last resort early career
8. 2D fenwick/CDQ/sweep before 2D seg
*/
} // namespace segtree_choice
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Ask: invertible? offline? static? need lazy? need 2D? need order-stat?
- If yes to invertible prefix → fenwick.
- If idempotent static RMQ → sparse table.
- If only “subarray k-th” → persistent, not general lazy.
- If chmin → confirm online necessity before beats.

---

#### 7. Contest WA / TLE / RE Traps

- Implementing lazy when fenwick difference works.
- Beats for a problem that is offline-friendly.
- 2D segtree as first idea → MLE/TLE/code bomb.
- Persistent when Mo + fenwick is enough offline.
- Dynamic when all coords offline-compressible.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- ICPC team: one member owns “lazy kitchen sink,” another “persistent k-th,” another “offline CDQ” — divide recognition.

---

#### 11. Typical Problem Archetypes

1. Standard application: read ops list → classify into table row.
2. Slightly disguised: tree path queries → HLD + (usually iterative/lazy) seg.
3. Difficult: mix version queries + range updates → rethink (often offline).
4. Very difficult / advanced: force beats + HLD — check constraints twice.

---

#### 12. Recognition & Identification Drills

1. Ops: range add, point query. Lightest tool?
2. Ops: point set, range matrix product. Why fenwick fails?
3. Ops: range chmin, range sum, `n=1e5`, online. What do you implement at 2600 vs at 1800 (alternative)?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: every time before coding a segtree.
- Key invariant: lightest correct tool wins.
- Key formula: fenwick ⊂ iterative ⊂ lazy ⊂ beats; MST ≈ persistent for static order-stat; 2D fenwick ≫ 2D seg.
- Complexity: pick structure whose complexity matches constraints with room.
- Template to remember: the decision table in B.

---

---


---

<a id="topic-10"></a>
### 10. Typical CF patterns

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2600 | **Frequency:** Very Common  
> **Prerequisites:** All core variants; constructive reading of CF statements  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2600
- Prerequisites: All core variants; constructive reading of CF statements

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

A Segment Tree is a full binary tree designed to perform range queries and range modifications on an underlying array in $\mathcal{O}(\log N)$ time by maintaining monoid aggregates $(S, \oplus, e)$.

##### Fundamental Theorems & Invariants

- **Monoid Property:** Range aggregation requires an associative binary operator $\oplus$ with an identity element $e$ such that $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ and $a \oplus e = a$.
- **Canonical Segment Cover:** Any arbitrary contiguous subarray $[L, R]$ is uniquely partitioned into at most $2 \lceil \log_2 N \rceil$ disjoint canonical segment tree nodes.
- **Lazy Propagation Postulate:** Range updates defer evaluation to subtrees by storing pending transformation tags in ancestors, pushing them to child nodes only when deeper queries/updates traverse down.
- **Segment Tree Beats Invariant:** Range $\text{chmin}(v)$ maintains the maximum and strict second maximum ($max_1, max_2$) in each node. If $max_2 < v < max_1$, the update acts as a uniform lazy subtraction on the count of maximums in $\mathcal{O}(\log N)$ amortized time.

##### Algorithmic Execution Blueprint

1. **Tree Allocation:** Allocate $4N$ nodes for recursive pointers or $2N$ nodes for iterative bottom-up trees where leaves reside at indices $N \dots 2N-1$.
2. **Merge Operation:** Define `pull(node)` as `tree[node] = merge(tree[2*node], tree[2*node+1])`.
3. **Pushing Lazy Tags:** Before traversing into children of `node`, apply `tree[node].lazy` to `2*node` and `2*node+1`, then clear `tree[node].lazy`.
4. **Range Query:** If current node interval $[l, r] \subseteq [L, R]$, return `tree[node]`. If $[l, r] \cap [L, R] = \emptyset$, return identity $e$. Otherwise push lazy tag, split query at $mid$, and merge child results.

##### Closed-Form Invariant Equations

$$\text{Query}([L, R]) = \bigoplus_{i \in \text{canonical}([L, R])} \text{Node}[i].\text{val}, \quad |\text{canonical}([L, R])| \le 2\lceil\log_2 N\rceil$$

##### Structural Edge Cases & Assumptions

- Ensure lazy tag composition is strictly associative: when assigning and adding, assignment overrides pending addition.
- For Range Assign, lazy tag empty state cannot be $0$ if $0$ is a valid value; use an explicit `has_lazy` boolean flag or $-1$/infinity sentinel.
- Iterative segment trees require $1$-based indexing and powers-of-two padding when performing non-commutative queries.

---

#### 3. Core Intuition & Problem Framing

CF does not say “use a segment tree.” It says:
- “maintain array under operations…”
- “for each query compute …”
- “online / you must answer before next…”

Pattern library (recognition → structure):

1. **HLD / Euler tour** + segtree — path/subtree aggregates.
2. **Kadane monoid** — max subarray under point updates.
3. **First position / walking** — `max_right` on sums or mins.
4. **Difference + fenwick** disguised as range add.
5. **Time-segment tree + DSU rollback** — offline dynamic connectivity.
6. **Persistent k-th** — “mex / k-th / count ≤x on subarray.”
7. **Lazy assign colors** — paint subarrays, query sums of values.
8. **Merge-sort tree** — static 2D count on array indices.
9. **Li Chao** (segtree of lines) — DP CHT geometric; related family.
10. **Beats** — rare Div.1 chmin statements.

---

#### 4. Proof Sketches & Recurrences

Map statement nouns to axes:
- **Index axis** (array position / Euler time / HLD position)
- **Value axis** (compressed for order-stat)
- **Time axis** (versions / offline segments)

Most CF segtree problems are 1–2 axes. Three axes → CDQ or heavy 2D.

Complexity target: usually `O((n+q) log n)` or `log²`; `log³` risky at 1e5 unless light.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: tour `O(n)`; HLD `O(n)`; structure as usual
- Per-query / per-operation: `O(log n)` to `O(log² n)` typical CF
- Total: design for `≤ 2e5` ops × `log`/`log²`
- Memory: stay within 256MB — avoid `O(n log n)` vectors unless needed`

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace cf_patterns {
// Max subarray (Kadane) monoid for point updates — classic CF pattern
struct Kadane {
  long long tot, pref, suf, best;
  static Kadane e() {
    // identity for merge: length-0; use careful sentinel
    return {0, (long long)-4e18, (long long)-4e18, (long long)-4e18};
  }
  static Kadane leaf(long long x) { return {x, x, x, x}; }
};
inline Kadane op(Kadane a, Kadane b) {
  Kadane c;
  c.tot = a.tot + b.tot;
  c.pref = max(a.pref, a.tot + b.pref);
  c.suf = max(b.suf, b.tot + a.suf);
  c.best = max({a.best, b.best, a.suf + b.pref});
  return c;
}

// Euler tour stubs — pair with any segtree on [tin, tout)
struct Euler {
  int n, timer = 0;
  vector<vector<int>> g;
  vector<int> tin, tout, flat;
  Euler(int n_) : n(n_), g(n_), tin(n_), tout(n_) {}
  void add_edge(int u, int v) { g[u].push_back(v); g[v].push_back(u); }
  void dfs(int v, int p) {
    tin[v] = timer++;
    flat.push_back(v);
    for (int to : g[v]) if (to != p) dfs(to, v);
    tout[v] = timer;
  }
};
} // namespace cf_patterns
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Subtree of rooted tree” → Euler `[in,out)` + fenwick/segtree.
- “Path u–v” → HLD or Euler+LCA tricks depending on op.
- “Delete edges for a period, answer connectivity” → time segtree.
- “K-th favorite number in range” → persistent.
- “Replace all >x by x on range” → beats keyword.
- Multiple paints of entire ranges → lazy set.

---

#### 7. Contest WA / TLE / RE Traps

- Euler half-open `[tin, tout)` vs inclusive.
- HLD wrong `op` order on path (non-commutative).
- Using segtree for static RMQ (sparse table faster/simpler).
- Offline problem solved online with persistent for no reason.
- Ignoring 64-bit sums on Kadane / paint problems.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-52C | Circular RMQ | 2200 | Segment Tree, Lazy Propagation | Range add with range min queries on circular arrays split into two intervals. | [Solve Problem](https://codeforces.com/contest/52/problem/C) |
| Codeforces | CF-438D | The Child and Sequence | 2300 | Segment Tree, Amortized Analysis | Modulo updates decrease value by at least half; prune segments with max < mod. | [Solve Problem](https://codeforces.com/contest/438/problem/D) |
| Codeforces | CF-840D | Destiny | 2600 | Persistent SegTree, Order Statistics | Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k. | [Solve Problem](https://codeforces.com/contest/840/problem/D) |
| Codeforces | CF-911G | Mass Change Queries | 2400 | Dynamic SegTree, Segment Tree Merging | Dynamic segment tree node merging for each value from 1 to 100. | [Solve Problem](https://codeforces.com/contest/911/problem/G) |
| CSES | CSES-1736 | Polynomial Queries | 2100 | Lazy SegTree, Range Updates | Lazy segment tree maintaining arithmetic progression tags (base and slope). | [Solve Problem](https://cses.fi/problemset/task/1736) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Segment Tree Core & Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html)
- **[Codeforces]** [Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)](https://codeforces.com/blog/entry/57319)
- **[USACO Guide]** [USACO Guide: Range Updates with Lazy Propagation](https://usaco.guide/plat/lazy-segtree)
- **[YouKn0wWho]** [YouKn0wWho Academy: Persistent Segment Tree](https://youkn0wwho.academy/topic-list#persistent-segtree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- CF Div.2 C/D: iterative / fenwick.
- Div.2 E / Div.1 A–B: lazy, Euler, simple HLD.
- Div.1 C–D: persistent, time segtree, rare beats.
- Educational rounds: pure lazy drills.

---

#### 11. Typical Problem Archetypes

1. Standard application: range sum updates on array (lazy or fenwick).
2. Slightly disguised: subtree add, vertex query via Euler + fenwick.
3. Difficult: path queries with HLD + lazy; or persistent distinct-count.
4. Very difficult / advanced: offline dynamic connectivity; beats on arrays; Li Chao DP.

---

#### 12. Recognition & Identification Drills

1. Tree rooted at 1; add `x` on subtree of `v`; query value at `u`. Structure sketch?
2. Array; point updates; query maximum subarray sum on full array after each update. Monoid?
3. Queries: k-th smallest on `[L,R]` interleaved with no updates. Which two structures are standard?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: map CF wording → axis → lightest DS.
- Key invariant: tour/HLD only remap indices; DS stays 1D.
- Key formula: subtree = `[tin,tout)`; k-th = persistent walk; paint = lazy set.
- Complexity: aim `(n+q) log` / `log²`.
- Template to remember: Kadane monoid + Euler tin/tout + decision table.

---

---


---
