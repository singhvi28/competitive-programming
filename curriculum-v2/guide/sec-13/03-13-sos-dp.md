# 3. SOS DP

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier · Frequency: Occasional · Rating: 1800–2400 | **Rating Range:** 1800–2400 | **Frequency:** Occasional · Rating: 1800–2400  
> **Prerequisites:** Bitmasks, DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier · Frequency: Occasional · Rating: 1800–2400
- Use when you need \(F[S] = \sum_{T \subseteq S} f[T]\) (or superset sums) for **all** \(S\) in \(O(n 2^n)\), not \(O(3^n)\) submask loops.

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

Fast zeta on the boolean lattice: fix one bit dimension at a time and prefix-sum along that bit.

---

## 4. Proof Sketches & Recurrences

Define $dp[i][mask]$ as the sum over all submasks $sub \subseteq mask$ that differ from $mask$ only on a subset of the first $i$ bits. If the $i$-th bit of $mask$ is 0, then any submask must also have the $i$-th bit as 0: $dp[i][mask] = dp[i-1][mask]$. If the $i$-th bit is 1, a submask can have this bit as either 0 or 1: $dp[i][mask] = dp[i-1][mask] + dp[i-1][mask \oplus 2^i]$. Memory can be rolled into a single 1D array of size $2^N$ by iterating $i$ in the outer loop.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Submask enum: “for this mask, look at its submasks” with light work.
- SOS: “transform whole arrays on the subset lattice,” then maybe Möbius invert.
- Related here: WHT/FWT (XOR/OR/AND convolutions) and fast subset convolution (below) build on the same lattice mindset.

---

## 7. Contest WA / TLE / RE Traps

- Inverting the loop nesting: if mask is the outer loop and bit $i$ is the inner loop, hypercube prefix sums will NOT propagate correctly, producing wrong results.
- Bitwise precedence error: `mask & 1 << i` evaluates as `mask & (1 << i)`, but `mask & 1 == 0` evaluates as `mask & (1 == 0)`; always wrap bitwise checks in parentheses.
- Array sizing: array must be allocated with size $2^N$ (`1 << n`), not $N$.
- Integer overflow: accumulating array values in `int` when sum of $2^N$ terms exceeds $2 \times 10^9$.

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

## 13. Fast-Lookup Cheat Sheet

- Open §04 SOS DP for C++/Python templates, bugs, and problem patterns.

---

---
