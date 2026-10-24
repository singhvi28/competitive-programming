# 1. Max Flow (Ford–Fulkerson / Edmonds–Karp)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Graphs, BFS/DFS, residual intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Graphs, BFS/DFS, residual intuition

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

A **feasible flow** respects capacities and conservation (except \(s,t\)). The **residual graph** encodes “send more forward” or “undo backward.” Any \(s\)–\(t\) path in the residual graph is an **augmenting path**; pushing bottleneck flow along it strictly increases value. Max flow = no residual \(s\)–\(t\) path. Edmonds–Karp always picks a **shortest** (fewest edges) augmenting path via BFS — polynomial and the mental model behind Dinic’s level graphs.

---

## 4. Proof Sketches & Recurrences

Residual: for edge \(u\to v\) with capacity \(c\) and flow \(f\), residual forward \(c-f\), backward \(f\).

Augmenting path \(P\): \(\delta=\min_{e\in P} c_r(e)\). Update along \(P\). Value increases by \(\delta\).

Edmonds–Karp: each BFS augmentation; number of augmentations \(O(VE)\) (critical edges argument) → \(O(VE^2)\) with adjacency lists.

Ford–Fulkerson with arbitrary paths can be exponential (or non-terminating on irrational caps — irrelevant in CP).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) build per edge
- Per-query / per-operation: one max flow \(O(VE^2)\) Edmonds–Karp
- Total: as above
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready — Edmonds–Karp
namespace ek_flow {
struct Edge { int to, rev; long long cap; };
struct MaxFlow {
  int n;
  vector<vector<Edge>> g;
  explicit MaxFlow(int n) : n(n), g(n) {}
  void add_edge(int u, int v, long long c) {
    Edge a{v, (int)g[v].size(), c};
    Edge b{u, (int)g[u].size(), 0};
    g[u].push_back(a); g[v].push_back(b);
  }
  long long maxflow(int s, int t) {
    long long flow = 0;
    const long long INF = (1LL << 62);
    while (true) {
      vector<int> par_v(n, -1), par_e(n, -1);
      queue<int> q; q.push(s); par_v[s] = s;
      while (!q.empty() && par_v[t] < 0) {
        int u = q.front(); q.pop();
        for (int i = 0; i < (int)g[u].size(); ++i) {
          auto &e = g[u][i];
          if (e.cap > 0 && par_v[e.to] < 0) {
            par_v[e.to] = u; par_e[e.to] = i; q.push(e.to);
          }
        }
      }
      if (par_v[t] < 0) break;
      long long aug = INF;
      for (int v = t; v != s; v = par_v[v])
        aug = min(aug, g[par_v[v]][par_e[v]].cap);
      for (int v = t; v != s; v = par_v[v]) {
        auto &e = g[par_v[v]][par_e[v]];
        e.cap -= aug; g[v][e.rev].cap += aug;
      }
      flow += aug;
    }
    return flow;
  }
};
} // namespace ek_flow
```

### Python 3 Template

```python
# Python 3.11+ — Edmonds–Karp (small graphs only)
from collections import deque

class MaxFlow:
    __slots__ = ("n", "g")
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]  # [to, rev, cap]

    def add_edge(self, u: int, v: int, c: int) -> None:
        self.g[u].append([v, len(self.g[v]), c])
        self.g[v].append([u, len(self.g[u]) - 1, 0])

    def maxflow(self, s: int, t: int) -> int:
        flow, INF = 0, 10**18
        while True:
            par_v = [-1] * self.n
            par_e = [-1] * self.n
            q = deque([s]); par_v[s] = s
            while q and par_v[t] < 0:
                u = q.popleft()
                for i, (to, rev, cap) in enumerate(self.g[u]):
                    if cap > 0 and par_v[to] < 0:
                        par_v[to] = u; par_e[to] = i; q.append(to)
            if par_v[t] < 0:
                break
            aug = INF
            v = t
            while v != s:
                u, i = par_v[v], par_e[v]
                aug = min(aug, self.g[u][i][2]); v = u
            v = t
            while v != s:
                u, i = par_v[v], par_e[v]
                self.g[u][i][2] -= aug
                to, rev, _ = self.g[u][i]
                self.g[to][rev][2] += aug
                v = u
            flow += aug
        return flow
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Maximum amount that can be shipped / routed under capacities”
- “How many units from source-like set to sink-like set”
- Statement already gives edges with capacities
- Dual: min edges/nodes to disconnect \(s\) from \(t\) (→ min cut)

---

## 7. Contest WA / TLE / RE Traps

- Forgetting reverse edges (residual undo) → wrong flow
- Using `int` for capacities that sum past \(2^{31}\)
- Multiple edges: OK if each has its own residual pair; don’t merge carelessly if you need per-edge flow
- Assuming uniqueness of max flow (flows aren’t unique; value is)

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

- **Capacity scaling**: augment with large \(\Delta\) first — rarely needed if you have Dinic
- **Unit-capacity networks**: better bounds; prefer Dinic
- **Undirected edges**: add both directions with capacity \(c\) (or one undirected residual trick carefully)

---

## 11. Typical Problem Archetypes

1. Standard application: max shipment \(s\to t\) with edge capacities
2. Slightly disguised: multiple sources/sinks → super-source/sink
3. Difficult: reconstruct an integral flow / edge usage under extra constraints
4. Very difficult / advanced: dynamic capacities, online flow (usually not FF)

---

## 12. Recognition & Identification Drills

1. City water pipes have capacities; max water from reservoir to downtown?
2. \(k\) warehouses and \(m\) stores with supply/demand and road caps — max satisfiable demand?
3. Undirected graph: max number of paths from \(s\) to \(t\) that don’t share edges?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: capacity routing; teaching residual graphs; tiny \(V\)
- Key invariant: conservation + capacity; augmenting path theorem
- Key formula: max-flow value = sum of augmentations
- Complexity: \(O(VE^2)\) EK
- Template to remember: BFS path + bottleneck + reverse edges

---

## 2. Dinic

---
