# Dinic’s Algorithm

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow / residual graphs, BFS + DFS  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Max flow / residual graphs, BFS + DFS

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

Don’t recompute shortest paths from scratch naively for every single edge push. Build a **level graph** by BFS on residual edges (distance from \(s\)). Then send a **blocking flow**: DFS only along edges \(u\to v\) with \(\mathrm{level}[v]=\mathrm{level}[u]+1\), advancing a current-edge pointer so each edge is scanned amortized \(O(1)\) per phase. When no more flow in the level graph, rebuild levels. Phases are few in practice; on unit networks the algorithm is especially fast.

---

## 4. Proof Sketches & Recurrences

Phase: BFS levels \(O(E)\). Blocking flow with current-arc DFS: \(O(VE)\) worst-case per phase. Number of phases \(O(V)\) → \(O(V^2E)\).

Unit-capacity / simple networks: \(O(\min(V^{2/3}, E^{1/2})E)\) style bounds; bipartite matching via Dinic: \(O(E\sqrt V)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) per edge
- Per-query / per-operation: \(O(V^2E)\) worst-case; much faster typical / unit
- Total: one max flow as above
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready — Dinic
namespace dinic {
struct Edge { int to, rev; long long cap; };
struct Dinic {
  int n, s, t;
  vector<vector<Edge>> g;
  vector<int> level, it;
  explicit Dinic(int n) : n(n), s(0), t(0), g(n), level(n), it(n) {}
  void add_edge(int u, int v, long long c) {
    Edge a{v, (int)g[v].size(), c};
    Edge b{u, (int)g[u].size(), 0};
    g[u].push_back(a); g[v].push_back(b);
  }
  bool bfs() {
    fill(level.begin(), level.end(), -1);
    queue<int> q; level[s] = 0; q.push(s);
    while (!q.empty()) {
      int u = q.front(); q.pop();
      for (auto &e : g[u]) if (e.cap > 0 && level[e.to] < 0) {
        level[e.to] = level[u] + 1; q.push(e.to);
      }
    }
    return level[t] >= 0;
  }
  long long dfs(int u, long long f) {
    if (u == t) return f;
    for (int &i = it[u]; i < (int)g[u].size(); ++i) {
      Edge &e = g[u][i];
      if (e.cap > 0 && level[e.to] == level[u] + 1) {
        long long got = dfs(e.to, min(f, e.cap));
        if (got > 0) {
          e.cap -= got; g[e.to][e.rev].cap += got; return got;
        }
      }
    }
    return 0;
  }
  long long maxflow(int S, int T) {
    s = S; t = T;
    long long flow = 0, INF = (1LL << 62);
    while (bfs()) {
      fill(it.begin(), it.end(), 0);
      while (long long f = dfs(s, INF)) flow += f;
    }
    return flow;
  }
};
} // namespace dinic
```

---

## 6. Recognition Trigger Signals & Heuristics

- Any max-flow / min-cut problem at ICPC/CF scale
- Bipartite matching via flow (unit caps)
- “Default” engine when editorial says max flow

---

## 7. Contest WA / TLE / RE Traps

- Missing current-arc `it[u]` → TLE
- DFS not restricted to `level[v]==level[u]+1`
- Recursion depth on long paths → iterative DFS if \(V\) huge (rare); raise stack or iterate
- Building level graph on zero-cap edges
- Reusing graph without resetting after capacity changes

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

## 10. Algorithmic Variants & Advanced Extensions

- **Scaling Dinic**: optional; niche
- **Undirected**: capacity both ways
- **Recover flow**: `original_cap - residual_forward` on each forward edge (store `cap0` if needed)
- **Min cut set**: nodes reachable from \(s\) in residual after max flow

---

## 11. Typical Problem Archetypes

1. Standard application: max flow with \(V\le 500\), \(E\le 10^4\)
2. Slightly disguised: bipartite matching as unit Dinic
3. Difficult: layered construction (time-expanded, state graph) + Dinic
4. Very difficult / advanced: combine with binary search on capacity / answer

---

## 12. Recognition & Identification Drills

1. \(n\le 400\) servers, links with bandwidth; max from gateway to DB?
2. Binary search “minimum capacity threshold” then connectivity — flow or just BFS?
3. Grid, move tokens with cell capacities — flow?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: default max flow / min cut
- Key invariant: blocking flow on level graph
- Key formula: phases until \(t\) unreachable
- Complexity: \(O(V^2E)\); \(O(E\sqrt V)\) bipartite unit
- Template to remember: `bfs` levels + `dfs` with `it[]`

---

## 3. Min Cut

---
