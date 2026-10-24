# 2. Randomized algorithms

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Probability basics, hashing, quickselect / shuffle intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Probability basics, hashing, quickselect / shuffle intuition

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

Randomness buys **simplicity** and sometimes **better expected complexity** when deterministic alternatives are heavy (derandomized constructions, worst-case adversarial order). In CP, “randomized algorithm” usually means: random shuffle to avoid worst case, random sampling / fingerprints, randomized incremental construction, or Monte Carlo identity testing — not ML. Always know whether you need **always-correct** (Las Vegas) or **probably-correct** (Monte Carlo).

---

## 4. Proof Sketches & Recurrences

Example — randomized quickselect: random pivot ⇒ expected \(T(n) = O(n)\).
Example — Freivalds’ matrix check: pick random \(r \in \{0,1\}^n\), compare \(A(Br)\) vs \(Cr\); error \(\le 1/2\) per trial.
Amplification: \(k\) independent trials → error \(\le 2^{-k}\).
Shuffle: `std::shuffle` with `mt19937_64` kills many “sorted input” traps.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: often \(O(1)\) seed
- Per-query / per-operation: depends (Freivalds \(O(n^2)\) per trial vs \(O(n^3)\) multiply)
- Total: expected or w.h.p. bounds as designed
- Memory: usually \(O(n)\) extra for vectors/perms`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace randalgo {
mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

void shuffle_vec(vector<int>& a) {
    shuffle(a.begin(), a.end(), rng);
}

// Freivalds: check A*B == C for n x n matrices over mod P (or 64-bit)
bool freivalds(const vector<vector<long long>>& A,
               const vector<vector<long long>>& B,
               const vector<vector<long long>>& C,
               long long MOD, int trials = 3) {
    int n = (int)A.size();
    uniform_int_distribution<int> bit(0, 1);
    for (int t = 0; t < trials; ++t) {
        vector<long long> r(n), Br(n), ABr(n), Cr(n);
        for (int i = 0; i < n; ++i) r[i] = bit(rng);
        for (int i = 0; i < n; ++i) {
            __int128 sum = 0;
            for (int j = 0; j < n; ++j) sum += (__int128)B[i][j] * r[j];
            Br[i] = (long long)(sum % MOD);
        }
        for (int i = 0; i < n; ++i) {
            __int128 sum = 0;
            for (int j = 0; j < n; ++j) sum += (__int128)A[i][j] * Br[j];
            ABr[i] = (long long)(sum % MOD);
        }
        for (int i = 0; i < n; ++i) {
            __int128 sum = 0;
            for (int j = 0; j < n; ++j) sum += (__int128)C[i][j] * r[j];
            Cr[i] = (long long)(sum % MOD);
        }
        if (ABr != Cr) return false;
    }
    return true; // probably equal
}
} // namespace randalgo
```

### Python 3 Template

```python
import random
def shuffle_inplace(a):
    random.shuffle(a)
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Expected \(O(n)\)” / “with high probability”
- Adversarial order breaks deterministic pivot / hash table ordering
- Need a random spanning structure, random permutation, or random point in a polytope-like search
- Fingerprinting: verify polynomial / matrix identities quickly

---

## 7. Contest WA / TLE / RE Traps

- Using Monte Carlo where WA on rare cases fails system tests (need more trials / Las Vegas)
- Seeding with `time(0)` second granularity → identical seeds in hacks
- Assuming `rand() % n` is uniform (bias); use `uniform_int_distribution`
- Forgetting to amplify probability

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

- Random incremental convex hull / Delaunay (geometry)
- Randomized binary search on interactive problems
- Color coding (random coloring + DP) for paths of length \(k\)
- Hashing as the default CP randomized tool (see §1)

---

## 11. Typical Problem Archetypes

1. Standard application: shuffle then greedy / scan to avoid worst case
2. Slightly disguised: fingerprint two large structures instead of full compare
3. Difficult: color coding / randomized selection of a hidden subset
4. Very difficult / advanced: randomized algebraic algorithms (Schwartz–Zippel counting)

---

## 12. Recognition & Identification Drills

1. Verify whether \(C = AB\) for \(n=2000\) faster than cubic multiply.
2. An interactive problem asks you to find a hidden index; random sampling reduces queries in expectation.
3. Count simple paths of length \(k\le 10\) in a graph with randomized coloring DP.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: when deterministic worst-case is ugly but random order/fingerprint works
- Key invariant: state expected complexity or error probability explicitly
- Key formula: amplify \(\varepsilon\) by \(O(\log(1/\delta))\) trials
- Complexity: problem-specific; quote expected / w.h.p.
- Template to remember: `mt19937_64` + `shuffle` / Freivalds vector trick

---


## 3. Randomized data structures (Implicit Treaps etc.)

---
