# Section §07: Graph Algorithms (SCC, Topo-DP, 2-SAT)

> **Module ID:** `sec-07`  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Topic Count:** 10  

**Module Summary:** Kosaraju and Tarjan SCC algorithms, Condensation DAG, Topological DP, 2-SAT variable implication graphs, and offline dynamic connectivity.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [SCC: Kosaraju + Tarjan](#topic-1) | `S-tier (Kosaraju) / A-tier (Tarjan)` | 1600–2200 | Common | [01-07-scc-kosaraju-tarjan.md](./01-07-scc-kosaraju-tarjan.md) |
| 2 | [Bridges and articulation points](#topic-2) | `A-tier` | 1600–2300 | Common | [02-07-bridges-and-articulation-points.md](./02-07-bridges-and-articulation-points.md) |
| 3 | [Condensation DAG](#topic-3) | `S-tier` | 1700–2300 | Common | [03-07-condensation-dag.md](./03-07-condensation-dag.md) |
| 4 | [2-SAT](#topic-4) | `A-tier` | 1800–2400 | Occasional | [04-07-2-sat.md](./04-07-2-sat.md) |
| 5 | [Topological-DP patterns](#topic-5) | `S-tier` | 1600–2200 | Common | [05-07-topological-dp-patterns.md](./05-07-topological-dp-patterns.md) |
| 6 | [Block-Cut Tree (BCT)](#topic-6) | `A-tier` | 1900–2500 | Occasional | [06-07-block-cut-tree-bct.md](./06-07-block-cut-tree-bct.md) |
| 7 | [DSU rollback](#topic-7) | `B-tier` | 2000–2600 | Occasional | [07-07-dsu-rollback.md](./07-07-dsu-rollback.md) |
| 8 | [Offline dynamic connectivity](#topic-8) | `B-tier` | 2200–2800 | Occasional | [08-07-offline-dynamic-connectivity.md](./08-07-offline-dynamic-connectivity.md) |
| 9 | [Heavy-Light Decomposition (STUB)](#topic-9) | `B-tier` | 1600–2200 | Common | [09-07-heavy-light-decomposition-stub.md](./09-07-heavy-light-decomposition-stub.md) |
| 10 | [Centroid decomposition (STUB)](#topic-10) | `B-tier` | 1600–2200 | Common | [10-07-centroid-decomposition-stub.md](./10-07-centroid-decomposition-stub.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. SCC: Kosaraju + Tarjan

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier (Kosaraju) / A-tier (Tarjan) | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Directed graphs, DFS, finish times / discovery times; adjacency lists  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (Kosaraju) / A-tier (Tarjan)
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Directed graphs, DFS, finish times / discovery times; adjacency lists

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

An SCC is a maximal set where every pair is mutually reachable. Collapsing each SCC to a supernode yields a **DAG** — cycles are “noise” inside components; the interesting global structure is the condensation.

**Kosaraju:** DFS finish order on \(G\) is a linear extension related to the reverse of the condensation topo order. The **transpose** \(G^T\) has the same SCCs. Processing nodes in decreasing finish time and DFS on \(G^T\) peels off one SCC at a time (sources in the reverse condensation become sinks in \(G^T\)).

**Tarjan:** One DFS maintains discovery time `disc`, low-link `low` (earliest discovered vertex reachable via tree edges + one back/cross edge into the stack), and an explicit stack of the current path’s “active” vertices. When `low[v] == disc[v]`, `v` is the root of an SCC — pop until `v`.

---

#### 4. Proof Sketches & Recurrences

Let \(C_1,\ldots,C_k\) be SCCs. Condensation edges \(C_i \to C_j\) (\(i\neq j\)) form a DAG (a cycle would merge components).

**Kosaraju correctness sketch:** The first node popped in decreasing finish order belongs to a source SCC of the condensation of \(G^T\) (equivalently a sink of \(G\)’s condensation). DFS on \(G^T\) from that node reaches exactly its SCC. Remove and repeat.

**Tarjan:** `low[v] = min(disc[v], disc[u]` for back-edges to stack vertices, `low[u]` for tree children). If a child has `low[child] >= disc[v]` that does **not** mean articulation here — for SCC, the pop condition is solely `low[v]==disc[v]`. Cross-edges to already-assigned nodes are ignored.

**Complexity:** Both \(O(n+m)\). Kosaraju: two DFS + transpose build. Tarjan: one DFS.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\) build / transpose
- Per-query / per-operation: \(O(1)\) component id after run
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace scc_kosaraju {
vector<int> ids; // 0..comp-1
int comp;

void dfs1(int v, const vector<vector<int>>& g, vector<char>& used, vector<int>& order) {
    used[v] = 1;
    for (int to : g[v]) if (!used[to]) dfs1(to, g, used, order);
    order.push_back(v);
}

void dfs2(int v, const vector<vector<int>>& gr, vector<char>& used, vector<int>& component) {
    used[v] = 1;
    component.push_back(v);
    for (int to : gr[v]) if (!used[to]) dfs2(to, gr, used, component);
}

// returns number of components; fills ids[v]
int run(int n, const vector<vector<int>>& g) {
    vector<vector<int>> gr(n);
    for (int v = 0; v < n; ++v)
        for (int to : g[v]) gr[to].push_back(v);

    vector<char> used(n, 0);
    vector<int> order;
    order.reserve(n);
    for (int i = 0; i < n; ++i) if (!used[i]) dfs1(i, g, used, order);

    fill(used.begin(), used.end(), 0);
    ids.assign(n, -1);
    comp = 0;
    reverse(order.begin(), order.end());
    for (int v : order) if (!used[v]) {
        vector<int> component;
        dfs2(v, gr, used, component);
        for (int x : component) ids[x] = comp;
        ++comp;
    }
    return comp;
}
} // namespace scc_kosaraju

namespace scc_tarjan {
vector<int> ids;
int comp;

void run(int n, const vector<vector<int>>& g) {
    ids.assign(n, -1);
    comp = 0;
    vector<int> disc(n, -1), low(n), st;
    vector<char> on(n, 0);
    int timer = 0;

    function<void(int)> dfs = [&](int v) {
        disc[v] = low[v] = timer++;
        st.push_back(v);
        on[v] = 1;
        for (int to : g[v]) {
            if (disc[to] == -1) {
                dfs(to);
                low[v] = min(low[v], low[to]);
            } else if (on[to]) {
                low[v] = min(low[v], disc[to]);
            }
        }
        if (low[v] == disc[v]) {
            while (true) {
                int u = st.back(); st.pop_back();
                on[u] = 0;
                ids[u] = comp;
                if (u == v) break;
            }
            ++comp;
        }
    };

    for (int i = 0; i < n; ++i) if (disc[i] == -1) dfs(i);
}
} // namespace scc_tarjan

// Iterative Kosaraju (avoids recursion depth on deep chains)
namespace scc_kosaraju_iter {
vector<int> ids;
int comp;

int run(int n, const vector<vector<int>>& g) {
    vector<vector<int>> gr(n);
    for (int v = 0; v < n; ++v)
        for (int to : g[v]) gr[to].push_back(v);

    vector<int> order;
    order.reserve(n);
    vector<char> used(n, 0);
    vector<int> it(n, 0);
    for (int s = 0; s < n; ++s) if (!used[s]) {
        vector<int> st = {s};
        used[s] = 1;
        while (!st.empty()) {
            int v = st.back();
            if (it[v] < (int)g[v].size()) {
                int to = g[v][it[v]++];
                if (!used[to]) { used[to] = 1; st.push_back(to); }
            } else {
                order.push_back(v);
                st.pop_back();
            }
        }
    }

    fill(used.begin(), used.end(), 0);
    fill(it.begin(), it.end(), 0);
    ids.assign(n, -1);
    comp = 0;
    for (int i = n - 1; i >= 0; --i) {
        int s = order[i];
        if (used[s]) continue;
        vector<int> st = {s};
        used[s] = 1;
        ids[s] = comp;
        while (!st.empty()) {
            int v = st.back();
            if (it[v] < (int)gr[v].size()) {
                int to = gr[v][it[v]++];
                if (!used[to]) { used[to] = 1; ids[to] = comp; st.push_back(to); }
            } else st.pop_back();
        }
        ++comp;
    }
    return comp;
}
} // namespace scc_kosaraju_iter
```

##### Python 3 Template

```python
# Python 3.11+ — usable for n,m ≤ ~2e5 if recursion raised or iterative Kosaraju used
import sys
sys.setrecursionlimit(1_000_000)

def kosaraju(n: int, g: list[list[int]]) -> tuple[list[int], int]:
    gr = [[] for _ in range(n)]
    for v, outs in enumerate(g):
        for to in outs:
            gr[to].append(v)
    used = [False] * n
    order: list[int] = []

    def dfs1(v: int) -> None:
        used[v] = True
        for to in g[v]:
            if not used[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if not used[i]:
            dfs1(i)

    used = [False] * n
    ids = [-1] * n
    comp = 0

    def dfs2(v: int) -> None:
        used[v] = True
        ids[v] = comp
        for to in gr[v]:
            if not used[to]:
                dfs2(to)

    for v in reversed(order):
        if not used[v]:
            dfs2(v)
            comp += 1
    return ids, comp


def tarjan(n: int, g: list[list[int]]) -> tuple[list[int], int]:
    ids = [-1] * n
    disc = [-1] * n
    low = [0] * n
    on = [False] * n
    st: list[int] = []
    timer = 0
    comp = 0

    def dfs(v: int) -> None:
        nonlocal timer, comp
        disc[v] = low[v] = timer
        timer += 1
        st.append(v)
        on[v] = True
        for to in g[v]:
            if disc[to] == -1:
                dfs(to)
                low[v] = min(low[v], low[to])
            elif on[to]:
                low[v] = min(low[v], disc[to])
        if low[v] == disc[v]:
            while True:
                u = st.pop()
                on[u] = False
                ids[u] = comp
                if u == v:
                    break
            comp += 1

    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    return ids, comp
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Mutually reachable,” “cycle of dependencies,” “can return to start”
- “Minimum edges to make the digraph strongly connected”
- Constraints that look like 2-SAT (implication cycles)
- “Condensation is a chain / has unique source”
- Need component id then DP on the DAG of components

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting transpose edges (Kosaraju) → wrong components
- Processing finish order **ascending** instead of descending
- Tarjan: updating `low` from nodes **not on stack** (cross to finished SCC) → merges distinct SCCs
- 1-index vs 0-index mismatch; isolated vertices must still get a component
- Recursion depth on a long path (\(n=10^6\)) → use iterative Kosaraju
- Multiple edges / self-loops: self-loop does not split SCC; fine to keep

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Component graph construction:** see Condensation DAG (§3)
- **Largest SCC / count SCCs:** trivial post-process on `ids`
- **Edge SCCs / bridge-block tree:** different (undirected); use bridges (§2)
- **Incremental SCC:** hard online; usually offline rebuild or special structure — not this template

---

#### 11. Typical Problem Archetypes

1. Standard application: label SCCs; print size of largest
2. Slightly disguised: “can A reach B and B reach A?” → same component
3. Difficult: minimum edges to make strongly connected (use condensation in/out degrees)
4. Very difficult / advanced: 2-SAT + optimization over condensation; or SCC of implication of a constructed graph

---

#### 12. Recognition & Identification Drills

1. Directed graph; for each vertex output the size of its strong component.
2. You may add edges; minimize additions so the digraph becomes strongly connected (or report impossible).
3. Cities with one-way roads; tourists want a tour that can revisit via mutual reachability clusters — count clusters with no outgoing road to another cluster.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: mutual reachability / collapse cycles in digraphs
- Key invariant: condensation of SCCs is a DAG
- Key formula: Kosaraju = DFS order on \(G\) + DFS on \(G^T\); Tarjan: pop when `low==disc`
- Complexity: \(O(n+m)\)
- Template to remember: finish-order peel (Kosaraju) or stack+lowlink (Tarjan)

---

---


---

<a id="topic-2"></a>
### 2. Bridges and articulation points

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Undirected graphs, DFS tree, discovery times; distinguish tree vs back edges  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Undirected graphs, DFS tree, discovery times; distinguish tree vs back edges

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

Run DFS on an **undirected** graph. Tree edges build a spanning forest; back edges go to ancestors.

- **Bridge:** tree edge \(v\to u\) (child) with `low[u] > disc[v]` — no back edge from \(u\)’s subtree escapes to \(v\) or above → removing it disconnects.
- **Articulation point:** non-root \(v\) if some child has `low[child] >= disc[v]`; root if it has ≥2 DFS children. Removing \(v\) disconnects the graph.

`low[x]` = earliest discovery time reachable from \(x\)’s subtree using tree edges and **at most one back edge**.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: \(O(1)\) after flags computed
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Critical road / cable / friendship whose removal disconnects”
- “Edges that lie on all paths between …” (bridges are exactly edges not on any cycle)
- Build **bridge-block tree** (components after deleting bridges form a tree)
- “How many edges must stay / are non-bridges”
- Vertex connectivity-1 cuts (articulation)

---

#### 7. Contest WA / TLE / RE Traps

- Treating the graph as directed; bridges are an **undirected** notion
- Not skipping parent edge → every tree edge looks like a back edge mess
- **Multi-edges:** parent check by edge id, not by vertex; parallel edges ⇒ not a bridge
- Using `low[to] >= disc[v]` for bridges (should be **strict** `>` for bridges)
- Root articulation: counting neighbors instead of DFS-tree children
- Articulation can be true for multiple reasons — use a `bool` flag, don’t early-return wrongly
- Disconnected graphs: loop over all starts

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Bridge-block tree:** shrink each 2-edge-connected component to a node; bridges become tree edges — then path queries / “must cross bridge”
- **Biconnected components (vertex):** stack of edges during DFS; pop when articulation condition triggers
- **Online bridges:** harder; usually rebuild or special structures
- **Directed “bridges”:** bridge-like notions differ (strong bridges) — rare; not this template

---

#### 11. Typical Problem Archetypes

1. Standard application: list all bridges / articulation points
2. Slightly disguised: count pairs of vertices whose unique path uses a given edge
3. Difficult: maximize components after removing one edge; or build bridge tree + binary lifting
4. Very difficult / advanced: 2-edge-connected orientation; cactus graphs; DP on bridge-block tree

---

#### 12. Recognition & Identification Drills

1. Undirected roads; find all roads whose destruction splits the country into more pieces.
2. Network nodes; find vertices whose failure disconnects communication.
3. After compressing bridge-blocks, answer whether two cities stay connected if any single non-bridge road fails (always yes inside a block).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: critical edges/vertices in undirected graphs
- Key invariant: `low` via DFS tree + back edges
- Key formula: bridge iff `low[child] > disc[v]`; art iff root≥2 children or `low[child] >= disc[v]`
- Complexity: \(O(n+m)\)
- Template to remember: edge-id parent skip + `disc`/`low`

---

---


---

<a id="topic-3"></a>
### 3. Condensation DAG

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** SCC labels; DAG algorithms (topo, DP)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: SCC labels; DAG algorithms (topo, DP)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

After SCC, every interesting **global** reachability question is a question on a DAG of \(k\le n\) supernodes. Multiple edges between the same pair of components collapse to one. Sources/sinks of this DAG control “make strongly connected,” “mandatory visits,” and DP entry points.

Classic theorem: for a digraph with \(k\) SCCs forming a condensation with \(a\) sources (in-degree 0) and \(b\) sinks (out-degree 0), if \(k=1\) answer 0; else minimum edges to make strongly connected is \(\max(a,b)\) (assuming the underlying undirected condensation is weakly connected — usually assumed or handled).

---

#### 4. Proof Sketches & Recurrences

Map each vertex \(v\) to \(c=\mathrm{id}[v]\). For every edge \(u\to v\) with \(\mathrm{id}[u]\neq\mathrm{id}[v]\), add condensation edge \(c_u\to c_v\). Deduplicate with `set` or sort+unique.

Weak connectivity of the **underlying** undirected condensation matters for the \(\max(a,b)\) formula; if the original digraph is not weakly connected, answer is often “impossible” for strong connectivity with arbitrary added edges still inside the vertex set (added edges can connect components — usually you may add any directed edge; then connect weak components carefully: formula generalizes by considering each weak piece).

Topo order of condensation = order of Tarjan component ids often already reverse-topo if Tarjan assigns in pop order — **do not rely on that**; run explicit topo/Kahn or DFS finish on the DAG.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m\log m)\) with sort-unique per list, or \(O(n+m)\) expected with hash sets
- Per-query / per-operation: topo \(O(k+e)\), \(k=\#SCC\)
- Total: dominated by SCC + build
- Memory: \(O(k+e)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Just computed SCCs and now need reachability / DP / counting paths between components
- “Add minimum edges to become strongly connected”
- Values on nodes; take max/sum along any path in the cyclic digraph → DP on condensation
- Unique sink / chain condensation ⇒ greedy forced order

---

#### 7. Contest WA / TLE / RE Traps

- Keeping intra-component edges in the DAG (breaks acyclicity / DP)
- Forgetting to unique multi-edges → wrong degrees for \(\max(a,b)\)
- Applying \(\max(a,b)\) when `comp==1` (should be 0) or when graph not weakly connected
- Using vertex weights twice when aggregating component weight (sum once per component)
- Assuming Tarjan ids are topo order without verifying

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Weighted condensation:** `w[c] = f(nodes in c)` then DAG DP
- **Reachability matrix on DAG:** bitsets on topo order \(O(k^2/64)\)
- **Minimum path cover style** on transitively reduced DAGs — different problem family
- **Condensation of undirected bridge-blocks:** tree, not DAG — see bridges variants

---

#### 11. Typical Problem Archetypes

1. Standard application: build DAG; count sources/sinks
2. Slightly disguised: max sum of node values on a path in a digraph with cycles
3. Difficult: min edges to strong; or assign each SCC a value under topo constraints
4. Very difficult / advanced: optimize over subsets of components with reachability bitsets; game on condensation

---

#### 12. Recognition & Identification Drills

1. After SCC, compute how many components have indegree 0 and outdegree 0.
2. Node scores; walk any directed path; maximize total score (each node at most once — cycles force component collapse).
3. Add the fewest one-way flights so from every airport you can reach every other.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: immediately after SCC for global structure
- Key invariant: condensation is a DAG
- Key formula: min edges to strong \(=\max(\#\mathrm{sources},\#\mathrm{sinks})\) if \(k>1\) (weakly connected)
- Complexity: \(O(n+m)\) plus DAG algos
- Template to remember: map edges by `ids`, unique, indeg/outdeg

---

---


---

<a id="topic-4"></a>
### 4. 2-SAT

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Implication logic, SCC on digraphs  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Implication logic, SCC on digraphs

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

Each clause \((a\lor b)\) is equivalent to \((\neg a\Rightarrow b)\land(\neg b\Rightarrow a)\). Build the implication graph on \(2n\) literals (\(x_i\) and \(\neg x_i\)). A variable assignment exists iff for every \(i\), \(x_i\) and \(\neg x_i\) lie in **different** SCCs. To assign: process condensation in **reverse topological** order; if a literal’s component is force-visited before its negation, set it true (standard: assign `x = true` iff `comp[id(x)] > comp[id(~x)]` when Kosaraju ids increase along topo of reverse… — match your SCC id convention carefully).

Common encoding: literal \(x_i\) → index \(2i\), \(\neg x_i\) → \(2i+1\); `NOT(v) = v^1`.

---

#### 4. Proof Sketches & Recurrences

\((a\lor b)\equiv(\neg a\to b)\land(\neg b\to a)\).  
\((a)\equiv(\neg a\to a)\).  
\((a\Leftrightarrow b)\equiv(a\to b)\land(b\to a)\land(\neg a\to\neg b)\land(\neg b\to\neg a)\) or clauses \((a\lor\neg b)(\neg a\lor b)\).

If \(x\) and \(\neg x\) in same SCC, then \(x\Leftrightarrow\neg x\), unsat.

**Assignment:** In the condensation DAG, if \(\mathrm{comp}[\ell]\) is reachable from \(\mathrm{comp}[\neg\ell]\) wrongly… Practical rule with Kosaraju as implemented above (ids increase as we peel sinks of \(G\) / sources of \(G^T\)): set `value[i] = ids[2*i] < ids[2*i+1]` or the opposite depending on peel order — **verify on a tiny sat/unsat instance**. With Tarjan component ids assigned in increasing order as SCCs are closed (often reverse topo of condensation), `value[i] = ids[2*i] > ids[2*i+1]` is the usual choice (true literal = later in reverse-topo = earlier forced). The templates below document the convention used.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\) implications
- Per-query / per-operation: one SCC solve
- Total: \(O(n+m)\) for \(n\) vars, \(m\) clauses
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace twosat {
int n; // number of variables x0..x_{n-1}
vector<vector<int>> g, gr;

int NOT(int x) { return x ^ 1; }
// var i true -> literal 2*i; false -> 2*i+1
int lit(int i, bool is_true) { return 2 * i + (is_true ? 0 : 1); }

void init(int n_vars) {
    n = n_vars;
    g.assign(2 * n, {});
    gr.assign(2 * n, {});
}

void add_imp(int a, int b) { // a => b
    g[a].push_back(b);
    gr[b].push_back(a);
}

void add_or(int a, int b) { // a ∨ b
    add_imp(NOT(a), b);
    add_imp(NOT(b), a);
}

void add_true(int a) { add_or(a, a); }

bool solve(vector<char>& assign) { // assign[i] = value of xi
    int N = 2 * n;
    vector<int> order, ids(N, -1);
    vector<char> used(N, 0);
    function<void(int)> dfs1 = [&](int v) {
        used[v] = 1;
        for (int to : g[v]) if (!used[to]) dfs1(to);
        order.push_back(v);
    };
    for (int i = 0; i < N; ++i) if (!used[i]) dfs1(i);

    function<void(int,int)> dfs2 = [&](int v, int c) {
        ids[v] = c;
        for (int to : gr[v]) if (ids[to] == -1) dfs2(to, c);
    };
    reverse(order.begin(), order.end());
    int comp = 0;
    for (int v : order) if (ids[v] == -1) dfs2(v, comp++);

    assign.assign(n, 0);
    for (int i = 0; i < n; ++i) {
        if (ids[2 * i] == ids[2 * i + 1]) return false;
        // Kosaraju peel: larger id is later source in Gt ≈ earlier in reverse topo of condensation
        assign[i] = ids[2 * i] > ids[2 * i + 1];
    }
    return true;
}
} // namespace twosat
```

##### Python 3 Template

```python
# Python 3.11+ — usable; watch recursion on 2n nodes
import sys
sys.setrecursionlimit(1_000_000)

class TwoSAT:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(2 * n)]
        self.gr = [[] for _ in range(2 * n)]

    @staticmethod
    def NOT(x: int) -> int:
        return x ^ 1

    def add_imp(self, a: int, b: int) -> None:
        self.g[a].append(b)
        self.gr[b].append(a)

    def add_or(self, a: int, b: int) -> None:
        self.add_imp(self.NOT(a), b)
        self.add_imp(self.NOT(b), a)

    def lit(self, i: int, is_true: bool) -> int:
        return 2 * i + (0 if is_true else 1)

    def solve(self) -> list[bool] | None:
        N = 2 * self.n
        used = [False] * N
        order: list[int] = []

        def dfs1(v: int) -> None:
            used[v] = True
            for to in self.g[v]:
                if not used[to]:
                    dfs1(to)
            order.append(v)

        for i in range(N):
            if not used[i]:
                dfs1(i)

        ids = [-1] * N
        comp = 0

        def dfs2(v: int, c: int) -> None:
            ids[v] = c
            for to in self.gr[v]:
                if ids[to] == -1:
                    dfs2(to, c)

        for v in reversed(order):
            if ids[v] == -1:
                dfs2(v, comp)
                comp += 1

        assign = [False] * self.n
        for i in range(self.n):
            if ids[2 * i] == ids[2 * i + 1]:
                return None
            assign[i] = ids[2 * i] > ids[2 * i + 1]
        return assign
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Boolean variables with constraints “at least one of …,” “same / different,” “if A then B”
- Pairing students / coloring with 2 colors under XOR-like constraints
- “Choose one of two options for each item” with conflicts
- Guessing binary choices where implications close under SCC

---

#### 7. Contest WA / TLE / RE Traps

- Wrong literal indexing (`2i` / `2i+1`) or forgotten `NOT`
- Adding only one implication for a clause
- Assignment comparison inverted → sat but wrong model (validate clauses!)
- Using undirected edges; implication graph is **directed**
- Forcing `x` and `~x` same by buggy force-true on both
- Variables 1..n vs 0..n-1 off-by-one in problem statements

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **At-most-one** among \(k\) options: pairwise \(\neg x_i\lor\neg x_j\) or prefix encodings
- **Exactly-one:** at-most-one + at-least-one
- **2-SAT + maximize true vars:** often binary search + force prefixes, or greedy on condensation
- **Weighted 2-SAT:** harder; sometimes min-cut reduction — not plain SCC

---

#### 11. Typical Problem Archetypes

1. Standard application: clauses given explicitly; output assignment
2. Slightly disguised: each object has two placements; conflicts → `add_or(NOT(a), NOT(b))`
3. Difficult: build implications from geometry / schedule “if use A then must use B”
4. Very difficult / advanced: 2-SAT layered with binary search on threshold; or SCC condensation DP for lexicographically least assignment

---

#### 12. Recognition & Identification Drills

1. \(n\) boolean vars; \(m\) clauses of size ≤2; decide satisfiability and print a model.
2. Each friend chooses room A or B; some pairs refuse to share; some refuse to separate — model as 2-SAT.
3. Pieces on a strip can face L/R; adjacency constraints of the form “if this faces L then neighbor must face R.”

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: boolean constraints reducible to 2-CNF / implications
- Key invariant: sat \(\iff\) no var shares SCC with its negation
- Key formula: \((a\lor b)\Rightarrow(\neg a\to b),(\neg b\to a)\)
- Complexity: \(O(n+m)\)
- Template to remember: `add_or` + Kosaraju on \(2n\) nodes + compare component ids

---

---


---

<a id="topic-5"></a>
### 5. Topological-DP patterns

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** DAG / condensation, memoized DP or topo iteration; shortest/longest paths on DAG  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: DAG / condensation, memoized DP or topo iteration; shortest/longest paths on DAG

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

On a DAG (or after condensation), every DP state can finalize when all incoming predecessors are done — **Kahn / reverse-topo loops** replace recursion. Patterns: longest path, min/max cost to reach, count paths, AND/OR game DP, knapsack along topo, DP on labeled DAGs from SCC.

If the original graph has cycles but DP “takes max over a walk,” either the answer is unbounded (positive cycle) or you must **collapse SCCs** and DP on the DAG with aggregated node weights.

---

#### 4. Proof Sketches & Recurrences

Let topo order be \(v_1,\ldots,v_n\). For longest path with node weight \(w\):
\[
\mathrm{dp}[v]=w[v]+\max_{u\to v}\mathrm{dp}[u]\quad(\max\emptyset=0\text{ if sources allowed empty pred})
\]
Or edge weights: \(\mathrm{dp}[v]=\max_{u\to v}(\mathrm{dp}[u]+w(u,v))\).

Count paths to \(t\): \(\mathrm{dp}[t]=1\); process reverse topo: \(\mathrm{dp}[u]=\sum_{u\to v}\mathrm{dp}[v]\).

**With cycles:** if seeking finite simple-path optimum under additive scores and cycles can be used to inflate, detect positive cycle in relevant part; else SCC-aggregate then DAG DP.

Complexity \(O(n+m)\) per DP layer.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: topo \(O(n+m)\)
- Per-query / per-operation: usually one linear DP
- Total: \(O(n+m)\) (or \(O(k+e)\) on condensation)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace topo_dp {
// Longest path by node weights on a DAG. dp[v] = best path ending at v (path may start anywhere).
vector<long long> longest_node_weight(int n, const vector<vector<int>>& g, const vector<long long>& w) {
    vector<int> indeg(n, 0);
    for (int v = 0; v < n; ++v) for (int to : g[v]) ++indeg[to];
    queue<int> q;
    for (int i = 0; i < n; ++i) if (indeg[i] == 0) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        order.push_back(v);
        for (int to : g[v]) if (--indeg[to] == 0) q.push(to);
    }
    const long long NEG = (long long)-4e18;
    vector<long long> dp(n, NEG);
    for (int v : order) {
        if (dp[v] == NEG) dp[v] = w[v]; // start a new path at v
        for (int to : g[v]) dp[to] = max(dp[to], dp[v] + w[to]);
    }
    return dp;
}

// Count paths from all sources to each node mod MOD
vector<int> count_paths(int n, const vector<vector<int>>& g, int MOD) {
    vector<int> indeg(n, 0);
    for (int v = 0; v < n; ++v) for (int to : g[v]) ++indeg[to];
    queue<int> q;
    vector<int> dp(n, 0);
    for (int i = 0; i < n; ++i) if (indeg[i] == 0) { q.push(i); dp[i] = 1; }
    vector<int> indeg2 = indeg;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        for (int to : g[v]) {
            dp[to] += dp[v];
            if (dp[to] >= MOD) dp[to] -= MOD;
            if (--indeg2[to] == 0) q.push(to);
        }
    }
    return dp;
}

// Condensation DP: max path sum of component weights
long long max_path_on_condensation(int comp, const vector<vector<int>>& dag, const vector<long long>& cw) {
    vector<int> indeg(comp, 0);
    for (int v = 0; v < comp; ++v) for (int to : dag[v]) ++indeg[to];
    queue<int> q;
    for (int i = 0; i < comp; ++i) if (indeg[i] == 0) q.push(i);
    vector<long long> dp(comp, 0);
    long long ans = 0;
    vector<int> indeg2 = indeg;
    // init: process in topo
    vector<int> order;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        order.push_back(v);
        for (int to : dag[v]) if (--indeg2[to] == 0) q.push(to);
    }
    const long long NEG = (long long)-4e18;
    fill(dp.begin(), dp.end(), NEG);
    for (int v : order) {
        if (dp[v] == NEG) dp[v] = cw[v];
        ans = max(ans, dp[v]);
        for (int to : dag[v]) dp[to] = max(dp[to], dp[v] + cw[to]);
    }
    return ans;
}
} // namespace topo_dp
```

##### Python 3 Template

```python
# Python 3.11+ — practical for n,m ≤ few 1e5
from collections import deque

NEG = -10**30

def longest_on_dag(n: int, g: list[list[int]], w: list[int]) -> list[int]:
    indeg = [0] * n
    for v in range(n):
        for to in g[v]:
            indeg[to] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    indeg2 = indeg[:]
    while q:
        v = q.popleft()
        order.append(v)
        for to in g[v]:
            indeg2[to] -= 1
            if indeg2[to] == 0:
                q.append(to)
    dp = [NEG] * n
    for v in order:
        if dp[v] == NEG:
            dp[v] = w[v]
        for to in g[v]:
            cand = dp[v] + w[to]
            if cand > dp[to]:
                dp[to] = cand
    return dp


def count_paths(n: int, g: list[list[int]], MOD: int) -> list[int]:
    indeg = [0] * n
    for v in range(n):
        for to in g[v]:
            indeg[to] += 1
    dp = [0] * n
    q = deque()
    for i in range(n):
        if indeg[i] == 0:
            q.append(i)
            dp[i] = 1
    indeg2 = indeg[:]
    while q:
        v = q.popleft()
        for to in g[v]:
            dp[to] = (dp[to] + dp[v]) % MOD
            indeg2[to] -= 1
            if indeg2[to] == 0:
                q.append(to)
    return dp
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Explicit DAG / dependency graph / course prerequisites
- Digraph + “maximum score along a path”
- After SCC: “value of a component is sum; edges between”
- Counting ways to reach sink; probability on DAG
- Game on DAG: win/lose/grundy from sinks upward

---

#### 7. Contest WA / TLE / RE Traps

- Running DP on a graph that still has cycles → infinite loop in Kahn or wrong recursion
- Initializing only sources when paths may start anywhere (or the opposite)
- Double-counting node weight at both ends of an edge relaxation
- Modulo bugs when counting paths; forgetting unreachable zeros
- After SCC: adding component weight on every edge relaxation incorrectly (add once at node)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Shortest path on DAG:** same but `min` and careful \(+\infty\) init
- **Knapsack on DAG:** state `(node, budget)` processed in topo — \(O((n+m)W)\)
- **Bitwise OR / idempotent merges:** DP values are sets/bitsets along topo
- **Labeled transitions:** matrix product along paths — combine with adjacency

---

#### 11. Typical Problem Archetypes

1. Standard application: longest path in a DAG
2. Slightly disguised: project dependencies with profits; max profit chain
3. Difficult: DP on condensation with large aggregated weights; count paths mod \(p\)
4. Very difficult / advanced: DP on DAG of SCCs + secondary constraints (bitset reachability filters)

---

#### 12. Recognition & Identification Drills

1. Directed acyclic task graph; each task has duration; longest chain of tasks.
2. City network with one-way streets forming cycles; maximize sum of attractions on a route without using a positive-score cycle forever — collapse first.
3. Count modulo \(10^9+7\) the number of paths from sources to a given sink in a DAG.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: dependencies / digraph DP after making acyclic
- Key invariant: process in topological order
- Key formula: \(\mathrm{dp}[v]=\mathrm{agg}_{u\to v}(\mathrm{dp}[u])\oplus w[v]\)
- Complexity: \(O(n+m)\)
- Template to remember: Kahn topo + relax; SCC then DP if cycles

---

[Back to Section 07 index](07-graph-algorithms-advanced.md) · [Part B](07-b-dsu-rollback-offline.md)

---

---


---

<a id="topic-6"></a>
### 6. Block-Cut Tree (BCT)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Articulation Points, Biconnected Components (BCC)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Articulation Points, Biconnected Components (BCC)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

The **Block-Cut Tree** is a meta-graph where:
1. Every articulation point is a "cut" vertex.
2. Every biconnected component is a "block" vertex.
3. Edges connect a block vertex to all cut vertices that belong to that BCC.

This forms a tree! Any path between $U$ and $V$ in the original graph must pass through the exact sequence of articulation points on the simple path between their corresponding nodes in the Block-Cut Tree. This trivially solves "must-pass-through" or "maximum weight cycle on path" queries.

---

#### 4. Proof Sketches & Recurrences

Tarjan's DFS maintains discovery times $tin[u]$ and lowest reachable ancestor times $low[u]$. Vertex $u$ is an articulation point if $low[v] \ge tin[u]$ for some child $v$ (or if root has $\ge 2$ children). During DFS, edges are maintained on an edge stack. When $low[v] \ge tin[u]$ triggers, all edges up to $(u, v)$ on the stack form a new biconnected block. The resulting BCT has at most $2V$ vertices and $2V - 1$ edges, with bipartite structure alternating between cut vertices and blocks.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Builds BCCs and the BCT
// graph is 0-indexed, output BCT has original vertices (articulation points) 
// and new block vertices starting from id N.
vector<vector<int>> bct; // size N + num_bccs
vector<int> bcc_id; // Maps original edge/vertex to BCC
```

---

#### 6. Recognition Trigger Signals & Heuristics

- (Omitted full template due to length, but relies on Tarjan's stack of edges).*

---

#### 7. Contest WA / TLE / RE Traps

- Root of DFS tree articulation condition: root is a cut vertex if and only if it has $\ge 2$ DFS children, not when $low[v] \ge tin[u]$.
- Popping the edge/vertex stack too far: the cut vertex $u$ itself must NOT be popped during child block extraction because $u$ belongs to multiple blocks.
- Graph has multiple disconnected components: must iterate DFS from $1$ to $N$ to cover all components.
- Index allocation: BCT contains up to $2V$ vertices; resizing arrays to $N$ causes out-of-bounds access.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---


---

<a id="topic-7"></a>
### 7. DSU rollback

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Classic DSU (union by rank/size); understanding that path compression prevents undo  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Classic DSU (union by rank/size); understanding that path compression prevents undo

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

Standard DSU with path compression is nearly \(O(1)\) but **irreversible**. If you need to **undo** unions (DFS backtrack, time travel, segment tree descent), drop path compression; keep **union by rank/size** only. Each `unite` pushes a stack record `{parent_changed, old_parent, rank_changed, old_rank, old_components}`; `rollback(t)` pops until stack size `t`.

This gives \(O(\log n)\) per unite/find (rank ≤ \(\log n\)) and \(O(1)\) amortized per undo step — perfect for offline structures that add edges on the way down a recursion and remove on the way up.

---

#### 4. Proof Sketches & Recurrences

Without path compression, find is \(O(\log n)\) with union-by-rank. Stack stores enough to invert the last link:
- only the child root’s `p[child]=parent` changes (and maybe `sz`/`rk` of parent)
- if already same component, push a no-op marker or skip

Checkpoint: `int checkpoint = dsu.history_size(); …; dsu.rollback(checkpoint);`

Component count: decrement on successful merge; restore on rollback.

**Bipartite DSU:** store parity relative to parent; rollback same way — useful for “odd cycle offline.”

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: find/unite \(O(\log n)\); rollback amortized \(O(1)\) per recorded change
- Total: depends on caller (often \(O((n+m+q)\log n\log T)\) with time segtree)
- Memory: \(O(n + \#\mathrm{unites})\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace dsu_rollback {
struct DSU {
    vector<int> p, r;
    int comps;
    struct Change { int u, pu, v, rv; int comps_before; bool merged; };
    vector<Change> st;

    DSU(int n = 0) { init(n); }
    void init(int n) {
        p.resize(n); r.assign(n, 0);
        iota(p.begin(), p.end(), 0);
        comps = n;
        st.clear();
    }
    int find(int x) {
        while (x != p[x]) x = p[x];
        return x;
    }
    int snapshot() const { return (int)st.size(); }

    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) {
            st.push_back({a, a, b, r[b], comps, false});
            return false;
        }
        if (r[a] < r[b]) swap(a, b);
        st.push_back({b, p[b], a, r[a], comps, true});
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
        --comps;
        return true;
    }

    void rollback(int snap) {
        while ((int)st.size() > snap) {
            auto ch = st.back(); st.pop_back();
            if (!ch.merged) continue;
            p[ch.u] = ch.pu;      // u was child root b
            r[ch.v] = ch.rv;      // v was parent a
            comps = ch.comps_before;
        }
    }
    bool same(int a, int b) { return find(a) == find(b); }
};

// Optional: DSU with parity (bipartite check)
struct DSUParity {
    vector<int> p, r, par; // par[x] = parity of x xor parent edge
    struct Change { int b, pb, pa_par, a, ra, merged; };
    vector<Change> st;
    bool bipok = true;
    vector<char> bip_st; // track bipok history if needed

    DSUParity(int n) { p.resize(n); iota(p.begin(), p.end(), 0); r.assign(n, 0); par.assign(n, 0); }

    int snapshot() const { return (int)st.size(); }

    pair<int,int> find(int x) { // {root, parity to root}
        int pr = 0;
        while (x != p[x]) { pr ^= par[x]; x = p[x]; }
        return {x, pr};
    }

    void unite(int a, int b) { // add edge a—b (should differ parity)
        auto [ra, pa] = find(a);
        auto [rb, pb] = find(b);
        if (ra == rb) {
            st.push_back({rb, rb, 0, ra, r[ra], 0});
            if ((pa ^ pb) == 0) bipok = false; // odd cycle
            return;
        }
        if (r[ra] < r[rb]) { swap(ra, rb); swap(pa, pb); }
        // link rb -> ra; edge means parity of rb relative to ra:
        // pa ^ edge ^ pb = 1 => edge_parity = 1 ^ pa ^ pb
        int edge = 1 ^ pa ^ pb;
        st.push_back({rb, p[rb], par[rb], ra, r[ra], 1});
        p[rb] = ra;
        par[rb] = edge;
        if (r[ra] == r[rb]) ++r[ra];
    }

    void rollback(int snap) {
        while ((int)st.size() > snap) {
            auto ch = st.back(); st.pop_back();
            if (!ch.merged) continue;
            p[ch.b] = ch.pb;
            par[ch.b] = ch.pa_par;
            r[ch.a] = ch.ra;
        }
    }
};
} // namespace dsu_rollback
```

##### Python 3 Template

```python
# Python 3.11+ — educational; prefer C++ in contest for large n
class DSURollback:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n
        self.comps = n
        self.st: list[tuple] = []

    def find(self, x: int) -> int:
        while x != self.p[x]:
            x = self.p[x]
        return x

    def snapshot(self) -> int:
        return len(self.st)

    def unite(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            self.st.append((a, a, b, self.r[b], self.comps, False))
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.st.append((b, self.p[b], a, self.r[a], self.comps, True))
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        self.comps -= 1
        return True

    def rollback(self, snap: int) -> None:
        while len(self.st) > snap:
            b, pb, a, ra, comps_before, merged = self.st.pop()
            if not merged:
                continue
            self.p[b] = pb
            self.r[a] = ra
            self.comps = comps_before
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Edges exist only during a time interval”
- DFS on a segment tree where each node stores a list of edges alive on that segment
- Divide-and-conquer on time; queries ask connectivity / component size / bipartiteness at a moment
- Persistent connectivity **offline** (all queries known)
- Need undo after exploring a hypothetical union

---

#### 7. Contest WA / TLE / RE Traps

- Enabling path compression → rollback corrupted
- Forgetting to store rank/size before increment
- Rolling back past 0 / mismatch snapshot indices
- Not pushing a record on “already united” when later logic expects aligned stack (optional; be consistent)
- Mixing two DSU instances’ snapshots
- Using recursive find with compression “just once”

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Union by size** instead of rank — store old size
- **Component aggregates** (sum of values): store old parent aggregate; update on merge
- **Bipartite / colored DSU** with parity (above)
- **Fully persistent DSU:** different (version trees); rollback is partial persistence via stack

---

#### 11. Typical Problem Archetypes

1. Standard application: add/undo edges in DFS; query `same` at leaves
2. Slightly disguised: spanning forest size history with backtracking
3. Difficult: offline dynamic connectivity (§7)
4. Very difficult / advanced: offline bipartiteness with edge lifespan; dynamic MST offline with LCT alternatives

---

#### 12. Recognition & Identification Drills

1. Process operations: add edge, delete last edge (LIFO), query connectivity — stack of unions.
2. A recursion explores unions; after each recursive call the DSU must match the pre-call state.
3. Edges live on time intervals; queries ask whether two vertices are connected at time \(t\) (prelude to §7).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need undo unions; offline time structure
- Key invariant: no path compression; union by rank/size + history stack
- Key formula: snapshot = stack size; rollback pops merges
- Complexity: \(O(\log n)\) per unite/find
- Template to remember: `snapshot/unite/rollback`

---

---


---

<a id="topic-8"></a>
### 8. Offline dynamic connectivity

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2200–2800 | **Frequency:** Occasional  
> **Prerequisites:** DSU rollback; segment tree over time; offline queries  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: DSU rollback; segment tree over time; offline queries

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

All edge insertions/deletions and connectivity queries are known offline. Each edge exists on a half-open time interval \([L,R)\). Build a **segment tree on time**; store the edge in \(O(\log T)\) nodes covering \([L,R)\). DFS the segment tree: at node, `unite` all stored edges; recurse children; answer queries living at time leaves; `rollback` to snapshot. Never delete online — deletion is “interval ends.”

This solves dynamic connectivity **offline** in \(O((n+m+q)\log n\log T)\) without Link-Cut Trees.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(m\log T)\) edge placements; \(O(n)\) DSU
- Per-query / per-operation: answered at leaf in \(O(\log n)\) find
- Total: \(O((n + m\log T + q)\log n)\) typical
- Memory: \(O(m\log T + q)\)`

##### C++17 Template

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

##### Python 3 Template

```python
# Python 3.11+ — sketch only; too slow for tight limits
# Same DFS-over-time-segtree + DSURollback as C++; omit full code for contest use.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Explicit timeline of add/remove edge + “are u,v connected?”
- Edges given as lifespan intervals
- “Graph evolves; answer after each day” with known future
- Same pattern for offline dynamic bipartiteness / component count / sum queries

---

#### 7. Contest WA / TLE / RE Traps

- Half-open interval off-by-one (`[L,R)` vs `[L,R]`)
- Forgetting to close edges still open at the end
- Parallel edges: treat each appearance as distinct lifespan, or multiset of lifetimes
- Answering queries before uniting leaf edges (leaf node must store edges covering that instant)
- Rollback in wrong order / skipping snapshot after unites
- Using path compression DSU
- Time coordinates not compressed → huge empty segtree (compress event times)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Component count / size queries:** maintain `comps` in rollback DSU; answer at leaves
- **Offline bipartiteness:** DSU with parity + rollback
- **Weighted edges / MST dynamic offline:** different (usually LCT or divide-conquer on weight)
- **Online dynamic connectivity:** much harder — skip unless specialty (HDT, LCT)

---

#### 11. Typical Problem Archetypes

1. Standard application: add/del/query connectivity offline
2. Slightly disguised: roads under repair on days; queries on other days
3. Difficult: same with component aggregates / bipartite checks
4. Very difficult / advanced: offline fully dynamic MST; multi-dimensional time (rare)

---

#### 12. Recognition & Identification Drills

1. Timeline of edge inserts/deletes; after some ops ask if two cities are connected — all ops given upfront.
2. Each edge has birth and death day; \(q\) night queries about connectivity.
3. Same as (1) but also ask whether the graph is bipartite after each query time.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: offline edge lifespan + connectivity queries
- Key invariant: segtree-on-time stores edges; DFS unite/rollback
- Key formula: interval cover \(O(\log T)\) nodes; total \(O(m\log T\log n)\)
- Complexity: \(O((m\log T+q)\log n)\)
- Template to remember: time segtree + `dsu_rollback`

---

---


---

<a id="topic-9"></a>
### 9. Heavy-Light Decomposition (STUB)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Tree DFS, Subtree Sizes, Euler Tour, Segment Tree
- Tradeoff: Decomposes any tree into $\mathcal{O}(\log N)$ contiguous array intervals for arbitrary path queries.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

To support arbitrary path queries ($u \leftrightarrow v$) with point or range updates on a tree: Heavy-Light Decomposition classifies each child edge as *heavy* (pointing to the child with the maximum subtree size $sz[v] > sz[u]/2$) or *light*. Because light child subtrees at most halve the tree size ($sz[v] \le sz[u]/2$), any path from root to any leaf encounters at most $\log_2 N$ light edges. Heavy edges form contiguous paths. By assigning DFS entrance times along heavy paths first, every heavy path maps to a contiguous interval on a 1D array. Any path query decomposes into at most $\mathcal{O}(\log N)$ segment tree queries!

---

#### 4. Proof Sketches & Recurrences

Let $sz[u]$ be the subtree size of $u$. Since $\sum_{v \in \text{children}(u)} sz[v] = sz[u] - 1$, at most one child can satisfy $sz[v] > (sz[u] - 1)/2$. Light edges strictly halve the component size: traversing a light edge reduces remaining vertices by $\ge 50\%$. Therefore, any root-to-node path crosses at most $\lfloor \log_2 N \rfloor$ light edges and at most $\lfloor \log_2 N \rfloor$ heavy paths. Any tree path $u \leftrightarrow v$ is split at $\text{LCA}(u, v)$ into two root-ward paths, each crossing $\le \log_2 N$ heavy chains. Query complexity is $\mathcal{O}(\log^2 N)$ with a standard Segment Tree.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Path modification: 'Add $X$ to all nodes/edges on path from $u$ to $v$' and query path sum/max.
- Subtree and path queries combined: subtrees are naturally contiguous intervals $[pos[u], pos[u] + sz[u] - 1]$.
- Dynamic path GCD, path XOR, or path maximum queries with point updates.
- LCA query in $\mathcal{O}(\log N)$ without binary lifting.

---

#### 7. Contest WA / TLE / RE Traps

- Edge weight queries: forgotten that edge between $u$ and parent corresponds to $pos[u]$. When querying path $u \leftrightarrow v$, the LCA node must be excluded: $[pos[u] + 1, pos[v]]$.
- Calling `dfs_hld` without visiting `heavy[u]` first; if light children are visited first, heavy path continuity in `pos` is broken.
- Swapping `u` and `v` based on `depth[u]` instead of `depth[head[u]]` during chain jumping.
- Failing to call `init()` before querying.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---


---

<a id="topic-10"></a>
### 10. Centroid decomposition (STUB)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 2100–2600
- Prerequisites: Tree DFS, Centroid of Tree, Divide and Conquer
- Tradeoff: Solves path counting/optimization problems on unrooted trees in $\mathcal{O}(N \log N)$ or $\mathcal{O}(N \log^2 N)$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

##### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

##### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

##### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

##### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

#### 3. Core Intuition & Problem Framing

A centroid of a tree of $N$ nodes is a vertex whose removal partitions the tree into connected components, each having size at most $\lfloor N/2 \rfloor$. Every tree has at least one and at most two centroids. Centroid Decomposition recursively finds the centroid $C$ of the tree, solves all path queries passing through $C$, removes $C$, and recurses on the remaining subtrees. Because the tree size halves at each step, the recursion depth is bounded by $\lceil \log_2 N \rceil$. The resulting 'Centroid Tree' has height $\le \log_2 N$, enabling dynamic distance updates and queries across the entire tree.

---

#### 4. Proof Sketches & Recurrences

At depth $k$ of the decomposition, the tree is partitioned into at most $2^k$ components, each of size $\le N / 2^k$. In each component, finding the centroid and aggregating path statistics takes time proportional to the component size. Summing across all components at depth $k$ gives $\mathcal{O}(N)$ work. Since maximum recursion depth is $\log_2 N$, total time for static path counting is $\mathcal{O}(N \log N)$. For dynamic queries, a node has at most $\log_2 N$ centroid ancestors; updating distance to all centroid ancestors takes $\mathcal{O}(\log^2 N)$ or $\mathcal{O}(\log N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Count pairs of vertices $(u, v)$ such that $\text{dist}(u, v) = K$ or $\text{dist}(u, v) \le K$ in a tree of $N \le 2 \times 10^5$.
- Dynamic queries: 'Turn node $u$ red' and 'Find distance from query node $v$ to the closest red node' (Centroid Tree with $\log N$ ancestor updates).
- Tree path problems where path property is non-invertible (e.g. median, bitwise conditions).
- Tree paths of length at most $K$ with maximum profit.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to mark `removed[c] = 1`: without marking removed centroids, DFS will traverse already processed components, causing $\mathcal{O}(N^2)$ worst-case TLE.
- Recalculating subtree sizes: must call `get_sz(u, 0)` on the current component before running `get_centroid` so `sz` values reflect the current component size, not the global tree size.
- Overcounting paths that lie within the same child subtree: must subtract contributions from individual subtrees of $c$.
- Stack overflow in deep trees if `sz` is computed incorrectly.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---


---
