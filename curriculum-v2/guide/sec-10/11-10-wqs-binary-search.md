# 11. WQS binary search

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2300–3000 | **Frequency:** Occasional  
> **Prerequisites:** Alien trick family, binary/ternary search, DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2300–3000
- Prerequisites: Alien trick family, binary/ternary search, DP

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

**WQS** (from OI folklore / “wqs二分”) is the standard **binary search on the Lagrangian multiplier** for the Alien setup. Same mathematics: search the slope \(\lambda\) such that the concave conjugate touches at the desired \(k\). Naming emphasis: treat \(\lambda\) as the search key; each check runs a \(k\)-free DP and reads off the optimal number of parts.

Use when you already know Alien applies and need a concrete search procedure (including integer \(\lambda\) and tie-breaking conventions used in Chinese OI blogs).

---

## 4. Proof Sketches & Recurrences

Identical conjugate:

\[
\text{check}(\lambda):\quad \min_P cost(P)+\lambda\cdot\kappa(P),\quad \text{observe }\kappa(P^\*).
\]

Because \(\kappa^\*(\lambda)\) is nonincreasing in \(\lambda\), binary search works. For integer costs, \(\lambda\) often integer in a bounded range; if not, search reals with enough iterations, or search on **slopes between consecutive hull points** (fractional \(\lambda=p/q\) via cross).

**Fractional binary search / deterministic slope:** when you need exact touch at \(k\), maintain the lower hull of points \((k,opt(k))\) implicitly; WQS finds the supporting line with the right contact \(k\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: 1 DP per mid
- Total: \(O(\mathrm{DP}\cdot\log\Lambda)\) or \(\mathrm{DP}\cdot\#iters\)
- Memory: inner DP`

### C++17 Template

```cpp
// C++17 — WQS binary search on lambda (min cost, exactly K parts)
#include <bits/stdc++.h>
using namespace std;

namespace wqs {
using ll = long long;
const ll INF = 4e18;

struct Result { ll penalized; int parts; ll true_cost; };

// run(lambda) must minimize true_cost + lambda * parts
template<class F>
ll wqs_min_exact_K(int K, ll lo, ll hi, F run) {
    ll best = INF;
    while (lo <= hi) {
        ll mid = lo + (hi - lo) / 2;
        Result r = run(mid);
        r.true_cost = r.penalized - mid * (ll)r.parts;
        if (r.parts == K) best = r.true_cost;
        // more parts than K → lambda too small
        if (r.parts > K) lo = mid + 1;
        else if (r.parts < K) hi = mid - 1;
        else {
            // found; still explore neighbors if ties / non-unique
            // optional: return immediately
            return r.true_cost;
        }
    }
    return best; // INF if impossible / convexity broken / bounds wrong
}

// Real lambda with fixed iterations (when integer search insufficient)
template<class F>
ll wqs_real(int K, double lo, double hi, F run, int iters = 80) {
    ll best = INF;
    for (int it = 0; it < iters; ++it) {
        double mid = (lo + hi) / 2;
        // encode lambda as scaled integer if DP needs ints:
        // pass mid into run carefully
        Result r = run(mid);
        if (r.parts >= K) lo = mid; // depends on sign convention
        else hi = mid;
        if (r.parts == K)
            best = min(best, (ll)llround(r.penalized - mid * r.parts));
    }
    return best;
}
} // namespace wqs
```

### Python 3 Template

```python
# Given opt[k] for k in range, find min opt[k]+lambda*k
def g(opt, lam):
    return min(opt[k] + lam * k for k in opt)

def best_k(opt, lam):
    return min(opt, key=lambda k: opt[k] + lam * k)
```

---

## 6. Recognition Trigger Signals & Heuristics

- Same as Alien; editorials say “wqs二分”.
- Minimizing \(f(x)+g(k)\) style with convex \(g\) or convex tradeoff.
- After fixing \(\lambda\), the problem reduces to a classical DP you already coded.
- Graph problems: “exactly \(k\) edges of type B” → weight shift on those edges + shortest path.

---

## 7. Contest WA / TLE / RE Traps

- Same as Alien: convexity, tie-breaking, answer recovery.
- Floating \(\lambda\) precision → wrong `parts`.
- Searching max problems with min template.
- Off-by-one on `parts > K` branch.
- Claiming WQS when the tradeoff is non-convex (must use explicit \(k\) DP).

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

- **At most \(K\)**: often take \(\lambda=0\) or clamp after unpenalized; or still search if unconstrained optimum uses fewer.
- **Graph WQS**: add \(\lambda\) to every chosen special edge; binary search until path uses \(K\) specials.
- **Ternary search** on \(\lambda\) when unimodal \(g\) alone is used (less common than binsearch on monotone `parts`).

---

## 11. Typical Problem Archetypes

1. Standard: OI-style “exactly \(k\) segments” with WQS + DP.
2. Slightly disguised: exactly \(k\) red edges on shortest path.
3. Difficult: need fractional slopes; hull edges between integer \(k\).
4. Very difficult: two-parameter WQS.

---

## 12. Recognition & Identification Drills

1. Shortest path with exactly \(k\) special edges — model \(\lambda\).
2. Minimize cost with exactly \(k\) groups; inner DP is CHT — outline solution.
3. When does binary search on answer **not** equal WQS?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: Alien applicable; search \(\lambda\) until `#parts=K`.
- Key invariant: `#parts(\lambda)` monotone in \(\lambda\).
- Key formula: answer \(=pen-\lambda K\) at the touching \(\lambda\).
- Complexity: \(\mathrm{DP}\cdot\log\Lambda\).
- Template to remember: `while lo<=hi` mid; `if parts>K: lo=mid+1`.

**Situational / hard.** Default to explicit-\(k\) DP when it fits TL.

---

## 12. DP optimization recognition patterns

---
