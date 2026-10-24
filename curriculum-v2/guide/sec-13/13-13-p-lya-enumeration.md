# 13. Pólya enumeration

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** Burnside's lemma, generating functions basics, cycle index  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Burnside's lemma, generating functions basics, cycle index

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

Pólya packages Burnside into the **cycle index** polynomial of the group action. Substituting \(x_i = 1+w^i+\cdots\) (or \(x_i = c\) for ordinary colors) generates inventories of colorings by color counts. For necklaces, the cycle index of \(C_n\) / \(D_n\) yields classic formulas; use when you need the generating function, not only the total count.

---

## 4. Proof Sketches & Recurrences

Cycle index:
\[
P_G(x_1,\ldots,x_n) = \frac{1}{|G|} \sum_{g\in G} \prod_{i=1}^{n} x_i^{c_i(g)},
\]
where \(c_i(g)\) = number of cycles of length \(i\).  
Ordinary \(c\)-color count: set every \(x_i = c\).  
Pattern inventory: set \(x_i = a^i + b^i + \cdots\) for color weights.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: group cycle types
- Per-query / per-operation: evaluate cycle index / Burnside sum
- Total: often \(O(n)\)–\(O(n \log n)\) for \(C_n\)
- Memory: \(O(1)\) or GF tables`

### C++17 Template

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

### Python 3 Template

```python
import math
# Total c-color necklaces under rotation = Burnside (Pólya with x_i=c)
def polya_cyclic_total(n, c, mod):
    s = sum(pow(c, math.gcd(k, n), mod) for k in range(n)) % mod
    return s * pow(n, mod - 2, mod) % mod
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Necklace polynomial,” bracelet, inventory of color multiplicities
- Editorial mentions cycle index \(P_G(x_1,\ldots,x_n)\)
- Burnside with bookkeeping of how many of each color

---

## 7. Contest WA / TLE / RE Traps

- Using cyclic formula when the problem is dihedral (bracelets).
- Substituting \(x_i = c\) vs \(x_i = \sum \mathrm{color}^i\) incorrectly.
- Inventory coefficient off-by-cycle-length constraints.

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

- Dihedral cycle index (reflections differ for odd/even \(n\)).
- Pólya for graph edges (counting graphs by edges — niche).
- Prefer plain Burnside unless inventory GF required.

---

## 11. Typical Problem Archetypes

1. Standard application: necklace color counts via cycle index.
2. Slightly disguised: bracelets (flips) with color multiplicity.
3. Difficult: multivariate inventory with constraints.
4. Very difficult / advanced: species / advanced enumeration.

---

## 12. Recognition & Identification Drills

1. Generate the cycle index of \(C_4\) and evaluate at \(x_i=c\).
2. Count binary necklaces of length \(n\) with exactly \(k\) ones (rotations).
3. When does Pólya reduce to ordinary Burnside with \(\mathrm{Fix}=c^{\mathrm{cyc}}\)?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: Burnside + pattern inventory / necklace polynomials
- Key invariant: cycle index encodes all Fix generating functions
- Key formula: \(P_G\); total colors \(P_G(c,\ldots,c)\)
- Complexity: like Burnside on cycle types
- Template to remember: cycle index → substitute → average

---

---
