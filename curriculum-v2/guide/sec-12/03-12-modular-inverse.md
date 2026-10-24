# 3. Modular Inverse

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Very Common  
> **Prerequisites:** binpow or ExtEuclid; primes vs composite moduli  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: binpow or ExtEuclid; primes vs composite moduli

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

## 3. Core Intuition & Problem Framing

Division mod `m` means multiply by `a^{-1}` where `a·a^{-1}≡1 (mod m)`, exists iff `gcd(a,m)=1`. Two engines: **Fermat/Euler** (`a^{φ(m)-1}`) when coprime, or **ExtEuclid** (`ax+my=1`). For factorials, precompute inv of `n!` then back-derive `inv[i]`.

---

## 4. Proof Sketches & Recurrences

- Prime `p`: Fermat `a^{p-2} ≡ a^{-1} (mod p)` for `a≠0`.
- General: ExtEuclid → `ax≡1 (mod m)` iff `gcd=1`; `x mod m` is inverse.
- Linear sieve of inverses: `inv[1]=1`, `inv[i] = mod - (mod/i)*inv[mod%i]%mod` for prime mod.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n + log mod)` for fact/invfact; `O(n)` inv_range
- Per-query / per-operation: `O(log mod)` single inverse; `O(1)` nCr after prep
- Total: as above
- Memory: `O(n)` for tables`

### C++17 Template

```cpp
namespace modinv {
using i64 = long long;
i64 mod_pow(i64 a, i64 e, i64 mod); // from binpow

i64 inv_fermat(i64 a, i64 mod) { // mod prime
    return mod_pow(a, mod - 2, mod);
}
i64 inv_egcd(i64 a, i64 mod) {
    i64 x, y;
    i64 g = extgcd::egcd(a, mod, x, y);
    if (g != 1 && g != -1) return -1; // no inverse
    x %= mod;
    if (x < 0) x += mod;
    return x;
}
// inv[1..n] mod prime P
void inv_range(int n, int P, std::vector<int>& inv) {
    inv.assign(n + 1, 0);
    inv[1] = 1;
    for (int i = 2; i <= n; ++i)
        inv[i] = (i64)(P - P / i) * inv[P % i] % P;
}
// factorial + inv factorial for nCr
struct FactInv {
    int mod;
    std::vector<int> fac, ifac;
    FactInv(int n, int mod) : mod(mod), fac(n + 1), ifac(n + 1) {
        fac[0] = 1;
        for (int i = 1; i <= n; ++i) fac[i] = (i64)fac[i - 1] * i % mod;
        ifac[n] = (int)inv_fermat(fac[n], mod);
        for (int i = n; i >= 1; --i) ifac[i - 1] = (i64)ifac[i] * i % mod;
    }
    int C(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (i64)fac[n] * ifac[k] % mod * ifac[n - k] % mod;
    }
};
} // namespace modinv
```

### Python 3 Template

```python
def inv_fermat(a: int, mod: int) -> int:
    return pow(a, mod - 2, mod)  # mod prime

def inv_egcd(a: int, mod: int) -> int | None:
    g, x, _ = egcd(a % mod, mod)
    if g != 1:
        return None
    return x % mod

def inv_range(n: int, P: int) -> list[int]:
    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (P - P // i) * inv[P % i] % P
    return inv
```

---

## 6. Recognition Trigger Signals & Heuristics

- Combinatorics mod prime: `nCr`, Catalan
- Formulas with division
- Modular geometric series
- Hashing with division (rare — prefer multiply)

---

## 7. Contest WA / TLE / RE Traps

- Fermat on composite modulus (wrong)
- `a=0` or not coprime — no inverse
- `ifac[n] = inv(fac[n])` then loop down — off-by-one if `n=0`
- Mixing `%` with negative intermediates

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

## 10. Algorithmic Variants & Advanced Extensions

- Inverse of product / geometric: `inv(1-r)`
- CRT: invert mod each prime power then combine
- Montgomery form (only for heavy mulmod engines)

---

## 11. Typical Problem Archetypes

1. Standard application: `nCr mod p`
2. Slightly disguised: expected value mod p (multiply by inv of denom)
3. Difficult: Lucas for large n, small p
4. Very difficult / advanced: inverse mod `p^k` via Hensel

---

## 12. Recognition & Identification Drills

1. Precompute all `nCr` for `n ≤ 1e6` mod `1e9+7`.
2. Solve `3x ≡ 1 (mod 10^{9}+9)` — wait, check if modulus prime first.
3. Sum of inverses `∑_{i=1}^n i^{-1} mod p`.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: division in modular formulas
- Key invariant: `a·inv(a)≡1`
- Key formula: `a^{p-2}` or ExtEuclid
- Complexity: `O(log m)` or `O(1)` after tables
- Template to remember: fact + ifac back-propagation

---

---
