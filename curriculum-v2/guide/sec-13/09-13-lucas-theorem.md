# Lucas theorem

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Binomial coefficients, base-\(p\) digits, prime modulus  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Binomial coefficients, base-\(p\) digits, prime modulus

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

For prime \(p\): write \(n = n_t p^t + \cdots + n_0\), \(k = k_t p^t + \cdots + k_0\) in base \(p\). Then
\[
C(n,k) \equiv \prod_{i=0}^{t} C(n_i, k_i) \pmod{p},
\]
with \(C(n_i,k_i)=0\) if \(k_i > n_i\). So huge binomials reduce to products of tiny ones (\(n_i < p\)).

---

## 4. Proof Sketches & Recurrences

From \((1+x)^{p} \equiv 1 + x^{p} \pmod p\) (Freshman’s dream) inductively \((1+x)^n = \prod (1+x)^{n_i p^i} \equiv \prod (1+x^{p^i})^{n_i}\), extract \([x^k]\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(p + \log p)\)
- Per-query / per-operation: \(O(\log_p n)\) small binomials
- Total: \(O(p + Q \log_p n)\)
- Memory: \(O(p)\)`

### C++17 Template

```cpp
namespace lucas {
struct Lucas {
    int p;
    vector<int> fact, invfact;
    Lucas(int p) : p(p), fact(p), invfact(p) {
        fact[0] = 1;
        for (int i = 1; i < p; ++i) fact[i] = (long long)fact[i - 1] * i % p;
        invfact[p - 1] = mod_pow(fact[p - 1], p - 2);
        for (int i = p - 1; i >= 1; --i) invfact[i - 1] = (long long)invfact[i] * i % p;
    }
    int mod_pow(long long a, long long e) const {
        long long r = 1;
        for (; e; e >>= 1, a = a * a % p) if (e & 1) r = r * a % p;
        return (int)r;
    }
    int C_small(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (long long)fact[n] * invfact[k] % p * invfact[n - k] % p;
    }
    int C(long long n, long long k) const {
        if (k < 0 || k > n) return 0;
        int ans = 1;
        while (n || k) {
            int ni = n % p, ki = k % p;
            ans = (long long)ans * C_small(ni, ki) % p;
            if (!ans) return 0;
            n /= p; k /= p;
        }
        return ans;
    }
};
} // namespace lucas
```

### Python 3 Template

```python
def lucas(n: int, k: int, p: int) -> int:
    if k < 0 or k > n:
        return 0
    fact = [1] * p
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    invfact = [1] * p
    invfact[p - 1] = pow(fact[p - 1], p - 2, p)
    for i in range(p - 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % p
    def C_small(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % p * invfact[a - b] % p
    ans = 1
    while n or k:
        ans = ans * C_small(n % p, k % p) % p
        n //= p
        k //= p
    return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- \(C(n,k) \bmod p\) with \(p\) prime and \(n\) up to \(10^{18}\)
- Digit-DP-looking constraints on base-\(p\) digits of \(n,k\)
- “When is \(C(n,k)\) divisible by \(p\)?” ↔ some digit \(k_i > n_i\)

---

## 7. Contest WA / TLE / RE Traps

- Using Lucas for composite modulus directly — wrong; factor + CRT.
- Building fact tables of size \(n\) instead of \(p\).
- Overflow on \(n\) as `int` when \(n > 2^{31}\).

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

- Lucas for prime powers (generalized) — hard, rarely needed.
- Combination with digit DP on base \(p\).

---

## 11. Typical Problem Archetypes

1. Standard application: \(C(n,k) \bmod p\), \(n \le 10^{18}\), \(p \le 10^6\).
2. Slightly disguised: count \(k\) with \(C(n,k) \not\equiv 0 \pmod p\).
3. Difficult: sum Lucas digits products under constraints.
4. Very difficult / advanced: multinomial Lucas / CRT composites.

---

## 12. Recognition & Identification Drills

1. Compute \(C(10^{18}, 10^{9}) \bmod 97\).
2. For prime \(p\), find largest \(k\) with \(C(n,k)\) not divisible by \(p\).
3. Modulus \(15 = 3\cdot 5\) — outline CRT + Lucas plan.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: prime mod, \(n\) too large for factorial tables
- Key invariant: base-\(p\) digit independence of binomials
- Key formula: \(C(n,k) \equiv \prod C(n_i,k_i) \pmod p\)
- Complexity: pre \(O(p)\), query \(O(\log_p n)\)
- Template to remember: while \(n|k\): multiply \(C(n\%p,k\%p)\)

---

---
