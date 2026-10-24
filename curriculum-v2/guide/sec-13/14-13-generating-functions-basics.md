# 14. Generating functions basics

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2800 | **Frequency:** Occasional  
> **Prerequisites:** Binomials, recurrences, optional FFT/NTT (see later FFT section)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2800
- Prerequisites: Binomials, recurrences, optional FFT/NTT (see later FFT section)

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

A generating function packs a sequence into an algebra object so recurrence ↔ equation, convolution ↔ product, and closed forms fall out.  
- **OGF** \(A(x)=\sum a_n x^n\): unlabeled / combination-style, products for disjoint union of structures.  
- **EGF** \(A(x)=\sum a_n \frac{x^n}{n!}\): labeled structures; \(\exp\) for sets of components.  
Contest use: write the GF, extract coefficients via recurrence, binomial theorem, or NTT — not formal Laurent series theory.

---

## 4. Proof Sketches & Recurrences

- Sum: \([x^n](A+B)=a_n+b_n\)
- Product OGF: \([x^n]AB = \sum_{k=0}^n a_k b_{n-k}\)
- EGF product: labeled merge \(\sum C(n,k) a_k b_{n-k}\)
- Geometric: \(\frac{1}{1-x} = \sum x^n\); \(\frac{1}{(1-x)^{k+1}} = \sum C(n+k,k) x^n\)
- Catalan: \(c=1+xc^2\) as earlier

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: model-dependent
- Per-query / per-operation: naive mul \(O(n^2)\); NTT \(O(n\log n)\) (elsewhere)
- Total: truncate at needed degree
- Memory: \(O(n)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Convolution in counting → product of GFs
- Partition into unordered components → \(\exp\) on EGF
- “Number of ways as coefficient of \(x^n\)”
- Linear recurrence → rational OGF

---

## 7. Contest WA / TLE / RE Traps

- OGF vs EGF mixups (forgetting \(n!\) factors).
- Truncation degree too small for the convolution.
- Treating formal identity as numeric without mod inverse for divisions.

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

- Dirichlet GF for multiplicative problems (number theory section).
- Ordinary partition GF \(\prod 1/(1-x^k)\).
- Full FPS toolkit (exp, log, inverse) — Niche / later NTT section.

---

## 11. Typical Problem Archetypes

1. Standard application: knapsack GF \(\prod (1+x^{w_i})\) coefficient.
2. Slightly disguised: rewrite recurrence as rational GF.
3. Difficult: EGF for labeled graphs / permutations components.
4. Very difficult / advanced: algebraic GF + Lagrange inversion (Catalan-like).

---

## 12. Recognition & Identification Drills

1. Ways to make sum \(n\) with unlimited coins \(\{1,5,10\}\) — write OGF.
2. Labeled sets of cycles (= permutations) → EGF \(\exp(\log\frac{1}{1-x})\).
3. From \(a_n = \sum_{k=0}^{n} a_k a_{n-1-k}\) recover Catalan GF equation.

---

## 13. Fast-Lookup Cheat Sheet

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
