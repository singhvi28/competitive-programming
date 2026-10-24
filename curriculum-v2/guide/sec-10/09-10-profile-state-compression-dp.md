# Profile / state-compression DP

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Bitmask DP, grid / tiling intuition, DFS/BFS on transitions between masks  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Bitmask DP, grid / tiling intuition, DFS/BFS on transitions between masks

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

When one dimension is tiny (width \(w\le 10\)–\(20\)), process the grid **column by column** (or row by row). The “profile” is a bitmask of which cells in the current column are already filled / need matching from a previous half-tile / store connectivity state. Transitions enumerate ways to place tiles that are consistent with the incoming profile and produce an outgoing profile for the next column. Complexity \(\sim O(\text{cols}\cdot 2^w\cdot \text{trans})\); precompute transitions if the plug DP graph is static.

---

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(2^h\cdot \mathrm{poly}(h))\) transition build (often \(O(3^{h/2})\)–style via DFS)
- Per-query / per-operation: N/A
- Total: \(O(w\cdot 2^h\cdot \mathrm{avg\_deg})\)
- Memory: \(O(2^h\cdot \mathrm{avg\_deg})\) for transitions + \(O(2^h)\) DP`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Grid \(n\times m\) with \(n\cdot m\le 100\) but one side \(\le 10\)–\(12\).
- Tiling with dominoes / trominoes / “fill without holes”.
- Hamiltonian paths on narrow grids; colorings with local constraints.
- Broken profile: state includes “connected components touching the frontier” (more bits / DSU hash — harder).
- Statement screams \(2^{w}\) DP after you rotate the grid so \(w=\min(n,m)\).

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to rotate grid so height is the small side.
- Allowing holes (skipping a cell without placing a tile).
- Final mask must be \(0\) (no pending verticals).
- Double-counting tiles; inconsistent meaning of bits.
- Connectivity profile: hashing DSU wrongly → WA.
- Overflow without mod.

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

- Tromino / larger polyominoes.
- Broken profile connectivity (plug DP / Chinese “contour DP”).
- Colorings, independent sets on grids (transfer matrix = same idea).
- Profile + digit constraints.

---

## 11. Typical Problem Archetypes

1. Standard: count domino tilings of \(n\times m\).
2. Slightly disguised: place kings/bishops with mask of previous column attacks.
3. Difficult: connectivity of empty cells / “all floors connected”.
4. Very difficult: plug DP for Hamiltonian cycles on grids.

---

## 12. Recognition & Identification Drills

1. \(3\times n\) tiling with dominoes — state space?
2. \(n\times m\) grid, \(n\le 8\), count independent sets.
3. Fill grid with “+” shapes — profile or dancing links?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: narrow grid + local tile/constraint transfer.
- Key invariant: profile mask = frontier occupation/connectivity.
- Key formula: \(dp[c+1][nxt]=\sum_{cur\to nxt}dp[c][cur]\).
- Complexity: \(O(w\cdot 2^h\cdot \deg)\).
- Template to remember: DFS generate transitions; DP over columns.

**Simpler DP passes when:** total cells \(\le 20\) — plain subset / backtrack; or closed formulas for tiny heights.

---

## 10. Alien trick / Lagrangian relaxation

---
