# Alien trick / Lagrangian relaxation

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2300–3000 | **Frequency:** Occasional  
> **Prerequisites:** DP with an extra cardinality dimension, convexity/concavity of optimal cost vs \(k\), binary search intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2300–3000
- Prerequisites: DP with an extra cardinality dimension, convexity/concavity of optimal cost vs \(k\), binary search intuition

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

You want

\[
\min\{\,cost(P):P\text{ uses exactly }k\text{ “parts” (segments, edges, groups)}\,\}.
\]

Explicit DP with dimension \(k\) may be too slow. **Relax**: ignore the exact-\(k\) constraint; for a penalty \(\lambda\), solve

\[
dp(\lambda)=\min_P\bigl(cost(P)+\lambda\cdot \#parts(P)\bigr).
\]

If \(opt(k)=\) best true cost with \(k\) parts is **convex** in \(k\) (discrete convex), then \(dp(\lambda)=\min_k(opt(k)+\lambda k)\) is the Legendre-like transform. By sweeping/searching \(\lambda\), you recover the right \(k\). Often you also recover the minimizing \(k(\lambda)\) from the DP that counts parts used in an optimal solution.

This is **situational / hard**: wrong convexity ⇒ wrong answer; discrete \(\lambda\) needs care (often search on integers or use fractions).

---

## 4. Proof Sketches & Recurrences

Assume \(opt(k)\) convex: \(opt(k+1)-opt(k)\) nondecreasing (for minimization of convex \(opt\)). Then

\[
g(\lambda)=\min_k\bigl(opt(k)+\lambda k\bigr)
\]

is concave in \(\lambda\); the minimizing \(k\) decreases as \(\lambda\) increases (paying more per part → fewer parts).

**Algorithm sketch:**
1. Binary search \(\lambda\) (or ternary on real; prefer integer with analysis).
2. Run DP for \(cost+\lambda\cdot\#parts\); let \(k^\*\) be #parts in optimum (break ties toward needed side).
3. If \(k^\*>k\) target, increase \(\lambda\); else decrease.
4. Answer \(= g(\lambda)-\lambda k\) when \(k^\*=k\).

**Tie-breaking:** when multiple \(k\) achieve same \(g(\lambda)\), convexity implies an interval of \(k\); nudge \(\lambda\) or add \(\epsilon\cdot\#parts\) with tiny \(\epsilon\), or return any and check.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: one penalized DP per probed \(\lambda\)
- Total: \(O((\text{cost of DP})\cdot\log\Lambda)\)
- Memory: as in inner DP`

### C++17 Template

```cpp
// C++17 — Alien skeleton: plug in your penalized DP
#include <bits/stdc++.h>
using namespace std;

namespace alien {
using ll = long long;
const ll INF = 4e18;

// User provides: for fixed lambda, returns {best penalized cost, parts used}
// penalized = true_cost + lambda * parts
using PenalizedDP = function<pair<ll,int>(ll /*lambda*/)>;

// Minimize true cost with exactly need_parts (convex opt assumed)
ll alien_exact(ll lo_l, ll hi_l, int need_parts, PenalizedDP run) {
    // Binary search lambda; adjust bounds to problem (can be negative)
    ll ans = INF;
    while (lo_l <= hi_l) {
        ll mid = lo_l + (hi_l - lo_l) / 2;
        auto [pen, parts] = run(mid);
        // true cost if this parts count:
        ll true_cost = pen - mid * parts;
        if (parts == need_parts) ans = min(ans, true_cost);
        if (parts >= need_parts) {
            // too many parts → increase penalty
            lo_l = mid + 1;
            if (parts == need_parts) ans = true_cost; // keep
        } else {
            hi_l = mid - 1;
        }
    }
    return ans;
}

// Example hook: partition into contiguous segments, cost = (sum)^2,
// minimize sum of costs + lambda * (#segments), return parts used.
// (D&C / CHT may replace the O(n^2) below.)
pair<ll,int> example_partition_penalized(const vector<ll>& pref, ll lambda) {
    int n = (int)pref.size() - 1;
    vector<ll> dp(n + 1, INF);
    vector<int> cnt(n + 1, 0);
    dp[0] = 0;
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < i; ++j) {
            ll s = pref[i] - pref[j];
            ll val = dp[j] + s * s + lambda; // +lambda per new segment
            if (val < dp[i]) {
                dp[i] = val;
                cnt[i] = cnt[j] + 1;
            }
        }
    }
    return {dp[n], cnt[n]};
}
} // namespace alien
```

### Python 3 Template

```python
# Verify discrete convexity of opt[k] on a small instance
def is_convex(opt):
    # opt[k] defined on an interval of k
    ks = sorted(opt)
    for i in range(1, len(ks) - 1):
        k = ks[i]
        if opt[k] - opt[ks[i-1]] > opt[ks[i+1]] - opt[k]:
            return False
    return True
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Exactly / at most \(k\) segments” but \(O(nk)\) or \(O(nk\log)\) too slow; \(n\) large, \(k\) large.
- Editorial words: Alien trick, wqs, Lagrangian relaxation, “penalty on number of groups”.
- You can solve unrestricted (or only soft-penalized) DP fast (CHT / D&C / Dijkstra).
- Plot of best cost vs \(k\) looks convex (check small \(n\)).
- Vs WQS:** Alien emphasizes the relaxation + DP; WQS emphasizes binary search on \(\lambda\). Same family — see next subsection.

---

## 7. Contest WA / TLE / RE Traps

- Applying without convexity → WA.
- Wrong direction when comparing `parts` vs `need`.
- Not handling ties (`parts` jumps over target \(k\)).
- Recovering answer as `pen` instead of `pen - lambda*k`.
- \(\lambda\) bounds too tight; overflow when \(\lambda\cdot k\).
- Maximization problems need sign flips (concave \(opt\)).

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

- At most \(k\) / at least \(k\) (often easier: monotone check).
- Multiple constraints (multi-dimensional Alien — rare, very hard).
- Fractional / slope trick viewpoint (same math as CHT conjugates).
- Combine with CHT/D&C inside penalized DP.

---

## 11. Typical Problem Archetypes

1. Standard: split into exactly \(k\) segments; large \(n,k\).
2. Slightly disguised: choose exactly \(k\) “expensive operations” on a path.
3. Difficult: ties; need secondary criterion.
4. Very difficult: prove convexity from QI; nested optimizations.

---

## 12. Recognition & Identification Drills

1. \(n=1e5\), split into exactly \(k=1e5\) segments, cost convex in segments — options?
2. Same but \(opt(k)\) not convex — what fails?
3. Maximize score with exactly \(k\) groups — how does \(\lambda\) move?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: exact \(k\) parts + convex \(opt(k)\) + fast penalized DP.
- Key invariant: discrete convexity of \(opt(k)\).
- Key formula: \(g(\lambda)=\min(opt(k)+\lambda k)\); answer \(g-\lambda k\).
- Complexity: DP cost \(\times\log\Lambda\).
- Template to remember: binsearch \(\lambda\); DP returns `(penalized, parts)`.

**Situational / hard.** If \(k\) small, keep explicit dimension. Prefer not forcing Alien.

---

## 11. WQS binary search

---
