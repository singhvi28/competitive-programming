# 3. Grundy numbers

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** mex, memoized DP on game graph, Sprague–Grundy  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: mex, memoized DP on game graph, Sprague–Grundy

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

## 3. Core Intuition & Problem Framing

Grundy number \(g(v)\) is the **nimber** of position \(v\): the smallest nonnegative integer not appearing among successors. It is DP on the DAG of positions (or memoized recursion). For a single pile/game you often need the full table \(g[0..n]\); for SG sums you only need \(g\) of each piece.

---

## 4. Proof Sketches & Recurrences

\[
g(v)=\operatorname{mex}\{ g(u) : v \to u \}
\]
- Terminal (no moves): \(g=0\) (\(P\)-position).
- Subtraction \(\{s\}\) on pile \(n\): \(g(n)=\operatorname{mex}\{g(n-s): s\in S, s\le n\}\); often eventually periodic.
- Split move \(n \to (a)+(b)\) with \(a+b=n\): \(g(n)=\operatorname{mex}\{ g(a)\oplus g(b) \}\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n \cdot |S|)\) typical for pile DP; or \(O(|V|+|E|)\) on explicit game graph
- Per-query / per-operation: \(O(1)\) lookup after table
- Total: as above
- Memory: \(O(n)\) or \(O(|V|)\)`

### C++17 Template

```cpp
namespace grundy {
  // subtraction game: remove s in S from one pile
  vector<int> subtraction(int n, const vector<int>& S) {
    vector<int> g(n + 1, 0);
    vector<char> seen;
    for (int i = 1; i <= n; ++i) {
      seen.assign(S.size() + 2, 0);
      for (int s : S) if (s <= i) {
        int x = g[i - s];
        if (x < (int)seen.size()) seen[x] = 1;
      }
      int m = 0;
      while (m < (int)seen.size() && seen[m]) ++m;
      g[i] = m;
    }
    return g;
  }

  // generic memo on int state (customize moves)
  int calc(int v, vector<int>& memo, auto&& moves) {
    if (memo[v] != -1) return memo[v];
    unordered_set<int> reach;
    for (int u : moves(v)) reach.insert(calc(u, memo, moves));
    int m = 0;
    while (reach.count(m)) ++m;
    return memo[v] = m;
  }
}
```

### Python 3 Template

```python
from functools import cache

def grundy_subtraction(n: int, S: list[int]) -> list[int]:
    g = [0] * (n + 1)
    for i in range(1, n + 1):
        reach = {g[i - s] for s in S if s <= i}
        m = 0
        while m in reach:
            m += 1
        g[i] = m
    return g

@cache
def grundy_split(n: int) -> int:
    # example: split pile n into two nonempty piles a+b=n
    if n == 0:
        return 0
    reach = set()
    for a in range(1, n):
        reach.add(grundy_split(a) ^ grundy_split(n - a))
    m = 0
    while m in reach:
        m += 1
    return m
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Compute who wins” but piles have **restricted** removals / merges / splits
- Need to combine many small games → must output numbers, not just W/L
- Positions form a DAG (moves decrease a potential: size, mask popcount, etc.)
- Statement asks for Grundy / “equivalent Nim heap”

---

## 7. Contest WA / TLE / RE Traps

- Not memoizing → exponential blowup
- Using W/L (`bool`) when later XOR composition needs full \(g\)
- Incorrect move generation (missing split → two-game XOR in mex set)
- Assuming periodicity without verifying period for given \(S\)

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Mask / grid Grundy**: state = bitset or pair; hash memo
- **Graph Nim / Kayles**: \(g\) on induced subgraphs (often \(2^n\) or component DP)
- **Optional pass / limited piles**: still mex, different edges

---

## 11. Typical Problem Archetypes

1. Standard application: subtraction / Euclidean-like pile; table \(g[0..n]\)
2. Slightly disguised: string / binary string moves; state compress to int
3. Difficult: move splits into two independent games; mex of XORs
4. Very difficult / advanced: Grundy on trees/paths with deletion; combine SG over forest

---

## 12. Recognition & Identification Drills

1. Pile \(n\); remove \(2^k\) stones only. Build \(g[0..n]\) and decide multi-pile winner.
2. Chomp on a \(1 \times n\) bar (equivalent to simple game) — compute Grundy of length.
3. Delete a vertex and adjacent edges on a path; remaining paths are a sum — define \(g\) of path length.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need nimber of a position / custom move set
- Key invariant: \(g=\operatorname{mex}\) of successor grundies
- Key formula: \(g(v)=\operatorname{mex}\{g(u)\}\) (or \(g(a)\oplus g(b)\) on splits)
- Complexity: DP on states
- Template to remember: memo + mex loop

---

---
