# 13. Digit DP Template

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Frequent  
> **Prerequisites:** Top-down DP (Memoization)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Frequent
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Top-down DP (Memoization)

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

Whenever a problem asks to count the number of integers in $[L, R]$ satisfying a certain property, we compute $solve(R) - solve(L-1)$. 
To compute $solve(X)$, we construct the number digit by digit from the most significant to the least significant. We maintain a `tight` boolean flag: if `tight` is true, the digits we can place are bounded by the current digit of $X$. If `tight` is false, we can place any digit from 0 to 9. We also often maintain a `leading_zero` boolean.

---

## 4. Proof Sketches & Recurrences

```cpp
#include <bits/stdc++.h>
using namespace std;

string S;
long long memo[20][2][2][100]; // [idx][tight][lead_zero][custom_state]

long long dp(int idx, bool tight, bool lead, int state) {
    if (idx == S.length()) {
        return (state == target) ? 1 : 0; // custom condition
    }
    if (memo[idx][tight][lead][state] != -1)
        return memo[idx][tight][lead][state];
        
    long long res = 0;
    int limit = tight ? (S[idx] - '0') : 9;
    
    for (int d = 0; d <= limit; ++d) {
        bool next_tight = tight && (d == limit);
        bool next_lead = lead && (d == 0);
        int next_state = state; // transition logic for state based on 'd'
        
        res += dp(idx + 1, next_tight, next_lead, next_state);
    }
    return memo[idx][tight][lead][state] = res;
}

long long solve(long long X) {
    if (X < 0) return 0;
    S = to_string(X);
    memset(memo, -1, sizeof(memo));
    return dp(0, true, true, 0);
}
```

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

string S;
long long memo[20][2][2][100]; // [idx][tight][lead_zero][custom_state]

long long dp(int idx, bool tight, bool lead, int state) {
    if (idx == S.length()) {
        return (state == target) ? 1 : 0; // custom condition
    }
    if (memo[idx][tight][lead][state] != -1)
        return memo[idx][tight][lead][state];
        
    long long res = 0;
    int limit = tight ? (S[idx] - '0') : 9;
    
    for (int d = 0; d <= limit; ++d) {
        bool next_tight = tight && (d == limit);
        bool next_lead = lead && (d == 0);
        int next_state = state; // transition logic for state based on 'd'
        
        res += dp(idx + 1, next_tight, next_lead, next_state);
    }
    return memo[idx][tight][lead][state] = res;
}

long long solve(long long X) {
    if (X < 0) return 0;
    S = to_string(X);
    memset(memo, -1, sizeof(memo));
    return dp(0, true, true, 0);
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- "Count the number of $X \in [A, B]$ such that..."
- $B$ is very large (e.g., $10^{18}$ or even 100,000 digits long).

---

## 7. Contest WA / TLE / RE Traps

- Memoizing tight states: storing DP results when $tight = 1$ is fatal because the result depends on the specific prefix digits of $X$, not just the suffix state.
- Ignoring leading zeros: numbers like `007` have length 1, but digit DP will treat them as length 3 with leading zero digits unless a `leading_zero` flag is maintained.
- Off-by-one in $[L, R]$: when calculating $f(R) - f(L - 1)$, make sure $L = 0$ is handled safely without negative bounds.
- Forgetting to clear or reset the memoization table between multiple test cases.

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
