# 1. Polynomial multiplication

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Modular arithmetic; arrays; comfort with \(O(n\log n)\) transforms (for the fast path)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Modular arithmetic; arrays; comfort with \(O(n\log n)\) transforms (for the fast path)

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

## 3. Core Intuition & Problem Framing

Multiplying \(A(x)=\sum a_i x^i\) and \(B(x)=\sum b_j x^j\) is exactly computing the **convolution**
\[
c_k=\sum_{i+j=k}a_i b_j.
\]
Almost every “FFT problem” is: *encode two (or more) sequences so the answer is some \(c_k\)*. The algorithm (naive / FFT / NTT) is secondary to this encoding.

---

## 4. Proof Sketches & Recurrences

Naive: for each \(i,j\), add \(a_i b_j\) into \(c_{i+j}\) → \(O(n^2)\).

Fast: evaluate \(A,B\) at \(n\) roots of unity (DFT), pointwise multiply, inverse DFT → \(O(n\log n)\) with \(n\ge \deg A+\deg B+1\), \(n\) power of two.

Padding: zero-pad to length \(2^{\lceil\log_2(\deg A+\deg B+1)\rceil}\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (naive); \(O(n)\) twiddle setup once (FFT/NTT)
- Per-query / per-operation: \(O(nm)\) naive; \(O(N\log N)\) FFT/NTT with \(N\ge n+m-1\)
- Total: as above for one product
- Memory: \(O(n+m)\) or \(O(N)\)`

### C++17 Template

```cpp
// C++17 — naive multiply (mod optional). Use when n*m is small.
#include <bits/stdc++.h>
using namespace std;

namespace polymul {
vector<long long> mul_naive(const vector<long long>& a,
                            const vector<long long>& b,
                            long long mod = 0) {
    if (a.empty() || b.empty()) return {};
    vector<long long> c(a.size() + b.size() - 1);
    for (size_t i = 0; i < a.size(); ++i)
        for (size_t j = 0; j < b.size(); ++j) {
            __int128 v = (__int128)a[i] * b[j] + c[i + j];
            c[i + j] = mod ? (long long)(v % mod) : (long long)v;
        }
    return c;
}
}  // namespace polymul
```

### Python 3 Template

```python
# Fine for n <= ~2000 or offline checks; not for tight NTT TLs.
def mul_naive(a: list[int], b: list[int], mod: int | None = None) -> list[int]:
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            s = c[i + j] + x * y
            c[i + j] = s % mod if mod else s
    return c
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Number of ways to choose one from A and one from B with sum/difference \(k\)”
- Generating functions \(A(x)B(x)\) in the statement or editorial
- DP transition \(dp'[k] += dp[k-i]\cdot w[i]\) for all \(k\) at once (batch convolution)
- Product of many small polys (binary-split multiply)
- Online/offline “combine histograms”

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to pad to next power of two / length \(\ge n+m-1\)
- Using NTT mod that does not divide \(N\)’s order (need \(2^e \mid p-1\), \(2^e\ge N\))
- Overflow before mod (`long long` / `__int128`)
- Off-by-one on degrees; trimming trailing zeros incorrectly when high coeffs matter
- Multiplying under wrong modulus (problem mod ≠ NTT mod → CRT or other plan)

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Many polys:** binary tree / divide-and-conquer multiply
- **Online convolution:** CDQ / “online FFT” (advanced)
- **Circular convolution:** length \(n\) without enough padding (usually wrong for poly product)
- **XOR/OR/AND convolution:** FWT, not this section’s DFT

---

## 11. Typical Problem Archetypes

1. Standard application: ways to get each sum with one element from each array
2. Slightly disguised: count pairs with \(a_i+b_j\) in a set; histogram multiply
3. Difficult: product of \(n\) polys with total degree bound; optimize order
4. Very difficult / advanced: online convolutions, multipoint eval (beyond basic multiply)

---

## 12. Recognition & Identification Drills

1. Arrays \(A,B\) of size \(n\le 2\cdot10^5\). For each \(k\), count pairs \(i,j\) with \(a_i+b_j=k\). Mod \(998244353\).
2. You have DP values \(f[0..n]\) and weights \(w[0..m]\). Need \(g[k]=\sum_i f[i]w[k-i]\) for all \(k\). Constraints force \(O(n\log n)\).
3. Compute coefficient of \(x^k\) in \(\prod_{i=1}^n (1+x^{a_i})\) for many queries \(k\); \(n,k\) large.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: answer is a convolution of two coefficient arrays
- Key invariant: \(c = a * b\) iff evaluation product on roots of unity
- Key formula: \(c_k=\sum_{i+j=k}a_i b_j\)
- Complexity: \(O(n^2)\) or \(O(n\log n)\)
- Template to remember: pad → DFT → pointwise mul → IDFT (NTT in practice)

---

## 2. FFT

---
