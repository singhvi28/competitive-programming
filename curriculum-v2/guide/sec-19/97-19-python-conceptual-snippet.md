# Python Conceptual Snippet

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
import heapq

class SlopeTrick:
    def __init__(self):
        self.L = [] # Max-heap (store as negative)
        self.R = [] # Min-heap
        self.min_f = 0
        
    def add_abs(self, a):
        """Adds |x - a| to the function"""
        # Note: heapq is a min-heap. For Max-heap L, use -val.
        
        # 1. Handle Left side
        if self.L and a < -self.L[0]:
            self.min_f += (-self.L[0] - a)
            heapq.heappush(self.L, -a)
            heapq.heappush(self.L, -a)
            # Move the old max(L) to R to balance the slope=0 zone
            heapq.heappush(self.R, -heapq.heappop(self.L))
        # 2. Handle Right side
        elif self.R and a > self.R[0]:
            self.min_f += (a - self.R[0])
            heapq.heappush(self.R, a)
            heapq.heappush(self.R, a)
            # Move the old min(R) to L to balance
            heapq.heappush(self.L, -heapq.heappop(self.R))
        # 3. Inside the zero-slope zone
        else:
            heapq.heappush(self.L, -a)
            heapq.heappush(self.R, a)

    def get_min(self):
        return self.min_f
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
