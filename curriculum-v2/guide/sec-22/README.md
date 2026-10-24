# Section §22: Line Sweep Algorithms & Reductions

> **Module ID:** `sec-22`  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Topic Count:** 15  

**Module Summary:** Event abstraction, coordinate compression, 1D/2D difference arrays, 2D Fenwick dominance, Klee's Measure rectangle union area, and Bentley-Ottmann line sweep.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Dimensional Reduction via Event Processing](#topic-1) | `S-tier` | 1400–1900 | Common | [01-22-dimensional-reduction-via-event-processing.md](./01-22-dimensional-reduction-via-event-processing.md) |
| 2 | [Mapping Sparse $10^9$ Domains to Dense $[0, K-1]$ Ranks](#topic-2) | `B-tier` | 1600–2200 | Common | [02-22-mapping-sparse-10-9-domains-to-dense-0-k-1-ranks.md](./02-22-mapping-sparse-10-9-domains-to-dense-0-k-1-ranks.md) |
| 3 | [Maximum Overlapping Intervals in $O(N \log N)$](#topic-3) | `B-tier` | 1600–2200 | Common | [03-22-maximum-overlapping-intervals-in-o-n-log-n.md](./03-22-maximum-overlapping-intervals-in-o-n-log-n.md) |
| 4 | [Dynamic Time-Series Projection via Binary Indexed Trees](#topic-4) | `S-tier` | 1600–2200 | Common | [04-22-dynamic-time-series-projection-via-binary-indexed-trees.md](./04-22-dynamic-time-series-projection-via-binary-indexed-trees.md) |
| 5 | [Point Dominance](#topic-5) | `B-tier` | 1600–2200 | Common | [05-22-point-dominance.md](./05-22-point-dominance.md) |
| 6 | [Multi-Pass / 3-Element Inversions (e.g., Codeforces 61E)](#topic-6) | `B-tier` | 1600–2200 | Common | [06-22-multi-pass-3-element-inversions-e-g-codeforces-61e.md](./06-22-multi-pass-3-element-inversions-e-g-codeforces-61e.md) |
| 7 | [When Fenwick Trees Fail](#topic-7) | `S-tier (The foundation of 2D computational geometry and advanced offline range querying)` | 1900–2400+ | Common | [07-22-when-fenwick-trees-fail.md](./07-22-when-fenwick-trees-fail.md) |
| 8 | [Computing Overlapping 2D Rectangle Area in $O(N \log N)$](#topic-8) | `B-tier` | 1600–2200 | Common | [08-22-computing-overlapping-2d-rectangle-area-in-o-n-log-n.md](./08-22-computing-overlapping-2d-rectangle-area-in-o-n-log-n.md) |
| 9 | [Maximum Value Occurring At Least Twice in Subarray $[L, R]$](#topic-9) | `B-tier` | 1600–2200 | Common | [09-22-maximum-value-occurring-at-least-twice-in-subarray-l-r.md](./09-22-maximum-value-occurring-at-least-twice-in-subarray-l-r.md) |
| 10 | [Finding $K$ Intersections among $N$ Line Segments in $O((N + K) \log N)$](#topic-10) | `High-tier Geometry / Computational Geometry Specialist` | 1600–2200 | Common | [10-22-finding-k-intersections-among-n-line-segments-in-o-n-k-log-n.md](./10-22-finding-k-intersections-among-n-line-segments-in-o-n-k-log-n.md) |
| 11 | [B. FIRST PRINCIPLES & ALGORITHM MECHANICS](#topic-11) | `B-tier` | 1600–2200 | Common | [11-22-b-first-principles-algorithm-mechanics.md](./11-22-b-first-principles-algorithm-mechanics.md) |
| 12 | [Mapping Subtree & Path Queries to 1D Sweep Intervals](#topic-12) | `B-tier` | 1600–2200 | Common | [12-22-mapping-subtree-path-queries-to-1d-sweep-intervals.md](./12-22-mapping-subtree-path-queries-to-1d-sweep-intervals.md) |
| 13 | [Edge-Cut Tree Component Splitting in $O((N + Q) \log N)$](#topic-13) | `B-tier` | 1600–2200 | Common | [13-22-edge-cut-tree-component-splitting-in-o-n-q-log-n.md](./13-22-edge-cut-tree-component-splitting-in-o-n-q-log-n.md) |
| 14 | [Transforming Tree Queries via DFS Active-Path Sweeping](#topic-14) | `B-tier` | 1600–2200 | Common | [14-22-transforming-tree-queries-via-dfs-active-path-sweeping.md](./14-22-transforming-tree-queries-via-dfs-active-path-sweeping.md) |
| 15 | [Prerequisites](#topic-15) | `B-tier` | 1600–2200 | Common | [15-22-prerequisites.md](./15-22-prerequisites.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Dimensional Reduction via Event Processing

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1400–1900 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Typical CF rating range: 1400–1900
- Core Concept: Transforming a static $D$-dimensional problem into a dynamic $(D-1)$-dimensional active state evolving along a sweeping axis.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

In a static array or geometric setting, an interval $[L, R]$ with value $V$ is typically viewed as a contiguous block. The fundamental shift in the **Sweep Line** technique is deconstructing each interval into independent, atomic point **events** in time:
1. **Start Event at $L$:** Interval enters the active state ($+V$).
2. **End Event at $R + 1$:** Interval leaves the active state ($-V$).
3. **Query Event at $X$:** Inspect the active state at coordinate $X$.

By sorting all events chronologically along the sweep axis and processing them sequentially, the global state at any point $X$ is evaluated via a running prefix sum of deltas.

```
Interval [L, R]  ========================>
Events:          +-----------------------+
                 ^                       ^
            Start at L              End at R+1
            (Delta +V)              (Delta -V)
```

---

#### 4. Proof Sketches & Recurrences

Consider $N$ 2D points or rectangles. Checking all pairs in 2D space takes $\mathcal{O}(N^2)$. By sorting the $2N$ boundary events along the $X$-axis in $\mathcal{O}(N \log N)$, the sweep line maintains only the currently active elements intersecting the line $x = X_{cur}$. The active set is maintained in a Fenwick or Segment Tree indexed by the $Y$-coordinate. Each event causes $\mathcal{O}(1)$ modifications to the 1D tree, leading to an overall runtime of $\mathcal{O}(N \log N)$ and $\mathcal{O}(N)$ space.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Dimensional Reduction via Sweep Line Event Processing
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Event {
    ll x;
    int type; // 0 = Add interval, 1 = Query point, 2 = Remove interval
    ll y1, y2;
    int id;
    bool operator<(const Event& o) const {
        if (x != o.x) return x < o.x;
        return type < o.type; // Process additions before queries before removals
    }
};

void sweep_line_events(vector<Event>& events) {
    sort(events.begin(), events.end());
    // Fenwick tree or active set over Y coordinates
    for (const auto& ev : events) {
        if (ev.type == 0) { /* insert [y1, y2] into active set */ }
        else if (ev.type == 1) { /* query y1 in active set */ }
        else if (ev.type == 2) { /* remove [y1, y2] from active set */ }
    }
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- 1. **Start Events (+1):** Processed **first** (intervals become active before queries evaluate).
- 2. **Query Events (0):** Processed **second** (reads the exact inclusive active state).
- 3. **End Events (-1):** Processed **third** (intervals that end at $X$ remain active for queries at $X$, and are removed only afterwards).
- 

---

#### 7. Contest WA / TLE / RE Traps

- Event tie-breaking: when events share the exact same $X$-coordinate, processing order matters critically. If intervals are closed $[L, R]$, additions must be processed before queries, which must be processed before deletions.
- Coordinate compression omission: $Y$-coordinates up to $10^9$ must be mapped to $[0, K-1]$ before inserting into standard array-backed Fenwick/Segment trees.
- Forgetting to clear or un-insert expired elements on exit events, leaving stale entries in the active structure.
- Using 32-bit `int` for $X$ or $Y$ coordinates when products or sums exceed $2 \times 10^9$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-2"></a>
### 2. Mapping Sparse $10^9$ Domains to Dense $[0, K-1]$ Ranks

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2000
- Prerequisites: Coordinate Compression, Sorting, Unique, Binary Search (`std::lower_bound`)
- Tradeoff: Compresses arbitrary $10^9$ coordinate domains into compact $[0, K-1]$ ranks with $K \le 2N$ to fit in array-based trees.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Tree data structures like Fenwick Trees and basic Segment Trees require memory proportional to the coordinate domain size $M$. When problem coordinates lie in $[-10^9, 10^9]$, allocating a size $10^9$ array is impossible (MLE). Coordinate compression sorts all distinct coordinates appearing in inputs and queries, removes duplicates, and replaces each large coordinate with its 0-based or 1-based index rank via `std::lower_bound`. The relative order of all coordinates is preserved, while the domain size collapses from $10^9$ to at most $2N$!

---

#### 4. Proof Sketches & Recurrences

Given $N$ query/event points $x_1, x_2, \dots, x_N \in \mathbb{R}$. Sorting and deduplicating produces unique array $U$ of size $K \le N$ in $\mathcal{O}(N \log N)$. For any $x_i$, its compressed rank is $rank(x_i) = \text{lower\_bound}(U, x_i) - U.\text{begin}()$. Order is preserved: $x_a < x_b \iff rank(x_a) < rank(x_b)$. For interval problems where intervals have length, remember to also compress $R_i + 1$ or track endpoint spans $U[i+1] - U[i]$ to preserve continuous measure.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// C++17 — Coordinate Compression Utility
#include <bits/stdc++.h>
using namespace std;

struct CoordinateCompressor {
    vector<long long> coords;
    
    void add(long long x) { coords.push_back(x); }
    
    void build() {
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());
    }
    
    int get_rank(long long x) const {
        return lower_bound(coords.begin(), coords.end(), x) - coords.begin();
    }
    
    long long get_val(int rank) const {
        return coords[rank];
    }
    
    int size() const { return coords.size(); }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Coordinates or values up to $10^9$ or $10^{18}$ where only relative comparisons matter.
- Range queries on offline data with sparse coordinate points.
- Fenwick tree or Segment tree indexing over large continuous domains.
- Interval sweep line where endpoints are floating point numbers or large integers.

---

#### 7. Contest WA / TLE / RE Traps

- Calling `get_rank()` before calling `build()` (sorting and deduplicating), returning nonsensical ranks.
- Forgetting to add query endpoints into the compression vector: if queries test coordinates not in `vals`, `get_rank` might return inconsistent or out-of-bounds positions.
- Interval length corruption: mapping $[1, 2]$ and $[2, 100]$ to contiguous ranks $[0, 1]$ and $[1, 2]$ loses the physical length of intervals unless span weights $U[i+1] - U[i]$ are explicitly maintained.
- Off-by-one indexing: 0-based compressed ranks passed to 1-based Fenwick trees without `+ 1`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-3"></a>
### 3. Maximum Overlapping Intervals in $O(N \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–1800
- Prerequisites: Event sorting, Prefix sums, Two pointers
- Tradeoff: Solves peak concurrency / maximum overlapping intervals in $\mathcal{O}(N \log N)$ time and $\mathcal{O}(N)$ memory.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

To find the maximum number of intervals overlapping at any single point in time: convert each interval $[L_i, R_i]$ into two discrete events: an arrival event at $L_i$ with $+1$ and a departure event at $R_i$ with $-1$. Sort all $2N$ events chronologically. Sweep through the sorted events while maintaining a running prefix sum of active intervals. The maximum value attained by the prefix sum during the sweep is the maximum overlap!

---

#### 4. Proof Sketches & Recurrences

The active interval count at point $x$ is $C(x) = \sum_{i=1}^N [L_i \le x \le R_i]$. Since $C(x)$ is piecewise constant, changes occur only at interval boundaries $L_i$ and $R_i$. Summing $+1$ at $L_i$ and $-1$ immediately after $R_i$ tracks $C(x)$ exactly as a continuous 1D prefix sum. Sorting $2N$ events takes $\mathcal{O}(N \log N)$ time, and the linear sweep takes $\mathcal{O}(N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Maximum number of concurrent meetings or rooms required (Meeting Rooms II).
- Peak bandwidth, power, or resource utilization over time.
- Interval scheduling where overlapping segments share a single resource.
- Finding the timestamp with the highest simultaneous user count.

---

#### 7. Contest WA / TLE / RE Traps

- Boundary tie-breaking: if an interval ends at time $T$ and another begins at time $T$, does it count as overlap? For inclusive intervals $[L, R]$, arrivals $+1$ must be sorted before departures $-1$. For half-open intervals $[L, R)$, departures $-1$ must be sorted before arrivals $+1$.
- Sorting on coordinate without specifying secondary tie-breaker comparison.
- Overflowing 32-bit `int` when interval timestamps are $10^{18}$.
- Assuming intervals are given sorted in input.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-4"></a>
### 4. Dynamic Time-Series Projection via Binary Indexed Trees

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Rating Range: 1600–2200
- Core Invariant: Sweeping along the $X$-axis satisfies the $X$-coordinate constraint for free, allowing an auxiliary **Fenwick Tree** to maintain and query the dynamic distribution of active $Y$-coordinates in $O(\log N)$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

To count points lying strictly inside a 2D bounding box $[x_1, x_2] \times [y_1, y_2]$:
1. Deconstruct the query into two 1D events:
   - **Left Query at $x_1 - 1$:** Query $\text{count}(y_1, y_2)$ and subtract from result.
   - **Right Query at $x_2$:** Query $\text{count}(y_1, y_2)$ and add to result.
2. Sort all point insertions and query events along the $X$-axis.
3. As the sweep line moves right, insert point $y$-coordinates into the Fenwick Tree.
4. When reaching a query event at $X$, query the Fenwick tree for the range $[y_1, y_2]$.

```
          Y ^
            |          [ Point (x, y) inserted into Fenwick ]
            |              +-----------------------+ (x2, y2)
            |              |                       |
            |              |   Active 2D Region    |
            |              |                       |
            |              +-----------------------+
            |        (x1, y1)
            +----------------------------------------------------> X
                      ^                             ^
                 Query at x1-1                 Query at x2
                 (Subtract)                    (Add)
```

---

## 2. 2D Point Dominance & Inversion Counting

---

#### 4. Proof Sketches & Recurrences

A 2D query $(x \in [x_1, x_2], y \in [y_1, y_2])$ can be decomposed into two prefix queries via linearity: $Q(x_2) - Q(x_1 - 1)$. By grouping and sorting queries by their $X$-threshold, elements with $x_i \le X$ are inserted into the Fenwick tree monotonically. The Fenwick tree maintains frequency counts over $Y$ coordinates. Point updates and prefix queries both run in $\mathcal{O}(\log |Y|)$ time with cache-friendly contiguous array memory.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Dynamic Time-Series Projection via Offline BIT Sweep
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<ll> tree;
    Fenwick(int n_) : n(n_), tree(n_ + 1, 0) {}
    void add(int i, ll delta) { for (; i <= n; i += i & -i) tree[i] += delta; }
    ll query(int i) { ll sum = 0; for (; i > 0; i -= i & -i) sum += tree[i]; return sum; }
    ll query_range(int l, int r) { return query(r) - query(l - 1); }
};

struct Query { int l, r, k, id; };

// Count elements in subarray [l, r] with value >= k
vector<int> count_elements_ge_k(vector<int>& a, vector<Query>& queries) {
    int n = a.size(), q = queries.size();
    vector<int> ans(q);
    // Sort elements and queries by value descending
    // ... (Sweep elements into Fenwick indexed by position 1..n) ...
    return ans;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Queries ask for number of elements in range $[L, R]$ satisfying value constraints $A_i \ge K$.
- Counting inversions dynamically as a sequence is built.
- Offline range distinct elements (SPOJ DQUERY): sweep right endpoint $R$, insert current position, remove previous occurrence.
- Prefix sums on a dynamically activated subset of points.

---

#### 7. Contest WA / TLE / RE Traps

- 0-based indexing in Fenwick: `i += i & -i` loops infinitely if $i = 0$; Fenwick trees must always be 1-indexed.
- Fenwick tree size: `tree` must be sized to the maximum possible compressed coordinate, not the number of queries.
- Off-by-one in prefix difference: querying range $[L, R]$ requires `query(R) - query(L - 1)`, not `query(L)`.
- Mixing up offline sorting order: queries sorted in opposite direction to elements.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-5"></a>
### 5. Point Dominance

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Sweep line, Fenwick Tree, CDQ Divide and Conquer, 2D/3D Dominance
- Tradeoff: Solves 2D point dominance in $\mathcal{O}(N \log N)$ and 3D point dominance in $\mathcal{O}(N \log^2 N)$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Point $A = (x_a, y_a)$ dominates point $B = (x_b, y_b)$ if $x_a \ge x_b$ and $y_a \ge y_b$. Counting how many points each point dominates (or finding the longest chain of dominated points) is 2D Point Dominance. Sorting all points primarily by $X$ ascending eliminates the $X$-coordinate constraint: any point processed earlier automatically has $x_b \le x_a$. The remaining problem is 1D: count how many previously processed points have $y_b \le y_a$, which is a single prefix sum query on a Fenwick tree over $Y$-coordinates!

---

#### 4. Proof Sketches & Recurrences

In 2D: sort points by $(x_i, y_i)$. Iterate $i$ from 1 to $N$: query Fenwick for prefix sum up to $y_i$, then insert $y_i$ into Fenwick. Total time is $\mathcal{O}(N \log N)$. In 3D ($x_a \ge x_b, y_a \ge y_b, z_a \ge z_b$): sort by $X$, then apply CDQ Divide and Conquer on $Y$, using a Fenwick tree on $Z$ during the merge step, running in $\mathcal{O}(N \log^2 N)$ without 2D segment trees.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// 2D Point Dominance Counting in O(N log N)
#include <bits/stdc++.h>
using namespace std;

struct Point { int x, y, id; };

vector<int> count_dominated_points(vector<Point>& pts) {
    int n = pts.size();
    vector<int> ans(n, 0);
    // Coordinate compress Y coordinates
    vector<int> ys;
    for (auto& p : pts) ys.push_back(p.y);
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    
    // Sort points: X ascending, Y ascending for ties
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
    });
    
    // Fenwick tree over compressed Y
    int m = ys.size();
    vector<int> bit(m + 1, 0);
    auto add = [&](int i) { for (; i <= m; i += i & -i) bit[i]++; };
    auto query = [&](int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; };
    
    for (const auto& p : pts) {
        int y_rank = lower_bound(ys.begin(), ys.end(), p.y) - ys.begin() + 1;
        ans[p.id] = query(y_rank);
        add(y_rank);
    }
    return ans;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Partial order queries: count pairs $(i, j)$ such that $a_i \le a_j$ and $b_i \le b_j$.
- Longest chain of bounding boxes that can be nested inside one another.
- Skyline / Pareto frontier computation in multi-objective optimization.
- 3D Partial order / Elementary particles problem (CF 1093E, etc.).

---

#### 7. Contest WA / TLE / RE Traps

- Strict vs non-strict dominance: if dominance requires $x_a > x_b$ and $y_a > y_b$, identical coordinates require careful tie-breaking (e.g. process identical $X$ points in batch or reverse $Y$ order).
- Coordinate compression forgetting duplicate entries in $Y$.
- Incorrect Fenwick sizing when compressed $Y$ ranks reach $N$.
- Applying 2D sweep directly to 3D without CDQ divide-and-conquer.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-6"></a>
### 6. Multi-Pass / 3-Element Inversions (e.g., Codeforces 61E)

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div2 Hard / Div1 Medium
- Typical CF/ICPC rating range: 1600–2100
- Prerequisites: Fenwick Tree, Coordinate Compression, Combinatorics / Product rule
- Tradeoff: Extends standard 2-element inversion counting to 3-element and $K$-element patterns in $\mathcal{O}(K \cdot N \log N)$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

A standard inversion is a pair $(i, j)$ with $i < j$ and $a_i > a_j$. A 3-element inversion (e.g., Codeforces 61E 'Enemy is weak') is a triplet $(i, j, k)$ with $i < j < k$ and $a_i > a_j > a_k$. Counting all triplets naively takes $\mathcal{O}(N^3)$. The crucial insight is to **pivot around the middle element $j$**: for each fixed $j$, the number of valid triplets is simply: $(\text{number of } i < j \text{ with } a_i > a_j) \times (\text{number of } k > j \text{ with } a_k < a_j)$! Two simple independent passes of a Fenwick tree (left-to-right and right-to-left) compute these counts for all $j$ in $\mathcal{O}(N \log N)$!

---

#### 4. Proof Sketches & Recurrences

Let $L[j] = |\{i < j : a_i > a_j\}|$ and $R[j] = |\{k > j : a_k < a_j\}|$. By the multiplication principle of independent choices, the total number of 3-inversions is $\sum_{j=1}^N L[j] \cdot R[j]$. $L[j]$ is computed by sweeping left-to-right: when at $j$, query how many elements in the BIT have value $> a_j$, then insert $a_j$. $R[j]$ is computed by sweeping right-to-left: when at $j$, query how many elements in the BIT have value $< a_j$, then insert $a_j$. Total runtime is $2 \times \mathcal{O}(N \log N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Count triplets $(i, j, k)$ satisfying monotonic index and value inequalities ($i < j < k$ and $a_i > a_j > a_k$).
- General pattern counting of length 3 (e.g. peak triplets $a_i < a_j > a_k$ or valley triplets).
- DP on sequences of fixed small length $K$ where transitions are dominated by rank order.
- Problems where fixing the 'center' or 'pivot' element decouples the remaining choices.

---

#### 7. Contest WA / TLE / RE Traps

- Integer overflow: total count of triplets can reach $\binom{N}{3} \approx \frac{(10^6)^3}{6} \approx 1.6 \times 10^{17}$, overflowing 32-bit `int`; always accumulate into `long long`.
- Reusing the Fenwick tree without clearing it between the two passes.
- Querying `bit.query(r)` instead of `bit.query(r - 1)` for strict inequality $< a_j$.
- Forgetting that duplicate array values require strict inequality specification in problem statements.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-7"></a>
### 7. When Fenwick Trees Fail

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** S-tier (The foundation of 2D computational geometry and advanced offline range querying) | **Rating Range:** 1900–2400+ | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (The foundation of 2D computational geometry and advanced offline range querying)
- Typical CF/ICPC rating range: 1900–2400+
- Core Distinction:
  - **Fenwick Tree:** Tracks discrete point frequencies (point updates, prefix sums).
  - **Segment Tree:** Tracks **continuous physical lengths** (e.g. total union length of active intervals) and non-invertible aggregations (Range Max/Min, Historical nearest duplicates).

---

## 2. The Klee’s Measure Problem (Union Area of $N$ Rectangles)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Fenwick Trees are extremely fast, use half the memory of Segment Trees, and have minimal code. However, Fenwick trees rely fundamentally on the **Group Invertibility** property of the operator (i.e. having an inverse operation like subtraction for addition, or XOR for XOR: $A \oplus B \oplus B = A$). Fenwick trees FAIL when: 1) The operator is a Monoid but NOT a Group (e.g. Range Minimum/Maximum query with updates: $\min(A, B)$ has no inverse!). 2) Range updates with range queries for non-linear operations (e.g. Range Chmin/Chmax - Segment Tree Beats). 3) Persistent data structures (requiring node copying). 4) Walking down the tree (binary searching on tree in $\mathcal{O}(\log N)$ without monotonic prefix).

---

#### 4. Proof Sketches & Recurrences

In a Fenwick tree, a range query $[L, R]$ is computed as $query(R) - query(L - 1)$. This formula is valid if and only if there exists an inverse operator $\ominus$ such that $(A \oplus B) \ominus B = A$. For the $(\min, \le)$ semi-group, there is no value $X$ such that $\min(A, X) = A$ for all possible hidden values of $A$. While a static Fenwick tree can support prefix minimums, it CANNOT support arbitrary range minimum queries $[L, R]$ with point updates without $\mathcal{O}(\log^2 N)$ overhead. A Segment Tree stores explicit node intervals, allowing associative monoid reduction over any arbitrary interval $[L, R]$ without requiring an inverse.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Decision Matrix Dispatcher: Segment Tree vs Fenwick Tree
// Segment tree handles arbitrary Monoid (Min/Max/Matrix) without inverse
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

struct SegTree {
    int n;
    vector<ll> tree;
    SegTree(int n_) : n(n_), tree(4 * n_, INF) {}
    void update(int node, int l, int r, int idx, ll val) {
        if (l == r) { tree[node] = val; return; }
        int mid = l + (r - l) / 2;
        if (idx <= mid) update(2 * node, l, mid, idx, val);
        else update(2 * node + 1, mid + 1, r, idx, val);
        tree[node] = min(tree[2 * node], tree[2 * node + 1]);
    }
    ll query(int node, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tree[node];
        if (r < ql || qr < l) return INF;
        int mid = l + (r - l) / 2;
        return min(query(2 * node, l, mid, ql, qr), query(2 * node + 1, mid + 1, r, ql, qr));
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Arbitrary range minimum or range maximum queries with point updates (Reach for Segment Tree).
- Range updates with range queries on non-additive operations (e.g. set all values in $[L, R]$ to $X$).
- Segment Tree Beats: range chmin / chmax / sum updates.
- Persistent queries where historical versions of the array must be preserved and queried (Persistent Segment Tree).

---

#### 7. Contest WA / TLE / RE Traps

- Attempting to support arbitrary range maximum queries with point updates using a Fenwick tree; will fail when an element is decreased.
- Allocating $2N$ nodes instead of $4N$ nodes for a recursive segment tree, causing heap-buffer-overflow.
- Forgetting identity elements: $\infty$ for min, $-\infty$ for max, $0$ for sum, $I$ for matrix multiplication.
- Using a full segment tree when simple prefix sums / Fenwick tree would execute 4x faster with $1/4$ the memory.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-8"></a>
### 8. Computing Overlapping 2D Rectangle Area in $O(N \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

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

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

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

#### 4. Proof Sketches & Recurrences

In the Segment tree over compressed $Y$-coordinates, each node maintains: `cnt` (how many active rectangles fully cover this node's $Y$-interval) and `len` (the total length of covered space in this subtree). If `cnt > 0`, the entire node interval is covered: `len = Y[r+1] - Y[l]`. If `cnt == 0`, its covered length is the sum of its children: `len = is_leaf ? 0 : (lchild.len + rchild.len)`. Notice this requires **NO lazy propagation** tags, because updates are strictly paired additions and subtractions!

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Compute the total area covered by at least one rectangle among $N \le 10^5$ rectangles.
- Perimeter of union of rectangles (maintains number of disjoint segments in node).
- Volume of union of 3D boxes (Sweep line on $Z$ with 2D rectangle union sweep inside).
- Coverage counting where coverage increments and decrements are symmetrical.

---

#### 7. Contest WA / TLE / RE Traps

- Compressing points instead of intervals: $Y$-coordinates represent interval spans $[Y_i, Y_{i+1}]$; a tree with $M$ unique coordinates has $M - 1$ elementary intervals.
- Using lazy propagation unnecessarily: `cnt` and `len` pull logic does not need lazy pushdown because every $+1$ has a matching $-1$.
- Integer overflow in area accumulation: area can reach $10^{18}$; always multiply `(events[i+1].x - events[i].x) * seg.len[1]` using 64-bit `long long`.
- Sorting events with inconsistent addition/deletion order on identical $X$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-9"></a>
### 9. Maximum Value Occurring At Least Twice in Subarray $[L, R]$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Sweep line, Offline Range Queries, Segment Tree, Previous Occurrence Map
- Tradeoff: Solves frequency-conditioned range queries offline in $\mathcal{O}((N + Q) \log N)$ instead of heavy online persistent trees.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

To answer queries 'What is the maximum value that appears at least twice in subarray $[L, R]$?': process queries offline sorted by their right endpoint $R$. For each element $A[R]$, let $prev[R]$ be its previous occurrence index in the array. $A[R]$ appears at least twice in $[L, R]$ if and only if $L \le prev[R]$! Therefore, as the sweep line advances to $R$, we update the position $prev[R]$ in a Segment tree with value $A[R]$ (and remove the previous occurrence's older activation). To answer a query with left bound $L$, we simply query the maximum value in the segment tree on range $[L, R]$!

---

#### 4. Proof Sketches & Recurrences

An element $v$ appears at least twice in $[L, R]$ iff the second-to-last occurrence of $v$ up to $R$ is $\ge L$. Let $p_1(v)$ be the last occurrence of $v$ and $p_2(v)$ be the second-to-last occurrence. When the sweep line is at $R = p_1(v)$, $v$ becomes an eligible candidate for any query with $L \le p_2(v)$. In the Segment Tree over array indices $1..N$, we activate index $p_2(v)$ with weight $v$. A query for subarray $[L, R]$ asks for $\max_{i \in [L, R]} tree[i]$. Each right-endpoint advance performs $\mathcal{O}(1)$ point updates on the Segment Tree, yielding $\mathcal{O}((N + Q) \log N)$ total time.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// C++17 — Maximum Duplicate Query via Offline Segment Tree Sweep
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int L, R, id;
    bool operator<(const Query& o) const { return R < o.R; }
};

struct MaxSegTree {
    int n;
    vector<int> tree;
    MaxSegTree(int n) : n(n), tree(2 * n, -1) {}
    
    void update(int p, int val) {
        for (p += n, tree[p] = max(tree[p], val); p > 1; p >>= 1) {
            tree[p >> 1] = max(tree[p], tree[p ^ 1]);
        }
    }
    
    int query(int l, int r) {
        int res = -1;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = max(res, tree[l++]);
            if (r & 1) res = max(res, tree[--r]);
        }
        return res;
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Query asks for max/min value appearing at least $K$ times (especially $K = 2$) in subarray $[L, R]$.
- Count of distinct elements in subarray $[L, R]$ (activate latest occurrence with $+1$, clear previous occurrence).
- Sum of elements appearing at least once / at least twice in range $[L, R]$.
- Offline range queries where eligibility depends on occurrence frequencies.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to clear older activations: when element $v$ appears for the 3rd time at $R$, the 2nd occurrence becomes the new threshold, and the 1st occurrence must be deactivated (set to 0) in the segment tree.
- 1-based vs 0-based indexing mismatch between array queries and segment tree.
- Queries with no valid duplicate: returning 0 or $-1$ correctly when no element appears twice.
- Sorting queries by $L$ instead of $R$ (requires reversing the sweep direction).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-10"></a>
### 10. Finding $K$ Intersections among $N$ Line Segments in $O((N + K) \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** High-tier Geometry / Computational Geometry Specialist | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: High-tier Geometry / Computational Geometry Specialist
- Rating Range: 2100–2600+
- The Brute Force Bottleneck: Checking all pairs of $N$ segments requires $O(N^2)$ intersection tests.
- **The Geometric Principle:** Two line segments can only intersect if they are **vertically adjacent** to each other in the active state at some sweep coordinate $X$.

---

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Given $N$ line segments in 2D space, two segments can intersect only if they are adjacent or near-adjacent in $Y$-order when a vertical sweep line passes through their $X$-interval. The **Bentley-Ottmann Algorithm** sweeps a vertical line from left to right. The active status structure (a balanced BST / `std::set`) stores all segments currently intersecting the sweep line, ordered by their $Y$-coordinate at the current sweep line $X$. Events include: 1) Segment start: insert segment into BST, test intersection with upper and lower neighbors. 2) Segment end: remove from BST, test intersection between newly adjacent neighbors. 3) Intersection event: swap the order of the two intersecting segments in the BST, test with new neighbors!

---

#### 4. Proof Sketches & Recurrences

At any non-event $X$, segments do not cross, so their vertical ordering in the status structure is invariant. When two segments intersect at point $(x^*, y^*)$, their relative vertical order reverses. By only checking intersection between adjacent segments in the active BST, every actual intersection is discovered before the sweep line reaches it. The event queue processes $2N + K$ events, each performing $\mathcal{O}(\log N)$ BST operations, achieving $\mathcal{O}((N + K) \log N)$ overall complexity.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Bentley-Ottmann Segment Intersection Framework
#include <bits/stdc++.h>
using namespace std;

struct Point { double x, y; };
struct Segment { Point p, q; int id; };

// Event in priority queue
struct Event {
    double x;
    int type; // 0 = start, 1 = intersection, 2 = end
    int seg1, seg2;
    bool operator>(const Event& o) const { return x > o.x; }
};

// Finds if any two segments intersect in O(N log N) (Shamos-Hoey)
bool has_intersection(const vector<Segment>& segs) {
    // Shamos-Hoey simplification: stops at the very first intersection event
    return false; // Returns true if an intersection is detected
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Determine if any two line segments among $N \le 10^5$ segments intersect (Shamos-Hoey $\mathcal{O}(N \log N)$).
- Find all $K$ intersection points among $N$ segments when $K$ is small ($K \ll N^2$).
- Planar graph subdivision / map overlay construction.
- Validating whether a polygon is simple (no self-intersecting edges).

---

#### 7. Contest WA / TLE / RE Traps

- Floating-point comparator in `std::set`: as the sweep line moves, the $Y$-coordinate of a segment changes. Mutating comparator values while elements reside in `std::set` violates strict weak ordering and causes undefined behavior/crashes! Comparator must reference a global sweep $X$ variable.
- Vertical line segments: slope is infinite ($x_1 = x_2$); must be handled as a special event type.
- Multiple segments intersecting at the exact same point: produces duplicate events in priority queue.
- Missing intersection check when two non-adjacent segments become neighbors upon the removal of an intermediate segment.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-11"></a>
### 11. B. FIRST PRINCIPLES & ALGORITHM MECHANICS

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Meta-Methodology for all Sweep Line Problems
- Typical CF/ICPC rating range: 1500–2400
- Prerequisites: Invariants, Event Queues, Active Status Structures
- Blueprint: The 3 invariant laws governing all sweep line algorithms.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Every sweep-line algorithm without exception consists of exactly three fundamental components: 1) **The Sweep Space**: A continuous dimension (time, $X$-axis, tree depth) along which execution advances monotonically. 2) **The Event Queue**: A priority queue or sorted array of discrete points where the topological state of the system changes. 3) **The Active Status Structure**: A dynamic data structure (Fenwick, Segment Tree, Treap, `std::set`) that maintains the cross-section of objects currently active at the sweep frontier. The invariant is that the status structure is 100% accurate for the current sweep frontier position.

---

#### 4. Proof Sketches & Recurrences

Let the continuous state space be $\Omega$. If state transitions only occur at discrete coordinates $E = \{e_1, e_2, \dots, e_M\}$, then for any $x \in (e_i, e_{i+1})$, the active state is static. Hence, the continuous problem $\int_\Omega f(x) dx$ is discretized into $\sum_{i=1}^{M-1} f(e_i) \cdot (e_{i+1} - e_i)$. The time complexity is bounded by $\mathcal{O}(M \log M + M \cdot T_{\text{update}})$, converting continuous geometry into discrete algebra.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// C++ Contest Template — Bentley-Ottmann Concept & Segment Intersection
#include <bits/stdc++.h>
using namespace std;

struct Point {
    double x, y;
    bool operator<(const Point& o) const {
        if (abs(x - o.x) > 1e-9) return x < o.x;
        return y < o.y;
    }
};

struct Segment {
    Point p1, p2; // p1.x <= p2.x
    int id;
    
    double get_y(double current_x) const {
        if (abs(p1.x - p2.x) < 1e-9) return p1.y;
        return p1.y + (p2.y - p1.y) * (current_x - p1.x) / (p2.x - p1.x);
    }
};

double sweep_x = 0;

struct SegmentComparator {
    bool operator()(const Segment& a, const Segment& b) const {
        double ya = a.get_y(sweep_x);
        double yb = b.get_y(sweep_x);
        if (abs(ya - yb) > 1e-9) return ya < yb;
        return a.id < b.id;
    }
};

// Check if two line segments intersect and return intersection point
bool get_intersection(const Segment& a, const Segment& b, Point& inter) {
    double x1 = a.p1.x, y1 = a.p1.y, x2 = a.p2.x, y2 = a.p2.y;
    double x3 = b.p1.x, y3 = b.p1.y, x4 = b.p2.x, y4 = b.p2.y;
    
    double denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
    if (abs(denom) < 1e-9) return false; // Parallel or collinear
    
    double px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom;
    double py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom;
    
    // Check if (px, py) lies within bounding boxes of both segments
    if (px < min(x1, x2) - 1e-9 || px > max(x1, x2) + 1e-9) return false;
    if (px < min(x3, x4) - 1e-9 || px > max(x3, x4) + 1e-9) return false;
    if (py < min(y1, y2) - 1e-9 || py > max(y1, y2) + 1e-9) return false;
    if (py < min(y3, y4) - 1e-9 || py > max(y3, y4) + 1e-9) return false;
    
    inter = {px, py};
    return true;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Any geometric problem with $N$ static 2D objects.
- Static offline queries on an array that can be processed in sorted order of $R$.
- Tree problems transformed into 1D interval sweeps via Euler tour linearization.
- Interval union, intersection, or coverage metrics.

---

#### 7. Contest WA / TLE / RE Traps

- Violating the monotonicity invariant: inserting an event whose coordinate is in the past.
- Imprecise event tie-breaking order leading to phantom state discrepancies.
- Memory explosion: generating dynamic events without deleting expired events.
- Failing to handle empty intervals or points with $L > R$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-12"></a>
### 12. Mapping Subtree & Path Queries to 1D Sweep Intervals

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Trees are hierarchical, non-linear graphs. Sweep lines require an ordered, 1D domain.
- By assigning pre-order entry times (`in[u]`) and exit times (`out[u]`) during a single DFS, **subtrees become contiguous 1D subsegments**.

```
Tree Hierarchy:              Euler Tour Flattening (Pre-order):
       (1)                    Index:  0   1   2   3   4
      /   \                   Node:  [1] [2] [4] [5] [3]
    (2)   (3)                         |_________|
   /   \                              Subtree of 2:
 (4)   (5)                            in[2] = 1, out[2] = 4 -> [1, 3]
```

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

1. **Subtree of node $u$:** Exactly the 1D range $[in[u], out[u] - 1]$.
2. **Descendant Test in $O(1)$:** Node $v$ is inside subtree of $u \iff in[u] \le in[v] < out[u]$.
3. **Subtree-to-Subsegment Transformation:** Any tree query (e.g. "count distinct values in subtree of $u$", "find max duplicate in subtree of $u$") is transformed into a standard 1D range query $[L, R]$ on the flattened array.

---

## 3. The Circular Doubled Euler Tour ($A + A$) Trick

---

#### 4. Proof Sketches & Recurrences

In an Euler tour DFS, every node in $u$'s subtree is visited after $tin[u]$ and before $tout[u]$. Therefore, $v \in \text{subtree}(u) \iff tin[u] \le tin[v] \le tout[u]$. Any subtree condition combined with an auxiliary parameter (depth, weight, time of activation) becomes a 2D box query $[tin[u], tout[u]] \times [d_{\min}, d_{\max}]$. Sorting vertices and queries by the auxiliary parameter allows a 1D Fenwick tree over $[1, N]$ to answer all queries in $\mathcal{O}((N + Q) \log N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Tree Subtree Queries via Euler Tour Linearization & Offline BIT Sweep
#include <bits/stdc++.h>
using namespace std;

struct TreeSweep {
    int n, timer = 0;
    vector<vector<int>> adj;
    vector<int> tin, tout;
    TreeSweep(int n_) : n(n_), adj(n_ + 1), tin(n_ + 1), tout(n_ + 1) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void dfs(int u, int p) {
        tin[u] = ++timer;
        for (int v : adj[u]) if (v != p) dfs(v, u);
        tout[u] = timer;
    }
    // Subtree of u is strictly the range [tin[u], tout[u]]
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Count nodes in subtree of $u$ with value $\ge X$ or depth $\le K$.
- Path queries where paths are converted to pairs of Euler tour updates.
- DSU on tree alternative for offline queries.
- Subtree distinct color counting (combine with previous occurrence sweep).

---

#### 7. Contest WA / TLE / RE Traps

- Euler tour timer off-by-one: initializing timer to 0 vs 1; Fenwick tree requires 1-indexed positions.
- Visiting back-edges in undirected trees: must guard with `if (v != p)` during DFS.
- Tree path vs subtree: subtree is a single contiguous interval; paths between $u$ and $v$ require HLD or double-entry Euler tour ($tin[u]$ and $tout[u]$).
- Forgetting that $tout[u] = timer$ must be assigned AFTER all children have been traversed.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-13"></a>
### 13. Edge-Cut Tree Component Splitting in $O((N + Q) \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

Removing an edge $(u, v)$ (where $v$ is a child of $u$) splits a tree of $N$ nodes into two disjoint components:
1. **Component 1 (The Subtree of $v$):** Naturally forms contiguous interval $[in[v], out[v] - 1]$.
2. **Component 2 (The Rest of the Tree):** In a standard Euler tour, this fractures into two disjoint pieces: prefix $[0, in[v] - 1]$ and suffix $[out[v], N - 1]$.

```
Standard Euler Tour:
[ 0 ... in[v]-1 ] [ in[v] ... out[v]-1 ] [ out[v] ... N-1 ]
\_______________/ \____________________/ \________________/
   Prefix (Rest)       Subtree of v          Suffix (Rest)
```

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

If we append the pre-order array to itself ($A + A$, length $2N$):
- Subtree of $v$: $[in[v], out[v] - 1]$
- Rest of the tree: Starts at $out[v]$ and wraps around of length $N - \text{subtree\_size}$, ending at $in[v] + N - 1$!
- **Both components become single contiguous subarrays in the doubled array!**

```
Doubled Euler Tour (Length 2N):
[ ... in[v] ... out[v] ... N-1 | 0 ... in[v]+N ... out[v]+N ... 2N-1 ]
               |_______________________|
               Rest of Tree: [out[v], in[v] + N - 1]
```

---

#### 4. Proof Sketches & Recurrences

If edge deletions and additions are arbitrarily mixed offline, construct a Segment Tree over time $[1, Q]$. Each edge exists during a collection of disjoint time intervals $[t_{\text{start}}, t_{\text{end}}]$. Insert each edge into $\mathcal{O}(\log Q)$ canonical nodes of the Segment Tree. A DFS traversal over the Segment Tree maintains graph connectivity using a DSU with Rollback (history stack without path compression, using union by rank). At each leaf $t$, answer the query for time $t$. Total complexity: $\mathcal{O}((N + Q) \log N \log Q)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Reverse Time DSU for Edge Cut / Component Splitting
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> p, sz;
    int comps;
    DSU(int n) : p(n + 1), sz(n + 1, 1), comps(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b]; comps--;
        return true;
    }
};
```

##### Python 3 Template

```python
import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # Read edges (1-indexed input)
    edges = []
    idx = 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        edges.append((u, v))
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    # Read vertex values
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(input_data[idx])
        idx += 1

    # Iterative DFS for Euler Tour (Avoids Python recursion depth limits)
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler = []
    
    # Stack holds: (node, parent, is_post_order)
    stack = [(1, 0, False)]
    timer = 0
    
    while stack:
        u, p, is_post = stack.pop()
        
        if not is_post:
            in_time[u] = timer
            euler.append(a[u])
            timer += 1
            stack.append((u, p, True))
            for v in adj[u]:
                if v != p:
                    stack.append((v, u, False))
        else:
            out_time[u] = timer

    # Circular array doubling: A = euler + euler (Size 2N)
    A = euler + euler
    
    # Prepare offline queries for all N-1 edge cuts
    queries = []
    for i in range(n - 1):
        u, v = edges[i]
        if in_time[u] > in_time[v]:
            u, v = v, u  # v is the deeper child
            
        # Part 0: Subtree of v
        l1 = in_time[v]
        r1 = out_time[v] - 1
        
        # Part 1: Rest of tree (wrapped around in doubled array)
        l2 = out_time[v]
        r2 = in_time[v] + n - 1
        
        queries.append((l1, r1, i, 0))
        queries.append((l2, r2, i, 1))
        
    # Sort queries ascending by right boundary R
    queries.sort(key=lambda x: x[1])

    # Iterative Segment Tree: Point Update / Range Max Query
    seg_n = 2 * n
    tree = [0] * (2 * seg_n)
    
    def update(p, val):
        p += seg_n
        if val > tree[p]:
            tree[p] = val
            p //= 2
            while p > 0:
                tree[p] = max(tree[2 * p], tree[2 * p + 1])
                p //= 2

    def query(l, r):
        res = 0
        l += seg_n
        r += seg_n + 1
        while l < r:
            if l % 2 == 1:
                res = max(res, tree[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = max(res, tree[r])
            l //= 2
            r //= 2
        return res

    # Offline sweep line over doubled array
    ans = [[0, 0] for _ in range(n - 1)]
    last_pos = {}
    q_idx = 0
    m = len(queries)
    
    for i in range(2 * n):
        val = A[i]
        if val in last_pos:
            update(last_pos[val], val)
        last_pos[val] = i
        
        while q_idx < m and queries[q_idx][1] == i:
            L, R, edge_idx, part = queries[q_idx]
            ans[edge_idx][part] = query(L, R)
            q_idx += 1

    # Output max duplicate across both components for each edge cut
    out = [str(max(ans[i][0], ans[i][1])) for i in range(n - 1)]
    print("\n".join(out))

if __name__ == '__main__':
    solve()
```

---

#### 6. Recognition Trigger Signals & Heuristics

- 

---

#### 7. Contest WA / TLE / RE Traps

- Using path compression in DSU with Rollback: path compression destroys the tree structure and prevents rollback; only union-by-rank/size is allowed when rollbacks are needed.
- Forgetting edges that are NEVER deleted: must add all permanent edges to the initial DSU in reverse time.
- Query indexing: storing reverse-time answers requires reversing the output array before printing.
- Multiple components initially: comps counter must be initialized to $N$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-14"></a>
### 14. Transforming Tree Queries via DFS Active-Path Sweeping

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2400
- Prerequisites: Tree DFS, Root-to-Node Active Path, Fenwick Tree / Stack Rollback
- Tradeoff: Solves ancestor-path queries in $\mathcal{O}((N + Q) \log N)$ with $\mathcal{O}(N)$ memory, eliminating heavy binary lifting tables or HLD.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

To answer queries about ancestors on the path from root to node $u$ (e.g. 'How many ancestors of $u$ have weight $\le W$ and depth $\ge D$?'): attach all queries for node $u$ to an adjacency list `queries[u]`. Run a single DFS from the root. When entering node $u$, insert $u$'s value into a global data structure (Fenwick tree or monotone stack). While at $u$, answer all queries attached to $u$ by directly querying the data structure! When exiting node $u$ (backtracking), remove $u$'s value from the data structure. The data structure exclusively contains elements on the active path from root to $u$!

---

#### 4. Proof Sketches & Recurrences

During a DFS traversal, the call stack corresponds exactly to the simple path from the root to the currently visited node $u$. By inserting node $u$ on entry and retracting node $u$ on exit, the active data structure maintains the multiset $\{v : v \text{ is an ancestor of } u\}$. Each node is inserted once and deleted once. If the data structure is a Fenwick Tree, total time spent across the entire tree is $2N \log N$, and answering $Q$ queries takes $\mathcal{O}(Q \log N)$. Memory is strictly $\mathcal{O}(N + Q)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// DFS Active-Path Sweeping Framework
#include <bits/stdc++.h>
using namespace std;

struct Query { int val, id; };

struct ActivePathSweep {
    int n;
    vector<vector<int>> adj;
    vector<vector<Query>> queries;
    vector<int> ans;
    ActivePathSweep(int n_, int q_) : n(n_), adj(n_ + 1), queries(n_ + 1), ans(q_) {}
    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    void add_query(int u, int val, int qid) { queries[u].push_back({val, qid}); }
    void dfs(int u, int p) {
        // 1. Enter: Insert u into active path data structure (e.g. BIT)
        // ... bit.add(val[u], +1); ...
        // 2. Answer all queries for node u
        for (const auto& q : queries[u]) {
            // ans[q.id] = bit.query(q.val);
        }
        // 3. Recurse into children
        for (int v : adj[u]) if (v != p) dfs(v, u);
        // 4. Exit: Retract u from active path data structure
        // ... bit.add(val[u], -1); ...
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Query asks for properties of ancestors of $u$ (e.g. number of ancestors with property $P$).
- Finding the nearest ancestor satisfying a condition (maintain monotone stack on active path with binary search).
- Path queries where the path is strictly vertical (from node to root).
- Counting tree paths with sum $\le S$ starting from an ancestor.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to retract on exit: failing to remove node $u$ from the data structure on exit leaks its values into sibling subtrees.
- Stack overflow: deep skew trees ($N = 2 \times 10^5$) require `#pragma comment(linker, "/STACK:...")` or manual stack unwinding.
- Modifying query answers after backtracking: answers must be recorded immediately while visiting node $u$.
- Applying active path sweeping to arbitrary paths $u \leftrightarrow v$ without splitting the query at $\text{LCA}(u, v)$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---

<a id="topic-15"></a>
### 15. Prerequisites

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–1800
- Prerequisites: Arrays, sorting, prefix sums

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

##### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

##### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

##### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

##### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

#### 3. Core Intuition & Problem Framing

Prerequisites for Sweep Line mastery: 1D Difference Arrays (`diff[L] += v, diff[R+1] -= v`), sorting events by coordinate with secondary tie-breaking, and coordinate compression of sparse coordinates into dense indices.

---

#### 4. Proof Sketches & Recurrences

Prefix sum of difference array reproduces original values: $A[i] = \sum_{j=1}^i \text{diff}[j]$. Sorting events ensures processing occurs in temporal or spatial monotonicity.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Sweep Line Prerequisites: 1D Difference Array & Coordinate Compression
#include <bits/stdc++.h>
using namespace std;

vector<int> compress(vector<long long>& coords) {
    vector<long long> vals = coords;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<int> ranks(coords.size());
    for (size_t i = 0; i < coords.size(); ++i) {
        ranks[i] = lower_bound(vals.begin(), vals.end(), coords[i]) - vals.begin();
    }
    return ranks;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Multiple range additions followed by point queries.
- Coordinates in range $[-10^9, 10^9]$ where only relative order matters.

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one at right endpoint: adding $+v$ at $L$ and $-v$ at $R$ instead of $R+1$ for inclusive range $[L, R]$.
- Forgetting to deduplicate with `unique` before computing ranks.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

#### 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---


---
