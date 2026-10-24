# 5. Monotone queue optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** DP, `deque`, sliding-window minimum  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: DP, `deque`, sliding-window minimum

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

When

\[
dp[i]=\min_{i-w\le j\le i-1} \bigl(dp[j]+f(j)\bigr)+g(i)
\]

(or any form where the best \(j\) in a **sliding window** is what you need), candidates that are older and worse than a newer one are never useful again. Maintain a deque of indices with **increasing \(dp[j]+f(j)\)** (for min); pop front out of window; pop back dominated. Each index enter/leave once → \(O(n)\).

---

## 4. Proof Sketches & Recurrences

Let \(v[j]=dp[j]+f(j)\). Need \(\min_{j\in[L_i,R_i]} v[j]\). If \(L_i,R_i\) both nondecreasing (sliding), deque works. Amortized \(O(1)\) per \(i\): each \(j\) pushed/popped ≤ once.

If \(cost(j,i)\) is not separable, you need **D&C / CHT / QI** instead — monotone queue alone is insufficient.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) if `add`/`fee` ready
- Per-query / per-operation: amortized \(O(1)\) per index
- Total: \(O(n)\) per DP layer
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — sliding-window DP: dp[i] = min_{i-W <= j < i} dp[j] + add(j) + fee(i)
#include <bits/stdc++.h>
using namespace std;

namespace mono_queue_dp {
using ll = long long;
const ll INF = 4e18;

vector<ll> solve(int n, int W, const vector<ll>& fee,
                 function<ll(int)> add) {
    // fee, add 1-indexed; dp[0]=0
    vector<ll> dp(n + 1, INF);
    dp[0] = 0;
    deque<int> dq; // stores j, increasing v[j]=dp[j]+add(j)
    auto val = [&](int j) { return dp[j] + add(j); };
    for (int i = 1; i <= n; ++i) {
        // push i-1 as candidate end
        int j = i - 1;
        while (!dq.empty() && val(dq.back()) >= val(j)) dq.pop_back();
        dq.push_back(j);
        while (!dq.empty() && dq.front() < i - W) dq.pop_front();
        if (!dq.empty()) dp[i] = val(dq.front()) + fee[i];
    }
    return dp;
}
} // namespace mono_queue_dp
```

### Python 3 Template

```python
from collections import deque

INF = 10**30

def mono_queue_dp(n, W, fee, add):
    # fee[1..n], add(j) callable; dp[0]=0
    dp = [INF] * (n + 1)
    dp[0] = 0
    dq = deque()
    def val(j): return dp[j] + add(j)
    for i in range(1, n + 1):
        j = i - 1
        while dq and val(dq[-1]) >= val(j):
            dq.pop()
        dq.append(j)
        while dq and dq[0] < i - W:
            dq.popleft()
        if dq:
            dp[i] = val(dq[0]) + fee[i]
    return dp
```

---

## 6. Recognition Trigger Signals & Heuristics

- Fixed window length \(w\): “last at most \(w\) steps”.
- \(dp[i]=\min_{j\in[i-r,i-l]} dp[j]+cost\) with cost separable as \(A_j+B_i\).
- Multiple knapsacks with bounded consecutive choices.
- After rewriting, transition depends only on a range-min of a precomputed array.
- **Vs monotone stack:** queue = window by index distance; stack = window by value dominance (next greater).

---

## 7. Contest WA / TLE / RE Traps

- Window bounds: `[i-W, i-1]` vs `[i-W, i]` inclusive mistakes.
- Pop condition `>` vs `>=` (strictness / stability).
- Pushing `i` before computing `dp[i]` (use `i-1`).
- Non-separable cost — queue gives wrong answer.
- Multiple layers forgetting to clear deque.

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

## 10. Algorithmic Variants & Advanced Extensions

- **Max** queue: reverse inequalities.
- **Two ends** / different \(L_i,R_i\) if both monotone.
- **0-1 knapsack** monotone queue on residual capacity (bounded item count).
- Combine with binary lifting / sparse table if windows arbitrary (not sliding) — different tool.

---

## 11. Typical Problem Archetypes

1. Standard: jump game with window costs; hotel stays within \(k\) days.
2. Slightly disguised: rearrange recurrence until `min` of `dp[j]+add[j]` appears.
3. Difficult: monotone queue inside each residue class (mod \(k\)).
4. Very difficult: queue + CHT hybrid when both structures appear.

---

## 12. Recognition & Identification Drills

1. \(dp[i]=\min_{i-k\le j<i} dp[j]+|a_i-a_j|\). Separable? Queue?
2. Partition into groups of length in \([L,R]\); cost = group sum squared.
3. Bounded knapsack: at most \(c\) copies of item weight \(w\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: sliding-window min/max of DP candidates.
- Key invariant: deque increasing by key; front = best.
- Key formula: \(dp[i]=\min_{j\in window} (dp[j]+f[j])+g[i]\).
- Complexity: \(O(n)\).
- Template to remember: pop back dominated; pop front out of window.

**Simpler DP passes when:** \(n\cdot W\) small — nested loops fine.

---

## 6. Monotone stack DP

---
