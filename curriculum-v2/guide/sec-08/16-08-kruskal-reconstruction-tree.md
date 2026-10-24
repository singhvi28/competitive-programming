# 16. Kruskal Reconstruction Tree

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Kruskal, LCA / binary lifting, tree queries  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Kruskal, LCA / binary lifting, tree queries

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

Run Kruskal; each time two components merge via edge weight \(w\), create a **new parent node** with value \(w\) whose children are the two component roots. Leaves are original vertices. The path-max edge between \(a\) and \(b\) in the MST equals the **LCA’s weight** in this binary-ish tree (often \(2n-1\) nodes). Transforms bottleneck queries into LCA. Prefer this over HLD on the MST when you only need path max/min of *merge weights*.

---

## 4. Proof Sketches & Recurrences

Edges added in increasing weight. LCA of leaves \(a,b\) is the first merge that connected them ⇒ that merge weight is the minimax path cost. Build LCA (binary lifting) on the reconstruction tree (rooted at final merges; forest if disconnected).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: Kruskal \(O(m\log m)\) + LCA build \(O(n\log n)\)
- Per-query / per-operation: \(O(\log n)\) LCA
- Total: preprocess + \(q\log n\)
- Memory: \(O(n\log n)\)`

### C++17 Template

```cpp
namespace kruskal_rebuild {
using ll = long long;

struct DSU {
    vector<int> p;
    DSU(int n) : p(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
};

struct Edge {
    int u, v;
    ll w;
    bool operator<(const Edge& o) const { return w < o.w; }
};

struct Tree {
    int n_leaves = 0, N = 0, LOG = 0;
    vector<vector<int>> g;
    vector<ll> val; // internals: merge weight; leaves typically 0
    vector<int> root;
    vector<int> dep;
    vector<vector<int>> up;

    int lca(int a, int b) const {
        if (dep[a] < dep[b]) swap(a, b);
        int d = dep[a] - dep[b];
        for (int j = 0; j < LOG; ++j)
            if (d & (1 << j)) a = up[j][a];
        if (a == b) return a;
        for (int j = LOG - 1; j >= 0; --j)
            if (up[j][a] != up[j][b]) {
                a = up[j][a];
                b = up[j][b];
            }
        return up[0][a];
    }

    int component_root(int x) const {
        while (up[0][x] != x) x = up[0][x];
        return x;
    }

    // minimax edge on path between leaves a,b; -1 if disconnected
    ll path_max(int a, int b) const {
        if (component_root(a) != component_root(b)) return -1;
        int p = lca(a, b);
        return (p < n_leaves) ? 0 : val[p]; // same leaf / degenerate
    }
};

// Leaves 0..n-1; each Kruskal merge creates a new parent with val = edge weight.
Tree build(int n, vector<Edge> edges) {
    sort(edges.begin(), edges.end());
    Tree t;
    t.n_leaves = n;
    int Nmax = 2 * n;
    t.g.assign(Nmax, {});
    t.val.assign(Nmax, 0);
    DSU dsu(n);
    vector<int> root_of(n);
    iota(root_of.begin(), root_of.end(), 0);
    t.N = n;
    for (auto e : edges) {
        int a = dsu.find(e.u), b = dsu.find(e.v);
        if (a == b) continue;
        int p = t.N++;
        t.val[p] = e.w;
        t.g[p] = {root_of[a], root_of[b]}; // rooted: children only
        dsu.p[b] = a;
        root_of[a] = p;
    }
    vector<char> has_parent(t.N, 0);
    for (int u = n; u < t.N; ++u)
        for (int v : t.g[u]) has_parent[v] = 1;
    t.root.clear();
    for (int i = 0; i < t.N; ++i)
        if (!has_parent[i]) t.root.push_back(i);

    t.LOG = 1;
    while ((1 << t.LOG) <= t.N) ++t.LOG;
    t.dep.assign(t.N, 0);
    t.up.assign(t.LOG, vector<int>(t.N));
    for (int r : t.root) {
        t.up[0][r] = r;
        vector<int> st = {r};
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (int v : t.g[u]) {
                t.up[0][v] = u;
                t.dep[v] = t.dep[u] + 1;
                st.push_back(v);
            }
        }
    }
    for (int j = 1; j < t.LOG; ++j)
        for (int i = 0; i < t.N; ++i)
            t.up[j][i] = t.up[j - 1][t.up[j - 1][i]];
    return t;
}
} // namespace kruskal_rebuild
```

---

## 6. Recognition Trigger Signals & Heuristics

- Many queries: min possible maximum edge on a path (undirected)
- “When do \(a\) and \(b\) become connected if edges added by weight?” → LCA depth/time
- Offline queries sorted by limit \(x\): equivalent to connectivity in Kruskal reconstr.
- Editorial mentions “Kruskal reconstruction tree” / “line tree” / “BCT-like merge tree”

---

## 7. Contest WA / TLE / RE Traps

- Not handling disconnected graphs (forest of reconstruction trees)
- Using edge weight on MST path via HLD incorrectly when reconstr. LCA is simpler
- Off-by-one node indexing (leaves \(0..n-1\), internals \(\ge n\))
- Sorting ascending vs descending for maximin vs minimax
- Building undirected cycles in the merge tree (keep rooted children lists)

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

- Max spanning reconstruction for maximin paths
- Persistent DSU / time = weight for “connected under limit \(x\)”
- Combine with virtual trees on reconstruction tree

---

## 11. Typical Problem Archetypes

1. Standard application: query minimax path between pairs
2. Slightly disguised: earliest time two nodes connect as edges appear by weight
3. Difficult: queries on subtree of reconstruction tree (component at a threshold)
4. Very difficult / advanced: path problems with layered constraints on merge weights

---

## 12. Recognition & Identification Drills

1. \(q\) queries: minimum possible maximum edge among all paths \(u\)–\(v\).
2. Edges appear in order of increasing length; for each query, when do \(u,v\) connect?
3. Same as (1) but you already know HLD — which structure is lighter?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: bottleneck path queries / connectivity-by-weight
- Key invariant: LCA merge weight = minimax edge
- Key formula: Kruskal merges → new parent nodes; query LCA
- Complexity: \(O(m\log m + (n+q)\log n)\)
- Template to remember: merge tree + binary lifting LCA  
- vs HLD: reconstr. for path max; HLD if arbitrary path aggregates/updates

---

---
