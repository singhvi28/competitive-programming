# 11. What to drill this week

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2400
- Prerequisites: Tree traversals, LCA, Euler Tour, Heavy-Light Decomposition

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

Tree algorithms in rated contests test structural reductions: converting arbitrary tree paths or subtree aggregates into contiguous ranges on an array via Euler tours and heavy paths. Master binary lifting for static tree paths, subtree difference arrays for subtree updates, and HLD for dynamic path operations.

---

## 4. Proof Sketches & Recurrences

A rooted tree of $N$ vertices can be linearized into an Euler tour of length $N$ or $2N$. For any vertex $u$, its subtree corresponds to the contiguous interval $[\text{tin}[u], \text{tout}[u]]$. Any path $u \leftrightarrow v$ decomposes into $\mathcal{O}(\log N)$ contiguous segments under Heavy-Light Decomposition.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Tree Drill Pipeline: LCA, Subtree Ranges, and Binary Lifting
#include <bits/stdc++.h>
using namespace std;

struct TreeDrill {
    int n, LOG;
    vector<vector<int>> adj, up;
    vector<int> depth, tin, tout;
    int timer = 0;
    TreeDrill(int n_) : n(n_), LOG(__lg(n_) + 2), adj(n_ + 1), up(LOG, vector<int>(n_ + 1)), depth(n_ + 1), tin(n_ + 1), tout(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void dfs(int u, int p) {
        tin[u] = ++timer;
        up[0][u] = p;
        for (int i = 1; i < LOG; ++i) up[i][u] = up[i - 1][up[i - 1][u]];
        for (int v : adj[u]) if (v != p) { depth[v] = depth[u] + 1; dfs(v, u); }
        tout[u] = timer;
    }
    int get_lca(int u, int v) {
        if (depth[u] < depth[v]) swap(u, v);
        for (int k = LOG - 1; k >= 0; --k) if (depth[u] - (1 << k) >= depth[v]) u = up[k][u];
        if (u == v) return u;
        for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return up[0][u];
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Queries over arbitrary tree paths $u \leftrightarrow v$ with point or range updates.
- Subtree color frequency counting (DSU on Tree / Small-to-Large merging).
- Path bottleneck queries where edge weights represent capacities or tolerances.
- Distance queries among dynamically added or deleted nodes (Centroid Tree).

---

## 7. Contest WA / TLE / RE Traps

- Forgetting 1-based vs 0-based indexing on tree Euler tours.
- Rooting the tree at an arbitrary vertex when directed edges require topological ordering.
- LCA query fails when start and end vertices are identical ($u = v$).
- Stack overflow in deep skew trees without `#pragma comment(linker)` or manual iterative DFS.

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
