# Primitive Roots

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** φ, factorization, modpow, orders  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: φ, factorization, modpow, orders

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

A primitive root g mod n is a generator of `(Z/nZ)*` when that group is cyclic. Exists for `n = 2,4,p^k,2p^k` (odd prime p). Order of g is `φ(n)`. Find by testing candidates: g is primitive root iff `g^{φ(n)/q} ≠ 1 (mod n)` for every prime q|φ(n).

---

## 4. Proof Sketches & Recurrences

Group cyclic ⇒ ∃ element of order `φ(n)`. Test: order divides φ(n); if `g^{φ(n)/q} ≠ 1` for every prime `q | φ(n)`, order is exactly φ(n). Factor `φ(n)` via Pollard if n large.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: factor `φ(n)` 
- Per-query / per-operation: `O(p^{ε} · |fac| log n)` search for small g (usually tiny)
- Total: dominated by factorization + few tests
- Memory: factor map`

### C++17 Template

```cpp
namespace prot {
using i64 = long long;
i64 mod_pow(i64 a, i64 e, i64 mod);

bool is_primitive_root(i64 g, i64 n, i64 phi, const std::vector<i64>& factors) {
    if (std::gcd(g, n) != 1) return false;
    for (i64 q : factors)
        if (mod_pow(g, phi / q, n) == 1) return false;
    return true;
}
// find primitive root mod prime p
i64 find_primitive_root(i64 p) {
    if (p == 2) return 1;
    i64 phi = p - 1;
    auto mp = pollard::factor_map(phi);
    std::vector<i64> fac;
    for (auto [q, _] : mp) fac.push_back(q);
    for (i64 g = 2; g < p; ++g)
        if (is_primitive_root(g, p, phi, fac)) return g;
    return -1;
}
} // namespace prot
```

### Python 3 Template

```python
def is_primitive_root(g: int, n: int, phi: int, primes_dividing_phi: list[int]) -> bool:
    if gcd(g, n) != 1:
        return False
    return all(pow(g, phi // q, n) != 1 for q in primes_dividing_phi)

def find_primitive_root(p: int) -> int:
    if p == 2:
        return 1
    phi = p - 1
    # factor phi with pollard/trial
    fac = sorted(set(factor(phi)))
    for g in range(2, p):
        if is_primitive_root(g, p, phi, fac):
            return g
    return -1
```

---

## 6. Recognition Trigger Signals & Heuristics

- Problem asks for generator mod p
- Discrete log setup
- Constructing NTT-ish generators (usually fixed primes)
- Problems about existence of generators

---

## 7. Contest WA / TLE / RE Traps

- Testing only `g^{φ/2}≠1` (insufficient)
- Assuming root exists for all n (e.g. mod 15 no)
- Using g not coprime to n
- Wrong factorization of p−1

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

- Discrete log needs any generator
- Minimal primitive root bounds (theory)
- Generators mod p^k via lift

---

## 11. Typical Problem Archetypes

1. Standard application: find g mod p
2. Slightly disguised: construct element of order k | p−1
3. Difficult: count primitive roots `φ(φ(n))`
4. Very difficult / advanced: Artin’s conjecture style (not contest)

---

## 12. Recognition & Identification Drills

1. Find a primitive root mod 7, mod 41.
2. Does 8 have a primitive root?
3. Given p, find g then solve discrete log of a small a.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: generators / setup for dlog
- Key invariant: `g^{φ/q}≠1` all prime q|φ
- Key formula: order test via factors of φ(n)
- Complexity: factor + few modpows
- Template to remember: factor p−1, test g=2,3,…

---

---
