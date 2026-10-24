# Decoupled Sweeps & Chebyshev-Manhattan Equivalence

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2300 | **Frequency:** Common in Div.1 A/B and Div.2 D/E  
> **Prerequisites:** Coordinate systems, prefix sums, sorting  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common in Div.1 A/B and Div.2 D/E
- Typical CF/ICPC rating range: 1900–2300
- Prerequisites: Coordinate systems, prefix sums, sorting

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

In $D$-dimensional optimization, problems often appear coupled because the objective function involves multiple variables simultaneously. However, if the objective function $F(x, y)$ can be algebraically partitioned into additive independent components:
$$F(x, y) = f(x) + g(y)$$
and the search space constraint domain is a Cartesian product $S = X \times Y$ (i.e., choosing $x$ does not restrict the valid choices for $y$), then:
$$\min_{(x, y) \in S} F(x, y) = \min_{x \in X} f(x) + \min_{y \in Y} g(y)$$
This reduces a $D$-dimensional search of size $O(N^D)$ into $D$ independent 1-dimensional searches of size $O(N)$.

---

## 4. Proof Sketches & Recurrences

```python
def solve_chebyshev_center(points):
    """
    Finds point (X, Y) minimizing sum of Chebyshev distances to all points.
    points: list of (x, y)
    """
    # Transform to Manhattan plane
    xs_prime = sorted([x + y for x, y in points])
    ys_prime = sorted([x - y for x, y in points])
    n = len(points)
    
    # In Manhattan plane, optimal point is the median of each axis
    med_x_prime = xs_prime[n // 2]
    med_y_prime = ys_prime[n // 2]
    
    # Transform back: x = (x' + y') / 2, y = (x' - y') / 2
    best_x = (med_x_prime + med_y_prime) / 2.0
    best_y = (med_x_prime - med_y_prime) / 2.0
    return best_x, best_y
```

```cpp
// C++17 — 2D Decoupled Manhattan Center
#include <bits/stdc++.h>
using namespace std;

long long min_manhattan_distance_sum(vector<pair<long long, long long>>& pts) {
    int n = pts.size();
    vector<long long> xs(n), ys(n);
    for (int i = 0; i < n; ++i) {
        xs[i] = pts[i].first;
        ys[i] = pts[i].second;
    }
    sort(xs.begin(), xs.end());
    sort(ys.begin(), ys.end());
    
    long long med_x = xs[n / 2];
    long long med_y = ys[n / 2];
    
    long long total_dist = 0;
    for (int i = 0; i < n; ++i) {
        total_dist += abs(xs[i] - med_x) + abs(ys[i] - med_y);
    }
    return total_dist;
}
```

---

## 2. 1D, 2D & Weighted Median Invariants

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — 2D Decoupled Manhattan Center
#include <bits/stdc++.h>
using namespace std;

long long min_manhattan_distance_sum(vector<pair<long long, long long>>& pts) {
    int n = pts.size();
    vector<long long> xs(n), ys(n);
    for (int i = 0; i < n; ++i) {
        xs[i] = pts[i].first;
        ys[i] = pts[i].second;
    }
    sort(xs.begin(), xs.end());
    sort(ys.begin(), ys.end());
    
    long long med_x = xs[n / 2];
    long long med_y = ys[n / 2];
    
    long long total_dist = 0;
    for (int i = 0; i < n; ++i) {
        total_dist += abs(xs[i] - med_x) + abs(ys[i] - med_y);
    }
    return total_dist;
}
```

### Python 3 Template

```python
def solve_chebyshev_center(points):
    """
    Finds point (X, Y) minimizing sum of Chebyshev distances to all points.
    points: list of (x, y)
    """
    # Transform to Manhattan plane
    xs_prime = sorted([x + y for x, y in points])
    ys_prime = sorted([x - y for x, y in points])
    n = len(points)
    
    # In Manhattan plane, optimal point is the median of each axis
    med_x_prime = xs_prime[n // 2]
    med_y_prime = ys_prime[n // 2]
    
    # Transform back: x = (x' + y') / 2, y = (x' - y') / 2
    best_x = (med_x_prime + med_y_prime) / 2.0
    best_y = (med_x_prime - med_y_prime) / 2.0
    return best_x, best_y
```

---

## 6. Recognition Trigger Signals & Heuristics

- When costs involve the maximum metric ($L_\infty$ or Chebyshev distance):
$$D_{\infty}((x_1, y_1), (x_2, y_2)) = \max(|x_1 - x_2|, |y_1 - y_2|)$$
the components are coupled by the $\max$ operator. We decouple them by rotating the coordinate axes by $45^\circ$ and scaling by $\sqrt{2}$:
$$(x', y') = (x + y, x - y)$$
Under this transformation, the Chebyshev distance in $(x, y)$ becomes the Manhattan distance ($L_1$) in $(x', y')$ divided by 2:
$$\max(|x_1 - x_2|, |y_1 - y_2|) = \frac{|(x_1 + y_1) - (x_2 + y_2)| + |(x_1 - y_1) - (x_2 - y_2)|}{2} = \frac{|x'_1 - x'_2| + |y'_1 - y'_2|}{2}$$
Now, $x'$ and $y'$ are completely additive and independent! We can sort $x'$ and $y'$ separately and solve with simple prefix sums or median sweeps.

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
