# Bitmask tricks

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–2000 | **Frequency:** Very Common  
> **Prerequisites:** integers, binary representation, basic loops  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–2000
- Prerequisites: integers, binary representation, basic loops

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

## 3. Core Intuition & Problem Framing

A mask is a set. Arithmetic on two’s-complement integers implements set ops in \(O(1)\): `&` intersection, `|` union, `^` symmetric difference, `~` complement (careful with width). The single most useful identity is `x & -x` = lowest set bit (LSB) as a power of two — it peels a set one element at a time without scanning all bits.

---

## 4. Proof Sketches & Recurrences

- LSB: in two’s complement, `-x = ~x + 1`, so `x & -x` keeps only the trailing 1.
- Clear LSB: `x &= x - 1`.
- Iterate bits: `for (int m = x; m; m &= m - 1) { int b = __builtin_ctz(m); ... }`.
- Subset of \([0..n)\): masks in `[0, 1<<n)`.
- Bit-reversal / Gray: see Gray code topic.
- Popcount parity: `__builtin_parity`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(1)\) or \(O(\mathrm{popcount})\) to iterate bits
- Total: problem-dependent
- Memory: \(O(1)\) extras`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- “Subset of \(n \le 20\) items,” flags, presence/absence
- Need popcount, next permutation of bits, iterate set bits only
- Coordinate compression into bitsets / bit-DP transitions

---

## 7. Contest WA / TLE / RE Traps

- Using `1 << n` when `n == 31` → UB in signed 32-bit; use `1LL << n` or unsigned.
- `~mask` without `& ((1<<n)-1)` → infinite high bits.
- `__builtin_ctz(0)` undefined — guard empty masks.
- Signed right shift for arithmetic when you wanted logical.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

## 10. Algorithmic Variants & Advanced Extensions

- 64-bit / `__int128` masks; arrays of `uint64_t` for \(n > 64\).
- `std::bitset<N>` for heavy bitset DP (AND/OR shifts).
- Builtins: `__builtin_mul_overflow` rarely mixed in.

---

## 11. Typical Problem Archetypes

1. Standard application: count subsets with property via bit-DP.
2. Slightly disguised: compress \(n \le 20\) boolean attributes into mask keys.
3. Difficult: bitset optimized transitions \(O(n^2 / 64)\).
4. Very difficult / advanced: meet-in-the-middle on masks + hashing.

---

## 12. Recognition & Identification Drills

1. Among \(n \le 20\) tasks, choose a subset maximizing value with conflict pairs.
2. Given integers, find a nonempty subset whose XOR is 0 (small \(n\)).
3. Process only set bits of a 64-bit mask without looping 0..63 blindly.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: any \(n \le 20\)–22 set / flag state
- Key invariant: mask ↔ subset bijection
- Key formula: `x & -x` LSB; `x &= x-1` clear LSB
- Complexity: bit ops \(O(1)\); iterate bits \(O(\mathrm{pop})\)
- Template to remember: `for (int m = x; m; m &= m - 1)`

---

---
