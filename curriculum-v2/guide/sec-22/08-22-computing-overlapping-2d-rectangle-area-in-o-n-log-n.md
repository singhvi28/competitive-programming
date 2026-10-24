# Computing Overlapping 2D Rectangle Area in $O(N \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

Given $N$ axis-aligned rectangles $[x_1, x_2] \times [y_1, y_2]$:
1. Deconstruct each rectangle into:
   - **Start Event at $x_1$:** Add interval $[y_1, y_2]$ to the active $Y$-set ($+1$).
   - **End Event at $x_2$:** Remove interval $[y_1, y_2]$ from the active $Y$-set ($-1$).
2. Sort all $2N$ events by their $X$-coordinate.
3. Between consecutive events $X_i$ and $X_{i+1}$, the active set of $Y$-intervals remains **constant**.
4. The area of the vertical strip between $X_i$ and $X_{i+1}$ is:
   $$\text{Strip Area} = (X_{i+1} - X_i) \times \text{Total Active } Y \text{ Length}$$
5. Summing across all strips gives the exact total union area.

```
          Y ^
            |          +-------+
            |          |       |
            |     +----+---+   |  <--- Total Active Y-Length (Root.len)
            |     |    |   |   |
            |     +----+---+---+
            |          |       |
            +----------+-------+--------------------> X
                      X_i     X_{i+1}
                      <--dx-->
               Strip Area = dx * Root.len
```

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

1. Compress unique $Y$-coordinates into $y_0 < y_1 < \dots < y_{K-1}$.
2. The leaves of the Segment Tree represent the elementary segments $[y_j, y_{j+1}]$ with physical length $y_{j+1} - y_j$.
3. Each node maintains:
   - `cover`: Integer count of active rectangles covering this node's interval.
   - `len`: Total physical $Y$-length covered within this node.
4. **Update Logic:**
   - If `cover > 0`, `len` = total physical span of this node.
   - If `cover == 0`, `len` = `left_child.len + right_child.len` (or 0 for leaves).

```cpp
// C++17 — Klee's Measure Problem (Rectangle Union Area)
#include <bits/stdc++.h>
using namespace std;

struct Event {
    long long x, y1, y2;
    int type; // +1 = Add, -1 = Remove
    bool operator<(const Event& o) const { return x < o.x; }
};

struct KleeSegTree {
    int n;
    vector<long long> y_coords;
    vector<int> cover;
    vector<long long> len;

    KleeSegTree(const vector<long long>& y_coords) : y_coords(y_coords) {
        n = y_coords.size() - 1;
        cover.assign(4 * n, 0);
        len.assign(4 * n, 0);
    }

    void update(int v, int tl, int tr, int l, int r, int val) {
        if (l > r) return;
        if (l == tl && r == tr) {
            cover[v] += val;
        } else {
            int tm = (tl + tr) / 2;
            update(v * 2, tl, tm, l, min(r, tm), val);
            update(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r, val);
        }
        if (cover[v] > 0) {
            len[v] = y_coords[tr + 1] - y_coords[tl];
        } else {
            len[v] = (tl == tr) ? 0 : (len[v * 2] + len[v * 2 + 1]);
        }
    }
};

long long calculate_rectangle_area(vector<array<long long, 4>>& rects) {
    // rect = {x1, y1, x2, y2}
    vector<long long> y_vals;
    vector<Event> events;
    for (const auto& r : rects) {
        y_vals.push_back(r[1]);
        y_vals.push_back(r[3]);
        events.push_back({r[0], r[1], r[3], +1});
        events.push_back({r[2], r[1], r[3], -1});
    }
    sort(y_vals.begin(), y_vals.end());
    y_vals.erase(unique(y_vals.begin(), y_vals.end()), y_vals.end());
    sort(events.begin(), events.end());

    auto get_y = [&](long long y) {
        return lower_bound(y_vals.begin(), y_vals.end(), y) - y_vals.begin();
    };

    KleeSegTree st(y_vals);
    long long total_area = 0;
    long long last_x = events[0].x;

    for (const auto& ev : events) {
        total_area += st.len[1] * (ev.x - last_x);
        last_x = ev.x;
        int y1_idx = get_y(ev.y1);
        int y2_idx = get_y(ev.y2) - 1; // Leaf intervals [y_idx, y_idx+1]
        st.update(1, 0, st.n - 1, y1_idx, y2_idx, ev.type);
    }
    return total_area;
}
```

---

## 3. Nearest-Duplicate & Historical Offline Sweeps

---

## 4. Proof Sketches & Recurrences

In the Segment tree over compressed $Y$-coordinates, each node maintains: `cnt` (how many active rectangles fully cover this node's $Y$-interval) and `len` (the total length of covered space in this subtree). If `cnt > 0`, the entire node interval is covered: `len = Y[r+1] - Y[l]`. If `cnt == 0`, its covered length is the sum of its children: `len = is_leaf ? 0 : (lchild.len + rchild.len)`. Notice this requires **NO lazy propagation** tags, because updates are strictly paired additions and subtractions!

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Klee's Measure Problem (Rectangle Union Area)
#include <bits/stdc++.h>
using namespace std;

struct Event {
    long long x, y1, y2;
    int type; // +1 = Add, -1 = Remove
    bool operator<(const Event& o) const { return x < o.x; }
};

struct KleeSegTree {
    int n;
    vector<long long> y_coords;
    vector<int> cover;
    vector<long long> len;

    KleeSegTree(const vector<long long>& y_coords) : y_coords(y_coords) {
        n = y_coords.size() - 1;
        cover.assign(4 * n, 0);
        len.assign(4 * n, 0);
    }

    void update(int v, int tl, int tr, int l, int r, int val) {
        if (l > r) return;
        if (l == tl && r == tr) {
            cover[v] += val;
        } else {
            int tm = (tl + tr) / 2;
            update(v * 2, tl, tm, l, min(r, tm), val);
            update(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r, val);
        }
        if (cover[v] > 0) {
            len[v] = y_coords[tr + 1] - y_coords[tl];
        } else {
            len[v] = (tl == tr) ? 0 : (len[v * 2] + len[v * 2 + 1]);
        }
    }
};

long long calculate_rectangle_area(vector<array<long long, 4>>& rects) {
    // rect = {x1, y1, x2, y2}
    vector<long long> y_vals;
    vector<Event> events;
    for (const auto& r : rects) {
        y_vals.push_back(r[1]);
        y_vals.push_back(r[3]);
        events.push_back({r[0], r[1], r[3], +1});
        events.push_back({r[2], r[1], r[3], -1});
    }
    sort(y_vals.begin(), y_vals.end());
    y_vals.erase(unique(y_vals.begin(), y_vals.end()), y_vals.end());
    sort(events.begin(), events.end());

    auto get_y = [&](long long y) {
        return lower_bound(y_vals.begin(), y_vals.end(), y) - y_vals.begin();
    };

    KleeSegTree st(y_vals);
    long long total_area = 0;
    long long last_x = events[0].x;

    for (const auto& ev : events) {
        total_area += st.len[1] * (ev.x - last_x);
        last_x = ev.x;
        int y1_idx = get_y(ev.y1);
        int y2_idx = get_y(ev.y2) - 1; // Leaf intervals [y_idx, y_idx+1]
        st.update(1, 0, st.n - 1, y1_idx, y2_idx, ev.type);
    }
    return total_area;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Compute the total area covered by at least one rectangle among $N \le 10^5$ rectangles.
- Perimeter of union of rectangles (maintains number of disjoint segments in node).
- Volume of union of 3D boxes (Sweep line on $Z$ with 2D rectangle union sweep inside).
- Coverage counting where coverage increments and decrements are symmetrical.

---

## 7. Contest WA / TLE / RE Traps

- Compressing points instead of intervals: $Y$-coordinates represent interval spans $[Y_i, Y_{i+1}]$; a tree with $M$ unique coordinates has $M - 1$ elementary intervals.
- Using lazy propagation unnecessarily: `cnt` and `len` pull logic does not need lazy pushdown because every $+1$ has a matching $-1$.
- Integer overflow in area accumulation: area can reach $10^{18}$; always multiply `(events[i+1].x - events[i].x) * seg.len[1]` using 64-bit `long long`.
- Sorting events with inconsistent addition/deletion order on identical $X$.

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
