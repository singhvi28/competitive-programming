# 2. Disjoint Sparse Table

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2500 | **Frequency:** Rare  
> **Prerequisites:** Sparse table, associative ops (semigroup), bit partitioning of ranges  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Sparse table, associative ops (semigroup), bit partitioning of ranges

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

## 3. Core Intuition & Problem Framing

Classic ST overlaps two blocks — fatal for non-idempotent ops like `+` or matrix multiply. A **disjoint** sparse table precomputes, for each dyadic “block boundary,” prefixes to the left and suffixes to the right so any range splits into **exactly two adjacent** precomputed halves meeting at a power-of-two aligned cut. Associativity alone suffices; idempotence not required. Still static.

---

## 4. Proof Sketches & Recurrences

Fix size \(n' = 2^{\lceil\log_2 n\rceil}\). For each level \(k\) with block length \(2^k\), at every boundary multiple of \(2^k\), store leftward suffixes and rightward prefixes under `op`. Query \([L,R]\): let \(k = \mathrm{msb}(L\oplus R)\) (highest differing bit); answer is `op(left_prefix, right_prefix)` from that level’s cut — two disjoint halves. Build \(O(n\log n)\), query \(O(1)\) op applications.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) applications of `op`
- Per-query / per-operation: \(O(1)\) applications of `op`
- Total: \(O(n\log n + q)\)
- Memory: \(O(n\log n)\)`

### C++17 Template

```cpp
namespace disjoint_st {
template <class T, class F>
struct DisjointSparseTable {
    int n, levels;
    vector<vector<T>> pref; // pref[k][i] = fold in direction toward boundary
    F op;
    T id; // unused if queries always nonempty; keep for clarity

    DisjointSparseTable(vector<T> a, F op_, T id_ = T{})
        : n((int)a.size()), op(op_), id(id_) {
        if (n == 0) { levels = 0; return; }
        levels = 32 - __builtin_clz(n);
        int N = 1 << levels;
        a.resize(N, id);
        pref.assign(levels + 1, vector<T>(N, id));
        pref[0] = a;
        for (int k = 1; k <= levels; ++k) {
            int len = 1 << k;
            for (int base = 0; base < N; base += len) {
                int mid = base + (len >> 1);
                pref[k][mid - 1] = a[mid - 1];
                for (int i = mid - 2; i >= base; --i)
                    pref[k][i] = op(a[i], pref[k][i + 1]);
                pref[k][mid] = a[mid];
                for (int i = mid + 1; i < base + len; ++i)
                    pref[k][i] = op(pref[k][i - 1], a[i]);
            }
        }
    }
    T query(int l, int r) const { // inclusive, nonempty
        if (l == r) return pref[0][l];
        int k = 32 - __builtin_clz(l ^ r); // msb index of l^r
        return op(pref[k][l], pref[k][r]);
    }
};
} // namespace disjoint_st
```

---

## 6. Recognition Trigger Signals & Heuristics

- Static array; associative op; want \(O(1)\) queries without segtree
- Matrix product on subarrays, non-idempotent semigroups
- You already know ST and someone forbids overlapping merges

---

## 7. Contest WA / TLE / RE Traps

- Using classic overlapping ST for `+` / matrix product
- Empty ranges / \(l>r\) not handled
- Incorrect MSB of `l^r` (`__builtin_clz` width assumptions)
- Padding with wrong identity for the semigroup

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

## 10. Algorithmic Variants & Advanced Extensions

- Sum / product / affine composition / small matrix mul
- Fallback: iterative segtree \(O(\log n)\) query is almost always acceptable — DST is micro-opt / elegance

---

## 11. Typical Problem Archetypes

1. Standard application: static range sum with \(O(1)\) (usually Fenwick/prefix better)
2. Slightly disguised: static range matrix product
3. Difficult: associative custom merge too fat for segtree constants (rare)
4. Very difficult / advanced: combine with monoid ideas in research-style tasks

---

## 12. Recognition & Identification Drills

1. Static array of \(2\times 2\) matrices; product on subarrays; \(q\) large.
2. Explain why classic sparse table fails for range sum with the two-block trick.
3. Same queries solvable by segtree — when would DST be worth coding?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: static associative non-idempotent \(O(1)\) queries (rare)
- Key invariant: range ↔ two disjoint halves at `msb(l^r)` cut
- Key formula: `op(pref[k][l], pref[k][r])`
- Complexity: \(O(n\log n)\) build, \(O(1)\) query
- Template to remember: build inward prefixes at each dyadic mid; query via `l^r`

---

## 5. Cartesian tree

---
