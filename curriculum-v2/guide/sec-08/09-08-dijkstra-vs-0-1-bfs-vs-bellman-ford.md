# Dijkstra vs 0-1 BFS vs Bellman–Ford

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2100
- Prerequisites: Graph representations, Priority Queues, Deque, BFS
- Tradeoff: Choosing the strictly minimal complexity tool based on edge weights prevents TLE/MLE.

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

The decision matrix for single-source shortest path is dictated strictly by edge weight distribution: Unit weights $w \in \{1\} \implies$ Standard Queue BFS in $\mathcal{O}(V + E)$. Binary weights $w \in \{0, k\} \implies$ 0-1 BFS with `std::deque` in $\mathcal{O}(V + E)$ by pushing 0-cost transitions to the front and $k$-cost to the back. General non-negative weights $w \ge 0 \implies$ Dijkstra with `std::priority_queue` in $\mathcal{O}((V + E) \log V)$. Arbitrary weights with negative cycles or cycle detection $\implies$ Bellman-Ford in $\mathcal{O}(V \cdot E)$.

---

## 4. Proof Sketches & Recurrences

Dijkstra's greedy choice holds because edge weights are non-negative ($w(u, v) \ge 0$), guaranteeing monotonic distance expansions along shortest paths: $d(u) \le d(v)$ for all explored vertices. 0-1 BFS maintains the invariant that the deque contains distances spanning at most $\{d, d + 1\}$, preserving the monotonic priority queue property in $\mathcal{O}(1)$ amortized time per pop. Bellman-Ford performs dynamic programming over path length: after $k$ relaxation passes over all $E$ edges, $dist[v]$ equals the length of the shortest path from source to $v$ containing at most $k$ edges.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Decision Matrix Dispatcher: 0-1 BFS vs Dijkstra
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

// 0-1 BFS: weights in {0, 1}, runs in O(V + E)
vector<ll> bfs_01(int n, int src, const vector<vector<pair<int, int>>>& adj) {
    vector<ll> dist(n + 1, INF);
    deque<int> dq;
    dist[src] = 0; dq.push_back(src);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto& [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    return dist;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Graph grid movements where turning or changing state costs 1 and moving straight costs 0 (reach for 0-1 BFS).
- Continuous state costs with non-negative arbitrary weights (reach for Dijkstra).
- Negative edge weights with at most $K$ step limits or currency arbitrage exchange rates (reach for Bellman-Ford).
- Dynamic graphs where distances wrap around modulo $M$ (reach for Dijkstra on residue classes / Dijkstra on modulo graph).

---

## 7. Contest WA / TLE / RE Traps

- Using 0-1 BFS when edge weights are in $\{0, 1, 2\}$; the deque distance invariant breaks down, leading to suboptimal distances.
- Using Dijkstra on graphs with negative edge weights; Dijkstra fails to re-evaluate finalized nodes and produces wrong answers.
- Forgetting to check the stale queue state `if (d > dist[u]) continue;` in Dijkstra, causing memory/time blowup.
- Running Bellman-Ford for exactly $V-1$ iterations without an early-break flag when no relaxations occur, wasting CPU time.

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
