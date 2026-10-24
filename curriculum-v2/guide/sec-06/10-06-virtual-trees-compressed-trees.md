# Virtual Trees (Compressed Trees)

> **Section:** §06 Tree Algorithms & Structural Decompositions  
> **Phase:** Phase 2 — Tree Algorithms & Structural Hierarchies  
> **Contest ROI:** B-tier | **Rating Range:** 2200–2800 | **Frequency:** Occasional  
> **Prerequisites:** LCA, Euler `tin`, stack construction  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: LCA, Euler `tin`, stack construction

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

Given \(k\) key nodes, the **virtual tree** is the tree on those keys plus their pairwise LCAs, with only compression edges between them. Size \(O(k)\). Build by sorting keys by `tin`, stacking LCAs. Then run DP only on \(O(k)\) nodes instead of \(n\). Prefer virtual trees when **many queries each with few keys**. Prefer Sack when every subtree of the full tree needs an answer.

---

## 4. Proof Sketches & Recurrences

Sort unique keys by `tin`. Stack maintains a chain of virtual-tree ancestors. For next key \(x\): while stack top is not ancestor of \(x\), pop (connecting edges). Insert LCA(`stack.top`, `x`) if needed, then push \(x\). Each key and each LCA inserted \(O(1)\) amortized → \(O(k\log n)\) with LCA. DP on built adjacency (undirected edges between parent links). Clear virtual adjacency after each query.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: LCA + tin \(O(n\log n)\)
- Per-query / per-operation: \(O(k\log n)\) build + \(O(k\cdot\text{DP})\)
- Total: \(O(n\log n + \sum k\log n)\)
- Memory: \(O(n + k)\) per query if cleared`

### C++17 Template

```cpp
// C++17 — virtual tree construction + cleanup (needs lca_bl + euler tin)
namespace vtree {
constexpr int N = 200005;
int n;
vector<int> g[N];          // original
vector<int> virt[N];       // virtual edges
int tin[N], timer_e;
// assume lca_bl::lca, lca_bl::dep available; tin from euler tour

void dfs_tin(int v, int p) {
    tin[v] = ++timer_e;
    for (int to : g[v]) if (to != p) dfs_tin(to, v);
}

bool anc(int a, int b) { // need tout OR use lca: lca(a,b)==a
    return lca_bl::lca(a, b) == a;
}

vector<int> nodes; // reusable buffer of involved nodes for cleanup

void add_edge(int u, int v) {
    virt[u].push_back(v);
    virt[v].push_back(u);
}

void build(vector<int> key) {
    sort(key.begin(), key.end(), [](int a, int b) { return tin[a] < tin[b]; });
    key.erase(unique(key.begin(), key.end()), key.end());
    nodes = key;
    vector<int> st;
    auto ensure = [&](int x) {
        nodes.push_back(x);
    };
    for (int x : key) {
        if (st.empty()) { st.push_back(x); continue; }
        int w = lca_bl::lca(x, st.back());
        if (w != st.back()) {
            while (st.size() >= 2 && tin[st[st.size() - 2]] >= tin[w]) {
                add_edge(st[st.size() - 2], st.back());
                st.pop_back();
            }
            if (st.back() != w) {
                add_edge(w, st.back());
                st.pop_back();
                ensure(w);
                st.push_back(w);
            }
        }
        st.push_back(x);
    }
    while (st.size() >= 2) {
        add_edge(st[st.size() - 2], st.back());
        st.pop_back();
    }
}

void clear() {
    for (int v : nodes) virt[v].clear();
    nodes.clear();
}

// Example DP stub: sum of edge lengths in virtual tree (Steiner for keys)
// long long dp(int v, int p) { ... use lca_bl::dep[u]+dep[v]-2*dep[lca] for real distance }
} // namespace vtree
```

---

## 6. Recognition Trigger Signals & Heuristics

- \(q\) queries, each with \(k_i\) important vertices, \(\sum k_i \le 10^5\)–\(2\cdot10^6\)
- DP / cost only depends on keys and LCAs between them
- “Steiner tree on tree”, key cities, important nodes
- Compress tree between specials

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to include LCAs as vertices
- Not sorting by `tin`
- Leaving stale `virt` edges between queries
- Duplicate keys
- Treating virtual edge weight as 1 instead of real tree distance
- Stack LCA cases off-by-one (need careful casework — test on chains)

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

- **Virtual tree + DP** for virus/infection, key black nodes
- **Only keys that are leaves of virtual tree** sometimes
- **Kruskal reconstruction + virtual** for max-edge queries among keys
- **Build with sparse table LCA \(O(1)\)**

---

## 11. Typical Problem Archetypes

1. Standard application: cost of connecting \(k\) cities along tree (Steiner = virtual tree edges)
2. Slightly disguised: queries with important festivals on nodes
3. Difficult: DP “cut edges so keys in different components”
4. Very difficult / advanced: virtual tree + HLD / segment trees on compressed nodes

---

## 12. Recognition & Identification Drills

1. \(q\) queries each listing \(k\) nodes; for each, compute the size of the minimal subtree containing all of them (number of edges).
2. Same keys; compute min edges to remove to isolate all keys into singleton components.
3. Multiple queries of key sets; count pairs of keys whose path passes through a given fixed node type — compress first.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: many queries, few keys each, DP on keys+LCAs
- Key invariant: sorted by `tin`, stack maintains ancestral chain; size \(O(k)\)
- Key formula: build \(O(k\log n)\); edge weight = tree distance
- Complexity: \(O(n\log n + \sum k\log n)\)
- Template to remember: sort keys → stack + LCA inserts → DP → clear

---

## End drills (part B focus)

1. Code HLD path sum + point update from scratch once; then add lazy path add.
2. Code centroid count-paths-of-length-\(k\); mutate to XOR\(=x\).
3. Code Sack distinct colors; extend to mode.
4. Code virtual tree builder; verify size \(O(k)\) on random keys; one Steiner-length query.

Back to index: [06-trees.md](06-trees.md) · Core techniques: [06-a-trees-core.md](06-a-trees-core.md).

---
