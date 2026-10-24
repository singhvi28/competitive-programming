# Invariants and Colouring

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Parity, Chessboard coloring, Ad-hoc logic  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Parity, Chessboard coloring, Ad-hoc logic

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

Some games cannot be solved by DP (state space too large) and are not Nim (no independent subgames). Instead, they are solved by finding a property that remains unchanged (**Invariant**) or predictably changes (**Monovariant**) after every valid move.
- **Parity / Chessboard Colouring:** E.g., A knight moving on a chessboard always changes the color of the square it is on. If the game ends on a specific square, you know exactly whose turn it will be based on the parity of the distance (Manhattan distance parity).
- **Domino Tiling Games:** If players place dominoes on a grid, coloring the grid like a chessboard reveals that every domino covers exactly one black and one white cell. This can reduce the game to finding maximum bipartite matchings.
- **Inversion Parity:** 15-puzzle style games. Sliding tiles preserves the parity of the number of inversions plus the row of the empty square. You can easily classify states as winning/losing or reachable/unreachable by checking this parity.

---

## 4. Proof Sketches & Recurrences

To prove a strategy using invariants:
1. Identify a coloring scheme or mathematical parity.
2. Prove that a move by Player A *preserves* the invariant, or forces a specific parity.
3. Show that the terminal losing state has a different parity, meaning Player A can never be forced into it.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Missing edge cases where the board dimensions are odd vs even (parity flips).
- Forgetting to account for the starting parity.

## End-of-section mini comparison

- **Nim vs SG:** Nim = special case where \(g(\text{heap }n)=n\); SG = compute \(g\) for custom moves, then same XOR composition.
- **Normal vs misère:** normal → XOR \(\neq 0\) wins; misère Nim → same **unless** all heaps \(\le 1\), then flip. General misère ≠ flip SG.
- **Game DP vs SG:** Game DP = one state space, W/L or score; SG = decompose into sum + mex tables + XOR. If it does not split, do not force Grundy.
- **Strategy-stealing vs DP:** stealing proves *someone* wins; DP/SG *computes* the winner when states are small.

## What to drill this week

1. Code **Nim** who-wins + one winning move; stress random heaps against brute for \(k\le 4, a_i\le 10\).
2. **Subtraction game** Grundy table; multi-pile XOR; verify vs recursive W/L on small.
3. One **split-into-two** game: \(g(n)=\operatorname{mex}\{g(a)\oplus g(b)\}\).
4. **Misère Nim** casework: compare \([1,1,1]\) vs \([2,1,1]\) by hand and with template.
5. **Interval take-ends** DP and one classic subtract-a-square win/lose DP.
6. Recognition only: read one Chomp / pairing editorial; do **not** prioritize implementing stealing.`

### C++17 Template

```cpp
// Typically an ad-hoc problem.
// Common helper: compute inversion parity
int count_inversions(const vector<int>& a) {
    int inv = 0, n = (int)a.size();
    for (int i = 0; i < n; ++i) {
        if (a[i] == 0) continue; // empty space
        for (int j = i + 1; j < n; ++j) {
            if (a[j] != 0 && a[i] > a[j]) inv++;
        }
    }
    return inv % 2;
}
```

---

## 6. Recognition Trigger Signals & Heuristics

- Grid-based games where players move tokens.
- Games where a state undergoes localized flips or swaps.
- Proving a target state is unreachable (if the invariant differs from the start state).

---

## 7. Contest WA / TLE / RE Traps

- Assuming an invariant is sufficient: invariant equality $I(A) = I(B)$ proves that transition is NOT IMPOSSIBLE, but does not always guarantee reachability without a constructive proof.
- Grid coordinate parity off-by-one: 0-indexed vs 1-indexed $(r + c) \pmod 2$.
- Missing monovariant lower bounds: assuming a quantity decreases without bounding it from below.
- Ignoring moves that temporarily increase the invariant before stabilizing.

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
