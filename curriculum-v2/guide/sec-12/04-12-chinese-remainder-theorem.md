# Chinese Remainder Theorem

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Occasional  
> **Prerequisites:** ExtEuclid, modular inverse, lcm/gcd  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: ExtEuclid, modular inverse, lcm/gcd

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

A system `x ≡ a_i (mod m_i)` asks for an integer living in several residue classes. If moduli are **pairwise coprime**, solutions exist unique mod `M=∏ m_i`. Constructively: `x = ∑ a_i M_i y_i` with `M_i=M/m_i`, `y_i = M_i^{-1} mod m_i`. If not coprime, still OK iff `a_i ≡ a_j (mod gcd(m_i,m_j))`; merge pairwise.

---

## 4. Proof Sketches & Recurrences

Merge two: `x ≡ a (mod m)`, `x ≡ b (mod n)`. Write `x = a + m·t`, need `a + m t ≡ b (mod n)` ⇒ `m t ≡ b-a (mod n)`. Solve with ExtEuclid; let `g=gcd(m,n)`. Solvable iff `g | (b-a)`. Then `t` mod `n/g`, and new modulus `lcm=m/g*n`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none
- Per-query / per-operation: `O(k log M)` for k equations
- Total: same
- Memory: `O(k)``

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- “Find x satisfying several remainders”
- Modulus is product of small primes; compute mod each then CRT
- Counting with period `lcm` of cycles
- Garner for explicit mixed-radix

---

## 7. Contest WA / TLE / RE Traps

- Overflow on `m/g*n` — use `__int128` or big int
- Not normalizing `a_i` into `[0,m_i)`
- Assuming pairwise coprime when they’re not
- Wrong `lcm` formula (`m*n` without `/g`)

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

- **Garner algorithm:** explicit coefficients for fixed moduli (NTT / multipoint)
- **Explicit formula** when pairwise coprime
- Mod `2^{64}` natural wrap as CRT component (hackcare)

---

## 11. Typical Problem Archetypes

1. Standard application: x ≡ a (mod m), x ≡ b (mod n)
2. Slightly disguised: two calendars / sleep cycles collide
3. Difficult: CRT + counting solutions in a range
4. Very difficult / advanced: CRT in non-coprime towers / Hensel lift

---

## 12. Recognition & Identification Drills

1. Find smallest nonneg x: x≡2 mod 3, x≡3 mod 5, x≡2 mod 7.
2. Impossible system: x≡1 mod 4, x≡2 mod 6 — explain.
3. Compute nCr mod 1e9+9? (composite) — CRT over prime factors.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: multi-modulus residues
- Key invariant: consistency mod gcd
- Key formula: pairwise merge via ExtEuclid
- Complexity: `O(k log)`
- Template to remember: `crt2` then fold

---

---
