# 3. \(s\)–\(t\) Min Cut

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, residual reachability  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Max flow, residual reachability

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

**Max-flow min-cut theorem:** minimum capacity of an \(s\)–\(t\) cut equals max flow. After computing max flow, let \(S=\) nodes reachable from \(s\) in the residual graph, \(T=V\setminus S\). Edges from \(S\) to \(T\) in the **original** network form a min cut. Modeling problems often ask to **choose a cut** (keep vs discard, open vs close) whose cost matches edge capacities you designed.

---

## 4. Proof Sketches & Recurrences

Cut \((S,T)\): \(s\in S\), \(t\in T\), capacity \(\sum_{u\in S,v\in T} c(u,v)\). Any flow ≤ every cut. Equality achieved by residual reachability cut after max flow.

**Project selection sketch:** edge \(u\to v\) capacity \(\infty\) means “cannot take \(u\) without \(v\)” (closed set). Profit/cost encoded via edges to \(s\)/\(t\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: one max flow
- Per-query / per-operation: \(O(V+E)\) residual BFS for the cut set
- Total: dominated by max flow
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — min-cut set after Dinic (reuse dinic::Dinic)
namespace mincut {
vector<int> side_of_s(dinic::Dinic &f, int s) {
  vector<char> vis(f.n, 0);
  queue<int> q; q.push(s); vis[s] = 1;
  while (!q.empty()) {
    int u = q.front(); q.pop();
    for (auto &e : f.g[u]) if (e.cap > 0 && !vis[e.to]) {
      vis[e.to] = 1; q.push(e.to);
    }
  }
  vector<int> S;
  for (int i = 0; i < f.n; ++i) if (vis[i]) S.push_back(i);
  return S;
}
// cut edges: original u->v with u in S, v not in S (track cap0 if needed)
} // namespace mincut
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Minimum cost to disconnect \(A\) from \(B\)”
- “Delete edges/nodes of minimum total weight”
- Project selection / closed set / “choose subset with pairwise penalties”
- Partition vertices into two labels with boundary costs

---

## 7. Contest WA / TLE / RE Traps

- Computing cut before finishing max flow
- Using residual edges as “cut edges” instead of original forward saturated cross edges
- \(\infty\) capacity too small (overflow / still “finite”) → wrong closed-set models
- Forgetting undirected edges contribute once to cut capacity modeling

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

- **Node cut:** vertex capacities (Part B §9)
- **Global min cut:** Stoer–Wagner / Karger — different problem (no fixed \(s,t\)); rare in CF
- **Gomory–Hu:** all-pairs min cuts — niche

---

## 11. Typical Problem Archetypes

1. Standard application: min edge weight to disconnect \(s,t\)
2. Slightly disguised: max score = const − min cut (project selection)
3. Difficult: multi-label reductions to binary cuts / successive cuts
4. Very difficult / advanced: planar dual shortest paths as min cut

---

## 12. Recognition & Identification Drills

1. Remove minimum total road length so city A cannot reach city B?
2. Open/close factories with profits and pairwise conflict costs?
3. Pixel labeling FG/BG with smoothness penalties — cut?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: disconnect / partition / closed-set scoring
- Key invariant: max flow = min cut capacity
- Key formula: \(S=\) residual-reachable from \(s\)
- Complexity: flow + \(O(V+E)\)
- Template to remember: Dinic then residual BFS

---

## 4. Bipartite Matching

---
