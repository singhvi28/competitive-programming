# Randomized hashing

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** Modular arithmetic, rolling hash / polynomial hash idea, basic probability  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: Modular arithmetic, rolling hash / polynomial hash idea, basic probability

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

A hash is a random projection from a huge space (strings, sets, trees) into a small field. With a **fixed** base and mod, an adversary (or anti-hash tests) can force collisions. With **random** bases (and preferably two independent mods / 64-bit splitmix), the probability that a specific wrong pair collides is \(\approx 1/M\) (or \(1/2^{64}\)); union-bound over the number of “dangerous comparisons” you make. Contests care about **hygiene**: randomize once per run, use two hashes or a strong 64-bit mixer, and never treat a single 32-bit mod as cryptographic truth.

---

## 4. Proof Sketches & Recurrences

Polynomial rolling hash: \(H(s) = \sum_i s_i B^i \pmod M\).
Collision of two distinct length-\(\le L\) strings: at most \(L\) roots of a nonzero polynomial of degree \(< L\), so if \(B\) random in a field of size \(M\), \(\Pr[\text{collide}] \le L/M\) for one pair (Schwartz–Zippel style intuition).
For \(Q\) equality tests, union bound \(\le QL/M\). Two independent hashes: square the probability.
Prefer \(M\) prime near \(10^9\), or use `uint64_t` with overflow + random odd base (not a field — still empirically strong if mixed; safer: double mod).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: \(O(1)\) substring hash
- Total: \(O(n + q)\) for \(q\) comparisons
- Memory: \(O(n)\)`

### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace rhash {
mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

struct Hasher {
    static constexpr uint64_t MOD1 = 1000000007ULL;
    static constexpr uint64_t MOD2 = 1000000009ULL;
    uint64_t B1, B2;
    vector<uint64_t> p1, p2, h1, h2;

    Hasher() {
        B1 = uniform_int_distribution<uint64_t>(256, MOD1 - 1)(rng);
        B2 = uniform_int_distribution<uint64_t>(256, MOD2 - 1)(rng);
    }

    void build(const string& s) {
        int n = (int)s.size();
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        for (int i = 0; i < n; ++i) {
            p1[i + 1] = p1[i] * B1 % MOD1;
            p2[i + 1] = p2[i] * B2 % MOD2;
            h1[i + 1] = (h1[i] * B1 + (unsigned char)s[i] + 1) % MOD1;
            h2[i + 1] = (h2[i] * B2 + (unsigned char)s[i] + 1) % MOD2;
        }
    }

    // substring s[l..r) as pair
    pair<uint64_t, uint64_t> get(int l, int r) const {
        uint64_t x1 = (h1[r] + MOD1 - h1[l] * p1[r - l] % MOD1) % MOD1;
        uint64_t x2 = (h2[r] + MOD2 - h2[l] * p2[r - l] % MOD2) % MOD2;
        return {x1, x2};
    }
};
} // namespace rhash
```

### Python 3 Template

```python
import random
MOD1, MOD2 = 10**9 + 7, 10**9 + 9
B1 = random.randrange(256, MOD1)
B2 = random.randrange(256, MOD2)

def build(s: str):
    n = len(s)
    p1 = [1] * (n + 1); p2 = [1] * (n + 1)
    h1 = [0] * (n + 1); h2 = [0] * (n + 1)
    for i, ch in enumerate(s):
        p1[i + 1] = p1[i] * B1 % MOD1
        p2[i + 1] = p2[i] * B2 % MOD2
        h1[i + 1] = (h1[i] * B1 + ord(ch) + 1) % MOD1
        h2[i + 1] = (h2[i] * B2 + ord(ch) + 1) % MOD2
    return p1, p2, h1, h2

def get(p1, p2, h1, h2, l, r):
    x1 = (h1[r] - h1[l] * p1[r - l]) % MOD1
    x2 = (h2[r] - h2[l] * p2[r - l]) % MOD2
    return x1, x2
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Check if two substrings / paths / multisets are equal” without needing lexicographic order
- Need unordered dictionary keyed by strings/sequences under TL pressure
- Editorial mentions “hash the tree / bracket sequence / Euler tour”
- Anti-hash or “hack” culture on CF → you need random bases

---

## 7. Contest WA / TLE / RE Traps

- Fixed bases `31/53` + single mod \(10^9+7\) → hacks / WA on anti-hash
- Forgetting `+1` so null characters / zeros collide with empty prefixes
- Mixing 0-index / 1-index in `get(l,r)`
- Using `rand()` without seeding from chrono; same seed every run on some judges
- Comparing hashes of different lengths without encoding length (usually OK for equality of full strings; dangerous for unordered multiset hashes without sorting)

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

- **64-bit only:** random odd base, unsigned overflow; optionally splitmix64 finalizer
- **Hash of set:** XOR of `splitmix(x ^ salt)` (order-independent; watch multiplicities)
- **Tree hash:** rooted tree → hash of sorted child hashes + random seed per depth
- **Double vs single:** always prefer double on CF unless 64-bit mixer is trusted

---

## 11. Typical Problem Archetypes

1. Standard application: count distinct substrings via set of hashes
2. Slightly disguised: compare paths in a tree via hash + binary lifting
3. Difficult: largest common substring of many strings (binary search length + hash set)
4. Very difficult / advanced: hash of dynamic strings (treap of hashes) / isomorphism with rooted hashes

---

## 12. Recognition & Identification Drills

1. Given two strings, answer \(q\) queries: are substrings \(s[l_1..r_1]\) and \(t[l_2..r_2]\) equal?
2. Count the number of distinct cyclic shifts of a string.
3. You have \(n\) rooted trees (\(n\sum |V| \le 2\cdot 10^5\)); count isomorphism classes.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: equality / dictionary on strings or structured objects when SA/SAM is overkill
- Key invariant: same content ⇒ same hash; different ⇒ collision w.p. \(\approx 1/M^k\)
- Key formula: \(H[l,r) = H[r] - H[l]\cdot B^{r-l}\)
- Complexity: \(O(n)\) prep, \(O(1)\) get
- Template to remember: random \(B\), two mods, prefix powers

---

## 2. Randomized algorithms

---
