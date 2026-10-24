# 14. Dinic vs Edmonds–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Max-Flow / Min-Cut
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Augmenting Paths, BFS, DFS, Level Graphs, Blocking Flows
- Tradeoff: Edmonds-Karp runs in $\mathcal{O}(V E^2)$ (too slow for $N > 100$); Dinic's runs in $\mathcal{O}(V^2 E)$, and $\mathcal{O}(E \sqrt{V})$ on unit capacity graphs.

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

Both Edmonds-Karp and Dinic find shortest augmenting paths using BFS. However, Edmonds-Karp finds a single augmenting path per BFS traversal and immediately updates residual capacities. Dinic decomposes the computation: a single BFS constructs a *level graph* (DAG of shortest paths), and a DFS with pointer work finds a *blocking flow* (saturating multiple augmenting paths simultaneously in the same level graph). Once blocked, the source-sink distance strictly increases by $\ge 1$. Thus, Dinic requires at most $V - 1$ BFS phases.

---

## 4. Proof Sketches & Recurrences

In Dinic's algorithm, the distance from source $S$ to sink $T$ in the level graph strictly increases after each phase: $dist_{k+1}(S, T) > dist_k(S, T)$. Hence there are at most $V - 1$ phases. In each phase, the DFS advances along unsaturated edges; whenever an edge is saturated or a dead-end is reached, the current-arc pointer increments. Across the phase, total time spent retreating is $\mathcal{O}(V E)$ and total time advancing is $\mathcal{O}(V E)$, giving $\mathcal{O}(V E)$ per phase, or $\mathcal{O}(V^2 E)$ total. On unit capacity networks, the number of phases is $\mathcal{O}(\sqrt{V})$ or $\mathcal{O}(E^{1/2})$, yielding $\mathcal{O}(E \sqrt{V})$ or $\mathcal{O}(E \min(V^{2/3}, E^{1/2}))$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Dinic's Algorithm (Fast competitive programming standard)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Dinic {
    struct Edge { int to; ll cap, flow; int rev; };
    int n, s, t;
    vector<vector<Edge>> adj;
    vector<int> level, ptr;
    Dinic(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1), level(n_ + 1), ptr(n_ + 1) {}
    void add_edge(int from, int to, ll cap) {
        adj[from].push_back({to, cap, 0, (int)adj[to].size()});
        adj[to].push_back({from, 0, 0, (int)adj[from].size() - 1});
    }
    bool bfs() {
        fill(level.begin(), level.end(), -1);
        level[s] = 0; queue<int> q; q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (auto& edge : adj[v]) {
                if (edge.cap - edge.flow > 0 && level[edge.to] == -1) {
                    level[edge.to] = level[v] + 1;
                    q.push(edge.to);
                }
            }
        }
        return level[t] != -1;
    }
    ll dfs(int v, ll pushed) {
        if (pushed == 0 || v == t) return pushed;
        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {
            auto& edge = adj[v][cid];
            int trg = edge.to;
            if (level[v] + 1 != level[trg] || edge.cap - edge.flow == 0) continue;
            ll tr = dfs(trg, min(pushed, edge.cap - edge.flow));
            if (tr == 0) continue;
            edge.flow += tr;
            adj[trg][edge.rev].flow -= tr;
            return tr;
        }
        return 0;
    }
    ll max_flow() {
        ll flow = 0;
        while (bfs()) {
            fill(ptr.begin(), ptr.end(), 0);
            while (ll pushed = dfs(s, 1e18)) flow += pushed;
        }
        return flow;
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Network capacity graph with $V \le 5000, E \le 30000$ where Edmonds-Karp would TLE.
- Unit network matching (e.g., bipartite matching via flow) where Dinic executes in blinding $\mathcal{O}(E \sqrt{V})$ speed.
- Project selection problem (closure graph with positive weights to source, negative to sink).
- Minimum cut partitioning where min-cut capacity equals max flow.

---

## 7. Contest WA / TLE / RE Traps

- Omitting the current-arc pointer `int& cid = ptr[v]` in DFS, degenerating Dinic to Edmonds-Karp complexity $\mathcal{O}(V E^2)$.
- Forgetting that backward residual edge has capacity 0 initially (`adj[to].push_back({from, 0, 0, ...})`) for directed graphs.
- Integer overflow: capacities or flow sum exceed $2^{31} - 1$; always use `long long` for `cap` and `flow`.
- Resetting `ptr` inside BFS rather than before the blocking DFS loop.

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
