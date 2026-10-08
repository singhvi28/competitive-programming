import os
import json
import re
import urllib.request
import urllib.parse

ADV_DSA_DIR = "/home/singhvi28/Desktop/adv-dsa"
DATA_JSON = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"

with open(DATA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded curriculum data: {len(data['modules'])} modules, {data['metadata']['totalTopics']} topics")

# External Curated Resource Links & Problem Banks
TOPIC_RESOURCES = {
    "01": {
        "externalLinks": [
            {"title": "CP-Algorithms: Fenwick Tree (Binary Indexed Tree)", "url": "https://cp-algorithms.com/data_structures/fenwick.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Point Update Range Sum (Fenwick)", "url": "https://usaco.guide/gold/purq", "source": "USACO Guide"},
            {"title": "YouKn0wWho Academy: Fenwick Tree Mastery", "url": "https://youkn0wwho.academy/topic-list#fenwick-tree", "source": "YouKn0wWho"},
            {"title": "Codeforces Blog: Binary Lifting on Fenwick Tree", "url": "https://codeforces.com/blog/entry/61364", "source": "Codeforces"}
        ],
        "problems": [
            {"id": "CF-1311F", "name": "Moving Points", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/1311/problem/F", "insight": "Sort by velocity, sweep with 2 Fenwicks for count and coordinate prefix sums.", "tags": ["Fenwick", "Line Sweep", "Coordinate Compression"]},
            {"id": "CF-1073D", "name": "Berland Fair", "platform": "Codeforces", "rating": 1800, "url": "https://codeforces.com/contest/1073/problem/D", "insight": "Fenwick tree tracking active stalls and sum of costs for fast cycle simulation.", "tags": ["Fenwick", "Binary Search"]},
            {"id": "CF-1208D", "name": "Restore Permutation", "platform": "Codeforces", "rating": 1900, "url": "https://codeforces.com/contest/1208/problem/D", "insight": "Reverse reconstruction using Fenwick binary lifting in O(log N).", "tags": ["Fenwick", "Binary Lifting", "Greedy"]},
            {"id": "CSES-1648", "name": "Dynamic Range Sum Queries", "platform": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1648", "insight": "Standard Fenwick tree 1-based prefix sums and point updates.", "tags": ["Fenwick", "Range Queries"]},
            {"id": "CF-1404C", "name": "Fixed Point Removal", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1404/problem/C", "insight": "Offline query sweep with Fenwick binary lifting to find maximum active prefix.", "tags": ["Fenwick", "Binary Lifting", "Offline Sweep"]}
        ]
    },
    "02": {
        "externalLinks": [
            {"title": "CP-Algorithms: Segment Tree Core & Lazy Propagation", "url": "https://cp-algorithms.com/data_structures/segment_tree.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: Segment Tree Beats (kenta_z / jiry_2)", "url": "https://codeforces.com/blog/entry/57319", "source": "Codeforces"},
            {"title": "USACO Guide: Range Updates with Lazy Propagation", "url": "https://usaco.guide/plat/lazy-segtree", "source": "USACO Guide"},
            {"title": "YouKn0wWho Academy: Persistent Segment Tree", "url": "https://youkn0wwho.academy/topic-list#persistent-segtree", "source": "YouKn0wWho"}
        ],
        "problems": [
            {"id": "CF-52C", "name": "Circular RMQ", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/52/problem/C", "insight": "Range add with range min queries on circular arrays split into two intervals.", "tags": ["Segment Tree", "Lazy Propagation"]},
            {"id": "CF-438D", "name": "The Child and Sequence", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/438/problem/D", "insight": "Modulo updates decrease value by at least half; prune segments with max < mod.", "tags": ["Segment Tree", "Amortized Analysis"]},
            {"id": "CF-840D", "name": "Destiny", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/840/problem/D", "insight": "Persistent segment tree on frequencies to query elements with frequency > (r-l+1)/k.", "tags": ["Persistent SegTree", "Order Statistics"]},
            {"id": "CF-911G", "name": "Mass Change Queries", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/911/problem/G", "insight": "Dynamic segment tree node merging for each value from 1 to 100.", "tags": ["Dynamic SegTree", "Segment Tree Merging"]},
            {"id": "CSES-1736", "name": "Polynomial Queries", "platform": "CSES", "rating": 2100, "url": "https://cses.fi/problemset/task/1736", "insight": "Lazy segment tree maintaining arithmetic progression tags (base and slope).", "tags": ["Lazy SegTree", "Range Updates"]}
        ]
    },
    "03": {
        "externalLinks": [
            {"title": "CP-Algorithms: Merge Sort Tree & Range Frequency", "url": "https://cp-algorithms.com/data_structures/segment_tree.html#merge-sort-tree", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: Fractional Cascading on Merge Sort Trees", "url": "https://codeforces.com/blog/entry/15890", "source": "Codeforces"},
            {"title": "USACO Guide: Static 2D Range Queries", "url": "https://usaco.guide/plat/2d-range", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "SPOJ-KQUERY", "name": "K-query", "platform": "SPOJ", "rating": 1800, "url": "https://www.spoj.com/problems/KQUERY/", "insight": "Count elements > k in [L, R] using Merge Sort Tree binary search or offline Fenwick.", "tags": ["Merge Sort Tree", "Fractional Cascading"]},
            {"id": "SPOJ-MKTHNUM", "name": "K-th Number", "platform": "SPOJ", "rating": 2000, "url": "https://www.spoj.com/problems/MKTHNUM/", "insight": "Binary search on answer + Merge Sort Tree count or Persistent SegTree walk.", "tags": ["Merge Sort Tree", "Persistent SegTree"]},
            {"id": "CF-990G", "name": "GCD Counting", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/990/problem/G", "insight": "Multiples grouping with tree paths and sorted divisor vectors.", "tags": ["Merge Sort Tree", "Number Theory", "Tree DP"]}
        ]
    },
    "04": {
        "externalLinks": [
            {"title": "CP-Algorithms: Sqrt Decomposition & Block Updates", "url": "https://cp-algorithms.com/data_structures/sqrt_decomposition.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: Mo's Algorithm on Arrays and Trees (Errichto)", "url": "https://codeforces.com/blog/entry/43230", "source": "Codeforces"},
            {"title": "USACO Guide: Mo's Algorithm with Hilbert Curve Sorting", "url": "https://usaco.guide/plat/mo", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-86D", "name": "Powerful array", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/86/problem/D", "insight": "Classic Mo's algorithm tracking frequency squares with O(1) state transitions.", "tags": ["Mo's Algorithm", "Sqrt Decomposition"]},
            {"id": "CF-617E", "name": "XOR and Favorite Number", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/617/problem/E", "insight": "Prefix XOR array with Mo's algorithm querying frequency of prefixXOR ^ k.", "tags": ["Mo's Algorithm", "Prefix XOR"]},
            {"id": "CF-375D", "name": "Tree and Queries", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/375/problem/D", "insight": "Euler tour subtree flattening with Mo's algorithm or DSU on Tree.", "tags": ["Mo's on Trees", "Euler Tour", "DSU on Tree"]},
            {"id": "CF-940F", "name": "Machine Learning", "platform": "Codeforces", "rating": 2500, "url": "https://codeforces.com/contest/940/problem/F", "insight": "3D Mo's Algorithm with point updates in O(N^(5/3)) time.", "tags": ["Mo's with Updates", "3D Sqrt"]}
        ]
    },
    "05": {
        "externalLinks": [
            {"title": "CP-Algorithms: Treap (Cartesian Tree with Random Priorities)", "url": "https://cp-algorithms.com/data_structures/treap.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Sparse Table RMQ", "url": "https://cp-algorithms.com/data_structures/sparse-table.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Link-Cut Trees (Dynamic Forest Connectivity)", "url": "https://usaco.guide/adv/lct", "source": "USACO Guide"},
            {"title": "YouKn0wWho Academy: PBDS Policy Based Data Structures", "url": "https://youkn0wwho.academy/topic-list#pbds", "source": "YouKn0wWho"}
        ],
        "problems": [
            {"id": "CF-863D", "name": "Almost Difference", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/863/problem/D", "insight": "Implicit Treap split/merge or reverse query coordinate tracking.", "tags": ["Implicit Treap", "Coordinate Tracking"]},
            {"id": "CF-702F", "name": "T-Shirts", "platform": "Codeforces", "rating": 2700, "url": "https://codeforces.com/contest/702/problem/F", "insight": "Treap split by affordability, subtract price, and re-insert with small-to-large merging.", "tags": ["Treap", "Small to Large"]},
            {"id": "CF-1175E", "name": "Minimal Segment Cover", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/1175/problem/E", "insight": "Binary lifting on greedy rightmost transitions over interval endpoints.", "tags": ["Binary Lifting", "Sparse Table", "Greedy"]},
            {"id": "CF-1144F", "name": "Graph Without Long Directed Paths", "platform": "Codeforces", "rating": 1700, "url": "https://codeforces.com/contest/1144/problem/F", "insight": "Bipartite graph 2-coloring for sink-source directed orientations.", "tags": ["DSU", "Graphs", "Bipartite"]}
        ]
    },
    "06": {
        "externalLinks": [
            {"title": "CP-Algorithms: Lowest Common Ancestor (Binary Lifting & RMQ)", "url": "https://cp-algorithms.com/graph/lca.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Heavy-Light Decomposition", "url": "https://cp-algorithms.com/graph/hld.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: DSU on Tree (Sack / Small-to-Large Merging)", "url": "https://codeforces.com/blog/entry/44351", "source": "Codeforces"},
            {"title": "USACO Guide: Centroid Decomposition", "url": "https://usaco.guide/plat/centroid", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-600E", "name": "Lomsat gelh", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/600/problem/E", "insight": "DSU on Tree / Sack maintains frequency sum of dominant colors across subtrees in O(N log N).", "tags": ["DSU on Tree", "Sack", "Euler Tour"]},
            {"id": "CF-343D", "name": "Water Tree", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/343/problem/D", "insight": "Euler tour subtree update (fill) + path to root query (empty) using Lazy SegTree.", "tags": ["Euler Tour", "HLD", "Lazy SegTree"]},
            {"id": "CF-1009F", "name": "Dominant Indices", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1009/problem/F", "insight": "Dsu on Tree with depth array or Long Path Decomposition in O(N).", "tags": ["DSU on Tree", "Tree DP"]},
            {"id": "CF-321C", "name": "Ciel the Commander", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/321/problem/C", "insight": "Centroid decomposition recursion assigns tree depth ranks A through Z (<= 26 levels).", "tags": ["Centroid Decomposition", "Divide and Conquer"]},
            {"id": "CSES-1138", "name": "Path Queries", "platform": "CSES", "rating": 1800, "url": "https://cses.fi/problemset/task/1138", "insight": "Euler tour + in/out difference updates on Fenwick tree for point updates and path sums.", "tags": ["Euler Tour", "Fenwick", "LCA"]}
        ]
    },
    "07": {
        "externalLinks": [
            {"title": "CP-Algorithms: Strongly Connected Components (Kosaraju & Tarjan)", "url": "https://cp-algorithms.com/graph/strongly-connected-components.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: 2-SAT Problem", "url": "https://cp-algorithms.com/graph/2SAT.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Topological Sort & DAG DP", "url": "https://usaco.guide/gold/topo", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-1239D", "name": "Catastrophe", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/1239/problem/D", "insight": "Kosaraju SCC on jury-personnel digraph; find a sink SCC without outgoing edges.", "tags": ["SCC", "Condensation DAG", "Graphs"]},
            {"id": "CF-228E", "name": "The Road to Berland is Paved With Good Intentions", "platform": "Codeforces", "rating": 1900, "url": "https://codeforces.com/contest/228/problem/E", "insight": "2-SAT clause modeling: x_u XOR x_v = state.", "tags": ["2-SAT", "SCC", "Implication Graph"]},
            {"id": "CF-1215D", "name": "Ticket Game", "platform": "Codeforces", "rating": 1800, "url": "https://codeforces.com/contest/1215/problem/D", "insight": "Game invariant symmetry and pair matching on questions.", "tags": ["Game Theory", "Greedy"]},
            {"id": "CSES-1684", "name": "Giant Pizza", "platform": "CSES", "rating": 1900, "url": "https://cses.fi/problemset/task/1684", "insight": "Standard 2-SAT construction for customer toppings preferences.", "tags": ["2-SAT", "SCC"]}
        ]
    },
    "08": {
        "externalLinks": [
            {"title": "CP-Algorithms: Shortest Paths (Dijkstra, 0-1 BFS, Floyd-Warshall)", "url": "https://cp-algorithms.com/graph/dijkstra.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Eulerian Path & Circuit (Hierholzer)", "url": "https://cp-algorithms.com/graph/euler_path.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Kruskal Reconstruction Tree", "url": "https://usaco.guide/adv/kruskal-tree", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-1076D", "name": "Edge Deletion", "platform": "Codeforces", "rating": 1800, "url": "https://codeforces.com/contest/1076/problem/D", "insight": "Shortest path DAG tree extracted from Dijkstra; take first k edges by BFS.", "tags": ["Dijkstra", "Shortest Path Tree"]},
            {"id": "CF-1156D", "name": "0-1-Tree", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/1156/problem/D", "insight": "DSU components on 0-edges and 1-edges; count 0-paths, 1-paths, and 01-transition paths.", "tags": ["DSU", "Trees", "Combinatorics"]},
            {"id": "CF-723E", "name": "One-Way Roads", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/723/problem/E", "insight": "Add dummy node connecting odd-degree vertices, build Eulerian circuit with Hierholzer.", "tags": ["Eulerian Circuit", "Graph Orientation"]},
            {"id": "CSES-1195", "name": "Flight Discount", "platform": "CSES", "rating": 1600, "url": "https://cses.fi/problemset/task/1195", "insight": "2-state Dijkstra: state 0 = coupon unused, state 1 = coupon used.", "tags": ["Dijkstra", "State Space Graph"]}
        ]
    },
    "09": {
        "externalLinks": [
            {"title": "CP-Algorithms: Dinic's Algorithm for Maximum Flow", "url": "https://cp-algorithms.com/graph/dinic.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Minimum Cost Maximum Flow (Successive Shortest Path & SPFA)", "url": "https://cp-algorithms.com/graph/min_cost_flow.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Min-Cut Modeling & Project Selection", "url": "https://usaco.guide/adv/max-flow", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-1082G", "name": "Petya and Graph", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1082/problem/G", "insight": "Maximum weight closure / Project selection with Min-Cut: total edge weight - min cut.", "tags": ["Min Cut", "Dinic", "Project Selection"]},
            {"id": "CF-1404E", "name": "Bricks", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/1404/problem/E", "insight": "Maximum Independent Set on bipartite conflict graph of horizontal and vertical bonds.", "tags": ["Bipartite Matching", "Min Cut", "Dinic"]},
            {"id": "CF-277E", "name": "Binary Tree on Plane", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/277/problem/E", "insight": "Min-Cost Max-Flow: parent out-capacity 2, child in-capacity 1, cost = Euclidean distance.", "tags": ["MCMF", "Network Flow", "Geometry"]},
            {"id": "CSES-1695", "name": "Police Chase", "platform": "CSES", "rating": 1900, "url": "https://cses.fi/problemset/task/1695", "insight": "Find min-cut edges after running Dinic's max flow from source to sink.", "tags": ["Dinic", "Min Cut", "Graphs"]}
        ]
    },
    "10": {
        "externalLinks": [
            {"title": "CP-Algorithms: Convex Hull Trick & Dynamic CHT", "url": "https://cp-algorithms.com/geometry/convex_hull_trick.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Divide and Conquer DP Optimization", "url": "https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: SOS DP (Sum Over Subsets) - Errichto", "url": "https://codeforces.com/blog/entry/45223", "source": "Codeforces"},
            {"title": "Codeforces Blog: 1D/1D Dynamic Programming Optimizations", "url": "https://codeforces.com/blog/entry/8284", "source": "Codeforces"}
        ],
        "problems": [
            {"id": "CF-319C", "name": "Kalila and Dimna in the Logging Industry", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/319/problem/C", "insight": "Standard CHT: dp[i] = min_{j<i} (dp[j] + b[j]*a[i]) with monotonically decreasing slopes.", "tags": ["Convex Hull Trick", "DP Optimization"]},
            {"id": "CF-1083E", "name": "The Fair Nut and Rectangles", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/1083/problem/E", "insight": "Li Chao Tree or Monotone CHT on sorted rectangle coordinates with cross-cost subtract.", "tags": ["CHT", "Li Chao Tree", "DP"]},
            {"id": "CF-1175G", "name": "Yet Another Partiton Problem", "platform": "Codeforces", "rating": 2900, "url": "https://codeforces.com/contest/1175/problem/G", "insight": "Monotone stack + Persistent Li Chao Tree for range-max multiplier DP in O(KN log N).", "tags": ["Li Chao Tree", "Monotone Stack", "D&C DP"]},
            {"id": "CF-165E", "name": "Compatible Numbers", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/165/problem/E", "insight": "SOS DP computes submask ancestor for inverted mask ~a[i] in O(N * 2^N).", "tags": ["SOS DP", "Bitmasks"]},
            {"id": "CF-321E", "name": "Ciel and Gondolas", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/321/problem/E", "insight": "Divide and Conquer DP optimization based on Quadrangle Inequality monotonicity.", "tags": ["Divide and Conquer DP", "Quadrangle Inequality"]}
        ]
    },
    "11": {
        "externalLinks": [
            {"title": "CP-Algorithms: String Hashing & Randomized Anti-Hash", "url": "https://cp-algorithms.com/string/string-hashing.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Prefix Function & KMP", "url": "https://cp-algorithms.com/string/prefix-function.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Aho-Corasick Automaton", "url": "https://cp-algorithms.com/string/aho_corasick.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Suffix Automaton (SAM)", "url": "https://cp-algorithms.com/string/suffix-automaton.html", "source": "CP-Algorithms"}
        ],
        "problems": [
            {"id": "CF-1200E", "name": "Compress Words", "platform": "Codeforces", "rating": 1600, "url": "https://codeforces.com/contest/1200/problem/E", "insight": "KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix.", "tags": ["KMP", "Rolling Hash", "Strings"]},
            {"id": "CF-432D", "name": "Prefixes and Suffixes", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/432/problem/D", "insight": "Z-algorithm + prefix function DP to count occurrences of all matching prefixes.", "tags": ["Z-Algorithm", "KMP", "DP"]},
            {"id": "CF-963D", "name": "Frequency of String", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/963/problem/D", "insight": "Aho-Corasick multi-pattern matching tracks occurrence position queues.", "tags": ["Aho-Corasick", "Trie", "Strings"]},
            {"id": "CF-1037H", "name": "Security", "platform": "Codeforces", "rating": 2800, "url": "https://codeforces.com/contest/1037/problem/H", "insight": "Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char.", "tags": ["Suffix Automaton", "Persistent SegTree"]},
            {"id": "CSES-1753", "name": "String Matching", "platform": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1753", "insight": "Classic KMP pattern search / Z-algorithm linear scan.", "tags": ["KMP", "Z-Algorithm"]}
        ]
    },
    "12": {
        "externalLinks": [
            {"title": "CP-Algorithms: Linear Sieve & Smallest Prime Factor (SPF)", "url": "https://cp-algorithms.com/algebra/prime-sieve-linear.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Extended Euclidean & Linear Diophantine", "url": "https://cp-algorithms.com/algebra/extended-euclid-algorithm.html", "source": "CP-Algorithms"},
            {"title": "YouKn0wWho Academy: Möbius Inversion & Multiplicative Functions", "url": "https://youkn0wwho.academy/topic-list#mobius-inversion", "source": "YouKn0wWho"}
        ],
        "problems": [
            {"id": "CF-1033D", "name": "Divisors", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/1033/problem/D", "insight": "GCD pairwise cross-elimination to factor numbers up to 2*10^18 without full Pollard-Rho.", "tags": ["Number Theory", "GCD", "Factoring"]},
            {"id": "CF-803F", "name": "Coprime Subsequences", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/803/problem/F", "insight": "Möbius inversion: count multiples of d, apply 2^(count) - 1 with mobius weights.", "tags": ["Möbius Inversion", "Inclusion Exclusion"]},
            {"id": "CF-900D", "name": "Unusual Sequences", "platform": "Codeforces", "rating": 2200, "url": "https://codeforces.com/contest/900/problem/D", "insight": "Möbius function over divisors of y/x with fast memoized recursion.", "tags": ["Möbius Inversion", "Number Theory", "Combinatorics"]},
            {"id": "CSES-1712", "name": "Exponentiation II", "platform": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1712", "insight": "Euler Totient theorem / Fermat: a^(b^c) mod p = a^(b^c mod (p-1)) mod p.", "tags": ["Binpow", "Euler Phi"]}
        ]
    },
    "13": {
        "externalLinks": [
            {"title": "CP-Algorithms: Binomial Coefficients & Lucas Theorem", "url": "https://cp-algorithms.com/combinatorics/binomial-coefficients.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Burnside's Lemma & Polya Enumeration", "url": "https://cp-algorithms.com/combinatorics/burnside.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Bitmask Operations and Submask Enumeration", "url": "https://usaco.guide/gold/combo", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-449D", "name": "Jzzhu and Numbers", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/449/problem/D", "insight": "SOS DP computes superset counts; apply Principle of Inclusion-Exclusion.", "tags": ["SOS DP", "Inclusion Exclusion", "Bitwise"]},
            {"id": "CF-1043F", "name": "Make It One", "platform": "Codeforces", "rating": 2500, "url": "https://codeforces.com/contest/1043/problem/F", "insight": "Combinatorics with Möbius inversion checking whether k elements have gcd = 1.", "tags": ["Combinatorics", "Möbius", "DP"]},
            {"id": "CSES-2209", "name": "Counting Necklaces", "platform": "CSES", "rating": 1800, "url": "https://cses.fi/problemset/task/2209", "insight": "Burnside's lemma over rotational group of order n: sum m^gcd(i, n) / n.", "tags": ["Burnside's Lemma", "Combinatorics"]}
        ]
    },
    "14": {
        "externalLinks": [
            {"title": "CP-Algorithms: Linear Systems & Gaussian Elimination", "url": "https://cp-algorithms.com/linear_algebra/linear-system-gauss.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Matrix Determinant & Matrix Tree Theorem", "url": "https://cp-algorithms.com/linear_algebra/determinant-gauss.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: Linear Basis Tutorial over F_2", "url": "https://codeforces.com/blog/entry/68953", "source": "Codeforces"}
        ],
        "problems": [
            {"id": "CF-1101G", "name": "Zero-XOR Subset-less", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1101/problem/G", "insight": "Prefix XOR array inserted into XOR linear basis; max partitions = basis size.", "tags": ["XOR Basis", "Linear Algebra"]},
            {"id": "CF-959F", "name": "Mahmoud and Ehab and yet another xor task", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/959/problem/F", "insight": "Incremental XOR basis; count combinations as 2^(prefix_len - basis_size).", "tags": ["XOR Basis", "Offline Queries"]},
            {"id": "CSES-2415", "name": "Spanning Trees", "platform": "CSES", "rating": 2300, "url": "https://cses.fi/problemset/task/2415", "insight": "Matrix Tree Theorem: compute (N-1)x(N-1) cofactor determinant of Laplacian matrix.", "tags": ["Matrix Tree Theorem", "Gaussian Elimination"]}
        ]
    },
    "15": {
        "externalLinks": [
            {"title": "CP-Algorithms: Fast Fourier Transform & NTT", "url": "https://cp-algorithms.com/algebra/fft.html", "source": "CP-Algorithms"},
            {"title": "Codeforces Blog: Fast Walsh-Hadamard Transform (FWHT)", "url": "https://codeforces.com/blog/entry/71892", "source": "Codeforces"},
            {"title": "YouKn0wWho Academy: Formal Power Series & NTT Convolutions", "url": "https://youkn0wwho.academy/topic-list#fft", "source": "YouKn0wWho"}
        ],
        "problems": [
            {"id": "CF-528D", "name": "Cutlet", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/528/problem/D", "insight": "Bitmask matching for 4 DNA bases converted into 4 independent FFT polynomial convolutions.", "tags": ["FFT", "Polynomial Multiplication", "Strings"]},
            {"id": "CF-1096G", "name": "Lucky Tickets", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1096/problem/G", "insight": "Polynomial exponentiation P(x)^(N/2) using NTT mod 998244353 in O(K log K log N).", "tags": ["NTT", "Polynomial Exponentiation"]},
            {"id": "CF-1251F", "name": "Red-White Fence", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/1251/problem/F", "insight": "Divide-and-Conquer NTT multiplying frequency polynomials.", "tags": ["D&C NTT", "Generating Functions"]}
        ]
    },
    "16": {
        "externalLinks": [
            {"title": "CP-Algorithms: Sprague-Grundy Theorem & Nim Games", "url": "https://cp-algorithms.com/game_theory/sprague-grundy-nim.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Combinatorial Game Theory", "url": "https://usaco.guide/adv/game-theory", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-1383B", "name": "GameGame", "platform": "Codeforces", "rating": 1900, "url": "https://codeforces.com/contest/1383/problem/B", "insight": "MSB parity invariant analysis; count ones and zeros at the highest differing bit.", "tags": ["Game Theory", "Bitwise Invariants"]},
            {"id": "CF-768E", "name": "Game of Stones", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/768/problem/E", "insight": "Compute Grundy numbers for state (x, mask of used moves) using MEX recursion.", "tags": ["Sprague Grundy", "MEX", "Game DP"]},
            {"id": "CSES-1738", "name": "Moving Robots", "platform": "CSES", "rating": 1900, "url": "https://cses.fi/problemset/task/1738", "insight": "Probability and matrix transition game DP.", "tags": ["Game DP", "Probability"]}
        ]
    },
    "17": {
        "externalLinks": [
            {"title": "CP-Algorithms: 2D Geometry Primitives & Cross Products", "url": "https://cp-algorithms.com/geometry/basic-geometry.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms: Convex Hull (Monotone Chain)", "url": "https://cp-algorithms.com/geometry/convex-hull.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Computational Geometry", "url": "https://usaco.guide/adv/geometry", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-166B", "name": "Polygons", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/166/problem/B", "insight": "Binary search on upper/lower convex hull rays or point-in-convex-polygon orientation checks.", "tags": ["Convex Hull", "Point in Polygon"]},
            {"id": "CF-70D", "name": "Professor's task", "platform": "Codeforces", "rating": 2400, "url": "https://codeforces.com/contest/70/problem/D", "insight": "Dynamic online convex hull maintenance using std::map for upper and lower envelopes.", "tags": ["Dynamic Convex Hull", "Geometry"]},
            {"id": "CSES-2195", "name": "Convex Hull", "platform": "CSES", "rating": 1700, "url": "https://cses.fi/problemset/task/2195", "insight": "Monotone Chain (Andrew's algorithm) sorting points by (x, y) with cross product tests.", "tags": ["Convex Hull", "Monotone Chain"]}
        ]
    },
    "18": {
        "externalLinks": [
            {"title": "Codeforces Blog: Anti-Hash Tests & 64-Bit SplitMix Hygiene (neal)", "url": "https://codeforces.com/blog/entry/62393", "source": "Codeforces"},
            {"title": "CP-Algorithms: Parallel Binary Search", "url": "https://cp-algorithms.com/others/parallel-binary-search.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide: Meet-in-the-Middle 2^(N/2)", "url": "https://usaco.guide/gold/mitm", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-888G", "name": "Xor-MST", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/888/problem/G", "insight": "Divide-and-Conquer Boruvka MST over Binary Trie bits.", "tags": ["Binary Trie", "Boruvka", "XOR"]},
            {"id": "CF-1006F", "name": "Xor-Paths", "platform": "Codeforces", "rating": 2000, "url": "https://codeforces.com/contest/1006/problem/F", "insight": "Meet-in-the-middle on grid diagonal: meet at step (n+m-2)/2 with hash map.", "tags": ["Meet in the Middle", "Grid Paths"]},
            {"id": "CF-484E", "name": "Sign on Fence", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/484/problem/E", "insight": "Parallel Binary Search + Persistent Segment Tree for range max contiguous ones.", "tags": ["Parallel Binary Search", "Persistent SegTree"]},
            {"id": "CSES-1628", "name": "Meet in the Middle", "platform": "CSES", "rating": 1600, "url": "https://cses.fi/problemset/task/1628", "insight": "Split 40 elements into two halves of 20, sort second half, two-pointer / binary search count.", "tags": ["Meet in the Middle", "Binary Search"]}
        ]
    },
    "19": {
        "externalLinks": [
            {"title": "Codeforces Blog: Greedy Exchange Arguments (Errichto)", "url": "https://codeforces.com/blog/entry/66734", "source": "Codeforces"},
            {"title": "USACO Guide: Priority Queue Regret / Undo Heaps", "url": "https://usaco.guide/silver/greedy-sorting", "source": "USACO Guide"}
        ],
        "problems": [
            {"id": "CF-1526C2", "name": "Potions (Hard Version)", "platform": "Codeforces", "rating": 1600, "url": "https://codeforces.com/contest/1526/problem/C2", "insight": "Regret / Undo Heap: greedily drink potion; if health < 0, pop and un-drink the most negative potion.", "tags": ["Regret Heap", "Greedy Invariants"]},
            {"id": "CF-864D", "name": "Make a Permutation!", "platform": "Codeforces", "rating": 1600, "url": "https://codeforces.com/contest/864/problem/D", "insight": "Greedy choice with frequency counters and skip-if-first-occurrence flags.", "tags": ["Greedy", "Frequencies"]},
            {"id": "CF-1157C2", "name": "Increasing Subsequence (hard version)", "platform": "Codeforces", "rating": 1700, "url": "https://codeforces.com/contest/1157/problem/C2", "insight": "Greedy two-pointer picks smaller side; if equal, simulate strictly longest run on both sides.", "tags": ["Greedy", "Two Pointers"]}
        ]
    },
    "20": {
        "externalLinks": [
            {"title": "Codeforces Blog: Slope Trick Tutorial (zscoder / SleepingCup)", "url": "https://codeforces.com/blog/entry/77298", "source": "Codeforces"},
            {"title": "Codeforces Blog: The Alien's Trick (WQS Binary Search / Lagrangian Relaxation)", "url": "https://codeforces.com/blog/entry/49691", "source": "Codeforces"}
        ],
        "problems": [
            {"id": "CF-713C", "name": "Sonya and Problem Wihtout a Legend", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/713/problem/C", "insight": "Slope Trick with max-heap maintaining slope change points of convex cost function in O(N log N).", "tags": ["Slope Trick", "Priority Queue", "Convexity"]},
            {"id": "CF-1279F", "name": "New Year and Handle Change", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/1279/problem/F", "insight": "Aliens Trick / WQS binary search penalizing each operation by lambda.", "tags": ["Aliens Trick", "WQS Binary Search", "DP"]},
            {"id": "CF-1534E", "name": "Lost Array", "platform": "Codeforces", "rating": 2300, "url": "https://codeforces.com/contest/1534/problem/E", "insight": "Shortest path BFS over odd/even bit counts or balanced decoupled greedy assignment.", "tags": ["Greedy", "BFS", "Parity"]}
        ]
    },
    "21": {
        "externalLinks": [
            {"title": "Codeforces Blog: Matroid Intersection in Competitive Programming (bqi343 / ecnerwala)", "url": "https://codeforces.com/blog/entry/69287", "source": "Codeforces"},
            {"title": "YouKn0wWho Academy: Matroid Theory, Duality and Antimatroids", "url": "https://youkn0wwho.academy/topic-list#matroids", "source": "YouKn0wWho"}
        ],
        "problems": [
            {"id": "CF-1556H", "name": "DIY Tree", "platform": "Codeforces", "rating": 3300, "url": "https://codeforces.com/contest/1556/problem/H", "insight": "Matroid Intersection: Graphic Matroid M(G) + Degree-Constrained Partition Matroid.", "tags": ["Matroid Intersection", "Spanning Tree", "Augmenting Paths"]},
            {"id": "CF-1408G", "name": "Clusterization Counting", "platform": "Codeforces", "rating": 2700, "url": "https://codeforces.com/contest/1408/problem/G", "insight": "Kruskal reconstruction tree + DP on clique subtrees.", "tags": ["Kruskal Tree", "Tree DP", "Matroid"]},
            {"id": "CF-1284E", "name": "New Year and Castle Construction", "platform": "Codeforces", "rating": 2600, "url": "https://codeforces.com/contest/1284/problem/E", "insight": "Angular sweep with complementary combinatorics counting points strictly outside convex hulls.", "tags": ["Angular Sweep", "Geometry", "Combinatorics"]}
        ]
    },
    "22": {
        "externalLinks": [
            {"title": "USACO Guide: Sweep-Line Algorithms & 2D Rectangle Union Area", "url": "https://usaco.guide/plat/sweep-line", "source": "USACO Guide"},
            {"title": "CP-Algorithms: Bentley-Ottmann Line Segment Intersections", "url": "https://cp-algorithms.com/geometry/intersecting_segments.html", "source": "CP-Algorithms"}
        ],
        "problems": [
            {"id": "CF-1000C", "name": "Covered Points Count", "platform": "Codeforces", "rating": 1700, "url": "https://codeforces.com/contest/1000/problem/C", "insight": "1D event abstraction (+1 at start, -1 at end+1) with coordinate difference accumulation.", "tags": ["Line Sweep", "Difference Array"]},
            {"id": "CF-1401E", "name": "Divide Square", "platform": "Codeforces", "rating": 2100, "url": "https://codeforces.com/contest/1401/problem/E", "insight": "Euler formula V - E + F = 2 + Line Sweep with Fenwick querying active horizontal segments.", "tags": ["Line Sweep", "Fenwick", "Geometry"]},
            {"id": "CSES-1741", "name": "Area of Rectangles", "platform": "CSES", "rating": 2100, "url": "https://cses.fi/problemset/task/1741", "insight": "Klee's Measure: 1D sweep on X, Segment tree maintaining min and min-count on Y in O(N log N).", "tags": ["Klee's Measure", "Segment Tree", "Line Sweep"]}
        ]
    }
}

# Attach external resources and curated problems to each module and topic
for module in data["modules"]:
    sec_id = module["sectionId"]
    res = TOPIC_RESOURCES.get(sec_id, {"externalLinks": [], "problems": []})
    module["externalLinks"] = res["externalLinks"]
    module["curatedProblems"] = res["problems"]
    
    # Also attach relevant problems and external resources to topics
    for topic in module["topics"]:
        topic["externalLinks"] = res["externalLinks"]
        topic["curatedProblems"] = res["problems"]

with open(DATA_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Enriched all modules and topics with external links and curated problem sets successfully!")
