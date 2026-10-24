# 2. Sprague-Grundy theorem

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** Impartial games, mex, Nim XOR, notion of game sum  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Impartial games, mex, Nim XOR, notion of game sum

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

Any impartial game under normal play is **equivalent to a single Nim heap** whose size is the game’s Grundy number. The **sum** of games (move in exactly one component) has Grundy equal to the **XOR** of component Grundies. So: break the board into independent pieces → compute \(g\) each → XOR → nonzero means first wins.

---

## 4. Proof Sketches & Recurrences

- Define \(g(G) = \operatorname{mex}\{ g(G') : G \to G' \}\), \(\operatorname{mex} S = \min\{ n \ge 0 : n \notin S \}\).
- Prove by induction: \(G\) is \(P\)-position \(\iff g(G)=0\).
- Sum \(G+H\): moves to \(G'+H\) or \(G+H'\); set of reachable Grundies forces \(g(G+H)=g(G)\oplus g(H)\).
- Hence overall first-win \(\iff g_1 \oplus \cdots \oplus g_m \neq 0\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: cost of computing all needed \(g\) (problem-specific)
- Per-query / per-operation: \(O(m)\) XOR over \(m\) components
- Total: dominated by Grundy DP
- Memory: store \(g\) table for states`

### C++17 Template

```cpp
namespace sg {
  // mex of a small set of nonnegative ints
  int mex(const vector<int>& s) {
    static bool seen[256]; // raise if grundy can be large
    int m = 0;
    for (int x : s) if (x < 256) seen[x] = true;
    while (seen[m]) ++m;
    for (int x : s) if (x < 256) seen[x] = false;
    return m;
  }

  // example: sum of independent components with precomputed g[]
  bool first_wins(const vector<int>& grundy_of_components) {
    int x = 0;
    for (int g : grundy_of_components) x ^= g;
    return x != 0;
  }
}
```

### Python 3 Template

```python
def mex(vals: set[int]) -> int:
    m = 0
    while m in vals:
        m += 1
    return m

def sg_first_wins(grundies: list[int]) -> bool:
    x = 0
    for g in grundies:
        x ^= g
    return x != 0
```

---

## 6. Recognition Trigger Signals & Heuristics

- Board splits into disjoint regions after a move style that never couples them
- “Several piles / strips / subgraphs; move affects only one”
- Editorial keywords: mex, nimber, SG, “replace with smaller games”
- Not one shared resource / not partizan (both players same moves)

---

## 7. Contest WA / TLE / RE Traps

- Applying SG to **partizan** games (different moves for Left/Right)
- Forgetting the game is a **sum** (must move in exactly one component)
- Computing win/lose boolean instead of full Grundy when sums appear later
- mex off-by-one / not clearing `seen[]`

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

- **Selective compounds** (move in all / some components): different combination rules — not plain XOR
- **Misère** sums: SG fails in general; only special cases (see Misère Nim)
- **Graph games** (node Kayles, subtraction on graphs): SG on graph state or on components after splits

---

## 11. Typical Problem Archetypes

1. Standard application: several piles with custom remove sets; XOR of per-pile Grundy
2. Slightly disguised: cutting a chocolate / splitting a strip into two independent games
3. Difficult: games that split into 2+ components — \(g = \operatorname{mex}\) over \(g(A)\oplus g(B)\)
4. Very difficult / advanced: SG on large DAGs with memoized hashing of states

---

## 12. Recognition & Identification Drills

1. Three independent subtraction piles with set \(S=\{1,3,4\}\); who wins from \((5,7,2)\)?
2. A move splits one strip into two strips; game is sum of strips thereafter.
3. Multiple connected components on a graph; a move deletes a vertex in one component only.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: impartial, normal play, position = sum of independent games
- Key invariant: \(g(\text{sum})=\bigoplus g_i\)
- Key formula: first wins \(\iff \bigoplus g_i \neq 0\)
- Complexity: XOR \(O(m)\) after computing \(g\)
- Template to remember: compute \(g\) per component → XOR

---

---
