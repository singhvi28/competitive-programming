# 8. Coordinate compression

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Very Common  
> **Prerequisites:** Sorting, `lower_bound`, Fenwick/segtree indexing  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Sorting, `lower_bound`, Fenwick/segtree indexing

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

Data structures want **dense ranks** \(1..k\), not raw values in \(\pm 10^9\). Collect every value that will ever appear as an index/key, sort-unique, replace each value by its rank. This is not optional garnish — it is how Fenwick/segtree/Mo frequency arrays become memory-feasible. Compress **exactly the set of coordinates you need** (endpoints, values, times); over-collecting is fine, under-collecting is WA.

---

## 4. Proof Sketches & Recurrences

Let \(V\) be the multiset of relevant coordinates, \(k = |unique(V)|\).
Map \(x \mapsto \mathrm{rank}(x) \in [1,k]\) via sort + lower_bound.
Order-preserving: \(x < y \iff \mathrm{rank}(x) < \mathrm{rank}(y)\).
All range-of-value queries become range-of-rank queries.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) sort-unique
- Per-query / per-operation: \(O(\log n)\) per `id`
- Total: dominated by DS using ranks
- Memory: \(O(k)\) for the sorted vector`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace compress {
struct Compr {
    vector<long long> vals;

    void add(long long x) { vals.push_back(x); }

    void build() {
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());
    }

    int size() const { return (int)vals.size(); }

    // 1-indexed rank; x must have been added
    int id(long long x) const {
        return (int)(lower_bound(vals.begin(), vals.end(), x) - vals.begin()) + 1;
    }

    // largest rank with vals[rank-1] <= x (1-index); 0 if all greater
    int id_leq(long long x) const {
        return (int)(upper_bound(vals.begin(), vals.end(), x) - vals.begin());
    }
};

struct Fenwick {
    int n; vector<int> bit;
    Fenwick(int n): n(n), bit(n + 1, 0) {}
    void add(int i, int v) { for (; i <= n; i += i & -i) bit[i] += v; }
    int sumPrefix(int i) const {
        int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s;
    }
};

vector<int> count_smaller_left(const vector<long long>& a) {
    Compr c;
    for (auto x : a) c.add(x);
    c.build();
    Fenwick fw(c.size());
    vector<int> ans(a.size());
    for (int i = 0; i < (int)a.size(); ++i) {
        int r = c.id(a[i]);
        ans[i] = fw.sumPrefix(r - 1);
        fw.add(r, 1);
    }
    return ans;
}
} // namespace compress
```

### Python 3 Template

```python
import bisect

class Compr:
    def __init__(self):
        self.vals = []
    def add(self, x):
        self.vals.append(x)
    def build(self):
        self.vals = sorted(set(self.vals))
    def id(self, x):  # 1-index
        return bisect.bisect_left(self.vals, x) + 1
    def id_leq(self, x):
        return bisect.bisect_right(self.vals, x)

def count_smaller_left(a):
    c = Compr()
    for x in a:
        c.add(x)
    c.build()
    n = len(c.vals)
    bit = [0] * (n + 1)
    def add(i, v):
        while i <= n:
            bit[i] += v
            i += i & -i
    def sum_prefix(i):
        s = 0
        while i:
            s += bit[i]
            i -= i & -i
        return s
    ans = []
    for x in a:
        r = c.id(x)
        ans.append(sum_prefix(r - 1))
        add(r, 1)
    return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- Values up to \(10^9\) but \(n \le 2\cdot 10^5\)
- Fenwick/segtree indexed by value
- Offline geometry: \(x\)-coordinates of segments
- “Rank of \(a_i\) among unique values”

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to `add` a query-only coordinate before `build`
- Mixing 0-index ranks with 1-index Fenwick
- Compressing after some updates already applied
- Using `map<int,int>` instead of vector ranks → extra \(\log\) everywhere (OK but slower)
- Assuming ranks are values — they are not; don’t output ranks unless asked

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

- Compress pairs \((x,y)\) for 2D Fenwick (linearize carefully)
- Dynamic compression via `map` / policy BBST when values stream online
- Discrete for floats: sort unique with epsilon care (prefer integers)

---

## 11. Typical Problem Archetypes

1. Standard application: inversion count with Fenwick
2. Slightly disguised: rectangle area union needs compressed \(y\) for sweep
3. Difficult: compress only “interesting” times for offline queries
4. Very difficult / advanced: online insertion of new coordinates into a dynamic segtree (no full compress)

---

## 12. Recognition & Identification Drills

1. \(n=2\cdot 10^5\) values in \([1,10^{18}]\); count inversions.
2. Queries ask frequency of values \(\le x\) for arbitrary \(x\) not in \(a\) — what must you compress?
3. Sweep-line on segments with \(x\in[1,10^9]\) — array of size \(10^9\) or compress?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: any value-indexed DS with huge universe, small \(n\)
- Key invariant: order-preserving bijection onto \(1..k\)
- Key formula: `sort + unique + lower_bound`
- Complexity: \(O(n\log n)\) build
- Template to remember: collect → `build` → `id(x)`

---

## 11. Sweep-line patterns

---
