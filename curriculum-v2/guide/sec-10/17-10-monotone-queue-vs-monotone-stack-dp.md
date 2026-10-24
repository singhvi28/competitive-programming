# Monotone queue vs monotone stack DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Two Pointers, Monotone Deque, Monotone Stack
- Tradeoff: Sliding window extrema vs nearest smaller/larger bounding indices.

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

1) **Monotone Queue (Deque)** optimizes DP transitions over a sliding window: $dp[i] = \min_{i - W \le j < i} (dp[j]) + c_i$. The window boundaries $[i - W, i - 1]$ move monotonically to the right. A deque maintains candidate values in increasing order of cost and pops elements from the front when they fall out of the sliding window, achieving $\mathcal{O}(1)$ amortized transition. 2) **Monotone Stack** finds nearest greater/smaller elements for each position $i$ (e.g. largest rectangle in histogram, finding the maximal subsegment where $a_i$ is the minimum). The stack pops elements that violate monotonicity, but does NOT enforce a sliding window length.

---

## 4. Proof Sketches & Recurrences

Monotone Deque invariant: for indices $j_1 < j_2$ stored in the deque, we must have $dp[j_1] < dp[j_2]$. If a newly considered index $i$ has $dp[i] \le dp[j]$, then $j$ can never be the optimum for any future window containing $i$, because $i$ is both smaller and lives longer. Thus, elements with $\ge dp[i]$ are popped from the back. Since every index is pushed and popped at most once, total amortized time across all $N$ steps is $\mathcal{O}(N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Monotone Queue DP: Sliding Window Min Transition in O(N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> sliding_window_min_dp(int n, int k, const vector<ll>& cost) {
    vector<ll> dp(n + 1, 0);
    deque<int> dq;
    dq.push_back(0); // dp[0] = 0
    for (int i = 1; i <= n; ++i) {
        // Pop elements outside window [i - k, i - 1]
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        dp[i] = dp[dq.front()] + cost[i - 1];
        // Maintain monotonic increasing order in deque
        while (!dq.empty() && dp[dq.back()] >= dp[i]) dq.pop_back();
        dq.push_back(i);
    }
    return dp;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- DP transition looks like $dp[i] = \min_{j \in [i - L, i - R]} dp[j] + f(i)$ (Monotone Queue).
- Finding the left and right boundary where $a[i]$ remains the minimum/maximum of the range (Monotone Stack).
- Sliding window maximum/minimum in an array (Monotone Queue).
- Histogram rectangle area or Cartesian Tree construction (Monotone Stack).

---

## 7. Contest WA / TLE / RE Traps

- Empty deque access: calling `dq.front()` before verifying `!dq.empty()`.
- Popping order confusion: front is popped for window expiry (`dq.front() < i - k`), back is popped for monotonicity (`dp[dq.back()] >= dp[i]`).
- Strict vs non-strict inequalities: duplicate values can cause improper early popping in monotone stack problems.
- Index offset errors between 0-indexed arrays and 1-indexed DP arrays.

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
