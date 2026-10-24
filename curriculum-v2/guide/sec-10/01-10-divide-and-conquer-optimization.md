# Divide-and-conquer optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Layered DP, comfort with proving monotonicity of argmin, recursion / iterative D&C  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Layered DP, comfort with proving monotonicity of argmin, recursion / iterative D&C

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

You have layers \(i=1..k\) and positions \(j=1..n\):

\[
dp[i][j]=\min_{t=0}^{j-1}\bigl(dp[i-1][t]+C(t+1,j)\bigr)
\]

(or \(t\) in some feasible range). Naively \(O(kn^2)\). If the **optimal \(t\)** for fixed \(i\) is monotone in \(j\) — \(opt(i,j)\le opt(i,j+1)\) — then when you solve all \(j\) in a mid range, the search for \(opt\) of the left half of \(j\)’s only needs \(t\le opt(mid)\), and the right half only \(t\ge opt(mid)\). One D&C over \(j\) with shrinking \(t\)-window gives \(O(n\log n)\) per layer → \(O(kn\log n)\).

The monotonicity is usually inherited from a **quadrangle inequality** on \(C\), but in contest you often **prove opt moves right** by a crossing argument, or trust the classic cost forms (see Recognition).

---

## 4. Proof Sketches & Recurrences

Assume for fixed layer \(i\), \(opt(j)\le opt(j+1)\). Define

\[
w(j,t)=dp[i-1][t]+C(t+1,j).
\]

Decision monotonicity: if \(j_1<j_2\) and \(t_1<t_2\), then \(w(j_1,t_2)<w(j_1,t_1)\) implies \(w(j_2,t_2)<w(j_2,t_1)\) (or the dual form). Then argmin is monotone.

**Algorithm:** `solve(jL, jR, tL, tR)`:
1. If \(jL>jR\) return.
2. \(jM=(jL+jR)/2\); find \(t^\*=\arg\min_{t\in[tL,tR]} w(jM,t)\) (respecting \(t<jM\)).
3. Set \(dp[i][jM]=w(jM,t^\*)\).
4. Recurse left: `solve(jL, jM-1, tL, t*)`, right: `solve(jM+1, jR, t*, tR)`.

Each element \(j\) is a midpoint \(O(\log n)\) times; each time you scan an interval of \(t\) that **partitions** so total work per layer is \(O(n\log n)\) if each \(C\) is \(O(1)\) (prefix sums).

**Complexity derivation:** At each recursion depth, the \(t\)-ranges for different midpoints are nested/partitioned so \(\sum |tR-tL|=O(n)\) across a level; depth \(O(\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: usually \(O(n)\) prefix sums for \(C\)
- Per-query / per-operation: N/A (offline DP)
- Total: \(O(kn\log n)\) if \(C=O(1)\); else multiply by cost of \(C\)
- Memory: \(O(n)\) with rolling layers; \(O(kn)\) if all layers stored`

### C++17 Template

```cpp
// C++17 — D&C DP opt for dp[i][j] = min_{t < j} dp[i-1][t] + cost(t+1, j)
#include <bits/stdc++.h>
using namespace std;

namespace dc_dp {
using ll = long long;
const ll INF = 4e18;

// cost(L,R) inclusive; must be O(1) via prefixes
function<ll(int,int)> cost;

void compute(vector<ll>& dp, const vector<ll>& dpp,
             int jl, int jr, int tl, int tr) {
    if (jl > jr) return;
    int jm = (jl + jr) >> 1;
    pair<ll,int> best = {INF, tl};
    int hi = min(tr, jm - 1);
    for (int t = tl; t <= hi; ++t) {
        ll val = dpp[t] + cost(t + 1, jm);
        if (val < best.first) best = {val, t};
    }
    dp[jm] = best.first;
    int opt = best.second;
    compute(dp, dpp, jl, jm - 1, tl, opt);
    compute(dp, dpp, jm + 1, jr, opt, tr);
}

// layers 1..k, positions 1..n (1-indexed dp)
vector<ll> solve(int n, int k, function<ll(int,int)> C) {
    cost = move(C);
    vector<ll> dp(n + 1, INF), dpp(n + 1, INF);
    dpp[0] = 0; // empty prefix with 0 groups
    for (int i = 1; i <= k; ++i) {
        fill(dp.begin(), dp.end(), INF);
        compute(dp, dpp, i, n, i - 1, n - 1); // t at least i-1 groups used
        swap(dp, dpp);
    }
    return dpp;
}
} // namespace dc_dp
```

### Python 3 Template

```python
# prototype only — verify opt monotonicity
def opts(n, dpp, cost):
    opt = []
    for j in range(1, n + 1):
        best_t, best = None, 10**30
        for t in range(j):
            v = dpp[t] + cost(t + 1, j)
            if v < best:
                best, best_t = v, t
        opt.append(best_t)
    return opt  # should be nondecreasing if D&C applies
```

---

## 6. Recognition Trigger Signals & Heuristics

- Layered DP: “use exactly \(i\) segments / groups ending at \(j\)”.
- Cost \(C(L,R)\) of a contiguous segment that is **convex** in the sense of QI: \(C(a,c)+C(b,d)\le C(a,d)+C(b,c)\) for \(a\le b\le c\le d\).
- Classic costs: variance of a segment, \(\bigl(\sum_{L..R} w\bigr)^2\), cost of grouping people on a line, “send all to median”, etc.
- You can compute \(opt(j)\) for small \(n\) and see it nondecreasing — strong empirical clue (not a proof, but good for contest confidence when theory matches).
- **Not:** the same as Knuth: Knuth is 2D interval DP; D&C is usually 1D per layer with a previous layer.

---

## 7. Contest WA / TLE / RE Traps

- Off-by-one in \(t\) range (`t < j` vs `t \le j`).
- Forgetting base layer: \(dp[0][0]=0\), \(dp[0][j>0]=\infty\).
- Using D&C without monotonicity → WA (silent wrong mins).
- Recursing with wrong `opt` bounds (must pass `opt` to both sides correctly).
- Cost not \(O(1)\) → TLE; precompute prefixes.
- Open vs closed segment boundaries inconsistent with `cost`.

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

- **Maximize** instead of minimize (reverse inequalities / negate).
- **opt decreasing**: mirror the array or swap roles.
- **Online / different layer shapes**: sometimes `dp[j]` depends on `dp[j']` same layer — D&C needs careful ordering (rarer).
- **Knuth–Yao style** related but for interval DP → see Knuth below.

---

## 11. Typical Problem Archetypes

1. Standard: split array into \(k\) contiguous segments; minimize sum of segment costs (variance, squared sum).
2. Slightly disguised: “factory placement”, “guardians on a line”, layered grouping.
3. Difficult: cost needs data structure to evaluate; combine with sparse table / offline.
4. Very difficult: prove QI for unusual \(C\); or nested D&C.

---

## 12. Recognition & Identification Drills

1. Split \(n\) people on a number line into \(k\) contiguous groups; cost of a group = distance from ends to median. Optimize total cost.
2. \(dp[i][j]=\min_{t<j} dp[i-1][t]+(pref[j]-pref[t])^2\). Can you beat \(O(kn^2)\)?
3. Same recurrence but \(C(L,R)=\max_{L..R} a - \min_{L..R} a\). Is opt monotone?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: layered segment DP + decision monotonicity / QI on \(C\).
- Key invariant: \(opt(j)\le opt(j+1)\).
- Key formula: \(dp[i][j]=\min_t dp[i-1][t]+C(t+1,j)\).
- Complexity: \(O(kn\log n)\).
- Template to remember: `compute(jl,jr,tl,tr)` mid + recurse.

**Simpler DP passes when:** \(kn^2 \lesssim 10^8\)–\(5\cdot 10^8\) (e.g. \(n\le 4000,k\le 20\) sometimes; \(n\le 500\) always try cubic/naive first).

---

## 2. Knuth optimization

---
