# Section §06: Tree Algorithms & Structural Decompositions

> **Module ID:** `sec-06`  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Topic Count:** 11  

**Module Summary:** Binary lifting, LCA, Euler tours, Tree DP, Tree rerooting DP, Heavy-Light Decomposition (HLD), Centroid Decomposition, and Sack (DSU on Tree).

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Binary Lifting](#topic-1) | `S-tier` | 1500–2100 | Very Common | [01-06-binary-lifting.md](./01-06-binary-lifting.md) |
| 2 | [LCA (Lowest Common Ancestor)](#topic-2) | `S-tier` | 1500–2100 | Very Common | [02-06-lca-lowest-common-ancestor.md](./02-06-lca-lowest-common-ancestor.md) |
| 3 | [Euler Tour (DFS order)](#topic-3) | `S-tier` | 1600–2200 | Common | [03-06-euler-tour-dfs-order.md](./03-06-euler-tour-dfs-order.md) |
| 4 | [Subtree Queries](#topic-4) | `S-tier` | 1600–2200 | Common | [04-06-subtree-queries.md](./04-06-subtree-queries.md) |
| 5 | [Tree DP](#topic-5) | `S-tier` | 1500–2200 | Very Common | [05-06-tree-dp.md](./05-06-tree-dp.md) |
| 6 | [Rerooting DP](#topic-6) | `A-tier` | 1800–2400 | Common | [06-06-rerooting-dp.md](./06-06-rerooting-dp.md) |
| 7 | [Heavy-Light Decomposition (HLD)](#topic-7) | `A-tier` | 2000–2600 | Occasional | [07-06-heavy-light-decomposition-hld.md](./07-06-heavy-light-decomposition-hld.md) |
| 8 | [Centroid Decomposition](#topic-8) | `A-tier` | 2000–2700 | Occasional | [08-06-centroid-decomposition.md](./08-06-centroid-decomposition.md) |
| 9 | [DSU on Tree (Sack)](#topic-9) | `B-tier` | 1900–2500 | Occasional | [09-06-dsu-on-tree-sack.md](./09-06-dsu-on-tree-sack.md) |
| 10 | [Virtual Trees (Compressed Trees)](#topic-10) | `B-tier` | 2200–2800 | Occasional | [10-06-virtual-trees-compressed-trees.md](./10-06-virtual-trees-compressed-trees.md) |
| 11 | [What to drill this week](#topic-11) | `B-tier` | 1600–2200 | Common | [11-06-what-to-drill-this-week.md](./11-06-what-to-drill-this-week.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Binary Lifting

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2100 | **Frequency:** Very Common  
> **Prerequisites:** Trees, DFS/BFS, bit tricks  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Trees, DFS/BFS, bit tricks

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Any upward jump of length \(k\) factors into at most \(\lfloor\log k\rfloor+1\) jumps of powers of two. Precompute `up[j][v]` = the \(2^j\)-th ancestor of \(v\). Then k-th ancestor, LCA lifts, and “jump while predicate” become bit loops. Prefer **iterative** builds (BFS/queue from root or two nested loops after a parent array) to avoid recursion depth on \(n=2\cdot10^5\) chains.

---

#### 4. Proof Sketches & Recurrences

Let `up[0][v] = parent[v]`. Recurrence:
\[
\mathrm{up}[j][v] = \mathrm{up}[j-1][\mathrm{up}[j-1][v]]
\]
(with sentinel 0 if missing). Depths from a root DFS/BFS. For k-th ancestor, for bit \(j\) from high to low: if \(k\) has bit \(j\), `v = up[j][v]`. Preprocess \(O(n\log n)\), query \(O(\log n)\). Memory \(O(n\log n)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\)
- Per-query / per-operation: \(O(\log n)\) for k-th / lift
- Total: depends on queries
- Memory: \(O(n\log n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “k-th ancestor”, “jump up by x”, “meet after walking”
- Distance on tree once LCA exists: `dep[u]+dep[v]-2*dep[lca]`
- Binary search on path depth / first ancestor satisfying a condition
- Functional graph / “teleport to parent” with large k

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting root’s parent is 0 / sentinel → infinite or out-of-bounds
- Lifting more than `dep[v]` without check
- Building `up[j]` before `up[j-1]` finished
- 0-index vs 1-index mix in `g` and arrays
- Using recursion DFS on deep trees without raising stack / iterative rewrite

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Weighted jumps:** store min/max/sum/gcd on `up` edge aggregates for path fold
- **Jump while:** binary search highest ancestor with property (combine with prefix on path)
- **Functional graphs:** same table on outdegree-1 digraphs (cycle + trees)
- **Doubling on sequences:** same idea off trees

---

#### 11. Typical Problem Archetypes

1. Standard application: k-th ancestor queries
2. Slightly disguised: cow/jump games — move up until energy runs out (binary lift on remaining)
3. Difficult: path aggregates (max edge) with lifting tables
4. Very difficult / advanced: combine with HLD or persistent structures on jumps

---

#### 12. Recognition & Identification Drills

1. Tree of \(n\) nodes; \(q\) queries “what is the k-th parent of v?” (\(n,q\le 2\cdot10^5\)).
2. Each edge has a weight; for queries \((u,v)\), report the maximum edge on the path \(u\!\to\!v\).
3. From city \(v\), you may jump to the \(2^j\)-th ancestor in one day for any \(j\); minimum days to reach the capital.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: large upward jumps / ancestors / path binary search
- Key invariant: any distance \(\le n\) is sum of distinct powers of two
- Key formula: `up[j][v] = up[j-1][up[j-1][v]]`
- Complexity: \(O(n\log n)\) prep, \(O(\log n)/\text{query}\)
- Template to remember: iterative BFS parents + doubling loop + bit walk

---

## 2. LCA

---


---

<a id="topic-2"></a>
### 2. LCA (Lowest Common Ancestor)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2100 | **Frequency:** Very Common  
> **Prerequisites:** Binary lifting (or Euler + RMQ)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Binary lifting (or Euler + RMQ)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

LCA is the deepest node that is an ancestor of both. Binary lifting: equalize depths, then lift both while ancestors differ; parent of the meeting point is LCA. Euler+RMQ: LCA = shallowest node on the Euler tour between first occurrences of \(u\) and \(v\) — RMQ on depths. Distance, path intersection, and “is ancestor” (`tin/tout`) all orbit LCA.

---

#### 4. Proof Sketches & Recurrences

**Binary lifting LCA.** After equalizing `dep[u]==dep[v]` by lifting the deeper node: if equal, done. Else for \(j=\mathrm{LOG}-1..0\): if `up[j][u] != up[j][v]`, lift both. Then `lca = up[0][u]`. Correct because the highest differing ancestors leave you at children of LCA.

**Euler+RMQ.** Tour length \(2n-1\); sparse table on depths at first-occurrence indices → \(O(1)\) LCA. Prefer lifting in contests unless you need constant-time LCA or already have RMQ.

Ancestor test without LCA: `tin[a] <= tin[b] && tout[b] <= tout[a]`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) lifting; Euler+RMQ also \(O(n\log n)\) (or \(O(n)\) ± Cartesian tricks)
- Per-query / per-operation: \(O(\log n)\) lifting; \(O(1)\) with sparse RMQ
- Total: \(O(n\log n + q\log n)\) typical
- Memory: \(O(n\log n)\)`

##### C++17 Template

```cpp
// C++17 — iterative binary lifting LCA (extends binlift namespace ideas)
namespace lca_bl {
constexpr int N = 200005, LOG = 18;
int n, up[LOG][N], dep[N];
vector<int> g[N];

void build(int root = 1) {
    fill(up[0], up[0] + n + 1, 0);
    queue<int> q;
    q.push(root);
    dep[root] = 0;
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

int lift(int v, int k) {
    for (int j = 0; j < LOG; ++j)
        if (k & (1 << j)) v = up[j][v];
    return v;
}

int lca(int u, int v) {
    if (dep[u] < dep[v]) swap(u, v);
    u = lift(u, dep[u] - dep[v]);
    if (u == v) return u;
    for (int j = LOG - 1; j >= 0; --j)
        if (up[j][u] != up[j][v]) {
            u = up[j][u];
            v = up[j][v];
        }
    return up[0][u];
}

int dist(int u, int v) {
    int w = lca(u, v);
    return dep[u] + dep[v] - 2 * dep[w];
}
} // namespace lca_bl
```

##### Python 3 Template

```python
# Python 3.11+ — binary lifting LCA
from collections import deque

class LCA:
    def __init__(self, n: int, g: list[list[int]], root: int = 1, LOG: int = 18):
        self.LOG = LOG
        self.up = [[0] * (n + 1) for _ in range(LOG)]
        self.dep = [0] * (n + 1)
        q = deque([root])
        while q:
            v = q.popleft()
            for to in g[v]:
                if to != self.up[0][v]:
                    self.up[0][to] = v
                    self.dep[to] = self.dep[v] + 1
                    q.append(to)
        for j in range(1, LOG):
            for v in range(1, n + 1):
                self.up[j][v] = self.up[j - 1][self.up[j - 1][v]]

    def lift(self, v: int, k: int) -> int:
        for j in range(self.LOG):
            if k & (1 << j):
                v = self.up[j][v]
        return v

    def lca(self, u: int, v: int) -> int:
        if self.dep[u] < self.dep[v]:
            u, v = v, u
        u = self.lift(u, self.dep[u] - self.dep[v])
        if u == v:
            return u
        for j in range(self.LOG - 1, -1, -1):
            if self.up[j][u] != self.up[j][v]:
                u, v = self.up[j][u], self.up[j][v]
        return self.up[0][u]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Distance / path length between two nodes
- “Closest meeting point”, “shared boss”, “subtree containing both”
- Path unique → properties of path reduce via LCA
- Offline/online LCA with \(q\sim n\sim 2\cdot10^5\)

---

#### 7. Contest WA / TLE / RE Traps

- Lifting both when depths unequal
- Comparing `up[j][u]` when one is already 0 (root’s parent)
- Off-by-one on distance (edges vs nodes)
- Assuming rooted tree when input is unrooted — pick any root
- Euler tour RMQ: using wrong index (first occurrence only)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **LCA with path min/max:** store edge weights on `up`
- **Tarjan offline LCA:** DSU + DFS — rare now vs lifting
- **Binary lifting on virtual tree / compressed tree**
- **k-th node on path u→v:** via LCA + depths

---

#### 11. Typical Problem Archetypes

1. Standard application: distance queries
2. Slightly disguised: minimum meetings / shared ancestor constraints
3. Difficult: path intersection of two paths (LCAs of endpoints)
4. Very difficult / advanced: dynamic trees (prefer HLD/LCT — not plain LCA)

---

#### 12. Recognition & Identification Drills

1. \(q\) distance queries on a weighted tree (\(n,q\le 2\cdot10^5\)).
2. For each query path \(u\!\to\!v\), find the node in the middle (or two middles if even length).
3. Given pairs of paths, decide whether they share a vertex.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any path endpoint problem on static trees
- Key invariant: after depth equalize, LCA is parent of first disagreeing jump
- Key formula: `dist = dep[u]+dep[v]-2*dep[lca]`
- Complexity: \(O(n\log n)\) prep, \(O(\log n)\) query
- Template to remember: equalize → lift while `up[j]` differs → `up[0]`

---

## 3. Euler tour

---


---

<a id="topic-3"></a>
### 3. Euler Tour (DFS order)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Trees, DFS, arrays / Fenwick / segtree  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Trees, DFS, arrays / Fenwick / segtree

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

A DFS timestamps nodes so each subtree is a **contiguous segment** `[tin[v], tout[v]]` (or `[tin, tin+sz-1]`). The tree becomes an array; subtree problems become range problems. Variant tours: enter-only (subtree ranges), enter+exit (path tricks / Mo on trees), edge tour for edge-subtree.

---

#### 4. Proof Sketches & Recurrences

DFS: on entry `tin[v] = ++timer`, recurse children, on exit `tout[v] = timer` (or `tout = ++timer` for exit-events). Subtree nodes = those with `tin` in `[tin[v], tout[v]]`. Size `sz[v] = tout[v]-tin[v]+1` if tout is last-in-subtree time. Path \(u\!\to\!v\) is **not** a single segment — need LCA + two chains or HLD.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: \(O(1)\) for tin/tout / ancestor
- Total: \(O(n)\)
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Subtree of v” with updates/queries
- Flatten tree, map to segment tree indices
- Ancestor checks via intervals
- Mo’s algorithm on trees (enter/exit tour)

---

#### 7. Contest WA / TLE / RE Traps

- Mixing “tout = timer” vs “tout = ++timer” conventions inconsistently with range DS
- Forgetting `order[tin[v]] = v`
- Treating path as one segment
- Parent edge double-counting in adjacency DFS
- Off-by-one in Fenwick indices (`tin` from 1)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Enter/exit event tour** length \(2n\) for Mo on trees / difference tricks
- **Edge Euler:** assign `tin` to child endpoint for edge values
- **Tour for RMQ LCA:** record node every visit (length \(2n-1\))
- **Heavy-light positions:** same DFS but reorder heavy child first

---

#### 11. Typical Problem Archetypes

1. Standard application: map subtree ↔ array range
2. Slightly disguised: paint subtree, query point (diff array on tour)
3. Difficult: subtree + path mixed → HLD or two structures
4. Very difficult / advanced: Mo on trees with enter/exit

---

#### 12. Recognition & Identification Drills

1. Assign values to nodes; support “add \(x\) to subtree of \(v\)” and “value at \(u\)”.
2. Count nodes with color \(c\) in subtree of \(v\) (offline or static).
3. Check for each query whether \(a\) lies on the path from root to \(b\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any subtree ↔ contiguous range reduction
- Key invariant: DFS discovery order nests subtrees
- Key formula: subtree = `[tin[v], tout[v]]`
- Complexity: \(O(n)\) build
- Template to remember: `tin` on entry, process children, `tout = timer`

---

## 4. Subtree queries

---


---

<a id="topic-4"></a>
### 4. Subtree Queries

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Euler tour, Fenwick / segment tree  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Euler tour, Fenwick / segment tree

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

After Euler flattening, subtree sum = range sum; subtree add = range add. Point update + subtree query, or subtree update + point query, are classic Fenwick duals. Path queries are **not** subtree queries — route those to lifting, HLD, or difference-on-tree (`add u,v,lca`).

---

#### 4. Proof Sketches & Recurrences

Place node value at index `tin[v]`. Subtree sum = `query(tin[v], tout[v])`. Subtree add \(+x\): range update on that segment. Point query after subtree adds: Fenwick difference — `add(tin[v], x); add(tout[v]+1, -x)`, query prefix `tin[u]`.

Path sum root↔u: if you store values on Fenwick at `tin` and use inclusion with LCA carefully, or maintain `pref[u] = pref[parent]+val[u]` with Euler tricks. Prefer explicit tools (HLD / lifting) for arbitrary paths.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) tour + \(O(n)\) or \(O(n\log n)\) to load values
- Per-query / per-operation: \(O(\log n)\) Fenwick / segtree
- Total: \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Subtree sum / min / gcd after updates
- “Tax in region of capital’s subtree”
- Difference array: add on subtree ↔ add at `tin`, subtract at `tout+1`
- Rooted tree + operations “on v and descendants”

---

#### 7. Contest WA / TLE / RE Traps

- Updating `v`’s value at index `v` instead of `tin[v]`
- Subtree add without complementary `-x` at `tout+1`
- Path sum coded as subtree sum
- Lazy segtree wrong bounds (`tout` exclusive vs inclusive)
- Re-rooting online without rebuilding tour (tour is root-dependent)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Segtree / merge-sort tree** on Euler for “k-th in subtree”, distinct colors (with persistence)
- **Edge values:** store on child `tin[child]`
- **Subtree + path:** HLD or Euler for subtree + lifting for path
- **Offline DSU on tree** for heavy frequency queries (see Sack)

---

#### 11. Typical Problem Archetypes

1. Standard application: point update, subtree sum
2. Slightly disguised: company hierarchy bonuses
3. Difficult: subtree mex / majority — Sack or segtree-of-vectors
4. Very difficult / advanced: dynamic reroot + subtree structures

---

#### 12. Recognition & Identification Drills

1. Support assign value at node and query sum of subtree.
2. Add \(x\) on entire subtree; query single node value after many updates.
3. For each node, count how many nodes in its subtree have value \(> a_v\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: rooted subtree aggregates as ranges
- Key invariant: Euler segment = subtree
- Key formula: sum = Fenwick`[tin..tout]`; subtree add ↔ diff at `tin`/`tout+1`
- Complexity: \(O(\log n)\) per op
- Template to remember: DFS times + BIT on `tin`

---

## 5. Tree DP

---


---

<a id="topic-5"></a>
### 5. Tree DP

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2200 | **Frequency:** Very Common  
> **Prerequisites:** DP, DFS on trees  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: DP, DFS on trees

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Root the tree; combine children’s DP into parent with a merge that respects “subtrees are independent given the root choice”. Classic forms: knapsack-on-tree (\(O(n^2)\) merging sizes), independent set, matching, diameter via heights, “max path in subtree”. Think **post-order**: children first, then node.

---

#### 4. Proof Sketches & Recurrences

Example — max weight independent set:
\[
dp[v][0] = \sum_c \max(dp[c][0], dp[c][1]),\quad
dp[v][1] = w[v] + \sum_c dp[c][0]
\]
Knapsack merge: when attaching child size \(s_c\) to current size \(s\), update backup array in \(O(s\cdot s_c)\); total over tree \(O(n^2)\). Diameter: for each node, best two child-down paths.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: usually one DFS
- Total: \(O(n)\) typical; \(O(n^2)\) knapsack merges; \(O(n\cdot\text{state})\) otherwise
- Memory: \(O(n\cdot\text{state})\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Choose vertices with adjacency constraints”
- Budget/size limited selection in subtrees
- Ground/facility on tree, DP states at node
- Diameter, max matching, vertex cover on trees

---

#### 7. Contest WA / TLE / RE Traps

- Using parent as child (missing `to != p`)
- Merging knapsack in-place without temp → double counting
- Wrong transition when “must take root” / “edge vs vertex” DP
- Not handling leaves
- \(O(n^2)\) memory with `f[N][N]` — allocate by size

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Edge DP:** state on edges / reroot along edges
- **Digit / digit-like on tree:** combine with digit DP rare
- **Tree knapsack with convexity** → D&C opt (Section 04)
- **Matching / cover / coloring** standard transitions

---

#### 11. Typical Problem Archetypes

1. Standard application: independent set / dominating set on tree
2. Slightly disguised: party invitation with boss constraints
3. Difficult: knapsack group merges with size
4. Very difficult / advanced: DP on treewidth / virtual tree DP

---

#### 12. Recognition & Identification Drills

1. Max weight set of vertices with no two adjacent.
2. Choose exactly \(k\) vertices in a tree maximizing sum with no two adjacent.
3. Each node has a cost to “install”; cover all edges by installing endpoints — minimize cost.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: optimize over subsets/configs respecting tree edges
- Key invariant: child subtrees independent given root state
- Key formula: post-order combine \(\bigoplus_c dp[c]\)
- Complexity: usually \(O(n)\) or \(O(n^2)\) merges
- Template to remember: `dfs(v): for child: dfs; merge`

---

## 6. Rerooting DP

---


---

<a id="topic-6"></a>
### 6. Rerooting DP

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Common  
> **Prerequisites:** Tree DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Tree DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Compute a rooted DP once, then **transfer** the answer from root \(r\) to neighbor \(u\) in \(O(1)\) or \(O(\deg)\) using prefix/suffix aggregates of children — total \(O(n)\). Prefer rerooting when the answer is needed for **every** node as root. Prefer **two BFS/DFS** when you only need diameter, farthest node, or a single “best eccentricity” style fact.

---

#### 4. Proof Sketches & Recurrences

Example — sum of distances: first DFS `down[v]` = sum of distances in subtree, `sz[v]` sizes. Reroot:
\[
\mathrm{up\_sum}[u] = \mathrm{ans}[v] - (\mathrm{down}[u] + \mathrm{sz}[u]) + (n - \mathrm{sz}[u])
\]
when moving root from \(v\) to child \(u\): nodes in \(u\)’s subtree get \(-1\) distance, others \(+1\). General pattern: maintain contribution of “rest of tree” as a fake parent child.

Prefix/suffix max for “max path going through parent”: store child values array, prefix/suffix bests, DFS2 passes parent contribution.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: —
- Total: \(O(n)\) for associative merges; \(O(n\cdot\text{cost})\) if merge heavier
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “For each vertex, compute f(tree rooted at v)”
- Sum of distances to all nodes; max distance (eccentricity) for all v
- Reroot with associative child merges (sum, max, xor)
- Statement asks \(n\) answers, one per node

---

#### 7. Contest WA / TLE / RE Traps

- Wrong \(+1/-1\) on sizes when rerooting distances
- Forgetting to include parent contribution as a “virtual child”
- Using only `down` without second DFS
- Non-invertible merges — need prefix/suffix recompute \(O(\deg)\)
- Applying rerooting when 2-BFS suffices (wasted complexity)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Max eccentricity / tree center:** reroot max-down + up
- **Colored / weighted edges:** adjust ± formulas
- **Invertible vs non-invertible:** XOR/sum invertible; max needs prefix/suffix
- **Reroot + knapsack:** rare, expensive

---

#### 11. Typical Problem Archetypes

1. Standard application: sum of distances for every root
2. Slightly disguised: fuel/cost to visit all cities from each start
3. Difficult: reroot with max/second-max child paths
4. Very difficult / advanced: reroot with data structures hanging on nodes

---

#### 12. Recognition & Identification Drills

1. For each city \(v\), compute sum of distances to all other cities.
2. For each \(v\), compute the farthest distance from \(v\) (eccentricity).
3. Paint each edge; for each root, count pairs of same-color paths — need rethink (maybe not plain reroot).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: answer for every root, merge is reroot-friendly
- Key invariant: moving root across edge updates contributions by subtree size
- Key formula: `ans[child] = ans[par] - sz[child] + (n - sz[child])` (distances)
- Complexity: \(O(n)\)
- Template to remember: dfs1 down → dfs2 transfer; else 2-BFS for diameter-only

---

Continue with HLD, centroid, Sack, virtual trees in [06-b-tree-decompositions.md](06-b-tree-decompositions.md).

---


---

<a id="topic-7"></a>
### 7. Heavy-Light Decomposition (HLD)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Trees, Euler/DFS order, segment tree / Fenwick, LCA ideas  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Trees, Euler/DFS order, segment tree / Fenwick, LCA ideas

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Classify edges: **heavy** = to the child with largest subtree size; others **light**. Heavy paths are contiguous chains. Any root↔node path crosses \(O(\log n)\) light edges, hence \(O(\log n)\) heavy paths. Map each heavy path to a contiguous segment-tree interval (DFS: visit heavy child first). Path query/update = \(O(\log n)\) segments × segtree \(O(\log n)\) → \(O(\log^2 n)\). Prefer HLD for **online path + subtree** with a standard DS. Prefer **centroid** when the problem is D&C path counting without a living DS on paths.

---

#### 4. Proof Sketches & Recurrences

`sz[v]` via DFS. Heavy child: \(\arg\max sz[c]\). Second DFS assigns `head[v]` (top of heavy path), `pos[v]` (segtree index), increasing along heavy edges. Path \(u\!\to\!v\): while `head[u] != head[v]`, lift the deeper head: query `[pos[head[u]], pos[u]]`, then `u = parent[head[u]]`. Finally query the remaining chain between `u,v`. Subtree of \(v\) is contiguous `[pos[v], pos[v]+sz[v]-1]` if heavy-first DFS. Light edges \(\Rightarrow\) size at least halves → \(O(\log n)\) chains.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) HLD + \(O(n)\) (or \(O(n\log n)\)) segtree build
- Per-query / per-operation: \(O(\log^2 n)\) path; \(O(\log n)\) subtree/point
- Total: \(O(n + q\log^2 n)\)
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
// C++17 — HLD + iterative segment tree (path/subtree sum, point add)
// Full primary template for Section 06
namespace hld {
constexpr int N = 200005;
int n, timer;
int sz[N], dep[N], parent[N], heavy[N], head[N], pos[N];
vector<int> g[N];
long long base[N]; // values by node, placed at pos[v]

struct Seg {
    int n; vector<long long> t;
    void init(int n_) { n = n_; t.assign(2 * n, 0); }
    void build(long long *a) { // a[0..n-1]
        for (int i = 0; i < n; ++i) t[n + i] = a[i];
        for (int i = n - 1; i > 0; --i) t[i] = t[i << 1] + t[i << 1 | 1];
    }
    void add(int p, long long x) {
        for (t[p += n] += x; p > 1; p >>= 1) t[p] = t[p << 1] + t[p << 1 | 1];
    }
    long long query(int l, int r) { // inclusive
        long long res = 0;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res += t[l++];
            if (r & 1) res += t[--r];
        }
        return res;
    }
} seg;

int dfs_sz(int v, int p) {
    sz[v] = 1; parent[v] = p; heavy[v] = -1;
    int best = 0;
    for (int to : g[v]) if (to != p) {
        dep[to] = dep[v] + 1;
        int s = dfs_sz(to, v);
        sz[v] += s;
        if (s > best) best = s, heavy[v] = to;
    }
    return sz[v];
}

void dfs_hld(int v, int h) {
    head[v] = h;
    pos[v] = timer++;
    if (heavy[v] != -1) dfs_hld(heavy[v], h);
    for (int to : g[v])
        if (to != parent[v] && to != heavy[v]) dfs_hld(to, to);
}

void build(int root = 1) {
    timer = 0;
    dep[root] = 0;
    dfs_sz(root, 0);
    dfs_hld(root, root);
    vector<long long> arr(n);
    for (int v = 1; v <= n; ++v) arr[pos[v]] = base[v];
    seg.init(n);
    seg.build(arr.data());
}

long long path_query(int u, int v) {
    long long res = 0;
    while (head[u] != head[v]) {
        if (dep[head[u]] < dep[head[v]]) swap(u, v);
        res += seg.query(pos[head[u]], pos[u]);
        u = parent[head[u]];
    }
    if (dep[u] > dep[v]) swap(u, v);
    res += seg.query(pos[u], pos[v]); // node values; for edge values use pos[u]+1..pos[v]
    return res;
}

void path_add(int u, int v, long long x) { // needs lazy segtree; sketch with point adds only below
    // replace seg with lazy range-add if required
    (void)u; (void)v; (void)x;
}

void point_add(int v, long long x) { seg.add(pos[v], x); }

long long subtree_query(int v) {
    return seg.query(pos[v], pos[v] + sz[v] - 1);
}
} // namespace hld

/* Lazy range-add + range-sum (drop-in for path_add / range updates)
struct LazySeg {
    int n; vector<long long> t, lz;
    void init(int n_) { n = n_; t.assign(4*n+4,0); lz.assign(4*n+4,0); }
    void apply(int p, int l, int r, long long x) { t[p]+=x*(r-l+1); lz[p]+=x; }
    void push(int p, int l, int r) {
        if (!lz[p] || l==r) return;
        int m=(l+r)/2;
        apply(p<<1,l,m,lz[p]); apply(p<<1|1,m+1,r,lz[p]); lz[p]=0;
    }
    void add(int p, int l, int r, int ql, int qr, long long x) {
        if (qr<l||r<ql) return;
        if (ql<=l&&r<=qr) { apply(p,l,r,x); return; }
        push(p,l,r);
        int m=(l+r)/2;
        add(p<<1,l,m,ql,qr,x); add(p<<1|1,m+1,r,ql,qr,x);
        t[p]=t[p<<1]+t[p<<1|1];
    }
    long long query(int p, int l, int r, int ql, int qr) {
        if (qr<l||r<ql) return 0;
        if (ql<=l&&r<=qr) return t[p];
        push(p,l,r);
        int m=(l+r)/2;
        return query(p<<1,l,m,ql,qr)+query(p<<1|1,m+1,r,ql,qr);
    }
};
// path_add: same while-loop as path_query, calling lazy.add on [pos[head], pos[u]]
*/
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Path sum/min/xor + point or path updates, \(n,q\sim 10^5\)
- Mix of path and subtree operations on one tree
- “Chain decomposition”, “heavy child”
- Offline path problems that still scream segtree

---

#### 7. Contest WA / TLE / RE Traps

- Not visiting heavy child first → subtree ranges break
- Edge vs node values: path query must skip LCA node or use `pos[child]` on edges
- Comparing `dep[u]` instead of `dep[head[u]]` when lifting chains
- Forgetting `u = parent[head[u]]` after querying a chain
- Lazy segtree push bugs under path updates
- Root parent = 0; `head` of root = root

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Edge HLD:** store value at deeper endpoint
- **HLD + lazy** for path add / path assign
- **HLD + merge sort tree / Mo** rare
- **Multiple trees / forests:** run per component
- **Binary lifting path aggregates** — lighter if only static idempotent ops

---

#### 11. Typical Problem Archetypes

1. Standard application: path sum + point update
2. Slightly disguised: company chain of command salary queries
3. Difficult: path add + subtree query simultaneously
4. Very difficult / advanced: HLD on condensed trees / with virtual trees

---

#### 12. Recognition & Identification Drills

1. Tree; queries: add \(x\) on path \(u\!\to\!v\); report sum on path \(a\!\to\!b\).
2. Same, but also query sum of subtree of \(v\).
3. Edge weights; update one edge; query max edge on path (static max → lifting also works; with updates → HLD).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: online path DS ops, optionally + subtree
- Key invariant: \(O(\log n)\) heavy paths per path; heavy-first DFS contiguous
- Key formula: lift deeper `head` until same chain, then mid-segment
- Complexity: \(O(\log^2 n)\) per path op
- Template to remember: `dfs_sz` → `dfs_hld` → segtree on `pos` → while heads differ

---

## 8. Centroid decomposition

---


---

<a id="topic-8"></a>
### 8. Centroid Decomposition

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Trees, recursion/D&C, hashing/maps or arrays for freq  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Trees, recursion/D&C, hashing/maps or arrays for freq

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

A **centroid** of a tree (or remaining component) is a node whose removal leaves components of size \(\le |component|/2\). Recursively decompose: for each centroid, solve all paths that **pass through** it (usually by enumerating rooted depths/XOR/weights in pending components), then mark centroid dead and recurse. Layer depth \(O(\log n)\); each node appears in \(O(\log n)\) layers. Prefer centroid for **counting/enumerating paths** with a property. Prefer HLD when you need a mutable path data structure.

---

#### 4. Proof Sketches & Recurrences

Find size of component ignoring `dead[]`. Find centroid: walk from any node to a child with `sz > comp_sz/2` until none. Collect contributions: DFS into each alive neighbor subtree collecting bag of path-monoids to centroid; query bag against global map **before** inserting (avoid same-subtree pairs), then insert; clear after all neighbors; recurse. Complexity: each layer \(O(n\cdot f)\) work if maps careful → \(O(n\log n\cdot f)\). Centroid tree edges from centroid to child-centroids form a tree of height \(O(\log n)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build once \(O(n\log n)\) layers
- Per-query / per-operation: usually baked into decompose
- Total: \(O(n\log n\cdot f)\) where \(f\) = cost per node visit (often \(O(1)\) or \(O(\log n)\) map)
- Memory: \(O(n)\) + maps`

##### C++17 Template

```cpp
// C++17 — centroid decomposition: count unordered pairs with dist == K
// Full primary template for Section 06
namespace centroid {
constexpr int N = 200005;
int n, K, sz[N];
bool dead[N];
vector<int> g[N];
long long answer = 0;

int dfs_sz(int v, int p) {
    sz[v] = 1;
    for (int to : g[v]) if (to != p && !dead[to]) sz[v] += dfs_sz(to, v);
    return sz[v];
}

int dfs_centroid(int v, int p, int comp) {
    for (int to : g[v]) if (to != p && !dead[to] && sz[to] > comp / 2)
        return dfs_centroid(to, v, comp);
    return v;
}

void dfs_depths(int v, int p, int d, vector<int>& bag) {
    if (d > K) return;
    bag.push_back(d);
    for (int to : g[v]) if (to != p && !dead[to]) dfs_depths(to, v, d + 1, bag);
}

void solve_centroid(int c) {
    // freq[d] = how many nodes at distance d from c already processed
    // Use array if K small; else hashmap. Here K < N assumed optional — use map-like vector.
    static int freq[N]; // clear carefully by touched list
    vector<int> touched;
    auto add_freq = [&](int d, int delta) {
        if (freq[d] == 0 && delta > 0) touched.push_back(d);
        freq[d] += delta;
    };

    // paths with endpoint = c
    add_freq(0, 1);

    for (int to : g[c]) if (!dead[to]) {
        vector<int> bag;
        dfs_depths(to, c, 1, bag);
        for (int d : bag) {
            if (K - d >= 0) answer += freq[K - d]; // pairs across different branches + to c
        }
        for (int d : bag) add_freq(d, 1);
    }
    for (int d : touched) freq[d] = 0;
}

void decompose(int entry) {
    int comp = dfs_sz(entry, -1);
    int c = dfs_centroid(entry, -1, comp);
    solve_centroid(c);
    dead[c] = true;
    for (int to : g[c]) if (!dead[to]) decompose(to);
}

long long count_paths_of_length(int k) {
    K = k;
    answer = 0;
    fill(dead, dead + n + 1, false);
    decompose(1);
    return answer;
}
} // namespace centroid

/* General pattern for XOR / weighted:
   - bag stores path_xor to centroid
   - query map[need ^ x] before inserting
   - unordered_map or fixed arrays by value domain
   Centroid tree parent:
   int cpar[N];
   // when recurse into component, cpar[child_centroid] = c;
*/
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Count pairs/paths with length \(=k\), XOR \(=x\), weight in range
- “Paths through a separator”, divide-and-conquer on trees
- Offline path statistics without updates
- Balanced separator on trees (size-halving)

---

#### 7. Contest WA / TLE / RE Traps

- Counting pairs inside the same subtree twice — **query before insert** per branch
- Forgetting `dead[]` when computing sizes
- Not clearing frequency structures (use touched lists)
- Off-by-one on path length (nodes vs edges)
- Recursing into `to` before marking centroid dead
- Using global `sz` without recomputing per component

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Centroid tree** as auxiliary tree for \(O(\log n)\) “jump” structures
- **XOR / and / gcd** path counts via maps at centroid
- **With updates:** harder — often BIT on centroid tree + reconstruction
- **Edge-weighted distances** in DFS collect

---

#### 11. Typical Problem Archetypes

1. Standard application: number of paths of length \(k\)
2. Slightly disguised: number of paths with XOR \(=x\)
3. Difficult: count paths with length in \([L,R]\) (prefix freq)
4. Very difficult / advanced: dynamic centroid / offline with BIT on layers

---

#### 12. Recognition & Identification Drills

1. Count simple paths with exactly \(k\) edges.
2. Count paths whose XOR of edge weights equals \(x\).
3. Find whether there is a path with sum of weights in a given set of targets.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: path counting / D&C by separator, not mutable path DS
- Key invariant: centroid splits sizes by \(\ge 1/2\); paths through centroid handled once
- Key formula: per branch query-then-insert into freq at centroid
- Complexity: \(O(n\log n\cdot f)\)
- Template to remember: `sz` → `centroid` → solve through-c → `dead[c]=1` → recurse

---

## 9. DSU on tree / Sack

---


---

<a id="topic-9"></a>
### 9. DSU on Tree (Sack)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Euler tour / DFS, tree sz, frequency maps  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Euler tour / DFS, tree sz, frequency maps

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Compute offline answers for **every subtree** by keeping a frequency map of values. DFS heavy child first **without clearing**; then add light subtrees; answer; if current node is not heavy child of parent, clear. Light edges clear \(O(\log n)\) times per node → \(O(n\log n)\) updates. Prefer Sack for **all-subtree frequency** problems. Prefer **virtual tree** when only \(k\ll n\) key nodes matter. Prefer Euler+Mo for harder non-additive offline queries.

---

#### 4. Proof Sketches & Recurrences

`sz` + heavy child as in HLD. `dfs(v, keep)`:
1. Process all light children with `keep=false`.
2. Process heavy child with `keep=true`.
3. Add light children’s nodes into the global map (re-DFS add).
4. Add `v` itself; write `ans[v]`.
5. If `!keep`, remove entire subtree of `v` from the map.

Each node added/removed once per light ancestor → \(O(n\log n)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) sizes/times
- Per-query / per-operation: offline all answers
- Total: \(O(n\log n\cdot \alpha)\) where \(\alpha\) = add/rem cost
- Memory: \(O(n)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- For every \(v\), something about multiset of colors/values in subtree
- Dominant color, mex, number of distinct, mode
- “DSU on tree”, “small-to-large on tree”, Sack
- Offline only; no path queries

---

#### 7. Contest WA / TLE / RE Traps

- Clearing after heavy child incorrectly
- Adding light subtrees before processing heavy
- Forgetting to add node `v` itself
- `keep=true` on root call when you still need a clean map afterward
- Using path structures — Sack is subtree-only

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Mode / sum of frequencies with f(freq)** — maintain extra aggregates on freq changes
- **Mex of subtree:** track freq of values + set of missing
- **Small-to-large with maps of maps** (merge maps by size) — similar complexity, different code
- **Sack + segtree** hanging values

---

#### 11. Typical Problem Archetypes

1. Standard application: distinct colors per subtree
2. Slightly disguised: most frequent color in each subtree
3. Difficult: mex of values in each subtree
4. Very difficult / advanced: Sack with heavy algebra on frequencies

---

#### 12. Recognition & Identification Drills

1. For each node, count distinct colors in its subtree.
2. For each node, find the sum of values that appear exactly once in its subtree.
3. For each node, compute mex of the set of colors in its subtree.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: offline answer for every subtree multiset
- Key invariant: keep heavy child’s map; light cleared \(O(\log n)\) times
- Key formula: light → heavy(keep) → add lights → answer → clear if !keep
- Complexity: \(O(n\log n\cdot\alpha)\)
- Template to remember: same heavy child as HLD + keep flag

---

## 10. Virtual trees

---


---

<a id="topic-10"></a>
### 10. Virtual Trees (Compressed Trees)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 2200–2800 | **Frequency:** Occasional  
> **Prerequisites:** LCA, Euler `tin`, stack construction  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: LCA, Euler `tin`, stack construction

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Given \(k\) key nodes, the **virtual tree** is the tree on those keys plus their pairwise LCAs, with only compression edges between them. Size \(O(k)\). Build by sorting keys by `tin`, stacking LCAs. Then run DP only on \(O(k)\) nodes instead of \(n\). Prefer virtual trees when **many queries each with few keys**. Prefer Sack when every subtree of the full tree needs an answer.

---

#### 4. Proof Sketches & Recurrences

Sort unique keys by `tin`. Stack maintains a chain of virtual-tree ancestors. For next key \(x\): while stack top is not ancestor of \(x\), pop (connecting edges). Insert LCA(`stack.top`, `x`) if needed, then push \(x\). Each key and each LCA inserted \(O(1)\) amortized → \(O(k\log n)\) with LCA. DP on built adjacency (undirected edges between parent links). Clear virtual adjacency after each query.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: LCA + tin \(O(n\log n)\)
- Per-query / per-operation: \(O(k\log n)\) build + \(O(k\cdot\text{DP})\)
- Total: \(O(n\log n + \sum k\log n)\)
- Memory: \(O(n + k)\) per query if cleared`

##### C++17 Template

```cpp
// C++17 — virtual tree construction + cleanup (needs lca_bl + euler tin)
namespace vtree {
constexpr int N = 200005;
int n;
vector<int> g[N];          // original
vector<int> virt[N];       // virtual edges
int tin[N], timer_e;
// assume lca_bl::lca, lca_bl::dep available; tin from euler tour

void dfs_tin(int v, int p) {
    tin[v] = ++timer_e;
    for (int to : g[v]) if (to != p) dfs_tin(to, v);
}

bool anc(int a, int b) { // need tout OR use lca: lca(a,b)==a
    return lca_bl::lca(a, b) == a;
}

vector<int> nodes; // reusable buffer of involved nodes for cleanup

void add_edge(int u, int v) {
    virt[u].push_back(v);
    virt[v].push_back(u);
}

void build(vector<int> key) {
    sort(key.begin(), key.end(), [](int a, int b) { return tin[a] < tin[b]; });
    key.erase(unique(key.begin(), key.end()), key.end());
    nodes = key;
    vector<int> st;
    auto ensure = [&](int x) {
        nodes.push_back(x);
    };
    for (int x : key) {
        if (st.empty()) { st.push_back(x); continue; }
        int w = lca_bl::lca(x, st.back());
        if (w != st.back()) {
            while (st.size() >= 2 && tin[st[st.size() - 2]] >= tin[w]) {
                add_edge(st[st.size() - 2], st.back());
                st.pop_back();
            }
            if (st.back() != w) {
                add_edge(w, st.back());
                st.pop_back();
                ensure(w);
                st.push_back(w);
            }
        }
        st.push_back(x);
    }
    while (st.size() >= 2) {
        add_edge(st[st.size() - 2], st.back());
        st.pop_back();
    }
}

void clear() {
    for (int v : nodes) virt[v].clear();
    nodes.clear();
}

// Example DP stub: sum of edge lengths in virtual tree (Steiner for keys)
// long long dp(int v, int p) { ... use lca_bl::dep[u]+dep[v]-2*dep[lca] for real distance }
} // namespace vtree
```

---

#### 6. Recognition Trigger Signals & Heuristics

- \(q\) queries, each with \(k_i\) important vertices, \(\sum k_i \le 10^5\)–\(2\cdot10^6\)
- DP / cost only depends on keys and LCAs between them
- “Steiner tree on tree”, key cities, important nodes
- Compress tree between specials

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to include LCAs as vertices
- Not sorting by `tin`
- Leaving stale `virt` edges between queries
- Duplicate keys
- Treating virtual edge weight as 1 instead of real tree distance
- Stack LCA cases off-by-one (need careful casework — test on chains)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Virtual tree + DP** for virus/infection, key black nodes
- **Only keys that are leaves of virtual tree** sometimes
- **Kruskal reconstruction + virtual** for max-edge queries among keys
- **Build with sparse table LCA \(O(1)\)**

---

#### 11. Typical Problem Archetypes

1. Standard application: cost of connecting \(k\) cities along tree (Steiner = virtual tree edges)
2. Slightly disguised: queries with important festivals on nodes
3. Difficult: DP “cut edges so keys in different components”
4. Very difficult / advanced: virtual tree + HLD / segment trees on compressed nodes

---

#### 12. Recognition & Identification Drills

1. \(q\) queries each listing \(k\) nodes; for each, compute the size of the minimal subtree containing all of them (number of edges).
2. Same keys; compute min edges to remove to isolate all keys into singleton components.
3. Multiple queries of key sets; count pairs of keys whose path passes through a given fixed node type — compress first.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: many queries, few keys each, DP on keys+LCAs
- Key invariant: sorted by `tin`, stack maintains ancestral chain; size \(O(k)\)
- Key formula: build \(O(k\log n)\); edge weight = tree distance
- Complexity: \(O(n\log n + \sum k\log n)\)
- Template to remember: sort keys → stack + LCA inserts → DP → clear

---

## End drills (part B focus)

1. Code HLD path sum + point update from scratch once; then add lazy path add.
2. Code centroid count-paths-of-length-\(k\); mutate to XOR\(=x\).
3. Code Sack distinct colors; extend to mode.
4. Code virtual tree builder; verify size \(O(k)\) on random keys; one Steiner-length query.

Back to index: [06-trees.md](06-trees.md) · Core techniques: [06-a-trees-core.md](06-a-trees-core.md).

---


---

<a id="topic-11"></a>
### 11. What to drill this week

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2400
- Prerequisites: Tree traversals, LCA, Euler Tour, Heavy-Light Decomposition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

##### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

##### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

##### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

##### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

#### 3. Core Intuition & Problem Framing

Tree algorithms in rated contests test structural reductions: converting arbitrary tree paths or subtree aggregates into contiguous ranges on an array via Euler tours and heavy paths. Master binary lifting for static tree paths, subtree difference arrays for subtree updates, and HLD for dynamic path operations.

---

#### 4. Proof Sketches & Recurrences

A rooted tree of $N$ vertices can be linearized into an Euler tour of length $N$ or $2N$. For any vertex $u$, its subtree corresponds to the contiguous interval $[\text{tin}[u], \text{tout}[u]]$. Any path $u \leftrightarrow v$ decomposes into $\mathcal{O}(\log N)$ contiguous segments under Heavy-Light Decomposition.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Queries over arbitrary tree paths $u \leftrightarrow v$ with point or range updates.
- Subtree color frequency counting (DSU on Tree / Small-to-Large merging).
- Path bottleneck queries where edge weights represent capacities or tolerances.
- Distance queries among dynamically added or deleted nodes (Centroid Tree).

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting 1-based vs 0-based indexing on tree Euler tours.
- Rooting the tree at an arbitrary vertex when directed edges require topological ordering.
- LCA query fails when start and end vertices are identical ($u = v$).
- Stack overflow in deep skew trees without `#pragma comment(linker)` or manual iterative DFS.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---


---
