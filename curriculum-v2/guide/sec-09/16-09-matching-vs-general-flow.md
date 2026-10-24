# 16. Matching vs General Flow

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Max Flow, Bipartite Matching, General Matching (Blossom), Capacitated Networks
- Tradeoff: Deciding between specialized bipartite matching, general graph matching, and general network flow models.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

## 3. Core Intuition & Problem Framing

When encountering an assignment problem, check graph structure: 1) Is the graph bipartite? If yes and unweighted, use Hopcroft-Karp or Dinic $\mathcal{O}(E \sqrt{V})$. 2) Is it bipartite with edge costs? Use Hungarian algorithm $\mathcal{O}(V^3)$ or MCMF $\mathcal{O}(F \cdot E \log V)$. 3) Is the graph general (non-bipartite, odd cycles present)? Bipartite matching and network flow FAIL! You must use Blossom Algorithm $\mathcal{O}(V^3)$ or Tutte matrix randomized matching. 4) Do vertices or edges have capacities $> 1$, or intermediate transit nodes? General network flow is mandatory.

---

## 4. Proof Sketches & Recurrences

Max flow models rely on the total unimodularity of bipartite incidence matrices: the linear programming relaxation has integral extreme points. In general non-bipartite graphs, odd cycles introduce fractional vertices (e.g., triangle with 0.5 flow on each edge gives 1.5 matching, impossible for discrete matching). Edmonds' Blossom algorithm contracts odd cycles into supernodes to restore augmenting path properties.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Decision Matrix Dispatcher
// General Network Flow vs Bipartite Matching
#include <bits/stdc++.h>
using namespace std;

// Check if graph is 2-colorable (bipartite)
bool is_bipartite(int n, const vector<vector<int>>& adj, vector<int>& color) {
    color.assign(n + 1, -1);
    for (int i = 1; i <= n; ++i) {
        if (color[i] != -1) continue;
        queue<int> q; q.push(i); color[i] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) return false; // Odd cycle found!
            }
        }
    }
    return true;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Grid cells where interactions occur only between adjacent cells (grids are naturally bipartite: $(r + c) \pmod 2$).
- Domino tiling problems: bipartite matching between black and white checkerboard squares.
- Pairing items where relationships form arbitrary non-bipartite friendship graphs (requires Blossom).
- Multi-commodity or capacitated bounds per node: split node into $u_{\text{in}} \to u_{\text{out}}$ with capacity $c_u$.

---

## 7. Contest WA / TLE / RE Traps

- Modeling general matching (odd cycles present) as a flow network: flow networks cannot handle non-bipartite vertex packing.
- Forgetting node capacities: to restrict a vertex to be used at most $K$ times, split $u \to (u_{in}, u_{out})$ with capacity $K$.
- Ignoring disconnected components when checking bipartiteness.
- Attempting to run Blossom algorithm when the constraints indicate $N \le 500$, but simple DP on tree or greedy would suffice.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---
