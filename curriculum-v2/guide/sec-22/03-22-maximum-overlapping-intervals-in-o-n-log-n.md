# Maximum Overlapping Intervals in $O(N \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–1800
- Prerequisites: Event sorting, Prefix sums, Two pointers
- Tradeoff: Solves peak concurrency / maximum overlapping intervals in $\mathcal{O}(N \log N)$ time and $\mathcal{O}(N)$ memory.

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

To find the maximum number of intervals overlapping at any single point in time: convert each interval $[L_i, R_i]$ into two discrete events: an arrival event at $L_i$ with $+1$ and a departure event at $R_i$ with $-1$. Sort all $2N$ events chronologically. Sweep through the sorted events while maintaining a running prefix sum of active intervals. The maximum value attained by the prefix sum during the sweep is the maximum overlap!

---

## 4. Proof Sketches & Recurrences

The active interval count at point $x$ is $C(x) = \sum_{i=1}^N [L_i \le x \le R_i]$. Since $C(x)$ is piecewise constant, changes occur only at interval boundaries $L_i$ and $R_i$. Summing $+1$ at $L_i$ and $-1$ immediately after $R_i$ tracks $C(x)$ exactly as a continuous 1D prefix sum. Sorting $2N$ events takes $\mathcal{O}(N \log N)$ time, and the linear sweep takes $\mathcal{O}(N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Maximum Overlapping Interval Sweep
#include <bits/stdc++.h>
using namespace std;

struct Event {
    long long time;
    int type; // 0 = Start (+1), 1 = End (-1)
    
    bool operator<(const Event& other) const {
        if (time != other.time) return time < other.time;
        return type < other.type; // Starts before Ends if times match
    }
};

int max_overlapping_intervals(const vector<pair<long long, long long>>& intervals) {
    vector<Event> events;
    for (const auto& iv : intervals) {
        events.push_back({iv.first, 0});       // Start at L
        events.push_back({iv.second + 1, 1});   // End at R + 1
    }
    sort(events.begin(), events.end());

    int current_active = 0, max_active = 0;
    for (const auto& ev : events) {
        if (ev.type == 0) {
            current_active++;
            max_active = max(max_active, current_active);
        } else {
            current_active--;
        }
    }
    return max_active;
}
```

### Python 3 Template

```python
# Python 3 — Interval Overlap Counting
def max_overlapping_intervals(intervals):
    events = []
    for L, R in intervals:
        events.append((L, 0))      # Start: time L, priority 0
        events.append((R + 1, 1))  # End: time R+1, priority 1
    events.sort()

    curr_active = 0
    max_active = 0
    for time, ev_type in events:
        if ev_type == 0:
            curr_active += 1
            if curr_active > max_active:
                max_active = curr_active
        else:
            curr_active -= 1
    return max_active
```

---

## 6. Recognition Trigger Signals & Heuristics

- Maximum number of concurrent meetings or rooms required (Meeting Rooms II).
- Peak bandwidth, power, or resource utilization over time.
- Interval scheduling where overlapping segments share a single resource.
- Finding the timestamp with the highest simultaneous user count.

---

## 7. Contest WA / TLE / RE Traps

- Boundary tie-breaking: if an interval ends at time $T$ and another begins at time $T$, does it count as overlap? For inclusive intervals $[L, R]$, arrivals $+1$ must be sorted before departures $-1$. For half-open intervals $[L, R)$, departures $-1$ must be sorted before arrivals $+1$.
- Sorting on coordinate without specifying secondary tie-breaker comparison.
- Overflowing 32-bit `int` when interval timestamps are $10^{18}$.
- Assuming intervals are given sorted in input.

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
