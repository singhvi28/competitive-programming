# Offline query processing

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1700–2400 | **Frequency:** Common  
> **Prerequisites:** Sorting, Fenwick/segtree, DSU optional, coordinate compression  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Sorting, Fenwick/segtree, DSU optional, coordinate compression

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

If **all queries are known before any answer is required**, you may reorder them, batch them, or sweep a pointer while maintaining a data structure. Offline is a *meta-technique*: the win is choosing an order where the DS only supports **easy transitions** (e.g. only increase \(r\), never decrease). Classic pattern: sort queries by \(r\); scan array left→right; answer when `i == query.r`. This often replaces Mo or persistent structures.

---

## 4. Proof Sketches & Recurrences

Online: each query \(O(\mathrm{cost_{online}})\).
Offline sort by key: \(O((n+q)\log(n+q) + (n+q)\cdot F)\) where \(F\) is Fenwick op.
Example — distinct values in \([l,r]\): keep last position of each value in Fenwick (point +1 at last pos, -1 at previous); sort queries by \(r\); when advancing \(r\), update last occurrence; query sum on \([l,r]\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort queries \(O(q\log q)\); map values if needed
- Per-query / per-operation: amortized \(O(F)\) as pointer advances
- Total: \(O((n+q)\log n)\) typical with Fenwick
- Memory: \(O(n+q)\)`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace offline {
struct Fenwick {
    int n; vector<int> bit;
    Fenwick(int n): n(n), bit(n + 1, 0) {}
    void add(int i, int v) { for (; i <= n; i += i & -i) bit[i] += v; }
    int sumPrefix(int i) const {
        int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s;
    }
    int rangeSum(int l, int r) const { // 1-index inclusive
        return sumPrefix(r) - sumPrefix(l - 1);
    }
};

struct Query { int l, r, idx; };

// Distinct count on [l,r] for static array a[1..n]
vector<int> distinct_offline(const vector<int>& a, vector<Query> qs) {
    int n = (int)a.size() - 1;
    sort(qs.begin(), qs.end(), [](const Query& A, const Query& B) {
        return A.r < B.r;
    });
    Fenwick fw(n);
    unordered_map<int, int> last; // value -> last position
    last.reserve(n * 2);
    vector<int> ans(qs.size());
    int r = 0;
    for (auto& q : qs) {
        while (r < q.r) {
            ++r;
            int v = a[r];
            if (last.count(v)) fw.add(last[v], -1);
            fw.add(r, +1);
            last[v] = r;
        }
        ans[q.idx] = fw.rangeSum(q.l, q.r);
    }
    return ans;
}
} // namespace offline
```

### Python 3 Template

```python
class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i
    def sum_prefix(self, i):
        s = 0
        while i:
            s += self.bit[i]
            i -= i & -i
        return s

def distinct_offline(a, queries):
    # a is 1-indexed list; queries = (l,r,idx)
    n = len(a) - 1
    qs = sorted(queries, key=lambda x: x[1])
    fw = Fenwick(n)
    last = {}
    ans = [0] * len(qs)
    r = 0
    for l, rr, idx in qs:
        while r < rr:
            r += 1
            v = a[r]
            if v in last:
                fw.add(last[v], -1)
            fw.add(r, +1)
            last[v] = r
        ans[idx] = fw.sum_prefix(rr) - fw.sum_prefix(l - 1)
    return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- “\(q\) queries on a static array” and answers independent
- Queries ask something monotone in an endpoint
- “Last time value \(x\) appeared”, distinct in prefix, invert queries
- Updates and queries mixed but **all given up front** → process by time with segtree-on-time / DSU rollback (see §02)
- You catch yourself wanting persistence only to go “back in time” for known queries

---

## 7. Contest WA / TLE / RE Traps

- Answering in sorted order but forgetting to write `ans[idx]`
- Advancing \(r\) past `q.r` incorrectly (off-by-one)
- Using offline when queries are adaptive/interactive
- Heavy `unordered_map` without reserve → TLE; compress values first

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

- Sort by \(l\) decreasing while maintaining a structure on suffixes
- CDQ divide-and-conquer (3D partial order) — offline + D&C
- Offline dynamic connectivity (segtree on time) — link §02
- Mo’s algorithm — offline with add/del both directions (§6)

---

## 11. Typical Problem Archetypes

1. Standard application: distinct values in \([l,r]\)
2. Slightly disguised: for each query, mex of subarray (offline + segtree on last positions)
3. Difficult: queries insert/delete known offline → process chronologically with rollback DS
4. Very difficult / advanced: CDQ / multi-level offline

---

## 12. Recognition & Identification Drills

1. \(q\) queries ask the sum of \(\mathrm{next}[i]\) for \(i\in[l,r]\) where \(\mathrm{next}\) depends only on prefixes of the array — can you avoid rebuilding?
2. Static array; for each query count pairs \((i,j)\) in range with \(a_i > a_j\) — offline inversion with Fenwick?
3. All updates and queries given; you need connectivity after each update — online DSU vs offline?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: all queries known; find a monotone order for a simple DS
- Key invariant: pointer only moves forward; answers stored by `idx`
- Key formula: sort by \(r\) + Fenwick last-occurrence → distinct count
- Complexity: \(O((n+q)\log n)\)
- Template to remember: `struct Query{l,r,idx}`; sort; expand; `ans[idx]=...`

---

---
