# 13. Edge-Cut Tree Component Splitting in $O((N + Q) \log N)$

> **Section:** §22 Line Sweep Algorithms & Reductions  
> **Phase:** Phase 1 — Range Queries & Sweeps  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

## 1. Contest Payoff & Why It Matters

Removing an edge $(u, v)$ (where $v$ is a child of $u$) splits a tree of $N$ nodes into two disjoint components:
1. **Component 1 (The Subtree of $v$):** Naturally forms contiguous interval $[in[v], out[v] - 1]$.
2. **Component 2 (The Rest of the Tree):** In a standard Euler tour, this fractures into two disjoint pieces: prefix $[0, in[v] - 1]$ and suffix $[out[v], N - 1]$.

```
Standard Euler Tour:
[ 0 ... in[v]-1 ] [ in[v] ... out[v]-1 ] [ out[v] ... N-1 ]
\_______________/ \____________________/ \________________/
   Prefix (Rest)       Subtree of v          Suffix (Rest)
```

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Line Sweep Algorithms reduce multi-dimensional spatial queries into dynamic 1D data structure operations: Event Sorting, Difference Arrays, 2D Fenwick Sweeps, Klee's Measure (Rectangle Union Area in $\mathcal{O}(N \log N)$), and Bentley-Ottmann Segment Intersections.

### Fundamental Theorems & Invariants

- **Dimensional Reduction Invariant:** Sorting geometric elements along a sweep axis $X$ transforms 2D static problems into a sequence of 1D updates and point/range queries on the active sweep line $Y$.
- **Klee's Measure Theorem:** The union area of $N$ axis-aligned rectangles is computed in $\mathcal{O}(N \log N)$ time by sweeping vertical edges on $X$ while maintaining active interval coverage lengths in a segment tree on $Y$.
- **Bentley-Ottmann Sweep Invariant:** All $K$ intersections among $N$ line segments are detected in $\mathcal{O}((N + K) \log N)$ time by maintaining the active $Y$-order of intersecting segments in a balanced binary search tree, checking only adjacent segments upon event transitions.

### Algorithmic Execution Blueprint

1. **Event Creation:** For rectangle $[x_1, x_2] \times [y_1, y_2]$, generate opening event at $x_1$ with weight $+1$ on interval $[y_1, y_2]$, and closing event at $x_2$ with weight $-1$.
2. **Segment Tree on Y:** Maintain `count[node]` (number of active covers) and `len[node]` (total length covered). If `count[node] > 0`, `len[node] = right - left`; else `len[node] = len[2*node] + len[2*node+1]`.
3. **Area Accumulation:** For consecutive events at $x_{i-1}$ and $x_i$, add `tree.len[root] * (x_i - x_{i-1})` to total area.

### Closed-Form Invariant Equations

$$\text{Area}(\bigcup R_i) = \sum_{i=1}^{2N-1} \text{ActiveLength}(Y, x_i) \cdot (x_{i+1} - x_i)$$

### Structural Edge Cases & Assumptions

- Coordinate compression on $Y$ coordinates must maintain interval segment lengths `compressed[y_{i+1}] - compressed[y_i]`, not single discrete points.
- In segment trees without lazy propagation for Klee's measure, never push tags down; instead evaluate coverage directly from `count[node]` and children lengths.

---

## 3. Core Intuition & Problem Framing

If we append the pre-order array to itself ($A + A$, length $2N$):
- Subtree of $v$: $[in[v], out[v] - 1]$
- Rest of the tree: Starts at $out[v]$ and wraps around of length $N - \text{subtree\_size}$, ending at $in[v] + N - 1$!
- **Both components become single contiguous subarrays in the doubled array!**

```
Doubled Euler Tour (Length 2N):
[ ... in[v] ... out[v] ... N-1 | 0 ... in[v]+N ... out[v]+N ... 2N-1 ]
               |_______________________|
               Rest of Tree: [out[v], in[v] + N - 1]
```

---

## 4. Proof Sketches & Recurrences

If edge deletions and additions are arbitrarily mixed offline, construct a Segment Tree over time $[1, Q]$. Each edge exists during a collection of disjoint time intervals $[t_{\text{start}}, t_{\text{end}}]$. Insert each edge into $\mathcal{O}(\log Q)$ canonical nodes of the Segment Tree. A DFS traversal over the Segment Tree maintains graph connectivity using a DSU with Rollback (history stack without path compression, using union by rank). At each leaf $t$, answer the query for time $t$. Total complexity: $\mathcal{O}((N + Q) \log N \log Q)$.

---

## 5. Contest-Ready Implementation Templates

### C++17 Template

```cpp
// Reverse Time DSU for Edge Cut / Component Splitting
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> p, sz;
    int comps;
    DSU(int n) : p(n + 1), sz(n + 1, 1), comps(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b]; comps--;
        return true;
    }
};
```

### Python 3 Template

```python
import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # Read edges (1-indexed input)
    edges = []
    idx = 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        edges.append((u, v))
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    # Read vertex values
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(input_data[idx])
        idx += 1

    # Iterative DFS for Euler Tour (Avoids Python recursion depth limits)
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler = []
    
    # Stack holds: (node, parent, is_post_order)
    stack = [(1, 0, False)]
    timer = 0
    
    while stack:
        u, p, is_post = stack.pop()
        
        if not is_post:
            in_time[u] = timer
            euler.append(a[u])
            timer += 1
            stack.append((u, p, True))
            for v in adj[u]:
                if v != p:
                    stack.append((v, u, False))
        else:
            out_time[u] = timer

    # Circular array doubling: A = euler + euler (Size 2N)
    A = euler + euler
    
    # Prepare offline queries for all N-1 edge cuts
    queries = []
    for i in range(n - 1):
        u, v = edges[i]
        if in_time[u] > in_time[v]:
            u, v = v, u  # v is the deeper child
            
        # Part 0: Subtree of v
        l1 = in_time[v]
        r1 = out_time[v] - 1
        
        # Part 1: Rest of tree (wrapped around in doubled array)
        l2 = out_time[v]
        r2 = in_time[v] + n - 1
        
        queries.append((l1, r1, i, 0))
        queries.append((l2, r2, i, 1))
        
    # Sort queries ascending by right boundary R
    queries.sort(key=lambda x: x[1])

    # Iterative Segment Tree: Point Update / Range Max Query
    seg_n = 2 * n
    tree = [0] * (2 * seg_n)
    
    def update(p, val):
        p += seg_n
        if val > tree[p]:
            tree[p] = val
            p //= 2
            while p > 0:
                tree[p] = max(tree[2 * p], tree[2 * p + 1])
                p //= 2

    def query(l, r):
        res = 0
        l += seg_n
        r += seg_n + 1
        while l < r:
            if l % 2 == 1:
                res = max(res, tree[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = max(res, tree[r])
            l //= 2
            r //= 2
        return res

    # Offline sweep line over doubled array
    ans = [[0, 0] for _ in range(n - 1)]
    last_pos = {}
    q_idx = 0
    m = len(queries)
    
    for i in range(2 * n):
        val = A[i]
        if val in last_pos:
            update(last_pos[val], val)
        last_pos[val] = i
        
        while q_idx < m and queries[q_idx][1] == i:
            L, R, edge_idx, part = queries[q_idx]
            ans[edge_idx][part] = query(L, R)
            q_idx += 1

    # Output max duplicate across both components for each edge cut
    out = [str(max(ans[i][0], ans[i][1])) for i in range(n - 1)]
    print("\n".join(out))

if __name__ == '__main__':
    solve()
```

---

## 6. Recognition Trigger Signals & Heuristics

- 

---

## 7. Contest WA / TLE / RE Traps

- Using path compression in DSU with Rollback: path compression destroys the tree structure and prevents rollback; only union-by-rank/size is allowed when rollbacks are needed.
- Forgetting edges that are NEVER deleted: must add all permanent edges to the initial DSU in reverse time.
- Query indexing: storing reverse-time answers requires reversing the output array before printing.
- Multiple components initially: comps counter must be initialized to $N$.

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1000C | Covered Points Count | 1700 | Line Sweep, Difference Array | 1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation. | [Solve Problem](https://codeforces.com/contest/1000/problem/C) |
| Codeforces | CF-1401E | Divide Square | 2100 | Line Sweep, Fenwick, Geometry | Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments. | [Solve Problem](https://codeforces.com/contest/1401/problem/E) |
| CSES | CSES-1741 | Area of Rectangles | 2100 | Klee's Measure, Segment Tree, Line Sweep | Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N). | [Solve Problem](https://cses.fi/problemset/task/1741) |

---

## 9. External Theory & Deep-Dive References

- **[USACO Guide]** [USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area](https://usaco.guide/plat/sweep-line)
- **[CP-Algorithms]** [CP-Algorithms: Bentley-Ottmann Line Segment Intersections](https://cp-algorithms.com/geometry/intersecting_segments.html)

---
