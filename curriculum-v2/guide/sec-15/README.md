# Section §15: FFT, NTT & Formal Power Series

> **Module ID:** `sec-15`  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Topic Count:** 8  

**Module Summary:** Fast Fourier Transform, Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series operations.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Polynomial multiplication](#topic-1) | `A-tier` | 2000–2600 | Occasional | [01-15-polynomial-multiplication.md](./01-15-polynomial-multiplication.md) |
| 2 | [FFT](#topic-2) | `B-tier` | 2100–2700 | Occasional | [02-15-fft.md](./02-15-fft.md) |
| 3 | [NTT](#topic-3) | `B-tier (A-tier *as the practical contest FFT*)` | 2100–2700 | Occasional | [03-15-ntt.md](./03-15-ntt.md) |
| 4 | [Polynomial inverse](#topic-4) | `C-tier` | 2400–3000 | Rare | [04-15-polynomial-inverse.md](./04-15-polynomial-inverse.md) |
| 5 | [Polynomial exponentiation](#topic-5) | `C-tier` | 2400–3000 | Rare | [05-15-polynomial-exponentiation.md](./05-15-polynomial-exponentiation.md) |
| 6 | [Formal power series concepts](#topic-6) | `Niche` | 2500–3200 | Rare | [06-15-formal-power-series-concepts.md](./06-15-formal-power-series-concepts.md) |
| 7 | [When FFT/NTT is actually worth using in contests](#topic-7) | `A-tier` | 2000–2700 | Occasional | [07-15-when-fft-ntt-is-actually-worth-using-in-contests.md](./07-15-when-fft-ntt-is-actually-worth-using-in-contests.md) |
| 8 | [Divide and Conquer FFT (Semi-Online Convolution)](#topic-8) | `B-tier` | 2400+ | Rare | [08-15-divide-and-conquer-fft-semi-online-convolution.md](./08-15-divide-and-conquer-fft-semi-online-convolution.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Polynomial multiplication

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Modular arithmetic; arrays; comfort with \(O(n\log n)\) transforms (for the fast path)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Modular arithmetic; arrays; comfort with \(O(n\log n)\) transforms (for the fast path)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

Multiplying \(A(x)=\sum a_i x^i\) and \(B(x)=\sum b_j x^j\) is exactly computing the **convolution**
\[
c_k=\sum_{i+j=k}a_i b_j.
\]
Almost every “FFT problem” is: *encode two (or more) sequences so the answer is some \(c_k\)*. The algorithm (naive / FFT / NTT) is secondary to this encoding.

---

#### 4. Proof Sketches & Recurrences

Naive: for each \(i,j\), add \(a_i b_j\) into \(c_{i+j}\) → \(O(n^2)\).

Fast: evaluate \(A,B\) at \(n\) roots of unity (DFT), pointwise multiply, inverse DFT → \(O(n\log n)\) with \(n\ge \deg A+\deg B+1\), \(n\) power of two.

Padding: zero-pad to length \(2^{\lceil\log_2(\deg A+\deg B+1)\rceil}\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none (naive); \(O(n)\) twiddle setup once (FFT/NTT)
- Per-query / per-operation: \(O(nm)\) naive; \(O(N\log N)\) FFT/NTT with \(N\ge n+m-1\)
- Total: as above for one product
- Memory: \(O(n+m)\) or \(O(N)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Number of ways to choose one from A and one from B with sum/difference \(k\)”
- Generating functions \(A(x)B(x)\) in the statement or editorial
- DP transition \(dp'[k] += dp[k-i]\cdot w[i]\) for all \(k\) at once (batch convolution)
- Product of many small polys (binary-split multiply)
- Online/offline “combine histograms”

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to pad to next power of two / length \(\ge n+m-1\)
- Using NTT mod that does not divide \(N\)’s order (need \(2^e \mid p-1\), \(2^e\ge N\))
- Overflow before mod (`long long` / `__int128`)
- Off-by-one on degrees; trimming trailing zeros incorrectly when high coeffs matter
- Multiplying under wrong modulus (problem mod ≠ NTT mod → CRT or other plan)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Many polys:** binary tree / divide-and-conquer multiply
- **Online convolution:** CDQ / “online FFT” (advanced)
- **Circular convolution:** length \(n\) without enough padding (usually wrong for poly product)
- **XOR/OR/AND convolution:** FWT, not this section’s DFT

---

#### 11. Typical Problem Archetypes

1. Standard application: ways to get each sum with one element from each array
2. Slightly disguised: count pairs with \(a_i+b_j\) in a set; histogram multiply
3. Difficult: product of \(n\) polys with total degree bound; optimize order
4. Very difficult / advanced: online convolutions, multipoint eval (beyond basic multiply)

---

#### 12. Recognition & Identification Drills

1. Arrays \(A,B\) of size \(n\le 2\cdot10^5\). For each \(k\), count pairs \(i,j\) with \(a_i+b_j=k\). Mod \(998244353\).
2. You have DP values \(f[0..n]\) and weights \(w[0..m]\). Need \(g[k]=\sum_i f[i]w[k-i]\) for all \(k\). Constraints force \(O(n\log n)\).
3. Compute coefficient of \(x^k\) in \(\prod_{i=1}^n (1+x^{a_i})\) for many queries \(k\); \(n,k\) large.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: answer is a convolution of two coefficient arrays
- Key invariant: \(c = a * b\) iff evaluation product on roots of unity
- Key formula: \(c_k=\sum_{i+j=k}a_i b_j\)
- Complexity: \(O(n^2)\) or \(O(n\log n)\)
- Template to remember: pad → DFT → pointwise mul → IDFT (NTT in practice)

---

## 2. FFT

---


---

<a id="topic-2"></a>
### 2. FFT

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Complex numbers; roots of unity; poly multiplication modeling  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Complex numbers; roots of unity; poly multiplication modeling

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

DFT turns convolution into pointwise product. FFT computes DFT in \(O(n\log n)\) by recursively splitting even/odd indices (Cooley–Tukey). In contests you almost always want the **iterative bit-reversal** form. Complex FFT answers are **approximate** — round to nearest integer when coeffs are known integral and not too large.

---

#### 4. Proof Sketches & Recurrences

Primitive \(n\)-th root \(\omega = e^{2\pi i/n}\).  
\[
\hat a_k=\sum_{j=0}^{n-1}a_j\omega^{jk},\quad
a_j=\frac1n\sum_{k=0}^{n-1}\hat a_k\omega^{-jk}.
\]
Butterfly: \(n\) length-\(n/2\) DFTs + \(O(n)\) combines → \(T(n)=2T(n/2)+O(n)=O(n\log n)\).

Precision: error grows with \(n\) and magnitude; if \(|c_k|\) large, prefer NTT+CRT.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) or \(O(n)\) if caching angles
- Per-query / per-operation: \(O(n\log n)\) per transform; multiply ≈ 3 FFTs
- Total: \(O(n\log n)\)
- Memory: \(O(n)\) complex doubles`

##### C++17 Template

```cpp
// C++17 iterative FFT (complex). Round carefully.
#include <bits/stdc++.h>
using namespace std;

namespace fft {
using cd = complex<double>;
const double PI = acos(-1.0);

void fft(vector<cd>& a, bool invert) {
    int n = (int)a.size();
    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; ++j) {
                cd u = a[i + j], v = a[i + j + len / 2] * w;
                a[i + j] = u + v;
                a[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert) for (cd& x : a) x /= n;
}

vector<long long> multiply(const vector<long long>& a,
                           const vector<long long>& b) {
    vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < (int)a.size() + (int)b.size()) n <<= 1;
    fa.resize(n); fb.resize(n);
    fft(fa, false); fft(fb, false);
    for (int i = 0; i < n; ++i) fa[i] *= fb[i];
    fft(fa, true);
    vector<long long> c(n);
    for (int i = 0; i < n; ++i) c[i] = llround(fa[i].real());
    return c;
}
}  // namespace fft
```

##### Python 3 Template

```python
# OK for learning / small n; slow + precision for contest n~1e6.
import cmath

def fft(a: list[complex], invert: bool = False) -> None:
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = 2 * cmath.pi / length * (-1 if invert else 1)
        wlen = cmath.exp(complex(0, ang))
        for i in range(0, n, length):
            w = 1 + 0j
            half = length // 2
            for j in range(half):
                u, v = a[i + j], a[i + j + half] * w
                a[i + j], a[i + j + half] = u + v, u - v
                w *= wlen
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n

def multiply(a: list[int], b: list[int]) -> list[int]:
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = [complex(x) for x in a] + [0j] * (n - len(a))
    fb = [complex(x) for x in b] + [0j] * (n - len(b))
    fft(fa); fft(fb)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, invert=True)
    return [int(round(fa[i].real)) for i in range(n)]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Product needed **without** modular arithmetic, coeffs \(\lesssim 10^{15}\) after careful bounds (or smaller)
- Editorial says “FFT” and mod is not NTT-friendly
- Geometry/trig generating tricks (rare)
- You already know NTT but mod is \(10^9+7\) and you consider FFT+rounding or CRT

---

#### 7. Contest WA / TLE / RE Traps

- Not using `llround` / wrong rounding → off-by-one coeffs
- Coefficients too large → float noise exceeds \(0.5\)
- Forgetting `a[i] /= n` on inverse
- Using FFT when answer needs mod \(p\) with large intermediate coeffs
- `PI` / `acos(-1)` inconsistencies; prefer `acos(-1.0)`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Real FFT / packing** two reals into one complex (constant-factor)
- **MTT** (mod \(10^9+7\) via FFT split) — precision-sensitive, situational
- Prefer **NTT** whenever modulus is \(998244353\) or another NTT prime

---

#### 11. Typical Problem Archetypes

1. Standard application: integer convolution, no mod, moderate size
2. Slightly disguised: count geometric pairs via polynomial encoding
3. Difficult: high dynamic range coeffs (need split FFT / CRT)
4. Very difficult / advanced: MTT for \(10^9+7\) under tight precision

---

#### 12. Recognition & Identification Drills

1. Multiply two integer polys degree \(n=10^5\), coeffs \(\le 100\), output exact coeffs (no mod).
2. Same but output coeffs mod \(10^9+7\) — decide FFT vs NTT+CRT vs MTT.
3. Statement mentions roots of unity filter + coefficient extraction without a friendly NTT mod.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: convolution with floats OK or small integer coeffs
- Key invariant: DFT diagonalizes cyclic convolution
- Key formula: \(\widehat{a*b}=\hat a\cdot\hat b\) (pointwise)
- Complexity: \(O(n\log n)\)
- Template to remember: bit-reverse + butterflies + `llround`

---

## 3. NTT

---


---

<a id="topic-3"></a>
### 3. NTT

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier (A-tier *as the practical contest FFT*) | **Rating Range:** 2100–2700 | **Frequency:** Occasional  
> **Prerequisites:** Modular mul/pow; primitive roots; poly multiply modeling  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier (A-tier *as the practical contest FFT*)
- Frequency: Occasional
- Typical CF/ICPC rating range: 2100–2700
- Prerequisites: Modular mul/pow; primitive roots; poly multiply modeling

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

NTT is FFT over \(\mathbb{Z}/p\mathbb{Z}\): replace \(\omega=e^{2\pi i/n}\) by a modular **primitive \(n\)-th root of unity**. Standard CF mod **\(998244353=119\cdot2^{23}+1\)** supports lengths up to \(2^{23}\). This is the **default contest tool** for exact modular convolution.

---

#### 4. Proof Sketches & Recurrences

Need prime \(p\) and \(n\mid(p-1)\), \(n=2^e\). Let \(g\) be primitive root mod \(p\); set \(\omega = g^{(p-1)/n}\). Same butterflies as FFT; inverse uses \(\omega^{-1}\) and multiply by \(n^{-1}\).

Common: `mod = 998244353`, `g = 3`, `omega = modpow(3, (mod-1)/n)`.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) (or pretabulate roots \(O(n)\))
- Per-query / per-operation: \(O(n\log n)\) per NTT; multiply ≈ \(3\) NTTs
- Total: \(O(n\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
// C++17 NTT multiply — contest workhorse (mod 998244353).
#include <bits/stdc++.h>
using namespace std;

namespace ntt {
const int MOD = 998244353;
const int G = 3;  // primitive root

int mod_pow(long long a, long long e) {
    long long r = 1;
    for (; e; e >>= 1, a = a * a % MOD)
        if (e & 1) r = r * a % MOD;
    return (int)r;
}

void ntt(vector<int>& a, bool invert) {
    int n = (int)a.size();
    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        int wlen = mod_pow(G, (MOD - 1) / len);
        if (invert) wlen = mod_pow(wlen, MOD - 2);
        for (int i = 0; i < n; i += len) {
            int w = 1;
            for (int j = 0; j < len / 2; ++j) {
                int u = a[i + j], v = (int)((long long)a[i + j + len / 2] * w % MOD);
                a[i + j] = u + v < MOD ? u + v : u + v - MOD;
                a[i + j + len / 2] = u - v >= 0 ? u - v : u - v + MOD;
                w = (int)((long long)w * wlen % MOD);
            }
        }
    }
    if (invert) {
        int n_inv = mod_pow(n, MOD - 2);
        for (int& x : a) x = (int)((long long)x * n_inv % MOD);
    }
}

vector<int> multiply(vector<int> a, vector<int> b) {
    if (a.empty() || b.empty()) return {};
    int need = (int)a.size() + (int)b.size() - 1;
    int n = 1;
    while (n < need) n <<= 1;
    a.resize(n); b.resize(n);
    ntt(a, false); ntt(b, false);
    for (int i = 0; i < n; ++i) a[i] = (int)((long long)a[i] * b[i] % MOD);
    ntt(a, true);
    a.resize(need);
    return a;
}
}  // namespace ntt
```

##### Python 3 Template

```python
MOD, G = 998244353, 3

def mod_pow(a: int, e: int) -> int:
    r = 1
    while e:
        if e & 1:
            r = r * a % MOD
        a = a * a % MOD
        e >>= 1
    return r

# Full NTT omitted on purpose for contests — port the C++17 template.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Mod is \(998244353\) (or \(985661441\), \(1012924417\), …) and you need convolution
- Generating function product / partition-style DP batched by convolution
- “Multiply polynomials mod \(p\)” in statement
- Multiple testcases still OK if total \(N\log N\) fits

---

#### 7. Contest WA / TLE / RE Traps

- Wrong primitive root / wrong mod
- Length \(n\) not dividing \(p-1\) (e.g. need \(>2^{23}\) on 998244353 — impossible)
- Forgot modular inverse of \(n\) on inverse transform
- Negative residues not normalized before output
- Using NTT for mod \(10^9+7\) without CRT/MTT plan
- Resizing to `need` vs leaving padded zeros inconsistently across tests

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Other NTT mods:** \(985661441\), \(754974721\), … for CRT
- **CRT NTT:** three mods → reconstruct large integer / mod \(10^9+7\)
- **In-place recursive** vs iterative (prefer iterative)
- **NTT any modulus** frameworks — heavier, rare in ICPs

---

#### 11. Typical Problem Archetypes

1. Standard application: poly product mod \(998244353\)
2. Slightly disguised: count sequences with sum constraints via GF product
3. Difficult: many multiplies / divide-conquer FFT DP
4. Very difficult / advanced: inv/exp/log pipelines (→ §4–6)

---

#### 12. Recognition & Identification Drills

1. Given \(A(x),B(x)\) degree \(<n\), \(n=2\cdot10^5\), print \(A\cdot B\) mod \(998244353\).
2. \(f(k)=\) number of ways to write \(k\) as \(a_i+b_j\) mod \(998244353\); \(n=m=2\cdot10^5\).
3. Mod is \(10^9+7\), \(n=10^5\) convolution — outline CRT with two/three NTT mods.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: modular convolution; especially mod \(998244353\)
- Key invariant: same butterflies as FFT, modular \(\omega\)
- Key formula: \(\omega = g^{(p-1)/n}\), inverse \(\times n^{-1}\)
- Complexity: \(O(n\log n)\)
- Template to remember: iterative NTT + pointwise mul + inv NTT (C++17)

---

Continue: [15-b-inverse-exp-fps.md](15-b-inverse-exp-fps.md) (inverse, exp, FPS, when worth it).

---


---

<a id="topic-4"></a>
### 4. Polynomial inverse

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** NTT multiply; Newton iteration idea; \(A(0)\) invertible  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: NTT multiply; Newton iteration idea; \(A(0)\) invertible

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

Want \(B\) with \(A\cdot B \equiv 1 \pmod{x^n}\). Newton doubles precision: if \(B\) works mod \(x^m\), then
\[
B' = 2B - A B^2 \pmod{x^{2m}}
\]
is the inverse mod \(x^{2m}\). Start from \(B_0 = A(0)^{-1}\). Every doubling costs a constant number of NTT multiplies → \(O(n\log n)\) total.

---

#### 4. Proof Sketches & Recurrences

Newton for \(f(B)=1/B-A=0\): \(B\leftarrow B-(1/B-A)/(-1/B^2)=2B-AB^2\).  
Precision doubles each step: \(1+2+4+\cdots+n = O(n)\) multiply work with NTT → \(O(n\log n)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: none beyond NTT
- Per-query / per-operation: \(O(n\log n)\)
- Total: \(O(n\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Editorial: “invert the generating function”
- Division of polys \(F/G\) as \(F\cdot G^{-1}\) mod \(x^n\)
- Exp/log/sqrt FPS pipelines (inv is the primitive)
- \(A(0)\not\equiv 0\pmod p\) required

---

#### 7. Contest WA / TLE / RE Traps

- \(A(0)=0\) (no inverse mod \(x^n\))
- Not doubling length correctly; using full \(n\) multiply every step carelessly (still OK asymptotically if careful resize)
- Wrong update formula (`B - B(AB-1)` vs `2B-AB^2` equivalence mistakes)
- Mod ≠ NTT mod

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Series reversion / division as corollaries
- Inverse mod \(x^n\) only (not full polynomial inverse in \(\mathbb{F}_p[x]\))

---

#### 11. Typical Problem Archetypes

1. Standard application: compute \(1/A(x)\) mod \(x^n\)
2. Slightly disguised: poly division for GF counting
3. Difficult: inv inside larger FPS expression
4. Very difficult / advanced: multivariable / compositional inverses

---

#### 12. Recognition & Identification Drills

1. \(A(0)=1\), degree \(<n\), output \(B\) with \(AB\equiv 1\pmod{x^n}\), mod \(998244353\).
2. Count structures whose EGF is \(1/(1-F(x))\); need series inv/exp combo.
3. Given \(G\), compute \(F\cdot G^{-1}\) mod \(x^n\) under NTT mod.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need reciprocal series mod \(x^n\), \(A(0)\) invertible
- Key invariant: Newton doubles precision
- Key formula: \(B\leftarrow 2B-AB^2\pmod{x^{2m}}\)
- Complexity: \(O(n\log n)\)
- Template to remember: start \(A(0)^{-1}\), double + NTT muls

---

## 5. Polynomial exponentiation

---


---

<a id="topic-5"></a>
### 5. Polynomial exponentiation

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 2400–3000 | **Frequency:** Rare  
> **Prerequisites:** NTT; poly inv; integration/differentiation of series; usually \(A(0)=0\) for \(\exp A\)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: NTT; poly inv; integration/differentiation of series; usually \(A(0)=0\) for \(\exp A\)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

For formal series, \(\exp A = \sum A^k/k!\) when it makes sense. Contest computation uses Newton / differential equation:
\[
\exp' = A'\cdot\exp,\quad (\exp A)(0)=1
\]
leading to doubling schemes with **mul + inv + integral**. Do **not** confuse with “fast pow of a single polynomial” via exponentiation-by-squaring of multiply (that is \(O(n\log n\log e)\) for \((P)^e\) truncated — different problem, often enough).

---

#### 4. Proof Sketches & Recurrences

Newton for \(B=\exp A\): solve \(\ln B - A = 0\) with \(B\leftarrow B(1-(\ln B-A))\), or integrate \(B\leftarrow B\cdot\int(A'-B'/B)\). Both need `log`/`inv` and NTT. Complexity \(O(n\log n)\).

For \(P^e \bmod x^n\): binary exponentiation with NTT mul → \(O(n\log n\log e)\); if \(P(0)=1\), can use \(\exp(e\cdot\ln P)\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(n\log n)\) for FPS exp; \(O(n\log n\log e)\) for binpow
- Total: as above
- Memory: \(O(n)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- EGF: labeled counting → \(\exp\) of a series
- “Set of components” → \(\exp(C(x))\)
- Editorial mentions `poly_exp` / `fps_exp`
- Contrast: \(P(x)^k \bmod x^n\) with large \(k\) may be **binpow on polys** (squaring), not `exp`

---

#### 7. Contest WA / TLE / RE Traps

- Calling \(\exp A\) when \(A(0)\ne 0\)
- Factorials / modular inverses missing in naive EGF
- Using FPS exp when simple poly binpow suffices
- Precision length not truncated to \(n\) after each mul

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- `log`, `sqrt`, `pow` for FPS (\(A(0)=1\) cases)
- EGF vs OGF exponential formulas

---

#### 11. Typical Problem Archetypes

1. Standard application: \(P^k \bmod x^n\) by squaring
2. Slightly disguised: EGF for sets of components \(\exp(C(x))\)
3. Difficult: mix inv/exp/log in one expression
4. Very difficult / advanced: compositional operations

---

#### 12. Recognition & Identification Drills

1. Compute \((1+x+x^2)^{10^{18}}\) mod \(x^n\), \(n\le 10^5\), mod \(998244353\).
2. Number of labeled forests via EGF involving \(\exp\).
3. Decide: binpow vs `exp(k log P)` for \(P(0)=1\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: EGF exp, or truncated \(P^e\); confirm \(A(0)\) conditions
- Key invariant: Newton / DE for FPS; squaring for poly power
- Key formula: \(\exp' = A'\exp\); or `res *= base` binpow
- Complexity: \(O(n\log n)\) or \(O(n\log n\log e)\)
- Template to remember: binpow+NTT first; full exp only if needed

---

## 6. Formal power series concepts

---


---

<a id="topic-6"></a>
### 6. Formal power series concepts

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** Niche | **Rating Range:** 2500–3200 | **Frequency:** Rare  
> **Prerequisites:** Generating functions; NTT toolkit; comfort with truncated series  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2500–3200
- Prerequisites: Generating functions; NTT toolkit; comfort with truncated series

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

An FPS is a sequence \((a_0,a_1,\dots)\) written \(A(x)=\sum a_i x^i\), manipulated **mod \(x^n\)** without caring about convergence. Contest “FPS” means: closed toolbox — mul, inv, exp, log, integral, derivative — to translate combinatorial constructions into coefficient arrays.

---

#### 4. Proof Sketches & Recurrences

Algebra: \(\mathbb{F}_p[[x]]/(x^n)\) is the working ring.  
Derivative: \([x^k]A'=(k+1)a_{k+1}\).  
Integral: \([x^k]\int A = a_{k-1}\cdot k^{-1}\) (\(k\ge 1\)).  
Log (for \(A(0)=1\)): \(\int A'/A\). These plus NTT give the toolkit.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: factorial/invfact if EGF
- Per-query / per-operation: \(O(n\log n)\) per heavy op; \(O(n)\) for deriv/integral
- Total: problem-dependent pipeline
- Memory: \(O(n)\)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Combinatorial species / EGF–OGF translations in editorial
- Need many series ops, not one multiply
- AtCoder library-style `fps` problems
- You already solve the model; implementation is the bottleneck

---

#### 7. Contest WA / TLE / RE Traps

- Mixing EGF and OGF factorials
- Applying `log`/`exp` with wrong constant term
- Truncation length bugs between ops
- Treating formal series like real analysis (radius of convergence irrelevant)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Bivariate GF (usually not full FPS code)
- Lazy / online FPS (research-level for contests)

---

#### 11. Typical Problem Archetypes

1. Standard application: one inv or exp after GF modeling
2. Slightly disguised: recursive GF \(A=1+xF(A)\) solved by Newton
3. Difficult: long pipeline of ops under tight \(n=10^6\)
4. Very difficult / advanced: compositional inverse, multipoint, chirp-z

---

#### 12. Recognition & Identification Drills

1. Translate “sets of directed cycles” into an EGF and list FPS ops needed.
2. \(A=1+xA^2\) — outline Newton lift mod \(x^n\).
3. Given only mul+inv, how do you get `log`?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: combinatorial GF that needs series algebra beyond one product
- Key invariant: work in \(\mathbb{F}_p[[x]]/(x^n)\)
- Key formula: Newton + mul/inv/exp/log/∫/∂
- Complexity: typically \(O(n\log n)\) per heavy op
- Template to remember: NTT mul is the engine; FPS ops are wrappers

---

## 7. When FFT/NTT is actually worth using in contests

---


---

<a id="topic-7"></a>
### 7. When FFT/NTT is actually worth using in contests

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Knowing naive multiply *and* NTT exist; modeling convolutions  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Knowing naive multiply *and* NTT exist; modeling convolutions

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

FFT/NTT is **not** a default hammer. It wins when (1) the answer is genuinely a **convolution** (or few of them), (2) size makes \(O(n^2)\) impossible, (3) modulus/precision cooperates. Mis-modeling (using DFT for XOR convolution, or NTT under \(10^9+7\) without a plan) costs more time than a correct \(O(n^2)\) or FFT-free math solution.

---

#### 4. Proof Sketches & Recurrences

Rough break-even (implementation-dependent): naive \(\approx n^2\) ops vs NTT \(\approx 3c\,N\log N\) with \(N\approx 2n\). For \(n\approx 2000\), often similar; for \(n\approx 10^5\), NTT mandatory if convolution is required. Constants in C++ NTT are excellent; in Python they are not (see wrapper).

Decision tree:
1. Is \(c_k=\sum_{i+j=k} a_i b_j\) (or cyclic variant) the bottleneck? If no → stop.
2. Constraints small? → naive.
3. Mod NTT-friendly? → NTT.
4. No mod / small coeffs? → FFT + round.
5. Hostile mod + large \(n\) → CRT NTT / MTT / rethink.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: modeling time (human)
- Per-query / per-operation: \(O(n^2)\) vs \(O(n\log n)\) choice
- Total: prefer asymptotically + constant that fits TL
- Memory: NTT needs \(O(N)\) with \(N\) next power of two`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

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

#### 7. Contest WA / TLE / RE Traps

- Spending 45 minutes on NTT when \(n=500\) naive works
- Ignoring that problem mod ≠ \(998244353\)
- Applying NTT to non-convolution DP
- Float FFT without bounding coefficients
- Multiple NTTs in \(T\) tests without summing sizes (TLE)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Online FFT** for DP prefix convolutions
- **CRT** path for \(10^9+7\)
- **Skip FFT**: closed form, stirling, combinatorial identities

---

#### 11. Typical Problem Archetypes

1. Standard application: large histogram convolution, mod \(998244353\)
2. Slightly disguised: DP transition rewritten as poly product
3. Difficult: hostile mod forcing CRT or alternative
4. Very difficult / advanced: online / multipoint / FPS — only after multiply ROI is clear

---

#### 12. Recognition & Identification Drills

1. \(n=800\), mod \(10^9+7\), need all \(c_k=\sum a_i b_{k-i}\). Tool?
2. \(n=2\cdot10^5\), mod \(998244353\), same. Tool?
3. \(n=2\cdot10^5\), need subset-XOR convolution. Tool?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: large true convolution + friendly mod/precision
- Key invariant: “Is it \(\sum_{i+j=k}\)?” before any transform
- Key formula: break-even ~ few thousand for naive vs NTT
- Complexity: choose \(O(n^2)\) vs \(O(n\log n)\) deliberately
- Template to remember: checklist → naive / NTT / FFT / FWT / give up to math

---

Back to [Section 15 wrapper](15-fft-polynomials.md).

---

---


---

<a id="topic-8"></a>
### 8. Divide and Conquer FFT (Semi-Online Convolution)

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2400+ | **Frequency:** Rare  
> **Prerequisites:** FFT/NTT, Divide and Conquer  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400+
- Prerequisites: FFT/NTT, Divide and Conquer

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Polynomial Algorithms utilize discrete transforms to compute fast convolutions and power series operations: Fast Fourier Transform (FFT), Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series (FPS).

##### Fundamental Theorems & Invariants

- **Cooley-Tukey FFT Theorem:** By recursively decomposing a polynomial $P(x) = P_{even}(x^2) + x \cdot P_{odd}(x^2)$ using complex roots of unity $\omega_n^k = e^{2\pi i k / n}$, polynomial multiplication computes in strictly $\mathcal{O}(N \log N)$ time.
- **NTT Modulo Primes:** For primes $P = c \cdot 2^k + 1$ (e.g. $998244353 = 119 \cdot 2^{23} + 1$), primitive root $g = 3$ provides exact integer roots of unity $g^{(P-1)/N}$, eliminating floating-point rounding errors.
- **FPS Inversion via Newton's Method:** Given $P(x)$ with $P(0) \neq 0$, its multiplicative inverse $Q(x) \equiv P(x)^{-1} \pmod{x^N}$ satisfies Newton iteration $Q_{2k} \equiv Q_k(2 - P \cdot Q_k) \pmod{x^{2k}}$, computing in $\mathcal{O}(N \log N)$.

##### Algorithmic Execution Blueprint

1. **Bit-Reversal Permutation:** Permute coefficient array by reversing the binary representation of indices in $\mathcal{O}(N)$.
2. **Butterfly Operations:** For length $len = 2, 4, 8 \dots N$, compute root of unity step $w_n$; for each butterfly pair, compute $u = a[i], v = a[i+len/2] \cdot w$; set $a[i] = u + v, a[i+len/2] = u - v$.
3. **Inverse NTT:** Execute forward transform with $w_n^{-1}$, then multiply each element by $N^{-1} \pmod P$.

##### Closed-Form Invariant Equations

$$A(x) \cdot B(x) = \text{INTT}\big(\text{NTT}(A) \odot \text{NTT}(B)\big), \quad Q_{new} = Q(2 - P \cdot Q) \pmod{x^{2k}}$$

##### Structural Edge Cases & Assumptions

- Padded polynomial length $N$ MUST be a power of 2 strictly greater than $\text{deg}(A) + \text{deg}(B)$.
- NTT with modulo 998244353 supports transform lengths up to $2^{23} \approx 8.38 \times 10^6$.
- For general arbitrary modulo (e.g. $10^9+7$), use MTT (3-prime NTT with CRT recombination) or split polynomials into $A(x) = A_1 \sqrt{M} + A_0$.

---

#### 3. Core Intuition & Problem Framing

You need to compute $f_i = \sum_{j=1}^{i-1} f_j g_{i-j}$ for $i=1 \dots N$. 
You cannot just multiply $f$ and $g$ because $f$ depends on its own previous values! 
Solution: CDQ Divide and Conquer. 
1. Solve for the left half $f_{L \dots M}$.
2. The left half contributes to the right half via a polynomial multiplication: $\text{contribution} = f_{L \dots M} \times g_{1 \dots R-L}$.
3. Add this contribution to the right half.
4. Recursively solve for the right half $f_{M+1 \dots R}$.
Time complexity: $O(N \log^2 N)$.

---

#### 4. Proof Sketches & Recurrences

The master theorem recurrence for the computation is $T(N) = 2 T(N / 2) + \mathcal{O}(N \log N)$. At recursion depth $k$, there are $2^k$ subproblems of size $N / 2^k$. In each subproblem, an NTT convolution of length $N / 2^k$ takes $\mathcal{O}(\frac{N}{2^k} \log \frac{N}{2^k})$. Summing over all $2^k$ subproblems at depth $k$ yields $\mathcal{O}(N \log N)$. Across all $\log_2 N$ levels of recursion, total time is $\mathcal{O}(N \log^2 N)$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// f is the array we are computing. g is the known coefficient array.
// Assume f[0] is base case.
void solve_dc_fft(int L, int R) {
    if (L == R) {
        // base case or finalize f[L]
        return;
    }
    int mid = L + (R - L) / 2;
    solve_dc_fft(L, mid);
    
    // Multiply f[L..mid] with g[1..R-L]
    vector<int> A(f.begin() + L, f.begin() + mid + 1);
    vector<int> B(g.begin() + 1, g.begin() + R - L + 1);
    vector<int> C = multiply_ntt(A, B);
    
    // Add contribution to right half
    for (int i = mid + 1; i <= R; ++i) {
        f[i] = (f[i] + C[i - L - 1]) % MOD;
    }
    
    solve_dc_fft(mid + 1, R);
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- ```cpp
// f is the array we are computing. g is the known coefficient array.
// Assume f[0] is base case.
void solve_dc_fft(int L, int R) {
    if (L == R) {
        // base case or finalize f[L]
        return;
    }
    int mid = L + (R - L) / 2;
    solve_dc_fft(L, mid);
    
    // Multiply f[L..mid] with g[1..R-L]
    vector<int> A(f.begin() + L, f.begin() + mid + 1);
    vector<int> B(g.begin() + 1, g.begin() + R - L + 1);
    vector<int> C = multiply_ntt(A, B);
    
    // Add contribution to right half
    for (int i = mid + 1; i <= R; ++i) {
        f[i] = (f[i] + C[i - L - 1]) % MOD;
    }
    
    solve_dc_fft(mid + 1, R);
}
```

---

#### 7. Contest WA / TLE / RE Traps

- Index offset errors in accumulation: $f[mid + 1]$ receives contribution from $A[mid - l] \times B[1]$, which is at index $(mid + 1) - l - 1 = mid - l$ of $C$.
- Recursion base case: forgetting that $f[0]$ must be initialized before recursing, or evaluating base case work at $l == r$.
- Padding vectors to powers of two incorrectly inside convolution.
- Modulo addition without taking `% MOD` during contribution accumulation.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-528D | Cutlet | 2400 | FFT, Polynomial Multiplication, Strings | Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions. | [Solve Problem](https://codeforces.com/contest/528/problem/D) |
| Codeforces | CF-1096G | Lucky Tickets | 2300 | NTT, Polynomial Exponentiation | Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N). | [Solve Problem](https://codeforces.com/contest/1096/problem/G) |
| Codeforces | CF-1251F | Red-White Fence | 2600 | D&C NTT, Generating Functions | Divide-and-Conquer NTT multiplying frequency polynomials. | [Solve Problem](https://codeforces.com/contest/1251/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Fast Fourier Transform & NTT](https://cp-algorithms.com/algebra/fft.html)
- **[Codeforces]** [Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)](https://codeforces.com/blog/entry/71892)
- **[YouKn0wWho]** [YouKn0wWho Academy: Formal Power Series & NTT Convolutions](https://youkn0wwho.academy/topic-list#fft)

---


---
