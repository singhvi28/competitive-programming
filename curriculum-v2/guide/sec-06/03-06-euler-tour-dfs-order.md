# 3. Euler Tour (DFS order)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Trees, DFS, arrays / Fenwick / segtree  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Trees, DFS, arrays / Fenwick / segtree

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

A DFS timestamps nodes so each subtree is a **contiguous segment** `[tin[v], tout[v]]` (or `[tin, tin+sz-1]`). The tree becomes an array; subtree problems become range problems. Variant tours: enter-only (subtree ranges), enter+exit (path tricks / Mo on trees), edge tour for edge-subtree.

---

## 4. Proof Sketches & Recurrences

DFS: on entry `tin[v] = ++timer`, recurse children, on exit `tout[v] = timer` (or `tout = ++timer` for exit-events). Subtree nodes = those with `tin` in `[tin[v], tout[v]]`. Size `sz[v] = tout[v]-tin[v]+1` if tout is last-in-subtree time. Path \(u\!\to\!v\) is **not** a single segment — need LCA + two chains or HLD.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: \(O(1)\) for tin/tout / ancestor
- Total: \(O(n)\)
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — Euler tour tin/tout + order array
namespace euler {
constexpr int N = 200005;
int n, timer, tin[N], tout[N], sz[N], order[N]; // order[tin] = node
vector<int> g[N];

void dfs(int v, int p) {
    tin[v] = ++timer;
    order[timer] = v;
    sz[v] = 1;
    for (int to : g[v]) if (to != p) {
        dfs(to, v);
        sz[v] += sz[to];
    }
    tout[v] = timer;
}

bool is_ancestor(int a, int b) { // a ancestor of b
    return tin[a] <= tin[b] && tout[b] <= tout[a];
}

void build(int root = 1) {
    timer = 0;
    dfs(root, 0);
}
} // namespace euler
```

### Python 3 Template

```python
# Python 3.11+ — iterative Euler tour
def euler_tour(n: int, g: list[list[int]], root: int = 1):
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = [0] * (n + 1)
    timer = 0
    stack = [(root, 0, 0)]  # node, parent, next child idx
    while stack:
        v, p, i = stack[-1]
        if i == 0:
            timer += 1
            tin[v] = timer
            order[timer] = v
        children = g[v]
        if i < len(children):
            stack[-1] = (v, p, i + 1)
            to = children[i]
            if to != p:
                stack.append((to, v, 0))
        else:
            tout[v] = timer
            stack.pop()
    return tin, tout, order
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Subtree of v” with updates/queries
- Flatten tree, map to segment tree indices
- Ancestor checks via intervals
- Mo’s algorithm on trees (enter/exit tour)

---

## 7. Contest WA / TLE / RE Traps

- Mixing “tout = timer” vs “tout = ++timer” conventions inconsistently with range DS
- Forgetting `order[tin[v]] = v`
- Treating path as one segment
- Parent edge double-counting in adjacency DFS
- Off-by-one in Fenwick indices (`tin` from 1)

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

- **Enter/exit event tour** length \(2n\) for Mo on trees / difference tricks
- **Edge Euler:** assign `tin` to child endpoint for edge values
- **Tour for RMQ LCA:** record node every visit (length \(2n-1\))
- **Heavy-light positions:** same DFS but reorder heavy child first

---

## 11. Typical Problem Archetypes

1. Standard application: map subtree ↔ array range
2. Slightly disguised: paint subtree, query point (diff array on tour)
3. Difficult: subtree + path mixed → HLD or two structures
4. Very difficult / advanced: Mo on trees with enter/exit

---

## 12. Recognition & Identification Drills

1. Assign values to nodes; support “add \(x\) to subtree of \(v\)” and “value at \(u\)”.
2. Count nodes with color \(c\) in subtree of \(v\) (offline or static).
3. Check for each query whether \(a\) lies on the path from root to \(b\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: any subtree ↔ contiguous range reduction
- Key invariant: DFS discovery order nests subtrees
- Key formula: subtree = `[tin[v], tout[v]]`
- Complexity: \(O(n)\) build
- Template to remember: `tin` on entry, process children, `tout = timer`

---

## 4. Subtree queries

---
