# Single-Pass $O(\log N)$ Binary Search on SegTrees

> **Section:** §21 Greedy Advanced (Matroids & Oracles)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Replaces external binary search ($O(\log^2 N)$) with a direct in-tree descent in $O(\log N)$.
- Crucial for dynamic resource allocation and finding first/last indices satisfying bounds under point/range updates.

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

## 3. Core Intuition & Problem Framing

To find the first index $i \ge L$ such that $A[i] \ge X$:
1. If the current node's range $[tl, tr]$ lies outside $[L, R]$ or $\max(node) < X$, prune immediately ($O(1)$).
2. If at a leaf, return its index.
3. Recursively search the **left child** first. If it yields a valid index, return it immediately without exploring the right child.
4. Otherwise, search the **right child**.

```cpp
// C++17 — Walkable Segment Tree (Find First >= X starting from L)
#include <bits/stdc++.h>
using namespace std;

struct WalkableSegTree {
    int n;
    vector<int> tree;

    WalkableSegTree(int n, const vector<int>& a) : n(n), tree(4 * n) {
        build(1, 0, n - 1, a);
    }

    void build(int v, int tl, int tr, const vector<int>& a) {
        if (tl == tr) tree[v] = a[tl];
        else {
            int tm = (tl + tr) / 2;
            build(v * 2, tl, tm, a);
            build(v * 2 + 1, tm + 1, tr, a);
            tree[v] = max(tree[v * 2], tree[v * 2 + 1]);
        }
    }

    void update(int v, int tl, int tr, int pos, int val) {
        if (tl == tr) tree[v] = val;
        else {
            int tm = (tl + tr) / 2;
            if (pos <= tm) update(v * 2, tl, tm, pos, val);
            else update(v * 2 + 1, tm + 1, tr, pos, val);
            tree[v] = max(tree[v * 2], tree[v * 2 + 1]);
        }
    }

    int find_first(int v, int tl, int tr, int l, int r, int x) {
        if (tl > r || tr < l || tree[v] < x) return -1;
        if (tl == tr) return tl;
        int tm = (tl + tr) / 2;
        int res = find_first(v * 2, tl, tm, l, r, x);
        if (res != -1) return res;
        return find_first(v * 2 + 1, tm + 1, tr, l, r, x);
    }
};
```

---

## 3. Hall’s Marriage Theorem & Lazy SegTree Oracles

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Walkable Segment Tree (Find First >= X starting from L)
#include <bits/stdc++.h>
using namespace std;

struct WalkableSegTree {
    int n;
    vector<int> tree;

    WalkableSegTree(int n, const vector<int>& a) : n(n), tree(4 * n) {
        build(1, 0, n - 1, a);
    }

    void build(int v, int tl, int tr, const vector<int>& a) {
        if (tl == tr) tree[v] = a[tl];
        else {
            int tm = (tl + tr) / 2;
            build(v * 2, tl, tm, a);
            build(v * 2 + 1, tm + 1, tr, a);
            tree[v] = max(tree[v * 2], tree[v * 2 + 1]);
        }
    }

    void update(int v, int tl, int tr, int pos, int val) {
        if (tl == tr) tree[v] = val;
        else {
            int tm = (tl + tr) / 2;
            if (pos <= tm) update(v * 2, tl, tm, pos, val);
            else update(v * 2 + 1, tm + 1, tr, pos, val);
            tree[v] = max(tree[v * 2], tree[v * 2 + 1]);
        }
    }

    int find_first(int v, int tl, int tr, int l, int r, int x) {
        if (tl > r || tr < l || tree[v] < x) return -1;
        if (tl == tr) return tl;
        int tm = (tl + tr) / 2;
        int res = find_first(v * 2, tl, tm, l, r, x);
        if (res != -1) return res;
        return find_first(v * 2 + 1, tm + 1, tr, l, r, x);
    }
};
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
