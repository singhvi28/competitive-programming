# Borůvka

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** MST cut property, DSU  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: MST cut property, DSU

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

In each phase, every component chooses its minimum-weight outgoing edge; add all such edges (carefully resolving conflicts) and merge. Components at least halve in count ⇒ \(O(\log n)\) phases. Same MST; the parallel “each component picks” view is what makes xor-MST / some algebraic MST variants natural. **Niche** as a default Kruskal replacement on CF.

---

## 4. Proof Sketches & Recurrences

Phase: compute `min_out[component]`; unite along those edges; ignore intra-component. \(O(\log n)\) phases × \(O(m)\) scan ⇒ \(O(m\log n)\) (plus DSU). Correct by cut property each chosen edge is safe (with tie-breaking).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(m)\)
- Per-query / per-operation: one MST \(O(m\log n)\) typical
- Total: \(O(m\log n)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
namespace boruvka {
using ll = long long;

struct DSU {
    vector<int> p, r;
    DSU(int n) : p(n), r(n, 0) { iota(p.begin(), p.end(), 0); }
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

struct Edge { int u, v; ll w; };

// returns MST weight or -1 if disconnected
ll mst(int n, const vector<Edge>& edges) {
    DSU dsu(n);
    ll total = 0;
    int comps = n;
    vector<int> best(n);
    vector<ll> best_w(n);
    while (comps > 1) {
        fill(best.begin(), best.end(), -1);
        fill(best_w.begin(), best_w.end(), (ll)4e18);
        for (int i = 0; i < (int)edges.size(); ++i) {
            int a = dsu.find(edges[i].u), b = dsu.find(edges[i].v);
            if (a == b) continue;
            if (edges[i].w < best_w[a]) {
                best_w[a] = edges[i].w;
                best[a] = i;
            }
            if (edges[i].w < best_w[b]) {
                best_w[b] = edges[i].w;
                best[b] = i;
            }
        }
        bool progressed = false;
        for (int c = 0; c < n; ++c) {
            if (dsu.find(c) != c || best[c] == -1) continue;
            auto e = edges[best[c]];
            if (dsu.unite(e.u, e.v)) {
                total += e.w;
                --comps;
                progressed = true;
            }
        }
        if (!progressed) return -1;
    }
    return total;
}
} // namespace boruvka
```

---

## 6. Recognition Trigger Signals & Heuristics

- Xor-MST / minimum spanning tree with edge weight \(a_u\oplus a_v\)
- Parallel MST / theoretical \(O(m\log n)\) without sorting all edges first
- Problem structure: “best edge out of each component” repeatedly

---

## 7. Contest WA / TLE / RE Traps

- Not skipping when `best[c]==-1` (disconnected)
- Double-adding the same edge when both sides selected it (unite handles; don’t add weight twice)
- Using Borůvka where Kruskal is shorter to code under time pressure
- Tie-breaking inconsistently causing cycles in naive parallel add

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

- **Xor-MST:** Borůvka phases + trie of component values
- Parallel / external-memory MST motivation
- Component-by-component Prim is related

---

## 11. Typical Problem Archetypes

1. Standard application: MST via Borůvka (rare vs Kruskal)
2. Slightly disguised: xor-MST
3. Difficult: Borůvka with dynamic best-edge data structures
4. Very difficult / advanced: theoretical MST algorithms inspired by Borůvka

---

## 12. Recognition & Identification Drills

1. MST where weight of \((i,j)\) is \(a_i\oplus a_j\).
2. Implement MST without sorting all edges globally — which algorithm fits?
3. Why does each phase roughly halve components?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: xor-MST / “min outgoing per component” structure; else Kruskal
- Key invariant: lightest outgoing edges are safe
- Key formula: \(O(\log n)\) phases of component matching
- Complexity: \(O(m\log n)\)
- Template to remember: per-component `best` edge then unite  
- Niche early ROI — don’t prioritize over Kruskal/Prim

---

---
