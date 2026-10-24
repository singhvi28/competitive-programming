# Divisor Tricks

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** Divisors, harmonic summation intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: Divisors, harmonic summation intuition

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

Two pillars: (1) **enumerate divisors** in `O(√n)` or via SPF; (2) **floor blocks** — `⌊n/i⌋` is constant on segments, so `∑_{i=1}^n f(⌊n/i⌋)` becomes `O(√n)` segments. Same idea for `∑_{d|k} g(d)` by iterating multiples. Thinking in “multiples vs divisors” swaps often simplifies counting.

---

## 4. Proof Sketches & Recurrences

Floor blocks: for fixed n and l, maximal r with `⌊n/i⌋` equal for i∈[l,r] is `min(n, ⌊n/⌊n/l⌋⌋)`.  
Number of blocks `O(√n)`.  
Dirichlet convolution on prefixes: `∑_{i=1}^n ∑_{d|i} f(d) = ∑_d f(d)⌊n/d⌋`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N log N)` for d/σ sieve
- Per-query / per-operation: `O(√n)` floor sum / divisors
- Total: as used
- Memory: `O(N)` tables or `O(√n)` divisor list`

### C++17 Template

```cpp
namespace divtricks {
using i64 = long long;
std::vector<i64> divisors(i64 n) {
    std::vector<i64> d, big;
    for (i64 i = 1; i * i <= n; ++i) if (n % i == 0) {
        d.push_back(i);
        if (i * i != n) big.push_back(n / i);
    }
    d.insert(d.end(), big.rbegin(), big.rend());
    return d;
}
// sum_{i=1}^n floor(n/i)
i64 sum_floor(i64 n) {
    i64 ans = 0;
    for (i64 l = 1, r; l <= n; l = r + 1) {
        i64 v = n / l;
        r = n / v;
        ans += (r - l + 1) * v;
    }
    return ans;
}
// generic: for each block [l,r], value = n/l
template <class F>
void floor_blocks(i64 n, F f) {
    for (i64 l = 1, r; l <= n; l = r + 1) {
        i64 v = n / l;
        r = n / v;
        f(l, r, v);
    }
}
// d[i] = number of divisors via sieve
void sieve_d_sigma(int n, std::vector<int>& d, std::vector<i64>& sigma) {
    d.assign(n + 1, 0);
    sigma.assign(n + 1, 0);
    for (int i = 1; i <= n; ++i)
        for (int j = i; j <= n; j += i) { ++d[j]; sigma[j] += i; }
}
} // namespace divtricks
```

### Python 3 Template

```python
def divisors(n: int) -> list[int]:
    small, big = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i * i != n:
                big.append(n // i)
        i += 1
    return small + big[::-1]

def floor_blocks(n: int):
    l = 1
    while l <= n:
        v = n // l
        r = n // v
        yield l, r, v
        l = r + 1

def sum_floor(n: int) -> int:
    return sum((r - l + 1) * v for l, r, v in floor_blocks(n))
```

---

## 6. Recognition Trigger Signals & Heuristics

- Sum involving `⌊n/i⌋`, `⌊n/i⌋·i`, divisor sums
- For all k, compute something about multiples of k
- Harmonic loops `for (i=1;i<=n;i+=…)`
- d(n), σ(n) batch computation

---

## 7. Contest WA / TLE / RE Traps

- `r = n/(n/l)` overflow / 0 when not careful with 64-bit
- Infinite loop if `r < l` (shouldn’t if careful)
- Enumerating all pairs `i,j` instead of multiples
- `O(n)` sum when `n=1e12` without blocks → TLE

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

- 2D floor: `⌊n/i/j⌋` nested blocks
- Min_25 / powerful number sieve (advanced)
- Enumerate `lcm(i,j)` via gcd rewrite

---

## 11. Typical Problem Archetypes

1. Standard application: `∑ ⌊n/i⌋`
2. Slightly disguised: sum of GCDs `∑_{i=1}^n gcd(i,n)`
3. Difficult: Dirichlet prefix / Titu’s lemma style sums
4. Very difficult / advanced: dual variables floor for Dujiao

---

## 12. Recognition & Identification Drills

1. Compute `∑_{i=1}^n ⌊n/i⌋` for `n=1e12`.
2. Sum of number of divisors `∑_{i=1}^n d(i)`.
3. For each q, answer `∑_{i=1}^{n} [⌊n/i⌋ = q]` counts.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: harmonic / divisor sums
- Key invariant: `⌊n/i⌋` constant on blocks
- Key formula: `r = n / (n/l)`
- Complexity: `O(√n)` per sum
- Template to remember: floor_blocks loop

---

---
