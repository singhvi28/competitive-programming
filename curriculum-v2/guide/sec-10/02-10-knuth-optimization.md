# 2. Knuth optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Interval DP, quadrangle inequality, opt-monotonicity lemma (Knuth–Yao)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Interval DP, quadrangle inequality, opt-monotonicity lemma (Knuth–Yao)

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

Classic interval DP:

\[
dp[l][r]=\min_{k=l}^{r-1}\bigl(dp[l][k]+dp[k+1][r]\bigr)+C(l,r)
\]

is \(O(n^3)\). If \(C\) satisfies the **quadrangle inequality** and is monotone on intervals, then

\[
opt[l][r-1]\le opt[l][r]\le opt[l+1][r]
\]

so when computing increasing length, the search range for \(k\) shrinks and total work becomes \(O(n^2)\).

---

## 4. Proof Sketches & Recurrences

Knuth–Yao speedup: under QI + monotonicity of \(C\), the argmin \(opt[l][r]\) is monotone as above. Loop:

```
for len = 2..n:
  for l = 1..n-len+1:
    r = l+len-1
    for k = opt[l][r-1] .. opt[l+1][r]:
      update dp[l][r], opt[l][r]
```

Each cell still examines a range, but amortized \(\sum (opt[l+1][r]-opt[l][r-1]) = O(n^2)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)–\(O(n^2)\) for \(C\)
- Per-query / per-operation: N/A
- Total: \(O(n^2)\) under Knuth conditions (vs \(O(n^3)\) naive)
- Memory: \(O(n^2)\) for `dp` and `opt``

### C++17 Template

```cpp
// C++17 — Knuth-optimized interval DP
#include <bits/stdc++.h>
using namespace std;

namespace knuth_dp {
using ll = long long;
const ll INF = 4e18;

// cost(l,r) inclusive, O(1)
pair<vector<vector<ll>>, vector<vector<int>>>
solve(int n, function<ll(int,int)> cost) {
    vector<vector<ll>> dp(n + 2, vector<ll>(n + 2, 0));
    vector<vector<int>> opt(n + 2, vector<int>(n + 2, 0));
    for (int i = 1; i <= n; ++i) {
        opt[i][i] = i;
        // dp[i][i] = 0; // or cost(i,i) depending on problem
    }
    for (int len = 2; len <= n; ++len) {
        for (int l = 1; l + len - 1 <= n; ++l) {
            int r = l + len - 1;
            dp[l][r] = INF;
            int ol = opt[l][r - 1];
            int orr = opt[l + 1][r];
            if (ol < l) ol = l;
            if (orr > r - 1) orr = r - 1;
            for (int k = ol; k <= orr; ++k) {
                ll val = dp[l][k] + dp[k + 1][r] + cost(l, r);
                if (val < dp[l][r]) {
                    dp[l][r] = val;
                    opt[l][r] = k;
                }
            }
        }
    }
    return {dp, opt};
}
} // namespace knuth_dp
```

### Python 3 Template

```python
INF = 10**30

def knuth(n, cost):
    dp = [[0]*(n+2) for _ in range(n+2)]
    opt = [[0]*(n+2) for _ in range(n+2)]
    for i in range(1, n+1):
        opt[i][i] = i
    for length in range(2, n+1):
        for l in range(1, n-length+2):
            r = l + length - 1
            dp[l][r] = INF
            lo, hi = opt[l][r-1], opt[l+1][r]
            lo, hi = max(lo, l), min(hi, r-1)
            for k in range(lo, hi+1):
                val = dp[l][k] + dp[k+1][r] + cost(l, r)
                if val < dp[l][r]:
                    dp[l][r], opt[l][r] = val, k
    return dp, opt
```

---

## 6. Recognition Trigger Signals & Heuristics

- Matrix chain multiplication shape; optimal BST; splitting arrays with cost on full interval.
- \(C(l,r)=w(l,r)\) where \(w\) is sum of weights on \([l,r]\) (optimal BST).
- You already have \(dp\) by length; you maintain `opt[l][r]` = best split.
- QI: \(C(a,c)+C(b,d)\le C(a,d)+C(b,c)\) for \(a\le b\le c\le d\).
- Vs D&C:** if the DP is **two intervals combining** (binary tree of merges), think Knuth; if **last segment cut** against previous layer, think D&C.

---

## 7. Contest WA / TLE / RE Traps

- Applying Knuth without QI → WA.
- Wrong initialization of `opt[l][l]` / empty intervals.
- Loop order: must increase length; need `opt[l][r-1]` and `opt[l+1][r]` already computed.
- Adding \(C(l,r)\) twice or outside the min incorrectly.
- Off-by-one when \(k\) ranges for length 2.

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

- **Optimal BST**: \(C(l,r)=\sum_{i=l}^{r} w_i\) (prefix); Knuth applies.
- **Matrix chain**: similar structure; cost of multiplying dimensions.
- **Maximize** versions with reversed inequalities (rare).
- If only QI fails mildly, sometimes still works — don’t rely on that.

---

## 11. Typical Problem Archetypes

1. Standard: optimal BST / merging files with cumulative cost.
2. Slightly disguised: stone merging (Chinese classic) with sum costs.
3. Difficult: cost is more complex but still QI.
4. Very difficult: choose between Knuth and D&C when both seem plausible — match recurrence shape.

---

## 12. Recognition & Identification Drills

1. Merge \(n\) adjacent piles; cost of merge = sum of sizes in range; minimize total.
2. Interval DP where \(C(l,r)=w[r]-w[l-1]\). What is `opt` monotonicity?
3. Same merge but cost = max pile in range. Does Knuth apply?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: interval DP + QI + monotone opt.
- Key invariant: \(opt[l][r-1]\le opt[l][r]\le opt[l+1][r]\).
- Key formula: \(dp[l][r]=\min_k dp[l][k]+dp[k+1][r]+C(l,r)\).
- Complexity: \(O(n^2)\).
- Template to remember: loop length; \(k\) from `opt[l][r-1]` to `opt[l+1][r]`.

**Simpler DP passes when:** \(n\le 400\) for \(O(n^3)\); don’t force Knuth early.

---

## 3. Convex Hull Trick

---
