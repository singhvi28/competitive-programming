# 10. Typical CF patterns

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2600 | **Frequency:** Very Common  
> **Prerequisites:** All core variants; constructive reading of CF statements  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2600
- Prerequisites: All core variants; constructive reading of CF statements

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

## 4. Proof Sketches & Recurrences

Map statement nouns to axes:
- **Index axis** (array position / Euler time / HLD position)
- **Value axis** (compressed for order-stat)
- **Time axis** (versions / offline segments)

Most CF segtree problems are 1–2 axes. Three axes → CDQ or heavy 2D.

Complexity target: usually `O((n+q) log n)` or `log²`; `log³` risky at 1e5 unless light.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: tour `O(n)`; HLD `O(n)`; structure as usual
- Per-query / per-operation: `O(log n)` to `O(log² n)` typical CF
- Total: design for `≤ 2e5` ops × `log`/`log²`
- Memory: stay within 256MB — avoid `O(n log n)` vectors unless needed`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- “Subtree of rooted tree” → Euler `[in,out)` + fenwick/segtree.
- “Path u–v” → HLD or Euler+LCA tricks depending on op.
- “Delete edges for a period, answer connectivity” → time segtree.
- “K-th favorite number in range” → persistent.
- “Replace all >x by x on range” → beats keyword.
- Multiple paints of entire ranges → lazy set.

---

## 7. Contest WA / TLE / RE Traps

- Euler half-open `[tin, tout)` vs inclusive.
- HLD wrong `op` order on path (non-commutative).
- Using segtree for static RMQ (sparse table faster/simpler).
- Offline problem solved online with persistent for no reason.
- Ignoring 64-bit sums on Kadane / paint problems.

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

- CF Div.2 C/D: iterative / fenwick.
- Div.2 E / Div.1 A–B: lazy, Euler, simple HLD.
- Div.1 C–D: persistent, time segtree, rare beats.
- Educational rounds: pure lazy drills.

---

## 11. Typical Problem Archetypes

1. Standard application: range sum updates on array (lazy or fenwick).
2. Slightly disguised: subtree add, vertex query via Euler + fenwick.
3. Difficult: path queries with HLD + lazy; or persistent distinct-count.
4. Very difficult / advanced: offline dynamic connectivity; beats on arrays; Li Chao DP.

---

## 12. Recognition & Identification Drills

1. Tree rooted at 1; add `x` on subtree of `v`; query value at `u`. Structure sketch?
2. Array; point updates; query maximum subarray sum on full array after each update. Monoid?
3. Queries: k-th smallest on `[L,R]` interleaved with no updates. Which two structures are standard?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: map CF wording → axis → lightest DS.
- Key invariant: tour/HLD only remap indices; DS stays 1D.
- Key formula: subtree = `[tin,tout)`; k-th = persistent walk; paint = lazy set.
- Complexity: aim `(n+q) log` / `log²`.
- Template to remember: Kadane monoid + Euler tin/tout + decision table.

---

---
