# 19. Functional Graphs

> **Section:** §08 Advanced Graphs (Shortest Paths, MST, Euler)  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Contest ROI:** A-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  
> **Prerequisites:** DFS/BFS, cycle detection, binary lifting optional  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1600–2200
- Prerequisites: DFS/BFS, cycle detection, binary lifting optional

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

Advanced Graph Algorithms address path optimization and tree graphs: Dijkstra with potential functions, 0-1 BFS with double-ended queues, Floyd-Warshall, Kruskal Reconstruction Trees, Functional Graphs, and Eulerian paths.

### Fundamental Theorems & Invariants

- **0-1 BFS Optimality:** When edge weights are restricted to $\{0, 1\}$, pushing 0-weight edges to the front and 1-weight edges to the back of a double-ended queue maintains monotonic distance order in strictly $\mathcal{O}(V + E)$ time.
- **Kruskal Reconstruction Tree (Reachability Tree):** Adding a new node for each merged edge in Kruskal's MST algorithm creates a binary tree of $2N-1$ nodes where the bottleneck edge between $u$ and $v$ is precisely the value of $\text{LCA}(u, v)$.
- **Eulerian Path Theorem (Hierholzer):** A connected directed graph has an Eulerian path if and only if at most one vertex has $\text{out} - \text{in} = 1$ and at most one vertex has $\text{in} - \text{out} = 1$, with all other vertices having $\text{in} = \text{out}$.

### Algorithmic Execution Blueprint

1. **0-1 BFS:** Initialize `deque<int> dq`; if $dist[v] > dist[u] + w$: update distance and push to front if $w=0$, push to back if $w=1$.
2. **Kruskal Tree:** When adding edge $(u, v, w)$ uniting components $r_u, r_v$, create new node $P$ with value $w$, set children $left=r_u, right=r_v$, and set DSU parent of $r_u, r_v$ to $P$.
3. **Hierholzer Eulerian Circuit:** Perform DFS, removing traversed edges dynamically; push vertex to result stack upon backtracking.

### Closed-Form Invariant Equations

$$\text{BottleneckWeight}(u, v) = \text{NodeVal}\big(\text{LCA}_{\text{KruskalTree}}(u, v)\big)$$

### Structural Edge Cases & Assumptions

- Hierholzer's algorithm must erase edges as they are traversed to avoid $\mathcal{O}(E^2)$ quadratic slowdown on dense multigraphs.
- In functional graphs with $N$ vertices and out-degree 1, every component consists of exactly one directed cycle with directed tree branches feeding into it.
- Floyd-Warshall loop order must strictly place the intermediate vertex $k$ in the outermost loop.

---

## 3. Core Intuition & Problem Framing

A **functional graph** has outdegree exactly 1 for every node (`next[u] = f(u)`). Structure: each component is a single cycle with trees directed **into** the cycle (inverted arborescences). Contests love: process \(k\) applications of \(f\), sum along path, find cycle length, rho/Floyd, or model permutations. Treat components independently: find cycle, compute depths of tree nodes into cycle entry, then answer jumps with `k` vs distance-to-cycle + modular arithmetic on cycle.

---

## 4. Proof Sketches & Recurrences

Follow edges; mark colors (0 unseen, 1 stack, 2 done) or record time-in-stack to extract cycles. For queries \(f^{(k)}(v)\): binary lifting table `up[j][v] = f^{(2^j)}(v)` in \(O(n\log K)\). Cycle answers: if \(k \ge dist\_to\_cycle\), reduce \((k - dist) \bmod len\).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: analyze \(O(n)\); lifting \(O(n\log K)\)
- Per-query / per-operation: jump \(O(\log K)\); cycle query \(O(1)\) after prep
- Total: \(O(n\log K + q\log K)\)
- Memory: \(O(n\log K)\) for lifting; \(O(n)\) for cycle info`

### C++17 Template

```cpp
namespace functional {
// next[u] in [0..n)
struct Info {
    vector<int> next;
    vector<int> cyc_id;      // -1 if not on cycle; else cycle index
    vector<int> cyc_pos;     // position on cycle
    vector<int> cyc_len;
    vector<int> dist_to_cyc; // 0 if on cycle
    vector<int> entry;       // first cycle vertex reached
    vector<vector<int>> cycles;
};

Info analyze(const vector<int>& next) {
    int n = (int)next.size();
    Info info;
    info.next = next;
    info.cyc_id.assign(n, -1);
    info.cyc_pos.assign(n, -1);
    info.dist_to_cyc.assign(n, -1);
    info.entry.assign(n, -1);
    vector<int> state(n, 0); // 0=unseen,1=visiting,2=done
    vector<int> stack;
    stack.reserve(n);

    for (int s = 0; s < n; ++s) {
        if (state[s]) continue;
        int u = s;
        while (state[u] == 0) {
            state[u] = 1;
            stack.push_back(u);
            u = next[u];
        }
        if (state[u] == 1) {
            // found cycle ending at u
            vector<int> cyc;
            while (true) {
                int x = stack.back();
                stack.pop_back();
                state[x] = 2;
                cyc.push_back(x);
                if (x == u) break;
            }
            reverse(cyc.begin(), cyc.end());
            int cid = (int)info.cycles.size();
            info.cycles.push_back(cyc);
            info.cyc_len.push_back((int)cyc.size());
            for (int i = 0; i < (int)cyc.size(); ++i) {
                int x = cyc[i];
                info.cyc_id[x] = cid;
                info.cyc_pos[x] = i;
                info.dist_to_cyc[x] = 0;
                info.entry[x] = x;
            }
        }
        while (!stack.empty()) {
            int x = stack.back();
            stack.pop_back();
            state[x] = 2;
        }
    }

    // dists for tree nodes: walk forward (memo)
    for (int v = 0; v < n; ++v) {
        if (info.dist_to_cyc[v] != -1) continue;
        vector<int> path;
        int u = v;
        while (info.dist_to_cyc[u] == -1) {
            path.push_back(u);
            u = next[u];
        }
        int d = info.dist_to_cyc[u];
        int ent = info.entry[u];
        for (int i = (int)path.size() - 1; i >= 0; --i) {
            ++d;
            info.dist_to_cyc[path[i]] = d;
            info.entry[path[i]] = ent;
            info.cyc_id[path[i]] = info.cyc_id[ent];
        }
    }
    return info;
}

// binary lifting for f^k
struct Lift {
    int LOG;
    vector<vector<int>> up;
    Lift(const vector<int>& next, int max_pow = 60) {
        int n = (int)next.size();
        LOG = max_pow;
        up.assign(LOG, vector<int>(n));
        up[0] = next;
        for (int j = 1; j < LOG; ++j)
            for (int i = 0; i < n; ++i)
                up[j][i] = up[j - 1][up[j - 1][i]];
    }
    int jump(int v, long long k) const {
        for (int j = 0; j < LOG && k; ++j)
            if (k & (1LL << j)) {
                v = up[j][v];
                k ^= (1LL << j);
            }
        return v;
    }
};
} // namespace functional
```

---

## 6. Recognition Trigger Signals & Heuristics

- Array `p[i]` or `a[i]` pointing to exactly one next index
- “Repeatedly replace \(x := f(x)\)”
- Permutation as special case (also indegree 1): disjoint cycles only
- Tortoise–hare cycle detection in arrays

---

## 7. Contest WA / TLE / RE Traps

- Treating functional graph as general digraph DP without cycle handling
- Infinite loops when summing along path without stopping at cycle
- Permutation assumed when duplicate `next` values exist (not a perm)
- Off-by-one: steps to enter cycle vs index on cycle
- Using recursion depth \(n\) for follow — iterative required

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1076D | Edge Deletion | 1800 | Dijkstra, Shortest Path Tree | Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS. | [Solve Problem](https://codeforces.com/contest/1076/problem/D) |
| Codeforces | CF-1156D | 0-1-Tree | 2100 | DSU, Trees, Combinatorics | DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths. | [Solve Problem](https://codeforces.com/contest/1156/problem/D) |
| Codeforces | CF-723E | One-Way Roads | 2200 | Eulerian Circuit, Graph Orientation | Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer. | [Solve Problem](https://codeforces.com/contest/723/problem/E) |
| CSES | CSES-1195 | Flight Discount | 1600 | Dijkstra, State Space Graph | 2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used. | [Solve Problem](https://cses.fi/problemset/task/1195) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)](https://cp-algorithms.com/graph/dijkstra.html)
- **[CP-Algorithms]** [CP-Algorithms: Eulerian Path & Circuit (Hierholzer)](https://cp-algorithms.com/graph/euler_path.html)
- **[USACO Guide]** [USACO Guide: Kruskal Reconstruction Tree](https://usaco.guide/adv/kruskal-tree)

---

## 10. Algorithmic Variants & Advanced Extensions

- Permutation: disjoint cycles only; \(k\)-th power of perm
- Partial functional (some nodes no out) — rare
- Weighted edges on `next`: prefix on trees + cycle prefix sums
- Floyd cycle detection without \(O(n)\) memory marks (interview style)

---

## 11. Typical Problem Archetypes

1. Standard application: where is token after \(k\) moves?
2. Slightly disguised: follow pointers until repeat; count distinct values
3. Difficult: sum of values on path of length \(k\) with cycle expansion
4. Very difficult / advanced: functional graph + segment tree on cycle / queries offline

---

## 12. Recognition & Identification Drills

1. Array \(a[1..n]\); from \(i\) go to \(a_i\); answer \(q\) queries after \(k_j\) steps.
2. Each component’s cycle length; count nodes not on any cycle.
3. Robot follows unique next cell; detect period before revisiting.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: outdegree exactly 1 everywhere
- Key invariant: one cycle per component + in-trees
- Key formula: \(f^{(k)}\) via lifting or dist-to-cycle + mod
- Complexity: \(O(n)\) structure; \(O(n\log K)\) jumps
- Template to remember: mark cycles, then depths into entry; binary lift optional

---
