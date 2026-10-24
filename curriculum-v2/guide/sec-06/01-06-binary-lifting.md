# Binary Lifting

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2100 | **Frequency:** Very Common  
> **Prerequisites:** Trees, DFS/BFS, bit tricks  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Trees, DFS/BFS, bit tricks

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

Any upward jump of length \(k\) factors into at most \(\lfloor\log k\rfloor+1\) jumps of powers of two. Precompute `up[j][v]` = the \(2^j\)-th ancestor of \(v\). Then k-th ancestor, LCA lifts, and “jump while predicate” become bit loops. Prefer **iterative** builds (BFS/queue from root or two nested loops after a parent array) to avoid recursion depth on \(n=2\cdot10^5\) chains.

---

## 4. Proof Sketches & Recurrences

Let `up[0][v] = parent[v]`. Recurrence:
\[
\mathrm{up}[j][v] = \mathrm{up}[j-1][\mathrm{up}[j-1][v]]
\]
(with sentinel 0 if missing). Depths from a root DFS/BFS. For k-th ancestor, for bit \(j\) from high to low: if \(k\) has bit \(j\), `v = up[j][v]`. Preprocess \(O(n\log n)\), query \(O(\log n)\). Memory \(O(n\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\)
- Per-query / per-operation: \(O(\log n)\) for k-th / lift
- Total: depends on queries
- Memory: \(O(n\log n)\)`

### C++17 Template

```cpp
// C++17 — iterative binary lifting (1-indexed nodes, root = 1, parent[root]=0)
namespace binlift {
constexpr int N = 200005, LOG = 18; // 2^18 > 2e5
int n, up[LOG][N], dep[N];
vector<int> g[N];

void build(int root = 1) {
    // parent + depth via BFS (iterative)
    fill(up[0], up[0] + n + 1, 0);
    fill(dep, dep + n + 1, 0);
    queue<int> q;
    q.push(root);
    dep[root] = 0;
    up[0][root] = 0;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        for (int to : g[v]) if (to != up[0][v]) {
            up[0][to] = v;
            dep[to] = dep[v] + 1;
            q.push(to);
        }
    }
    for (int j = 1; j < LOG; ++j)
        for (int v = 1; v <= n; ++v)
            up[j][v] = up[j - 1][up[j - 1][v]];
}

int kth(int v, int k) {
    if (k > dep[v]) return 0;
    for (int j = 0; j < LOG; ++j)
        if (k & (1 << j)) v = up[j][v];
    return v;
}

int dist(int u, int v, int lca) {
    return dep[u] + dep[v] - 2 * dep[lca];
}
} // namespace binlift
```

### Python 3 Template

```python
# Python 3.11+ — iterative binary lifting
from collections import deque

class BinLift:
    def __init__(self, n: int, g: list[list[int]], root: int = 1, LOG: int = 18):
        self.n, self.LOG = n, LOG
        self.up = [[0] * (n + 1) for _ in range(LOG)]
        self.dep = [0] * (n + 1)
        q = deque([root])
        self.up[0][root] = 0
        while q:
            v = q.popleft()
            for to in g[v]:
                if to != self.up[0][v]:
                    self.up[0][to] = v
                    self.dep[to] = self.dep[v] + 1
                    q.append(to)
        for j in range(1, LOG):
            uj, uj1 = self.up[j], self.up[j - 1]
            for v in range(1, n + 1):
                uj[v] = uj1[uj1[v]]

    def kth(self, v: int, k: int) -> int:
        if k > self.dep[v]:
            return 0
        for j in range(self.LOG):
            if k & (1 << j):
                v = self.up[j][v]
        return v
```

---

## 6. Recognition Trigger Signals & Heuristics

- “k-th ancestor”, “jump up by x”, “meet after walking”
- Distance on tree once LCA exists: `dep[u]+dep[v]-2*dep[lca]`
- Binary search on path depth / first ancestor satisfying a condition
- Functional graph / “teleport to parent” with large k

---

## 7. Contest WA / TLE / RE Traps

- Forgetting root’s parent is 0 / sentinel → infinite or out-of-bounds
- Lifting more than `dep[v]` without check
- Building `up[j]` before `up[j-1]` finished
- 0-index vs 1-index mix in `g` and arrays
- Using recursion DFS on deep trees without raising stack / iterative rewrite

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

- **Weighted jumps:** store min/max/sum/gcd on `up` edge aggregates for path fold
- **Jump while:** binary search highest ancestor with property (combine with prefix on path)
- **Functional graphs:** same table on outdegree-1 digraphs (cycle + trees)
- **Doubling on sequences:** same idea off trees

---

## 11. Typical Problem Archetypes

1. Standard application: k-th ancestor queries
2. Slightly disguised: cow/jump games — move up until energy runs out (binary lift on remaining)
3. Difficult: path aggregates (max edge) with lifting tables
4. Very difficult / advanced: combine with HLD or persistent structures on jumps

---

## 12. Recognition & Identification Drills

1. Tree of \(n\) nodes; \(q\) queries “what is the k-th parent of v?” (\(n,q\le 2\cdot10^5\)).
2. Each edge has a weight; for queries \((u,v)\), report the maximum edge on the path \(u\!\to\!v\).
3. From city \(v\), you may jump to the \(2^j\)-th ancestor in one day for any \(j\); minimum days to reach the capital.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: large upward jumps / ancestors / path binary search
- Key invariant: any distance \(\le n\) is sum of distinct powers of two
- Key formula: `up[j][v] = up[j-1][up[j-1][v]]`
- Complexity: \(O(n\log n)\) prep, \(O(\log n)/\text{query}\)
- Template to remember: iterative BFS parents + doubling loop + bit walk

---

## 2. LCA

---
