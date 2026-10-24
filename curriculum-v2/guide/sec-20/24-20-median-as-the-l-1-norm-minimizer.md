# Median as the $L_1$ Norm Minimizer

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** High  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: High
- Rating Range: 1500–2100
- Core Invariant: Balancing subgradient sign counts

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Intermediate Greedy techniques bridge convex optimization and dynamic programming: Decoupled Dimension Sweeps, Slope Trick (piecewise linear convex function maintenance via priority queues), and WQS Binary Search (Alien's Trick).

### Fundamental Theorems & Invariants

- **Additive Independence & Chebyshev Transform:** In $\ell_1$ (Manhattan) and $\ell_\infty$ (Chebyshev) metrics, coordinate transformations $(x', y') = (x+y, x-y)$ decouple multi-dimensional distance minimization into independent 1D median problems.
- **Slope Trick Invariant:** Any continuous piecewise linear convex function $f(x)$ with integer slopes can be represented by its minimum value and two priority queues storing the inflection points where the slope changes by $+1$ and $-1$. Adding $|x - a|$ updates slope inflection points in $\mathcal{O}(\log N)$.
- **Alien's Trick / WQS Binary Search:** If the optimal value $OPT(k)$ as a function of choice count $k$ is strictly concave/convex, introducing a Lagrange multiplier penalty $\lambda$ removes the exact-count constraint, binary searching $\lambda$ in $\mathcal{O}(\text{BaseDP} \cdot \log(\text{Range})))$.

### Algorithmic Execution Blueprint

1. **Chebyshev Transformation:** Map each point $(x, y) \to (x+y, x-y)$. The maximum Chebyshev distance $\max(|x_1-x_2|, |y_1-y_2|)$ becomes $\frac{1}{2}(|x'_1-x'_2| + |y'_1-y'_2|)$.
2. **Slope Trick Maintenance:** Maintain left heap $L$ (max-heap) and right heap $R$ (min-heap). To add $|x - a|$: if $a < L.\text{top}()$, add cost $L.\text{top}() - a$, push $a$ twice to $L$, and move $L.\text{top}()$ to $R$.
3. **WQS Binary Search:** Binary search penalty $\lambda$. Run unconstrained DP where each selection costs $+\lambda$. If optimal selections count $> k$, increase $\lambda$.

### Closed-Form Invariant Equations

$$f_{new}(x) = f(x) + |x - a|, \quad \text{WQS}: \min_k \big(dp[k] - \lambda k\big) \iff \text{Lagrangian Duality}$$

### Structural Edge Cases & Assumptions

- Slope Trick requires the underlying objective function to be strictly convex; non-convex cost functions require general CHT or DP.
- In WQS Binary Search, collinear points (flat segments in the convex hull of $OPT(k)$) require careful tie-breaking (preferring max count or min count) to avoid binary search oscillation.

---

## 3. Core Intuition & Problem Framing

Consider the convex cost function $C(x) = \sum_{i=1}^N |x - a_i|$ with sorted $a_1 \le a_2 \le \dots \le a_N$.
Take the derivative (subgradient) with respect to $x$:
$$\frac{d}{dx} |x - a_i| = \text{sgn}(x - a_i) = \begin{cases} +1 & \text{if } x > a_i \\ -1 & \text{if } x < a_i \end{cases}$$
Summing across all points:
$$\frac{d}{dx} C(x) = \sum_{i=1}^N \text{sgn}(x - a_i) = (\# \text{ points to the left of } x) - (\# \text{ points to the right of } x)$$
- If $x$ is to the left of the median, $(\# \text{ left}) < (\# \text{ right}) \implies C'(x) < 0$, so moving $x$ right **decreases** cost.
- If $x$ is to the right of the median, $(\# \text{ left}) > (\# \text{ right}) \implies C'(x) > 0$, so moving $x$ left **decreases** cost.
- The global minimum occurs where $C'(x) = 0 \iff (\# \text{ left}) = (\# \text{ right})$, which is precisely the **Median**.

---

## 4. Proof Sketches & Recurrences

To maintain the median of a dynamic set under insertions and deletions in $O(\log N)$:
1. Maintain **`L`** (Max-Heap) storing the smaller half and **`R`** (Min-Heap) storing the larger half.
2. Invariant: $\text{size}(L) \in \{\text{size}(R), \text{size}(R) + 1\}$ and $\max(L) \le \min(R)$.
3. Median is always $\text{top}(L)$.

```cpp
// C++17 — Dynamic Running Median with Lazy Deletions
#include <bits/stdc++.h>
using namespace std;

class DynamicMedian {
    priority_queue<long long> L; // max-heap
    priority_queue<long long, vector<long long>, greater<long long>> R; // min-heap
    unordered_map<long long, int> delayed;
    int size_L = 0, size_R = 0;

    void clean(auto& pq, int sign) {
        while (!pq.empty()) {
            long long val = pq.top();
            if (delayed[val] > 0) {
                delayed[val]--;
                pq.pop();
            } else break;
        }
    }

    void rebalance() {
        if (size_L > size_R + 1) {
            R.push(L.top()); L.pop();
            size_L--; size_R++;
            clean(L, 1);
        } else if (size_L < size_R) {
            L.push(R.top()); R.pop();
            size_L++; size_R--;
            clean(R, -1);
        }
    }

public:
    void insert(long long x) {
        if (L.empty() || x <= L.top()) {
            L.push(x); size_L++;
        } else {
            R.push(x); size_R++;
        }
        rebalance();
    }

    void erase(long long x) {
        delayed[x]++;
        if (!L.empty() && x <= L.top()) size_L--;
        else size_R--;
        clean(L, 1); clean(R, -1);
        rebalance();
    }

    long long get_median() {
        clean(L, 1);
        return L.top();
    }
};
```

---

## 3. Prefix-Suffix Sweeps & Block Compression

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Dynamic Running Median with Lazy Deletions
#include <bits/stdc++.h>
using namespace std;

class DynamicMedian {
    priority_queue<long long> L; // max-heap
    priority_queue<long long, vector<long long>, greater<long long>> R; // min-heap
    unordered_map<long long, int> delayed;
    int size_L = 0, size_R = 0;

    void clean(auto& pq, int sign) {
        while (!pq.empty()) {
            long long val = pq.top();
            if (delayed[val] > 0) {
                delayed[val]--;
                pq.pop();
            } else break;
        }
    }

    void rebalance() {
        if (size_L > size_R + 1) {
            R.push(L.top()); L.pop();
            size_L--; size_R++;
            clean(L, 1);
        } else if (size_L < size_R) {
            L.push(R.top()); R.pop();
            size_L++; size_R--;
            clean(R, -1);
        }
    }

public:
    void insert(long long x) {
        if (L.empty() || x <= L.top()) {
            L.push(x); size_L++;
        } else {
            R.push(x); size_R++;
        }
        rebalance();
    }

    void erase(long long x) {
        delayed[x]++;
        if (!L.empty() && x <= L.top()) size_L--;
        else size_R--;
        clean(L, 1); clean(R, -1);
        rebalance();
    }

    long long get_median() {
        clean(L, 1);
        return L.top();
    }
};
```

---

## 6. Recognition Trigger Signals & Heuristics

- If each point $a_i$ carries a positive weight $w_i$, the cost is $C(x) = \sum_{i=1}^N w_i |x - a_i|$.
The derivative becomes:
$$\frac{d}{dx} C(x) = \sum_{a_i < x} w_i - \sum_{a_i > x} w_i$$
The optimum is reached at the **Weighted Median**: the smallest $a_k$ such that the cumulative weight reaches at least half the total weight:
$$\sum_{i=1}^k w_i \ge \frac{1}{2} \sum_{i=1}^N w_i$$

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-713C | Sonya and Problem Wihtout a Legend | 2300 | Slope Trick, Priority Queue, Convexity | Slope Trick with max-heap maintaining slope change points of convex cost function in O(N log N). | [Solve Problem](https://codeforces.com/contest/713/problem/C) |
| Codeforces | CF-1279F | New Year and Handle Change | 2600 | Aliens Trick, WQS Binary Search, DP | Aliens Trick / WQS binary search penalizing each operation by lambda. | [Solve Problem](https://codeforces.com/contest/1279/problem/F) |
| Codeforces | CF-1534E | Lost Array | 2300 | Greedy, BFS, Parity | Shortest path BFS over odd/even bit counts or balanced decoupled greedy assignment. | [Solve Problem](https://codeforces.com/contest/1534/problem/E) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Slope Trick Tutorial (zscoder / SleepingCup)](https://codeforces.com/blog/entry/77298)
- **[Codeforces]** [Codeforces Blog: The Alien's Trick (WQS Binary Search / Lagrangian Relaxation)](https://codeforces.com/blog/entry/49691)

---
