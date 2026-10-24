# Ordered Statistics (PBDS / Fenwick / Treap)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Coordinate compression, Fenwick or BST; GCC PBDS extension  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Coordinate compression, Fenwick or BST; GCC PBDS extension

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

Need **rank** (how many \(< x\)) and **select** (k-th smallest) under online inserts/erases. Three contest tools: (1) **GNU PBDS** `tree` with `order_of_key` / `find_by_order` — shortest; (2) **Fenwick/segtree on compressed values** as frequency array — safest portable; (3) **treap** when you also need splits/aggregates. Prefer PBDS or Fenwick over rolling your own BST for pure order stats.

---

## 4. Proof Sketches & Recurrences

Compress values to \(1..m\). Fenwick `add(rank(x),+1)` on insert; `order = sumPrefix(rank(x)-1)`; k-th = Fenwick `lower_bound(k)`. PBDS maintains a BST augmented with subtree sizes — same select/rank in \(O(\log n)\). Duplicates: store `{value, unique id}` pairs in PBDS; Fenwick naturally counts multiplicity.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) compression
- Per-query / per-operation: \(O(\log n)\)
- Total: \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// Headers (file scope):
// #include <ext/pb_ds/assoc_container.hpp>
// #include <ext/pb_ds/tree_policy.hpp>

namespace ordstats {
using namespace __gnu_pbds;

template <class T>
using ordered_set = tree<T, null_type, less<T>, rb_tree_tag,
                         tree_order_statistics_node_update>;
// ordered_set<pair<int,int>> st;
// st.insert({x, id});
// st.order_of_key({x, -1});           // count strictly < x
// *st.find_by_order(k);               // k-th (0-indexed)

// Portable Fenwick frequency version (values compressed to 1..m).
// Uses fenwick::BIT from 05-a-fenwick-sparse-tables-cartesian.md.
struct CompressedOrder {
    vector<int> coords;
    fenwick::BIT bit;
    void init(vector<int> all) {
        coords = all;
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());
        bit = fenwick::BIT((int)coords.size());
    }
    int rid(int x) const { // 1-indexed rank
        return (int)(lower_bound(coords.begin(), coords.end(), x) - coords.begin()) + 1;
    }
    void insert(int x) { bit.add(rid(x), +1); }
    void erase(int x) { bit.add(rid(x), -1); }
    int order_of_key(int x) const { // # strictly < x
        int r = (int)(lower_bound(coords.begin(), coords.end(), x) - coords.begin());
        return (int)bit.sumPrefix(r);
    }
    int find_by_order(int k) const { // 0-indexed; needs k in range
        int idx = bit.lower_bound(k + 1);
        return coords[idx - 1];
    }
};
} // namespace ordstats
```

### Python 3 Template

```python
# Assume BIT from Section 05a; coords = sorted unique values
def rid(coords, x):
    from bisect import bisect_left
    return bisect_left(coords, x) + 1

# insert: bit.add(rid(coords, x), +1)
# order_of_key: bit.sum_prefix(bisect_left(coords, x))
# kth: bit.lower_bound(k+1) -> coords[idx-1]
```

---

## 6. Recognition Trigger Signals & Heuristics

- “k-th smallest online,” “count elements \(< x\)”
- Inversions with updates; dynamic median
- Multiset + rank queries
- Sliding window k-th (Fenwick / PBDS / policy two-heaps variants)

---

## 7. Contest WA / TLE / RE Traps

- PBDS `less` vs `less_equal` for multisets — prefer `pair<value,id>` with `less`
- `find_by_order` is 0-indexed; off-by-one vs problem statements
- Fenwick erase without checking presence → negative freqs break `lower_bound`
- Forgetting to compress all query values that may appear as keys

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

- Dynamic median (two ordered multisets / PBDS)
- Count inversions online
- Order stats on segtree merges (merge-sort tree — different section family)
- Implicit treap ranks by position not value

---

## 11. Typical Problem Archetypes

1. Standard application: online k-th / rank in a multiset
2. Slightly disguised: inversions; “how many in \([L,R]\)” with Fenwick of freqs
3. Difficult: k-th on path / subtree (HLD + BIT / persistent segtree)
4. Very difficult / advanced: with range updates on values (heavier structures)

---

## 12. Recognition & Identification Drills

1. Maintain a multiset; answer “k-th smallest” after inserts/deletes.
2. Stream of numbers; after each insert print number of inversions so far.
3. Compressed values; queries “count in \([L,R]\) currently present.”

---

## 13. Fast-Lookup Cheat Sheet

- When to use: online rank / select
- Key invariant: augmented sizes or frequency prefix sums
- Key formula: `order_of_key` / `find_by_order` or Fenwick prefix + binary lift
- Complexity: \(O(\log n)\)
- Template to remember: PBDS pair-id OR Fenwick on ranks

---

## 10. Link-cut tree

---
