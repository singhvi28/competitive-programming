# Submask enumeration

> **Section:** §13 Bit Manipulation & Advanced Combinatorics  
> **Phase:** Phase 7 — Mathematics, Linear Algebra & Polynomials  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Common  
> **Prerequisites:** Bitmask tricks, bit-DP basics  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Bitmask tricks, bit-DP basics

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

For a fixed mask \(m\), every nonempty submask appears exactly once in the loop `for (int s = m; s; s = (s - 1) & m)`, and `s = 0` can be handled separately. Over all \(m\), \(\sum_m 2^{\mathrm{pop}(m)} = 3^n\) for an \(n\)-bit universe — the classic \(O(3^n)\) budget.

---

## 4. Proof Sketches & Recurrences

Identity: decrementing \(s\) then `& m` clears bits outside \(m\) and walks all submasks in reverse order.
Total time if you do this for every \(m\):
\[
\sum_{m=0}^{2^n-1} 2^{\mathrm{popcount}(m)} = \sum_{k=0}^{n} C(n,k) 2^k = 3^n.
\]
Supermasks of \(m\): iterate bits free outside \(m\), or use `for (int s = m; s < (1<<n); s = (s + 1) | m)`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(1)\)
- Per-query / per-operation: \(O(2^{\mathrm{pop}(m)})\) for one mask
- Total: \(O(3^n)\) over all masks
- Memory: \(O(1)\) or \(O(2^n)\) for DP tables`

### C++17 Template

```cpp
namespace submask {
// all nonempty submasks of m, then optionally 0
template <class F>
void enum_submasks(int m, F&& f, bool include_zero = true) {
    for (int s = m; s; s = (s - 1) & m) f(s);
    if (include_zero) f(0);
}

// for every mask: process all its submasks — O(3^n)
template <class F>
void for_all_mask_submasks(int n, F&& f) {
    int N = 1 << n;
    for (int m = 0; m < N; ++m)
        for (int s = m;; s = (s - 1) & m) {
            f(m, s);
            if (s == 0) break;
        }
}

// split m = a | b, a & b == 0, a,b nonempty optional
// enumerate a ⊆ m, b = m ^ a
template <class F>
void enum_splits(int m, F&& f, bool allow_empty = false) {
    for (int a = m;; a = (a - 1) & m) {
        int b = m ^ a;
        if (allow_empty || (a && b)) f(a, b);
        if (a == 0) break;
    }
}

// supermasks of m in universe n bits
template <class F>
void enum_supermasks(int m, int n, F&& f) {
    int U = (1 << n) - 1;
    int free = U ^ m;
    for (int s = free;; s = (s - 1) & free) {
        f(m | s);
        if (!s) break;
    }
}
} // namespace submask
```

### Python 3 Template

```python
def enum_submasks(m: int, include_zero: bool = True):
    s = m
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & m
    # note: yields m ... 0; if not include_zero, stop before 0
```

---

## 6. Recognition Trigger Signals & Heuristics

- DP transition: “split mask into two disjoint parts” or “submask of previous”
- Enumerate partitions of a bit-set into labeled/unlabeled blocks
- Statement mentions \(n \le 20\) and subset-of-subset structure

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `s == 0` (infinite loop if you write `do/while` wrong).
- Using submask enum when you need **SOS** (all-subset sums for every mask efficiently structured).
- Double-counting unordered splits \(\{a,b\}\) — iterate `a < b` or `a <= m/2` style.
- \(n = 20\) → \(3^{20} \approx 3.4 \cdot 10^9\) too slow; \(n \le 18\) typical for full \(3^n\), \(n \le 20\) only light work inside.

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

- Enumerate submasks by popcount layers.
- SOS DP (stub below / full in §04) replaces many “sum over submasks” DPs.
- Meet-in-the-middle: \(n=40\) → two halves + submask / subset sums.

---

## 11. Typical Problem Archetypes

1. Standard application: DP over subsets with transition from submasks.
2. Slightly disguised: assign people to teams — split bits.
3. Difficult: optimize constants / prune by popcount.
4. Very difficult / advanced: combine with SOS or FWT for convolutions.

---

## 12. Recognition & Identification Drills

1. \(n \le 18\) cities; DP over visited subset with split tours.
2. Count ways to partition a set of \(n \le 16\) into unordered pairs of blocks with scores.
3. For each mask, sum \(f[s]\) over \(s \subseteq m\) (hint: may be SOS, not raw enum).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: local submask walks / splits, \(n \le 18\)–20
- Key invariant: `(s - 1) & m` visits each submask once
- Key formula: total \(\sum 2^{\mathrm{pop}(m)} = 3^n\)
- Complexity: \(O(3^n)\) all pairs \((m,s\subseteq m)\)
- Template to remember: `for (int s = m; ; s = (s - 1) & m) { ...; if (!s) break; }`

---

---
