# 5. Splay Tree (Concepts)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** Niche | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** BST rotations, amortized analysis intuition; treap usually preferred for sequences  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: BST rotations, amortized analysis intuition; treap usually preferred for sequences

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

Splay trees move the accessed node to the root via zig / zig-zig / zig-zag rotations. No random priorities: amortization gives \(O(\log n)\) per op. In contests, **implicit treaps replace most sequence uses**; splay matters mainly as the **access primitive inside link-cut trees** (preferred-path representation). Mark **Niche for early ROI** — learn rotations + “access brings node to root,” not a full production splay library first.

---

## 4. Proof Sketches & Recurrences

Potential = sum of log subtree sizes (or ranks). Zig-zig / zig-zag cases telescope so a sequence of \(m\) ops on \(n\) nodes is \(O((m+n)\log n)\) amortized. Single ops can be \(O(n)\) worst-case — important for TL paranoia vs treap’s expected bounds.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) to build a chain then splay, or insert one-by-one amortized \(O(n\log n)\)
- Per-query / per-operation: amortized \(O(\log n)\); worst single \(O(n)\)
- Total: amortized \(O((n+q)\log n)\)
- Memory: \(O(n)\)`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Problem mentions splay / LCT / dynamic trees
- Need amortised BST without RNG
- Implementing LCT preferred paths
- Interview question on zig-zig vs zig-zag (rare in CF)

---

## 7. Contest WA / TLE / RE Traps

- Forgetting parent updates on both sides of rotate
- Not handling root / `g` null when linking after rotate
- Expecting strict \(O(\log n)\) worst-case per op
- Reimplementing splay for a problem a treap solves in 40 lines

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

- Implicit splay (size keys) for sequences — same niche as implicit treap
- Top tree / LCT built on splay
- Tango trees etc. — not contest-relevant

---

## 11. Typical Problem Archetypes

1. Standard application: textbook BST with amortised access (rare as standalone CF task)
2. Slightly disguised: sequence maintenance where author solution is splay
3. Difficult: LCT path aggregates (depends on splay access)
4. Very difficult / advanced: full LCT + subtree mods

---

## 12. Recognition & Identification Drills

1. Why zig-zig rotates parent first, then node?
2. Given parent pointers, bring node `u` to root of its BST.
3. Contrast: when would you code treap instead of splay for reverse-on-segment?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: LCT building block; rarely standalone in CF
- Key invariant: accessed node becomes root; amortised balance
- Key formula: zig / zig-zig / zig-zag
- Complexity: amortised \(O(\log n)\)
- Template to remember: `rotate` + `splay` loop; prefer treap otherwise

---

## 8. Randomized BST

---
