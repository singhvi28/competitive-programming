# 7. Parallel binary search

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Binary search on answer, offline queries, Fenwick/segtree/DSU  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Binary search on answer, offline queries, Fenwick/segtree/DSU

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

You have \(q\) independent problems of the form “binary search the earliest time / minimum \(x\) such that predicate \(P_i(x)\) holds,” and \(P_i\) is **monotone**, and checking \(P_i(\mathrm{mid})\) needs a heavy shared data structure that can be built by scanning events up to `mid`. Instead of \(q\) separate binary searches, keep an interval \([lo_i,hi_i]\) per query and process **all queries with the same mid** together in rounds (\(\log\) rounds). Each round: bucket queries by mid, scan the global timeline once, answer all mid-checks.

---

## 4. Proof Sketches & Recurrences

Sequential: \(q \cdot \log X \cdot C\) if each check costs \(C\) from scratch.
PBS: \(\log X\) rounds; each round scans all updates once \(O(U\cdot F)\) and assigns checks to buckets \(O(q)\).
Total \(O((U\cdot F + q)\log X)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(\log\) rounds shared
- Total: \(O((m\alpha(n)+q)\log m)\) for connectivity example
- Memory: \(O(n+m+q)\)`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace pbs {
struct DSU {
    vector<int> p, r;
    DSU(int n): p(n), r(n, 0) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    void unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return;
        if (r[a] < r[b]) swap(a, b);
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
    }
};

struct Edge { int u, v; };
struct Query { int u, v, idx; };

// Earliest edge index (1-based) connecting query ends; -1 if never
vector<int> earliest_connect(int n, const vector<Edge>& edges, vector<Query> qs) {
    int m = (int)edges.size();
    int qn = (int)qs.size();
    vector<int> lo(qn, 0), hi(qn, m + 1); // answer = hi when hi <= m

    for (int iter = 0; iter < 22; ++iter) {
        bool cont = false;
        vector<vector<int>> bucket(m + 2);
        for (int i = 0; i < qn; ++i) {
            if (lo[i] + 1 < hi[i]) {
                cont = true;
                int mid = (lo[i] + hi[i]) >> 1;
                bucket[mid].push_back(i);
            }
        }
        if (!cont) break;

        DSU dsu(n);
        for (int t = 1; t <= m; ++t) {
            dsu.unite(edges[t - 1].u, edges[t - 1].v);
            for (int qi : bucket[t]) {
                if (dsu.find(qs[qi].u) == dsu.find(qs[qi].v))
                    hi[qi] = t;
                else
                    lo[qi] = t;
            }
        }
        for (int qi : bucket[m + 1]) {
            // mid beyond all edges: still disconnected after m
            if (dsu.find(qs[qi].u) == dsu.find(qs[qi].v))
                hi[qi] = m + 1; // should not happen if mid=m+1 means "after all"
            else
                lo[qi] = m + 1;
        }
    }
    vector<int> ans(qn);
    for (int i = 0; i < qn; ++i)
        ans[qs[i].idx] = (hi[i] > m ? -1 : hi[i]);
    return ans;
}
} // namespace pbs
```

---

## 6. Recognition Trigger Signals & Heuristics

- “When does query \(i\) become true?” as edges/updates arrive in order
- \(q\) binary searches each needing a DSU/Fenwick rebuilt from scratch → TLE, but offline batching works
- Classic: for each query pair \((u,v)\), earliest edge index connecting them (DSU + PBS)
- Statement has time-ordered updates + monotone reachability / threshold

---

## 7. Contest WA / TLE / RE Traps

- Off-by-one in `lo`/`hi` invariant (answer space empty)
- Reusing DSU without rebuilding each round
- Bucketing by mid but scanning updates in wrong order
- Not enough iterations when `hi-lo` large

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

- PBS on value threshold with Fenwick (e.g. k-th addition)
- Whole-binary-search space is 2D → still \(\log\) rounds
- Replace DSU with rollback DSU if mid-order is tree-shaped (alt: segtree on time)

---

## 11. Typical Problem Archetypes

1. Standard application: earliest time two cities connect
2. Slightly disguised: minimum maximum edge on path for many queries (Kruskal + PBS / reconstruction tree)
3. Difficult: PBS where check is a flow / matching
4. Very difficult / advanced: nested PBS

---

## 12. Recognition & Identification Drills

1. Edges arrive online; for each query \((u,v)\) output the first time they share a component.
2. You binary search the median of a subarray for \(q\) queries with a shared rebuild — batch?
3. Persistent DSU vs PBS for earliest connect — tradeoffs?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: many monotone binary searches sharing one event timeline
- Key invariant: each round, one scan answers all mid checks
- Key formula: \(O((U\cdot F+q)\log)\)
- Complexity: \(\log\) rounds × linear scan
- Template to remember: `lo/hi` arrays + `bucket[mid]` + rebuild DS

---

## 10. Coordinate compression

---
