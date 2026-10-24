# Recognition shortcuts

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common in Div1/Div2 Hard
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: Bitwise operations, Submask enumeration, SOS DP, Fast Walsh-Hadamard Transform (FWHT)
- Tradeoff: Recognizing the exact bitwise algorithm immediately from $N$ and problem constraints.

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

Bitwise problem constraints form an infallible recognition matrix: 1) $N \le 20 \implies$ Iterate all submasks $\sum_{mask} 2^{|mask|} = 3^N \approx 3.5 \times 10^9$ (or $N \le 16 \implies 3^{16} = 4.3 \times 10^7$). 2) $N \le 24 \implies$ Sum Over Subsets (SOS) DP in $\mathcal{O}(N \cdot 2^N) \approx 4 \times 10^8$ operations. 3) $N \le 20$ with bitwise AND/OR/XOR convolution $c_k = \sum_{i \star j = k} a_i b_j \implies$ Fast Walsh-Hadamard Transform (FWHT) in $\mathcal{O}(N \cdot 2^N)$. 4) Subset Convolution (enforcing disjoint sets $i \cup j = k$ with $i \cap j = \emptyset$) $\implies$ Ranked SOS DP in $\mathcal{O}(N^2 \cdot 2^N)$.

---

## 4. Proof Sketches & Recurrences

Submask iteration loop `for (int sub = mask; sub; sub = (sub - 1) & mask)` visits each pair $(sub, mask)$ such that $sub \subseteq mask$. The total number of iterations is $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$. SOS DP computes prefix sums along Boolean hypercube dimensions: iterating coordinate bit $i$ from $0$ to $N-1$ updates $dp[mask] += dp[mask \oplus 2^i]$ if bit $i$ is set, evaluating all subset sums in exactly $N \cdot 2^N$ operations.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Constraints state $N \le 20$ or $N \le 24$ (universal signal for bitmask / SOS DP).
- Count pairs $(i, j)$ such that $a_i \text{ AND } a_j = 0$ (SOS DP on complement mask $\sim a_i$).
- Finding shortest Hamiltonian path / Traveling Salesperson Problem on $N \le 20$ vertices.
- Set cover or partition problems where items are represented as bit flags.

---

## 7. Contest WA / TLE / RE Traps

- Submask iteration infinite loop: using `sub >= 0` instead of `sub > 0` causes `(0 - 1) & mask = mask`, looping infinitely.
- Loop order in SOS DP: outer loop MUST iterate over dimension $i \in [0, N-1]$ and inner loop over masks to correctly accumulate multi-dimensional prefix sums.
- Bitwise operator precedence: `1 << n - 1` evaluates as `1 << (n - 1)`. Always use parentheses `(1 << n) - 1` and `(mask & (1 << i))`.
- Integer overflow: using 32-bit `int` for bit shifts when $N \ge 31$; use `1LL << i`.

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
