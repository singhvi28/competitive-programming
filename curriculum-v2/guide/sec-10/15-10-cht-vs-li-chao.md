# CHT vs Li Chao

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Convex Hull Trick (CHT), Li Chao Segment Tree, Line Geometry
- Tradeoff: CHT is $\mathcal{O}(N)$ or $\mathcal{O}(N \log N)$ but requires monotonic slopes/queries or dynamic pointers (LineContainer); Li Chao Tree handles arbitrary slope/query insertions in $\mathcal{O}(\log C)$ with minimal bug surface.

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

When optimizing transitions of the form $dp[i] = \min_j (dp[j] + m_j \cdot x_i + c_j)$: 1) Use **Monotonic CHT (Deque)** if slopes $m_j$ are added in sorted order and query points $x_i$ are sorted: runs in pure $\mathcal{O}(N)$ time with 15 lines of code. 2) Use **LineContainer (Dynamic CHT)** if slopes or queries arrive in arbitrary order and coordinates are continuous reals/large integers: maintains upper/lower hull via `std::set` in $\mathcal{O}(\log N)$ per operation. 3) Use **Li Chao Segment Tree** if queries are over a fixed coordinate domain $[X_{\min}, X_{\max}]$ (e.g., $[1, 10^6]$ or via coordinate compression) or when line segments (restricted intervals $[l_j, r_j]$) are inserted: stores dominant lines in segment tree nodes with trivial maintenance.

---

## 4. Proof Sketches & Recurrences

In dynamic CHT, lines form the lower envelope of a family of affine functions. Adjacent lines intersect at $x = (c_1 - c_2) / (m_2 - m_1)$. In a Li Chao Tree over interval $[L, R]$ with midpoint $M$, inserting a new line $L_{new}$ into a node holding line $L_{cur}$ compares values at $M$: the winning line remains at the node, and the losing line can only possibly dominate in the half where it was better at the boundary. Hence, recursion descends into only one child, running in $\mathcal{O}(\log(R - L))$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- DP equation contains a cross term of the form $a_j \cdot b_i$.
- Slopes and query points both monotonic: implement $\mathcal{O}(N)$ Monotone CHT with `std::deque`.
- Slopes or queries are not monotonic: reach for Li Chao tree or LineContainer.
- Lines are only valid on a restricted segment $[L_j, R_j]$: Li Chao segment tree handles segment updates in $\mathcal{O}(\log^2 C)$ naturally.

---

## 7. Contest WA / TLE / RE Traps

- Integer overflow in cross product or intersection point calculation $(c_1 - c_2) / (m_2 - m_1)$; use `__int128`.
- Division truncation in integer arithmetic: standard integer `/` rounds toward zero; floor division requires `x / y - ((x ^ y) < 0 && x % y)`.
- Querying outside the predefined $[L, R]$ coordinate range in Li Chao tree without dynamic pointer node allocation.
- Mixing up Min vs Max envelope logic when flipping sign of slopes.

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
