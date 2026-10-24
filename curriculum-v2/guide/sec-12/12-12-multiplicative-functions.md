# 12. Multiplicative Functions

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** SPF / linear sieve, φ, μ, d, σ  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: SPF / linear sieve, φ, μ, d, σ

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

`f` multiplicative means `gcd(a,b)=1 ⇒ f(ab)=f(a)f(b)`. Completely multiplicative: even without coprime. **Define on prime powers, extend by product.** Linear sieve computes any multiplicative f if you know how `f(i*p)` relates when `p|i` vs not. Dirichlet convolution of multiplicative functions stays multiplicative.

---

## 4. Proof Sketches & Recurrences

Linear sieve skeleton for multiplicative f:
- If `i % p != 0`: `f(i*p) = f(i)*f(p)`
- If `i % p == 0`: need `f(p^{e+1})` from knowing power — maintain `p^e || i` or special-case known f

Examples:
- `d(p^e)=e+1` → if p|i, `d(i*p)=d(i)/(e+1)*(e+2)` (store e) or simpler double loop
- `σ(p^e)=(p^{e+1}-1)/(p-1)`

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)`
- Per-query / per-operation: `O(1)`
- Total: `O(N)`
- Memory: `O(N)` (extra cnt/pw arrays)`

### C++17 Template

```cpp
namespace multfn {
// compute phi, mu, d simultaneously (d needs care)
void sieve_mult(int n, std::vector<int>& phi, std::vector<int>& mu,
                std::vector<int>& d, std::vector<int>& spf, std::vector<int>& primes) {
    phi.assign(n + 1, 0); mu.assign(n + 1, 0); d.assign(n + 1, 0);
    spf.assign(n + 1, 0);
    std::vector<int> cnt(n + 1, 0), pw(n + 1, 0); // cnt=exponent of spf, pw=p^e
    primes.clear();
    phi[1] = 1; mu[1] = 1; d[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!spf[i]) {
            spf[i] = i; primes.push_back(i);
            phi[i] = i - 1; mu[i] = -1; d[i] = 2;
            cnt[i] = 1; pw[i] = i;
        }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > n) break;
            int ip = i * p;
            spf[ip] = p;
            if (i % p == 0) {
                phi[ip] = phi[i] * p;
                mu[ip] = 0;
                cnt[ip] = cnt[i] + 1;
                pw[ip] = pw[i] * p;
                d[ip] = d[i] / (cnt[i] + 1) * (cnt[i] + 2);
                break;
            } else {
                phi[ip] = phi[i] * (p - 1);
                mu[ip] = -mu[i];
                cnt[ip] = 1; pw[ip] = p;
                d[ip] = d[i] * 2;
            }
        }
    }
}
} // namespace multfn
```

### Python 3 Template

```python
def sieve_phi_mu_d(n: int):
    phi = [0] * (n + 1)
    mu = [0] * (n + 1)
    d = [0] * (n + 1)
    spf = [0] * (n + 1)
    cnt = [0] * (n + 1)
    primes = []
    phi[1] = mu[1] = d[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
            phi[i], mu[i], d[i], cnt[i] = i - 1, -1, 2, 1
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            ip = i * p
            spf[ip] = p
            if i % p == 0:
                phi[ip] = phi[i] * p
                mu[ip] = 0
                cnt[ip] = cnt[i] + 1
                d[ip] = d[i] // (cnt[i] + 1) * (cnt[i] + 2)
                break
            else:
                phi[ip] = phi[i] * (p - 1)
                mu[ip] = -mu[i]
                cnt[ip] = 1
                d[ip] = d[i] * 2
    return phi, mu, d, spf, primes
```

---

## 6. Recognition Trigger Signals & Heuristics

- Need f(n) for all n≤N: φ, μ, d, σ, id_k, Jordan
- Prove a formula factors over primes
- GCD-sum rewritten as multiplicative series

---

## 7. Contest WA / TLE / RE Traps

- Wrong branch when `p|i` for d(n)/σ(n)
- Treating additive functions as multiplicative
- Forgetting `f(1)=1`

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

- Dirichlet convolution codes
- Prefix sums of multiplicative f (advanced)
- Completely multiplicative powers `n^k`

---

## 11. Typical Problem Archetypes

1. Standard application: batch φ,μ,d
2. Slightly disguised: sum of multiplicative f over multiples
3. Difficult: invent f from problem, prove multiplicative, sieve it
4. Very difficult / advanced: Dirichlet series / L-functions style (not CF)

---

## 12. Recognition & Identification Drills

1. Sieve `σ(n)` (sum of divisors) linearly.
2. Show `id = 1 * φ` and recover φ by inversion.
3. Compute `∑_{k=1}^n μ(k)^2` (square-free count).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: f defined via prime powers for all ≤N
- Key invariant: multiplicativity + sieve branches
- Key formula: `f(ab)=f(a)f(b)` when coprime
- Complexity: `O(N)`
- Template to remember: linear sieve with p|i case

---

---
