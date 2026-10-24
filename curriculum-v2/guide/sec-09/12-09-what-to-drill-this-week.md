# What to drill this week

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2500
- Prerequisites: Max Flow, Min-Cut, Bipartite Matching, Project Selection

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

Flow networks solve resource allocation, constraint satisfiability, and bipartite assignment. The central contest paradigm is the **Max-Flow Min-Cut Theorem**: finding maximum flow from source to sink simultaneously identifies the minimum capacity edge set whose removal disconnects source from sink.

---

## 4. Proof Sketches & Recurrences

Dinic's algorithm constructs a layered level graph via BFS and finds blocking flows via DFS with current-arc optimization. It runs in $\mathcal{O}(V^2 E)$ generally and strictly in $\mathcal{O}(E \sqrt{V})$ on unit capacity networks.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Dinic Blocking Flow Algorithm with Current-Arc Pruning
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

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
            for (auto& e : adj[v]) {
                if (e.cap - e.flow > 0 && level[e.to] == -1) {
                    level[e.to] = level[v] + 1; q.push(e.to);
                }
            }
        }
        return level[t] != -1;
    }
    ll dfs(int v, ll pushed) {
        if (pushed == 0 || v == t) return pushed;
        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {
            auto& e = adj[v][cid];
            if (level[v] + 1 != level[e.to] || e.cap - e.flow == 0) continue;
            ll tr = dfs(e.to, min(pushed, e.cap - e.flow));
            if (tr == 0) continue;
            e.flow += tr; adj[e.to][e.rev].flow -= tr;
            return tr;
        }
        return 0;
    }
    ll max_flow() {
        ll flow = 0;
        while (bfs()) {
            fill(ptr.begin(), ptr.end(), 0);
            while (ll pushed = dfs(s, INF)) flow += pushed;
        }
        return flow;
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Project Selection: picking items with positive profits and prerequisite costs.
- Maximum Bipartite Matching: assigning students to mentors, tasks to processors.
- Minimum Path Cover in DAGs: decomposing tasks into disjoint execution paths.
- Grid cell coloring / chessboard adjacency reductions (bipartite cuts).

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to add backward edge with 0 initial capacity.
- Omitting current-arc pointers `ptr[v]` in Dinic's DFS, degrading $\mathcal{O}(V^2 E)$ to $\mathcal{O}(V E^2)$.
- Integer overflow when adding large capacities: use `long long` for all flow variables.
- Incorrect Min-Cut vertex reconstruction: cut consists of edges $(u, v)$ where `level[u] != -1` and `level[v] == -1`.

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
