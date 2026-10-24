# The Mathematical Origin of WQS Binary Search

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** S-tier in Grandmaster/IOI contests | **Rating Range:** 1600–2200 | **Frequency:** Essential for high-tier CF (2200–2600+)  
> **Prerequisites:** Convexity/concavity, binary search on real/integer slopes, standard DP  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier in Grandmaster/IOI contests
- Frequency: Essential for high-tier CF (2200–2600+)
- Core Superpower: **Removes an entire dimension** from DP state (e.g., $O(N K)$ becomes $O(N \log V)$)
- Prerequisites: Convexity/concavity, binary search on real/integer slopes, standard DP

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

Suppose we wish to solve:
$$\min_{x \in \mathcal{X}, \, \text{count}(x) = K} \text{cost}(x)$$
Let $F(k)$ be the minimum cost achieved using **exactly $k$ items**. 
Computing $F(K)$ directly typically requires storing the count $k \in [0, K]$ in the DP state, yielding $O(N K)$ time. When $N, K \le 10^5$, this TLEs.

---

## 4. Proof Sketches & Recurrences

Plot the points $(k, F(k))$ in the Cartesian plane:
1. The line $y = -\lambda k + c$ has slope $-\lambda$ and $y$-intercept $c$.
2. Finding $\min_k (F(k) + \lambda k)$ is equivalent to finding the line of slope $-\lambda$ that touches the lower boundary of the point set from below.
3. The point of tangency $(k^*, F(k^*))$ gives:
   - $k^* = \arg\min_k (F(k) + \lambda k)$
   - $c^* = g(\lambda) = F(k^*) + \lambda k^*$
4. If $F(k)$ is **strictly convex** (the slopes between consecutive points $F(k+1) - F(k)$ are strictly increasing):
   - Higher $\lambda \implies$ higher penalty per item $\implies$ fewer items chosen ($k^*$ decreases).
   - Lower $\lambda \implies$ lower penalty per item $\implies$ more items chosen ($k^*$ increases).
5. Because $k^*(\lambda)$ is **monotone** with respect to $\lambda$, we can **binary search for the optimal slope $\lambda^*$** that forces $k^*(\lambda^*) = K$!
6. Once $\lambda^*$ is found, the true answer is recovered in $O(1)$:
   $$F(K) = g(\lambda^*) - \lambda^* \cdot K$$

```
   F(k) ^
        |        (1, F(1))
        |          \
        |           \    (2, F(2))  <- Tangent point where slope = -lambda
        |            \___/
        |                \___ (3, F(3))
        |                    \___
        |                        (4, F(4))
        +-----------------------------------> k
```

---

## 2. Dealing with Collinear Points & Tie-Breaking (LIP)

---

## 6. Recognition Trigger Signals & Heuristics

- Instead of forcing $\text{count}(x) = K$, we introduce a cost **penalty $\lambda$** per item chosen and solve the **unconstrained problem**:
$$g(\lambda) = \min_{x \in \mathcal{X}} \big( \text{cost}(x) + \lambda \cdot \text{count}(x) \big)$$
In terms of the function $F(k)$:
$$g(\lambda) = \min_{k} \big( F(k) + \lambda \cdot k \big)$$

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
