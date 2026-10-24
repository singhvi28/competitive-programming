# 4. Bipartite Cardinality Matching (Kuhn)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Graphs, DFS, bipartite graphs  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Graphs, DFS, bipartite graphs

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

Match left nodes to right nodes with no shared vertex. Kuhn: for each left vertex, DFS looking for an **augmenting path** in the alternating sense (free right, or rematch via `pair_of`). Maximum matching size = max number of such assignments. Equivalent to unit-cap flow \(s\to L\to R\to t\). Hall’s theorem explains impossibility; in contest you compute size / reconstruct pairs.

---

## 4. Proof Sketches & Recurrences

Augmenting path flips matching status → size +1. Kuhn tries each left node once per “round” with visited marks; \(O(VE)\) worst-case.

Flow view: caps \(s\to L = 1\), \(L\to R = 1\) (or ∞ if multi ok), \(R\to t = 1\); max flow = matching size.

König: min bipartite vertex cover = max matching.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(E)\)
- Per-query / per-operation: \(O(VE)\) Kuhn
- Total: \(O(VE)\); or Dinic \(O(E\sqrt V)\)
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — Kuhn bipartite matching
namespace kuhn {
struct Matcher {
  int nL, nR;
  vector<vector<int>> adj; // L -> R
  vector<int> ml, mr, vis;
  int timer = 0;
  Matcher(int nL, int nR)
      : nL(nL), nR(nR), adj(nL), ml(nL, -1), mr(nR, -1), vis(nL, 0) {}
  void add_edge(int u, int v) { adj[u].push_back(v); }
  bool dfs(int u) {
    if (vis[u] == timer) return false;
    vis[u] = timer;
    for (int v : adj[u]) {
      if (mr[v] < 0 || dfs(mr[v])) {
        ml[u] = v; mr[v] = u; return true;
      }
    }
    return false;
  }
  int max_matching() {
    int match = 0;
    for (int u = 0; u < nL; ++u) {
      ++timer;
      if (ml[u] < 0 && dfs(u)) ++match;
    }
    // optional second pass helps some graphs
    for (int u = 0; u < nL; ++u) {
      ++timer;
      if (ml[u] < 0 && dfs(u)) ++match;
    }
    return match;
  }
  // recover: for u in L, if ml[u]>=0 then edge u--ml[u]
};
} // namespace kuhn
```

### Python 3 Template

```python
# Python 3.11+ — Kuhn; OK for n~200–400 depending on TL
def max_bipartite(adj: list[list[int]], n_r: int) -> tuple[int, list[int]]:
    n_l = len(adj)
    mr = [-1] * n_r
    vis = [0] * n_l
    timer = 0

    def dfs(u: int) -> bool:
        if vis[u] == timer:
            return False
        vis[u] = timer
        for v in adj[u]:
            if mr[v] < 0 or dfs(mr[v]):
                mr[v] = u
                return True
        return False

    match = 0
    for u in range(n_l):
        timer += 1
        if dfs(u):
            match += 1
    return match, mr
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Assign jobs to workers,” “boys–girls,” “rows–columns”
- Grid / chessboard placement with attacks → bipartite
- Independent set / vertex cover on bipartite (König)
- “Each item used at most once on each side”

---

## 7. Contest WA / TLE / RE Traps

- Not resetting `vis` timer per DFS attempt
- 1-index / 0-index left-right mixups
- Assuming matching is unique
- Using general matching (blossom) when graph is bipartite

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

- **Maximum edge-weighted bipartite matching:** Hungarian / MCMF
- **Multiple slots:** capacity on \(s\to L\) or \(R\to t\) via flow
- **König cover / independent set:** derive from max matching
- **Dinic reduction:** preferred when you already trust your Dinic

---

## 11. Typical Problem Archetypes

1. Standard application: max jobs assigned
2. Slightly disguised: place rooks / students in timeslots
3. Difficult: min path cover in DAG = \(n -\) matching in transit graph
4. Very difficult / advanced: matchings with side constraints → flow

---

## 12. Recognition & Identification Drills

1. \(n\) tasks, \(m\) machines, compatibility list — max assignments?
2. DAG: minimum paths to cover all vertices?
3. Bipartite graph: size of maximum independent set?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: bipartite assignment, cardinality
- Key invariant: augmenting paths
- Key formula: matching = flow through unit bipartite network
- Complexity: \(O(VE)\) or \(O(E\sqrt V)\)
- Template to remember: Kuhn DFS or Dinic \(s\)–\(L\)–\(R\)–\(t\)

---

## 5. Hopcroft–Karp

---
