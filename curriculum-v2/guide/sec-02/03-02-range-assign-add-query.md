# Range assign/add/query

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Lazy propagation; tag composition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Lazy propagation; tag composition

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

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: `O(log n)`
- Total: `O((n+q) log n)`
- Memory: `O(n)``

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Statement lists both “paint range to x” and “increment range” plus sum/min queries.
- “Reset segment then keep adding” stories (timelines, coverage with rebuild).
- Need length-aware aggregates under both ops.
- If only assign (no add): single set-tag suffices.
- If only add: pure add-tag; don’t overbuild.

---

## 7. Contest WA / TLE / RE Traps

- Assign not clearing pending add (or vice versa).
- Double-counting: set tag stores `set_val` and also `add` inconsistently.
- `len` wrong on partial nodes after bad pull.
- Composition: “new set should wipe old add” forgotten → WA on mixed ops.
- Min/max not updated on add.
- Using int for sum when `x * len` overflows → use `int64`.

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

- Assign + sum only.
- Assign + add + min/max/sum (full).
- Affine `a*x+b` with composition `(a1,b1)∘(a2,b2)=(a1*a2, a1*b2+b1)`.
- Modulo arithmetic on sums.
- History: persistent lazy is rarely needed; usually offline or beats instead.

---

## 11. Typical Problem Archetypes

1. Standard: paint / increment / sum.
2. Slightly disguised: “set range to 0 then add 1 on subranges” coverage rebuilds.
3. Difficult: maintain sum of `f(a_i)` under assign/add when `f` is polynomial — store power sums.
4. Very difficult: assign/add plus chmin (forces beats or casesplit).

---

## 12. Recognition & Identification Drills

1. Support range set, range add, range sum. Sketch tag composition when set follows add.
2. Same ops but query “number of zeros in range”. What extra info do nodes store under assign/add?
3. Only range set + range sum — can you use a fenwick? When yes/no?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: mixed paint + increment + aggregates.
- Key invariant: set dominates; add stacks; `sum`/`mn`/`mx` always consistent with tags.
- Key formula: set ⇒ `sum=x*len`; add ⇒ `sum+=d*len`.
- Complexity: `O(log n)` per op.
- Template to remember: two-field tag `(set?, add)` with wipe-on-set.

---

---
