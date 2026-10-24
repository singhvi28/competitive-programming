# Kruskal Reconstruction vs HLD for Path Max

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in CF Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Kruskal's MST, Disjoint Set Union (DSU), Heavy-Light Decomposition (HLD), Binary Lifting
- Tradeoff: Kruskal Reconstruction Tree (Reachability Tree) reduces path bottleneck queries to a single LCA in $\mathcal{O}(1)$ or $\mathcal{O}(\log N)$ without writing any segment tree or HLD.

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

To find the maximum edge weight on the path between $u$ and $v$ in a graph's MST: standard HLD builds an MST, decomposes tree paths into $\mathcal{O}(\log N)$ segments, and queries a segment tree in $\mathcal{O}(\log^2 N)$ time with 100+ lines of code. Kruskal's Reconstruction Tree (KRT) builds a binary tree with $2N - 1$ nodes: whenever Kruskal joins two components with edge $e = (u, v, w)$, a new node is created with weight $w$, having the roots of $u$ and $v$ as left and right children. The bottleneck maximum weight on the path between $u$ and $v$ is simply the weight of $\text{LCA}(u, v)$ in the KRT!

---

## 4. Proof Sketches & Recurrences

In Kruskal's algorithm, edges are processed in non-decreasing order of weight. Thus, in the KRT, child nodes always have weights less than or equal to their parent nodes: the tree is a min/max heap on node weights. The first time $u$ and $v$ become connected in Kruskal's process is precisely at $\text{LCA}(u, v)$ in the KRT, and the edge weight that connected them is $weight[\text{LCA}(u, v)]$. Any reachability query 'nodes reachable from $u$ using edges $\le W$' maps to the subtree of the highest ancestor of $u$ with weight $\le W$, solvable via binary lifting in $\mathcal{O}(\log N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Kruskal Reconstruction Tree (Reachability Tree)
#include <bits/stdc++.h>
using namespace std;

struct KRT {
    int n, node_cnt;
    vector<int> par, val;
    vector<vector<int>> up, adj;
    int LOG;
    KRT(int n_) : n(n_), node_cnt(n_), par(2 * n_ + 1), val(2 * n_ + 1), LOG(__lg(2 * n_) + 2) {
        iota(par.begin(), par.end(), 0);
        up.assign(LOG, vector<int>(2 * n_ + 1, 0));
        adj.assign(2 * n_ + 1, {});
    }
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
    void build(vector<tuple<int, int, int>>& edges) {
        sort(edges.begin(), edges.end());
        for (auto& [w, u, v] : edges) {
            int ru = find(u), rv = find(v);
            if (ru != rv) {
                int cur = ++node_cnt;
                val[cur] = w;
                par[ru] = par[rv] = par[cur] = cur;
                adj[cur].push_back(ru); adj[cur].push_back(rv);
                up[0][ru] = up[0][rv] = cur;
            }
        }
        for (int k = 1; k < LOG; ++k)
            for (int i = 1; i <= node_cnt; ++i)
                up[k][i] = up[k - 1][up[k - 1][i]];
    }
    int query_max_edge(int u, int v, const vector<int>& depth) {
        if (depth[u] < depth[v]) swap(u, v);
        for (int k = LOG - 1; k >= 0; --k) if (depth[u] - (1 << k) >= depth[v]) u = up[k][u];
        if (u == v) return val[u];
        for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return val[up[0][u]];
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Query asks: 'What is the maximum/minimum capacity edge on the safest path between $u$ and $v$?'
- Query asks: 'How many vertices are reachable from $u$ using only edges with weight $\le W$?'
- Static graph connectivity with threshold queries (KRT turns it into a subtree query on Euler tour).
- Comparing path bottleneck queries on undirected graphs without dynamic edge weight updates.

---

## 7. Contest WA / TLE / RE Traps

- Allocating only $N$ nodes instead of $2N$ nodes for the KRT internal join vertices.
- Forgetting that isolated vertices in a disconnected graph will produce a forest; run DFS/LCA preprocessing for every tree root.
- Using KRT when edge weights are dynamically updated during queries; KRT requires static edge weights (use Link-Cut Trees or HLD if edges update).
- Failing to initialize `par` array up to $2N$ elements.

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
