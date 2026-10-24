# Section §10: Dynamic Programming Optimizations

> **Module ID:** `sec-10`  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Topic Count:** 22  

**Module Summary:** Monotone Queue/Stack DP, Convex Hull Trick (CHT), Li Chao Tree, Divide-and-Conquer DP, Knuth Quadrangle Inequality, SOS DP, Bitset DP, and Profile DP.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Divide-and-conquer optimization](#topic-1) | `A-tier` | 2000–2600 | Occasional | [01-10-divide-and-conquer-optimization.md](./01-10-divide-and-conquer-optimization.md) |
| 2 | [Knuth optimization](#topic-2) | `B-tier` | 2100–2700 | Occasional | [02-10-knuth-optimization.md](./02-10-knuth-optimization.md) |
| 3 | [Convex Hull Trick](#topic-3) | `A-tier` | 2000–2600 | Occasional | [03-10-convex-hull-trick.md](./03-10-convex-hull-trick.md) |
| 4 | [Li Chao Tree](#topic-4) | `B-tier` | 2100–2700 | Occasional | [04-10-li-chao-tree.md](./04-10-li-chao-tree.md) |
| 5 | [Monotone queue optimization](#topic-5) | `A-tier` | 1700–2300 | Common | [05-10-monotone-queue-optimization.md](./05-10-monotone-queue-optimization.md) |
| 6 | [Monotone stack DP](#topic-6) | `A-tier` | 1600–2200 | Common | [06-10-monotone-stack-dp.md](./06-10-monotone-stack-dp.md) |
| 7 | [Bitset DP](#topic-7) | `A-tier` | 1600–2300 | Common | [07-10-bitset-dp.md](./07-10-bitset-dp.md) |
| 8 | [SOS DP (Sum over Subsets) — primary home](#topic-8) | `A-tier` | 1800–2400 | Occasional | [08-10-sos-dp-sum-over-subsets-primary-home.md](./08-10-sos-dp-sum-over-subsets-primary-home.md) |
| 9 | [Profile / state-compression DP](#topic-9) | `B-tier` | 2000–2700 | Occasional | [09-10-profile-state-compression-dp.md](./09-10-profile-state-compression-dp.md) |
| 10 | [Alien trick / Lagrangian relaxation](#topic-10) | `B-tier` | 2300–3000 | Occasional | [10-10-alien-trick-lagrangian-relaxation.md](./10-10-alien-trick-lagrangian-relaxation.md) |
| 11 | [WQS binary search](#topic-11) | `B-tier` | 2300–3000 | Occasional | [11-10-wqs-binary-search.md](./11-10-wqs-binary-search.md) |
| 12 | [DP optimization recognition patterns (synthesis)](#topic-12) | `S-tier` | 1800–2600 | Common | [12-10-dp-optimization-recognition-patterns-synthesis.md](./12-10-dp-optimization-recognition-patterns-synthesis.md) |
| 13 | [Digit DP Template](#topic-13) | `S-tier` | 1600–2200 | Frequent | [13-10-digit-dp-template.md](./13-10-digit-dp-template.md) |
| 14 | [D&C DP vs Knuth](#topic-14) | `B-tier` | 1600–2200 | Common | [14-10-d-c-dp-vs-knuth.md](./14-10-d-c-dp-vs-knuth.md) |
| 15 | [CHT vs Li Chao](#topic-15) | `B-tier` | 1600–2200 | Common | [15-10-cht-vs-li-chao.md](./15-10-cht-vs-li-chao.md) |
| 16 | [Alien trick vs WQS binary search](#topic-16) | `B-tier` | 1600–2200 | Common | [16-10-alien-trick-vs-wqs-binary-search.md](./16-10-alien-trick-vs-wqs-binary-search.md) |
| 17 | [Monotone queue vs monotone stack DP](#topic-17) | `B-tier` | 1600–2200 | Common | [17-10-monotone-queue-vs-monotone-stack-dp.md](./17-10-monotone-queue-vs-monotone-stack-dp.md) |
| 18 | [High-ROI (learn early in this section)](#topic-18) | `B-tier` | 1600–2200 | Common | [18-10-high-roi-learn-early-in-this-section.md](./18-10-high-roi-learn-early-in-this-section.md) |
| 19 | [Situational (clear recognition pattern first)](#topic-19) | `B-tier` | 1600–2200 | Common | [19-10-situational-clear-recognition-pattern-first.md](./19-10-situational-clear-recognition-pattern-first.md) |
| 20 | [Rarely worth early / niche early](#topic-20) | `B-tier` | 1600–2200 | Common | [20-10-rarely-worth-early-niche-early.md](./20-10-rarely-worth-early-niche-early.md) |
| 21 | [Suggested learning order (exact subtopic order)](#topic-21) | `B-tier` | 1600–2200 | Common | [21-10-suggested-learning-order-exact-subtopic-order.md](./21-10-suggested-learning-order-exact-subtopic-order.md) |
| 22 | [What to drill this week](#topic-22) | `B-tier` | 1600–2200 | Common | [22-10-what-to-drill-this-week.md](./22-10-what-to-drill-this-week.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Divide-and-conquer optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Layered DP, comfort with proving monotonicity of argmin, recursion / iterative D&C  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Layered DP, comfort with proving monotonicity of argmin, recursion / iterative D&C

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

You have layers \(i=1..k\) and positions \(j=1..n\):

\[
dp[i][j]=\min_{t=0}^{j-1}\bigl(dp[i-1][t]+C(t+1,j)\bigr)
\]

(or \(t\) in some feasible range). Naively \(O(kn^2)\). If the **optimal \(t\)** for fixed \(i\) is monotone in \(j\) — \(opt(i,j)\le opt(i,j+1)\) — then when you solve all \(j\) in a mid range, the search for \(opt\) of the left half of \(j\)’s only needs \(t\le opt(mid)\), and the right half only \(t\ge opt(mid)\). One D&C over \(j\) with shrinking \(t\)-window gives \(O(n\log n)\) per layer → \(O(kn\log n)\).

The monotonicity is usually inherited from a **quadrangle inequality** on \(C\), but in contest you often **prove opt moves right** by a crossing argument, or trust the classic cost forms (see Recognition).

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: usually \(O(n)\) prefix sums for \(C\)
- Per-query / per-operation: N/A (offline DP)
- Total: \(O(kn\log n)\) if \(C=O(1)\); else multiply by cost of \(C\)
- Memory: \(O(n)\) with rolling layers; \(O(kn)\) if all layers stored`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Layered DP: “use exactly \(i\) segments / groups ending at \(j\)”.
- Cost \(C(L,R)\) of a contiguous segment that is **convex** in the sense of QI: \(C(a,c)+C(b,d)\le C(a,d)+C(b,c)\) for \(a\le b\le c\le d\).
- Classic costs: variance of a segment, \(\bigl(\sum_{L..R} w\bigr)^2\), cost of grouping people on a line, “send all to median”, etc.
- You can compute \(opt(j)\) for small \(n\) and see it nondecreasing — strong empirical clue (not a proof, but good for contest confidence when theory matches).
- **Not:** the same as Knuth: Knuth is 2D interval DP; D&C is usually 1D per layer with a previous layer.

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one in \(t\) range (`t < j` vs `t \le j`).
- Forgetting base layer: \(dp[0][0]=0\), \(dp[0][j>0]=\infty\).
- Using D&C without monotonicity → WA (silent wrong mins).
- Recursing with wrong `opt` bounds (must pass `opt` to both sides correctly).
- Cost not \(O(1)\) → TLE; precompute prefixes.
- Open vs closed segment boundaries inconsistent with `cost`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Maximize** instead of minimize (reverse inequalities / negate).
- **opt decreasing**: mirror the array or swap roles.
- **Online / different layer shapes**: sometimes `dp[j]` depends on `dp[j']` same layer — D&C needs careful ordering (rarer).
- **Knuth–Yao style** related but for interval DP → see Knuth below.

---

#### 11. Typical Problem Archetypes

1. Standard: split array into \(k\) contiguous segments; minimize sum of segment costs (variance, squared sum).
2. Slightly disguised: “factory placement”, “guardians on a line”, layered grouping.
3. Difficult: cost needs data structure to evaluate; combine with sparse table / offline.
4. Very difficult: prove QI for unusual \(C\); or nested D&C.

---

#### 12. Recognition & Identification Drills

1. Split \(n\) people on a number line into \(k\) contiguous groups; cost of a group = distance from ends to median. Optimize total cost.
2. \(dp[i][j]=\min_{t<j} dp[i-1][t]+(pref[j]-pref[t])^2\). Can you beat \(O(kn^2)\)?
3. Same recurrence but \(C(L,R)=\max_{L..R} a - \min_{L..R} a\). Is opt monotone?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: layered segment DP + decision monotonicity / QI on \(C\).
- Key invariant: \(opt(j)\le opt(j+1)\).
- Key formula: \(dp[i][j]=\min_t dp[i-1][t]+C(t+1,j)\).
- Complexity: \(O(kn\log n)\).
- Template to remember: `compute(jl,jr,tl,tr)` mid + recurse.

**Simpler DP passes when:** \(kn^2 \lesssim 10^8\)–\(5\cdot 10^8\) (e.g. \(n\le 4000,k\le 20\) sometimes; \(n\le 500\) always try cubic/naive first).

---

## 2. Knuth optimization

---


---

<a id="topic-2"></a>
### 2. Knuth optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Interval DP, quadrangle inequality, opt-monotonicity lemma (Knuth–Yao)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Interval DP, quadrangle inequality, opt-monotonicity lemma (Knuth–Yao)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

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

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)–\(O(n^2)\) for \(C\)
- Per-query / per-operation: N/A
- Total: \(O(n^2)\) under Knuth conditions (vs \(O(n^3)\) naive)
- Memory: \(O(n^2)\) for `dp` and `opt``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Matrix chain multiplication shape; optimal BST; splitting arrays with cost on full interval.
- \(C(l,r)=w(l,r)\) where \(w\) is sum of weights on \([l,r]\) (optimal BST).
- You already have \(dp\) by length; you maintain `opt[l][r]` = best split.
- QI: \(C(a,c)+C(b,d)\le C(a,d)+C(b,c)\) for \(a\le b\le c\le d\).
- Vs D&C:** if the DP is **two intervals combining** (binary tree of merges), think Knuth; if **last segment cut** against previous layer, think D&C.

---

#### 7. Contest WA / TLE / RE Traps

- Applying Knuth without QI → WA.
- Wrong initialization of `opt[l][l]` / empty intervals.
- Loop order: must increase length; need `opt[l][r-1]` and `opt[l+1][r]` already computed.
- Adding \(C(l,r)\) twice or outside the min incorrectly.
- Off-by-one when \(k\) ranges for length 2.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Optimal BST**: \(C(l,r)=\sum_{i=l}^{r} w_i\) (prefix); Knuth applies.
- **Matrix chain**: similar structure; cost of multiplying dimensions.
- **Maximize** versions with reversed inequalities (rare).
- If only QI fails mildly, sometimes still works — don’t rely on that.

---

#### 11. Typical Problem Archetypes

1. Standard: optimal BST / merging files with cumulative cost.
2. Slightly disguised: stone merging (Chinese classic) with sum costs.
3. Difficult: cost is more complex but still QI.
4. Very difficult: choose between Knuth and D&C when both seem plausible — match recurrence shape.

---

#### 12. Recognition & Identification Drills

1. Merge \(n\) adjacent piles; cost of merge = sum of sizes in range; minimize total.
2. Interval DP where \(C(l,r)=w[r]-w[l-1]\). What is `opt` monotonicity?
3. Same merge but cost = max pile in range. Does Knuth apply?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: interval DP + QI + monotone opt.
- Key invariant: \(opt[l][r-1]\le opt[l][r]\le opt[l+1][r]\).
- Key formula: \(dp[l][r]=\min_k dp[l][k]+dp[k+1][r]+C(l,r)\).
- Complexity: \(O(n^2)\).
- Template to remember: loop length; \(k\) from `opt[l][r-1]` to `opt[l+1][r]`.

**Simpler DP passes when:** \(n\le 400\) for \(O(n^3)\); don’t force Knuth early.

---

## 3. Convex Hull Trick

---


---

<a id="topic-3"></a>
### 3. Convex Hull Trick

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** DP rewriting as lines, deque / geometry of lower hull, integer cross products  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: DP rewriting as lines, deque / geometry of lower hull, integer cross products

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Many DPs rewrite as

\[
dp[i]=\min_j\bigl(dp[j]+B_j+A_i\cdot X_j\bigr)
\]

For fixed \(i\), each previous \(j\) is a line \(y = m_j x + c_j\) evaluated at \(x=A_i\) (or dual). Maintaining the **lower (or upper) envelope** of lines lets each query answer in \(O(1)\) or \(O(\log n)\) after amortized inserts.

If slopes \(m_j\) are monotone **and** query \(x\) are monotone, a **deque CHT** is \(O(n)\). Otherwise use Li Chao or multiset CHT (slope-ordered).

---

#### 4. Proof Sketches & Recurrences

Line \(L_j: y = m_j x + c_j\). Lower hull: intersection \(x\)-coordinate of \(L_1,L_2\):

\[
x=\frac{c_2-c_1}{m_1-m_2}
\]

Use cross-multiplication to avoid floats:

```
// bad: intersect(a,b) >= intersect(b,c)  (b useless)
// (c.b - a.b) / (a.m - c.m)  vs  (c.b - b.b)/(b.m - c.m)
```

For deque: lines in increasing slope; remove back while new line makes middle obsolete; remove front while front is worse than second for current \(x\).

**Squared distance classic:**

\[
dp[i]=\min_j dp[j]+(h_i-h_j)^2 = h_i^2+\min_j\bigl(dp[j]+h_j^2-2h_j h_i\bigr)
\]

Line slope \(m=-2h_j\), intercept \(dp[j]+h_j^2\), query \(x=h_i\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none beyond sorting if needed
- Per-query / per-operation: amortized \(O(1)\) monotone deque; \(O(\log n)\) multiset / Li Chao
- Total: \(O(n)\) monotone; \(O(n\log n)\) general
- Memory: \(O(n)\) lines`

##### C++17 Template

```cpp
// C++17 — monotone CHT (min), slopes increasing, queries increasing
#include <bits/stdc++.h>
using namespace std;

namespace cht {
using ll = long long;

struct Line {
    ll m, b; // y = m*x + b
    ll eval(ll x) const { return m * x + b; }
};

struct MinCHT {
    deque<Line> dq;

    // intersection x of a and b: a obsolete between if ...
    static bool bad(const Line& a, const Line& b, const Line& c) {
        // intersect(b,c) <= intersect(a,b)  => b never min
        // (a.b-b.b)/(b.m-a.m) >= (b.b-c.b)/(c.m-b.m)
        return (__int128)(b.b - a.b) * (b.m - c.m) >=
               (__int128)(c.b - b.b) * (a.m - b.m);
    }

    void add(ll m, ll b) { // slopes must be nondecreasing
        Line L{m, b};
        while (dq.size() >= 2 && bad(dq[dq.size()-2], dq.back(), L))
            dq.pop_back();
        dq.push_back(L);
    }

    ll query(ll x) { // x nondecreasing
        assert(!dq.empty());
        while (dq.size() >= 2 && dq[0].eval(x) >= dq[1].eval(x))
            dq.pop_front();
        return dq[0].eval(x);
    }
};
} // namespace cht
```

##### Python 3 Template

```python
# monotone min CHT — educational
from collections import deque

class MinCHT:
    def __init__(self):
        self.dq = deque()
    @staticmethod
    def bad(a, b, c):
        # a,b,c = (m,b)
        return (b[1]-a[1])*(b[0]-c[0]) >= (c[1]-b[1])*(a[0]-b[0])
    def add(self, m, b):
        L = (m, b)
        while len(self.dq) >= 2 and self.bad(self.dq[-2], self.dq[-1], L):
            self.dq.pop()
        self.dq.append(L)
    def query(self, x):
        while len(self.dq) >= 2 and self.dq[0][0]*x+self.dq[0][1] >= self.dq[1][0]*x+self.dq[1][1]:
            self.dq.popleft()
        return self.dq[0][0]*x + self.dq[0][1]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Algebraic form: \(dp[i]=\min_j dp[j]+(x_i-x_j)^2\) expands to lines after opening squares.
- “Cost linear in something that only depends on \(i\) times something of \(j\)”.
- Transitions look like \(\min_j \{c_j + m_j\cdot x_i\}\).
- Geometric: maintain hull of lines / dual points.
- If queries offline and sortable by \(x\), sort + deque still works even if insert order needs sorting by slope.

---

#### 7. Contest WA / TLE / RE Traps

- Overflow: use `__int128` for cross checks.
- Min vs max hull (sign of slope / pop conditions).
- Slopes not monotone → deque WA; switch to Li Chao.
- Queries not monotone → don’t pop front based on \(x\); binary search on hull.
- Parallel lines: handle equal slopes (keep better intercept).
- Forgetting constant terms pulled out of the min (\(h_i^2\) outside).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Max CHT**: mirror inequalities / negate.
- **Li Chao**: arbitrary order (next subsection).
- **Fully dynamic** multiset of lines (share pointers / set by slope).
- **Offline CDQ + CHT**: when both inserts and queries mixed with other dimensions.

---

#### 11. Typical Problem Archetypes

1. Standard: divide into segments with squared length cost; land purchase CHT classics.
2. Slightly disguised: expand \((x_i-x_j)^2\) or \(a_i\cdot b_j\) forms.
3. Difficult: slopes not sorted — sort transitions or use Li Chao.
4. Very difficult: CHT inside D&C / CDQ; persistent hulls.

---

#### 12. Recognition & Identification Drills

1. \(dp[i]=\min_{j<i} dp[j]+(x_i-x_j)^2+w\). Identify lines.
2. Same with \(x\) not sorted. Which structure?
3. \(dp[i]=\max_j dp[j]+a_j\cdot i+b_j\). Min or max hull?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: DP = min of linear functions of previous states.
- Key invariant: lower envelope of lines.
- Key formula: \(dp[i]=\min_j(m_j x_i+c_j)+f(i)\).
- Complexity: \(O(n)\) monotone / \(O(n\log n)\) general.
- Template to remember: deque add by slope; query by \(x\); `__int128` intersect.

**Simpler DP passes when:** \(n\le 5000\) for \(O(n^2)\) line evaluation; implement naive first under time.

---

## 4. Li Chao Tree

---


---

<a id="topic-4"></a>
### 4. Li Chao Tree

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Segment tree intuition, CHT, coordinate compression on \(x\)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Segment tree intuition, CHT, coordinate compression on \(x\)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

CHT without monotone order: store lines in a **segment tree over the \(x\)-domain**. Each node holds one line that is best on a portion of that segment; when inserting a new line, compare with the stored line at mid, keep the better one at mid, and recurse into the side where the new line might win. Queries traverse root→leaf evaluating \(O(\log)\) candidate lines.

---

#### 4. Proof Sketches & Recurrences

Node covers \(x\in[L,R]\); stores line \(cur\). Insert line \(nw\):
1. Let \(mid=(L+R)/2\).
2. If \(nw\) better than \(cur\) at \(mid\), swap \(nw\leftrightarrow cur\).
3. If \(L=R\) stop.
4. If \(nw\) better than \(cur\) on the left end, recurse left; else recurse right  
   (because lines cross at most once: the winner on one side is determined).

Query \(x\): walk to leaf, take min of `eval` of all lines on the path.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: compress \(x\) / set domain size \(X\)
- Per-query / per-operation: \(O(\log X)\) insert and query (dynamic nodes \(O(\log X)\) memory each insert)
- Total: \(O(n\log X)\)
- Memory: \(O(n\log X)\) worst case with dynamic nodes`

##### C++17 Template

```cpp
// C++17 — Li Chao for min lines on compressed x in [0..X]
#include <bits/stdc++.h>
using namespace std;

namespace lichao {
using ll = long long;
const ll INF = 4e18;

struct Line {
    ll m, b;
    ll eval(ll x) const { return m * x + b; }
};

struct LiChao {
    struct Node {
        Line ln;
        int l = -1, r = -1;
        Node(Line L = {0, INF}) : ln(L) {}
    };
    vector<Node> tr;
    int X; // domain 0..X inclusive

    explicit LiChao(int X) : X(X) {
        tr.reserve(1 << 20);
        tr.push_back(Node());
    }

    int new_node() {
        tr.push_back(Node());
        return (int)tr.size() - 1;
    }

    void add_line(Line nw, int idx, int L, int R) {
        int mid = (L + R) >> 1;
        bool lef = nw.eval(L) < tr[idx].ln.eval(L);
        bool midb = nw.eval(mid) < tr[idx].ln.eval(mid);
        if (midb) swap(nw, tr[idx].ln);
        if (L == R) return;
        if (lef != midb) {
            if (tr[idx].l == -1) tr[idx].l = new_node();
            add_line(nw, tr[idx].l, L, mid);
        } else {
            if (tr[idx].r == -1) tr[idx].r = new_node();
            add_line(nw, tr[idx].r, mid + 1, R);
        }
    }

    void add(ll m, ll b) { add_line({m, b}, 0, 0, X); }

    ll query(ll x, int idx, int L, int R) const {
        if (idx == -1) return INF;
        ll ans = tr[idx].ln.eval(x);
        if (L == R) return ans;
        int mid = (L + R) >> 1;
        if (x <= mid) return min(ans, query(x, tr[idx].l, L, mid));
        return min(ans, query(x, tr[idx].r, mid + 1, R));
    }

    ll query(ll x) const { return query(x, 0, 0, X); }
};
} // namespace lichao
```

##### Python 3 Template

```python
INF = 10**30

class LiChao:
    __slots__ = ("m", "b", "left", "right", "L", "R")
    def __init__(self, L, R):
        self.L, self.R = L, R
        self.m, self.b = 0, INF
        self.left = self.right = None
    def eval(self, x):
        return self.m * x + self.b
    def add(self, m, b):
        self._add(m, b, self.L, self.R)
    def _add(self, m, b, L, R):
        mid = (L + R) // 2
        # compare and recurse (mirror C++)
        ...
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Need \(\min_j m_j x+c_j\) but inserts/queries in arbitrary order.
- \(x\) coordinates are in a known range or compressible to \(1..n\).
- “Dynamic CHT” / “add line, query point” online.
- Segments of lines (line only valid on \([L,R]\)) → Li Chao on that range (segment add).

---

#### 7. Contest WA / TLE / RE Traps

- Domain not covering all query \(x\) (compress consistently).
- Overflow in `m*x+b` — use careful types / `__int128` if needed.
- Min vs max: flip comparisons.
- Recursing into wrong child after swap.
- Using floating domain without discretization when \(x\) huge but sparse.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Segment add**: insert line only on \([ql,qr]\) — standard segtree split + Li Chao node.
- **Max Li Chao**.
- **Persistent Li Chao** for rollback / versions.
- Prefer **deque CHT** when monotone — much faster constants.

---

#### 11. Typical Problem Archetypes

1. Standard: online add line + query min at \(x\).
2. Slightly disguised: DP where \(j\) processed out of slope order.
3. Difficult: lines valid on intervals; segment Li Chao.
4. Very difficult: Li Chao + another DS dimension; persistent.

---

#### 12. Recognition & Identification Drills

1. Process updates “add line” and queries “min at x” interleaved arbitrarily.
2. Same as CHT classic but \(h_i\) not sorted.
3. Line added only for \(x\in[L,R]\). Structure?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: CHT without monotone slope/query order.
- Key invariant: lines cross ≤ once; keep better line at mid.
- Key formula: point query over envelope via segtree path.
- Complexity: \(O(\log X)\) per op.
- Template to remember: compare at mid; swap; recurse one side.

**Simpler DP passes when:** few lines — brute all lines per query; or offline sort to reduce to deque CHT.

---

→ Continue: [`10-b-monotone-queue-stack-dp-bitset-sos.md`](10-b-monotone-queue-stack-dp-bitset-sos.md) (monotone queue/stack, bitset, SOS).

---


---

<a id="topic-5"></a>
### 5. Monotone queue optimization

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** DP, `deque`, sliding-window minimum  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: DP, `deque`, sliding-window minimum

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

When

\[
dp[i]=\min_{i-w\le j\le i-1} \bigl(dp[j]+f(j)\bigr)+g(i)
\]

(or any form where the best \(j\) in a **sliding window** is what you need), candidates that are older and worse than a newer one are never useful again. Maintain a deque of indices with **increasing \(dp[j]+f(j)\)** (for min); pop front out of window; pop back dominated. Each index enter/leave once → \(O(n)\).

---

#### 4. Proof Sketches & Recurrences

Let \(v[j]=dp[j]+f(j)\). Need \(\min_{j\in[L_i,R_i]} v[j]\). If \(L_i,R_i\) both nondecreasing (sliding), deque works. Amortized \(O(1)\) per \(i\): each \(j\) pushed/popped ≤ once.

If \(cost(j,i)\) is not separable, you need **D&C / CHT / QI** instead — monotone queue alone is insufficient.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) if `add`/`fee` ready
- Per-query / per-operation: amortized \(O(1)\) per index
- Total: \(O(n)\) per DP layer
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Fixed window length \(w\): “last at most \(w\) steps”.
- \(dp[i]=\min_{j\in[i-r,i-l]} dp[j]+cost\) with cost separable as \(A_j+B_i\).
- Multiple knapsacks with bounded consecutive choices.
- After rewriting, transition depends only on a range-min of a precomputed array.
- **Vs monotone stack:** queue = window by index distance; stack = window by value dominance (next greater).

---

#### 7. Contest WA / TLE / RE Traps

- Window bounds: `[i-W, i-1]` vs `[i-W, i]` inclusive mistakes.
- Pop condition `>` vs `>=` (strictness / stability).
- Pushing `i` before computing `dp[i]` (use `i-1`).
- Non-separable cost — queue gives wrong answer.
- Multiple layers forgetting to clear deque.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Max** queue: reverse inequalities.
- **Two ends** / different \(L_i,R_i\) if both monotone.
- **0-1 knapsack** monotone queue on residual capacity (bounded item count).
- Combine with binary lifting / sparse table if windows arbitrary (not sliding) — different tool.

---

#### 11. Typical Problem Archetypes

1. Standard: jump game with window costs; hotel stays within \(k\) days.
2. Slightly disguised: rearrange recurrence until `min` of `dp[j]+add[j]` appears.
3. Difficult: monotone queue inside each residue class (mod \(k\)).
4. Very difficult: queue + CHT hybrid when both structures appear.

---

#### 12. Recognition & Identification Drills

1. \(dp[i]=\min_{i-k\le j<i} dp[j]+|a_i-a_j|\). Separable? Queue?
2. Partition into groups of length in \([L,R]\); cost = group sum squared.
3. Bounded knapsack: at most \(c\) copies of item weight \(w\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: sliding-window min/max of DP candidates.
- Key invariant: deque increasing by key; front = best.
- Key formula: \(dp[i]=\min_{j\in window} (dp[j]+f[j])+g[i]\).
- Complexity: \(O(n)\).
- Template to remember: pop back dominated; pop front out of window.

**Simpler DP passes when:** \(n\cdot W\) small — nested loops fine.

---

## 6. Monotone stack DP

---


---

<a id="topic-6"></a>
### 6. Monotone stack DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Next greater/smaller element, contribution trick, basic DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Next greater/smaller element, contribution trick, basic DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

For arrays, many DP / counting / sum-of-subarray-function problems reduce to: for each position \(i\), find the largest segment where \(a_i\) is the strict (or non-strict) maximum/minimum. A **monotone stack** computes previous/next greater in \(O(n)\). Then:

- Contribution: \(a_i\) adds \(a_i\cdot left\cdot right\) to “sum of mins/maxs of all subarrays”.
- DP: \(dp[i]\) = best using a segment ending at \(i\) whose max is \(a_i\), jumping to `prev_greater[i]`.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) NGE / contribution setup
- Per-query / per-operation: \(O(1)\) after arrays built
- Total: \(O(n)\) typical
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Subarrays where max/min is …” / sum of f(max) over subarrays.
- Histogram largest rectangle (classic stack).
- DP transition “go back until a larger obstacle”.
- Cartesian tree structure (stack builds tree; DP on tree).
- Vs queue:** stack answers **value-monotone** ranges, not fixed index windows.

---

#### 7. Contest WA / TLE / RE Traps

- Strict vs non-strict inequalities → double-counting equal elements.
- Sentinels wrong (`0` / `n+1`).
- Using stack for fixed index window (should be queue).
- Off-by-one in `left * right` contribution lengths.
- Assuming \(O(n)\) folding for a DP without verifying the merge invariant.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Next smaller / previous smaller.
- Cartesian tree DP.
- Contribution of max AND min (two stacks).
- Stack + segtree for richer aggregates while popping.

---

#### 11. Typical Problem Archetypes

1. Standard: largest rectangle; sum of subarray minimums.
2. Slightly disguised: DP where transition jumps to previous greater barrier.
3. Difficult: count pairs / triples with stack + combinatorics.
4. Very difficult: stack DP on trees / with updates.

---

#### 12. Recognition & Identification Drills

1. Sum over all subarrays of (max - min).
2. For each \(i\), largest \(j\) with \(\max(a[j..i])=a[i]\).
3. DP cover array; cost of segment = its maximum — aim better than \(O(n^2)\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: ranges ruled by nearest greater/smaller.
- Key invariant: stack monotone by value.
- Key formula: contribution \(a_i\cdot L_i\cdot R_i\); or DP jump to `prev_gt`.
- Complexity: \(O(n)\).
- Template to remember: while top dominated, pop; set prev/next; push.

**Simpler DP passes when:** \(n\le 5000\) for \(O(n^2)\) subarray enumeration.

---

## 7. Bitset DP

---


---

<a id="topic-7"></a>
### 7. Bitset DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Bitset / bitwise ops, classic knapsack & Floyd-like DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Bitset / bitwise ops, classic knapsack & Floyd-like DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Boolean (or small-int mod) DP over a large universe of sums/positions can be packed into machine words. Shifting and OR-ing a `std::bitset` or raw `uint64_t[]` gives a **\(64\times\)** (or word-size) speedup on transitions like “reach new sum = old sum + w”. Same idea for path existence, digit DP compressions, and some \(O(n^3)/64\) graph problems.

---

#### 4. Proof Sketches & Recurrences

Subset sum:

```
bitset<S+1> dp; dp[0]=1;
for w in items: dp |= (dp << w);
```

Each `<<` and `|` on \(S/64\) words → \(O(nS/w)\).

For bounded counts, loop reverse like knapsack or use multiple shifts.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: check bit \(O(1)\)
- Total: \(O(nS/64)\) subset sum; \(O(n^3/64)\) bitset Floyd
- Memory: \(O(S/64)\) or \(O(n^2/64)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Knapsack **existence** / reachable sums; subset sum.
- \(dp[i][s]\) boolean with transitions \(s\to s+a_i\).
- Floyd Warshall / transitive closure with bitsets.
- “Can you form k?” with many items.
- Need speed from \(O(nS)\) to \(O(nS/64)\).

---

#### 7. Contest WA / TLE / RE Traps

- `bitset` size not compile-time constant when needed — use templates / max bound.
- Shifting beyond size silently truncates — ensure `MAXS > S`.
- Using bitset for **values** not booleans (need SOS / other).
- Off-by-one on reachable index \(S\).
- Reverse-order knapsack confusion when mixing classic array DP with bitset (bitset `<<` is multi-use in one step — like unbounded if you loop wrong; for 0-1, single `|= << w` per item is correct).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Meet-in-the-middle + bitset.
- Bitset optimization of DP on broken profile (narrow grids).
- `__int128` manual for small \(S\le 128\).
- GCC `bitset` `_Find_first` / `_Find_next` for enumerating set bits.

---

#### 11. Typical Problem Archetypes

1. Standard: subset sum existence; partition equal sum.
2. Slightly disguised: scheduling reachability of timelines.
3. Difficult: bitset + SOS hybrid; or \(k\)-sum with bitset layers.
4. Very difficult: bitset inside D&C / offline queries.

---

#### 12. Recognition & Identification Drills

1. \(n\le 1000\) weights, \(S\le 10^6\), existence of subset sum — complexity target?
2. Transitive closure \(n=4000\) — how?
3. 0-1 knapsack maximizing value with \(S\le 10^5\) — bitset enough?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: boolean DP over sums/graphs word-packable.
- Key invariant: word-parallel OR/AND/shifts.
- Key formula: `dp |= dp << w`.
- Complexity: \(O(nS/64)\).
- Template to remember: `bitset` + shift-or for 0-1 items.

**Simpler DP passes when:** \(nS\le 10^7\) classic bool array is fine.

---

## 8. SOS DP

---


---

<a id="topic-8"></a>
### 8. SOS DP (Sum over Subsets) — primary home

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Bitmasks, inclusion on the subset lattice, iterative DP over bits  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Bitmasks, inclusion on the subset lattice, iterative DP over bits

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Given values \(A[mask]\) on \(\{0,1\}^n\), many tasks need

\[
Z[S]=\sum_{T\subseteq S} A[T]
\qquad\text{or}\qquad
M[S]=\sum_{T\supseteq S} A[T]
\]

Naively \(O(3^n)\). **SOS DP / fast zeta transform** does it in \(O(2^n\cdot n)\): for each bit \(b\), “push” contributions along that bit dimension (like a high-dimensional prefix sum on the boolean cube).

Möbius inversion recovers \(A\) from \(Z\):

\[
A[S]=\sum_{T\subseteq S}(-1)^{|S\setminus T|}Z[T]
\]

also in \(O(2^n n)\) (fast Möbius).

This is the engine under OR-convolutions, subset-sum style bit DP aggregations, and “for each mask, combine all submasks”.

---

#### 4. Proof Sketches & Recurrences

**Submask zeta (sum over subsets):** interpret \(A\) as values on an \(n\)-dimensional \(0/1\) grid. Prefix along dimension \(b\):

```
f = A
for b in 0..n-1:
  for mask in 0..(1<<n)-1:
    if mask & (1<<b):
      f[mask] += f[mask ^ (1<<b)]
```

Invariant after processing bits \(0..b\): \(f[S]\) sums \(A[T]\) over \(T\) that may differ from \(S\) only in bits \(\le b\) (and \(T\subseteq S\)). At the end, \(f[S]=\sum_{T\subseteq S}A[T]\).

**Superset zeta (sum over supersets):**

```
if (mask & (1<<b)) == 0:
  f[mask] += f[mask | (1<<b)]
```
(order of loops carefully; common form iterate bits, then masks).

**Möbius (invert submask zeta):**

```
for b in 0..n-1:
  for mask:
    if mask & (1<<b):
      f[mask] -= f[mask ^ (1<<b)]
```

**Submask enumeration** (still useful when you need every pair \((S,T\subseteq S)\)):

```
for (int s = 0; s < (1<<n); ++s)
  for (int t = s; t; t = (t - 1) & s)
    // use t
  // also t=0
```
Total \(O(3^n)\). Prefer SOS when only **aggregates** matter.

**OR convolution** via zeta: for \(h=f\ast_{OR} g\) meaning \(h[S]=\sum_{i|j=S}f[i]g[j]\),

1. \(F=\zeta f\), \(G=\zeta g\) (submask sums)
2. \(H[S]=F[S]\cdot G[S]\) pointwise
3. \(h=\mu H\) (Möbius)

(Exact identities vary for AND/OR; XOR uses FWHT.)

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(2^n)\) fill of \(A\)
- Per-query / per-operation: \(O(1)\) after transform if answers are \(Z[S]\)
- Total: \(O(2^n\cdot n)\) per zeta/Möbius; submask enum \(O(3^n)\)
- Memory: \(O(2^n)\)`

##### C++17 Template

```cpp
// C++17 — SOS DP: zeta / Möbius on subset lattice
#include <bits/stdc++.h>
using namespace std;

namespace sos {
using ll = long long;

// In-place sum over subsets: f[S] <- sum_{Tsubseteq S} f[T]
void zeta_subsets(vector<ll>& f) {
    int N = (int)f.size(); // N = 1<<n
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] += f[mask ^ b];
}

// Inverse: recover A from Z
void mobius_subsets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] -= f[mask ^ b];
}

// Sum over supersets: f[S] <- sum_{T supseteq S} f[T]
void zeta_supersets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (!(mask & b)) f[mask] += f[mask | b];
}

void mobius_supersets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (!(mask & b)) f[mask] -= f[mask | b];
}

// Pointwise max over submasks (common contest variant)
void zeta_subsets_max(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] = max(f[mask], f[mask ^ b]);
}

// Enumerate all submasks of m: O(3^n) total over all m if done for all
template<class F>
void for_submasks(int m, F &&consume) {
    for (int s = m;; s = (s - 1) & m) {
        consume(s);
        if (!s) break;
    }
}

// OR-convolution h[s] = sum_{i|j = s} f[i]*g[j]
vector<ll> or_convolution(vector<ll> f, vector<ll> g) {
    int N = (int)f.size();
    zeta_subsets(f);
    zeta_subsets(g);
    vector<ll> h(N);
    for (int i = 0; i < N; ++i) h[i] = f[i] * g[i];
    mobius_subsets(h);
    return h;
}

// Classic: dp[mask] = sum of a[i] over i in mask, then queries SOS
vector<ll> sum_over_submasks_values(const vector<ll>& a) {
    // a indexed by mask already
    vector<ll> f = a;
    zeta_subsets(f);
    return f;
}

// DP: for each mask, best over submasks of popcount transition example
// f[mask] += product over bit contributions — place problem-specific code atop zeta
} // namespace sos
```

##### Python 3 Template

```python
def zeta_subsets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if mask & b:
                f[mask] += f[mask ^ b]
        b <<= 1
    return f

def mobius_subsets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if mask & b:
                f[mask] -= f[mask ^ b]
        b <<= 1
    return f

def zeta_supersets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if not (mask & b):
                f[mask] += f[mask | b]
        b <<= 1
    return f

def or_convolution(f, g):
    f, g = f[:], g[:]
    zeta_subsets(f)
    zeta_subsets(g)
    h = [f[i] * g[i] for i in range(len(f))]
    mobius_subsets(h)
    return h
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “For every mask, sum/fmax over all submasks / supermasks”.
- Enumerating submasks \(O(3^n)\) appears; \(n\le 20\)–\(22\) with need for \(2^n n\).
- Problems: sum of AND/OR over pairs; DP over subsets with submask transitions that only need aggregates.
- After computing \(f[S]\), need \(g[S]=\sum_{T\subseteq S}f[T]\).
- Keywords: zeta transform, Möbius on subset lattice, FWHT cousin (XOR is different — Walsh–Hadamard).
- **Stub elsewhere:** bit/combinatorics section links here for full treatment.

---

#### 7. Contest WA / TLE / RE Traps

- Mixing subset vs superset transforms (wrong `if` on bit).
- Forgetting mod normalization on Möbius subtract.
- Using XOR-FWHT identities for OR/AND (wrong).
- In-place transform then needing original \(A\) — copy first.
- \(n\) not matching `f.size()==1<<n`.
- Off-by-one: empty mask handling in enumeration.
- Overflow on products in OR-convolution before Möbius.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Max / min / gcd / OR** over submasks (same loop, change `+=` to op; not all invertible).
- **Fast subset convolution** \(h[S]=\sum_{T\subseteq S}f[T]g[S\setminus T]\) in \(O(2^n n^2)\) — advanced; Niche early.
- **AND convolution** via superset zeta or bit-complementation tricks.
- **Weighted popcount layers** for subset convolution.
- Online SOS / segmented — rare.

---

#### 11. Typical Problem Archetypes

1. Standard: given \(a[mask]\), answer \(\sum_{T\subseteq S}a[T]\) for all \(S\).
2. Slightly disguised: for each mask, max value among submasks; then DP.
3. Difficult: OR/AND convolution counting pairs with \(i|j=k\).
4. Very difficult: subset convolution / FWHT hybrids / high constraints \(n=23\).

---

#### 12. Recognition & Identification Drills

1. Array \(a[0..2^n-1]\); for each \(x\), compute sum of \(a[y]\) over \(y\subseteq x\). Target complexity?
2. Count pairs \((i,j)\) with \(a_i|a_j=X\) for all \(X\).
3. \(dp[S]=\sum_{T\subseteq S} dp[T]\cdot cost[S\setminus T]\) — SOS enough or need subset convolution?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: aggregates over submasks/supermasks; OR/AND lattice convolutions.
- Key invariant: boolean-cube prefix sums bit by bit.
- Key formula: `if (mask&b) f[mask]+=f[mask^b]` (subset zeta).
- Complexity: \(O(2^n n)\).
- Template to remember: zeta → pointwise → Möbius for OR-conv; copy before in-place.

**Simpler DP passes when:** only few masks queried — enumerate submasks of those; or \(n\le 16\) and \(3^n\) OK (\(\sim 43M\)).

---

→ Continue: [`10-c-profile-dp-alien-wqs.md`](10-c-profile-dp-alien-wqs.md) (profile DP, Alien, WQS, recognition synthesis).

---


---

<a id="topic-9"></a>
### 9. Profile / state-compression DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Bitmask DP, grid / tiling intuition, DFS/BFS on transitions between masks  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Bitmask DP, grid / tiling intuition, DFS/BFS on transitions between masks

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

When one dimension is tiny (width \(w\le 10\)–\(20\)), process the grid **column by column** (or row by row). The “profile” is a bitmask of which cells in the current column are already filled / need matching from a previous half-tile / store connectivity state. Transitions enumerate ways to place tiles that are consistent with the incoming profile and produce an outgoing profile for the next column. Complexity \(\sim O(\text{cols}\cdot 2^w\cdot \text{trans})\); precompute transitions if the plug DP graph is static.

---

#### 4. Proof Sketches & Recurrences

Domino tiling classic: for column \(c\), mask bit \(i\) means row \(i\) is **occupied by a vertical domino sticking out** (or empty needing fill — be consistent). Recurse cell-by-cell inside the column:

```
dfs(row, cur_mask, next_mask):
  if row == h: trans[cur_mask].push(next_mask); return
  if cur_mask already filled at row: dfs(row+1, ...)
  else:
    place vertical: set bit in next_mask; dfs(row+1,...)
    place horizontal if row+1 free: fill both; dfs(row+2,...)
```

Then `dp[c+1][next] += dp[c][cur]` over transitions. Empty start/end masks must be 0.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(2^h\cdot \mathrm{poly}(h))\) transition build (often \(O(3^{h/2})\)–style via DFS)
- Per-query / per-operation: N/A
- Total: \(O(w\cdot 2^h\cdot \mathrm{avg\_deg})\)
- Memory: \(O(2^h\cdot \mathrm{avg\_deg})\) for transitions + \(O(2^h)\) DP`

##### C++17 Template

```cpp
// C++17 — domino tiling profile DP on h x w grid, h <= 20, w large
#include <bits/stdc++.h>
using namespace std;

namespace profile_dp {
using ll = long long;

struct DominoTiling {
    int h, w;
    vector<vector<int>> trans; // cur -> list of next masks

    DominoTiling(int h, int w) : h(h), w(w) { rebuild_all(); }

    void gen(int row, int cur, int nxt) {
        if (row == h) {
            trans[cur].push_back(nxt);
            return;
        }
        // bit of `cur`: cell already filled by previous column's vertical domino
        if ((cur >> row) & 1) {
            gen(row + 1, cur, nxt);
            return;
        }
        // vertical domino: occupies this cell now, protrudes into next column
        gen(row + 1, cur, nxt | (1 << row));
        // two-row block in this column (one vertical domino standing in-column)
        if (row + 1 < h && !((cur >> (row + 1)) & 1))
            gen(row + 2, cur, nxt);
    }

    void rebuild_all() {
        trans.assign(1 << h, {});
        for (int cur = 0; cur < (1 << h); ++cur)
            gen(0, cur, 0);
    }

    ll count() {
        vector<ll> dp(1 << h), ndp(1 << h);
        dp[0] = 1;
        for (int col = 0; col < w; ++col) {
            fill(ndp.begin(), ndp.end(), 0);
            for (int m = 0; m < (1 << h); ++m) if (dp[m])
                for (int nxt : trans[m]) ndp[nxt] += dp[m];
            swap(dp, ndp);
        }
        return dp[0];
    }
};
} // namespace profile_dp
```

##### Python 3 Template

```python
# Usable for h <= 10, w <= 100 in PyPy; prefer C++ when h >= 12

def domino_count(h, w):
    trans = [[] for _ in range(1 << h)]

    def gen(row, cur, nxt):
        if row == h:
            trans[cur].append(nxt)
            return
        if (cur >> row) & 1:
            gen(row + 1, cur, nxt)
            return
        gen(row + 1, cur, nxt | (1 << row))  # protrude vertical into next col
        if row + 1 < h and not ((cur >> (row + 1)) & 1):
            gen(row + 2, cur, nxt)  # fill two rows in this column

    for cur in range(1 << h):
        gen(0, cur, 0)

    dp = [0] * (1 << h)
    dp[0] = 1
    for _ in range(w):
        ndp = [0] * (1 << h)
        for m, v in enumerate(dp):
            if not v: continue
            for nxt in trans[m]:
                ndp[nxt] += v
        dp = ndp
    return dp[0]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Grid \(n\times m\) with \(n\cdot m\le 100\) but one side \(\le 10\)–\(12\).
- Tiling with dominoes / trominoes / “fill without holes”.
- Hamiltonian paths on narrow grids; colorings with local constraints.
- Broken profile: state includes “connected components touching the frontier” (more bits / DSU hash — harder).
- Statement screams \(2^{w}\) DP after you rotate the grid so \(w=\min(n,m)\).

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to rotate grid so height is the small side.
- Allowing holes (skipping a cell without placing a tile).
- Final mask must be \(0\) (no pending verticals).
- Double-counting tiles; inconsistent meaning of bits.
- Connectivity profile: hashing DSU wrongly → WA.
- Overflow without mod.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Tromino / larger polyominoes.
- Broken profile connectivity (plug DP / Chinese “contour DP”).
- Colorings, independent sets on grids (transfer matrix = same idea).
- Profile + digit constraints.

---

#### 11. Typical Problem Archetypes

1. Standard: count domino tilings of \(n\times m\).
2. Slightly disguised: place kings/bishops with mask of previous column attacks.
3. Difficult: connectivity of empty cells / “all floors connected”.
4. Very difficult: plug DP for Hamiltonian cycles on grids.

---

#### 12. Recognition & Identification Drills

1. \(3\times n\) tiling with dominoes — state space?
2. \(n\times m\) grid, \(n\le 8\), count independent sets.
3. Fill grid with “+” shapes — profile or dancing links?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: narrow grid + local tile/constraint transfer.
- Key invariant: profile mask = frontier occupation/connectivity.
- Key formula: \(dp[c+1][nxt]=\sum_{cur\to nxt}dp[c][cur]\).
- Complexity: \(O(w\cdot 2^h\cdot \deg)\).
- Template to remember: DFS generate transitions; DP over columns.

**Simpler DP passes when:** total cells \(\le 20\) — plain subset / backtrack; or closed formulas for tiny heights.

---

## 10. Alien trick / Lagrangian relaxation

---


---

<a id="topic-10"></a>
### 10. Alien trick / Lagrangian relaxation

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2300–3000 | **Frequency:** Occasional  
> **Prerequisites:** DP with an extra cardinality dimension, convexity/concavity of optimal cost vs \(k\), binary search intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2300–3000
- Prerequisites: DP with an extra cardinality dimension, convexity/concavity of optimal cost vs \(k\), binary search intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

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

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: one penalized DP per probed \(\lambda\)
- Total: \(O((\text{cost of DP})\cdot\log\Lambda)\)
- Memory: as in inner DP`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Exactly / at most \(k\) segments” but \(O(nk)\) or \(O(nk\log)\) too slow; \(n\) large, \(k\) large.
- Editorial words: Alien trick, wqs, Lagrangian relaxation, “penalty on number of groups”.
- You can solve unrestricted (or only soft-penalized) DP fast (CHT / D&C / Dijkstra).
- Plot of best cost vs \(k\) looks convex (check small \(n\)).
- Vs WQS:** Alien emphasizes the relaxation + DP; WQS emphasizes binary search on \(\lambda\). Same family — see next subsection.

---

#### 7. Contest WA / TLE / RE Traps

- Applying without convexity → WA.
- Wrong direction when comparing `parts` vs `need`.
- Not handling ties (`parts` jumps over target \(k\)).
- Recovering answer as `pen` instead of `pen - lambda*k`.
- \(\lambda\) bounds too tight; overflow when \(\lambda\cdot k\).
- Maximization problems need sign flips (concave \(opt\)).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- At most \(k\) / at least \(k\) (often easier: monotone check).
- Multiple constraints (multi-dimensional Alien — rare, very hard).
- Fractional / slope trick viewpoint (same math as CHT conjugates).
- Combine with CHT/D&C inside penalized DP.

---

#### 11. Typical Problem Archetypes

1. Standard: split into exactly \(k\) segments; large \(n,k\).
2. Slightly disguised: choose exactly \(k\) “expensive operations” on a path.
3. Difficult: ties; need secondary criterion.
4. Very difficult: prove convexity from QI; nested optimizations.

---

#### 12. Recognition & Identification Drills

1. \(n=1e5\), split into exactly \(k=1e5\) segments, cost convex in segments — options?
2. Same but \(opt(k)\) not convex — what fails?
3. Maximize score with exactly \(k\) groups — how does \(\lambda\) move?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: exact \(k\) parts + convex \(opt(k)\) + fast penalized DP.
- Key invariant: discrete convexity of \(opt(k)\).
- Key formula: \(g(\lambda)=\min(opt(k)+\lambda k)\); answer \(g-\lambda k\).
- Complexity: DP cost \(\times\log\Lambda\).
- Template to remember: binsearch \(\lambda\); DP returns `(penalized, parts)`.

**Situational / hard.** If \(k\) small, keep explicit dimension. Prefer not forcing Alien.

---

## 11. WQS binary search

---


---

<a id="topic-11"></a>
### 11. WQS binary search

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2300–3000 | **Frequency:** Occasional  
> **Prerequisites:** Alien trick family, binary/ternary search, DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2300–3000
- Prerequisites: Alien trick family, binary/ternary search, DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

**WQS** (from OI folklore / “wqs二分”) is the standard **binary search on the Lagrangian multiplier** for the Alien setup. Same mathematics: search the slope \(\lambda\) such that the concave conjugate touches at the desired \(k\). Naming emphasis: treat \(\lambda\) as the search key; each check runs a \(k\)-free DP and reads off the optimal number of parts.

Use when you already know Alien applies and need a concrete search procedure (including integer \(\lambda\) and tie-breaking conventions used in Chinese OI blogs).

---

#### 4. Proof Sketches & Recurrences

Identical conjugate:

\[
\text{check}(\lambda):\quad \min_P cost(P)+\lambda\cdot\kappa(P),\quad \text{observe }\kappa(P^\*).
\]

Because \(\kappa^\*(\lambda)\) is nonincreasing in \(\lambda\), binary search works. For integer costs, \(\lambda\) often integer in a bounded range; if not, search reals with enough iterations, or search on **slopes between consecutive hull points** (fractional \(\lambda=p/q\) via cross).

**Fractional binary search / deterministic slope:** when you need exact touch at \(k\), maintain the lower hull of points \((k,opt(k))\) implicitly; WQS finds the supporting line with the right contact \(k\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: 1 DP per mid
- Total: \(O(\mathrm{DP}\cdot\log\Lambda)\) or \(\mathrm{DP}\cdot\#iters\)
- Memory: inner DP`

##### C++17 Template

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

##### Python 3 Template

```python
# Given opt[k] for k in range, find min opt[k]+lambda*k
def g(opt, lam):
    return min(opt[k] + lam * k for k in opt)

def best_k(opt, lam):
    return min(opt, key=lambda k: opt[k] + lam * k)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Same as Alien; editorials say “wqs二分”.
- Minimizing \(f(x)+g(k)\) style with convex \(g\) or convex tradeoff.
- After fixing \(\lambda\), the problem reduces to a classical DP you already coded.
- Graph problems: “exactly \(k\) edges of type B” → weight shift on those edges + shortest path.

---

#### 7. Contest WA / TLE / RE Traps

- Same as Alien: convexity, tie-breaking, answer recovery.
- Floating \(\lambda\) precision → wrong `parts`.
- Searching max problems with min template.
- Off-by-one on `parts > K` branch.
- Claiming WQS when the tradeoff is non-convex (must use explicit \(k\) DP).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **At most \(K\)**: often take \(\lambda=0\) or clamp after unpenalized; or still search if unconstrained optimum uses fewer.
- **Graph WQS**: add \(\lambda\) to every chosen special edge; binary search until path uses \(K\) specials.
- **Ternary search** on \(\lambda\) when unimodal \(g\) alone is used (less common than binsearch on monotone `parts`).

---

#### 11. Typical Problem Archetypes

1. Standard: OI-style “exactly \(k\) segments” with WQS + DP.
2. Slightly disguised: exactly \(k\) red edges on shortest path.
3. Difficult: need fractional slopes; hull edges between integer \(k\).
4. Very difficult: two-parameter WQS.

---

#### 12. Recognition & Identification Drills

1. Shortest path with exactly \(k\) special edges — model \(\lambda\).
2. Minimize cost with exactly \(k\) groups; inner DP is CHT — outline solution.
3. When does binary search on answer **not** equal WQS?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: Alien applicable; search \(\lambda\) until `#parts=K`.
- Key invariant: `#parts(\lambda)` monotone in \(\lambda\).
- Key formula: answer \(=pen-\lambda K\) at the touching \(\lambda\).
- Complexity: \(\mathrm{DP}\cdot\log\Lambda\).
- Template to remember: `while lo<=hi` mid; `if parts>K: lo=mid+1`.

**Situational / hard.** Default to explicit-\(k\) DP when it fits TL.

---

## 12. DP optimization recognition patterns

---


---

<a id="topic-12"></a>
### 12. DP optimization recognition patterns (synthesis)

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier | **Rating Range:** 1800–2600 | **Frequency:** Common  
> **Prerequisites:** Exposure to techniques 1–11 in this section  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2600
- Prerequisites: Exposure to techniques 1–11 in this section

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Optimizations are not random speed hacks — each requires a **structural property**:

| Property | Points to |
|----------|-----------|
| Decision monotonicity \(opt(j)\le opt(j+1)\) | D&C DP |
| Quadrangle inequality + interval merge | Knuth |
| Transition = min of lines | CHT / Li Chao |
| Sliding index window | Monotone queue |
| Ranges ruled by nearest greater/smaller | Monotone stack |
| Boolean / word-parallel | Bitset |
| Lattice aggregates on submasks | SOS |
| Narrow frontier | Profile DP |
| Exact \(k\) + convex \(opt(k)\) | Alien / WQS |

**Flow:** write naive recurrence → name the property → pick the lightest tool that fits → if \(n\) already allows naive, **ship naive**.

---

#### 4. Proof Sketches & Recurrences

**Recognition flowchart (contest mental model):**

```text
Can naive pass?
  yes → implement naive
  no ↓
Is state a bitmask lattice aggregate?
  yes → SOS / submask enum
  no ↓
Boolean reachability / subset sum shaped?
  yes → bitset
  no ↓
Narrow grid frontier?
  yes → profile DP
  no ↓
Transition = min_j m_j*x_i + c_j ?
  yes → monotone? deque CHT : Li Chao
  no ↓
Sliding window of j for dp[i]?
  yes → monotone queue
  no ↓
Depends on nearest greater/smaller geometry?
  yes → monotone stack
  no ↓
Interval DP dp[l][r]=min_k dp[l][k]+dp[k+1][r]+C ?
  yes → QI? Knuth : naive / other
  no ↓
Layered dp[i][j]=min_t dp[i-1][t]+C(t,j) with opt monotone?
  yes → D&C DP
  no ↓
Need exactly k parts & opt(k) convex & penalized DP easy?
  yes → Alien / WQS
  no ↓
Different section (data structures, FFT, ...)
```

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: thinking time
- Per-query / per-operation: N/A
- Total: saves wrong \(O(n^2)\) attempts / wrong Knuth applications
- Memory: N/A`

##### C++17 Template

```cpp
// C++17 — not one algorithm; a checklist encoded as comments for contest headers
namespace dp_opt_recognition {
/*
Checklist before coding an optimization:
1. Constraints: what complexity needed?
2. Recurrence written cleanly with domains of min/max.
3. Property:
   - monotone opt? (D&C)
   - QI interval? (Knuth)
   - linear in j with x_i? (CHT)
   - window? (queue) / NGE? (stack)
   - bits lattice? (SOS) / bool sums? (bitset)
   - exact k convex? (Alien/WQS)
4. Prove or empirically test property on random small cases.
5. Prefer simpler structure (queue before CHT before Alien).
*/
} // namespace dp_opt_recognition
```

##### Python 3 Template

```python
def test_opt_monotone(compute_opt_array):
    opt = compute_opt_array()
    return all(opt[i] <= opt[i+1] for i in range(len(opt)-1))

def test_quadrangle(C, n):
    # C(a,c)+C(b,d) <= C(a,d)+C(b,c) for a<=b<=c<=d
    for a in range(n):
        for b in range(a, n):
            for c in range(b, n):
                for d in range(c, n):
                    if C(a,c)+C(b,d) > C(a,d)+C(b,c)+1e-9:
                        return False
    return True
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Expand algebra: squares → lines (CHT).
- “Last cut position” layered → D&C; “merge two sides” → Knuth.
- Window of length \(w\) → queue; “until bigger barrier” → stack.
- Masks + submasks sum → SOS before inventing \(3^n\) for all queries.
- \(k\) dimension only exists to count parts → Alien sniff (then prove convexity).

---

#### 7. Contest WA / TLE / RE Traps

- Optimizing without a property (D&C on non-monotone opt).
- Using Knuth for layered last-cut DP (should be D&C) and vice versa.
- CHT when cost not linear after rewrite.
- Alien because \(k\) “feels annoying” without convexity.
- Ignoring that naive passes — burned time.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Hybrid: D&C + CHT; WQS + CHT; bitset + SOS.
- Offline CDQ when online structure fails.
- Brute force property testing in stress against naive.

---

#### 11. Typical Problem Archetypes

1. Standard: classify a known problem into the table above.
2. Slightly disguised: rewrite recurrence until a row matches.
3. Difficult: two properties fire — pick cheaper (queue vs CHT).
4. Very difficult: no classical opt; need new structure / DS.

---

#### 12. Recognition & Identification Drills

1. \(dp[i][j]=\min_{t<j}dp[i-1][t]+(pref[j]-pref[t])^2\), \(n=1e5,k=200\) — name the opt(s).
2. \(dp[l][r]=\min_k dp[l][k]+dp[k+1][r]+w[l][r]\) with QI — name the opt.
3. Exactly \(k\) segments, \(n=1e5\), inner becomes CHT after \(\lambda\) — name the stack of techniques.
4. For each mask, max of \(a[t]\) over \(t\subseteq mask\) — name the opt.
5. \(dp[i]=\min_{i-k\le j<i}dp[j]+c[j]+f[i]\) — name the opt.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: always, before implementing a fancy DP.
- Key invariant: structure before asymptotics.
- Key formula: see flowchart property table.
- Complexity: naive if it passes; else match property → tool.
- Template to remember: **naive? → lattice/bitset/profile? → line/window/stack? → Knuth/D&C? → Alien?**

---

## End link

Return to hub: [`10-dp-optimizations.md`](10-dp-optimizations.md) for comparison tables and weekly drills.

---


---

<a id="topic-13"></a>
### 13. Digit DP Template

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Frequent  
> **Prerequisites:** Top-down DP (Memoization)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Frequent
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Top-down DP (Memoization)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Whenever a problem asks to count the number of integers in $[L, R]$ satisfying a certain property, we compute $solve(R) - solve(L-1)$. 
To compute $solve(X)$, we construct the number digit by digit from the most significant to the least significant. We maintain a `tight` boolean flag: if `tight` is true, the digits we can place are bounded by the current digit of $X$. If `tight` is false, we can place any digit from 0 to 9. We also often maintain a `leading_zero` boolean.

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- "Count the number of $X \in [A, B]$ such that..."
- $B$ is very large (e.g., $10^{18}$ or even 100,000 digits long).

---

#### 7. Contest WA / TLE / RE Traps

- Memoizing tight states: storing DP results when $tight = 1$ is fatal because the result depends on the specific prefix digits of $X$, not just the suffix state.
- Ignoring leading zeros: numbers like `007` have length 1, but digit DP will treat them as length 3 with leading zero digits unless a `leading_zero` flag is maintained.
- Off-by-one in $[L, R]$: when calculating $f(R) - f(L - 1)$, make sure $L = 0$ is handled safely without negative bounds.
- Forgetting to clear or reset the memoization table between multiple test cases.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-14"></a>
### 14. D&C DP vs Knuth

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Dynamic Programming, Monotonicity of Optimal Split, Quadrangle Inequality
- Tradeoff: Reduces $\mathcal{O}(K N^2)$ or $\mathcal{O}(N^3)$ 2D DP to $\mathcal{O}(K N \log N)$ or $\mathcal{O}(N^2)$ via monotonicity.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Both Divide & Conquer DP optimization and Knuth's optimization exploit the monotonicity of the optimal decision point: $\text{opt}(i, j) \le \text{opt}(i, j+1)$. 1) Use **Divide and Conquer DP** when the transition is between distinct layers $dp[k][i] = \min_{j < i} (dp[k-1][j] + \text{cost}(j, i))$. The layer structure allows solving mid-point $mid = (l + r)/2$ and dividing the search range for the remaining indices, achieving $\mathcal{O}(K N \log N)$. 2) Use **Knuth's Optimization** when the DP is interval-based $dp[i][j] = \min_{i \le k < j} (dp[i][k] + dp[k+1][j]) + \text{cost}(i, j)$ and optimal split satisfies $\text{opt}(i, j-1) \le \text{opt}(i, j) \le \text{opt}(i+1, j)$. The search space telescopically sums to $\mathcal{O}(N^2)$!

---

#### 4. Proof Sketches & Recurrences

Quadrangle Inequality: $\text{cost}(a, c) + \text{cost}(b, d) \le \text{cost}(a, d) + \text{cost}(b, c)$ for $a \le b \le c \le d$. In D&C DP, the monotonic property $\text{opt}(k, i) \le \text{opt}(k, i+1)$ allows partitioning the search interval $[\text{optL}, \text{optR}]$ at each divide-and-conquer level. In Knuth's optimization, the sum of loop bounds is $\sum_{i, j} (\text{opt}(i+1, j) - \text{opt}(i, j-1)) = \sum_{len} \mathcal{O}(N) = \mathcal{O}(N^2)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Divide and Conquer DP Optimization: O(K * N log N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll dp[25][5005];
ll cost(int j, int i); // Contest-specific cost function

void compute(int k, int l, int r, int optL, int optR) {
    if (l > r) return;
    int mid = (l + r) / 2;
    pair<ll, int> best = {1e18, -1};
    for (int j = optL; j <= min(mid, optR); ++j) {
        best = min(best, {dp[k - 1][j] + cost(j, mid), j});
    }
    dp[k][mid] = best.first;
    int opt = best.second;
    compute(k, l, mid - 1, optL, opt);
    compute(k, mid + 1, r, opt, optR);
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Partitioning an array of length $N$ into $K$ contiguous subarrays to minimize sum of costs ($K \le 50, N \le 5000$).
- Optimal binary search tree or merging adjacent elements on interval $[i, j]$ (Knuth optimization).
- Cost function satisfies Quadrangle Inequality / Monge property.
- Testing brute force reveals that $\text{opt}[i] \le \text{opt}[i+1]$ unconditionally.

---

#### 7. Contest WA / TLE / RE Traps

- Attempting D&C DP when transitions depend on the current layer (e.g., $dp[k][i]$ depends on $dp[k][j]$ where $j < i$); D&C requires dependencies to be strictly on the previous layer $k-1$.
- Knuth optimization index bounds: iterating length from smallest to largest is required so that $\text{opt}[i+1][j]$ and $\text{opt}[i][j-1]$ are already computed.
- Cost function does not satisfy Quadrangle Inequality (e.g., non-convex or non-monotonic penalties), yielding incorrect answers.
- Off-by-one errors in `min(mid, optR)` bounding inside D&C.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-15"></a>
### 15. CHT vs Li Chao

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Convex Hull Trick (CHT), Li Chao Segment Tree, Line Geometry
- Tradeoff: CHT is $\mathcal{O}(N)$ or $\mathcal{O}(N \log N)$ but requires monotonic slopes/queries or dynamic pointers (LineContainer); Li Chao Tree handles arbitrary slope/query insertions in $\mathcal{O}(\log C)$ with minimal bug surface.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

When optimizing transitions of the form $dp[i] = \min_j (dp[j] + m_j \cdot x_i + c_j)$: 1) Use **Monotonic CHT (Deque)** if slopes $m_j$ are added in sorted order and query points $x_i$ are sorted: runs in pure $\mathcal{O}(N)$ time with 15 lines of code. 2) Use **LineContainer (Dynamic CHT)** if slopes or queries arrive in arbitrary order and coordinates are continuous reals/large integers: maintains upper/lower hull via `std::set` in $\mathcal{O}(\log N)$ per operation. 3) Use **Li Chao Segment Tree** if queries are over a fixed coordinate domain $[X_{\min}, X_{\max}]$ (e.g., $[1, 10^6]$ or via coordinate compression) or when line segments (restricted intervals $[l_j, r_j]$) are inserted: stores dominant lines in segment tree nodes with trivial maintenance.

---

#### 4. Proof Sketches & Recurrences

In dynamic CHT, lines form the lower envelope of a family of affine functions. Adjacent lines intersect at $x = (c_1 - c_2) / (m_2 - m_1)$. In a Li Chao Tree over interval $[L, R]$ with midpoint $M$, inserting a new line $L_{new}$ into a node holding line $L_{cur}$ compares values at $M$: the winning line remains at the node, and the losing line can only possibly dominate in the half where it was better at the boundary. Hence, recursion descends into only one child, running in $\mathcal{O}(\log(R - L))$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Li Chao Tree for Min Queries (Handles arbitrary slopes & insertions)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 2e18;

struct Line { ll m, c; ll eval(ll x) const { return m * x + c; } };

struct LiChaoTree {
    int sz;
    vector<Line> tree;
    LiChaoTree(int sz_) : sz(sz_), tree(4 * sz_, {0, INF}) {}
    void add_line(int node, int l, int r, Line newline) {
        int mid = l + (r - l) / 2;
        bool left_better = newline.eval(l) < tree[node].eval(l);
        bool mid_better = newline.eval(mid) < tree[node].eval(mid);
        if (mid_better) swap(tree[node], newline);
        if (r - l == 1) return;
        if (left_better != mid_better) add_line(2 * node, l, mid, newline);
        else add_line(2 * node + 1, mid, r, newline);
    }
    ll query(int node, int l, int r, ll x) {
        ll res = tree[node].eval(x);
        if (r - l == 1) return res;
        int mid = l + (r - l) / 2;
        if (x < mid) return min(res, query(2 * node, l, mid, x));
        else return min(res, query(2 * node + 1, mid, r, x));
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- DP equation contains a cross term of the form $a_j \cdot b_i$.
- Slopes and query points both monotonic: implement $\mathcal{O}(N)$ Monotone CHT with `std::deque`.
- Slopes or queries are not monotonic: reach for Li Chao tree or LineContainer.
- Lines are only valid on a restricted segment $[L_j, R_j]$: Li Chao segment tree handles segment updates in $\mathcal{O}(\log^2 C)$ naturally.

---

#### 7. Contest WA / TLE / RE Traps

- Integer overflow in cross product or intersection point calculation $(c_1 - c_2) / (m_2 - m_1)$; use `__int128`.
- Division truncation in integer arithmetic: standard integer `/` rounds toward zero; floor division requires `x / y - ((x ^ y) < 0 && x % y)`.
- Querying outside the predefined $[L, R]$ coordinate range in Li Chao tree without dynamic pointer node allocation.
- Mixing up Min vs Max envelope logic when flipping sign of slopes.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-16"></a>
### 16. Alien trick vs WQS binary search

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 D/E & ICPC Regionals
- Typical CF/ICPC rating range: 2200–2700
- Prerequisites: Convex Optimization, Lagrange Multipliers, Binary Search, DP
- Tradeoff: Eliminates a state dimension $K$ (e.g. choose exactly $K$ items) from $\mathcal{O}(N K)$ down to $\mathcal{O}(N \log(\text{cost}))$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Alien's Trick and WQS Binary Search are two names for the same algorithmic technique: Lagrangian relaxation applied to convex DP. When the maximum profit $f(k)$ as a function of the number of chosen items $k$ is strictly concave (or convex for cost minimization), the constraint 'choose exactly $K$ items' can be relaxed by introducing a penalty $\lambda$ for each chosen item. By binary searching on $\lambda$, we find the slope of the tangent line touching the curve at $k = K$, solving the problem without maintaining $k$ in the DP state!

---

#### 4. Proof Sketches & Recurrences

Let $g(\lambda) = \max_k (f(k) - \lambda k)$. The function $g(\lambda)$ is the Legendre transform of $f(k)$. For a fixed $\lambda$, the unconstrained problem $\max_k (f(k) - \lambda k)$ can be evaluated in $\mathcal{O}(N)$ time, returning both the optimal value and the number of items chosen $k^*$. Since $f$ is concave, the optimal $k^*(\lambda)$ is a monotonically decreasing function of $\lambda$. Binary search on $\lambda$ finds $\lambda^*$ such that $k^*(\lambda^*) = K$. The original answer is then $g(\lambda^*) + \lambda^* K$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Problem specifies 'choose exactly $K$ disjoint subsegments/elements' to maximize/minimize total weight.
- Standard DP is $dp[i][k]$ taking $\mathcal{O}(N K)$ or $\mathcal{O}(N^2 K)$, where $K, N \le 2 \times 10^5$.
- Plotting or mathematically checking $f(k)$ shows diminishing returns (strict concavity / quadrangle inequality).
- Tree partitioning into exactly $K$ connected components with optimal weight.

---

#### 7. Contest WA / TLE / RE Traps

- Function $f(k)$ is not concave/convex; applying Aliens trick on non-convex functions yields completely wrong answers.
- Collinear points on the hull: multiple values of $k$ share the same slope $\lambda$. When tie-breaking, consistently choose either the minimum or maximum items chosen to ensure binary search converges.
- Off-by-one in binary search range $[\text{low}, \text{high}]$: penalty bounds must cover $[-2 \times \max|v|, 2 \times \max|v|]$.
- Forgetting to add back the penalty `+ best_lambda * k` to the final answer.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-17"></a>
### 17. Monotone queue vs monotone stack DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Two Pointers, Monotone Deque, Monotone Stack
- Tradeoff: Sliding window extrema vs nearest smaller/larger bounding indices.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

1) **Monotone Queue (Deque)** optimizes DP transitions over a sliding window: $dp[i] = \min_{i - W \le j < i} (dp[j]) + c_i$. The window boundaries $[i - W, i - 1]$ move monotonically to the right. A deque maintains candidate values in increasing order of cost and pops elements from the front when they fall out of the sliding window, achieving $\mathcal{O}(1)$ amortized transition. 2) **Monotone Stack** finds nearest greater/smaller elements for each position $i$ (e.g. largest rectangle in histogram, finding the maximal subsegment where $a_i$ is the minimum). The stack pops elements that violate monotonicity, but does NOT enforce a sliding window length.

---

#### 4. Proof Sketches & Recurrences

Monotone Deque invariant: for indices $j_1 < j_2$ stored in the deque, we must have $dp[j_1] < dp[j_2]$. If a newly considered index $i$ has $dp[i] \le dp[j]$, then $j$ can never be the optimum for any future window containing $i$, because $i$ is both smaller and lives longer. Thus, elements with $\ge dp[i]$ are popped from the back. Since every index is pushed and popped at most once, total amortized time across all $N$ steps is $\mathcal{O}(N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- DP transition looks like $dp[i] = \min_{j \in [i - L, i - R]} dp[j] + f(i)$ (Monotone Queue).
- Finding the left and right boundary where $a[i]$ remains the minimum/maximum of the range (Monotone Stack).
- Sliding window maximum/minimum in an array (Monotone Queue).
- Histogram rectangle area or Cartesian Tree construction (Monotone Stack).

---

#### 7. Contest WA / TLE / RE Traps

- Empty deque access: calling `dq.front()` before verifying `!dq.empty()`.
- Popping order confusion: front is popped for window expiry (`dq.front() < i - k`), back is popped for monotonicity (`dp[dq.back()] >= dp[i]`).
- Strict vs non-strict inequalities: duplicate values can cause improper early popping in monotone stack problems.
- Index offset errors between 0-indexed arrays and 1-indexed DP arrays.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-18"></a>
### 18. High-ROI (learn early in this section)

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: 1D/2D DP recurrences, Monotonicity

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

DP optimizations reduce quadratic $\mathcal{O}(N^2)$ state transitions to $\mathcal{O}(N \log N)$ or $\mathcal{O}(N)$. Prioritize learning: (1) Monotone Deque for sliding window transitions, (2) Convex Hull Trick (CHT) for linear transitions $dp[i] = \min_j (m_j x_i + c_j)$, and (3) Divide & Conquer DP for Monge cost matrices.

---

#### 4. Proof Sketches & Recurrences

When the optimal decision index satisfies $opt(i, j) \le opt(i, j+1)$, the decision space is monotone, allowing D&C recursion over index midpoints.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Monotone Deque DP Optimization Template
#include <bits/stdc++.h>
using namespace std;

struct MonotoneDeque {
    deque<pair<long long, int>> dq; // {val, index}
    void push(long long val, int idx) {
        while (!dq.empty() && dq.back().first >= val) dq.pop_back();
        dq.push_back({val, idx});
    }
    void pop_expired(int min_idx) {
        while (!dq.empty() && dq.front().second < min_idx) dq.pop_front();
    }
    long long query() { return dq.front().first; }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Transitions of the form $dp[i] = \min_{i - K \le j < i} (dp[j] + \text{cost})$.
- Cost function has negative or positive linear slope terms: $A[i] \cdot B[j]$.
- Optimal transition point moves monotonically rightward as $i$ increases.

---

#### 7. Contest WA / TLE / RE Traps

- Slopes not strictly monotonic: using standard deque CHT instead of Li Chao Tree.
- Off-by-one in window expiration bound `i - K`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-19"></a>
### 19. Situational (clear recognition pattern first)

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: CHT, Knuth Optimization, Quadrangle Inequality

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Knuth Optimization optimizes 2D interval DP $dp[i][j] = \min_{i \le k < j} (dp[i][k] + dp[k+1][j]) + C[i][j]$ from $\mathcal{O}(N^3)$ to $\mathcal{O}(N^2)$ whenever $opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$.

---

#### 4. Proof Sketches & Recurrences

Quadrangle inequality: $C[a][c] + C[b][d] \le C[a][d] + C[b][c]$ for $a \le b \le c \le d$. This ensures decision monotonicity.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Knuth 2D Interval DP Template in O(N^2)
#include <bits/stdc++.h>
using namespace std;

const long long INF = 1e18;
long long dp[505][505];
int opt[505][505];
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Interval splitting DP with Monge cost property (e.g., optimal binary search tree, polygon triangulation).
- Subarray partitioning with exact $K$ parts where cost satisfies convex quadrangle inequality.

---

#### 7. Contest WA / TLE / RE Traps

- Loop order incorrect: must iterate by increasing interval length $len = 2 \dots N$.
- Assuming Knuth applies when cost matrix violates quadrangle inequality.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-20"></a>
### 20. Rarely worth early / niche early

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2500–3000
- Prerequisites: SMAWK algorithm, 1D/1D D-search

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

SMAWK computes row minima of an implicitly defined totally monotone matrix in $\mathcal{O}(N)$ without evaluating all entries. Rarely required outside top-level onsite contests (ICPC World Finals, Petrozavodsk).

---

#### 4. Proof Sketches & Recurrences

Total monotonicity ensures that if $M_{i, j_1} \le M_{i, j_2}$, then $M_{i', j_1} \le M_{i', j_2}$ for all $i' > i$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// SMAWK framework reference for totally monotone matrices
```

---

#### 6. Recognition Trigger Signals & Heuristics

- 1D/1D DP optimization where Knuth or CHT cannot be applied due to non-linear cost.
- Subquadratic evaluation of totally monotone matrix rows.

---

#### 7. Contest WA / TLE / RE Traps

- Matrix is monotone but not totally monotone.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-21"></a>
### 21. Suggested learning order (exact subtopic order)

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2600
- Prerequisites: DP foundations, Convexity

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Follow this battle-tested mastery order: 1. Monotone Deque / Sliding Window DP $\to$ 2. Convex Hull Trick (monotone slopes) $\to$ 3. Dynamic CHT / Li Chao Tree (arbitrary lines) $\to$ 4. Divide & Conquer DP $\to$ 5. Knuth 2D Interval DP $\to$ 6. WQS Binary Search / Aliens Trick.

---

#### 4. Proof Sketches & Recurrences

Each optimization step builds upon the previous invariant: from 1D monotonicity to linear geometric envelopes, then to 2D decision intervals, and finally to Lagrangian convex relaxation.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Master DP Optimization Reference Order:
// Step 1: Deque
// Step 2: CHT
// Step 3: Li Chao
// Step 4: D&C
// Step 5: Knuth
// Step 6: Aliens Trick
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Structured learning roadmap for Div2C through Div1D problems.

---

#### 7. Contest WA / TLE / RE Traps

- Attempting Aliens trick before mastering standard CHT and binary search on gradients.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---

<a id="topic-22"></a>
### 22. What to drill this week

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: DP optimization archetypes

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

##### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

##### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

##### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

##### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

#### 3. Core Intuition & Problem Framing

Focus drills on recognizing which DP speedup applies from the mathematical form of the transition equation. Equation containing $A[i] \cdot B[j] \implies$ CHT; equation with $j \in [i-k, i] \implies$ Deque; 2D interval with Monge cost $\implies$ Knuth; exact $K$ parts with convex cost $\implies$ Aliens Trick.

---

#### 4. Proof Sketches & Recurrences

Analyzing the transition: $dp[i] = \min_j (f(j) + g(i) + h(j) \cdot k(i))$. When $h(j) \cdot k(i)$ is a product of separate functions of $j$ and $i$, it represents a line $y = m x + c$ evaluated at $x = k(i)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Contest DP Drill Check:
// 1. Write naive O(N^2) or O(N^3) DP.
// 2. Identify the bottleneck transition.
// 3. Match against the 6 speedup archetypes.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Quadratic DP passes on sample tests but TLEs on $N = 10^5$.

---

#### 7. Contest WA / TLE / RE Traps

- Prematurely optimizing before verifying the base recurrence correctness.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---


---
