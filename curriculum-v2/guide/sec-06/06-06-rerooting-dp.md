# Rerooting DP

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Common  
> **Prerequisites:** Tree DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Tree DP

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

Compute a rooted DP once, then **transfer** the answer from root \(r\) to neighbor \(u\) in \(O(1)\) or \(O(\deg)\) using prefix/suffix aggregates of children — total \(O(n)\). Prefer rerooting when the answer is needed for **every** node as root. Prefer **two BFS/DFS** when you only need diameter, farthest node, or a single “best eccentricity” style fact.

---

## 4. Proof Sketches & Recurrences

Example — sum of distances: first DFS `down[v]` = sum of distances in subtree, `sz[v]` sizes. Reroot:
\[
\mathrm{up\_sum}[u] = \mathrm{ans}[v] - (\mathrm{down}[u] + \mathrm{sz}[u]) + (n - \mathrm{sz}[u])
\]
when moving root from \(v\) to child \(u\): nodes in \(u\)’s subtree get \(-1\) distance, others \(+1\). General pattern: maintain contribution of “rest of tree” as a fake parent child.

Prefix/suffix max for “max path going through parent”: store child values array, prefix/suffix bests, DFS2 passes parent contribution.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: —
- Total: \(O(n)\) for associative merges; \(O(n\cdot\text{cost})\) if merge heavier
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — rerooting: sum of distances to all nodes
namespace reroot {
constexpr int N = 200005;
int n, sz[N];
long long down[N], ans[N];
vector<int> g[N];

void dfs1(int v, int p) {
    sz[v] = 1;
    down[v] = 0;
    for (int to : g[v]) if (to != p) {
        dfs1(to, v);
        sz[v] += sz[to];
        down[v] += down[to] + sz[to];
    }
}

void dfs2(int v, int p) {
    for (int to : g[v]) if (to != p) {
        // ans[v] known; move root v -> to
        ans[to] = ans[v] - sz[to] + (n - sz[to]);
        dfs2(to, v);
    }
}

void solve(int root = 1) {
    dfs1(root, 0);
    ans[root] = down[root];
    dfs2(root, 0);
}
} // namespace reroot
```

### Python 3 Template

```python
# Python 3.11+ — sum of distances rerooting
import sys
sys.setrecursionlimit(1_000_000)

def sum_dist_all_roots(n, g, root=1):
    sz = [0] * (n + 1)
    down = [0] * (n + 1)
    ans = [0] * (n + 1)
    def dfs1(v, p):
        sz[v] = 1
        for to in g[v]:
            if to == p: continue
            dfs1(to, v)
            sz[v] += sz[to]
            down[v] += down[to] + sz[to]
    def dfs2(v, p):
        for to in g[v]:
            if to == p: continue
            ans[to] = ans[v] - sz[to] + (n - sz[to])
            dfs2(to, v)
    dfs1(root, 0)
    ans[root] = down[root]
    dfs2(root, 0)
    return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- “For each vertex, compute f(tree rooted at v)”
- Sum of distances to all nodes; max distance (eccentricity) for all v
- Reroot with associative child merges (sum, max, xor)
- Statement asks \(n\) answers, one per node

---

## 7. Contest WA / TLE / RE Traps

- Wrong \(+1/-1\) on sizes when rerooting distances
- Forgetting to include parent contribution as a “virtual child”
- Using only `down` without second DFS
- Non-invertible merges — need prefix/suffix recompute \(O(\deg)\)
- Applying rerooting when 2-BFS suffices (wasted complexity)

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

- **Max eccentricity / tree center:** reroot max-down + up
- **Colored / weighted edges:** adjust ± formulas
- **Invertible vs non-invertible:** XOR/sum invertible; max needs prefix/suffix
- **Reroot + knapsack:** rare, expensive

---

## 11. Typical Problem Archetypes

1. Standard application: sum of distances for every root
2. Slightly disguised: fuel/cost to visit all cities from each start
3. Difficult: reroot with max/second-max child paths
4. Very difficult / advanced: reroot with data structures hanging on nodes

---

## 12. Recognition & Identification Drills

1. For each city \(v\), compute sum of distances to all other cities.
2. For each \(v\), compute the farthest distance from \(v\) (eccentricity).
3. Paint each edge; for each root, count pairs of same-color paths — need rethink (maybe not plain reroot).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: answer for every root, merge is reroot-friendly
- Key invariant: moving root across edge updates contributions by subtree size
- Key formula: `ans[child] = ans[par] - sz[child] + (n - sz[child])` (distances)
- Complexity: \(O(n)\)
- Template to remember: dfs1 down → dfs2 transfer; else 2-BFS for diameter-only

---

Continue with HLD, centroid, Sack, virtual trees in [06-b-tree-decompositions.md](06-b-tree-decompositions.md).

---
