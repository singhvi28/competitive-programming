# 7. Fast subset convolution concepts

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** Niche | **Rating Range:** 2500–3200 | **Frequency:** Rare  
> **Prerequisites:** SOS DP (§04), FWT/WHT, popcount rankings  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2500–3200
- Prerequisites: SOS DP (§04), FWT/WHT, popcount rankings

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

Subset convolution (cover product with disjoint union):
\[
(f * g)(S) = \sum_{A \subseteq S} f(A)\, g(S \setminus A)
\]
(equivalently sum over disjoint \(A \sqcup B = S\)). Naive \(O(3^n)\). Fast methods use **ranked** zeta: let \(f_k[S] = f[S]\) if \(\mathrm{pop}(S)=k\) else 0, SOS-transform each layer, pointwise multiply with convolution on ranks \(h_k = \sum_{i+j=k} F_i G_j\), then Möbius invert — \(O(n^2 2^n)\).

---

## 4. Proof Sketches & Recurrences

1. Rank: \(f_i[S] = [\mathrm{pop}(S)=i] f[S]\).
2. \(\hat f_i = \zeta f_i\) (SOS subset-sum transform).
3. \(\hat h_k[S] = \sum_{i=0}^{k} \hat f_i[S] \hat g_{k-i}[S]\).
4. \(h_k = \mu \hat h_k\); answer \(h[S] = h_{\mathrm{pop}(S)}[S]\).  
Correctness: zeta turns disjoint convolutions into products on the lattice after ranking.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(n^2 2^n)\)
- Total: usually one convolution
- Memory: \(O(n 2^n)\)`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Editorial says “subset convolution” / “disjoint union convolution”
- DP combining two subset functions with empty intersection
- \(n \le 20\) but \(3^n\) TLE while \(n^2 2^n\) fits

---

## 7. Contest WA / TLE / RE Traps

- Forgetting rank (plain FWT XOR ≠ subset convolution).
- Modular reduction missing in accumulators → overflow.
- Using OR-convolution when disjointness is required.

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

- Cover product \(\sum_{A \cup B = S} f(A)g(B)\) via different transforms.
- Constrained popcount / colored subset conv.
- Niche: keep as editorial vocabulary, implement only when forced.

---

## 11. Typical Problem Archetypes

1. Standard application: disjoint merge of two subset DPs.
2. Slightly disguised: counting perfect matchings-style via subsets (rare).
3. Difficult: repeated convolutions / exp on subset lattice.
4. Very difficult / advanced: FPS on subset lattice / advanced FWT packs.

---

## 12. Recognition & Identification Drills

1. Given \(f,g\) on masks, compute \(\sum_{A \sqcup B = S} f(A)g(B)\) for all \(S\), \(n=18\).
2. Explain why XOR-FWT does **not** solve disjoint subset convolution.
3. Reduce \(O(3^n)\) DP merge to \(O(n^2 2^n)\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: disjoint-union convolution, Niche only
- Key invariant: ranked zeta → pointwise rank convolution → Möbius
- Key formula: \((f*g)(S)=\sum_{A\subseteq S}f(A)g(S\setminus A)\)
- Complexity: \(O(n^2 2^n)\)
- Template to remember: rank layers + SOS ζ + mul + μ

---

Back to [`13-bit-combinatorics.md`](13-bit-combinatorics.md) · Combinatorics: [`13-b-advanced-combinatorics.md`](13-b-advanced-combinatorics.md)

---
