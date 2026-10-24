# 5. Meet-in-the-middle

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** Bitmask enumeration, sorting / hashing, knapsack intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Bitmask enumeration, sorting / hashing, knapsack intuition

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

When \(n\) is too large for \(2^n\) but \(n/2\) is fine (\(n \approx 40\)), split the instance into two halves, enumerate all states on each half (\(2^{n/2}\)), then **combine** with sort + two pointers, binary search, or a hash map. The art is designing the half-state so the combination condition is a simple equality / inequality on a few integers.

---

## 4. Proof Sketches & Recurrences

Naive: \(O(2^n)\).
Split: \(L = \lfloor n/2\rfloor\), \(R = n-L\). Enumerate \(2^L + 2^R\) subsets.
Combine sorted lists: \(O(2^{n/2}\log)\) or \(O(2^{n/2})\) two pointers.
Memory: store one half fully \(O(2^{n/2})\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build half lists \(O(2^{n/2}\cdot n)\) or \(O(2^{n/2})\) incremental
- Per-query / per-operation: usually one-shot solve
- Total: \(O(2^{n/2} n)\) or \(O(2^{n/2}\log)\) with sort
- Memory: \(O(2^{n/2})\)`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace mitm {
// Subset sums of a[l..r)
vector<long long> subset_sums(const vector<long long>& a, int l, int r) {
    int m = r - l;
    vector<long long> s(1 << m);
    for (int mask = 0; mask < (1 << m); ++mask) {
        long long sum = 0;
        for (int i = 0; i < m; ++i)
            if (mask & (1 << i)) sum += a[l + i];
        s[mask] = sum;
    }
    return s;
}

// number of subsets with sum == target
long long count_sum(const vector<long long>& a, long long target) {
    int n = (int)a.size();
    int mid = n / 2;
    auto left = subset_sums(a, 0, mid);
    auto right = subset_sums(a, mid, n);
    sort(left.begin(), left.end());
    sort(right.begin(), right.end());
    long long ans = 0;
    int j = (int)right.size() - 1;
    // for each L, count R with L+R == target
    for (long long x : left) {
        long long need = target - x;
        auto lo = lower_bound(right.begin(), right.end(), need);
        auto hi = upper_bound(right.begin(), right.end(), need);
        ans += hi - lo;
    }
    return ans;
}
} // namespace mitm
```

### Python 3 Template

```python
from bisect import bisect_left, bisect_right

def subset_sums(a):
    m = len(a)
    s = [0] * (1 << m)
    for mask in range(1 << m):
        total = 0
        for i in range(m):
            if mask >> i & 1:
                total += a[i]
        s[mask] = total
    return s

def count_sum(a, target):
    mid = len(a) // 2
    left = sorted(subset_sums(a[:mid]))
    right = sorted(subset_sums(a[mid:]))
    ans = 0
    for x in left:
        need = target - x
        ans += bisect_right(right, need) - bisect_left(right, need)
    return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- \(n \le 40\), \(w_i\) weights, target sum / XOR / product constraints
- “Choose a subset with property P” where P factors across halves
- BSGS (baby-step giant-step) for discrete log — MITM in a group
- \(4^{n/2}\) style for more complex local choices (two options per item → still split)

---

## 7. Contest WA / TLE / RE Traps

- Forgetting empty subset (sum 0)
- Overflow on sums — use `__int128` / check constraints
- Storing both halves with heavy payloads → MLE; store one half, stream the other
- Wrong split when items are not free subsets (need DP half-states)

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

- **MITM + knapsack DP** on each half when values are larger but count of items is small
- **3-way split** rare; usually two
- **BSGS:** baby steps table, giant steps query
- **XOR MITM:** map from XOR value to mask

---

## 11. Typical Problem Archetypes

1. Standard application: subset sum count for \(n=40\)
2. Slightly disguised: closest sum to target (minimum \(|L+R-T|\))
3. Difficult: MITM on pairs of constraints (sum + XOR)
4. Very difficult / advanced: MITM on tree path / diameter-like splits

---

## 12. Recognition & Identification Drills

1. \(n=40\) integers; how many subsets have sum in \([L,R]\)?
2. Given \(a_1..a_{36}\), find a nonempty subset with XOR \(=0\) or report none.
3. String of length 40 over a small alphabet; count ways to split into two subsequences with equal sums of values.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: \(n\sim 40\), exponential in \(n/2\) fits
- Key invariant: every full configuration = left config ⊕ right config
- Key formula: time \(\Theta(2^{n/2}\mathrm{polylog})\)
- Complexity: memory \(\Theta(2^{n/2})\)
- Template to remember: enum left, sort, enum right + `lower_bound`

---

## 6. Offline query processing

---
