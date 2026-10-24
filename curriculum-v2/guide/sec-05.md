# Section §05: Advanced Data Structures (Treaps, LCT, PBDS)

> **Module ID:** `sec-05`  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Topic Count:** 8  

**Module Summary:** Sparse tables, Cartesian trees, Implicit & explicit Treaps, PBDS ordered statistics, DSU with rollback, and Link-Cut Trees.

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [Sparse Table (RMQ / Idempotent Range Queries)](#topic-1) | `S-tier` | 1400–1900 | Common | [01-05-sparse-table-rmq-idempotent-range-queries.md](./01-05-sparse-table-rmq-idempotent-range-queries.md) |
| 2 | [Disjoint Sparse Table](#topic-2) | `C-tier` | 2000–2500 | Rare | [02-05-disjoint-sparse-table.md](./02-05-disjoint-sparse-table.md) |
| 3 | [Cartesian Tree](#topic-3) | `B-tier` | 1900–2500 | Occasional | [03-05-cartesian-tree.md](./03-05-cartesian-tree.md) |
| 4 | [Treap (Explicit + Implicit)](#topic-4) | `B-tier` | 2000–2700 | Occasional | [04-05-treap-explicit-implicit.md](./04-05-treap-explicit-implicit.md) |
| 5 | [Splay Tree (Concepts)](#topic-5) | `Niche` | 2200–2800 | Rare | [05-05-splay-tree-concepts.md](./05-05-splay-tree-concepts.md) |
| 6 | [Randomized BST](#topic-6) | `C-tier` | 2000–2600 | Rare | [06-05-randomized-bst.md](./06-05-randomized-bst.md) |
| 7 | [Ordered Statistics (PBDS / Fenwick / Treap)](#topic-7) | `A-tier` | 1600–2200 | Common | [07-05-ordered-statistics-pbds-fenwick-treap.md](./07-05-ordered-statistics-pbds-fenwick-treap.md) |
| 8 | [Link-Cut Tree (Concept + Preferred-Path Sketch)](#topic-8) | `Niche` | 2600–3500 | Rare | [08-05-link-cut-tree-concept-preferred-path-sketch.md](./08-05-link-cut-tree-concept-preferred-path-sketch.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. Sparse Table (RMQ / Idempotent Range Queries)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** S-tier | **Rating Range:** 1400–1900 | **Frequency:** Common  
> **Prerequisites:** Binary lifting idea, idempotent semigroup ops (min, max, gcd, AND, OR)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–1900
- Prerequisites: Binary lifting idea, idempotent semigroup ops (min, max, gcd, AND, OR)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Precompute every interval whose length is a power of two. For idempotent ops, any \([L,R]\) is the op of **two overlapping** \(2^k\) blocks covering it — overlap is fine because \(x\oplus x=x\). That gives true \(O(1)\) queries after \(O(n\log n)\) build. No updates: if the array mutates, use a segtree/Fenwick instead.

---

#### 4. Proof Sketches & Recurrences

\[
st[k][i] = \mathrm{op}(st[k-1][i], st[k-1][i+2^{k-1}])
\]
For query \([L,R]\) (0-index), \(len=R-L+1\), \(k=\lfloor\log_2 len\rfloor\):
\[
\mathrm{op}(st[k][L], st[k][R-2^k+1]).
\]
Works iff `op` is idempotent (and associative). For pure associative non-idempotent ops, use disjoint sparse table or segtree.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\)
- Per-query / per-operation: \(O(1)\)
- Total: \(O(n\log n + q)\)
- Memory: \(O(n\log n)\)`

##### C++17 Template

```cpp
namespace sparse_table {
template <class T, class F>
struct SparseTable {
    int n;
    vector<int> lg;
    vector<vector<T>> st;
    F op;
    SparseTable() : n(0), op() {}
    SparseTable(const vector<T>& a, F op_) : n((int)a.size()), op(op_) {
        lg.assign(n + 1, 0);
        for (int i = 2; i <= n; ++i) lg[i] = lg[i / 2] + 1;
        int K = lg[n] + 1;
        st.assign(K, vector<T>(n));
        st[0] = a;
        for (int k = 1; k < K; ++k)
            for (int i = 0; i + (1 << k) <= n; ++i)
                st[k][i] = op(st[k - 1][i], st[k - 1][i + (1 << (k - 1))]);
    }
    T query(int l, int r) const { // inclusive, 0-indexed
        int k = lg[r - l + 1];
        return op(st[k][l], st[k][r - (1 << k) + 1]);
    }
};

struct MinOp {
    int operator()(int a, int b) const { return a < b ? a : b; }
};
// SparseTable<int, MinOp> st(a, MinOp{});
} // namespace sparse_table
```

##### Python 3 Template

```python
class SparseTableMin:
    def __init__(self, a: list[int]):
        n = len(a)
        self.lg = [0] * (n + 1)
        for i in range(2, n + 1):
            self.lg[i] = self.lg[i // 2] + 1
        K = self.lg[n] + 1
        self.st = [a[:]]
        for k in range(1, K):
            prev = self.st[k - 1]
            cur = [0] * (n - (1 << k) + 1)
            half = 1 << (k - 1)
            for i in range(len(cur)):
                cur[i] = prev[i] if prev[i] < prev[i + half] else prev[i + half]
            self.st.append(cur)
    def query(self, l: int, r: int) -> int:
        k = self.lg[r - l + 1]
        x = self.st[k][l]
        y = self.st[k][r - (1 << k) + 1]
        return x if x < y else y
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Static array; many range min/max/gcd queries
- LCA via Euler tour + RMQ
- “No updates” explicitly or array fixed after input
- Need \(O(1)\) per query with comfortable \(O(n\log n)\) memory

---

#### 7. Contest WA / TLE / RE Traps

- Using sparse table when updates exist
- Using `+` / matrix mul with overlapping two-block query (wrong — not idempotent)
- `lg` table off-by-one: must use `r-l+1`, not `r-l`
- Forgetting inclusive bounds when porting from segtree habits

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Index-of-minimum (store indices, compare `a[i]`)
- GCD / AND / OR sparse tables (idempotent)
- `<O(n), O(1)>` RMQ via Cartesian + LCA (overkill for CF; classic ST is enough)
- Disjoint sparse table for non-idempotent associative ops (next)

---

#### 11. Typical Problem Archetypes

1. Standard application: static range minimum queries
2. Slightly disguised: range gcd; “can all equal after range?” via min=max
3. Difficult: LCA with Euler tour + RMQ sparse table
4. Very difficult / advanced: combine with Mo / offline when static structure is one layer

---

#### 12. Recognition & Identification Drills

1. Array fixed; \(q\le 10^6\) range minimum queries — need fast answers.
2. Static array; range gcd queries.
3. Tree LCA queries with Euler tour technique.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: static idempotent range queries
- Key invariant: two overlapping \(2^k\) blocks cover any range
- Key formula: \(k=\lfloor\log_2(r-l+1)\rfloor\)
- Complexity: build \(O(n\log n)\), query \(O(1)\)
- Template to remember: `st[k][i] = op(st[k-1][i], st[k-1][i+2^{k-1}])`

---

## 4. Disjoint sparse table

---


---

<a id="topic-2"></a>
### 2. Disjoint Sparse Table

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2500 | **Frequency:** Rare  
> **Prerequisites:** Sparse table, associative ops (semigroup), bit partitioning of ranges  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2500
- Prerequisites: Sparse table, associative ops (semigroup), bit partitioning of ranges

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Classic ST overlaps two blocks — fatal for non-idempotent ops like `+` or matrix multiply. A **disjoint** sparse table precomputes, for each dyadic “block boundary,” prefixes to the left and suffixes to the right so any range splits into **exactly two adjacent** precomputed halves meeting at a power-of-two aligned cut. Associativity alone suffices; idempotence not required. Still static.

---

#### 4. Proof Sketches & Recurrences

Fix size \(n' = 2^{\lceil\log_2 n\rceil}\). For each level \(k\) with block length \(2^k\), at every boundary multiple of \(2^k\), store leftward suffixes and rightward prefixes under `op`. Query \([L,R]\): let \(k = \mathrm{msb}(L\oplus R)\) (highest differing bit); answer is `op(left_prefix, right_prefix)` from that level’s cut — two disjoint halves. Build \(O(n\log n)\), query \(O(1)\) op applications.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) applications of `op`
- Per-query / per-operation: \(O(1)\) applications of `op`
- Total: \(O(n\log n + q)\)
- Memory: \(O(n\log n)\)`

##### C++17 Template

```cpp
namespace disjoint_st {
template <class T, class F>
struct DisjointSparseTable {
    int n, levels;
    vector<vector<T>> pref; // pref[k][i] = fold in direction toward boundary
    F op;
    T id; // unused if queries always nonempty; keep for clarity

    DisjointSparseTable(vector<T> a, F op_, T id_ = T{})
        : n((int)a.size()), op(op_), id(id_) {
        if (n == 0) { levels = 0; return; }
        levels = 32 - __builtin_clz(n);
        int N = 1 << levels;
        a.resize(N, id);
        pref.assign(levels + 1, vector<T>(N, id));
        pref[0] = a;
        for (int k = 1; k <= levels; ++k) {
            int len = 1 << k;
            for (int base = 0; base < N; base += len) {
                int mid = base + (len >> 1);
                pref[k][mid - 1] = a[mid - 1];
                for (int i = mid - 2; i >= base; --i)
                    pref[k][i] = op(a[i], pref[k][i + 1]);
                pref[k][mid] = a[mid];
                for (int i = mid + 1; i < base + len; ++i)
                    pref[k][i] = op(pref[k][i - 1], a[i]);
            }
        }
    }
    T query(int l, int r) const { // inclusive, nonempty
        if (l == r) return pref[0][l];
        int k = 32 - __builtin_clz(l ^ r); // msb index of l^r
        return op(pref[k][l], pref[k][r]);
    }
};
} // namespace disjoint_st
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Static array; associative op; want \(O(1)\) queries without segtree
- Matrix product on subarrays, non-idempotent semigroups
- You already know ST and someone forbids overlapping merges

---

#### 7. Contest WA / TLE / RE Traps

- Using classic overlapping ST for `+` / matrix product
- Empty ranges / \(l>r\) not handled
- Incorrect MSB of `l^r` (`__builtin_clz` width assumptions)
- Padding with wrong identity for the semigroup

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Sum / product / affine composition / small matrix mul
- Fallback: iterative segtree \(O(\log n)\) query is almost always acceptable — DST is micro-opt / elegance

---

#### 11. Typical Problem Archetypes

1. Standard application: static range sum with \(O(1)\) (usually Fenwick/prefix better)
2. Slightly disguised: static range matrix product
3. Difficult: associative custom merge too fat for segtree constants (rare)
4. Very difficult / advanced: combine with monoid ideas in research-style tasks

---

#### 12. Recognition & Identification Drills

1. Static array of \(2\times 2\) matrices; product on subarrays; \(q\) large.
2. Explain why classic sparse table fails for range sum with the two-block trick.
3. Same queries solvable by segtree — when would DST be worth coding?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: static associative non-idempotent \(O(1)\) queries (rare)
- Key invariant: range ↔ two disjoint halves at `msb(l^r)` cut
- Key formula: `op(pref[k][l], pref[k][r])`
- Complexity: \(O(n\log n)\) build, \(O(1)\) query
- Template to remember: build inward prefixes at each dyadic mid; query via `l^r`

---

## 5. Cartesian tree

---


---

<a id="topic-3"></a>
### 3. Cartesian Tree

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Monotone stack, heap+BST properties, RMQ↔LCA equivalence  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Monotone stack, heap+BST properties, RMQ↔LCA equivalence

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Build a binary tree on array indices: inorder = array order (BST on index), heap order on values (e.g. min-heap on \(a_i\)). Range minimum on \([L,R]\) is the LCA of nodes \(L\) and \(R\) in this tree. Conversely, the tree encodes nearest smaller elements: parent = nearest smaller to left/right in the stack construction. One \(O(n)\) monotone stack builds it.

---

#### 4. Proof Sketches & Recurrences

Stack of indices with increasing \(a[\cdot]\) (for min-Cartesian). For each `i` left-to-right: pop until `a[stack.top()] < a[i]` (strictness = tie-break); last popped becomes left child of `i`; `i` becomes right child of new top.  
Heap property + inorder indices ⇒ for range \([L,R]\), the minimum’s index is LCA\((L,R)\). Construction \(O(n)\); then LCA via binary lifting \(O(n\log n)\) prep if needed.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) build; \(+O(n\log n)\) if adding LCA
- Per-query / per-operation: \(O(1)\) / \(O(\log n)\) with LCA; or use tree DP offline
- Total: usually \(O(n)\) + tree processing
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
namespace cartesian {
// Min-Cartesian tree: parent/left/right, root; ties -> first wins (change cmp as needed)
struct CartesianTree {
    int n, root;
    vector<int> l, r, p;
    CartesianTree(const vector<int>& a) : n((int)a.size()), root(-1),
        l(n, -1), r(n, -1), p(n, -1) {
        vector<int> st;
        for (int i = 0; i < n; ++i) {
            int last = -1;
            while (!st.empty() && a[st.back()] > a[i]) {
                last = st.back();
                st.pop_back();
            }
            if (!st.empty()) {
                r[st.back()] = i;
                p[i] = st.back();
            }
            if (last != -1) {
                l[i] = last;
                p[last] = i;
            }
            st.push_back(i);
        }
        root = st.empty() ? -1 : st.front();
        while (root != -1 && p[root] != -1) root = p[root];
    }
};
} // namespace cartesian
```

##### Python 3 Template

```python
def cartesian_tree(a: list[int]):
    n = len(a)
    left, right, parent = [-1] * n, [-1] * n, [-1] * n
    st: list[int] = []
    for i, v in enumerate(a):
        last = -1
        while st and a[st[-1]] > v:
            last = st.pop()
        if st:
            right[st[-1]] = i
            parent[i] = st[-1]
        if last != -1:
            left[i] = last
            parent[last] = i
        st.append(i)
    root = st[0] if st else -1
    while root != -1 and parent[root] != -1:
        root = parent[root]
    return root, left, right, parent
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Nearest greater/smaller to left/right → tree edges
- Histogram largest rectangle / contribution of each element as minimum
- Want to recurse on “range split by minimum”
- RMQ reductions, treap-like structure with priorities = values

---

#### 7. Contest WA / TLE / RE Traps

- Strict vs non-strict inequality on ties (duplicate values) — define policy
- Assuming root is `st.back()` instead of walking parents / `st.front()`
- Confusing min-Cartesian with max-Cartesian for “nearest greater”
- Using as online RMQ without LCA preprocessing

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Max-Cartesian (nearest greater)
- Recursive D&C on ranges “split by minimum” without storing tree
- Bridge to treaps: random priorities ≈ Cartesian on `(key, priority)`

---

#### 11. Typical Problem Archetypes

1. Standard application: nearest smaller to left/right in one pass
2. Slightly disguised: sum of range minimums over all subarrays via contribution
3. Difficult: tree DP on Cartesian tree of the array
4. Very difficult / advanced: RMQ↔LCA reductions; persistent / offline structures on Cartesian

---

#### 12. Recognition & Identification Drills

1. For each index, find nearest strictly smaller to the left and to the right.
2. Array; compute \(\sum_{l\le r} \min(a_l,\ldots,a_r)\) in \(O(n)\).
3. Recursively split ranges at their minimum — need the explicit tree for DP.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: nearest smaller/greater, range-min D&C tree, RMQ↔LCA
- Key invariant: heap on values + inorder = indices
- Key formula: parent = nearest smaller (stack); RMQ = LCA
- Complexity: \(O(n)\) build
- Template to remember: monotone stack left-to-right linking `l`/`r`/`p`

---

[Hub](05-advanced-data-structures.md) · [Part b: Treap → LCT](05-b-treaps-ordered-stats-lct.md)

---


---

<a id="topic-4"></a>
### 4. Treap (Explicit + Implicit)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** BST split/merge mental model, random priorities, subtree sizes  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: BST split/merge mental model, random priorities, subtree sizes

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

A treap is a BST on keys and a heap on random priorities — equivalently a Cartesian tree of `(key, priority)`. **Split/merge** replace insert/erase rotations as the API: any segment of keys (or implicit indices) can be cut out and glued back in \(O(\log n)\) expected. **Implicit treap** uses subtree size as the key → sequences with insert/erase/reverse/lazy become natural.

---

#### 4. Proof Sketches & Recurrences

Priorities uniform random ⇒ expected heap shape is random binary tree ⇒ expected depth \(O(\log n)\).  
`merge(L,R)` assumes \(\max key(L) \le \min key(R)\); recursively attach by priority.  
`split(T,k) → (A,B)` with keys \(<k\) / \(\ge k\) (explicit) or size `k` | rest (implicit).  
Insert = split by key + merge three parts; erase similar. Implicit: rotate/reverse via lazy XOR flag on node.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) expected to build by merges
- Per-query / per-operation: \(O(\log n)\) expected
- Total: \(O((n+q)\log n)\) expected
- Memory: \(O(n)\) nodes`

##### C++17 Template

```cpp
namespace treap {
using ll = long long;
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

struct Node {
    int prio, sz;
    ll val, sum;
    bool rev;
    Node *l, *r;
    Node(ll v) : prio(rng()), sz(1), val(v), sum(v), rev(false), l(nullptr), r(nullptr) {}
};

int size(Node* t) { return t ? t->sz : 0; }
ll get_sum(Node* t) { return t ? t->sum : 0; }

void pull(Node* t) {
    if (!t) return;
    t->sz = 1 + size(t->l) + size(t->r);
    t->sum = t->val + get_sum(t->l) + get_sum(t->r);
}
void push(Node* t) {
    if (!t || !t->rev) return;
    swap(t->l, t->r);
    if (t->l) t->l->rev ^= 1;
    if (t->r) t->r->rev ^= 1;
    t->rev = false;
}

void split(Node* t, int k, Node*& a, Node*& b) { // first k elements -> a
    if (!t) { a = b = nullptr; return; }
    push(t);
    if (size(t->l) >= k) {
        split(t->l, k, a, t->l);
        b = t;
        pull(b);
    } else {
        split(t->r, k - size(t->l) - 1, t->r, b);
        a = t;
        pull(a);
    }
}

Node* merge(Node* a, Node* b) {
    if (!a || !b) return a ? a : b;
    push(a); push(b);
    if (a->prio < b->prio) {
        a->r = merge(a->r, b);
        pull(a);
        return a;
    }
    b->l = merge(a, b->l);
    pull(b);
    return b;
}

void reverse_seg(Node*& root, int ql, int qr) { // 0-indexed inclusive
    Node *a, *b, *c;
    split(root, ql, a, b);
    split(b, qr - ql + 1, b, c);
    if (b) b->rev ^= 1;
    root = merge(a, merge(b, c));
}
} // namespace treap
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Need split array/string into pieces, reverse a segment, re-concatenate
- Ordered multiset with custom aggregates on key ranges
- “BST + heap priorities” or policy-based structure insufficient (need lazy/reverse)
- Sequence problems where splay/LCT would be overkill

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `push` before reading children / sizes
- Wrong split size: `k - size(l) - 1` off-by-one
- Using `rand()` without wide priority space → degeneration
- Not `pull`ing after merge/split
- Recursion depth on adversarial priorities (use `mt19937`, not fixed)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Explicit-key treap:** split by key instead of size
- **Lazy add on segment:** push additive tag like segtree
- **Persistent treap:** copy nodes on path (rare)
- vs **PBDS:** PBDS shorter for pure order stats; treap wins for sequence lazy

---

#### 11. Typical Problem Archetypes

1. Standard application: insert/erase in sorted order by key
2. Slightly disguised: reverse subarray + sum queries (implicit)
3. Difficult: cut/paste substrings; maintain hashes on treap
4. Very difficult / advanced: treap on tree rerooting / geometric divide

---

#### 12. Recognition & Identification Drills

1. Array; reverse \([l,r]\) online many times; query sum on \([L,R]\).
2. Maintain a string; cut substring and paste elsewhere.
3. Multiset with “sum of keys in rank range \([a,b]\)”.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: split/merge sequences or keyed BSTs with aggregates
- Key invariant: BST(keys or implicit index) + heap(priorities)
- Key formula: split by size/key + merge by priority
- Complexity: expected \(O(\log n)\)
- Template to remember: `split` / `merge` / lazy `rev` push

---

## 7. Splay tree concepts

---


---

<a id="topic-5"></a>
### 5. Splay Tree (Concepts)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** Niche | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** BST rotations, amortized analysis intuition; treap usually preferred for sequences  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: BST rotations, amortized analysis intuition; treap usually preferred for sequences

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Splay trees move the accessed node to the root via zig / zig-zig / zig-zag rotations. No random priorities: amortization gives \(O(\log n)\) per op. In contests, **implicit treaps replace most sequence uses**; splay matters mainly as the **access primitive inside link-cut trees** (preferred-path representation). Mark **Niche for early ROI** — learn rotations + “access brings node to root,” not a full production splay library first.

---

#### 4. Proof Sketches & Recurrences

Potential = sum of log subtree sizes (or ranks). Zig-zig / zig-zag cases telescope so a sequence of \(m\) ops on \(n\) nodes is \(O((m+n)\log n)\) amortized. Single ops can be \(O(n)\) worst-case — important for TL paranoia vs treap’s expected bounds.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) to build a chain then splay, or insert one-by-one amortized \(O(n\log n)\)
- Per-query / per-operation: amortized \(O(\log n)\); worst single \(O(n)\)
- Total: amortized \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
namespace splay_concepts {
// Minimal rotate + splay sketch (explicit parent pointers). Niche — prefer treap for sequences.
struct Node {
    Node *l, *r, *p;
    int sz;
    Node() : l(nullptr), r(nullptr), p(nullptr), sz(1) {}
};

void pull(Node* x) {
    x->sz = 1 + (x->l ? x->l->sz : 0) + (x->r ? x->r->sz : 0);
}
void rotate(Node* x) {
    Node* p = x->p;
    Node* g = p->p;
    if (p->l == x) {
        p->l = x->r;
        if (x->r) x->r->p = p;
        x->r = p;
    } else {
        p->r = x->l;
        if (x->l) x->l->p = p;
        x->l = p;
    }
    p->p = x;
    x->p = g;
    if (g) {
        if (g->l == p) g->l = x;
        else if (g->r == p) g->r = x;
    }
    pull(p);
    pull(x);
}
void splay(Node* x) {
    while (x->p) {
        Node* p = x->p;
        Node* g = p->p;
        if (!g) rotate(x);
        else if ((g->l == p) == (p->l == x)) { // zig-zig
            rotate(p);
            rotate(x);
        } else { // zig-zag
            rotate(x);
            rotate(x);
        }
    }
}
} // namespace splay_concepts
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Problem mentions splay / LCT / dynamic trees
- Need amortised BST without RNG
- Implementing LCT preferred paths
- Interview question on zig-zig vs zig-zag (rare in CF)

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting parent updates on both sides of rotate
- Not handling root / `g` null when linking after rotate
- Expecting strict \(O(\log n)\) worst-case per op
- Reimplementing splay for a problem a treap solves in 40 lines

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Implicit splay (size keys) for sequences — same niche as implicit treap
- Top tree / LCT built on splay
- Tango trees etc. — not contest-relevant

---

#### 11. Typical Problem Archetypes

1. Standard application: textbook BST with amortised access (rare as standalone CF task)
2. Slightly disguised: sequence maintenance where author solution is splay
3. Difficult: LCT path aggregates (depends on splay access)
4. Very difficult / advanced: full LCT + subtree mods

---

#### 12. Recognition & Identification Drills

1. Why zig-zig rotates parent first, then node?
2. Given parent pointers, bring node `u` to root of its BST.
3. Contrast: when would you code treap instead of splay for reverse-on-segment?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: LCT building block; rarely standalone in CF
- Key invariant: accessed node becomes root; amortised balance
- Key formula: zig / zig-zig / zig-zag
- Complexity: amortised \(O(\log n)\)
- Template to remember: `rotate` + `splay` loop; prefer treap otherwise

---

## 8. Randomized BST

---


---

<a id="topic-6"></a>
### 6. Randomized BST

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** BST insert, treap idea; knowing treap is enough for contests  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: BST insert, treap idea; knowing treap is enough for contests

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

A randomized BST inserts a new key at the root with probability \(1/(n+1)\) (or recursively), else recurses left/right — yielding the same distribution as a random permutation insertion order / treap priorities. **In practice you implement a treap** (explicit random priority) rather than the recursive “root with prob \(1/(size+1)\)” form. Treat this as the theory twin of treaps.

---

#### 4. Proof Sketches & Recurrences

For a fixed set of \(n\) distinct keys, every key equally likely to be root ⇒ recurrence \(T(n)=\Theta(n)+\frac{1}{n}\sum_i(T(i-1)+T(n-i))\) ⇒ expected depth \(O(\log n)\). Equivalent to: assign random priorities, build Cartesian tree (treap).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) expected builds
- Per-query / per-operation: \(O(\log n)\) expected
- Total: \(O((n+q)\log n)\) expected
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
namespace rbst {
// Insert-at-root randomized BST (theoretical twin of treap). Prefer treap:: in contests.
struct Node {
    int key, sz;
    Node *l, *r;
    Node(int k) : key(k), sz(1), l(nullptr), r(nullptr) {}
};
int size(Node* t) { return t ? t->sz : 0; }
void pull(Node* t) { if (t) t->sz = 1 + size(t->l) + size(t->r); }

Node* rotate_right(Node* p) {
    Node* x = p->l;
    p->l = x->r;
    x->r = p;
    pull(p);
    pull(x);
    return x;
}
Node* rotate_left(Node* p) {
    Node* x = p->r;
    p->r = x->l;
    x->l = p;
    pull(p);
    pull(x);
    return x;
}

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

Node* insert(Node* t, int key) {
    if (!t) return new Node(key);
    // probability 1/(sz+1) to become new root
    if (uniform_int_distribution<int>(0, size(t))(rng) == 0) {
        // insert at root: standard BST insert then rotate up (simplified path)
        if (key < t->key) {
            t->l = insert(t->l, key);
            t = rotate_right(t);
        } else {
            t->r = insert(t->r, key);
            t = rotate_left(t);
        }
        return t;
    }
    if (key < t->key) t->l = insert(t->l, key);
    else t->r = insert(t->r, key);
    pull(t);
    return t;
}
} // namespace rbst
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Statement or editorial says “randomized BST”
- Analysis problem about expected depth
- You want treap semantics without storing priorities (insert-at-root with probability)

---

#### 7. Contest WA / TLE / RE Traps

- Biased RNG → unbalanced trees
- Implementing RBST poorly when `policy_based_data_structures` or Fenwick suffice
- Off-by-one in probability \(1/(sz+1)\)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Treap (preferred implementation)
- Zipper / rope randomized structures
- Skip lists — another randomized ordered dictionary (rare in CF)

---

#### 11. Typical Problem Archetypes

1. Standard application: ordered set with expected log ops
2. Slightly disguised: editorial proves expected depth via random root
3. Difficult: same as hard treap tasks
4. Very difficult / advanced: analysis of random recursive trees

---

#### 12. Recognition & Identification Drills

1. Show expected depth is \(O(\log n)\) if each key equally likely root.
2. Map “insert at root with prob \(1/(n+1)\)” to treap priorities.
3. Given PBDS exists, when is RBST/treap still needed?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: theory / interviews; in CF implement **treap**
- Key invariant: uniform random root among keys in subtree
- Key formula: \(P(\text{root})=1/(\text{size})\)
- Complexity: expected \(O(\log n)\)
- Template to remember: equivalent to treap; prefer priorities + split/merge

---

## 9. Ordered statistics

---


---

<a id="topic-7"></a>
### 7. Ordered Statistics (PBDS / Fenwick / Treap)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** Coordinate compression, Fenwick or BST; GCC PBDS extension  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: Coordinate compression, Fenwick or BST; GCC PBDS extension

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Need **rank** (how many \(< x\)) and **select** (k-th smallest) under online inserts/erases. Three contest tools: (1) **GNU PBDS** `tree` with `order_of_key` / `find_by_order` — shortest; (2) **Fenwick/segtree on compressed values** as frequency array — safest portable; (3) **treap** when you also need splits/aggregates. Prefer PBDS or Fenwick over rolling your own BST for pure order stats.

---

#### 4. Proof Sketches & Recurrences

Compress values to \(1..m\). Fenwick `add(rank(x),+1)` on insert; `order = sumPrefix(rank(x)-1)`; k-th = Fenwick `lower_bound(k)`. PBDS maintains a BST augmented with subtree sizes — same select/rank in \(O(\log n)\). Duplicates: store `{value, unique id}` pairs in PBDS; Fenwick naturally counts multiplicity.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) compression
- Per-query / per-operation: \(O(\log n)\)
- Total: \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
// Headers (file scope):
// #include <ext/pb_ds/assoc_container.hpp>
// #include <ext/pb_ds/tree_policy.hpp>

namespace ordstats {
using namespace __gnu_pbds;

template <class T>
using ordered_set = tree<T, null_type, less<T>, rb_tree_tag,
                         tree_order_statistics_node_update>;
// ordered_set<pair<int,int>> st;
// st.insert({x, id});
// st.order_of_key({x, -1});           // count strictly < x
// *st.find_by_order(k);               // k-th (0-indexed)

// Portable Fenwick frequency version (values compressed to 1..m).
// Uses fenwick::BIT from 05-a-fenwick-sparse-tables-cartesian.md.
struct CompressedOrder {
    vector<int> coords;
    fenwick::BIT bit;
    void init(vector<int> all) {
        coords = all;
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());
        bit = fenwick::BIT((int)coords.size());
    }
    int rid(int x) const { // 1-indexed rank
        return (int)(lower_bound(coords.begin(), coords.end(), x) - coords.begin()) + 1;
    }
    void insert(int x) { bit.add(rid(x), +1); }
    void erase(int x) { bit.add(rid(x), -1); }
    int order_of_key(int x) const { // # strictly < x
        int r = (int)(lower_bound(coords.begin(), coords.end(), x) - coords.begin());
        return (int)bit.sumPrefix(r);
    }
    int find_by_order(int k) const { // 0-indexed; needs k in range
        int idx = bit.lower_bound(k + 1);
        return coords[idx - 1];
    }
};
} // namespace ordstats
```

##### Python 3 Template

```python
# Assume BIT from Section 05a; coords = sorted unique values
def rid(coords, x):
    from bisect import bisect_left
    return bisect_left(coords, x) + 1

# insert: bit.add(rid(coords, x), +1)
# order_of_key: bit.sum_prefix(bisect_left(coords, x))
# kth: bit.lower_bound(k+1) -> coords[idx-1]
```

---

#### 6. Recognition Trigger Signals & Heuristics

- “k-th smallest online,” “count elements \(< x\)”
- Inversions with updates; dynamic median
- Multiset + rank queries
- Sliding window k-th (Fenwick / PBDS / policy two-heaps variants)

---

#### 7. Contest WA / TLE / RE Traps

- PBDS `less` vs `less_equal` for multisets — prefer `pair<value,id>` with `less`
- `find_by_order` is 0-indexed; off-by-one vs problem statements
- Fenwick erase without checking presence → negative freqs break `lower_bound`
- Forgetting to compress all query values that may appear as keys

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Dynamic median (two ordered multisets / PBDS)
- Count inversions online
- Order stats on segtree merges (merge-sort tree — different section family)
- Implicit treap ranks by position not value

---

#### 11. Typical Problem Archetypes

1. Standard application: online k-th / rank in a multiset
2. Slightly disguised: inversions; “how many in \([L,R]\)” with Fenwick of freqs
3. Difficult: k-th on path / subtree (HLD + BIT / persistent segtree)
4. Very difficult / advanced: with range updates on values (heavier structures)

---

#### 12. Recognition & Identification Drills

1. Maintain a multiset; answer “k-th smallest” after inserts/deletes.
2. Stream of numbers; after each insert print number of inversions so far.
3. Compressed values; queries “count in \([L,R]\) currently present.”

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: online rank / select
- Key invariant: augmented sizes or frequency prefix sums
- Key formula: `order_of_key` / `find_by_order` or Fenwick prefix + binary lift
- Complexity: \(O(\log n)\)
- Template to remember: PBDS pair-id OR Fenwick on ranks

---

## 10. Link-cut tree

---


---

<a id="topic-8"></a>
### 8. Link-Cut Tree (Concept + Preferred-Path Sketch)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** Niche | **Rating Range:** 2600–3500 | **Frequency:** Rare  
> **Prerequisites:** Splay concepts, tree path aggregates, understanding HLD as the static analogue  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2600–3500
- Prerequisites: Splay concepts, tree path aggregates, understanding HLD as the static analogue

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

##### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

##### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

##### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

##### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

#### 3. Core Intuition & Problem Framing

Represent a forest as **preferred paths** (heavy-ish chains that change dynamically), each path stored in a **splay tree** keyed by depth. `access(v)` splays `v` and reassembles the preferred path from root to `v`. `link` / `cut` change forest edges; path aggregates (sum/min) live in the splay. **Early ROI: Niche** — for almost all CF/ICPC tasks prefer **HLD + segtree**, Euler tour, or DSU. Only invest in full LCT when the forest is truly dynamic (edges link/cut online) and path queries matter.

If a full production LCT is too large for this masterclass week: solid concept + `access` / splay / preferred-path sketch below is enough; treat complete `link`/`cut`/`path_aggregate` libraries as reference code to paste when forced.

---

#### 4. Proof Sketches & Recurrences

Each real tree edge is either preferred or not. Preferred paths partition nodes. Within a path, splay by depth; `path-parent` pointer connects path head to light parent.  
`access(v)`: splay up preferred path, disconnect right child (deeper nodes no longer preferred), then splice into parent path — repeat until root. After `access(v)`, root-to-`v` is one preferred path with `v` at the right end (depth order).  
`link(u,v)`: make `u` root (`evert`), `access(v)`, attach. `cut`: `access` + disconnect parent edge in splay.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) nodes
- Per-query / per-operation: amortized \(O(\log n)\) for access/link/cut/path
- Total: amortized \(O(q\log n)\)
- Memory: \(O(n)\)`

##### C++17 Template

```cpp
namespace lct {
// Niche sketch: node + splay + access. Enough to remember preferred-path mechanics.
// Full contest LCT also needs: evert/makeroot, link, cut, path_sum, lazy push — long.
struct Node {
    Node *l, *r, *p;
    bool rev;
    // ll val, sum; // add for path aggregates
    Node() : l(nullptr), r(nullptr), p(nullptr), rev(false) {}
};

bool is_root(Node* x) {
    return !x->p || (x->p->l != x && x->p->r != x);
}
void push(Node* x) {
    if (!x || !x->rev) return;
    swap(x->l, x->r);
    if (x->l) x->l->rev ^= 1;
    if (x->r) x->r->rev ^= 1;
    x->rev = false;
}
void rotate(Node* x) {
    Node* p = x->p;
    Node* g = p->p;
    push(p); push(x);
    if (p->l == x) {
        p->l = x->r;
        if (x->r) x->r->p = p;
        x->r = p;
    } else {
        p->r = x->l;
        if (x->l) x->l->p = p;
        x->l = p;
    }
    p->p = x;
    x->p = g;
    if (g && !is_root(p)) {
        if (g->l == p) g->l = x;
        else g->r = x;
    }
}
void splay(Node* x) {
    while (!is_root(x)) {
        Node* p = x->p;
        Node* g = p->p;
        if (!is_root(p)) push(g);
        push(p); push(x);
        if (!is_root(p)) {
            if ((p->l == x) == (g->l == p)) rotate(p);
            else rotate(x);
        }
        rotate(x);
    }
}
void access(Node* x) {
    Node* last = nullptr;
    for (Node* y = x; y; y = y->p) {
        splay(y);
        y->r = last;      // prefer path down to x
        last = y;
    }
    splay(x);
}
void makeroot(Node* x) { // evert
    access(x);
    x->rev ^= 1;
    push(x);
}
// link(u,v): makeroot(u); u->p = v;
// cut(u,v):  makeroot(u); access(v); /* v->l == u */ v->l->p = nullptr; v->l = nullptr;
} // namespace lct
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Online link and cut edges in a forest + path min/sum
- “Dynamic tree” in editorial; LCT / top trees mentioned
- HLD fails because tree shape changes
- Subtree queries on dynamic trees (even harder — often needs ST-trees / Euler+LCT hybrids)

---

#### 7. Contest WA / TLE / RE Traps

- Confusing path-parent (`p` when `is_root`) with splay parent
- Forgetting `rev` / `makeroot` before link/cut
- Using LCT when HLD on a static tree suffices
- Subtree ≠ path: classic LCT does paths; subtrees need extra orientation tricks

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Path sum / min / XOR with pull on splay nodes
- LCT + lazy path add
- Euler-tour + LCT hybrids for subtrees (expert niche)
- AAA tree / top trees — theory generalizations

---

#### 11. Typical Problem Archetypes

1. Standard application: maintain forest, query path XOR/min after links/cuts
2. Slightly disguised: dynamic connectivity in trees with weights
3. Difficult: dynamic tree DP via LCT
4. Very difficult / advanced: subtree updates on dynamic trees; combining LCT with segtree on time

---

#### 12. Recognition & Identification Drills

1. Forest starts as \(n\) isolated vertices; process `link`, `cut`, `path_sum` online.
2. Same queries but tree is static — which structure should you use instead?
3. After `access(v)`, what does the preferred-path partition look like?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: truly dynamic forest + path aggregates (Niche)
- Key invariant: preferred paths in splay trees by depth; `access` builds root→v
- Key formula: `access` / `makeroot` / `link` / `cut`
- Complexity: amortized \(O(\log n)\)
- Template to remember: splay + `access` loop setting `y->r = last`; else use HLD

---

[Hub](05-advanced-data-structures.md) · [Part a: Fenwick → Cartesian](05-a-fenwick-sparse-tables-cartesian.md)

---


---
