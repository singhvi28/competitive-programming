# Heavy-Light Decomposition (STUB)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Tree DFS, Subtree Sizes, Euler Tour, Segment Tree
- Tradeoff: Decomposes any tree into $\mathcal{O}(\log N)$ contiguous array intervals for arbitrary path queries.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

## 3. Core Intuition & Problem Framing

To support arbitrary path queries ($u \leftrightarrow v$) with point or range updates on a tree: Heavy-Light Decomposition classifies each child edge as *heavy* (pointing to the child with the maximum subtree size $sz[v] > sz[u]/2$) or *light*. Because light child subtrees at most halve the tree size ($sz[v] \le sz[u]/2$), any path from root to any leaf encounters at most $\log_2 N$ light edges. Heavy edges form contiguous paths. By assigning DFS entrance times along heavy paths first, every heavy path maps to a contiguous interval on a 1D array. Any path query decomposes into at most $\mathcal{O}(\log N)$ segment tree queries!

---

## 4. Proof Sketches & Recurrences

Let $sz[u]$ be the subtree size of $u$. Since $\sum_{v \in \text{children}(u)} sz[v] = sz[u] - 1$, at most one child can satisfy $sz[v] > (sz[u] - 1)/2$. Light edges strictly halve the component size: traversing a light edge reduces remaining vertices by $\ge 50\%$. Therefore, any root-to-node path crosses at most $\lfloor \log_2 N \rfloor$ light edges and at most $\lfloor \log_2 N \rfloor$ heavy paths. Any tree path $u \leftrightarrow v$ is split at $\text{LCA}(u, v)$ into two root-ward paths, each crossing $\le \log_2 N$ heavy chains. Query complexity is $\mathcal{O}(\log^2 N)$ with a standard Segment Tree.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Heavy-Light Decomposition (HLD) Engine
#include <bits/stdc++.h>
using namespace std;

struct HLD {
    int n, timer = 0;
    vector<vector<int>> adj;
    vector<int> parent, depth, heavy, head, pos, sz;
    HLD(int n_) : n(n_), adj(n_ + 1), parent(n_ + 1), depth(n_ + 1), heavy(n_ + 1, -1), head(n_ + 1), pos(n_ + 1), sz(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void dfs_sz(int u, int p, int d) {
        parent[u] = p; depth[u] = d; sz[u] = 1;
        int max_c = 0;
        for (int v : adj[u]) if (v != p) {
            dfs_sz(v, u, d + 1);
            sz[u] += sz[v];
            if (sz[v] > max_c) { max_c = sz[v]; heavy[u] = v; }
        }
    }
    void dfs_hld(int u, int h) {
        head[u] = h; pos[u] = ++timer;
        if (heavy[u] != -1) dfs_hld(heavy[u], h);
        for (int v : adj[u]) if (v != parent[u] && v != heavy[u]) dfs_hld(v, v);
    }
    void init(int root = 1) { dfs_sz(root, 0, 0); dfs_hld(root, root); }
    // Iterating segments on path u <-> v
    void query_path(int u, int v) {
        for (; head[u] != head[v]; v = parent[head[v]]) {
            if (depth[head[u]] > depth[head[v]]) swap(u, v);
            // Query segment [pos[head[v]], pos[v]] in Segment Tree
        }
        if (depth[u] > depth[v]) swap(u, v);
        // Query segment [pos[u], pos[v]] in Segment Tree (or pos[u]+1 if edge weights)
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Path modification: 'Add $X$ to all nodes/edges on path from $u$ to $v$' and query path sum/max.
- Subtree and path queries combined: subtrees are naturally contiguous intervals $[pos[u], pos[u] + sz[u] - 1]$.
- Dynamic path GCD, path XOR, or path maximum queries with point updates.
- LCA query in $\mathcal{O}(\log N)$ without binary lifting.

---

## 7. Contest WA / TLE / RE Traps

- Edge weight queries: forgotten that edge between $u$ and parent corresponds to $pos[u]$. When querying path $u \leftrightarrow v$, the LCA node must be excluded: $[pos[u] + 1, pos[v]]$.
- Calling `dfs_hld` without visiting `heavy[u]` first; if light children are visited first, heavy path continuity in `pos` is broken.
- Swapping `u` and `v` based on `depth[u]` instead of `depth[head[u]]` during chain jumping.
- Failing to call `init()` before querying.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---
