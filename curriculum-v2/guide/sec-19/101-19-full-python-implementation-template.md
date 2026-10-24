# Full Python Implementation Template

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
        # L is a Max-Heap. In Python, we store -val to simulate Max-Heap.
        self.L = [] 
        self.R = [] 
        self.min_f = 0
        self.off_L = 0
        self.off_R = 0

    def add_abs(self, a):
        """Adds |x - a| to the current function f(x)"""
        # Current actual boundaries of the zero-slope (min) region:
        left_max = -self.L[0] + self.off_L if self.L else float('-inf')
        right_min = self.R[0] + self.off_R if self.R else float('inf')

        if a < left_max:
            # Case 1: a is to the left of the minimum region
            # We add |x - a| which has slope -1 here.
            self.min_f += abs(left_max - a)
            # Push a into L twice (to change slope from 0 to -1 to -2...)
            heapq.heappush(self.L, -(a - self.off_L))
            heapq.heappush(self.L, -(a - self.off_L))
            # Move one from L to R to restore the 0-slope segment
            val = -heapq.heappop(self.L) + self.off_L
            heapq.heappush(self.R, val - self.off_R)
        elif a > right_min:
            # Case 2: a is to the right of the minimum region
            self.min_f += abs(a - right_min)
            heapq.heappush(self.R, a - self.off_R)
            heapq.heappush(self.R, a - self.off_R)
            val = heapq.heappop(self.R) + self.off_R
            heapq.heappush(self.L, -(val - self.off_L))
        else:
            # Case 3: a is within the [left_max, right_min] range
            heapq.heappush(self.L, -(a - self.off_L))
            heapq.heappush(self.R, a - self.off_R)

    def shift_range(self, dl, dr):
        """Shifts L boundary by dl and R boundary by dr"""
        self.off_L += dl
        self.off_R += dr

# Example Usage: Solve CF 713C (Make array strictly increasing)
# Trick: a[i] < a[i+1]  =>  a[i]-i <= a[i+1]-(i+1). 
# Let b[i] = a[i] - i. Now we need b[i] <= b[i+1] (non-decreasing).
def solve():
    import sys
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    st = SlopeTrick()
    for i in range(n):
        b_i = a[i] - i
        st.add_abs(b_i)
        # To handle b[i] <= b[i+1], we take the prefix minimum:
        # Clear the right heap (positive slopes)
        st.R = [] 
    print(st.min_f)
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
