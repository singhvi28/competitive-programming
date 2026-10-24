# Pollard-Rho Factorization

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Miller–Rabin, gcd, mulmod  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Miller–Rabin, gcd, mulmod

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

Factor composite n by walking a polynomial sequence `x ↦ x^2+c mod n` and using **Floyd / Brent** to find `x,y` with `g=gcd(|x-y|,n)` nontrivial. Birthday collision in the hidden factor’s residue class. Recurse with MR as prime check. For `n≤1e18`, this is the standard contest factorizer.

---

## 4. Proof Sketches & Recurrences

If p|n unknown, sequence mod p has cycle ~`O(√p)`. Brent’s cycle detection accumulates product of differences to amortize gcd. Expected time roughly `O(n^{1/4})` per factor for typical n. Trial-divide small primes first; then Rho; then MR.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: expected `~O(n^{1/4})` per hard factor
- Total: factorization tree
- Memory: `O(log n)` recursion + factor list`

### C++17 Template

```cpp
namespace pollard {
using u64 = unsigned long long;
using u128 = __uint128_t;
u64 mul_mod(u64 a, u64 b, u64 mod) { return (u128)a * b % mod; }
u64 f(u64 x, u64 c, u64 mod) { return (mul_mod(x, x, mod) + c) % mod; }

u64 brent(u64 n) {
    if (n % 2 == 0) return 2;
    std::mt19937_64 rng(n);
    for (;;) {
        u64 y = rng() % (n - 1) + 1, c = rng() % (n - 1) + 1, m = 128;
        u64 g = 1, r = 1, q = 1, x = 0, ys = 0;
        while (g == 1) {
            x = y;
            for (u64 i = 0; i < r; ++i) y = f(y, c, n);
            u64 k = 0;
            while (k < r && g == 1) {
                ys = y;
                u64 lim = std::min(m, r - k);
                for (u64 i = 0; i < lim; ++i) {
                    y = f(y, c, n);
                    q = mul_mod(q, x > y ? x - y : y - x, n);
                }
                g = std::gcd(q, n);
                k += lim;
            }
            r *= 2;
        }
        if (g == n) {
            do {
                ys = f(ys, c, n);
                g = std::gcd(x > ys ? x - ys : ys - x, n);
            } while (g == 1);
        }
        if (g != n) return g;
    }
}

void factor(u64 n, std::vector<u64>& fac) {
    if (n == 1) return;
    if (miller_rabin::is_prime(n)) { fac.push_back(n); return; }
    for (u64 p : {2ull, 3, 5, 7, 11, 13, 17, 19, 23, 29}) {
        while (n % p == 0) { fac.push_back(p); n /= p; }
    }
    if (n == 1) return;
    if (miller_rabin::is_prime(n)) { fac.push_back(n); return; }
    u64 d = brent(n);
    factor(d, fac);
    factor(n / d, fac);
}
std::map<u64, int> factor_map(u64 n) {
    std::vector<u64> fac;
    factor(n, fac);
    std::map<u64, int> mp;
    for (u64 p : fac) ++mp[p];
    return mp;
}
} // namespace pollard
```

### Python 3 Template

```python
import random
from math import gcd

def brent(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        y, c, m = random.randrange(1, n), random.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (pow(y, 2, n) + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (pow(y, 2, n) + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            while True:
                ys = (pow(ys, 2, n) + c) % n
                g = gcd(abs(x - ys), n)
                if g > 1:
                    break
        if g != n:
            return g

def factor(n: int, out: list[int] | None = None) -> list[int]:
    if out is None:
        out = []
    if n == 1:
        return out
    if is_prime(n):
        out.append(n)
        return out
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        while n % p == 0:
            out.append(p)
            n //= p
    if n == 1:
        return out
    if is_prime(n):
        out.append(n)
        return out
    d = brent(n)
    factor(d, out)
    factor(n // d, out)
    return out
```

---

## 6. Recognition Trigger Signals & Heuristics

- Factor one / few integers up to `1e18`
- Need full factorization for φ(n), orders, CRT moduli
- Semiprime challenges (not crypto-hard)

---

## 7. Contest WA / TLE / RE Traps

- Missing MR → infinite recursion on primes
- Not trial-dividing small primes
- `gcd` product overflow without mod n
- Unlucky `c` — must retry loop
- Returning n itself forever without Brent fallback loop

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

- Floyd vs Brent
- Pollard p−1 (smooth p−1)
- ECM (almost never needed in CF)

---

## 11. Typical Problem Archetypes

1. Standard application: factor `n≤1e18`
2. Slightly disguised: compute φ(n) for large n
3. Difficult: factor many n with shared templates
4. Very difficult / advanced: crypto CTF sizes (out of scope)

---

## 12. Recognition & Identification Drills

1. Factor `100000000003` (example — use your tester).
2. Given n, count divisors via full factorization.
3. Solve order problems needing factor of `p-1`.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: 64-bit factorization
- Key invariant: gcd of sequence diffs hits a factor
- Key formula: Brent rho + MR leaves
- Complexity: ~`n^{1/4}`
- Template to remember: brent + recursive factor

---

---
