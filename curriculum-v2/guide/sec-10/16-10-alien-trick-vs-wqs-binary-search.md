# 16. Alien trick vs WQS binary search

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 D/E & ICPC Regionals
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Convex Optimization, Lagrange Multipliers, Binary Search, DP
- Tradeoff: Eliminates a state dimension $K$ (e.g. choose exactly $K$ items) from $\mathcal{O}(N K)$ down to $\mathcal{O}(N \log(\text{cost}))$.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

## 3. Core Intuition & Problem Framing

Alien's Trick and WQS Binary Search are two names for the same algorithmic technique: Lagrangian relaxation applied to convex DP. When the maximum profit $f(k)$ as a function of the number of chosen items $k$ is strictly concave (or convex for cost minimization), the constraint 'choose exactly $K$ items' can be relaxed by introducing a penalty $\lambda$ for each chosen item. By binary searching on $\lambda$, we find the slope of the tangent line touching the curve at $k = K$, solving the problem without maintaining $k$ in the DP state!

---

## 4. Proof Sketches & Recurrences

Let $g(\lambda) = \max_k (f(k) - \lambda k)$. The function $g(\lambda)$ is the Legendre transform of $f(k)$. For a fixed $\lambda$, the unconstrained problem $\max_k (f(k) - \lambda k)$ can be evaluated in $\mathcal{O}(N)$ time, returning both the optimal value and the number of items chosen $k^*$. Since $f$ is concave, the optimal $k^*(\lambda)$ is a monotonically decreasing function of $\lambda$. Binary search on $\lambda$ finds $\lambda^*$ such that $k^*(\lambda^*) = K$. The original answer is then $g(\lambda^*) + \lambda^* K$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Aliens Trick / WQS Binary Search Template
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// Solve unconstrained DP with penalty lambda per item
pair<ll, int> solve_unconstrained(ll lambda, int n);

ll aliens_trick(int n, int k, ll low_penalty, ll high_penalty) {
    ll l = low_penalty, r = high_penalty, best_lambda = 0;
    while (l <= r) {
        ll mid = l + (r - l) / 2;
        auto [val, cnt] = solve_unconstrained(mid, n);
        if (cnt >= k) {
            best_lambda = mid;
            l = mid + 1; // Increase penalty to pick fewer items
        } else {
            r = mid - 1;
        }
    }
    auto [val, cnt] = solve_unconstrained(best_lambda, n);
    return val + best_lambda * k;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Problem specifies 'choose exactly $K$ disjoint subsegments/elements' to maximize/minimize total weight.
- Standard DP is $dp[i][k]$ taking $\mathcal{O}(N K)$ or $\mathcal{O}(N^2 K)$, where $K, N \le 2 \times 10^5$.
- Plotting or mathematically checking $f(k)$ shows diminishing returns (strict concavity / quadrangle inequality).
- Tree partitioning into exactly $K$ connected components with optimal weight.

---

## 7. Contest WA / TLE / RE Traps

- Function $f(k)$ is not concave/convex; applying Aliens trick on non-convex functions yields completely wrong answers.
- Collinear points on the hull: multiple values of $k$ share the same slope $\lambda$. When tie-breaking, consistently choose either the minimum or maximum items chosen to ensure binary search converges.
- Off-by-one in binary search range $[\text{low}, \text{high}]$: penalty bounds must cover $[-2 \times \max|v|, 2 \times \max|v|]$.
- Forgetting to add back the penalty `+ best_lambda * k` to the final answer.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---
