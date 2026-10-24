# 5. Hopcroft–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2500 | **Frequency:** Occasional  
> **Prerequisites:** Bipartite matching, BFS+DFS layers  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Bipartite matching, BFS+DFS layers

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

Kuhn finds one augmenting path at a time. Hopcroft–Karp finds a **maximal set of shortest augmenting paths** each phase (BFS builds distance layers on free vertices; DFS walks them disjointly) — same spirit as Dinic on the bipartite unit network. Use when \(n,m,E\) are large and Kuhn TLEs.

---

## 4. Proof Sketches & Recurrences

Phases \(O(\sqrt V)\); each phase \(O(E)\) → \(O(E\sqrt V)\). Equivalent order to Dinic on unit bipartite flow.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: \(O(E\sqrt V)\)
- Total: \(O(E\sqrt V)\)
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — Hopcroft–Karp
namespace hopcroft {
struct HK {
  int nL, nR;
  vector<vector<int>> adj;
  vector<int> ml, mr, dist;
  HK(int nL, int nR) : nL(nL), nR(nR), adj(nL), ml(nL, -1), mr(nR, -1), dist(nL) {}
  void add_edge(int u, int v) { adj[u].push_back(v); }
  bool bfs() {
    queue<int> q;
    const int INF = 1e9;
    for (int u = 0; u < nL; ++u) {
      if (ml[u] < 0) { dist[u] = 0; q.push(u); }
      else dist[u] = INF;
    }
    bool found = false;
    vector<int> dr(nR, INF);
    while (!q.empty()) {
      int u = q.front(); q.pop();
      for (int v : adj[u]) {
        if (dr[v] == INF) {
          dr[v] = dist[u] + 1;
          if (mr[v] < 0) found = true;
          else if (dist[mr[v]] == INF) {
            dist[mr[v]] = dr[v] + 1; q.push(mr[v]);
          }
        }
      }
    }
    return found;
  }
  bool dfs(int u) {
    for (int v : adj[u]) {
      if (mr[v] < 0 || (dist[mr[v]] == dist[u] + 2 && dfs(mr[v]))) {
        ml[u] = v; mr[v] = u; return true;
      }
    }
    dist[u] = 1e9; // block
    return false;
  }
  int max_matching() {
    int match = 0;
    while (bfs()) {
      for (int u = 0; u < nL; ++u)
        if (ml[u] < 0 && dfs(u)) ++match;
    }
    return match;
  }
};
} // namespace hopcroft
```

### Python 3 Template

```python
# Python 3.11+ — Hopcroft–Karp (borderline for large E)
from collections import deque

class HopcroftKarp:
    def __init__(self, n_l: int, n_r: int):
        self.n_l, self.n_r = n_l, n_r
        self.adj = [[] for _ in range(n_l)]
        self.ml = [-1] * n_l
        self.mr = [-1] * n_r
        self.dist = [0] * n_l

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def bfs(self) -> bool:
        INF = 10**9
        q = deque()
        for u in range(self.n_l):
            if self.ml[u] < 0:
                self.dist[u] = 0; q.append(u)
            else:
                self.dist[u] = INF
        found = False
        dr = [INF] * self.n_r
        while q:
            u = q.popleft()
            for v in self.adj[u]:
                if dr[v] == INF:
                    dr[v] = self.dist[u] + 1
                    if self.mr[v] < 0:
                        found = True
                    else:
                        w = self.mr[v]
                        if self.dist[w] == INF:
                            self.dist[w] = dr[v] + 1; q.append(w)
        return found

    def dfs(self, u: int) -> bool:
        for v in self.adj[u]:
            w = self.mr[v]
            if w < 0 or (self.dist[w] == self.dist[u] + 2 and self.dfs(w)):
                self.ml[u] = v; self.mr[v] = u
                return True
        self.dist[u] = 10**9
        return False

    def max_matching(self) -> int:
        match = 0
        while self.bfs():
            for u in range(self.n_l):
                if self.ml[u] < 0 and self.dfs(u):
                    match += 1
        return match
```

---

## 6. Recognition Trigger Signals & Heuristics

- Bipartite matching with \(E\sim 10^5\), \(V\sim 10^5\) under tight TL
- Editorial mentions Hopcroft–Karp / \(O(E\sqrt V)\)
- You already know Dinic: implementing Dinic on matching network is equally valid

---

## 7. Contest WA / TLE / RE Traps

- Wrong layer check (`dist[mr[v]] == dist[u] + 2`)
- Not blocking failed vertices → infinite loops / TLE
- Mixing L/R index spaces
- Preferring HK when Dinic template already passes

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

- Multiple edges / capacities >1 → use general Dinic, not HK
- Weighted → MCMF / Hungarian
- Dinic-on-bipartite as drop-in replacement

---

## 11. Typical Problem Archetypes

1. Standard application: large bipartite matching cardinality
2. Slightly disguised: tiling / pairing at scale
3. Difficult: repeated matchings in binary search on threshold graph
4. Very difficult / advanced: HK inside more complex reductions (rare)

---

## 12. Recognition & Identification Drills

1. \(2\cdot 10^5\) possible internship pairs — max matching under 1s TL?
2. Threshold: max edges with weight \(\ge x\) forming matching of size \(k\)?
3. Same as Kuhn problem but TL halved — which algorithm?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: large bipartite cardinality matching
- Key invariant: shortest augmenting paths in phases
- Key formula: \(O(E\sqrt V)\)
- Complexity: \(O(E\sqrt V)\)
- Template to remember: BFS layers + DFS disjoint shortest paths

---

Continue: [09-b-network-flow-mcmf-recognition.md](09-b-network-flow-mcmf-recognition.md) (MCMF → recognition).

---
