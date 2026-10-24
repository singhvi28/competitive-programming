# 8. Euler phi

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** Multiplicative functions, factorization / sieve  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Multiplicative functions, factorization / sieve

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

`φ(n) = |{k: 1≤k≤n, gcd(k,n)=1}|`. Multiplicative: for `n=∏ p^e`, `φ(n)=n∏_{p|n}(1-1/p)`. Appears in **Euler’s theorem** `a^{φ(n)}≡1 (mod n)` when coprime, order divides φ(n), and counting fractions / necklaces / generators bounds.

---

## 4. Proof Sketches & Recurrences

Inclusion-exclusion: `φ(n)=n∑_{d|n} μ(d)/d`.  
Prime power: `φ(p^e)=p^e-p^{e-1}=p^{e-1}(p-1)`.  
Sieve: `φ[i]=i` init; for prime p, for multiples: `φ[j]-=φ[j]/p`.  
Linear sieve: if `i%p==0` then `φ[i*p]=φ[i]*p` else `φ[i*p]=φ[i]*(p-1)`.

Identity: `∑_{d|n} φ(d) = n`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)` sieve; `O(√n)` single
- Per-query / per-operation: `O(1)` after sieve
- Total: prep dominated
- Memory: `O(N)``

### C++17 Template

```cpp
namespace euler_phi {
using i64 = long long;
i64 phi_single(i64 n) {
    i64 res = n, x = n;
    for (i64 p = 2; p * p <= x; ++p) if (x % p == 0) {
        while (x % p == 0) x /= p;
        res -= res / p;
    }
    if (x > 1) res -= res / x;
    return res;
}
void phi_sieve(int n, std::vector<int>& phi, std::vector<int>& spf, std::vector<int>& primes) {
    phi.assign(n + 1, 0);
    spf.assign(n + 1, 0);
    primes.clear();
    phi[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!spf[i]) { spf[i] = i; primes.push_back(i); phi[i] = i - 1; }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > n) break;
            spf[i * p] = p;
            if (i % p == 0) { phi[i * p] = phi[i] * p; break; }
            else phi[i * p] = phi[i] * (p - 1);
        }
    }
}
// prefix sum of phi
std::vector<i64> phi_prefix(const std::vector<int>& phi) {
    std::vector<i64> s(phi.size());
    for (size_t i = 1; i < phi.size(); ++i) s[i] = s[i - 1] + phi[i];
    return s;
}
} // namespace euler_phi
```

### Python 3 Template

```python
def phi_single(n: int) -> int:
    res, x = n, n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            res -= res // p
        p += 1 if p == 2 else 2
    if x > 1:
        res -= res // x
    return res

def phi_sieve(n: int):
    phi = [0] * (n + 1)
    spf = [0] * (n + 1)
    primes = []
    phi[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
            if i % p == 0:
                phi[i * p] = phi[i] * p
                break
            else:
                phi[i * p] = phi[i] * (p - 1)
    return phi, spf, primes
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count integers ≤n coprime to n / to m
- Reduce huge exponents mod φ(m)
- Sum of `φ(d)` over d|n equals n
- Totient summatory `∑_{i=1}^n φ(i)`

---

## 7. Contest WA / TLE / RE Traps

- Using `a^{φ(m)}≡1` when `gcd(a,m)≠1`
- Exponent reduction: need `n ≥ some threshold` when not coprime (CRT by prime powers)
- `phi[1]=1` forgotten
- Linear sieve: forgetting `break` when `i%p==0`

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

- Summatory totient / lattice points visible from origin: `∑ φ(d)⌊n/d⌋^2` style
- Jordan totient (rare)
- φ inverse (find n given φ(n) — search)

---

## 11. Typical Problem Archetypes

1. Standard application: compute φ(n)
2. Slightly disguised: count fractions a/b ≤1 with denom ≤n in lowest terms
3. Difficult: sum `∑_{i=1}^n φ(i)` for large n (Dirichlet convolution / Du Jiao)
4. Very difficult / advanced: orders / Carmichael λ alongside φ

---

## 12. Recognition & Identification Drills

1. Compute φ(1), φ(p), φ(p^k), φ(2p).
2. Prove/use `∑_{d|n} φ(d)=n` to count generators of cyclic something.
3. Evaluate `2^{10^{18}} mod 10^{9}+7` vs mod composite — when reduce by φ?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: coprime counts, Euler theorem
- Key invariant: multiplicative; `∑_{d|n}φ(d)=n`
- Key formula: `φ(n)=n∏(1-1/p)`
- Complexity: `O(√n)` or `O(N)` sieve
- Template to remember: linear sieve φ recurrence

---

Continue with Möbius → BSGS in [12-b-number-theory-mobius-bsgs.md](12-b-number-theory-mobius-bsgs.md).

---
