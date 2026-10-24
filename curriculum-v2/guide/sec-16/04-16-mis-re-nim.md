# Misère Nim

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 1800–2400 | **Frequency:** Rare  
> **Prerequisites:** Normal Nim / Bouton, careful casework  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Normal Nim / Bouton, careful casework

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

**Misère** = player who takes the last object **loses**. For standard Nim, Bouton’s XOR rule still works **unless** every heap has size at most \(1\) (and there is at least one heap). In that “all heaps \(\le 1\)” regime, the winner is the opposite of the normal-play winner (equivalently: first wins iff the number of heaps of size \(1\) is even — including the empty-all case carefully). Intuition: long heaps give enough “room” to mirror; when only singletons remain, the last-take-loses flips the count parity.

---

## 4. Proof Sketches & Recurrences

Let \(x = \bigoplus a_i\), \(M = \max a_i\). Contest misère Nim = last player to move loses.
- If \(M > 1\): identical to normal play — first wins \(\iff x \neq 0\).
- If \(M \le 1\): flip vs normal — first wins \(\iff x = 0\).

When all heaps are \(0/1\), \(x\) is the parity of the number of size-\(1\) heaps; the flip says first wins on even count (including \(0\) heaps: first cannot move and loses under the usual “no move” reading paired with this formula — match the statement’s terminal rule).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(k)\)
- Total: \(O(k)\)
- Memory: \(O(1)\)`

### C++17 Template

```cpp
namespace misere_nim {
  // true = first wins; misère standard Nim (last move loses)
  bool first_wins(const vector<long long>& a) {
    long long x = 0, mx = 0;
    for (long long v : a) {
      x ^= v;
      mx = max(mx, v);
    }
    if (mx > 1) return x != 0;
    return x == 0; // flip of normal when all heaps size <= 1
  }
}
```

### Python 3 Template

```python
def misere_nim_first_wins(a: list[int]) -> bool:
    x = 0
    mx = 0
    for v in a:
        x ^= v
        mx = max(mx, v)
    if mx > 1:
        return x != 0
    return x == 0
```

---

## 6. Recognition Trigger Signals & Heuristics

- Explicit “player who takes the last stone loses” / “misère”
- Otherwise standard multi-heap Nim
- Heaps can be large — do **not** only special-case \(n=1\)

---

## 7. Contest WA / TLE / RE Traps

- Flipping XOR for **all** positions (wrong when some heap \(> 1\))
- Confusing “cannot move loses” vs “last move loses” wording — read statement
- General misère SG (not just Nim) — **no** simple XOR formula
- Heap size \(0\) cluttering counts

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

- **Misère subtraction** on one pile: period changes; often DP
- **Misère Kayles** etc.: hard; usually DP on small \(n\) only
- “Last loses” on a **single** pile: first wins iff \(n \neq 1\) (or \(n=0\) edge)

---

## 11. Typical Problem Archetypes

1. Standard application: multi-heap misère Nim who-wins
2. Slightly disguised: “poisoned” last stone / hot potato stone
3. Difficult: misère + non-standard moves → fall back to DP, not this theorem
4. Very difficult / advanced: general misère analysis (rarely needed)

---

## 12. Recognition & Identification Drills

1. Heaps \([1,1,1]\), last move loses — who wins?
2. Heaps \([3,1,1]\), last move loses — who wins?
3. Same as Nim but the player forced to take the final stone loses; \(t\) test cases.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: classic Nim + last move loses
- Key invariant: XOR, except flip when \(\max\le 1\)
- Key formula: `mx>1 ? xor!=0 : xor==0`
- Complexity: \(O(k)\)
- Template to remember: Bouton + single `if (max <= 1) flip`

---

---
