# Classical Matroid Archetypes in CP

> **Section:** §19 Greedy Fundamentals & Invariants  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

* $E$: Any set of $n$ elements.
* $\mathcal{I} = \{S \subseteq E \mid |S| \le k\}$.
* *Problem Context:* "Pick at most $k$ elements to maximize sum."

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Greedy Fundamentals establish formal proof techniques and data structure invariants for greedy optimization: Exchange Arguments, Stays-Ahead Invariants, and Priority Queue Regret / Undo Maintenance.

### Fundamental Theorems & Invariants

- **Exchange Argument Theorem:** To prove greedy sorting criteria $A < B$ is optimal, assume an optimal solution violates the order. Show that swapping adjacent out-of-order elements cannot worsen the objective function.
- **Smith's Rule for Scheduling:** When scheduling $N$ jobs with processing time $p_i$ and weight $w_i$ to minimize weighted completion time $\sum w_i C_i$, sorting in descending order of $\frac{w_i}{p_i}$ is strictly optimal.
- **Regret / Undo Heap Invariant:** When choices cannot be verified greedily upfront, accept the current greedy choice optimistically; if constraints are violated later, undo the worst prior choice by popping from a priority queue.

### Algorithmic Execution Blueprint

1. **Deriving Exchange Condition:** Write objective for pair $(i, j)$ in order $i$ then $j$ vs $j$ then $i$. Cancel common terms to isolate sorting comparator `return w[i] * p[j] > w[j] * p[i]`.
2. **Regret Heap (e.g. Potions):** Iterate through events; add current item. If health becomes negative, pop and reverse the effect of the most punishing past item from `priority_queue`.

### Closed-Form Invariant Equations

$$\text{Exchange Condition}: \quad \text{Cost}(i, j) \le \text{Cost}(j, i) \iff \frac{w_i}{p_i} \ge \frac{w_j}{p_j}$$

### Structural Edge Cases & Assumptions

- Comparators passed to `std::sort` must satisfy Strict Weak Ordering ($a < a$ must return `false`).
- Greedy exchange arguments require pairwise independence; if choice $i$ alters the available choices for subsequent elements non-linearly, DP or flows are required.

---

## 3. Core Intuition & Problem Framing

* $E$: Edges of an undirected graph $G = (V, E)$.
* $\mathcal{I}$: Subsets of edges that contain **no cycles** (forests).
* *Bases:* Spanning forests (or Spanning Trees if $G$ is connected).
* *Circuits:* Simple cycles.
* *Greedy Algorithm:* **Kruskal's Algorithm**. Kruskal is literally the Rado-Edmonds greedy algorithm on a Graphic Matroid.

---

## 4. Proof Sketches & Recurrences

* $E$ is partitioned into disjoint categories: $E = B_1 \sqcup B_2 \sqcup \dots \sqcup B_k$.
* Bounds $d_1, d_2, \dots, d_k$ for each category.
* $\mathcal{I} = \{S \subseteq E \mid |S \cap B_i| \le d_i \text{ for all } i\}$.
* *Problem Context:* "Select items of various categories, taking at most $d_i$ items of category $i$."

---

---

## 6. Recognition Trigger Signals & Heuristics

- $E$: A set of vectors over a field $\mathbb{F}$ (e.g., $\mathbb{F}_2$ for XOR).
- $\mathcal{I}$: Subsets of vectors that are **linearly independent**.
- Circuits:* Minimally linearly dependent sets of vectors.
- Greedy Algorithm:* **XOR Linear Basis** (Gaussian elimination over $\mathbb{F}_2$).

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1526C2 | Potions (Hard Version) | 1600 | Regret Heap, Greedy Invariants | Regret / Undo Heap: greedily drink potion; if health < 0, pop and un-drink the most negative potion. | [Solve Problem](https://codeforces.com/contest/1526/problem/C2) |
| Codeforces | CF-864D | Make a Permutation! | 1600 | Greedy, Frequencies | Greedy choice with frequency counters and skip-if-first-occurrence flags. | [Solve Problem](https://codeforces.com/contest/864/problem/D) |
| Codeforces | CF-1157C2 | Increasing Subsequence (hard version) | 1700 | Greedy, Two Pointers | Greedy two-pointer picks smaller side; if equal, simulate strictly longest run on both sides. | [Solve Problem](https://codeforces.com/contest/1157/problem/C2) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Greedy Exchange Arguments (Errichto)](https://codeforces.com/blog/entry/66734)
- **[USACO Guide]** [USACO Guide: Priority Queue Regret / Undo Heaps](https://usaco.guide/silver/greedy-sorting)

---
