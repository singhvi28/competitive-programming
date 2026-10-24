# XOR basis / linear basis

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Bitwise XOR, greedy on bits, basic linear algebra intuition over GF(2)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Bitwise XOR, greedy on bits, basic linear algebra intuition over GF(2)

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

Subset XORs of a multiset of integers form a subspace of \(\mathrm{GF}(2)^w\). A **linear basis** stores at most \(w\) vectors (usually \(w \le 32\) or \(64\)) in row-echelon form by highest bit: insertion tries to eliminate using existing pivots; if a bit position is free, the value becomes the pivot. Then: max XOR = greedy take/reject pivots from MSB; size of span = \(2^{|\mathrm{basis}|}\) (if 0 not forced extra); check representability by elimination.

*Note: This is Gaussian Elimination over GF(2). For general Gaussian Elimination over Reals or Modulo $P$, see [Section 14a](../16-a-gaussian-elimination-determinants.md).*

---

## 4. Proof Sketches & Recurrences

Gaussian elimination over GF(2) on columns = bits. Insertion of \(x\):
for \(b = w-1 \ldots 0\): if bit \(b\) of \(x\) set, if `basis[b]` empty assign, else `x ^= basis[b]`.  
If \(x\) becomes 0, it was dependent.  
Max: start `ans = 0`; for \(b = w-1 \ldots 0\): if `(ans ^ basis[b]) > ans` (unsigned) take it — for maximizing value.  
Count distinct: \(2^{sz}\) if we don’t store duplicates; if zero-subset only empty, still \(2^{sz}\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: insert / query \(O(W^2)\) naive or \(O(W)\) with care
- Total: \(O(n W)\) typical
- Memory: \(O(W)\)`

### C++17 Template

```cpp
namespace xor_basis {
struct Basis {
    static constexpr int W = 32; // use 64 for long long
    unsigned bas[W]{};
    int sz = 0;
    bool insert(unsigned x) {
        for (int b = W - 1; b >= 0; --b) {
            if (!((x >> b) & 1u)) continue;
            if (!bas[b]) { bas[b] = x; ++sz; return true; }
            x ^= bas[b];
        }
        return false; // dependent
    }
    bool representable(unsigned x) const {
        for (int b = W - 1; b >= 0; --b)
            if ((x >> b) & 1u) x ^= bas[b];
        return x == 0;
    }
    unsigned max_xor() const {
        unsigned ans = 0;
        for (int b = W - 1; b >= 0; --b)
            if ((ans ^ bas[b]) > ans) ans ^= bas[b];
        return ans;
    }
    // k-th smallest nonempty? usually k-th in span including 0:
    // rebuild triangular basis then digitize k
    unsigned kth(unsigned long long k) const { // 0-indexed in sorted span
        vector<unsigned> v;
        for (int b = 0; b < W; ++b) if (bas[b]) v.push_back(bas[b]);
        // optional: clean to diagonal for unique digits
        for (int i = 0; i < (int)v.size(); ++i)
            for (int j = 0; j < i; ++j)
                if ((v[i] ^ v[j]) < v[i]) v[i] ^= v[j];
        sort(v.begin(), v.end());
        if (k >= (1ULL << v.size())) return UINT_MAX; // invalid
        unsigned ans = 0;
        for (int i = 0; i < (int)v.size(); ++i)
            if ((k >> i) & 1ULL) ans ^= v[i];
        return ans;
    }
};
} // namespace xor_basis
```

### Python 3 Template

```python
class XorBasis:
    __slots__ = ("bas", "sz", "W")
    def __init__(self, W: int = 32):
        self.W = W
        self.bas = [0] * W
        self.sz = 0
    def insert(self, x: int) -> bool:
        for b in range(self.W - 1, -1, -1):
            if ((x >> b) & 1) == 0:
                continue
            if self.bas[b] == 0:
                self.bas[b] = x
                self.sz += 1
                return True
            x ^= self.bas[b]
        return False
    def max_xor(self) -> int:
        ans = 0
        for b in range(self.W - 1, -1, -1):
            if (ans ^ self.bas[b]) > ans:
                ans ^= self.bas[b]
        return ans
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Maximum XOR of a subset,” “number of distinct subset XORs”
- Insert numbers online; query max XOR with a value
- Paths on trees/graphs with XOR weights → basis of cycle XORs + path
- “Make XOR = x using subset” / independence

---

## 7. Contest WA / TLE / RE Traps

- Mixing signed comparisons for max XOR — prefer `unsigned`.
- Forgetting that inserting 0 does nothing.
- Counting \(2^{sz}\) vs \(2^{sz}-1\) (empty subset).
- Offline path-XOR on trees: need basis of **fundamental cycles**, not raw edges.

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

- Basis for AND/OR is **not** linear the same way — don’t force it.
- d-dimensional / larger fields rare in CF.
- Merge two bases: insert all pivots of one into the other (\(O(W^2)\)).

---

## 11. Typical Problem Archetypes

1. Standard application: max subset XOR.
2. Slightly disguised: max XOR of path in a tree (basis + dfs xor).
3. Difficult: k-th largest subset XOR; forced include/exclude.
4. Very difficult / advanced: linear basis + segment tree / time machine offline.

---

## 12. Recognition & Identification Drills

1. Array of \(n\) ints; maximize XOR of a subset.
2. Online insert; after each insert print size of set of subset XORs.
3. Edge-XOR weighted graph; can you achieve XOR \(x\) on a walk from \(u\) to \(v\)?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: subset XOR space questions
- Key invariant: span closed under XOR; basis size \(\le W\)
- Key formula: insert by MSB elimination; max via greedy MSB
- Complexity: \(O(n W)\)
- Template to remember: `if (!bas[b]) bas[b]=x; else x^=bas[b];`

---

---
