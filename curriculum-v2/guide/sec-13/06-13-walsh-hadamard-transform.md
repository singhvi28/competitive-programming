# 6. Walsh-Hadamard Transform

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2300–2900 | **Frequency:** Rare  
> **Prerequisites:** Bitmasks, SOS intuition, modular arithmetic / FFT mindset  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2300–2900
- Prerequisites: Bitmasks, SOS intuition, modular arithmetic / FFT mindset

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

WHT (FWT for XOR) diagonalizes subset-XOR convolution:
\[
(f *_{\oplus} g)(k) = \sum_{i \oplus j = k} f(i)g(j).
\]
Like FFT: transform → pointwise multiply → inverse transform. OR/AND convolutions have analogous FWTs (closely related to SOS zeta). For XOR, butterflies are \(a' = a+b,\ b' = a-b\) (or modular equivalents).

---

## 4. Proof Sketches & Recurrences

Hadamard matrix \(H_2 = \begin{bmatrix}1&1\\1&-1\end{bmatrix}\), \(H_{2^{n}} = H_2 \otimes H_{2^{n-1}}\).  
FWHT in-place: for `len = 1; len < N; len <<= 1` for each block apply butterfly.  
Inverse: same transform, then divide by \(N = 2^n\) (or multiply by \(\mathrm{inv}(N)\)).  
OR-FWT: \(a' = a,\ b' = a+b\); AND-FWT: \(a' = a+b,\ b' = b\); invert with minus.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: one FWHT \(O(N \log N)\) with \(N = 2^n\)
- Total: XOR conv \(O(N \log N)\)
- Memory: \(O(N)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Convolution where indices combine by XOR (sometimes OR/AND)
- Count pairs/triples with \(a_i \oplus a_j = a_k\)
- Generating functions over \(\mathrm{GF}(2)^n\) characters

---

## 7. Contest WA / TLE / RE Traps

- Forgetting divide-by-\(N\) on inverse XOR-FWT.
- Using OR/AND butterflies for XOR problems.
- `n` not a power of two — pad.
- Modular negative handling after `u - v`.

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

- OR / AND FWT; subset zeta (SOS) for subset-sum style.
- Multiple sequences: pointwise product of \(k\) transforms.
- Untyped integer FWHT when values small (no mod).

---

## 11. Typical Problem Archetypes

1. Standard application: count pairs with given XOR via freq FWHT.
2. Slightly disguised: expected value over XOR combinations.
3. Difficult: constrained convolutions + DP on bits.
4. Very difficult / advanced: subset convolution via ranked FWHT (next topic).

---

## 12. Recognition & Identification Drills

1. Arrays \(A,B\); for every \(x\) count pairs \(a \oplus b = x\).
2. Number of triples \(i,j,k\) with \(a_i \oplus a_j \oplus a_k = 0\).
3. Polynomial product where exponents XOR instead of add.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: XOR/OR/AND index convolutions on \(2^n\) arrays
- Key invariant: FWHT diagonalizes the group character table of \((\mathbb{Z}/2\mathbb{Z})^n\)
- Key formula: butterfly \(+(a+b),\ -(a-b)\); inv `/N`
- Complexity: \(O(N \log N)\), \(N=2^n\)
- Template to remember: transform → pointwise mul → inverse

---

---
