# Sparse Table (RMQ / Idempotent Range Queries)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** S-tier | **Rating Range:** 1400–1900 | **Frequency:** Common  
> **Prerequisites:** Binary lifting idea, idempotent semigroup ops (min, max, gcd, AND, OR)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–1900
- Prerequisites: Binary lifting idea, idempotent semigroup ops (min, max, gcd, AND, OR)

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Data Structures encompass persistent segment trees (versioned immutability), Treaps (randomized priority binary search trees for implicit sequence operations), Cartesian Trees, and Link-Cut Trees (dynamic forest connectivity).

### Fundamental Theorems & Invariants

- **Path Copy Persistence:** Updating a persistent data structure creates only $\mathcal{O}(\log N)$ new nodes along the modified path, sharing all unchanged subtrees with previous versions in $\mathcal{O}(\log N)$ space per version.
- **Treap Random Priority Balance:** Assigning uniform random priorities $\text{prio} \sim \text{Uniform}(0, 2^{31}-1)$ to each key ensures the expected tree depth is $2 \ln N \approx 1.386 \log_2 N$.
- **Cartesian Tree Linear Construction:** A Cartesian tree where each node is the range minimum can be built in strictly $\mathcal{O}(N)$ time using a monotonic stack of rightmost spine ancestors.
- **Link-Cut Tree Preferred Path Invariant:** Decomposing a tree into vertex-disjoint preferred paths maintained via Splay trees supports dynamic `link`, `cut`, and path aggregates in amortized $\mathcal{O}(\log N)$ time.

### Algorithmic Execution Blueprint

1. **Persistent Update:** `int update(int prev, int l, int r, int pos, int val)` creates a clone node $curr$, copies children from $prev$, recursively updates the target branch, and returns $curr$.
2. **Treap Split:** `split(node, key, leftTree, rightTree)` partitions tree into keys $\le key$ and keys $> key$.
3. **Treap Merge:** `merge(node, leftTree, rightTree)` assumes all keys in $leftTree$ are smaller than $rightTree$; places highest priority at root.

### Closed-Form Invariant Equations

$$\text{Depth}(\text{Treap}) = \mathcal{O}(\log N) \quad \text{(with probability } 1 - N^{-c}\text{)}, \quad \text{Space}(\text{PersistSeg}) = \mathcal{O}(N \log N + Q \log N)$$

### Structural Edge Cases & Assumptions

- Persistent segment trees over dynamic coordinate spaces require dynamic pointer allocation; allocate a pool of at least $40N$ nodes to prevent runtime memory exhaustion.
- Always push lazy tags before performing `split` and `merge` in implicit Treaps (e.g. range reversals).
- Link-Cut Trees require `splay(u)` and `access(u)` before querying path aggregates or modifying edges.

---

## 3. Core Intuition & Problem Framing

Precompute every interval whose length is a power of two. For idempotent ops, any \([L,R]\) is the op of **two overlapping** \(2^k\) blocks covering it — overlap is fine because \(x\oplus x=x\). That gives true \(O(1)\) queries after \(O(n\log n)\) build. No updates: if the array mutates, use a segtree/Fenwick instead.

---

## 4. Proof Sketches & Recurrences

\[
st[k][i] = \mathrm{op}(st[k-1][i], st[k-1][i+2^{k-1}])
\]
For query \([L,R]\) (0-index), \(len=R-L+1\), \(k=\lfloor\log_2 len\rfloor\):
\[
\mathrm{op}(st[k][L], st[k][R-2^k+1]).
\]
Works iff `op` is idempotent (and associative). For pure associative non-idempotent ops, use disjoint sparse table or segtree.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\)
- Per-query / per-operation: \(O(1)\)
- Total: \(O(n\log n + q)\)
- Memory: \(O(n\log n)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Static array; many range min/max/gcd queries
- LCA via Euler tour + RMQ
- “No updates” explicitly or array fixed after input
- Need \(O(1)\) per query with comfortable \(O(n\log n)\) memory

---

## 7. Contest WA / TLE / RE Traps

- Using sparse table when updates exist
- Using `+` / matrix mul with overlapping two-block query (wrong — not idempotent)
- `lg` table off-by-one: must use `r-l+1`, not `r-l`
- Forgetting inclusive bounds when porting from segtree habits

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-863D | Almost Difference | 2000 | Implicit Treap, Coordinate Tracking | Implicit Treap split/merge or reverse query coordinate tracking. | [Solve Problem](https://codeforces.com/contest/863/problem/D) |
| Codeforces | CF-702F | T-Shirts | 2700 | Treap, Small to Large | Treap split by affordability, subtract price, and re-insert with small-to-large merging. | [Solve Problem](https://codeforces.com/contest/702/problem/F) |
| Codeforces | CF-1175E | Minimal Segment Cover | 2200 | Binary Lifting, Sparse Table, Greedy | Binary lifting on greedy rightmost transitions over interval endpoints. | [Solve Problem](https://codeforces.com/contest/1175/problem/E) |
| Codeforces | CF-1144F | Graph Without Long Directed Paths | 1700 | DSU, Graphs, Bipartite | Bipartite graph 2-coloring for sink-source directed orientations. | [Solve Problem](https://codeforces.com/contest/1144/problem/F) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Treap (Cartesian Tree with Random Priorities)](https://cp-algorithms.com/data_structures/treap.html)
- **[CP-Algorithms]** [CP-Algorithms: Sparse Table RMQ](https://cp-algorithms.com/data_structures/sparse-table.html)
- **[USACO Guide]** [USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)](https://usaco.guide/adv/lct)
- **[YouKn0wWho]** [YouKn0wWho Academy: PBDS Policy Based Data Structures](https://youkn0wwho.academy/topic-list#pbds)

---

## 10. Algorithmic Variants & Advanced Extensions

- Index-of-minimum (store indices, compare `a[i]`)
- GCD / AND / OR sparse tables (idempotent)
- `<O(n), O(1)>` RMQ via Cartesian + LCA (overkill for CF; classic ST is enough)
- Disjoint sparse table for non-idempotent associative ops (next)

---

## 11. Typical Problem Archetypes

1. Standard application: static range minimum queries
2. Slightly disguised: range gcd; “can all equal after range?” via min=max
3. Difficult: LCA with Euler tour + RMQ sparse table
4. Very difficult / advanced: combine with Mo / offline when static structure is one layer

---

## 12. Recognition & Identification Drills

1. Array fixed; \(q\le 10^6\) range minimum queries — need fast answers.
2. Static array; range gcd queries.
3. Tree LCA queries with Euler tour technique.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: static idempotent range queries
- Key invariant: two overlapping \(2^k\) blocks cover any range
- Key formula: \(k=\lfloor\log_2(r-l+1)\rfloor\)
- Complexity: build \(O(n\log n)\), query \(O(1)\)
- Template to remember: `st[k][i] = op(st[k-1][i], st[k-1][i+2^{k-1}])`

---

## 4. Disjoint sparse table

---
