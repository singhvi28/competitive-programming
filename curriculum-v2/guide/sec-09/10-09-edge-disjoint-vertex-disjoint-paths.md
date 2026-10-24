# 10. Edge-Disjoint & Vertex-Disjoint Paths

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, vertex capacities (for vertex-disjoint)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Max flow, vertex capacities (for vertex-disjoint)

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

**Edge-disjoint** \(s\)–\(t\) paths: every edge capacity \(1\), max flow = max number of paths (integral). **Vertex-disjoint** (internally): unit capacities on vertex splits (and usually edges capacity \(1\)). Menger’s theorem: min edge cut = max edge-disjoint paths; min vertex cut = max internally vertex-disjoint paths.

---

## 4. Proof Sketches & Recurrences

Integral flow decomposition: any integral flow of value \(k\) decomposes into \(k\) paths (+ cycles). Unit caps ⇒ paths are edge-disjoint. Vertex unit splits ⇒ internally vertex-disjoint.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: Dinic; unit networks often fast
- Total: \(O(E\sqrt V)\)-class typical for unit
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — edge-disjoint path count
namespace disjoint_paths {
long long edge_disjoint(int n, int s, int t, const vector<pair<int,int>> &edges) {
  dinic::Dinic f(n);
  for (auto [u, v] : edges) f.add_edge(u, v, 1); // undirected: add both dirs cap 1
  return f.maxflow(s, t);
}
long long vertex_disjoint(int n, int s, int t, const vector<pair<int,int>> &edges) {
  vertcap::Solver sol(n);
  for (int v = 0; v < n; ++v) {
    if (v == s || v == t) sol.set_vertex_cap(v, (1LL << 62)); // unlimited terminals
    else sol.set_vertex_cap(v, 1);
  }
  for (auto [u, v] : edges) sol.add_edge(u, v, 1);
  return sol.maxflow(s, t);
}
} // namespace disjoint_paths
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Maximum number of routes that don’t share roads/cities”
- Connectivity checks with disjointness
- DAG path packing (sometimes matching; sometimes flow)

---

## 7. Contest WA / TLE / RE Traps

- Undirected graph: capacity 1 each direction can allow “use both ways” weirdness — use one undirected residual carefully or cap 1 total via undirected modeling
- Allowing \(s\) or \(t\) to be “blocked” by vertex cap 1
- Counting walks that reuse vertices when asking vertex-disjoint

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

- Length-bounded disjoint paths — harder (not plain flow)
- Disjoint paths with costs — MCMF unit
- \(k\) pairs multi-commodity — generally NP-hard; not single commodity flow

---

## 11. Typical Problem Archetypes

1. Standard application: max edge-disjoint \(s\)–\(t\) paths
2. Slightly disguised: connectivity = disjoint paths by Menger
3. Difficult: reconstruct the paths explicitly
4. Very difficult / advanced: disjoint paths in planar graphs with extras

---

## 12. Recognition & Identification Drills

1. Max number of bus routes sharing no road from depot to airport?
2. Max internally vertex-disjoint paths in a directed city graph?
3. Undirected cubic graph connectivity between two vertices?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: disjoint route packing / Menger
- Key invariant: unit-cap integral flow ↔ paths
- Key formula: edge-disjoint = unit edge flow; vertex = split + unit
- Complexity: unit Dinic
- Template to remember: cap 1 (+ split)

---

## 11. How to Recognize When a Problem Is Secretly a Flow Problem (Synthesis)

---
