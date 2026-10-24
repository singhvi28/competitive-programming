# 7. Heavy-Light Decomposition (HLD)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Trees, Euler/DFS order, segment tree / Fenwick, LCA ideas  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Trees, Euler/DFS order, segment tree / Fenwick, LCA ideas

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

Classify edges: **heavy** = to the child with largest subtree size; others **light**. Heavy paths are contiguous chains. Any root↔node path crosses \(O(\log n)\) light edges, hence \(O(\log n)\) heavy paths. Map each heavy path to a contiguous segment-tree interval (DFS: visit heavy child first). Path query/update = \(O(\log n)\) segments × segtree \(O(\log n)\) → \(O(\log^2 n)\). Prefer HLD for **online path + subtree** with a standard DS. Prefer **centroid** when the problem is D&C path counting without a living DS on paths.

---

## 4. Proof Sketches & Recurrences

`sz[v]` via DFS. Heavy child: \(\arg\max sz[c]\). Second DFS assigns `head[v]` (top of heavy path), `pos[v]` (segtree index), increasing along heavy edges. Path \(u\!\to\!v\): while `head[u] != head[v]`, lift the deeper head: query `[pos[head[u]], pos[u]]`, then `u = parent[head[u]]`. Finally query the remaining chain between `u,v`. Subtree of \(v\) is contiguous `[pos[v], pos[v]+sz[v]-1]` if heavy-first DFS. Light edges \(\Rightarrow\) size at least halves → \(O(\log n)\) chains.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) HLD + \(O(n)\) (or \(O(n\log n)\)) segtree build
- Per-query / per-operation: \(O(\log^2 n)\) path; \(O(\log n)\) subtree/point
- Total: \(O(n + q\log^2 n)\)
- Memory: \(O(n)\)`

### C++17 Template

```cpp
// C++17 — HLD + iterative segment tree (path/subtree sum, point add)
// Full primary template for Section 06
namespace hld {
constexpr int N = 200005;
int n, timer;
int sz[N], dep[N], parent[N], heavy[N], head[N], pos[N];
vector<int> g[N];
long long base[N]; // values by node, placed at pos[v]

struct Seg {
    int n; vector<long long> t;
    void init(int n_) { n = n_; t.assign(2 * n, 0); }
    void build(long long *a) { // a[0..n-1]
        for (int i = 0; i < n; ++i) t[n + i] = a[i];
        for (int i = n - 1; i > 0; --i) t[i] = t[i << 1] + t[i << 1 | 1];
    }
    void add(int p, long long x) {
        for (t[p += n] += x; p > 1; p >>= 1) t[p] = t[p << 1] + t[p << 1 | 1];
    }
    long long query(int l, int r) { // inclusive
        long long res = 0;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res += t[l++];
            if (r & 1) res += t[--r];
        }
        return res;
    }
} seg;

int dfs_sz(int v, int p) {
    sz[v] = 1; parent[v] = p; heavy[v] = -1;
    int best = 0;
    for (int to : g[v]) if (to != p) {
        dep[to] = dep[v] + 1;
        int s = dfs_sz(to, v);
        sz[v] += s;
        if (s > best) best = s, heavy[v] = to;
    }
    return sz[v];
}

void dfs_hld(int v, int h) {
    head[v] = h;
    pos[v] = timer++;
    if (heavy[v] != -1) dfs_hld(heavy[v], h);
    for (int to : g[v])
        if (to != parent[v] && to != heavy[v]) dfs_hld(to, to);
}

void build(int root = 1) {
    timer = 0;
    dep[root] = 0;
    dfs_sz(root, 0);
    dfs_hld(root, root);
    vector<long long> arr(n);
    for (int v = 1; v <= n; ++v) arr[pos[v]] = base[v];
    seg.init(n);
    seg.build(arr.data());
}

long long path_query(int u, int v) {
    long long res = 0;
    while (head[u] != head[v]) {
        if (dep[head[u]] < dep[head[v]]) swap(u, v);
        res += seg.query(pos[head[u]], pos[u]);
        u = parent[head[u]];
    }
    if (dep[u] > dep[v]) swap(u, v);
    res += seg.query(pos[u], pos[v]); // node values; for edge values use pos[u]+1..pos[v]
    return res;
}

void path_add(int u, int v, long long x) { // needs lazy segtree; sketch with point adds only below
    // replace seg with lazy range-add if required
    (void)u; (void)v; (void)x;
}

void point_add(int v, long long x) { seg.add(pos[v], x); }

long long subtree_query(int v) {
    return seg.query(pos[v], pos[v] + sz[v] - 1);
}
} // namespace hld

/* Lazy range-add + range-sum (drop-in for path_add / range updates)
struct LazySeg {
    int n; vector<long long> t, lz;
    void init(int n_) { n = n_; t.assign(4*n+4,0); lz.assign(4*n+4,0); }
    void apply(int p, int l, int r, long long x) { t[p]+=x*(r-l+1); lz[p]+=x; }
    void push(int p, int l, int r) {
        if (!lz[p] || l==r) return;
        int m=(l+r)/2;
        apply(p<<1,l,m,lz[p]); apply(p<<1|1,m+1,r,lz[p]); lz[p]=0;
    }
    void add(int p, int l, int r, int ql, int qr, long long x) {
        if (qr<l||r<ql) return;
        if (ql<=l&&r<=qr) { apply(p,l,r,x); return; }
        push(p,l,r);
        int m=(l+r)/2;
        add(p<<1,l,m,ql,qr,x); add(p<<1|1,m+1,r,ql,qr,x);
        t[p]=t[p<<1]+t[p<<1|1];
    }
    long long query(int p, int l, int r, int ql, int qr) {
        if (qr<l||r<ql) return 0;
        if (ql<=l&&r<=qr) return t[p];
        push(p,l,r);
        int m=(l+r)/2;
        return query(p<<1,l,m,ql,qr)+query(p<<1|1,m+1,r,ql,qr);
    }
};
// path_add: same while-loop as path_query, calling lazy.add on [pos[head], pos[u]]
*/
```

---

## 6. Recognition Trigger Signals & Heuristics

- Path sum/min/xor + point or path updates, \(n,q\sim 10^5\)
- Mix of path and subtree operations on one tree
- “Chain decomposition”, “heavy child”
- Offline path problems that still scream segtree

---

## 7. Contest WA / TLE / RE Traps

- Not visiting heavy child first → subtree ranges break
- Edge vs node values: path query must skip LCA node or use `pos[child]` on edges
- Comparing `dep[u]` instead of `dep[head[u]]` when lifting chains
- Forgetting `u = parent[head[u]]` after querying a chain
- Lazy segtree push bugs under path updates
- Root parent = 0; `head` of root = root

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

- **Edge HLD:** store value at deeper endpoint
- **HLD + lazy** for path add / path assign
- **HLD + merge sort tree / Mo** rare
- **Multiple trees / forests:** run per component
- **Binary lifting path aggregates** — lighter if only static idempotent ops

---

## 11. Typical Problem Archetypes

1. Standard application: path sum + point update
2. Slightly disguised: company chain of command salary queries
3. Difficult: path add + subtree query simultaneously
4. Very difficult / advanced: HLD on condensed trees / with virtual trees

---

## 12. Recognition & Identification Drills

1. Tree; queries: add \(x\) on path \(u\!\to\!v\); report sum on path \(a\!\to\!b\).
2. Same, but also query sum of subtree of \(v\).
3. Edge weights; update one edge; query max edge on path (static max → lifting also works; with updates → HLD).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: online path DS ops, optionally + subtree
- Key invariant: \(O(\log n)\) heavy paths per path; heavy-first DFS contiguous
- Key formula: lift deeper `head` until same chain, then mid-segment
- Complexity: \(O(\log^2 n)\) per path op
- Template to remember: `dfs_sz` → `dfs_hld` → segtree on `pos` → while heads differ

---

## 8. Centroid decomposition

---
