# Group 1: Drill & Meta Overviews (32 topics)

G1_DATA = {
    "06-what-to-drill-this-week": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1600–2400\n- Prerequisites: Tree traversals, LCA, Euler Tour, Heavy-Light Decomposition",
        "coreIntuition": "Tree algorithms in rated contests test structural reductions: converting arbitrary tree paths or subtree aggregates into contiguous ranges on an array via Euler tours and heavy paths. Master binary lifting for static tree paths, subtree difference arrays for subtree updates, and HLD for dynamic path operations.",
        "derivation": "A rooted tree of $N$ vertices can be linearized into an Euler tour of length $N$ or $2N$. For any vertex $u$, its subtree corresponds to the contiguous interval $[\\text{tin}[u], \\text{tout}[u]]$. Any path $u \\leftrightarrow v$ decomposes into $\\mathcal{O}(\\log N)$ contiguous segments under Heavy-Light Decomposition.",
        "templateCpp": "// Tree Drill Pipeline: LCA, Subtree Ranges, and Binary Lifting\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct TreeDrill {\n    int n, LOG;\n    vector<vector<int>> adj, up;\n    vector<int> depth, tin, tout;\n    int timer = 0;\n    TreeDrill(int n_) : n(n_), LOG(__lg(n_) + 2), adj(n_ + 1), up(LOG, vector<int>(n_ + 1)), depth(n_ + 1), tin(n_ + 1), tout(n_ + 1) {}\n    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }\n    void dfs(int u, int p) {\n        tin[u] = ++timer;\n        up[0][u] = p;\n        for (int i = 1; i < LOG; ++i) up[i][u] = up[i - 1][up[i - 1][u]];\n        for (int v : adj[u]) if (v != p) { depth[v] = depth[u] + 1; dfs(v, u); }\n        tout[u] = timer;\n    }\n    int get_lca(int u, int v) {\n        if (depth[u] < depth[v]) swap(u, v);\n        for (int k = LOG - 1; k >= 0; --k) if (depth[u] - (1 << k) >= depth[v]) u = up[k][u];\n        if (u == v) return u;\n        for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }\n        return up[0][u];\n    }\n};",
        "recognitionPatterns": [
            "Queries over arbitrary tree paths $u \\leftrightarrow v$ with point or range updates.",
            "Subtree color frequency counting (DSU on Tree / Small-to-Large merging).",
            "Path bottleneck queries where edge weights represent capacities or tolerances.",
            "Distance queries among dynamically added or deleted nodes (Centroid Tree)."
        ],
        "commonBugs": [
            "Forgetting 1-based vs 0-based indexing on tree Euler tours.",
            "Rooting the tree at an arbitrary vertex when directed edges require topological ordering.",
            "LCA query fails when start and end vertices are identical ($u = v$).",
            "Stack overflow in deep skew trees without `#pragma comment(linker)` or manual iterative DFS."
        ]
    },
    "08-part-a-08-a-shortest-paths-md-08-a-shortest-paths-md": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1400–2200\n- Prerequisites: Graph representation, adjacency lists, priority queues",
        "coreIntuition": "Shortest path algorithms are the primary workhorse for state-space exploration. The optimal algorithm is determined strictly by edge weight characteristics: unit weights $\\implies$ BFS $\\mathcal{O}(V + E)$; weights in $\\{0, 1\\} \\implies$ 0-1 BFS $\\mathcal{O}(V + E)$; non-negative weights $\\implies$ Dijkstra $\\mathcal{O}((V + E) \\log V)$; arbitrary weights $\\implies$ Bellman-Ford $\\mathcal{O}(V \\cdot E)$.",
        "derivation": "Dijkstra relies on the triangle inequality $d(v) \\le d(u) + w(u, v)$ and greedily finalizes the minimum distance unvisited vertex. Non-negativity guarantees that once popped from the priority queue, $d(u)$ is optimal.",
        "templateCpp": "// State-space Dijkstra template\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\nvector<ll> dijkstra(int n, int src, const vector<vector<pair<int, ll>>>& adj) {\n    vector<ll> dist(n + 1, INF);\n    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;\n    dist[src] = 0; pq.push({0, src});\n    while (!pq.empty()) {\n        auto [d, u] = pq.top(); pq.pop();\n        if (d > dist[u]) continue;\n        for (auto& [v, w] : adj[u]) {\n            if (dist[u] + w < dist[v]) {\n                dist[v] = dist[u] + w;\n                pq.push({dist[v], v});\n            }\n        }\n    }\n    return dist;\n}",
        "recognitionPatterns": [
            "Minimum cost or time to reach target in state graph.",
            "Transforming edge weights into potentials to eliminate negative costs.",
            "Shortest path DAG formulation to count number of shortest paths.",
            "Dynamic graph transitions dependent on modulo or resource state (e.g., fuel $\\le K$)."
        ],
        "commonBugs": [
            "Omitting the stale state check `if (d > dist[u]) continue;` leading to $\\mathcal{O}(E \\log E)$ performance regression.",
            "Integer overflow: using 32-bit `int` for accumulated distances instead of 64-bit `long long`.",
            "Using SPFA on dense or crafted anti-SPFA contest test cases leading to worst-case $\\mathcal{O}(V \\cdot 2^V)$.",
            "Failing to detect unreachable vertices ($dist[v] = \\infty$)."
        ]
    },
    "08-part-b-08-b-mst-euler-functional-md-08-b-mst-euler-functional-md": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1600–2300\n- Prerequisites: DSU, Euler tour, in-degree/out-degree graph analysis",
        "coreIntuition": "Spanning trees minimize total edge weight while preserving connectivity. Functional graphs (where every vertex has out-degree 1) decompose uniquely into directed cycles with trees rooted on cycle vertices. Eulerian circuits require all vertices in a connected component to have equal in-degree and out-degree.",
        "derivation": "Kruskal's algorithm relies on the Cut Property: for any partition $(S, V \\setminus S)$, the minimum weight edge crossing the cut belongs to an MST. Euler's theorem states that a directed connected graph has an Eulerian cycle iff $\\text{in-deg}(u) = \\text{out-deg}(u)$ for all $u$.",
        "templateCpp": "// Kruskal MST with DSU and Hierholzer Eulerian Trail\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct DSU {\n    vector<int> p;\n    DSU(int n) : p(n + 1) { iota(p.begin(), p.end(), 0); }\n    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }\n    bool unite(int a, int b) {\n        a = find(a); b = find(b);\n        if (a == b) return false;\n        p[a] = b; return true;\n    }\n};\n\nlong long kruskal(int n, vector<tuple<long long, int, int>>& edges) {\n    sort(edges.begin(), edges.end());\n    DSU dsu(n); long long total_weight = 0; int cnt = 0;\n    for (auto& [w, u, v] : edges) {\n        if (dsu.unite(u, v)) { total_weight += w; cnt++; }\n    }\n    return cnt == n - 1 ? total_weight : -1;\n}",
        "recognitionPatterns": [
            "Connecting all components with minimum total cable, road, or edge cost.",
            "Each element transitions deterministically to exactly one other element ($x \\to f(x)$).",
            "Traversing every edge of a graph exactly once.",
            "Bottleneck edge minimization on paths across a network."
        ],
        "commonBugs": [
            "Graph is disconnected: MST contains $< N - 1$ edges, but the algorithm reports partial weight without checking component count.",
            "Eulerian path start vertex not initialized to the unique vertex with $\\text{out-deg} - \\text{in-deg} = 1$.",
            "Recursion stack overflow in Hierholzer's algorithm on large graphs ($E > 10^5$); use an iterative stack.",
            "Modifying edge adjacency list while iterating without tracking used edge IDs in undirected multigraphs."
        ]
    },
    "09-what-to-drill-this-week": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1700–2500\n- Prerequisites: Max Flow, Min-Cut, Bipartite Matching, Project Selection",
        "coreIntuition": "Flow networks solve resource allocation, constraint satisfiability, and bipartite assignment. The central contest paradigm is the **Max-Flow Min-Cut Theorem**: finding maximum flow from source to sink simultaneously identifies the minimum capacity edge set whose removal disconnects source from sink.",
        "derivation": "Dinic's algorithm constructs a layered level graph via BFS and finds blocking flows via DFS with current-arc optimization. It runs in $\\mathcal{O}(V^2 E)$ generally and strictly in $\\mathcal{O}(E \\sqrt{V})$ on unit capacity networks.",
        "templateCpp": "// Dinic Blocking Flow Algorithm with Current-Arc Pruning\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\nstruct Dinic {\n    struct Edge { int to; ll cap, flow; int rev; };\n    int n, s, t;\n    vector<vector<Edge>> adj;\n    vector<int> level, ptr;\n    Dinic(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1), level(n_ + 1), ptr(n_ + 1) {}\n    void add_edge(int from, int to, ll cap) {\n        adj[from].push_back({to, cap, 0, (int)adj[to].size()});\n        adj[to].push_back({from, 0, 0, (int)adj[from].size() - 1});\n    }\n    bool bfs() {\n        fill(level.begin(), level.end(), -1);\n        level[s] = 0; queue<int> q; q.push(s);\n        while (!q.empty()) {\n            int v = q.front(); q.pop();\n            for (auto& e : adj[v]) {\n                if (e.cap - e.flow > 0 && level[e.to] == -1) {\n                    level[e.to] = level[v] + 1; q.push(e.to);\n                }\n            }\n        }\n        return level[t] != -1;\n    }\n    ll dfs(int v, ll pushed) {\n        if (pushed == 0 || v == t) return pushed;\n        for (int& cid = ptr[v]; cid < (int)adj[v].size(); ++cid) {\n            auto& e = adj[v][cid];\n            if (level[v] + 1 != level[e.to] || e.cap - e.flow == 0) continue;\n            ll tr = dfs(e.to, min(pushed, e.cap - e.flow));\n            if (tr == 0) continue;\n            e.flow += tr; adj[e.to][e.rev].flow -= tr;\n            return tr;\n        }\n        return 0;\n    }\n    ll max_flow() {\n        ll flow = 0;\n        while (bfs()) {\n            fill(ptr.begin(), ptr.end(), 0);\n            while (ll pushed = dfs(s, INF)) flow += pushed;\n        }\n        return flow;\n    }\n};",
        "recognitionPatterns": [
            "Project Selection: picking items with positive profits and prerequisite costs.",
            "Maximum Bipartite Matching: assigning students to mentors, tasks to processors.",
            "Minimum Path Cover in DAGs: decomposing tasks into disjoint execution paths.",
            "Grid cell coloring / chessboard adjacency reductions (bipartite cuts)."
        ],
        "commonBugs": [
            "Forgetting to add backward edge with 0 initial capacity.",
            "Omitting current-arc pointers `ptr[v]` in Dinic's DFS, degrading $\\mathcal{O}(V^2 E)$ to $\\mathcal{O}(V E^2)$.",
            "Integer overflow when adding large capacities: use `long long` for all flow variables.",
            "Incorrect Min-Cut vertex reconstruction: cut consists of edges $(u, v)$ where `level[u] != -1` and `level[v] == -1`."
        ]
    },
    "09-high-roi-master-first": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1700–2200\n- Prerequisites: Dinic Max-Flow, Bipartite Matching",
        "coreIntuition": "In rated competitive programming, over 80% of flow problems do not require esoteric minimum cost flows or Gomory-Hu trees; they reduce cleanly to either **Unit Network Matching** or **Project Selection Min-Cut**. Master these two archetypes first.",
        "derivation": "Project Selection: positive reward nodes connect to source with capacity $P_i$; negative cost nodes connect to sink with capacity $C_i$; dependency $u \\to v$ has infinite capacity $\\infty$. Maximum profit equals $\\sum P_i - \\text{MinCut}$.",
        "templateCpp": "// Project Selection / Closure Reduction Scaffold\n#include <bits/stdc++.h>\nusing namespace std;\n// Uses Dinic with Source = 0, Sink = N + 1\n// For profit item i: dinic.add_edge(0, i, profit)\n// For cost item j:   dinic.add_edge(j, sink, cost)\n// Dependency i -> j: dinic.add_edge(i, j, 1e18)",
        "recognitionPatterns": [
            "Maximizing revenue minus penalties subject to prerequisite implications.",
            "Independent Set on bipartite graphs (Dual of Minimum Vertex Cover).",
            "Grid problems where adjacent cells cannot both be chosen."
        ],
        "commonBugs": [
            "Direction of prerequisite edge reversed: prerequisite $A \\implies B$ must be directed $A \\to B$ with $\\infty$ capacity.",
            "Adding negative profits directly into flow graph instead of offsetting by total potential profit."
        ]
    },
    "09-situational-learn-when-patterns-appear": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Occasional\n- Typical CF/ICPC rating range: 2100–2600\n- Prerequisites: MCMF, Successive Shortest Paths",
        "coreIntuition": "Situational flow problems involve edge costs alongside capacities (Minimum Cost Maximum Flow), circulation with node demands, and vertex capacities. When $N \\le 400$, MCMF with SPFA or Dijkstra potentials computes minimum cost assignments.",
        "derivation": "Reduced costs using Johnson potentials $\\pi(u)$: $w'(u, v) = w(u, v) + \\pi(u) - \\pi(v) \\ge 0$ allows using Dijkstra instead of SPFA for augmenting path search.",
        "templateCpp": "// MCMF with SPFA Augmenting Paths\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\nstruct MCMF {\n    struct Edge { int to; ll cap, flow, cost; int rev; };\n    int n, s, t;\n    vector<vector<Edge>> adj;\n    MCMF(int n_, int s_, int t_) : n(n_), s(s_), t(t_), adj(n_ + 1) {}\n    void add_edge(int from, int to, ll cap, ll cost) {\n        adj[from].push_back({to, cap, 0, cost, (int)adj[to].size()});\n        adj[to].push_back({from, 0, 0, -cost, (int)adj[from].size() - 1});\n    }\n};",
        "recognitionPatterns": [
            "K-disjoint paths with minimum total cost.",
            "Worker-to-job matching where assignment has a variable matrix cost.",
            "Graph with upper and lower flow bounds per edge."
        ],
        "commonBugs": [
            "Negative cycles in residual graph causing infinite augmentations.",
            "Backward edge cost must be strictly $-cost$ of forward edge."
        ]
    },
    "09-rarely-worth-early-niche": {
        "whyItMatters": "- Contest ROI: C-tier\n- Frequency: Rare\n- Typical CF/ICPC rating range: 2400–3000\n- Prerequisites: Push-Relabel, Gomory-Hu Tree, Stoer-Wagner",
        "coreIntuition": "Advanced flow constructs such as Gomory-Hu Cut Trees ($N-1$ min-cuts representing all pairs in a tree) and Stoer-Wagner global min-cut appear rarely in standard Div2/Div1 contests. Spend practice time on Dinic and reductions before mastering these niche topics.",
        "derivation": "Gomory-Hu Tree computes all $\\binom{N}{2}$ pairwise minimum cuts using exactly $N-1$ max-flow computations via recursive partitioning.",
        "templateCpp": "// Reference note: Gomory-Hu tree computes all-pairs min-cut in N-1 max-flow executions.\n// Use Dinic subroutines on contracted component sets.",
        "recognitionPatterns": [
            "All-pairs min-cut queries on an undirected network.",
            "Global minimum cut without specified source and sink in undirected graph."
        ],
        "commonBugs": [
            "Applying Gomory-Hu tree on directed graphs (valid only on undirected networks)."
        ]
    },
    "10-high-roi-learn-early-in-this-section": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: 1D/2D DP recurrences, Monotonicity",
        "coreIntuition": "DP optimizations reduce quadratic $\\mathcal{O}(N^2)$ state transitions to $\\mathcal{O}(N \\log N)$ or $\\mathcal{O}(N)$. Prioritize learning: (1) Monotone Deque for sliding window transitions, (2) Convex Hull Trick (CHT) for linear transitions $dp[i] = \\min_j (m_j x_i + c_j)$, and (3) Divide & Conquer DP for Monge cost matrices.",
        "derivation": "When the optimal decision index satisfies $opt(i, j) \\le opt(i, j+1)$, the decision space is monotone, allowing D&C recursion over index midpoints.",
        "templateCpp": "// Monotone Deque DP Optimization Template\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct MonotoneDeque {\n    deque<pair<long long, int>> dq; // {val, index}\n    void push(long long val, int idx) {\n        while (!dq.empty() && dq.back().first >= val) dq.pop_back();\n        dq.push_back({val, idx});\n    }\n    void pop_expired(int min_idx) {\n        while (!dq.empty() && dq.front().second < min_idx) dq.pop_front();\n    }\n    long long query() { return dq.front().first; }\n};",
        "recognitionPatterns": [
            "Transitions of the form $dp[i] = \\min_{i - K \\le j < i} (dp[j] + \\text{cost})$.",
            "Cost function has negative or positive linear slope terms: $A[i] \\cdot B[j]$.",
            "Optimal transition point moves monotonically rightward as $i$ increases."
        ],
        "commonBugs": [
            "Slopes not strictly monotonic: using standard deque CHT instead of Li Chao Tree.",
            "Off-by-one in window expiration bound `i - K`."
        ]
    },
    "10-situational-clear-recognition-pattern-first": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Occasional\n- Typical CF/ICPC rating range: 2000–2600\n- Prerequisites: CHT, Knuth Optimization, Quadrangle Inequality",
        "coreIntuition": "Knuth Optimization optimizes 2D interval DP $dp[i][j] = \\min_{i \\le k < j} (dp[i][k] + dp[k+1][j]) + C[i][j]$ from $\\mathcal{O}(N^3)$ to $\\mathcal{O}(N^2)$ whenever $opt[i][j-1] \\le opt[i][j] \\le opt[i+1][j]$.",
        "derivation": "Quadrangle inequality: $C[a][c] + C[b][d] \\le C[a][d] + C[b][c]$ for $a \\le b \\le c \\le d$. This ensures decision monotonicity.",
        "templateCpp": "// Knuth 2D Interval DP Template in O(N^2)\n#include <bits/stdc++.h>\nusing namespace std;\n\nconst long long INF = 1e18;\nlong long dp[505][505];\nint opt[505][505];",
        "recognitionPatterns": [
            "Interval splitting DP with Monge cost property (e.g., optimal binary search tree, polygon triangulation).",
            "Subarray partitioning with exact $K$ parts where cost satisfies convex quadrangle inequality."
        ],
        "commonBugs": [
            "Loop order incorrect: must iterate by increasing interval length $len = 2 \\dots N$.",
            "Assuming Knuth applies when cost matrix violates quadrangle inequality."
        ]
    },
    "10-rarely-worth-early-niche-early": {
        "whyItMatters": "- Contest ROI: C-tier\n- Frequency: Rare\n- Typical CF/ICPC rating range: 2500–3000\n- Prerequisites: SMAWK algorithm, 1D/1D D-search",
        "coreIntuition": "SMAWK computes row minima of an implicitly defined totally monotone matrix in $\\mathcal{O}(N)$ without evaluating all entries. Rarely required outside top-level onsite contests (ICPC World Finals, Petrozavodsk).",
        "derivation": "Total monotonicity ensures that if $M_{i, j_1} \\le M_{i, j_2}$, then $M_{i', j_1} \\le M_{i', j_2}$ for all $i' > i$.",
        "templateCpp": "// SMAWK framework reference for totally monotone matrices",
        "recognitionPatterns": [
            "1D/1D DP optimization where Knuth or CHT cannot be applied due to non-linear cost.",
            "Subquadratic evaluation of totally monotone matrix rows."
        ],
        "commonBugs": [
            "Matrix is monotone but not totally monotone."
        ]
    },
    "10-suggested-learning-order-exact-subtopic-order": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1600–2600\n- Prerequisites: DP foundations, Convexity",
        "coreIntuition": "Follow this battle-tested mastery order: 1. Monotone Deque / Sliding Window DP $\\to$ 2. Convex Hull Trick (monotone slopes) $\\to$ 3. Dynamic CHT / Li Chao Tree (arbitrary lines) $\\to$ 4. Divide & Conquer DP $\\to$ 5. Knuth 2D Interval DP $\\to$ 6. WQS Binary Search / Aliens Trick.",
        "derivation": "Each optimization step builds upon the previous invariant: from 1D monotonicity to linear geometric envelopes, then to 2D decision intervals, and finally to Lagrangian convex relaxation.",
        "templateCpp": "// Master DP Optimization Reference Order:\n// Step 1: Deque\n// Step 2: CHT\n// Step 3: Li Chao\n// Step 4: D&C\n// Step 5: Knuth\n// Step 6: Aliens Trick",
        "recognitionPatterns": [
            "Structured learning roadmap for Div2C through Div1D problems."
        ],
        "commonBugs": [
            "Attempting Aliens trick before mastering standard CHT and binary search on gradients."
        ]
    },
    "10-what-to-drill-this-week": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1800–2500\n- Prerequisites: DP optimization archetypes",
        "coreIntuition": "Focus drills on recognizing which DP speedup applies from the mathematical form of the transition equation. Equation containing $A[i] \\cdot B[j] \\implies$ CHT; equation with $j \\in [i-k, i] \\implies$ Deque; 2D interval with Monge cost $\\implies$ Knuth; exact $K$ parts with convex cost $\\implies$ Aliens Trick.",
        "derivation": "Analyzing the transition: $dp[i] = \\min_j (f(j) + g(i) + h(j) \\cdot k(i))$. When $h(j) \\cdot k(i)$ is a product of separate functions of $j$ and $i$, it represents a line $y = m x + c$ evaluated at $x = k(i)$.",
        "templateCpp": "// Contest DP Drill Check:\n// 1. Write naive O(N^2) or O(N^3) DP.\n// 2. Identify the bottleneck transition.\n// 3. Match against the 6 speedup archetypes.",
        "recognitionPatterns": [
            "Quadratic DP passes on sample tests but TLEs on $N = 10^5$."
        ],
        "commonBugs": [
            "Prematurely optimizing before verifying the base recurrence correctness."
        ]
    },
    "11-quick-reference-algorithm-problem-class": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1400–2400\n- Prerequisites: String matching basics",
        "coreIntuition": "String algorithm matching matrix: Single pattern matching $\\to$ KMP / Z-algorithm $\\mathcal{O}(N + M)$; Multiple pattern matching $\\to$ Aho-Corasick Automaton; Palindrome enumeration $\\to$ Manacher $\\mathcal{O}(N)$; Lexicographical queries / LCP $\\to$ Suffix Array + LCP; All substring transitions $\\to$ Suffix Automaton (SAM) $\\mathcal{O}(N)$.",
        "derivation": "KMP computes prefix failure links $\\pi[i] = \\max \\{ k < i : s[0..k-1] = s[i-k..i-1] \\}$. Suffix Automaton constructs the minimal DFA recognizing all substrings with at most $2N-1$ states and $3N-4$ transitions.",
        "templateCpp": "// String Quick Reference Matrix Implementation Check\n#include <bits/stdc++.h>\nusing namespace std;\n\nvector<int> prefix_function(const string& s) {\n    int n = s.size();\n    vector<int> pi(n);\n    for (int i = 1; i < n; ++i) {\n        int j = pi[i - 1];\n        while (j > 0 && s[i] != s[j]) j = pi[j - 1];\n        if (s[i] == s[j]) j++;\n        pi[i] = j;\n    }\n    return pi;\n}",
        "recognitionPatterns": [
            "Pattern search, periodic string prefixes, substring count, longest common substring."
        ],
        "commonBugs": [
            "Off-by-one in string length comparisons and prefix function transitions."
        ]
    },
    "11-high-roi-drill-first": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1400–2000\n- Prerequisites: Arrays, modulo arithmetic",
        "coreIntuition": "Start with Polynomial Rolling Hashing with double 64-bit moduli ($10^9+7$ and $10^9+9$) and base $B = 313$ or random odd integer, followed by KMP and Z-algorithm. These solve 70% of contest string tasks.",
        "derivation": "Hash invariant: $H(s[0..i]) = (H(s[0..i-1]) \\cdot B + s[i]) \\pmod M$. Substring hash in $\\mathcal{O}(1)$: $H(s[l..r]) = (H[r+1] - H[l] \\cdot B^{r - l + 1}) \\pmod M$.",
        "templateCpp": "// Double Polynomial Rolling Hash Template\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct StringHash {\n    int n;\n    ll B1 = 313, M1 = 1e9 + 7;\n    ll B2 = 317, M2 = 1e9 + 9;\n    vector<ll> h1, h2, p1, p2;\n    StringHash(const string& s) : n(s.size()), h1(n + 1), h2(n + 1), p1(n + 1, 1), p2(n + 1, 1) {\n        for (int i = 0; i < n; ++i) {\n            h1[i + 1] = (h1[i] * B1 + s[i]) % M1;\n            h2[i + 1] = (h2[i] * B2 + s[i]) % M2;\n            p1[i + 1] = (p1[i] * B1) % M1;\n            p2[i + 1] = (p2[i] * B2) % M2;\n        }\n    }\n    pair<ll, ll> get_hash(int l, int r) {\n        ll a = (h1[r + 1] - h1[l] * p1[r - l + 1]) % M1; if (a < 0) a += M1;\n        ll b = (h2[r + 1] - h2[l] * p2[r - l + 1]) % M2; if (b < 0) b += M2;\n        return {a, b};\n    }\n};",
        "recognitionPatterns": [
            "Checking if two substrings are equal in $O(1)$.",
            "Longest common prefix via binary search on hash values."
        ],
        "commonBugs": [
            "Single modulo hash hacked by anti-hash test cases; always use double hash with random base."
        ]
    },
    "11-situational-medium-b-tier": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1800–2400\n- Prerequisites: KMP, Trie, BFS",
        "coreIntuition": "Aho-Corasick builds a Trie over a dictionary of patterns and connects failure links via BFS, mimicking KMP on a tree. Manacher finds all maximal palindromic radii centered at each character/interstice in linear $\\mathcal{O}(N)$ time.",
        "derivation": "Failure link of node $u$ points to the longest proper suffix of $u$ present in the Trie. Manacher reuses the palindromic symmetry around the current rightmost boundary $R$.",
        "templateCpp": "// Aho-Corasick Multi-Pattern Automaton\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct AhoCorasick {\n    struct Node { int next[26] = {0}; int link = 0; int cnt = 0; };\n    vector<Node> t = {Node()};\n    void insert(const string& s) {\n        int v = 0;\n        for (char c : s) {\n            int idx = c - 'a';\n            if (!t[v].next[idx]) { t[v].next[idx] = t.size(); t.emplace_back(); }\n            v = t[v].next[idx];\n        }\n        t[v].cnt++;\n    }\n    void build() {\n        queue<int> q;\n        for (int c = 0; c < 26; ++c) if (t[0].next[c]) q.push(t[0].next[c]);\n        while (!q.empty()) {\n            int v = q.front(); q.pop();\n            for (int c = 0; c < 26; ++c) {\n                int u = t[v].next[c];\n                if (u) { t[u].link = t[t[v].link].next[c]; q.push(u); }\n                else { t[v].next[c] = t[t[v].link].next[c]; }\n            }\n        }\n    }\n};",
        "recognitionPatterns": [
            "Given text $T$ and $K$ patterns, count occurrences of each pattern in $T$.",
            "Longest palindromic substring or palindromic prefix factorization."
        ],
        "commonBugs": [
            "Forgetting to propagate pattern counts along failure links in Aho-Corasick."
        ]
    },
    "11-rarely-worth-early-niche-c-tier": {
        "whyItMatters": "- Contest ROI: C-tier\n- Frequency: Rare\n- Typical CF/ICPC rating range: 2400–3000\n- Prerequisites: Suffix Automaton, Palindromic Tree",
        "coreIntuition": "Eertree (Palindromic Automaton) and Lyndon Factorization (Duval's algorithm) are specialized string constructs. Master Suffix Automaton and Aho-Corasick before investing time here.",
        "derivation": "Eertree maintains directed transitions on characters between palindromic states with two roots (lengths $-1$ and $0$).",
        "templateCpp": "// Palindromic Tree (Eertree) outline",
        "recognitionPatterns": [
            "Number of distinct palindromic substrings in each prefix dynamically."
        ],
        "commonBugs": [
            "Incorrect initialization of length -1 imaginary root."
        ]
    },
    "12-high-roi-learn-now": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–2100\n- Prerequisites: Modular arithmetic, Euclidean GCD",
        "coreIntuition": "High-yield Number Theory fundamentals: (1) Linear Sieve in $\\mathcal{O}(N)$ computing Smallest Prime Factor (SPF), (2) Extended Euclidean Algorithm for modular inverses, and (3) Binary Exponentiation for fast powers and Fermat's Little Theorem.",
        "derivation": "Linear Sieve invariant: each composite number $x$ is visited and marked exactly once by its smallest prime factor $p = \\text{SPF}[x]$. Extended GCD: $a x + b y = \\gcd(a, b)$.",
        "templateCpp": "// Linear Sieve & Extended GCD Template\n#include <bits/stdc++.h>\nusing namespace std;\n\nconst int MAXN = 1e7 + 5;\nint spf[MAXN];\nvector<int> primes;\n\nvoid linear_sieve(int n) {\n    for (int i = 2; i <= n; ++i) {\n        if (!spf[i]) { spf[i] = i; primes.push_back(i); }\n        for (int p : primes) {\n            if (p > spf[i] || 1LL * i * p > n) break;\n            spf[i * p] = p;\n        }\n    }\n}\n\nlong long ext_gcd(long long a, long long b, long long& x, long long& y) {\n    if (b == 0) { x = 1; y = 0; return a; }\n    long long x1, y1;\n    long long d = ext_gcd(b, a % b, x1, y1);\n    x = y1; y = x1 - y1 * (a / b);\n    return d;\n}",
        "recognitionPatterns": [
            "Factoring integers up to $10^7$ in $\\mathcal{O}(\\log X)$ queries.",
            "Solving linear congruence $a x \\equiv b \\pmod m$.",
            "Modular combinations $\\binom{N}{K} \\pmod P$ using precomputed factorials."
        ],
        "commonBugs": [
            "Negative modulo result: `(a % m + m) % m` required in C++.",
            "Using `int` for intermediate products in modular multiplication."
        ]
    },
    "12-situational-clear-recognition-deploy": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1800–2400\n- Prerequisites: Multiplicative functions, Dirichlet convolution",
        "coreIntuition": "Möbius Inversion converts GCD conditions into divisor sums: $[\\gcd(i, j) = 1] = \\sum_{d | \\gcd(i, j)} \\mu(d)$. This simplifies double sums $\\sum_{i=1}^N \\sum_{j=1}^M f(\\gcd(i, j))$ into single harmonic sweeps in $\\mathcal{O}(N)$ or $\\mathcal{O}(\\sqrt{N})$.",
        "derivation": "Dirichlet convolution $(f * g)(n) = \\sum_{d | n} f(d) g(n/d)$. Inversion formula: $g = f * 1 \\iff f = g * \\mu$.",
        "templateCpp": "// Mobius Inversion & Square-Root Block Sums\n#include <bits/stdc++.h>\nusing namespace std;\nconst int MAXN = 1e6 + 5;\nint mu[MAXN];\n\nvoid compute_mu(int n) {\n    vector<int> primes;\n    vector<bool> is_comp(n + 1, false);\n    mu[1] = 1;\n    for (int i = 2; i <= n; ++i) {\n        if (!is_comp[i]) { primes.push_back(i); mu[i] = -1; }\n        for (int p : primes) {\n            if (i * p > n) break;\n            is_comp[i * p] = true;\n            if (i % p == 0) { mu[i * p] = 0; break; }\n            else { mu[i * p] = -mu[i]; }\n        }\n    }\n}",
        "recognitionPatterns": [
            "Counting coprime pairs in range $[1, N] \\times [1, M]$.",
            "Sum involving $\\gcd(i, j)$ or $\\text{lcm}(i, j)$ over multiple query bounds."
        ],
        "commonBugs": [
            "Forgetting to stop prime loop when `i % p == 0`, violating linear sieve complexity."
        ]
    },
    "12-rarely-worth-early-niche": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Occasional\n- Typical CF/ICPC rating range: 2200–2800\n- Prerequisites: Miller-Rabin, Pollard's Rho, Baby-Step Giant-Step",
        "coreIntuition": "Large integer factorization ($N \\le 10^{18}$) requires Miller-Rabin primality testing and Pollard's Rho algorithm in $\\mathcal{O}(N^{1/4})$. Discrete logarithm $a^x \\equiv b \\pmod m$ requires Baby-Step Giant-Step (BSGS) in $\\mathcal{O}(\\sqrt{m})$.",
        "derivation": "Pollard's Rho detects cycles in sequence $x_{i+1} = (x_i^2 + c) \\pmod N$ using Floyd's cycle-finding algorithm and $\\gcd(|x_i - x_j|, N)$.",
        "templateCpp": "// Pollard Rho & Miller Rabin 64-bit Primality Test\n#include <bits/stdc++.h>\nusing namespace std;\nusing u64 = unsigned long long;\nusing u128 = __uint128_t;\n\nu64 power(u64 base, u64 exp, u64 mod) {\n    u64 res = 1; base %= mod;\n    while (exp > 0) {\n        if (exp & 1) res = (u128)res * base % mod;\n        base = (u128)base * base % mod;\n        exp >>= 1;\n    }\n    return res;\n}",
        "recognitionPatterns": [
            "Factoring integers up to $10^{18}$ in contest problems.",
            "Finding smallest $x$ such that $A^x \\equiv B \\pmod P$."
        ],
        "commonBugs": [
            "Overflow in 64-bit multiplication: must use `__int128`."
        ]
    },
    "12-part-a-12-a-number-theory-binpow-euler-md-12-a-number-theory-binpow-euler-md": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–2000\n- Prerequisites: Modular arithmetic, prime factorization",
        "coreIntuition": "Number Theory Architecture Part A: Binary exponentiation, Fermat's Little Theorem, Euler's Totient Function $\\phi(N)$, and linear Diophantine equations via Extended Euclidean algorithm.",
        "derivation": "Euler's theorem: $a^{\\phi(m)} \\equiv 1 \\pmod m$ whenever $\\gcd(a, m) = 1$. Power reduction: $a^b \\equiv a^{b \\bmod \\phi(m) + \\phi(m)} \\pmod m$ for $b \\ge \\phi(m)$.",
        "templateCpp": "// Euler Totient Function phi(N)\n#include <bits/stdc++.h>\nusing namespace std;\n\nlong long phi(long long n) {\n    long long result = n;\n    for (long long p = 2; p * p <= n; ++p) {\n        if (n % p == 0) {\n            while (n % p == 0) n /= p;\n            result -= result / p;\n        }\n    }\n    if (n > 1) result -= result / n;\n    return result;\n}",
        "recognitionPatterns": [
            "Computing large power towers $a^{b^c} \\pmod m$.",
            "Inverting non-prime modulo arithmetic."
        ],
        "commonBugs": [
            "Applying Fermat's Little Theorem $a^{P-2}$ when modulo is composite; must use Euler Totient or Extended GCD."
        ]
    },
    "12-what-to-drill-this-week": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1400–2200\n- Prerequisites: Core Number Theory formulas",
        "coreIntuition": "Drill speed and precision on: (1) Linear sieve with SPF, (2) Fast factorial and inverse factorial tables, (3) Chinese Remainder Theorem (CRT), and (4) Floor sum $\\sum_{i=0}^{n-1} \\lfloor \\frac{a i + b}{m} \\rfloor$ in $\\mathcal{O}(\\log m)$.",
        "derivation": "Floor sum can be evaluated like the Euclidean algorithm by reflecting axes when $a \\ge m$ or swapping variables.",
        "templateCpp": "// Floor sum algorithm in O(log m)\n#include <bits/stdc++.h>\nusing namespace std;\n\nlong long floor_sum(long long n, long long m, long long a, long long b) {\n    long long ans = 0;\n    if (a >= m) { ans += (n - 1) * n / 2 * (a / m); a %= m; }\n    if (b >= m) { ans += n * (b / m); b %= m; }\n    long long y_max = (a * n + b) / m;\n    long long x_max = y_max * m - b;\n    if (y_max == 0) return ans;\n    ans += (n - (x_max + a - 1) / a) * y_max;\n    ans += floor_sum(y_max, a, m, (a - x_max % a) % a);\n    return ans;\n}",
        "recognitionPatterns": [
            "Arithmetic progressions under floor functions.",
            "Lattice point counting under a line segment."
        ],
        "commonBugs": [
            "Integer overflow in `(n - 1) * n / 2 * (a / m)`."
        ]
    },
    "13-part-a-13-a-bit-manipulation-transforms-md-13-a-bit-manipulation-transforms-md": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1500–2300\n- Prerequisites: Bitwise operators, submask iteration",
        "coreIntuition": "Bitmask manipulations provide $\\mathcal{O}(1)$ parallel operations across word sizes. Master: `__builtin_popcount`, `__builtin_clz`, submask iteration in $\\mathcal{O}(3^N)$, and Sum Over Subsets (SOS DP) in $\\mathcal{O}(N \\cdot 2^N)$.",
        "derivation": "Submask iteration loop: `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)`. Total pairs across all masks is $\\sum_{k=0}^N \\binom{N}{k} 2^k = 3^N$.",
        "templateCpp": "// SOS DP (Sum Over Subsets) in O(N * 2^N)\n#include <bits/stdc++.h>\nusing namespace std;\n\nvoid sos_dp(int n, vector<long long>& f) {\n    for (int i = 0; i < n; ++i) {\n        for (int mask = 0; mask < (1 << n); ++mask) {\n            if (mask & (1 << i)) f[mask] += f[mask ^ (1 << i)];\n        }\n    }\n}",
        "recognitionPatterns": [
            "Evaluating subset sums or superset sums for all masks of size $N \\le 22$.",
            "Iterating over all submasks of all masks."
        ],
        "commonBugs": [
            "Submask loop termination condition: `sub > 0` misses empty mask `0`; process `0` separately if needed."
        ]
    },
    "13-part-b-13-b-advanced-combinatorics-md-13-b-advanced-combinatorics-md": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: Permutations, combinations, inclusion-exclusion",
        "coreIntuition": "Combinatorial counting models arrangements and partitions: Stars and Bars for non-negative solutions to $\\sum x_i = S$, Principle of Inclusion-Exclusion (PIE) for union sizes, Derangements, and Stirling numbers of the first and second kind.",
        "derivation": "Stars and Bars: placing $K-1$ dividers among $N$ stars gives $\\binom{N + K - 1}{K - 1}$. Derangements recurrence: $D_n = (n - 1)(D_{n-1} + D_{n-2})$.",
        "templateCpp": "// Combinatorics precomputation: Factorials, Inverses, and nCr\n#include <bits/stdc++.h>\nusing namespace std;\nconst int MAX = 1e6 + 5, MOD = 1e9 + 7;\nlong long fact[MAX], inv_fact[MAX];\n\nlong long nCr(int n, int r) {\n    if (r < 0 || r > n) return 0;\n    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD;\n}",
        "recognitionPatterns": [
            "Counting ways to distribute identical items into distinct bins.",
            "Counting permutations with no fixed points."
        ],
        "commonBugs": [
            "Negative values in modulo addition inside PIE parity loop."
        ]
    },
    "13-high-roi-drill-first": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1500–2100\n- Prerequisites: Precomputed factorials, SOS DP",
        "coreIntuition": "Drill the standard combinatorial toolkit: $\\binom{N}{K} \\pmod P$, Catalan numbers $C_n = \\frac{1}{n+1} \\binom{2n}{n}$ (valid bracket sequences, non-intersecting chords, binary tree topologies), and SOS DP submask accumulations.",
        "derivation": "Catalan recurrence: $C_{n+1} = \\sum_{i=0}^n C_i C_{n-i} = \\frac{2(2n+1)}{n+2} C_n$.",
        "templateCpp": "// Catalan Numbers computation\n#include <bits/stdc++.h>\nusing namespace std;\n// Catalan C_n = nCr(2n, n) / (n + 1)",
        "recognitionPatterns": [
            "Valid Dyck paths that do not cross the diagonal.",
            "Number of distinct full binary trees with $n+1$ leaves."
        ],
        "commonBugs": [
            "Dividing by $n+1$ without computing modular inverse under composite modulo."
        ]
    },
    "13-situational-learn-after-high-roi": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Occasional\n- Typical CF/ICPC rating range: 2000–2600\n- Prerequisites: FWHT, XOR / AND / OR transforms",
        "coreIntuition": "Fast Walsh-Hadamard Transform (FWHT) performs bitwise convolutions $C[k] = \\sum_{i \\oplus j = k} A[i] B[j]$ in $\\mathcal{O}(N \\cdot 2^N)$ for $\\oplus \\in \\{\\text{XOR}, \\text{AND}, \\text{OR}\\}$.",
        "derivation": "Hadamard matrix $H_2 = \\begin{pmatrix} 1 & 1 \\\\ 1 & -1 \\end{pmatrix}$. Applying tensor product $H_{2^N} = H_2^{\\otimes N}$ diagonalizes XOR convolution.",
        "templateCpp": "// Fast Walsh-Hadamard Transform (FWHT) for XOR Convolution\n#include <bits/stdc++.h>\nusing namespace std;\n\nvoid fwht_xor(vector<long long>& a, bool invert) {\n    int n = a.size();\n    for (int len = 1; 2 * len <= n; len <<= 1) {\n        for (int i = 0; i < n; i += 2 * len) {\n            for (int j = 0; j < len; ++j) {\n                long long u = a[i + j], v = a[i + len + j];\n                a[i + j] = u + v;\n                a[i + len + j] = u - v;\n            }\n        }\n    }\n    if (invert) for (auto& x : a) x /= n;\n}",
        "recognitionPatterns": [
            "Computing all pairs $(i, j)$ with $A[i] \\oplus A[j] = X$ across an array.",
            "Subset convolution combining size and mask state."
        ],
        "commonBugs": [
            "Dividing by $N$ without modular inverse when FWHT is computed modulo $P$."
        ]
    },
    "13-rarely-worth-early-niche": {
        "whyItMatters": "- Contest ROI: C-tier\n- Frequency: Rare\n- Typical CF/ICPC rating range: 2400–3000\n- Prerequisites: Burnside's Lemma, Polya Enumeration Theorem",
        "coreIntuition": "Burnside's Lemma and Polya Enumeration count non-isomorphic colorings and structures under group actions (rotations, reflections, automorphisms): $|X/G| = \\frac{1}{|G|} \\sum_{g \\in G} |X^g|$.",
        "derivation": "Each symmetry group element $g \\in G$ has a cycle decomposition; coloring assignments invariant under $g$ assign uniform color to all elements in each cycle.",
        "templateCpp": "// Burnside's Lemma for Necklaces with K colors and N beads\n#include <bits/stdc++.h>\nusing namespace std;\n// |X/G| = (1/N) * sum_{i=0}^{N-1} K^gcd(i, N)",
        "recognitionPatterns": [
            "Counting unique bracelets, cubes, or graphs under rotational equivalence."
        ],
        "commonBugs": [
            "Missing reflection elements when symmetries include dihedral group $D_N$ rather than cyclic group $C_N$."
        ]
    },
    "13-what-to-drill-this-week": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1600–2300\n- Prerequisites: Combinatorics & Bit manipulation toolkit",
        "coreIntuition": "Drill: (1) Fast combination queries, (2) Submask iteration loops, (3) SOS DP prefix table, (4) Inversion parity checks, and (5) Nim-sum game reductions.",
        "derivation": "SOS DP computes $F[\\text{mask}] = \\sum_{sub \\subseteq mask} A[sub]$ in exactly $N \\cdot 2^N$ operations.",
        "templateCpp": "// Weekly Combinatorics & Bit Drill Scaffold",
        "recognitionPatterns": [
            "Fast bit operations inside tightly nested DP loops."
        ],
        "commonBugs": [
            "Left-shift overflow: `1 << i` instead of `1LL << i` when $i \\ge 31$."
        ]
    },
    "17-high-roi-learn-early-in-this-section": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1500–2200\n- Prerequisites: 2D Point struct, 2D cross product, sorting",
        "coreIntuition": "Master Andrew's Monotone Chain algorithm for Convex Hull in $\\mathcal{O}(N \\log N)$ and 2D cross product turn tests (`cross(B-A, C-A)`). These two primitives solve the vast majority of geometric contest problems.",
        "derivation": "Cross product $(B - A) \\times (C - A) = (B_x - A_x)(C_y - A_y) - (B_y - A_y)(C_x - A_x)$. Positive $\\implies$ Counter-Clockwise (left turn); negative $\\implies$ Clockwise (right turn); zero $\\implies$ collinear.",
        "templateCpp": "// Andrew Monotone Chain Convex Hull in O(N log N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Point {\n    ll x, y;\n    bool operator<(const Point& o) const { return x < o.x || (x == o.x && y < o.y); }\n};\n\nll cross(Point o, Point a, Point b) {\n    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);\n}\n\nvector<Point> convex_hull(vector<Point>& pts) {\n    int n = pts.size(), k = 0;\n    if (n <= 2) return pts;\n    vector<Point> h(2 * n);\n    sort(pts.begin(), pts.end());\n    for (int i = 0; i < n; ++i) {\n        while (k >= 2 && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;\n        h[k++] = pts[i];\n    }\n    for (int i = n - 2, t = k + 1; i >= 0; --i) {\n        while (k >= t && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;\n        h[k++] = pts[i];\n    }\n    h.resize(k - 1);\n    return h;\n}",
        "recognitionPatterns": [
            "Enclosing a set of points with minimal perimeter or area.",
            "Sorting points radially around an origin to detect angular intervals."
        ],
        "commonBugs": [
            "Collinear points: strictly `< 0` vs `<= 0` pop condition in convex hull depending on whether collinear points on edges must be preserved.",
            "Floating point inaccuracies; always use 64-bit integer cross products when coordinates are integers."
        ]
    },
    "17-situational-learn-when-recognition-hits": {
        "whyItMatters": "- Contest ROI: B-tier\n- Frequency: Occasional\n- Typical CF/ICPC rating range: 1900–2500\n- Prerequisites: Convex Hull, Two Pointers, Half-Plane Intersection",
        "coreIntuition": "Situational Geometry: (1) Rotating Calipers for polygon diameter and minimum bounding box in $\\mathcal{O}(N)$, (2) Half-Plane Intersection in $\\mathcal{O}(N \\log N)$ using sorted polar angles, and (3) Point-in-Convex-Polygon binary search in $\\mathcal{O}(\\log N)$.",
        "derivation": "Rotating calipers advances two antipodal pointers around the convex hull based on triangle area maximization using cross products.",
        "templateCpp": "// Rotating Calipers Polygon Diameter in O(N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n// Advances pointer j around hull while cross product area increases",
        "recognitionPatterns": [
            "Maximum distance between any two points in a 2D cloud.",
            "Finding the kernel of a polygon or region satisfying a set of linear half-plane constraints."
        ],
        "commonBugs": [
            "Antipodal pointer cycle wrap-around off-by-one."
        ]
    },
    "17-rarely-worth-early-niche": {
        "whyItMatters": "- Contest ROI: C-tier\n- Frequency: Rare\n- Typical CF/ICPC rating range: 2400–3000\n- Prerequisites: Minkowski Sum, Delaunay Triangulation, 3D Convex Hull",
        "coreIntuition": "Niche geometry constructs: Minkowski Sum of convex polygons in $\\mathcal{O}(N + M)$ for collision detection and 3D Convex Hull in $\\mathcal{O}(N^2)$ or $\\mathcal{O}(N \\log N)$.",
        "derivation": "Minkowski Sum $A + B = \\{a + b : a \\in A, b \\in B\\}$ is computed by merging the edge vectors of both convex hulls sorted by polar angle.",
        "templateCpp": "// Minkowski Sum of Convex Polygons",
        "recognitionPatterns": [
            "Shortest distance between two moving convex polygons over time.",
            "Point location in Voronoi diagrams."
        ],
        "commonBugs": [
            "Cyclic ordering of edge vectors during Minkowski merge."
        ]
    },
    "18-mo-vs-segment-tree-drill-this-distinction": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1600–2200\n- Prerequisites: Mo's Algorithm, Segment Trees",
        "coreIntuition": "Decision Matrix: If queries have point updates $\\implies$ Segment Tree or Fenwick. If queries are static, offline, and the aggregate state has no clean associative merge but supports $\\mathcal{O}(1)$ insertion and deletion of single elements (e.g., number of distinct elements, frequency counts) $\\implies$ Mo's Algorithm in $\\mathcal{O}((N + Q) \\sqrt{N})$.",
        "derivation": "Mo's algorithm partitions queries into $B \\approx N / \\sqrt{Q}$ blocks by left endpoint and sorts right endpoints. Total pointer movements: $Q \\cdot B + N \\cdot (N / B) = \\mathcal{O}(N \\sqrt{Q})$.",
        "templateCpp": "// Mo Algorithm vs Segtree Decision Guide Template\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct Query {\n    int l, r, id, block;\n    bool operator<(const Query& o) const {\n        if (block != o.block) return block < o.block;\n        return (block & 1) ? r < o.r : r > o.r; // Hilbert / serpentine optimization\n    }\n};",
        "recognitionPatterns": [
            "Query asks for number of distinct elements, modes, or frequency threshold in $[L, R]$.",
            "No updates are performed during query execution.",
            "Adding or removing one element to the current range takes $\\mathcal{O}(1)$ or $\\mathcal{O}(\\log N)$."
        ],
        "commonBugs": [
            "Applying Mo's algorithm when queries require online answers.",
            "Choosing block size $B = \\sqrt{N}$ when $Q \\ll N$ or $Q \\gg N$; optimal is $B = \\max(1, N / \\sqrt{Q})$."
        ]
    },
    "22-prerequisites": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–1800\n- Prerequisites: Arrays, sorting, prefix sums",
        "coreIntuition": "Prerequisites for Sweep Line mastery: 1D Difference Arrays (`diff[L] += v, diff[R+1] -= v`), sorting events by coordinate with secondary tie-breaking, and coordinate compression of sparse coordinates into dense indices.",
        "derivation": "Prefix sum of difference array reproduces original values: $A[i] = \\sum_{j=1}^i \\text{diff}[j]$. Sorting events ensures processing occurs in temporal or spatial monotonicity.",
        "templateCpp": "// Sweep Line Prerequisites: 1D Difference Array & Coordinate Compression\n#include <bits/stdc++.h>\nusing namespace std;\n\nvector<int> compress(vector<long long>& coords) {\n    vector<long long> vals = coords;\n    sort(vals.begin(), vals.end());\n    vals.erase(unique(vals.begin(), vals.end()), vals.end());\n    vector<int> ranks(coords.size());\n    for (size_t i = 0; i < coords.size(); ++i) {\n        ranks[i] = lower_bound(vals.begin(), vals.end(), coords[i]) - vals.begin();\n    }\n    return ranks;\n}",
        "recognitionPatterns": [
            "Multiple range additions followed by point queries.",
            "Coordinates in range $[-10^9, 10^9]$ where only relative order matters."
        ],
        "commonBugs": [
            "Off-by-one at right endpoint: adding $+v$ at $L$ and $-v$ at $R$ instead of $R+1$ for inclusive range $[L, R]$.",
            "Forgetting to deduplicate with `unique` before computing ranks."
        ]
    }
}
