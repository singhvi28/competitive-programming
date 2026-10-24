# Section §16: Game Theory & Sprague-Grundy

> **Module ID:** `sec-16`  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Topic Count:** 7  

**Module Summary:** Impartial games, Nim-sum XOR, Sprague-Grundy theorem with MEX transitions, Game graph DAG DP, and Misere Nim modifications.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Nim](#topic-1) | `A-tier` | 1400–2000 | Occasional | [01-16-nim.md](./01-16-nim.md) |
| 2 | [Sprague-Grundy theorem](#topic-2) | `A-tier` | 1700–2300 | Occasional | [02-16-sprague-grundy-theorem.md](./02-16-sprague-grundy-theorem.md) |
| 3 | [Grundy numbers](#topic-3) | `A-tier` | 1700–2400 | Occasional | [03-16-grundy-numbers.md](./03-16-grundy-numbers.md) |
| 4 | [Misère Nim](#topic-4) | `C-tier` | 1800–2400 | Rare | [04-16-mis-re-nim.md](./04-16-mis-re-nim.md) |
| 5 | [Game DP](#topic-5) | `A-tier` | 1500–2200 | Common | [05-16-game-dp.md](./05-16-game-dp.md) |
| 6 | [Symmetry and Strategy-Stealing](#topic-6) | `B-tier` | 1700–2600 | Occasional | [06-16-symmetry-and-strategy-stealing.md](./06-16-symmetry-and-strategy-stealing.md) |
| 7 | [Invariants and Colouring](#topic-7) | `B-tier` | 1800–2500 | Occasional | [07-16-invariants-and-colouring.md](./07-16-invariants-and-colouring.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Nim

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Occasional  
> **Prerequisites:** XOR, impartial games (normal play: last move wins)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: XOR, impartial games (normal play: last move wins)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

A Nim heap of size \(n\) under normal play is completely described by \(n\) itself as its “nimber.” Multiple heaps combine by **XOR**: the position is losing iff the XOR of all heap sizes is \(0\). Intuition: any move that changes one heap can be answered to restore XOR \(0\) when the opponent left XOR \(\neq 0\); from XOR \(0\), every move breaks the balance.

---

#### 4. Proof Sketches & Recurrences

- Single heap \(n\): first wins iff \(n > 0\) (take all).
- Two heaps \(a,b\): first wins iff \(a \neq b\) (equalize).
- Inductive: \(P\)-position (previous-player wins / second-player wins) iff all moves go to \(N\)-positions.
- Bouton’s theorem: \(P\)-positions \(\iff a_1 \oplus a_2 \oplus \cdots \oplus a_k = 0\).
- Winning move from \(x = a_1\oplus\cdots\oplus a_k \neq 0\): pick heap \(a_i\) with high bit of \(x\) set; set \(a_i' = a_i \oplus x\) (then \(a_i' < a_i\)).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(k)\) for \(k\) heaps
- Total: \(O(k)\)
- Memory: \(O(1)\) extra`

##### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace nim {
  // returns true if first player wins (normal play)
  bool first_wins(const vector<long long>& a) {
    long long x = 0;
    for (long long v : a) x ^= v;
    return x != 0;
  }

  // one winning move (heap index, new size); assumes first_wins
  pair<int, long long> winning_move(const vector<long long>& a) {
    long long x = 0;
    for (long long v : a) x ^= v;
    for (int i = 0; i < (int)a.size(); ++i) {
      if ((a[i] ^ x) < a[i]) return {i, a[i] ^ x};
    }
    return {-1, -1}; // XOR was 0
  }
}
```

##### Python 3 Template

```python
def nim_first_wins(a: list[int]) -> bool:
    x = 0
    for v in a:
        x ^= v
    return x != 0

def nim_winning_move(a: list[int]) -> tuple[int, int]:
    x = 0
    for v in a:
        x ^= v
    for i, v in enumerate(a):
        if (v ^ x) < v:
            return i, v ^ x
    return -1, -1
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “\(n\) piles of stones; remove any positive number from a single pile”
- “Kayles-like” statement that *is* standard Nim after rephrasing (one pile only)
- Multiplicative / stone games that reduce to independent heaps with remove-any
- Output “who wins” with perfect play, last move wins, no other coupling

---

#### 7. Contest WA / TLE / RE Traps

- Using `+` or `max` instead of XOR
- Misère rules silently applied (last loses) while coding normal Nim
- 32-bit overflow on heap sizes (use 64-bit)
- “Remove from *one or more* piles in one turn” → not standard Nim

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Subtraction game** on one pile (remove from fixed set \(S\)): period / Grundy, not raw size
- **Nim with limited removals** per pile: Grundy per pile then XOR
- **“Staircase Nim” / moving stones left**: XOR of odd-indexed piles (or even — check convention)

---

#### 11. Typical Problem Archetypes

1. Standard application: multi-heap Nim, print First/Second
2. Slightly disguised: game on arrays where each index is an independent heap
3. Difficult: find lexicographically smallest winning move / count winning moves
4. Very difficult / advanced: Nim on graphs / turning turtles / Staircase Nim reductions

---

#### 12. Recognition & Identification Drills

1. \(k\) piles; remove any positive count from exactly one pile; last move wins. Who wins?
2. Same rules, but also output any winning first move if one exists.
3. Stones on a path; a move shifts a stone left onto empty cells — reduce and decide winner.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: independent heaps, remove any from one heap, normal play
- Key invariant: XOR of heap sizes
- Key formula: first wins \(\iff \bigoplus a_i \neq 0\)
- Complexity: \(O(k)\)
- Template to remember: `x ^= a[i]; return x != 0`

---

---


---

<a id="topic-2"></a>
### 2. Sprague-Grundy theorem

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** Impartial games, mex, Nim XOR, notion of game sum  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: Impartial games, mex, Nim XOR, notion of game sum

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

Any impartial game under normal play is **equivalent to a single Nim heap** whose size is the game’s Grundy number. The **sum** of games (move in exactly one component) has Grundy equal to the **XOR** of component Grundies. So: break the board into independent pieces → compute \(g\) each → XOR → nonzero means first wins.

---

#### 4. Proof Sketches & Recurrences

- Define \(g(G) = \operatorname{mex}\{ g(G') : G \to G' \}\), \(\operatorname{mex} S = \min\{ n \ge 0 : n \notin S \}\).
- Prove by induction: \(G\) is \(P\)-position \(\iff g(G)=0\).
- Sum \(G+H\): moves to \(G'+H\) or \(G+H'\); set of reachable Grundies forces \(g(G+H)=g(G)\oplus g(H)\).
- Hence overall first-win \(\iff g_1 \oplus \cdots \oplus g_m \neq 0\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: cost of computing all needed \(g\) (problem-specific)
- Per-query / per-operation: \(O(m)\) XOR over \(m\) components
- Total: dominated by Grundy DP
- Memory: store \(g\) table for states`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Board splits into disjoint regions after a move style that never couples them
- “Several piles / strips / subgraphs; move affects only one”
- Editorial keywords: mex, nimber, SG, “replace with smaller games”
- Not one shared resource / not partizan (both players same moves)

---

#### 7. Contest WA / TLE / RE Traps

- Applying SG to **partizan** games (different moves for Left/Right)
- Forgetting the game is a **sum** (must move in exactly one component)
- Computing win/lose boolean instead of full Grundy when sums appear later
- mex off-by-one / not clearing `seen[]`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Selective compounds** (move in all / some components): different combination rules — not plain XOR
- **Misère** sums: SG fails in general; only special cases (see Misère Nim)
- **Graph games** (node Kayles, subtraction on graphs): SG on graph state or on components after splits

---

#### 11. Typical Problem Archetypes

1. Standard application: several piles with custom remove sets; XOR of per-pile Grundy
2. Slightly disguised: cutting a chocolate / splitting a strip into two independent games
3. Difficult: games that split into 2+ components — \(g = \operatorname{mex}\) over \(g(A)\oplus g(B)\)
4. Very difficult / advanced: SG on large DAGs with memoized hashing of states

---

#### 12. Recognition & Identification Drills

1. Three independent subtraction piles with set \(S=\{1,3,4\}\); who wins from \((5,7,2)\)?
2. A move splits one strip into two strips; game is sum of strips thereafter.
3. Multiple connected components on a graph; a move deletes a vertex in one component only.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: impartial, normal play, position = sum of independent games
- Key invariant: \(g(\text{sum})=\bigoplus g_i\)
- Key formula: first wins \(\iff \bigoplus g_i \neq 0\)
- Complexity: XOR \(O(m)\) after computing \(g\)
- Template to remember: compute \(g\) per component → XOR

---

---


---

<a id="topic-3"></a>
### 3. Grundy numbers

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1700–2400 | **Frequency:** Occasional  
> **Prerequisites:** mex, memoized DP on game graph, Sprague–Grundy  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2400
- Prerequisites: mex, memoized DP on game graph, Sprague–Grundy

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

Grundy number \(g(v)\) is the **nimber** of position \(v\): the smallest nonnegative integer not appearing among successors. It is DP on the DAG of positions (or memoized recursion). For a single pile/game you often need the full table \(g[0..n]\); for SG sums you only need \(g\) of each piece.

---

#### 4. Proof Sketches & Recurrences

\[
g(v)=\operatorname{mex}\{ g(u) : v \to u \}
\]
- Terminal (no moves): \(g=0\) (\(P\)-position).
- Subtraction \(\{s\}\) on pile \(n\): \(g(n)=\operatorname{mex}\{g(n-s): s\in S, s\le n\}\); often eventually periodic.
- Split move \(n \to (a)+(b)\) with \(a+b=n\): \(g(n)=\operatorname{mex}\{ g(a)\oplus g(b) \}\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n \cdot |S|)\) typical for pile DP; or \(O(|V|+|E|)\) on explicit game graph
- Per-query / per-operation: \(O(1)\) lookup after table
- Total: as above
- Memory: \(O(n)\) or \(O(|V|)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Compute who wins” but piles have **restricted** removals / merges / splits
- Need to combine many small games → must output numbers, not just W/L
- Positions form a DAG (moves decrease a potential: size, mask popcount, etc.)
- Statement asks for Grundy / “equivalent Nim heap”

---

#### 7. Contest WA / TLE / RE Traps

- Not memoizing → exponential blowup
- Using W/L (`bool`) when later XOR composition needs full \(g\)
- Incorrect move generation (missing split → two-game XOR in mex set)
- Assuming periodicity without verifying period for given \(S\)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Mask / grid Grundy**: state = bitset or pair; hash memo
- **Graph Nim / Kayles**: \(g\) on induced subgraphs (often \(2^n\) or component DP)
- **Optional pass / limited piles**: still mex, different edges

---

#### 11. Typical Problem Archetypes

1. Standard application: subtraction / Euclidean-like pile; table \(g[0..n]\)
2. Slightly disguised: string / binary string moves; state compress to int
3. Difficult: move splits into two independent games; mex of XORs
4. Very difficult / advanced: Grundy on trees/paths with deletion; combine SG over forest

---

#### 12. Recognition & Identification Drills

1. Pile \(n\); remove \(2^k\) stones only. Build \(g[0..n]\) and decide multi-pile winner.
2. Chomp on a \(1 \times n\) bar (equivalent to simple game) — compute Grundy of length.
3. Delete a vertex and adjacent edges on a path; remaining paths are a sum — define \(g\) of path length.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need nimber of a position / custom move set
- Key invariant: \(g=\operatorname{mex}\) of successor grundies
- Key formula: \(g(v)=\operatorname{mex}\{g(u)\}\) (or \(g(a)\oplus g(b)\) on splits)
- Complexity: DP on states
- Template to remember: memo + mex loop

---

---


---

<a id="topic-4"></a>
### 4. Misère Nim

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 1800–2400 | **Frequency:** Rare  
> **Prerequisites:** Normal Nim / Bouton, careful casework  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: Normal Nim / Bouton, careful casework

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

**Misère** = player who takes the last object **loses**. For standard Nim, Bouton’s XOR rule still works **unless** every heap has size at most \(1\) (and there is at least one heap). In that “all heaps \(\le 1\)” regime, the winner is the opposite of the normal-play winner (equivalently: first wins iff the number of heaps of size \(1\) is even — including the empty-all case carefully). Intuition: long heaps give enough “room” to mirror; when only singletons remain, the last-take-loses flips the count parity.

---

#### 4. Proof Sketches & Recurrences

Let \(x = \bigoplus a_i\), \(M = \max a_i\). Contest misère Nim = last player to move loses.
- If \(M > 1\): identical to normal play — first wins \(\iff x \neq 0\).
- If \(M \le 1\): flip vs normal — first wins \(\iff x = 0\).

When all heaps are \(0/1\), \(x\) is the parity of the number of size-\(1\) heaps; the flip says first wins on even count (including \(0\) heaps: first cannot move and loses under the usual “no move” reading paired with this formula — match the statement’s terminal rule).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(k)\)
- Total: \(O(k)\)
- Memory: \(O(1)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Explicit “player who takes the last stone loses” / “misère”
- Otherwise standard multi-heap Nim
- Heaps can be large — do **not** only special-case \(n=1\)

---

#### 7. Contest WA / TLE / RE Traps

- Flipping XOR for **all** positions (wrong when some heap \(> 1\))
- Confusing “cannot move loses” vs “last move loses” wording — read statement
- General misère SG (not just Nim) — **no** simple XOR formula
- Heap size \(0\) cluttering counts

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Misère subtraction** on one pile: period changes; often DP
- **Misère Kayles** etc.: hard; usually DP on small \(n\) only
- “Last loses” on a **single** pile: first wins iff \(n \neq 1\) (or \(n=0\) edge)

---

#### 11. Typical Problem Archetypes

1. Standard application: multi-heap misère Nim who-wins
2. Slightly disguised: “poisoned” last stone / hot potato stone
3. Difficult: misère + non-standard moves → fall back to DP, not this theorem
4. Very difficult / advanced: general misère analysis (rarely needed)

---

#### 12. Recognition & Identification Drills

1. Heaps \([1,1,1]\), last move loses — who wins?
2. Heaps \([3,1,1]\), last move loses — who wins?
3. Same as Nim but the player forced to take the final stone loses; \(t\) test cases.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: classic Nim + last move loses
- Key invariant: XOR, except flip when \(\max\le 1\)
- Key formula: `mx>1 ? xor!=0 : xor==0`
- Complexity: \(O(k)\)
- Template to remember: Bouton + single `if (max <= 1) flip`

---

---


---

<a id="topic-5"></a>
### 5. Game DP

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1500–2200 | **Frequency:** Common  
> **Prerequisites:** DP / memoization, recursion on states, win-lose definitions  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1500–2200
- Prerequisites: DP / memoization, recursion on states, win-lose definitions

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

When the position is **one coupled state** (not a tidy sum of heaps), compute directly: a position is losing iff **all** moves lead to a winning position for the opponent (or no moves — usually lose under normal play). Optionally DP the **best score** under optimal play (minimax). Use SG only when you need composition; use Game DP when the whole game is one DP.

---

#### 4. Proof Sketches & Recurrences

- Normal play W/L: \(\mathrm{win}(v)=\exists u{\leftarrow}v:\neg\mathrm{win}(u)\); \(\mathrm{win}(\text{terminal})=\bot\).
- Score: \(\mathrm{dp}(v)=\operatorname{opt}_{u} \mathrm{value}(v\to u)+\mathrm{dp}(u)\) with alternating max/min or “current player maximizes own score.”
- Interval games (take ends of array): \(dp[l][r]\) = best for player to move on \(a[l..r]\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(|\text{states}| \cdot |\text{moves}|)\)
- Total: problem-specific (often \(O(n^2)\) intervals, \(O(2^n n)\) masks)
- Memory: \(O(|\text{states}|)\)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Shared board / one array / one number that both alter
- “Both play optimally; maximize score / difference”
- States small enough: \(n \le 10^3\) with \(O(n^2)\), masks \(2^n\), interval DP
- No clean split into independent impartial components

---

#### 7. Contest WA / TLE / RE Traps

- Wrong terminal: empty moves → lose (normal) vs score \(0\)
- Alternating players but coding both as maximizers without negate/diff trick
- Recursion depth on deep chains — prefer iterative bottoms-up when DAG is sized
- Using SG XOR on a **non**-sum game

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Grundy via game DP**: same recursion but mex instead of bool
- **Partizan / different move sets**: still DP; no SG
- **Probability / expected value games**: DP expectations

---

#### 11. Typical Problem Archetypes

1. Standard application: subtract a square; win/lose DP on \(n\)
2. Slightly disguised: take 1..m from a pile; or stone piles with shared rules
3. Difficult: interval DP take from ends; optimal score
4. Very difficult / advanced: game on graphs with state compression / pairing strategy DP

---

#### 12. Recognition & Identification Drills

1. Starting from \(n\); subtract a positive perfect square; last move wins.
2. Array of coins; each turn take leftmost or rightmost; maximize own sum.
3. Shared matrix; players color cells with constraints; decide winner with small \(n\).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: single coupled position / scoring; states enumerable
- Key invariant: win iff exists move to lose for opponent
- Key formula: \(\mathrm{win}(v)=\exists u:\neg\mathrm{win}(u)\)
- Complexity: DP on state graph
- Template to remember: memoized `any(not win(u))`

---

---


---

<a id="topic-6"></a>
### 6. Symmetry and Strategy-Stealing

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1700–2600 | **Frequency:** Occasional  
> **Prerequisites:** Combinatorial game basics, proof-oriented thinking, ad-hoc  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2600
- Prerequisites: Combinatorial game basics, proof-oriented thinking, ad-hoc

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

In perfectly symmetric games, the Second Player often has a dominant **Mirroring** strategy. 
- **Classic Example:** Placing non-overlapping coins on a circular table. The First Player places a coin in the exact center. From then on, the First Player just mirrors the Second Player's moves diametrically opposite. Because of symmetry, whenever the Second player finds a valid spot, the First player is guaranteed to find its symmetric counterpart empty.
- **Bipartite Graphs:** If the game is played on a graph with a perfect matching, and you can always move along the matched edge, you win.
- **Strategy-Stealing:** Used to prove the First Player wins without exhibiting the strategy. E.g., Chomp. First player makes a harmless "null" move. If the Second player had a winning strategy, the First player steals it. Since someone must win (no draws), the First player wins.

---

#### 4. Proof Sketches & Recurrences

Sketch (Chomp-style):
1. Position is finite, deterministic, perfect information, no draw → someone wins.
2. Second-player win assumption ⇒ strategy \(S\).
3. First takes a “neutral” bite; thereafter answers with \(S\); if \(S\) asks for the already-taken cell, take another neutral and continue.
4. Contradiction because \(S\) would also win for first → first wins.
Mirroring: on symmetric graphs, second copies across automorphism unless first breaks symmetry (then steal).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: —
- Per-query / per-operation: \(O(1)\) mirror reply when constructive
- Total: proof \(O(1)\) insight; code only for pairing simulation
- Memory: \(O(n)\) for pairs`

##### C++17 Template

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

##### Python 3 Template

```python
def mirror_reply(move: int, n: int) -> int:
    # 1-indexed circle / array mirror example
    return n + 1 - move
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “Prove first player wins” in math/ICPC theory problems
- Symmetric boards where extra move cannot hurt
- Mirror / pairing strategies as the **constructive** twin of stealing
- Chomp, positional games, maker-breaker intuition questions

---

#### 7. Contest WA / TLE / RE Traps

- Treating stealing as an implementable DP
- Broken symmetry: mirror fails when center cell / odd dimension not handled
- Assuming draws impossible when the rules allow draws
- Using stealing on **partizan** games incorrectly

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Pairing strategy** (second player): block all threats via fixed pairs
- **Mirroring** on symmetric graphs / centrals
- **Strategy stealing + extra pawn**: “null move” harmless in monotone games

---

#### 11. Typical Problem Archetypes

1. Standard application: prove first wins at Chomp / similar (theory)
2. Slightly disguised: constructive mirror on symmetric pile/board CF task
3. Difficult: design a pairing that blocks all winning configurations
4. Very difficult / advanced: maker-breaker positional games criteria

---

#### 12. Recognition & Identification Drills

1. Chomp on \(2\times n\); argue who wins without listing all states.
2. Symmetric game on a path; second mirrors across center — when does this work?
3. Prove that an extra isolated winning token cannot hurt the player who “owns” a stolen strategy.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: existence proofs; or constructive mirror/pairing
- Key invariant: extra move does not hurt in monotone claiming games
- Key formula: none algorithmic — contradiction via stolen \(S\)
- Complexity: insight / \(O(1)\) mirror
- Template to remember: assume second wins → steal \(S\); else code pairing

---


---

---


---

<a id="topic-7"></a>
### 7. Invariants and Colouring

> **Section:** §16 Game Theory & Sprague-Grundy  
> **Phase:** Phase 8 — Game Theory, Geometry & Meta-Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1800–2500 | **Frequency:** Occasional  
> **Prerequisites:** Parity, Chessboard coloring, Ad-hoc logic  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2500
- Prerequisites: Parity, Chessboard coloring, Ad-hoc logic

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Game Theory models impartial games under normal play convention using Nim games, XOR invariants, the Sprague-Grundy Theorem, and DAG Game State DP.

##### Fundamental Theorems & Invariants

- **Bouton's Theorem for Nim:** In a game of Nim with heaps $x_1, x_2, \dots, x_k$, a position is a losing P-position (second player wins) if and only if $x_1 \oplus x_2 \oplus \dots \oplus x_k = 0$.
- **Sprague-Grundy Theorem:** Every impartial game played under normal play convention is isomorphic to a single Nim heap of size $G(v)$, where $G(v) = \text{MEX}\big(\{G(u) : v \to u\}\big)$.
- **Misère Play Modification:** In Misère Nim (last to move loses), play with standard Sprague-Grundy XOR sum until all remaining heaps have size $\le 1$. If all heaps have size $\le 1$, the winning condition flips: first player wins if and only if the number of heaps of size 1 is even.

##### Algorithmic Execution Blueprint

1. **Compute Grundy Numbers:** For game state $v$, recursively compute $G(u)$ for all valid next states $u$. Compute $G(v) = \min\{k \ge 0 : k \notin \{G(u)\}\}$.
2. **Independent Games Sum:** The Grundy value of a composite game consisting of independent sub-games $G_1, G_2, \dots$ is $G_{total} = G_1 \oplus G_2 \oplus \dots$.

##### Closed-Form Invariant Equations

$$G(v) = \text{MEX}\Big(\{G(u) \mid v \to u\}\Big), \quad G(A + B) = G(A) \oplus G(B)$$

##### Structural Edge Cases & Assumptions

- Sprague-Grundy theorem applies strictly to impartial games (both players have identical allowed moves) without cycles and under normal play convention.
- When computing MEX, ensure visited markers are cleared or use an incrementing timestamp array to achieve $\mathcal{O}(\text{deg}(v))$ complexity.

---

#### 3. Core Intuition & Problem Framing

Some games cannot be solved by DP (state space too large) and are not Nim (no independent subgames). Instead, they are solved by finding a property that remains unchanged (**Invariant**) or predictably changes (**Monovariant**) after every valid move.
- **Parity / Chessboard Colouring:** E.g., A knight moving on a chessboard always changes the color of the square it is on. If the game ends on a specific square, you know exactly whose turn it will be based on the parity of the distance (Manhattan distance parity).
- **Domino Tiling Games:** If players place dominoes on a grid, coloring the grid like a chessboard reveals that every domino covers exactly one black and one white cell. This can reduce the game to finding maximum bipartite matchings.
- **Inversion Parity:** 15-puzzle style games. Sliding tiles preserves the parity of the number of inversions plus the row of the empty square. You can easily classify states as winning/losing or reachable/unreachable by checking this parity.

---

#### 4. Proof Sketches & Recurrences

To prove a strategy using invariants:
1. Identify a coloring scheme or mathematical parity.
2. Prove that a move by Player A *preserves* the invariant, or forces a specific parity.
3. Show that the terminal losing state has a different parity, meaning Player A can never be forced into it.

---

#### 5. Contest-Ready Implementation Templates

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

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Grid-based games where players move tokens.
- Games where a state undergoes localized flips or swaps.
- Proving a target state is unreachable (if the invariant differs from the start state).

---

#### 7. Contest WA / TLE / RE Traps

- Assuming an invariant is sufficient: invariant equality $I(A) = I(B)$ proves that transition is NOT IMPOSSIBLE, but does not always guarantee reachability without a constructive proof.
- Grid coordinate parity off-by-one: 0-indexed vs 1-indexed $(r + c) \pmod 2$.
- Missing monovariant lower bounds: assuming a quantity decreases without bounding it from below.
- Ignoring moves that temporarily increase the invariant before stabilizing.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1383B | GameGame | 1900 | Game Theory, Bitwise Invariants | MSB parity invariant analysis; count ones and zeros at the highest differing bit. | [Solve Problem](https://codeforces.com/contest/1383/problem/B) |
| Codeforces | CF-768E | Game of Stones | 2100 | Sprague Grundy, MEX, Game DP | Compute Grundy numbers for state (x, mask of used moves) using MEX recursion. | [Solve Problem](https://codeforces.com/contest/768/problem/E) |
| CSES | CSES-1738 | Moving Robots | 1900 | Game DP, Probability | Probability and matrix transition game DP. | [Solve Problem](https://cses.fi/problemset/task/1738) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sprague-Grundy Theorem & Nim Games](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- **[USACO Guide]** [USACO Guide: Combinatorial Game Theory](https://usaco.guide/adv/game-theory)

---


---
