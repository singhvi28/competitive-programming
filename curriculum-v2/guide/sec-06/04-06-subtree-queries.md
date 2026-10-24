# Subtree Queries

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Euler tour, Fenwick / segment tree  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Euler tour, Fenwick / segment tree

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

## 3. Core Intuition & Problem Framing

After Euler flattening, subtree sum = range sum; subtree add = range add. Point update + subtree query, or subtree update + point query, are classic Fenwick duals. Path queries are **not** subtree queries — route those to lifting, HLD, or difference-on-tree (`add u,v,lca`).

---

## 4. Proof Sketches & Recurrences

Place node value at index `tin[v]`. Subtree sum = `query(tin[v], tout[v])`. Subtree add \(+x\): range update on that segment. Point query after subtree adds: Fenwick difference — `add(tin[v], x); add(tout[v]+1, -x)`, query prefix `tin[u]`.

Path sum root↔u: if you store values on Fenwick at `tin` and use inclusion with LCA carefully, or maintain `pref[u] = pref[parent]+val[u]` with Euler tricks. Prefer explicit tools (HLD / lifting) for arbitrary paths.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) tour + \(O(n)\) or \(O(n\log n)\) to load values
- Per-query / per-operation: \(O(\log n)\) Fenwick / segtree
- Total: \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — Euler + Fenwick subtree sum / point update
namespace subq {
constexpr int N = 200005;
int n, timer, tin[N], tout[N];
vector<int> g[N];
long long bit[N];

void badd(int i, long long x) {
    for (; i <= n; i += i & -i) bit[i] += x;
}
long long bsum(int i) {
    long long r = 0;
    for (; i > 0; i -= i & -i) r += bit[i];
    return r;
}
long long brange(int l, int r) { return bsum(r) - bsum(l - 1); }

void dfs(int v, int p) {
    tin[v] = ++timer;
    for (int to : g[v]) if (to != p) dfs(to, v);
    tout[v] = timer;
}

void build(int root = 1) {
    timer = 0;
    dfs(root, 0);
    fill(bit, bit + n + 1, 0);
}

void point_set_delta(int v, long long delta) { badd(tin[v], delta); }
long long subtree_sum(int v) { return brange(tin[v], tout[v]); }

// subtree add + point query (difference Fenwick)
void subtree_add(int v, long long x) {
    badd(tin[v], x);
    if (tout[v] + 1 <= n) badd(tout[v] + 1, -x);
}
long long point_query(int v) { return bsum(tin[v]); }
} // namespace subq
```

### Python 3 Template

```python
# Python 3.11+ — Fenwick subtree ops
class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.b = [0] * (n + 1)
    def add(self, i: int, x: int) -> None:
        while i <= self.n:
            self.b[i] += x
            i += i & -i
    def sum(self, i: int) -> int:
        r = 0
        while i > 0:
            r += self.b[i]
            i -= i & -i
        return r
    def range(self, l: int, r: int) -> int:
        return self.sum(r) - self.sum(l - 1)
```

---

## 6. Recognition Trigger Signals & Heuristics

- Subtree sum / min / gcd after updates
- “Tax in region of capital’s subtree”
- Difference array: add on subtree ↔ add at `tin`, subtract at `tout+1`
- Rooted tree + operations “on v and descendants”

---

## 7. Contest WA / TLE / RE Traps

- Updating `v`’s value at index `v` instead of `tin[v]`
- Subtree add without complementary `-x` at `tout+1`
- Path sum coded as subtree sum
- Lazy segtree wrong bounds (`tout` exclusive vs inclusive)
- Re-rooting online without rebuilding tour (tour is root-dependent)

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Segtree / merge-sort tree** on Euler for “k-th in subtree”, distinct colors (with persistence)
- **Edge values:** store on child `tin[child]`
- **Subtree + path:** HLD or Euler for subtree + lifting for path
- **Offline DSU on tree** for heavy frequency queries (see Sack)

---

## 11. Typical Problem Archetypes

1. Standard application: point update, subtree sum
2. Slightly disguised: company hierarchy bonuses
3. Difficult: subtree mex / majority — Sack or segtree-of-vectors
4. Very difficult / advanced: dynamic reroot + subtree structures

---

## 12. Recognition & Identification Drills

1. Support assign value at node and query sum of subtree.
2. Add \(x\) on entire subtree; query single node value after many updates.
3. For each node, count how many nodes in its subtree have value \(> a_v\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: rooted subtree aggregates as ranges
- Key invariant: Euler segment = subtree
- Key formula: sum = Fenwick`[tin..tout]`; subtree add ↔ diff at `tin`/`tout+1`
- Complexity: \(O(\log n)\) per op
- Template to remember: DFS times + BIT on `tin`

---

## 5. Tree DP

---
