# Section §08: Advanced Graphs (Shortest Paths, MST, Euler)

> **Module ID:** `sec-08`  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Topic Count:** 19  

**Module Summary:** Dijkstra variants, 0-1 BFS, Floyd-Warshall, DAG paths, Functional graphs, Kruskal reconstruction tree, and Eulerian path construction.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Dijkstra Variants](#topic-1) | `S-tier` | 1400–2100 (variants to 2500+) | Very Common | [01-08-dijkstra-variants.md](./01-08-dijkstra-variants.md) |
| 2 | [0-1 BFS](#topic-2) | `A-tier` | 1500–2100 | Common | [02-08-0-1-bfs.md](./02-08-0-1-bfs.md) |
| 3 | [Bellman–Ford](#topic-3) | `A-tier` | 1500–2100 | Occasional | [03-08-bellman-ford.md](./03-08-bellman-ford.md) |
| 4 | [SPFA (Including Why It Is Dangerous)](#topic-4) | `C-tier` | 1600–2200 (avoid) | Rare (as a *good* choice); historically overused | [04-08-spfa-including-why-it-is-dangerous.md](./04-08-spfa-including-why-it-is-dangerous.md) |
| 5 | [Floyd–Warshall](#topic-5) | `A-tier` | 1400–2000 | Common | [05-08-floyd-warshall.md](./05-08-floyd-warshall.md) |
| 6 | [DAG Shortest Paths](#topic-6) | `A-tier` | 1500–2000 | Common | [06-08-dag-shortest-paths.md](./06-08-dag-shortest-paths.md) |
| 7 | [Multi-Source Shortest Paths](#topic-7) | `A-tier` | 1500–2100 | Common | [07-08-multi-source-shortest-paths.md](./07-08-multi-source-shortest-paths.md) |
| 8 | [Johnson’s Algorithm](#topic-8) | `C-tier` | 2200–2700 | Rare | [08-08-johnson-s-algorithm.md](./08-08-johnson-s-algorithm.md) |
| 9 | [Dijkstra vs 0-1 BFS vs Bellman–Ford](#topic-9) | `B-tier` | 1600–2200 | Common | [09-08-dijkstra-vs-0-1-bfs-vs-bellman-ford.md](./09-08-dijkstra-vs-0-1-bfs-vs-bellman-ford.md) |
| 10 | [Why SPFA Is Dangerous](#topic-10) | `B-tier` | 1600–2200 | Common | [10-08-why-spfa-is-dangerous.md](./10-08-why-spfa-is-dangerous.md) |
| 11 | [Kruskal Reconstruction vs HLD for Path Max](#topic-11) | `B-tier` | 1600–2200 | Common | [11-08-kruskal-reconstruction-vs-hld-for-path-max.md](./11-08-kruskal-reconstruction-vs-hld-for-path-max.md) |
| 12 | [Borůvka Niche](#topic-12) | `B-tier` | 1600–2200 | Common | [12-08-bor-vka-niche.md](./12-08-bor-vka-niche.md) |
| 13 | [Part A — [08-a-shortest-paths.md](08-a-shortest-paths.md)](#topic-13) | `B-tier` | 1600–2200 | Common | [13-08-part-a-08-a-shortest-paths-md-08-a-shortest-paths-md.md](./13-08-part-a-08-a-shortest-paths-md-08-a-shortest-paths-md.md) |
| 14 | [Part B — [08-b-mst-euler-functional.md](08-b-mst-euler-functional.md)](#topic-14) | `B-tier` | 1600–2200 | Common | [14-08-part-b-08-b-mst-euler-functional-md-08-b-mst-euler-functional-md.md](./14-08-part-b-08-b-mst-euler-functional-md-08-b-mst-euler-functional-md.md) |
| 15 | [Minimum Spanning Tree Variants](#topic-15) | `A-tier` | 1400–2200 | Common | [15-08-minimum-spanning-tree-variants.md](./15-08-minimum-spanning-tree-variants.md) |
| 16 | [Kruskal Reconstruction Tree](#topic-16) | `B-tier` | 2100–2700 | Occasional | [16-08-kruskal-reconstruction-tree.md](./16-08-kruskal-reconstruction-tree.md) |
| 17 | [Borůvka](#topic-17) | `C-tier` | 2000–2600 | Rare | [17-08-bor-vka.md](./17-08-bor-vka.md) |
| 18 | [Eulerian Paths / Circuits](#topic-18) | `A-tier` | 1700–2300 | Occasional | [18-08-eulerian-paths-circuits.md](./18-08-eulerian-paths-circuits.md) |
| 19 | [Functional Graphs](#topic-19) | `A-tier` | 1600–2200 | Common | [19-08-functional-graphs.md](./19-08-functional-graphs.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Dijkstra Variants

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2100 (variants to 2500+) | **Frequency:** Very Common  
> **Prerequisites:** Graphs, binary heaps / `priority_queue`, adjacency lists  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2100 (variants to 2500+)
- Prerequisites: Graphs, binary heaps / `priority_queue`, adjacency lists

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Dijkstra grows a set of vertices whose **final** distance is known, always extending from the unsettled vertex with smallest tentative distance. With nonnegative weights, the first time you pop a node from the min-heap (lazy version: first time you pop with `d == dist[u]`), that distance is optimal—no future path can undercut it without a negative edge. Contest power is not the heap: it is **modeling**—extra state in the node, edge weights as costs of decisions, and “implicit graphs” (grids, digit DP graphs, product graphs).

---

#### 4. Proof Sketches & Recurrences

Lazy binary-heap Dijkstra: each edge may push a new pair → \(O(m\log m)\) pushes, \(O((n+m)\log n)\) typical bound. Correctness: induction on pop order; nonnegative edges ⇒ no decrease of a finalized distance. Dial’s algorithm / radix ideas exist for small integer weights but rarely needed vs 0-1 BFS + Dijkstra.

Potential/`h(u)` (Johnson): run Dijkstra on reduced costs \(w'(u,v)=w(u,v)+h(u)-h(v)\ge 0\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(n+m)\)
- Per-query / per-operation: one source \(O((n+m)\log n)\) binary heap
- Total: as above; \(k\) sources without multi-source trick: \(\times k\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace dijkstra {
using ll = long long;
const ll INF = 4e18;

vector<ll> shortest(int n, int src,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue; // lazy deletion
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// Optional: recover parents
vector<ll> shortest_parent(int n, int src,
                           const vector<vector<pair<int, ll>>>& g,
                           vector<int>& par) {
    vector<ll> dist(n, INF);
    par.assign(n, -1);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                par[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
} // namespace dijkstra
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Minimum cost / time / fuel” with nonnegative costs
- Graph is explicit or product of (position × resource)
- Not unweighted (else BFS); not 0/1-only (else 0-1 BFS); not DAG-only (else topo)
- You need single-source or few sources, not dense all-pairs

---

#### 7. Contest WA / TLE / RE Traps

- Using Dijkstra with **negative** edges (silent WA)
- Forgetting `if (d != dist[u]) continue` → TLE from stale heap entries
- `int` overflow on `dist[u] + w` — use `long long`, cap INF carefully (`INF + w` must not wrap)
- 1-index vs 0-index; bidirectional edges added once by mistake
- Early exit only valid if you need one target and pop that target with final dist

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **K shortest / count paths:** extra state or A* carefully; counting: DP on DAG of shortest-path edges
- **Dijkstra on state graph:** node id = `u * (S+1) + s`
- **Dense graphs:** \(O(n^2)\) classic Dijkstra (no heap) when \(m\sim n^2\)
- **Prim = Dijkstra on “dist to tree”** for MST
- **Potentials** for MCMF / Johnson

---

#### 11. Typical Problem Archetypes

1. Standard application: single-source distances on weighted undirected/directed graph
2. Slightly disguised: grid with cell costs; compress to graph
3. Difficult: state expansion (fuel, discounts, parity of edges)
4. Very difficult / advanced: optimizing over choices via potentials / nested Dijkstra in flow

---

#### 12. Recognition & Identification Drills

1. Cities and flights with nonnegative costs; minimize cost from capital to all cities.
2. You may use one “coupon” that halves one edge; minimize path cost.
3. Graph edges have length; you walk at speed 1 but can teleport with cooldown — minimize time.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: nonnegative weights, single-/few-source
- Key invariant: popped distance is final
- Key formula: `dist[v] = min(dist[v], dist[u] + w(u,v))` with heap order
- Complexity: \(O((n+m)\log n)\)
- Template to remember: lazy PQ + `d != dist[u]` skip

---

---


---

<a id="topic-2"></a>
### 2. 0-1 BFS

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Common  
> **Prerequisites:** Deque, BFS, shortest paths intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Deque, BFS, shortest paths intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

When every edge weight is 0 or 1, Dijkstra’s “closest first” rule becomes: append 1-edges to the **back** of a deque and 0-edges to the **front**. The deque stays monotonic in distance; each node is processed like 0-1 Dial with buckets of size 1. Same correctness as Dijkstra, linear time.

---

#### 4. Proof Sketches & Recurrences

Reduced costs are 0/1 ⇒ only two buckets needed. Push_front for 0 preserves “smaller or equal distance first.” Each edge examined once if you mark carefully; standard safe pattern still allows multiple queue entries but \(O(n+m)\) with `if (nd > dist[v]) continue` before push and update-on-improve. Classic: each node entered deque \(O(1)\) times if you only push when strictly improving and use visited-on-pop for 0-1 — use the improve-and-push template below (simple, \(O(n+m)\)).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: \(O(n+m)\)
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace zero_one_bfs {
using ll = long long;
const ll INF = 4e18;

vector<ll> shortest(int n, int src,
                    const vector<vector<pair<int, int>>>& g) {
    // edge weight must be 0 or 1
    vector<ll> dist(n, INF);
    deque<int> dq;
    dist[src] = 0;
    dq.push_back(src);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        for (auto [v, w] : g[u]) {
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    return dist;
}
} // namespace zero_one_bfs
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Edge costs only 0 and 1 (or “free vs cost 1”)
- Grid: move to neighbor cost 1, “stay in component” / open door cost 0
- Building walls vs walking; changing direction costs 1
- You almost wrote Dijkstra but weights are boolean

---

#### 7. Contest WA / TLE / RE Traps

- Using `priority_queue` unnecessarily (AC but slower; wrong habit)
- Weights not actually 0/1 (WA) — if weights are 0 and \(x\), scale or use Dijkstra
- `push_front`/`push_back` swapped
- Treating as unweighted BFS (ignoring 0-edges’ “free” progress)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Two weights \(a < b\):** can map to more buckets (Dial) or stick with Dijkstra
- **0/k BFS:** still deque if carefully generalized; often Dijkstra simpler
- Multi-source 0-1 BFS: seed all sources at dist 0

---

#### 11. Typical Problem Archetypes

1. Standard application: graph with edges type A (cost 0) and B (cost 1)
2. Slightly disguised: minimum changes of direction on a grid
3. Difficult: 0-1 on implicit state graph
4. Very difficult / advanced: combine with binary search on threshold → edges become 0/1

---

#### 12. Recognition & Identification Drills

1. Grid; moving straight is free continuation, turning costs 1 — min turns to target.
2. Edges are portals (cost 0) or roads (cost 1).
3. Binary search on max edge used; check connectivity with 0-1 costs “above/below.”

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: weights ∈ {0,1}
- Key invariant: deque sorted by nondecreasing distance
- Key formula: 0 → front, 1 → back
- Complexity: \(O(n+m)\)
- Template to remember: `deque` + improve-and-push

---

---


---

<a id="topic-3"></a>
### 3. Bellman–Ford

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Occasional  
> **Prerequisites:** Edge list, relaxation, negative weights  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Edge list, relaxation, negative weights

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Relax **all** edges up to \(n-1\) times; if a shortest path is simple, it has \(\le n-1\) edges, so \(n-1\) rounds suffice. A successful relaxation on round \(n\) means a negative cycle is reachable from the source (or from the virtual super-source if you initialize all `dist=0` for “any cycle”). This is the trustworthy negative-weight algorithm when you do not need Dijkstra’s assumptions.

---

#### 4. Proof Sketches & Recurrences

After \(k\) rounds, `dist[v]` equals shortest path using \(\le k\) edges (if no neg cycle). Neg cycle ⇒ unbounded decrease along a walk. Difference constraints satisfiable iff no negative cycle in the constraint graph.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: edge list \(O(m)\)
- Per-query / per-operation: \(O(nm)\)
- Total: \(O(nm)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace bellman_ford {
using ll = long long;
const ll INF = 4e18;

struct Edge { int u, v; ll w; };

// returns false if negative cycle reachable from src
bool shortest(int n, int src, const vector<Edge>& edges,
              vector<ll>& dist) {
    dist.assign(n, INF);
    dist[src] = 0;
    for (int it = 0; it < n - 1; ++it) {
        bool any = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] == INF) continue;
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                any = true;
            }
        }
        if (!any) break;
    }
    for (auto [u, v, w] : edges) {
        if (dist[u] == INF) continue;
        if (dist[v] > dist[u] + w) return false; // neg cycle reachable
    }
    return true;
}

// Mark nodes that can be improved via neg cycle (optional)
void mark_neg_reachable(int n, const vector<Edge>& edges,
                        vector<ll>& dist, vector<char>& bad) {
    bad.assign(n, 0);
    for (int it = 0; it < n; ++it) {
        for (auto [u, v, w] : edges) {
            if (dist[u] == INF) continue;
            if (dist[v] > dist[u] + w) {
                dist[v] = max(-INF / 4, dist[u] + w); // avoid wild overflow
                bad[v] = 1;
            }
            if (bad[u]) bad[v] = 1;
        }
    }
}
} // namespace bellman_ford
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Explicit negative edges or “gain” that decreases cost
- Detect arbitrage / negative cycle
- Difference constraints: \(x_v - x_u \le w\) → edge \(u\to v\) weight \(w\)
- \(n,m\) small enough for \(O(nm)\) (\(nm \lesssim 10^7\)–\(10^8\))

---

#### 7. Contest WA / TLE / RE Traps

- Relaxing when `dist[u]==INF` (creating fake paths)
- Overflow: `INF + w` — skip or use saturated arithmetic
- Detecting a neg cycle that is **not** reachable from `src` (still “exists” if you init all zeros)
- Off-by-one: only \(n-2\) rounds
- Printing cycle without parent pointers / DFS on improving edges

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Shortest path with ≤K edges:** exactly \(K\) rounds (or DP `dist[k][v]`)
- **Difference constraints system**
- **SPFA:** queue variant — see next (avoid)
- Initialize all `dist=0` to find any neg cycle in the graph

---

#### 11. Typical Problem Archetypes

1. Standard application: shortest paths with negatives
2. Slightly disguised: currency exchange / arbitrage
3. Difficult: recover a negative cycle vertices
4. Very difficult / advanced: difference constraints + binary search on answer

---

#### 12. Recognition & Identification Drills

1. Directed graph with negative weights; detect if a neg cycle can reach node \(t\).
2. Variables with inequalities \(x_i - x_j \le c\); check feasibility.
3. Max score with possible loops that increase score forever.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: negatives or neg-cycle / difference constraints
- Key invariant: \(n-1\) relaxations finalize simple shortest paths
- Key formula: relax all edges; \(n\)th improve ⇒ neg cycle
- Complexity: \(O(nm)\)
- Template to remember: edge-list relax loop

---

---


---

<a id="topic-4"></a>
### 4. SPFA (Including Why It Is Dangerous)

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 1600–2200 (avoid) | **Frequency:** Rare (as a *good* choice); historically overused  
> **Prerequisites:** Bellman–Ford, queues  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare (as a *good* choice); historically overused
- Typical CF/ICPC rating range: 1600–2200 (avoid)
- Prerequisites: Bellman–Ford, queues

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

SPFA only relaxes edges out of nodes whose distance improved, using a queue (or SLF/LLL heuristics). On “random” graphs it can look like \(O(m)\)–\(O(m\log n)\), which is why it feels attractive. On crafted graphs (grids with special weights, long decreasing chains with re-queueing), it degenerates to **exponential / \(\Theta(nm)\)** behavior and **TLEs under CF time limits** while Dijkstra or BF with early break passes. Modern meta: **SPFA is rarely worth using in contests.**

---

#### 4. Proof Sketches & Recurrences

Still Bellman–Ford; worst-case every round can reinsert many vertices. SLF (Small Label First) / LLL heuristics try to reduce average case but **do not fix adversarial TLE**. Correctness ≠ good complexity. Negative cycle detection via “pop count > n” is fragile under TLE (may not finish).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: average “often fine,” **worst \(\Theta(nm)\) or worse in practice**
- Total: unreliable
- Memory: \(O(n+m)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Legacy tutorials say “use SPFA for negatives”
- Someone’s code has `inqueue[]` + `while (queue)`
- Anti-SPFA comment in editorial — if you used SPFA, expect pain
- **Recognition for you:** if you reach for SPFA, stop and pick Dijkstra (nonneg) or Bellman–Ford (neg)

---

#### 7. Contest WA / TLE / RE Traps

- **Contest bug:** choosing SPFA → TLE on anti-tests
- Trusting “cnt > n” while still TLE before detection
- Using SPFA on nonnegative graphs instead of Dijkstra
- SLF/LLL still failing on CF

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- SLF: push_front if `dist[v] < dist[front]`
- LLL: large label last
- None of these make SPFA a good default — document only

---

#### 11. Typical Problem Archetypes

1. Standard application: none recommended on modern CF
2. Slightly disguised: MCMF codes that embed SPFA for potentials — prefer Dijkstra with potentials
3. Difficult: passing anti-SPFA tests (rewrite to Dijkstra / Bellman–Ford)
4. Very difficult / advanced: understanding adversarial graphs for complexity literacy

---

#### 12. Recognition & Identification Drills

1. You have nonnegative weights and wrote SPFA — what should you rewrite?
2. Negatives, \(n=1000\), \(m=5000\) — BF or SPFA?
3. Editorial says “anti-SPFA” — which algorithms are safe?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: **almost never** in contests
- Key invariant: same as BF, but scheduling is hostile
- Key formula: queue of improved vertices
- Complexity: unreliable worst case
- Template to remember: “replace SPFA with Dijkstra/BF”

---

---


---

<a id="topic-5"></a>
### 5. Floyd–Warshall

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** DP on pairs, adjacency matrix  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: DP on pairs, adjacency matrix

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

`dp[k][i][j]` = shortest \(i\to j\) using intermediate nodes from \(\{1..k\}\). Rolling away \(k\) yields the classic triple loop. Dense all-pairs, easy negative-cycle check (`dist[i][i] < 0`), easy “add vertex/edge online” variants by running the same recurrence.

---

#### 4. Proof Sketches & Recurrences

\[
d_{ij}^{(k)} = \min\bigl(d_{ij}^{(k-1)},\, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\bigr)
\]
After \(k=n\), all simple intermediates allowed; neg cycle ⇒ some \(d_{ii}<0\). Semiring variants: replace \((\min,+)\) by \((\max,\min)\) for bottleneck, etc.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: matrix init \(O(n^2)\)
- Per-query / per-operation: after FW, \(O(1)\) pair query
- Total: \(O(n^3)\)
- Memory: \(O(n^2)\)`

##### C++17 Template

```cpp
namespace floyd {
using ll = long long;
const ll INF = 4e18;

void all_pairs(int n, vector<vector<ll>>& d) {
    // d[i][j] = w or INF; d[i][i] = 0
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            if (d[i][k] < INF)
                for (int j = 0; j < n; ++j)
                    if (d[k][j] < INF)
                        d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
}

bool has_neg_cycle(int n, const vector<vector<ll>>& d) {
    for (int i = 0; i < n; ++i)
        if (d[i][i] < 0) return true;
    return false;
}
} // namespace floyd
```

---

#### 6. Recognition Trigger Signals & Heuristics

- \(n \le 400\) (sometimes 500 if tight / bitset tricks)
- Need all-pairs or many pairs and graph dense
- Minimax / maximin path variants (change `min`/`max` algebra)
- Closure-like problems (reachability with OR-AND)

---

#### 7. Contest WA / TLE / RE Traps

- Not setting `d[i][i]=0`; missing undirected edges both ways
- Overflow on `d[i][k]+d[k][j]` — guard with INF checks
- \(n=500\) without constant-care → TLE
- Forgetting neg self-loop after FW means reachable neg cycle only if you care about that component

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Path reconstruction with `nxt[i][j]`
- **Offline add edges** from heavy to light / process reverse deletions
- Bottleneck: `d[i][j] = min(d[i][j], max(d[i][k], d[k][j]))`
- Transitive closure: boolean FW

---

#### 11. Typical Problem Archetypes

1. Standard application: all-pairs shortest paths, small \(n\)
2. Slightly disguised: min max-edge between all pairs (bottleneck FW)
3. Difficult: FW DP on “using first k cities as hubs”
4. Very difficult / advanced: combine with bitsets for reachability counts

---

#### 12. Recognition & Identification Drills

1. \(n=300\) directed graph; answer \(q=n^2\) distance queries.
2. Find if any negative cycle exists in a dense graph.
3. For each pair, minimum possible “worst edge” on a path.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: dense / small \(n\) all-pairs
- Key invariant: intermediates \(1..k\) processed
- Key formula: `d[i][j] = min(d[i][j], d[i][k]+d[k][j])`
- Complexity: \(O(n^3)\)
- Template to remember: `k,i,j` triple loop

---

---


---

<a id="topic-6"></a>
### 6. DAG Shortest Paths

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2000 | **Frequency:** Common  
> **Prerequisites:** Topological sort, DP on DAGs  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2000
- Prerequisites: Topological sort, DP on DAGs

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

On a DAG, process vertices in topo order; each edge relaxes forward once. Works with **negative weights** (no cycles at all). Same skeleton as longest path on DAG (flip to max). Many “DP on graph” problems are exactly this.

---

#### 4. Proof Sketches & Recurrences

Topo order ensures when you process \(u\), all incoming paths are finalized if you relax outgoing, or dually: relax edges when popping \(u\). \(O(n+m)\). Negatives fine; no need BF.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: topo \(O(n+m)\)
- Per-query / per-operation: \(O(n+m)\) after topo (or same pass)
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace dag_sp {
using ll = long long;
const ll INF = 4e18;

// g must be a DAG; returns dist from src (INF = unreachable)
vector<ll> shortest(int n, int src,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u)
        for (auto [v, w] : g[u]) indeg[v]++;
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (!indeg[i]) q.push(i);
    vector<int> order;
    order.reserve(n);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto [v, w] : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    vector<ll> dist(n, INF);
    dist[src] = 0;
    for (int u : order) {
        if (dist[u] == INF) continue;
        for (auto [v, w] : g[u])
            dist[v] = min(dist[v], dist[u] + w);
    }
    return dist;
}
} // namespace dag_sp
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Explicit DAG or SCC condensation
- Tasks with precedence constraints
- Longest path in project network
- Grid DP moving only right/down (implicit DAG)

---

#### 7. Contest WA / TLE / RE Traps

- Graph not actually DAG (need SCC first)
- Relaxing before topo readiness
- Longest path: forgetting to init reachable nodes to 0 / -INF correctly
- Multiple sources: init all sources to 0 then one topo pass

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Longest path: `max` and `-INF` init
- Count paths while relaxing
- DP on condensation DAG of SCCs
- Lexicographically shortest path via parent ties

---

#### 11. Typical Problem Archetypes

1. Standard application: shortest/longest path in DAG
2. Slightly disguised: nested segments / precedence
3. Difficult: DP on DAG with extra state
4. Very difficult / advanced: optimize DAG DP with CHT along topo

---

#### 12. Recognition & Identification Drills

1. Directed graph guaranteed acyclic; edge weights may be negative — shortest paths.
2. Maximum points collecting quests with prerequisites.
3. After SCC compression, path among components with weights.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: DAG (or condensation)
- Key invariant: topo order finalizes DP
- Key formula: relax in topo order
- Complexity: \(O(n+m)\)
- Template to remember: Kahn/DFS topo + one relax pass

---

---


---

<a id="topic-7"></a>
### 7. Multi-Source Shortest Paths

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Common  
> **Prerequisites:** BFS / Dijkstra  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: BFS / Dijkstra

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Distance to the **nearest** source is ordinary shortest path on a graph with a virtual super-source linked to all sources by weight-0 edges—or equivalently, seed the queue/heap with all sources at distance 0. One search replaces \(k\) searches when you only need `min over sources`.

---

#### 4. Proof Sketches & Recurrences

Super-source \(s^\*\) with edges \(s^\*\to s_i\) weight 0 ⇒ distances from \(s^\*\) equal min distance to any \(s_i\). Implementation: initialize `dist[s_i]=0` and push all.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n+m)\)
- Per-query / per-operation: same as BFS/Dijkstra once
- Total: \(O(n+m)\) or \(O((n+m)\log n)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace multisource {
using ll = long long;
const ll INF = 4e18;

vector<ll> dijkstra(int n, const vector<int>& sources,
                    const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    for (int s : sources) {
        if (dist[s] > 0) {
            dist[s] = 0;
            pq.push({0, s});
        }
    }
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

vector<int> bfs(int n, const vector<int>& sources,
                const vector<vector<int>>& g) {
    vector<int> dist(n, -1);
    queue<int> q;
    for (int s : sources) {
        if (dist[s] == -1) {
            dist[s] = 0;
            q.push(s);
        }
    }
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u])
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
    }
    return dist;
}
} // namespace multisource
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Nearest hospital / exit / enemy”
- Fire spread vs you moving (two multi-source BFS)
- Paint components from multiple seeds
- All sources same type; answer is min distance

---

#### 7. Contest WA / TLE / RE Traps

- Running \(k\) Dijkstras when one multi-source suffices
- Not handling duplicate sources
- Fire+player: wrong order of comparison (need fire time strictly `<` or `<=` carefully)
- Mixing directed edges incorrectly for “nearest”

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Multi-source 0-1 BFS
- Keep `nearest_source[v]` for reconstruction / coloring
- Binary search + multi-source check

---

#### 11. Typical Problem Archetypes

1. Standard application: distance to closest special vertex
2. Slightly disguised: infection / fire grids
3. Difficult: two competing multi-source spreads with different speeds
4. Very difficult / advanced: dynamic sources offline with DSU / timeline

---

#### 12. Recognition & Identification Drills

1. Multiple exits in a maze; min steps for each cell to an exit.
2. Fires start at several cells simultaneously; can you reach the gate?
3. Each special node paints its Voronoi cell under graph distance.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: min distance to any of a set
- Key invariant: virtual super-source weight 0
- Key formula: seed all sources at 0, one search
- Complexity: one BFS/Dijkstra
- Template to remember: push all sources first

---

---


---

<a id="topic-8"></a>
### 8. Johnson’s Algorithm

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2700 | **Frequency:** Rare  
> **Prerequisites:** Bellman–Ford, Dijkstra, potentials  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Bellman–Ford, Dijkstra, potentials

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

All-pairs on sparse graphs with negatives: compute potentials \(h(v)\) via Bellman–Ford from a super-source so reduced costs \(w'(u,v)=w(u,v)+h(u)-h(v)\) are nonnegative; then run Dijkstra from every vertex on \(w'\). True distance: \(d(u,v)=d'(u,v)-h(u)+h(v)\). Beats \(O(n^3)\) FW when \(m\) is sparse and \(n\) is too large for FW but \(n\) Dijkstra runs fit.

---

#### 4. Proof Sketches & Recurrences

Feasible potential: \(h(v)\le h(u)+w(u,v)\) ⇒ \(w'\ge 0\). Super-source edges of weight 0 into all nodes; BF gives \(h=\mathrm{dist}\) from super-source. Correctness of reduction is standard for MCMF potentials too.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: BF \(O(nm)\) for potentials
- Per-query / per-operation: after all-pairs matrix, \(O(1)\)
- Total: \(O(nm + n(n+m)\log n)\) with binary heaps
- Memory: \(O(n^2 + m)\) for full matrix`

##### C++17 Template

```cpp
namespace johnson {
using ll = long long;
const ll INF = 4e18;

struct Edge { int u, v; ll w; };

// dist[u][v] = shortest; returns false on neg cycle
bool all_pairs(int n, vector<Edge> edges, vector<vector<ll>>& dist) {
    // potentials via super-source n
    vector<Edge> e2 = edges;
    for (int v = 0; v < n; ++v) e2.push_back({n, v, 0});
    vector<ll> h(n + 1, INF);
    h[n] = 0;
    for (int it = 0; it < n; ++it) {
        bool any = false;
        for (auto [u, v, w] : e2) {
            if (h[u] == INF) continue;
            if (h[v] > h[u] + w) {
                h[v] = h[u] + w;
                any = true;
            }
        }
        if (!any) break;
    }
    for (auto [u, v, w] : e2) {
        if (h[u] == INF) continue;
        if (h[v] > h[u] + w) return false;
    }

    vector<vector<pair<int, ll>>> g(n);
    for (auto [u, v, w] : edges) {
        ll nw = w + h[u] - h[v];
        g[u].push_back({v, nw});
    }

    dist.assign(n, vector<ll>(n, INF));
    for (int s = 0; s < n; ++s) {
        vector<ll> d(n, INF);
        priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
        d[s] = 0;
        pq.push({0, s});
        while (!pq.empty()) {
            auto [dd, u] = pq.top();
            pq.pop();
            if (dd != d[u]) continue;
            for (auto [v, w] : g[u]) {
                if (d[v] > dd + w) {
                    d[v] = dd + w;
                    pq.push({d[v], v});
                }
            }
        }
        for (int v = 0; v < n; ++v)
            if (d[v] < INF) dist[s][v] = d[v] - h[s] + h[v];
    }
    return true;
}
} // namespace johnson
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Need all-pairs (or many pairs) + negative edges + sparse
- \(n\sim 10^3\), \(m\sim 10^4\) — FW too slow, \(n\) Dijkstras OK after reweight
- Almost never appears as a named requirement; usually FW or \(n\) Dijkstras (nonneg) suffice

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to re-translate distances with \(h\)
- Using Johnson when FW is simpler (\(n\le 400\))
- Neg cycle mishandled in potential phase
- Applying to undirected graphs with neg edges incorrectly (undirected neg edge is already a cycle)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Only need distances from few sources: skip full Johnson; BF per source or one BF if enough
- Same potential idea inside min-cost flow

---

#### 11. Typical Problem Archetypes

1. Standard application: all-pairs with negatives, sparse
2. Slightly disguised: reweight so Dijkstra works
3. Difficult: large sparse all-pairs with cycle reporting
4. Very difficult / advanced: shared potentials across multiple queries

---

#### 12. Recognition & Identification Drills

1. \(n=2000\), \(m=5000\), negative edges, need all-pairs — FW or Johnson?
2. Why must potentials come from BF (or equiv) before Dijkstra?
3. Undirected graph with a negative edge — what happens?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: sparse all-pairs + negatives; FW too slow
- Key invariant: feasible potentials ⇒ nonnegative reduced costs
- Key formula: \(w'=w+h(u)-h(v)\), \(d=d'-h(u)+h(v)\)
- Complexity: \(O(nm + n(n+m)\log n)\)
- Template to remember: super-source BF → \(n\times\) Dijkstra

---


---

<a id="topic-9"></a>
### 9. Dijkstra vs 0-1 BFS vs Bellman–Ford

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2100
- Prerequisites: Graph representations, Priority Queues, Deque, BFS
- Tradeoff: Choosing the strictly minimal complexity tool based on edge weights prevents TLE/MLE.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

The decision matrix for single-source shortest path is dictated strictly by edge weight distribution: Unit weights $w \in \{1\} \implies$ Standard Queue BFS in $\mathcal{O}(V + E)$. Binary weights $w \in \{0, k\} \implies$ 0-1 BFS with `std::deque` in $\mathcal{O}(V + E)$ by pushing 0-cost transitions to the front and $k$-cost to the back. General non-negative weights $w \ge 0 \implies$ Dijkstra with `std::priority_queue` in $\mathcal{O}((V + E) \log V)$. Arbitrary weights with negative cycles or cycle detection $\implies$ Bellman-Ford in $\mathcal{O}(V \cdot E)$.

---

#### 4. Proof Sketches & Recurrences

Dijkstra's greedy choice holds because edge weights are non-negative ($w(u, v) \ge 0$), guaranteeing monotonic distance expansions along shortest paths: $d(u) \le d(v)$ for all explored vertices. 0-1 BFS maintains the invariant that the deque contains distances spanning at most $\{d, d + 1\}$, preserving the monotonic priority queue property in $\mathcal{O}(1)$ amortized time per pop. Bellman-Ford performs dynamic programming over path length: after $k$ relaxation passes over all $E$ edges, $dist[v]$ equals the length of the shortest path from source to $v$ containing at most $k$ edges.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Graph grid movements where turning or changing state costs 1 and moving straight costs 0 (reach for 0-1 BFS).
- Continuous state costs with non-negative arbitrary weights (reach for Dijkstra).
- Negative edge weights with at most $K$ step limits or currency arbitrage exchange rates (reach for Bellman-Ford).
- Dynamic graphs where distances wrap around modulo $M$ (reach for Dijkstra on residue classes / Dijkstra on modulo graph).

---

#### 7. Contest WA / TLE / RE Traps

- Using 0-1 BFS when edge weights are in $\{0, 1, 2\}$; the deque distance invariant breaks down, leading to suboptimal distances.
- Using Dijkstra on graphs with negative edge weights; Dijkstra fails to re-evaluate finalized nodes and produces wrong answers.
- Forgetting to check the stale queue state `if (d > dist[u]) continue;` in Dijkstra, causing memory/time blowup.
- Running Bellman-Ford for exactly $V-1$ iterations without an early-break flag when no relaxations occur, wasting CPU time.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-10"></a>
### 10. Why SPFA Is Dangerous

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier (Defense / Anti-TLE)
- Frequency: Situational
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Shortest Path Faster Algorithm (SPFA), Bellman-Ford, Queue heuristics
- Tradeoff: SPFA is worst-case $\mathcal{O}(V \cdot E)$ or even $\mathcal{O}(2^V)$ on adversarial test cases designed by contest problem setters.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

SPFA is essentially queue-optimized Bellman-Ford. While its average running time on random sparse graphs is often empirical $\mathcal{O}(E)$, contest setters can construct special adversarial test cases (e.g., nested diamond graphs, grid graphs with alternating high/low path shortcuts) that force vertices into the queue exponentially or quadratic number of times ($V \cdot E$). Never rely on SPFA when Dijkstra with potentials (Johnson's algorithm) or 0-1 BFS is applicable.

---

#### 4. Proof Sketches & Recurrences

On a directed graph constructed with $k$ nested diamond stages, each stage doubles the number of times downstream vertices are updated and re-enqueued: a vertex at depth $k$ is enqueued $\Omega(2^k)$ times under FIFO queue discipline. Even heuristics like Small Label First (SLF) and Large Label Last (LLL) have been broken by explicit adversarial constructions in published competitive programming literature.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Safe SPFA with Negative Cycle Detection and Guard Counter
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

bool safe_spfa(int n, int src, const vector<vector<pair<int, ll>>>& adj, vector<ll>& dist) {
    dist.assign(n + 1, INF);
    vector<int> cnt(n + 1, 0);
    vector<bool> in_queue(n + 1, false);
    queue<int> q;
    dist[src] = 0; q.push(src); in_queue[src] = true;
    while (!q.empty()) {
        int u = q.front(); q.pop(); in_queue[u] = false;
        for (auto& [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (!in_queue[v]) {
                    q.push(v); in_queue[v] = true;
                    if (++cnt[v] >= n) return false; // Negative cycle detected!
                }
            }
        }
    }
    return true; // No negative cycles reachable from src
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Problem specifies arbitrary edge weights (positive and negative) and asks for shortest paths or negative cycle detection.
- Constraints have $V, E \le 5000$ where Bellman-Ford passes comfortably, but SPFA offers lower average runtime.
- Min-cost Max-flow (MCMF) implementations using successive shortest path with SPFA (vulnerable to hack on dense graphs; prefer SPFA once then Johnson potentials with Dijkstra).
- Detecting whether an arbitrage cycle exists in currency rates: transform weights $w = -\ln(rate)$.

---

#### 7. Contest WA / TLE / RE Traps

- Assuming SPFA runs in $\mathcal{O}(E)$ on all test cases; Codeforces test suites actively include anti-SPFA tests.
- Not resetting the `in_queue[u] = false` flag when popping from the queue, preventing future valid distance relaxations.
- Using 32-bit integer distances where negative edge accumulations cause underflow/overflow.
- Allowing infinite loop when an unreachable negative cycle exists in the graph; iterate over all components if global negative cycle detection is needed.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-11"></a>
### 11. Kruskal Reconstruction vs HLD for Path Max

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in CF Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Kruskal's MST, Disjoint Set Union (DSU), Heavy-Light Decomposition (HLD), Binary Lifting
- Tradeoff: Kruskal Reconstruction Tree (Reachability Tree) reduces path bottleneck queries to a single LCA in $\mathcal{O}(1)$ or $\mathcal{O}(\log N)$ without writing any segment tree or HLD.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

To find the maximum edge weight on the path between $u$ and $v$ in a graph's MST: standard HLD builds an MST, decomposes tree paths into $\mathcal{O}(\log N)$ segments, and queries a segment tree in $\mathcal{O}(\log^2 N)$ time with 100+ lines of code. Kruskal's Reconstruction Tree (KRT) builds a binary tree with $2N - 1$ nodes: whenever Kruskal joins two components with edge $e = (u, v, w)$, a new node is created with weight $w$, having the roots of $u$ and $v$ as left and right children. The bottleneck maximum weight on the path between $u$ and $v$ is simply the weight of $\text{LCA}(u, v)$ in the KRT!

---

#### 4. Proof Sketches & Recurrences

In Kruskal's algorithm, edges are processed in non-decreasing order of weight. Thus, in the KRT, child nodes always have weights less than or equal to their parent nodes: the tree is a min/max heap on node weights. The first time $u$ and $v$ become connected in Kruskal's process is precisely at $\text{LCA}(u, v)$ in the KRT, and the edge weight that connected them is $weight[\text{LCA}(u, v)]$. Any reachability query 'nodes reachable from $u$ using edges $\le W$' maps to the subtree of the highest ancestor of $u$ with weight $\le W$, solvable via binary lifting in $\mathcal{O}(\log N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Kruskal Reconstruction Tree (Reachability Tree)
#include <bits/stdc++.h>
using namespace std;

struct KRT {
    int n, node_cnt;
    vector<int> par, val;
    vector<vector<int>> up, adj;
    int LOG;
    KRT(int n_) : n(n_), node_cnt(n_), par(2 * n_ + 1), val(2 * n_ + 1), LOG(__lg(2 * n_) + 2) {
        iota(par.begin(), par.end(), 0);
        up.assign(LOG, vector<int>(2 * n_ + 1, 0));
        adj.assign(2 * n_ + 1, {});
    }
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
    void build(vector<tuple<int, int, int>>& edges) {
        sort(edges.begin(), edges.end());
        for (auto& [w, u, v] : edges) {
            int ru = find(u), rv = find(v);
            if (ru != rv) {
                int cur = ++node_cnt;
                val[cur] = w;
                par[ru] = par[rv] = par[cur] = cur;
                adj[cur].push_back(ru); adj[cur].push_back(rv);
                up[0][ru] = up[0][rv] = cur;
            }
        }
        for (int k = 1; k < LOG; ++k)
            for (int i = 1; i <= node_cnt; ++i)
                up[k][i] = up[k - 1][up[k - 1][i]];
    }
    int query_max_edge(int u, int v, const vector<int>& depth) {
        if (depth[u] < depth[v]) swap(u, v);
        for (int k = LOG - 1; k >= 0; --k) if (depth[u] - (1 << k) >= depth[v]) u = up[k][u];
        if (u == v) return val[u];
        for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return val[up[0][u]];
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Query asks: 'What is the maximum/minimum capacity edge on the safest path between $u$ and $v$?'
- Query asks: 'How many vertices are reachable from $u$ using only edges with weight $\le W$?'
- Static graph connectivity with threshold queries (KRT turns it into a subtree query on Euler tour).
- Comparing path bottleneck queries on undirected graphs without dynamic edge weight updates.

---

#### 7. Contest WA / TLE / RE Traps

- Allocating only $N$ nodes instead of $2N$ nodes for the KRT internal join vertices.
- Forgetting that isolated vertices in a disconnected graph will produce a forest; run DFS/LCA preprocessing for every tree root.
- Using KRT when edge weights are dynamically updated during queries; KRT requires static edge weights (use Link-Cut Trees or HLD if edges update).
- Failing to initialize `par` array up to $2N$ elements.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-12"></a>
### 12. Borůvka Niche

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Niche but decisive in Hard CF/ICPC problems
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Minimum Spanning Tree (MST), Bitwise Trie, Geometric Voronoi, DSU
- Tradeoff: Kruskal/Prim require explicit edges ($\mathcal{O}(E \log E)$ or $\mathcal{O}(V^2)$); Borůvka constructs MST on implicit complete graphs where finding the cheapest outgoing edge takes sublinear time.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Borůvka's algorithm operates in phases: in each phase, every connected component simultaneously finds its cheapest outgoing incident edge, and all chosen edges are contracted. Because the number of connected components halves in each phase, there are at most $\lceil \log_2 V \rceil$ phases. In complete graphs where edges are implicit (e.g., $w(u, v) = u \oplus v$ via bitwise XOR, or Manhattan/Euclidean distances in geometry), we cannot sort all $\mathcal{O}(V^2)$ edges. Borůvka allows us to find the cheapest outgoing edge for each component in $\mathcal{O}(V \log(\text{coordinate}))$ using a 0-1 Trie or KD-tree, giving overall $\mathcal{O}(V \log V \log C)$ runtime!

---

#### 4. Proof Sketches & Recurrences

Let $C$ be the number of components at phase $t$. Each component identifies an incident edge with minimal weight. Since each component has at least one edge picked, the contracted graph has at most $\lfloor C/2 \rfloor$ components. Thus, $C_{t+1} \le C_t / 2$, terminating in $\le \log_2 V$ rounds. Total time is $\mathcal{O}(\log V \cdot (\text{cost to query all components' cheapest edge}))$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Boruvka Framework for Implicit Graphs (e.g., XOR MST)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DSU {
    vector<int> p;
    int comps;
    DSU(int n) : p(n), comps(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        p[a] = b; comps--; return true;
    }
};

ll boruvka_xor_mst(int n, vector<int>& a) {
    DSU dsu(n);
    ll total_mst_weight = 0;
    while (dsu.comps > 1) {
        // In each phase, find cheapest outgoing edge for each component root
        // best_edge[comp_root] = {min_weight, target_node}
        vector<pair<int, int>> best(n, {INT_MAX, -1});
        // ... (populate best edges via 0-1 Trie search excluding same component) ...
        bool added = false;
        for (int i = 0; i < n; ++i) {
            if (best[i].second != -1 && dsu.unite(i, best[i].second)) {
                total_mst_weight += best[i].first;
                added = true;
            }
        }
        if (!added) break; // Graph disconnected
    }
    return total_mst_weight;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Complete graph where edge weight is defined by bitwise XOR $w(u, v) = a_u \oplus a_v$ for $N \le 2 \times 10^5$.
- Dense geometric graphs where nearest-neighbor queries can be accelerated by Voronoi diagrams or Delaunay triangulation.
- Graph where edges are implicit and finding the minimum weight outgoing edge from a set of nodes takes sub-linear time.
- Contest problem where $E = \Theta(V^2)$ but $N \approx 10^5$.

---

#### 7. Contest WA / TLE / RE Traps

- Picking an internal edge: cheapest edge query must ensure the endpoint does NOT belong to the same component (`find(u) != find(v)`).
- Tie-breaking: if two components pick edges of equal weight, ensure unique edge ordering $(w, \min(u, v), \max(u, v))$ to prevent cycles with equal weights.
- Infinite loops if graph is disconnected: ensure the loop terminates when no edges are added in a round.
- Trie deletion/insertion overhead: rebuilding or modifying the Trie dynamically must be done efficiently per round.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-13"></a>
### 13. Part A — [08-a-shortest-paths.md](08-a-shortest-paths.md)

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2200
- Prerequisites: Graph representation, adjacency lists, priority queues

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Shortest path algorithms are the primary workhorse for state-space exploration. The optimal algorithm is determined strictly by edge weight characteristics: unit weights $\implies$ BFS $\mathcal{O}(V + E)$; weights in $\{0, 1\} \implies$ 0-1 BFS $\mathcal{O}(V + E)$; non-negative weights $\implies$ Dijkstra $\mathcal{O}((V + E) \log V)$; arbitrary weights $\implies$ Bellman-Ford $\mathcal{O}(V \cdot E)$.

---

#### 4. Proof Sketches & Recurrences

Dijkstra relies on the triangle inequality $d(v) \le d(u) + w(u, v)$ and greedily finalizes the minimum distance unvisited vertex. Non-negativity guarantees that once popped from the priority queue, $d(u)$ is optimal.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// State-space Dijkstra template
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

vector<ll> dijkstra(int n, int src, const vector<vector<pair<int, ll>>>& adj) {
    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0; pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto& [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Minimum cost or time to reach target in state graph.
- Transforming edge weights into potentials to eliminate negative costs.
- Shortest path DAG formulation to count number of shortest paths.
- Dynamic graph transitions dependent on modulo or resource state (e.g., fuel $\le K$).

---

#### 7. Contest WA / TLE / RE Traps

- Omitting the stale state check `if (d > dist[u]) continue;` leading to $\mathcal{O}(E \log E)$ performance regression.
- Integer overflow: using 32-bit `int` for accumulated distances instead of 64-bit `long long`.
- Using SPFA on dense or crafted anti-SPFA contest test cases leading to worst-case $\mathcal{O}(V \cdot 2^V)$.
- Failing to detect unreachable vertices ($dist[v] = \infty$).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-14"></a>
### 14. Part B — [08-b-mst-euler-functional.md](08-b-mst-euler-functional.md)

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: DSU, Euler tour, in-degree/out-degree graph analysis

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Spanning trees minimize total edge weight while preserving connectivity. Functional graphs (where every vertex has out-degree 1) decompose uniquely into directed cycles with trees rooted on cycle vertices. Eulerian circuits require all vertices in a connected component to have equal in-degree and out-degree.

---

#### 4. Proof Sketches & Recurrences

Kruskal's algorithm relies on the Cut Property: for any partition $(S, V \setminus S)$, the minimum weight edge crossing the cut belongs to an MST. Euler's theorem states that a directed connected graph has an Eulerian cycle iff $\text{in-deg}(u) = \text{out-deg}(u)$ for all $u$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Kruskal MST with DSU and Hierholzer Eulerian Trail
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> p;
    DSU(int n) : p(n + 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        p[a] = b; return true;
    }
};

long long kruskal(int n, vector<tuple<long long, int, int>>& edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n); long long total_weight = 0; int cnt = 0;
    for (auto& [w, u, v] : edges) {
        if (dsu.unite(u, v)) { total_weight += w; cnt++; }
    }
    return cnt == n - 1 ? total_weight : -1;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Connecting all components with minimum total cable, road, or edge cost.
- Each element transitions deterministically to exactly one other element ($x \to f(x)$).
- Traversing every edge of a graph exactly once.
- Bottleneck edge minimization on paths across a network.

---

#### 7. Contest WA / TLE / RE Traps

- Graph is disconnected: MST contains $< N - 1$ edges, but the algorithm reports partial weight without checking component count.
- Eulerian path start vertex not initialized to the unique vertex with $\text{out-deg} - \text{in-deg} = 1$.
- Recursion stack overflow in Hierholzer's algorithm on large graphs ($E > 10^5$); use an iterative stack.
- Modifying edge adjacency list while iterating without tracking used edge IDs in undirected multigraphs.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---


---

<a id="topic-15"></a>
### 15. Minimum Spanning Tree Variants

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2200 | **Frequency:** Common  
> **Prerequisites:** DSU (Kruskal), heap / Dijkstra-like Prim  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2200
- Prerequisites: DSU (Kruskal), heap / Dijkstra-like Prim

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

MST minimizes total edge weight connecting all vertices (forest if disconnected: MSF). Cut property: the lightest edge across any cut is safe to include. Cycle property: the heaviest edge on any cycle is not needed. Kruskal sorts edges and adds if endpoints in different components; Prim grows a tree like Dijkstra. Many problems are not “compute MST weight” but use **MST structure** (bottleneck paths, second-best MST, forced edges).

*Note: If you need to **count** the total number of valid Minimum Spanning Trees (or just spanning trees in general), you must use Kirchhoff's Matrix Tree Theorem. → [Go to Section 14b](14-b-matrix-tree-theorem.md)*

---

#### 4. Proof Sketches & Recurrences

Kruskal: sort \(O(m\log m)\); DSU \(\approx O(m\alpha(n))\). Prim with binary heap: \(O((n+m)\log n)\) like Dijkstra. Bottleneck: for undirected graphs, path minimizing the maximum edge equals the max edge on the unique path in any MST (when weights distinct; otherwise some MST).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build edges \(O(m)\)
- Per-query / per-operation: Kruskal \(O(m\log m)\); Prim \(O((n+m)\log n)\)
- Total: as above
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace mst {
using ll = long long;

struct DSU {
    vector<int> p, r;
    DSU(int n = 0) { init(n); }
    void init(int n) {
        p.resize(n);
        r.assign(n, 0);
        iota(p.begin(), p.end(), 0);
    }
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

struct Edge {
    int u, v;
    ll w;
    bool operator<(const Edge& o) const { return w < o.w; }
};

// returns {total_weight, edges_in_mst}; total = -1 if not connected
pair<ll, vector<Edge>> kruskal(int n, vector<Edge> edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    ll total = 0;
    vector<Edge> used;
    used.reserve(n - 1);
    for (auto e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total += e.w;
            used.push_back(e);
            if ((int)used.size() == n - 1) break;
        }
    }
    if ((int)used.size() != n - 1) return {-1, {}};
    return {total, used};
}

// Prim from src; assumes connected undirected g
pair<ll, vector<Edge>> prim(int n, int src,
                            const vector<vector<pair<int, ll>>>& g) {
    vector<ll> dist(n, (ll)4e18);
    vector<int> par(n, -1);
    vector<char> in(n, 0);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    ll total = 0;
    int taken = 0;
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (in[u]) continue;
        in[u] = 1;
        total += d;
        ++taken;
        for (auto [v, w] : g[u]) {
            if (!in[v] && w < dist[v]) {
                dist[v] = w;
                par[v] = u;
                pq.push({w, v});
            }
        }
    }
    if (taken != n) return {-1, {}};
    vector<Edge> used;
    for (int v = 0; v < n; ++v)
        if (par[v] != -1) used.push_back({par[v], v, dist[v]});
    return {total, used};
}
} // namespace mst
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Connect all cities with min cable cost
- Minimax path in undirected graph (= max edge on MST path)
- “Remove max edge / add constraints” → MST edges unique or not
- Second best spanning tree; MST with one edge forced/forbidden

---

#### 7. Contest WA / TLE / RE Traps

- Assuming connectivity without checking `|MST edges| == n-1`
- Using directed edges in Kruskal incorrectly
- `long long` for sums; overflow on weights
- Second-best MST: forgetting to try replacing non-tree edges correctly
- Distinct vs non-distinct weights for “unique MST”

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Minimum spanning forest**
- **Maximum spanning tree:** negate weights or sort descending
- **Second-best MST:** for each non-tree edge, replace max on tree path
- **Directed MST (Chu–Liu/Edmonds):** rare, harder — niche
- **MST with degree constraints / \(k\) edges:** often binary search + matroid or Prim variants

---

#### 11. Typical Problem Archetypes

1. Standard application: MST total weight
2. Slightly disguised: minimax path queries via MST
3. Difficult: second-best MST; count distinct MSTs
4. Very difficult / advanced: xor-MST (Borůvka-like trie); dynamic MST offline

---

#### 12. Recognition & Identification Drills

1. Connect \(n\) vertices with given undirected edges, minimize total cost.
2. For each query pair, minimize the maximum edge on any path.
3. Find spanning tree weight if a given edge must be included.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: undirected connectivity with min total / bottleneck
- Key invariant: cut & cycle properties
- Key formula: Kruskal sort + DSU; Prim grow lightest cut edge
- Complexity: \(O(m\log m)\) Kruskal typical
- Template to remember: sort edges + `unite`

---

---


---

<a id="topic-16"></a>
### 16. Kruskal Reconstruction Tree

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Kruskal, LCA / binary lifting, tree queries  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Kruskal, LCA / binary lifting, tree queries

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Run Kruskal; each time two components merge via edge weight \(w\), create a **new parent node** with value \(w\) whose children are the two component roots. Leaves are original vertices. The path-max edge between \(a\) and \(b\) in the MST equals the **LCA’s weight** in this binary-ish tree (often \(2n-1\) nodes). Transforms bottleneck queries into LCA. Prefer this over HLD on the MST when you only need path max/min of *merge weights*.

---

#### 4. Proof Sketches & Recurrences

Edges added in increasing weight. LCA of leaves \(a,b\) is the first merge that connected them ⇒ that merge weight is the minimax path cost. Build LCA (binary lifting) on the reconstruction tree (rooted at final merges; forest if disconnected).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: Kruskal \(O(m\log m)\) + LCA build \(O(n\log n)\)
- Per-query / per-operation: \(O(\log n)\) LCA
- Total: preprocess + \(q\log n\)
- Memory: \(O(n\log n)\)`

##### C++17 Template

```cpp
namespace kruskal_rebuild {
using ll = long long;

struct DSU {
    vector<int> p;
    DSU(int n) : p(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
};

struct Edge {
    int u, v;
    ll w;
    bool operator<(const Edge& o) const { return w < o.w; }
};

struct Tree {
    int n_leaves = 0, N = 0, LOG = 0;
    vector<vector<int>> g;
    vector<ll> val; // internals: merge weight; leaves typically 0
    vector<int> root;
    vector<int> dep;
    vector<vector<int>> up;

    int lca(int a, int b) const {
        if (dep[a] < dep[b]) swap(a, b);
        int d = dep[a] - dep[b];
        for (int j = 0; j < LOG; ++j)
            if (d & (1 << j)) a = up[j][a];
        if (a == b) return a;
        for (int j = LOG - 1; j >= 0; --j)
            if (up[j][a] != up[j][b]) {
                a = up[j][a];
                b = up[j][b];
            }
        return up[0][a];
    }

    int component_root(int x) const {
        while (up[0][x] != x) x = up[0][x];
        return x;
    }

    // minimax edge on path between leaves a,b; -1 if disconnected
    ll path_max(int a, int b) const {
        if (component_root(a) != component_root(b)) return -1;
        int p = lca(a, b);
        return (p < n_leaves) ? 0 : val[p]; // same leaf / degenerate
    }
};

// Leaves 0..n-1; each Kruskal merge creates a new parent with val = edge weight.
Tree build(int n, vector<Edge> edges) {
    sort(edges.begin(), edges.end());
    Tree t;
    t.n_leaves = n;
    int Nmax = 2 * n;
    t.g.assign(Nmax, {});
    t.val.assign(Nmax, 0);
    DSU dsu(n);
    vector<int> root_of(n);
    iota(root_of.begin(), root_of.end(), 0);
    t.N = n;
    for (auto e : edges) {
        int a = dsu.find(e.u), b = dsu.find(e.v);
        if (a == b) continue;
        int p = t.N++;
        t.val[p] = e.w;
        t.g[p] = {root_of[a], root_of[b]}; // rooted: children only
        dsu.p[b] = a;
        root_of[a] = p;
    }
    vector<char> has_parent(t.N, 0);
    for (int u = n; u < t.N; ++u)
        for (int v : t.g[u]) has_parent[v] = 1;
    t.root.clear();
    for (int i = 0; i < t.N; ++i)
        if (!has_parent[i]) t.root.push_back(i);

    t.LOG = 1;
    while ((1 << t.LOG) <= t.N) ++t.LOG;
    t.dep.assign(t.N, 0);
    t.up.assign(t.LOG, vector<int>(t.N));
    for (int r : t.root) {
        t.up[0][r] = r;
        vector<int> st = {r};
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (int v : t.g[u]) {
                t.up[0][v] = u;
                t.dep[v] = t.dep[u] + 1;
                st.push_back(v);
            }
        }
    }
    for (int j = 1; j < t.LOG; ++j)
        for (int i = 0; i < t.N; ++i)
            t.up[j][i] = t.up[j - 1][t.up[j - 1][i]];
    return t;
}
} // namespace kruskal_rebuild
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Many queries: min possible maximum edge on a path (undirected)
- “When do \(a\) and \(b\) become connected if edges added by weight?” → LCA depth/time
- Offline queries sorted by limit \(x\): equivalent to connectivity in Kruskal reconstr.
- Editorial mentions “Kruskal reconstruction tree” / “line tree” / “BCT-like merge tree”

---

#### 7. Contest WA / TLE / RE Traps

- Not handling disconnected graphs (forest of reconstruction trees)
- Using edge weight on MST path via HLD incorrectly when reconstr. LCA is simpler
- Off-by-one node indexing (leaves \(0..n-1\), internals \(\ge n\))
- Sorting ascending vs descending for maximin vs minimax
- Building undirected cycles in the merge tree (keep rooted children lists)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Max spanning reconstruction for maximin paths
- Persistent DSU / time = weight for “connected under limit \(x\)”
- Combine with virtual trees on reconstruction tree

---

#### 11. Typical Problem Archetypes

1. Standard application: query minimax path between pairs
2. Slightly disguised: earliest time two nodes connect as edges appear by weight
3. Difficult: queries on subtree of reconstruction tree (component at a threshold)
4. Very difficult / advanced: path problems with layered constraints on merge weights

---

#### 12. Recognition & Identification Drills

1. \(q\) queries: minimum possible maximum edge among all paths \(u\)–\(v\).
2. Edges appear in order of increasing length; for each query, when do \(u,v\) connect?
3. Same as (1) but you already know HLD — which structure is lighter?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: bottleneck path queries / connectivity-by-weight
- Key invariant: LCA merge weight = minimax edge
- Key formula: Kruskal merges → new parent nodes; query LCA
- Complexity: \(O(m\log m + (n+q)\log n)\)
- Template to remember: merge tree + binary lifting LCA  
- vs HLD: reconstr. for path max; HLD if arbitrary path aggregates/updates

---

---


---

<a id="topic-17"></a>
### 17. Borůvka

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** MST cut property, DSU  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: MST cut property, DSU

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

In each phase, every component chooses its minimum-weight outgoing edge; add all such edges (carefully resolving conflicts) and merge. Components at least halve in count ⇒ \(O(\log n)\) phases. Same MST; the parallel “each component picks” view is what makes xor-MST / some algebraic MST variants natural. **Niche** as a default Kruskal replacement on CF.

---

#### 4. Proof Sketches & Recurrences

Phase: compute `min_out[component]`; unite along those edges; ignore intra-component. \(O(\log n)\) phases × \(O(m)\) scan ⇒ \(O(m\log n)\) (plus DSU). Correct by cut property each chosen edge is safe (with tie-breaking).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(m)\)
- Per-query / per-operation: one MST \(O(m\log n)\) typical
- Total: \(O(m\log n)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Xor-MST / minimum spanning tree with edge weight \(a_u\oplus a_v\)
- Parallel MST / theoretical \(O(m\log n)\) without sorting all edges first
- Problem structure: “best edge out of each component” repeatedly

---

#### 7. Contest WA / TLE / RE Traps

- Not skipping when `best[c]==-1` (disconnected)
- Double-adding the same edge when both sides selected it (unite handles; don’t add weight twice)
- Using Borůvka where Kruskal is shorter to code under time pressure
- Tie-breaking inconsistently causing cycles in naive parallel add

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Xor-MST:** Borůvka phases + trie of component values
- Parallel / external-memory MST motivation
- Component-by-component Prim is related

---

#### 11. Typical Problem Archetypes

1. Standard application: MST via Borůvka (rare vs Kruskal)
2. Slightly disguised: xor-MST
3. Difficult: Borůvka with dynamic best-edge data structures
4. Very difficult / advanced: theoretical MST algorithms inspired by Borůvka

---

#### 12. Recognition & Identification Drills

1. MST where weight of \((i,j)\) is \(a_i\oplus a_j\).
2. Implement MST without sorting all edges globally — which algorithm fits?
3. Why does each phase roughly halve components?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: xor-MST / “min outgoing per component” structure; else Kruskal
- Key invariant: lightest outgoing edges are safe
- Key formula: \(O(\log n)\) phases of component matching
- Complexity: \(O(m\log n)\)
- Template to remember: per-component `best` edge then unite  
- Niche early ROI — don’t prioritize over Kruskal/Prim

---

---


---

<a id="topic-18"></a>
### 18. Eulerian Paths / Circuits

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** Hierholzer, degree / in–out degree, adjacency with deletion  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Hierholzer, degree / in–out degree, adjacency with deletion

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

Eulerian circuit traverses every **edge** exactly once and returns; path allows different start/end. Undirected: circuit iff all degrees even (+ connectivity on edges); path iff exactly 0 or 2 odd degrees. Directed: circuit iff in=out for all; path iff one vertex out=in+1 (start), one in=out+1 (end), others equal. Hierholzer: DFS-consume edges, append node on retreat (reverse at end). Modeling: “draw without lifting pen,” DNA assembly, rotate strings / balance parentheses as edges.

*Note: If you need to **count** the number of Eulerian paths/circuits, use the BEST Theorem. → [Go to Section 14c](14-c-algebraic-graph-theory.md)*

---

#### 4. Proof Sketches & Recurrences

Hierholzer builds closed tours in residual unused edges and splices them. Complexity \(O(n+m)\) with explicit edge deletion (iterators / stack indices). Connectivity: consider only vertices with nonzero degree.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build adj \(O(n+m)\)
- Per-query / per-operation: \(O(n+m)\)
- Total: \(O(n+m)\)
- Memory: \(O(n+m)\)`

##### C++17 Template

```cpp
namespace euler {
// Undirected Hierholzer. edges as adj[u] = list of {to, edge_id}
// Each undirected edge once in `used`
vector<int> undirected_trail(int n, int m,
                             vector<vector<pair<int, int>>>& adj,
                             int start = -1) {
    vector<char> used(m, 0);
    vector<int> deg(n, 0);
    for (int u = 0; u < n; ++u) deg[u] = (int)adj[u].size();
    int odd = 0, any = -1;
    for (int u = 0; u < n; ++u) {
        if (deg[u]) any = u;
        if (deg[u] & 1) {
            ++odd;
            start = u;
        }
    }
    if (any == -1) return {}; // no edges
    if (odd != 0 && odd != 2) return {}; // impossible
    if (start < 0) start = any;

    vector<int> st, path;
    st.push_back(start);
    vector<int> it(n, 0);
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)adj[u].size() && used[adj[u][it[u]].second]) ++it[u];
        if (it[u] == (int)adj[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = adj[u][it[u]];
            ++it[u];
            if (used[id]) continue;
            used[id] = 1;
            st.push_back(v);
        }
    }
    if ((int)path.size() != m + 1) return {}; // not connected on edges
    reverse(path.begin(), path.end());
    return path; // vertex sequence
}

// Directed: adj[u] = list of {to, edge_id}; m edges
vector<int> directed_trail(int n, int m,
                           vector<vector<pair<int, int>>>& adj,
                           const vector<int>& indeg,
                           const vector<int>& outdeg) {
    int start = -1, end = -1;
    for (int i = 0; i < n; ++i) {
        if (outdeg[i] == indeg[i] + 1) {
            if (start != -1) return {};
            start = i;
        } else if (indeg[i] == outdeg[i] + 1) {
            if (end != -1) return {};
            end = i;
        } else if (indeg[i] != outdeg[i]) return {};
    }
    if (start == -1) {
        for (int i = 0; i < n; ++i)
            if (outdeg[i]) {
                start = i;
                break;
            }
    }
    if (start == -1) return {};

    vector<char> used(m, 0);
    vector<int> it(n, 0), st, path;
    st.push_back(start);
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)adj[u].size() && used[adj[u][it[u]].second]) ++it[u];
        if (it[u] == (int)adj[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = adj[u][it[u]++];
            if (used[id]) continue;
            used[id] = 1;
            st.push_back(v);
        }
    }
    if ((int)path.size() != m + 1) return {};
    reverse(path.begin(), path.end());
    return path;
}
} // namespace euler
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Use each edge exactly once
- Reconstruct a sequence from adjacent pairs (de Bruijn style)
- Directed: “words” as edges between prefix/suffix nodes
- Add minimum edges to make Eulerian

---

#### 7. Contest WA / TLE / RE Traps

- Checking vertex connectivity instead of **edge-relevant** connectivity
- Multiedges / self-loops mishandled in `used[]`
- Recursive Hierholzer → stack overflow; use iterative
- Directed: wrong start/end degree pattern
- Returning edge order vs vertex order off-by-one
- Not reversing the postorder path

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Chinese Postman (undirected): add min matching on odd vertices + Euler
- Make Eulerian with min added edges
- de Bruijn sequence via Euler in \(k\)-mer graph
- Mixed graphs (harder)

---

#### 11. Typical Problem Archetypes

1. Standard application: output Euler circuit/path
2. Slightly disguised: reconstruct permutation from consecutive pairs
3. Difficult: min edges to add to become Eulerian + construct
4. Very difficult / advanced: Chinese Postman / directed CPP

---

#### 12. Recognition & Identification Drills

1. Undirected multigraph; print a tour using every edge once.
2. Alphabet digraph of substring transitions; build shortest superstring-like sequence via Euler.
3. Exactly two odd-degree vertices — what tour exists?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: traverse every edge once
- Key invariant: degree / in-out conditions + weak connectivity
- Key formula: Hierholzer consume-edges + reverse path
- Complexity: \(O(n+m)\)
- Template to remember: iterative stack + `used[edge]`

---

---


---

<a id="topic-19"></a>
### 19. Functional Graphs

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** DFS/BFS, cycle detection, binary lifting optional  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: DFS/BFS, cycle detection, binary lifting optional

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

##### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

##### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

##### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

##### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

#### 3. Core Intuition & Problem Framing

A **functional graph** has outdegree exactly 1 for every node (`next[u] = f(u)`). Structure: each component is a single cycle with trees directed **into** the cycle (inverted arborescences). Contests love: process \(k\) applications of \(f\), sum along path, find cycle length, rho/Floyd, or model permutations. Treat components independently: find cycle, compute depths of tree nodes into cycle entry, then answer jumps with `k` vs distance-to-cycle + modular arithmetic on cycle.

---

#### 4. Proof Sketches & Recurrences

Follow edges; mark colors (0 unseen, 1 stack, 2 done) or record time-in-stack to extract cycles. For queries \(f^{(k)}(v)\): binary lifting table `up[j][v] = f^{(2^j)}(v)` in \(O(n\log K)\). Cycle answers: if \(k \ge dist\_to\_cycle\), reduce \((k - dist) \bmod len\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: analyze \(O(n)\); lifting \(O(n\log K)\)
- Per-query / per-operation: jump \(O(\log K)\); cycle query \(O(1)\) after prep
- Total: \(O(n\log K + q\log K)\)
- Memory: \(O(n\log K)\) for lifting; \(O(n)\) for cycle info`

##### C++17 Template

```cpp
namespace functional {
// next[u] in [0..n)
struct Info {
    vector<int> next;
    vector<int> cyc_id;      // -1 if not on cycle; else cycle index
    vector<int> cyc_pos;     // position on cycle
    vector<int> cyc_len;
    vector<int> dist_to_cyc; // 0 if on cycle
    vector<int> entry;       // first cycle vertex reached
    vector<vector<int>> cycles;
};

Info analyze(const vector<int>& next) {
    int n = (int)next.size();
    Info info;
    info.next = next;
    info.cyc_id.assign(n, -1);
    info.cyc_pos.assign(n, -1);
    info.dist_to_cyc.assign(n, -1);
    info.entry.assign(n, -1);
    vector<int> state(n, 0); // 0=unseen,1=visiting,2=done
    vector<int> stack;
    stack.reserve(n);

    for (int s = 0; s < n; ++s) {
        if (state[s]) continue;
        int u = s;
        while (state[u] == 0) {
            state[u] = 1;
            stack.push_back(u);
            u = next[u];
        }
        if (state[u] == 1) {
            // found cycle ending at u
            vector<int> cyc;
            while (true) {
                int x = stack.back();
                stack.pop_back();
                state[x] = 2;
                cyc.push_back(x);
                if (x == u) break;
            }
            reverse(cyc.begin(), cyc.end());
            int cid = (int)info.cycles.size();
            info.cycles.push_back(cyc);
            info.cyc_len.push_back((int)cyc.size());
            for (int i = 0; i < (int)cyc.size(); ++i) {
                int x = cyc[i];
                info.cyc_id[x] = cid;
                info.cyc_pos[x] = i;
                info.dist_to_cyc[x] = 0;
                info.entry[x] = x;
            }
        }
        while (!stack.empty()) {
            int x = stack.back();
            stack.pop_back();
            state[x] = 2;
        }
    }

    // dists for tree nodes: walk forward (memo)
    for (int v = 0; v < n; ++v) {
        if (info.dist_to_cyc[v] != -1) continue;
        vector<int> path;
        int u = v;
        while (info.dist_to_cyc[u] == -1) {
            path.push_back(u);
            u = next[u];
        }
        int d = info.dist_to_cyc[u];
        int ent = info.entry[u];
        for (int i = (int)path.size() - 1; i >= 0; --i) {
            ++d;
            info.dist_to_cyc[path[i]] = d;
            info.entry[path[i]] = ent;
            info.cyc_id[path[i]] = info.cyc_id[ent];
        }
    }
    return info;
}

// binary lifting for f^k
struct Lift {
    int LOG;
    vector<vector<int>> up;
    Lift(const vector<int>& next, int max_pow = 60) {
        int n = (int)next.size();
        LOG = max_pow;
        up.assign(LOG, vector<int>(n));
        up[0] = next;
        for (int j = 1; j < LOG; ++j)
            for (int i = 0; i < n; ++i)
                up[j][i] = up[j - 1][up[j - 1][i]];
    }
    int jump(int v, long long k) const {
        for (int j = 0; j < LOG && k; ++j)
            if (k & (1LL << j)) {
                v = up[j][v];
                k ^= (1LL << j);
            }
        return v;
    }
};
} // namespace functional
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Array `p[i]` or `a[i]` pointing to exactly one next index
- “Repeatedly replace \(x := f(x)\)”
- Permutation as special case (also indegree 1): disjoint cycles only
- Tortoise–hare cycle detection in arrays

---

#### 7. Contest WA / TLE / RE Traps

- Treating functional graph as general digraph DP without cycle handling
- Infinite loops when summing along path without stopping at cycle
- Permutation assumed when duplicate `next` values exist (not a perm)
- Off-by-one: steps to enter cycle vs index on cycle
- Using recursion depth \(n\) for follow — iterative required

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Permutation: disjoint cycles only; \(k\)-th power of perm
- Partial functional (some nodes no out) — rare
- Weighted edges on `next`: prefix on trees + cycle prefix sums
- Floyd cycle detection without \(O(n)\) memory marks (interview style)

---

#### 11. Typical Problem Archetypes

1. Standard application: where is token after \(k\) moves?
2. Slightly disguised: follow pointers until repeat; count distinct values
3. Difficult: sum of values on path of length \(k\) with cycle expansion
4. Very difficult / advanced: functional graph + segment tree on cycle / queries offline

---

#### 12. Recognition & Identification Drills

1. Array \(a[1..n]\); from \(i\) go to \(a_i\); answer \(q\) queries after \(k_j\) steps.
2. Each component’s cycle length; count nodes not on any cycle.
3. Robot follows unique next cell; detect period before revisiting.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: outdegree exactly 1 everywhere
- Key invariant: one cycle per component + in-trees
- Key formula: \(f^{(k)}\) via lifting or dist-to-cycle + mod
- Complexity: \(O(n)\) structure; \(O(n\log K)\) jumps
- Template to remember: mark cycles, then depths into entry; binary lift optional

---


---
