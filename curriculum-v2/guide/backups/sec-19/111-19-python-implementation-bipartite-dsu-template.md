# Python Implementation: Bipartite DSU Template

> **Section:** §19 Greedy Fundamentals & Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Greedy Fundamentals establish formal proof techniques and data structure invariants for greedy optimization: Exchange Arguments, Stays-Ahead Invariants, and Priority Queue Regret / Undo Maintenance.

### Fundamental Theorems & Invariants

- **Exchange Argument Theorem:** To prove greedy sorting criteria $A < B$ is optimal, assume an optimal solution violates the order. Show that swapping adjacent out-of-order elements cannot worsen the objective function.
- **Smith's Rule for Scheduling:** When scheduling $N$ jobs with processing time $p_i$ and weight $w_i$ to minimize weighted completion time $\sum w_i C_i$, sorting in descending order of $\frac{w_i}{p_i}$ is strictly optimal.
- **Regret / Undo Heap Invariant:** When choices cannot be verified greedily upfront, accept the current greedy choice optimistically; if constraints are violated later, undo the worst prior choice by popping from a priority queue.

### Algorithmic Execution Blueprint

1. **Deriving Exchange Condition:** Write objective for pair $(i, j)$ in order $i$ then $j$ vs $j$ then $i$. Cancel common terms to isolate sorting comparator `return w[i] * p[j] > w[j] * p[i]`.
2. **Regret Heap (e.g. Potions):** Iterate through events; add current item. If health becomes negative, pop and reverse the effect of the most punishing past item from `priority_queue`.

### Closed-Form Invariant Equations

$$\text{Exchange Condition}: \quad \text{Cost}(i, j) \le \text{Cost}(j, i) \iff \frac{w_i}{p_i} \ge \frac{w_j}{p_j}$$

### Structural Edge Cases & Assumptions

- Comparators passed to `std::sort` must satisfy Strict Weak Ordering ($a < a$ must return `false`).
- Greedy exchange arguments require pairwise independence; if choice $i$ alters the available choices for subsequent elements non-linearly, DP or flows are required.

---

## 5. Contest-Ready Implementation Templates

### Python 3 Template

```python
import sys

# Increase recursion depth for deep DSU trees
sys.setrecursionlimit(200000)

class BipartiteDSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.dist = [0] * (n + 1) # Parity relative to parent
        self.size = [1] * (n + 1)
        self.is_bipartite = True

    def find(self, i):
        if self.parent[i] == i:
            return i, 0
        
        # Path compression with parity update
        root, root_dist = self.find(self.parent[i])
        self.parent[i] = root
        self.dist[i] = (self.dist[i] + root_dist) % 2
        return self.parent[i], self.dist[i]

    def union(self, u, v):
        root_u, p_u = self.find(u)
        root_v, p_v = self.find(v)

        if root_u != root_v:
            # Union by size
            if self.size[root_u] < self.size[root_v]:
                root_u, root_v = root_v, root_u
                p_u, p_v = p_v, p_u
            
            self.parent[root_v] = root_u
            # The edge (u, v) must have parity 1
            # p_u + new_edge_dist + p_v = 1 (mod 2)
            self.dist[root_v] = (p_u + p_v + 1) % 2
            self.size[root_u] += self.size[root_v]
            return True
        else:
            # Check for conflict
            if p_u == p_v:
                self.is_bipartite = False
                return False
            return True
```

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1526C2 | Potions (Hard Version) | 1600 | Regret Heap, Greedy Invariants | Regret / Undo Heap: greedily drink potion; if health < 0, pop and un-drink the most negative potion. | [Solve Problem](https://codeforces.com/contest/1526/problem/C2) |
| Codeforces | CF-864D | Make a Permutation! | 1600 | Greedy, Frequencies | Greedy choice with frequency counters and skip-if-first-occurrence flags. | [Solve Problem](https://codeforces.com/contest/864/problem/D) |
| Codeforces | CF-1157C2 | Increasing Subsequence (hard version) | 1700 | Greedy, Two Pointers | Greedy two-pointer picks smaller side; if equal, simulate strictly longest run on both sides. | [Solve Problem](https://codeforces.com/contest/1157/problem/C2) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Greedy Exchange Arguments (Errichto)](https://codeforces.com/blog/entry/66734)
- **[USACO Guide]** [USACO Guide: Priority Queue Regret / Undo Heaps](https://usaco.guide/silver/greedy-sorting)

---
