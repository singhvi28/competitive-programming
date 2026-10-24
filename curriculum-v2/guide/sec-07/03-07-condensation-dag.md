# 3. Condensation DAG

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** SCC labels; DAG algorithms (topo, DP)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: SCC labels; DAG algorithms (topo, DP)

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

After SCC, every interesting **global** reachability question is a question on a DAG of \(k\le n\) supernodes. Multiple edges between the same pair of components collapse to one. Sources/sinks of this DAG control “make strongly connected,” “mandatory visits,” and DP entry points.

Classic theorem: for a digraph with \(k\) SCCs forming a condensation with \(a\) sources (in-degree 0) and \(b\) sinks (out-degree 0), if \(k=1\) answer 0; else minimum edges to make strongly connected is \(\max(a,b)\) (assuming the underlying undirected condensation is weakly connected — usually assumed or handled).

---

## 4. Proof Sketches & Recurrences

Map each vertex \(v\) to \(c=\mathrm{id}[v]\). For every edge \(u\to v\) with \(\mathrm{id}[u]\neq\mathrm{id}[v]\), add condensation edge \(c_u\to c_v\). Deduplicate with `set` or sort+unique.

Weak connectivity of the **underlying** undirected condensation matters for the \(\max(a,b)\) formula; if the original digraph is not weakly connected, answer is often “impossible” for strong connectivity with arbitrary added edges still inside the vertex set (added edges can connect components — usually you may add any directed edge; then connect weak components carefully: formula generalizes by considering each weak piece).

Topo order of condensation = order of Tarjan component ids often already reverse-topo if Tarjan assigns in pop order — **do not rely on that**; run explicit topo/Kahn or DFS finish on the DAG.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m\log m)\) with sort-unique per list, or \(O(n+m)\) expected with hash sets
- Per-query / per-operation: topo \(O(k+e)\), \(k=\#SCC\)
- Total: dominated by SCC + build
- Memory: \(O(k+e)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace condensation {
// ids[v] in [0..comp), from Kosaraju/Tarjan
struct Dag {
    int comp;
    vector<vector<int>> g;   // unique edges
    vector<int> indeg, outdeg;
};

Dag build(int n, int comp, const vector<int>& ids, const vector<vector<int>>& g) {
    vector<vector<int>> raw(comp);
    vector<int> indeg(comp, 0), outdeg(comp, 0);
    for (int v = 0; v < n; ++v) {
        for (int to : g[v]) {
            int a = ids[v], b = ids[to];
            if (a != b) raw[a].push_back(b);
        }
    }
    vector<vector<int>> dag(comp);
    for (int i = 0; i < comp; ++i) {
        auto& e = raw[i];
        sort(e.begin(), e.end());
        e.erase(unique(e.begin(), e.end()), e.end());
        for (int b : e) {
            dag[i].push_back(b);
            ++outdeg[i];
            ++indeg[b];
        }
    }
    return {comp, dag, indeg, outdeg};
}

// Minimum edges to make strongly connected (weakly connected digraph).
// Returns -1 if not weakly connected (optional check omitted: assume yes).
int min_edges_to_strong(const Dag& d) {
    if (d.comp == 1) return 0;
    int sources = 0, sinks = 0;
    for (int i = 0; i < d.comp; ++i) {
        if (d.indeg[i] == 0) ++sources;
        if (d.outdeg[i] == 0) ++sinks;
    }
    return max(sources, sinks);
}

vector<int> topo(const Dag& d) {
    queue<int> q;
    vector<int> deg = d.indeg, order;
    for (int i = 0; i < d.comp; ++i) if (deg[i] == 0) q.push(i);
    while (!q.empty()) {
        int v = q.front(); q.pop();
        order.push_back(v);
        for (int to : d.g[v]) if (--deg[to] == 0) q.push(to);
    }
    return order; // size==comp if DAG (always)
}
} // namespace condensation
```

### Python 3 Template

```python
# Python 3.11+ — fine; graph sizes same as SCC
from collections import deque

def build_condensation(n: int, comp: int, ids: list[int], g: list[list[int]]):
    raw = [[] for _ in range(comp)]
    for v in range(n):
        for to in g[v]:
            a, b = ids[v], ids[to]
            if a != b:
                raw[a].append(b)
    dag = [[] for _ in range(comp)]
    indeg = [0] * comp
    outdeg = [0] * comp
    for a in range(comp):
        e = sorted(set(raw[a]))
        dag[a] = e
        outdeg[a] = len(e)
        for b in e:
            indeg[b] += 1
    return dag, indeg, outdeg


def min_edges_to_strong(comp: int, indeg: list[int], outdeg: list[int]) -> int:
    if comp == 1:
        return 0
    sources = sum(1 for i in range(comp) if indeg[i] == 0)
    sinks = sum(1 for i in range(comp) if outdeg[i] == 0)
    return max(sources, sinks)


def topo(dag: list[list[int]], indeg: list[int]) -> list[int]:
    deg = indeg[:]
    q = deque(i for i, d in enumerate(deg) if d == 0)
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for to in dag[v]:
            deg[to] -= 1
            if deg[to] == 0:
                q.append(to)
    return order
```

---

## 6. Recognition Trigger Signals & Heuristics

- Just computed SCCs and now need reachability / DP / counting paths between components
- “Add minimum edges to become strongly connected”
- Values on nodes; take max/sum along any path in the cyclic digraph → DP on condensation
- Unique sink / chain condensation ⇒ greedy forced order

---

## 7. Contest WA / TLE / RE Traps

- Keeping intra-component edges in the DAG (breaks acyclicity / DP)
- Forgetting to unique multi-edges → wrong degrees for \(\max(a,b)\)
- Applying \(\max(a,b)\) when `comp==1` (should be 0) or when graph not weakly connected
- Using vertex weights twice when aggregating component weight (sum once per component)
- Assuming Tarjan ids are topo order without verifying

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

- **Weighted condensation:** `w[c] = f(nodes in c)` then DAG DP
- **Reachability matrix on DAG:** bitsets on topo order \(O(k^2/64)\)
- **Minimum path cover style** on transitively reduced DAGs — different problem family
- **Condensation of undirected bridge-blocks:** tree, not DAG — see bridges variants

---

## 11. Typical Problem Archetypes

1. Standard application: build DAG; count sources/sinks
2. Slightly disguised: max sum of node values on a path in a digraph with cycles
3. Difficult: min edges to strong; or assign each SCC a value under topo constraints
4. Very difficult / advanced: optimize over subsets of components with reachability bitsets; game on condensation

---

## 12. Recognition & Identification Drills

1. After SCC, compute how many components have indegree 0 and outdegree 0.
2. Node scores; walk any directed path; maximize total score (each node at most once — cycles force component collapse).
3. Add the fewest one-way flights so from every airport you can reach every other.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: immediately after SCC for global structure
- Key invariant: condensation is a DAG
- Key formula: min edges to strong \(=\max(\#\mathrm{sources},\#\mathrm{sinks})\) if \(k>1\) (weakly connected)
- Complexity: \(O(n+m)\) plus DAG algos
- Template to remember: map edges by `ids`, unique, indeg/outdeg

---

---
