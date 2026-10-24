# Eulerian Paths / Circuits

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** Hierholzer, degree / in–out degree, adjacency with deletion  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Hierholzer, degree / in–out degree, adjacency with deletion

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

Eulerian circuit traverses every **edge** exactly once and returns; path allows different start/end. Undirected: circuit iff all degrees even (+ connectivity on edges); path iff exactly 0 or 2 odd degrees. Directed: circuit iff in=out for all; path iff one vertex out=in+1 (start), one in=out+1 (end), others equal. Hierholzer: DFS-consume edges, append node on retreat (reverse at end). Modeling: “draw without lifting pen,” DNA assembly, rotate strings / balance parentheses as edges.

*Note: If you need to **count** the number of Eulerian paths/circuits, use the BEST Theorem. → [Go to Section 14c](14-c-algebraic-graph-theory.md)*

---

## 4. Proof Sketches & Recurrences

Hierholzer builds closed tours in residual unused edges and splices them. Complexity \(O(n+m)\) with explicit edge deletion (iterators / stack indices). Connectivity: consider only vertices with nonzero degree.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(n+m)\)
- Per-query / per-operation: \(O(n+m)\)
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace euler {
// Undirected Hierholzer. edges as adj[u] = list of {to, edge_id}
// Each undirected edge once in `used`
vector<int> undirected_trail(int n, int m,
                             vector<vector<pair<int, int>>>& adj,
                             int start = -1) {
    vector<char> used(m, 0);
    vector<int> deg(n, 0);
    for (int u = 0; u < n; ++u) deg[u] = (int)adj[u].size();
    int odd = 0, any = -1;
    for (int u = 0; u < n; ++u) {
        if (deg[u]) any = u;
        if (deg[u] & 1) {
            ++odd;
            start = u;
        }
    }
    if (any == -1) return {}; // no edges
    if (odd != 0 && odd != 2) return {}; // impossible
    if (start < 0) start = any;

    vector<int> st, path;
    st.push_back(start);
    vector<int> it(n, 0);
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)adj[u].size() && used[adj[u][it[u]].second]) ++it[u];
        if (it[u] == (int)adj[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = adj[u][it[u]];
            ++it[u];
            if (used[id]) continue;
            used[id] = 1;
            st.push_back(v);
        }
    }
    if ((int)path.size() != m + 1) return {}; // not connected on edges
    reverse(path.begin(), path.end());
    return path; // vertex sequence
}

// Directed: adj[u] = list of {to, edge_id}; m edges
vector<int> directed_trail(int n, int m,
                           vector<vector<pair<int, int>>>& adj,
                           const vector<int>& indeg,
                           const vector<int>& outdeg) {
    int start = -1, end = -1;
    for (int i = 0; i < n; ++i) {
        if (outdeg[i] == indeg[i] + 1) {
            if (start != -1) return {};
            start = i;
        } else if (indeg[i] == outdeg[i] + 1) {
            if (end != -1) return {};
            end = i;
        } else if (indeg[i] != outdeg[i]) return {};
    }
    if (start == -1) {
        for (int i = 0; i < n; ++i)
            if (outdeg[i]) {
                start = i;
                break;
            }
    }
    if (start == -1) return {};

    vector<char> used(m, 0);
    vector<int> it(n, 0), st, path;
    st.push_back(start);
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)adj[u].size() && used[adj[u][it[u]].second]) ++it[u];
        if (it[u] == (int)adj[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = adj[u][it[u]++];
            if (used[id]) continue;
            used[id] = 1;
            st.push_back(v);
        }
    }
    if ((int)path.size() != m + 1) return {};
    reverse(path.begin(), path.end());
    return path;
}
} // namespace euler
```

---

## 6. Recognition Trigger Signals & Heuristics

- Use each edge exactly once
- Reconstruct a sequence from adjacent pairs (de Bruijn style)
- Directed: “words” as edges between prefix/suffix nodes
- Add minimum edges to make Eulerian

---

## 7. Contest WA / TLE / RE Traps

- Checking vertex connectivity instead of **edge-relevant** connectivity
- Multiedges / self-loops mishandled in `used[]`
- Recursive Hierholzer → stack overflow; use iterative
- Directed: wrong start/end degree pattern
- Returning edge order vs vertex order off-by-one
- Not reversing the postorder path

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

- Chinese Postman (undirected): add min matching on odd vertices + Euler
- Make Eulerian with min added edges
- de Bruijn sequence via Euler in \(k\)-mer graph
- Mixed graphs (harder)

---

## 11. Typical Problem Archetypes

1. Standard application: output Euler circuit/path
2. Slightly disguised: reconstruct permutation from consecutive pairs
3. Difficult: min edges to add to become Eulerian + construct
4. Very difficult / advanced: Chinese Postman / directed CPP

---

## 12. Recognition & Identification Drills

1. Undirected multigraph; print a tour using every edge once.
2. Alphabet digraph of substring transitions; build shortest superstring-like sequence via Euler.
3. Exactly two odd-degree vertices — what tour exists?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: traverse every edge once
- Key invariant: degree / in-out conditions + weak connectivity
- Key formula: Hierholzer consume-edges + reverse path
- Complexity: \(O(n+m)\)
- Template to remember: iterative stack + `used[edge]`

---

---
