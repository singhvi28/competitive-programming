# Bitset DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Bitset / bitwise ops, classic knapsack & Floyd-like DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Bitset / bitwise ops, classic knapsack & Floyd-like DP

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

Boolean (or small-int mod) DP over a large universe of sums/positions can be packed into machine words. Shifting and OR-ing a `std::bitset` or raw `uint64_t[]` gives a **\(64\times\)** (or word-size) speedup on transitions like “reach new sum = old sum + w”. Same idea for path existence, digit DP compressions, and some \(O(n^3)/64\) graph problems.

---

## 4. Proof Sketches & Recurrences

Subset sum:

```
bitset<S+1> dp; dp[0]=1;
for w in items: dp |= (dp << w);
```

Each `<<` and `|` on \(S/64\) words → \(O(nS/w)\).

For bounded counts, loop reverse like knapsack or use multiple shifts.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: check bit \(O(1)\)
- Total: \(O(nS/64)\) subset sum; \(O(n^3/64)\) bitset Floyd
- Memory: \(O(S/64)\) or \(O(n^2/64)\)`

### C++17 Template

```cpp
// C++17 — subset sum / knapsack reachability
#include <bits/stdc++.h>
using namespace std;

namespace bitset_dp {
constexpr int MAXS = 1000005;

bitset<MAXS> subset_sum(const vector<int>& w, int S) {
    bitset<MAXS> dp;
    dp[0] = 1;
    for (int x : w) {
        if (x <= S) dp |= (dp << x);
    }
    return dp;
}

// Boolean matrix / reachability: G[i] = bitset of out-neighbors
vector<bitset<4096>> floyd_bitset(vector<bitset<4096>> g) {
    int n = (int)g.size();
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            if (g[i][k]) g[i] |= g[k];
    return g;
}

// Digit / position DP acceleration: OR-convolution style shifts
void add_item_count(bitset<MAXS>& dp, int w, int cnt, int S) {
    // at most cnt copies of w
    for (int b = 1; cnt > 0; b <<= 1) {
        int take = min(b, cnt);
        int sh = take * w;
        if (sh <= S) dp |= (dp << sh);
        cnt -= take;
    }
}
} // namespace bitset_dp
```

### Python 3 Template

```python
def subset_sum(weights, S):
    dp = 1  # bit 0 set
    mask = (1 << (S + 1)) - 1
    for w in weights:
        if 0 < w <= S:
            dp |= (dp << w) & mask
    return dp

def can_make(dp, x):
    return (dp >> x) & 1
```

---

## 6. Recognition Trigger Signals & Heuristics

- Knapsack **existence** / reachable sums; subset sum.
- \(dp[i][s]\) boolean with transitions \(s\to s+a_i\).
- Floyd Warshall / transitive closure with bitsets.
- “Can you form k?” with many items.
- Need speed from \(O(nS)\) to \(O(nS/64)\).

---

## 7. Contest WA / TLE / RE Traps

- `bitset` size not compile-time constant when needed — use templates / max bound.
- Shifting beyond size silently truncates — ensure `MAXS > S`.
- Using bitset for **values** not booleans (need SOS / other).
- Off-by-one on reachable index \(S\).
- Reverse-order knapsack confusion when mixing classic array DP with bitset (bitset `<<` is multi-use in one step — like unbounded if you loop wrong; for 0-1, single `|= << w` per item is correct).

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

- Meet-in-the-middle + bitset.
- Bitset optimization of DP on broken profile (narrow grids).
- `__int128` manual for small \(S\le 128\).
- GCC `bitset` `_Find_first` / `_Find_next` for enumerating set bits.

---

## 11. Typical Problem Archetypes

1. Standard: subset sum existence; partition equal sum.
2. Slightly disguised: scheduling reachability of timelines.
3. Difficult: bitset + SOS hybrid; or \(k\)-sum with bitset layers.
4. Very difficult: bitset inside D&C / offline queries.

---

## 12. Recognition & Identification Drills

1. \(n\le 1000\) weights, \(S\le 10^6\), existence of subset sum — complexity target?
2. Transitive closure \(n=4000\) — how?
3. 0-1 knapsack maximizing value with \(S\le 10^5\) — bitset enough?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: boolean DP over sums/graphs word-packable.
- Key invariant: word-parallel OR/AND/shifts.
- Key formula: `dp |= dp << w`.
- Complexity: \(O(nS/64)\).
- Template to remember: `bitset` + shift-or for 0-1 items.

**Simpler DP passes when:** \(nS\le 10^7\) classic bool array is fine.

---

## 8. SOS DP

---
