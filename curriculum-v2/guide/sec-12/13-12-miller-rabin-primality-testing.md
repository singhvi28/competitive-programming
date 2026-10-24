# 13. Miller-Rabin Primality Testing

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** modpow, careful 64-bit mulmod; factorization pipeline  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: modpow, careful 64-bit mulmod; factorization pipeline

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

Fermat tests are weak; MR uses the factorization of `a^{n-1}-1` along the chain `a^q, a^{2q}, …, a^{2^{s-1}q}` (where `n-1=2^s q`). A prime forces this sequence to hit `1` only after a `-1` (or start at `1`); a composite “witness” fails with high probability. For 64-bit integers, **deterministic base sets** exist: check a fixed handful of bases → exact primality for `n < 2^64`.

---

## 4. Proof Sketches & Recurrences

Write `n-1 = 2^s · q` (q odd). For base a: compute `a^q mod n`. Prime ⇒ sequence becomes 1 after some squaring, and first 1 is preceded by n-1 (or already 1). If neither `a^q≡1` nor `a^{2^i q}≡-1` for some i<s → composite.  
Deterministic bases for 64-bit: `{2,3,5,7,11,13,23}` (one common set; others exist).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(k · log n · mul)` with k≈7 bases
- Total: same
- Memory: `O(1)``

### C++17 Template

```cpp
namespace miller_rabin {
using u64 = unsigned long long;
using u128 = __uint128_t;
u64 mul_mod(u64 a, u64 b, u64 mod) {
    return (u128)a * b % mod;
}
u64 pow_mod(u64 a, u64 e, u64 mod) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return r;
}
bool is_prime(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ull, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37})
        if (n % p == 0) return n == p;
    u64 d = n - 1, s = 0;
    while ((d & 1) == 0) d >>= 1, ++s;
    auto check = [&](u64 a) {
        if (a % n == 0) return true;
        u64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) return true;
        for (u64 i = 1; i < s; ++i) {
            x = mul_mod(x, x, n);
            if (x == n - 1) return true;
        }
        return false;
    };
    // deterministic for all 64-bit n
    for (u64 a : {2ull, 3, 5, 7, 11, 13, 23})
        if (!check(a)) return false;
    return true;
}
} // namespace miller_rabin
```

### Python 3 Template

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    def check(a: int) -> bool:
        if a % n == 0:
            return True
        x = pow(a, d, n)  # big-int safe; no manual mulmod
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False
    return all(check(a) for a in (2, 3, 5, 7, 11, 13, 23))
```

---

## 6. Recognition Trigger Signals & Heuristics

- Test primality of `n ≤ 10^18` (or `2^64-1`)
- Inside Pollard–Rho recursion
- Sparse need for many random big primes

---

## 7. Contest WA / TLE / RE Traps

- Overflow mulmod in C++
- Forgetting small prime trial (speed + edge)
- Using probabilistic bases without enough rounds for 64-bit
- `n=1`, even n edge cases

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

- Probabilistic MR for bigints >>64-bit (crypto sizes)
- Baillie–PSW (stronger hybrid)
- Deterministic bases for 32-bit only: `{2,7,61}`

---

## 11. Typical Problem Archetypes

1. Standard application: is `n` prime?
2. Slightly disguised: next prime / generate prime
3. Difficult: count primes in weird sequences with MR tests
4. Very difficult / advanced: primality for 256-bit (need more)

---

## 12. Recognition & Identification Drills

1. Test `10^9+7`, `10^18+3`, and a semiprime near `1e18`.
2. Find any witness that detects a known Carmichael number via MR (vs Fermat).
3. Wire MR as the leaf test of Pollard–Rho.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: 64-bit primality
- Key invariant: strong pseudoprime conditions
- Key formula: `n-1=2^s q` witness check
- Complexity: `O(k log n)` mulmods
- Template to remember: deterministic bases + mulmod

---

---
