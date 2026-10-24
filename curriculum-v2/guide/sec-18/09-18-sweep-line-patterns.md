# 9. Sweep-line patterns

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Coordinate compression, Fenwick/segtree, event sorting  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Coordinate compression, Fenwick/segtree, event sorting

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

## 3. Core Intuition & Problem Framing

Sort geometric (or 1D) **events** by a sweep coordinate; maintain the active cross-section in a DS. Vertical line sweeps left→right: at each \(x\), process all events at that \(x\) (insert segment, delete segment, query stabbing). The same pattern is “sort endpoints + Fenwick” for intervals on a line. Sweep converts 2D problems into dynamic 1D problems.

---

## 4. Proof Sketches & Recurrences

Sort \(E\) events: \(O(E\log E)\).
Each insert/delete/query into DS: \(O(F)\).
Total \(O(E\log E + E\cdot F)\).
For interval coverage on a line: events \(+1\) at \(L\), \(-1\) at \(R+1\); sweep prefix sum.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: compress + sort events \(O(E\log E)\)
- Per-query / per-operation: \(O(\log n)\) DS ops
- Total: \(O(E\log E)\)
- Memory: \(O(E + k)\)`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace sweep {
struct Fenwick {
    int n; vector<int> bit;
    Fenwick(int n): n(n), bit(n + 1, 0) {}
    void add(int i, int v) { for (; i <= n; i += i & -i) bit[i] += v; }
    int sumPrefix(int i) const {
        int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s;
    }
    int rangeSum(int l, int r) const {
        if (l > r) return 0;
        return sumPrefix(r) - sumPrefix(l - 1);
    }
};

struct Compr {
    vector<long long> vals;
    void add(long long x) { vals.push_back(x); }
    void build() {
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());
    }
    int size() const { return (int)vals.size(); }
    int id(long long x) const {
        return (int)(lower_bound(vals.begin(), vals.end(), x) - vals.begin()) + 1;
    }
};

struct Event {
    long long x;
    int type; // 0=add, 1=query, 2=remove
    int y1, y2, idx;
    bool operator<(const Event& o) const {
        if (x != o.x) return x < o.x;
        return type < o.type; // add before query before remove
    }
};

// Horizontal seg [x1,x2] at y; vertical query at x on [y1,y2]
vector<int> count_intersections(
    vector<tuple<long long,long long,long long>> horiz, // x1,x2,y
    vector<tuple<long long,long long,long long>> vert    // x,y1,y2
) {
    Compr yc;
    for (auto [x1, x2, y] : horiz) yc.add(y);
    for (auto [x, y1, y2] : vert) { yc.add(y1); yc.add(y2); }
    yc.build();

    vector<Event> ev;
    for (auto [x1, x2, y] : horiz) {
        int yy = yc.id(y);
        ev.push_back({x1, 0, yy, yy, -1});
        ev.push_back({x2 + 1, 2, yy, yy, -1});
    }
    int qi = 0;
    for (auto [x, y1, y2] : vert) {
        int ya = yc.id(y1), yb = yc.id(y2);
        if (ya > yb) swap(ya, yb);
        ev.push_back({x, 1, ya, yb, qi++});
    }
    sort(ev.begin(), ev.end());
    Fenwick fw(yc.size());
    vector<int> ans(qi);
    for (auto& e : ev) {
        if (e.type == 0) fw.add(e.y1, +1);
        else if (e.type == 2) fw.add(e.y1, -1);
        else ans[e.idx] = fw.rangeSum(e.y1, e.y2);
    }
    return ans;
}
} // namespace sweep
```

### Python 3 Template

```python
# Event = (x, type, y1, y2, idx); type 0 add, 1 query, 2 remove
# Same algorithm as C++; Fenwick on compressed y.
```

---

## 6. Recognition Trigger Signals & Heuristics

- Rectangles / segments / intervals; ask intersections, union area, coverage
- “For each point, how many segments cover it?”
- Events: open, close, query — process opens before queries before closes at same \(x\) (tie-break carefully)
- Closest pair / line sweep with active set ordered by \(y\)

---

## 7. Contest WA / TLE / RE Traps

- Wrong tie-break at equal \(x\) (query before add → miss; remove before query → miss)
- Off-by-one on closed/open segments (`x2+1` vs `x2`)
- Forgetting to compress all \(y\) from queries and segments
- Using `set` of active \(y\) when multiples needed → multiset / Fenwick freqs

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

## 10. Algorithmic Variants & Advanced Extensions

- Union area of rectangles (sweep + segtree on coverage lengths)
- Closest pair sweep with active window of width \(d\)
- 1D interval sweep (difference array / events) — simplest form
- Angular sweep around a point

---

## 11. Typical Problem Archetypes

1. Standard application: how many segments cover each query point
2. Slightly disguised: intersection count of horiz/vert segments
3. Difficult: rectangle union area
4. Very difficult / advanced: Bentley–Ottmann style general segment intersections

---

## 12. Recognition & Identification Drills

1. \(n\) axis-parallel rectangles; compute union area.
2. \(n\) intervals on \(\mathbb{Z}\); for each query point, coverage count.
3. Closest pair of points in the plane — D&C vs sweep?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: geometry/intervals reduce to sorted events + 1D DS
- Key invariant: active set = all objects stabbed by the sweep line
- Key formula: sort events; fix ties by type order
- Complexity: \(O(E\log E)\)
- Template to remember: `Event{x,type,...}` + Fenwick/segtree on other axis

---

---
