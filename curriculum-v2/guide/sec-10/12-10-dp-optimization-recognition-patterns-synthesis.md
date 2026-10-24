# DP optimization recognition patterns (synthesis)

> **Section:** §10 Dynamic Programming Optimizations  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier | **Rating Range:** 1800–2600 | **Frequency:** Common  
> **Prerequisites:** Exposure to techniques 1–11 in this section  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2600
- Prerequisites: Exposure to techniques 1–11 in this section

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

Optimizations are not random speed hacks — each requires a **structural property**:

| Property | Points to |
|----------|-----------|
| Decision monotonicity \(opt(j)\le opt(j+1)\) | D&C DP |
| Quadrangle inequality + interval merge | Knuth |
| Transition = min of lines | CHT / Li Chao |
| Sliding index window | Monotone queue |
| Ranges ruled by nearest greater/smaller | Monotone stack |
| Boolean / word-parallel | Bitset |
| Lattice aggregates on submasks | SOS |
| Narrow frontier | Profile DP |
| Exact \(k\) + convex \(opt(k)\) | Alien / WQS |

**Flow:** write naive recurrence → name the property → pick the lightest tool that fits → if \(n\) already allows naive, **ship naive**.

---

## 4. Proof Sketches & Recurrences

**Recognition flowchart (contest mental model):**

```text
Can naive pass?
  yes → implement naive
  no ↓
Is state a bitmask lattice aggregate?
  yes → SOS / submask enum
  no ↓
Boolean reachability / subset sum shaped?
  yes → bitset
  no ↓
Narrow grid frontier?
  yes → profile DP
  no ↓
Transition = min_j m_j*x_i + c_j ?
  yes → monotone? deque CHT : Li Chao
  no ↓
Sliding window of j for dp[i]?
  yes → monotone queue
  no ↓
Depends on nearest greater/smaller geometry?
  yes → monotone stack
  no ↓
Interval DP dp[l][r]=min_k dp[l][k]+dp[k+1][r]+C ?
  yes → QI? Knuth : naive / other
  no ↓
Layered dp[i][j]=min_t dp[i-1][t]+C(t,j) with opt monotone?
  yes → D&C DP
  no ↓
Need exactly k parts & opt(k) convex & penalized DP easy?
  yes → Alien / WQS
  no ↓
Different section (data structures, FFT, ...)
```

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: thinking time
- Per-query / per-operation: N/A
- Total: saves wrong \(O(n^2)\) attempts / wrong Knuth applications
- Memory: N/A`

### C++17 Template

```cpp
// C++17 — not one algorithm; a checklist encoded as comments for contest headers
namespace dp_opt_recognition {
/*
Checklist before coding an optimization:
1. Constraints: what complexity needed?
2. Recurrence written cleanly with domains of min/max.
3. Property:
   - monotone opt? (D&C)
   - QI interval? (Knuth)
   - linear in j with x_i? (CHT)
   - window? (queue) / NGE? (stack)
   - bits lattice? (SOS) / bool sums? (bitset)
   - exact k convex? (Alien/WQS)
4. Prove or empirically test property on random small cases.
5. Prefer simpler structure (queue before CHT before Alien).
*/
} // namespace dp_opt_recognition
```

### Python 3 Template

```python
def test_opt_monotone(compute_opt_array):
    opt = compute_opt_array()
    return all(opt[i] <= opt[i+1] for i in range(len(opt)-1))

def test_quadrangle(C, n):
    # C(a,c)+C(b,d) <= C(a,d)+C(b,c) for a<=b<=c<=d
    for a in range(n):
        for b in range(a, n):
            for c in range(b, n):
                for d in range(c, n):
                    if C(a,c)+C(b,d) > C(a,d)+C(b,c)+1e-9:
                        return False
    return True
```

---

## 6. Recognition Trigger Signals & Heuristics

- Expand algebra: squares → lines (CHT).
- “Last cut position” layered → D&C; “merge two sides” → Knuth.
- Window of length \(w\) → queue; “until bigger barrier” → stack.
- Masks + submasks sum → SOS before inventing \(3^n\) for all queries.
- \(k\) dimension only exists to count parts → Alien sniff (then prove convexity).

---

## 7. Contest WA / TLE / RE Traps

- Optimizing without a property (D&C on non-monotone opt).
- Using Knuth for layered last-cut DP (should be D&C) and vice versa.
- CHT when cost not linear after rewrite.
- Alien because \(k\) “feels annoying” without convexity.
- Ignoring that naive passes — burned time.

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

- Hybrid: D&C + CHT; WQS + CHT; bitset + SOS.
- Offline CDQ when online structure fails.
- Brute force property testing in stress against naive.

---

## 11. Typical Problem Archetypes

1. Standard: classify a known problem into the table above.
2. Slightly disguised: rewrite recurrence until a row matches.
3. Difficult: two properties fire — pick cheaper (queue vs CHT).
4. Very difficult: no classical opt; need new structure / DS.

---

## 12. Recognition & Identification Drills

1. \(dp[i][j]=\min_{t<j}dp[i-1][t]+(pref[j]-pref[t])^2\), \(n=1e5,k=200\) — name the opt(s).
2. \(dp[l][r]=\min_k dp[l][k]+dp[k+1][r]+w[l][r]\) with QI — name the opt.
3. Exactly \(k\) segments, \(n=1e5\), inner becomes CHT after \(\lambda\) — name the stack of techniques.
4. For each mask, max of \(a[t]\) over \(t\subseteq mask\) — name the opt.
5. \(dp[i]=\min_{i-k\le j<i}dp[j]+c[j]+f[i]\) — name the opt.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: always, before implementing a fancy DP.
- Key invariant: structure before asymptotics.
- Key formula: see flowchart property table.
- Complexity: naive if it passes; else match property → tool.
- Template to remember: **naive? → lattice/bitset/profile? → line/window/stack? → Knuth/D&C? → Alien?**

---

## End link

Return to hub: [`10-dp-optimizations.md`](10-dp-optimizations.md) for comparison tables and weekly drills.

---
