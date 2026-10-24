# 7. Multi-Source Shortest Paths

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Common  
> **Prerequisites:** BFS / Dijkstra  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: BFS / Dijkstra

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

Distance to the **nearest** source is ordinary shortest path on a graph with a virtual super-source linked to all sources by weight-0 edges—or equivalently, seed the queue/heap with all sources at distance 0. One search replaces \(k\) searches when you only need `min over sources`.

---

## 4. Proof Sketches & Recurrences

Super-source \(s^\*\) with edges \(s^\*\to s_i\) weight 0 ⇒ distances from \(s^\*\) equal min distance to any \(s_i\). Implementation: initialize `dist[s_i]=0` and push all.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: same as BFS/Dijkstra once
- Total: \(O(n+m)\) or \(O((n+m)\log n)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace multisource {
using ll = long long;
const ll INF = 4e18;

vector<ll> dijkstra(int n, const vector<int>& sources,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    for (int s : sources) {
        if (dist[s] > 0) {
            dist[s] = 0;
            pq.push({0, s});
        }
    }
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

vector<int> bfs(int n, const vector<int>& sources,
                const vector<vector<int>>& g) {
    vector<int> dist(n, -1);
    queue<int> q;
    for (int s : sources) {
        if (dist[s] == -1) {
            dist[s] = 0;
            q.push(s);
        }
    }
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u])
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
    }
    return dist;
}
} // namespace multisource
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Nearest hospital / exit / enemy”
- Fire spread vs you moving (two multi-source BFS)
- Paint components from multiple seeds
- All sources same type; answer is min distance

---

## 7. Contest WA / TLE / RE Traps

- Running \(k\) Dijkstras when one multi-source suffices
- Not handling duplicate sources
- Fire+player: wrong order of comparison (need fire time strictly `<` or `<=` carefully)
- Mixing directed edges incorrectly for “nearest”

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

- Multi-source 0-1 BFS
- Keep `nearest_source[v]` for reconstruction / coloring
- Binary search + multi-source check

---

## 11. Typical Problem Archetypes

1. Standard application: distance to closest special vertex
2. Slightly disguised: infection / fire grids
3. Difficult: two competing multi-source spreads with different speeds
4. Very difficult / advanced: dynamic sources offline with DSU / timeline

---

## 12. Recognition & Identification Drills

1. Multiple exits in a maze; min steps for each cell to an exit.
2. Fires start at several cells simultaneously; can you reach the gate?
3. Each special node paints its Voronoi cell under graph distance.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: min distance to any of a set
- Key invariant: virtual super-source weight 0
- Key formula: seed all sources at 0, one search
- Complexity: one BFS/Dijkstra
- Template to remember: push all sources first

---

---
