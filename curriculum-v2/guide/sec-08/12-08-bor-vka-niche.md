# 12. Borůvka Niche

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Niche but decisive in Hard CF/ICPC problems
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Minimum Spanning Tree (MST), Bitwise Trie, Geometric Voronoi, DSU
- Tradeoff: Kruskal/Prim require explicit edges ($\mathcal{O}(E \log E)$ or $\mathcal{O}(V^2)$); Borůvka constructs MST on implicit complete graphs where finding the cheapest outgoing edge takes sublinear time.

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

Borůvka's algorithm operates in phases: in each phase, every connected component simultaneously finds its cheapest outgoing incident edge, and all chosen edges are contracted. Because the number of connected components halves in each phase, there are at most $\lceil \log_2 V \rceil$ phases. In complete graphs where edges are implicit (e.g., $w(u, v) = u \oplus v$ via bitwise XOR, or Manhattan/Euclidean distances in geometry), we cannot sort all $\mathcal{O}(V^2)$ edges. Borůvka allows us to find the cheapest outgoing edge for each component in $\mathcal{O}(V \log(\text{coordinate}))$ using a 0-1 Trie or KD-tree, giving overall $\mathcal{O}(V \log V \log C)$ runtime!

---

## 4. Proof Sketches & Recurrences

Let $C$ be the number of components at phase $t$. Each component identifies an incident edge with minimal weight. Since each component has at least one edge picked, the contracted graph has at most $\lfloor C/2 \rfloor$ components. Thus, $C_{t+1} \le C_t / 2$, terminating in $\le \log_2 V$ rounds. Total time is $\mathcal{O}(\log V \cdot (\text{cost to query all components' cheapest edge}))$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Boruvka Framework for Implicit Graphs (e.g., XOR MST)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DSU {
    vector<int> p;
    int comps;
    DSU(int n) : p(n), comps(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        p[a] = b; comps--; return true;
    }
};

ll boruvka_xor_mst(int n, vector<int>& a) {
    DSU dsu(n);
    ll total_mst_weight = 0;
    while (dsu.comps > 1) {
        // In each phase, find cheapest outgoing edge for each component root
        // best_edge[comp_root] = {min_weight, target_node}
        vector<pair<int, int>> best(n, {INT_MAX, -1});
        // ... (populate best edges via 0-1 Trie search excluding same component) ...
        bool added = false;
        for (int i = 0; i < n; ++i) {
            if (best[i].second != -1 && dsu.unite(i, best[i].second)) {
                total_mst_weight += best[i].first;
                added = true;
            }
        }
        if (!added) break; // Graph disconnected
    }
    return total_mst_weight;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Complete graph where edge weight is defined by bitwise XOR $w(u, v) = a_u \oplus a_v$ for $N \le 2 \times 10^5$.
- Dense geometric graphs where nearest-neighbor queries can be accelerated by Voronoi diagrams or Delaunay triangulation.
- Graph where edges are implicit and finding the minimum weight outgoing edge from a set of nodes takes sub-linear time.
- Contest problem where $E = \Theta(V^2)$ but $N \approx 10^5$.

---

## 7. Contest WA / TLE / RE Traps

- Picking an internal edge: cheapest edge query must ensure the endpoint does NOT belong to the same component (`find(u) != find(v)`).
- Tie-breaking: if two components pick edges of equal weight, ensure unique edge ordering $(w, \min(u, v), \max(u, v))$ to prevent cycles with equal weights.
- Infinite loops if graph is disconnected: ensure the loop terminates when no edges are added in a round.
- Trie deletion/insertion overhead: rebuilding or modifying the Trie dynamically must be done efficiently per round.

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
