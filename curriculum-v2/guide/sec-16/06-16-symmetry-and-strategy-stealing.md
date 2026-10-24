# 6. Symmetry and Strategy-Stealing

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1700–2600 | **Frequency:** Occasional  
> **Prerequisites:** Combinatorial game basics, proof-oriented thinking, ad-hoc  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2600
- Prerequisites: Combinatorial game basics, proof-oriented thinking, ad-hoc

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

In perfectly symmetric games, the Second Player often has a dominant **Mirroring** strategy. 
- **Classic Example:** Placing non-overlapping coins on a circular table. The First Player places a coin in the exact center. From then on, the First Player just mirrors the Second Player's moves diametrically opposite. Because of symmetry, whenever the Second player finds a valid spot, the First player is guaranteed to find its symmetric counterpart empty.
- **Bipartite Graphs:** If the game is played on a graph with a perfect matching, and you can always move along the matched edge, you win.
- **Strategy-Stealing:** Used to prove the First Player wins without exhibiting the strategy. E.g., Chomp. First player makes a harmless "null" move. If the Second player had a winning strategy, the First player steals it. Since someone must win (no draws), the First player wins.

---

## 4. Proof Sketches & Recurrences

Sketch (Chomp-style):
1. Position is finite, deterministic, perfect information, no draw → someone wins.
2. Second-player win assumption ⇒ strategy \(S\).
3. First takes a “neutral” bite; thereafter answers with \(S\); if \(S\) asks for the already-taken cell, take another neutral and continue.
4. Contradiction because \(S\) would also win for first → first wins.
Mirroring: on symmetric graphs, second copies across automorphism unless first breaks symmetry (then steal).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(1)\) mirror reply when constructive
- Total: proof \(O(1)\) insight; code only for pairing simulation
- Memory: \(O(n)\) for pairs`

### C++17 Template

```cpp
// No general solver — strategy-stealing is a proof pattern.
// Constructive cousin: pairing / mirroring strategy for SECOND player.
namespace pairing_strategy {
  // Example idea: cells paired (i -> p[i]). Whatever first takes in a pair,
  // second takes the mate if free. Second wins if every winning set
  // is blocked by the pairing (problem-specific check).
  bool second_can_mirror(int n, const vector<int>& pair_of) {
    // placeholder: validate pairing involution
    for (int i = 0; i < n; ++i)
      if (pair_of[pair_of[i]] != i) return false;
    return true;
  }
}
```

### Python 3 Template

```python
def mirror_reply(move: int, n: int) -> int:
    # 1-indexed circle / array mirror example
    return n + 1 - move
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Prove first player wins” in math/ICPC theory problems
- Symmetric boards where extra move cannot hurt
- Mirror / pairing strategies as the **constructive** twin of stealing
- Chomp, positional games, maker-breaker intuition questions

---

## 7. Contest WA / TLE / RE Traps

- Treating stealing as an implementable DP
- Broken symmetry: mirror fails when center cell / odd dimension not handled
- Assuming draws impossible when the rules allow draws
- Using stealing on **partizan** games incorrectly

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

- **Pairing strategy** (second player): block all threats via fixed pairs
- **Mirroring** on symmetric graphs / centrals
- **Strategy stealing + extra pawn**: “null move” harmless in monotone games

---

## 11. Typical Problem Archetypes

1. Standard application: prove first wins at Chomp / similar (theory)
2. Slightly disguised: constructive mirror on symmetric pile/board CF task
3. Difficult: design a pairing that blocks all winning configurations
4. Very difficult / advanced: maker-breaker positional games criteria

---

## 12. Recognition & Identification Drills

1. Chomp on \(2\times n\); argue who wins without listing all states.
2. Symmetric game on a path; second mirrors across center — when does this work?
3. Prove that an extra isolated winning token cannot hurt the player who “owns” a stolen strategy.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: existence proofs; or constructive mirror/pairing
- Key invariant: extra move does not hurt in monotone claiming games
- Key formula: none algorithmic — contradiction via stolen \(S\)
- Complexity: insight / \(O(1)\) mirror
- Template to remember: assume second wins → steal \(S\); else code pairing

---


---

---
