# When each variant is actually useful

> **Section:** §02 Segment Trees & Range Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier (as decision skill) | **Rating Range:** 1400–2800 | **Frequency:** Very Common (every segtree problem is a choice)  
> **Prerequisites:** Exposure to the variants above; fenwick fluency  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (as decision skill)
- Frequency: Very Common (every segtree problem is a choice)
- Typical CF/ICPC rating range: 1400–2800
- Prerequisites: Exposure to the variants above; fenwick fluency

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

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: N/A (decision O(1) with practice)
- Per-query / per-operation: whatever chosen structure
- Total: minimizing implement + debug time is the real objective
- Memory: prefer `O(n)` fenwick/iterative over `O(n log n)` MST when possible`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Ask: invertible? offline? static? need lazy? need 2D? need order-stat?
- If yes to invertible prefix → fenwick.
- If idempotent static RMQ → sparse table.
- If only “subarray k-th” → persistent, not general lazy.
- If chmin → confirm online necessity before beats.

---

## 7. Contest WA / TLE / RE Traps

- Implementing lazy when fenwick difference works.
- Beats for a problem that is offline-friendly.
- 2D segtree as first idea → MLE/TLE/code bomb.
- Persistent when Mo + fenwick is enough offline.
- Dynamic when all coords offline-compressible.

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

- ICPC team: one member owns “lazy kitchen sink,” another “persistent k-th,” another “offline CDQ” — divide recognition.

---

## 11. Typical Problem Archetypes

1. Standard application: read ops list → classify into table row.
2. Slightly disguised: tree path queries → HLD + (usually iterative/lazy) seg.
3. Difficult: mix version queries + range updates → rethink (often offline).
4. Very difficult / advanced: force beats + HLD — check constraints twice.

---

## 12. Recognition & Identification Drills

1. Ops: range add, point query. Lightest tool?
2. Ops: point set, range matrix product. Why fenwick fails?
3. Ops: range chmin, range sum, `n=1e5`, online. What do you implement at 2600 vs at 1800 (alternative)?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: every time before coding a segtree.
- Key invariant: lightest correct tool wins.
- Key formula: fenwick ⊂ iterative ⊂ lazy ⊂ beats; MST ≈ persistent for static order-stat; 2D fenwick ≫ 2D seg.
- Complexity: pick structure whose complexity matches constraints with room.
- Template to remember: the decision table in B.

---

---
