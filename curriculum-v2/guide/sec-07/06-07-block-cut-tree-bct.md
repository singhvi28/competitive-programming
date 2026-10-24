# 6. Block-Cut Tree (BCT)

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Articulation Points, Biconnected Components (BCC)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Articulation Points, Biconnected Components (BCC)

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

The **Block-Cut Tree** is a meta-graph where:
1. Every articulation point is a "cut" vertex.
2. Every biconnected component is a "block" vertex.
3. Edges connect a block vertex to all cut vertices that belong to that BCC.

This forms a tree! Any path between $U$ and $V$ in the original graph must pass through the exact sequence of articulation points on the simple path between their corresponding nodes in the Block-Cut Tree. This trivially solves "must-pass-through" or "maximum weight cycle on path" queries.

---

## 4. Proof Sketches & Recurrences

Tarjan's DFS maintains discovery times $tin[u]$ and lowest reachable ancestor times $low[u]$. Vertex $u$ is an articulation point if $low[v] \ge tin[u]$ for some child $v$ (or if root has $\ge 2$ children). During DFS, edges are maintained on an edge stack. When $low[v] \ge tin[u]$ triggers, all edges up to $(u, v)$ on the stack form a new biconnected block. The resulting BCT has at most $2V$ vertices and $2V - 1$ edges, with bipartite structure alternating between cut vertices and blocks.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Builds BCCs and the BCT
// graph is 0-indexed, output BCT has original vertices (articulation points) 
// and new block vertices starting from id N.
vector<vector<int>> bct; // size N + num_bccs
vector<int> bcc_id; // Maps original edge/vertex to BCC
```

---

## 6. Recognition Trigger Signals & Heuristics

- (Omitted full template due to length, but relies on Tarjan's stack of edges).*

---

## 7. Contest WA / TLE / RE Traps

- Root of DFS tree articulation condition: root is a cut vertex if and only if it has $\ge 2$ DFS children, not when $low[v] \ge tin[u]$.
- Popping the edge/vertex stack too far: the cut vertex $u$ itself must NOT be popped during child block extraction because $u$ belongs to multiple blocks.
- Graph has multiple disconnected components: must iterate DFS from $1$ to $N$ to cover all components.
- Index allocation: BCT contains up to $2V$ vertices; resizing arrays to $N$ causes out-of-bounds access.

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
