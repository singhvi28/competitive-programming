# Monte Carlo vs Las Vegas

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** conceptual (labels appear 1800+) | **Frequency:** Occasional  
> **Prerequisites:** Randomized algorithms vocabulary  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: conceptual (labels appear 1800+)
- Prerequisites: Randomized algorithms vocabulary

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

Two different contracts with randomness:
- **Monte Carlo:** runtime bounded (often deterministic); answer may be wrong with small probability. Example: Freivalds, Miller–Rabin (primality), many hash equality checks if you accept tiny collision risk.
- **Las Vegas:** answer always correct; running time is a random variable. Example: randomized quicksort, randomized incremental constructions that retry until success, rejection sampling until a valid witness.

In contests you almost always want **Las Vegas** for final answers (or Monte Carlo with astronomically small error via double hashing / enough Miller–Rabin rounds so that WA is negligible).

---

## 4. Proof Sketches & Recurrences

If one Monte Carlo trial errs with \(\varepsilon\), \(k\) independent trials (AND for “all say yes”, OR for “exists yes” depending on one-sided error) give \(\varepsilon^k\) or similar.
Las Vegas expected time \(E[T]\); Markov: \(\Pr[T > c\,E[T]] \le 1/c\) — useful for timeout risk analysis.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: MC = fixed \(k\) trials; LV = expected trials \(\times\) cost
- Total: as above
- Memory: \(O(1)\) extra for the wrapper`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace mclv {
mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

// Monte Carlo: probably-correct predicate (one-sided: false => definitely false)
bool monte_carlo_probably_true(function<bool()> trial, int rounds) {
    for (int i = 0; i < rounds; ++i)
        if (!trial()) return false; // caught a counterexample
    return true; // probably true
}

// Las Vegas: always-correct; retry until constructive witness
int las_vegas_find(function<optional<int>()> attempt) {
    while (true) {
        if (auto v = attempt()) return *v;
    }
}
} // namespace mclv
```

### Python 3 Template

```python
# Python impractical as a standalone contest technique here.
# Useful: name the contract (MC vs LV) before coding.
```

---

## 6. Recognition Trigger Signals & Heuristics

- Statement/editorial: “probability of error \(< 10^{-9}\)” → Monte Carlo OK
- “Expected time” with guaranteed correctness → Las Vegas
- You can verify a candidate cheaply → convert MC → LV by retry until verify passes

---

## 7. Contest WA / TLE / RE Traps

- Calling a Las Vegas loop without a progress guarantee → infinite loop
- Too few Miller–Rabin / Freivalds rounds on adversarial data
- Treating hash collisions as impossible (they are MC equality tests)

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

- **One-sided vs two-sided error** Monte Carlo
- **Atlantic City** algorithms (rarely named in CP)
- Convert MC → LV when a deterministic verifier exists

---

## 11. Typical Problem Archetypes

1. Standard application: Miller–Rabin primality (MC, tiny error)
2. Slightly disguised: hash-based equality accepted as answer (MC)
3. Difficult: randomized matching algorithms with verification
4. Very difficult / advanced: algebraic identity testing pipelines

---

## 12. Recognition & Identification Drills

1. Algorithm always returns a correct MST but randomly permutes edges first — MC or LV?
2. Primality test that may call composites prime with prob \(2^{-40}\) — MC or LV?
3. You sample random subsets until a feasible solution appears, then return it — MC or LV?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: label your algorithm’s contract before submitting
- Key invariant: MC = maybe wrong; LV = maybe slow
- Key formula: error \(\varepsilon^k\) after \(k\) independent trials (one-sided)
- Complexity: fixed vs expected
- Template to remember: verify ⇒ turn MC into LV

---

## 5. Meet-in-the-middle

---
