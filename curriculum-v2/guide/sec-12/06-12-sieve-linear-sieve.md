# 6. Sieve / Linear Sieve

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Very Common  
> **Prerequisites:** primes, arrays  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: primes, arrays

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

Classic Eratosthenes marks multiples of each prime. **Linear sieve** ensures each composite `n` is crossed out **once**, by its SPF: for prime `p ≤ spf[i]`, mark `i*p`. Same pass builds the prime list and SPF table — the gateway to factoring many small numbers and sieving multiplicative functions.

---

## 4. Proof Sketches & Recurrences

Classic: for `p` prime, mark `2p,3p,...` → `∑_{p} N/p = O(N log log N)`.  
Linear: each `n=spf(n)·m` with `spf(n) ≤ spf(m)` is generated once. Proof of linearity: every composite has unique SPF factorization order in the nested loops. `O(N)` time, `O(N)` memory.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)` linear; `O(N log log N)` classic
- Per-query / per-operation: `O(1)` prime test via `spf[i]==i`
- Total: prep dominated
- Memory: `O(N)``

### C++17 Template

```cpp
namespace sieve {
constexpr int N = 1'000'000;
int spf[N + 1];
std::vector<int> primes;
void linear_sieve() {
    std::fill(spf, spf + N + 1, 0);
    primes.clear();
    for (int i = 2; i <= N; ++i) {
        if (!spf[i]) { spf[i] = i; primes.push_back(i); }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > N) break;
            spf[i * p] = p;
        }
    }
}
// classic Eratosthenes (bitset-friendly)
void eratosthenes(std::vector<bool>& is_prime, int n) {
    is_prime.assign(n + 1, true);
    if (n >= 0) is_prime[0] = false;
    if (n >= 1) is_prime[1] = false;
    for (int i = 2; 1LL * i * i <= n; ++i)
        if (is_prime[i])
            for (int j = i * i; j <= n; j += i) is_prime[j] = false;
}
} // namespace sieve
```

### Python 3 Template

```python
def linear_sieve(n: int):
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
    return spf, primes

def eratosthenes(n: int) -> list[bool]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start : n + 1 : step] = [False] * (((n - start) // step) + 1)
    return is_prime
```

---

## 6. Recognition Trigger Signals & Heuristics

- Need all primes ≤ N (`N≤1e7` typical)
- Prefactorization of many queries `≤N`
- Compute φ, μ, d(n), σ(n) for all `≤N`
- Count primes / sum primes in prefix

---

## 7. Contest WA / TLE / RE Traps

- `N` too large for memory (`1e8` ints ~400MB — watch limits)
- Breaking condition `p > spf[i]` wrong → not linear / wrong SPF
- Marking `1` as prime
- Segmented sieve needed when `R-L` small but `R` huge — different tool

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

- **Segmented sieve:** primes in `[L,R]` with `R≤1e12`, `R-L≤1e7`
- **Bitset sieve:** memory/speed win for prime list only
- Wheel factorization (niche)

---

## 11. Typical Problem Archetypes

1. Standard application: list primes ≤ n
2. Slightly disguised: sum of primes in range via prefix
3. Difficult: sieve DP over primes
4. Very difficult / advanced: min_25 / advanced prime sums (beyond this section)

---

## 12. Recognition & Identification Drills

1. Count primes in `[1,n]` for `n=1e7`.
2. For t=1e5 queries, factor each `x≤1e7`.
3. Find all primes in `[1e12, 1e12+1e6]` — which sieve?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: batch prime/SPF work ≤1e7
- Key invariant: each n marked by SPF once (linear)
- Key formula: for p≤spf[i], mark i*p
- Complexity: `O(N)`
- Template to remember: linear sieve loop with break

---

---
