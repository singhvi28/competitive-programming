# The Augmentation Step

> **Section:** §21 Greedy Advanced (Matroids & Oracles)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Greedy and Combinatorial Optimization: Axiomatic Matroid Theory, Rado-Edmonds Greedy Optimality, Matroid Intersection on Bipartite Exchange DAGs, Antimatroids, and Dynamic Verification Oracles.

### Fundamental Theorems & Invariants

- **Matroid Axioms (Whitney):** A ground set $E$ and family of independent sets $\mathcal{I}$ form a Matroid $(E, \mathcal{I})$ if: (1) $\emptyset \in \mathcal{I}$, (2) $I \in \mathcal{I}, J \subseteq I \implies J \in \mathcal{I}$ (hereditary), (3) $I, J \in \mathcal{I}, |I| < |J| \implies \exists e \in J \setminus I$ such that $I \cup \{e\} \in \mathcal{I}$ (augmentation).
- **Rado-Edmonds Theorem:** The greedy algorithm finds the maximum-weight independent set for any weight function if and only if $(E, \mathcal{I})$ is a matroid.
- **Matroid Intersection Theorem:** Given two matroids $M_1 = (E, \mathcal{I}_1)$ and $M_2 = (E, \mathcal{I}_2)$, the maximum cardinality common independent set $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ is found by repeatedly finding shortest augmenting paths on the bipartite exchange graph in $\mathcal{O}(R^3 Q)$ time.

### Algorithmic Execution Blueprint

1. **Matroid Intersection Exchange Graph:** Start with independent set $I$. Build bipartite graph with parts $I$ and $E \setminus I$. Add directed edges $y \to x$ if $I \setminus \{y\} \cup \{x\} \in \mathcal{I}_1$, and $x \to y$ if $I \setminus \{y\} \cup \{x\} \in \mathcal{I}_2$.
2. **Augmentation:** Find shortest path from $X_1 = \{x \in E \setminus I : I \cup \{x\} \in \mathcal{I}_1\}$ to $X_2 = \{x \in E \setminus I : I \cup \{x\} \in \mathcal{I}_2\}$ via BFS. Augment $I \leftarrow I \Delta P$.

### Closed-Form Invariant Equations

$$r(M_1 \cap M_2) = \min_{U \subseteq E} \big(r_1(U) + r_2(E \setminus U)\big) \quad \text{(Min-Max Duality)}$$

### Structural Edge Cases & Assumptions

- Matroid intersection works for TWO matroids; 3-Matroid intersection is NP-hard.
- Augmenting paths on the exchange graph MUST be strictly shortest paths by edge count (computed via BFS) to guarantee that symmetric difference updates preserve independence.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Generic Matroid Intersection Engine
#include <bits/stdc++.h>
using namespace std;

template <typename Matroid1, typename Matroid2>
vector<int> matroid_intersection(int n, Matroid1& m1, Matroid2& m2) {
    vector<int> I;
    vector<bool> in_I(n, false);

    while (true) {
        vector<int> X1, X2;
        vector<vector<int>> adj(n);

        // 1. Identify Sources (X1) and Sinks (X2)
        for (int y = 0; y < n; ++y) {
            if (in_I[y]) continue;
            if (m1.can_add(I, y)) X1.push_back(y);
            if (m2.can_add(I, y)) X2.push_back(y);
        }

        // 2. Build Exchange Graph Edges
        for (int x : I) {
            vector<int> I_minus_x;
            for (int elem : I) if (elem != x) I_minus_x.push_back(elem);

            for (int y = 0; y < n; ++y) {
                if (in_I[y]) continue;
                // M1 edge: y -> x
                if (m1.can_add(I_minus_x, y)) adj[y].push_back(x);
                // M2 edge: x -> y
                if (m2.can_add(I_minus_x, y)) adj[x].push_back(y);
            }
        }

        // 3. BFS Shortest Path from X1 to X2
        vector<int> parent(n, -1);
        queue<int> q;
        for (int src : X1) {
            q.push(src);
            parent[src] = src;
        }

        int target = -1;
        vector<bool> is_sink(n, false);
        for (int snk : X2) is_sink[snk] = true;

        while (!q.empty() && target == -1) {
            int u = q.front(); q.pop();
            if (is_sink[u]) {
                target = u;
                break;
            }
            for (int v : adj[u]) {
                if (parent[v] == -1) {
                    parent[v] = u;
                    q.push(v);
                }
            }
        }

        if (target == -1) break; // Maximum independent set reached

        // 4. Augment along the shortest path
        int curr = target;
        while (true) {
            in_I[curr] = !in_I[curr];
            if (curr == parent[curr]) break;
            curr = parent[curr];
        }

        I.clear();
        for (int i = 0; i < n; ++i) {
            if (in_I[i]) I.push_back(i);
        }
    }
    return I;
}
```

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1556H | DIY Tree | 3300 | Matroid Intersection, Spanning Tree, Augmenting Paths | Matroid Intersection: Graphic Matroid M(G) + Degree-Constrained Partition Matroid. | [Solve Problem](https://codeforces.com/contest/1556/problem/H) |
| Codeforces | CF-1408G | Clusterization Counting | 2700 | Kruskal Tree, Tree DP, Matroid | Kruskal reconstruction tree + DP on clique subtrees. | [Solve Problem](https://codeforces.com/contest/1408/problem/G) |
| Codeforces | CF-1284E | New Year and Castle Construction | 2600 | Angular Sweep, Geometry, Combinatorics | Angular sweep with complementary combinatorics counting points strictly outside convex hulls. | [Solve Problem](https://codeforces.com/contest/1284/problem/E) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Matroid Intersection in Competitive Programming (bqi343 / ecnerwala)](https://codeforces.com/blog/entry/69287)
- **[YouKn0wWho]** [YouKn0wWho Academy: Matroid Theory, Duality and Antimatroids](https://youkn0wwho.academy/topic-list#matroids)

---
