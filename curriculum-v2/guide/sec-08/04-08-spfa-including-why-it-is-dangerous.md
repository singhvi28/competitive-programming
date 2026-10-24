# SPFA (Including Why It Is Dangerous)

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 1600–2200 (avoid) | **Frequency:** Rare (as a *good* choice); historically overused  
> **Prerequisites:** Bellman–Ford, queues  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare (as a *good* choice); historically overused
- Typical CF/ICPC rating range: 1600–2200 (avoid)
- Prerequisites: Bellman–Ford, queues

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

SPFA only relaxes edges out of nodes whose distance improved, using a queue (or SLF/LLL heuristics). On “random” graphs it can look like \(O(m)\)–\(O(m\log n)\), which is why it feels attractive. On crafted graphs (grids with special weights, long decreasing chains with re-queueing), it degenerates to **exponential / \(\Theta(nm)\)** behavior and **TLEs under CF time limits** while Dijkstra or BF with early break passes. Modern meta: **SPFA is rarely worth using in contests.**

---

## 4. Proof Sketches & Recurrences

Still Bellman–Ford; worst-case every round can reinsert many vertices. SLF (Small Label First) / LLL heuristics try to reduce average case but **do not fix adversarial TLE**. Correctness ≠ good complexity. Negative cycle detection via “pop count > n” is fragile under TLE (may not finish).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: average “often fine,” **worst \(\Theta(nm)\) or worse in practice**
- Total: unreliable
- Memory: \(O(n+m)\)`

### C++17 Template

```cpp
// Educational / legacy only — prefer Dijkstra or Bellman-Ford in contests.
namespace spfa {
using ll = long long;
const ll INF = 4e18;

// returns false if neg cycle detected by pop-count heuristic
bool shortest(int n, int src,
              const vector<vector<pair<int, ll>>>& g,
              vector<ll>& dist) {
    dist.assign(n, INF);
    vector<char> inq(n, 0);
    vector<int> cnt(n, 0);
    queue<int> q;
    dist[src] = 0;
    q.push(src);
    inq[src] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        inq[u] = 0;
        for (auto [v, w] : g[u]) {
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                if (!inq[v]) {
                    q.push(v);
                    inq[v] = 1;
                    if (++cnt[v] > n) return false; // neg cycle heuristic
                }
            }
        }
    }
    return true;
}
} // namespace spfa
```

---

## 6. Recognition Trigger Signals & Heuristics

- Legacy tutorials say “use SPFA for negatives”
- Someone’s code has `inqueue[]` + `while (queue)`
- Anti-SPFA comment in editorial — if you used SPFA, expect pain
- **Recognition for you:** if you reach for SPFA, stop and pick Dijkstra (nonneg) or Bellman–Ford (neg)

---

## 7. Contest WA / TLE / RE Traps

- **Contest bug:** choosing SPFA → TLE on anti-tests
- Trusting “cnt > n” while still TLE before detection
- Using SPFA on nonnegative graphs instead of Dijkstra
- SLF/LLL still failing on CF

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

- SLF: push_front if `dist[v] < dist[front]`
- LLL: large label last
- None of these make SPFA a good default — document only

---

## 11. Typical Problem Archetypes

1. Standard application: none recommended on modern CF
2. Slightly disguised: MCMF codes that embed SPFA for potentials — prefer Dijkstra with potentials
3. Difficult: passing anti-SPFA tests (rewrite to Dijkstra / Bellman–Ford)
4. Very difficult / advanced: understanding adversarial graphs for complexity literacy

---

## 12. Recognition & Identification Drills

1. You have nonnegative weights and wrote SPFA — what should you rewrite?
2. Negatives, \(n=1000\), \(m=5000\) — BF or SPFA?
3. Editorial says “anti-SPFA” — which algorithms are safe?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: **almost never** in contests
- Key invariant: same as BF, but scheduling is hostile
- Key formula: queue of improved vertices
- Complexity: unreliable worst case
- Template to remember: “replace SPFA with Dijkstra/BF”

---

---
