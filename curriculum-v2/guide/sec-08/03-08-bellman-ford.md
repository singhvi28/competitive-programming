# 3. Bellman–Ford

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Occasional  
> **Prerequisites:** Edge list, relaxation, negative weights  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Edge list, relaxation, negative weights

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

Relax **all** edges up to \(n-1\) times; if a shortest path is simple, it has \(\le n-1\) edges, so \(n-1\) rounds suffice. A successful relaxation on round \(n\) means a negative cycle is reachable from the source (or from the virtual super-source if you initialize all `dist=0` for “any cycle”). This is the trustworthy negative-weight algorithm when you do not need Dijkstra’s assumptions.

---

## 4. Proof Sketches & Recurrences

After \(k\) rounds, `dist[v]` equals shortest path using \(\le k\) edges (if no neg cycle). Neg cycle ⇒ unbounded decrease along a walk. Difference constraints satisfiable iff no negative cycle in the constraint graph.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: edge list \(O(m)\)
- Per-query / per-operation: \(O(nm)\)
- Total: \(O(nm)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace bellman_ford {
using ll = long long;
const ll INF = 4e18;

struct Edge { int u, v; ll w; };

// returns false if negative cycle reachable from src
bool shortest(int n, int src, const vector<Edge>& edges,
              vector<ll>& dist) {
    dist.assign(n, INF);
    dist[src] = 0;
    for (int it = 0; it < n - 1; ++it) {
        bool any = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] == INF) continue;
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                any = true;
            }
        }
        if (!any) break;
    }
    for (auto [u, v, w] : edges) {
        if (dist[u] == INF) continue;
        if (dist[v] > dist[u] + w) return false; // neg cycle reachable
    }
    return true;
}

// Mark nodes that can be improved via neg cycle (optional)
void mark_neg_reachable(int n, const vector<Edge>& edges,
                        vector<ll>& dist, vector<char>& bad) {
    bad.assign(n, 0);
    for (int it = 0; it < n; ++it) {
        for (auto [u, v, w] : edges) {
            if (dist[u] == INF) continue;
            if (dist[v] > dist[u] + w) {
                dist[v] = max(-INF / 4, dist[u] + w); // avoid wild overflow
                bad[v] = 1;
            }
            if (bad[u]) bad[v] = 1;
        }
    }
}
} // namespace bellman_ford
```

---

## 6. Recognition Trigger Signals & Heuristics

- Explicit negative edges or “gain” that decreases cost
- Detect arbitrage / negative cycle
- Difference constraints: \(x_v - x_u \le w\) → edge \(u\to v\) weight \(w\)
- \(n,m\) small enough for \(O(nm)\) (\(nm \lesssim 10^7\)–\(10^8\))

---

## 7. Contest WA / TLE / RE Traps

- Relaxing when `dist[u]==INF` (creating fake paths)
- Overflow: `INF + w` — skip or use saturated arithmetic
- Detecting a neg cycle that is **not** reachable from `src` (still “exists” if you init all zeros)
- Off-by-one: only \(n-2\) rounds
- Printing cycle without parent pointers / DFS on improving edges

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

- **Shortest path with ≤K edges:** exactly \(K\) rounds (or DP `dist[k][v]`)
- **Difference constraints system**
- **SPFA:** queue variant — see next (avoid)
- Initialize all `dist=0` to find any neg cycle in the graph

---

## 11. Typical Problem Archetypes

1. Standard application: shortest paths with negatives
2. Slightly disguised: currency exchange / arbitrage
3. Difficult: recover a negative cycle vertices
4. Very difficult / advanced: difference constraints + binary search on answer

---

## 12. Recognition & Identification Drills

1. Directed graph with negative weights; detect if a neg cycle can reach node \(t\).
2. Variables with inequalities \(x_i - x_j \le c\); check feasibility.
3. Max score with possible loops that increase score forever.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: negatives or neg-cycle / difference constraints
- Key invariant: \(n-1\) relaxations finalize simple shortest paths
- Key formula: relax all edges; \(n\)th improve ⇒ neg cycle
- Complexity: \(O(nm)\)
- Template to remember: edge-list relax loop

---

---
