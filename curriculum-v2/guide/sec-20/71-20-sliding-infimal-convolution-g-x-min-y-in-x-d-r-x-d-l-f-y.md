# Sliding / Infimal Convolution: $g(x) = \min_{y \in [x - d_R, x - d_L]} f(y)$

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

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

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Complete Slope Trick Class
#include <bits/stdc++.h>
using namespace std;

class SlopeTrick {
public:
    long long min_f = 0;
    long long off_L = 0, off_R = 0;
    priority_queue<long long> L; // Max-heap
    priority_queue<long long, vector<long long>, greater<long long>> R; // Min-heap

    // Adds |x - a| to f(x)
    void add_abs(long long a) {
        long long l_max = L.empty() ? -1e18 : (L.top() + off_L);
        long long r_min = R.empty() ? 1e18 : (R.top() + off_R);

        if (a < l_max) {
            min_f += (l_max - a);
            L.push(a - off_L);
            L.push(a - off_L);
            long long move_val = L.top() + off_L;
            L.pop();
            R.push(move_val - off_R);
        } else if (a > r_min) {
            min_f += (a - r_min);
            R.push(a - off_R);
            R.push(a - off_R);
            long long move_val = R.top() + off_R;
            R.pop();
            L.push(move_val - off_L);
        } else {
            L.push(a - off_L);
            R.push(a - off_R);
        }
    }

    // Adds max(0, a - x) (only left-sloping penalty)
    void add_left_penalty(long long a) {
        long long r_min = R.empty() ? 1e18 : (R.top() + off_R);
        if (a > r_min) {
            min_f += (a - r_min);
            R.push(a - off_R);
            long long move_val = R.top() + off_R;
            R.pop();
            L.push(move_val - off_L);
        } else {
            L.push(a - off_L);
        }
    }

    // Adds max(0, x - a) (only right-sloping penalty)
    void add_right_penalty(long long a) {
        long long l_max = L.empty() ? -1e18 : (L.top() + off_L);
        if (a < l_max) {
            min_f += (l_max - a);
            L.push(a - off_L);
            long long move_val = L.top() + off_L;
            L.pop();
            R.push(move_val - off_R);
        } else {
            R.push(a - off_R);
        }
    }

    // Prefix minimum: g(x) = min_{y <= x} f(y)
    void prefix_min() {
        while (!R.empty()) R.pop();
    }

    // Suffix minimum: g(x) = min_{y >= x} f(y)
    void suffix_min() {
        while (!L.empty()) L.pop();
    }

    // Horizontal shift: expands minimum range by [dL, dR]
    void shift_range(long long dL, long long dR) {
        off_L += dL;
        off_R += dR;
    }

    long long get_min() const {
        return min_f;
    }
};
```

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
