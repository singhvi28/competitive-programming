# Section §12: Number Theory & Multiplicative Functions

> **Module ID:** `sec-12`  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Topic Count:** 21  

**Module Summary:** Extended Euclidean, Linear Diophantine, Linear Sieve with Smallest Prime Factor (SPF), Euler Totient phi, Dirichlet convolution, Möbius Inversion, and BSGS.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Fast Exponentiation](#topic-1) | `S-tier` | 800–1600 (appears inside harder problems constantly) | Very Common | [01-12-fast-exponentiation.md](./01-12-fast-exponentiation.md) |
| 2 | [Extended Euclidean Algorithm](#topic-2) | `S-tier` | 1200–1800 | Common | [02-12-extended-euclidean-algorithm.md](./02-12-extended-euclidean-algorithm.md) |
| 3 | [Modular Inverse](#topic-3) | `S-tier` | 1200–1800 | Very Common | [03-12-modular-inverse.md](./03-12-modular-inverse.md) |
| 4 | [Chinese Remainder Theorem](#topic-4) | `A-tier` | 1600–2200 | Occasional | [04-12-chinese-remainder-theorem.md](./04-12-chinese-remainder-theorem.md) |
| 5 | [Linear Diophantine Equations](#topic-5) | `A-tier` | 1400–2000 | Occasional | [05-12-linear-diophantine-equations.md](./05-12-linear-diophantine-equations.md) |
| 6 | [Sieve / Linear Sieve](#topic-6) | `S-tier` | 1200–1800 | Very Common | [06-12-sieve-linear-sieve.md](./06-12-sieve-linear-sieve.md) |
| 7 | [SPF](#topic-7) | `S-tier` | 1400–2000 | Common | [07-12-spf.md](./07-12-spf.md) |
| 8 | [Euler phi](#topic-8) | `A-tier` | 1400–2000 | Common | [08-12-euler-phi.md](./08-12-euler-phi.md) |
| 9 | [Möbius Function](#topic-9) | `A-tier` | 1800–2400 | Occasional | [09-12-m-bius-function.md](./09-12-m-bius-function.md) |
| 10 | [Divisor Tricks](#topic-10) | `A-tier` | 1500–2200 | Common | [10-12-divisor-tricks.md](./10-12-divisor-tricks.md) |
| 11 | [Inclusion-Exclusion](#topic-11) | `S-tier` | 1600–2300 | Common | [11-12-inclusion-exclusion.md](./11-12-inclusion-exclusion.md) |
| 12 | [Multiplicative Functions](#topic-12) | `A-tier` | 1700–2400 | Occasional | [12-12-multiplicative-functions.md](./12-12-multiplicative-functions.md) |
| 13 | [Miller-Rabin Primality Testing](#topic-13) | `B-tier` | 1800–2400 | Occasional | [13-12-miller-rabin-primality-testing.md](./13-12-miller-rabin-primality-testing.md) |
| 14 | [Pollard-Rho Factorization](#topic-14) | `B-tier` | 2000–2600 | Occasional | [14-12-pollard-rho-factorization.md](./14-12-pollard-rho-factorization.md) |
| 15 | [Primitive Roots](#topic-15) | `C-tier` | 2000–2600 | Rare | [15-12-primitive-roots.md](./15-12-primitive-roots.md) |
| 16 | [Discrete Logarithm / Baby-Step Giant-Step](#topic-16) | `C-tier` | 2100–2700 | Rare | [16-12-discrete-logarithm-baby-step-giant-step.md](./16-12-discrete-logarithm-baby-step-giant-step.md) |
| 17 | [High ROI (learn now)](#topic-17) | `B-tier` | 1600–2200 | Common | [17-12-high-roi-learn-now.md](./17-12-high-roi-learn-now.md) |
| 18 | [Situational (clear recognition → deploy)](#topic-18) | `B-tier` | 1600–2200 | Common | [18-12-situational-clear-recognition-deploy.md](./18-12-situational-clear-recognition-deploy.md) |
| 19 | [Rarely worth early / niche](#topic-19) | `B-tier` | 1600–2200 | Common | [19-12-rarely-worth-early-niche.md](./19-12-rarely-worth-early-niche.md) |
| 20 | [Part A — [12-a-number-theory-binpow-euler.md](12-a-number-theory-binpow-euler.md)](#topic-20) | `B-tier` | 1600–2200 | Common | [20-12-part-a-12-a-number-theory-binpow-euler-md-12-a-number-theory-binpow-euler-md.md](./20-12-part-a-12-a-number-theory-binpow-euler-md-12-a-number-theory-binpow-euler-md.md) |
| 21 | [Part B — [12-b-number-theory-mobius-bsgs.md](12-b-number-theory-mobius-bsgs.md)](#topic-21) | `B-tier` | 1600–2200 | Common | [21-12-part-b-12-b-number-theory-mobius-bsgs-md-12-b-number-theory-mobius-bsgs-md.md](./21-12-part-b-12-b-number-theory-mobius-bsgs-md-12-b-number-theory-mobius-bsgs-md.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Fast Exponentiation

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 800–1600 (appears inside harder problems constantly) | **Frequency:** Very Common  
> **Prerequisites:** Modular arithmetic, integer overflow awareness  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 800–1600 (appears inside harder problems constantly)
- Prerequisites: Modular arithmetic, integer overflow awareness

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Multiplying `a` by itself `n` times is linear. Binary exponentiation rewrites `n` in binary: each bit is a squaring step, and you multiply into the answer only for set bits. Same idea lifts to **matrix powering**, **binary lifting on functional graphs**, and **modpow inside MR**. Mentally: “square the base, consume the exponent bit.”

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log e)` mulmods (`O(d^3 log e)` matrices)
- Total: as above
- Memory: `O(1)` scalar; `O(d^2)` matrices`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Compute `a^b`, `a^b mod m`, or huge powers in formulas
- Fibonacci / linear recurrences → matrix expo
- “Apply operation k times” on a small state
- Need `pow(a, n-2, n)` for inverse (prime mod)

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `a %= mod` when `a` can be negative or `≥ mod`
- Using `long long` mul without `__int128` when `mod ~ 1e18`
- `mod=1` → result must be `0`
- Recursive pow blowing stack on deep recursion (prefer iterative)
- Matrix identity wrong size / not taking mod on intermediate sums

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Euler totient reduction:** if `gcd(a,m)=1`, `a^n ≡ a^{n mod φ(m)} (mod m)`; if not coprime, need `a^n = a^{φ(m)+[n≥φ(m)?...]}` carefully (use CRT / lifting)
- **Power tower:** right-assoc, reduce exponents mod `λ(m)` with thresholds
- **Infinite modpow for products:** keep exponents for each prime separately

---

#### 11. Typical Problem Archetypes

1. Standard application: `a^b mod m`
2. Slightly disguised: count strings / colorings `k^n mod p`
3. Difficult: matrix expo DP transition
4. Very difficult / advanced: tetration / power towers mod m

---

#### 12. Recognition & Identification Drills

1. Compute `2^{10^{18}} mod 1e9+7`.
2. nth Fibonacci mod m for `n ≤ 10^{18}`.
3. Number of paths of length k in a digraph with ≤100 nodes.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: any large exponent
- Key invariant: `a^n = a^{2⌊n/2⌋} · a^{n mod 2}`
- Key formula: binary decomposition of exponent
- Complexity: `O(log n)` mul
- Template to remember: while e: if e&1 r*=a; a*=a; e>>=1

---

---


---

<a id="topic-2"></a>
### 2. Extended Euclidean Algorithm

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Common  
> **Prerequisites:** gcd, modular arithmetic basics  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: gcd, modular arithmetic basics

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`gcd(a,b) = gcd(b, a mod b)`. Back-substitute to write `gcd = ax + by`. This single identity unlocks **modular inverse**, **linear Diophantine**, and **CRT merge**. Don’t memorize coefficients — run the recursive (or iterative) process and reconstruct `x,y`.

---

#### 4. Proof Sketches & Recurrences

Base: `b=0` → `gcd=a`, `x=1`, `y=0`.  
Inductive: `a = bq + r`. If `bx' + ry' = g`, then `bx' + (a-bq)y' = g` ⇒ `a y' + b(x' - q y') = g`.  
So `(x,y) = (y', x' - ⌊a/b⌋ y')`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log min(a,b))`
- Total: same
- Memory: `O(log)` recursion depth or `O(1)` iterative`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Find any / all integer solutions to `ax + by = c`”
- Inverse when modulus is not prime
- Merge two congruences
- Bézout coefficients needed explicitly

---

#### 7. Contest WA / TLE / RE Traps

- Signs: `a,b` negative — normalize or track signs
- Returning `y` for the wrong variable after swap
- Assuming `gcd` always positive — take `abs` if needed for inverse
- Using recursive version on pathological deep cases (rare for 64-bit)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Generalized:** `gcd` of n numbers + coefficients via fold
- **Half-GCD / Knuth-Schönhage:** niche, not for CF
- Feed into CRT / Diophantine sections below

---

#### 11. Typical Problem Archetypes

1. Standard application: inverse of `a` mod `m`
2. Slightly disguised: chicken nugget / Frobenius with two numbers
3. Difficult: parametric solutions under inequalities
4. Very difficult / advanced: lattice reduction style (rare)

---

#### 12. Recognition & Identification Drills

1. Find integers x,y with `39x + 15y = 12` or prove impossible.
2. Compute inverse of 7 mod 26.
3. Merge `x≡2 (mod 6)` with a second congruence using Bézout.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: Bézout / inverse / Diophantine
- Key invariant: `gcd` preserved; coefficients back-sub
- Key formula: `g = ax+by`
- Complexity: `O(log)`
- Template to remember: recursive swap `(x,y)=(y1, x1-(a/b)y1)`

---

---


---

<a id="topic-3"></a>
### 3. Modular Inverse

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Very Common  
> **Prerequisites:** binpow or ExtEuclid; primes vs composite moduli  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: binpow or ExtEuclid; primes vs composite moduli

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Division mod `m` means multiply by `a^{-1}` where `a·a^{-1}≡1 (mod m)`, exists iff `gcd(a,m)=1`. Two engines: **Fermat/Euler** (`a^{φ(m)-1}`) when coprime, or **ExtEuclid** (`ax+my=1`). For factorials, precompute inv of `n!` then back-derive `inv[i]`.

---

#### 4. Proof Sketches & Recurrences

- Prime `p`: Fermat `a^{p-2} ≡ a^{-1} (mod p)` for `a≠0`.
- General: ExtEuclid → `ax≡1 (mod m)` iff `gcd=1`; `x mod m` is inverse.
- Linear sieve of inverses: `inv[1]=1`, `inv[i] = mod - (mod/i)*inv[mod%i]%mod` for prime mod.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(n + log mod)` for fact/invfact; `O(n)` inv_range
- Per-query / per-operation: `O(log mod)` single inverse; `O(1)` nCr after prep
- Total: as above
- Memory: `O(n)` for tables`

##### C++17 Template

```cpp
namespace modinv {
using i64 = long long;
i64 mod_pow(i64 a, i64 e, i64 mod); // from binpow

i64 inv_fermat(i64 a, i64 mod) { // mod prime
    return mod_pow(a, mod - 2, mod);
}
i64 inv_egcd(i64 a, i64 mod) {
    i64 x, y;
    i64 g = extgcd::egcd(a, mod, x, y);
    if (g != 1 && g != -1) return -1; // no inverse
    x %= mod;
    if (x < 0) x += mod;
    return x;
}
// inv[1..n] mod prime P
void inv_range(int n, int P, std::vector<int>& inv) {
    inv.assign(n + 1, 0);
    inv[1] = 1;
    for (int i = 2; i <= n; ++i)
        inv[i] = (i64)(P - P / i) * inv[P % i] % P;
}
// factorial + inv factorial for nCr
struct FactInv {
    int mod;
    std::vector<int> fac, ifac;
    FactInv(int n, int mod) : mod(mod), fac(n + 1), ifac(n + 1) {
        fac[0] = 1;
        for (int i = 1; i <= n; ++i) fac[i] = (i64)fac[i - 1] * i % mod;
        ifac[n] = (int)inv_fermat(fac[n], mod);
        for (int i = n; i >= 1; --i) ifac[i - 1] = (i64)ifac[i] * i % mod;
    }
    int C(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return (i64)fac[n] * ifac[k] % mod * ifac[n - k] % mod;
    }
};
} // namespace modinv
```

##### Python 3 Template

```python
def inv_fermat(a: int, mod: int) -> int:
    return pow(a, mod - 2, mod)  # mod prime

def inv_egcd(a: int, mod: int) -> int | None:
    g, x, _ = egcd(a % mod, mod)
    if g != 1:
        return None
    return x % mod

def inv_range(n: int, P: int) -> list[int]:
    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (P - P // i) * inv[P % i] % P
    return inv
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Combinatorics mod prime: `nCr`, Catalan
- Formulas with division
- Modular geometric series
- Hashing with division (rare — prefer multiply)

---

#### 7. Contest WA / TLE / RE Traps

- Fermat on composite modulus (wrong)
- `a=0` or not coprime — no inverse
- `ifac[n] = inv(fac[n])` then loop down — off-by-one if `n=0`
- Mixing `%` with negative intermediates

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Inverse of product / geometric: `inv(1-r)`
- CRT: invert mod each prime power then combine
- Montgomery form (only for heavy mulmod engines)

---

#### 11. Typical Problem Archetypes

1. Standard application: `nCr mod p`
2. Slightly disguised: expected value mod p (multiply by inv of denom)
3. Difficult: Lucas for large n, small p
4. Very difficult / advanced: inverse mod `p^k` via Hensel

---

#### 12. Recognition & Identification Drills

1. Precompute all `nCr` for `n ≤ 1e6` mod `1e9+7`.
2. Solve `3x ≡ 1 (mod 10^{9}+9)` — wait, check if modulus prime first.
3. Sum of inverses `∑_{i=1}^n i^{-1} mod p`.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: division in modular formulas
- Key invariant: `a·inv(a)≡1`
- Key formula: `a^{p-2}` or ExtEuclid
- Complexity: `O(log m)` or `O(1)` after tables
- Template to remember: fact + ifac back-propagation

---

---


---

<a id="topic-4"></a>
### 4. Chinese Remainder Theorem

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Occasional  
> **Prerequisites:** ExtEuclid, modular inverse, lcm/gcd  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: ExtEuclid, modular inverse, lcm/gcd

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

A system `x ≡ a_i (mod m_i)` asks for an integer living in several residue classes. If moduli are **pairwise coprime**, solutions exist unique mod `M=∏ m_i`. Constructively: `x = ∑ a_i M_i y_i` with `M_i=M/m_i`, `y_i = M_i^{-1} mod m_i`. If not coprime, still OK iff `a_i ≡ a_j (mod gcd(m_i,m_j))`; merge pairwise.

---

#### 4. Proof Sketches & Recurrences

Merge two: `x ≡ a (mod m)`, `x ≡ b (mod n)`. Write `x = a + m·t`, need `a + m t ≡ b (mod n)` ⇒ `m t ≡ b-a (mod n)`. Solve with ExtEuclid; let `g=gcd(m,n)`. Solvable iff `g | (b-a)`. Then `t` mod `n/g`, and new modulus `lcm=m/g*n`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(k log M)` for k equations
- Total: same
- Memory: `O(k)``

##### C++17 Template

```cpp
namespace crt {
using i64 = long long;
// merge x≡a (mod m), x≡b (mod n) -> {x0, lcm} or {-1,-1} if impossible
// assumes 0 ≤ a < m, 0 ≤ b < n; result x0 in [0, lcm)
std::pair<i64, i64> crt2(i64 a, i64 m, i64 b, i64 n) {
    i64 x, y;
    i64 g = extgcd::egcd(m, n, x, y);
    if ((b - a) % g) return {-1, -1};
    i64 mod = n / g;
    i64 t = ((__int128)(b - a) / g * x) % mod;
    if (t < 0) t += mod;
    i64 lcm = m / g * n;
    i64 res = ((__int128)a + (__int128)m * t) % lcm;
    if (res < 0) res += lcm;
    return {res, lcm};
}
// general: vectors a[i], m[i]
std::pair<i64, i64> crt_all(const std::vector<i64>& a, const std::vector<i64>& m) {
    i64 A = 0, M = 1;
    for (size_t i = 0; i < a.size(); ++i) {
        auto [nA, nM] = crt2(A, M, a[i] % m[i], m[i]);
        if (nM == -1) return {-1, -1};
        A = nA; M = nM;
    }
    return {A, M};
}
} // namespace crt
```

##### Python 3 Template

```python
def crt2(a: int, m: int, b: int, n: int) -> tuple[int, int] | None:
    g, x, _ = egcd(m, n)
    if (b - a) % g:
        return None
    mod = n // g
    t = ((b - a) // g * x) % mod
    lcm = m // g * n
    return (a + m * t) % lcm, lcm

def crt_all(aa: list[int], mm: list[int]) -> tuple[int, int] | None:
    A, M = 0, 1
    for a, m in zip(aa, mm):
        merged = crt2(A, M, a % m, m)
        if merged is None:
            return None
        A, M = merged
    return A, M
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Find x satisfying several remainders”
- Modulus is product of small primes; compute mod each then CRT
- Counting with period `lcm` of cycles
- Garner for explicit mixed-radix

---

#### 7. Contest WA / TLE / RE Traps

- Overflow on `m/g*n` — use `__int128` or big int
- Not normalizing `a_i` into `[0,m_i)`
- Assuming pairwise coprime when they’re not
- Wrong `lcm` formula (`m*n` without `/g`)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Garner algorithm:** explicit coefficients for fixed moduli (NTT / multipoint)
- **Explicit formula** when pairwise coprime
- Mod `2^{64}` natural wrap as CRT component (hackcare)

---

#### 11. Typical Problem Archetypes

1. Standard application: x ≡ a (mod m), x ≡ b (mod n)
2. Slightly disguised: two calendars / sleep cycles collide
3. Difficult: CRT + counting solutions in a range
4. Very difficult / advanced: CRT in non-coprime towers / Hensel lift

---

#### 12. Recognition & Identification Drills

1. Find smallest nonneg x: x≡2 mod 3, x≡3 mod 5, x≡2 mod 7.
2. Impossible system: x≡1 mod 4, x≡2 mod 6 — explain.
3. Compute nCr mod 1e9+9? (composite) — CRT over prime factors.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: multi-modulus residues
- Key invariant: consistency mod gcd
- Key formula: pairwise merge via ExtEuclid
- Complexity: `O(k log)`
- Template to remember: `crt2` then fold

---

---


---

<a id="topic-5"></a>
### 5. Linear Diophantine Equations

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Occasional  
> **Prerequisites:** ExtEuclid  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: ExtEuclid

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`ax + by = c` solvable ⇔ `gcd(a,b) | c`. One particular solution from ExtEuclid scaled by `c/g`; general solution adds the kernel: `x += (b/g)·t`, `y -= (a/g)·t`. Contest problems often ask **nonnegative** solutions or min `x+y` — constrain `t` by inequalities.

---

#### 4. Proof Sketches & Recurrences

Let `g=gcd(a,b)`. ExtEuclid: `a x0 + b y0 = g`. Multiply by `c/g`: particular `(x*,y*)`.  
General: `x = x* + (b/g)t`, `y = y* - (a/g)t`, `t∈Z`.  
Nonnegative: solve bounds on `t` from `x≥0`, `y≥0`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log)`
- Total: same
- Memory: `O(1)``

##### C++17 Template

```cpp
namespace dioph {
using i64 = long long;
// find any solution to a x + b y = c; false if impossible
bool any_sol(i64 a, i64 b, i64 c, i64 &x, i64 &y, i64 &g) {
    g = extgcd::egcd(std::abs(a), std::abs(b), x, y);
    if (c % g) return false;
    x *= c / g;
    y *= c / g;
    if (a < 0) x = -x;
    if (b < 0) y = -y;
    return true;
}
// shift particular solution by t
void shift(i64 a, i64 b, i64 g, i64 &x, i64 &y, i64 t) {
    x += t * (b / g);
    y -= t * (a / g);
}
// count nonnegative solutions (a,b>0)
i64 count_nonneg(i64 a, i64 b, i64 c) {
    i64 x, y, g;
    if (!any_sol(a, b, c, x, y, g)) return 0;
    i64 bg = b / g, ag = a / g;
    // x + bg*t ≥ 0, y - ag*t ≥ 0
    // ceil((-x)/bg) ≤ t ≤ floor(y/ag)
    auto ceil_div = [](i64 p, i64 q) {
        if (q < 0) p = -p, q = -q;
        return p >= 0 ? (p + q - 1) / q : p / q;
    };
    auto floor_div = [](i64 p, i64 q) {
        if (q < 0) p = -p, q = -q;
        return p >= 0 ? p / q : -((-p + q - 1) / q);
    };
    i64 lo = ceil_div(-x, bg);
    i64 hi = floor_div(y, ag);
    return hi >= lo ? hi - lo + 1 : 0;
}
} // namespace dioph
```

##### Python 3 Template

```python
def any_sol(a: int, b: int, c: int):
    g, x, y = egcd(abs(a), abs(b))
    if c % g:
        return None
    x *= c // g
    y *= c // g
    if a < 0:
        x = -x
    if b < 0:
        y = -y
    return x, y, g

def count_nonneg(a: int, b: int, c: int) -> int:
    sol = any_sol(a, b, c)
    if sol is None:
        return 0
    x, y, g = sol
    from math import ceil
    bg, ag = b // g, a // g
    lo = ceil(-x / bg)
    hi = y // ag
    return max(0, hi - lo + 1)
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Frogs, jumps, buying items with two costs
- “Can you make sum s with coins a,b (unlimited)?”
- Number of nonnegative solutions
- Same as CRT when rewritten as congruences

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `g | c`
- Sign errors when `a` or `b` negative
- Off-by-one in ceil/floor for `t` range
- Overflow when `a,b` near `1e18`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Three variables: reduce free variables (harder constraints)
- `ax + by + cz = n` with bounds — enumerate one variable
- Congruence form `ax ≡ c (mod b)`

---

#### 11. Typical Problem Archetypes

1. Standard application: solve `ax+by=c`
2. Slightly disguised: two button presses to reach n
3. Difficult: minimize cost with `x,y ≥ 0`
4. Very difficult / advanced: lattice points in polygons (geometry+)

---

#### 12. Recognition & Identification Drills

1. Number of nonnegative solutions to `3x+5y=100`.
2. Can you measure exactly z liters with jugs a,b?
3. Smallest nonnegative x with `ax ≡ b (mod m)`.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: linear eq in integers
- Key invariant: `g|c`
- Key formula: `x=x0+(b/g)t`, `y=y0-(a/g)t`
- Complexity: `O(log)`
- Template to remember: ExtEuclid then bound `t`

---

---


---

<a id="topic-6"></a>
### 6. Sieve / Linear Sieve

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1200–1800 | **Frequency:** Very Common  
> **Prerequisites:** primes, arrays  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1200–1800
- Prerequisites: primes, arrays

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Classic Eratosthenes marks multiples of each prime. **Linear sieve** ensures each composite `n` is crossed out **once**, by its SPF: for prime `p ≤ spf[i]`, mark `i*p`. Same pass builds the prime list and SPF table — the gateway to factoring many small numbers and sieving multiplicative functions.

---

#### 4. Proof Sketches & Recurrences

Classic: for `p` prime, mark `2p,3p,...` → `∑_{p} N/p = O(N log log N)`.  
Linear: each `n=spf(n)·m` with `spf(n) ≤ spf(m)` is generated once. Proof of linearity: every composite has unique SPF factorization order in the nested loops. `O(N)` time, `O(N)` memory.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)` linear; `O(N log log N)` classic
- Per-query / per-operation: `O(1)` prime test via `spf[i]==i`
- Total: prep dominated
- Memory: `O(N)``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Need all primes ≤ N (`N≤1e7` typical)
- Prefactorization of many queries `≤N`
- Compute φ, μ, d(n), σ(n) for all `≤N`
- Count primes / sum primes in prefix

---

#### 7. Contest WA / TLE / RE Traps

- `N` too large for memory (`1e8` ints ~400MB — watch limits)
- Breaking condition `p > spf[i]` wrong → not linear / wrong SPF
- Marking `1` as prime
- Segmented sieve needed when `R-L` small but `R` huge — different tool

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Segmented sieve:** primes in `[L,R]` with `R≤1e12`, `R-L≤1e7`
- **Bitset sieve:** memory/speed win for prime list only
- Wheel factorization (niche)

---

#### 11. Typical Problem Archetypes

1. Standard application: list primes ≤ n
2. Slightly disguised: sum of primes in range via prefix
3. Difficult: sieve DP over primes
4. Very difficult / advanced: min_25 / advanced prime sums (beyond this section)

---

#### 12. Recognition & Identification Drills

1. Count primes in `[1,n]` for `n=1e7`.
2. For t=1e5 queries, factor each `x≤1e7`.
3. Find all primes in `[1e12, 1e12+1e6]` — which sieve?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: batch prime/SPF work ≤1e7
- Key invariant: each n marked by SPF once (linear)
- Key formula: for p≤spf[i], mark i*p
- Complexity: `O(N)`
- Template to remember: linear sieve loop with break

---

---


---

<a id="topic-7"></a>
### 7. SPF

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** Linear sieve  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Linear sieve

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`spf[n]` = smallest prime dividing `n`. Factorization becomes repeated division by SPF: `n → n/spf[n]` until 1 — **`O(log n)` per number** after `O(N)` prep. This dominates “factor many numbers ≤ N” problems and feeds μ/φ sieves.

---

#### 4. Proof Sketches & Recurrences

From linear sieve, `spf[i*p]=p` when `p ≤ spf[i]`. Correctness: p is smallest prime factor of `i*p`. Factor loop: while n>1, pe = spf[n], count multiplicity while divisible.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)` sieve
- Per-query / per-operation: `O(log n)` factor
- Total: `O(N + q log A)`
- Memory: `O(N)``

##### C++17 Template

```cpp
namespace spf_fact {
// requires sieve::spf filled
std::vector<std::pair<int,int>> factor(int n) {
    std::vector<std::pair<int,int>> f;
    while (n > 1) {
        int p = sieve::spf[n], e = 0;
        while (n % p == 0) n /= p, ++e;
        f.push_back({p, e});
    }
    return f;
}
int omega(int n) { // distinct primes
    return (int)factor(n).size();
}
bool square_free(int n) {
    while (n > 1) {
        int p = sieve::spf[n];
        n /= p;
        if (n % p == 0) return false;
    }
    return true;
}
// factorize with trial using primes when n > sieve bound once
} // namespace spf_fact
```

##### Python 3 Template

```python
def factor_spf(n: int, spf: list[int]) -> list[tuple[int, int]]:
    f = []
    while n > 1:
        p, e = spf[n], 0
        while n % p == 0:
            n //= p
            e += 1
        f.append((p, e))
    return f
```

---

#### 6. Recognition Trigger Signals & Heuristics

- t up to 1e5–1e6 factorizations with `a_i ≤ 1e6–1e7`
- Need prime omega / big omega / radical quickly
- Square-free checks
- GCD convolution prep

---

#### 7. Contest WA / TLE / RE Traps

- Using SPF on `n > N` without fallback trial/Pollard
- Infinite loop if `spf[n]=0` for unset entries
- Multiplying factors back with overflow

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Keep only radical / μ sign while dividing
- Batch factor via SPF for arrays
- Highest prime factor (HPF) sieve variant

---

#### 11. Typical Problem Archetypes

1. Standard application: factor all a_i
2. Slightly disguised: remove square factors efficiently
3. Difficult: lcm of prefixes via max exponents
4. Very difficult / advanced: SPF + DSU on prime graph

---

#### 12. Recognition & Identification Drills

1. For each a_i, compute number of divisors using SPF.
2. Check if product of array is square (exponent parity).
3. Build graph: edge if gcd>1, using primes as hubs.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: many factorizations ≤ N
- Key invariant: divide by spf repeatedly
- Key formula: `n = ∏ p^e`
- Complexity: `O(log n)/query`
- Template to remember: while n>1: p=spf[n], peel

---

---


---

<a id="topic-8"></a>
### 8. Euler phi

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** Multiplicative functions, factorization / sieve  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Multiplicative functions, factorization / sieve

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`φ(n) = |{k: 1≤k≤n, gcd(k,n)=1}|`. Multiplicative: for `n=∏ p^e`, `φ(n)=n∏_{p|n}(1-1/p)`. Appears in **Euler’s theorem** `a^{φ(n)}≡1 (mod n)` when coprime, order divides φ(n), and counting fractions / necklaces / generators bounds.

---

#### 4. Proof Sketches & Recurrences

Inclusion-exclusion: `φ(n)=n∑_{d|n} μ(d)/d`.  
Prime power: `φ(p^e)=p^e-p^{e-1}=p^{e-1}(p-1)`.  
Sieve: `φ[i]=i` init; for prime p, for multiples: `φ[j]-=φ[j]/p`.  
Linear sieve: if `i%p==0` then `φ[i*p]=φ[i]*p` else `φ[i*p]=φ[i]*(p-1)`.

Identity: `∑_{d|n} φ(d) = n`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)` sieve; `O(√n)` single
- Per-query / per-operation: `O(1)` after sieve
- Total: prep dominated
- Memory: `O(N)``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Count integers ≤n coprime to n / to m
- Reduce huge exponents mod φ(m)
- Sum of `φ(d)` over d|n equals n
- Totient summatory `∑_{i=1}^n φ(i)`

---

#### 7. Contest WA / TLE / RE Traps

- Using `a^{φ(m)}≡1` when `gcd(a,m)≠1`
- Exponent reduction: need `n ≥ some threshold` when not coprime (CRT by prime powers)
- `phi[1]=1` forgotten
- Linear sieve: forgetting `break` when `i%p==0`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Summatory totient / lattice points visible from origin: `∑ φ(d)⌊n/d⌋^2` style
- Jordan totient (rare)
- φ inverse (find n given φ(n) — search)

---

#### 11. Typical Problem Archetypes

1. Standard application: compute φ(n)
2. Slightly disguised: count fractions a/b ≤1 with denom ≤n in lowest terms
3. Difficult: sum `∑_{i=1}^n φ(i)` for large n (Dirichlet convolution / Du Jiao)
4. Very difficult / advanced: orders / Carmichael λ alongside φ

---

#### 12. Recognition & Identification Drills

1. Compute φ(1), φ(p), φ(p^k), φ(2p).
2. Prove/use `∑_{d|n} φ(d)=n` to count generators of cyclic something.
3. Evaluate `2^{10^{18}} mod 10^{9}+7` vs mod composite — when reduce by φ?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: coprime counts, Euler theorem
- Key invariant: multiplicative; `∑_{d|n}φ(d)=n`
- Key formula: `φ(n)=n∏(1-1/p)`
- Complexity: `O(√n)` or `O(N)` sieve
- Template to remember: linear sieve φ recurrence

---

Continue with Möbius → BSGS in [12-b-number-theory-mobius-bsgs.md](12-b-number-theory-mobius-bsgs.md).

---


---

<a id="topic-9"></a>
### 9. Möbius Function

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Linear sieve, inclusion-exclusion, multiplicative functions  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Linear sieve, inclusion-exclusion, multiplicative functions

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`μ(n)` is the **signed square-free indicator** on the divisor lattice: `μ(n)=0` if square divides n; else `(-1)^k` for k distinct prime factors. Dirichlet inversion of the constant-1 function: `∑_{d|n} μ(d) = [n=1]`. That identity is why gcd-counting collapses — Möbius is IE packaged for divisors.

---

#### 4. Proof Sketches & Recurrences

Definition as above. Multiplicative. Linear sieve:
- prime p: `μ[p]=-1`
- `i%p==0` → `μ[i*p]=0` (square)
- else `μ[i*p]=-μ[i]`

Classic IE: numbers ≤n coprime to m: `∑_{d|m} μ(d)⌊n/d⌋`.  
Pairs: `∑_{i=1}^n∑_{j=1}^m [gcd=1] = ∑_d μ(d)⌊n/d⌋⌊m/d⌋`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)`
- Per-query / per-operation: `O(min(n,m))` naive; `O(√n)` with floor blocks
- Total: depends on floor enumeration
- Memory: `O(N)``

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Count pairs with `gcd=1` or `gcd=k`
- Invert `F(n)=∑_{d|n} f(d)` → `f(n)=∑_{d|n} μ(d)F(n/d)`
- Square-free enumeration
- GCD convolution / lcm counting

---

#### 7. Contest WA / TLE / RE Traps

- Using μ on non-square-free without zeroing
- Off-by-one on `μ[1]=1`
- TLE: summing `d=1..n` without `⌊n/d⌋` blocks when n=1e12
- Sign errors in inversion formula direction

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Möbius inversion on subset lattice** — different μ (see bitsets/SOS)
- Prefix μ + Dirichlet prefix techniques
- Sum of μ over `[1,n]` for large n (min_25 / Du Jiao — niche)

---

#### 11. Typical Problem Archetypes

1. Standard application: count coprime pairs
2. Slightly disguised: `∑∑ f(gcd(i,j))` rewrite via μ
3. Difficult: GCD convolution offline
4. Very difficult / advanced: Dirichlet prefix sums of μ·id_k

---

#### 12. Recognition & Identification Drills

1. Count pairs `(i,j)` in `[1,n]^2` with `gcd=1`.
2. Invert `F(n)=∑_{d|n}f(d)` given all F.
3. Count square-free integers ≤ n via μ^2.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: divisor-lattice IE / gcd conditions
- Key invariant: `∑_{d|n}μ(d)=[n=1]`
- Key formula: coprime pairs `∑ μ(d)⌊n/d⌋⌊m/d⌋`
- Complexity: sieve `O(N)`; queries with floor tricks
- Template to remember: linear sieve μ

---

---


---

<a id="topic-10"></a>
### 10. Divisor Tricks

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** Divisors, harmonic summation intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: Divisors, harmonic summation intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Two pillars: (1) **enumerate divisors** in `O(√n)` or via SPF; (2) **floor blocks** — `⌊n/i⌋` is constant on segments, so `∑_{i=1}^n f(⌊n/i⌋)` becomes `O(√n)` segments. Same idea for `∑_{d|k} g(d)` by iterating multiples. Thinking in “multiples vs divisors” swaps often simplifies counting.

---

#### 4. Proof Sketches & Recurrences

Floor blocks: for fixed n and l, maximal r with `⌊n/i⌋` equal for i∈[l,r] is `min(n, ⌊n/⌊n/l⌋⌋)`.  
Number of blocks `O(√n)`.  
Dirichlet convolution on prefixes: `∑_{i=1}^n ∑_{d|i} f(d) = ∑_d f(d)⌊n/d⌋`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N log N)` for d/σ sieve
- Per-query / per-operation: `O(√n)` floor sum / divisors
- Total: as used
- Memory: `O(N)` tables or `O(√n)` divisor list`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Sum involving `⌊n/i⌋`, `⌊n/i⌋·i`, divisor sums
- For all k, compute something about multiples of k
- Harmonic loops `for (i=1;i<=n;i+=…)`
- d(n), σ(n) batch computation

---

#### 7. Contest WA / TLE / RE Traps

- `r = n/(n/l)` overflow / 0 when not careful with 64-bit
- Infinite loop if `r < l` (shouldn’t if careful)
- Enumerating all pairs `i,j` instead of multiples
- `O(n)` sum when `n=1e12` without blocks → TLE

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- 2D floor: `⌊n/i/j⌋` nested blocks
- Min_25 / powerful number sieve (advanced)
- Enumerate `lcm(i,j)` via gcd rewrite

---

#### 11. Typical Problem Archetypes

1. Standard application: `∑ ⌊n/i⌋`
2. Slightly disguised: sum of GCDs `∑_{i=1}^n gcd(i,n)`
3. Difficult: Dirichlet prefix / Titu’s lemma style sums
4. Very difficult / advanced: dual variables floor for Dujiao

---

#### 12. Recognition & Identification Drills

1. Compute `∑_{i=1}^n ⌊n/i⌋` for `n=1e12`.
2. Sum of number of divisors `∑_{i=1}^n d(i)`.
3. For each q, answer `∑_{i=1}^{n} [⌊n/i⌋ = q]` counts.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: harmonic / divisor sums
- Key invariant: `⌊n/i⌋` constant on blocks
- Key formula: `r = n / (n/l)`
- Complexity: `O(√n)` per sum
- Template to remember: floor_blocks loop

---

---


---

<a id="topic-11"></a>
### 11. Inclusion-Exclusion

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Combinatorics, bitmasks or Möbius for lattices  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Combinatorics, bitmasks or Möbius for lattices

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Overcount unions by adding singles, subtracting doubles, …. In CP: either **bitmask IE** over ≤20 properties, or **divisor Möbius** when properties are “divisible by p”. Don’t force Möbius onto arbitrary sets — use plain IE when properties aren’t a product lattice.

---

#### 4. Proof Sketches & Recurrences

\[
\Bigl|\bigcup A_i\Bigr| = \sum |A_i| - \sum |A_i∩A_j| + \cdots + (-1)^{k+1}|∩_1^k A_i|
\]
Complement form often cleaner: total − union.  
Bitmask: for mask≠0, sign = `(-1)^{popcount+1}` for union, or `(-1)^{popcount}` for product IE `∏(1-x_p)`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: optional factorial tables
- Per-query / per-operation: `O(2^k · cost(∩))`
- Total: exponential in property count
- Memory: `O(k)``

##### C++17 Template

```cpp
namespace ie {
using i64 = long long;
// count integers in [1,n] not divisible by any a[i] (a[i] pairwise handled via lcm)
i64 count_free(i64 n, const std::vector<i64>& a) {
    int m = (int)a.size();
    i64 ans = 0;
    for (int mask = 1; mask < (1 << m); ++mask) {
        i64 l = 1;
        bool ok = true;
        int bits = 0;
        for (int i = 0; i < m; ++i) if (mask & (1 << i)) {
            ++bits;
            if (l > n / a[i]) { ok = false; break; } // lcm overflow guard (approx)
            i64 g = std::gcd(l, a[i]);
            l = l / g * a[i];
        }
        if (!ok || l == 0) continue;
        i64 add = n / l;
        ans += (bits % 2 ? add : -add);
    }
    return n - ans; // none of the a_i divide
}
// surjections onto [k]: ∑_{i=0}^{k} (-1)^i C(k,i) (k-i)^n
i64 surjections(int n, int k, int mod, const modinv::FactInv& fi) {
    i64 ans = 0;
    for (int i = 0; i <= k; ++i) {
        i64 ways = binpow::mod_pow(k - i, n, mod);
        i64 term = (i64)fi.C(k, i) * ways % mod;
        if (i & 1) ans = (ans - term) % mod;
        else ans = (ans + term) % mod;
    }
    if (ans < 0) ans += mod;
    return ans;
}
} // namespace ie
```

##### Python 3 Template

```python
from math import gcd

def count_not_divisible(n: int, a: list[int]) -> int:
    m = len(a)
    bad = 0
    for mask in range(1, 1 << m):
        l, bits = 1, 0
        ok = True
        for i in range(m):
            if mask >> i & 1:
                bits += 1
                g = gcd(l, a[i])
                if l // g > n // a[i]:
                    ok = False
                    break
                l = l // g * a[i]
        if not ok:
            continue
        bad += (n // l) if bits % 2 else -(n // l)
    return n - bad
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Count objects avoiding a list of bad events
- “At least one / exactly k” constraints
- Coprimality with small prime set
- Surjective functions / onto mappings (`k! · Stirling2` = IE)

---

#### 7. Contest WA / TLE / RE Traps

- Wrong sign (`(-1)^{|S|}` vs `|S|+1`)
- LCM overflow / not using gcd when multiplying
- Double-counting unstructured properties that aren’t independent in model
- Using Möbius μ when a plain bitmask IE is enough (overkill bugs)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- IE on trees / graphs (chromatic polynomial style)
- Principle for expected value linearity (not IE but related)
- Stirling / onto counts

---

#### 11. Typical Problem Archetypes

1. Standard application: multiples of at least one of given primes
2. Slightly disguised: derangements formula
3. Difficult: IE over primes of a modulus + CRT
4. Very difficult / advanced: IE + generating functions

---

#### 12. Recognition & Identification Drills

1. Count integers ≤n divisible by 2,3, or 5.
2. Number of onto functions `[n]→[k]`.
3. Count arrays where no position equals a forbidden list (per-index).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: union of structured bad sets
- Key invariant: alternating signs by subset size
- Key formula: classic IE sum
- Complexity: `O(2^k)`
- Template to remember: iterate masks, lcm, sign

---

---


---

<a id="topic-12"></a>
### 12. Multiplicative Functions

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** SPF / linear sieve, φ, μ, d, σ  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: SPF / linear sieve, φ, μ, d, σ

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

`f` multiplicative means `gcd(a,b)=1 ⇒ f(ab)=f(a)f(b)`. Completely multiplicative: even without coprime. **Define on prime powers, extend by product.** Linear sieve computes any multiplicative f if you know how `f(i*p)` relates when `p|i` vs not. Dirichlet convolution of multiplicative functions stays multiplicative.

---

#### 4. Proof Sketches & Recurrences

Linear sieve skeleton for multiplicative f:
- If `i % p != 0`: `f(i*p) = f(i)*f(p)`
- If `i % p == 0`: need `f(p^{e+1})` from knowing power — maintain `p^e || i` or special-case known f

Examples:
- `d(p^e)=e+1` → if p|i, `d(i*p)=d(i)/(e+1)*(e+2)` (store e) or simpler double loop
- `σ(p^e)=(p^{e+1}-1)/(p-1)`

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: `O(N)`
- Per-query / per-operation: `O(1)`
- Total: `O(N)`
- Memory: `O(N)` (extra cnt/pw arrays)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Need f(n) for all n≤N: φ, μ, d, σ, id_k, Jordan
- Prove a formula factors over primes
- GCD-sum rewritten as multiplicative series

---

#### 7. Contest WA / TLE / RE Traps

- Wrong branch when `p|i` for d(n)/σ(n)
- Treating additive functions as multiplicative
- Forgetting `f(1)=1`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Dirichlet convolution codes
- Prefix sums of multiplicative f (advanced)
- Completely multiplicative powers `n^k`

---

#### 11. Typical Problem Archetypes

1. Standard application: batch φ,μ,d
2. Slightly disguised: sum of multiplicative f over multiples
3. Difficult: invent f from problem, prove multiplicative, sieve it
4. Very difficult / advanced: Dirichlet series / L-functions style (not CF)

---

#### 12. Recognition & Identification Drills

1. Sieve `σ(n)` (sum of divisors) linearly.
2. Show `id = 1 * φ` and recover φ by inversion.
3. Compute `∑_{k=1}^n μ(k)^2` (square-free count).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: f defined via prime powers for all ≤N
- Key invariant: multiplicativity + sieve branches
- Key formula: `f(ab)=f(a)f(b)` when coprime
- Complexity: `O(N)`
- Template to remember: linear sieve with p|i case

---

---


---

<a id="topic-13"></a>
### 13. Miller-Rabin Primality Testing

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** modpow, careful 64-bit mulmod; factorization pipeline  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: modpow, careful 64-bit mulmod; factorization pipeline

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Fermat tests are weak; MR uses the factorization of `a^{n-1}-1` along the chain `a^q, a^{2q}, …, a^{2^{s-1}q}` (where `n-1=2^s q`). A prime forces this sequence to hit `1` only after a `-1` (or start at `1`); a composite “witness” fails with high probability. For 64-bit integers, **deterministic base sets** exist: check a fixed handful of bases → exact primality for `n < 2^64`.

---

#### 4. Proof Sketches & Recurrences

Write `n-1 = 2^s · q` (q odd). For base a: compute `a^q mod n`. Prime ⇒ sequence becomes 1 after some squaring, and first 1 is preceded by n-1 (or already 1). If neither `a^q≡1` nor `a^{2^i q}≡-1` for some i<s → composite.  
Deterministic bases for 64-bit: `{2,3,5,7,11,13,23}` (one common set; others exist).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(k · log n · mul)` with k≈7 bases
- Total: same
- Memory: `O(1)``

##### C++17 Template

```cpp
namespace miller_rabin {
using u64 = unsigned long long;
using u128 = __uint128_t;
u64 mul_mod(u64 a, u64 b, u64 mod) {
    return (u128)a * b % mod;
}
u64 pow_mod(u64 a, u64 e, u64 mod) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return r;
}
bool is_prime(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ull, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37})
        if (n % p == 0) return n == p;
    u64 d = n - 1, s = 0;
    while ((d & 1) == 0) d >>= 1, ++s;
    auto check = [&](u64 a) {
        if (a % n == 0) return true;
        u64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) return true;
        for (u64 i = 1; i < s; ++i) {
            x = mul_mod(x, x, n);
            if (x == n - 1) return true;
        }
        return false;
    };
    // deterministic for all 64-bit n
    for (u64 a : {2ull, 3, 5, 7, 11, 13, 23})
        if (!check(a)) return false;
    return true;
}
} // namespace miller_rabin
```

##### Python 3 Template

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    def check(a: int) -> bool:
        if a % n == 0:
            return True
        x = pow(a, d, n)  # big-int safe; no manual mulmod
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False
    return all(check(a) for a in (2, 3, 5, 7, 11, 13, 23))
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Test primality of `n ≤ 10^18` (or `2^64-1`)
- Inside Pollard–Rho recursion
- Sparse need for many random big primes

---

#### 7. Contest WA / TLE / RE Traps

- Overflow mulmod in C++
- Forgetting small prime trial (speed + edge)
- Using probabilistic bases without enough rounds for 64-bit
- `n=1`, even n edge cases

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Probabilistic MR for bigints >>64-bit (crypto sizes)
- Baillie–PSW (stronger hybrid)
- Deterministic bases for 32-bit only: `{2,7,61}`

---

#### 11. Typical Problem Archetypes

1. Standard application: is `n` prime?
2. Slightly disguised: next prime / generate prime
3. Difficult: count primes in weird sequences with MR tests
4. Very difficult / advanced: primality for 256-bit (need more)

---

#### 12. Recognition & Identification Drills

1. Test `10^9+7`, `10^18+3`, and a semiprime near `1e18`.
2. Find any witness that detects a known Carmichael number via MR (vs Fermat).
3. Wire MR as the leaf test of Pollard–Rho.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: 64-bit primality
- Key invariant: strong pseudoprime conditions
- Key formula: `n-1=2^s q` witness check
- Complexity: `O(k log n)` mulmods
- Template to remember: deterministic bases + mulmod

---

---


---

<a id="topic-14"></a>
### 14. Pollard-Rho Factorization

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Miller–Rabin, gcd, mulmod  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Miller–Rabin, gcd, mulmod

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Factor composite n by walking a polynomial sequence `x ↦ x^2+c mod n` and using **Floyd / Brent** to find `x,y` with `g=gcd(|x-y|,n)` nontrivial. Birthday collision in the hidden factor’s residue class. Recurse with MR as prime check. For `n≤1e18`, this is the standard contest factorizer.

---

#### 4. Proof Sketches & Recurrences

If p|n unknown, sequence mod p has cycle ~`O(√p)`. Brent’s cycle detection accumulates product of differences to amortize gcd. Expected time roughly `O(n^{1/4})` per factor for typical n. Trial-divide small primes first; then Rho; then MR.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: expected `~O(n^{1/4})` per hard factor
- Total: factorization tree
- Memory: `O(log n)` recursion + factor list`

##### C++17 Template

```cpp
namespace pollard {
using u64 = unsigned long long;
using u128 = __uint128_t;
u64 mul_mod(u64 a, u64 b, u64 mod) { return (u128)a * b % mod; }
u64 f(u64 x, u64 c, u64 mod) { return (mul_mod(x, x, mod) + c) % mod; }

u64 brent(u64 n) {
    if (n % 2 == 0) return 2;
    std::mt19937_64 rng(n);
    for (;;) {
        u64 y = rng() % (n - 1) + 1, c = rng() % (n - 1) + 1, m = 128;
        u64 g = 1, r = 1, q = 1, x = 0, ys = 0;
        while (g == 1) {
            x = y;
            for (u64 i = 0; i < r; ++i) y = f(y, c, n);
            u64 k = 0;
            while (k < r && g == 1) {
                ys = y;
                u64 lim = std::min(m, r - k);
                for (u64 i = 0; i < lim; ++i) {
                    y = f(y, c, n);
                    q = mul_mod(q, x > y ? x - y : y - x, n);
                }
                g = std::gcd(q, n);
                k += lim;
            }
            r *= 2;
        }
        if (g == n) {
            do {
                ys = f(ys, c, n);
                g = std::gcd(x > ys ? x - ys : ys - x, n);
            } while (g == 1);
        }
        if (g != n) return g;
    }
}

void factor(u64 n, std::vector<u64>& fac) {
    if (n == 1) return;
    if (miller_rabin::is_prime(n)) { fac.push_back(n); return; }
    for (u64 p : {2ull, 3, 5, 7, 11, 13, 17, 19, 23, 29}) {
        while (n % p == 0) { fac.push_back(p); n /= p; }
    }
    if (n == 1) return;
    if (miller_rabin::is_prime(n)) { fac.push_back(n); return; }
    u64 d = brent(n);
    factor(d, fac);
    factor(n / d, fac);
}
std::map<u64, int> factor_map(u64 n) {
    std::vector<u64> fac;
    factor(n, fac);
    std::map<u64, int> mp;
    for (u64 p : fac) ++mp[p];
    return mp;
}
} // namespace pollard
```

##### Python 3 Template

```python
import random
from math import gcd

def brent(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        y, c, m = random.randrange(1, n), random.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (pow(y, 2, n) + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (pow(y, 2, n) + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            while True:
                ys = (pow(ys, 2, n) + c) % n
                g = gcd(abs(x - ys), n)
                if g > 1:
                    break
        if g != n:
            return g

def factor(n: int, out: list[int] | None = None) -> list[int]:
    if out is None:
        out = []
    if n == 1:
        return out
    if is_prime(n):
        out.append(n)
        return out
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        while n % p == 0:
            out.append(p)
            n //= p
    if n == 1:
        return out
    if is_prime(n):
        out.append(n)
        return out
    d = brent(n)
    factor(d, out)
    factor(n // d, out)
    return out
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Factor one / few integers up to `1e18`
- Need full factorization for φ(n), orders, CRT moduli
- Semiprime challenges (not crypto-hard)

---

#### 7. Contest WA / TLE / RE Traps

- Missing MR → infinite recursion on primes
- Not trial-dividing small primes
- `gcd` product overflow without mod n
- Unlucky `c` — must retry loop
- Returning n itself forever without Brent fallback loop

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Floyd vs Brent
- Pollard p−1 (smooth p−1)
- ECM (almost never needed in CF)

---

#### 11. Typical Problem Archetypes

1. Standard application: factor `n≤1e18`
2. Slightly disguised: compute φ(n) for large n
3. Difficult: factor many n with shared templates
4. Very difficult / advanced: crypto CTF sizes (out of scope)

---

#### 12. Recognition & Identification Drills

1. Factor `100000000003` (example — use your tester).
2. Given n, count divisors via full factorization.
3. Solve order problems needing factor of `p-1`.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: 64-bit factorization
- Key invariant: gcd of sequence diffs hits a factor
- Key formula: Brent rho + MR leaves
- Complexity: ~`n^{1/4}`
- Template to remember: brent + recursive factor

---

---


---

<a id="topic-15"></a>
### 15. Primitive Roots

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** φ, factorization, modpow, orders  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: φ, factorization, modpow, orders

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

A primitive root g mod n is a generator of `(Z/nZ)*` when that group is cyclic. Exists for `n = 2,4,p^k,2p^k` (odd prime p). Order of g is `φ(n)`. Find by testing candidates: g is primitive root iff `g^{φ(n)/q} ≠ 1 (mod n)` for every prime q|φ(n).

---

#### 4. Proof Sketches & Recurrences

Group cyclic ⇒ ∃ element of order `φ(n)`. Test: order divides φ(n); if `g^{φ(n)/q} ≠ 1` for every prime `q | φ(n)`, order is exactly φ(n). Factor `φ(n)` via Pollard if n large.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: factor `φ(n)` 
- Per-query / per-operation: `O(p^{ε} · |fac| log n)` search for small g (usually tiny)
- Total: dominated by factorization + few tests
- Memory: factor map`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Problem asks for generator mod p
- Discrete log setup
- Constructing NTT-ish generators (usually fixed primes)
- Problems about existence of generators

---

#### 7. Contest WA / TLE / RE Traps

- Testing only `g^{φ/2}≠1` (insufficient)
- Assuming root exists for all n (e.g. mod 15 no)
- Using g not coprime to n
- Wrong factorization of p−1

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Discrete log needs any generator
- Minimal primitive root bounds (theory)
- Generators mod p^k via lift

---

#### 11. Typical Problem Archetypes

1. Standard application: find g mod p
2. Slightly disguised: construct element of order k | p−1
3. Difficult: count primitive roots `φ(φ(n))`
4. Very difficult / advanced: Artin’s conjecture style (not contest)

---

#### 12. Recognition & Identification Drills

1. Find a primitive root mod 7, mod 41.
2. Does 8 have a primitive root?
3. Given p, find g then solve discrete log of a small a.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: generators / setup for dlog
- Key invariant: `g^{φ/q}≠1` all prime q|φ
- Key formula: order test via factors of φ(n)
- Complexity: factor + few modpows
- Template to remember: factor p−1, test g=2,3,…

---

---


---

<a id="topic-16"></a>
### 16. Discrete Logarithm / Baby-Step Giant-Step

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2100–2700 | **Frequency:** Rare  
> **Prerequisites:** modpow, meet-in-the-middle, inverse, preferably primitive roots / gcd handling  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: modpow, meet-in-the-middle, inverse, preferably primitive roots / gcd handling

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Solve `a^x ≡ b (mod m)` for x. BSGS: let `x = i·B - j` with `B≈√N`, `N=order` (often `m-1` for prime m). Precompute baby steps `a^j`, match giant steps `b·(a^{-B})^i`. Meet-in-the-middle in the cyclic subgroup. If gcd(a,m)>1, peel common factors / reduce carefully.

---

#### 4. Proof Sketches & Recurrences

Assume mod prime p, a≠0, work in order `n = ord(a)` or `p-1`.  
`a^{iB} ≡ b · a^j` with `0≤j<B`, `i=0..⌈n/B⌉`.  
Hash map `a^j → j` (keep minimal j). For each i, query.  
Complexity `O(√n)` time and memory. Pohlig–Hellman reduces to dlog mod prime powers of `p-1` when smooth.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (per query map)
- Per-query / per-operation: `O(√p)` time and memory (prime modulus case)
- Total: same; Pohlig–Hellman faster if `p-1` smooth
- Memory: `O(√p)` hashmap`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Explicit “find discrete log”
- Order / exponential Diophantine in multiplicative group
- Hash-map meet-in-the-middle with powers

---

#### 7. Contest WA / TLE / RE Traps

- Hash collisions / forgetting `unordered_map` reserve
- Not handling `b=1` → x=0
- `gcd(a,p)>1` without reduction
- Using wrong order (should use ord(a) when subgroup smaller)
- Giant-step inverse wrong direction (`iB+j` vs `iB-j` convention)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Pohlig–Hellman:** factor order, solve CRT of subgroup logs
- BSGS for `a^x = b` in any group with known order
- Kangaroo / Pollard lambda for interval-restricted x

---

#### 11. Typical Problem Archetypes

1. Standard application: dlog mod p
2. Slightly disguised: find period / first time power hits b
3. Difficult: composite modulus + CRT split
4. Very difficult / advanced: PH + BSGS on 256-bit smooth orders

---

#### 12. Recognition & Identification Drills

1. Solve `2^x ≡ 5 (mod 101)`.
2. When does BSGS beat naive? Estimate √(p-1).
3. Outline Pohlig–Hellman given factorization of p−1.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: discrete log, order ~1e10–1e14 max for √
- Key invariant: meet-in-the-middle on exponent
- Key formula: `x = i√n + j`
- Complexity: `O(√n)`
- Template to remember: baby map + giant multiply by `a^{-B}`

---

## End Drill Pointer

Full weekly drill list and comparison tables live in [12-number-theory.md](12-number-theory.md). After Part B, prioritize: μ + floor blocks + IE recognition; keep MR+Pollard as a paste-ready block; skim primitive roots/BSGS until a problem forces them.

---


---

<a id="topic-17"></a>
### 17. High ROI (learn now)

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2100
- Prerequisites: Modular arithmetic, Euclidean GCD

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

High-yield Number Theory fundamentals: (1) Linear Sieve in $\mathcal{O}(N)$ computing Smallest Prime Factor (SPF), (2) Extended Euclidean Algorithm for modular inverses, and (3) Binary Exponentiation for fast powers and Fermat's Little Theorem.

---

#### 4. Proof Sketches & Recurrences

Linear Sieve invariant: each composite number $x$ is visited and marked exactly once by its smallest prime factor $p = \text{SPF}[x]$. Extended GCD: $a x + b y = \gcd(a, b)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Linear Sieve & Extended GCD Template
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e7 + 5;
int spf[MAXN];
vector<int> primes;

void linear_sieve(int n) {
    for (int i = 2; i <= n; ++i) {
        if (!spf[i]) { spf[i] = i; primes.push_back(i); }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > n) break;
            spf[i * p] = p;
        }
    }
}

long long ext_gcd(long long a, long long b, long long& x, long long& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    long long x1, y1;
    long long d = ext_gcd(b, a % b, x1, y1);
    x = y1; y = x1 - y1 * (a / b);
    return d;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Factoring integers up to $10^7$ in $\mathcal{O}(\log X)$ queries.
- Solving linear congruence $a x \equiv b \pmod m$.
- Modular combinations $\binom{N}{K} \pmod P$ using precomputed factorials.

---

#### 7. Contest WA / TLE / RE Traps

- Negative modulo result: `(a % m + m) % m` required in C++.
- Using `int` for intermediate products in modular multiplication.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---


---

<a id="topic-18"></a>
### 18. Situational (clear recognition → deploy)

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Multiplicative functions, Dirichlet convolution

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Möbius Inversion converts GCD conditions into divisor sums: $[\gcd(i, j) = 1] = \sum_{d | \gcd(i, j)} \mu(d)$. This simplifies double sums $\sum_{i=1}^N \sum_{j=1}^M f(\gcd(i, j))$ into single harmonic sweeps in $\mathcal{O}(N)$ or $\mathcal{O}(\sqrt{N})$.

---

#### 4. Proof Sketches & Recurrences

Dirichlet convolution $(f * g)(n) = \sum_{d | n} f(d) g(n/d)$. Inversion formula: $g = f * 1 \iff f = g * \mu$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Mobius Inversion & Square-Root Block Sums
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e6 + 5;
int mu[MAXN];

void compute_mu(int n) {
    vector<int> primes;
    vector<bool> is_comp(n + 1, false);
    mu[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!is_comp[i]) { primes.push_back(i); mu[i] = -1; }
        for (int p : primes) {
            if (i * p > n) break;
            is_comp[i * p] = true;
            if (i % p == 0) { mu[i * p] = 0; break; }
            else { mu[i * p] = -mu[i]; }
        }
    }
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Counting coprime pairs in range $[1, N] \times [1, M]$.
- Sum involving $\gcd(i, j)$ or $\text{lcm}(i, j)$ over multiple query bounds.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to stop prime loop when `i % p == 0`, violating linear sieve complexity.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---


---

<a id="topic-19"></a>
### 19. Rarely worth early / niche

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Miller-Rabin, Pollard's Rho, Baby-Step Giant-Step

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Large integer factorization ($N \le 10^{18}$) requires Miller-Rabin primality testing and Pollard's Rho algorithm in $\mathcal{O}(N^{1/4})$. Discrete logarithm $a^x \equiv b \pmod m$ requires Baby-Step Giant-Step (BSGS) in $\mathcal{O}(\sqrt{m})$.

---

#### 4. Proof Sketches & Recurrences

Pollard's Rho detects cycles in sequence $x_{i+1} = (x_i^2 + c) \pmod N$ using Floyd's cycle-finding algorithm and $\gcd(|x_i - x_j|, N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Pollard Rho & Miller Rabin 64-bit Primality Test
#include <bits/stdc++.h>
using namespace std;
using u64 = unsigned long long;
using u128 = __uint128_t;

u64 power(u64 base, u64 exp, u64 mod) {
    u64 res = 1; base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (u128)res * base % mod;
        base = (u128)base * base % mod;
        exp >>= 1;
    }
    return res;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Factoring integers up to $10^{18}$ in contest problems.
- Finding smallest $x$ such that $A^x \equiv B \pmod P$.

---

#### 7. Contest WA / TLE / RE Traps

- Overflow in 64-bit multiplication: must use `__int128`.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---


---

<a id="topic-20"></a>
### 20. Part A — [12-a-number-theory-binpow-euler.md](12-a-number-theory-binpow-euler.md)

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1300–2000
- Prerequisites: Modular arithmetic, prime factorization

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Number Theory Architecture Part A: Binary exponentiation, Fermat's Little Theorem, Euler's Totient Function $\phi(N)$, and linear Diophantine equations via Extended Euclidean algorithm.

---

#### 4. Proof Sketches & Recurrences

Euler's theorem: $a^{\phi(m)} \equiv 1 \pmod m$ whenever $\gcd(a, m) = 1$. Power reduction: $a^b \equiv a^{b \bmod \phi(m) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Euler Totient Function phi(N)
#include <bits/stdc++.h>
using namespace std;

long long phi(long long n) {
    long long result = n;
    for (long long p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Computing large power towers $a^{b^c} \pmod m$.
- Inverting non-prime modulo arithmetic.

---

#### 7. Contest WA / TLE / RE Traps

- Applying Fermat's Little Theorem $a^{P-2}$ when modulo is composite; must use Euler Totient or Extended GCD.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---


---

<a id="topic-21"></a>
### 21. Part B — [12-b-number-theory-mobius-bsgs.md](12-b-number-theory-mobius-bsgs.md)

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common in Div1 / ICPC
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Linear Sieve, Euler Totient, Möbius Inversion, Dirichlet Convolution, Baby-Step Giant-Step
- Tradeoff: Accelerates $\mathcal{O}(N^2)$ GCD summations to $\mathcal{O}(N)$ or $\mathcal{O}(\sqrt{N})$ and solves discrete logarithms in $\mathcal{O}(\sqrt{P})$.

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Number Theory provides the algebraic foundation for modular computation and prime factorization: Linear Sieve with Smallest Prime Factor (SPF), Extended Euclidean Algorithm, Chinese Remainder Theorem (CRT), Möbius Inversion, and Baby-Step Giant-Step (BSGS).

##### Fundamental Theorems & Invariants

- **Linear Sieve Theorem:** By ensuring each composite number $x = p \cdot i$ is marked only by its smallest prime factor $p = \text{SPF}[x]$, the sieve computes all primes and prime factorizations up to $N$ in strictly $\mathcal{O}(N)$ operations.
- **Bézout's Identity & ExtGCD:** For any integers $a, b$, there exist integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$, computed in $\mathcal{O}(\log(\min(a, b)))$ steps.
- **Möbius Inversion Formula:** If $g(n) = \sum_{d | n} f(d)$, then $f(n) = \sum_{d | n} \mu(d) g(n/d)$, where $\mu(n)$ is the Möbius function.
- **Euler's Totient Theorem:** For $\gcd(a, m) = 1$, $a^{\phi(m)} \equiv 1 \pmod m$. For arbitrary exponents, $a^b \equiv a^{(b \pmod{\phi(m)}) + \phi(m)} \pmod m$ for $b \ge \phi(m)$.

##### Algorithmic Execution Blueprint

1. **Linear Sieve:** Iterate $i$ from 2 to $N$. If $i$ is prime, add to `primes` and set $\text{SPF}[i]=i$. For each prime $p \le \text{SPF}[i]$ with $p \cdot i \le N$, set $\text{SPF}[p \cdot i] = p$.
2. **Extended GCD:** `extgcd(a, b, x, y)`: if $b == 0$, set $x=1, y=0$, return $a$. Recursively call `extgcd(b, a%b, x1, y1)`, then set $x = y1, y = x1 - y1 \cdot (a / b)$.
3. **Möbius Inversion for Coprime Pairs:** To count pairs $(i, j) \le N$ with $\gcd(i, j) = 1$, compute $\sum_{d=1}^N \mu(d) \lfloor N/d \rfloor^2$.

##### Closed-Form Invariant Equations

$$\mu(n) = \begin{cases} 1 & n=1 \\ 0 & p^2 | n \\ (-1)^k & n = p_1 p_2 \dots p_k \end{cases}, \quad \sum_{d | n} \mu(d) = [n = 1]$$

##### Structural Edge Cases & Assumptions

- Modular inverse of $a \pmod m$ exists if and only if $\gcd(a, m) = 1$.
- When working with power towers $a^{b^c} \pmod M$, modular reductions in exponents must use $\pmod{\phi(M)}$, not $\pmod M$.
- Möbius harmonic summation with $\lfloor N/d \rfloor$ square root partitioning evaluates in $\mathcal{O}(\sqrt{N})$ time.

---

#### 3. Core Intuition & Problem Framing

Part B covers multiplicative functions and discrete log: 1) **Möbius Inversion**: transforms GCD conditions $[\gcd(i, j) = 1] = \sum_{d | \gcd(i, j)} \mu(d)$. This swaps double summations $\sum_{i=1}^N \sum_{j=1}^M [\gcd(i, j) = 1] = \sum_{d=1}^{\min(N, M)} \mu(d) \lfloor N/d \rfloor \lfloor M/d \rfloor$, solvable in $\mathcal{O}(\sqrt{N})$ via square-root block decomposition. 2) **Baby-Step Giant-Step (BSGS)**: solves $a^x \equiv b \pmod m$ by writing $x = i \cdot m_0 - j$ with $m_0 = \lceil \sqrt{m} \rceil$, balancing table lookups in $\mathcal{O}(\sqrt{m})$.

---

#### 4. Proof Sketches & Recurrences

Möbius function $\mu(n)$ is defined as $(-1)^k$ if $n$ is square-free with $k$ prime factors, and $0$ otherwise. Dirichlet identity $\mu * 1 = \epsilon$ means $\sum_{d | n} \mu(d) = [n = 1]$. For BSGS, $a^{i \cdot m_0 - j} \equiv b \implies (a^{m_0})^i \equiv b \cdot a^j \pmod m$. We precompute all $b \cdot a^j$ for $j \in [0, m_0]$ in a hash map, then test $i = 1, 2, \dots, m_0$ until a collision is found.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Compute $\sum_{i=1}^N \sum_{j=1}^M \gcd(i, j)$ or $\text{lcm}(i, j)$ for $N, M \le 10^7$ or $10^9$.
- Solve modular exponential equation $A^X \equiv B \pmod P$ where $P \le 10^9$ (BSGS).
- Counting coprime pairs in a large grid.
- Evaluating Dirichlet convolutions $f * g$ using linear sieve.

---

#### 7. Contest WA / TLE / RE Traps

- BSGS when $\gcd(a, m) \ne 1$: standard BSGS assumes $\gcd(a, m) = 1$; if non-coprime, must factor out common divisors (Extended BSGS).
- Square-root floor division step: forgetting `int r = min(n / (n / l), m / (m / l))` causes incorrect chunk boundaries.
- Prefix sum array overflow: prefix sum of $\mu(i)$ can exceed 32-bit integer when multiplied by $\lfloor N/d \rfloor^2$; cast to `long long`.
- Modulo zero: $m = 1$ edge case in BSGS returning -1 instead of 0.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1033D | Divisors | 2100 | Number Theory, GCD, Factoring | GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho. | [Solve Problem](https://codeforces.com/contest/1033/problem/D) |
| Codeforces | CF-803F | Coprime Subsequences | 2000 | Möbius Inversion, Inclusion Exclusion | Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights. | [Solve Problem](https://codeforces.com/contest/803/problem/F) |
| Codeforces | CF-900D | Unusual Sequences | 2200 | Möbius Inversion, Number Theory, Combinatorics | Möbius function over divisors of y/x with fast memoized recursion. | [Solve Problem](https://codeforces.com/contest/900/problem/D) |
| CSES | CSES-1712 | Exponentiation II | 1500 | Binpow, Euler Phi | Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p. | [Solve Problem](https://cses.fi/problemset/task/1712) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- **[CP-Algorithms]** [CP-Algorithms: Extended Euclidean & Linear Diophantine](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- **[YouKn0wWho]** [YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions](https://youkn0wwho.academy/topic-list#mobius-inversion)

---


---
