# 9. Möbius Function

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Linear sieve, inclusion-exclusion, multiplicative functions  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Linear sieve, inclusion-exclusion, multiplicative functions

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

`μ(n)` is the **signed square-free indicator** on the divisor lattice: `μ(n)=0` if square divides n; else `(-1)^k` for k distinct prime factors. Dirichlet inversion of the constant-1 function: `∑_{d|n} μ(d) = [n=1]`. That identity is why gcd-counting collapses — Möbius is IE packaged for divisors.

---

## 4. Proof Sketches & Recurrences

Definition as above. Multiplicative. Linear sieve:
- prime p: `μ[p]=-1`
- `i%p==0` → `μ[i*p]=0` (square)
- else `μ[i*p]=-μ[i]`

Classic IE: numbers ≤n coprime to m: `∑_{d|m} μ(d)⌊n/d⌋`.  
Pairs: `∑_{i=1}^n∑_{j=1}^m [gcd=1] = ∑_d μ(d)⌊n/d⌋⌊m/d⌋`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)`
- Per-query / per-operation: `O(min(n,m))` naive; `O(√n)` with floor blocks
- Total: depends on floor enumeration
- Memory: `O(N)``

### C++17 Template

```cpp
namespace mobius {
void mu_sieve(int n, std::vector<int>& mu, std::vector<int>& spf, std::vector<int>& primes) {
    mu.assign(n + 1, 0);
    spf.assign(n + 1, 0);
    primes.clear();
    mu[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!spf[i]) { spf[i] = i; primes.push_back(i); mu[i] = -1; }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > n) break;
            spf[i * p] = p;
            if (i % p == 0) { mu[i * p] = 0; break; }
            else mu[i * p] = -mu[i];
        }
    }
}
// prefix of mu for faster sums
std::vector<long long> mu_prefix(const std::vector<int>& mu) {
    std::vector<long long> s(mu.size());
    for (size_t i = 1; i < mu.size(); ++i) s[i] = s[i - 1] + mu[i];
    return s;
}
long long coprime_pairs(int n, int m, const std::vector<int>& mu) {
    int k = std::min(n, m);
    long long ans = 0;
    for (int d = 1; d <= k; ++d)
        if (mu[d]) ans += 1LL * mu[d] * (n / d) * (m / d);
    return ans;
}
} // namespace mobius
```

### Python 3 Template

```python
def mu_sieve(n: int):
    mu = [0] * (n + 1)
    spf = [0] * (n + 1)
    primes = []
    mu[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu, spf, primes

def coprime_pairs(n: int, m: int, mu: list[int]) -> int:
    return sum(mu[d] * (n // d) * (m // d) for d in range(1, min(n, m) + 1) if mu[d])
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count pairs with `gcd=1` or `gcd=k`
- Invert `F(n)=∑_{d|n} f(d)` → `f(n)=∑_{d|n} μ(d)F(n/d)`
- Square-free enumeration
- GCD convolution / lcm counting

---

## 7. Contest WA / TLE / RE Traps

- Using μ on non-square-free without zeroing
- Off-by-one on `μ[1]=1`
- TLE: summing `d=1..n` without `⌊n/d⌋` blocks when n=1e12
- Sign errors in inversion formula direction

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

- **Möbius inversion on subset lattice** — different μ (see bitsets/SOS)
- Prefix μ + Dirichlet prefix techniques
- Sum of μ over `[1,n]` for large n (min_25 / Du Jiao — niche)

---

## 11. Typical Problem Archetypes

1. Standard application: count coprime pairs
2. Slightly disguised: `∑∑ f(gcd(i,j))` rewrite via μ
3. Difficult: GCD convolution offline
4. Very difficult / advanced: Dirichlet prefix sums of μ·id_k

---

## 12. Recognition & Identification Drills

1. Count pairs `(i,j)` in `[1,n]^2` with `gcd=1`.
2. Invert `F(n)=∑_{d|n}f(d)` given all F.
3. Count square-free integers ≤ n via μ^2.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: divisor-lattice IE / gcd conditions
- Key invariant: `∑_{d|n}μ(d)=[n=1]`
- Key formula: coprime pairs `∑ μ(d)⌊n/d⌋⌊m/d⌋`
- Complexity: sieve `O(N)`; queries with floor tricks
- Template to remember: linear sieve μ

---

---
