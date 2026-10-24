# Group 2: Comparisons / Decision Matrices & Tradeoffs (16 topics)

G2_DATA = {
    "08-dijkstra-vs-0-1-bfs-vs-bellman-ford": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–2100\n- Prerequisites: Graph representations, Priority Queues, Deque, BFS\n- Tradeoff: Choosing the strictly minimal complexity tool based on edge weights prevents TLE/MLE.",
        "coreIntuition": "The decision matrix for single-source shortest path is dictated strictly by edge weight distribution: Unit weights $w \\in \\{1\\} \\implies$ Standard Queue BFS in $\\mathcal{O}(V + E)$. Binary weights $w \\in \\{0, k\\} \\implies$ 0-1 BFS with `std::deque` in $\\mathcal{O}(V + E)$ by pushing 0-cost transitions to the front and $k$-cost to the back. General non-negative weights $w \\ge 0 \\implies$ Dijkstra with `std::priority_queue` in $\\mathcal{O}((V + E) \\log V)$. Arbitrary weights with negative cycles or cycle detection $\\implies$ Bellman-Ford in $\\mathcal{O}(V \\cdot E)$.",
        "derivation": "Dijkstra's greedy choice holds because edge weights are non-negative ($w(u, v) \\ge 0$), guaranteeing monotonic distance expansions along shortest paths: $d(u) \\le d(v)$ for all explored vertices. 0-1 BFS maintains the invariant that the deque contains distances spanning at most $\\{d, d + 1\\}$, preserving the monotonic priority queue property in $\\mathcal{O}(1)$ amortized time per pop. Bellman-Ford performs dynamic programming over path length: after $k$ relaxation passes over all $E$ edges, $dist[v]$ equals the length of the shortest path from source to $v$ containing at most $k$ edges.",
        "templateCpp": "// Decision Matrix Dispatcher: 0-1 BFS vs Dijkstra\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\n// 0-1 BFS: weights in {0, 1}, runs in O(V + E)\nvector<ll> bfs_01(int n, int src, const vector<vector<pair<int, int>>>& adj) {\n    vector<ll> dist(n + 1, INF);\n    deque<int> dq;\n    dist[src] = 0; dq.push_back(src);\n    while (!dq.empty()) {\n        int u = dq.front(); dq.pop_front();\n        for (auto& [v, w] : adj[u]) {\n            if (dist[u] + w < dist[v]) {\n                dist[v] = dist[u] + w;\n                if (w == 0) dq.push_front(v);\n                else dq.push_back(v);\n            }\n        }\n    }\n    return dist;\n}",
        "recognitionPatterns": [
            "Graph grid movements where turning or changing state costs 1 and moving straight costs 0 (reach for 0-1 BFS).",
            "Continuous state costs with non-negative arbitrary weights (reach for Dijkstra).",
            "Negative edge weights with at most $K$ step limits or currency arbitrage exchange rates (reach for Bellman-Ford).",
            "Dynamic graphs where distances wrap around modulo $M$ (reach for Dijkstra on residue classes / Dijkstra on modulo graph)."
        ],
        "commonBugs": [
            "Using 0-1 BFS when edge weights are in $\{0, 1, 2\}$; the deque distance invariant breaks down, leading to suboptimal distances.",
            "Using Dijkstra on graphs with negative edge weights; Dijkstra fails to re-evaluate finalized nodes and produces wrong answers.",
            "Forgetting to check the stale queue state `if (d > dist[u]) continue;` in Dijkstra, causing memory/time blowup.",
            "Running Bellman-Ford for exactly $V-1$ iterations without an early-break flag when no relaxations occur, wasting CPU time."
        ]
    },
    "08-why-spfa-is-dangerous": {
        "whyItMatters": "- Contest ROI: A-tier (Defense / Anti-TLE)\n- Frequency: Situational\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: Shortest Path Faster Algorithm (SPFA), Bellman-Ford, Queue heuristics\n- Tradeoff: SPFA is worst-case $\\mathcal{O}(V \\cdot E)$ or even $\\mathcal{O}(2^V)$ on adversarial test cases designed by contest problem setters.",
        "coreIntuition": "SPFA is essentially queue-optimized Bellman-Ford. While its average running time on random sparse graphs is often empirical $\\mathcal{O}(E)$, contest setters can construct special adversarial test cases (e.g., nested diamond graphs, grid graphs with alternating high/low path shortcuts) that force vertices into the queue exponentially or quadratic number of times ($V \\cdot E$). Never rely on SPFA when Dijkstra with potentials (Johnson's algorithm) or 0-1 BFS is applicable.",
        "derivation": "On a directed graph constructed with $k$ nested diamond stages, each stage doubles the number of times downstream vertices are updated and re-enqueued: a vertex at depth $k$ is enqueued $\\Omega(2^k)$ times under FIFO queue discipline. Even heuristics like Small Label First (SLF) and Large Label Last (LLL) have been broken by explicit adversarial constructions in published competitive programming literature.",
        "templateCpp": "// Safe SPFA with Negative Cycle Detection and Guard Counter\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\nbool safe_spfa(int n, int src, const vector<vector<pair<int, ll>>>& adj, vector<ll>& dist) {\n    dist.assign(n + 1, INF);\n    vector<int> cnt(n + 1, 0);\n    vector<bool> in_queue(n + 1, false);\n    queue<int> q;\n    dist[src] = 0; q.push(src); in_queue[src] = true;\n    while (!q.empty()) {\n        int u = q.front(); q.pop(); in_queue[u] = false;\n        for (auto& [v, w] : adj[u]) {\n            if (dist[u] + w < dist[v]) {\n                dist[v] = dist[u] + w;\n                if (!in_queue[v]) {\n                    q.push(v); in_queue[v] = true;\n                    if (++cnt[v] >= n) return false; // Negative cycle detected!\n                }\n            }\n        }\n    }\n    return true; // No negative cycles reachable from src\n}",
        "recognitionPatterns": [
            "Problem specifies arbitrary edge weights (positive and negative) and asks for shortest paths or negative cycle detection.",
            "Constraints have $V, E \\le 5000$ where Bellman-Ford passes comfortably, but SPFA offers lower average runtime.",
            "Min-cost Max-flow (MCMF) implementations using successive shortest path with SPFA (vulnerable to hack on dense graphs; prefer SPFA once then Johnson potentials with Dijkstra).",
            "Detecting whether an arbitrage cycle exists in currency rates: transform weights $w = -\\ln(rate)$."
        ],
        "commonBugs": [
            "Assuming SPFA runs in $\\mathcal{O}(E)$ on all test cases; Codeforces test suites actively include anti-SPFA tests.",
            "Not resetting the `in_queue[u] = false` flag when popping from the queue, preventing future valid distance relaxations.",
            "Using 32-bit integer distances where negative edge accumulations cause underflow/overflow.",
            "Allowing infinite loop when an unreachable negative cycle exists in the graph; iterate over all components if global negative cycle detection is needed."
        ]
    },
    "08-kruskal-reconstruction-vs-hld-for-path-max": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common in CF Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Kruskal's MST, Disjoint Set Union (DSU), Heavy-Light Decomposition (HLD), Binary Lifting\n- Tradeoff: Kruskal Reconstruction Tree (Reachability Tree) reduces path bottleneck queries to a single LCA in $\\mathcal{O}(1)$ or $\\mathcal{O}(\\log N)$ without writing any segment tree or HLD.",
        "coreIntuition": "To find the maximum edge weight on the path between $u$ and $v$ in a graph's MST: standard HLD builds an MST, decomposes tree paths into $\\mathcal{O}(\\log N)$ segments, and queries a segment tree in $\\mathcal{O}(\\log^2 N)$ time with 100+ lines of code. Kruskal's Reconstruction Tree (KRT) builds a binary tree with $2N - 1$ nodes: whenever Kruskal joins two components with edge $e = (u, v, w)$, a new node is created with weight $w$, having the roots of $u$ and $v$ as left and right children. The bottleneck maximum weight on the path between $u$ and $v$ is simply the weight of $\\text{LCA}(u, v)$ in the KRT!",
        "derivation": "In Kruskal's algorithm, edges are processed in non-decreasing order of weight. Thus, in the KRT, child nodes always have weights less than or equal to their parent nodes: the tree is a min/max heap on node weights. The first time $u$ and $v$ become connected in Kruskal's process is precisely at $\\text{LCA}(u, v)$ in the KRT, and the edge weight that connected them is $weight[\\text{LCA}(u, v)]$. Any reachability query 'nodes reachable from $u$ using edges $\\le W$' maps to the subtree of the highest ancestor of $u$ with weight $\\le W$, solvable via binary lifting in $\\mathcal{O}(\\log N)$.",
        "templateCpp": "// Kruskal Reconstruction Tree (Reachability Tree)\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct KRT {\n    int n, node_cnt;\n    vector<int> par, val;\n    vector<vector<int>> up, adj;\n    int LOG;\n    KRT(int n_) : n(n_), node_cnt(n_), par(2 * n_ + 1), val(2 * n_ + 1), LOG(__lg(2 * n_) + 2) {\n        iota(par.begin(), par.end(), 0);\n        up.assign(LOG, vector<int>(2 * n_ + 1, 0));\n        adj.assign(2 * n_ + 1, {});\n    }\n    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }\n    void build(vector<tuple<int, int, int>>& edges) {\n        sort(edges.begin(), edges.end());\n        for (auto& [w, u, v] : edges) {\n            int ru = find(u), rv = find(v);\n            if (ru != rv) {\n                int cur = ++node_cnt;\n                val[cur] = w;\n                par[ru] = par[rv] = par[cur] = cur;\n                adj[cur].push_back(ru); adj[cur].push_back(rv);\n                up[0][ru] = up[0][rv] = cur;\n            }\n        }\n        for (int k = 1; k < LOG; ++k)\n            for (int i = 1; i <= node_cnt; ++i)\n                up[k][i] = up[k - 1][up[k - 1][i]];\n    }\n    int query_max_edge(int u, int v, const vector<int>& depth) {\n        if (depth[u] < depth[v]) swap(u, v);\n        for (int k = LOG - 1; k >= 0; --k) if (depth[u] - (1 << k) >= depth[v]) u = up[k][u];\n        if (u == v) return val[u];\n        for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }\n        return val[up[0][u]];\n    }\n};",
        "recognitionPatterns": [
            "Query asks: 'What is the maximum/minimum capacity edge on the safest path between $u$ and $v$?'",
            "Query asks: 'How many vertices are reachable from $u$ using only edges with weight $\\le W$?'",
            "Static graph connectivity with threshold queries (KRT turns it into a subtree query on Euler tour).",
            "Comparing path bottleneck queries on undirected graphs without dynamic edge weight updates."
        ],
        "commonBugs": [
            "Allocating only $N$ nodes instead of $2N$ nodes for the KRT internal join vertices.",
            "Forgetting that isolated vertices in a disconnected graph will produce a forest; run DFS/LCA preprocessing for every tree root.",
            "Using KRT when edge weights are dynamically updated during queries; KRT requires static edge weights (use Link-Cut Trees or HLD if edges update).",
            "Failing to initialize `par` array up to $2N$ elements."
        ]
    },
    "08-bor-vka-niche": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Niche but decisive in Hard CF/ICPC problems\n- Typical CF/ICPC rating range: 2200–2700\n- Prerequisites: Minimum Spanning Tree (MST), Bitwise Trie, Geometric Voronoi, DSU\n- Tradeoff: Kruskal/Prim require explicit edges ($\\mathcal{O}(E \\log E)$ or $\\mathcal{O}(V^2)$); Borůvka constructs MST on implicit complete graphs where finding the cheapest outgoing edge takes sublinear time.",
        "coreIntuition": "Borůvka's algorithm operates in phases: in each phase, every connected component simultaneously finds its cheapest outgoing incident edge, and all chosen edges are contracted. Because the number of connected components halves in each phase, there are at most $\\lceil \\log_2 V \\rceil$ phases. In complete graphs where edges are implicit (e.g., $w(u, v) = u \\oplus v$ via bitwise XOR, or Manhattan/Euclidean distances in geometry), we cannot sort all $\\mathcal{O}(V^2)$ edges. Borůvka allows us to find the cheapest outgoing edge for each component in $\\mathcal{O}(V \\log(\\text{coordinate}))$ using a 0-1 Trie or KD-tree, giving overall $\\mathcal{O}(V \\log V \\log C)$ runtime!",
        "derivation": "Let $C$ be the number of components at phase $t$. Each component identifies an incident edge with minimal weight. Since each component has at least one edge picked, the contracted graph has at most $\\lfloor C/2 \\rfloor$ components. Thus, $C_{t+1} \\le C_t / 2$, terminating in $\\le \\log_2 V$ rounds. Total time is $\\mathcal{O}(\\log V \\cdot (\\text{cost to query all components' cheapest edge}))$.",
        "templateCpp": "// Boruvka Framework for Implicit Graphs (e.g., XOR MST)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct DSU {\n    vector<int> p;\n    int comps;\n    DSU(int n) : p(n), comps(n) { iota(p.begin(), p.end(), 0); }\n    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }\n    bool unite(int a, int b) {\n        a = find(a); b = find(b);\n        if (a == b) return false;\n        p[a] = b; comps--; return true;\n    }\n};\n\nll boruvka_xor_mst(int n, vector<int>& a) {\n    DSU dsu(n);\n    ll total_mst_weight = 0;\n    while (dsu.comps > 1) {\n        // In each phase, find cheapest outgoing edge for each component root\n        // best_edge[comp_root] = {min_weight, target_node}\n        vector<pair<int, int>> best(n, {INT_MAX, -1});\n        // ... (populate best edges via 0-1 Trie search excluding same component) ...\n        bool added = false;\n        for (int i = 0; i < n; ++i) {\n            if (best[i].second != -1 && dsu.unite(i, best[i].second)) {\n                total_mst_weight += best[i].first;\n                added = true;\n            }\n        }\n        if (!added) break; // Graph disconnected\n    }\n    return total_mst_weight;\n}",
        "recognitionPatterns": [
            "Complete graph where edge weight is defined by bitwise XOR $w(u, v) = a_u \\oplus a_v$ for $N \\le 2 \\times 10^5$.",
            "Dense geometric graphs where nearest-neighbor queries can be accelerated by Voronoi diagrams or Delaunay triangulation.",
            "Graph where edges are implicit and finding the minimum weight outgoing edge from a set of nodes takes sub-linear time.",
            "Contest problem where $E = \\Theta(V^2)$ but $N \\approx 10^5$."
        ],
        "commonBugs": [
            "Picking an internal edge: cheapest edge query must ensure the endpoint does NOT belong to the same component (`find(u) != find(v)`).",
            "Tie-breaking: if two components pick edges of equal weight, ensure unique edge ordering $(w, \\min(u, v), \\max(u, v))$ to prevent cycles with equal weights.",
            "Infinite loops if graph is disconnected: ensure the loop terminates when no edges are added in a round.",
            "Trie deletion/insertion overhead: rebuilding or modifying the Trie dynamically must be done efficiently per round."
        ]
    },
    "09-dinic-vs-edmonds-karp": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Max-Flow / Min-Cut\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: Augmenting Paths, BFS, DFS, Level Graphs, Blocking Flows\n- Tradeoff: Edmonds-Karp runs in $\\mathcal{O}(V E^2)$ (too slow for $N > 100$); Dinic's runs in $\\mathcal{O}(V^2 E)$, and $\\mathcal{O}(E \\sqrt{V})$ on unit capacity graphs.",
        "coreIntuition": "Both Edmonds-Karp and Dinic find shortest augmenting paths using BFS. However, Edmonds-Karp finds a single augmenting path per BFS traversal and immediately updates residual capacities. Dinic decomposes the computation: a single BFS constructs a *level graph* (DAG of shortest paths), and a DFS with pointer work finds a *blocking flow* (saturating multiple augmenting paths simultaneously in the same level graph). Once blocked, the source-sink distance strictly increases by $\\ge 1$. Thus, Dinic requires at most $V - 1$ BFS phases.",
        "derivation": "In Dinic's algorithm, the distance from source $S$ to sink $T$ in the level graph strictly increases after each phase: $dist_{k+1}(S, T) > dist_k(S, T)$. Hence there are at most $V - 1$ phases. In each phase, the DFS advances along unsaturated edges; whenever an edge is saturated or a dead-end is reached, the current-arc pointer increments. Across the phase, total time spent retreating is $\\mathcal{O}(V E)$ and total time advancing is $\\mathcal{O}(V E)$, giving $\\mathcal{O}(V E)$ per phase, or $\\mathcal{O}(V^2 E)$ total. On unit capacity networks, the number of phases is $\\mathcal{O}(\\sqrt{V})$ or $\\mathcal{O}(E^{1/2})$, yielding $\\mathcal{O}(E \\sqrt{V})$ or $\\mathcal{O}(E \\min(V^{2/3}, E^{1/2}))$.",
        "templateCpp": "// Dinic's Algorithm (Fast competitive programming standard)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Dinic {\n    struct Edge { int to; ll cap, flow; int rev; };\n    int n, s, t;\n    vector<vector<Edge>> adj;\n    vector<int> level, ptr;\n    Dinic(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1), level(n_ + 1), ptr(n_ + 1) {}\n    void add_edge(int from, int to, ll cap) {\n        adj[from].push_back({to, cap, 0, (int)adj[to].size()});\n        adj[to].push_back({from, 0, 0, (int)adj[from].size() - 1});\n    }\n    bool bfs() {\n        fill(level.begin(), level.end(), -1);\n        level[s] = 0; queue<int> q; q.push(s);\n        while (!q.empty()) {\n            int v = q.front(); q.pop();\n            for (auto& edge : adj[v]) {\n                if (edge.cap - edge.flow > 0 && level[edge.to] == -1) {\n                    level[edge.to] = level[v] + 1;\n                    q.push(edge.to);\n                }\n            }\n        }\n        return level[t] != -1;\n    }\n    ll dfs(int v, ll pushed) {\n        if (pushed == 0 || v == t) return pushed;\n        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {\n            auto& edge = adj[v][cid];\n            int trg = edge.to;\n            if (level[v] + 1 != level[trg] || edge.cap - edge.flow == 0) continue;\n            ll tr = dfs(trg, min(pushed, edge.cap - edge.flow));\n            if (tr == 0) continue;\n            edge.flow += tr;\n            adj[trg][edge.rev].flow -= tr;\n            return tr;\n        }\n        return 0;\n    }\n    ll max_flow() {\n        ll flow = 0;\n        while (bfs()) {\n            fill(ptr.begin(), ptr.end(), 0);\n            while (ll pushed = dfs(s, 1e18)) flow += pushed;\n        }\n        return flow;\n    }\n};",
        "recognitionPatterns": [
            "Network capacity graph with $V \\le 5000, E \\le 30000$ where Edmonds-Karp would TLE.",
            "Unit network matching (e.g., bipartite matching via flow) where Dinic executes in blinding $\\mathcal{O}(E \\sqrt{V})$ speed.",
            "Project selection problem (closure graph with positive weights to source, negative to sink).",
            "Minimum cut partitioning where min-cut capacity equals max flow."
        ],
        "commonBugs": [
            "Omitting the current-arc pointer `int& cid = ptr[v]` in DFS, degenerating Dinic to Edmonds-Karp complexity $\\mathcal{O}(V E^2)$.",
            "Forgetting that backward residual edge has capacity 0 initially (`adj[to].push_back({from, 0, 0, ...})`) for directed graphs.",
            "Integer overflow: capacities or flow sum exceed $2^{31} - 1$; always use `long long` for `cap` and `flow`.",
            "Resetting `ptr` inside BFS rather than before the blocking DFS loop."
        ]
    },
    "09-dinic-vs-hopcroft-karp": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1700–2300\n- Prerequisites: Bipartite Matching, Dinic's Algorithm, Hopcroft-Karp\n- Tradeoff: Hopcroft-Karp is mathematically identical to Dinic on unit bipartite networks; knowing this saves memorizing two separate algorithms.",
        "coreIntuition": "Hopcroft-Karp is specifically Dinic's algorithm specialized for bipartite matching networks. In a bipartite graph with unit capacity edges, Dinic's level graph BFS finds shortest alternating paths from unmatched left nodes to unmatched right nodes, and the DFS augments along vertex-disjoint paths in $\\mathcal{O}(E \\sqrt{V})$ time. Dinic's algorithm achieves this exact same $\\mathcal{O}(E \\sqrt{V})$ bound naturally on unit networks without requiring a bespoke Hopcroft-Karp implementation.",
        "derivation": "In unit bipartite graphs, every vertex in $L \\cup R$ has either in-degree 1 or out-degree 1 in the residual network. Therefore, augmenting paths in a single phase are strictly vertex-disjoint. After $k$ phases of augmentation, the length of the shortest augmenting path is at least $k + 1$, and the difference between the current matching $M$ and maximum matching $M^*$ satisfies $|M^* \\setminus M| \\le V / k$. Balancing $k = \\sqrt{V}$ yields $\\mathcal{O}(\\sqrt{V})$ phases, with $\\mathcal{O}(E)$ work per phase.",
        "templateCpp": "// Hopcroft-Karp Bipartite Matching via Dinic or Dedicated Array HK\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct HopcroftKarp {\n    int n, m; // Sizes of left (1..n) and right (1..m) sets\n    vector<vector<int>> adj;\n    vector<int> pair_u, pair_v, dist;\n    HopcroftKarp(int n_, int m_) : n(n_), m(m_), adj(n_ + 1), pair_u(n_ + 1, 0), pair_v(m_ + 1, 0), dist(n_ + 1) {}\n    void add_edge(int u, int v) { adj[u].push_back(v); }\n    bool bfs() {\n        queue<int> q;\n        for (int u = 1; u <= n; ++u) {\n            if (pair_u[u] == 0) { dist[u] = 0; q.push(u); }\n            else dist[u] = INT_MAX;\n        }\n        dist[0] = INT_MAX;\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            if (dist[u] < dist[0]) {\n                for (int v : adj[u]) {\n                    if (dist[pair_v[v]] == INT_MAX) {\n                        dist[pair_v[v]] = dist[u] + 1;\n                        q.push(pair_v[v]);\n                    }\n                }\n            }\n        }\n        return dist[0] != INT_MAX;\n    }\n    bool dfs(int u) {\n        if (u == 0) return true;\n        for (int v : adj[u]) {\n            if (dist[pair_v[v]] == dist[u] + 1 && dfs(pair_v[v])) {\n                pair_v[v] = u; pair_u[u] = v;\n                return true;\n            }\n        }\n        dist[u] = INT_MAX;\n        return false;\n    }\n    int max_matching() {\n        int matching = 0;\n        while (bfs()) for (int u = 1; u <= n; ++u) if (pair_u[u] == 0 && dfs(u)) matching++;\n        return matching;\n    }\n};",
        "recognitionPatterns": [
            "Bipartite graph matching where $N, M \\le 5 \\times 10^4$ and $E \\le 2 \\times 10^5$ (Kuhn's $\\mathcal{O}(V E)$ will TLE; Hopcroft-Karp/Dinic passes in 100ms).",
            "Maximum Independent Set on bipartite graph ($|MIS| = |V| - |\\text{Max Matching}|$).",
            "Minimum Vertex Cover on bipartite graph (Kőnig's Theorem: $|\\text{MVC}| = |\\text{Max Matching}|$).",
            "Minimum Path Cover in a Directed Acyclic Graph (DAG)."
        ],
        "commonBugs": [
            "Off-by-one indexing on 0-based vs 1-based left/right partitions (Hopcroft-Karp uses index 0 as dummy unmatched node).",
            "Graph is not bipartite: applying Hopcroft-Karp or Dinic bipartite reduction on general graphs with odd cycles fails (requires Edmond's Blossom).",
            "Forgetting to reconstruct minimum vertex cover by DFS reachability from unmatched left vertices in residual graph.",
            "Reusing `dist` array across iterations without re-clearing."
        ]
    },
    "09-matching-vs-general-flow": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1800–2400\n- Prerequisites: Max Flow, Bipartite Matching, General Matching (Blossom), Capacitated Networks\n- Tradeoff: Deciding between specialized bipartite matching, general graph matching, and general network flow models.",
        "coreIntuition": "When encountering an assignment problem, check graph structure: 1) Is the graph bipartite? If yes and unweighted, use Hopcroft-Karp or Dinic $\\mathcal{O}(E \\sqrt{V})$. 2) Is it bipartite with edge costs? Use Hungarian algorithm $\\mathcal{O}(V^3)$ or MCMF $\\mathcal{O}(F \\cdot E \\log V)$. 3) Is the graph general (non-bipartite, odd cycles present)? Bipartite matching and network flow FAIL! You must use Blossom Algorithm $\\mathcal{O}(V^3)$ or Tutte matrix randomized matching. 4) Do vertices or edges have capacities $> 1$, or intermediate transit nodes? General network flow is mandatory.",
        "derivation": "Max flow models rely on the total unimodularity of bipartite incidence matrices: the linear programming relaxation has integral extreme points. In general non-bipartite graphs, odd cycles introduce fractional vertices (e.g., triangle with 0.5 flow on each edge gives 1.5 matching, impossible for discrete matching). Edmonds' Blossom algorithm contracts odd cycles into supernodes to restore augmenting path properties.",
        "templateCpp": "// Decision Matrix Dispatcher\n// General Network Flow vs Bipartite Matching\n#include <bits/stdc++.h>\nusing namespace std;\n\n// Check if graph is 2-colorable (bipartite)\nbool is_bipartite(int n, const vector<vector<int>>& adj, vector<int>& color) {\n    color.assign(n + 1, -1);\n    for (int i = 1; i <= n; ++i) {\n        if (color[i] != -1) continue;\n        queue<int> q; q.push(i); color[i] = 0;\n        while (!q.empty()) {\n            int u = q.front(); q.pop();\n            for (int v : adj[u]) {\n                if (color[v] == -1) {\n                    color[v] = 1 - color[u];\n                    q.push(v);\n                } else if (color[v] == color[u]) return false; // Odd cycle found!\n            }\n        }\n    }\n    return true;\n}",
        "recognitionPatterns": [
            "Grid cells where interactions occur only between adjacent cells (grids are naturally bipartite: $(r + c) \\pmod 2$).",
            "Domino tiling problems: bipartite matching between black and white checkerboard squares.",
            "Pairing items where relationships form arbitrary non-bipartite friendship graphs (requires Blossom).",
            "Multi-commodity or capacitated bounds per node: split node into $u_{\\text{in}} \\to u_{\\text{out}}$ with capacity $c_u$."
        ],
        "commonBugs": [
            "Modeling general matching (odd cycles present) as a flow network: flow networks cannot handle non-bipartite vertex packing.",
            "Forgetting node capacities: to restrict a vertex to be used at most $K$ times, split $u \\to (u_{in}, u_{out})$ with capacity $K$.",
            "Ignoring disconnected components when checking bipartiteness.",
            "Attempting to run Blossom algorithm when the constraints indicate $N \\le 500$, but simple DP on tree or greedy would suffice."
        ]
    },
    "09-mcmf-vs-greedy": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 2000–2600\n- Prerequisites: Min-Cost Max-Flow (MCMF), Slope Trick, Priority Queue / Regret Greedy\n- Tradeoff: MCMF guarantees global optimality on complex network topologies but is $\\mathcal{O}(F \\cdot E \\log V)$; Greedy with regret (simulated network flow) runs in $\\mathcal{O}(N \\log N)$ on linear or tree topologies.",
        "coreIntuition": "MCMF and greedy are two ends of convex optimization. When the underlying graph is a 1D sequence (e.g., buy/sell stock with transaction fees, pairing parentheses, matching intervals on a line), the min-cost flow problem exhibits total unimodularity and convexity. Instead of running a general graph MCMF algorithm, you can 'simulate' the augmenting paths of MCMF using two priority queues (Slope Trick / Regret Greedy). If the topology is an arbitrary graph or bipartite with irregular edges, general MCMF is required.",
        "derivation": "The cost of sending $k$ units of flow $f(k)$ is piecewise linear and strictly convex: $f(k+1) - f(k) \\ge f(k) - f(k-1)$ due to shortest augmenting path potentials. In 1D interval problems, the dual problem is equivalent to optimizing a convex function under slope changes. A priority queue tracks potential slopes, and choosing an element corresponds to augmenting flow; pushing the negative back into the queue allows the algorithm to 'cancel' or 'regret' an earlier choice along a residual backward edge in $\\mathcal{O}(\\log N)$ time.",
        "templateCpp": "// Simulated Network Flow / Regret Greedy (Slope Trick) in O(N log N)\n// Example: Buy and Sell Stock with Regret\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nll simulated_mcmf_buy_sell(const vector<ll>& prices) {\n    priority_queue<ll, vector<ll>, greater<ll>> pq;\n    ll total_profit = 0;\n    for (ll p : prices) {\n        if (!pq.empty() && pq.top() < p) {\n            total_profit += p - pq.top();\n            pq.pop();\n            pq.push(p); // Can regret selling here if a higher future price exists\n        }\n        pq.push(p); // Option to buy at current price\n    }\n    return total_profit;\n}",
        "recognitionPatterns": [
            "Problem asks for min-cost matching of points on a line or timestamps in a schedule ($N \\approx 2 \\times 10^5$, MCMF would TLE).",
            "Arbitrary bipartite graph where left side wants to match right side with minimum total cost ($N \\le 500$, reach for MCMF).",
            "Convex cost functions on edge flows (piecewise linear cost).",
            "Workload distribution where previous decisions can be revoked if a more profitable option arrives."
        ],
        "commonBugs": [
            "Attempting MCMF with $N = 10^5$; standard MCMF will heavily TLE (needs $\\mathcal{O}(N \\log N)$ simulated flow).",
            "In simulated flow, forgetting the regret element: failing to push the new state back into the priority queue prevents cancellation.",
            "Handling negative cycles in general MCMF without proper initial potentials or Bellman-Ford/SPFA initialization.",
            "Using floating-point costs without epsilon checks in MCMF."
        ]
    },
    "10-d-c-dp-vs-knuth": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2500\n- Prerequisites: Dynamic Programming, Monotonicity of Optimal Split, Quadrangle Inequality\n- Tradeoff: Reduces $\\mathcal{O}(K N^2)$ or $\\mathcal{O}(N^3)$ 2D DP to $\\mathcal{O}(K N \\log N)$ or $\\mathcal{O}(N^2)$ via monotonicity.",
        "coreIntuition": "Both Divide & Conquer DP optimization and Knuth's optimization exploit the monotonicity of the optimal decision point: $\\text{opt}(i, j) \\le \\text{opt}(i, j+1)$. 1) Use **Divide and Conquer DP** when the transition is between distinct layers $dp[k][i] = \\min_{j < i} (dp[k-1][j] + \\text{cost}(j, i))$. The layer structure allows solving mid-point $mid = (l + r)/2$ and dividing the search range for the remaining indices, achieving $\\mathcal{O}(K N \\log N)$. 2) Use **Knuth's Optimization** when the DP is interval-based $dp[i][j] = \\min_{i \\le k < j} (dp[i][k] + dp[k+1][j]) + \\text{cost}(i, j)$ and optimal split satisfies $\\text{opt}(i, j-1) \\le \\text{opt}(i, j) \\le \\text{opt}(i+1, j)$. The search space telescopically sums to $\\mathcal{O}(N^2)$!",
        "derivation": "Quadrangle Inequality: $\\text{cost}(a, c) + \\text{cost}(b, d) \\le \\text{cost}(a, d) + \\text{cost}(b, c)$ for $a \\le b \\le c \\le d$. In D&C DP, the monotonic property $\\text{opt}(k, i) \\le \\text{opt}(k, i+1)$ allows partitioning the search interval $[\\text{optL}, \\text{optR}]$ at each divide-and-conquer level. In Knuth's optimization, the sum of loop bounds is $\\sum_{i, j} (\\text{opt}(i+1, j) - \\text{opt}(i, j-1)) = \\sum_{len} \\mathcal{O}(N) = \\mathcal{O}(N^2)$.",
        "templateCpp": "// Divide and Conquer DP Optimization: O(K * N log N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nll dp[25][5005];\nll cost(int j, int i); // Contest-specific cost function\n\nvoid compute(int k, int l, int r, int optL, int optR) {\n    if (l > r) return;\n    int mid = (l + r) / 2;\n    pair<ll, int> best = {1e18, -1};\n    for (int j = optL; j <= min(mid, optR); ++j) {\n        best = min(best, {dp[k - 1][j] + cost(j, mid), j});\n    }\n    dp[k][mid] = best.first;\n    int opt = best.second;\n    compute(k, l, mid - 1, optL, opt);\n    compute(k, mid + 1, r, opt, optR);\n}",
        "recognitionPatterns": [
            "Partitioning an array of length $N$ into $K$ contiguous subarrays to minimize sum of costs ($K \\le 50, N \\le 5000$).",
            "Optimal binary search tree or merging adjacent elements on interval $[i, j]$ (Knuth optimization).",
            "Cost function satisfies Quadrangle Inequality / Monge property.",
            "Testing brute force reveals that $\\text{opt}[i] \\le \\text{opt}[i+1]$ unconditionally."
        ],
        "commonBugs": [
            "Attempting D&C DP when transitions depend on the current layer (e.g., $dp[k][i]$ depends on $dp[k][j]$ where $j < i$); D&C requires dependencies to be strictly on the previous layer $k-1$.",
            "Knuth optimization index bounds: iterating length from smallest to largest is required so that $\\text{opt}[i+1][j]$ and $\\text{opt}[i][j-1]$ are already computed.",
            "Cost function does not satisfy Quadrangle Inequality (e.g., non-convex or non-monotonic penalties), yielding incorrect answers.",
            "Off-by-one errors in `min(mid, optR)` bounding inside D&C."
        ]
    },
    "10-cht-vs-li-chao": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2500\n- Prerequisites: Convex Hull Trick (CHT), Li Chao Segment Tree, Line Geometry\n- Tradeoff: CHT is $\\mathcal{O}(N)$ or $\\mathcal{O}(N \\log N)$ but requires monotonic slopes/queries or dynamic pointers (LineContainer); Li Chao Tree handles arbitrary slope/query insertions in $\\mathcal{O}(\\log C)$ with minimal bug surface.",
        "coreIntuition": "When optimizing transitions of the form $dp[i] = \\min_j (dp[j] + m_j \\cdot x_i + c_j)$: 1) Use **Monotonic CHT (Deque)** if slopes $m_j$ are added in sorted order and query points $x_i$ are sorted: runs in pure $\\mathcal{O}(N)$ time with 15 lines of code. 2) Use **LineContainer (Dynamic CHT)** if slopes or queries arrive in arbitrary order and coordinates are continuous reals/large integers: maintains upper/lower hull via `std::set` in $\\mathcal{O}(\\log N)$ per operation. 3) Use **Li Chao Segment Tree** if queries are over a fixed coordinate domain $[X_{\\min}, X_{\\max}]$ (e.g., $[1, 10^6]$ or via coordinate compression) or when line segments (restricted intervals $[l_j, r_j]$) are inserted: stores dominant lines in segment tree nodes with trivial maintenance.",
        "derivation": "In dynamic CHT, lines form the lower envelope of a family of affine functions. Adjacent lines intersect at $x = (c_1 - c_2) / (m_2 - m_1)$. In a Li Chao Tree over interval $[L, R]$ with midpoint $M$, inserting a new line $L_{new}$ into a node holding line $L_{cur}$ compares values at $M$: the winning line remains at the node, and the losing line can only possibly dominate in the half where it was better at the boundary. Hence, recursion descends into only one child, running in $\\mathcal{O}(\\log(R - L))$.",
        "templateCpp": "// Li Chao Tree for Min Queries (Handles arbitrary slopes & insertions)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 2e18;\n\nstruct Line { ll m, c; ll eval(ll x) const { return m * x + c; } };\n\nstruct LiChaoTree {\n    int sz;\n    vector<Line> tree;\n    LiChaoTree(int sz_) : sz(sz_), tree(4 * sz_, {0, INF}) {}\n    void add_line(int node, int l, int r, Line newline) {\n        int mid = l + (r - l) / 2;\n        bool left_better = newline.eval(l) < tree[node].eval(l);\n        bool mid_better = newline.eval(mid) < tree[node].eval(mid);\n        if (mid_better) swap(tree[node], newline);\n        if (r - l == 1) return;\n        if (left_better != mid_better) add_line(2 * node, l, mid, newline);\n        else add_line(2 * node + 1, mid, r, newline);\n    }\n    ll query(int node, int l, int r, ll x) {\n        ll res = tree[node].eval(x);\n        if (r - l == 1) return res;\n        int mid = l + (r - l) / 2;\n        if (x < mid) return min(res, query(2 * node, l, mid, x));\n        else return min(res, query(2 * node + 1, mid, r, x));\n    }\n};",
        "recognitionPatterns": [
            "DP equation contains a cross term of the form $a_j \\cdot b_i$.",
            "Slopes and query points both monotonic: implement $\\mathcal{O}(N)$ Monotone CHT with `std::deque`.",
            "Slopes or queries are not monotonic: reach for Li Chao tree or LineContainer.",
            "Lines are only valid on a restricted segment $[L_j, R_j]$: Li Chao segment tree handles segment updates in $\\mathcal{O}(\\log^2 C)$ naturally."
        ],
        "commonBugs": [
            "Integer overflow in cross product or intersection point calculation $(c_1 - c_2) / (m_2 - m_1)$; use `__int128`.",
            "Division truncation in integer arithmetic: standard integer `/` rounds toward zero; floor division requires `x / y - ((x ^ y) < 0 && x % y)`.",
            "Querying outside the predefined $[L, R]$ coordinate range in Li Chao tree without dynamic pointer node allocation.",
            "Mixing up Min vs Max envelope logic when flipping sign of slopes."
        ]
    },
    "10-alien-trick-vs-wqs-binary-search": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common in Div1 D/E & ICPC Regionals\n- Typical CF/ICPC rating range: 2200–2700\n- Prerequisites: Convex Optimization, Lagrange Multipliers, Binary Search, DP\n- Tradeoff: Eliminates a state dimension $K$ (e.g. choose exactly $K$ items) from $\\mathcal{O}(N K)$ down to $\\mathcal{O}(N \\log(\\text{cost}))$.",
        "coreIntuition": "Alien's Trick and WQS Binary Search are two names for the same algorithmic technique: Lagrangian relaxation applied to convex DP. When the maximum profit $f(k)$ as a function of the number of chosen items $k$ is strictly concave (or convex for cost minimization), the constraint 'choose exactly $K$ items' can be relaxed by introducing a penalty $\\lambda$ for each chosen item. By binary searching on $\\lambda$, we find the slope of the tangent line touching the curve at $k = K$, solving the problem without maintaining $k$ in the DP state!",
        "derivation": "Let $g(\\lambda) = \\max_k (f(k) - \\lambda k)$. The function $g(\\lambda)$ is the Legendre transform of $f(k)$. For a fixed $\\lambda$, the unconstrained problem $\\max_k (f(k) - \\lambda k)$ can be evaluated in $\\mathcal{O}(N)$ time, returning both the optimal value and the number of items chosen $k^*$. Since $f$ is concave, the optimal $k^*(\\lambda)$ is a monotonically decreasing function of $\\lambda$. Binary search on $\\lambda$ finds $\\lambda^*$ such that $k^*(\\lambda^*) = K$. The original answer is then $g(\\lambda^*) + \\lambda^* K$.",
        "templateCpp": "// Aliens Trick / WQS Binary Search Template\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\n// Solve unconstrained DP with penalty lambda per item\npair<ll, int> solve_unconstrained(ll lambda, int n);\n\nll aliens_trick(int n, int k, ll low_penalty, ll high_penalty) {\n    ll l = low_penalty, r = high_penalty, best_lambda = 0;\n    while (l <= r) {\n        ll mid = l + (r - l) / 2;\n        auto [val, cnt] = solve_unconstrained(mid, n);\n        if (cnt >= k) {\n            best_lambda = mid;\n            l = mid + 1; // Increase penalty to pick fewer items\n        } else {\n            r = mid - 1;\n        }\n    }\n    auto [val, cnt] = solve_unconstrained(best_lambda, n);\n    return val + best_lambda * k;\n}",
        "recognitionPatterns": [
            "Problem specifies 'choose exactly $K$ disjoint subsegments/elements' to maximize/minimize total weight.",
            "Standard DP is $dp[i][k]$ taking $\\mathcal{O}(N K)$ or $\\mathcal{O}(N^2 K)$, where $K, N \\le 2 \\times 10^5$.",
            "Plotting or mathematically checking $f(k)$ shows diminishing returns (strict concavity / quadrangle inequality).",
            "Tree partitioning into exactly $K$ connected components with optimal weight."
        ],
        "commonBugs": [
            "Function $f(k)$ is not concave/convex; applying Aliens trick on non-convex functions yields completely wrong answers.",
            "Collinear points on the hull: multiple values of $k$ share the same slope $\\lambda$. When tie-breaking, consistently choose either the minimum or maximum items chosen to ensure binary search converges.",
            "Off-by-one in binary search range $[\\text{low}, \\text{high}]$: penalty bounds must cover $[-2 \\times \\max|v|, 2 \\times \\max|v|]$.",
            "Forgetting to add back the penalty `+ best_lambda * k` to the final answer."
        ]
    },
    "10-monotone-queue-vs-monotone-stack-dp": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1500–2100\n- Prerequisites: Two Pointers, Monotone Deque, Monotone Stack\n- Tradeoff: Sliding window extrema vs nearest smaller/larger bounding indices.",
        "coreIntuition": "1) **Monotone Queue (Deque)** optimizes DP transitions over a sliding window: $dp[i] = \\min_{i - W \\le j < i} (dp[j]) + c_i$. The window boundaries $[i - W, i - 1]$ move monotonically to the right. A deque maintains candidate values in increasing order of cost and pops elements from the front when they fall out of the sliding window, achieving $\\mathcal{O}(1)$ amortized transition. 2) **Monotone Stack** finds nearest greater/smaller elements for each position $i$ (e.g. largest rectangle in histogram, finding the maximal subsegment where $a_i$ is the minimum). The stack pops elements that violate monotonicity, but does NOT enforce a sliding window length.",
        "derivation": "Monotone Deque invariant: for indices $j_1 < j_2$ stored in the deque, we must have $dp[j_1] < dp[j_2]$. If a newly considered index $i$ has $dp[i] \\le dp[j]$, then $j$ can never be the optimum for any future window containing $i$, because $i$ is both smaller and lives longer. Thus, elements with $\\ge dp[i]$ are popped from the back. Since every index is pushed and popped at most once, total amortized time across all $N$ steps is $\\mathcal{O}(N)$.",
        "templateCpp": "// Monotone Queue DP: Sliding Window Min Transition in O(N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nvector<ll> sliding_window_min_dp(int n, int k, const vector<ll>& cost) {\n    vector<ll> dp(n + 1, 0);\n    deque<int> dq;\n    dq.push_back(0); // dp[0] = 0\n    for (int i = 1; i <= n; ++i) {\n        // Pop elements outside window [i - k, i - 1]\n        while (!dq.empty() && dq.front() < i - k) dq.pop_front();\n        dp[i] = dp[dq.front()] + cost[i - 1];\n        // Maintain monotonic increasing order in deque\n        while (!dq.empty() && dp[dq.back()] >= dp[i]) dq.pop_back();\n        dq.push_back(i);\n    }\n    return dp;\n}",
        "recognitionPatterns": [
            "DP transition looks like $dp[i] = \\min_{j \\in [i - L, i - R]} dp[j] + f(i)$ (Monotone Queue).",
            "Finding the left and right boundary where $a[i]$ remains the minimum/maximum of the range (Monotone Stack).",
            "Sliding window maximum/minimum in an array (Monotone Queue).",
            "Histogram rectangle area or Cartesian Tree construction (Monotone Stack)."
        ],
        "commonBugs": [
            "Empty deque access: calling `dq.front()` before verifying `!dq.empty()`.",
            "Popping order confusion: front is popped for window expiry (`dq.front() < i - k`), back is popped for monotonicity (`dp[dq.back()] >= dp[i]`).",
            "Strict vs non-strict inequalities: duplicate values can cause improper early popping in monotone stack problems.",
            "Index offset errors between 0-indexed arrays and 1-indexed DP arrays."
        ]
    },
    "13-recognition-shortcuts": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1/Div2 Hard\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: Bitwise operations, Submask enumeration, SOS DP, Fast Walsh-Hadamard Transform (FWHT)\n- Tradeoff: Recognizing the exact bitwise algorithm immediately from $N$ and problem constraints.",
        "coreIntuition": "Bitwise problem constraints form an infallible recognition matrix: 1) $N \\le 20 \\implies$ Iterate all submasks $\\sum_{mask} 2^{|mask|} = 3^N \\approx 3.5 \\times 10^9$ (or $N \\le 16 \\implies 3^{16} = 4.3 \\times 10^7$). 2) $N \\le 24 \\implies$ Sum Over Subsets (SOS) DP in $\\mathcal{O}(N \\cdot 2^N) \\approx 4 \\times 10^8$ operations. 3) $N \\le 20$ with bitwise AND/OR/XOR convolution $c_k = \\sum_{i \\star j = k} a_i b_j \\implies$ Fast Walsh-Hadamard Transform (FWHT) in $\\mathcal{O}(N \\cdot 2^N)$. 4) Subset Convolution (enforcing disjoint sets $i \\cup j = k$ with $i \\cap j = \\emptyset$) $\\implies$ Ranked SOS DP in $\\mathcal{O}(N^2 \\cdot 2^N)$.",
        "derivation": "Submask iteration loop `for (int sub = mask; sub; sub = (sub - 1) & mask)` visits each pair $(sub, mask)$ such that $sub \\subseteq mask$. The total number of iterations is $\\sum_{k=0}^N \\binom{N}{k} 2^k = (1 + 2)^N = 3^N$. SOS DP computes prefix sums along Boolean hypercube dimensions: iterating coordinate bit $i$ from $0$ to $N-1$ updates $dp[mask] += dp[mask \\oplus 2^i]$ if bit $i$ is set, evaluating all subset sums in exactly $N \\cdot 2^N$ operations.",
        "templateCpp": "// Bitwise Recognition Toolkit: Submask Enumeration & SOS DP\n#include <bits/stdc++.h>\nusing namespace std;\n\n// 1. All submasks enumeration: O(3^N)\nvoid enumerate_submasks(int n) {\n    for (int mask = 0; mask < (1 << n); ++mask) {\n        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {\n            // process submask 'sub' of 'mask'\n        }\n    }\n}\n\n// 2. Sum Over Subsets (SOS) DP: O(N * 2^N)\nvoid sos_dp(int n, vector<int>& f) {\n    for (int i = 0; i < n; ++i) {\n        for (int mask = 0; mask < (1 << n); ++mask) {\n            if (mask & (1 << i)) {\n                f[mask] += f[mask ^ (1 << i)];\n            }\n        }\n    }\n}",
        "recognitionPatterns": [
            "Constraints state $N \\le 20$ or $N \\le 24$ (universal signal for bitmask / SOS DP).",
            "Count pairs $(i, j)$ such that $a_i \\text{ AND } a_j = 0$ (SOS DP on complement mask $\\sim a_i$).",
            "Finding shortest Hamiltonian path / Traveling Salesperson Problem on $N \\le 20$ vertices.",
            "Set cover or partition problems where items are represented as bit flags."
        ],
        "commonBugs": [
            "Submask iteration infinite loop: using `sub >= 0` instead of `sub > 0` causes `(0 - 1) & mask = mask`, looping infinitely.",
            "Loop order in SOS DP: outer loop MUST iterate over dimension $i \\in [0, N-1]$ and inner loop over masks to correctly accumulate multi-dimensional prefix sums.",
            "Bitwise operator precedence: `1 << n - 1` evaluates as `1 << (n - 1)`. Always use parentheses `(1 << n) - 1` and `(mask & (1 << i))`.",
            "Integer overflow: using 32-bit `int` for bit shifts when $N \\ge 31$; use `1LL << i`."
        ]
    },
    "17-integer-cross-vs-floats": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Universal in Computational Geometry\n- Typical CF/ICPC rating range: 1400–2500\n- Prerequisites: Vector cross product, dot product, orientation tests\n- Tradeoff: Floating-point arithmetic suffers from precision breakdown, epsilon tuning nightmares, and `NaN` errors; integer cross products are 100% exact and deterministic.",
        "coreIntuition": "In computational geometry, 95% of contest problems can and should be solved using pure 64-bit or 128-bit integer arithmetic. The cross product of vectors $\\vec{u} = (x_1, y_1)$ and $\\vec{v} = (x_2, y_2)$ is $\\vec{u} \\times \\vec{v} = x_1 y_2 - x_2 y_1$. Its sign deterministically tells whether $\\vec{v}$ turns counter-clockwise ($> 0$), clockwise ($< 0$), or is collinear ($= 0$) with $\\vec{u}$. Never use `atan2`, slope division $y/x$, or `double` trigonometry to check orientation or sorting.",
        "derivation": "The 2D cross product equals the signed area of the parallelogram formed by $\\vec{u}$ and $\\vec{v}$. For integer coordinates bounded by $C = 10^9$, the cross product $x_1 y_2 - x_2 y_1$ reaches up to $2 \\times 10^{18}$, which fits within signed 64-bit integer `long long`. For products of differences $(x_b - x_a)(y_c - y_a) - (y_b - y_a)(x_c - x_a)$, maximum magnitude is $4 \\times 10^{18}$, comfortably within `long long` (or `__int128_t` for intermediate calculations to prevent any overflow).",
        "templateCpp": "// 100% Exact Integer Geometry Point & Orientation Test\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Point {\n    ll x, y;\n    Point operator-(const Point& o) const { return {x - o.x, y - o.y}; }\n    ll cross(const Point& o) const { return x * o.y - y * o.x; }\n    ll dot(const Point& o) const { return x * o.x + y * o.y; }\n};\n\n// Returns: +1 for CCW (left turn), -1 for CW (right turn), 0 for Collinear\nint orient(Point a, Point b, Point c) {\n    __int128 val = (__int128)(b.x - a.x) * (c.y - a.y) - (__int128)(b.y - a.y) * (c.x - a.x);\n    if (val > 0) return 1;\n    if (val < 0) return -1;\n    return 0;\n}",
        "recognitionPatterns": [
            "Convex Hull construction (Monotone Chain / Graham Scan).",
            "Checking whether two line segments intersect.",
            "Testing if a point lies to the left or right of a directed line.",
            "Sorting points radially around a pivot (half-plane radial sorting without `atan2`)."
        ],
        "commonBugs": [
            "Using `float` or `double` slopes $m = (y_2 - y_1)/(x_2 - x_1)$, causing division by zero on vertical lines and rounding errors on nearly collinear points.",
            "32-bit integer overflow: cross product of coordinates up to $10^5$ exceeds $2^{31} - 1$; always use `long long` or `__int128`.",
            "Using `acos` or `asin` without clamping argument to $[-1.0, 1.0]$, producing `NaN` due to slight floating point drift.",
            "Comparing floats with strict `== 0.0` instead of `std::abs(x) < 1e-9` when floats are unavoidable."
        ]
    },
    "17-ray-casting-vs-winding-point-in-polygon": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1700–2300\n- Prerequisites: Point in Polygon, Ray Casting, Winding Number, Cross Product\n- Tradeoff: Ray casting is simple parity counting but has tricky boundary edge cases; winding number is robust against complex/self-intersecting polygons.",
        "coreIntuition": "To determine whether a query point $P$ lies inside a polygon: 1) **Ray Casting Algorithm** shoots a horizontal ray from $P$ to $(+\\infty, y_P)$ and counts intersections with polygon edges. If the number of crossings is odd, $P$ is inside; if even, $P$ is outside. 2) **Winding Number Algorithm** computes the total number of counter-clockwise revolutions made by the polygon boundaries around $P$. Non-zero winding number $\\implies$ inside. Winding number handles self-intersecting polygons and is immune to vertex-grazing ambiguities when implemented with cross product signs.",
        "derivation": "Jordan Curve Theorem: Any continuous simple closed curve divides the plane into an 'inside' and an 'outside'. A ray starting from infinity (outside) alternates between inside and outside with each boundary crossing. For winding number, edge $(A, B)$ contributes $+1$ to the winding count if it crosses the horizontal ray upwards and $P$ is to the left of the edge, and $-1$ if it crosses downwards and $P$ is to the right.",
        "templateCpp": "// Robust Point in Polygon via Winding Number (Integer Precision)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Point { ll x, y; };\nll cross_product(Point a, Point b, Point c) {\n    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);\n}\n\n// Returns: 1 if inside, 0 if outside, -1 if strictly on boundary\nint point_in_polygon(Point p, const vector<Point>& poly) {\n    int n = poly.size();\n    int wn = 0;\n    for (int i = 0; i < n; ++i) {\n        Point a = poly[i], b = poly[(i + 1) % n];\n        // Check if p is on segment ab\n        if (cross_product(a, b, p) == 0 &&\n            min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&\n            min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y)) return -1;\n        if (a.y <= p.y) {\n            if (b.y > p.y && cross_product(a, b, p) > 0) wn++;\n        } else {\n            if (b.y <= p.y && cross_product(a, b, p) < 0) wn--;\n        }\n    }\n    return wn != 0 ? 1 : 0;\n}",
        "recognitionPatterns": [
            "Query asks whether a point lies strictly inside, outside, or on the boundary of an arbitrary polygon.",
            "Geofencing or territorial containment queries in computational geometry.",
            "Polygon triangulation or ear clipping preprocessing.",
            "Testing point containment in non-convex polygons where binary search on angle cannot be used."
        ],
        "commonBugs": [
            "Ray passes exactly through a polygon vertex: standard ray casting double-counts or misses the intersection unless half-open vertical intervals $[y_1, y_2)$ are strictly enforced.",
            "Horizontal polygon edges: ray overlaps collinear horizontal edges; ensure horizontal segments are ignored or explicitly handled.",
            "Forgetting boundary check: query point lies exactly on an edge or vertex, but the algorithm reports strictly inside or outside.",
            "Polygon vertices not oriented in consistent order (CCW or CW)."
        ]
    },
    "17-rotating-calipers-vs-n": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Convex Hull, Antipodal Pairs, Cross Product, Two Pointers\n- Tradeoff: Reduces polygon diameter / minimum bounding box from $\\mathcal{O}(N^2)$ brute force to $\\mathcal{O}(N)$ after $\\mathcal{O}(N \\log N)$ convex hull.",
        "coreIntuition": "To find the maximum distance between any two points in a 2D set of $N$ points (the polygon diameter), checking all pairs takes $\\mathcal{O}(N^2)$, which TLEs for $N = 2 \\times 10^5$. The two furthest points must both lie on the vertices of the Convex Hull. Furthermore, the distance from an edge $(P_i, P_{i+1})$ to hull vertices is unimodal: as we advance along hull edges, the furthest opposite vertex (antipodal point) advances monotonically in the same direction. Rotating Calipers maintains an antipodal pointer with two pointers, traversing the entire convex hull in $\\mathcal{O}(N)$ total steps!",
        "derivation": "The distance from a point $C$ to the line through $A$ and $B$ is proportional to the triangle area $|(B - A) \\times (C - A)|$. Because the polygon is convex, the area function is strictly unimodal. When we advance the base edge from $(P_i, P_{i+1})$ to $(P_{i+1}, P_{i+2})$, the peak of the triangle area also advances counter-clockwise. Thus, the antipodal pointer index $j$ only advances forward and never retreats, wrapping around $N$ vertices in at most $2N$ steps.",
        "templateCpp": "// Rotating Calipers: Convex Polygon Diameter in O(N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Point {\n    ll x, y;\n    ll dist_sq(const Point& o) const { return (x - o.x) * (x - o.x) + (y - o.y) * (y - o.y); }\n};\n\nll cross_product(Point a, Point b, Point c) {\n    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);\n}\n\n// Returns maximum squared Euclidean distance between any pair of points on convex hull\nll rotating_calipers_diameter(const vector<Point>& hull) {\n    int n = hull.size();\n    if (n < 2) return 0;\n    if (n == 2) return hull[0].dist_sq(hull[1]);\n    ll max_dist = 0;\n    int j = 1;\n    for (int i = 0; i < n; ++i) {\n        Point next_i = hull[(i + 1) % n];\n        while (cross_product(hull[i], next_i, hull[(j + 1) % n]) >\n               cross_product(hull[i], next_i, hull[j])) {\n            j = (j + 1) % n;\n        }\n        max_dist = max({max_dist, hull[i].dist_sq(hull[j]), next_i.dist_sq(hull[j])});\n    }\n    return max_dist;\n}",
        "recognitionPatterns": [
            "Find the maximum Euclidean distance between any two points among $N \\le 2 \\times 10^5$ points.",
            "Minimum enclosing bounding box (minimum area or perimeter rectangle enclosing point set).",
            "Maximum area triangle inscribed in a convex polygon.",
            "Widest empty corridor between two disjoint convex point sets."
        ],
        "commonBugs": [
            "Running Rotating Calipers on raw points without computing the Convex Hull first.",
            "Handling collinear edges on the convex hull: strictly greater `>` vs `>=` in cross product area comparison.",
            "Degenerate hull size: $N = 1$ or $N = 2$ causes infinite while loop if modular indexing is not guarded.",
            "Using floating-point sqrt when the problem asks for squared distance, losing precision on large coordinates."
        ]
    }
}
