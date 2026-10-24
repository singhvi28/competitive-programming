# Section §18: Randomization & Meta-Techniques

> **Module ID:** `sec-18`  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Topic Count:** 10  

**Module Summary:** Meet-in-the-Middle 2^(N/2), Randomized 64-bit splitmix hashing hygiene, Offline query processing, Parallel Binary Search, and Tree Mo's algorithm.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Randomized hashing](#topic-1) | `S-tier` | 1500–2200 | Common | [01-18-randomized-hashing.md](./01-18-randomized-hashing.md) |
| 2 | [Randomized algorithms](#topic-2) | `B-tier` | 1800–2500 | Occasional | [02-18-randomized-algorithms.md](./02-18-randomized-algorithms.md) |
| 3 | [Implicit Treaps and Randomized BSTs](#topic-3) | `B-tier` | 1900–2600 | Occasional | [03-18-implicit-treaps-and-randomized-bsts.md](./03-18-implicit-treaps-and-randomized-bsts.md) |
| 4 | [Monte Carlo vs Las Vegas](#topic-4) | `B-tier` | conceptual (labels appear 1800+) | Occasional | [04-18-monte-carlo-vs-las-vegas.md](./04-18-monte-carlo-vs-las-vegas.md) |
| 5 | [Meet-in-the-middle](#topic-5) | `A-tier` | 1700–2400 | Occasional | [05-18-meet-in-the-middle.md](./05-18-meet-in-the-middle.md) |
| 6 | [Offline query processing](#topic-6) | `S-tier` | 1700–2400 | Common | [06-18-offline-query-processing.md](./06-18-offline-query-processing.md) |
| 7 | [Parallel binary search](#topic-7) | `B-tier` | 2100–2700 | Occasional | [07-18-parallel-binary-search.md](./07-18-parallel-binary-search.md) |
| 8 | [Coordinate compression](#topic-8) | `S-tier` | 1400–2000 | Very Common | [08-18-coordinate-compression.md](./08-18-coordinate-compression.md) |
| 9 | [Sweep-line patterns](#topic-9) | `A-tier` | 1800–2500 | Occasional | [09-18-sweep-line-patterns.md](./09-18-sweep-line-patterns.md) |
| 10 | [Mo vs segment tree (drill this distinction)](#topic-10) | `B-tier` | 1600–2200 | Common | [10-18-mo-vs-segment-tree-drill-this-distinction.md](./10-18-mo-vs-segment-tree-drill-this-distinction.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Randomized hashing

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** Modular arithmetic, rolling hash / polynomial hash idea, basic probability  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: Modular arithmetic, rolling hash / polynomial hash idea, basic probability

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

A hash is a random projection from a huge space (strings, sets, trees) into a small field. With a **fixed** base and mod, an adversary (or anti-hash tests) can force collisions. With **random** bases (and preferably two independent mods / 64-bit splitmix), the probability that a specific wrong pair collides is \(\approx 1/M\) (or \(1/2^{64}\)); union-bound over the number of “dangerous comparisons” you make. Contests care about **hygiene**: randomize once per run, use two hashes or a strong 64-bit mixer, and never treat a single 32-bit mod as cryptographic truth.

---

#### 4. Proof Sketches & Recurrences

Polynomial rolling hash: \(H(s) = \sum_i s_i B^i \pmod M\).
Collision of two distinct length-\(\le L\) strings: at most \(L\) roots of a nonzero polynomial of degree \(< L\), so if \(B\) random in a field of size \(M\), \(\Pr[\text{collide}] \le L/M\) for one pair (Schwartz–Zippel style intuition).
For \(Q\) equality tests, union bound \(\le QL/M\). Two independent hashes: square the probability.
Prefer \(M\) prime near \(10^9\), or use `uint64_t` with overflow + random odd base (not a field — still empirically strong if mixed; safer: double mod).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: \(O(1)\) substring hash
- Total: \(O(n + q)\) for \(q\) comparisons
- Memory: \(O(n)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Check if two substrings / paths / multisets are equal” without needing lexicographic order
- Need unordered dictionary keyed by strings/sequences under TL pressure
- Editorial mentions “hash the tree / bracket sequence / Euler tour”
- Anti-hash or “hack” culture on CF → you need random bases

---

#### 7. Contest WA / TLE / RE Traps

- Fixed bases `31/53` + single mod \(10^9+7\) → hacks / WA on anti-hash
- Forgetting `+1` so null characters / zeros collide with empty prefixes
- Mixing 0-index / 1-index in `get(l,r)`
- Using `rand()` without seeding from chrono; same seed every run on some judges
- Comparing hashes of different lengths without encoding length (usually OK for equality of full strings; dangerous for unordered multiset hashes without sorting)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **64-bit only:** random odd base, unsigned overflow; optionally splitmix64 finalizer
- **Hash of set:** XOR of `splitmix(x ^ salt)` (order-independent; watch multiplicities)
- **Tree hash:** rooted tree → hash of sorted child hashes + random seed per depth
- **Double vs single:** always prefer double on CF unless 64-bit mixer is trusted

---

#### 11. Typical Problem Archetypes

1. Standard application: count distinct substrings via set of hashes
2. Slightly disguised: compare paths in a tree via hash + binary lifting
3. Difficult: largest common substring of many strings (binary search length + hash set)
4. Very difficult / advanced: hash of dynamic strings (treap of hashes) / isomorphism with rooted hashes

---

#### 12. Recognition & Identification Drills

1. Given two strings, answer \(q\) queries: are substrings \(s[l_1..r_1]\) and \(t[l_2..r_2]\) equal?
2. Count the number of distinct cyclic shifts of a string.
3. You have \(n\) rooted trees (\(n\sum |V| \le 2\cdot 10^5\)); count isomorphism classes.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: equality / dictionary on strings or structured objects when SA/SAM is overkill
- Key invariant: same content ⇒ same hash; different ⇒ collision w.p. \(\approx 1/M^k\)
- Key formula: \(H[l,r) = H[r] - H[l]\cdot B^{r-l}\)
- Complexity: \(O(n)\) prep, \(O(1)\) get
- Template to remember: random \(B\), two mods, prefix powers

---

## 2. Randomized algorithms

---


---

<a id="topic-2"></a>
### 2. Randomized algorithms

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Probability basics, hashing, quickselect / shuffle intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Probability basics, hashing, quickselect / shuffle intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Randomness buys **simplicity** and sometimes **better expected complexity** when deterministic alternatives are heavy (derandomized constructions, worst-case adversarial order). In CP, “randomized algorithm” usually means: random shuffle to avoid worst case, random sampling / fingerprints, randomized incremental construction, or Monte Carlo identity testing — not ML. Always know whether you need **always-correct** (Las Vegas) or **probably-correct** (Monte Carlo).

---

#### 4. Proof Sketches & Recurrences

Example — randomized quickselect: random pivot ⇒ expected \(T(n) = O(n)\).
Example — Freivalds’ matrix check: pick random \(r \in \{0,1\}^n\), compare \(A(Br)\) vs \(Cr\); error \(\le 1/2\) per trial.
Amplification: \(k\) independent trials → error \(\le 2^{-k}\).
Shuffle: `std::shuffle` with `mt19937_64` kills many “sorted input” traps.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: often \(O(1)\) seed
- Per-query / per-operation: depends (Freivalds \(O(n^2)\) per trial vs \(O(n^3)\) multiply)
- Total: expected or w.h.p. bounds as designed
- Memory: usually \(O(n)\) extra for vectors/perms`

##### C++17 Template

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

##### Python 3 Template

```python
import random
def shuffle_inplace(a):
    random.shuffle(a)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Expected \(O(n)\)” / “with high probability”
- Adversarial order breaks deterministic pivot / hash table ordering
- Need a random spanning structure, random permutation, or random point in a polytope-like search
- Fingerprinting: verify polynomial / matrix identities quickly

---

#### 7. Contest WA / TLE / RE Traps

- Using Monte Carlo where WA on rare cases fails system tests (need more trials / Las Vegas)
- Seeding with `time(0)` second granularity → identical seeds in hacks
- Assuming `rand() % n` is uniform (bias); use `uniform_int_distribution`
- Forgetting to amplify probability

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Random incremental convex hull / Delaunay (geometry)
- Randomized binary search on interactive problems
- Color coding (random coloring + DP) for paths of length \(k\)
- Hashing as the default CP randomized tool (see §1)

---

#### 11. Typical Problem Archetypes

1. Standard application: shuffle then greedy / scan to avoid worst case
2. Slightly disguised: fingerprint two large structures instead of full compare
3. Difficult: color coding / randomized selection of a hidden subset
4. Very difficult / advanced: randomized algebraic algorithms (Schwartz–Zippel counting)

---

#### 12. Recognition & Identification Drills

1. Verify whether \(C = AB\) for \(n=2000\) faster than cubic multiply.
2. An interactive problem asks you to find a hidden index; random sampling reduces queries in expectation.
3. Count simple paths of length \(k\le 10\) in a graph with randomized coloring DP.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: when deterministic worst-case is ugly but random order/fingerprint works
- Key invariant: state expected complexity or error probability explicitly
- Key formula: amplify \(\varepsilon\) by \(O(\log(1/\delta))\) trials
- Complexity: problem-specific; quote expected / w.h.p.
- Template to remember: `mt19937_64` + `shuffle` / Freivalds vector trick

---


## 3. Randomized data structures (Implicit Treaps etc.)

---


---

<a id="topic-3"></a>
### 3. Implicit Treaps and Randomized BSTs

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** BST, Expected Value, Random Priorities  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: BST, Expected Value, Random Priorities

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Some deterministic data structures (like AVL or Red-Black trees) are notoriously difficult to implement in a contest setting. By assigning **random priorities** to elements and maintaining heap properties (like in a **Treap**), we achieve $O(\log N)$ expected depth with much simpler code. 
- **Explicit Treaps** use the values as BST keys.
- **Implicit Treaps** (the contest favorite) use the *size of the left subtree* as the BST key. This effectively creates an array where you can split, merge, insert, delete, or reverse arbitrary segments in $O(\log N)$ time.
- **Skip Lists** are another alternative using coin flips to build layered linked lists, though Treaps are strictly preferred in CP.

---

#### 4. Proof Sketches & Recurrences

A node has `left`, `right`, `size`, `val`, `priority`.
- `split(node, k)`: Divides the implicit treap into two treaps (first $k$ elements, and the rest).
- `merge(left, right)`: Combines two treaps (assuming `left` comes before `right` in array order), using the highest random priority to decide the new root.
Every query (like reversing) is just a `split` to extract the segment, lazily flipping it, and then two `merge`s to put it back.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// (See Section 05b for the full Implicit Treap implementation)
// Key mechanism for randomness:
mt19937 rng(1337);
struct Node {
    int val, pri, sz;
    bool rev;
    Node *l, *r;
    Node(int v) : val(v), pri(rng()), sz(1), rev(false), l(nullptr), r(nullptr) {}
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Operations like: "Reverse subarray $A[L \dots R]$", "Move subarray $A[L \dots R]$ to the front".
- "Insert element at index $K$" followed by range queries.
- These operations break Segment Trees because the underlying array structure fundamentally changes. An Implicit Treap is required.

---

#### 7. Contest WA / TLE / RE Traps

- Missing `push(t)` before accessing children: if lazy tags are not propagated before recursing down in `split` or `merge`, tree structure becomes corrupted.
- Weak random number generator: using `rand()` (which often has RAND_MAX = 32767) causes priority collisions and tree degeneration to $\mathcal{O}(N)$; always use `mt19937`.
- Memory leaks in competitive programming: allocate nodes from a static pool array `Node pool[MAXN]` rather than repeated `new Node()` to avoid allocator overhead and heap fragmentation.
- Forgetting `pull(t)` after modifying child pointers, causing incorrect subtree sizes and wrong index calculations.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---


---

<a id="topic-4"></a>
### 4. Monte Carlo vs Las Vegas

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** conceptual (labels appear 1800+) | **Frequency:** Occasional  
> **Prerequisites:** Randomized algorithms vocabulary  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: conceptual (labels appear 1800+)
- Prerequisites: Randomized algorithms vocabulary

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Two different contracts with randomness:
- **Monte Carlo:** runtime bounded (often deterministic); answer may be wrong with small probability. Example: Freivalds, Miller–Rabin (primality), many hash equality checks if you accept tiny collision risk.
- **Las Vegas:** answer always correct; running time is a random variable. Example: randomized quicksort, randomized incremental constructions that retry until success, rejection sampling until a valid witness.

In contests you almost always want **Las Vegas** for final answers (or Monte Carlo with astronomically small error via double hashing / enough Miller–Rabin rounds so that WA is negligible).

---

#### 4. Proof Sketches & Recurrences

If one Monte Carlo trial errs with \(\varepsilon\), \(k\) independent trials (AND for “all say yes”, OR for “exists yes” depending on one-sided error) give \(\varepsilon^k\) or similar.
Las Vegas expected time \(E[T]\); Markov: \(\Pr[T > c\,E[T]] \le 1/c\) — useful for timeout risk analysis.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: MC = fixed \(k\) trials; LV = expected trials \(\times\) cost
- Total: as above
- Memory: \(O(1)\) extra for the wrapper`

##### C++17 Template

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

##### Python 3 Template

```python
# Python impractical as a standalone contest technique here.
# Useful: name the contract (MC vs LV) before coding.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Statement/editorial: “probability of error \(< 10^{-9}\)” → Monte Carlo OK
- “Expected time” with guaranteed correctness → Las Vegas
- You can verify a candidate cheaply → convert MC → LV by retry until verify passes

---

#### 7. Contest WA / TLE / RE Traps

- Calling a Las Vegas loop without a progress guarantee → infinite loop
- Too few Miller–Rabin / Freivalds rounds on adversarial data
- Treating hash collisions as impossible (they are MC equality tests)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **One-sided vs two-sided error** Monte Carlo
- **Atlantic City** algorithms (rarely named in CP)
- Convert MC → LV when a deterministic verifier exists

---

#### 11. Typical Problem Archetypes

1. Standard application: Miller–Rabin primality (MC, tiny error)
2. Slightly disguised: hash-based equality accepted as answer (MC)
3. Difficult: randomized matching algorithms with verification
4. Very difficult / advanced: algebraic identity testing pipelines

---

#### 12. Recognition & Identification Drills

1. Algorithm always returns a correct MST but randomly permutes edges first — MC or LV?
2. Primality test that may call composites prime with prob \(2^{-40}\) — MC or LV?
3. You sample random subsets until a feasible solution appears, then return it — MC or LV?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: label your algorithm’s contract before submitting
- Key invariant: MC = maybe wrong; LV = maybe slow
- Key formula: error \(\varepsilon^k\) after \(k\) independent trials (one-sided)
- Complexity: fixed vs expected
- Template to remember: verify ⇒ turn MC into LV

---

## 5. Meet-in-the-middle

---


---

<a id="topic-5"></a>
### 5. Meet-in-the-middle

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** Bitmask enumeration, sorting / hashing, knapsack intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Bitmask enumeration, sorting / hashing, knapsack intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

When \(n\) is too large for \(2^n\) but \(n/2\) is fine (\(n \approx 40\)), split the instance into two halves, enumerate all states on each half (\(2^{n/2}\)), then **combine** with sort + two pointers, binary search, or a hash map. The art is designing the half-state so the combination condition is a simple equality / inequality on a few integers.

---

#### 4. Proof Sketches & Recurrences

Naive: \(O(2^n)\).
Split: \(L = \lfloor n/2\rfloor\), \(R = n-L\). Enumerate \(2^L + 2^R\) subsets.
Combine sorted lists: \(O(2^{n/2}\log)\) or \(O(2^{n/2})\) two pointers.
Memory: store one half fully \(O(2^{n/2})\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build half lists \(O(2^{n/2}\cdot n)\) or \(O(2^{n/2})\) incremental
- Per-query / per-operation: usually one-shot solve
- Total: \(O(2^{n/2} n)\) or \(O(2^{n/2}\log)\) with sort
- Memory: \(O(2^{n/2})\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- \(n \le 40\), \(w_i\) weights, target sum / XOR / product constraints
- “Choose a subset with property P” where P factors across halves
- BSGS (baby-step giant-step) for discrete log — MITM in a group
- \(4^{n/2}\) style for more complex local choices (two options per item → still split)

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting empty subset (sum 0)
- Overflow on sums — use `__int128` / check constraints
- Storing both halves with heavy payloads → MLE; store one half, stream the other
- Wrong split when items are not free subsets (need DP half-states)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **MITM + knapsack DP** on each half when values are larger but count of items is small
- **3-way split** rare; usually two
- **BSGS:** baby steps table, giant steps query
- **XOR MITM:** map from XOR value to mask

---

#### 11. Typical Problem Archetypes

1. Standard application: subset sum count for \(n=40\)
2. Slightly disguised: closest sum to target (minimum \(|L+R-T|\))
3. Difficult: MITM on pairs of constraints (sum + XOR)
4. Very difficult / advanced: MITM on tree path / diameter-like splits

---

#### 12. Recognition & Identification Drills

1. \(n=40\) integers; how many subsets have sum in \([L,R]\)?
2. Given \(a_1..a_{36}\), find a nonempty subset with XOR \(=0\) or report none.
3. String of length 40 over a small alphabet; count ways to split into two subsequences with equal sums of values.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: \(n\sim 40\), exponential in \(n/2\) fits
- Key invariant: every full configuration = left config ⊕ right config
- Key formula: time \(\Theta(2^{n/2}\mathrm{polylog})\)
- Complexity: memory \(\Theta(2^{n/2})\)
- Template to remember: enum left, sort, enum right + `lower_bound`

---

## 6. Offline query processing

---


---

<a id="topic-6"></a>
### 6. Offline query processing

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1700–2400 | **Frequency:** Common  
> **Prerequisites:** Sorting, Fenwick/segtree, DSU optional, coordinate compression  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Sorting, Fenwick/segtree, DSU optional, coordinate compression

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

If **all queries are known before any answer is required**, you may reorder them, batch them, or sweep a pointer while maintaining a data structure. Offline is a *meta-technique*: the win is choosing an order where the DS only supports **easy transitions** (e.g. only increase \(r\), never decrease). Classic pattern: sort queries by \(r\); scan array left→right; answer when `i == query.r`. This often replaces Mo or persistent structures.

---

#### 4. Proof Sketches & Recurrences

Online: each query \(O(\mathrm{cost_{online}})\).
Offline sort by key: \(O((n+q)\log(n+q) + (n+q)\cdot F)\) where \(F\) is Fenwick op.
Example — distinct values in \([l,r]\): keep last position of each value in Fenwick (point +1 at last pos, -1 at previous); sort queries by \(r\); when advancing \(r\), update last occurrence; query sum on \([l,r]\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: sort queries \(O(q\log q)\); map values if needed
- Per-query / per-operation: amortized \(O(F)\) as pointer advances
- Total: \(O((n+q)\log n)\) typical with Fenwick
- Memory: \(O(n+q)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “\(q\) queries on a static array” and answers independent
- Queries ask something monotone in an endpoint
- “Last time value \(x\) appeared”, distinct in prefix, invert queries
- Updates and queries mixed but **all given up front** → process by time with segtree-on-time / DSU rollback (see §02)
- You catch yourself wanting persistence only to go “back in time” for known queries

---

#### 7. Contest WA / TLE / RE Traps

- Answering in sorted order but forgetting to write `ans[idx]`
- Advancing \(r\) past `q.r` incorrectly (off-by-one)
- Using offline when queries are adaptive/interactive
- Heavy `unordered_map` without reserve → TLE; compress values first

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Sort by \(l\) decreasing while maintaining a structure on suffixes
- CDQ divide-and-conquer (3D partial order) — offline + D&C
- Offline dynamic connectivity (segtree on time) — link §02
- Mo’s algorithm — offline with add/del both directions (§6)

---

#### 11. Typical Problem Archetypes

1. Standard application: distinct values in \([l,r]\)
2. Slightly disguised: for each query, mex of subarray (offline + segtree on last positions)
3. Difficult: queries insert/delete known offline → process chronologically with rollback DS
4. Very difficult / advanced: CDQ / multi-level offline

---

#### 12. Recognition & Identification Drills

1. \(q\) queries ask the sum of \(\mathrm{next}[i]\) for \(i\in[l,r]\) where \(\mathrm{next}\) depends only on prefixes of the array — can you avoid rebuilding?
2. Static array; for each query count pairs \((i,j)\) in range with \(a_i > a_j\) — offline inversion with Fenwick?
3. All updates and queries given; you need connectivity after each update — online DSU vs offline?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: all queries known; find a monotone order for a simple DS
- Key invariant: pointer only moves forward; answers stored by `idx`
- Key formula: sort by \(r\) + Fenwick last-occurrence → distinct count
- Complexity: \(O((n+q)\log n)\)
- Template to remember: `struct Query{l,r,idx}`; sort; expand; `ans[idx]=...`

---

---


---

<a id="topic-7"></a>
### 7. Parallel binary search

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Binary search on answer, offline queries, Fenwick/segtree/DSU  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Binary search on answer, offline queries, Fenwick/segtree/DSU

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

You have \(q\) independent problems of the form “binary search the earliest time / minimum \(x\) such that predicate \(P_i(x)\) holds,” and \(P_i\) is **monotone**, and checking \(P_i(\mathrm{mid})\) needs a heavy shared data structure that can be built by scanning events up to `mid`. Instead of \(q\) separate binary searches, keep an interval \([lo_i,hi_i]\) per query and process **all queries with the same mid** together in rounds (\(\log\) rounds). Each round: bucket queries by mid, scan the global timeline once, answer all mid-checks.

---

#### 4. Proof Sketches & Recurrences

Sequential: \(q \cdot \log X \cdot C\) if each check costs \(C\) from scratch.
PBS: \(\log X\) rounds; each round scans all updates once \(O(U\cdot F)\) and assigns checks to buckets \(O(q)\).
Total \(O((U\cdot F + q)\log X)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(\log\) rounds shared
- Total: \(O((m\alpha(n)+q)\log m)\) for connectivity example
- Memory: \(O(n+m+q)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “When does query \(i\) become true?” as edges/updates arrive in order
- \(q\) binary searches each needing a DSU/Fenwick rebuilt from scratch → TLE, but offline batching works
- Classic: for each query pair \((u,v)\), earliest edge index connecting them (DSU + PBS)
- Statement has time-ordered updates + monotone reachability / threshold

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one in `lo`/`hi` invariant (answer space empty)
- Reusing DSU without rebuilding each round
- Bucketing by mid but scanning updates in wrong order
- Not enough iterations when `hi-lo` large

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- PBS on value threshold with Fenwick (e.g. k-th addition)
- Whole-binary-search space is 2D → still \(\log\) rounds
- Replace DSU with rollback DSU if mid-order is tree-shaped (alt: segtree on time)

---

#### 11. Typical Problem Archetypes

1. Standard application: earliest time two cities connect
2. Slightly disguised: minimum maximum edge on path for many queries (Kruskal + PBS / reconstruction tree)
3. Difficult: PBS where check is a flow / matching
4. Very difficult / advanced: nested PBS

---

#### 12. Recognition & Identification Drills

1. Edges arrive online; for each query \((u,v)\) output the first time they share a component.
2. You binary search the median of a subarray for \(q\) queries with a shared rebuild — batch?
3. Persistent DSU vs PBS for earliest connect — tradeoffs?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: many monotone binary searches sharing one event timeline
- Key invariant: each round, one scan answers all mid checks
- Key formula: \(O((U\cdot F+q)\log)\)
- Complexity: \(\log\) rounds × linear scan
- Template to remember: `lo/hi` arrays + `bucket[mid]` + rebuild DS

---

## 10. Coordinate compression

---


---

<a id="topic-8"></a>
### 8. Coordinate compression

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Very Common  
> **Prerequisites:** Sorting, `lower_bound`, Fenwick/segtree indexing  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Sorting, `lower_bound`, Fenwick/segtree indexing

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Data structures want **dense ranks** \(1..k\), not raw values in \(\pm 10^9\). Collect every value that will ever appear as an index/key, sort-unique, replace each value by its rank. This is not optional garnish — it is how Fenwick/segtree/Mo frequency arrays become memory-feasible. Compress **exactly the set of coordinates you need** (endpoints, values, times); over-collecting is fine, under-collecting is WA.

---

#### 4. Proof Sketches & Recurrences

Let \(V\) be the multiset of relevant coordinates, \(k = |unique(V)|\).
Map \(x \mapsto \mathrm{rank}(x) \in [1,k]\) via sort + lower_bound.
Order-preserving: \(x < y \iff \mathrm{rank}(x) < \mathrm{rank}(y)\).
All range-of-value queries become range-of-rank queries.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) sort-unique
- Per-query / per-operation: \(O(\log n)\) per `id`
- Total: dominated by DS using ranks
- Memory: \(O(k)\) for the sorted vector`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Values up to \(10^9\) but \(n \le 2\cdot 10^5\)
- Fenwick/segtree indexed by value
- Offline geometry: \(x\)-coordinates of segments
- “Rank of \(a_i\) among unique values”

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to `add` a query-only coordinate before `build`
- Mixing 0-index ranks with 1-index Fenwick
- Compressing after some updates already applied
- Using `map<int,int>` instead of vector ranks → extra \(\log\) everywhere (OK but slower)
- Assuming ranks are values — they are not; don’t output ranks unless asked

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Compress pairs \((x,y)\) for 2D Fenwick (linearize carefully)
- Dynamic compression via `map` / policy BBST when values stream online
- Discrete for floats: sort unique with epsilon care (prefer integers)

---

#### 11. Typical Problem Archetypes

1. Standard application: inversion count with Fenwick
2. Slightly disguised: rectangle area union needs compressed \(y\) for sweep
3. Difficult: compress only “interesting” times for offline queries
4. Very difficult / advanced: online insertion of new coordinates into a dynamic segtree (no full compress)

---

#### 12. Recognition & Identification Drills

1. \(n=2\cdot 10^5\) values in \([1,10^{18}]\); count inversions.
2. Queries ask frequency of values \(\le x\) for arbitrary \(x\) not in \(a\) — what must you compress?
3. Sweep-line on segments with \(x\in[1,10^9]\) — array of size \(10^9\) or compress?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any value-indexed DS with huge universe, small \(n\)
- Key invariant: order-preserving bijection onto \(1..k\)
- Key formula: `sort + unique + lower_bound`
- Complexity: \(O(n\log n)\) build
- Template to remember: collect → `build` → `id(x)`

---

## 11. Sweep-line patterns

---


---

<a id="topic-9"></a>
### 9. Sweep-line patterns

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Coordinate compression, Fenwick/segtree, event sorting  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Coordinate compression, Fenwick/segtree, event sorting

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Sort geometric (or 1D) **events** by a sweep coordinate; maintain the active cross-section in a DS. Vertical line sweeps left→right: at each \(x\), process all events at that \(x\) (insert segment, delete segment, query stabbing). The same pattern is “sort endpoints + Fenwick” for intervals on a line. Sweep converts 2D problems into dynamic 1D problems.

---

#### 4. Proof Sketches & Recurrences

Sort \(E\) events: \(O(E\log E)\).
Each insert/delete/query into DS: \(O(F)\).
Total \(O(E\log E + E\cdot F)\).
For interval coverage on a line: events \(+1\) at \(L\), \(-1\) at \(R+1\); sweep prefix sum.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: compress + sort events \(O(E\log E)\)
- Per-query / per-operation: \(O(\log n)\) DS ops
- Total: \(O(E\log E)\)
- Memory: \(O(E + k)\)`

##### C++17 Template

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

##### Python 3 Template

```python
# Event = (x, type, y1, y2, idx); type 0 add, 1 query, 2 remove
# Same algorithm as C++; Fenwick on compressed y.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Rectangles / segments / intervals; ask intersections, union area, coverage
- “For each point, how many segments cover it?”
- Events: open, close, query — process opens before queries before closes at same \(x\) (tie-break carefully)
- Closest pair / line sweep with active set ordered by \(y\)

---

#### 7. Contest WA / TLE / RE Traps

- Wrong tie-break at equal \(x\) (query before add → miss; remove before query → miss)
- Off-by-one on closed/open segments (`x2+1` vs `x2`)
- Forgetting to compress all \(y\) from queries and segments
- Using `set` of active \(y\) when multiples needed → multiset / Fenwick freqs

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Union area of rectangles (sweep + segtree on coverage lengths)
- Closest pair sweep with active window of width \(d\)
- 1D interval sweep (difference array / events) — simplest form
- Angular sweep around a point

---

#### 11. Typical Problem Archetypes

1. Standard application: how many segments cover each query point
2. Slightly disguised: intersection count of horiz/vert segments
3. Difficult: rectangle union area
4. Very difficult / advanced: Bentley–Ottmann style general segment intersections

---

#### 12. Recognition & Identification Drills

1. \(n\) axis-parallel rectangles; compute union area.
2. \(n\) intervals on \(\mathbb{Z}\); for each query point, coverage count.
3. Closest pair of points in the plane — D&C vs sweep?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: geometry/intervals reduce to sorted events + 1D DS
- Key invariant: active set = all objects stabbed by the sweep line
- Key formula: sort events; fix ties by type order
- Complexity: \(O(E\log E)\)
- Template to remember: `Event{x,type,...}` + Fenwick/segtree on other axis

---

---


---

<a id="topic-10"></a>
### 10. Mo vs segment tree (drill this distinction)

> **Section:** §18 Randomization & Meta-Techniques  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Mo's Algorithm, Segment Trees

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Randomization and Meta-Techniques bypass worst-case complexity barriers and adversarial tests: Meet-in-the-Middle $\mathcal{O}(2^{N/2})$, 64-bit SplitMix Anti-Hash Hygiene, Parallel Binary Search, and Randomized Graph Contracting.

##### Fundamental Theorems & Invariants

- **Meet-in-the-Middle Principle:** Splitting a search space of size $2^N$ into two halves of size $2^{N/2}$, sorting the second half, and matching elements reduces complexity from $\mathcal{O}(2^N)$ to $\mathcal{O}(2^{N/2} N)$.
- **Parallel Binary Search Invariant:** When $Q$ independent offline queries each require binary searching an event timeline of length $M$, processing all $Q$ queries concurrently in $\mathcal{O}((N + Q) \log M)$ sweeps the event list only $\log M$ times.
- **SplitMix64 Hash Defense:** Standard `std::unordered_map` with identity hash is vulnerable to linear-time collision hacking ($\mathcal{O}(N^2)$); applying a randomized 64-bit integer permutation guarantees $\mathcal{O}(1)$ expected lookup against any adversary.

##### Algorithmic Execution Blueprint

1. **Meet-in-the-Middle:** Generate all subset sums of $A[0 \dots N/2-1]$ into vector $L$. Generate all subset sums of $A[N/2 \dots N-1]$ into vector $R$. Sort $R$, and for each $s \in L$, binary search in $R$ for target $- s$.
2. **Parallel Binary Search:** Maintain interval $[lo_i, hi_i]$ for each query. In each round, midpoint $mid_i = (lo_i + hi_i)/2$ groups queries. Apply events up to $mid$, evaluate queries, and shrink bounds.

##### Closed-Form Invariant Equations

$$\text{Time}(\text{MITM}) = \mathcal{O}\big(2^{N/2} \log(2^{N/2})\big) = \mathcal{O}\big(N \cdot 2^{N/2}\big), \quad \text{Time}(\text{PBS}) = \mathcal{O}\big((N + Q)\log M\big)$$

##### Structural Edge Cases & Assumptions

- In Meet-in-the-Middle, ensure $N/2$ splitting is balanced; an asymmetric split (e.g. $18$ and $22$) degrades performance significantly.
- Use custom `custom_hash` with `splitmix64` for all `gp_hash_table` and `std::unordered_map` structures in competitive programming.

---

#### 3. Core Intuition & Problem Framing

Decision Matrix: If queries have point updates $\implies$ Segment Tree or Fenwick. If queries are static, offline, and the aggregate state has no clean associative merge but supports $\mathcal{O}(1)$ insertion and deletion of single elements (e.g., number of distinct elements, frequency counts) $\implies$ Mo's Algorithm in $\mathcal{O}((N + Q) \sqrt{N})$.

---

#### 4. Proof Sketches & Recurrences

Mo's algorithm partitions queries into $B \approx N / \sqrt{Q}$ blocks by left endpoint and sorts right endpoints. Total pointer movements: $Q \cdot B + N \cdot (N / B) = \mathcal{O}(N \sqrt{Q})$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Mo Algorithm vs Segtree Decision Guide Template
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int l, r, id, block;
    bool operator<(const Query& o) const {
        if (block != o.block) return block < o.block;
        return (block & 1) ? r < o.r : r > o.r; // Hilbert / serpentine optimization
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Query asks for number of distinct elements, modes, or frequency threshold in $[L, R]$.
- No updates are performed during query execution.
- Adding or removing one element to the current range takes $\mathcal{O}(1)$ or $\mathcal{O}(\log N)$.

---

#### 7. Contest WA / TLE / RE Traps

- Applying Mo's algorithm when queries require online answers.
- Choosing block size $B = \sqrt{N}$ when $Q \ll N$ or $Q \gg N$; optimal is $B = \max(1, N / \sqrt{Q})$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-888G | Xor-MST | 2300 | Binary Trie, Boruvka, XOR | Divide-and-Conquer Boruvka MST over Binary Trie bits. | [Solve Problem](https://codeforces.com/contest/888/problem/G) |
| Codeforces | CF-1006F | Xor-Paths | 2000 | Meet in the Middle, Grid Paths | Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map. | [Solve Problem](https://codeforces.com/contest/1006/problem/F) |
| Codeforces | CF-484E | Sign on Fence | 2600 | Parallel Binary Search, Persistent SegTree | Parallel Binary Search + Persistent Segment Tree for range max contiguous ones. | [Solve Problem](https://codeforces.com/contest/484/problem/E) |
| CSES | CSES-1628 | Meet in the Middle | 1600 | Meet in the Middle, Binary Search | Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count. | [Solve Problem](https://cses.fi/problemset/task/1628) |

---

#### 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)](https://codeforces.com/blog/entry/62393)
- **[CP-Algorithms]** [CP-Algorithms: Parallel Binary Search](https://cp-algorithms.com/others/parallel-binary-search.html)
- **[USACO Guide]** [USACO Guide: Meet-in-the-Middle 2^(N/2)](https://usaco.guide/gold/mitm)

---


---
