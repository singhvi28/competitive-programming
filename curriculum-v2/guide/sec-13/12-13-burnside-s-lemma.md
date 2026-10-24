# Burnside's lemma

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Group actions intuition, modular arithmetic / counting, gcd often  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Group actions intuition, modular arithmetic / counting, gcd often

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

To count objects up to symmetry, average the number of colorings fixed by each group element:
\[
|X/G| = \frac{1}{|G|} \sum_{g \in G} \mathrm{Fix}(g).
\]
A coloring is fixed by \(g\) iff it is constant on every cycle of \(g\)’s permutation of cells. So \(\mathrm{Fix}(g) = c^{\mathrm{cycles}(g)}\) for \(c\) colors on a set acted on by \(g\).

---

## 4. Proof Sketches & Recurrences

Orbit-stabilizer → class equation form yields Burnside. Practical recipe: list all \(g\), factor permutation into cycles on the domain, require equal colors on each cycle.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: group-dependent
- Per-query / per-operation: \(O(|G| \cdot \mathrm{cost}(\mathrm{cycles}))\)
- Total: often \(O(n \log n)\) for cyclic necklaces via gcd
- Memory: \(O(1)\)–\(O(|G|)\)`

### C++17 Template

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

### Python 3 Template

```python
import math
def necklaces_rotations(n: int, c: int, mod: int) -> int:
    s = 0
    for k in range(n):
        s = (s + pow(c, math.gcd(k, n), mod)) % mod
    return s * pow(n, mod - 2, mod) % mod
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Up to rotation,” “rotations and reflections,” necklace without full Pólya toolkit
- Cube face colorings, grid colorings under dihedral group
- Explicit small group \(G\) you can enumerate

---

## 7. Contest WA / TLE / RE Traps

- Forgetting reflections when the problem allows flipping (dihedral vs cyclic).
- Dividing by \(|G|\) without modular inverse (or when answer isn’t integer mod \(p\) — usually it is).
- Wrong cycle index for a symmetry (draw the permutation!).

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

- Weighted Burnside (generating functions per cycle).
- Group acting on functions / graphs (count graphs up to iso — hard).
- Step toward Pólya cycle index (next).

---

## 11. Typical Problem Archetypes

1. Standard application: beads on a loop, rotations only.
2. Slightly disguised: paint cube vertices/faces up to rotation.
3. Difficult: dihedral group + restricted color multiplicities.
4. Very difficult / advanced: Burnside on large implied groups with smart cycle formulas.

---

## 12. Recognition & Identification Drills

1. \(n\) beads, \(c\) colors, count distinct under rotation.
2. Color \(2\times 2\) grid with \(c\) colors up to rotation.
3. Same as (1) but flips allowed — what changes?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: count up to explicit symmetry group
- Key invariant: fixed colorings constant on cycles
- Key formula: \(\frac{1}{|G|}\sum_g c^{\mathrm{cyc}(g)}\)
- Complexity: \(O(|G|)\) typical
- Template to remember: average Fix; rotations → \(c^{\gcd(k,n)}\)

---

---
