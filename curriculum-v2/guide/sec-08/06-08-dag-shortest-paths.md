# DAG Shortest Paths

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2000 | **Frequency:** Common  
> **Prerequisites:** Topological sort, DP on DAGs  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2000
- Prerequisites: Topological sort, DP on DAGs

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

On a DAG, process vertices in topo order; each edge relaxes forward once. Works with **negative weights** (no cycles at all). Same skeleton as longest path on DAG (flip to max). Many “DP on graph” problems are exactly this.

---

## 4. Proof Sketches & Recurrences

Topo order ensures when you process \(u\), all incoming paths are finalized if you relax outgoing, or dually: relax edges when popping \(u\). \(O(n+m)\). Negatives fine; no need BF.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: topo \(O(n+m)\)
- Per-query / per-operation: \(O(n+m)\) after topo (or same pass)
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace dag_sp {
using ll = long long;
const ll INF = 4e18;

// g must be a DAG; returns dist from src (INF = unreachable)
vector<ll> shortest(int n, int src,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u)
        for (auto [v, w] : g[u]) indeg[v]++;
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (!indeg[i]) q.push(i);
    vector<int> order;
    order.reserve(n);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto [v, w] : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    vector<ll> dist(n, INF);
    dist[src] = 0;
    for (int u : order) {
        if (dist[u] == INF) continue;
        for (auto [v, w] : g[u])
            dist[v] = min(dist[v], dist[u] + w);
    }
    return dist;
}
} // namespace dag_sp
```

---

## 6. Recognition Trigger Signals & Heuristics

- Explicit DAG or SCC condensation
- Tasks with precedence constraints
- Longest path in project network
- Grid DP moving only right/down (implicit DAG)

---

## 7. Contest WA / TLE / RE Traps

- Graph not actually DAG (need SCC first)
- Relaxing before topo readiness
- Longest path: forgetting to init reachable nodes to 0 / -INF correctly
- Multiple sources: init all sources to 0 then one topo pass

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

- Longest path: `max` and `-INF` init
- Count paths while relaxing
- DP on condensation DAG of SCCs
- Lexicographically shortest path via parent ties

---

## 11. Typical Problem Archetypes

1. Standard application: shortest/longest path in DAG
2. Slightly disguised: nested segments / precedence
3. Difficult: DP on DAG with extra state
4. Very difficult / advanced: optimize DAG DP with CHT along topo

---

## 12. Recognition & Identification Drills

1. Directed graph guaranteed acyclic; edge weights may be negative — shortest paths.
2. Maximum points collecting quests with prerequisites.
3. After SCC compression, path among components with weights.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: DAG (or condensation)
- Key invariant: topo order finalizes DP
- Key formula: relax in topo order
- Complexity: \(O(n+m)\)
- Template to remember: Kahn/DFS topo + one relax pass

---

---
