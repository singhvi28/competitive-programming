# Divide and Conquer FFT (Semi-Online Convolution)

> **Section:** §15 FFT, NTT & Formal Power Series  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** B-tier | **Rating Range:** 2400+ | **Frequency:** Rare  
> **Prerequisites:** FFT/NTT, Divide and Conquer  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400+
- Prerequisites: FFT/NTT, Divide and Conquer

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

You need to compute $f_i = \sum_{j=1}^{i-1} f_j g_{i-j}$ for $i=1 \dots N$. 
You cannot just multiply $f$ and $g$ because $f$ depends on its own previous values! 
Solution: CDQ Divide and Conquer. 
1. Solve for the left half $f_{L \dots M}$.
2. The left half contributes to the right half via a polynomial multiplication: $\text{contribution} = f_{L \dots M} \times g_{1 \dots R-L}$.
3. Add this contribution to the right half.
4. Recursively solve for the right half $f_{M+1 \dots R}$.
Time complexity: $O(N \log^2 N)$.

---

## 4. Proof Sketches & Recurrences

The master theorem recurrence for the computation is $T(N) = 2 T(N / 2) + \mathcal{O}(N \log N)$. At recursion depth $k$, there are $2^k$ subproblems of size $N / 2^k$. In each subproblem, an NTT convolution of length $N / 2^k$ takes $\mathcal{O}(\frac{N}{2^k} \log \frac{N}{2^k})$. Summing over all $2^k$ subproblems at depth $k$ yields $\mathcal{O}(N \log N)$. Across all $\log_2 N$ levels of recursion, total time is $\mathcal{O}(N \log^2 N)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

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

## 7. Contest WA / TLE / RE Traps

- Index offset errors in accumulation: $f[mid + 1]$ receives contribution from $A[mid - l] \times B[1]$, which is at index $(mid + 1) - l - 1 = mid - l$ of $C$.
- Recursion base case: forgetting that $f[0]$ must be initialized before recursing, or evaluating base case work at $l == r$.
- Padding vectors to powers of two incorrectly inside convolution.
- Modulo addition without taking `% MOD` during contribution accumulation.

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
