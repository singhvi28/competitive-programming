# 5. Floyd–Warshall

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** DP on pairs, adjacency matrix  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: DP on pairs, adjacency matrix

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

## 3. Core Intuition & Problem Framing

`dp[k][i][j]` = shortest \(i\to j\) using intermediate nodes from \(\{1..k\}\). Rolling away \(k\) yields the classic triple loop. Dense all-pairs, easy negative-cycle check (`dist[i][i] < 0`), easy “add vertex/edge online” variants by running the same recurrence.

---

## 4. Proof Sketches & Recurrences

\[
d_{ij}^{(k)} = \min\bigl(d_{ij}^{(k-1)},\, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\bigr)
\]
After \(k=n\), all simple intermediates allowed; neg cycle ⇒ some \(d_{ii}<0\). Semiring variants: replace \((\min,+)\) by \((\max,\min)\) for bottleneck, etc.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: matrix init \(O(n^2)\)
- Per-query / per-operation: after FW, \(O(1)\) pair query
- Total: \(O(n^3)\)
- Memory: \(O(n^2)\)`

### C++17 Template

```cpp
namespace floyd {
using ll = long long;
const ll INF = 4e18;

void all_pairs(int n, vector<vector<ll>>& d) {
    // d[i][j] = w or INF; d[i][i] = 0
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            if (d[i][k] < INF)
                for (int j = 0; j < n; ++j)
                    if (d[k][j] < INF)
                        d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
}

bool has_neg_cycle(int n, const vector<vector<ll>>& d) {
    for (int i = 0; i < n; ++i)
        if (d[i][i] < 0) return true;
    return false;
}
} // namespace floyd
```

---

## 6. Recognition Trigger Signals & Heuristics

- \(n \le 400\) (sometimes 500 if tight / bitset tricks)
- Need all-pairs or many pairs and graph dense
- Minimax / maximin path variants (change `min`/`max` algebra)
- Closure-like problems (reachability with OR-AND)

---

## 7. Contest WA / TLE / RE Traps

- Not setting `d[i][i]=0`; missing undirected edges both ways
- Overflow on `d[i][k]+d[k][j]` — guard with INF checks
- \(n=500\) without constant-care → TLE
- Forgetting neg self-loop after FW means reachable neg cycle only if you care about that component

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

## 10. Algorithmic Variants & Advanced Extensions

- Path reconstruction with `nxt[i][j]`
- **Offline add edges** from heavy to light / process reverse deletions
- Bottleneck: `d[i][j] = min(d[i][j], max(d[i][k], d[k][j]))`
- Transitive closure: boolean FW

---

## 11. Typical Problem Archetypes

1. Standard application: all-pairs shortest paths, small \(n\)
2. Slightly disguised: min max-edge between all pairs (bottleneck FW)
3. Difficult: FW DP on “using first k cities as hubs”
4. Very difficult / advanced: combine with bitsets for reachability counts

---

## 12. Recognition & Identification Drills

1. \(n=300\) directed graph; answer \(q=n^2\) distance queries.
2. Find if any negative cycle exists in a dense graph.
3. For each pair, minimum possible “worst edge” on a path.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: dense / small \(n\) all-pairs
- Key invariant: intermediates \(1..k\) processed
- Key formula: `d[i][j] = min(d[i][j], d[i][k]+d[k][j])`
- Complexity: \(O(n^3)\)
- Template to remember: `k,i,j` triple loop

---

---
