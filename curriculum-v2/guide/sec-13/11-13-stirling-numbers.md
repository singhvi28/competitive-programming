# 11. Stirling numbers

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Binomials, inclusion-exclusion, basic DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Binomials, inclusion-exclusion, basic DP

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

- **Stirling 2nd kind** \(S(n,k)\): ways to partition \(n\) labeled objects into \(k\) nonempty **unlabeled** subsets.  
- **Stirling 1st kind** \(s(n,k)\) / \(|s(n,k)|\): permutations of \(n\) with \(k\) cycles (signed vs unsigned).  
Surjections onto \(k\) labels: \(k! S(n,k) = \sum_{i=0}^{k} (-1)^{k-i} C(k,i) i^n\).

---

## 4. Proof Sketches & Recurrences

Recurrences:  
\(S(n,k) = S(n-1,k-1) + k\, S(n-1,k)\),  
\(|s(n,k)| = |s(n-1,k-1)| + (n-1)|s(n-1,k)|\).  
Falling factorial: \(x^n = \sum_k S(n,k) (x)_k\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n^2)\) table
- Per-query / per-operation: \(O(1)\) lookup or \(O(k \log n)\) surjection formula
- Total: \(O(n^2)\)
- Memory: \(O(n^2)\) (or \(O(n)\) rolling)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Partition people into \(k\) nonempty unlabeled teams
- “Onto functions” / functions with exactly \(k\) nonempty image sizes
- Cycle counts in permutations; rising/falling factorial basis change

---

## 7. Contest WA / TLE / RE Traps

- Confusing labeled vs unlabeled partitions (\(k! S(n,k)\) vs \(S(n,k)\)).
- Mixing signed 1st kind with unsigned cycle counts.
- \(S(0,0)=1\) but \(S(n,0)=0\) for \(n>0\).

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

- Bell numbers \(B_n = \sum_k S(n,k)\).
- r-Stirling, associated Stirling — rare.
- FFT / NTT for rows when \(n\) large and formula allows (advanced).

---

## 11. Typical Problem Archetypes

1. Standard application: partitions into \(k\) nonempty subsets.
2. Slightly disguised: count functions with image size \(k\).
3. Difficult: DP mixing Stirling with other counts.
4. Very difficult / advanced: basis conversion of polynomials via Stirling.

---

## 12. Recognition & Identification Drills

1. Ways to split \(n\) distinct people into \(k\) nonempty unlabeled rooms.
2. Number of permutations of \(n\) with exactly \(k\) cycles.
3. Compute \(k! S(n,k)\) via inclusion-exclusion without building \(S\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: set partitions / cycle counts / surjections
- Key invariant: \(S(n,k)=S(n-1,k-1)+k S(n-1,k)\)
- Key formula: \(k! S(n,k)=\sum (-1)^{k-i}C(k,i)i^n\)
- Complexity: \(O(n^2)\) table
- Template to remember: 2D DP recurrence above

---

---
