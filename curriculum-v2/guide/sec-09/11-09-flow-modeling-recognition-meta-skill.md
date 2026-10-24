# Flow Modeling Recognition (Meta-Skill)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1800–2500 | **Frequency:** Common  
> **Prerequisites:** Matching, Dinic, min cut, basic gadgets (this section)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Matching, Dinic, min cut, basic gadgets (this section)

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

Flow problems rarely say “compute max flow.” They say **assign, cut, route, saturate, separate, cover with paths**. Your job is to invent vertices/edges so that **feasible integral flows ↔ valid solutions** and **objective ↔ flow value or cut capacity**. If the hard part is conflicts of limited resources along graphs, think flow before DP.

---

## 4. Proof Sketches & Recurrences

Checklist (run in order):

1. **Cardinality bipartite assignment?** → Kuhn / HK / Dinic  
2. **Disjoint paths / connectivity cut?** → unit flow / min cut  
3. **Vertex limits?** → split  
4. **Partition / project selection / close set?** → min cut gadgets  
5. **Costs on edges with capacities?** → MCMF (vs greedy proof?)  
6. **Lower quotas?** → niche lower-bound / circulation  
7. **Still stuck?** → maybe not flow; try DP / greedy / matching-only

Gadget inventory:

| Need | Gadget |
|------|--------|
| Multiple sources | Super-source → sources with supplies |
| Multiple sinks | Sinks → super-sink with demands |
| At most \(k\) from a group | Cap on group→sink or source→group |
| Force “A implies B” in cut | \(\infty\) edge \(A\to B\) in closure model |
| Cost vs benefit | Edges to \(s\)/\(t\) with weights; answer \(=\mathrm{const}-\mathrm{mincut}\) |

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: modeling time dominates human side
- Per-query / per-operation: underlying Dinic/MCMF/matching
- Total: as chosen engine
- Memory: as engine + gadget nodes`

### C++17 Template

```cpp
// C++17 — modeling sketch (fill gadgets, then dinic)
void solve_flow_model() {
  // 1. Map entities -> nodes (and splits if needed)
  // 2. add_edge with capacities (1, k, INF, profits...)
  // 3. long long ans = dinic.maxflow(S, T);
  // 4. If cut-model: ans = CONST - ans; optional residual side_of_s
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Limited capacities / “at most \(k\) through …”
- Assignment between two sides (→ matching / flow)
- Min cost to separate / delete / cut
- Path cover / disjoint routes
- “Max score = constant − penalty” with pairwise or cut penalties
- Binary decisions with implication “A forces B” (\(\infty\) edges in cut models)
- Multiple sources/sinks, supplies/demands
- Reductions mentioned in editorials: matching, cut, Dinic

---

## 7. Contest WA / TLE / RE Traps

- Wrong \(\infty\) (too small) breaking forced implications
- Off-by-one on “at most \(k\)” vs “exactly \(k\)” (exactly → often lower bounds or force flow value)
- Building a flow when bipartite matching sufficed (wasted time) or vice versa
- Non-integral assumptions when problem needs counts (use integral caps)

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

- Binary search on answer + feasibility flow
- Flow on state graphs (time × node)
- Matching reductions (DAG min path cover)

---

## 11. Typical Problem Archetypes

1. Standard application: explicit capacities
2. Slightly disguised: assignment / path cover
3. Difficult: cut = optimization score
4. Very difficult / advanced: layered gadgets + MCMF + binary search

---

## 12. Recognition & Identification Drills

1. Maximize profit of open projects with dependencies and conflict penalties — algorithm family?
2. Cover all vertices of a DAG with minimum paths — which graph do you match on?
3. Evacuation: each hallway capacity \(c_e\), each intersection holds \(\le p_v\) people — model?
4. Select a subset of websites to hack with gains; if you hack A you must hack B — flow/cut?
5. Min cost to assign every student a unique dorm with prefs — matching or MCMF?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: capacity, cut, assignment, disjoint routing
- Key invariant: solutions ↔ integral flows/cuts
- Key formula: checklist 1→7 above
- Complexity: usually Dinic \(O(V^2E)\) / matching \(O(E\sqrt V)\)
- Template to remember: map entities → nodes; conflicts → caps; objective → \(|f|\) or cut

---

## End-of-Section Mini Comparison

| Need | Reach for |
|------|-----------|
| Default max flow / min cut | Dinic ([09-a §2–3](09-a-network-flow-max-flow-hopcroft.md#2-dinic)) |
| Bipartite matching | Kuhn → Dinic/HK if needed |
| Costs | MCMF (or Hungarian if dense assignment) |
| Node limits / vertex-disjoint | Split + unit caps |
| Edge-disjoint paths | Unit-cap flow |
| Lower bounds / circulation | Niche reductions (§7–8) |
| Unknown | Recognition checklist (§11) |

---
