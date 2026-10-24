# 5. Polynomial exponentiation

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** NTT; poly inv; integration/differentiation of series; usually \(A(0)=0\) for \(\exp A\)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: NTT; poly inv; integration/differentiation of series; usually \(A(0)=0\) for \(\exp A\)

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

For formal series, \(\exp A = \sum A^k/k!\) when it makes sense. Contest computation uses Newton / differential equation:
\[
\exp' = A'\cdot\exp,\quad (\exp A)(0)=1
\]
leading to doubling schemes with **mul + inv + integral**. Do **not** confuse with “fast pow of a single polynomial” via exponentiation-by-squaring of multiply (that is \(O(n\log n\log e)\) for \((P)^e\) truncated — different problem, often enough).

---

## 4. Proof Sketches & Recurrences

Newton for \(B=\exp A\): solve \(\ln B - A = 0\) with \(B\leftarrow B(1-(\ln B-A))\), or integrate \(B\leftarrow B\cdot\int(A'-B'/B)\). Both need `log`/`inv` and NTT. Complexity \(O(n\log n)\).

For \(P^e \bmod x^n\): binary exponentiation with NTT mul → \(O(n\log n\log e)\); if \(P(0)=1\), can use \(\exp(e\cdot\ln P)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(n\log n)\) for FPS exp; \(O(n\log n\log e)\) for binpow
- Total: as above
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — truncated poly power via squaring (most useful "exp" in contests).
// Full fps_exp omitted: niche; implement from library when needed.
namespace polypow {
vector<int> pow_poly(vector<int> base, long long e, int n) {
    vector<int> res(1, 1);
    base.resize(n);
    while (e) {
        if (e & 1) {
            res = ntt::multiply(res, base);
            res.resize(n);
        }
        base = ntt::multiply(base, base);
        base.resize(n);
        e >>= 1;
    }
    return res;
}
}  // namespace polypow
```

---

## 6. Recognition Trigger Signals & Heuristics

- EGF: labeled counting → \(\exp\) of a series
- “Set of components” → \(\exp(C(x))\)
- Editorial mentions `poly_exp` / `fps_exp`
- Contrast: \(P(x)^k \bmod x^n\) with large \(k\) may be **binpow on polys** (squaring), not `exp`

---

## 7. Contest WA / TLE / RE Traps

- Calling \(\exp A\) when \(A(0)\ne 0\)
- Factorials / modular inverses missing in naive EGF
- Using FPS exp when simple poly binpow suffices
- Precision length not truncated to \(n\) after each mul

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

- `log`, `sqrt`, `pow` for FPS (\(A(0)=1\) cases)
- EGF vs OGF exponential formulas

---

## 11. Typical Problem Archetypes

1. Standard application: \(P^k \bmod x^n\) by squaring
2. Slightly disguised: EGF for sets of components \(\exp(C(x))\)
3. Difficult: mix inv/exp/log in one expression
4. Very difficult / advanced: compositional operations

---

## 12. Recognition & Identification Drills

1. Compute \((1+x+x^2)^{10^{18}}\) mod \(x^n\), \(n\le 10^5\), mod \(998244353\).
2. Number of labeled forests via EGF involving \(\exp\).
3. Decide: binpow vs `exp(k log P)` for \(P(0)=1\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: EGF exp, or truncated \(P^e\); confirm \(A(0)\) conditions
- Key invariant: Newton / DE for FPS; squaring for poly power
- Key formula: \(\exp' = A'\exp\); or `res *= base` binpow
- Complexity: \(O(n\log n)\) or \(O(n\log n\log e)\)
- Template to remember: binpow+NTT first; full exp only if needed

---

## 6. Formal power series concepts

---
