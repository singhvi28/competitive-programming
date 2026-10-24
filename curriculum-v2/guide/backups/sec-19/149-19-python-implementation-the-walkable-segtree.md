# Python Implementation: The Walkable SegTree

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
class WalkableSegTree:
    def __init__(self, n, data):
        self.n = n
        self.tree = [0] * (4 * n)
        self.build(data, 1, 0, n - 1)

    def build(self, data, v, tl, tr):
        if tl == tr:
            self.tree[v] = data[tl]
        else:
            tm = (tl + tr) // 2
            self.build(data, v * 2, tl, tm)
            self.build(data, v * 2 + 1, tm + 1, tr)
            self.tree[v] = max(self.tree[v * 2], self.tree[v * 2 + 1])

    def update(self, v, tl, tr, pos, new_val):
        """Standard Point Update"""
        if tl == tr:
            self.tree[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v * 2, tl, tm, pos, new_val)
            else:
                self.update(v * 2 + 1, tm + 1, tr, pos, new_val)
            self.tree[v] = max(self.tree[v * 2], self.tree[v * 2 + 1])

    def find_first(self, v, tl, tr, x):
        """Finds the first index i in [0, N-1] where A[i] >= x"""
        if self.tree[v] < x:
            return -1
        if tl == tr:
            return tl
            
        tm = (tl + tr) // 2
        if self.tree[v * 2] >= x:
            return self.find_first(v * 2, tl, tm, x)
        else:
            return self.find_first(v * 2 + 1, tm + 1, tr, x)
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
