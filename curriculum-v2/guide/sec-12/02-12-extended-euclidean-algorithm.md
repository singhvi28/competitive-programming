# 2. Extended Euclidean Algorithm

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Common  
> **Prerequisites:** gcd, modular arithmetic basics  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: gcd, modular arithmetic basics

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

`gcd(a,b) = gcd(b, a mod b)`. Back-substitute to write `gcd = ax + by`. This single identity unlocks **modular inverse**, **linear Diophantine**, and **CRT merge**. Don’t memorize coefficients — run the recursive (or iterative) process and reconstruct `x,y`.

---

## 4. Proof Sketches & Recurrences

Base: `b=0` → `gcd=a`, `x=1`, `y=0`.  
Inductive: `a = bq + r`. If `bx' + ry' = g`, then `bx' + (a-bq)y' = g` ⇒ `a y' + b(x' - q y') = g`.  
So `(x,y) = (y', x' - ⌊a/b⌋ y')`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log min(a,b))`
- Total: same
- Memory: `O(log)` recursion depth or `O(1)` iterative`

### C++17 Template

```cpp
namespace extgcd {
using i64 = long long;
// returns gcd; x,y satisfy a*x + b*y = gcd
i64 egcd(i64 a, i64 b, i64 &x, i64 &y) {
    if (b == 0) { x = 1; y = 0; return a; }
    i64 x1, y1;
    i64 g = egcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}
// iterative
i64 egcd_iter(i64 a, i64 b, i64 &x, i64 &y) {
    i64 x0 = 1, y0 = 0, x1 = 0, y1 = 1;
    while (b) {
        i64 q = a / b;
        a -= q * b; std::swap(a, b);
        x0 -= q * x1; std::swap(x0, x1);
        y0 -= q * y1; std::swap(y0, y1);
    }
    x = x0; y = y0;
    return a;
}
} // namespace extgcd
```

### Python 3 Template

```python
def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a,b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def egcd_iter(a: int, b: int) -> tuple[int, int, int]:
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Find any / all integer solutions to `ax + by = c`”
- Inverse when modulus is not prime
- Merge two congruences
- Bézout coefficients needed explicitly

---

## 7. Contest WA / TLE / RE Traps

- Signs: `a,b` negative — normalize or track signs
- Returning `y` for the wrong variable after swap
- Assuming `gcd` always positive — take `abs` if needed for inverse
- Using recursive version on pathological deep cases (rare for 64-bit)

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

- **Generalized:** `gcd` of n numbers + coefficients via fold
- **Half-GCD / Knuth-Schönhage:** niche, not for CF
- Feed into CRT / Diophantine sections below

---

## 11. Typical Problem Archetypes

1. Standard application: inverse of `a` mod `m`
2. Slightly disguised: chicken nugget / Frobenius with two numbers
3. Difficult: parametric solutions under inequalities
4. Very difficult / advanced: lattice reduction style (rare)

---

## 12. Recognition & Identification Drills

1. Find integers x,y with `39x + 15y = 12` or prove impossible.
2. Compute inverse of 7 mod 26.
3. Merge `x≡2 (mod 6)` with a second congruence using Bézout.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: Bézout / inverse / Diophantine
- Key invariant: `gcd` preserved; coefficients back-sub
- Key formula: `g = ax+by`
- Complexity: `O(log)`
- Template to remember: recursive swap `(x,y)=(y1, x1-(a/b)y1)`

---

---
