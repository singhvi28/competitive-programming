# 5. Linear Diophantine Equations

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Occasional  
> **Prerequisites:** ExtEuclid  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: ExtEuclid

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

`ax + by = c` solvable ⇔ `gcd(a,b) | c`. One particular solution from ExtEuclid scaled by `c/g`; general solution adds the kernel: `x += (b/g)·t`, `y -= (a/g)·t`. Contest problems often ask **nonnegative** solutions or min `x+y` — constrain `t` by inequalities.

---

## 4. Proof Sketches & Recurrences

Let `g=gcd(a,b)`. ExtEuclid: `a x0 + b y0 = g`. Multiply by `c/g`: particular `(x*,y*)`.  
General: `x = x* + (b/g)t`, `y = y* - (a/g)t`, `t∈Z`.  
Nonnegative: solve bounds on `t` from `x≥0`, `y≥0`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(log)`
- Total: same
- Memory: `O(1)``

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Frogs, jumps, buying items with two costs
- “Can you make sum s with coins a,b (unlimited)?”
- Number of nonnegative solutions
- Same as CRT when rewritten as congruences

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `g | c`
- Sign errors when `a` or `b` negative
- Off-by-one in ceil/floor for `t` range
- Overflow when `a,b` near `1e18`

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

- Three variables: reduce free variables (harder constraints)
- `ax + by + cz = n` with bounds — enumerate one variable
- Congruence form `ax ≡ c (mod b)`

---

## 11. Typical Problem Archetypes

1. Standard application: solve `ax+by=c`
2. Slightly disguised: two button presses to reach n
3. Difficult: minimize cost with `x,y ≥ 0`
4. Very difficult / advanced: lattice points in polygons (geometry+)

---

## 12. Recognition & Identification Drills

1. Number of nonnegative solutions to `3x+5y=100`.
2. Can you measure exactly z liters with jugs a,b?
3. Smallest nonnegative x with `ax ≡ b (mod m)`.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: linear eq in integers
- Key invariant: `g|c`
- Key formula: `x=x0+(b/g)t`, `y=y0-(a/g)t`
- Complexity: `O(log)`
- Template to remember: ExtEuclid then bound `t`

---

---
