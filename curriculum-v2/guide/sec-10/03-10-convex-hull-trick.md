# 3. Convex Hull Trick

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** DP rewriting as lines, deque / geometry of lower hull, integer cross products  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: DP rewriting as lines, deque / geometry of lower hull, integer cross products

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

Many DPs rewrite as

\[
dp[i]=\min_j\bigl(dp[j]+B_j+A_i\cdot X_j\bigr)
\]

For fixed \(i\), each previous \(j\) is a line \(y = m_j x + c_j\) evaluated at \(x=A_i\) (or dual). Maintaining the **lower (or upper) envelope** of lines lets each query answer in \(O(1)\) or \(O(\log n)\) after amortized inserts.

If slopes \(m_j\) are monotone **and** query \(x\) are monotone, a **deque CHT** is \(O(n)\). Otherwise use Li Chao or multiset CHT (slope-ordered).

---

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none beyond sorting if needed
- Per-query / per-operation: amortized \(O(1)\) monotone deque; \(O(\log n)\) multiset / Li Chao
- Total: \(O(n)\) monotone; \(O(n\log n)\) general
- Memory: \(O(n)\) lines`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Algebraic form: \(dp[i]=\min_j dp[j]+(x_i-x_j)^2\) expands to lines after opening squares.
- “Cost linear in something that only depends on \(i\) times something of \(j\)”.
- Transitions look like \(\min_j \{c_j + m_j\cdot x_i\}\).
- Geometric: maintain hull of lines / dual points.
- If queries offline and sortable by \(x\), sort + deque still works even if insert order needs sorting by slope.

---

## 7. Contest WA / TLE / RE Traps

- Overflow: use `__int128` for cross checks.
- Min vs max hull (sign of slope / pop conditions).
- Slopes not monotone → deque WA; switch to Li Chao.
- Queries not monotone → don’t pop front based on \(x\); binary search on hull.
- Parallel lines: handle equal slopes (keep better intercept).
- Forgetting constant terms pulled out of the min (\(h_i^2\) outside).

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

- **Max CHT**: mirror inequalities / negate.
- **Li Chao**: arbitrary order (next subsection).
- **Fully dynamic** multiset of lines (share pointers / set by slope).
- **Offline CDQ + CHT**: when both inserts and queries mixed with other dimensions.

---

## 11. Typical Problem Archetypes

1. Standard: divide into segments with squared length cost; land purchase CHT classics.
2. Slightly disguised: expand \((x_i-x_j)^2\) or \(a_i\cdot b_j\) forms.
3. Difficult: slopes not sorted — sort transitions or use Li Chao.
4. Very difficult: CHT inside D&C / CDQ; persistent hulls.

---

## 12. Recognition & Identification Drills

1. \(dp[i]=\min_{j<i} dp[j]+(x_i-x_j)^2+w\). Identify lines.
2. Same with \(x\) not sorted. Which structure?
3. \(dp[i]=\max_j dp[j]+a_j\cdot i+b_j\). Min or max hull?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: DP = min of linear functions of previous states.
- Key invariant: lower envelope of lines.
- Key formula: \(dp[i]=\min_j(m_j x_i+c_j)+f(i)\).
- Complexity: \(O(n)\) monotone / \(O(n\log n)\) general.
- Template to remember: deque add by slope; query by \(x\); `__int128` intersect.

**Simpler DP passes when:** \(n\le 5000\) for \(O(n^2)\) line evaluation; implement naive first under time.

---

## 4. Li Chao Tree

---
