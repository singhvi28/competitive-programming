# What is Slope Trick?

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier (Turns $O(N^2)$ DP into $O(N \log N)$) | **Rating Range:** 1600–2200 | **Frequency:** Classic in Codeforces 2000–2600+  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (Turns $O(N^2)$ DP into $O(N \log N)$)
- Frequency: Classic in Codeforces 2000–2600+
- Core Concept: Tracking the **derivative / slope transitions** of a dynamic cost function rather than tabular values.

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Intermediate Greedy techniques bridge convex optimization and dynamic programming: Decoupled Dimension Sweeps, Slope Trick (piecewise linear convex function maintenance via priority queues), and WQS Binary Search (Alien's Trick).

### Fundamental Theorems & Invariants

- **Additive Independence & Chebyshev Transform:** In $\ell_1$ (Manhattan) and $\ell_\infty$ (Chebyshev) metrics, coordinate transformations $(x', y') = (x+y, x-y)$ decouple multi-dimensional distance minimization into independent 1D median problems.
- **Slope Trick Invariant:** Any continuous piecewise linear convex function $f(x)$ with integer slopes can be represented by its minimum value and two priority queues storing the inflection points where the slope changes by $+1$ and $-1$. Adding $|x - a|$ updates slope inflection points in $\mathcal{O}(\log N)$.
- **Alien's Trick / WQS Binary Search:** If the optimal value $OPT(k)$ as a function of choice count $k$ is strictly concave/convex, introducing a Lagrange multiplier penalty $\lambda$ removes the exact-count constraint, binary searching $\lambda$ in $\mathcal{O}(\text{BaseDP} \cdot \log(\text{Range})))$.

### Algorithmic Execution Blueprint

1. **Chebyshev Transformation:** Map each point $(x, y) \to (x+y, x-y)$. The maximum Chebyshev distance $\max(|x_1-x_2|, |y_1-y_2|)$ becomes $\frac{1}{2}(|x'_1-x'_2| + |y'_1-y'_2|)$.
2. **Slope Trick Maintenance:** Maintain left heap $L$ (max-heap) and right heap $R$ (min-heap). To add $|x - a|$: if $a < L.\text{top}()$, add cost $L.\text{top}() - a$, push $a$ twice to $L$, and move $L.\text{top}()$ to $R$.
3. **WQS Binary Search:** Binary search penalty $\lambda$. Run unconstrained DP where each selection costs $+\lambda$. If optimal selections count $> k$, increase $\lambda$.

### Closed-Form Invariant Equations

$$f_{new}(x) = f(x) + |x - a|, \quad \text{WQS}: \min_k \big(dp[k] - \lambda k\big) \iff \text{Lagrangian Duality}$$

### Structural Edge Cases & Assumptions

- Slope Trick requires the underlying objective function to be strictly convex; non-convex cost functions require general CHT or DP.
- In WQS Binary Search, collinear points (flat segments in the convex hull of $OPT(k)$) require careful tie-breaking (preferring max count or min count) to avoid binary search oscillation.

---

## 3. Core Intuition & Problem Framing

A function $f: \mathbb{R} \to \mathbb{R}$ is **continuous, piecewise linear, and convex** if:
1. It is composed of linear segments with integer slopes: $\dots, -3, -2, -1, 0, 1, 2, 3, \dots$.
2. The derivative (slope) $f'(x)$ is a **monotone non-decreasing step function**.
3. Because $f'(x)$ is non-decreasing, it is completely defined by the **locations of its step increases**.
4. By the Fundamental Theorem of Calculus:
   $$f(x) = f(x_0) + \int_{x_0}^x f'(t) \, dt$$
   Knowing the minimum value $f_{\min}$, the interval $[L, R]$ where $f'(x) = 0$, and the multiset of slope change locations completely determines the entire function $f(x)$ for all $x \in \mathbb{R}$!

---

## 6. Recognition Trigger Signals & Heuristics

- `L` (Max-Heap):** Contains points where the slope changes in $(-\infty, \text{min\_range\_left}]$. These define slopes $-1, -2, -3, \dots$ moving leftward.
- `R` (Min-Heap):** Contains points where the slope changes in $[\text{min\_range\_right}, \infty)$. These define slopes $+1, +2, +3, \dots$ moving rightward.
- `min_f`:** A scalar maintaining the minimum value $\min_{x} f(x)$.
- `off_L`, `off_R`:** Lazy horizontal shift offsets applied to all elements in $L$ and $R$.
- 

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-713C | Sonya and Problem Wihtout a Legend | 2300 | Slope Trick, Priority Queue, Convexity | Slope Trick with max-heap maintaining slope change points of convex cost function in O(N log N). | [Solve Problem](https://codeforces.com/contest/713/problem/C) |
| Codeforces | CF-1279F | New Year and Handle Change | 2600 | Aliens Trick, WQS Binary Search, DP | Aliens Trick / WQS binary search penalizing each operation by lambda. | [Solve Problem](https://codeforces.com/contest/1279/problem/F) |
| Codeforces | CF-1534E | Lost Array | 2300 | Greedy, BFS, Parity | Shortest path BFS over odd/even bit counts or balanced decoupled greedy assignment. | [Solve Problem](https://codeforces.com/contest/1534/problem/E) |

---

## 9. External Theory & Deep-Dive References

- **[Codeforces]** [Codeforces Blog: Slope Trick Tutorial (zscoder / SleepingCup)](https://codeforces.com/blog/entry/77298)
- **[Codeforces]** [Codeforces Blog: The Alien's Trick (WQS Binary Search / Lagrangian Relaxation)](https://codeforces.com/blog/entry/49691)

---
