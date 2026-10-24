# Randomized BST

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** C-tier | **Rating Range:** 2000–2600 | **Frequency:** Rare  
> **Prerequisites:** BST insert, treap idea; knowing treap is enough for contests  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: BST insert, treap idea; knowing treap is enough for contests

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

A randomized BST inserts a new key at the root with probability \(1/(n+1)\) (or recursively), else recurses left/right — yielding the same distribution as a random permutation insertion order / treap priorities. **In practice you implement a treap** (explicit random priority) rather than the recursive “root with prob \(1/(size+1)\)” form. Treat this as the theory twin of treaps.

---

## 4. Proof Sketches & Recurrences

For a fixed set of \(n\) distinct keys, every key equally likely to be root ⇒ recurrence \(T(n)=\Theta(n)+\frac{1}{n}\sum_i(T(i-1)+T(n-i))\) ⇒ expected depth \(O(\log n)\). Equivalent to: assign random priorities, build Cartesian tree (treap).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) expected builds
- Per-query / per-operation: \(O(\log n)\) expected
- Total: \(O((n+q)\log n)\) expected
- Memory: \(O(n)\)`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Statement or editorial says “randomized BST”
- Analysis problem about expected depth
- You want treap semantics without storing priorities (insert-at-root with probability)

---

## 7. Contest WA / TLE / RE Traps

- Biased RNG → unbalanced trees
- Implementing RBST poorly when `policy_based_data_structures` or Fenwick suffice
- Off-by-one in probability \(1/(sz+1)\)

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

- Treap (preferred implementation)
- Zipper / rope randomized structures
- Skip lists — another randomized ordered dictionary (rare in CF)

---

## 11. Typical Problem Archetypes

1. Standard application: ordered set with expected log ops
2. Slightly disguised: editorial proves expected depth via random root
3. Difficult: same as hard treap tasks
4. Very difficult / advanced: analysis of random recursive trees

---

## 12. Recognition & Identification Drills

1. Show expected depth is \(O(\log n)\) if each key equally likely root.
2. Map “insert at root with prob \(1/(n+1)\)” to treap priorities.
3. Given PBDS exists, when is RBST/treap still needed?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: theory / interviews; in CF implement **treap**
- Key invariant: uniform random root among keys in subtree
- Key formula: \(P(\text{root})=1/(\text{size})\)
- Complexity: expected \(O(\log n)\)
- Template to remember: equivalent to treap; prefer priorities + split/merge

---

## 9. Ordered statistics

---
