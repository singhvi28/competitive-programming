# 4. Polynomial inverse

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** NTT multiply; Newton iteration idea; \(A(0)\) invertible  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: NTT multiply; Newton iteration idea; \(A(0)\) invertible

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

Want \(B\) with \(A\cdot B \equiv 1 \pmod{x^n}\). Newton doubles precision: if \(B\) works mod \(x^m\), then
\[
B' = 2B - A B^2 \pmod{x^{2m}}
\]
is the inverse mod \(x^{2m}\). Start from \(B_0 = A(0)^{-1}\). Every doubling costs a constant number of NTT multiplies → \(O(n\log n)\) total.

---

## 4. Proof Sketches & Recurrences

Newton for \(f(B)=1/B-A=0\): \(B\leftarrow B-(1/B-A)/(-1/B^2)=2B-AB^2\).  
Precision doubles each step: \(1+2+4+\cdots+n = O(n)\) multiply work with NTT → \(O(n\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none beyond NTT
- Per-query / per-operation: \(O(n\log n)\)
- Total: \(O(n\log n)\)
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — poly inv mod x^n using ntt::multiply (mod 998244353). Sketch.
#include <bits/stdc++.h>
using namespace std;
// assumes ntt::MOD, ntt::mod_pow, ntt::multiply from 15-a-poly-multiply-fft-ntt.md

namespace polyinv {
vector<int> inv(vector<int> a, int n) {
    assert(!a.empty() && a[0] != 0);
    a.resize(n);
    vector<int> b(1, ntt::mod_pow(a[0], ntt::MOD - 2));  // B = 1/a0
    for (int m = 1; m < n; m <<= 1) {
        vector<int> aa(a.begin(), a.begin() + min((int)a.size(), 2 * m));
        auto t = ntt::multiply(aa, b);  // A*B
        t.resize(2 * m, 0);
        for (int& x : t) x = x ? ntt::MOD - x : 0;  // -A*B
        t[0] = t[0] + 2 < ntt::MOD ? t[0] + 2 : t[0] + 2 - ntt::MOD;  // 2 - A*B
        b = ntt::multiply(b, t);
        b.resize(2 * m);
    }
    b.resize(n);
    return b;
}
}  // namespace polyinv
```

---

## 6. Recognition Trigger Signals & Heuristics

- Editorial: “invert the generating function”
- Division of polys \(F/G\) as \(F\cdot G^{-1}\) mod \(x^n\)
- Exp/log/sqrt FPS pipelines (inv is the primitive)
- \(A(0)\not\equiv 0\pmod p\) required

---

## 7. Contest WA / TLE / RE Traps

- \(A(0)=0\) (no inverse mod \(x^n\))
- Not doubling length correctly; using full \(n\) multiply every step carelessly (still OK asymptotically if careful resize)
- Wrong update formula (`B - B(AB-1)` vs `2B-AB^2` equivalence mistakes)
- Mod ≠ NTT mod

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

- Series reversion / division as corollaries
- Inverse mod \(x^n\) only (not full polynomial inverse in \(\mathbb{F}_p[x]\))

---

## 11. Typical Problem Archetypes

1. Standard application: compute \(1/A(x)\) mod \(x^n\)
2. Slightly disguised: poly division for GF counting
3. Difficult: inv inside larger FPS expression
4. Very difficult / advanced: multivariable / compositional inverses

---

## 12. Recognition & Identification Drills

1. \(A(0)=1\), degree \(<n\), output \(B\) with \(AB\equiv 1\pmod{x^n}\), mod \(998244353\).
2. Count structures whose EGF is \(1/(1-F(x))\); need series inv/exp combo.
3. Given \(G\), compute \(F\cdot G^{-1}\) mod \(x^n\) under NTT mod.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need reciprocal series mod \(x^n\), \(A(0)\) invertible
- Key invariant: Newton doubles precision
- Key formula: \(B\leftarrow 2B-AB^2\pmod{x^{2m}}\)
- Complexity: \(O(n\log n)\)
- Template to remember: start \(A(0)^{-1}\), double + NTT muls

---

## 5. Polynomial exponentiation

---
