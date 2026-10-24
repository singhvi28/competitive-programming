# Link-Cut Tree (Concept + Preferred-Path Sketch)

> **Section:** §05 Advanced Data Structures (Treaps, LCT, PBDS)  
> **Phase:** Phase 3 — Advanced Data Structures & Sqrt Techniques  
> **Contest ROI:** Niche | **Rating Range:** 2600–3500 | **Frequency:** Rare  
> **Prerequisites:** Splay concepts, tree path aggregates, understanding HLD as the static analogue  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: Niche
- Frequency: Rare
- Typical CF/ICPC rating range: 2600–3500
- Prerequisites: Splay concepts, tree path aggregates, understanding HLD as the static analogue

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

Represent a forest as **preferred paths** (heavy-ish chains that change dynamically), each path stored in a **splay tree** keyed by depth. `access(v)` splays `v` and reassembles the preferred path from root to `v`. `link` / `cut` change forest edges; path aggregates (sum/min) live in the splay. **Early ROI: Niche** — for almost all CF/ICPC tasks prefer **HLD + segtree**, Euler tour, or DSU. Only invest in full LCT when the forest is truly dynamic (edges link/cut online) and path queries matter.

If a full production LCT is too large for this masterclass week: solid concept + `access` / splay / preferred-path sketch below is enough; treat complete `link`/`cut`/`path_aggregate` libraries as reference code to paste when forced.

---

## 4. Proof Sketches & Recurrences

Each real tree edge is either preferred or not. Preferred paths partition nodes. Within a path, splay by depth; `path-parent` pointer connects path head to light parent.  
`access(v)`: splay up preferred path, disconnect right child (deeper nodes no longer preferred), then splice into parent path — repeat until root. After `access(v)`, root-to-`v` is one preferred path with `v` at the right end (depth order).  
`link(u,v)`: make `u` root (`evert`), `access(v)`, attach. `cut`: `access` + disconnect parent edge in splay.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\) nodes
- Per-query / per-operation: amortized \(O(\log n)\) for access/link/cut/path
- Total: amortized \(O(q\log n)\)
- Memory: \(O(n)\)`

### C++17 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Online link and cut edges in a forest + path min/sum
- “Dynamic tree” in editorial; LCT / top trees mentioned
- HLD fails because tree shape changes
- Subtree queries on dynamic trees (even harder — often needs ST-trees / Euler+LCT hybrids)

---

## 7. Contest WA / TLE / RE Traps

- Confusing path-parent (`p` when `is_root`) with splay parent
- Forgetting `rev` / `makeroot` before link/cut
- Using LCT when HLD on a static tree suffices
- Subtree ≠ path: classic LCT does paths; subtrees need extra orientation tricks

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

- Path sum / min / XOR with pull on splay nodes
- LCT + lazy path add
- Euler-tour + LCT hybrids for subtrees (expert niche)
- AAA tree / top trees — theory generalizations

---

## 11. Typical Problem Archetypes

1. Standard application: maintain forest, query path XOR/min after links/cuts
2. Slightly disguised: dynamic connectivity in trees with weights
3. Difficult: dynamic tree DP via LCT
4. Very difficult / advanced: subtree updates on dynamic trees; combining LCT with segtree on time

---

## 12. Recognition & Identification Drills

1. Forest starts as \(n\) isolated vertices; process `link`, `cut`, `path_sum` online.
2. Same queries but tree is static — which structure should you use instead?
3. After `access(v)`, what does the preferred-path partition look like?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: truly dynamic forest + path aggregates (Niche)
- Key invariant: preferred paths in splay trees by depth; `access` builds root→v
- Key formula: `access` / `makeroot` / `link` / `cut`
- Complexity: amortized \(O(\log n)\)
- Template to remember: splay + `access` loop setting `y->r = last`; else use HLD

---

[Hub](05-advanced-data-structures.md) · [Part a: Fenwick → Cartesian](05-a-fenwick-sparse-tables-cartesian.md)

---
