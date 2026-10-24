# 8. Circulation (Feasibility / Balances)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Flow with lower bounds, max flow  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Flow with lower bounds, max flow

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

A **circulation** is a flow with **no** distinguished \(s,t\) — conservation at every vertex. With upper caps (and often lowers), feasibility reduces to the lower-bound transform: supplies/demands from compulsory flow, then max flow \(S'\to T'\) must meet \(\sum\) supply. Min-cost circulation cancels negative-cost residual cycles. Treat as niche early; same gadgets as §7.

---

## 4. Proof Sketches & Recurrences

Same as §7 without original \(s,t\). Feasibility iff demand max-flow saturates. Hoffman circulation theorem: for every cut, capacity constraints vs lower bounds — in CP you compute, don’t check all cuts.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: one Dinic
- Total: Dinic
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — circulation feasibility with [lo,hi] on edges (no s,t)
namespace circ {
bool feasible(int n, const vector<lower_flow::EdgeReq> &edges) {
  return lower_flow::feasible_with_lowers(n, edges, nullptr);
}
} // namespace circ
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Flow around a network,” no single source
- Balanced transports / tour decompositions with capacities
- Edge lower bounds without \(s,t\)

---

## 7. Contest WA / TLE / RE Traps

- Confusing circulation with \(s\)–\(t\) flow
- Missing edges in balance computation
- Cost circulation with undetected neg cycle (unbounded)

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

- Circulation with demands \(d(v)\) (imbalances) — same \(S',T'\)
- Bounded circulation + max throughput elsewhere

---

## 11. Typical Problem Archetypes

1. Standard application: exists circulation respecting \([\ell,c]\)
2. Slightly disguised: rearrange tokens on graph with edge limits
3. Difficult: min-cost circulation encoding scheduling
4. Very difficult / advanced: parametric circulations

---

## 12. Recognition & Identification Drills

1. Directed roads with min/max traffic; can traffic be balanced everywhere?
2. Reorient / reroute flow to satisfy lower bounds with zero external supply?
3. Tournament scheduling as circulation? (often yes in editorials)

---

## 13. Fast-Lookup Cheat Sheet

- When to use: conservation everywhere + bounds
- Key invariant: supply/demand saturation
- Key formula: same \(b(v)\) as lowers
- Complexity: one max flow
- Template to remember: §7 reduction without \(s,t\)

---

## 9. Vertex Capacities

---
