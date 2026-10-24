# Centroid decomposition (STUB)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 2100–2600
- Prerequisites: Tree DFS, Centroid of Tree, Divide and Conquer
- Tradeoff: Solves path counting/optimization problems on unrooted trees in $\mathcal{O}(N \log N)$ or $\mathcal{O}(N \log^2 N)$.

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

A centroid of a tree of $N$ nodes is a vertex whose removal partitions the tree into connected components, each having size at most $\lfloor N/2 \rfloor$. Every tree has at least one and at most two centroids. Centroid Decomposition recursively finds the centroid $C$ of the tree, solves all path queries passing through $C$, removes $C$, and recurses on the remaining subtrees. Because the tree size halves at each step, the recursion depth is bounded by $\lceil \log_2 N \rceil$. The resulting 'Centroid Tree' has height $\le \log_2 N$, enabling dynamic distance updates and queries across the entire tree.

---

## 4. Proof Sketches & Recurrences

At depth $k$ of the decomposition, the tree is partitioned into at most $2^k$ components, each of size $\le N / 2^k$. In each component, finding the centroid and aggregating path statistics takes time proportional to the component size. Summing across all components at depth $k$ gives $\mathcal{O}(N)$ work. Since maximum recursion depth is $\log_2 N$, total time for static path counting is $\mathcal{O}(N \log N)$. For dynamic queries, a node has at most $\log_2 N$ centroid ancestors; updating distance to all centroid ancestors takes $\mathcal{O}(\log^2 N)$ or $\mathcal{O}(\log N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Centroid Decomposition Framework
#include <bits/stdc++.h>
using namespace std;

struct CentroidDecomp {
    int n;
    vector<vector<int>> adj;
    vector<int> sz, removed, c_parent;
    CentroidDecomp(int n_) : n(n_), adj(n_ + 1), sz(n_ + 1), removed(n_ + 1, 0), c_parent(n_ + 1, 0) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void get_sz(int u, int p) {
        sz[u] = 1;
        for (int v : adj[u]) if (v != p && !removed[v]) {
            get_sz(v, u); sz[u] += sz[v];
        }
    }
    int get_centroid(int u, int p, int total) {
        for (int v : adj[u]) if (v != p && !removed[v]) {
            if (sz[v] > total / 2) return get_centroid(v, u, total);
        }
        return u;
    }
    int decompose(int u, int p = 0) {
        get_sz(u, 0);
        int c = get_centroid(u, 0, sz[u]);
        removed[c] = 1; c_parent[c] = p;
        // ... (Solve paths passing through centroid c) ...
        for (int v : adj[c]) if (!removed[v]) decompose(v, c);
        return c;
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count pairs of vertices $(u, v)$ such that $\text{dist}(u, v) = K$ or $\text{dist}(u, v) \le K$ in a tree of $N \le 2 \times 10^5$.
- Dynamic queries: 'Turn node $u$ red' and 'Find distance from query node $v$ to the closest red node' (Centroid Tree with $\log N$ ancestor updates).
- Tree path problems where path property is non-invertible (e.g. median, bitwise conditions).
- Tree paths of length at most $K$ with maximum profit.

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to mark `removed[c] = 1`: without marking removed centroids, DFS will traverse already processed components, causing $\mathcal{O}(N^2)$ worst-case TLE.
- Recalculating subtree sizes: must call `get_sz(u, 0)` on the current component before running `get_centroid` so `sz` values reflect the current component size, not the global tree size.
- Overcounting paths that lie within the same child subtree: must subtract contributions from individual subtrees of $c$.
- Stack overflow in deep trees if `sz` is computed incorrectly.

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
