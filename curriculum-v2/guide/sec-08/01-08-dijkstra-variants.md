# Dijkstra Variants

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2100 (variants to 2500+) | **Frequency:** Very Common  
> **Prerequisites:** Graphs, binary heaps / `priority_queue`, adjacency lists  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2100 (variants to 2500+)
- Prerequisites: Graphs, binary heaps / `priority_queue`, adjacency lists

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

## 3. Core Intuition & Problem Framing

Dijkstra grows a set of vertices whose **final** distance is known, always extending from the unsettled vertex with smallest tentative distance. With nonnegative weights, the first time you pop a node from the min-heap (lazy version: first time you pop with `d == dist[u]`), that distance is optimal—no future path can undercut it without a negative edge. Contest power is not the heap: it is **modeling**—extra state in the node, edge weights as costs of decisions, and “implicit graphs” (grids, digit DP graphs, product graphs).

---

## 4. Proof Sketches & Recurrences

Lazy binary-heap Dijkstra: each edge may push a new pair → \(O(m\log m)\) pushes, \(O((n+m)\log n)\) typical bound. Correctness: induction on pop order; nonnegative edges ⇒ no decrease of a finalized distance. Dial’s algorithm / radix ideas exist for small integer weights but rarely needed vs 0-1 BFS + Dijkstra.

Potential/`h(u)` (Johnson): run Dijkstra on reduced costs \(w'(u,v)=w(u,v)+h(u)-h(v)\ge 0\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(n+m)\)
- Per-query / per-operation: one source \(O((n+m)\log n)\) binary heap
- Total: as above; \(k\) sources without multi-source trick: \(\times k\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace dijkstra {
using ll = long long;
const ll INF = 4e18;

vector<ll> shortest(int n, int src,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue; // lazy deletion
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// Optional: recover parents
vector<ll> shortest_parent(int n, int src,
                           const vector<vector<pair<int, ll>>>& g,
                           vector<int>& par) {
    vector<ll> dist(n, INF);
    par.assign(n, -1);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                par[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
} // namespace dijkstra
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Minimum cost / time / fuel” with nonnegative costs
- Graph is explicit or product of (position × resource)
- Not unweighted (else BFS); not 0/1-only (else 0-1 BFS); not DAG-only (else topo)
- You need single-source or few sources, not dense all-pairs

---

## 7. Contest WA / TLE / RE Traps

- Using Dijkstra with **negative** edges (silent WA)
- Forgetting `if (d != dist[u]) continue` → TLE from stale heap entries
- `int` overflow on `dist[u] + w` — use `long long`, cap INF carefully (`INF + w` must not wrap)
- 1-index vs 0-index; bidirectional edges added once by mistake
- Early exit only valid if you need one target and pop that target with final dist

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

## 10. Algorithmic Variants & Advanced Extensions

- **K shortest / count paths:** extra state or A* carefully; counting: DP on DAG of shortest-path edges
- **Dijkstra on state graph:** node id = `u * (S+1) + s`
- **Dense graphs:** \(O(n^2)\) classic Dijkstra (no heap) when \(m\sim n^2\)
- **Prim = Dijkstra on “dist to tree”** for MST
- **Potentials** for MCMF / Johnson

---

## 11. Typical Problem Archetypes

1. Standard application: single-source distances on weighted undirected/directed graph
2. Slightly disguised: grid with cell costs; compress to graph
3. Difficult: state expansion (fuel, discounts, parity of edges)
4. Very difficult / advanced: optimizing over choices via potentials / nested Dijkstra in flow

---

## 12. Recognition & Identification Drills

1. Cities and flights with nonnegative costs; minimize cost from capital to all cities.
2. You may use one “coupon” that halves one edge; minimize path cost.
3. Graph edges have length; you walk at speed 1 but can teleport with cooldown — minimize time.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: nonnegative weights, single-/few-source
- Key invariant: popped distance is final
- Key formula: `dist[v] = min(dist[v], dist[u] + w(u,v))` with heap order
- Complexity: \(O((n+m)\log n)\)
- Template to remember: lazy PQ + `d != dist[u]` skip

---

---
