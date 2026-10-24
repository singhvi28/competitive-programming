# 9. DSU on Tree (Sack)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Euler tour / DFS, tree sz, frequency maps  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Euler tour / DFS, tree sz, frequency maps

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

Compute offline answers for **every subtree** by keeping a frequency map of values. DFS heavy child first **without clearing**; then add light subtrees; answer; if current node is not heavy child of parent, clear. Light edges clear \(O(\log n)\) times per node → \(O(n\log n)\) updates. Prefer Sack for **all-subtree frequency** problems. Prefer **virtual tree** when only \(k\ll n\) key nodes matter. Prefer Euler+Mo for harder non-additive offline queries.

---

## 4. Proof Sketches & Recurrences

`sz` + heavy child as in HLD. `dfs(v, keep)`:
1. Process all light children with `keep=false`.
2. Process heavy child with `keep=true`.
3. Add light children’s nodes into the global map (re-DFS add).
4. Add `v` itself; write `ans[v]`.
5. If `!keep`, remove entire subtree of `v` from the map.

Each node added/removed once per light ancestor → \(O(n\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) sizes/times
- Per-query / per-operation: offline all answers
- Total: \(O(n\log n\cdot \alpha)\) where \(\alpha\) = add/rem cost
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — Sack: count distinct colors in every subtree
namespace sack {
constexpr int N = 200005;
int n, sz[N], heavy[N], col[N], ans[N], timer;
int tin[N], tout[N], ver[N]; // ver[t] = node with tin = t
vector<int> g[N];
int freq[N], distinct = 0; // color -> count; colors compressed to [1..n]

void add_color(int c) {
    if (freq[c] == 0) ++distinct;
    ++freq[c];
}
void rem_color(int c) {
    --freq[c];
    if (freq[c] == 0) --distinct;
}

int dfs_sz(int v, int p) {
    sz[v] = 1; heavy[v] = -1;
    int best = 0;
    for (int to : g[v]) if (to != p) {
        int s = dfs_sz(to, v);
        sz[v] += s;
        if (s > best) best = s, heavy[v] = to;
    }
    return sz[v];
}

void dfs_time(int v, int p) {
    tin[v] = ++timer;
    ver[timer] = v;
    for (int to : g[v]) if (to != p) dfs_time(to, v);
    tout[v] = timer;
}

void dfs(int v, int p, bool keep) {
    for (int to : g[v]) if (to != p && to != heavy[v]) dfs(to, v, false);
    if (heavy[v] != -1) dfs(heavy[v], v, true);
    for (int to : g[v]) if (to != p && to != heavy[v]) {
        for (int t = tin[to]; t <= tout[to]; ++t) add_color(col[ver[t]]);
    }
    add_color(col[v]);
    ans[v] = distinct;
    if (!keep) {
        for (int t = tin[v]; t <= tout[v]; ++t) rem_color(col[ver[t]]);
    }
}

void solve(int root = 1) {
    timer = 0;
    dfs_sz(root, 0);
    dfs_time(root, 0);
    // clear freq...
    dfs(root, 0, false);
}
} // namespace sack
```

---

## 6. Recognition Trigger Signals & Heuristics

- For every \(v\), something about multiset of colors/values in subtree
- Dominant color, mex, number of distinct, mode
- “DSU on tree”, “small-to-large on tree”, Sack
- Offline only; no path queries

---

## 7. Contest WA / TLE / RE Traps

- Clearing after heavy child incorrectly
- Adding light subtrees before processing heavy
- Forgetting to add node `v` itself
- `keep=true` on root call when you still need a clean map afterward
- Using path structures — Sack is subtree-only

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

- **Mode / sum of frequencies with f(freq)** — maintain extra aggregates on freq changes
- **Mex of subtree:** track freq of values + set of missing
- **Small-to-large with maps of maps** (merge maps by size) — similar complexity, different code
- **Sack + segtree** hanging values

---

## 11. Typical Problem Archetypes

1. Standard application: distinct colors per subtree
2. Slightly disguised: most frequent color in each subtree
3. Difficult: mex of values in each subtree
4. Very difficult / advanced: Sack with heavy algebra on frequencies

---

## 12. Recognition & Identification Drills

1. For each node, count distinct colors in its subtree.
2. For each node, find the sum of values that appear exactly once in its subtree.
3. For each node, compute mex of the set of colors in its subtree.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: offline answer for every subtree multiset
- Key invariant: keep heavy child’s map; light cleared \(O(\log n)\) times
- Key formula: light → heavy(keep) → add lights → answer → clear if !keep
- Complexity: \(O(n\log n\cdot\alpha)\)
- Template to remember: same heavy child as HLD + keep flag

---

## 10. Virtual trees

---
