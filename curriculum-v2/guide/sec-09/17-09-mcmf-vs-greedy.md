# 17. MCMF vs Greedy

> **Section:** §09 Network Flow & Matchings  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Min-Cost Max-Flow (MCMF), Slope Trick, Priority Queue / Regret Greedy
- Tradeoff: MCMF guarantees global optimality on complex network topologies but is $\mathcal{O}(F \cdot E \log V)$; Greedy with regret (simulated network flow) runs in $\mathcal{O}(N \log N)$ on linear or tree topologies.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Network Flow models capacity and assignment problems through directed residual graphs. Key frameworks include Dinic's Blocking Flow Algorithm, the Max-Flow Min-Cut Theorem, Bipartite Matching, and Min-Cost Max-Flow (MCMF).

### Fundamental Theorems & Invariants

- **Max-Flow Min-Cut Theorem:** The maximum value of an $(s, t)$-flow equals the minimum capacity of an $(s, t)$-cut $(S, T)$ separating source $s$ and sink $t$.
- **Dinic's Algorithm Complexity:** By decomposing the residual network into a layered graph via BFS and finding blocking flows via DFS with current-arc optimization, Dinic runs in $\mathcal{O}(V^2 E)$ on general networks and $\mathcal{O}(E \sqrt{V})$ on unit networks.
- **König's Theorem:** In any bipartite graph, the size of the Maximum Matching equals the size of the Minimum Vertex Cover.
- **Project Selection Closure:** Given items with profit/loss values $w_i$ and dependency implications $i \to j$, optimal subset profit equals $\sum_{w_i > 0} w_i - \text{MinCut}(s, t)$ where $s \to i$ has capacity $w_i$, $j \to t$ has capacity $-w_j$, and dependencies have capacity $\infty$.

### Algorithmic Execution Blueprint

1. **Layered Graph BFS:** Compute shortest distance $level[u]$ from source $s$ using available residual capacities ($cap[e] - flow[e] > 0$). If $level[t] == -1$, terminate.
2. **Blocking Flow DFS:** Push flow along edges satisfying $level[v] == level[u] + 1$, maintaining `head[u]` to avoid re-examining saturated edges.
3. **Min-Cut Extraction:** After max flow terminates, all vertices reachable from $s$ in the residual graph form $S$. Cut edges are all original edges from $S$ to $T$.

### Closed-Form Invariant Equations

$$\text{MaxFlow}(s, t) = \min_{S \cup T = V, \, s \in S, \, t \in T} \sum_{u \in S, v \in T} C(u, v), \quad \text{MaxProfit} = \sum_{w_i > 0} w_i - \text{MinCut}$$

### Structural Edge Cases & Assumptions

- Always add reverse edges with capacity 0 (or capacity $C$ for undirected graphs) in the adjacency list.
- In Min-Cost Max-Flow, negative cost cycles require Johnson potential transformations or Bellman-Ford initialization to prevent infinite cycling.
- Vertex capacities must be modeled by splitting each vertex $v$ into $v_{in}$ and $v_{out}$ connected by a directed edge with capacity $C(v)$.

---

## 3. Core Intuition & Problem Framing

MCMF and greedy are two ends of convex optimization. When the underlying graph is a 1D sequence (e.g., buy/sell stock with transaction fees, pairing parentheses, matching intervals on a line), the min-cost flow problem exhibits total unimodularity and convexity. Instead of running a general graph MCMF algorithm, you can 'simulate' the augmenting paths of MCMF using two priority queues (Slope Trick / Regret Greedy). If the topology is an arbitrary graph or bipartite with irregular edges, general MCMF is required.

---

## 4. Proof Sketches & Recurrences

The cost of sending $k$ units of flow $f(k)$ is piecewise linear and strictly convex: $f(k+1) - f(k) \ge f(k) - f(k-1)$ due to shortest augmenting path potentials. In 1D interval problems, the dual problem is equivalent to optimizing a convex function under slope changes. A priority queue tracks potential slopes, and choosing an element corresponds to augmenting flow; pushing the negative back into the queue allows the algorithm to 'cancel' or 'regret' an earlier choice along a residual backward edge in $\mathcal{O}(\log N)$ time.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Simulated Network Flow / Regret Greedy (Slope Trick) in O(N log N)
// Example: Buy and Sell Stock with Regret
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll simulated_mcmf_buy_sell(const vector<ll>& prices) {
    priority_queue<ll, vector<ll>, greater<ll>> pq;
    ll total_profit = 0;
    for (ll p : prices) {
        if (!pq.empty() && pq.top() < p) {
            total_profit += p - pq.top();
            pq.pop();
            pq.push(p); // Can regret selling here if a higher future price exists
        }
        pq.push(p); // Option to buy at current price
    }
    return total_profit;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Problem asks for min-cost matching of points on a line or timestamps in a schedule ($N \approx 2 \times 10^5$, MCMF would TLE).
- Arbitrary bipartite graph where left side wants to match right side with minimum total cost ($N \le 500$, reach for MCMF).
- Convex cost functions on edge flows (piecewise linear cost).
- Workload distribution where previous decisions can be revoked if a more profitable option arrives.

---

## 7. Contest WA / TLE / RE Traps

- Attempting MCMF with $N = 10^5$; standard MCMF will heavily TLE (needs $\mathcal{O}(N \log N)$ simulated flow).
- In simulated flow, forgetting the regret element: failing to push the new state back into the priority queue prevents cancellation.
- Handling negative cycles in general MCMF without proper initial potentials or Bellman-Ford/SPFA initialization.
- Using floating-point costs without epsilon checks in MCMF.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1082G | Petya and Graph | 2300 | Min Cut, Dinic, Project Selection | Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut. | [Solve Problem](https://codeforces.com/contest/1082/problem/G) |
| Codeforces | CF-1404E | Bricks | 2600 | Bipartite Matching, Min Cut, Dinic | Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds. | [Solve Problem](https://codeforces.com/contest/1404/problem/E) |
| Codeforces | CF-277E | Binary Tree on Plane | 2400 | MCMF, Network Flow, Geometry | Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance. | [Solve Problem](https://codeforces.com/contest/277/problem/E) |
| CSES | CSES-1695 | Police Chase | 1900 | Dinic, Min Cut, Graphs | Find min-cut edges after running Dinic's max flow from source to sink. | [Solve Problem](https://cses.fi/problemset/task/1695) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Dinic's Algorithm for Maximum Flow](https://cp-algorithms.com/graph/dinic.html)
- **[CP-Algorithms]** [CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)](https://cp-algorithms.com/graph/min_cost_flow.html)
- **[USACO Guide]** [USACO Guide: Min-Cut Modeling & Project Selection](https://usaco.guide/adv/max-flow)

---
