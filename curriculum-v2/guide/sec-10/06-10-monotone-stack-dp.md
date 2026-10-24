# Monotone stack DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Next greater/smaller element, contribution trick, basic DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Next greater/smaller element, contribution trick, basic DP

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

For arrays, many DP / counting / sum-of-subarray-function problems reduce to: for each position \(i\), find the largest segment where \(a_i\) is the strict (or non-strict) maximum/minimum. A **monotone stack** computes previous/next greater in \(O(n)\). Then:

- Contribution: \(a_i\) adds \(a_i\cdot left\cdot right\) to “sum of mins/maxs of all subarrays”.
- DP: \(dp[i]\) = best using a segment ending at \(i\) whose max is \(a_i\), jumping to `prev_greater[i]`.

---

## 4. Proof Sketches & Recurrences

Previous strictly greater:

```
for i in 1..n:
  while stack not empty and a[stack.top] <= a[i]: pop
  prev[i] = stack.top or 0
  push i
```

If \(dp[i]=\min_{j=prev[i]}^{i-1} dp[j]+cost(a[i])\) with structure, sometimes fold into stack while popping (maintain aggregate on stack).

Cartesian tree: parent of \(i\) is nearest greater; tree DP follows.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) NGE / contribution setup
- Per-query / per-operation: \(O(1)\) after arrays built
- Total: \(O(n)\) typical
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — NGE primitives, contribution trick, histogram, stack-folding DP
#include <bits/stdc++.h>
using namespace std;

namespace mono_stack {
using ll = long long;
const ll INF = 4e18;

// prev / next strict greater (sentinels 0, n+1); a is 1-indexed
void nge(const vector<ll>& a, vector<int>& pg, vector<int>& ng) {
    int n = (int)a.size() - 1;
    pg.assign(n + 2, 0);
    ng.assign(n + 2, n + 1);
    vector<int> st;
    for (int i = 1; i <= n; ++i) {
        while (!st.empty() && a[st.back()] < a[i]) {
            ng[st.back()] = i;
            st.pop_back();
        }
        pg[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }
}

// Sum of minimums of all subarrays — O(n)
ll sum_of_subarray_mins(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<int> pl(n + 2), nr(n + 2);
    vector<int> st;
    for (int i = 1; i <= n; ++i) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        pl[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = n; i >= 1; --i) {
        while (!st.empty() && a[st.back()] > a[i]) st.pop_back();
        nr[i] = st.empty() ? n + 1 : st.back();
        st.push_back(i);
    }
    ll ans = 0;
    for (int i = 1; i <= n; ++i)
        ans += a[i] * (ll)(i - pl[i]) * (nr[i] - i);
    return ans;
}

// Largest rectangle in histogram — O(n)
ll largest_rectangle(const vector<ll>& h) {
    int n = (int)h.size() - 1;
    vector<int> L(n + 2), R(n + 2);
    vector<int> st;
    for (int i = 1; i <= n; ++i) {
        while (!st.empty() && h[st.back()] >= h[i]) st.pop_back();
        L[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = n; i >= 1; --i) {
        while (!st.empty() && h[st.back()] >= h[i]) st.pop_back();
        R[i] = st.empty() ? n + 1 : st.back();
        st.push_back(i);
    }
    ll ans = 0;
    for (int i = 1; i <= n; ++i)
        ans = max(ans, h[i] * (R[i] - L[i] - 1));
    return ans;
}

// dp[i] = min_{j < i} dp[j] + max(a[j+1..i]), a[1..n] > 0 — O(n)
// Stack of decreasing maxima; each item stores min dp in its plateau + best answer.
vector<ll> dp_cover_by_range_max(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<ll> dp(n + 1, INF);
    dp[0] = 0;
    struct Item { ll mx, min_dp, best; };
    vector<Item> st;
    for (int i = 1; i <= n; ++i) {
        ll min_dp = dp[i - 1];
        while (!st.empty() && st.back().mx <= a[i]) {
            min_dp = min(min_dp, st.back().min_dp);
            st.pop_back();
        }
        ll best = min_dp + a[i];
        if (!st.empty()) best = min(best, st.back().best);
        st.push_back({a[i], min_dp, best});
        dp[i] = best;
    }
    return dp;
}
} // namespace mono_stack
```

### Python 3 Template

```python
def nge(a):
    # a[1..n], return prev_gt, next_gt
    n = len(a) - 1
    pg = [0] * (n + 2)
    ng = [n + 1] * (n + 2)
    st = []
    for i in range(1, n + 1):
        while st and a[st[-1]] < a[i]:
            ng[st.pop()] = i
        pg[i] = st[-1] if st else 0
        st.append(i)
    return pg, ng

def sum_subarray_mins(a):
    n = len(a) - 1
    pl, nr = [0]*(n+2), [n+1]*(n+2)
    st = []
    for i in range(1, n+1):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        pl[i] = st[-1] if st else 0
        st.append(i)
    st.clear()
    for i in range(n, 0, -1):
        while st and a[st[-1]] > a[i]:
            st.pop()
        nr[i] = st[-1] if st else n + 1
        st.append(i)
    return sum(a[i] * (i - pl[i]) * (nr[i] - i) for i in range(1, n+1))
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Subarrays where max/min is …” / sum of f(max) over subarrays.
- Histogram largest rectangle (classic stack).
- DP transition “go back until a larger obstacle”.
- Cartesian tree structure (stack builds tree; DP on tree).
- Vs queue:** stack answers **value-monotone** ranges, not fixed index windows.

---

## 7. Contest WA / TLE / RE Traps

- Strict vs non-strict inequalities → double-counting equal elements.
- Sentinels wrong (`0` / `n+1`).
- Using stack for fixed index window (should be queue).
- Off-by-one in `left * right` contribution lengths.
- Assuming \(O(n)\) folding for a DP without verifying the merge invariant.

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

- Next smaller / previous smaller.
- Cartesian tree DP.
- Contribution of max AND min (two stacks).
- Stack + segtree for richer aggregates while popping.

---

## 11. Typical Problem Archetypes

1. Standard: largest rectangle; sum of subarray minimums.
2. Slightly disguised: DP where transition jumps to previous greater barrier.
3. Difficult: count pairs / triples with stack + combinatorics.
4. Very difficult: stack DP on trees / with updates.

---

## 12. Recognition & Identification Drills

1. Sum over all subarrays of (max - min).
2. For each \(i\), largest \(j\) with \(\max(a[j..i])=a[i]\).
3. DP cover array; cost of segment = its maximum — aim better than \(O(n^2)\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: ranges ruled by nearest greater/smaller.
- Key invariant: stack monotone by value.
- Key formula: contribution \(a_i\cdot L_i\cdot R_i\); or DP jump to `prev_gt`.
- Complexity: \(O(n)\).
- Template to remember: while top dominated, pop; set prev/next; push.

**Simpler DP passes when:** \(n\le 5000\) for \(O(n^2)\) subarray enumeration.

---

## 7. Bitset DP

---
