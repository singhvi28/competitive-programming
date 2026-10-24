# Catalan numbers

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2100 | **Frequency:** Occasional  
> **Prerequisites:** Binomial coefficients, modular inverse  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1500–2100
- Prerequisites: Binomial coefficients, modular inverse

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

The Catalan number \(C_n = \frac{1}{n+1} C(2n, n) = C(2n,n) - C(2n, n-1)\) counts the same structure under many costumes: valid parentheses, Dyck paths, BSTs on \(n\) keys, triangulations of convex \((n+2)\)-gon, noncrossing partitions, monotonic lattice paths below diagonal. Recurrence \(C_0=1\), \(C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}\).

---

## 4. Proof Sketches & Recurrences

Ballot theorem → \(C_n = \frac{1}{n+1}C(2n,n)\).  
OGF \(c(x) = \sum C_n x^n = \frac{1 - \sqrt{1-4x}}{2x}\) (\(c(0)=1\)), satisfies \(c = 1 + x c^2\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: binomial tables \(O(N)\) or DP \(O(n^2)\)
- Per-query / per-operation: \(O(1)\) with tables
- Total: \(O(N)\) or \(O(n^2)\)
- Memory: \(O(N)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Balanced parentheses / stack-sortable / Dyck words
- “Non-crossing,” triangulations, full binary trees with \(n\) internal nodes
- Recurrence that is clearly Cauchy product of the same sequence

---

## 7. Contest WA / TLE / RE Traps

- Off-by-one: triangulation of \(n\)-gon is \(C_{n-2}\), not \(C_n\).
- Using `/ (n+1)` without modular inverse.
- Wrong modulus non-prime for inv.

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

- Motzkin / Schröder numbers (extra patterns).
- Ballot numbers / Catalan triangle.
- Super Catalan / related — rare.

---

## 11. Typical Problem Archetypes

1. Standard application: count valid parentheses strings length \(2n\).
2. Slightly disguised: count BSTs / binary trees.
3. Difficult: weighted Catalan / constraints on height.
4. Very difficult / advanced: q-Catalan, generatingfunctionology.

---

## 12. Recognition & Identification Drills

1. Number of ways to triangulate a convex hexagon.
2. Count Dyck paths of semilength \(n\) mod \(10^9+7\).
3. Recurrence \(a_0=1,\ a_n=\sum a_i a_{n-1-i}\) — name \(a_n\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: Dyck / noncrossing / BST / triangulation counts
- Key invariant: \(c = 1 + x c^2\)
- Key formula: \(C_n = \frac{1}{n+1}C(2n,n)\)
- Complexity: \(O(1)\) with binomials
- Template to remember: `C(2n,n) * inv(n+1)`

---

---
