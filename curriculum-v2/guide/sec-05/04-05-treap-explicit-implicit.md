# 4. Treap (Explicit + Implicit)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** BST split/merge mental model, random priorities, subtree sizes  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: BST split/merge mental model, random priorities, subtree sizes

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

A treap is a BST on keys and a heap on random priorities — equivalently a Cartesian tree of `(key, priority)`. **Split/merge** replace insert/erase rotations as the API: any segment of keys (or implicit indices) can be cut out and glued back in \(O(\log n)\) expected. **Implicit treap** uses subtree size as the key → sequences with insert/erase/reverse/lazy become natural.

---

## 4. Proof Sketches & Recurrences

Priorities uniform random ⇒ expected heap shape is random binary tree ⇒ expected depth \(O(\log n)\).  
`merge(L,R)` assumes \(\max key(L) \le \min key(R)\); recursively attach by priority.  
`split(T,k) → (A,B)` with keys \(<k\) / \(\ge k\) (explicit) or size `k` | rest (implicit).  
Insert = split by key + merge three parts; erase similar. Implicit: rotate/reverse via lazy XOR flag on node.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n\log n)\) expected to build by merges
- Per-query / per-operation: \(O(\log n)\) expected
- Total: \(O((n+q)\log n)\) expected
- Memory: \(O(n)\) nodes`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Need split array/string into pieces, reverse a segment, re-concatenate
- Ordered multiset with custom aggregates on key ranges
- “BST + heap priorities” or policy-based structure insufficient (need lazy/reverse)
- Sequence problems where splay/LCT would be overkill

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `push` before reading children / sizes
- Wrong split size: `k - size(l) - 1` off-by-one
- Using `rand()` without wide priority space → degeneration
- Not `pull`ing after merge/split
- Recursion depth on adversarial priorities (use `mt19937`, not fixed)

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

- **Explicit-key treap:** split by key instead of size
- **Lazy add on segment:** push additive tag like segtree
- **Persistent treap:** copy nodes on path (rare)
- vs **PBDS:** PBDS shorter for pure order stats; treap wins for sequence lazy

---

## 11. Typical Problem Archetypes

1. Standard application: insert/erase in sorted order by key
2. Slightly disguised: reverse subarray + sum queries (implicit)
3. Difficult: cut/paste substrings; maintain hashes on treap
4. Very difficult / advanced: treap on tree rerooting / geometric divide

---

## 12. Recognition & Identification Drills

1. Array; reverse \([l,r]\) online many times; query sum on \([L,R]\).
2. Maintain a string; cut substring and paste elsewhere.
3. Multiset with “sum of keys in rank range \([a,b]\)”.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: split/merge sequences or keyed BSTs with aggregates
- Key invariant: BST(keys or implicit index) + heap(priorities)
- Key formula: split by size/key + merge by priority
- Complexity: expected \(O(\log n)\)
- Template to remember: `split` / `merge` / lazy `rev` push

---

## 7. Splay tree concepts

---
