# Gray code

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** C-tier | **Rating Range:** 1600–2200 | **Frequency:** Rare  
> **Prerequisites:** Bitmask tricks  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Bitmask tricks

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Bit Manipulation and Advanced Combinatorics address subset lattices, binomial coefficients modulo arbitrary integers, Lucas Theorem, Catalan Numbers, Stirling Numbers, and Burnside's Lemma for group action symmetries.

### Fundamental Theorems & Invariants

- **Submask Iteration Lemma:** Iterating over all submasks of all masks of size $N$ using `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)` executes in strictly $\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$ steps.
- **Lucas Theorem:** For prime $p$, $\binom{n}{k} \equiv \prod_{i=0}^m \binom{n_i}{k_i} \pmod p$, where $n_i, k_i$ are base-$p$ digits of $n$ and $k$.
- **Burnside's Lemma:** The number of distinct orbits under group action $G$ on set $X$ equals the average number of fixed points: $|X / G| = \frac{1}{|G|} \sum_{g \in G} |X^g|$.

### Algorithmic Execution Blueprint

1. **Binomial Precomputation:** Precompute factorials $fact[i] = fact[i-1] \cdot i \pmod P$ and inverse factorials $invFact[i] = invFact[i+1] \cdot (i+1) \pmod P$ in $\mathcal{O}(N)$ linear time.
2. **Rotational Symmetry (Necklaces):** For $N$ beads with $K$ colors under rotation, $|G| = N$, and rotation by $i$ fixes $K^{\gcd(i, N)}$ colorings. Compute $\frac{1}{N} \sum_{i=0}^{N-1} K^{\gcd(i, N)} \pmod P$.

### Closed-Form Invariant Equations

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1}, \quad \binom{n}{k} \equiv \prod \binom{n_i}{k_i} \pmod p$$

### Structural Edge Cases & Assumptions

- Lucas Theorem applies only for prime modulo $p$; for prime powers $p^k$, use Andrew Granville's generalization or Prime-Factorization tracking.
- Submask iteration without `sub > 0` condition creates an infinite loop because `(0 - 1) & mask = mask`.
- Dividing by group size $|G|$ under modulo $P$ requires $\gcd(|G|, P) = 1$.

---

## 3. Core Intuition & Problem Framing

Binary-reflected Gray code orders all \(n\)-bit strings so consecutive codes differ by exactly one bit. The map \(i \mapsto i \oplus (i >> 1)\) is the standard encoding; decoding recovers \(i\) by XORing down prefixes. Useful when you must traverse the hypercube with single-bit flips (Hamiltonian path on the cube).

---

## 4. Proof Sketches & Recurrences

Encode: \(g(i) = i \oplus \lfloor i/2 \rfloor\).  
Decode: \(i = g \oplus (g >> 1) \oplus (g >> 2) \oplus \cdots\).  
Binary-reflected construction: \(n\)-bit list = \(0\cdot G_{n-1}\) then \(1\cdot \mathrm{rev}(G_{n-1})\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\) or \(O(2^n)\) to materialize
- Per-query / per-operation: \(O(1)\) encode; \(O(\log i)\) naive decode
- Total: \(O(2^n)\) full tour
- Memory: \(O(1)\) streaming or \(O(2^n)\) list`

### C++17 Template

```cpp
namespace gray {
int encode(int i) { return i ^ (i >> 1); }
int decode(int g) {
    int i = g;
    while (g) { g >>= 1; i ^= g; }
    return i;
}
// visit all masks in Gray order: start 0, flip bit ctz(i^(i-1)) ...
vector<int> sequence(int n) {
    vector<int> a(1 << n);
    for (int i = 0; i < (1 << n); ++i) a[i] = encode(i);
    return a;
}
} // namespace gray
```

### Python 3 Template

```python
def gray_encode(i: int) -> int:
    return i ^ (i >> 1)

def gray_decode(g: int) -> int:
    i = g
    while g:
        g >>= 1
        i ^= g
    return i
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Adjacent configurations differ by one element”
- Hardware / puzzle: revolving drum, Tower-adjacent flips
- Generate all subsets with only add/remove one element between neighbors

---

## 7. Contest WA / TLE / RE Traps

- Confusing encode/decode direction.
- Assuming Gray order equals numeric order for DP transitions — it does not.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-449D | Jzzhu and Numbers | 2400 | SOS DP, Inclusion Exclusion, Bitwise | SOS DP computes superset counts; apply Principle of Inclusion-Exclusion. | [Solve Problem](https://codeforces.com/contest/449/problem/D) |
| Codeforces | CF-1043F | Make It One | 2500 | Combinatorics, Möbius, DP | Combinatorics with Möbius inversion checking whether k elements have gcd = 1. | [Solve Problem](https://codeforces.com/contest/1043/problem/F) |
| CSES | CSES-2209 | Counting Necklaces | 1800 | Burnside's Lemma, Combinatorics | Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n. | [Solve Problem](https://cses.fi/problemset/task/2209) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Binomial Coefficients & Lucas Theorem](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- **[CP-Algorithms]** [CP-Algorithms: Burnside's Lemma & Polya Enumeration](https://cp-algorithms.com/combinatorics/burnside.html)
- **[USACO Guide]** [USACO Guide: Bitmask Operations and Submask Enumeration](https://usaco.guide/gold/combo)

---

## 10. Algorithmic Variants & Advanced Extensions

- Balanced Gray codes; combinatorial Gray codes for combinations (\(k\)-subsets).
- Steinhaus–Johnson–Trotter for permutations (adjacent swaps) — cousin idea.

---

## 11. Typical Problem Archetypes

1. Standard application: list all masks with single-bit transitions.
2. Slightly disguised: minimize changes when sweeping configurations.
3. Difficult: \(k\)-subset Gray code for combination generation.
4. Very difficult / advanced: Gray codes on other graphs / necklaces.

---

## 12. Recognition & Identification Drills

1. Output a sequence of all \(2^n\) subsets where each step adds or removes one element.
2. Convert index \(i\) to Gray code and back for \(n=20\).
3. Robot must visit all switch states flipping one switch at a time.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: single-bit-flip Hamiltonian path on \(\{0,1\}^n\)
- Key invariant: consecutive Gray codes differ by 1 bit
- Key formula: \(g = i \oplus (i >> 1)\)
- Complexity: \(O(1)\) per code
- Template to remember: `i ^ (i >> 1)`

---

---
