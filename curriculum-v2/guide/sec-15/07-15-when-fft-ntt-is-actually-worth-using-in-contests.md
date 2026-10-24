# When FFT/NTT is actually worth using in contests

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Knowing naive multiply *and* NTT exist; modeling convolutions  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Knowing naive multiply *and* NTT exist; modeling convolutions

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

FFT/NTT is **not** a default hammer. It wins when (1) the answer is genuinely a **convolution** (or few of them), (2) size makes \(O(n^2)\) impossible, (3) modulus/precision cooperates. Mis-modeling (using DFT for XOR convolution, or NTT under \(10^9+7\) without a plan) costs more time than a correct \(O(n^2)\) or FFT-free math solution.

---

## 4. Proof Sketches & Recurrences

Rough break-even (implementation-dependent): naive \(\approx n^2\) ops vs NTT \(\approx 3c\,N\log N\) with \(N\approx 2n\). For \(n\approx 2000\), often similar; for \(n\approx 10^5\), NTT mandatory if convolution is required. Constants in C++ NTT are excellent; in Python they are not (see wrapper).

Decision tree:
1. Is \(c_k=\sum_{i+j=k} a_i b_j\) (or cyclic variant) the bottleneck? If no → stop.
2. Constraints small? → naive.
3. Mod NTT-friendly? → NTT.
4. No mod / small coeffs? → FFT + round.
5. Hostile mod + large \(n\) → CRT NTT / MTT / rethink.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: modeling time (human)
- Per-query / per-operation: \(O(n^2)\) vs \(O(n\log n)\) choice
- Total: prefer asymptotically + constant that fits TL
- Memory: NTT needs \(O(N)\) with \(N\) next power of two`

### C++17 Template

```cpp
// C++17 — contest decision helper (comments as checklist, not runtime).
namespace fft_roi {
// Use NTT multiply when ALL hold:
//  (1) modeling is convolution
//  (2) n large enough that n*n TLE
//  (3) MOD is 998244353 (or other NTT prime) OR you CRT
// Else: polymul::mul_naive or non-poly approach.
bool prefer_ntt(int n, int mod) {
    if (n < 2000) return false;           // heuristic
    if (mod == 998244353) return true;
    return false;                         // need CRT/MTT plan
}
}  // namespace fft_roi
```

---

## 6. Recognition Trigger Signals & Heuristics

- **Worth reaching for NTT/FFT:**
- Explicit product of generating functions / histograms
- \(n\ge\sim 2\)–\(4\cdot 10^3\) and \(O(n^2)\) TLE; mod \(998244353\)
- Batching a DP transition that is a convolution
- **Prefer something else:**
- \(n\le 1000\) → naive
- Mod \(10^9+7\) and you lack CRT/MTT — seek combinatorial closed form / other DP
- Subset XOR / OR / AND → FWT/SOS, not NTT
- String matching → KMP/Z/hash/Aho unless convolution matching is intended
- One coefficient only → maybe roots-of-unity filter + interpolation, or smarter math

---

## 7. Contest WA / TLE / RE Traps

- Spending 45 minutes on NTT when \(n=500\) naive works
- Ignoring that problem mod ≠ \(998244353\)
- Applying NTT to non-convolution DP
- Float FFT without bounding coefficients
- Multiple NTTs in \(T\) tests without summing sizes (TLE)

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

- **Online FFT** for DP prefix convolutions
- **CRT** path for \(10^9+7\)
- **Skip FFT**: closed form, stirling, combinatorial identities

---

## 11. Typical Problem Archetypes

1. Standard application: large histogram convolution, mod \(998244353\)
2. Slightly disguised: DP transition rewritten as poly product
3. Difficult: hostile mod forcing CRT or alternative
4. Very difficult / advanced: online / multipoint / FPS — only after multiply ROI is clear

---

## 12. Recognition & Identification Drills

1. \(n=800\), mod \(10^9+7\), need all \(c_k=\sum a_i b_{k-i}\). Tool?
2. \(n=2\cdot10^5\), mod \(998244353\), same. Tool?
3. \(n=2\cdot10^5\), need subset-XOR convolution. Tool?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: large true convolution + friendly mod/precision
- Key invariant: “Is it \(\sum_{i+j=k}\)?” before any transform
- Key formula: break-even ~ few thousand for naive vs NTT
- Complexity: choose \(O(n^2)\) vs \(O(n\log n)\) deliberately
- Template to remember: checklist → naive / NTT / FFT / FWT / give up to math

---

Back to [Section 15 wrapper](15-fft-polynomials.md).

---

---
