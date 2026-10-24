# 1. SCC: Kosaraju + Tarjan

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier (Kosaraju) / A-tier (Tarjan) | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Directed graphs, DFS, finish times / discovery times; adjacency lists  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (Kosaraju) / A-tier (Tarjan)
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Directed graphs, DFS, finish times / discovery times; adjacency lists

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

An SCC is a maximal set where every pair is mutually reachable. Collapsing each SCC to a supernode yields a **DAG** — cycles are “noise” inside components; the interesting global structure is the condensation.

**Kosaraju:** DFS finish order on \(G\) is a linear extension related to the reverse of the condensation topo order. The **transpose** \(G^T\) has the same SCCs. Processing nodes in decreasing finish time and DFS on \(G^T\) peels off one SCC at a time (sources in the reverse condensation become sinks in \(G^T\)).

**Tarjan:** One DFS maintains discovery time `disc`, low-link `low` (earliest discovered vertex reachable via tree edges + one back/cross edge into the stack), and an explicit stack of the current path’s “active” vertices. When `low[v] == disc[v]`, `v` is the root of an SCC — pop until `v`.

---

## 4. Proof Sketches & Recurrences

Let \(C_1,\ldots,C_k\) be SCCs. Condensation edges \(C_i \to C_j\) (\(i\neq j\)) form a DAG (a cycle would merge components).

**Kosaraju correctness sketch:** The first node popped in decreasing finish order belongs to a source SCC of the condensation of \(G^T\) (equivalently a sink of \(G\)’s condensation). DFS on \(G^T\) from that node reaches exactly its SCC. Remove and repeat.

**Tarjan:** `low[v] = min(disc[v], disc[u]` for back-edges to stack vertices, `low[u]` for tree children). If a child has `low[child] >= disc[v]` that does **not** mean articulation here — for SCC, the pop condition is solely `low[v]==disc[v]`. Cross-edges to already-assigned nodes are ignored.

**Complexity:** Both \(O(n+m)\). Kosaraju: two DFS + transpose build. Tarjan: one DFS.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\) build / transpose
- Per-query / per-operation: \(O(1)\) component id after run
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- “Mutually reachable,” “cycle of dependencies,” “can return to start”
- “Minimum edges to make the digraph strongly connected”
- Constraints that look like 2-SAT (implication cycles)
- “Condensation is a chain / has unique source”
- Need component id then DP on the DAG of components

---

## 7. Contest WA / TLE / RE Traps

- Forgetting transpose edges (Kosaraju) → wrong components
- Processing finish order **ascending** instead of descending
- Tarjan: updating `low` from nodes **not on stack** (cross to finished SCC) → merges distinct SCCs
- 1-index vs 0-index mismatch; isolated vertices must still get a component
- Recursion depth on a long path (\(n=10^6\)) → use iterative Kosaraju
- Multiple edges / self-loops: self-loop does not split SCC; fine to keep

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

- **Component graph construction:** see Condensation DAG (§3)
- **Largest SCC / count SCCs:** trivial post-process on `ids`
- **Edge SCCs / bridge-block tree:** different (undirected); use bridges (§2)
- **Incremental SCC:** hard online; usually offline rebuild or special structure — not this template

---

## 11. Typical Problem Archetypes

1. Standard application: label SCCs; print size of largest
2. Slightly disguised: “can A reach B and B reach A?” → same component
3. Difficult: minimum edges to make strongly connected (use condensation in/out degrees)
4. Very difficult / advanced: 2-SAT + optimization over condensation; or SCC of implication of a constructed graph

---

## 12. Recognition & Identification Drills

1. Directed graph; for each vertex output the size of its strong component.
2. You may add edges; minimize additions so the digraph becomes strongly connected (or report impossible).
3. Cities with one-way roads; tourists want a tour that can revisit via mutual reachability clusters — count clusters with no outgoing road to another cluster.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: mutual reachability / collapse cycles in digraphs
- Key invariant: condensation of SCCs is a DAG
- Key formula: Kosaraju = DFS order on \(G\) + DFS on \(G^T\); Tarjan: pop when `low==disc`
- Complexity: \(O(n+m)\)
- Template to remember: finish-order peel (Kosaraju) or stack+lowlink (Tarjan)

---

---
