# 15. Minimum Spanning Tree Variants

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2200 | **Frequency:** Common  
> **Prerequisites:** DSU (Kruskal), heap / Dijkstra-like Prim  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2200
- Prerequisites: DSU (Kruskal), heap / Dijkstra-like Prim

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

MST minimizes total edge weight connecting all vertices (forest if disconnected: MSF). Cut property: the lightest edge across any cut is safe to include. Cycle property: the heaviest edge on any cycle is not needed. Kruskal sorts edges and adds if endpoints in different components; Prim grows a tree like Dijkstra. Many problems are not “compute MST weight” but use **MST structure** (bottleneck paths, second-best MST, forced edges).

*Note: If you need to **count** the total number of valid Minimum Spanning Trees (or just spanning trees in general), you must use Kirchhoff's Matrix Tree Theorem. → [Go to Section 14b](14-b-matrix-tree-theorem.md)*

---

## 4. Proof Sketches & Recurrences

Kruskal: sort \(O(m\log m)\); DSU \(\approx O(m\alpha(n))\). Prim with binary heap: \(O((n+m)\log n)\) like Dijkstra. Bottleneck: for undirected graphs, path minimizing the maximum edge equals the max edge on the unique path in any MST (when weights distinct; otherwise some MST).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build edges \(O(m)\)
- Per-query / per-operation: Kruskal \(O(m\log m)\); Prim \(O((n+m)\log n)\)
- Total: as above
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace mst {
using ll = long long;

struct DSU {
    vector<int> p, r;
    DSU(int n = 0) { init(n); }
    void init(int n) {
        p.resize(n);
        r.assign(n, 0);
        iota(p.begin(), p.end(), 0);
    }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (r[a] < r[b]) swap(a, b);
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
        return true;
    }
};

struct Edge {
    int u, v;
    ll w;
    bool operator<(const Edge& o) const { return w < o.w; }
};

// returns {total_weight, edges_in_mst}; total = -1 if not connected
pair<ll, vector<Edge>> kruskal(int n, vector<Edge> edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    ll total = 0;
    vector<Edge> used;
    used.reserve(n - 1);
    for (auto e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total += e.w;
            used.push_back(e);
            if ((int)used.size() == n - 1) break;
        }
    }
    if ((int)used.size() != n - 1) return {-1, {}};
    return {total, used};
}

// Prim from src; assumes connected undirected g
pair<ll, vector<Edge>> prim(int n, int src,
                            const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, (ll)4e18);
    vector<int> par(n, -1);
    vector<char> in(n, 0);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    ll total = 0;
    int taken = 0;
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (in[u]) continue;
        in[u] = 1;
        total += d;
        ++taken;
        for (auto [v, w] : g[u]) {
            if (!in[v] && w < dist[v]) {
                dist[v] = w;
                par[v] = u;
                pq.push({w, v});
            }
        }
    }
    if (taken != n) return {-1, {}};
    vector<Edge> used;
    for (int v = 0; v < n; ++v)
        if (par[v] != -1) used.push_back({par[v], v, dist[v]});
    return {total, used};
}
} // namespace mst
```

---

## 6. Recognition Trigger Signals & Heuristics

- Connect all cities with min cable cost
- Minimax path in undirected graph (= max edge on MST path)
- “Remove max edge / add constraints” → MST edges unique or not
- Second best spanning tree; MST with one edge forced/forbidden

---

## 7. Contest WA / TLE / RE Traps

- Assuming connectivity without checking `|MST edges| == n-1`
- Using directed edges in Kruskal incorrectly
- `long long` for sums; overflow on weights
- Second-best MST: forgetting to try replacing non-tree edges correctly
- Distinct vs non-distinct weights for “unique MST”

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

- **Minimum spanning forest**
- **Maximum spanning tree:** negate weights or sort descending
- **Second-best MST:** for each non-tree edge, replace max on tree path
- **Directed MST (Chu–Liu/Edmonds):** rare, harder — niche
- **MST with degree constraints / \(k\) edges:** often binary search + matroid or Prim variants

---

## 11. Typical Problem Archetypes

1. Standard application: MST total weight
2. Slightly disguised: minimax path queries via MST
3. Difficult: second-best MST; count distinct MSTs
4. Very difficult / advanced: xor-MST (Borůvka-like trie); dynamic MST offline

---

## 12. Recognition & Identification Drills

1. Connect \(n\) vertices with given undirected edges, minimize total cost.
2. For each query pair, minimize the maximum edge on any path.
3. Find spanning tree weight if a given edge must be included.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: undirected connectivity with min total / bottleneck
- Key invariant: cut & cycle properties
- Key formula: Kruskal sort + DSU; Prim grow lightest cut edge
- Complexity: \(O(m\log m)\) Kruskal typical
- Template to remember: sort edges + `unite`

---

---
