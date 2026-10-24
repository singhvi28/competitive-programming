# Vertex Capacities (Node Split)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow modeling  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Max flow modeling

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

If a **vertex** \(v\) may be used by at most \(c_v\) flow, split into \(v_{\mathrm{in}}\to v_{\mathrm{out}}\) with capacity \(c_v\). Original edge \(u\to v\) becomes \(u_{\mathrm{out}}\to v_{\mathrm{in}}\) (edge cap unchanged). This turns vertex cuts / “robots through cities” into ordinary edge-cap flow.

---

## 4. Proof Sketches & Recurrences

Any flow through \(v\) must cross the split edge ⇒ limited by \(c_v\). Correctness: bijection between flows in original vertex-cap network and edge-cap network on split graph.

\(V'=2V\), \(E'=E+V\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(V+E)\) split
- Per-query / per-operation: Dinic on \(2V\) vertices
- Total: Dinic complexity on split network
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — vertex-cap max flow via split
namespace vertcap {
struct Solver {
  int n;
  dinic::Dinic f;
  explicit Solver(int n) : n(n), f(2 * n) {}
  int in(int v) { return 2 * v; }
  int out(int v) { return 2 * v + 1; }
  void set_vertex_cap(int v, long long c) { f.add_edge(in(v), out(v), c); }
  void add_edge(int u, int v, long long c) { // u_out -> v_in
    f.add_edge(out(u), in(v), c);
  }
  long long maxflow(int s, int t) {
    // usually infinite cap through s,t splits, or set carefully
    return f.maxflow(in(s), out(t)); // common pattern; verify s/t caps
  }
};
} // namespace vertcap
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Each city can be visited by at most \(k\) paths”
- Min vertices to delete to disconnect \(s,t\) (unit vertex caps)
- Servers with processing limits; edges unlimited or separate

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to split \(s\) or \(t\) correctly (often leave infinite through terminals)
- Wiring `u_in → v_in` by mistake
- Unit vertex-disjoint paths need cap \(1\) on splits
- Double-limiting undirected edges

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

- Only some vertices capacitated
- Vertex costs → MCMF on split edge
- Vertex lowers → lower bounds on split edge

---

## 11. Typical Problem Archetypes

1. Standard application: max flow with node bandwidths
2. Slightly disguised: min nodes to remove to disconnect (unit caps)
3. Difficult: mix edge + vertex capacities
4. Very difficult / advanced: time-expanded + vertex caps

---

## 12. Recognition & Identification Drills

1. At most 3 agents may pass each junction — max agents \(s\to t\)?
2. Destroy minimum number of stations to separate two cities?
3. CPU nodes have job limits; network links have bandwidth — max jobs?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: limits on vertices / vertex cuts
- Key invariant: all flow through \(v\) crosses split
- Key formula: \(v_{\mathrm{in}}\to v_{\mathrm{out}}\) cap \(c_v\)
- Complexity: Dinic on \(2V\)
- Template to remember: split nodes

---

## 10. Edge-Disjoint / Vertex-Disjoint Paths

---
