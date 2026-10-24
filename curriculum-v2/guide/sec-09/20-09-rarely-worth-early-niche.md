# 20. Rarely worth early / Niche

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Push-Relabel, Gomory-Hu Tree, Stoer-Wagner

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

Advanced flow constructs such as Gomory-Hu Cut Trees ($N-1$ min-cuts representing all pairs in a tree) and Stoer-Wagner global min-cut appear rarely in standard Div2/Div1 contests. Spend practice time on Dinic and reductions before mastering these niche topics.

---

## 4. Proof Sketches & Recurrences

Gomory-Hu Tree computes all $\binom{N}{2}$ pairwise minimum cuts using exactly $N-1$ max-flow computations via recursive partitioning.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Reference note: Gomory-Hu tree computes all-pairs min-cut in N-1 max-flow executions.
// Use Dinic subroutines on contracted component sets.
```

---

## 6. Recognition Trigger Signals & Heuristics

- All-pairs min-cut queries on an undirected network.
- Global minimum cut without specified source and sink in undirected graph.

---

## 7. Contest WA / TLE / RE Traps

- Applying Gomory-Hu tree on directed graphs (valid only on undirected networks).

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
