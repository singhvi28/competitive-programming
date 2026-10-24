# Bridges and articulation points

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Undirected graphs, DFS tree, discovery times; distinguish tree vs back edges  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Undirected graphs, DFS tree, discovery times; distinguish tree vs back edges

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

Run DFS on an **undirected** graph. Tree edges build a spanning forest; back edges go to ancestors.

- **Bridge:** tree edge \(v\to u\) (child) with `low[u] > disc[v]` — no back edge from \(u\)’s subtree escapes to \(v\) or above → removing it disconnects.
- **Articulation point:** non-root \(v\) if some child has `low[child] >= disc[v]`; root if it has ≥2 DFS children. Removing \(v\) disconnects the graph.

`low[x]` = earliest discovery time reachable from \(x\)’s subtree using tree edges and **at most one back edge**.

---

## 4. Proof Sketches & Recurrences

For undirected DFS:
\[
\mathrm{low}[v]=\min\Big(\mathrm{disc}[v],\ \min_{\text{back }v\to u}\mathrm{disc}[u],\ \min_{\text{child }c}\mathrm{low}[c]\Big)
\]
Ignore parent edge when scanning neighbors (or handle multi-edges carefully: if parallel edges exist, parent edge is not a bridge).

**Bridge:** tree edge \((v,c)\) is a bridge \(\iff \mathrm{low}[c]>\mathrm{disc}[v]\).

**Articulation:**  
- Root: \(\#\) of children in DFS tree \(\ge 2\).  
- Non-root: \(\exists\) child \(c\) with \(\mathrm{low}[c]\ge\mathrm{disc}[v]\).

Complexity \(O(n+m)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: \(O(1)\) after flags computed
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace bridges_arts {
struct Edge { int to, id; };

vector<int> disc, low;
vector<char> is_art, is_bridge; // is_bridge[edge_id]
vector<int> tin_parent_edge;
int timer;

void dfs(int v, int pe, const vector<vector<Edge>>& g) {
    disc[v] = low[v] = timer++;
    int children = 0;
    for (auto [to, id] : g[v]) {
        if (id == pe) continue;
        if (disc[to] != -1) {
            low[v] = min(low[v], disc[to]); // back edge
        } else {
            dfs(to, id, g);
            low[v] = min(low[v], low[to]);
            if (low[to] > disc[v]) is_bridge[id] = 1;
            if (pe != -1 && low[to] >= disc[v]) is_art[v] = 1;
            ++children;
        }
    }
    if (pe == -1 && children >= 2) is_art[v] = 1;
}

// n vertices, m edges as pairs (u,v); undirected
void run(int n, const vector<pair<int,int>>& edges) {
    int m = (int)edges.size();
    vector<vector<Edge>> g(n);
    for (int i = 0; i < m; ++i) {
        auto [u, v] = edges[i];
        g[u].push_back({v, i});
        g[v].push_back({u, i});
    }
    disc.assign(n, -1);
    low.assign(n, 0);
    is_art.assign(n, 0);
    is_bridge.assign(m, 0);
    timer = 0;
    for (int i = 0; i < n; ++i) if (disc[i] == -1) dfs(i, -1, g);
}
} // namespace bridges_arts
```

### Python 3 Template

```python
# Python 3.11+ — OK for typical CF limits with raised recursion; prefer iterative for n~1e6
import sys
sys.setrecursionlimit(1_000_000)

def bridges_and_arts(n: int, edges: list[tuple[int, int]]):
    m = len(edges)
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        g[v].append((u, i))
    disc = [-1] * n
    low = [0] * n
    is_art = [False] * n
    is_bridge = [False] * m
    timer = 0

    def dfs(v: int, pe: int) -> None:
        nonlocal timer
        disc[v] = low[v] = timer
        timer += 1
        children = 0
        for to, eid in g[v]:
            if eid == pe:
                continue
            if disc[to] != -1:
                low[v] = min(low[v], disc[to])
            else:
                dfs(to, eid)
                low[v] = min(low[v], low[to])
                if low[to] > disc[v]:
                    is_bridge[eid] = True
                if pe != -1 and low[to] >= disc[v]:
                    is_art[v] = True
                children += 1
        if pe == -1 and children >= 2:
            is_art[v] = True

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return is_bridge, is_art
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Critical road / cable / friendship whose removal disconnects”
- “Edges that lie on all paths between …” (bridges are exactly edges not on any cycle)
- Build **bridge-block tree** (components after deleting bridges form a tree)
- “How many edges must stay / are non-bridges”
- Vertex connectivity-1 cuts (articulation)

---

## 7. Contest WA / TLE / RE Traps

- Treating the graph as directed; bridges are an **undirected** notion
- Not skipping parent edge → every tree edge looks like a back edge mess
- **Multi-edges:** parent check by edge id, not by vertex; parallel edges ⇒ not a bridge
- Using `low[to] >= disc[v]` for bridges (should be **strict** `>` for bridges)
- Root articulation: counting neighbors instead of DFS-tree children
- Articulation can be true for multiple reasons — use a `bool` flag, don’t early-return wrongly
- Disconnected graphs: loop over all starts

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

- **Bridge-block tree:** shrink each 2-edge-connected component to a node; bridges become tree edges — then path queries / “must cross bridge”
- **Biconnected components (vertex):** stack of edges during DFS; pop when articulation condition triggers
- **Online bridges:** harder; usually rebuild or special structures
- **Directed “bridges”:** bridge-like notions differ (strong bridges) — rare; not this template

---

## 11. Typical Problem Archetypes

1. Standard application: list all bridges / articulation points
2. Slightly disguised: count pairs of vertices whose unique path uses a given edge
3. Difficult: maximize components after removing one edge; or build bridge tree + binary lifting
4. Very difficult / advanced: 2-edge-connected orientation; cactus graphs; DP on bridge-block tree

---

## 12. Recognition & Identification Drills

1. Undirected roads; find all roads whose destruction splits the country into more pieces.
2. Network nodes; find vertices whose failure disconnects communication.
3. After compressing bridge-blocks, answer whether two cities stay connected if any single non-bridge road fails (always yes inside a block).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: critical edges/vertices in undirected graphs
- Key invariant: `low` via DFS tree + back edges
- Key formula: bridge iff `low[child] > disc[v]`; art iff root≥2 children or `low[child] >= disc[v]`
- Complexity: \(O(n+m)\)
- Template to remember: edge-id parent skip + `disc`/`low`

---

---
