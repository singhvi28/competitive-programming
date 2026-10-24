# Multi-Pass / 3-Element Inversions (e.g., Codeforces 61E)

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div2 Hard / Div1 Medium
- Typical CF/ICPC rating range: 1600–2100
- Prerequisites: Fenwick Tree, Coordinate Compression, Combinatorics / Product rule
- Tradeoff: Extends standard 2-element inversion counting to 3-element and $K$-element patterns in $\mathcal{O}(K \cdot N \log N)$.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

## 3. Core Intuition & Problem Framing

A standard inversion is a pair $(i, j)$ with $i < j$ and $a_i > a_j$. A 3-element inversion (e.g., Codeforces 61E 'Enemy is weak') is a triplet $(i, j, k)$ with $i < j < k$ and $a_i > a_j > a_k$. Counting all triplets naively takes $\mathcal{O}(N^3)$. The crucial insight is to **pivot around the middle element $j$**: for each fixed $j$, the number of valid triplets is simply: $(\text{number of } i < j \text{ with } a_i > a_j) \times (\text{number of } k > j \text{ with } a_k < a_j)$! Two simple independent passes of a Fenwick tree (left-to-right and right-to-left) compute these counts for all $j$ in $\mathcal{O}(N \log N)$!

---

## 4. Proof Sketches & Recurrences

Let $L[j] = |\{i < j : a_i > a_j\}|$ and $R[j] = |\{k > j : a_k < a_j\}|$. By the multiplication principle of independent choices, the total number of 3-inversions is $\sum_{j=1}^N L[j] \cdot R[j]$. $L[j]$ is computed by sweeping left-to-right: when at $j$, query how many elements in the BIT have value $> a_j$, then insert $a_j$. $R[j]$ is computed by sweeping right-to-left: when at $j$, query how many elements in the BIT have value $< a_j$, then insert $a_j$. Total runtime is $2 \times \mathcal{O}(N \log N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — 2D Offline Range Rectangle Point Counter
#include <bits/stdc++.h>
using namespace std;

struct FenwickTree {
    int n;
    vector<int> tree;
    FenwickTree(int n) : n(n), tree(n + 1, 0) {}
    
    void add(int i, int delta) {
        for (++i; i <= n; i += i & -i) tree[i] += delta;
    }
    
    int query(int i) { // prefix sum [0, i]
        int sum = 0;
        for (++i; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
    
    int query(int l, int r) {
        if (l > r) return 0;
        return query(r) - (l == 0 ? 0 : query(l - 1));
    }
};

struct Event {
    int x, type; // 0 = Query Left (x1-1), 1 = Point Insert (x), 2 = Query Right (x2)
    int y1, y2, id, sign;
    
    bool operator<(const Event& o) const {
        if (x != o.x) return x < o.x;
        return type < o.type; // Left Queries -> Points -> Right Queries
    }
};

vector<int> count_points_in_rectangles(vector<pair<int, int>>& points, 
                                      vector<array<int, 4>>& queries) {
    // queries[i] = {x1, x2, y1, y2}
    vector<int> all_y;
    for (const auto& p : points) all_y.push_back(p.second);
    for (const auto& q : queries) {
        all_y.push_back(q[2]);
        all_y.push_back(q[3]);
    }
    sort(all_y.begin(), all_y.end());
    all_y.erase(unique(all_y.begin(), all_y.end()), all_y.end());
    
    auto get_y_rank = [&](int y) {
        return lower_bound(all_y.begin(), all_y.end(), y) - all_y.begin();
    };

    vector<Event> events;
    for (const auto& p : points) {
        events.push_back({p.first, 1, get_y_rank(p.second), 0, -1, 0});
    }
    for (int i = 0; i < (int)queries.size(); ++i) {
        int x1 = queries[i][0], x2 = queries[i][1];
        int y1_r = get_y_rank(queries[i][2]), y2_r = get_y_rank(queries[i][3]);
        events.push_back({x1 - 1, 0, y1_r, y2_r, i, -1}); // Subtract left
        events.push_back({x2, 2, y1_r, y2_r, i, +1});     // Add right
    }
    sort(events.begin(), events.end());

    FenwickTree bit(all_y.size());
    vector<int> ans(queries.size(), 0);

    for (const auto& ev : events) {
        if (ev.type == 1) { // Point Insert
            bit.add(ev.y1, 1);
        } else { // Query Event
            int cnt = bit.query(ev.y1, ev.y2);
            ans[ev.id] += ev.sign * cnt;
        }
    }
    return ans;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count triplets $(i, j, k)$ satisfying monotonic index and value inequalities ($i < j < k$ and $a_i > a_j > a_k$).
- General pattern counting of length 3 (e.g. peak triplets $a_i < a_j > a_k$ or valley triplets).
- DP on sequences of fixed small length $K$ where transitions are dominated by rank order.
- Problems where fixing the 'center' or 'pivot' element decouples the remaining choices.

---

## 7. Contest WA / TLE / RE Traps

- Integer overflow: total count of triplets can reach $\binom{N}{3} \approx \frac{(10^6)^3}{6} \approx 1.6 \times 10^{17}$, overflowing 32-bit `int`; always accumulate into `long long`.
- Reusing the Fenwick tree without clearing it between the two passes.
- Querying `bit.query(r)` instead of `bit.query(r - 1)` for strict inequality $< a_j$.
- Forgetting that duplicate array values require strict inequality specification in problem statements.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

## 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---
