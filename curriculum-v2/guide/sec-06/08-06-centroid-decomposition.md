# 8. Centroid Decomposition

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** Trees, recursion/D&C, hashing/maps or arrays for freq  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: Trees, recursion/D&C, hashing/maps or arrays for freq

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Tree Algorithms leverage topological hierarchy, DFS orders, and structural decompositions. Essential techniques include Binary Lifting, Lowest Common Ancestor (LCA), Euler Tour Subtree Reductions, Tree DP with Rerooting, Heavy-Light Decomposition (HLD), and Centroid Decomposition.

### Fundamental Theorems & Invariants

- **Euler Tour Subtree Flattening:** A subtree rooted at $u$ corresponds to a contiguous subsegment $[in[u], out[u]]$ in the DFS entry/exit tour, transforming subtree updates into standard 1D range queries.
- **Heavy-Light Decomposition Theorem:** Any path between two nodes in an $N$-vertex tree traverses at most $\lfloor \log_2 N \rfloor$ heavy chains. Range queries along tree paths reduce to $\mathcal{O}(\log^2 N)$ segment tree queries.
- **Centroid Existence Theorem:** In any tree with $N$ vertices, there exists a centroid node whose removal splits the tree into subtrees each having size $\le \lfloor N / 2 \rfloor$. Decomposing recursively produces a centroid tree of depth $\le \log_2 N$.
- **Sack (DSU on Tree) Complexity:** Small-to-large merging where heavy child state is preserved and light child subtrees are re-inserted runs in strictly $\mathcal{O}(N \log N)$ total time.

### Algorithmic Execution Blueprint

1. **Binary Lifting Table:** Compute $up[u][k] = up[up[u][k-1]][k-1]$ for $k \in [1, \lceil \log_2 N \rceil]$.
2. **HLD Construction:** In DFS 1, compute $size[u]$ and identify heavy child $heavy[u] = \text{argmax}_{v \in children} size[v]$. In DFS 2, assign contiguous DFS traversal labels giving heavy children priority.
3. **Rerooting DP:** Pass 1 computes bottom-up subtree DP values $dp[u]$. Pass 2 computes global values when rerooting to child $v$ by subtracting $v$'s contribution from $u$ and merging back into $v$ in $\mathcal{O}(1)$.

### Closed-Form Invariant Equations

$$\text{Path}(u, v) = \bigcup_{k=1}^m \text{HeavyChainSegment}_k, \quad m \le \log_2 N, \quad \text{Cost}(\text{DSU on Tree}) = \sum_{u} \text{depth}_{\text{light}}(u) = \mathcal{O}(N \log N)$$

### Structural Edge Cases & Assumptions

- In Tree DP rerooting with non-invertible operations (e.g. prefix max), precompute prefix and suffix aggregates of child DP values to avoid invalid division or removal.
- Centroid decomposition requires recomputing subtree sizes inside the current component before each centroid search.
- When querying edges via HLD, the LCA vertex represents the incoming edge from its parent and must be excluded from path queries.

---

## 3. Core Intuition & Problem Framing

A **centroid** of a tree (or remaining component) is a node whose removal leaves components of size \(\le |component|/2\). Recursively decompose: for each centroid, solve all paths that **pass through** it (usually by enumerating rooted depths/XOR/weights in pending components), then mark centroid dead and recurse. Layer depth \(O(\log n)\); each node appears in \(O(\log n)\) layers. Prefer centroid for **counting/enumerating paths** with a property. Prefer HLD when you need a mutable path data structure.

---

## 4. Proof Sketches & Recurrences

Find size of component ignoring `dead[]`. Find centroid: walk from any node to a child with `sz > comp_sz/2` until none. Collect contributions: DFS into each alive neighbor subtree collecting bag of path-monoids to centroid; query bag against global map **before** inserting (avoid same-subtree pairs), then insert; clear after all neighbors; recurse. Complexity: each layer \(O(n\cdot f)\) work if maps careful → \(O(n\log n\cdot f)\). Centroid tree edges from centroid to child-centroids form a tree of height \(O(\log n)\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: build once \(O(n\log n)\) layers
- Per-query / per-operation: usually baked into decompose
- Total: \(O(n\log n\cdot f)\) where \(f\) = cost per node visit (often \(O(1)\) or \(O(\log n)\) map)
- Memory: \(O(n)\) + maps`

### C++17 Template

```cpp
// C++17 — centroid decomposition: count unordered pairs with dist == K
// Full primary template for Section 06
namespace centroid {
constexpr int N = 200005;
int n, K, sz[N];
bool dead[N];
vector<int> g[N];
long long answer = 0;

int dfs_sz(int v, int p) {
    sz[v] = 1;
    for (int to : g[v]) if (to != p && !dead[to]) sz[v] += dfs_sz(to, v);
    return sz[v];
}

int dfs_centroid(int v, int p, int comp) {
    for (int to : g[v]) if (to != p && !dead[to] && sz[to] > comp / 2)
        return dfs_centroid(to, v, comp);
    return v;
}

void dfs_depths(int v, int p, int d, vector<int>& bag) {
    if (d > K) return;
    bag.push_back(d);
    for (int to : g[v]) if (to != p && !dead[to]) dfs_depths(to, v, d + 1, bag);
}

void solve_centroid(int c) {
    // freq[d] = how many nodes at distance d from c already processed
    // Use array if K small; else hashmap. Here K < N assumed optional — use map-like vector.
    static int freq[N]; // clear carefully by touched list
    vector<int> touched;
    auto add_freq = [&](int d, int delta) {
        if (freq[d] == 0 && delta > 0) touched.push_back(d);
        freq[d] += delta;
    };

    // paths with endpoint = c
    add_freq(0, 1);

    for (int to : g[c]) if (!dead[to]) {
        vector<int> bag;
        dfs_depths(to, c, 1, bag);
        for (int d : bag) {
            if (K - d >= 0) answer += freq[K - d]; // pairs across different branches + to c
        }
        for (int d : bag) add_freq(d, 1);
    }
    for (int d : touched) freq[d] = 0;
}

void decompose(int entry) {
    int comp = dfs_sz(entry, -1);
    int c = dfs_centroid(entry, -1, comp);
    solve_centroid(c);
    dead[c] = true;
    for (int to : g[c]) if (!dead[to]) decompose(to);
}

long long count_paths_of_length(int k) {
    K = k;
    answer = 0;
    fill(dead, dead + n + 1, false);
    decompose(1);
    return answer;
}
} // namespace centroid

/* General pattern for XOR / weighted:
   - bag stores path_xor to centroid
   - query map[need ^ x] before inserting
   - unordered_map or fixed arrays by value domain
   Centroid tree parent:
   int cpar[N];
   // when recurse into component, cpar[child_centroid] = c;
*/
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count pairs/paths with length \(=k\), XOR \(=x\), weight in range
- “Paths through a separator”, divide-and-conquer on trees
- Offline path statistics without updates
- Balanced separator on trees (size-halving)

---

## 7. Contest WA / TLE / RE Traps

- Counting pairs inside the same subtree twice — **query before insert** per branch
- Forgetting `dead[]` when computing sizes
- Not clearing frequency structures (use touched lists)
- Off-by-one on path length (nodes vs edges)
- Recursing into `to` before marking centroid dead
- Using global `sz` without recomputing per component

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-600E | Lomsat gelh | 2000 | DSU on Tree, Sack, Euler Tour | DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N). | [Solve Problem](https://codeforces.com/contest/600/problem/E) |
| Codeforces | CF-343D | Water Tree | 2100 | Euler Tour, HLD, Lazy SegTree | Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree. | [Solve Problem](https://codeforces.com/contest/343/problem/D) |
| Codeforces | CF-1009F | Dominant Indices | 2300 | DSU on Tree, Tree DP | Dsu on Tree with depth array or Long Path Decomposition in O(N). | [Solve Problem](https://codeforces.com/contest/1009/problem/F) |
| Codeforces | CF-321C | Ciel the Commander | 2100 | Centroid Decomposition, Divide and Conquer | Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels). | [Solve Problem](https://codeforces.com/contest/321/problem/C) |
| CSES | CSES-1138 | Path Queries | 1800 | Euler Tour, Fenwick, LCA | Euler tour + in/out difference updates on Fenwick tree for point updates and path sums. | [Solve Problem](https://cses.fi/problemset/task/1138) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)](https://cp-algorithms.com/graph/lca.html)
- **[CP-Algorithms]** [CP-Algorithms: Heavy-Light Decomposition](https://cp-algorithms.com/graph/hld.html)
- **[Codeforces]** [Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)](https://codeforces.com/blog/entry/44351)
- **[USACO Guide]** [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Centroid tree** as auxiliary tree for \(O(\log n)\) “jump” structures
- **XOR / and / gcd** path counts via maps at centroid
- **With updates:** harder — often BIT on centroid tree + reconstruction
- **Edge-weighted distances** in DFS collect

---

## 11. Typical Problem Archetypes

1. Standard application: number of paths of length \(k\)
2. Slightly disguised: number of paths with XOR \(=x\)
3. Difficult: count paths with length in \([L,R]\) (prefix freq)
4. Very difficult / advanced: dynamic centroid / offline with BIT on layers

---

## 12. Recognition & Identification Drills

1. Count simple paths with exactly \(k\) edges.
2. Count paths whose XOR of edge weights equals \(x\).
3. Find whether there is a path with sum of weights in a given set of targets.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: path counting / D&C by separator, not mutable path DS
- Key invariant: centroid splits sizes by \(\ge 1/2\); paths through centroid handled once
- Key formula: per branch query-then-insert into freq at centroid
- Complexity: \(O(n\log n\cdot f)\)
- Template to remember: `sz` → `centroid` → solve through-c → `dead[c]=1` → recurse

---

## 9. DSU on tree / Sack

---
