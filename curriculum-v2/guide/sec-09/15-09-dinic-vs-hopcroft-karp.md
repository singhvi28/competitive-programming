# 15. Dinic vs Hopcroft–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Bipartite Matching, Dinic's Algorithm, Hopcroft-Karp
- Tradeoff: Hopcroft-Karp is mathematically identical to Dinic on unit bipartite networks; knowing this saves memorizing two separate algorithms.

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

Hopcroft-Karp is specifically Dinic's algorithm specialized for bipartite matching networks. In a bipartite graph with unit capacity edges, Dinic's level graph BFS finds shortest alternating paths from unmatched left nodes to unmatched right nodes, and the DFS augments along vertex-disjoint paths in $\mathcal{O}(E \sqrt{V})$ time. Dinic's algorithm achieves this exact same $\mathcal{O}(E \sqrt{V})$ bound naturally on unit networks without requiring a bespoke Hopcroft-Karp implementation.

---

## 4. Proof Sketches & Recurrences

In unit bipartite graphs, every vertex in $L \cup R$ has either in-degree 1 or out-degree 1 in the residual network. Therefore, augmenting paths in a single phase are strictly vertex-disjoint. After $k$ phases of augmentation, the length of the shortest augmenting path is at least $k + 1$, and the difference between the current matching $M$ and maximum matching $M^*$ satisfies $|M^* \setminus M| \le V / k$. Balancing $k = \sqrt{V}$ yields $\mathcal{O}(\sqrt{V})$ phases, with $\mathcal{O}(E)$ work per phase.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Hopcroft-Karp Bipartite Matching via Dinic or Dedicated Array HK
#include <bits/stdc++.h>
using namespace std;

struct HopcroftKarp {
    int n, m; // Sizes of left (1..n) and right (1..m) sets
    vector<vector<int>> adj;
    vector<int> pair_u, pair_v, dist;
    HopcroftKarp(int n_, int m_) : n(n_), m(m_), adj(n_ + 1), pair_u(n_ + 1, 0), pair_v(m_ + 1, 0), dist(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); }
    bool bfs() {
        queue<int> q;
        for (int u = 1; u <= n; ++u) {
            if (pair_u[u] == 0) { dist[u] = 0; q.push(u); }
            else dist[u] = INT_MAX;
        }
        dist[0] = INT_MAX;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            if (dist[u] < dist[0]) {
                for (int v : adj[u]) {
                    if (dist[pair_v[v]] == INT_MAX) {
                        dist[pair_v[v]] = dist[u] + 1;
                        q.push(pair_v[v]);
                    }
                }
            }
        }
        return dist[0] != INT_MAX;
    }
    bool dfs(int u) {
        if (u == 0) return true;
        for (int v : adj[u]) {
            if (dist[pair_v[v]] == dist[u] + 1 && dfs(pair_v[v])) {
                pair_v[v] = u; pair_u[u] = v;
                return true;
            }
        }
        dist[u] = INT_MAX;
        return false;
    }
    int max_matching() {
        int matching = 0;
        while (bfs()) for (int u = 1; u <= n; ++u) if (pair_u[u] == 0 && dfs(u)) matching++;
        return matching;
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Bipartite graph matching where $N, M \le 5 \times 10^4$ and $E \le 2 \times 10^5$ (Kuhn's $\mathcal{O}(V E)$ will TLE; Hopcroft-Karp/Dinic passes in 100ms).
- Maximum Independent Set on bipartite graph ($|MIS| = |V| - |\text{Max Matching}|$).
- Minimum Vertex Cover on bipartite graph (Kőnig's Theorem: $|\text{MVC}| = |\text{Max Matching}|$).
- Minimum Path Cover in a Directed Acyclic Graph (DAG).

---

## 7. Contest WA / TLE / RE Traps

- Off-by-one indexing on 0-based vs 1-based left/right partitions (Hopcroft-Karp uses index 0 as dummy unmatched node).
- Graph is not bipartite: applying Hopcroft-Karp or Dinic bipartite reduction on general graphs with odd cycles fails (requires Edmond's Blossom).
- Forgetting to reconstruct minimum vertex cover by DFS reachability from unmatched left vertices in residual graph.
- Reusing `dist` array across iterations without re-clearing.

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
