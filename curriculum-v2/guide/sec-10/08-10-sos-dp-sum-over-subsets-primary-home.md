# SOS DP (Sum over Subsets) — primary home

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** Bitmasks, inclusion on the subset lattice, iterative DP over bits  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Bitmasks, inclusion on the subset lattice, iterative DP over bits

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Dynamic Programming Optimizations accelerate quadratic or cubic recurrences to linear or linearithmic time by exploiting geometric properties and monotonicity: Convex Hull Trick (CHT), Li Chao Tree, Divide and Conquer DP, Knuth Optimization, and SOS DP.

### Fundamental Theorems & Invariants

- **Convex Hull Trick (CHT):** Optimizes $dp[i] = \min_{j < i} (dp[j] + m_j \cdot x_i + c_j)$. If slopes $m_j$ and query points $x_i$ are monotonic, lines are maintained on a convex envelope in $\mathcal{O}(1)$ amortized per query.
- **Li Chao Tree Invariant:** A segment tree storing line segments where each node holds the line with greatest value at the segment midpoint. Supports insertion of arbitrary non-monotonic lines and point evaluation in $\mathcal{O}(\log C)$.
- **Quadrangle Inequality & D&C DP:** If transition cost satisfies $C(a, c) + C(b, d) \le C(a, d) + C(b, c)$ for $a \le b \le c \le d$, the optimal split points satisfy $opt(i, j) \le opt(i, j+1)$, enabling Divide & Conquer DP in $\mathcal{O}(K N \log N)$.
- **Knuth Optimization:** If $opt(i, j-1) \le opt(i, j) \le opt(i+1, j)$, standard interval DP runs in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.

### Algorithmic Execution Blueprint

1. **Monotone CHT:** Maintain deque of lines. To insert $(m, c)$, remove lines from back if intersection with new line precedes intersection with second-to-last line. To query $x$, pop from front while front line is suboptimal.
2. **SOS DP (Sum Over Subsets):** For bitmask size $N$, run $N$ phases: `for i from 0 to N-1: for mask from 0 to 2^N-1: if mask & (1<<i): dp[mask] += dp[mask ^ (1<<i)]` in $\mathcal{O}(N \cdot 2^N)$ time.

### Closed-Form Invariant Equations

$$dp[i] = \min_{j < i} \big(dp[j] + m_j x_i + c_j\big), \quad \text{Intersect}(L_1, L_2) = \frac{c_1 - c_2}{m_2 - m_1}$$

### Structural Edge Cases & Assumptions

- In CHT slope intersection, avoid floating-point inaccuracies by cross-multiplying integer slopes and intercepts with `__int128_t`.
- When slopes are identical ($m_1 = m_2$), keep only the line with the better intercept ($c_1 < c_2$ for min queries).
- Divide and Conquer DP applies only when transitions depend strictly on the previous layer $k-1$, not within the current layer $k$.

---

## 3. Core Intuition & Problem Framing

Given values \(A[mask]\) on \(\{0,1\}^n\), many tasks need

\[
Z[S]=\sum_{T\subseteq S} A[T]
\qquad\text{or}\qquad
M[S]=\sum_{T\supseteq S} A[T]
\]

Naively \(O(3^n)\). **SOS DP / fast zeta transform** does it in \(O(2^n\cdot n)\): for each bit \(b\), “push” contributions along that bit dimension (like a high-dimensional prefix sum on the boolean cube).

Möbius inversion recovers \(A\) from \(Z\):

\[
A[S]=\sum_{T\subseteq S}(-1)^{|S\setminus T|}Z[T]
\]

also in \(O(2^n n)\) (fast Möbius).

This is the engine under OR-convolutions, subset-sum style bit DP aggregations, and “for each mask, combine all submasks”.

---

## 4. Proof Sketches & Recurrences

**Submask zeta (sum over subsets):** interpret \(A\) as values on an \(n\)-dimensional \(0/1\) grid. Prefix along dimension \(b\):

```
f = A
for b in 0..n-1:
  for mask in 0..(1<<n)-1:
    if mask & (1<<b):
      f[mask] += f[mask ^ (1<<b)]
```

Invariant after processing bits \(0..b\): \(f[S]\) sums \(A[T]\) over \(T\) that may differ from \(S\) only in bits \(\le b\) (and \(T\subseteq S\)). At the end, \(f[S]=\sum_{T\subseteq S}A[T]\).

**Superset zeta (sum over supersets):**

```
if (mask & (1<<b)) == 0:
  f[mask] += f[mask | (1<<b)]
```
(order of loops carefully; common form iterate bits, then masks).

**Möbius (invert submask zeta):**

```
for b in 0..n-1:
  for mask:
    if mask & (1<<b):
      f[mask] -= f[mask ^ (1<<b)]
```

**Submask enumeration** (still useful when you need every pair \((S,T\subseteq S)\)):

```
for (int s = 0; s < (1<<n); ++s)
  for (int t = s; t; t = (t - 1) & s)
    // use t
  // also t=0
```
Total \(O(3^n)\). Prefer SOS when only **aggregates** matter.

**OR convolution** via zeta: for \(h=f\ast_{OR} g\) meaning \(h[S]=\sum_{i|j=S}f[i]g[j]\),

1. \(F=\zeta f\), \(G=\zeta g\) (submask sums)
2. \(H[S]=F[S]\cdot G[S]\) pointwise
3. \(h=\mu H\) (Möbius)

(Exact identities vary for AND/OR; XOR uses FWHT.)

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(2^n)\) fill of \(A\)
- Per-query / per-operation: \(O(1)\) after transform if answers are \(Z[S]\)
- Total: \(O(2^n\cdot n)\) per zeta/Möbius; submask enum \(O(3^n)\)
- Memory: \(O(2^n)\)`

### C++17 Template

```cpp
// C++17 — SOS DP: zeta / Möbius on subset lattice
#include <bits/stdc++.h>
using namespace std;

namespace sos {
using ll = long long;

// In-place sum over subsets: f[S] <- sum_{Tsubseteq S} f[T]
void zeta_subsets(vector<ll>& f) {
    int N = (int)f.size(); // N = 1<<n
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] += f[mask ^ b];
}

// Inverse: recover A from Z
void mobius_subsets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] -= f[mask ^ b];
}

// Sum over supersets: f[S] <- sum_{T supseteq S} f[T]
void zeta_supersets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (!(mask & b)) f[mask] += f[mask | b];
}

void mobius_supersets(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (!(mask & b)) f[mask] -= f[mask | b];
}

// Pointwise max over submasks (common contest variant)
void zeta_subsets_max(vector<ll>& f) {
    int N = (int)f.size();
    for (int b = 1; b < N; b <<= 1)
        for (int mask = 0; mask < N; ++mask)
            if (mask & b) f[mask] = max(f[mask], f[mask ^ b]);
}

// Enumerate all submasks of m: O(3^n) total over all m if done for all
template<class F>
void for_submasks(int m, F &&consume) {
    for (int s = m;; s = (s - 1) & m) {
        consume(s);
        if (!s) break;
    }
}

// OR-convolution h[s] = sum_{i|j = s} f[i]*g[j]
vector<ll> or_convolution(vector<ll> f, vector<ll> g) {
    int N = (int)f.size();
    zeta_subsets(f);
    zeta_subsets(g);
    vector<ll> h(N);
    for (int i = 0; i < N; ++i) h[i] = f[i] * g[i];
    mobius_subsets(h);
    return h;
}

// Classic: dp[mask] = sum of a[i] over i in mask, then queries SOS
vector<ll> sum_over_submasks_values(const vector<ll>& a) {
    // a indexed by mask already
    vector<ll> f = a;
    zeta_subsets(f);
    return f;
}

// DP: for each mask, best over submasks of popcount transition example
// f[mask] += product over bit contributions — place problem-specific code atop zeta
} // namespace sos
```

### Python 3 Template

```python
def zeta_subsets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if mask & b:
                f[mask] += f[mask ^ b]
        b <<= 1
    return f

def mobius_subsets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if mask & b:
                f[mask] -= f[mask ^ b]
        b <<= 1
    return f

def zeta_supersets(f):
    N = len(f)
    b = 1
    while b < N:
        for mask in range(N):
            if not (mask & b):
                f[mask] += f[mask | b]
        b <<= 1
    return f

def or_convolution(f, g):
    f, g = f[:], g[:]
    zeta_subsets(f)
    zeta_subsets(g)
    h = [f[i] * g[i] for i in range(len(f))]
    mobius_subsets(h)
    return h
```

---

## 6. Recognition Trigger Signals & Heuristics

- “For every mask, sum/fmax over all submasks / supermasks”.
- Enumerating submasks \(O(3^n)\) appears; \(n\le 20\)–\(22\) with need for \(2^n n\).
- Problems: sum of AND/OR over pairs; DP over subsets with submask transitions that only need aggregates.
- After computing \(f[S]\), need \(g[S]=\sum_{T\subseteq S}f[T]\).
- Keywords: zeta transform, Möbius on subset lattice, FWHT cousin (XOR is different — Walsh–Hadamard).
- **Stub elsewhere:** bit/combinatorics section links here for full treatment.

---

## 7. Contest WA / TLE / RE Traps

- Mixing subset vs superset transforms (wrong `if` on bit).
- Forgetting mod normalization on Möbius subtract.
- Using XOR-FWHT identities for OR/AND (wrong).
- In-place transform then needing original \(A\) — copy first.
- \(n\) not matching `f.size()==1<<n`.
- Off-by-one: empty mask handling in enumeration.
- Overflow on products in OR-convolution before Möbius.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-319C | Kalila and Dimna in the Logging Industry | 2100 | Convex Hull Trick, DP Optimization | Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes. | [Solve Problem](https://codeforces.com/contest/319/problem/C) |
| Codeforces | CF-1083E | The Fair Nut and Rectangles | 2400 | CHT, Li Chao Tree, DP | Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract. | [Solve Problem](https://codeforces.com/contest/1083/problem/E) |
| Codeforces | CF-1175G | Yet Another Partiton Problem | 2900 | Li Chao Tree, Monotone Stack, D&C DP | Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N). | [Solve Problem](https://codeforces.com/contest/1175/problem/G) |
| Codeforces | CF-165E | Compatible Numbers | 2200 | SOS DP, Bitmasks | SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N). | [Solve Problem](https://codeforces.com/contest/165/problem/E) |
| Codeforces | CF-321E | Ciel and Gondolas | 2600 | Divide and Conquer DP, Quadrangle Inequality | Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity. | [Solve Problem](https://codeforces.com/contest/321/problem/E) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Convex Hull Trick & Dynamic CHT](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- **[CP-Algorithms]** [CP-Algorithms: Divide and Conquer DP Optimization](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- **[Codeforces]** [Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto](https://codeforces.com/blog/entry/45223)
- **[Codeforces]** [Codeforces Blog: 1D/1D Dynamic Programming Optimizations](https://codeforces.com/blog/entry/8284)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Max / min / gcd / OR** over submasks (same loop, change `+=` to op; not all invertible).
- **Fast subset convolution** \(h[S]=\sum_{T\subseteq S}f[T]g[S\setminus T]\) in \(O(2^n n^2)\) — advanced; Niche early.
- **AND convolution** via superset zeta or bit-complementation tricks.
- **Weighted popcount layers** for subset convolution.
- Online SOS / segmented — rare.

---

## 11. Typical Problem Archetypes

1. Standard: given \(a[mask]\), answer \(\sum_{T\subseteq S}a[T]\) for all \(S\).
2. Slightly disguised: for each mask, max value among submasks; then DP.
3. Difficult: OR/AND convolution counting pairs with \(i|j=k\).
4. Very difficult: subset convolution / FWHT hybrids / high constraints \(n=23\).

---

## 12. Recognition & Identification Drills

1. Array \(a[0..2^n-1]\); for each \(x\), compute sum of \(a[y]\) over \(y\subseteq x\). Target complexity?
2. Count pairs \((i,j)\) with \(a_i|a_j=X\) for all \(X\).
3. \(dp[S]=\sum_{T\subseteq S} dp[T]\cdot cost[S\setminus T]\) — SOS enough or need subset convolution?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: aggregates over submasks/supermasks; OR/AND lattice convolutions.
- Key invariant: boolean-cube prefix sums bit by bit.
- Key formula: `if (mask&b) f[mask]+=f[mask^b]` (subset zeta).
- Complexity: \(O(2^n n)\).
- Template to remember: zeta → pointwise → Möbius for OR-conv; copy before in-place.

**Simpler DP passes when:** only few masks queried — enumerate submasks of those; or \(n\le 16\) and \(3^n\) OK (\(\sim 43M\)).

---

→ Continue: [`10-c-profile-dp-alien-wqs.md`](10-c-profile-dp-alien-wqs.md) (profile DP, Alien, WQS, recognition synthesis).

---
