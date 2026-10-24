# Tree DP

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2200 | **Frequency:** Very Common  
> **Prerequisites:** DP, DFS on trees  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: DP, DFS on trees

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

Root the tree; combine children’s DP into parent with a merge that respects “subtrees are independent given the root choice”. Classic forms: knapsack-on-tree (\(O(n^2)\) merging sizes), independent set, matching, diameter via heights, “max path in subtree”. Think **post-order**: children first, then node.

---

## 4. Proof Sketches & Recurrences

Example — max weight independent set:
\[
dp[v][0] = \sum_c \max(dp[c][0], dp[c][1]),\quad
dp[v][1] = w[v] + \sum_c dp[c][0]
\]
Knapsack merge: when attaching child size \(s_c\) to current size \(s\), update backup array in \(O(s\cdot s_c)\); total over tree \(O(n^2)\). Diameter: for each node, best two child-down paths.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: usually one DFS
- Total: \(O(n)\) typical; \(O(n^2)\) knapsack merges; \(O(n\cdot\text{state})\) otherwise
- Memory: \(O(n\cdot\text{state})\)`

### C++17 Template

```cpp
// C++17 — tree DP skeletons (independent set + knapsack merge)
namespace treedp {
constexpr int N = 200005;
int n;
long long w[N], dp0[N], dp1[N];
vector<int> g[N];

void dfs_is(int v, int p) {
    dp0[v] = 0;
    dp1[v] = w[v];
    for (int to : g[v]) if (to != p) {
        dfs_is(to, v);
        dp0[v] += max(dp0[to], dp1[to]);
        dp1[v] += dp0[to];
    }
}

// O(n^2) knapsack: dp[v][k] = best with k nodes chosen in subtree (example: max weight)
int sz[N];
long long f[N][N], tmp[N]; // care: memory — use vectors sized by sz in practice
void dfs_knap(int v, int p) {
    sz[v] = 1;
    f[v][0] = 0;
    f[v][1] = w[v]; // depending on problem
    for (int to : g[v]) if (to != p) {
        dfs_knap(to, v);
        for (int i = 0; i <= sz[v] + sz[to]; ++i) tmp[i] = (long long)-4e18;
        for (int i = 0; i <= sz[v]; ++i)
            for (int j = 0; j <= sz[to]; ++j)
                tmp[i + j] = max(tmp[i + j], f[v][i] + f[to][j]);
        sz[v] += sz[to];
        for (int i = 0; i <= sz[v]; ++i) f[v][i] = tmp[i];
    }
}
} // namespace treedp
```

### Python 3 Template

```python
# Python 3.11+ — independent set tree DP
import sys
sys.setrecursionlimit(1_000_000)

def max_independent_set(n, g, w, root=1):
    dp0 = [0] * (n + 1)
    dp1 = [0] * (n + 1)
    def dfs(v, p):
        dp1[v] = w[v]
        for to in g[v]:
            if to == p:
                continue
            dfs(to, v)
            dp0[v] += max(dp0[to], dp1[to])
            dp1[v] += dp0[to]
    dfs(root, 0)
    return max(dp0[root], dp1[root])
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Choose vertices with adjacency constraints”
- Budget/size limited selection in subtrees
- Ground/facility on tree, DP states at node
- Diameter, max matching, vertex cover on trees

---

## 7. Contest WA / TLE / RE Traps

- Using parent as child (missing `to != p`)
- Merging knapsack in-place without temp → double counting
- Wrong transition when “must take root” / “edge vs vertex” DP
- Not handling leaves
- \(O(n^2)\) memory with `f[N][N]` — allocate by size

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

- **Edge DP:** state on edges / reroot along edges
- **Digit / digit-like on tree:** combine with digit DP rare
- **Tree knapsack with convexity** → D&C opt (Section 04)
- **Matching / cover / coloring** standard transitions

---

## 11. Typical Problem Archetypes

1. Standard application: independent set / dominating set on tree
2. Slightly disguised: party invitation with boss constraints
3. Difficult: knapsack group merges with size
4. Very difficult / advanced: DP on treewidth / virtual tree DP

---

## 12. Recognition & Identification Drills

1. Max weight set of vertices with no two adjacent.
2. Choose exactly \(k\) vertices in a tree maximizing sum with no two adjacent.
3. Each node has a cost to “install”; cover all edges by installing endpoints — minimize cost.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: optimize over subsets/configs respecting tree edges
- Key invariant: child subtrees independent given root state
- Key formula: post-order combine \(\bigoplus_c dp[c]\)
- Complexity: usually \(O(n)\) or \(O(n^2)\) merges
- Template to remember: `dfs(v): for child: dfs; merge`

---

## 6. Rerooting DP

---
