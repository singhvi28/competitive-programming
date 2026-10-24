# 6. Min-Cost Max-Flow (MCMF)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, shortest paths (Bellman–Ford / Dijkstra + potentials)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Max flow, shortest paths (Bellman–Ford / Dijkstra + potentials)

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

Among all maximum flows (or flows of value \(K\)), pick one with **minimum total cost** \(\sum f_e\cdot w_e\). Residual edges carry costs: forward \(+w\), backward \(-w\). Each augmentation along a **shortest path by cost** in the residual graph yields an optimal successive-shortest-path algorithm. With **potentials** (reduced costs \(w^h(u,v)=w(u,v)+h(u)-h(v)\ge 0\)), Dijkstra works after the first BF/zero init — mandatory for contest speed.

---

## 4. Proof Sketches & Recurrences

Successive shortest paths: \(O(F\cdot SP)\) where \(F\) is total flow. With Dijkstra + potentials: \(SP=O(E\log V)\) (or \(O(V^2)\)). Negative cycles in residual ⇒ can decrease cost without bound (or need canceling); for standard MCMF from zero flow with no neg cycle initially, potentials maintain non-negative reduced costs.

If only bipartite perfect matching dense \(n\le 400\): Hungarian \(O(n^3)\) often beats generic MCMF.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: \(O(F\cdot E\log V)\) typical Dijkstra MCMF
- Total: as above; \(F\) can be large — watch limits
- Memory: \(O(V+E)\)`

### C++17 Template

```cpp
// C++17 — MCMF, Dijkstra + potentials (non-neg costs OK from pot=0;
// if build has negative costs, BF-init pot first — no neg cycle)
namespace mcmf {
struct Edge { int to, rev; long long cap, cost; };
struct MCMF {
  int n;
  vector<vector<Edge>> g;
  explicit MCMF(int n) : n(n), g(n) {}
  void add_edge(int u, int v, long long cap, long long cost) {
    Edge a{v, (int)g[v].size(), cap, cost};
    Edge b{u, (int)g[u].size(), 0, -cost};
    g[u].push_back(a); g[v].push_back(b);
  }
  // {flow, cost}; need < 0 → push max flow; else stop at need
  pair<long long, long long> min_cost_flow(int s, int t, long long need = -1) {
    const long long INF = (1LL << 62);
    long long flow = 0, cost = 0;
    vector<long long> pot(n, 0), dist(n);
    vector<int> pv(n), pe(n);
    while (need < 0 || flow < need) {
      fill(dist.begin(), dist.end(), INF);
      dist[s] = 0;
      priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
      pq.push({0, s});
      while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (int i = 0; i < (int)g[u].size(); ++i) {
          auto &e = g[u][i];
          if (e.cap <= 0) continue;
          long long nd = d + e.cost + pot[u] - pot[e.to];
          if (nd < dist[e.to]) {
            dist[e.to] = nd; pv[e.to] = u; pe[e.to] = i;
            pq.push({nd, e.to});
          }
        }
      }
      if (dist[t] == INF) break;
      long long path_cost = 0;
      long long aug = (need < 0 ? INF : need - flow);
      for (int v = t; v != s; v = pv[v]) {
        auto &e = g[pv[v]][pe[v]];
        aug = min(aug, e.cap);
        path_cost += e.cost;
      }
      for (int v = t; v != s; v = pv[v]) {
        auto &e = g[pv[v]][pe[v]];
        e.cap -= aug; g[v][e.rev].cap += aug;
      }
      for (int i = 0; i < n; ++i) if (dist[i] < INF) pot[i] += dist[i];
      flow += aug; cost += aug * path_cost;
    }
    return {flow, cost};
  }
};
} // namespace mcmf
```

---

## 6. Recognition Trigger Signals & Heuristics

- Assignment with costs + capacities (“send exactly \(k\)”, “min cost to satisfy”)
- Grid path packing with costs
- “Greedy by cost fails” because of capacity conflicts
- Circulation with costs (min-cost circulation) — related

---

## 7. Contest WA / TLE / RE Traps

- Forgetting reverse edge cost \(=-w\)
- Dijkstra without potentials when neg residual costs exist → WA
- Overflow on `flow * cost`
- Maximizing cost: negate weights
- Stopping at max flow when problem wants flow exactly \(k\) (or any flow with min cost — different)

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

- **Min-cost circulation** (cancel neg cycles) — related niche
- **Capacity scaling / cost scaling** — rare in CF
- **Hungarian** for dense bipartite assignment
- **Primal-dual** variants — same complexity class

---

## 11. Typical Problem Archetypes

1. Standard application: min cost to send \(k\) units \(s\to t\)
2. Slightly disguised: assign rows to cols with costs + “must use all”
3. Difficult: build gadgets so cost encodes penalties / bonuses
4. Very difficult / advanced: MCMF on time-expanded graphs

---

## 12. Recognition & Identification Drills

1. Taxi rides: match taxis to customers with travel cost; each taxi one ride?
2. Send exactly 10 units through a network with edge costs — min cost?
3. Place \(n\) pieces on a grid with distance costs and cell capacities?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: flow + linear edge costs
- Key invariant: successive shortest residual paths
- Key formula: reduced costs \(w+h(u)-h(v)\)
- Complexity: \(O(F E\log V)\)
- Template to remember: MCMF + potentials + Dijkstra

---

## 7. Flow with Lower Bounds

---
