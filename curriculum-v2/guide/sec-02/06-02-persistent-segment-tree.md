# Persistent segment tree

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** Segtree; path-copying persistence; coordinate compression  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: Segtree; path-copying persistence; coordinate compression

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

Each update creates a **new root**; unchanged subtrees are **shared**. An update copies `O(log n)` nodes. You keep `roots[0..q]` representing versions of the array / frequency tree.

Killer application: **k-th smallest on `[L,R]`** — build persistent frequency tree over compressed values, version `i` = after inserting `a[0..i)`. Then k-th on `[L,R]` = walk on `roots[R] - roots[L]` (subtract counts on the fly) in `O(log V)`.

**Vs merge-sort tree:** persistent usually less memory (`O((n+q) log V)` nodes vs `O(n log n)` full vectors), faster k-th, supports “versions.” Merge-sort tree easier for arbitrary `[lo,hi]` counts without thinking in roots.

**Vs Mo + fenwick:** Mo is offline only; persistent is online-friendly for prefix versions.

---

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n log V)` to insert n points
- Per-query / per-operation: `O(log V)` update or k-th / range count
- Total: `O((n+q) log V)`
- Memory: `O((n+q) log V)` nodes (~2 ints + sum each)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- K-th in subarray `[L,R]` (static).
- “How array looked after update `t`” queries.
- Count of values in `[a,b]` on `[L,R]` via version difference.
- Functional graph / DFS timestamps with historical queries.
- Need true mutable persistence with range lazy — rare and hard; usually avoid.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting compression; `N` too large → MLE.
- Using `roots[R]-roots[L-1]` indexing off-by-one on half-open.
- Not reserving vector capacity → slow realloc.
- Recursing with null child `0` incorrectly (ensure `t[0]` is empty identity).
- Persistent **lazy** without care → exponential copies; avoid unless expert.

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

- Persistent on index axis with point set (historical arrays).
- Persistent + segment tree on time for rollback-like queries.
- Chairman tree = persistent frequency tree nickname.
- Fully persistent vs partial (only update latest) — contests almost always partial.

---

## 11. Typical Problem Archetypes

1. Standard application: k-th smallest in `[L,R]`.
2. Slightly disguised: count distinct in `[L,R]` with last-occurrence persistent trick.
3. Difficult: persistent + HLD / trees.
4. Very difficult / advanced: persistent Li Chao; persistent lazy (rare).

---

## 12. Recognition & Identification Drills

1. Static `a[1..n]`; query k-th in `[L,R]`. Merge-sort tree vs persistent — tradeoffs?
2. After each update you must answer queries on **past** versions. Which property do you need?
3. Count values in `[x,y]` on index `[L,R]` with persistent freq tree — how, in one walk?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: versions / k-th on subarrays / rectangle counts via roots.
- Key invariant: path copy O(log); shared unchanged subtrees.
- Key formula: `kth(roots[L], roots[R], k)` on value tree.
- Complexity: `O(log V)` per op, `O(n log V)` memory.
- Template to remember: node pool + copy-on-write add.

---

---
