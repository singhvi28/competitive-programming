# 5. Game DP

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** DP / memoization, recursion on states, win-lose definitions  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: DP / memoization, recursion on states, win-lose definitions

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

When the position is **one coupled state** (not a tidy sum of heaps), compute directly: a position is losing iff **all** moves lead to a winning position for the opponent (or no moves — usually lose under normal play). Optionally DP the **best score** under optimal play (minimax). Use SG only when you need composition; use Game DP when the whole game is one DP.

---

## 4. Proof Sketches & Recurrences

- Normal play W/L: \(\mathrm{win}(v)=\exists u{\leftarrow}v:\neg\mathrm{win}(u)\); \(\mathrm{win}(\text{terminal})=\bot\).
- Score: \(\mathrm{dp}(v)=\operatorname{opt}_{u} \mathrm{value}(v\to u)+\mathrm{dp}(u)\) with alternating max/min or “current player maximizes own score.”
- Interval games (take ends of array): \(dp[l][r]\) = best for player to move on \(a[l..r]\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(|\text{states}| \cdot |\text{moves}|)\)
- Total: problem-specific (often \(O(n^2)\) intervals, \(O(2^n n)\) masks)
- Memory: \(O(|\text{states}|)\)`

### C++17 Template

```cpp
namespace game_dp {
  // win/lose on int state; moves(v) lists successors
  bool is_win(int v, vector<int>& memo, auto&& moves) {
    if (memo[v] != -1) return memo[v];
    for (int u : moves(v))
      if (!is_win(u, memo, moves)) return memo[v] = 1;
    return memo[v] = 0; // no move to a losing position
  }

  // interval: take a[l] or a[r]; return best score for current player
  // opponent also optimal; total remaining sum known → maximize own score
  long long interval_best(const vector<long long>& a) {
    int n = (int)a.size();
    vector<vector<long long>> dp(n, vector<long long>(n));
    for (int i = 0; i < n; ++i) dp[i][i] = a[i];
    for (int len = 2; len <= n; ++len)
      for (int l = 0; l + len - 1 < n; ++l) {
        int r = l + len - 1;
        dp[l][r] = max(a[l] - dp[l + 1][r], a[r] - dp[l][r - 1]);
      }
    return dp[0][n - 1]; // score difference current - opponent
  }
}
```

### Python 3 Template

```python
from functools import cache

def is_win(start: int, moves) -> bool:
    @cache
    def win(v: int) -> bool:
        return any(not win(u) for u in moves(v))
    return win(start)

def interval_diff(a: list[int]) -> int:
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = a[i]
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = max(a[l] - dp[l + 1][r], a[r] - dp[l][r - 1])
    return dp[0][n - 1]
```

---

## 6. Recognition Trigger Signals & Heuristics

- Shared board / one array / one number that both alter
- “Both play optimally; maximize score / difference”
- States small enough: \(n \le 10^3\) with \(O(n^2)\), masks \(2^n\), interval DP
- No clean split into independent impartial components

---

## 7. Contest WA / TLE / RE Traps

- Wrong terminal: empty moves → lose (normal) vs score \(0\)
- Alternating players but coding both as maximizers without negate/diff trick
- Recursion depth on deep chains — prefer iterative bottoms-up when DAG is sized
- Using SG XOR on a **non**-sum game

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

- **Grundy via game DP**: same recursion but mex instead of bool
- **Partizan / different move sets**: still DP; no SG
- **Probability / expected value games**: DP expectations

---

## 11. Typical Problem Archetypes

1. Standard application: subtract a square; win/lose DP on \(n\)
2. Slightly disguised: take 1..m from a pile; or stone piles with shared rules
3. Difficult: interval DP take from ends; optimal score
4. Very difficult / advanced: game on graphs with state compression / pairing strategy DP

---

## 12. Recognition & Identification Drills

1. Starting from \(n\); subtract a positive perfect square; last move wins.
2. Array of coins; each turn take leftmost or rightmost; maximize own sum.
3. Shared matrix; players color cells with constraints; decide winner with small \(n\).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: single coupled position / scoring; states enumerable
- Key invariant: win iff exists move to lose for opponent
- Key formula: \(\mathrm{win}(v)=\exists u:\neg\mathrm{win}(u)\)
- Complexity: DP on state graph
- Template to remember: memoized `any(not win(u))`

---

---
