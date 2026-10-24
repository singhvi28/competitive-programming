# 3. Cartesian Tree

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** B-tier | **Rating Range:** 1900–2500 | **Frequency:** Occasional  
> **Prerequisites:** Monotone stack, heap+BST properties, RMQ↔LCA equivalence  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2500
- Prerequisites: Monotone stack, heap+BST properties, RMQ↔LCA equivalence

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

Build a binary tree on array indices: inorder = array order (BST on index), heap order on values (e.g. min-heap on \(a_i\)). Range minimum on \([L,R]\) is the LCA of nodes \(L\) and \(R\) in this tree. Conversely, the tree encodes nearest smaller elements: parent = nearest smaller to left/right in the stack construction. One \(O(n)\) monotone stack builds it.

---

## 4. Proof Sketches & Recurrences

Stack of indices with increasing \(a[\cdot]\) (for min-Cartesian). For each `i` left-to-right: pop until `a[stack.top()] < a[i]` (strictness = tie-break); last popped becomes left child of `i`; `i` becomes right child of new top.  
Heap property + inorder indices ⇒ for range \([L,R]\), the minimum’s index is LCA\((L,R)\). Construction \(O(n)\); then LCA via binary lifting \(O(n\log n)\) prep if needed.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) build; \(+O(n\log n)\) if adding LCA
- Per-query / per-operation: \(O(1)\) / \(O(\log n)\) with LCA; or use tree DP offline
- Total: usually \(O(n)\) + tree processing
- Memory: \(O(n)\)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Nearest greater/smaller to left/right → tree edges
- Histogram largest rectangle / contribution of each element as minimum
- Want to recurse on “range split by minimum”
- RMQ reductions, treap-like structure with priorities = values

---

## 7. Contest WA / TLE / RE Traps

- Strict vs non-strict inequality on ties (duplicate values) — define policy
- Assuming root is `st.back()` instead of walking parents / `st.front()`
- Confusing min-Cartesian with max-Cartesian for “nearest greater”
- Using as online RMQ without LCA preprocessing

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

- Max-Cartesian (nearest greater)
- Recursive D&C on ranges “split by minimum” without storing tree
- Bridge to treaps: random priorities ≈ Cartesian on `(key, priority)`

---

## 11. Typical Problem Archetypes

1. Standard application: nearest smaller to left/right in one pass
2. Slightly disguised: sum of range minimums over all subarrays via contribution
3. Difficult: tree DP on Cartesian tree of the array
4. Very difficult / advanced: RMQ↔LCA reductions; persistent / offline structures on Cartesian

---

## 12. Recognition & Identification Drills

1. For each index, find nearest strictly smaller to the left and to the right.
2. Array; compute \(\sum_{l\le r} \min(a_l,\ldots,a_r)\) in \(O(n)\).
3. Recursively split ranges at their minimum — need the explicit tree for DP.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: nearest smaller/greater, range-min D&C tree, RMQ↔LCA
- Key invariant: heap on values + inorder = indices
- Key formula: parent = nearest smaller (stack); RMQ = LCA
- Complexity: \(O(n)\) build
- Template to remember: monotone stack left-to-right linking `l`/`r`/`p`

---

[Hub](05-advanced-data-structures.md) · [Part b: Treap → LCT](05-b-treaps-ordered-stats-lct.md)

---
