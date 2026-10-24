# When Multiple Counts Share the Same Optimal Tangency

> **Section:** §20 Greedy Intermediate (Slope Trick, WQS)  
> **Phase:** Phase 5 — Dynamic Programming & Advanced Greedy  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

If $F(k)$ is not strictly convex (i.e., several points $(k_1, F(k_1)), (k_2, F(k_2)), \dots$ are collinear with slope $-\lambda$), then for that exact $\lambda$:
$$F(k_1) + \lambda k_1 = F(k_2) + \lambda k_2 = \dots = g(\lambda)$$
The binary search may jump directly from $k < K$ to $k > K$ without ever hitting $k = K$ exactly.

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

1. In your `check(lambda)` function, when two choices have the same cost, consistently break ties by choosing the **maximum count** (or minimum count).
2. Because the points are collinear, the true value $F(K)$ lies on the straight line connecting $(k_{\min}, F(k_{\min}))$ and $(k_{\max}, F(k_{\max}))$.
3. The exact same recovery formula still holds:
   $$F(K) = g(\lambda) - \lambda \cdot K$$
   You **do not need to reconstruct the exact configuration of $K$ items**—the formula computes the exact mathematical value $F(K)$ on the line segment!

---

## 3. Reusable C++ WQS Template

```cpp
// C++17 — WQS Binary Search (Alien's Trick) Template
#include <bits/stdc++.h>
using namespace std;

struct Result {
    long long cost;
    int count;
};

// Solve unconstrained problem with penalty lambda per chosen element
Result check(long long lambda, const vector<long long>& a) {
    int n = a.size();
    // dp[i] = {min_cost, min_count_used}
    vector<pair<long long, int>> dp(n + 1, {0, 0});
    
    for (int i = 1; i <= n; ++i) {
        // Option 1: Do not pick
        dp[i] = dp[i - 1];
        
        // Option 2: Pick item i (costs a[i-1] + lambda)
        long long take_cost = dp[i - 1].first + a[i - 1] + lambda;
        int take_cnt = dp[i - 1].second + 1;
        
        if (take_cost < dp[i].first || (take_cost == dp[i].first && take_cnt > dp[i].second)) {
            dp[i] = {take_cost, take_cnt};
        }
    }
    return {dp[n].first, dp[n].second};
}

long long wqs_solve(int n, int K, const vector<long long>& a) {
    long long low = -1e14, high = 1e14;
    long long best_lambda = 0;
    
    while (low <= high) {
        long long mid = low + (high - low) / 2;
        Result res = check(mid, a);
        
        if (res.count >= K) {
            best_lambda = mid;
            low = mid + 1; // Increase penalty to reduce count
        } else {
            high = mid - 1; // Decrease penalty to increase count
        }
    }
    
    Result final_res = check(best_lambda, a);
    return final_res.cost - best_lambda * K;
}
```

---

## 4. Multi-Dimensional / Nested WQS Binary Search

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// C++17 — WQS Binary Search (Alien's Trick) Template
#include <bits/stdc++.h>
using namespace std;

struct Result {
    long long cost;
    int count;
};

// Solve unconstrained problem with penalty lambda per chosen element
Result check(long long lambda, const vector<long long>& a) {
    int n = a.size();
    // dp[i] = {min_cost, min_count_used}
    vector<pair<long long, int>> dp(n + 1, {0, 0});
    
    for (int i = 1; i <= n; ++i) {
        // Option 1: Do not pick
        dp[i] = dp[i - 1];
        
        // Option 2: Pick item i (costs a[i-1] + lambda)
        long long take_cost = dp[i - 1].first + a[i - 1] + lambda;
        int take_cnt = dp[i - 1].second + 1;
        
        if (take_cost < dp[i].first || (take_cost == dp[i].first && take_cnt > dp[i].second)) {
            dp[i] = {take_cost, take_cnt};
        }
    }
    return {dp[n].first, dp[n].second};
}

long long wqs_solve(int n, int K, const vector<long long>& a) {
    long long low = -1e14, high = 1e14;
    long long best_lambda = 0;
    
    while (low <= high) {
        long long mid = low + (high - low) / 2;
        Result res = check(mid, a);
        
        if (res.count >= K) {
            best_lambda = mid;
            low = mid + 1; // Increase penalty to reduce count
        } else {
            high = mid - 1; // Decrease penalty to increase count
        }
    }
    
    Result final_res = check(best_lambda, a);
    return final_res.cost - best_lambda * K;
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
