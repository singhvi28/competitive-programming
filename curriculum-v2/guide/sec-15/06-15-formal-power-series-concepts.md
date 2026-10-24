# 6. Formal power series concepts

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** Niche | **Rating Range:** 2500–3200 | **Frequency:** Rare  
> **Prerequisites:** Generating functions; NTT toolkit; comfort with truncated series  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2500–3200
- Prerequisites: Generating functions; NTT toolkit; comfort with truncated series

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

An FPS is a sequence \((a_0,a_1,\dots)\) written \(A(x)=\sum a_i x^i\), manipulated **mod \(x^n\)** without caring about convergence. Contest “FPS” means: closed toolbox — mul, inv, exp, log, integral, derivative — to translate combinatorial constructions into coefficient arrays.

---

## 4. Proof Sketches & Recurrences

Algebra: \(\mathbb{F}_p[[x]]/(x^n)\) is the working ring.  
Derivative: \([x^k]A'=(k+1)a_{k+1}\).  
Integral: \([x^k]\int A = a_{k-1}\cdot k^{-1}\) (\(k\ge 1\)).  
Log (for \(A(0)=1\)): \(\int A'/A\). These plus NTT give the toolkit.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: factorial/invfact if EGF
- Per-query / per-operation: \(O(n\log n)\) per heavy op; \(O(n)\) for deriv/integral
- Total: problem-dependent pipeline
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — FPS primitives (derivative / integral). Build inv/exp on top.
namespace fps {
const int MOD = 998244353;
vector<int> derivative(const vector<int>& a) {
    if (a.size() <= 1) return {0};
    vector<int> b(a.size() - 1);
    for (int i = 1; i < (int)a.size(); ++i)
        b[i - 1] = (int)((long long)a[i] * i % MOD);
    return b;
}
vector<int> integral(const vector<int>& a) {
    vector<int> b(a.size() + 1);
    b[0] = 0;
    for (int i = 0; i < (int)a.size(); ++i)
        b[i + 1] = (int)((long long)a[i] * ntt::mod_pow(i + 1, MOD - 2) % MOD);
    return b;
}
}  // namespace fps
```

---

## 6. Recognition Trigger Signals & Heuristics

- Combinatorial species / EGF–OGF translations in editorial
- Need many series ops, not one multiply
- AtCoder library-style `fps` problems
- You already solve the model; implementation is the bottleneck

---

## 7. Contest WA / TLE / RE Traps

- Mixing EGF and OGF factorials
- Applying `log`/`exp` with wrong constant term
- Truncation length bugs between ops
- Treating formal series like real analysis (radius of convergence irrelevant)

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

- Bivariate GF (usually not full FPS code)
- Lazy / online FPS (research-level for contests)

---

## 11. Typical Problem Archetypes

1. Standard application: one inv or exp after GF modeling
2. Slightly disguised: recursive GF \(A=1+xF(A)\) solved by Newton
3. Difficult: long pipeline of ops under tight \(n=10^6\)
4. Very difficult / advanced: compositional inverse, multipoint, chirp-z

---

## 12. Recognition & Identification Drills

1. Translate “sets of directed cycles” into an EGF and list FPS ops needed.
2. \(A=1+xA^2\) — outline Newton lift mod \(x^n\).
3. Given only mul+inv, how do you get `log`?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: combinatorial GF that needs series algebra beyond one product
- Key invariant: work in \(\mathbb{F}_p[[x]]/(x^n)\)
- Key formula: Newton + mul/inv/exp/log/∫/∂
- Complexity: typically \(O(n\log n)\) per heavy op
- Template to remember: NTT mul is the engine; FPS ops are wrappers

---

## 7. When FFT/NTT is actually worth using in contests

---
