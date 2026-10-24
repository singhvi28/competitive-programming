# 7. Flows with Lower Bounds on Edges

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Max flow, circulation ideas  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Max flow, circulation ideas

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

Edge must carry flow in \([\ell,c]\), not \([0,c]\). Force \(\ell\) by sending \(\ell\) “already,” leaving residual capacity \(c-\ell\), and fixing **imbalance** at vertices with a super-source/sink demand network. Feasibility first; then maximize additional flow \(s\to t\) if needed. Early-contest ROI is low — learn the reduction, don’t memorize every variant until forced.

---

## 4. Proof Sketches & Recurrences

For each edge \(u\to v\) with \([\ell,c]\): put residual edge capacity \(c-\ell\). Vertex balance \(b(x)=\sum \ell_{\mathrm{in}}-\sum \ell_{\mathrm{out}}\). If \(b(x)>0\), demand \(b(x)\) (edge from \(x\) to \(T'\)); if \(b(x)<0\), supply \(-b(x)\) (edge \(S'\to x\)). Add edge \(t\to s\) with capacity \(\infty\) for circulation between original terminals when finding feasible \(s\)–\(t\) flow with lowers. Feasible iff max flow from \(S'\) to \(T'\) saturates all supplies.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\) build
- Per-query / per-operation: one Dinic on \(O(V+E)\)
- Total: Dinic complexity
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — feasible flow with lower bounds (circulation-style check)
namespace lower_flow {
struct EdgeReq { int u, v; long long lo, hi; };
// returns whether assignments exist; optional: then maxflow on residual of (hi-lo)
bool feasible_with_lowers(int n, vector<EdgeReq> edges, dinic::Dinic *out_resid = nullptr) {
  vector<long long> bal(n, 0);
  dinic::Dinic f(n + 2);
  int S = n, T = n + 1;
  for (auto [u, v, lo, hi] : edges) {
    if (lo > hi) return false;
    bal[u] -= lo; bal[v] += lo;
    f.add_edge(u, v, hi - lo);
  }
  long long need = 0;
  for (int i = 0; i < n; ++i) {
    if (bal[i] > 0) { f.add_edge(i, T, bal[i]); need += bal[i]; }
    if (bal[i] < 0) f.add_edge(S, i, -bal[i]);
  }
  long long got = f.maxflow(S, T);
  if (out_resid) *out_resid = std::move(f);
  return got == need;
}
} // namespace lower_flow
```

---

## 6. Recognition Trigger Signals & Heuristics

- “At least \(L_e\) must go through edge \(e\)”
- “Lower and upper quotas on flights / pipes”
- Statements with both minimum and maximum usage

---

## 7. Contest WA / TLE / RE Traps

- Sign error on balance \(b(v)\)
- Forgetting \(t\to s\) link when forcing \(s\)–\(t\) structure
- \(\ell>c\) not checked
- Using lowers without saturating supply/demand check

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

- Lower bounds only on some edges
- Vertex lower bounds → split + edge lowers
- Min-cost with lowers → MCMF on the transformed network

---

## 11. Typical Problem Archetypes

1. Standard application: feasible flow with \([\ell,c]\)
2. Slightly disguised: “each edge used at least once” in Eulerian-ish flow clothing
3. Difficult: max flow with lowers + costs
4. Very difficult / advanced: dynamic lowers (rare)

---

## 12. Recognition & Identification Drills

1. Every pipe must carry at least 5 units, at most 20 — is a valid shipping possible?
2. Flights with minimum passenger guarantees and seat caps?
3. Round-trip circulation where each arc has a minimum load?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: edge quotas \([\ell,c]\)
- Key invariant: fix \(\ell\), balance via \(S',T'\)
- Key formula: \(b(v)=\sum\ell_{\mathrm{in}}-\sum\ell_{\mathrm{out}}\)
- Complexity: one max flow
- Template to remember: demand network + Dinic saturate supplies

---

## 8. Circulation

---
