# Binomial coefficients

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–2000 | **Frequency:** Very Common  
> **Prerequisites:** Modular arithmetic, modular inverse, factorials  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–2000
- Prerequisites: Modular arithmetic, modular inverse, factorials

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

\(C(n,k) = \frac{n!}{k!(n-k)!}\) counts \(k\)-subsets. In contests you almost always need many queries mod prime \(p\): precompute \(fact[i]\), \(invfact[i]\) in \(O(n + \log p)\), then \(C(n,k) = fact[n] \cdot invfact[k] \cdot invfact[n-k]\). For non-prime moduli, use Lucas (prime powers / CRT) or DP \(C(i,j) = C(i-1,j)+C(i-1,j-1)\).

---

## 4. Proof Sketches & Recurrences

Pascal: \(C(n,k) = C(n-1,k) + C(n-1,k-1)\).  
Inverse factorial: \(invfact[n] = fact[n]^{-1}\), then \(invfact[i] = invfact[i+1] \cdot (i+1)\).  
Stars and bars: \(C(n+k-1, k-1)\) nonneg solutions to \(x_1+\cdots+x_k=n\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(N + \log \mathrm{mod})\)
- Per-query / per-operation: \(O(1)\)
- Total: \(O(N + Q)\)
- Memory: \(O(N)\)`

### C++17 Template

```cpp
namespace binom {
struct Comb {
    int mod;
    vector<int> fact, invfact;
    Comb(int n, int mod) : mod(mod), fact(n + 1), invfact(n + 1) {
        fact[0] = 1;
        for (int i = 1; i <= n; ++i) fact[i] = (long long)fact[i - 1] * i % mod;
        invfact[n] = mod_pow(fact[n], mod - 2);
        for (int i = n; i >= 1; --i) invfact[i - 1] = (long long)invfact[i] * i % mod;
    }
    int mod_pow(long long a, long long e) const {
        long long r = 1;
        for (; e; e >>= 1, a = a * a % mod) if (e & 1) r = r * a % mod;
        return (int)r;
    }
    int C(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[k] % mod * invfact[n - k] % mod;
    }
    int P(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[n - k] % mod;
    }
};
} // namespace binom
```

### Python 3 Template

```python
class Comb:
    def __init__(self, n: int, mod: int):
        self.mod = mod
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.invfact = [1] * (n + 1)
        self.invfact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n, 0, -1):
            self.invfact[i - 1] = self.invfact[i] * i % mod
    def C(self, n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.invfact[k] % self.mod * self.invfact[n - k] % self.mod
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Number of ways to choose,” paths on grid, stars and bars
- Probability written as ratios of binomials
- \(n \le 10^6\), prime mod \(998244353\) / \(10^9+7\)

---

## 7. Contest WA / TLE / RE Traps

- Calling \(C(n,k)\) with \(n\) larger than precompute limit.
- Non-prime mod → Fermat inverse wrong; use ExtEuclid only if \(\gcd(fact,mod)=1\).
- Forgetting \(k > n \Rightarrow 0\).

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

- Prefix products for huge \(n\) single query: multiply \(n/k \cdot (n-1)/(k-1)\cdots\) carefully.
- Lucas for \(n \gg p\) (next topic).
- Binomial mod \(p^e\) — rare, CRT + factor \(p\).

---

## 11. Typical Problem Archetypes

1. Standard application: ways to choose \(k\) of \(n\) mod prime.
2. Slightly disguised: grid paths \(C(n+m, n)\).
3. Difficult: sum of binomials / hockey-stick identity.
4. Very difficult / advanced: binomial transforms, formal power series coeffs.

---

## 12. Recognition & Identification Drills

1. \(Q \le 10^5\) queries \(C(n_i,k_i)\) with \(n_i \le 10^6\), mod \(10^9+7\).
2. Number of nonnegative solutions to \(x_1+\cdots+x_m = n\).
3. Expected number of fixed points — rewrite with binomials.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: almost any counting with choices
- Key invariant: \(C(n,k)=C(n,n-k)\); Pascal recurrence
- Key formula: \(fact[n]\cdot invfact[k]\cdot invfact[n-k]\)
- Complexity: pre \(O(N)\), query \(O(1)\)
- Template to remember: fact + invfact tables

---

---
