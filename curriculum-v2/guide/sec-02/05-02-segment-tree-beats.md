# 5. Segment tree beats

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** Niche | **Rating Range:** 2400–3200 | **Frequency:** Rare  
> **Prerequisites:** Lazy segtree fluency; chmin/chmax intuition; amortized analysis comfort  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3200
- Prerequisites: Lazy segtree fluency; chmin/chmax intuition; amortized analysis comfort

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

Classic lazy fails for **range chmin** (`a_i ← min(a_i, x)`) because the update is not a uniform affine tag on arbitrary child values — unless the whole segment’s maximum is `≤ x` (tag is no-op) or you know enough structure to update aggregates in O(1).

**Beats** stores at each node: `mx`, `se` (strict second max), `mx_cnt`, often `sum`, and maybe `mn`/`se_min` for chmax. On chmin(`x`):
- If `mx ≤ x`: break (nothing changes).
- If `se < x < mx`: you can **beat** the node — only the maximums drop to `x`; update `sum`, `mx`, tags; **do not descend**.
- Else (`x ≤ se`): must push and recurse both children.

Amortized potential on “number of distinct values / tight maxima” gives **O(log² n)** per op typical (sometimes O(log n) amortized depending on proof). Extremely powerful on the right problem; **terrible early ROI** — learn after lazy mastery, ignore until ~2400+.

---

## 4. Proof Sketches & Recurrences

Node invariants: `mx` = maximum; `se` = max among strictly `< mx` (or `-inf`); `cnt` = count of `mx`.

Chmin tag `x` when `se < x < mx`:
```
sum -= (mx - x) * cnt
mx = x
```
Push chmin to children with same rules.

Potential Φ = Σ_nodes (number of “distinct maximum chains”) — each failed beat (recurse) decreases global potential enough to amortize. Practical bound used in contests: treat as `O(log² n)` per update/query.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n)`
- Per-query / per-operation: amortized `O(log² n)` typical for chmin/chmax/add/sum suite
- Total: ~`O(q log² n)` 
- Memory: `O(n)` with large constant (~10–20 fields/node)`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Range `a_i = min(a_i, x)` / `max(a_i, x)` plus sum or max queries.
- “Cap all values in range above threshold” repeatedly.
- Not plain assign/add; not invertible fenwick.
- If offline and only chmin + sum, sometimes CDQ / divide-conquer on time beats beats — consider alternatives first.

---

## 7. Contest WA / TLE / RE Traps

- Wrong second-max after partial beat.
- Not handling all-equal segment (`se = -inf`) when chmin collapses.
- Forgetting to push add before chmin tags (tag order).
- Using beats when assign would suffice.
- TLE from missing break `mx ≤ x` → descends like O(n).

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

- Chmin + sum only (lighter node).
- Chmin + chmax + add + sum (full “beats”).
- Historic beats on CF (jiupeng / angel) tutorials — stick to one verified template.
- Alternative: sqrt decomposition on values for some chmin problems.

---

## 11. Typical Problem Archetypes

1. Standard application: range chmin, query sum.
2. Slightly disguised: repeatedly replace `a_i` with `min(a_i, x)` offline online mix.
3. Difficult: chmin/chmax/add together with max and sum queries.
4. Very difficult / advanced: beats on trees via HLD (constants brutal).

---

## 12. Recognition & Identification Drills

1. Range operation `a_i ← min(a_i, x)`, query sum. Why classic lazy assign fails?
2. Same problem offline with all `x` known — name one alternative to beats.
3. Node stores `mx` but not `se`. Can you still beat in O(1) on a full cover?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: range chmin/chmax (+ add/sum) when forced online; else consider offline.
- Key invariant: second extremum enables O(1) partial update when only maxima change.
- Key formula: if `se < x < mx`, drop maxima to `x` and stop.
- Complexity: amortized ~`O(log² n)`.
- Template to remember: break / beat / recurse trichotomy + push order add→chmin→chmax.

---

---
