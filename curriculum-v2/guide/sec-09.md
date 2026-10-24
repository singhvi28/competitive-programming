# Section §09: Network Flow & Matchings

> **Module ID:** `sec-09`  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Topic Count:** 20  

**Module Summary:** Dinic's blocking flow algorithm, Min-Cut theorem & project selection closures, Bipartite matching (Kuhn / Hopcroft-Karp), MCMF with SPFA/Potentials, and Demands.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Max Flow (Ford–Fulkerson / Edmonds–Karp)](#topic-1) | `A-tier` | 1800–2400 | Occasional | [01-09-max-flow-ford-fulkerson-edmonds-karp.md](./01-09-max-flow-ford-fulkerson-edmonds-karp.md) |
| 2 | [Dinic’s Algorithm](#topic-2) | `A-tier` | 1900–2500 | Occasional | [02-09-dinic-s-algorithm.md](./02-09-dinic-s-algorithm.md) |
| 3 | [\(s\)–\(t\) Min Cut](#topic-3) | `A-tier` | 1900–2500 | Occasional | [03-09-s-t-min-cut.md](./03-09-s-t-min-cut.md) |
| 4 | [Bipartite Cardinality Matching (Kuhn)](#topic-4) | `S-tier` | 1600–2200 | Common | [04-09-bipartite-cardinality-matching-kuhn.md](./04-09-bipartite-cardinality-matching-kuhn.md) |
| 5 | [Hopcroft–Karp](#topic-5) | `B-tier` | 2000–2500 | Occasional | [05-09-hopcroft-karp.md](./05-09-hopcroft-karp.md) |
| 6 | [Min-Cost Max-Flow (MCMF)](#topic-6) | `B-tier` | 2100–2700 | Occasional | [06-09-min-cost-max-flow-mcmf.md](./06-09-min-cost-max-flow-mcmf.md) |
| 7 | [Flows with Lower Bounds on Edges](#topic-7) | `C-tier` | 2300–2900 | Rare | [07-09-flows-with-lower-bounds-on-edges.md](./07-09-flows-with-lower-bounds-on-edges.md) |
| 8 | [Circulation (Feasibility / Balances)](#topic-8) | `C-tier` | 2300–2900 | Rare | [08-09-circulation-feasibility-balances.md](./08-09-circulation-feasibility-balances.md) |
| 9 | [Vertex Capacities (Node Split)](#topic-9) | `B-tier` | 2000–2500 | Occasional | [09-09-vertex-capacities-node-split.md](./09-09-vertex-capacities-node-split.md) |
| 10 | [Edge-Disjoint & Vertex-Disjoint Paths](#topic-10) | `A-tier` | 1800–2400 | Occasional | [10-09-edge-disjoint-vertex-disjoint-paths.md](./10-09-edge-disjoint-vertex-disjoint-paths.md) |
| 11 | [Flow Modeling Recognition (Meta-Skill)](#topic-11) | `S-tier` | 1800–2500 | Common | [11-09-flow-modeling-recognition-meta-skill.md](./11-09-flow-modeling-recognition-meta-skill.md) |
| 12 | [What to drill this week](#topic-12) | `B-tier` | 1600–2200 | Common | [12-09-what-to-drill-this-week.md](./12-09-what-to-drill-this-week.md) |
| 13 | [Hungarian Algorithm (Kuhn-Munkres)](#topic-13) | `B-tier` | 2100–2600 | Occasional | [13-09-hungarian-algorithm-kuhn-munkres.md](./13-09-hungarian-algorithm-kuhn-munkres.md) |
| 14 | [Dinic vs Edmonds–Karp](#topic-14) | `B-tier` | 1600–2200 | Common | [14-09-dinic-vs-edmonds-karp.md](./14-09-dinic-vs-edmonds-karp.md) |
| 15 | [Dinic vs Hopcroft–Karp](#topic-15) | `B-tier` | 1600–2200 | Common | [15-09-dinic-vs-hopcroft-karp.md](./15-09-dinic-vs-hopcroft-karp.md) |
| 16 | [Matching vs General Flow](#topic-16) | `B-tier` | 1600–2200 | Common | [16-09-matching-vs-general-flow.md](./16-09-matching-vs-general-flow.md) |
| 17 | [MCMF vs Greedy](#topic-17) | `B-tier` | 1600–2200 | Common | [17-09-mcmf-vs-greedy.md](./17-09-mcmf-vs-greedy.md) |
| 18 | [High-ROI (master first)](#topic-18) | `B-tier` | 1600–2200 | Common | [18-09-high-roi-master-first.md](./18-09-high-roi-master-first.md) |
| 19 | [Situational (learn when patterns appear)](#topic-19) | `B-tier` | 1600–2200 | Common | [19-09-situational-learn-when-patterns-appear.md](./19-09-situational-learn-when-patterns-appear.md) |
| 20 | [Rarely worth early / Niche](#topic-20) | `B-tier` | 1600–2200 | Common | [20-09-rarely-worth-early-niche.md](./20-09-rarely-worth-early-niche.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Max Flow (Ford–Fulkerson / Edmonds–Karp)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Graphs, BFS/DFS, residual intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Graphs, BFS/DFS, residual intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

A **feasible flow** respects capacities and conservation (except \(s,t\)). The **residual graph** encodes “send more forward” or “undo backward.” Any \(s\)–\(t\) path in the residual graph is an **augmenting path**; pushing bottleneck flow along it strictly increases value. Max flow = no residual \(s\)–\(t\) path. Edmonds–Karp always picks a **shortest** (fewest edges) augmenting path via BFS — polynomial and the mental model behind Dinic’s level graphs.

---

#### 4. Proof Sketches & Recurrences

Residual: for edge \(u\to v\) with capacity \(c\) and flow \(f\), residual forward \(c-f\), backward \(f\).

Augmenting path \(P\): \(\delta=\min_{e\in P} c_r(e)\). Update along \(P\). Value increases by \(\delta\).

Edmonds–Karp: each BFS augmentation; number of augmentations \(O(VE)\) (critical edges argument) → \(O(VE^2)\) with adjacency lists.

Ford–Fulkerson with arbitrary paths can be exponential (or non-terminating on irrational caps — irrelevant in CP).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) build per edge
- Per-query / per-operation: one max flow \(O(VE^2)\) Edmonds–Karp
- Total: as above
- Memory: \(O(V+E)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready — Edmonds–Karp
namespace ek_flow {
struct Edge { int to, rev; long long cap; };
struct MaxFlow {
  int n;
  vector<vector<Edge>> g;
  explicit MaxFlow(int n) : n(n), g(n) {}
  void add_edge(int u, int v, long long c) {
    Edge a{v, (int)g[v].size(), c};
    Edge b{u, (int)g[u].size(), 0};
    g[u].push_back(a); g[v].push_back(b);
  }
  long long maxflow(int s, int t) {
    long long flow = 0;
    const long long INF = (1LL << 62);
    while (true) {
      vector<int> par_v(n, -1), par_e(n, -1);
      queue<int> q; q.push(s); par_v[s] = s;
      while (!q.empty() && par_v[t] < 0) {
        int u = q.front(); q.pop();
        for (int i = 0; i < (int)g[u].size(); ++i) {
          auto &e = g[u][i];
          if (e.cap > 0 && par_v[e.to] < 0) {
            par_v[e.to] = u; par_e[e.to] = i; q.push(e.to);
          }
        }
      }
      if (par_v[t] < 0) break;
      long long aug = INF;
      for (int v = t; v != s; v = par_v[v])
        aug = min(aug, g[par_v[v]][par_e[v]].cap);
      for (int v = t; v != s; v = par_v[v]) {
        auto &e = g[par_v[v]][par_e[v]];
        e.cap -= aug; g[v][e.rev].cap += aug;
      }
      flow += aug;
    }
    return flow;
  }
};
} // namespace ek_flow
```

##### Python 3 Template

```python
# Python 3.11+ — Edmonds–Karp (small graphs only)
from collections import deque

class MaxFlow:
    __slots__ = ("n", "g")
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]  # [to, rev, cap]

    def add_edge(self, u: int, v: int, c: int) -> None:
        self.g[u].append([v, len(self.g[v]), c])
        self.g[v].append([u, len(self.g[u]) - 1, 0])

    def maxflow(self, s: int, t: int) -> int:
        flow, INF = 0, 10**18
        while True:
            par_v = [-1] * self.n
            par_e = [-1] * self.n
            q = deque([s]); par_v[s] = s
            while q and par_v[t] < 0:
                u = q.popleft()
                for i, (to, rev, cap) in enumerate(self.g[u]):
                    if cap > 0 and par_v[to] < 0:
                        par_v[to] = u; par_e[to] = i; q.append(to)
            if par_v[t] < 0:
                break
            aug = INF
            v = t
            while v != s:
                u, i = par_v[v], par_e[v]
                aug = min(aug, self.g[u][i][2]); v = u
            v = t
            while v != s:
                u, i = par_v[v], par_e[v]
                self.g[u][i][2] -= aug
                to, rev, _ = self.g[u][i]
                self.g[to][rev][2] += aug
                v = u
            flow += aug
        return flow
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Maximum amount that can be shipped / routed under capacities”
- “How many units from source-like set to sink-like set”
- Statement already gives edges with capacities
- Dual: min edges/nodes to disconnect \(s\) from \(t\) (→ min cut)

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting reverse edges (residual undo) → wrong flow
- Using `int` for capacities that sum past \(2^{31}\)
- Multiple edges: OK if each has its own residual pair; don’t merge carelessly if you need per-edge flow
- Assuming uniqueness of max flow (flows aren’t unique; value is)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Capacity scaling**: augment with large \(\Delta\) first — rarely needed if you have Dinic
- **Unit-capacity networks**: better bounds; prefer Dinic
- **Undirected edges**: add both directions with capacity \(c\) (or one undirected residual trick carefully)

---

#### 11. Typical Problem Archetypes

1. Standard application: max shipment \(s\to t\) with edge capacities
2. Slightly disguised: multiple sources/sinks → super-source/sink
3. Difficult: reconstruct an integral flow / edge usage under extra constraints
4. Very difficult / advanced: dynamic capacities, online flow (usually not FF)

---

#### 12. Recognition & Identification Drills

1. City water pipes have capacities; max water from reservoir to downtown?
2. \(k\) warehouses and \(m\) stores with supply/demand and road caps — max satisfiable demand?
3. Undirected graph: max number of paths from \(s\) to \(t\) that don’t share edges?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: capacity routing; teaching residual graphs; tiny \(V\)
- Key invariant: conservation + capacity; augmenting path theorem
- Key formula: max-flow value = sum of augmentations
- Complexity: \(O(VE^2)\) EK
- Template to remember: BFS path + bottleneck + reverse edges

---

## 2. Dinic

---


---

<a id="topic-2"></a>
### 2. Dinic’s Algorithm

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow / residual graphs, BFS + DFS  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Max flow / residual graphs, BFS + DFS

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Don’t recompute shortest paths from scratch naively for every single edge push. Build a **level graph** by BFS on residual edges (distance from \(s\)). Then send a **blocking flow**: DFS only along edges \(u\to v\) with \(\mathrm{level}[v]=\mathrm{level}[u]+1\), advancing a current-edge pointer so each edge is scanned amortized \(O(1)\) per phase. When no more flow in the level graph, rebuild levels. Phases are few in practice; on unit networks the algorithm is especially fast.

---

#### 4. Proof Sketches & Recurrences

Phase: BFS levels \(O(E)\). Blocking flow with current-arc DFS: \(O(VE)\) worst-case per phase. Number of phases \(O(V)\) → \(O(V^2E)\).

Unit-capacity / simple networks: \(O(\min(V^{2/3}, E^{1/2})E)\) style bounds; bipartite matching via Dinic: \(O(E\sqrt V)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) per edge
- Per-query / per-operation: \(O(V^2E)\) worst-case; much faster typical / unit
- Total: one max flow as above
- Memory: \(O(V+E)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready — Dinic
namespace dinic {
struct Edge { int to, rev; long long cap; };
struct Dinic {
  int n, s, t;
  vector<vector<Edge>> g;
  vector<int> level, it;
  explicit Dinic(int n) : n(n), s(0), t(0), g(n), level(n), it(n) {}
  void add_edge(int u, int v, long long c) {
    Edge a{v, (int)g[v].size(), c};
    Edge b{u, (int)g[u].size(), 0};
    g[u].push_back(a); g[v].push_back(b);
  }
  bool bfs() {
    fill(level.begin(), level.end(), -1);
    queue<int> q; level[s] = 0; q.push(s);
    while (!q.empty()) {
      int u = q.front(); q.pop();
      for (auto &e : g[u]) if (e.cap > 0 && level[e.to] < 0) {
        level[e.to] = level[u] + 1; q.push(e.to);
      }
    }
    return level[t] >= 0;
  }
  long long dfs(int u, long long f) {
    if (u == t) return f;
    for (int &i = it[u]; i < (int)g[u].size(); ++i) {
      Edge &e = g[u][i];
      if (e.cap > 0 && level[e.to] == level[u] + 1) {
        long long got = dfs(e.to, min(f, e.cap));
        if (got > 0) {
          e.cap -= got; g[e.to][e.rev].cap += got; return got;
        }
      }
    }
    return 0;
  }
  long long maxflow(int S, int T) {
    s = S; t = T;
    long long flow = 0, INF = (1LL << 62);
    while (bfs()) {
      fill(it.begin(), it.end(), 0);
      while (long long f = dfs(s, INF)) flow += f;
    }
    return flow;
  }
};
} // namespace dinic
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Any max-flow / min-cut problem at ICPC/CF scale
- Bipartite matching via flow (unit caps)
- “Default” engine when editorial says max flow

---

#### 7. Contest WA / TLE / RE Traps

- Missing current-arc `it[u]` → TLE
- DFS not restricted to `level[v]==level[u]+1`
- Recursion depth on long paths → iterative DFS if \(V\) huge (rare); raise stack or iterate
- Building level graph on zero-cap edges
- Reusing graph without resetting after capacity changes

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Scaling Dinic**: optional; niche
- **Undirected**: capacity both ways
- **Recover flow**: `original_cap - residual_forward` on each forward edge (store `cap0` if needed)
- **Min cut set**: nodes reachable from \(s\) in residual after max flow

---

#### 11. Typical Problem Archetypes

1. Standard application: max flow with \(V\le 500\), \(E\le 10^4\)
2. Slightly disguised: bipartite matching as unit Dinic
3. Difficult: layered construction (time-expanded, state graph) + Dinic
4. Very difficult / advanced: combine with binary search on capacity / answer

---

#### 12. Recognition & Identification Drills

1. \(n\le 400\) servers, links with bandwidth; max from gateway to DB?
2. Binary search “minimum capacity threshold” then connectivity — flow or just BFS?
3. Grid, move tokens with cell capacities — flow?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: default max flow / min cut
- Key invariant: blocking flow on level graph
- Key formula: phases until \(t\) unreachable
- Complexity: \(O(V^2E)\); \(O(E\sqrt V)\) bipartite unit
- Template to remember: `bfs` levels + `dfs` with `it[]`

---

## 3. Min Cut

---


---

<a id="topic-3"></a>
### 3. \(s\)–\(t\) Min Cut

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, residual reachability  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Max flow, residual reachability

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

**Max-flow min-cut theorem:** minimum capacity of an \(s\)–\(t\) cut equals max flow. After computing max flow, let \(S=\) nodes reachable from \(s\) in the residual graph, \(T=V\setminus S\). Edges from \(S\) to \(T\) in the **original** network form a min cut. Modeling problems often ask to **choose a cut** (keep vs discard, open vs close) whose cost matches edge capacities you designed.

---

#### 4. Proof Sketches & Recurrences

Cut \((S,T)\): \(s\in S\), \(t\in T\), capacity \(\sum_{u\in S,v\in T} c(u,v)\). Any flow ≤ every cut. Equality achieved by residual reachability cut after max flow.

**Project selection sketch:** edge \(u\to v\) capacity \(\infty\) means “cannot take \(u\) without \(v\)” (closed set). Profit/cost encoded via edges to \(s\)/\(t\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: one max flow
- Per-query / per-operation: \(O(V+E)\) residual BFS for the cut set
- Total: dominated by max flow
- Memory: \(O(V+E)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Minimum cost to disconnect \(A\) from \(B\)”
- “Delete edges/nodes of minimum total weight”
- Project selection / closed set / “choose subset with pairwise penalties”
- Partition vertices into two labels with boundary costs

---

#### 7. Contest WA / TLE / RE Traps

- Computing cut before finishing max flow
- Using residual edges as “cut edges” instead of original forward saturated cross edges
- \(\infty\) capacity too small (overflow / still “finite”) → wrong closed-set models
- Forgetting undirected edges contribute once to cut capacity modeling

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Node cut:** vertex capacities (Part B §9)
- **Global min cut:** Stoer–Wagner / Karger — different problem (no fixed \(s,t\)); rare in CF
- **Gomory–Hu:** all-pairs min cuts — niche

---

#### 11. Typical Problem Archetypes

1. Standard application: min edge weight to disconnect \(s,t\)
2. Slightly disguised: max score = const − min cut (project selection)
3. Difficult: multi-label reductions to binary cuts / successive cuts
4. Very difficult / advanced: planar dual shortest paths as min cut

---

#### 12. Recognition & Identification Drills

1. Remove minimum total road length so city A cannot reach city B?
2. Open/close factories with profits and pairwise conflict costs?
3. Pixel labeling FG/BG with smoothness penalties — cut?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: disconnect / partition / closed-set scoring
- Key invariant: max flow = min cut capacity
- Key formula: \(S=\) residual-reachable from \(s\)
- Complexity: flow + \(O(V+E)\)
- Template to remember: Dinic then residual BFS

---

## 4. Bipartite Matching

---


---

<a id="topic-4"></a>
### 4. Bipartite Cardinality Matching (Kuhn)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Graphs, DFS, bipartite graphs  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Graphs, DFS, bipartite graphs

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Match left nodes to right nodes with no shared vertex. Kuhn: for each left vertex, DFS looking for an **augmenting path** in the alternating sense (free right, or rematch via `pair_of`). Maximum matching size = max number of such assignments. Equivalent to unit-cap flow \(s\to L\to R\to t\). Hall’s theorem explains impossibility; in contest you compute size / reconstruct pairs.

---

#### 4. Proof Sketches & Recurrences

Augmenting path flips matching status → size +1. Kuhn tries each left node once per “round” with visited marks; \(O(VE)\) worst-case.

Flow view: caps \(s\to L = 1\), \(L\to R = 1\) (or ∞ if multi ok), \(R\to t = 1\); max flow = matching size.

König: min bipartite vertex cover = max matching.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(E)\)
- Per-query / per-operation: \(O(VE)\) Kuhn
- Total: \(O(VE)\); or Dinic \(O(E\sqrt V)\)
- Memory: \(O(V+E)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Assign jobs to workers,” “boys–girls,” “rows–columns”
- Grid / chessboard placement with attacks → bipartite
- Independent set / vertex cover on bipartite (König)
- “Each item used at most once on each side”

---

#### 7. Contest WA / TLE / RE Traps

- Not resetting `vis` timer per DFS attempt
- 1-index / 0-index left-right mixups
- Assuming matching is unique
- Using general matching (blossom) when graph is bipartite

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Maximum edge-weighted bipartite matching:** Hungarian / MCMF
- **Multiple slots:** capacity on \(s\to L\) or \(R\to t\) via flow
- **König cover / independent set:** derive from max matching
- **Dinic reduction:** preferred when you already trust your Dinic

---

#### 11. Typical Problem Archetypes

1. Standard application: max jobs assigned
2. Slightly disguised: place rooks / students in timeslots
3. Difficult: min path cover in DAG = \(n -\) matching in transit graph
4. Very difficult / advanced: matchings with side constraints → flow

---

#### 12. Recognition & Identification Drills

1. \(n\) tasks, \(m\) machines, compatibility list — max assignments?
2. DAG: minimum paths to cover all vertices?
3. Bipartite graph: size of maximum independent set?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: bipartite assignment, cardinality
- Key invariant: augmenting paths
- Key formula: matching = flow through unit bipartite network
- Complexity: \(O(VE)\) or \(O(E\sqrt V)\)
- Template to remember: Kuhn DFS or Dinic \(s\)–\(L\)–\(R\)–\(t\)

---

## 5. Hopcroft–Karp

---


---

<a id="topic-5"></a>
### 5. Hopcroft–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2500 | **Frequency:** Occasional  
> **Prerequisites:** Bipartite matching, BFS+DFS layers  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Bipartite matching, BFS+DFS layers

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Kuhn finds one augmenting path at a time. Hopcroft–Karp finds a **maximal set of shortest augmenting paths** each phase (BFS builds distance layers on free vertices; DFS walks them disjointly) — same spirit as Dinic on the bipartite unit network. Use when \(n,m,E\) are large and Kuhn TLEs.

---

#### 4. Proof Sketches & Recurrences

Phases \(O(\sqrt V)\); each phase \(O(E)\) → \(O(E\sqrt V)\). Equivalent order to Dinic on unit bipartite flow.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: \(O(E\sqrt V)\)
- Total: \(O(E\sqrt V)\)
- Memory: \(O(V+E)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Bipartite matching with \(E\sim 10^5\), \(V\sim 10^5\) under tight TL
- Editorial mentions Hopcroft–Karp / \(O(E\sqrt V)\)
- You already know Dinic: implementing Dinic on matching network is equally valid

---

#### 7. Contest WA / TLE / RE Traps

- Wrong layer check (`dist[mr[v]] == dist[u] + 2`)
- Not blocking failed vertices → infinite loops / TLE
- Mixing L/R index spaces
- Preferring HK when Dinic template already passes

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Multiple edges / capacities >1 → use general Dinic, not HK
- Weighted → MCMF / Hungarian
- Dinic-on-bipartite as drop-in replacement

---

#### 11. Typical Problem Archetypes

1. Standard application: large bipartite matching cardinality
2. Slightly disguised: tiling / pairing at scale
3. Difficult: repeated matchings in binary search on threshold graph
4. Very difficult / advanced: HK inside more complex reductions (rare)

---

#### 12. Recognition & Identification Drills

1. \(2\cdot 10^5\) possible internship pairs — max matching under 1s TL?
2. Threshold: max edges with weight \(\ge x\) forming matching of size \(k\)?
3. Same as Kuhn problem but TL halved — which algorithm?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: large bipartite cardinality matching
- Key invariant: shortest augmenting paths in phases
- Key formula: \(O(E\sqrt V)\)
- Complexity: \(O(E\sqrt V)\)
- Template to remember: BFS layers + DFS disjoint shortest paths

---

Continue: [09-b-network-flow-mcmf-recognition.md](09-b-network-flow-mcmf-recognition.md) (MCMF → recognition).

---


---

<a id="topic-6"></a>
### 6. Min-Cost Max-Flow (MCMF)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, shortest paths (Bellman–Ford / Dijkstra + potentials)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Max flow, shortest paths (Bellman–Ford / Dijkstra + potentials)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Among all maximum flows (or flows of value \(K\)), pick one with **minimum total cost** \(\sum f_e\cdot w_e\). Residual edges carry costs: forward \(+w\), backward \(-w\). Each augmentation along a **shortest path by cost** in the residual graph yields an optimal successive-shortest-path algorithm. With **potentials** (reduced costs \(w^h(u,v)=w(u,v)+h(u)-h(v)\ge 0\)), Dijkstra works after the first BF/zero init — mandatory for contest speed.

---

#### 4. Proof Sketches & Recurrences

Successive shortest paths: \(O(F\cdot SP)\) where \(F\) is total flow. With Dijkstra + potentials: \(SP=O(E\log V)\) (or \(O(V^2)\)). Negative cycles in residual ⇒ can decrease cost without bound (or need canceling); for standard MCMF from zero flow with no neg cycle initially, potentials maintain non-negative reduced costs.

If only bipartite perfect matching dense \(n\le 400\): Hungarian \(O(n^3)\) often beats generic MCMF.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: \(O(F\cdot E\log V)\) typical Dijkstra MCMF
- Total: as above; \(F\) can be large — watch limits
- Memory: \(O(V+E)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Assignment with costs + capacities (“send exactly \(k\)”, “min cost to satisfy”)
- Grid path packing with costs
- “Greedy by cost fails” because of capacity conflicts
- Circulation with costs (min-cost circulation) — related

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting reverse edge cost \(=-w\)
- Dijkstra without potentials when neg residual costs exist → WA
- Overflow on `flow * cost`
- Maximizing cost: negate weights
- Stopping at max flow when problem wants flow exactly \(k\) (or any flow with min cost — different)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Min-cost circulation** (cancel neg cycles) — related niche
- **Capacity scaling / cost scaling** — rare in CF
- **Hungarian** for dense bipartite assignment
- **Primal-dual** variants — same complexity class

---

#### 11. Typical Problem Archetypes

1. Standard application: min cost to send \(k\) units \(s\to t\)
2. Slightly disguised: assign rows to cols with costs + “must use all”
3. Difficult: build gadgets so cost encodes penalties / bonuses
4. Very difficult / advanced: MCMF on time-expanded graphs

---

#### 12. Recognition & Identification Drills

1. Taxi rides: match taxis to customers with travel cost; each taxi one ride?
2. Send exactly 10 units through a network with edge costs — min cost?
3. Place \(n\) pieces on a grid with distance costs and cell capacities?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: flow + linear edge costs
- Key invariant: successive shortest residual paths
- Key formula: reduced costs \(w+h(u)-h(v)\)
- Complexity: \(O(F E\log V)\)
- Template to remember: MCMF + potentials + Dijkstra

---

## 7. Flow with Lower Bounds

---


---

<a id="topic-7"></a>
### 7. Flows with Lower Bounds on Edges

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Max flow, circulation ideas  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Max flow, circulation ideas

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Edge must carry flow in \([\ell,c]\), not \([0,c]\). Force \(\ell\) by sending \(\ell\) “already,” leaving residual capacity \(c-\ell\), and fixing **imbalance** at vertices with a super-source/sink demand network. Feasibility first; then maximize additional flow \(s\to t\) if needed. Early-contest ROI is low — learn the reduction, don’t memorize every variant until forced.

---

#### 4. Proof Sketches & Recurrences

For each edge \(u\to v\) with \([\ell,c]\): put residual edge capacity \(c-\ell\). Vertex balance \(b(x)=\sum \ell_{\mathrm{in}}-\sum \ell_{\mathrm{out}}\). If \(b(x)>0\), demand \(b(x)\) (edge from \(x\) to \(T'\)); if \(b(x)<0\), supply \(-b(x)\) (edge \(S'\to x\)). Add edge \(t\to s\) with capacity \(\infty\) for circulation between original terminals when finding feasible \(s\)–\(t\) flow with lowers. Feasible iff max flow from \(S'\) to \(T'\) saturates all supplies.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\) build
- Per-query / per-operation: one Dinic on \(O(V+E)\)
- Total: Dinic complexity
- Memory: \(O(V+E)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “At least \(L_e\) must go through edge \(e\)”
- “Lower and upper quotas on flights / pipes”
- Statements with both minimum and maximum usage

---

#### 7. Contest WA / TLE / RE Traps

- Sign error on balance \(b(v)\)
- Forgetting \(t\to s\) link when forcing \(s\)–\(t\) structure
- \(\ell>c\) not checked
- Using lowers without saturating supply/demand check

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Lower bounds only on some edges
- Vertex lower bounds → split + edge lowers
- Min-cost with lowers → MCMF on the transformed network

---

#### 11. Typical Problem Archetypes

1. Standard application: feasible flow with \([\ell,c]\)
2. Slightly disguised: “each edge used at least once” in Eulerian-ish flow clothing
3. Difficult: max flow with lowers + costs
4. Very difficult / advanced: dynamic lowers (rare)

---

#### 12. Recognition & Identification Drills

1. Every pipe must carry at least 5 units, at most 20 — is a valid shipping possible?
2. Flights with minimum passenger guarantees and seat caps?
3. Round-trip circulation where each arc has a minimum load?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: edge quotas \([\ell,c]\)
- Key invariant: fix \(\ell\), balance via \(S',T'\)
- Key formula: \(b(v)=\sum\ell_{\mathrm{in}}-\sum\ell_{\mathrm{out}}\)
- Complexity: one max flow
- Template to remember: demand network + Dinic saturate supplies

---

## 8. Circulation

---


---

<a id="topic-8"></a>
### 8. Circulation (Feasibility / Balances)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Flow with lower bounds, max flow  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Flow with lower bounds, max flow

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

A **circulation** is a flow with **no** distinguished \(s,t\) — conservation at every vertex. With upper caps (and often lowers), feasibility reduces to the lower-bound transform: supplies/demands from compulsory flow, then max flow \(S'\to T'\) must meet \(\sum\) supply. Min-cost circulation cancels negative-cost residual cycles. Treat as niche early; same gadgets as §7.

---

#### 4. Proof Sketches & Recurrences

Same as §7 without original \(s,t\). Feasibility iff demand max-flow saturates. Hoffman circulation theorem: for every cut, capacity constraints vs lower bounds — in CP you compute, don’t check all cuts.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: one Dinic
- Total: Dinic
- Memory: \(O(V+E)\)`

##### C++17 Template

```cpp
// C++17 — circulation feasibility with [lo,hi] on edges (no s,t)
namespace circ {
bool feasible(int n, const vector<lower_flow::EdgeReq> &edges) {
  return lower_flow::feasible_with_lowers(n, edges, nullptr);
}
} // namespace circ
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Flow around a network,” no single source
- Balanced transports / tour decompositions with capacities
- Edge lower bounds without \(s,t\)

---

#### 7. Contest WA / TLE / RE Traps

- Confusing circulation with \(s\)–\(t\) flow
- Missing edges in balance computation
- Cost circulation with undetected neg cycle (unbounded)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Circulation with demands \(d(v)\) (imbalances) — same \(S',T'\)
- Bounded circulation + max throughput elsewhere

---

#### 11. Typical Problem Archetypes

1. Standard application: exists circulation respecting \([\ell,c]\)
2. Slightly disguised: rearrange tokens on graph with edge limits
3. Difficult: min-cost circulation encoding scheduling
4. Very difficult / advanced: parametric circulations

---

#### 12. Recognition & Identification Drills

1. Directed roads with min/max traffic; can traffic be balanced everywhere?
2. Reorient / reroute flow to satisfy lower bounds with zero external supply?
3. Tournament scheduling as circulation? (often yes in editorials)

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: conservation everywhere + bounds
- Key invariant: supply/demand saturation
- Key formula: same \(b(v)\) as lowers
- Complexity: one max flow
- Template to remember: §7 reduction without \(s,t\)

---

## 9. Vertex Capacities

---


---

<a id="topic-9"></a>
### 9. Vertex Capacities (Node Split)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2500 | **Frequency:** Occasional  
> **Prerequisites:** Max flow modeling  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Max flow modeling

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

If a **vertex** \(v\) may be used by at most \(c_v\) flow, split into \(v_{\mathrm{in}}\to v_{\mathrm{out}}\) with capacity \(c_v\). Original edge \(u\to v\) becomes \(u_{\mathrm{out}}\to v_{\mathrm{in}}\) (edge cap unchanged). This turns vertex cuts / “robots through cities” into ordinary edge-cap flow.

---

#### 4. Proof Sketches & Recurrences

Any flow through \(v\) must cross the split edge ⇒ limited by \(c_v\). Correctness: bijection between flows in original vertex-cap network and edge-cap network on split graph.

\(V'=2V\), \(E'=E+V\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(V+E)\) split
- Per-query / per-operation: Dinic on \(2V\) vertices
- Total: Dinic complexity on split network
- Memory: \(O(V+E)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Each city can be visited by at most \(k\) paths”
- Min vertices to delete to disconnect \(s,t\) (unit vertex caps)
- Servers with processing limits; edges unlimited or separate

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to split \(s\) or \(t\) correctly (often leave infinite through terminals)
- Wiring `u_in → v_in` by mistake
- Unit vertex-disjoint paths need cap \(1\) on splits
- Double-limiting undirected edges

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Only some vertices capacitated
- Vertex costs → MCMF on split edge
- Vertex lowers → lower bounds on split edge

---

#### 11. Typical Problem Archetypes

1. Standard application: max flow with node bandwidths
2. Slightly disguised: min nodes to remove to disconnect (unit caps)
3. Difficult: mix edge + vertex capacities
4. Very difficult / advanced: time-expanded + vertex caps

---

#### 12. Recognition & Identification Drills

1. At most 3 agents may pass each junction — max agents \(s\to t\)?
2. Destroy minimum number of stations to separate two cities?
3. CPU nodes have job limits; network links have bandwidth — max jobs?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: limits on vertices / vertex cuts
- Key invariant: all flow through \(v\) crosses split
- Key formula: \(v_{\mathrm{in}}\to v_{\mathrm{out}}\) cap \(c_v\)
- Complexity: Dinic on \(2V\)
- Template to remember: split nodes

---

## 10. Edge-Disjoint / Vertex-Disjoint Paths

---


---

<a id="topic-10"></a>
### 10. Edge-Disjoint & Vertex-Disjoint Paths

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Max flow, vertex capacities (for vertex-disjoint)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Max flow, vertex capacities (for vertex-disjoint)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

**Edge-disjoint** \(s\)–\(t\) paths: every edge capacity \(1\), max flow = max number of paths (integral). **Vertex-disjoint** (internally): unit capacities on vertex splits (and usually edges capacity \(1\)). Menger’s theorem: min edge cut = max edge-disjoint paths; min vertex cut = max internally vertex-disjoint paths.

---

#### 4. Proof Sketches & Recurrences

Integral flow decomposition: any integral flow of value \(k\) decomposes into \(k\) paths (+ cycles). Unit caps ⇒ paths are edge-disjoint. Vertex unit splits ⇒ internally vertex-disjoint.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(E)\)
- Per-query / per-operation: Dinic; unit networks often fast
- Total: \(O(E\sqrt V)\)-class typical for unit
- Memory: \(O(V+E)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Maximum number of routes that don’t share roads/cities”
- Connectivity checks with disjointness
- DAG path packing (sometimes matching; sometimes flow)

---

#### 7. Contest WA / TLE / RE Traps

- Undirected graph: capacity 1 each direction can allow “use both ways” weirdness — use one undirected residual carefully or cap 1 total via undirected modeling
- Allowing \(s\) or \(t\) to be “blocked” by vertex cap 1
- Counting walks that reuse vertices when asking vertex-disjoint

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Length-bounded disjoint paths — harder (not plain flow)
- Disjoint paths with costs — MCMF unit
- \(k\) pairs multi-commodity — generally NP-hard; not single commodity flow

---

#### 11. Typical Problem Archetypes

1. Standard application: max edge-disjoint \(s\)–\(t\) paths
2. Slightly disguised: connectivity = disjoint paths by Menger
3. Difficult: reconstruct the paths explicitly
4. Very difficult / advanced: disjoint paths in planar graphs with extras

---

#### 12. Recognition & Identification Drills

1. Max number of bus routes sharing no road from depot to airport?
2. Max internally vertex-disjoint paths in a directed city graph?
3. Undirected cubic graph connectivity between two vertices?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: disjoint route packing / Menger
- Key invariant: unit-cap integral flow ↔ paths
- Key formula: edge-disjoint = unit edge flow; vertex = split + unit
- Complexity: unit Dinic
- Template to remember: cap 1 (+ split)

---

## 11. How to Recognize When a Problem Is Secretly a Flow Problem (Synthesis)

---


---

<a id="topic-11"></a>
### 11. Flow Modeling Recognition (Meta-Skill)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1800–2500 | **Frequency:** Common  
> **Prerequisites:** Matching, Dinic, min cut, basic gadgets (this section)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Matching, Dinic, min cut, basic gadgets (this section)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Flow problems rarely say “compute max flow.” They say **assign, cut, route, saturate, separate, cover with paths**. Your job is to invent vertices/edges so that **feasible integral flows ↔ valid solutions** and **objective ↔ flow value or cut capacity**. If the hard part is conflicts of limited resources along graphs, think flow before DP.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: modeling time dominates human side
- Per-query / per-operation: underlying Dinic/MCMF/matching
- Total: as chosen engine
- Memory: as engine + gadget nodes`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Limited capacities / “at most \(k\) through …”
- Assignment between two sides (→ matching / flow)
- Min cost to separate / delete / cut
- Path cover / disjoint routes
- “Max score = constant − penalty” with pairwise or cut penalties
- Binary decisions with implication “A forces B” (\(\infty\) edges in cut models)
- Multiple sources/sinks, supplies/demands
- Reductions mentioned in editorials: matching, cut, Dinic

---

#### 7. Contest WA / TLE / RE Traps

- Wrong \(\infty\) (too small) breaking forced implications
- Off-by-one on “at most \(k\)” vs “exactly \(k\)” (exactly → often lower bounds or force flow value)
- Building a flow when bipartite matching sufficed (wasted time) or vice versa
- Non-integral assumptions when problem needs counts (use integral caps)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Binary search on answer + feasibility flow
- Flow on state graphs (time × node)
- Matching reductions (DAG min path cover)

---

#### 11. Typical Problem Archetypes

1. Standard application: explicit capacities
2. Slightly disguised: assignment / path cover
3. Difficult: cut = optimization score
4. Very difficult / advanced: layered gadgets + MCMF + binary search

---

#### 12. Recognition & Identification Drills

1. Maximize profit of open projects with dependencies and conflict penalties — algorithm family?
2. Cover all vertices of a DAG with minimum paths — which graph do you match on?
3. Evacuation: each hallway capacity \(c_e\), each intersection holds \(\le p_v\) people — model?
4. Select a subset of websites to hack with gains; if you hack A you must hack B — flow/cut?
5. Min cost to assign every student a unique dorm with prefs — matching or MCMF?

---

#### 13. Fast-Lookup Cheat Sheet

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


---

<a id="topic-12"></a>
### 12. What to drill this week

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2500
- Prerequisites: Max Flow, Min-Cut, Bipartite Matching, Project Selection

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Flow networks solve resource allocation, constraint satisfiability, and bipartite assignment. The central contest paradigm is the **Max-Flow Min-Cut Theorem**: finding maximum flow from source to sink simultaneously identifies the minimum capacity edge set whose removal disconnects source from sink.

---

#### 4. Proof Sketches & Recurrences

Dinic's algorithm constructs a layered level graph via BFS and finds blocking flows via DFS with current-arc optimization. It runs in $\mathcal{O}(V^2 E)$ generally and strictly in $\mathcal{O}(E \sqrt{V})$ on unit capacity networks.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Dinic Blocking Flow Algorithm with Current-Arc Pruning
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

struct Dinic {
    struct Edge { int to; ll cap, flow; int rev; };
    int n, s, t;
    vector<vector<Edge>> adj;
    vector<int> level, ptr;
    Dinic(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1), level(n_ + 1), ptr(n_ + 1) {}
    void add_edge(int from, int to, ll cap) {
        adj[from].push_back({to, cap, 0, (int)adj[to].size()});
        adj[to].push_back({from, 0, 0, (int)adj[from].size() - 1});
    }
    bool bfs() {
        fill(level.begin(), level.end(), -1);
        level[s] = 0; queue<int> q; q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (auto& e : adj[v]) {
                if (e.cap - e.flow > 0 && level[e.to] == -1) {
                    level[e.to] = level[v] + 1; q.push(e.to);
                }
            }
        }
        return level[t] != -1;
    }
    ll dfs(int v, ll pushed) {
        if (pushed == 0 || v == t) return pushed;
        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {
            auto& e = adj[v][cid];
            if (level[v] + 1 != level[e.to] || e.cap - e.flow == 0) continue;
            ll tr = dfs(e.to, min(pushed, e.cap - e.flow));
            if (tr == 0) continue;
            e.flow += tr; adj[e.to][e.rev].flow -= tr;
            return tr;
        }
        return 0;
    }
    ll max_flow() {
        ll flow = 0;
        while (bfs()) {
            fill(ptr.begin(), ptr.end(), 0);
            while (ll pushed = dfs(s, INF)) flow += pushed;
        }
        return flow;
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Project Selection: picking items with positive profits and prerequisite costs.
- Maximum Bipartite Matching: assigning students to mentors, tasks to processors.
- Minimum Path Cover in DAGs: decomposing tasks into disjoint execution paths.
- Grid cell coloring / chessboard adjacency reductions (bipartite cuts).

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to add backward edge with 0 initial capacity.
- Omitting current-arc pointers `ptr[v]` in Dinic's DFS, degrading $\mathcal{O}(V^2 E)$ to $\mathcal{O}(V E^2)$.
- Integer overflow when adding large capacities: use `long long` for all flow variables.
- Incorrect Min-Cut vertex reconstruction: cut consists of edges $(u, v)$ where `level[u] != -1` and `level[v] == -1`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-13"></a>
### 13. Hungarian Algorithm (Kuhn-Munkres)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2600 | **Frequency:** Occasional  
> **Prerequisites:** Bipartite Matching  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2600
- Prerequisites: Bipartite Matching

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

While MCMF solves min-cost matching, it relies on shortest paths which take $O(VE)$ per unit of flow. For a dense $N \times N$ complete bipartite graph, $V=2N, E=N^2$, making MCMF $O(N^4)$. The **Hungarian algorithm** solves the assignment problem in strictly $O(N^3)$ by maintaining vertex potentials (labels) and searching for augmenting paths efficiently.

---

#### 4. Proof Sketches & Recurrences

Linear Programming Dual for bipartite matching: $\max \sum u_i + \sum v_j$ subject to $u_i + v_j \le A_{i, j}$. By complementary slackness, an edge $(i, j)$ carries positive flow only if $u_i + v_j = A_{i, j}$. In each step, the algorithm maintains feasible potentials $u, v$. The slack array $slack[j] = \min_{i \in S} (A_{i, j} - u_i - v_j)$ tracks the minimum gap to bring an unvisited right-hand vertex $j$ into the alternating tree. Potentials are updated in $\mathcal{O}(N)$ using $\delta = \min_{j \notin T} slack[j]$, taking $\mathcal{O}(N^2)$ per matched left vertex.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
const long long INF = 1e18;
// cost matrix 1-indexed, N rows (jobs), M cols (workers), N <= M
// Returns min cost and assignment array `match` where match[j] = i
long long hungarian(const vector<vector<long long>>& a) {
    int n = a.size() - 1;
    int m = a[0].size() - 1;
    vector<long long> u(n + 1), v(m + 1), p(m + 1), way(m + 1);
    for (int i = 1; i <= n; ++i) {
        p[0] = i;
        int j0 = 0;
        vector<long long> minv(m + 1, INF);
        vector<bool> used(m + 1, false);
        do {
            used[j0] = true;
            int i0 = p[j0], j1 = 0;
            long long delta = INF;
            for (int j = 1; j <= m; ++j) {
                if (!used[j]) {
                    long long cur = a[i0][j] - u[i0] - v[j];
                    if (cur < minv[j]) {
                        minv[j] = cur;
                        way[j] = j0;
                    }
                    if (minv[j] < delta) {
                        delta = minv[j];
                        j1 = j;
                    }
                }
            }
            for (int j = 0; j <= m; ++j) {
                if (used[j]) {
                    u[p[j]] += delta;
                    v[j] -= delta;
                } else {
                    minv[j] -= delta;
                }
            }
            j0 = j1;
        } while (p[j0] != 0);
        do {
            int j1 = way[j0];
            p[j0] = p[j1];
            j0 = j1;
        } while (j0);
    }
    return -v[0]; // min cost
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- ```cpp
const long long INF = 1e18;
// cost matrix 1-indexed, N rows (jobs), M cols (workers), N <= M
// Returns min cost and assignment array `match` where match[j] = i
long long hungarian(const vector<vector<long long>>& a) {
    int n = a.size() - 1;
    int m = a[0].size() - 1;
    vector<long long> u(n + 1), v(m + 1), p(m + 1), way(m + 1);
    for (int i = 1; i <= n; ++i) {
        p[0] = i;
        int j0 = 0;
        vector<long long> minv(m + 1, INF);
        vector<bool> used(m + 1, false);
        do {
            used[j0] = true;
            int i0 = p[j0], j1 = 0;
            long long delta = INF;
            for (int j = 1; j <= m; ++j) {
                if (!used[j]) {
                    long long cur = a[i0][j] - u[i0] - v[j];
                    if (cur < minv[j]) {
                        minv[j] = cur;
                        way[j] = j0;
                    }
                    if (minv[j] < delta) {
                        delta = minv[j];
                        j1 = j;
                    }
                }
            }
            for (int j = 0; j <= m; ++j) {
                if (used[j]) {
                    u[p[j]] += delta;
                    v[j] -= delta;
                } else {
                    minv[j] -= delta;
                }
            }
            j0 = j1;
        } while (p[j0] != 0);
        do {
            int j1 = way[j0];
            p[j0] = p[j1];
            j0 = j1;
        } while (j0);
    }
    return -v[0]; // min cost
}
```

---

#### 7. Contest WA / TLE / RE Traps

- Dimensions mismatch: graph requires $N \le M$ (more tasks than workers); if $N > M$, pad matrix with dummy zero-cost columns.
- Maximization vs minimization: to find maximum weight matching, negate costs $C_{i, j} = -C_{i, j}$ or use $C_{i, j} = \text{MAX} - C_{i, j}$.
- Integer overflow in potentials: accumulating large weights requires 64-bit integer `long long` for $u, v, minv, delta$.
- 1-based indexing confusion: standard Hungarian template reserves index 0 for the dummy augmenting node.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-14"></a>
### 14. Dinic vs Edmonds–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Max-Flow / Min-Cut
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Augmenting Paths, BFS, DFS, Level Graphs, Blocking Flows
- Tradeoff: Edmonds-Karp runs in $\mathcal{O}(V E^2)$ (too slow for $N > 100$); Dinic's runs in $\mathcal{O}(V^2 E)$, and $\mathcal{O}(E \sqrt{V})$ on unit capacity graphs.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Both Edmonds-Karp and Dinic find shortest augmenting paths using BFS. However, Edmonds-Karp finds a single augmenting path per BFS traversal and immediately updates residual capacities. Dinic decomposes the computation: a single BFS constructs a *level graph* (DAG of shortest paths), and a DFS with pointer work finds a *blocking flow* (saturating multiple augmenting paths simultaneously in the same level graph). Once blocked, the source-sink distance strictly increases by $\ge 1$. Thus, Dinic requires at most $V - 1$ BFS phases.

---

#### 4. Proof Sketches & Recurrences

In Dinic's algorithm, the distance from source $S$ to sink $T$ in the level graph strictly increases after each phase: $dist_{k+1}(S, T) > dist_k(S, T)$. Hence there are at most $V - 1$ phases. In each phase, the DFS advances along unsaturated edges; whenever an edge is saturated or a dead-end is reached, the current-arc pointer increments. Across the phase, total time spent retreating is $\mathcal{O}(V E)$ and total time advancing is $\mathcal{O}(V E)$, giving $\mathcal{O}(V E)$ per phase, or $\mathcal{O}(V^2 E)$ total. On unit capacity networks, the number of phases is $\mathcal{O}(\sqrt{V})$ or $\mathcal{O}(E^{1/2})$, yielding $\mathcal{O}(E \sqrt{V})$ or $\mathcal{O}(E \min(V^{2/3}, E^{1/2}))$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Dinic's Algorithm (Fast competitive programming standard)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Dinic {
    struct Edge { int to; ll cap, flow; int rev; };
    int n, s, t;
    vector<vector<Edge>> adj;
    vector<int> level, ptr;
    Dinic(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1), level(n_ + 1), ptr(n_ + 1) {}
    void add_edge(int from, int to, ll cap) {
        adj[from].push_back({to, cap, 0, (int)adj[to].size()});
        adj[to].push_back({from, 0, 0, (int)adj[from].size() - 1});
    }
    bool bfs() {
        fill(level.begin(), level.end(), -1);
        level[s] = 0; queue<int> q; q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (auto& edge : adj[v]) {
                if (edge.cap - edge.flow > 0 && level[edge.to] == -1) {
                    level[edge.to] = level[v] + 1;
                    q.push(edge.to);
                }
            }
        }
        return level[t] != -1;
    }
    ll dfs(int v, ll pushed) {
        if (pushed == 0 || v == t) return pushed;
        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {
            auto& edge = adj[v][cid];
            int trg = edge.to;
            if (level[v] + 1 != level[trg] || edge.cap - edge.flow == 0) continue;
            ll tr = dfs(trg, min(pushed, edge.cap - edge.flow));
            if (tr == 0) continue;
            edge.flow += tr;
            adj[trg][edge.rev].flow -= tr;
            return tr;
        }
        return 0;
    }
    ll max_flow() {
        ll flow = 0;
        while (bfs()) {
            fill(ptr.begin(), ptr.end(), 0);
            while (ll pushed = dfs(s, 1e18)) flow += pushed;
        }
        return flow;
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Network capacity graph with $V \le 5000, E \le 30000$ where Edmonds-Karp would TLE.
- Unit network matching (e.g., bipartite matching via flow) where Dinic executes in blinding $\mathcal{O}(E \sqrt{V})$ speed.
- Project selection problem (closure graph with positive weights to source, negative to sink).
- Minimum cut partitioning where min-cut capacity equals max flow.

---

#### 7. Contest WA / TLE / RE Traps

- Omitting the current-arc pointer `int& cid = ptr[v]` in DFS, degenerating Dinic to Edmonds-Karp complexity $\mathcal{O}(V E^2)$.
- Forgetting that backward residual edge has capacity 0 initially (`adj[to].push_back({from, 0, 0, ...})`) for directed graphs.
- Integer overflow: capacities or flow sum exceed $2^{31} - 1$; always use `long long` for `cap` and `flow`.
- Resetting `ptr` inside BFS rather than before the blocking DFS loop.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-15"></a>
### 15. Dinic vs Hopcroft–Karp

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Bipartite Matching, Dinic's Algorithm, Hopcroft-Karp
- Tradeoff: Hopcroft-Karp is mathematically identical to Dinic on unit bipartite networks; knowing this saves memorizing two separate algorithms.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Hopcroft-Karp is specifically Dinic's algorithm specialized for bipartite matching networks. In a bipartite graph with unit capacity edges, Dinic's level graph BFS finds shortest alternating paths from unmatched left nodes to unmatched right nodes, and the DFS augments along vertex-disjoint paths in $\mathcal{O}(E \sqrt{V})$ time. Dinic's algorithm achieves this exact same $\mathcal{O}(E \sqrt{V})$ bound naturally on unit networks without requiring a bespoke Hopcroft-Karp implementation.

---

#### 4. Proof Sketches & Recurrences

In unit bipartite graphs, every vertex in $L \cup R$ has either in-degree 1 or out-degree 1 in the residual network. Therefore, augmenting paths in a single phase are strictly vertex-disjoint. After $k$ phases of augmentation, the length of the shortest augmenting path is at least $k + 1$, and the difference between the current matching $M$ and maximum matching $M^*$ satisfies $|M^* \setminus M| \le V / k$. Balancing $k = \sqrt{V}$ yields $\mathcal{O}(\sqrt{V})$ phases, with $\mathcal{O}(E)$ work per phase.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Hopcroft-Karp Bipartite Matching via Dinic or Dedicated Array HK
#include <bits/stdc++.h>
using namespace std;

struct HopcroftKarp {
    int n, m; // Sizes of left (1..n) and right (1..m) sets
    vector<vector<int>> adj;
    vector<int> pair_u, pair_v, dist;
    HopcroftKarp(int n_, int m_) : n(n_), m(m_), adj(n_ + 1), pair_u(n_ + 1, 0), pair_v(m_ + 1, 0), dist(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); }
    bool bfs() {
        queue<int> q;
        for (int u = 1; u <= n; ++u) {
            if (pair_u[u] == 0) { dist[u] = 0; q.push(u); }
            else dist[u] = INT_MAX;
        }
        dist[0] = INT_MAX;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            if (dist[u] < dist[0]) {
                for (int v : adj[u]) {
                    if (dist[pair_v[v]] == INT_MAX) {
                        dist[pair_v[v]] = dist[u] + 1;
                        q.push(pair_v[v]);
                    }
                }
            }
        }
        return dist[0] != INT_MAX;
    }
    bool dfs(int u) {
        if (u == 0) return true;
        for (int v : adj[u]) {
            if (dist[pair_v[v]] == dist[u] + 1 && dfs(pair_v[v])) {
                pair_v[v] = u; pair_u[u] = v;
                return true;
            }
        }
        dist[u] = INT_MAX;
        return false;
    }
    int max_matching() {
        int matching = 0;
        while (bfs()) for (int u = 1; u <= n; ++u) if (pair_u[u] == 0 && dfs(u)) matching++;
        return matching;
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Bipartite graph matching where $N, M \le 5 \times 10^4$ and $E \le 2 \times 10^5$ (Kuhn's $\mathcal{O}(V E)$ will TLE; Hopcroft-Karp/Dinic passes in 100ms).
- Maximum Independent Set on bipartite graph ($|MIS| = |V| - |\text{Max Matching}|$).
- Minimum Vertex Cover on bipartite graph (Kőnig's Theorem: $|\text{MVC}| = |\text{Max Matching}|$).
- Minimum Path Cover in a Directed Acyclic Graph (DAG).

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one indexing on 0-based vs 1-based left/right partitions (Hopcroft-Karp uses index 0 as dummy unmatched node).
- Graph is not bipartite: applying Hopcroft-Karp or Dinic bipartite reduction on general graphs with odd cycles fails (requires Edmond's Blossom).
- Forgetting to reconstruct minimum vertex cover by DFS reachability from unmatched left vertices in residual graph.
- Reusing `dist` array across iterations without re-clearing.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-16"></a>
### 16. Matching vs General Flow

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Max Flow, Bipartite Matching, General Matching (Blossom), Capacitated Networks
- Tradeoff: Deciding between specialized bipartite matching, general graph matching, and general network flow models.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

When encountering an assignment problem, check graph structure: 1) Is the graph bipartite? If yes and unweighted, use Hopcroft-Karp or Dinic $\mathcal{O}(E \sqrt{V})$. 2) Is it bipartite with edge costs? Use Hungarian algorithm $\mathcal{O}(V^3)$ or MCMF $\mathcal{O}(F \cdot E \log V)$. 3) Is the graph general (non-bipartite, odd cycles present)? Bipartite matching and network flow FAIL! You must use Blossom Algorithm $\mathcal{O}(V^3)$ or Tutte matrix randomized matching. 4) Do vertices or edges have capacities $> 1$, or intermediate transit nodes? General network flow is mandatory.

---

#### 4. Proof Sketches & Recurrences

Max flow models rely on the total unimodularity of bipartite incidence matrices: the linear programming relaxation has integral extreme points. In general non-bipartite graphs, odd cycles introduce fractional vertices (e.g., triangle with 0.5 flow on each edge gives 1.5 matching, impossible for discrete matching). Edmonds' Blossom algorithm contracts odd cycles into supernodes to restore augmenting path properties.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Decision Matrix Dispatcher
// General Network Flow vs Bipartite Matching
#include <bits/stdc++.h>
using namespace std;

// Check if graph is 2-colorable (bipartite)
bool is_bipartite(int n, const vector<vector<int>>& adj, vector<int>& color) {
    color.assign(n + 1, -1);
    for (int i = 1; i <= n; ++i) {
        if (color[i] != -1) continue;
        queue<int> q; q.push(i); color[i] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) return false; // Odd cycle found!
            }
        }
    }
    return true;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Grid cells where interactions occur only between adjacent cells (grids are naturally bipartite: $(r + c) \pmod 2$).
- Domino tiling problems: bipartite matching between black and white checkerboard squares.
- Pairing items where relationships form arbitrary non-bipartite friendship graphs (requires Blossom).
- Multi-commodity or capacitated bounds per node: split node into $u_{\text{in}} \to u_{\text{out}}$ with capacity $c_u$.

---

#### 7. Contest WA / TLE / RE Traps

- Modeling general matching (odd cycles present) as a flow network: flow networks cannot handle non-bipartite vertex packing.
- Forgetting node capacities: to restrict a vertex to be used at most $K$ times, split $u \to (u_{in}, u_{out})$ with capacity $K$.
- Ignoring disconnected components when checking bipartiteness.
- Attempting to run Blossom algorithm when the constraints indicate $N \le 500$, but simple DP on tree or greedy would suffice.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-17"></a>
### 17. MCMF vs Greedy

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Min-Cost Max-Flow (MCMF), Slope Trick, Priority Queue / Regret Greedy
- Tradeoff: MCMF guarantees global optimality on complex network topologies but is $\mathcal{O}(F \cdot E \log V)$; Greedy with regret (simulated network flow) runs in $\mathcal{O}(N \log N)$ on linear or tree topologies.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

MCMF and greedy are two ends of convex optimization. When the underlying graph is a 1D sequence (e.g., buy/sell stock with transaction fees, pairing parentheses, matching intervals on a line), the min-cost flow problem exhibits total unimodularity and convexity. Instead of running a general graph MCMF algorithm, you can 'simulate' the augmenting paths of MCMF using two priority queues (Slope Trick / Regret Greedy). If the topology is an arbitrary graph or bipartite with irregular edges, general MCMF is required.

---

#### 4. Proof Sketches & Recurrences

The cost of sending $k$ units of flow $f(k)$ is piecewise linear and strictly convex: $f(k+1) - f(k) \ge f(k) - f(k-1)$ due to shortest augmenting path potentials. In 1D interval problems, the dual problem is equivalent to optimizing a convex function under slope changes. A priority queue tracks potential slopes, and choosing an element corresponds to augmenting flow; pushing the negative back into the queue allows the algorithm to 'cancel' or 'regret' an earlier choice along a residual backward edge in $\mathcal{O}(\log N)$ time.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Simulated Network Flow / Regret Greedy (Slope Trick) in O(N log N)
// Example: Buy and Sell Stock with Regret
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll simulated_mcmf_buy_sell(const vector<ll>& prices) {
    priority_queue<ll, vector<ll>, greater<ll>> pq;
    ll total_profit = 0;
    for (ll p : prices) {
        if (!pq.empty() && pq.top() < p) {
            total_profit += p - pq.top();
            pq.pop();
            pq.push(p); // Can regret selling here if a higher future price exists
        }
        pq.push(p); // Option to buy at current price
    }
    return total_profit;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Problem asks for min-cost matching of points on a line or timestamps in a schedule ($N \approx 2 \times 10^5$, MCMF would TLE).
- Arbitrary bipartite graph where left side wants to match right side with minimum total cost ($N \le 500$, reach for MCMF).
- Convex cost functions on edge flows (piecewise linear cost).
- Workload distribution where previous decisions can be revoked if a more profitable option arrives.

---

#### 7. Contest WA / TLE / RE Traps

- Attempting MCMF with $N = 10^5$; standard MCMF will heavily TLE (needs $\mathcal{O}(N \log N)$ simulated flow).
- In simulated flow, forgetting the regret element: failing to push the new state back into the priority queue prevents cancellation.
- Handling negative cycles in general MCMF without proper initial potentials or Bellman-Ford/SPFA initialization.
- Using floating-point costs without epsilon checks in MCMF.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-18"></a>
### 18. High-ROI (master first)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2200
- Prerequisites: Dinic Max-Flow, Bipartite Matching

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

In rated competitive programming, over 80% of flow problems do not require esoteric minimum cost flows or Gomory-Hu trees; they reduce cleanly to either **Unit Network Matching** or **Project Selection Min-Cut**. Master these two archetypes first.

---

#### 4. Proof Sketches & Recurrences

Project Selection: positive reward nodes connect to source with capacity $P_i$; negative cost nodes connect to sink with capacity $C_i$; dependency $u \to v$ has infinite capacity $\infty$. Maximum profit equals $\sum P_i - \text{MinCut}$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Project Selection / Closure Reduction Scaffold
#include <bits/stdc++.h>
using namespace std;
// Uses Dinic with Source = 0, Sink = N + 1
// For profit item i: dinic.add_edge(0, i, profit)
// For cost item j:   dinic.add_edge(j, sink, cost)
// Dependency i -> j: dinic.add_edge(i, j, 1e18)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Maximizing revenue minus penalties subject to prerequisite implications.
- Independent Set on bipartite graphs (Dual of Minimum Vertex Cover).
- Grid problems where adjacent cells cannot both be chosen.

---

#### 7. Contest WA / TLE / RE Traps

- Direction of prerequisite edge reversed: prerequisite $A \implies B$ must be directed $A \to B$ with $\infty$ capacity.
- Adding negative profits directly into flow graph instead of offsetting by total potential profit.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-19"></a>
### 19. Situational (learn when patterns appear)

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2600
- Prerequisites: MCMF, Successive Shortest Paths

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Situational flow problems involve edge costs alongside capacities (Minimum Cost Maximum Flow), circulation with node demands, and vertex capacities. When $N \le 400$, MCMF with SPFA or Dijkstra potentials computes minimum cost assignments.

---

#### 4. Proof Sketches & Recurrences

Reduced costs using Johnson potentials $\pi(u)$: $w'(u, v) = w(u, v) + \pi(u) - \pi(v) \ge 0$ allows using Dijkstra instead of SPFA for augmenting path search.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// MCMF with SPFA Augmenting Paths
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

struct MCMF {
    struct Edge { int to; ll cap, flow, cost; int rev; };
    int n, s, t;
    vector<vector<Edge>> adj;
    MCMF(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1) {}
    void add_edge(int from, int to, ll cap, ll cost) {
        adj[from].push_back({to, cap, 0, cost, (int)adj[to].size()});
        adj[to].push_back({from, 0, 0, -cost, (int)adj[from].size() - 1});
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- K-disjoint paths with minimum total cost.
- Worker-to-job matching where assignment has a variable matrix cost.
- Graph with upper and lower flow bounds per edge.

---

#### 7. Contest WA / TLE / RE Traps

- Negative cycles in residual graph causing infinite augmentations.
- Backward edge cost must be strictly $-cost$ of forward edge.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---

<a id="topic-20"></a>
### 20. Rarely worth early / Niche

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Push-Relabel, Gomory-Hu Tree, Stoer-Wagner

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

##### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

##### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

##### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

##### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

#### 3. Core Intuition & Problem Framing

Advanced flow constructs such as Gomory-Hu Cut Trees ($N-1$ min-cuts representing all pairs in a tree) and Stoer-Wagner global min-cut appear rarely in standard Div2/Div1 contests. Spend practice time on Dinic and reductions before mastering these niche topics.

---

#### 4. Proof Sketches & Recurrences

Gomory-Hu Tree computes all $\binom{N}{2}$ pairwise minimum cuts using exactly $N-1$ max-flow computations via recursive partitioning.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Reference note: Gomory-Hu tree computes all-pairs min-cut in N-1 max-flow executions.
// Use Dinic subroutines on contracted component sets.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- All-pairs min-cut queries on an undirected network.
- Global minimum cut without specified source and sink in undirected graph.

---

#### 7. Contest WA / TLE / RE Traps

- Applying Gomory-Hu tree on directed graphs (valid only on undirected networks).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---


---
