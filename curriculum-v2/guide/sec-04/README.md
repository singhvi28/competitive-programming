# Section §04: Square Root Decomposition & Mo's Algorithm

> **Module ID:** `sec-04`  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Topic Count:** 2  

**Module Summary:** Block decomposition, range updates with O(sqrt(N)) blocks, Mo's algorithm on arrays in O((N+Q)sqrt(N)), Hilbert curve sorting, and Mo's on trees.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Mo's algorithm](#topic-1) | `B-tier` | 1900–2500 | Occasional | [01-04-mo-s-algorithm.md](./01-04-mo-s-algorithm.md) |
| 2 | [Mo's algorithm on trees](#topic-2) | `C-tier` | 2200–2800 | Rare | [02-04-mo-s-algorithm-on-trees.md](./02-04-mo-s-algorithm-on-trees.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Mo's algorithm

> **Section:** §04 Square Root Decomposition & Mo's Algorithm  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Offline queries, block ordering, frequency maps  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Offline queries, block ordering, frequency maps

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Square Root Decomposition partitions data of size $N$ into blocks of size $B \approx \sqrt{N}$, reducing range queries and updates to $\mathcal{O}(\sqrt{N})$. Mo's Algorithm processes $Q$ offline range queries in $\mathcal{O}((N + Q)\sqrt{N})$ by ordering queries along a Hilbert space-filling curve.

##### Fundamental Theorems & Invariants

- **Optimal Block Size:** Setting block size $B = \frac{N}{\sqrt{Q}}$ balances the total left-pointer movement ($Q \cdot B$) and right-pointer movement ($N \cdot \frac{N}{B}$), achieving minimal state transitions.
- **Hilbert Curve Sorting:** Ordering queries by Hilbert curve coordinates rather than simple serpentine block indices reduces total pointer movements by $25\%–40\%$, avoiding worst-case boundary oscillations.
- **Tree Mo via Euler Tour:** Flattening a tree into its DFS entry/exit tour allows arbitrary path queries $u \leftrightarrow v$ to be mapped to contiguous range queries on the tour array with an LCA parity toggle.

##### Algorithmic Execution Blueprint

1. **Query Sorting:** Sort queries $(L_i, R_i)$ primarily by $L_i / B$, and secondarily by $R_i$ (alternating ascending/descending on odd/even blocks).
2. **Two-Pointer Maintenance:** Maintain current state $[curL, curR]$ and an aggregate frequency array. Step $curL$ and $curR$ one element at a time via `add(idx)` and `remove(idx)`.
3. **Tree Path Adaptation:** If $u$ is an ancestor of $v$, query range is $[in[u], in[v]]$. Otherwise query is $[out[u], in[v]] + \{LCA(u, v)\}$. Toggle vertex presence via XOR parity.

##### Closed-Form Invariant Equations

$$\text{Total Steps} = \sum_{i} |L_i - L_{i-1}| + \sum_i |R_i - R_{i-1}| \le 2N\sqrt{Q} + \frac{N^2}{B} = \mathcal{O}((N+Q)\sqrt{N})$$

##### Structural Edge Cases & Assumptions

- In Mo's algorithm, remember to update the answer after adjusting both left and right pointers, not in between.
- When removing elements, ensure counters do not decrement below 0 or access negative array indices.
- For Mo's on Trees, if $u$ and $v$ have an LCA that is not $u$, the LCA node itself must be manually toggled before answering the query and toggled back immediately after.

---

#### 3. Core Intuition & Problem Framing

Mo answers many range queries on a **static** array by physically moving a sliding window \([cl,cr]\) to each query’s \([l,r]\), applying `add`/`del` at the endpoints. Sorting queries in **blocks** (by \(l/\mathrm{B}\), then by \(r\)) makes total movement \(O(n\sqrt q)\) (or \(O(n\sqrt n)\)). Prefer Mo when **maintaining the answer under ± one endpoint** is easy, but building a mergeable segment-tree node for the same answer is painful (distinct count with fancy secondary stats, mode, XOR basis size, etc.). Prefer a **segtree** when you need updates or online answers — see comparison in the [section index](18-randomization-misc.md).

---

#### 4. Proof Sketches & Recurrences

Block size \(B \approx n / \sqrt{q}\) (or \(\sqrt n\)).
Sort: key `(l/B, r)` (odd blocks can reverse \(r\) — Hilbert/improving constant).
Across \(q\) queries: \(l\) moves \(O(B)\) within a block × \(q\) plus \(O(n/B)\) block changes × \(n\) → with \(B\sim n/\sqrt{q}\), total endpoint moves \(O(n\sqrt{q})\).
Time \(O((n\sqrt{q})\cdot F)\) for add/del cost \(F\).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: compress + sort queries \(O((n+q)\log n)\)
- Per-query / per-operation: amortized via total moves
- Total: \(O((n+q)\sqrt{n}\cdot F)\) typical with \(F=O(1)\)
- Memory: \(O(n+q + \sigma)\) for frequencies`

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace mo {
struct Query { int l, r, idx; }; // inclusive l,r; 0-index

int BLOCK;

// Distinct count example
vector<int> solve(const vector<int>& a, vector<Query> qs) {
    int n = (int)a.size();
    BLOCK = max(1, (int)(n / sqrt(max(1, (int)qs.size()))));
    sort(qs.begin(), qs.end(), [](const Query& A, const Query& B) {
        int ba = A.l / BLOCK, bb = B.l / BLOCK;
        if (ba != bb) return ba < bb;
        return (ba & 1) ? (A.r > B.r) : (A.r < B.r);
    });

    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<int> b(n);
    for (int i = 0; i < n; ++i)
        b[i] = (int)(lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin());

    vector<int> freq(vals.size(), 0);
    int distinct = 0;
    auto add = [&](int i) {
        if (freq[b[i]]++ == 0) ++distinct;
    };
    auto del = [&](int i) {
        if (--freq[b[i]] == 0) --distinct;
    };

    vector<int> ans(qs.size());
    int cl = 0, cr = -1;
    for (auto& q : qs) {
        while (cl > q.l) add(--cl);
        while (cr < q.r) add(++cr);
        while (cl < q.l) del(cl++);
        while (cr > q.r) del(cr--);
        ans[q.idx] = distinct;
    }
    return ans;
}
} // namespace mo
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Offline \([l,r]\) queries, array immutable
- “Number of distinct”, “frequency of mode”, “count values with freq > 0 satisfying P”
- Add/del an index updates a global frequency structure in \(O(1)\) or \(O(\log)\)
- Segtree merge would need sets/maps in each node → TLE/MLE

---

#### 7. Contest WA / TLE / RE Traps

- Wrong block size → TLE
- Inclusive/exclusive bounds mismatch in add/del loops
- Forgetting to restore `ans[idx]` after sort
- Using Mo when updates exist (need Mo with updates / different technique)
- `freq--` then check vs check then `--` order bugs

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-86D | Powerful array | 2200 | Mo's Algorithm, Sqrt Decomposition | Classic Mo's algorithm tracking frequency squares with O(1) state transitions. | [Solve Problem](https://codeforces.com/contest/86/problem/D) |
| Codeforces | CF-617E | XOR and Favorite Number | 2000 | Mo's Algorithm, Prefix XOR | Prefix XOR array with Mo's algorithm querying frequency of prefixXOR ^ k. | [Solve Problem](https://codeforces.com/contest/617/problem/E) |
| Codeforces | CF-375D | Tree and Queries | 2400 | Mo's on Trees, Euler Tour, DSU on Tree | Euler tour subtree flattening with Mo's algorithm or DSU on Tree. | [Solve Problem](https://codeforces.com/contest/375/problem/D) |
| Codeforces | CF-940F | Machine Learning | 2500 | Mo's with Updates, 3D Sqrt | 3D Mo's Algorithm with point updates in O(N^(5/3)) time. | [Solve Problem](https://codeforces.com/contest/940/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sqrt Decomposition & Block Updates](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
- **[Codeforces]** [Codeforces Blog: Mo's Algorithm on Arrays and Trees (Errichto)](https://codeforces.com/blog/entry/43230)
- **[USACO Guide]** [USACO Guide: Mo's Algorithm with Hilbert Curve Sorting](https://usaco.guide/plat/mo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Mo with updates** (time as third dimension) — heavier
- **Hilbert order** — better cache / constants
- **Rollback Mo** — only add, rollback to checkpoint (when delete hard)
- Tree Mo — §7

---

#### 11. Typical Problem Archetypes

1. Standard application: distinct values in \([l,r]\)
2. Slightly disguised: count pairs with equal values in range (freq choose 2)
3. Difficult: maintain XOR basis under add/del on range
4. Very difficult / advanced: Mo on trees / Mo with updates

---

#### 12. Recognition & Identification Drills

1. Static array; \(q=10^5\) queries ask how many values appear exactly \(k\) times in \([l,r]\).
2. Same but array updates between queries — is Mo still OK?
3. Online distinct queries stream in — Mo or persistent segtree?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: offline static ranges; add/del easy; merge hard
- Key invariant: window always equals current query range after moves
- Key formula: \(O(n\sqrt{q}\,F)\); \(B \approx n/\sqrt{q}\)
- Complexity: usually \(O(n\sqrt{n})\)
- Template to remember: sort by block, `add/del`, four while-loops

---

## 8. Mo's algorithm on trees

---


---

<a id="topic-2"></a>
### 2. Mo's algorithm on trees

> **Section:** §04 Square Root Decomposition & Mo's Algorithm  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** Euler tour (entry/exit), LCA, array Mo  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: Euler tour (entry/exit), LCA, array Mo

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Square Root Decomposition partitions data of size $N$ into blocks of size $B \approx \sqrt{N}$, reducing range queries and updates to $\mathcal{O}(\sqrt{N})$. Mo's Algorithm processes $Q$ offline range queries in $\mathcal{O}((N + Q)\sqrt{N})$ by ordering queries along a Hilbert space-filling curve.

##### Fundamental Theorems & Invariants

- **Optimal Block Size:** Setting block size $B = \frac{N}{\sqrt{Q}}$ balances the total left-pointer movement ($Q \cdot B$) and right-pointer movement ($N \cdot \frac{N}{B}$), achieving minimal state transitions.
- **Hilbert Curve Sorting:** Ordering queries by Hilbert curve coordinates rather than simple serpentine block indices reduces total pointer movements by $25\%–40\%$, avoiding worst-case boundary oscillations.
- **Tree Mo via Euler Tour:** Flattening a tree into its DFS entry/exit tour allows arbitrary path queries $u \leftrightarrow v$ to be mapped to contiguous range queries on the tour array with an LCA parity toggle.

##### Algorithmic Execution Blueprint

1. **Query Sorting:** Sort queries $(L_i, R_i)$ primarily by $L_i / B$, and secondarily by $R_i$ (alternating ascending/descending on odd/even blocks).
2. **Two-Pointer Maintenance:** Maintain current state $[curL, curR]$ and an aggregate frequency array. Step $curL$ and $curR$ one element at a time via `add(idx)` and `remove(idx)`.
3. **Tree Path Adaptation:** If $u$ is an ancestor of $v$, query range is $[in[u], in[v]]$. Otherwise query is $[out[u], in[v]] + \{LCA(u, v)\}$. Toggle vertex presence via XOR parity.

##### Closed-Form Invariant Equations

$$\text{Total Steps} = \sum_{i} |L_i - L_{i-1}| + \sum_i |R_i - R_{i-1}| \le 2N\sqrt{Q} + \frac{N^2}{B} = \mathcal{O}((N+Q)\sqrt{N})$$

##### Structural Edge Cases & Assumptions

- In Mo's algorithm, remember to update the answer after adjusting both left and right pointers, not in between.
- When removing elements, ensure counters do not decrement below 0 or access negative array indices.
- For Mo's on Trees, if $u$ and $v$ have an LCA that is not $u$, the LCA node itself must be manually toggled before answering the query and toggled back immediately after.

---

#### 3. Core Intuition & Problem Framing

Map tree-path queries to array Mo on the **Euler tour**. One standard scheme: store entry and exit times; a path \(u\sim v\) becomes a mix of tour segments plus LCA handling. A common “tour + toggle” approach: flatten `tin`/`tout` so each node appears twice; toggling presence of a node when the Mo window crosses an occurrence puts nodes on the \(u\)–\(v\) path (with LCA carefully added/removed) into the frequency structure. Powerful but brittle — prefer HLD + segtree / binary lifting when the query is associative.

---

#### 4. Proof Sketches & Recurrences

Euler tour length \(O(n)\). \(q\) path queries → Mo on tour length \(O(n)\) with same \(O(n\sqrt{q})\) moves, plus LCA in \(O(1)/O(\log)\) per query. Total like array Mo with larger constant and harder `add` (toggle).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: Euler + LCA \(O(n\log n)\)
- Per-query / per-operation: Mo moves + toggle
- Total: \(O(n\sqrt{q}\cdot F)\) with large constant
- Memory: \(O(n\log n + q)\)`

##### C++17 Template

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace tree_mo {
// Sketch: Euler tour + toggle Mo for path distinct colors.
// Structural template — wire LCA (binary lifting) in contest.

int n, timer;
vector<vector<int>> g;
vector<int> a, tin, tout, euler, depth, parent;

void dfs(int v, int p) {
    parent[v] = p;
    tin[v] = timer;
    euler[timer++] = v;
    for (int to : g[v]) if (to != p) {
        depth[to] = depth[v] + 1;
        dfs(to, v);
    }
    tout[v] = timer;
    euler[timer++] = v;
}

// Assume: int lca(int u, int v);

struct Query { int l, r, lca, idx; bool need_lca; };

// if lca(u,v)==u: Mo on [tin[u], tin[v]]
// else: Mo on [tout[u], tin[v]] and add lca node separately
Query make_query(int u, int v, int idx) {
    int w = lca(u, v);
    if (tin[u] > tin[v]) swap(u, v);
    Query q;
    q.idx = idx; q.lca = w;
    if (w == u) {
        q.l = tin[u]; q.r = tin[v]; q.need_lca = false;
    } else {
        q.l = tout[u]; q.r = tin[v]; q.need_lca = true;
    }
    return q;
}

// In Mo add/del: toggle node x = euler[pos]:
// if currently in: remove value a[x]; else insert.
// After answering window, if q.need_lca: temporarily add lca.
} // namespace tree_mo
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Queries = properties of **values on the path** \(u\sim v\) (distinct colors, mode, …)
- Same additive frequency logic as array Mo
- Editorial: “Mo on tree” / “Euler tour Mo”

---

#### 7. Contest WA / TLE / RE Traps

- Wrong path↔tour mapping (LCA cases)
- Forgetting to toggle LCA when `need_lca`
- Treating tree Mo as first solution before HLD/sack
- Double-appearance toggle off-by-one on `tin`/`tout`

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-86D | Powerful array | 2200 | Mo's Algorithm, Sqrt Decomposition | Classic Mo's algorithm tracking frequency squares with O(1) state transitions. | [Solve Problem](https://codeforces.com/contest/86/problem/D) |
| Codeforces | CF-617E | XOR and Favorite Number | 2000 | Mo's Algorithm, Prefix XOR | Prefix XOR array with Mo's algorithm querying frequency of prefixXOR ^ k. | [Solve Problem](https://codeforces.com/contest/617/problem/E) |
| Codeforces | CF-375D | Tree and Queries | 2400 | Mo's on Trees, Euler Tour, DSU on Tree | Euler tour subtree flattening with Mo's algorithm or DSU on Tree. | [Solve Problem](https://codeforces.com/contest/375/problem/D) |
| Codeforces | CF-940F | Machine Learning | 2500 | Mo's with Updates, 3D Sqrt | 3D Mo's Algorithm with point updates in O(N^(5/3)) time. | [Solve Problem](https://codeforces.com/contest/940/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Sqrt Decomposition & Block Updates](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
- **[Codeforces]** [Codeforces Blog: Mo's Algorithm on Arrays and Trees (Errichto)](https://codeforces.com/blog/entry/43230)
- **[USACO Guide]** [USACO Guide: Mo's Algorithm with Hilbert Curve Sorting](https://usaco.guide/plat/mo)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Sack (DSU on tree) for subtree queries — often better than Mo for subtrees
- Path queries with updates → HLD, not Mo

---

#### 11. Typical Problem Archetypes

1. Standard application: distinct colors on path
2. Slightly disguised: count colors with odd frequency on path
3. Difficult: Mo on tree with secondary constraints
4. Very difficult / advanced: tree Mo + updates

---

#### 12. Recognition & Identification Drills

1. Tree \(n=10^5\); queries ask number of distinct node colors on path \(u\sim v\).
2. Same for **subtree** queries — Mo on tree or sack?
3. Path minimum — Mo or binary lifting?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: rare; path frequency queries where only Mo-style state works
- Key invariant: toggle Euler occurrences ↔ nodes on path (plus LCA fix)
- Key formula: same Mo bound on tour length \(2n\)
- Complexity: \(O(n\sqrt{q}\,F)\) heavy
- Template to remember: `tin`/`tout` cases + LCA patch

---

## 9. Parallel binary search

---


---
