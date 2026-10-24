# 8. Johnson’s Algorithm

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2700 | **Frequency:** Rare  
> **Prerequisites:** Bellman–Ford, Dijkstra, potentials  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Bellman–Ford, Dijkstra, potentials

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

All-pairs on sparse graphs with negatives: compute potentials \(h(v)\) via Bellman–Ford from a super-source so reduced costs \(w'(u,v)=w(u,v)+h(u)-h(v)\) are nonnegative; then run Dijkstra from every vertex on \(w'\). True distance: \(d(u,v)=d'(u,v)-h(u)+h(v)\). Beats \(O(n^3)\) FW when \(m\) is sparse and \(n\) is too large for FW but \(n\) Dijkstra runs fit.

---

## 4. Proof Sketches & Recurrences

Feasible potential: \(h(v)\le h(u)+w(u,v)\) ⇒ \(w'\ge 0\). Super-source edges of weight 0 into all nodes; BF gives \(h=\mathrm{dist}\) from super-source. Correctness of reduction is standard for MCMF potentials too.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: BF \(O(nm)\) for potentials
- Per-query / per-operation: after all-pairs matrix, \(O(1)\)
- Total: \(O(nm + n(n+m)\log n)\) with binary heaps
- Memory: \(O(n^2 + m)\) for full matrix`

### C++17 Template

```cpp
namespace johnson {
using ll = long long;
const ll INF = 4e18;

struct Edge { int u, v; ll w; };

// dist[u][v] = shortest; returns false on neg cycle
bool all_pairs(int n, vector<Edge> edges, vector<vector<ll>>& dist) {
    // potentials via super-source n
    vector<Edge> e2 = edges;
    for (int v = 0; v < n; ++v) e2.push_back({n, v, 0});
    vector<ll> h(n + 1, INF);
    h[n] = 0;
    for (int it = 0; it < n; ++it) {
        bool any = false;
        for (auto [u, v, w] : e2) {
            if (h[u] == INF) continue;
            if (h[v] > h[u] + w) {
                h[v] = h[u] + w;
                any = true;
            }
        }
        if (!any) break;
    }
    for (auto [u, v, w] : e2) {
        if (h[u] == INF) continue;
        if (h[v] > h[u] + w) return false;
    }

    vector<vector<pair<int, ll>>> g(n);
    for (auto [u, v, w] : edges) {
        ll nw = w + h[u] - h[v];
        g[u].push_back({v, nw});
    }

    dist.assign(n, vector<ll>(n, INF));
    for (int s = 0; s < n; ++s) {
        vector<ll> d(n, INF);
        priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
        d[s] = 0;
        pq.push({0, s});
        while (!pq.empty()) {
            auto [dd, u] = pq.top();
            pq.pop();
            if (dd != d[u]) continue;
            for (auto [v, w] : g[u]) {
                if (d[v] > dd + w) {
                    d[v] = dd + w;
                    pq.push({d[v], v});
                }
            }
        }
        for (int v = 0; v < n; ++v)
            if (d[v] < INF) dist[s][v] = d[v] - h[s] + h[v];
    }
    return true;
}
} // namespace johnson
```

---

## 6. Recognition Trigger Signals & Heuristics

- Need all-pairs (or many pairs) + negative edges + sparse
- \(n\sim 10^3\), \(m\sim 10^4\) — FW too slow, \(n\) Dijkstras OK after reweight
- Almost never appears as a named requirement; usually FW or \(n\) Dijkstras (nonneg) suffice

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to re-translate distances with \(h\)
- Using Johnson when FW is simpler (\(n\le 400\))
- Neg cycle mishandled in potential phase
- Applying to undirected graphs with neg edges incorrectly (undirected neg edge is already a cycle)

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

- Only need distances from few sources: skip full Johnson; BF per source or one BF if enough
- Same potential idea inside min-cost flow

---

## 11. Typical Problem Archetypes

1. Standard application: all-pairs with negatives, sparse
2. Slightly disguised: reweight so Dijkstra works
3. Difficult: large sparse all-pairs with cycle reporting
4. Very difficult / advanced: shared potentials across multiple queries

---

## 12. Recognition & Identification Drills

1. \(n=2000\), \(m=5000\), negative edges, need all-pairs — FW or Johnson?
2. Why must potentials come from BF (or equiv) before Dijkstra?
3. Undirected graph with a negative edge — what happens?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: sparse all-pairs + negatives; FW too slow
- Key invariant: feasible potentials ⇒ nonnegative reduced costs
- Key formula: \(w'=w+h(u)-h(v)\), \(d=d'-h(u)+h(v)\)
- Complexity: \(O(nm + n(n+m)\log n)\)
- Template to remember: super-source BF → \(n\times\) Dijkstra

---
