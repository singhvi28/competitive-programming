# 7. DSU rollback

> **Section:** §07 Graph Algorithms (SCC, Topo-DP, 2-SAT)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** B-tier | **Rating Range:** 2000–2600 | **Frequency:** Occasional  
> **Prerequisites:** Classic DSU (union by rank/size); understanding that path compression prevents undo  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2600
- Prerequisites: Classic DSU (union by rank/size); understanding that path compression prevents undo

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Graph Algorithms focus on structural connectivity in directed graphs: Kosaraju and Tarjan Strongly Connected Components (SCC), Condensation DAGs, 2-Satisfiability (2-SAT), and Topological Dynamic Programming.

### Fundamental Theorems & Invariants

- **Condensation DAG Theorem:** Contracting each strongly connected component into a single super-node yields a Directed Acyclic Graph (DAG), enabling optimal dynamic programming in topological order.
- **2-SAT Implication Invariant:** A 2-SAT formula $(x_i \lor x_j) \land (\neg x_i \lor x_k) \dots$ is satisfiable if and only if no variable $x$ and its negation $\neg x$ lie within the same SCC in the implication graph.
- **2-SAT Topological Assignment:** If satisfiable, assigning $x_i = \text{true} \iff \text{SCC}(x_i) < \text{SCC}(\neg x_i)$ in topological order produces a valid satisfying assignment.

### Algorithmic Execution Blueprint

1. **Kosaraju SCC:** Run DFS 1 on graph $G$ to compute exit order stack. Run DFS 2 on transposed graph $G^T$ in decreasing exit order to label SCC components.
2. **Tarjan SCC:** Maintain discovery time $tin[u]$ and lowest reachable discovery time $low[u]$ on a DFS recursion stack. If $low[u] == tin[u]$, pop all vertices above $u$ as an SCC.
3. **2-SAT Construction:** Clause $(A \lor B)$ translates into directed implication edges $(\neg A \to B)$ and $(\neg B \to A)$. Check if $\text{scc}[2v] == \text{scc}[2v+1]$.

### Closed-Form Invariant Equations

$$(A \lor B) \iff (\neg A \implies B) \land (\neg B \implies A), \quad \text{Satisfiable} \iff \forall v, \; \text{SCC}(v) \neq \text{SCC}(\neg v)$$

### Structural Edge Cases & Assumptions

- In 2-SAT, a variable must take 2 consecutive integer indices (e.g., $2i$ for $x_i$ and $2i+1$ for $\neg x_i$).
- Tarjan's algorithm requires verifying that cross-edges connect only to nodes currently active on the stack.
- Single literal requirements $(A)$ must be modeled as $(\neg A \implies A)$.

---

## 3. Core Intuition & Problem Framing

Standard DSU with path compression is nearly \(O(1)\) but **irreversible**. If you need to **undo** unions (DFS backtrack, time travel, segment tree descent), drop path compression; keep **union by rank/size** only. Each `unite` pushes a stack record `{parent_changed, old_parent, rank_changed, old_rank, old_components}`; `rollback(t)` pops until stack size `t`.

This gives \(O(\log n)\) per unite/find (rank ≤ \(\log n\)) and \(O(1)\) amortized per undo step — perfect for offline structures that add edges on the way down a recursion and remove on the way up.

---

## 4. Proof Sketches & Recurrences

Without path compression, find is \(O(\log n)\) with union-by-rank. Stack stores enough to invert the last link:
- only the child root’s `p[child]=parent` changes (and maybe `sz`/`rk` of parent)
- if already same component, push a no-op marker or skip

Checkpoint: `int checkpoint = dsu.history_size(); …; dsu.rollback(checkpoint);`

Component count: decrement on successful merge; restore on rollback.

**Bipartite DSU:** store parity relative to parent; rollback same way — useful for “odd cycle offline.”

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: \(O(n)\)
- Per-query / per-operation: find/unite \(O(\log n)\); rollback amortized \(O(1)\) per recorded change
- Total: depends on caller (often \(O((n+m+q)\log n\log T)\) with time segtree)
- Memory: \(O(n + \#\mathrm{unites})\)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
#include <bits/stdc++.h>
using namespace std;

namespace dsu_rollback {
struct DSU {
    vector<int> p, r;
    int comps;
    struct Change { int u, pu, v, rv; int comps_before; bool merged; };
    vector<Change> st;

    DSU(int n = 0) { init(n); }
    void init(int n) {
        p.resize(n); r.assign(n, 0);
        iota(p.begin(), p.end(), 0);
        comps = n;
        st.clear();
    }
    int find(int x) {
        while (x != p[x]) x = p[x];
        return x;
    }
    int snapshot() const { return (int)st.size(); }

    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) {
            st.push_back({a, a, b, r[b], comps, false});
            return false;
        }
        if (r[a] < r[b]) swap(a, b);
        st.push_back({b, p[b], a, r[a], comps, true});
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
        --comps;
        return true;
    }

    void rollback(int snap) {
        while ((int)st.size() > snap) {
            auto ch = st.back(); st.pop_back();
            if (!ch.merged) continue;
            p[ch.u] = ch.pu;      // u was child root b
            r[ch.v] = ch.rv;      // v was parent a
            comps = ch.comps_before;
        }
    }
    bool same(int a, int b) { return find(a) == find(b); }
};

// Optional: DSU with parity (bipartite check)
struct DSUParity {
    vector<int> p, r, par; // par[x] = parity of x xor parent edge
    struct Change { int b, pb, pa_par, a, ra, merged; };
    vector<Change> st;
    bool bipok = true;
    vector<char> bip_st; // track bipok history if needed

    DSUParity(int n) { p.resize(n); iota(p.begin(), p.end(), 0); r.assign(n, 0); par.assign(n, 0); }

    int snapshot() const { return (int)st.size(); }

    pair<int,int> find(int x) { // {root, parity to root}
        int pr = 0;
        while (x != p[x]) { pr ^= par[x]; x = p[x]; }
        return {x, pr};
    }

    void unite(int a, int b) { // add edge a—b (should differ parity)
        auto [ra, pa] = find(a);
        auto [rb, pb] = find(b);
        if (ra == rb) {
            st.push_back({rb, rb, 0, ra, r[ra], 0});
            if ((pa ^ pb) == 0) bipok = false; // odd cycle
            return;
        }
        if (r[ra] < r[rb]) { swap(ra, rb); swap(pa, pb); }
        // link rb -> ra; edge means parity of rb relative to ra:
        // pa ^ edge ^ pb = 1 => edge_parity = 1 ^ pa ^ pb
        int edge = 1 ^ pa ^ pb;
        st.push_back({rb, p[rb], par[rb], ra, r[ra], 1});
        p[rb] = ra;
        par[rb] = edge;
        if (r[ra] == r[rb]) ++r[ra];
    }

    void rollback(int snap) {
        while ((int)st.size() > snap) {
            auto ch = st.back(); st.pop_back();
            if (!ch.merged) continue;
            p[ch.b] = ch.pb;
            par[ch.b] = ch.pa_par;
            r[ch.a] = ch.ra;
        }
    }
};
} // namespace dsu_rollback
```

### Python 3 Template

```python
# Python 3.11+ — educational; prefer C++ in contest for large n
class DSURollback:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n
        self.comps = n
        self.st: list[tuple] = []

    def find(self, x: int) -> int:
        while x != self.p[x]:
            x = self.p[x]
        return x

    def snapshot(self) -> int:
        return len(self.st)

    def unite(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            self.st.append((a, a, b, self.r[b], self.comps, False))
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.st.append((b, self.p[b], a, self.r[a], self.comps, True))
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        self.comps -= 1
        return True

    def rollback(self, snap: int) -> None:
        while len(self.st) > snap:
            b, pb, a, ra, comps_before, merged = self.st.pop()
            if not merged:
                continue
            self.p[b] = pb
            self.r[a] = ra
            self.comps = comps_before
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Edges exist only during a time interval”
- DFS on a segment tree where each node stores a list of edges alive on that segment
- Divide-and-conquer on time; queries ask connectivity / component size / bipartiteness at a moment
- Persistent connectivity **offline** (all queries known)
- Need undo after exploring a hypothetical union

---

## 7. Contest WA / TLE / RE Traps

- Enabling path compression → rollback corrupted
- Forgetting to store rank/size before increment
- Rolling back past 0 / mismatch snapshot indices
- Not pushing a record on “already united” when later logic expects aligned stack (optional; be consistent)
- Mixing two DSU instances’ snapshots
- Using recursive find with compression “just once”

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1239D | Catastrophe | 2200 | SCC, Condensation DAG, Graphs | Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges. | [Solve Problem](https://codeforces.com/contest/1239/problem/D) |
| Codeforces | CF-228E | The Road to Berland is Paved With Good Intentions | 1900 | 2-SAT, SCC, Implication Graph | 2-SAT clause modeling: x_u XOR x_v = state. | [Solve Problem](https://codeforces.com/contest/228/problem/E) |
| Codeforces | CF-1215D | Ticket Game | 1800 | Game Theory, Greedy | Game invariant symmetry and pair matching on questions. | [Solve Problem](https://codeforces.com/contest/1215/problem/D) |
| CSES | CSES-1684 | Giant Pizza | 1900 | 2-SAT, SCC | Standard 2-SAT construction for customer toppings preferences. | [Solve Problem](https://cses.fi/problemset/task/1684) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)](https://cp-algorithms.com/graph/strongly-connected-components.html)
- **[CP-Algorithms]** [CP-Algorithms: 2-SAT Problem](https://cp-algorithms.com/graph/2SAT.html)
- **[USACO Guide]** [USACO Guide: Topological Sort & DAG DP](https://usaco.guide/gold/topo)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Union by size** instead of rank — store old size
- **Component aggregates** (sum of values): store old parent aggregate; update on merge
- **Bipartite / colored DSU** with parity (above)
- **Fully persistent DSU:** different (version trees); rollback is partial persistence via stack

---

## 11. Typical Problem Archetypes

1. Standard application: add/undo edges in DFS; query `same` at leaves
2. Slightly disguised: spanning forest size history with backtracking
3. Difficult: offline dynamic connectivity (§7)
4. Very difficult / advanced: offline bipartiteness with edge lifespan; dynamic MST offline with LCT alternatives

---

## 12. Recognition & Identification Drills

1. Process operations: add edge, delete last edge (LIFO), query connectivity — stack of unions.
2. A recursion explores unions; after each recursive call the DSU must match the pre-call state.
3. Edges live on time intervals; queries ask whether two vertices are connected at time \(t\) (prelude to §7).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need undo unions; offline time structure
- Key invariant: no path compression; union by rank/size + history stack
- Key formula: snapshot = stack size; rollback pops merges
- Complexity: \(O(\log n)\) per unite/find
- Template to remember: `snapshot/unite/rollback`

---

---
