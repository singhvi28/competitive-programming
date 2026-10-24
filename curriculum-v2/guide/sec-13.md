# Section §13: Bit Manipulation & Advanced Combinatorics

> **Module ID:** `sec-13`  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Topic Count:** 19  

**Module Summary:** Bitmask tricks, submask enumeration in 3^n, Binomial coefficients mod P, Lucas theorem, Catalan/Stirling numbers, and Burnside's Lemma.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Bitmask tricks](#topic-1) | `S-tier` | 1200–2000 | Very Common | [01-13-bitmask-tricks.md](./01-13-bitmask-tricks.md) |
| 2 | [Submask enumeration](#topic-2) | `A-tier` | 1700–2300 | Common | [02-13-submask-enumeration.md](./02-13-submask-enumeration.md) |
| 3 | [SOS DP](#topic-3) | `A-tier · Frequency: Occasional · Rating: 1800–2400` | 1800–2400 | Occasional · Rating: 1800–2400 | [03-13-sos-dp.md](./03-13-sos-dp.md) |
| 4 | [Gray code](#topic-4) | `C-tier` | 1600–2200 | Rare | [04-13-gray-code.md](./04-13-gray-code.md) |
| 5 | [XOR basis / linear basis](#topic-5) | `A-tier` | 1800–2500 | Occasional | [05-13-xor-basis-linear-basis.md](./05-13-xor-basis-linear-basis.md) |
| 6 | [Walsh-Hadamard Transform](#topic-6) | `C-tier` | 2300–2900 | Rare | [06-13-walsh-hadamard-transform.md](./06-13-walsh-hadamard-transform.md) |
| 7 | [Fast subset convolution concepts](#topic-7) | `Niche` | 2500–3200 | Rare | [07-13-fast-subset-convolution-concepts.md](./07-13-fast-subset-convolution-concepts.md) |
| 8 | [Binomial coefficients](#topic-8) | `S-tier` | 1200–2000 | Very Common | [08-13-binomial-coefficients.md](./08-13-binomial-coefficients.md) |
| 9 | [Lucas theorem](#topic-9) | `B-tier` | 1800–2400 | Occasional | [09-13-lucas-theorem.md](./09-13-lucas-theorem.md) |
| 10 | [Catalan numbers](#topic-10) | `A-tier` | 1500–2100 | Occasional | [10-13-catalan-numbers.md](./10-13-catalan-numbers.md) |
| 11 | [Stirling numbers](#topic-11) | `B-tier` | 1800–2500 | Occasional | [11-13-stirling-numbers.md](./11-13-stirling-numbers.md) |
| 12 | [Burnside's lemma](#topic-12) | `B-tier` | 1900–2500 | Occasional | [12-13-burnside-s-lemma.md](./12-13-burnside-s-lemma.md) |
| 13 | [Pólya enumeration](#topic-13) | `C-tier` | 2200–2800 | Rare | [13-13-p-lya-enumeration.md](./13-13-p-lya-enumeration.md) |
| 14 | [Generating functions basics](#topic-14) | `B-tier` | 2000–2800 | Occasional | [14-13-generating-functions-basics.md](./14-13-generating-functions-basics.md) |
| 15 | [Recognition shortcuts](#topic-15) | `B-tier` | 1600–2200 | Common | [15-13-recognition-shortcuts.md](./15-13-recognition-shortcuts.md) |
| 16 | [High-ROI (drill first)](#topic-16) | `B-tier` | 1600–2200 | Common | [16-13-high-roi-drill-first.md](./16-13-high-roi-drill-first.md) |
| 17 | [Situational (learn after High-ROI)](#topic-17) | `B-tier` | 1600–2200 | Common | [17-13-situational-learn-after-high-roi.md](./17-13-situational-learn-after-high-roi.md) |
| 18 | [Rarely worth early / Niche](#topic-18) | `B-tier` | 1600–2200 | Common | [18-13-rarely-worth-early-niche.md](./18-13-rarely-worth-early-niche.md) |
| 19 | [What to drill this week](#topic-19) | `B-tier` | 1600–2200 | Common | [19-13-what-to-drill-this-week.md](./19-13-what-to-drill-this-week.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Bitmask tricks

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–2000 | **Frequency:** Very Common  
> **Prerequisites:** integers, binary representation, basic loops  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–2000
- Prerequisites: integers, binary representation, basic loops

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

A mask is a set. Arithmetic on two’s-complement integers implements set ops in \(O(1)\): `&` intersection, `|` union, `^` symmetric difference, `~` complement (careful with width). The single most useful identity is `x & -x` = lowest set bit (LSB) as a power of two — it peels a set one element at a time without scanning all bits.

---

#### 4. Proof Sketches & Recurrences

- LSB: in two’s complement, `-x = ~x + 1`, so `x & -x` keeps only the trailing 1.
- Clear LSB: `x &= x - 1`.
- Iterate bits: `for (int m = x; m; m &= m - 1) { int b = __builtin_ctz(m); ... }`.
- Subset of \([0..n)\): masks in `[0, 1<<n)`.
- Bit-reversal / Gray: see Gray code topic.
- Popcount parity: `__builtin_parity`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(1)\) or \(O(\mathrm{popcount})\) to iterate bits
- Total: problem-dependent
- Memory: \(O(1)\) extras`

##### C++17 Template

```cpp
namespace bitmask {
inline int lsb(int x) { return x & -x; }
inline int ctz(int x) { return __builtin_ctz(x); }       // x > 0
inline int clz(int x) { return __builtin_clz(x); }       // x > 0
inline int pop(int x) { return __builtin_popcount(x); }
inline long long popl(long long x) { return __builtin_popcountll(x); }

// iterate set bit indices of mask
template <class F>
void for_bits(int mask, F&& f) {
    for (int m = mask; m; m &= m - 1) f(__builtin_ctz(m));
}

// next mask with same popcount (combinations in lex order)
bool next_combination_mask(int& mask, int n) {
    // Gosper's hack: next number with same number of 1-bits
    int c = mask & -mask;
    int r = mask + c;
    if (r >= (1 << n)) return false;
    mask = (((r ^ mask) >> 2) / c) | r;
    return true;
}

// all submasks of universe U = (1<<n)-1 that contain required bits R
void for_masks_containing(int n, int R, auto&& f) {
    int free = ((1 << n) - 1) ^ R;
    for (int s = free;; s = (s - 1) & free) {
        f(s | R);
        if (!s) break;
    }
}
} // namespace bitmask
```

##### Python 3 Template

```python
def lsb(x: int) -> int:
    return x & -x

def for_bits(mask: int):
    m = mask
    while m:
        b = (m & -m).bit_length() - 1
        yield b
        m &= m - 1

def popcount(x: int) -> int:
    return x.bit_count()  # 3.10+
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Subset of \(n \le 20\) items,” flags, presence/absence
- Need popcount, next permutation of bits, iterate set bits only
- Coordinate compression into bitsets / bit-DP transitions

---

#### 7. Contest WA / TLE / RE Traps

- Using `1 << n` when `n == 31` → UB in signed 32-bit; use `1LL << n` or unsigned.
- `~mask` without `& ((1<<n)-1)` → infinite high bits.
- `__builtin_ctz(0)` undefined — guard empty masks.
- Signed right shift for arithmetic when you wanted logical.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- 64-bit / `__int128` masks; arrays of `uint64_t` for \(n > 64\).
- `std::bitset<N>` for heavy bitset DP (AND/OR shifts).
- Builtins: `__builtin_mul_overflow` rarely mixed in.

---

#### 11. Typical Problem Archetypes

1. Standard application: count subsets with property via bit-DP.
2. Slightly disguised: compress \(n \le 20\) boolean attributes into mask keys.
3. Difficult: bitset optimized transitions \(O(n^2 / 64)\).
4. Very difficult / advanced: meet-in-the-middle on masks + hashing.

---

#### 12. Recognition & Identification Drills

1. Among \(n \le 20\) tasks, choose a subset maximizing value with conflict pairs.
2. Given integers, find a nonempty subset whose XOR is 0 (small \(n\)).
3. Process only set bits of a 64-bit mask without looping 0..63 blindly.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any \(n \le 20\)–22 set / flag state
- Key invariant: mask ↔ subset bijection
- Key formula: `x & -x` LSB; `x &= x-1` clear LSB
- Complexity: bit ops \(O(1)\); iterate bits \(O(\mathrm{pop})\)
- Template to remember: `for (int m = x; m; m &= m - 1)`

---

---


---

<a id="topic-2"></a>
### 2. Submask enumeration

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** Bitmask tricks, bit-DP basics  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Bitmask tricks, bit-DP basics

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

For a fixed mask \(m\), every nonempty submask appears exactly once in the loop `for (int s = m; s; s = (s - 1) & m)`, and `s = 0` can be handled separately. Over all \(m\), \(\sum_m 2^{\mathrm{pop}(m)} = 3^n\) for an \(n\)-bit universe — the classic \(O(3^n)\) budget.

---

#### 4. Proof Sketches & Recurrences

Identity: decrementing \(s\) then `& m` clears bits outside \(m\) and walks all submasks in reverse order.
Total time if you do this for every \(m\):
\[
\sum_{m=0}^{2^n-1} 2^{\mathrm{popcount}(m)} = \sum_{k=0}^{n} C(n,k) 2^k = 3^n.
\]
Supermasks of \(m\): iterate bits free outside \(m\), or use `for (int s = m; s < (1<<n); s = (s + 1) | m)`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(2^{\mathrm{pop}(m)})\) for one mask
- Total: \(O(3^n)\) over all masks
- Memory: \(O(1)\) or \(O(2^n)\) for DP tables`

##### C++17 Template

```cpp
namespace submask {
// all nonempty submasks of m, then optionally 0
template <class F>
void enum_submasks(int m, F&& f, bool include_zero = true) {
    for (int s = m; s; s = (s - 1) & m) f(s);
    if (include_zero) f(0);
}

// for every mask: process all its submasks — O(3^n)
template <class F>
void for_all_mask_submasks(int n, F&& f) {
    int N = 1 << n;
    for (int m = 0; m < N; ++m)
        for (int s = m;; s = (s - 1) & m) {
            f(m, s);
            if (s == 0) break;
        }
}

// split m = a | b, a & b == 0, a,b nonempty optional
// enumerate a ⊆ m, b = m ^ a
template <class F>
void enum_splits(int m, F&& f, bool allow_empty = false) {
    for (int a = m;; a = (a - 1) & m) {
        int b = m ^ a;
        if (allow_empty || (a && b)) f(a, b);
        if (a == 0) break;
    }
}

// supermasks of m in universe n bits
template <class F>
void enum_supermasks(int m, int n, F&& f) {
    int U = (1 << n) - 1;
    int free = U ^ m;
    for (int s = free;; s = (s - 1) & free) {
        f(m | s);
        if (!s) break;
    }
}
} // namespace submask
```

##### Python 3 Template

```python
def enum_submasks(m: int, include_zero: bool = True):
    s = m
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & m
    # note: yields m ... 0; if not include_zero, stop before 0
```

---

#### 6. Recognition Trigger Signals & Heuristics

- DP transition: “split mask into two disjoint parts” or “submask of previous”
- Enumerate partitions of a bit-set into labeled/unlabeled blocks
- Statement mentions \(n \le 20\) and subset-of-subset structure

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `s == 0` (infinite loop if you write `do/while` wrong).
- Using submask enum when you need **SOS** (all-subset sums for every mask efficiently structured).
- Double-counting unordered splits \(\{a,b\}\) — iterate `a < b` or `a <= m/2` style.
- \(n = 20\) → \(3^{20} \approx 3.4 \cdot 10^9\) too slow; \(n \le 18\) typical for full \(3^n\), \(n \le 20\) only light work inside.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Enumerate submasks by popcount layers.
- SOS DP (stub below / full in §04) replaces many “sum over submasks” DPs.
- Meet-in-the-middle: \(n=40\) → two halves + submask / subset sums.

---

#### 11. Typical Problem Archetypes

1. Standard application: DP over subsets with transition from submasks.
2. Slightly disguised: assign people to teams — split bits.
3. Difficult: optimize constants / prune by popcount.
4. Very difficult / advanced: combine with SOS or FWT for convolutions.

---

#### 12. Recognition & Identification Drills

1. \(n \le 18\) cities; DP over visited subset with split tours.
2. Count ways to partition a set of \(n \le 16\) into unordered pairs of blocks with scores.
3. For each mask, sum \(f[s]\) over \(s \subseteq m\) (hint: may be SOS, not raw enum).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: local submask walks / splits, \(n \le 18\)–20
- Key invariant: `(s - 1) & m` visits each submask once
- Key formula: total \(\sum 2^{\mathrm{pop}(m)} = 3^n\)
- Complexity: \(O(3^n)\) all pairs \((m,s\subseteq m)\)
- Template to remember: `for (int s = m; ; s = (s - 1) & m) { ...; if (!s) break; }`

---

---


---

<a id="topic-3"></a>
### 3. SOS DP

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier · Frequency: Occasional · Rating: 1800–2400 | **Rating Range:** 1800–2400 | **Frequency:** Occasional · Rating: 1800–2400  
> **Prerequisites:** Bitmasks, DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier · Frequency: Occasional · Rating: 1800–2400
- Use when you need \(F[S] = \sum_{T \subseteq S} f[T]\) (or superset sums) for **all** \(S\) in \(O(n 2^n)\), not \(O(3^n)\) submask loops.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Fast zeta on the boolean lattice: fix one bit dimension at a time and prefix-sum along that bit.

---

#### 4. Proof Sketches & Recurrences

Define $dp[i][mask]$ as the sum over all submasks $sub \subseteq mask$ that differ from $mask$ only on a subset of the first $i$ bits. If the $i$-th bit of $mask$ is 0, then any submask must also have the $i$-th bit as 0: $dp[i][mask] = dp[i-1][mask]$. If the $i$-th bit is 1, a submask can have this bit as either 0 or 1: $dp[i][mask] = dp[i-1][mask] + dp[i-1][mask \oplus 2^i]$. Memory can be rolled into a single 1D array of size $2^N$ by iterating $i$ in the outer loop.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// SOS DP: Fast Multi-dimensional Prefix Sum over Hypercube in O(N * 2^N)
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void sos_dp_inplace(int n, vector<ll>& f) {
    // f[mask] initially stores A[mask]
    for (int i = 0; i < n; ++i) {
        for (int mask = 0; mask < (1 << n); ++mask) {
            if (mask & (1 << i)) {
                f[mask] += f[mask ^ (1 << i)];
            }
        }
    }
    // Now f[mask] = sum_{sub in mask} A[sub]
}

// Superset sum: sum_{mask in sup} A[sup] in O(N * 2^N)
void sos_superset_inplace(int n, vector<ll>& f) {
    for (int i = 0; i < n; ++i) {
        for (int mask = (1 << n) - 1; mask >= 0; --mask) {
            if (!(mask & (1 << i))) {
                f[mask] += f[mask ^ (1 << i)];
            }
        }
    }
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Submask enum: “for this mask, look at its submasks” with light work.
- SOS: “transform whole arrays on the subset lattice,” then maybe Möbius invert.
- Related here: WHT/FWT (XOR/OR/AND convolutions) and fast subset convolution (below) build on the same lattice mindset.

---

#### 7. Contest WA / TLE / RE Traps

- Inverting the loop nesting: if mask is the outer loop and bit $i$ is the inner loop, hypercube prefix sums will NOT propagate correctly, producing wrong results.
- Bitwise precedence error: `mask & 1 << i` evaluates as `mask & (1 << i)`, but `mask & 1 == 0` evaluates as `mask & (1 == 0)`; always wrap bitwise checks in parentheses.
- Array sizing: array must be allocated with size $2^N$ (`1 << n`), not $N$.
- Integer overflow: accumulating array values in `int` when sum of $2^N$ terms exceeds $2 \times 10^9$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 13. Fast-Lookup Cheat Sheet

- Open §04 SOS DP for C++/Python templates, bugs, and problem patterns.

---

---


---

<a id="topic-4"></a>
### 4. Gray code

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 1600–2200 | **Frequency:** Rare  
> **Prerequisites:** Bitmask tricks  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Bitmask tricks

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Binary-reflected Gray code orders all \(n\)-bit strings so consecutive codes differ by exactly one bit. The map \(i \mapsto i \oplus (i >> 1)\) is the standard encoding; decoding recovers \(i\) by XORing down prefixes. Useful when you must traverse the hypercube with single-bit flips (Hamiltonian path on the cube).

---

#### 4. Proof Sketches & Recurrences

Encode: \(g(i) = i \oplus \lfloor i/2 \rfloor\).  
Decode: \(i = g \oplus (g >> 1) \oplus (g >> 2) \oplus \cdots\).  
Binary-reflected construction: \(n\)-bit list = \(0\cdot G_{n-1}\) then \(1\cdot \mathrm{rev}(G_{n-1})\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) or \(O(2^n)\) to materialize
- Per-query / per-operation: \(O(1)\) encode; \(O(\log i)\) naive decode
- Total: \(O(2^n)\) full tour
- Memory: \(O(1)\) streaming or \(O(2^n)\) list`

##### C++17 Template

```cpp
namespace gray {
int encode(int i) { return i ^ (i >> 1); }
int decode(int g) {
    int i = g;
    while (g) { g >>= 1; i ^= g; }
    return i;
}
// visit all masks in Gray order: start 0, flip bit ctz(i^(i-1)) ...
vector<int> sequence(int n) {
    vector<int> a(1 << n);
    for (int i = 0; i < (1 << n); ++i) a[i] = encode(i);
    return a;
}
} // namespace gray
```

##### Python 3 Template

```python
def gray_encode(i: int) -> int:
    return i ^ (i >> 1)

def gray_decode(g: int) -> int:
    i = g
    while g:
        g >>= 1
        i ^= g
    return i
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Adjacent configurations differ by one element”
- Hardware / puzzle: revolving drum, Tower-adjacent flips
- Generate all subsets with only add/remove one element between neighbors

---

#### 7. Contest WA / TLE / RE Traps

- Confusing encode/decode direction.
- Assuming Gray order equals numeric order for DP transitions — it does not.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Balanced Gray codes; combinatorial Gray codes for combinations (\(k\)-subsets).
- Steinhaus–Johnson–Trotter for permutations (adjacent swaps) — cousin idea.

---

#### 11. Typical Problem Archetypes

1. Standard application: list all masks with single-bit transitions.
2. Slightly disguised: minimize changes when sweeping configurations.
3. Difficult: \(k\)-subset Gray code for combination generation.
4. Very difficult / advanced: Gray codes on other graphs / necklaces.

---

#### 12. Recognition & Identification Drills

1. Output a sequence of all \(2^n\) subsets where each step adds or removes one element.
2. Convert index \(i\) to Gray code and back for \(n=20\).
3. Robot must visit all switch states flipping one switch at a time.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: single-bit-flip Hamiltonian path on \(\{0,1\}^n\)
- Key invariant: consecutive Gray codes differ by 1 bit
- Key formula: \(g = i \oplus (i >> 1)\)
- Complexity: \(O(1)\) per code
- Template to remember: `i ^ (i >> 1)`

---

---


---

<a id="topic-5"></a>
### 5. XOR basis / linear basis

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Bitwise XOR, greedy on bits, basic linear algebra intuition over GF(2)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Bitwise XOR, greedy on bits, basic linear algebra intuition over GF(2)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Subset XORs of a multiset of integers form a subspace of \(\mathrm{GF}(2)^w\). A **linear basis** stores at most \(w\) vectors (usually \(w \le 32\) or \(64\)) in row-echelon form by highest bit: insertion tries to eliminate using existing pivots; if a bit position is free, the value becomes the pivot. Then: max XOR = greedy take/reject pivots from MSB; size of span = \(2^{|\mathrm{basis}|}\) (if 0 not forced extra); check representability by elimination.

*Note: This is Gaussian Elimination over GF(2). For general Gaussian Elimination over Reals or Modulo $P$, see [Section 14a](../16-a-gaussian-elimination-determinants.md).*

---

#### 4. Proof Sketches & Recurrences

Gaussian elimination over GF(2) on columns = bits. Insertion of \(x\):
for \(b = w-1 \ldots 0\): if bit \(b\) of \(x\) set, if `basis[b]` empty assign, else `x ^= basis[b]`.  
If \(x\) becomes 0, it was dependent.  
Max: start `ans = 0`; for \(b = w-1 \ldots 0\): if `(ans ^ basis[b]) > ans` (unsigned) take it — for maximizing value.  
Count distinct: \(2^{sz}\) if we don’t store duplicates; if zero-subset only empty, still \(2^{sz}\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: insert / query \(O(W^2)\) naive or \(O(W)\) with care
- Total: \(O(n W)\) typical
- Memory: \(O(W)\)`

##### C++17 Template

```cpp
namespace xor_basis {
struct Basis {
    static constexpr int W = 32; // use 64 for long long
    unsigned bas[W]{};
    int sz = 0;
    bool insert(unsigned x) {
        for (int b = W - 1; b >= 0; --b) {
            if (!((x >> b) & 1u)) continue;
            if (!bas[b]) { bas[b] = x; ++sz; return true; }
            x ^= bas[b];
        }
        return false; // dependent
    }
    bool representable(unsigned x) const {
        for (int b = W - 1; b >= 0; --b)
            if ((x >> b) & 1u) x ^= bas[b];
        return x == 0;
    }
    unsigned max_xor() const {
        unsigned ans = 0;
        for (int b = W - 1; b >= 0; --b)
            if ((ans ^ bas[b]) > ans) ans ^= bas[b];
        return ans;
    }
    // k-th smallest nonempty? usually k-th in span including 0:
    // rebuild triangular basis then digitize k
    unsigned kth(unsigned long long k) const { // 0-indexed in sorted span
        vector<unsigned> v;
        for (int b = 0; b < W; ++b) if (bas[b]) v.push_back(bas[b]);
        // optional: clean to diagonal for unique digits
        for (int i = 0; i < (int)v.size(); ++i)
            for (int j = 0; j < i; ++j)
                if ((v[i] ^ v[j]) < v[i]) v[i] ^= v[j];
        sort(v.begin(), v.end());
        if (k >= (1ULL << v.size())) return UINT_MAX; // invalid
        unsigned ans = 0;
        for (int i = 0; i < (int)v.size(); ++i)
            if ((k >> i) & 1ULL) ans ^= v[i];
        return ans;
    }
};
} // namespace xor_basis
```

##### Python 3 Template

```python
class XorBasis:
    __slots__ = ("bas", "sz", "W")
    def __init__(self, W: int = 32):
        self.W = W
        self.bas = [0] * W
        self.sz = 0
    def insert(self, x: int) -> bool:
        for b in range(self.W - 1, -1, -1):
            if ((x >> b) & 1) == 0:
                continue
            if self.bas[b] == 0:
                self.bas[b] = x
                self.sz += 1
                return True
            x ^= self.bas[b]
        return False
    def max_xor(self) -> int:
        ans = 0
        for b in range(self.W - 1, -1, -1):
            if (ans ^ self.bas[b]) > ans:
                ans ^= self.bas[b]
        return ans
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Maximum XOR of a subset,” “number of distinct subset XORs”
- Insert numbers online; query max XOR with a value
- Paths on trees/graphs with XOR weights → basis of cycle XORs + path
- “Make XOR = x using subset” / independence

---

#### 7. Contest WA / TLE / RE Traps

- Mixing signed comparisons for max XOR — prefer `unsigned`.
- Forgetting that inserting 0 does nothing.
- Counting \(2^{sz}\) vs \(2^{sz}-1\) (empty subset).
- Offline path-XOR on trees: need basis of **fundamental cycles**, not raw edges.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Basis for AND/OR is **not** linear the same way — don’t force it.
- d-dimensional / larger fields rare in CF.
- Merge two bases: insert all pivots of one into the other (\(O(W^2)\)).

---

#### 11. Typical Problem Archetypes

1. Standard application: max subset XOR.
2. Slightly disguised: max XOR of path in a tree (basis + dfs xor).
3. Difficult: k-th largest subset XOR; forced include/exclude.
4. Very difficult / advanced: linear basis + segment tree / time machine offline.

---

#### 12. Recognition & Identification Drills

1. Array of \(n\) ints; maximize XOR of a subset.
2. Online insert; after each insert print size of set of subset XORs.
3. Edge-XOR weighted graph; can you achieve XOR \(x\) on a walk from \(u\) to \(v\)?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: subset XOR space questions
- Key invariant: span closed under XOR; basis size \(\le W\)
- Key formula: insert by MSB elimination; max via greedy MSB
- Complexity: \(O(n W)\)
- Template to remember: `if (!bas[b]) bas[b]=x; else x^=bas[b];`

---

---


---

<a id="topic-6"></a>
### 6. Walsh-Hadamard Transform

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Bitmasks, SOS intuition, modular arithmetic / FFT mindset  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Bitmasks, SOS intuition, modular arithmetic / FFT mindset

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

WHT (FWT for XOR) diagonalizes subset-XOR convolution:
\[
(f *_{\oplus} g)(k) = \sum_{i \oplus j = k} f(i)g(j).
\]
Like FFT: transform → pointwise multiply → inverse transform. OR/AND convolutions have analogous FWTs (closely related to SOS zeta). For XOR, butterflies are \(a' = a+b,\ b' = a-b\) (or modular equivalents).

---

#### 4. Proof Sketches & Recurrences

Hadamard matrix \(H_2 = \begin{bmatrix}1&1\\1&-1\end{bmatrix}\), \(H_{2^{n}} = H_2 \otimes H_{2^{n-1}}\).  
FWHT in-place: for `len = 1; len < N; len <<= 1` for each block apply butterfly.  
Inverse: same transform, then divide by \(N = 2^n\) (or multiply by \(\mathrm{inv}(N)\)).  
OR-FWT: \(a' = a,\ b' = a+b\); AND-FWT: \(a' = a+b,\ b' = b\); invert with minus.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: one FWHT \(O(N \log N)\) with \(N = 2^n\)
- Total: XOR conv \(O(N \log N)\)
- Memory: \(O(N)\)`

##### C++17 Template

```cpp
namespace fwt {
using i64 = long long;
// XOR FWHT; mod prime. invN applied only on inverse.
void fwht_xor(vector<i64>& a, bool invert, i64 mod) {
    int n = (int)a.size();
    for (int len = 1; len < n; len <<= 1) {
        for (int i = 0; i < n; i += len << 1) {
            for (int j = 0; j < len; ++j) {
                i64 u = a[i + j], v = a[i + j + len];
                a[i + j] = u + v;
                if (a[i + j] >= mod) a[i + j] -= mod;
                a[i + j + len] = u - v;
                if (a[i + j + len] < 0) a[i + j + len] += mod;
            }
        }
    }
    if (invert) {
        i64 inv = 1, base = n % mod;
        for (i64 e = mod - 2; e; e >>= 1) {
            if (e & 1) inv = inv * base % mod;
            base = base * base % mod;
        }
        for (i64& x : a) x = x * inv % mod;
    }
}

vector<i64> conv_xor(vector<i64> f, vector<i64> g, i64 mod) {
    int n = 1;
    while (n < (int)max(f.size(), g.size())) n <<= 1;
    f.resize(n); g.resize(n);
    fwht_xor(f, false, mod);
    fwht_xor(g, false, mod);
    for (int i = 0; i < n; ++i) f[i] = f[i] * g[i] % mod;
    fwht_xor(f, true, mod);
    return f;
}
} // namespace fwt
```

##### Python 3 Template

```python
# Reference only — prefer C++ in contest
def fwht_xor(a, invert=False):
    n = len(a)
    len_ = 1
    while len_ < n:
        for i in range(0, n, len_ << 1):
            for j in range(len_):
                u, v = a[i + j], a[i + j + len_]
                a[i + j], a[i + j + len_] = u + v, u - v
        len_ <<= 1
    if invert:
        a[:] = [x // n for x in a]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Convolution where indices combine by XOR (sometimes OR/AND)
- Count pairs/triples with \(a_i \oplus a_j = a_k\)
- Generating functions over \(\mathrm{GF}(2)^n\) characters

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting divide-by-\(N\) on inverse XOR-FWT.
- Using OR/AND butterflies for XOR problems.
- `n` not a power of two — pad.
- Modular negative handling after `u - v`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- OR / AND FWT; subset zeta (SOS) for subset-sum style.
- Multiple sequences: pointwise product of \(k\) transforms.
- Untyped integer FWHT when values small (no mod).

---

#### 11. Typical Problem Archetypes

1. Standard application: count pairs with given XOR via freq FWHT.
2. Slightly disguised: expected value over XOR combinations.
3. Difficult: constrained convolutions + DP on bits.
4. Very difficult / advanced: subset convolution via ranked FWHT (next topic).

---

#### 12. Recognition & Identification Drills

1. Arrays \(A,B\); for every \(x\) count pairs \(a \oplus b = x\).
2. Number of triples \(i,j,k\) with \(a_i \oplus a_j \oplus a_k = 0\).
3. Polynomial product where exponents XOR instead of add.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: XOR/OR/AND index convolutions on \(2^n\) arrays
- Key invariant: FWHT diagonalizes the group character table of \((\mathbb{Z}/2\mathbb{Z})^n\)
- Key formula: butterfly \(+(a+b),\ -(a-b)\); inv `/N`
- Complexity: \(O(N \log N)\), \(N=2^n\)
- Template to remember: transform → pointwise mul → inverse

---

---


---

<a id="topic-7"></a>
### 7. Fast subset convolution concepts

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** Niche | **Rating Range:** 2500–3200 | **Frequency:** Rare  
> **Prerequisites:** SOS DP (§04), FWT/WHT, popcount rankings  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2500–3200
- Prerequisites: SOS DP (§04), FWT/WHT, popcount rankings

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Subset convolution (cover product with disjoint union):
\[
(f * g)(S) = \sum_{A \subseteq S} f(A)\, g(S \setminus A)
\]
(equivalently sum over disjoint \(A \sqcup B = S\)). Naive \(O(3^n)\). Fast methods use **ranked** zeta: let \(f_k[S] = f[S]\) if \(\mathrm{pop}(S)=k\) else 0, SOS-transform each layer, pointwise multiply with convolution on ranks \(h_k = \sum_{i+j=k} F_i G_j\), then Möbius invert — \(O(n^2 2^n)\).

---

#### 4. Proof Sketches & Recurrences

1. Rank: \(f_i[S] = [\mathrm{pop}(S)=i] f[S]\).
2. \(\hat f_i = \zeta f_i\) (SOS subset-sum transform).
3. \(\hat h_k[S] = \sum_{i=0}^{k} \hat f_i[S] \hat g_{k-i}[S]\).
4. \(h_k = \mu \hat h_k\); answer \(h[S] = h_{\mathrm{pop}(S)}[S]\).  
Correctness: zeta turns disjoint convolutions into products on the lattice after ranking.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(n^2 2^n)\)
- Total: usually one convolution
- Memory: \(O(n 2^n)\)`

##### C++17 Template

```cpp
namespace subset_conv {
using i64 = long long;
void zeta(vector<i64>& a, int n) { // subset SOS
    for (int i = 0; i < n; ++i)
        for (int m = 0; m < (1 << n); ++m)
            if (m & (1 << i)) a[m] += a[m ^ (1 << i)];
}
void mobius(vector<i64>& a, int n) {
    for (int i = 0; i < n; ++i)
        for (int m = 0; m < (1 << n); ++m)
            if (m & (1 << i)) a[m] -= a[m ^ (1 << i)];
}

// f,g sized 1<<n; mod not applied (add yourself)
vector<i64> subset_convolution(const vector<i64>& f, const vector<i64>& g, int n) {
    int N = 1 << n;
    vector<vector<i64>> F(n + 1, vector<i64>(N)), G(n + 1, vector<i64>(N)), H(n + 1, vector<i64>(N));
    for (int m = 0; m < N; ++m) {
        F[__builtin_popcount(m)][m] = f[m];
        G[__builtin_popcount(m)][m] = g[m];
    }
    for (int k = 0; k <= n; ++k) { zeta(F[k], n); zeta(G[k], n); }
    for (int k = 0; k <= n; ++k)
        for (int i = 0; i <= k; ++i)
            for (int m = 0; m < N; ++m)
                H[k][m] += F[i][m] * G[k - i][m];
    for (int k = 0; k <= n; ++k) mobius(H[k], n);
    vector<i64> h(N);
    for (int m = 0; m < N; ++m) h[m] = H[__builtin_popcount(m)][m];
    return h;
}
} // namespace subset_conv
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Editorial says “subset convolution” / “disjoint union convolution”
- DP combining two subset functions with empty intersection
- \(n \le 20\) but \(3^n\) TLE while \(n^2 2^n\) fits

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting rank (plain FWT XOR ≠ subset convolution).
- Modular reduction missing in accumulators → overflow.
- Using OR-convolution when disjointness is required.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Cover product \(\sum_{A \cup B = S} f(A)g(B)\) via different transforms.
- Constrained popcount / colored subset conv.
- Niche: keep as editorial vocabulary, implement only when forced.

---

#### 11. Typical Problem Archetypes

1. Standard application: disjoint merge of two subset DPs.
2. Slightly disguised: counting perfect matchings-style via subsets (rare).
3. Difficult: repeated convolutions / exp on subset lattice.
4. Very difficult / advanced: FPS on subset lattice / advanced FWT packs.

---

#### 12. Recognition & Identification Drills

1. Given \(f,g\) on masks, compute \(\sum_{A \sqcup B = S} f(A)g(B)\) for all \(S\), \(n=18\).
2. Explain why XOR-FWT does **not** solve disjoint subset convolution.
3. Reduce \(O(3^n)\) DP merge to \(O(n^2 2^n)\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: disjoint-union convolution, Niche only
- Key invariant: ranked zeta → pointwise rank convolution → Möbius
- Key formula: \((f*g)(S)=\sum_{A\subseteq S}f(A)g(S\setminus A)\)
- Complexity: \(O(n^2 2^n)\)
- Template to remember: rank layers + SOS ζ + mul + μ

---

Back to [`13-bit-combinatorics.md`](13-bit-combinatorics.md) · Combinatorics: [`13-b-advanced-combinatorics.md`](13-b-advanced-combinatorics.md)

---


---

<a id="topic-8"></a>
### 8. Binomial coefficients

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–2000 | **Frequency:** Very Common  
> **Prerequisites:** Modular arithmetic, modular inverse, factorials  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–2000
- Prerequisites: Modular arithmetic, modular inverse, factorials

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

\(C(n,k) = \frac{n!}{k!(n-k)!}\) counts \(k\)-subsets. In contests you almost always need many queries mod prime \(p\): precompute \(fact[i]\), \(invfact[i]\) in \(O(n + \log p)\), then \(C(n,k) = fact[n] \cdot invfact[k] \cdot invfact[n-k]\). For non-prime moduli, use Lucas (prime powers / CRT) or DP \(C(i,j) = C(i-1,j)+C(i-1,j-1)\).

---

#### 4. Proof Sketches & Recurrences

Pascal: \(C(n,k) = C(n-1,k) + C(n-1,k-1)\).  
Inverse factorial: \(invfact[n] = fact[n]^{-1}\), then \(invfact[i] = invfact[i+1] \cdot (i+1)\).  
Stars and bars: \(C(n+k-1, k-1)\) nonneg solutions to \(x_1+\cdots+x_k=n\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(N + \log \mathrm{mod})\)
- Per-query / per-operation: \(O(1)\)
- Total: \(O(N + Q)\)
- Memory: \(O(N)\)`

##### C++17 Template

```cpp
namespace binom {
struct Comb {
    int mod;
    vector<int> fact, invfact;
    Comb(int n, int mod) : mod(mod), fact(n + 1), invfact(n + 1) {
        fact[0] = 1;
        for (int i = 1; i <= n; ++i) fact[i] = (long long)fact[i - 1] * i % mod;
        invfact[n] = mod_pow(fact[n], mod - 2);
        for (int i = n; i >= 1; --i) invfact[i - 1] = (long long)invfact[i] * i % mod;
    }
    int mod_pow(long long a, long long e) const {
        long long r = 1;
        for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
        return (int)r;
    }
    int C(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[k] % mod * invfact[n - k] % mod;
    }
    int P(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[n - k] % mod;
    }
};
} // namespace binom
```

##### Python 3 Template

```python
class Comb:
    def __init__(self, n: int, mod: int):
        self.mod = mod
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.invfact = [1] * (n + 1)
        self.invfact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n, 0, -1):
            self.invfact[i - 1] = self.invfact[i] * i % mod
    def C(self, n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.invfact[k] % self.mod * self.invfact[n - k] % self.mod
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Number of ways to choose,” paths on grid, stars and bars
- Probability written as ratios of binomials
- \(n \le 10^6\), prime mod \(998244353\) / \(10^9+7\)

---

#### 7. Contest WA / TLE / RE Traps

- Calling \(C(n,k)\) with \(n\) larger than precompute limit.
- Non-prime mod → Fermat inverse wrong; use ExtEuclid only if \(\gcd(fact,mod)=1\).
- Forgetting \(k > n \Rightarrow 0\).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Prefix products for huge \(n\) single query: multiply \(n/k \cdot (n-1)/(k-1)\cdots\) carefully.
- Lucas for \(n \gg p\) (next topic).
- Binomial mod \(p^e\) — rare, CRT + factor \(p\).

---

#### 11. Typical Problem Archetypes

1. Standard application: ways to choose \(k\) of \(n\) mod prime.
2. Slightly disguised: grid paths \(C(n+m, n)\).
3. Difficult: sum of binomials / hockey-stick identity.
4. Very difficult / advanced: binomial transforms, formal power series coeffs.

---

#### 12. Recognition & Identification Drills

1. \(Q \le 10^5\) queries \(C(n_i,k_i)\) with \(n_i \le 10^6\), mod \(10^9+7\).
2. Number of nonnegative solutions to \(x_1+\cdots+x_m = n\).
3. Expected number of fixed points — rewrite with binomials.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: almost any counting with choices
- Key invariant: \(C(n,k)=C(n,n-k)\); Pascal recurrence
- Key formula: \(fact[n]\cdot invfact[k]\cdot invfact[n-k]\)
- Complexity: pre \(O(N)\), query \(O(1)\)
- Template to remember: fact + invfact tables

---

---


---

<a id="topic-9"></a>
### 9. Lucas theorem

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Binomial coefficients, base-\(p\) digits, prime modulus  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Binomial coefficients, base-\(p\) digits, prime modulus

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

For prime \(p\): write \(n = n_t p^t + \cdots + n_0\), \(k = k_t p^t + \cdots + k_0\) in base \(p\). Then
\[
C(n,k) \equiv \prod_{i=0}^{t} C(n_i, k_i) \pmod{p},
\]
with \(C(n_i,k_i)=0\) if \(k_i > n_i\). So huge binomials reduce to products of tiny ones (\(n_i < p\)).

---

#### 4. Proof Sketches & Recurrences

From \((1+x)^{p} \equiv 1 + x^{p} \pmod p\) (Freshman’s dream) inductively \((1+x)^n = \prod (1+x)^{n_i p^i} \equiv \prod (1+x^{p^i})^{n_i}\), extract \([x^k]\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(p + \log p)\)
- Per-query / per-operation: \(O(\log_p n)\) small binomials
- Total: \(O(p + Q \log_p n)\)
- Memory: \(O(p)\)`

##### C++17 Template

```cpp
namespace lucas {
struct Lucas {
    int p;
    vector<int> fact, invfact;
    Lucas(int p) : p(p), fact(p), invfact(p) {
        fact[0] = 1;
        for (int i = 1; i < p; ++i) fact[i] = (long long)fact[i - 1] * i % p;
        invfact[p - 1] = mod_pow(fact[p - 1], p - 2);
        for (int i = p - 1; i >= 1; --i) invfact[i - 1] = (long long)invfact[i] * i % p;
    }
    int mod_pow(long long a, long long e) const {
        long long r = 1;
        for (; e; e >>= 1, a = a * a % p) if (e & 1) r = r * a % p;
        return (int)r;
    }
    int C_small(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[k] % p * invfact[n - k] % p;
    }
    int C(long long n, long long k) const {
        if (k < 0 || k > n) return 0;
        int ans = 1;
        while (n || k) {
            int ni = n % p, ki = k % p;
            ans = (long long)ans * C_small(ni, ki) % p;
            if (!ans) return 0;
            n /= p; k /= p;
        }
        return ans;
    }
};
} // namespace lucas
```

##### Python 3 Template

```python
def lucas(n: int, k: int, p: int) -> int:
    if k < 0 or k > n:
        return 0
    fact = [1] * p
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    invfact = [1] * p
    invfact[p - 1] = pow(fact[p - 1], p - 2, p)
    for i in range(p - 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % p
    def C_small(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % p * invfact[a - b] % p
    ans = 1
    while n or k:
        ans = ans * C_small(n % p, k % p) % p
        n //= p
        k //= p
    return ans
```

---

#### 6. Recognition Trigger Signals & Heuristics

- \(C(n,k) \bmod p\) with \(p\) prime and \(n\) up to \(10^{18}\)
- Digit-DP-looking constraints on base-\(p\) digits of \(n,k\)
- “When is \(C(n,k)\) divisible by \(p\)?” ↔ some digit \(k_i > n_i\)

---

#### 7. Contest WA / TLE / RE Traps

- Using Lucas for composite modulus directly — wrong; factor + CRT.
- Building fact tables of size \(n\) instead of \(p\).
- Overflow on \(n\) as `int` when \(n > 2^{31}\).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Lucas for prime powers (generalized) — hard, rarely needed.
- Combination with digit DP on base \(p\).

---

#### 11. Typical Problem Archetypes

1. Standard application: \(C(n,k) \bmod p\), \(n \le 10^{18}\), \(p \le 10^6\).
2. Slightly disguised: count \(k\) with \(C(n,k) \not\equiv 0 \pmod p\).
3. Difficult: sum Lucas digits products under constraints.
4. Very difficult / advanced: multinomial Lucas / CRT composites.

---

#### 12. Recognition & Identification Drills

1. Compute \(C(10^{18}, 10^{9}) \bmod 97\).
2. For prime \(p\), find largest \(k\) with \(C(n,k)\) not divisible by \(p\).
3. Modulus \(15 = 3\cdot 5\) — outline CRT + Lucas plan.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: prime mod, \(n\) too large for factorial tables
- Key invariant: base-\(p\) digit independence of binomials
- Key formula: \(C(n,k) \equiv \prod C(n_i,k_i) \pmod p\)
- Complexity: pre \(O(p)\), query \(O(\log_p n)\)
- Template to remember: while \(n|k\): multiply \(C(n\%p,k\%p)\)

---

---


---

<a id="topic-10"></a>
### 10. Catalan numbers

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Occasional  
> **Prerequisites:** Binomial coefficients, modular inverse  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Binomial coefficients, modular inverse

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

The Catalan number \(C_n = \frac{1}{n+1} C(2n, n) = C(2n,n) - C(2n, n-1)\) counts the same structure under many costumes: valid parentheses, Dyck paths, BSTs on \(n\) keys, triangulations of convex \((n+2)\)-gon, noncrossing partitions, monotonic lattice paths below diagonal. Recurrence \(C_0=1\), \(C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}\).

---

#### 4. Proof Sketches & Recurrences

Ballot theorem → \(C_n = \frac{1}{n+1}C(2n,n)\).  
OGF \(c(x) = \sum C_n x^n = \frac{1 - \sqrt{1-4x}}{2x}\) (\(c(0)=1\)), satisfies \(c = 1 + x c^2\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: binomial tables \(O(N)\) or DP \(O(n^2)\)
- Per-query / per-operation: \(O(1)\) with tables
- Total: \(O(N)\) or \(O(n^2)\)
- Memory: \(O(N)\)`

##### C++17 Template

```cpp
namespace catalan {
// needs binom::Comb with size >= 2n
int catalan(int n, const binom::Comb& comb) {
    // C_n = C(2n, n) / (n+1)
    int c = comb.C(2 * n, n);
    return (long long)c * comb.mod_pow(n + 1, comb.mod - 2) % comb.mod;
}
// recursive DP: Cat[0]=1; Cat[n] = sum Cat[i]*Cat[n-1-i]
vector<int> catalan_dp(int n, int mod) {
    vector<int> Cat(n + 1);
    Cat[0] = 1;
    for (int i = 1; i <= n; ++i) {
        long long s = 0;
        for (int j = 0; j < i; ++j)
            s = (s + (long long)Cat[j] * Cat[i - 1 - j]) % mod;
        Cat[i] = (int)s;
    }
    return Cat;
}
} // namespace catalan
```

##### Python 3 Template

```python
def catalan(n: int, mod: int) -> int:
    # C(2n, n) * inv(n+1)
    num = 1
    for i in range(n):
        num = num * (2 * n - i) % mod
        num = num * pow(i + 1, mod - 2, mod) % mod
    return num * pow(n + 1, mod - 2, mod) % mod
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Balanced parentheses / stack-sortable / Dyck words
- “Non-crossing,” triangulations, full binary trees with \(n\) internal nodes
- Recurrence that is clearly Cauchy product of the same sequence

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one: triangulation of \(n\)-gon is \(C_{n-2}\), not \(C_n\).
- Using `/ (n+1)` without modular inverse.
- Wrong modulus non-prime for inv.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Motzkin / Schröder numbers (extra patterns).
- Ballot numbers / Catalan triangle.
- Super Catalan / related — rare.

---

#### 11. Typical Problem Archetypes

1. Standard application: count valid parentheses strings length \(2n\).
2. Slightly disguised: count BSTs / binary trees.
3. Difficult: weighted Catalan / constraints on height.
4. Very difficult / advanced: q-Catalan, generatingfunctionology.

---

#### 12. Recognition & Identification Drills

1. Number of ways to triangulate a convex hexagon.
2. Count Dyck paths of semilength \(n\) mod \(10^9+7\).
3. Recurrence \(a_0=1,\ a_n=\sum a_i a_{n-1-i}\) — name \(a_n\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: Dyck / noncrossing / BST / triangulation counts
- Key invariant: \(c = 1 + x c^2\)
- Key formula: \(C_n = \frac{1}{n+1}C(2n,n)\)
- Complexity: \(O(1)\) with binomials
- Template to remember: `C(2n,n) * inv(n+1)`

---

---


---

<a id="topic-11"></a>
### 11. Stirling numbers

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Binomials, inclusion-exclusion, basic DP  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Binomials, inclusion-exclusion, basic DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

- **Stirling 2nd kind** \(S(n,k)\): ways to partition \(n\) labeled objects into \(k\) nonempty **unlabeled** subsets.  
- **Stirling 1st kind** \(s(n,k)\) / \(|s(n,k)|\): permutations of \(n\) with \(k\) cycles (signed vs unsigned).  
Surjections onto \(k\) labels: \(k! S(n,k) = \sum_{i=0}^{k} (-1)^{k-i} C(k,i) i^n\).

---

#### 4. Proof Sketches & Recurrences

Recurrences:  
\(S(n,k) = S(n-1,k-1) + k\, S(n-1,k)\),  
\(|s(n,k)| = |s(n-1,k-1)| + (n-1)|s(n-1,k)|\).  
Falling factorial: \(x^n = \sum_k S(n,k) (x)_k\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n^2)\) table
- Per-query / per-operation: \(O(1)\) lookup or \(O(k \log n)\) surjection formula
- Total: \(O(n^2)\)
- Memory: \(O(n^2)\) (or \(O(n)\) rolling)`

##### C++17 Template

```cpp
namespace stirling {
// Stirling 2nd kind table S[n][k], mod prime
vector<vector<int>> stirling2(int n, int mod) {
    vector<vector<int>> S(n + 1, vector<int>(n + 1));
    S[0][0] = 1;
    for (int i = 1; i <= n; ++i)
        for (int k = 1; k <= i; ++k)
            S[i][k] = (S[i - 1][k - 1] + (long long)k * S[i - 1][k]) % mod;
    return S;
}
// unsigned Stirling 1st kind c[n][k]
vector<vector<int>> stirling1_unsigned(int n, int mod) {
    vector<vector<int>> c(n + 1, vector<int>(n + 1));
    c[0][0] = 1;
    for (int i = 1; i <= n; ++i)
        for (int k = 1; k <= i; ++k)
            c[i][k] = (c[i - 1][k - 1] + (long long)(i - 1) * c[i - 1][k]) % mod;
    return c;
}
// surjections n -> k
int surjections(int n, int k, const binom::Comb& comb) {
    int mod = comb.mod;
    long long ans = 0;
    for (int i = 0; i <= k; ++i) {
        long long term = comb.C(k, i);
        term = term * comb.mod_pow(i, n) % mod;
        if ((k - i) & 1) ans = (ans - term) % mod;
        else ans = (ans + term) % mod;
    }
    if (ans < 0) ans += mod;
    return (int)ans; // = k! S(n,k)
}
} // namespace stirling
```

##### Python 3 Template

```python
def stirling2(n: int, mod: int):
    S = [[0] * (n + 1) for _ in range(n + 1)]
    S[0][0] = 1
    for i in range(1, n + 1):
        for k in range(1, i + 1):
            S[i][k] = (S[i - 1][k - 1] + k * S[i - 1][k]) % mod
    return S
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Partition people into \(k\) nonempty unlabeled teams
- “Onto functions” / functions with exactly \(k\) nonempty image sizes
- Cycle counts in permutations; rising/falling factorial basis change

---

#### 7. Contest WA / TLE / RE Traps

- Confusing labeled vs unlabeled partitions (\(k! S(n,k)\) vs \(S(n,k)\)).
- Mixing signed 1st kind with unsigned cycle counts.
- \(S(0,0)=1\) but \(S(n,0)=0\) for \(n>0\).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Bell numbers \(B_n = \sum_k S(n,k)\).
- r-Stirling, associated Stirling — rare.
- FFT / NTT for rows when \(n\) large and formula allows (advanced).

---

#### 11. Typical Problem Archetypes

1. Standard application: partitions into \(k\) nonempty subsets.
2. Slightly disguised: count functions with image size \(k\).
3. Difficult: DP mixing Stirling with other counts.
4. Very difficult / advanced: basis conversion of polynomials via Stirling.

---

#### 12. Recognition & Identification Drills

1. Ways to split \(n\) distinct people into \(k\) nonempty unlabeled rooms.
2. Number of permutations of \(n\) with exactly \(k\) cycles.
3. Compute \(k! S(n,k)\) via inclusion-exclusion without building \(S\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: set partitions / cycle counts / surjections
- Key invariant: \(S(n,k)=S(n-1,k-1)+k S(n-1,k)\)
- Key formula: \(k! S(n,k)=\sum (-1)^{k-i}C(k,i)i^n\)
- Complexity: \(O(n^2)\) table
- Template to remember: 2D DP recurrence above

---

---


---

<a id="topic-12"></a>
### 12. Burnside's lemma

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Group actions intuition, modular arithmetic / counting, gcd often  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Group actions intuition, modular arithmetic / counting, gcd often

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

To count objects up to symmetry, average the number of colorings fixed by each group element:
\[
|X/G| = \frac{1}{|G|} \sum_{g \in G} \mathrm{Fix}(g).
\]
A coloring is fixed by \(g\) iff it is constant on every cycle of \(g\)’s permutation of cells. So \(\mathrm{Fix}(g) = c^{\mathrm{cycles}(g)}\) for \(c\) colors on a set acted on by \(g\).

---

#### 4. Proof Sketches & Recurrences

Orbit-stabilizer → class equation form yields Burnside. Practical recipe: list all \(g\), factor permutation into cycles on the domain, require equal colors on each cycle.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: group-dependent
- Per-query / per-operation: \(O(|G| \cdot \mathrm{cost}(\mathrm{cycles}))\)
- Total: often \(O(n \log n)\) for cyclic necklaces via gcd
- Memory: \(O(1)\)–\(O(|G|)\)`

##### C++17 Template

```cpp
namespace burnside {
// colorings of n beads on a necklace under rotation (cyclic group), c colors
// Fix(rotation by k) = c^{gcd(k,n)}
long long necklaces_rotations(int n, int c, int mod) {
    auto mod_pow = [&](long long a, long long e) {
        long long r = 1 % mod;
        for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
        return r;
    };
    long long sum = 0;
    for (int k = 0; k < n; ++k) {
        int g = std::gcd(k, n);
        sum += mod_pow(c, g);
        if (sum >= mod) sum -= mod;
    }
    return sum * mod_pow(n, mod - 2) % mod; // / |G| = / n
}
// generic: pass list of cycle_counts for each group element
long long burnside_avg(const vector<int>& cycles, int colors, int mod) {
    auto mod_pow = [&](long long a, long long e) {
        long long r = 1 % mod;
        for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
        return r;
    };
    long long sum = 0;
    for (int cy : cycles) {
        sum += mod_pow(colors, cy);
        if (sum >= mod) sum -= mod;
    }
    return sum * mod_pow((int)cycles.size(), mod - 2) % mod;
}
} // namespace burnside
```

##### Python 3 Template

```python
import math
def necklaces_rotations(n: int, c: int, mod: int) -> int:
    s = 0
    for k in range(n):
        s = (s + pow(c, math.gcd(k, n), mod)) % mod
    return s * pow(n, mod - 2, mod) % mod
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Up to rotation,” “rotations and reflections,” necklace without full Pólya toolkit
- Cube face colorings, grid colorings under dihedral group
- Explicit small group \(G\) you can enumerate

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting reflections when the problem allows flipping (dihedral vs cyclic).
- Dividing by \(|G|\) without modular inverse (or when answer isn’t integer mod \(p\) — usually it is).
- Wrong cycle index for a symmetry (draw the permutation!).

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Weighted Burnside (generating functions per cycle).
- Group acting on functions / graphs (count graphs up to iso — hard).
- Step toward Pólya cycle index (next).

---

#### 11. Typical Problem Archetypes

1. Standard application: beads on a loop, rotations only.
2. Slightly disguised: paint cube vertices/faces up to rotation.
3. Difficult: dihedral group + restricted color multiplicities.
4. Very difficult / advanced: Burnside on large implied groups with smart cycle formulas.

---

#### 12. Recognition & Identification Drills

1. \(n\) beads, \(c\) colors, count distinct under rotation.
2. Color \(2\times 2\) grid with \(c\) colors up to rotation.
3. Same as (1) but flips allowed — what changes?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: count up to explicit symmetry group
- Key invariant: fixed colorings constant on cycles
- Key formula: \(\frac{1}{|G|}\sum_g c^{\mathrm{cyc}(g)}\)
- Complexity: \(O(|G|)\) typical
- Template to remember: average Fix; rotations → \(c^{\gcd(k,n)}\)

---

---


---

<a id="topic-13"></a>
### 13. Pólya enumeration

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** Burnside's lemma, generating functions basics, cycle index  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Burnside's lemma, generating functions basics, cycle index

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Pólya packages Burnside into the **cycle index** polynomial of the group action. Substituting \(x_i = 1+w^i+\cdots\) (or \(x_i = c\) for ordinary colors) generates inventories of colorings by color counts. For necklaces, the cycle index of \(C_n\) / \(D_n\) yields classic formulas; use when you need the generating function, not only the total count.

---

#### 4. Proof Sketches & Recurrences

Cycle index:
\[
P_G(x_1,\ldots,x_n) = \frac{1}{|G|} \sum_{g\in G} \prod_{i=1}^{n} x_i^{c_i(g)},
\]
where \(c_i(g)\) = number of cycles of length \(i\).  
Ordinary \(c\)-color count: set every \(x_i = c\).  
Pattern inventory: set \(x_i = a^i + b^i + \cdots\) for color weights.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: group cycle types
- Per-query / per-operation: evaluate cycle index / Burnside sum
- Total: often \(O(n)\)–\(O(n \log n)\) for \(C_n\)
- Memory: \(O(1)\) or GF tables`

##### C++17 Template

```cpp
namespace polya {
// Total c-color necklaces under C_n: P_G(c,...,c) == Burnside average
long long cyclic_total(int n, int c, int mod) {
    auto mod_pow = [&](long long a, long long e) {
        long long r = 1 % mod;
        for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
        return r;
    };
    long long sum = 0;
    for (int k = 0; k < n; ++k) {
        sum += mod_pow(c, std::gcd(k, n));
        if (sum >= mod) sum -= mod;
    }
    return sum * mod_pow(n, mod - 2) % mod;
}

// Binary necklaces length n with exactly k ones, rotations only (cycle index inventory).
// Each rotation by r has g=gcd(r,n) cycles of length n/g; fixed iff cyc_len | k.
long long binary_fixed_k(int n, int k, int mod, const binom::Comb& comb) {
    long long sum = 0;
    for (int r = 0; r < n; ++r) {
        int g = std::gcd(r, n);
        int cyc_len = n / g;
        if (k % cyc_len == 0) {
            int ones_cycles = k / cyc_len;
            if (ones_cycles >= 0 && ones_cycles <= g)
                sum = (sum + comb.C(g, ones_cycles)) % mod;
        }
    }
    return sum * comb.mod_pow(n, mod - 2) % mod;
}
// Dihedral: add reflection conjugacy types (odd n: n flips, (n-1)/2 + 1 cycle structures).
} // namespace polya
```

##### Python 3 Template

```python
import math
# Total c-color necklaces under rotation = Burnside (Pólya with x_i=c)
def polya_cyclic_total(n, c, mod):
    s = sum(pow(c, math.gcd(k, n), mod) for k in range(n)) % mod
    return s * pow(n, mod - 2, mod) % mod
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Necklace polynomial,” bracelet, inventory of color multiplicities
- Editorial mentions cycle index \(P_G(x_1,\ldots,x_n)\)
- Burnside with bookkeeping of how many of each color

---

#### 7. Contest WA / TLE / RE Traps

- Using cyclic formula when the problem is dihedral (bracelets).
- Substituting \(x_i = c\) vs \(x_i = \sum \mathrm{color}^i\) incorrectly.
- Inventory coefficient off-by-cycle-length constraints.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Dihedral cycle index (reflections differ for odd/even \(n\)).
- Pólya for graph edges (counting graphs by edges — niche).
- Prefer plain Burnside unless inventory GF required.

---

#### 11. Typical Problem Archetypes

1. Standard application: necklace color counts via cycle index.
2. Slightly disguised: bracelets (flips) with color multiplicity.
3. Difficult: multivariate inventory with constraints.
4. Very difficult / advanced: species / advanced enumeration.

---

#### 12. Recognition & Identification Drills

1. Generate the cycle index of \(C_4\) and evaluate at \(x_i=c\).
2. Count binary necklaces of length \(n\) with exactly \(k\) ones (rotations).
3. When does Pólya reduce to ordinary Burnside with \(\mathrm{Fix}=c^{\mathrm{cyc}}\)?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: Burnside + pattern inventory / necklace polynomials
- Key invariant: cycle index encodes all Fix generating functions
- Key formula: \(P_G\); total colors \(P_G(c,\ldots,c)\)
- Complexity: like Burnside on cycle types
- Template to remember: cycle index → substitute → average

---

---


---

<a id="topic-14"></a>
### 14. Generating functions basics

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2800 | **Frequency:** Occasional  
> **Prerequisites:** Binomials, recurrences, optional FFT/NTT (see later FFT section)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2800
- Prerequisites: Binomials, recurrences, optional FFT/NTT (see later FFT section)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

A generating function packs a sequence into an algebra object so recurrence ↔ equation, convolution ↔ product, and closed forms fall out.  
- **OGF** \(A(x)=\sum a_n x^n\): unlabeled / combination-style, products for disjoint union of structures.  
- **EGF** \(A(x)=\sum a_n \frac{x^n}{n!}\): labeled structures; \(\exp\) for sets of components.  
Contest use: write the GF, extract coefficients via recurrence, binomial theorem, or NTT — not formal Laurent series theory.

---

#### 4. Proof Sketches & Recurrences

- Sum: \([x^n](A+B)=a_n+b_n\)
- Product OGF: \([x^n]AB = \sum_{k=0}^n a_k b_{n-k}\)
- EGF product: labeled merge \(\sum C(n,k) a_k b_{n-k}\)
- Geometric: \(\frac{1}{1-x} = \sum x^n\); \(\frac{1}{(1-x)^{k+1}} = \sum C(n+k,k) x^n\)
- Catalan: \(c=1+xc^2\) as earlier

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: model-dependent
- Per-query / per-operation: naive mul \(O(n^2)\); NTT \(O(n\log n)\) (elsewhere)
- Total: truncate at needed degree
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
namespace gf_basic {
using i64 = long long;
// multiply two OGFs truncated to degree < n (naive); use NTT when n large
vector<i64> mul_naive(const vector<i64>& a, const vector<i64>& b, int mod, int n) {
    vector<i64> c(n);
    for (int i = 0; i < (int)a.size() && i < n; ++i)
        for (int j = 0; j < (int)b.size() && i + j < n; ++j)
            c[i + j] = (c[i + j] + a[i] * b[j]) % mod;
    return c;
}
// extract recurrence a[n] = sum_{i=1}^k c[i]*a[n-i] with a[0..k-1] given — linear
vector<i64> linrec(vector<i64> init, const vector<i64>& c, int n, int mod) {
    int k = (int)c.size();
    vector<i64> a(n);
    for (int i = 0; i < (int)init.size() && i < n; ++i) a[i] = init[i];
    for (int i = (int)init.size(); i < n; ++i) {
        i64 s = 0;
        for (int j = 1; j <= k && j <= i; ++j)
            s = (s + c[j - 1] * a[i - j]) % mod;
        a[i] = s;
    }
    return a;
}
i64 mod_pow(i64 a, i64 e, int mod) {
    i64 r = 1 % mod;
    for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
    return r;
}
// [x^0..n] (1+x)^m mod prime via successive ratios
vector<i64> binom_pow_series(long long m, int n, int mod) {
    vector<i64> a(n + 1);
    a[0] = 1;
    for (int i = 0; i < n; ++i) {
        a[i + 1] = a[i] * ((m - i) % mod + mod) % mod;
        a[i + 1] = a[i + 1] * mod_pow(i + 1, mod - 2, mod) % mod;
    }
    return a;
}
} // namespace gf_basic
```

##### Python 3 Template

```python
def mul_naive(a, b, mod, n):
    c = [0] * n
    for i, ai in enumerate(a):
        if i >= n:
            break
        for j, bj in enumerate(b):
            if i + j >= n:
                break
            c[i + j] = (c[i + j] + ai * bj) % mod
    return c
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Convolution in counting → product of GFs
- Partition into unordered components → \(\exp\) on EGF
- “Number of ways as coefficient of \(x^n\)”
- Linear recurrence → rational OGF

---

#### 7. Contest WA / TLE / RE Traps

- OGF vs EGF mixups (forgetting \(n!\) factors).
- Truncation degree too small for the convolution.
- Treating formal identity as numeric without mod inverse for divisions.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Dirichlet GF for multiplicative problems (number theory section).
- Ordinary partition GF \(\prod 1/(1-x^k)\).
- Full FPS toolkit (exp, log, inverse) — Niche / later NTT section.

---

#### 11. Typical Problem Archetypes

1. Standard application: knapsack GF \(\prod (1+x^{w_i})\) coefficient.
2. Slightly disguised: rewrite recurrence as rational GF.
3. Difficult: EGF for labeled graphs / permutations components.
4. Very difficult / advanced: algebraic GF + Lagrange inversion (Catalan-like).

---

#### 12. Recognition & Identification Drills

1. Ways to make sum \(n\) with unlimited coins \(\{1,5,10\}\) — write OGF.
2. Labeled sets of cycles (= permutations) → EGF \(\exp(\log\frac{1}{1-x})\).
3. From \(a_n = \sum_{k=0}^{n} a_k a_{n-1-k}\) recover Catalan GF equation.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: convolutions, structure decompositions, recurrence → closed form
- Key invariant: product ↔ convolution (OGF/EGF variants)
- Key formula: \(\frac{1}{(1-x)^{k+1}}=\sum C(n+k,k)x^n\)
- Complexity: \(O(n^2)\) naive; NTT if needed
- Template to remember: write GF equation → extract coeffs

---

## Mini drills (combinatorics half)

1. Implement `Comb` + `Lucas` and verify \(C(n,k) \bmod p\) for random \(n < p\) and \(n > p\).
2. Derive which Catalan index counts triangulations of an \(n\)-gon.
3. One Burnside rotation-only necklace; extend to flips only if time.

Back to [`13-bit-combinatorics.md`](13-bit-combinatorics.md).

---


---

<a id="topic-15"></a>
### 15. Recognition shortcuts

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1/Div2 Hard
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Bitwise operations, Submask enumeration, SOS DP, Fast Walsh-Hadamard Transform (FWHT)
- Tradeoff: Recognizing the exact bitwise algorithm immediately from $N$ and problem constraints.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Bitwise problem constraints form an infallible recognition matrix: 1) $N \le 20 \implies$ Iterate all submasks $\sum_{mask} 2^{|mask|} = 3^N \approx 3.5 \times 10^9$ (or $N \le 16 \implies 3^{16} = 4.3 \times 10^7$). 2) $N \le 24 \implies$ Sum Over Subsets (SOS) DP in $\mathcal{O}(N \cdot 2^N) \approx 4 \times 10^8$ operations. 3) $N \le 20$ with bitwise AND/OR/XOR convolution $c_k = \sum_{i \star j = k} a_i b_j \implies$ Fast Walsh-Hadamard Transform (FWHT) in $\mathcal{O}(N \cdot 2^N)$. 4) Subset Convolution (enforcing disjoint sets $i \cup j = k$ with $i \cap j = \emptyset$) $\implies$ Ranked SOS DP in $\mathcal{O}(N^2 \cdot 2^N)$.

---

#### 4. Proof Sketches & Recurrences

Submask iteration loop `for (int sub = mask; sub; sub = (sub - 1) & mask)` visits each pair $(sub, mask)$ such that $sub \subseteq mask$. The total number of iterations is $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$. SOS DP computes prefix sums along Boolean hypercube dimensions: iterating coordinate bit $i$ from $0$ to $N-1$ updates $dp[mask] += dp[mask \oplus 2^i]$ if bit $i$ is set, evaluating all subset sums in exactly $N \cdot 2^N$ operations.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Bitwise Recognition Toolkit: Submask Enumeration & SOS DP
#include <bits/stdc++.h>
using namespace std;

// 1. All submasks enumeration: O(3^N)
void enumerate_submasks(int n) {
    for (int mask = 0; mask < (1 << n); ++mask) {
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
            // process submask 'sub' of 'mask'
        }
    }
}

// 2. Sum Over Subsets (SOS) DP: O(N * 2^N)
void sos_dp(int n, vector<int>& f) {
    for (int i = 0; i < n; ++i) {
        for (int mask = 0; mask < (1 << n); ++mask) {
            if (mask & (1 << i)) {
                f[mask] += f[mask ^ (1 << i)];
            }
        }
    }
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Constraints state $N \le 20$ or $N \le 24$ (universal signal for bitmask / SOS DP).
- Count pairs $(i, j)$ such that $a_i \text{ AND } a_j = 0$ (SOS DP on complement mask $\sim a_i$).
- Finding shortest Hamiltonian path / Traveling Salesperson Problem on $N \le 20$ vertices.
- Set cover or partition problems where items are represented as bit flags.

---

#### 7. Contest WA / TLE / RE Traps

- Submask iteration infinite loop: using `sub >= 0` instead of `sub > 0` causes `(0 - 1) & mask = mask`, looping infinitely.
- Loop order in SOS DP: outer loop MUST iterate over dimension $i \in [0, N-1]$ and inner loop over masks to correctly accumulate multi-dimensional prefix sums.
- Bitwise operator precedence: `1 << n - 1` evaluates as `1 << (n - 1)`. Always use parentheses `(1 << n) - 1` and `(mask & (1 << i))`.
- Integer overflow: using 32-bit `int` for bit shifts when $N \ge 31$; use `1LL << i`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---


---

<a id="topic-16"></a>
### 16. High-ROI (drill first)

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Precomputed factorials, SOS DP

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Drill the standard combinatorial toolkit: $\binom{N}{K} \pmod P$, Catalan numbers $C_n = \frac{1}{n+1} \binom{2n}{n}$ (valid bracket sequences, non-intersecting chords, binary tree topologies), and SOS DP submask accumulations.

---

#### 4. Proof Sketches & Recurrences

Catalan recurrence: $C_{n+1} = \sum_{i=0}^n C_i C_{n-i} = \frac{2(2n+1)}{n+2} C_n$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Catalan Numbers computation
#include <bits/stdc++.h>
using namespace std;
// Catalan C_n = nCr(2n, n) / (n + 1)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Valid Dyck paths that do not cross the diagonal.
- Number of distinct full binary trees with $n+1$ leaves.

---

#### 7. Contest WA / TLE / RE Traps

- Dividing by $n+1$ without computing modular inverse under composite modulo.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---


---

<a id="topic-17"></a>
### 17. Situational (learn after High-ROI)

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: FWHT, XOR / AND / OR transforms

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Fast Walsh-Hadamard Transform (FWHT) performs bitwise convolutions $C[k] = \sum_{i \oplus j = k} A[i] B[j]$ in $\mathcal{O}(N \cdot 2^N)$ for $\oplus \in \{\text{XOR}, \text{AND}, \text{OR}\}$.

---

#### 4. Proof Sketches & Recurrences

Hadamard matrix $H_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. Applying tensor product $H_{2^N} = H_2^{\otimes N}$ diagonalizes XOR convolution.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Fast Walsh-Hadamard Transform (FWHT) for XOR Convolution
#include <bits/stdc++.h>
using namespace std;

void fwht_xor(vector<long long>& a, bool invert) {
    int n = a.size();
    for (int len = 1; 2 * len <= n; len <<= 1) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; ++j) {
                long long u = a[i + j], v = a[i + len + j];
                a[i + j] = u + v;
                a[i + len + j] = u - v;
            }
        }
    }
    if (invert) for (auto& x : a) x /= n;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Computing all pairs $(i, j)$ with $A[i] \oplus A[j] = X$ across an array.
- Subset convolution combining size and mask state.

---

#### 7. Contest WA / TLE / RE Traps

- Dividing by $N$ without modular inverse when FWHT is computed modulo $P$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---


---

<a id="topic-18"></a>
### 18. Rarely worth early / Niche

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Burnside's Lemma, Polya Enumeration Theorem

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Burnside's Lemma and Polya Enumeration count non-isomorphic colorings and structures under group actions (rotations, reflections, automorphisms): $|X/G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

---

#### 4. Proof Sketches & Recurrences

Each symmetry group element $g \in G$ has a cycle decomposition; coloring assignments invariant under $g$ assign uniform color to all elements in each cycle.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Burnside's Lemma for Necklaces with K colors and N beads
#include <bits/stdc++.h>
using namespace std;
// |X/G| = (1/N) * sum_{i=0}^{N-1} K^gcd(i, N)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Counting unique bracelets, cubes, or graphs under rotational equivalence.

---

#### 7. Contest WA / TLE / RE Traps

- Missing reflection elements when symmetries include dihedral group $D_N$ rather than cyclic group $C_N$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---


---

<a id="topic-19"></a>
### 19. What to drill this week

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Combinatorics & Bit manipulation toolkit

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

##### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

##### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

##### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

##### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

#### 3. Core Intuition & Problem Framing

Drill: (1) Fast combination queries, (2) Submask iteration loops, (3) SOS DP prefix table, (4) Inversion parity checks, and (5) Nim-sum game reductions.

---

#### 4. Proof Sketches & Recurrences

SOS DP computes $F[\text{mask}] = \sum_{sub \subseteq mask} A[sub]$ in exactly $N \cdot 2^N$ operations.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Weekly Combinatorics & Bit Drill Scaffold
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Fast bit operations inside tightly nested DP loops.

---

#### 7. Contest WA / TLE / RE Traps

- Left-shift overflow: `1 << i` instead of `1LL << i` when $i \ge 31$.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---


---
