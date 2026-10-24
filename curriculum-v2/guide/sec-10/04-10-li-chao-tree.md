# Li Chao Tree

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Segment tree intuition, CHT, coordinate compression on \(x\)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Segment tree intuition, CHT, coordinate compression on \(x\)

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

CHT without monotone order: store lines in a **segment tree over the \(x\)-domain**. Each node holds one line that is best on a portion of that segment; when inserting a new line, compare with the stored line at mid, keep the better one at mid, and recurse into the side where the new line might win. Queries traverse root→leaf evaluating \(O(\log)\) candidate lines.

---

## 4. Proof Sketches & Recurrences

Node covers \(x\in[L,R]\); stores line \(cur\). Insert line \(nw\):
1. Let \(mid=(L+R)/2\).
2. If \(nw\) better than \(cur\) at \(mid\), swap \(nw\leftrightarrow cur\).
3. If \(L=R\) stop.
4. If \(nw\) better than \(cur\) on the left end, recurse left; else recurse right  
   (because lines cross at most once: the winner on one side is determined).

Query \(x\): walk to leaf, take min of `eval` of all lines on the path.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: compress \(x\) / set domain size \(X\)
- Per-query / per-operation: \(O(\log X)\) insert and query (dynamic nodes \(O(\log X)\) memory each insert)
- Total: \(O(n\log X)\)
- Memory: \(O(n\log X)\) worst case with dynamic nodes`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Need \(\min_j m_j x+c_j\) but inserts/queries in arbitrary order.
- \(x\) coordinates are in a known range or compressible to \(1..n\).
- “Dynamic CHT” / “add line, query point” online.
- Segments of lines (line only valid on \([L,R]\)) → Li Chao on that range (segment add).

---

## 7. Contest WA / TLE / RE Traps

- Domain not covering all query \(x\) (compress consistently).
- Overflow in `m*x+b` — use careful types / `__int128` if needed.
- Min vs max: flip comparisons.
- Recursing into wrong child after swap.
- Using floating domain without discretization when \(x\) huge but sparse.

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

- **Segment add**: insert line only on \([ql,qr]\) — standard segtree split + Li Chao node.
- **Max Li Chao**.
- **Persistent Li Chao** for rollback / versions.
- Prefer **deque CHT** when monotone — much faster constants.

---

## 11. Typical Problem Archetypes

1. Standard: online add line + query min at \(x\).
2. Slightly disguised: DP where \(j\) processed out of slope order.
3. Difficult: lines valid on intervals; segment Li Chao.
4. Very difficult: Li Chao + another DS dimension; persistent.

---

## 12. Recognition & Identification Drills

1. Process updates “add line” and queries “min at x” interleaved arbitrarily.
2. Same as CHT classic but \(h_i\) not sorted.
3. Line added only for \(x\in[L,R]\). Structure?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: CHT without monotone slope/query order.
- Key invariant: lines cross ≤ once; keep better line at mid.
- Key formula: point query over envelope via segtree path.
- Complexity: \(O(\log X)\) per op.
- Template to remember: compare at mid; swap; recurse one side.

**Simpler DP passes when:** few lines — brute all lines per query; or offline sort to reduce to deque CHT.

---

→ Continue: [`10-b-monotone-queue-stack-dp-bitset-sos.md`](10-b-monotone-queue-stack-dp-bitset-sos.md) (monotone queue/stack, bitset, SOS).

---
