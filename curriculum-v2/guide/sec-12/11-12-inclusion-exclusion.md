# 11. Inclusion-Exclusion

> **Section:** §12 Number Theory & Multiplicative Functions  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** S-tier | **Rating Range:** 1600–2300 | **Frequency:** Common  
> **Prerequisites:** Combinatorics, bitmasks or Möbius for lattices  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2300
- Prerequisites: Combinatorics, bitmasks or Möbius for lattices

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

Overcount unions by adding singles, subtracting doubles, …. In CP: either **bitmask IE** over ≤20 properties, or **divisor Möbius** when properties are “divisible by p”. Don’t force Möbius onto arbitrary sets — use plain IE when properties aren’t a product lattice.

---

## 4. Proof Sketches & Recurrences

\[
\Bigl|\bigcup A_i\Bigr| = \sum |A_i| - \sum |A_i∩A_j| + \cdots + (-1)^{k+1}|∩_1^k A_i|
\]
Complement form often cleaner: total − union.  
Bitmask: for mask≠0, sign = `(-1)^{popcount+1}` for union, or `(-1)^{popcount}` for product IE `∏(1-x_p)`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: optional factorial tables
- Per-query / per-operation: `O(2^k · cost(∩))`
- Total: exponential in property count
- Memory: `O(k)``

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Count objects avoiding a list of bad events
- “At least one / exactly k” constraints
- Coprimality with small prime set
- Surjective functions / onto mappings (`k! · Stirling2` = IE)

---

## 7. Contest WA / TLE / RE Traps

- Wrong sign (`(-1)^{|S|}` vs `|S|+1`)
- LCM overflow / not using gcd when multiplying
- Double-counting unstructured properties that aren’t independent in model
- Using Möbius μ when a plain bitmask IE is enough (overkill bugs)

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

- IE on trees / graphs (chromatic polynomial style)
- Principle for expected value linearity (not IE but related)
- Stirling / onto counts

---

## 11. Typical Problem Archetypes

1. Standard application: multiples of at least one of given primes
2. Slightly disguised: derangements formula
3. Difficult: IE over primes of a modulus + CRT
4. Very difficult / advanced: IE + generating functions

---

## 12. Recognition & Identification Drills

1. Count integers ≤n divisible by 2,3, or 5.
2. Number of onto functions `[n]→[k]`.
3. Count arrays where no position equals a forbidden list (per-index).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: union of structured bad sets
- Key invariant: alternating signs by subset size
- Key formula: classic IE sum
- Complexity: `O(2^k)`
- Template to remember: iterate masks, lcm, sign

---

---
