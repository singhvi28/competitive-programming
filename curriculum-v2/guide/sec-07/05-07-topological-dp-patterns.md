# Topological-DP patterns

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** DAG / condensation, memoized DP or topo iteration; shortest/longest paths on DAG  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: DAG / condensation, memoized DP or topo iteration; shortest/longest paths on DAG

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

On a DAG (or after condensation), every DP state can finalize when all incoming predecessors are done — **Kahn / reverse-topo loops** replace recursion. Patterns: longest path, min/max cost to reach, count paths, AND/OR game DP, knapsack along topo, DP on labeled DAGs from SCC.

If the original graph has cycles but DP “takes max over a walk,” either the answer is unbounded (positive cycle) or you must **collapse SCCs** and DP on the DAG with aggregated node weights.

---

## 4. Proof Sketches & Recurrences

Let topo order be \(v_1,\ldots,v_n\). For longest path with node weight \(w\):
\[
\mathrm{dp}[v]=w[v]+\max_{u\to v}\mathrm{dp}[u]\quad(\max\emptyset=0\text{ if sources allowed empty pred})
\]
Or edge weights: \(\mathrm{dp}[v]=\max_{u\to v}(\mathrm{dp}[u]+w(u,v))\).

Count paths to \(t\): \(\mathrm{dp}[t]=1\); process reverse topo: \(\mathrm{dp}[u]=\sum_{u\to v}\mathrm{dp}[v]\).

**With cycles:** if seeking finite simple-path optimum under additive scores and cycles can be used to inflate, detect positive cycle in relevant part; else SCC-aggregate then DAG DP.

Complexity \(O(n+m)\) per DP layer.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: topo \(O(n+m)\)
- Per-query / per-operation: usually one linear DP
- Total: \(O(n+m)\) (or \(O(k+e)\) on condensation)
- Memory: \(O(n+m)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Explicit DAG / dependency graph / course prerequisites
- Digraph + “maximum score along a path”
- After SCC: “value of a component is sum; edges between”
- Counting ways to reach sink; probability on DAG
- Game on DAG: win/lose/grundy from sinks upward

---

## 7. Contest WA / TLE / RE Traps

- Running DP on a graph that still has cycles → infinite loop in Kahn or wrong recursion
- Initializing only sources when paths may start anywhere (or the opposite)
- Double-counting node weight at both ends of an edge relaxation
- Modulo bugs when counting paths; forgetting unreachable zeros
- After SCC: adding component weight on every edge relaxation incorrectly (add once at node)

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

- **Shortest path on DAG:** same but `min` and careful \(+\infty\) init
- **Knapsack on DAG:** state `(node, budget)` processed in topo — \(O((n+m)W)\)
- **Bitwise OR / idempotent merges:** DP values are sets/bitsets along topo
- **Labeled transitions:** matrix product along paths — combine with adjacency

---

## 11. Typical Problem Archetypes

1. Standard application: longest path in a DAG
2. Slightly disguised: project dependencies with profits; max profit chain
3. Difficult: DP on condensation with large aggregated weights; count paths mod \(p\)
4. Very difficult / advanced: DP on DAG of SCCs + secondary constraints (bitset reachability filters)

---

## 12. Recognition & Identification Drills

1. Directed acyclic task graph; each task has duration; longest chain of tasks.
2. City network with one-way streets forming cycles; maximize sum of attractions on a route without using a positive-score cycle forever — collapse first.
3. Count modulo \(10^9+7\) the number of paths from sources to a given sink in a DAG.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: dependencies / digraph DP after making acyclic
- Key invariant: process in topological order
- Key formula: \(\mathrm{dp}[v]=\mathrm{agg}_{u\to v}(\mathrm{dp}[u])\oplus w[v]\)
- Complexity: \(O(n+m)\)
- Template to remember: Kahn topo + relax; SCC then DP if cycles

---

[Back to Section 07 index](07-graph-algorithms-advanced.md) · [Part B](07-b-dsu-rollback-offline.md)

---

---
