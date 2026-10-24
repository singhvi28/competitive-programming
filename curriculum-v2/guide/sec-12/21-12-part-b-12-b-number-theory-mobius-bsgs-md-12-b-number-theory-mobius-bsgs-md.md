# Part B — [12-b-number-theory-mobius-bsgs.md](12-b-number-theory-mobius-bsgs.md)

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Linear Sieve, Euler Totient, Möbius Inversion, Dirichlet Convolution, Baby-Step Giant-Step
- Tradeoff: Accelerates $\mathcal{O}(N^2)$ GCD summations to $\mathcal{O}(N)$ or $\mathcal{O}(\sqrt{N})$ and solves discrete logarithms in $\mathcal{O}(\sqrt{P})$.

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

Part B covers multiplicative functions and discrete log: 1) **Möbius Inversion**: transforms GCD conditions $[\gcd(i, j) = 1] = \sum_{d | \gcd(i, j)} \mu(d)$. This swaps double summations $\sum_{i=1}^N \sum_{j=1}^M [\gcd(i, j) = 1] = \sum_{d=1}^{\min(N, M)} \mu(d) \lfloor N/d \rfloor \lfloor M/d \rfloor$, solvable in $\mathcal{O}(\sqrt{N})$ via square-root block decomposition. 2) **Baby-Step Giant-Step (BSGS)**: solves $a^x \equiv b \pmod m$ by writing $x = i \cdot m_0 - j$ with $m_0 = \lceil \sqrt{m} \rceil$, balancing table lookups in $\mathcal{O}(\sqrt{m})$.

---

## 4. Proof Sketches & Recurrences

Möbius function $\mu(n)$ is defined as $(-1)^k$ if $n$ is square-free with $k$ prime factors, and $0$ otherwise. Dirichlet identity $\mu * 1 = \epsilon$ means $\sum_{d | n} \mu(d) = [n = 1]$. For BSGS, $a^{i \cdot m_0 - j} \equiv b \implies (a^{m_0})^i \equiv b \cdot a^j \pmod m$. We precompute all $b \cdot a^j$ for $j \in [0, m_0]$ in a hash map, then test $i = 1, 2, \dots, m_0$ until a collision is found.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// 1. Mobius Sieve & Floor Sum in O(sqrt(N))
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MAXN = 1e6 + 5;
int mu[MAXN], primes[MAXN], p_cnt = 0;
bool is_p[MAXN];

void sieve(int n) {
    fill(is_p, is_p + n + 1, true);
    mu[1] = 1; is_p[0] = is_p[1] = false;
    for (int i = 2; i <= n; ++i) {
        if (is_p[i]) { primes[++p_cnt] = i; mu[i] = -1; }
        for (int j = 1; j <= p_cnt && i * primes[j] <= n; ++j) {
            is_p[i * primes[j]] = false;
            if (i % primes[j] == 0) { mu[i * primes[j]] = 0; break; }
            mu[i * primes[j]] = -mu[i];
        }
    }
}

// 2. Baby-Step Giant-Step for a^x = b (mod m)
ll bsgs(ll a, ll b, ll m) {
    a %= m; b %= m;
    if (b == 1 || m == 1) return 0;
    ll k = ceil(sqrt(m)), cur = b;
    unordered_map<ll, ll> val;
    for (ll j = 0; j <= k; ++j) { val[cur] = j; cur = (cur * a) % m; }
    ll base = 1;
    for (ll i = 0; i < k; ++i) base = (base * a) % m;
    cur = 1;
    for (ll i = 1; i <= k + 1; ++i) {
        cur = (cur * base) % m;
        if (val.count(cur)) return i * k - val[cur];
    }
    return -1; // No solution
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Compute $\sum_{i=1}^N \sum_{j=1}^M \gcd(i, j)$ or $\text{lcm}(i, j)$ for $N, M \le 10^7$ or $10^9$.
- Solve modular exponential equation $A^X \equiv B \pmod P$ where $P \le 10^9$ (BSGS).
- Counting coprime pairs in a large grid.
- Evaluating Dirichlet convolutions $f * g$ using linear sieve.

---

## 7. Contest WA / TLE / RE Traps

- BSGS when $\gcd(a, m) \ne 1$: standard BSGS assumes $\gcd(a, m) = 1$; if non-coprime, must factor out common divisors (Extended BSGS).
- Square-root floor division step: forgetting `int r = min(n / (n / l), m / (m / l))` causes incorrect chunk boundaries.
- Prefix sum array overflow: prefix sum of $\mu(i)$ can exceed 32-bit integer when multiplied by $\lfloor N/d \rfloor^2$; cast to `long long`.
- Modulo zero: $m = 1$ edge case in BSGS returning -1 instead of 0.

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
