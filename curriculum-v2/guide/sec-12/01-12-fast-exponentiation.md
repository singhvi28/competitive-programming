# 1. Fast Exponentiation

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 800–1600 (appears inside harder problems constantly) | **Frequency:** Very Common  
> **Prerequisites:** Modular arithmetic, integer overflow awareness  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 800–1600 (appears inside harder problems constantly)
- Prerequisites: Modular arithmetic, integer overflow awareness

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

Multiplying `a` by itself `n` times is linear. Binary exponentiation rewrites `n` in binary: each bit is a squaring step, and you multiply into the answer only for set bits. Same idea lifts to **matrix powering**, **binary lifting on functional graphs**, and **modpow inside MR**. Mentally: “square the base, consume the exponent bit.”

---

## 4. Proof Sketches & Recurrences

\[
a^n = \begin{cases}
1 & n=0 \\
(a^{n/2})^2 & n \text{ even} \\
a \cdot a^{n-1} & n \text{ odd}
\end{cases}
\]
Iterative: `res=1`; while `n`: if `n&1` `res*=a`; `a*=a`; `n>>=1`.  
Complexity `O(log n)` multiplications. Modulo: reduce after each mul. For matrix expo, each “mul” is `O(d^3)` → `O(d^3 log n)`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log e)` mulmods (`O(d^3 log e)` matrices)
- Total: as above
- Memory: `O(1)` scalar; `O(d^2)` matrices`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace binpow {
using i64 = long long;
i64 mod_pow(i64 a, i64 e, i64 mod) {
    a %= mod;
    if (a < 0) a += mod;
    i64 r = 1 % mod;
    while (e > 0) {
        if (e & 1) r = (__int128)r * a % mod;
        a = (__int128)a * a % mod;
        e >>= 1;
    }
    return r;
}
// unmodular: overflow risk — use only when result fits type
i64 pow_i64(i64 a, i64 e) {
    i64 r = 1;
    while (e > 0) {
        if (e & 1) r *= a;
        a *= a;
        e >>= 1;
    }
    return r;
}
} // namespace binpow
```

### Python 3 Template

```python
def mod_pow(a: int, e: int, mod: int) -> int:
    return pow(a % mod, e, mod)  # CPython built-in; prefer this always

def mat_mul(A, B, mod):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if not aik:
                continue
            for j in range(p):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C

def mat_pow(A, e, mod):
    n = len(A)
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        e >>= 1
    return R
```

---

## 6. Recognition Trigger Signals & Heuristics

- Compute `a^b`, `a^b mod m`, or huge powers in formulas
- Fibonacci / linear recurrences → matrix expo
- “Apply operation k times” on a small state
- Need `pow(a, n-2, n)` for inverse (prime mod)

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `a %= mod` when `a` can be negative or `≥ mod`
- Using `long long` mul without `__int128` when `mod ~ 1e18`
- `mod=1` → result must be `0`
- Recursive pow blowing stack on deep recursion (prefer iterative)
- Matrix identity wrong size / not taking mod on intermediate sums

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

- **Euler totient reduction:** if `gcd(a,m)=1`, `a^n ≡ a^{n mod φ(m)} (mod m)`; if not coprime, need `a^n = a^{φ(m)+[n≥φ(m)?...]}` carefully (use CRT / lifting)
- **Power tower:** right-assoc, reduce exponents mod `λ(m)` with thresholds
- **Infinite modpow for products:** keep exponents for each prime separately

---

## 11. Typical Problem Archetypes

1. Standard application: `a^b mod m`
2. Slightly disguised: count strings / colorings `k^n mod p`
3. Difficult: matrix expo DP transition
4. Very difficult / advanced: tetration / power towers mod m

---

## 12. Recognition & Identification Drills

1. Compute `2^{10^{18}} mod 1e9+7`.
2. nth Fibonacci mod m for `n ≤ 10^{18}`.
3. Number of paths of length k in a digraph with ≤100 nodes.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: any large exponent
- Key invariant: `a^n = a^{2⌊n/2⌋} · a^{n mod 2}`
- Key formula: binary decomposition of exponent
- Complexity: `O(log n)` mul
- Template to remember: while e: if e&1 r*=a; a*=a; e>>=1

---

---
