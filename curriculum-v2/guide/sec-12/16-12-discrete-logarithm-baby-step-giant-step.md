# Discrete Logarithm / Baby-Step Giant-Step

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2100–2700 | **Frequency:** Rare  
> **Prerequisites:** modpow, meet-in-the-middle, inverse, preferably primitive roots / gcd handling  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: modpow, meet-in-the-middle, inverse, preferably primitive roots / gcd handling

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

Solve `a^x ≡ b (mod m)` for x. BSGS: let `x = i·B - j` with `B≈√N`, `N=order` (often `m-1` for prime m). Precompute baby steps `a^j`, match giant steps `b·(a^{-B})^i`. Meet-in-the-middle in the cyclic subgroup. If gcd(a,m)>1, peel common factors / reduce carefully.

---

## 4. Proof Sketches & Recurrences

Assume mod prime p, a≠0, work in order `n = ord(a)` or `p-1`.  
`a^{iB} ≡ b · a^j` with `0≤j<B`, `i=0..⌈n/B⌉`.  
Hash map `a^j → j` (keep minimal j). For each i, query.  
Complexity `O(√n)` time and memory. Pohlig–Hellman reduces to dlog mod prime powers of `p-1` when smooth.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (per query map)
- Per-query / per-operation: `O(√p)` time and memory (prime modulus case)
- Total: same; Pohlig–Hellman faster if `p-1` smooth
- Memory: `O(√p)` hashmap`

### C++17 Template

```cpp
namespace bsgs {
using i64 = long long;
// solve a^x = b (mod p), p prime, gcd(a,p)=1; return minimal x≥0 or -1
i64 discrete_log(i64 a, i64 b, i64 p) {
    a %= p; b %= p;
    if (b == 1 % p) return 0;
    i64 m = (i64)std::sqrt(p) + 1;
    std::unordered_map<i64, i64> baby;
    baby.reserve(m * 2);
    i64 e = 1;
    for (i64 j = 0; j < m; ++j) {
        if (!baby.count(e)) baby[e] = j;
        e = (__int128)e * a % p;
    }
    i64 am = binpow::mod_pow(a, m, p);
    i64 inv_am = binpow::mod_pow(am, p - 2, p);
    i64 gamma = b;
    for (i64 i = 0; i <= m; ++i) {
        auto it = baby.find(gamma);
        if (it != baby.end()) return i * m + it->second;
        gamma = (__int128)gamma * inv_am % p;
    }
    return -1;
}
} // namespace bsgs
```

### Python 3 Template

```python
import math

def discrete_log(a: int, b: int, p: int) -> int | None:
    """Minimal x>=0 with pow(a,x,p)==b; p prime, gcd(a,p)=1."""
    a %= p
    b %= p
    if b == 1 % p:
        return 0
    m = int(math.isqrt(p)) + 1
    baby = {}
    e = 1
    for j in range(m):
        baby.setdefault(e, j)
        e = e * a % p
    am = pow(a, m, p)
    inv_am = pow(am, p - 2, p)
    gamma = b
    for i in range(m + 1):
        if gamma in baby:
            return i * m + baby[gamma]
        gamma = gamma * inv_am % p
    return None
```

---

## 6. Recognition Trigger Signals & Heuristics

- Explicit “find discrete log”
- Order / exponential Diophantine in multiplicative group
- Hash-map meet-in-the-middle with powers

---

## 7. Contest WA / TLE / RE Traps

- Hash collisions / forgetting `unordered_map` reserve
- Not handling `b=1` → x=0
- `gcd(a,p)>1` without reduction
- Using wrong order (should use ord(a) when subgroup smaller)
- Giant-step inverse wrong direction (`iB+j` vs `iB-j` convention)

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

- **Pohlig–Hellman:** factor order, solve CRT of subgroup logs
- BSGS for `a^x = b` in any group with known order
- Kangaroo / Pollard lambda for interval-restricted x

---

## 11. Typical Problem Archetypes

1. Standard application: dlog mod p
2. Slightly disguised: find period / first time power hits b
3. Difficult: composite modulus + CRT split
4. Very difficult / advanced: PH + BSGS on 256-bit smooth orders

---

## 12. Recognition & Identification Drills

1. Solve `2^x ≡ 5 (mod 101)`.
2. When does BSGS beat naive? Estimate √(p-1).
3. Outline Pohlig–Hellman given factorization of p−1.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: discrete log, order ~1e10–1e14 max for √
- Key invariant: meet-in-the-middle on exponent
- Key formula: `x = i√n + j`
- Complexity: `O(√n)`
- Template to remember: baby map + giant multiply by `a^{-B}`

---

## End Drill Pointer

Full weekly drill list and comparison tables live in [12-number-theory.md](12-number-theory.md). After Part B, prioritize: μ + floor blocks + IE recognition; keep MR+Pollard as a paste-ready block; skim primitive roots/BSGS until a problem forces them.

---
