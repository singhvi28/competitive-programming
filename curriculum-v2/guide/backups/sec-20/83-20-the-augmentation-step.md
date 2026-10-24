# The Augmentation Step

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

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

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — Generic Matroid Intersection Engine
#include <bits/stdc++.h>
using namespace std;

template <typename Matroid1, typename Matroid2>
vector<int> matroid_intersection(int n, Matroid1& m1, Matroid2& m2) {
    vector<int> I;
    vector<bool> in_I(n, false);

    while (true) {
        vector<int> X1, X2;
        vector<vector<int>> adj(n);

        // 1. Identify Sources (X1) and Sinks (X2)
        for (int y = 0; y < n; ++y) {
            if (in_I[y]) continue;
            if (m1.can_add(I, y)) X1.push_back(y);
            if (m2.can_add(I, y)) X2.push_back(y);
        }

        // 2. Build Exchange Graph Edges
        for (int x : I) {
            vector<int> I_minus_x;
            for (int elem : I) if (elem != x) I_minus_x.push_back(elem);

            for (int y = 0; y < n; ++y) {
                if (in_I[y]) continue;
                // M1 edge: y -> x
                if (m1.can_add(I_minus_x, y)) adj[y].push_back(x);
                // M2 edge: x -> y
                if (m2.can_add(I_minus_x, y)) adj[x].push_back(y);
            }
        }

        // 3. BFS Shortest Path from X1 to X2
        vector<int> parent(n, -1);
        queue<int> q;
        for (int src : X1) {
            q.push(src);
            parent[src] = src;
        }

        int target = -1;
        vector<bool> is_sink(n, false);
        for (int snk : X2) is_sink[snk] = true;

        while (!q.empty() && target == -1) {
            int u = q.front(); q.pop();
            if (is_sink[u]) {
                target = u;
                break;
            }
            for (int v : adj[u]) {
                if (parent[v] == -1) {
                    parent[v] = u;
                    q.push(v);
                }
            }
        }

        if (target == -1) break; // Maximum independent set reached

        // 4. Augment along the shortest path
        int curr = target;
        while (true) {
            in_I[curr] = !in_I[curr];
            if (curr == parent[curr]) break;
            curr = parent[curr];
        }

        I.clear();
        for (int i = 0; i < n; ++i) {
            if (in_I[i]) I.push_back(i);
        }
    }
    return I;
}
```

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
