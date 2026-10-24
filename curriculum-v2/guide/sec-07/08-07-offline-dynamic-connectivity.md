# Offline dynamic connectivity

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2200–2800 | **Frequency:** Occasional  
> **Prerequisites:** DSU rollback; segment tree over time; offline queries  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: DSU rollback; segment tree over time; offline queries

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

All edge insertions/deletions and connectivity queries are known offline. Each edge exists on a half-open time interval \([L,R)\). Build a **segment tree on time**; store the edge in \(O(\log T)\) nodes covering \([L,R)\). DFS the segment tree: at node, `unite` all stored edges; recurse children; answer queries living at time leaves; `rollback` to snapshot. Never delete online — deletion is “interval ends.”

This solves dynamic connectivity **offline** in \(O((n+m+q)\log n\log T)\) without Link-Cut Trees.

---

## 4. Proof Sketches & Recurrences

Time moments \(0..T-1\) (or \(1..T\)). Segment tree node covering \([tl,tr)\) holds edges fully alive on that segment when added via standard “segment add range update” decomposition.

DFS:
```
void dfs(node):
  snap = dsu.snapshot()
  for e in edges[node]: dsu.unite(e.u, e.v)
  if leaf: answer all queries at this time
  else: dfs(left); dfs(right)
  dsu.rollback(snap)
```

Each edge contributes \(O(\log T)\) unites across the DFS (once per stored node, and each appears on one root-to-leaf path… actually each edge is stored in \(O(\log T)\) nodes, and a root-to-leaf path hits \(O(\log T)\) nodes, but an edge is united when DFS visits a node containing it — each edge is united \(O(\log T)\) times total). Find \(O(\log n)\) ⇒ total \(O(m\log T\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(m\log T)\) edge placements; \(O(n)\) DSU
- Per-query / per-operation: answered at leaf in \(O(\log n)\) find
- Total: \(O((n + m\log T + q)\log n)\) typical
- Memory: \(O(m\log T + q)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace offline_connectivity {
struct DSU {
    vector<int> p, r;
    struct Change { int b, pb, a, ra; bool merged; };
    vector<Change> st;
    DSU(int n) : p(n), r(n, 0) { iota(p.begin(), p.end(), 0); }
    int find(int x) { while (x != p[x]) x = p[x]; return x; }
    int snapshot() const { return (int)st.size(); }
    void unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) { st.push_back({b, b, a, r[a], false}); return; }
        if (r[a] < r[b]) swap(a, b);
        st.push_back({b, p[b], a, r[a], true});
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
    }
    void rollback(int snap) {
        while ((int)st.size() > snap) {
            auto ch = st.back(); st.pop_back();
            if (!ch.merged) continue;
            p[ch.b] = ch.pb;
            r[ch.a] = ch.ra;
        }
    }
    bool same(int a, int b) { return find(a) == find(b); }
};

struct Edge { int u, v; };
struct Query { int u, v, time, idx; };

struct Solver {
    int n, T;
    vector<vector<Edge>> seg; // segtree of edges
    vector<vector<Query>> qat; // queries at leaf time
    vector<int> ans;

    Solver(int n, int T) : n(n), T(T), seg(4 * T), qat(T) {}

    void add_edge(int node, int tl, int tr, int l, int r, Edge e) {
        if (r <= tl || tr <= l) return;
        if (l <= tl && tr <= r) { seg[node].push_back(e); return; }
        int tm = (tl + tr) / 2;
        add_edge(node * 2, tl, tm, l, r, e);
        add_edge(node * 2 + 1, tm, tr, l, r, e);
    }
    void add_edge_interval(int L, int R, Edge e) { // alive on [L,R)
        if (L >= R) return;
        add_edge(1, 0, T, L, R, e);
    }
    void add_query(Query q) { qat[q.time].push_back(q); }

    void dfs(int node, int tl, int tr, DSU& dsu) {
        int snap = dsu.snapshot();
        for (auto e : seg[node]) dsu.unite(e.u, e.v);
        if (tl + 1 == tr) {
            for (auto& q : qat[tl]) ans[q.idx] = dsu.same(q.u, q.v);
        } else {
            int tm = (tl + tr) / 2;
            dfs(node * 2, tl, tm, dsu);
            dfs(node * 2 + 1, tm, tr, dsu);
        }
        dsu.rollback(snap);
    }

    vector<int> solve(int qcnt) {
        ans.assign(qcnt, 0);
        DSU dsu(n);
        if (T > 0) dfs(1, 0, T, dsu);
        return ans;
    }
};

/*
Typical offline compression:
- Map each unique edge (u,v) with u<v to last activation time.
- On ADD: store open time.
- On DEL: close interval [open, now).
- On QUERY: record (u,v,now).
- At end, close still-open edges at T.
*/
} // namespace offline_connectivity
```

### Python 3 Template

```python
# Python 3.11+ — sketch only; too slow for tight limits
# Same DFS-over-time-segtree + DSURollback as C++; omit full code for contest use.
```

---

## 6. Recognition Trigger Signals & Heuristics

- Explicit timeline of add/remove edge + “are u,v connected?”
- Edges given as lifespan intervals
- “Graph evolves; answer after each day” with known future
- Same pattern for offline dynamic bipartiteness / component count / sum queries

---

## 7. Contest WA / TLE / RE Traps

- Half-open interval off-by-one (`[L,R)` vs `[L,R]`)
- Forgetting to close edges still open at the end
- Parallel edges: treat each appearance as distinct lifespan, or multiset of lifetimes
- Answering queries before uniting leaf edges (leaf node must store edges covering that instant)
- Rollback in wrong order / skipping snapshot after unites
- Using path compression DSU
- Time coordinates not compressed → huge empty segtree (compress event times)

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

## 10. Algorithmic Variants & Advanced Extensions

- **Component count / size queries:** maintain `comps` in rollback DSU; answer at leaves
- **Offline bipartiteness:** DSU with parity + rollback
- **Weighted edges / MST dynamic offline:** different (usually LCT or divide-conquer on weight)
- **Online dynamic connectivity:** much harder — skip unless specialty (HDT, LCT)

---

## 11. Typical Problem Archetypes

1. Standard application: add/del/query connectivity offline
2. Slightly disguised: roads under repair on days; queries on other days
3. Difficult: same with component aggregates / bipartite checks
4. Very difficult / advanced: offline fully dynamic MST; multi-dimensional time (rare)

---

## 12. Recognition & Identification Drills

1. Timeline of edge inserts/deletes; after some ops ask if two cities are connected — all ops given upfront.
2. Each edge has birth and death day; \(q\) night queries about connectivity.
3. Same as (1) but also ask whether the graph is bipartite after each query time.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: offline edge lifespan + connectivity queries
- Key invariant: segtree-on-time stores edges; DFS unite/rollback
- Key formula: interval cover \(O(\log T)\) nodes; total \(O(m\log T\log n)\)
- Complexity: \(O((m\log T+q)\log n)\)
- Template to remember: time segtree + `dsu_rollback`

---

---
