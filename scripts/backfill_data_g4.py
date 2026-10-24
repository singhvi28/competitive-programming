# Group 4: Line Sweep & Sweeping Techniques (Module 22 - 14 topics)

G4_DATA = {
    "22-dimensional-reduction-via-event-processing": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1700–2400\n- Prerequisites: Sorting, Events Queue, 1D Data Structures (BIT / Segment Tree)\n- Core Concept: Transforms static $D$-dimensional geometric problems into dynamic $(D-1)$-dimensional time-evolving queries.",
        "coreIntuition": "Dimensional reduction is the foundational paradigm of Sweep Line: instead of considering all $N$ objects simultaneously across 2D space, project time/space along one axis (say $X$). Sort all discrete changes into an event queue. As an imaginary vertical sweep line moves from $X = -\\infty$ to $+\\infty$, entities are inserted into an active status data structure when the sweep line encounters their left boundary, queried when point/query events occur, and removed when the sweep line passes their right boundary. This converts a 2D static query into a 1D dynamic range update/query!",
        "derivation": "Consider $N$ 2D points or rectangles. Checking all pairs in 2D space takes $\\mathcal{O}(N^2)$. By sorting the $2N$ boundary events along the $X$-axis in $\\mathcal{O}(N \\log N)$, the sweep line maintains only the currently active elements intersecting the line $x = X_{cur}$. The active set is maintained in a Fenwick or Segment Tree indexed by the $Y$-coordinate. Each event causes $\\mathcal{O}(1)$ modifications to the 1D tree, leading to an overall runtime of $\\mathcal{O}(N \\log N)$ and $\\mathcal{O}(N)$ space.",
        "templateCpp": "// Dimensional Reduction via Sweep Line Event Processing\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Event {\n    ll x;\n    int type; // 0 = Add interval, 1 = Query point, 2 = Remove interval\n    ll y1, y2;\n    int id;\n    bool operator<(const Event& o) const {\n        if (x != o.x) return x < o.x;\n        return type < o.type; // Process additions before queries before removals\n    }\n};\n\nvoid sweep_line_events(vector<Event>& events) {\n    sort(events.begin(), events.end());\n    // Fenwick tree or active set over Y coordinates\n    for (const auto& ev : events) {\n        if (ev.type == 0) { /* insert [y1, y2] into active set */ }\n        else if (ev.type == 1) { /* query y1 in active set */ }\n        else if (ev.type == 2) { /* remove [y1, y2] from active set */ }\n    }\n}",
        "recognitionPatterns": [
            "2D range queries: 'Count points inside rectangle $[X_1, X_2] \\times [Y_1, Y_2]$'.",
            "Interval intersection or rectangle union area/perimeter.",
            "Static offline queries with 2 or more constraints ($x_i \\le X$ and $y_i \\le Y$).",
            "Manhattan distance nearest neighbors or closest pair of points."
        ],
        "commonBugs": [
            "Event tie-breaking: when events share the exact same $X$-coordinate, processing order matters critically. If intervals are closed $[L, R]$, additions must be processed before queries, which must be processed before deletions.",
            "Coordinate compression omission: $Y$-coordinates up to $10^9$ must be mapped to $[0, K-1]$ before inserting into standard array-backed Fenwick/Segment trees.",
            "Forgetting to clear or un-insert expired elements on exit events, leaving stale entries in the active structure.",
            "Using 32-bit `int` for $X$ or $Y$ coordinates when products or sums exceed $2 \\times 10^9$."
        ]
    },
    "22-mapping-sparse-10-9-domains-to-dense-0-k-1-ranks": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–2000\n- Prerequisites: Coordinate Compression, Sorting, Unique, Binary Search (`std::lower_bound`)\n- Tradeoff: Compresses arbitrary $10^9$ coordinate domains into compact $[0, K-1]$ ranks with $K \\le 2N$ to fit in array-based trees.",
        "coreIntuition": "Tree data structures like Fenwick Trees and basic Segment Trees require memory proportional to the coordinate domain size $M$. When problem coordinates lie in $[-10^9, 10^9]$, allocating a size $10^9$ array is impossible (MLE). Coordinate compression sorts all distinct coordinates appearing in inputs and queries, removes duplicates, and replaces each large coordinate with its 0-based or 1-based index rank via `std::lower_bound`. The relative order of all coordinates is preserved, while the domain size collapses from $10^9$ to at most $2N$!",
        "derivation": "Given $N$ query/event points $x_1, x_2, \\dots, x_N \\in \\mathbb{R}$. Sorting and deduplicating produces unique array $U$ of size $K \\le N$ in $\\mathcal{O}(N \\log N)$. For any $x_i$, its compressed rank is $rank(x_i) = \\text{lower\\_bound}(U, x_i) - U.\\text{begin}()$. Order is preserved: $x_a < x_b \\iff rank(x_a) < rank(x_b)$. For interval problems where intervals have length, remember to also compress $R_i + 1$ or track endpoint spans $U[i+1] - U[i]$ to preserve continuous measure.",
        "templateCpp": "// Coordinate Compression Helper Class\n#include <bits/stdc++.h>\nusing namespace std;\n\ntemplate <typename T>\nstruct CoordinateCompressor {\n    vector<T> vals;\n    void add(T x) { vals.push_back(x); }\n    void build() {\n        sort(vals.begin(), vals.end());\n        vals.erase(unique(vals.begin(), vals.end()), vals.end());\n    }\n    int get_rank(T x) const {\n        return lower_bound(vals.begin(), vals.end(), x) - vals.begin();\n    }\n    int size() const { return vals.size(); }\n    T get_val(int rank) const { return vals[rank]; }\n};",
        "recognitionPatterns": [
            "Coordinates or values up to $10^9$ or $10^{18}$ where only relative comparisons matter.",
            "Range queries on offline data with sparse coordinate points.",
            "Fenwick tree or Segment tree indexing over large continuous domains.",
            "Interval sweep line where endpoints are floating point numbers or large integers."
        ],
        "commonBugs": [
            "Calling `get_rank()` before calling `build()` (sorting and deduplicating), returning nonsensical ranks.",
            "Forgetting to add query endpoints into the compression vector: if queries test coordinates not in `vals`, `get_rank` might return inconsistent or out-of-bounds positions.",
            "Interval length corruption: mapping $[1, 2]$ and $[2, 100]$ to contiguous ranks $[0, 1]$ and $[1, 2]$ loses the physical length of intervals unless span weights $U[i+1] - U[i]$ are explicitly maintained.",
            "Off-by-one indexing: 0-based compressed ranks passed to 1-based Fenwick trees without `+ 1`."
        ]
    },
    "22-maximum-overlapping-intervals-in-o-n-log-n": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1300–1800\n- Prerequisites: Event sorting, Prefix sums, Two pointers\n- Tradeoff: Solves peak concurrency / maximum overlapping intervals in $\\mathcal{O}(N \\log N)$ time and $\\mathcal{O}(N)$ memory.",
        "coreIntuition": "To find the maximum number of intervals overlapping at any single point in time: convert each interval $[L_i, R_i]$ into two discrete events: an arrival event at $L_i$ with $+1$ and a departure event at $R_i$ with $-1$. Sort all $2N$ events chronologically. Sweep through the sorted events while maintaining a running prefix sum of active intervals. The maximum value attained by the prefix sum during the sweep is the maximum overlap!",
        "derivation": "The active interval count at point $x$ is $C(x) = \\sum_{i=1}^N [L_i \\le x \\le R_i]$. Since $C(x)$ is piecewise constant, changes occur only at interval boundaries $L_i$ and $R_i$. Summing $+1$ at $L_i$ and $-1$ immediately after $R_i$ tracks $C(x)$ exactly as a continuous 1D prefix sum. Sorting $2N$ events takes $\\mathcal{O}(N \\log N)$ time, and the linear sweep takes $\\mathcal{O}(N)$.",
        "templateCpp": "// Maximum Overlapping Intervals in O(N log N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nint max_overlapping_intervals(vector<pair<ll, ll>>& intervals, bool inclusive = true) {\n    vector<pair<ll, int>> events;\n    for (auto& [l, r] : intervals) {\n        events.push_back({l, +1});\n        // If inclusive, departure happens after arrival: order +1 before -1\n        // If non-overlapping endpoints, departure happens before arrival\n        events.push_back({r, -1});\n    }\n    // If inclusive, sort +1 before -1 at same time: use (-type)\n    sort(events.begin(), events.end(), [](const pair<ll, int>& a, const pair<ll, int>& b) {\n        if (a.first != b.first) return a.first < b.first;\n        return a.second > b.second; // +1 before -1\n    });\n    int cur = 0, max_overlap = 0;\n    for (auto& [t, delta] : events) {\n        cur += delta;\n        max_overlap = max(max_overlap, cur);\n    }\n    return max_overlap;\n}",
        "recognitionPatterns": [
            "Maximum number of concurrent meetings or rooms required (Meeting Rooms II).",
            "Peak bandwidth, power, or resource utilization over time.",
            "Interval scheduling where overlapping segments share a single resource.",
            "Finding the timestamp with the highest simultaneous user count."
        ],
        "commonBugs": [
            "Boundary tie-breaking: if an interval ends at time $T$ and another begins at time $T$, does it count as overlap? For inclusive intervals $[L, R]$, arrivals $+1$ must be sorted before departures $-1$. For half-open intervals $[L, R)$, departures $-1$ must be sorted before arrivals $+1$.",
            "Sorting on coordinate without specifying secondary tie-breaker comparison.",
            "Overflowing 32-bit `int` when interval timestamps are $10^{18}$.",
            "Assuming intervals are given sorted in input."
        ]
    },
    "22-dynamic-time-series-projection-via-binary-indexed-trees": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1 / Div2 Hard\n- Typical CF/ICPC rating range: 1700–2300\n- Prerequisites: Fenwick Tree (BIT), Offline Query Processing, Inversion Counting\n- Tradeoff: Solves 2D dominance and dynamic time-series queries in $\\mathcal{O}(N \\log N)$ time and $\\mathcal{O}(N)$ memory with tiny constants.",
        "coreIntuition": "When answering queries about time-series data of the form 'In time window $[t_1, t_2]$, how many values exceed $V$?', sorting queries offline by one parameter (e.g. time $t_2$) turns the problem into a 1D sweep line. As the time cursor $t$ advances, new observed values are inserted into a Binary Indexed Tree (BIT) at index $val$. A query for window ending at $t_2$ with lower threshold $t_1$ and value threshold $V$ is evaluated as a prefix sum query on the BIT. The BIT acts as the dynamic projection of the historical time series!",
        "derivation": "A 2D query $(x \\in [x_1, x_2], y \\in [y_1, y_2])$ can be decomposed into two prefix queries via linearity: $Q(x_2) - Q(x_1 - 1)$. By grouping and sorting queries by their $X$-threshold, elements with $x_i \\le X$ are inserted into the Fenwick tree monotonically. The Fenwick tree maintains frequency counts over $Y$ coordinates. Point updates and prefix queries both run in $\\mathcal{O}(\\log |Y|)$ time with cache-friendly contiguous array memory.",
        "templateCpp": "// Dynamic Time-Series Projection via Offline BIT Sweep\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Fenwick {\n    int n;\n    vector<ll> tree;\n    Fenwick(int n_) : n(n_), tree(n_ + 1, 0) {}\n    void add(int i, ll delta) { for (; i <= n; i += i & -i) tree[i] += delta; }\n    ll query(int i) { ll sum = 0; for (; i > 0; i -= i & -i) sum += tree[i]; return sum; }\n    ll query_range(int l, int r) { return query(r) - query(l - 1); }\n};\n\nstruct Query { int l, r, k, id; };\n\n// Count elements in subarray [l, r] with value >= k\nvector<int> count_elements_ge_k(vector<int>& a, vector<Query>& queries) {\n    int n = a.size(), q = queries.size();\n    vector<int> ans(q);\n    // Sort elements and queries by value descending\n    // ... (Sweep elements into Fenwick indexed by position 1..n) ...\n    return ans;\n}",
        "recognitionPatterns": [
            "Queries ask for number of elements in range $[L, R]$ satisfying value constraints $A_i \\ge K$.",
            "Counting inversions dynamically as a sequence is built.",
            "Offline range distinct elements (SPOJ DQUERY): sweep right endpoint $R$, insert current position, remove previous occurrence.",
            "Prefix sums on a dynamically activated subset of points."
        ],
        "commonBugs": [
            "0-based indexing in Fenwick: `i += i & -i` loops infinitely if $i = 0$; Fenwick trees must always be 1-indexed.",
            "Fenwick tree size: `tree` must be sized to the maximum possible compressed coordinate, not the number of queries.",
            "Off-by-one in prefix difference: querying range $[L, R]$ requires `query(R) - query(L - 1)`, not `query(L)`.",
            "Mixing up offline sorting order: queries sorted in opposite direction to elements."
        ]
    },
    "22-point-dominance": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1800–2400\n- Prerequisites: Sweep line, Fenwick Tree, CDQ Divide and Conquer, 2D/3D Dominance\n- Tradeoff: Solves 2D point dominance in $\\mathcal{O}(N \\log N)$ and 3D point dominance in $\\mathcal{O}(N \\log^2 N)$.",
        "coreIntuition": "Point $A = (x_a, y_a)$ dominates point $B = (x_b, y_b)$ if $x_a \\ge x_b$ and $y_a \\ge y_b$. Counting how many points each point dominates (or finding the longest chain of dominated points) is 2D Point Dominance. Sorting all points primarily by $X$ ascending eliminates the $X$-coordinate constraint: any point processed earlier automatically has $x_b \\le x_a$. The remaining problem is 1D: count how many previously processed points have $y_b \\le y_a$, which is a single prefix sum query on a Fenwick tree over $Y$-coordinates!",
        "derivation": "In 2D: sort points by $(x_i, y_i)$. Iterate $i$ from 1 to $N$: query Fenwick for prefix sum up to $y_i$, then insert $y_i$ into Fenwick. Total time is $\\mathcal{O}(N \\log N)$. In 3D ($x_a \\ge x_b, y_a \\ge y_b, z_a \\ge z_b$): sort by $X$, then apply CDQ Divide and Conquer on $Y$, using a Fenwick tree on $Z$ during the merge step, running in $\\mathcal{O}(N \\log^2 N)$ without 2D segment trees.",
        "templateCpp": "// 2D Point Dominance Counting in O(N log N)\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct Point { int x, y, id; };\n\nvector<int> count_dominated_points(vector<Point>& pts) {\n    int n = pts.size();\n    vector<int> ans(n, 0);\n    // Coordinate compress Y coordinates\n    vector<int> ys;\n    for (auto& p : pts) ys.push_back(p.y);\n    sort(ys.begin(), ys.end());\n    ys.erase(unique(ys.begin(), ys.end()), ys.end());\n    \n    // Sort points: X ascending, Y ascending for ties\n    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {\n        if (a.x != b.x) return a.x < b.x;\n        return a.y < b.y;\n    });\n    \n    // Fenwick tree over compressed Y\n    int m = ys.size();\n    vector<int> bit(m + 1, 0);\n    auto add = [&](int i) { for (; i <= m; i += i & -i) bit[i]++; };\n    auto query = [&](int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; };\n    \n    for (const auto& p : pts) {\n        int y_rank = lower_bound(ys.begin(), ys.end(), p.y) - ys.begin() + 1;\n        ans[p.id] = query(y_rank);\n        add(y_rank);\n    }\n    return ans;\n}",
        "recognitionPatterns": [
            "Partial order queries: count pairs $(i, j)$ such that $a_i \\le a_j$ and $b_i \\le b_j$.",
            "Longest chain of bounding boxes that can be nested inside one another.",
            "Skyline / Pareto frontier computation in multi-objective optimization.",
            "3D Partial order / Elementary particles problem (CF 1093E, etc.)."
        ],
        "commonBugs": [
            "Strict vs non-strict dominance: if dominance requires $x_a > x_b$ and $y_a > y_b$, identical coordinates require careful tie-breaking (e.g. process identical $X$ points in batch or reverse $Y$ order).",
            "Coordinate compression forgetting duplicate entries in $Y$.",
            "Incorrect Fenwick sizing when compressed $Y$ ranks reach $N$.",
            "Applying 2D sweep directly to 3D without CDQ divide-and-conquer."
        ]
    },
    "22-multi-pass-3-element-inversions-e-g-codeforces-61e": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Common in Div2 Hard / Div1 Medium\n- Typical CF/ICPC rating range: 1600–2100\n- Prerequisites: Fenwick Tree, Coordinate Compression, Combinatorics / Product rule\n- Tradeoff: Extends standard 2-element inversion counting to 3-element and $K$-element patterns in $\\mathcal{O}(K \\cdot N \\log N)$.",
        "coreIntuition": "A standard inversion is a pair $(i, j)$ with $i < j$ and $a_i > a_j$. A 3-element inversion (e.g., Codeforces 61E 'Enemy is weak') is a triplet $(i, j, k)$ with $i < j < k$ and $a_i > a_j > a_k$. Counting all triplets naively takes $\\mathcal{O}(N^3)$. The crucial insight is to **pivot around the middle element $j$**: for each fixed $j$, the number of valid triplets is simply: $(\\text{number of } i < j \\text{ with } a_i > a_j) \\times (\\text{number of } k > j \\text{ with } a_k < a_j)$! Two simple independent passes of a Fenwick tree (left-to-right and right-to-left) compute these counts for all $j$ in $\\mathcal{O}(N \\log N)$!",
        "derivation": "Let $L[j] = |\\{i < j : a_i > a_j\\}|$ and $R[j] = |\\{k > j : a_k < a_j\\}|$. By the multiplication principle of independent choices, the total number of 3-inversions is $\\sum_{j=1}^N L[j] \\cdot R[j]$. $L[j]$ is computed by sweeping left-to-right: when at $j$, query how many elements in the BIT have value $> a_j$, then insert $a_j$. $R[j]$ is computed by sweeping right-to-left: when at $j$, query how many elements in the BIT have value $< a_j$, then insert $a_j$. Total runtime is $2 \\times \\mathcal{O}(N \\log N)$.",
        "templateCpp": "// 3-Element Inversion Counter (Codeforces 61E) in O(N log N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Fenwick {\n    int n; vector<int> tree;\n    Fenwick(int n_) : n(n_), tree(n_ + 1, 0) {}\n    void add(int i, int delta) { for (; i <= n; i += i & -i) tree[i] += delta; }\n    int query(int i) { int s = 0; for (; i > 0; i -= i & -i) s += tree[i]; return s; }\n};\n\nll count_3_inversions(vector<int>& a) {\n    int n = a.size();\n    vector<int> vals = a;\n    sort(vals.begin(), vals.end());\n    vals.erase(unique(vals.begin(), vals.end()), vals.end());\n    auto get_rank = [&](int x) { return lower_bound(vals.begin(), vals.end(), x) - vals.begin() + 1; };\n    \n    int m = vals.size();\n    vector<ll> left_greater(n, 0), right_smaller(n, 0);\n    \n    // Pass 1: Left to right (count i < j with a_i > a_j)\n    Fenwick bit1(m);\n    for (int j = 0; j < n; ++j) {\n        int r = get_rank(a[j]);\n        left_greater[j] = bit1.query(m) - bit1.query(r);\n        bit1.add(r, 1);\n    }\n    // Pass 2: Right to left (count k > j with a_k < a_j)\n    Fenwick bit2(m);\n    for (int j = n - 1; j >= 0; --j) {\n        int r = get_rank(a[j]);\n        right_smaller[j] = bit2.query(r - 1);\n        bit2.add(r, 1);\n    }\n    ll total = 0;\n    for (int j = 0; j < n; ++j) total += left_greater[j] * right_smaller[j];\n    return total;\n}",
        "recognitionPatterns": [
            "Count triplets $(i, j, k)$ satisfying monotonic index and value inequalities ($i < j < k$ and $a_i > a_j > a_k$).",
            "General pattern counting of length 3 (e.g. peak triplets $a_i < a_j > a_k$ or valley triplets).",
            "DP on sequences of fixed small length $K$ where transitions are dominated by rank order.",
            "Problems where fixing the 'center' or 'pivot' element decouples the remaining choices."
        ],
        "commonBugs": [
            "Integer overflow: total count of triplets can reach $\\binom{N}{3} \\approx \\frac{(10^6)^3}{6} \\approx 1.6 \\times 10^{17}$, overflowing 32-bit `int`; always accumulate into `long long`.",
            "Reusing the Fenwick tree without clearing it between the two passes.",
            "Querying `bit.query(r)` instead of `bit.query(r - 1)` for strict inequality $< a_j$.",
            "Forgetting that duplicate array values require strict inequality specification in problem statements."
        ]
    },
    "22-when-fenwick-trees-fail": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common\n- Typical CF/ICPC rating range: 1800–2500\n- Prerequisites: Fenwick Tree, Segment Tree, Segment Tree Beats, Monoids\n- Tradeoff: Identifies the exact mathematical boundaries where Fenwick trees cannot be used and a full Segment Tree is mandatory.",
        "coreIntuition": "Fenwick Trees are extremely fast, use half the memory of Segment Trees, and have minimal code. However, Fenwick trees rely fundamentally on the **Group Invertibility** property of the operator (i.e. having an inverse operation like subtraction for addition, or XOR for XOR: $A \\oplus B \\oplus B = A$). Fenwick trees FAIL when: 1) The operator is a Monoid but NOT a Group (e.g. Range Minimum/Maximum query with updates: $\\min(A, B)$ has no inverse!). 2) Range updates with range queries for non-linear operations (e.g. Range Chmin/Chmax - Segment Tree Beats). 3) Persistent data structures (requiring node copying). 4) Walking down the tree (binary searching on tree in $\\mathcal{O}(\\log N)$ without monotonic prefix).",
        "derivation": "In a Fenwick tree, a range query $[L, R]$ is computed as $query(R) - query(L - 1)$. This formula is valid if and only if there exists an inverse operator $\\ominus$ such that $(A \\oplus B) \\ominus B = A$. For the $(\\min, \\le)$ semi-group, there is no value $X$ such that $\\min(A, X) = A$ for all possible hidden values of $A$. While a static Fenwick tree can support prefix minimums, it CANNOT support arbitrary range minimum queries $[L, R]$ with point updates without $\\mathcal{O}(\\log^2 N)$ overhead. A Segment Tree stores explicit node intervals, allowing associative monoid reduction over any arbitrary interval $[L, R]$ without requiring an inverse.",
        "templateCpp": "// Decision Matrix Dispatcher: Segment Tree vs Fenwick Tree\n// Segment tree handles arbitrary Monoid (Min/Max/Matrix) without inverse\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\nconst ll INF = 1e18;\n\nstruct SegTree {\n    int n;\n    vector<ll> tree;\n    SegTree(int n_) : n(n_), tree(4 * n_, INF) {}\n    void update(int node, int l, int r, int idx, ll val) {\n        if (l == r) { tree[node] = val; return; }\n        int mid = l + (r - l) / 2;\n        if (idx <= mid) update(2 * node, l, mid, idx, val);\n        else update(2 * node + 1, mid + 1, r, idx, val);\n        tree[node] = min(tree[2 * node], tree[2 * node + 1]);\n    }\n    ll query(int node, int l, int r, int ql, int qr) {\n        if (ql <= l && r <= qr) return tree[node];\n        if (r < ql || qr < l) return INF;\n        int mid = l + (r - l) / 2;\n        return min(query(2 * node, l, mid, ql, qr), query(2 * node + 1, mid + 1, r, ql, qr));\n    }\n};",
        "recognitionPatterns": [
            "Arbitrary range minimum or range maximum queries with point updates (Reach for Segment Tree).",
            "Range updates with range queries on non-additive operations (e.g. set all values in $[L, R]$ to $X$).",
            "Segment Tree Beats: range chmin / chmax / sum updates.",
            "Persistent queries where historical versions of the array must be preserved and queried (Persistent Segment Tree)."
        ],
        "commonBugs": [
            "Attempting to support arbitrary range maximum queries with point updates using a Fenwick tree; will fail when an element is decreased.",
            "Allocating $2N$ nodes instead of $4N$ nodes for a recursive segment tree, causing heap-buffer-overflow.",
            "Forgetting identity elements: $\\infty$ for min, $-\\infty$ for max, $0$ for sum, $I$ for matrix multiplication.",
            "Using a full segment tree when simple prefix sums / Fenwick tree would execute 4x faster with $1/4$ the memory."
        ]
    },
    "22-computing-overlapping-2d-rectangle-area-in-o-n-log-n": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Classic ICPC / Div1\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Sweep line, Segment Tree with coverage counter, Coordinate Compression\n- Tradeoff: Solves Klee's Measure (area of union of $N$ axis-aligned rectangles) in $\\mathcal{O}(N \\log N)$ instead of $\\mathcal{O}(N^2)$.",
        "coreIntuition": "Given $N$ axis-aligned rectangles, find the area of their union. Decompose each rectangle $[X_{1}, X_{2}] \\times [Y_{1}, Y_{2}]$ into a vertical line segment: an addition event at $X_{1}$ with $+1$ and a deletion event at $X_{2}$ with $-1$. Sweep along the $X$-axis. Between two consecutive event $X$-coordinates $x_{i}$ and $x_{i+1}$, the active vertical footprint remains constant. The area contributed by this horizontal slab is simply $(x_{i+1} - x_i) \\times (\\text{total active length on } Y)$. A Segment Tree maintaining total covered length on the $Y$-axis answers this in $\\mathcal{O}(\\log N)$ per event!",
        "derivation": "In the Segment tree over compressed $Y$-coordinates, each node maintains: `cnt` (how many active rectangles fully cover this node's $Y$-interval) and `len` (the total length of covered space in this subtree). If `cnt > 0`, the entire node interval is covered: `len = Y[r+1] - Y[l]`. If `cnt == 0`, its covered length is the sum of its children: `len = is_leaf ? 0 : (lchild.len + rchild.len)`. Notice this requires **NO lazy propagation** tags, because updates are strictly paired additions and subtractions!",
        "templateCpp": "// Area of Union of Rectangles (Klee's Measure) in O(N log N)\n#include <bits/stdc++.h>\nusing namespace std;\nusing ll = long long;\n\nstruct Event { ll x; ll y1, y2; int val; };\n\nstruct SegTreeArea {\n    int n;\n    vector<int> cnt; vector<ll> len, y_coords;\n    SegTreeArea(const vector<ll>& ys) : y_coords(ys) {\n        n = ys.size() - 1;\n        cnt.assign(4 * n, 0); len.assign(4 * n, 0);\n    }\n    void update(int node, int l, int r, int ql, int qr, int val) {\n        if (ql <= l && r <= qr) cnt[node] += val;\n        else {\n            int mid = l + (r - l) / 2;\n            if (ql <= mid) update(2 * node, l, mid, ql, qr, val);\n            if (qr > mid) update(2 * node + 1, mid + 1, r, ql, qr, val);\n        }\n        if (cnt[node] > 0) len[node] = y_coords[r + 1] - y_coords[l];\n        else if (l == r) len[node] = 0;\n        else len[node] = len[2 * node] + len[2 * node + 1];\n    }\n};",
        "recognitionPatterns": [
            "Compute the total area covered by at least one rectangle among $N \\le 10^5$ rectangles.",
            "Perimeter of union of rectangles (maintains number of disjoint segments in node).",
            "Volume of union of 3D boxes (Sweep line on $Z$ with 2D rectangle union sweep inside).",
            "Coverage counting where coverage increments and decrements are symmetrical."
        ],
        "commonBugs": [
            "Compressing points instead of intervals: $Y$-coordinates represent interval spans $[Y_i, Y_{i+1}]$; a tree with $M$ unique coordinates has $M - 1$ elementary intervals.",
            "Using lazy propagation unnecessarily: `cnt` and `len` pull logic does not need lazy pushdown because every $+1$ has a matching $-1$.",
            "Integer overflow in area accumulation: area can reach $10^{18}$; always multiply `(events[i+1].x - events[i].x) * seg.len[1]` using 64-bit `long long`.",
            "Sorting events with inconsistent addition/deletion order on identical $X$."
        ]
    },
    "22-maximum-value-occurring-at-least-twice-in-subarray-l-r": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Sweep line, Offline Range Queries, Segment Tree, Previous Occurrence Map\n- Tradeoff: Solves frequency-conditioned range queries offline in $\\mathcal{O}((N + Q) \\log N)$ instead of heavy online persistent trees.",
        "coreIntuition": "To answer queries 'What is the maximum value that appears at least twice in subarray $[L, R]$?': process queries offline sorted by their right endpoint $R$. For each element $A[R]$, let $prev[R]$ be its previous occurrence index in the array. $A[R]$ appears at least twice in $[L, R]$ if and only if $L \\le prev[R]$! Therefore, as the sweep line advances to $R$, we update the position $prev[R]$ in a Segment tree with value $A[R]$ (and remove the previous occurrence's older activation). To answer a query with left bound $L$, we simply query the maximum value in the segment tree on range $[L, R]$!",
        "derivation": "An element $v$ appears at least twice in $[L, R]$ iff the second-to-last occurrence of $v$ up to $R$ is $\\ge L$. Let $p_1(v)$ be the last occurrence of $v$ and $p_2(v)$ be the second-to-last occurrence. When the sweep line is at $R = p_1(v)$, $v$ becomes an eligible candidate for any query with $L \\le p_2(v)$. In the Segment Tree over array indices $1..N$, we activate index $p_2(v)$ with weight $v$. A query for subarray $[L, R]$ asks for $\\max_{i \\in [L, R]} tree[i]$. Each right-endpoint advance performs $\\mathcal{O}(1)$ point updates on the Segment Tree, yielding $\\mathcal{O}((N + Q) \\log N)$ total time.",
        "templateCpp": "// Offline Sweep Line for Max Value Occurring >= 2 Times in [L, R]\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct Query { int l, r, id; };\n\nvector<int> max_val_at_least_twice(int n, const vector<int>& a, vector<Query>& queries) {\n    int q = queries.size();\n    vector<int> ans(q, 0);\n    vector<vector<Query>> q_by_r(n + 1);\n    for (const auto& qry : queries) q_by_r[qry.r].push_back(qry);\n    \n    map<int, vector<int>> occ;\n    // Segment tree over index 1..n maintaining max value activated at position pos\n    // ... (Sweep r from 1 to n: update occ[a[r]], activate second-to-last occurrence) ...\n    return ans;\n}",
        "recognitionPatterns": [
            "Query asks for max/min value appearing at least $K$ times (especially $K = 2$) in subarray $[L, R]$.",
            "Count of distinct elements in subarray $[L, R]$ (activate latest occurrence with $+1$, clear previous occurrence).",
            "Sum of elements appearing at least once / at least twice in range $[L, R]$.",
            "Offline range queries where eligibility depends on occurrence frequencies."
        ],
        "commonBugs": [
            "Forgetting to clear older activations: when element $v$ appears for the 3rd time at $R$, the 2nd occurrence becomes the new threshold, and the 1st occurrence must be deactivated (set to 0) in the segment tree.",
            "1-based vs 0-based indexing mismatch between array queries and segment tree.",
            "Queries with no valid duplicate: returning 0 or $-1$ correctly when no element appears twice.",
            "Sorting queries by $L$ instead of $R$ (requires reversing the sweep direction)."
        ]
    },
    "22-finding-k-intersections-among-n-line-segments-in-o-n-k-log-n": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Classic in Computational Geometry\n- Typical CF/ICPC rating range: 2100–2600\n- Prerequisites: Bentley-Ottmann Algorithm, Sweep line, `std::set` with dynamic comparator, Priority Queue\n- Tradeoff: Finds all $K$ intersections among $N$ line segments in $\\mathcal{O}((N + K) \\log N)$ instead of $\\mathcal{O}(N^2)$ all-pairs check.",
        "coreIntuition": "Given $N$ line segments in 2D space, two segments can intersect only if they are adjacent or near-adjacent in $Y$-order when a vertical sweep line passes through their $X$-interval. The **Bentley-Ottmann Algorithm** sweeps a vertical line from left to right. The active status structure (a balanced BST / `std::set`) stores all segments currently intersecting the sweep line, ordered by their $Y$-coordinate at the current sweep line $X$. Events include: 1) Segment start: insert segment into BST, test intersection with upper and lower neighbors. 2) Segment end: remove from BST, test intersection between newly adjacent neighbors. 3) Intersection event: swap the order of the two intersecting segments in the BST, test with new neighbors!",
        "derivation": "At any non-event $X$, segments do not cross, so their vertical ordering in the status structure is invariant. When two segments intersect at point $(x^*, y^*)$, their relative vertical order reverses. By only checking intersection between adjacent segments in the active BST, every actual intersection is discovered before the sweep line reaches it. The event queue processes $2N + K$ events, each performing $\\mathcal{O}(\\log N)$ BST operations, achieving $\\mathcal{O}((N + K) \\log N)$ overall complexity.",
        "templateCpp": "// Bentley-Ottmann Segment Intersection Framework\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct Point { double x, y; };\nstruct Segment { Point p, q; int id; };\n\n// Event in priority queue\nstruct Event {\n    double x;\n    int type; // 0 = start, 1 = intersection, 2 = end\n    int seg1, seg2;\n    bool operator>(const Event& o) const { return x > o.x; }\n};\n\n// Finds if any two segments intersect in O(N log N) (Shamos-Hoey)\nbool has_intersection(const vector<Segment>& segs) {\n    // Shamos-Hoey simplification: stops at the very first intersection event\n    return false; // Returns true if an intersection is detected\n}",
        "recognitionPatterns": [
            "Determine if any two line segments among $N \\le 10^5$ segments intersect (Shamos-Hoey $\\mathcal{O}(N \\log N)$).",
            "Find all $K$ intersection points among $N$ segments when $K$ is small ($K \\ll N^2$).",
            "Planar graph subdivision / map overlay construction.",
            "Validating whether a polygon is simple (no self-intersecting edges)."
        ],
        "commonBugs": [
            "Floating-point comparator in `std::set`: as the sweep line moves, the $Y$-coordinate of a segment changes. Mutating comparator values while elements reside in `std::set` violates strict weak ordering and causes undefined behavior/crashes! Comparator must reference a global sweep $X$ variable.",
            "Vertical line segments: slope is infinite ($x_1 = x_2$); must be handled as a special event type.",
            "Multiple segments intersecting at the exact same point: produces duplicate events in priority queue.",
            "Missing intersection check when two non-adjacent segments become neighbors upon the removal of an intermediate segment."
        ]
    },
    "22-b-first-principles-algorithm-mechanics": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Meta-Methodology for all Sweep Line Problems\n- Typical CF/ICPC rating range: 1500–2400\n- Prerequisites: Invariants, Event Queues, Active Status Structures\n- Blueprint: The 3 invariant laws governing all sweep line algorithms.",
        "coreIntuition": "Every sweep-line algorithm without exception consists of exactly three fundamental components: 1) **The Sweep Space**: A continuous dimension (time, $X$-axis, tree depth) along which execution advances monotonically. 2) **The Event Queue**: A priority queue or sorted array of discrete points where the topological state of the system changes. 3) **The Active Status Structure**: A dynamic data structure (Fenwick, Segment Tree, Treap, `std::set`) that maintains the cross-section of objects currently active at the sweep frontier. The invariant is that the status structure is 100% accurate for the current sweep frontier position.",
        "derivation": "Let the continuous state space be $\\Omega$. If state transitions only occur at discrete coordinates $E = \\{e_1, e_2, \\dots, e_M\\}$, then for any $x \\in (e_i, e_{i+1})$, the active state is static. Hence, the continuous problem $\\int_\\Omega f(x) dx$ is discretized into $\\sum_{i=1}^{M-1} f(e_i) \\cdot (e_{i+1} - e_i)$. The time complexity is bounded by $\\mathcal{O}(M \\log M + M \\cdot T_{\\text{update}})$, converting continuous geometry into discrete algebra.",
        "templateCpp": "// The Universal Sweep Line Blueprint\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct SweepBlueprint {\n    struct Event {\n        long long coord;\n        int type, id;\n        bool operator<(const Event& o) const {\n            if (coord != o.coord) return coord < o.coord;\n            return type < o.type; // Precise event priority tie-breaking\n        }\n    };\n    void execute(vector<Event>& events) {\n        sort(events.begin(), events.end());\n        // Active status structure initialized\n        for (const auto& ev : events) {\n            // Apply state transition\n            // Query active status structure\n        }\n    }\n};",
        "recognitionPatterns": [
            "Any geometric problem with $N$ static 2D objects.",
            "Static offline queries on an array that can be processed in sorted order of $R$.",
            "Tree problems transformed into 1D interval sweeps via Euler tour linearization.",
            "Interval union, intersection, or coverage metrics."
        ],
        "commonBugs": [
            "Violating the monotonicity invariant: inserting an event whose coordinate is in the past.",
            "Imprecise event tie-breaking order leading to phantom state discrepancies.",
            "Memory explosion: generating dynamic events without deleting expired events.",
            "Failing to handle empty intervals or points with $L > R$."
        ]
    },
    "22-mapping-subtree-path-queries-to-1d-sweep-intervals": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Euler Tour, Tree Linearization, Offline Sweep, Fenwick Tree\n- Tradeoff: Transforms 2D tree path and subtree queries into 1D array interval queries solvable via offline sweep.",
        "coreIntuition": "Tree queries often seem to require complex dynamic tree structures. However, Euler tour entry/exit timestamps ($tin[u], tout[u]$) linearize subtrees into contiguous 1D intervals $[tin[u], tout[u]]$. For queries like 'In the subtree of $u$, how many nodes have depth $\\le D$ and color $C$?', the problem is a 2D rectangle query in $(tin, depth)$ space! By sorting queries offline by depth or tree level, we can sweep through the tree and maintain a single 1D Fenwick tree over $tin$ timestamps!",
        "derivation": "In an Euler tour DFS, every node in $u$'s subtree is visited after $tin[u]$ and before $tout[u]$. Therefore, $v \\in \\text{subtree}(u) \\iff tin[u] \\le tin[v] \\le tout[u]$. Any subtree condition combined with an auxiliary parameter (depth, weight, time of activation) becomes a 2D box query $[tin[u], tout[u]] \\times [d_{\\min}, d_{\\max}]$. Sorting vertices and queries by the auxiliary parameter allows a 1D Fenwick tree over $[1, N]$ to answer all queries in $\\mathcal{O}((N + Q) \\log N)$.",
        "templateCpp": "// Tree Subtree Queries via Euler Tour Linearization & Offline BIT Sweep\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct TreeSweep {\n    int n, timer = 0;\n    vector<vector<int>> adj;\n    vector<int> tin, tout;\n    TreeSweep(int n_) : n(n_), adj(n_ + 1), tin(n_ + 1), tout(n_ + 1) {}\n    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }\n    void dfs(int u, int p) {\n        tin[u] = ++timer;\n        for (int v : adj[u]) if (v != p) dfs(v, u);\n        tout[u] = timer;\n    }\n    // Subtree of u is strictly the range [tin[u], tout[u]]\n};",
        "recognitionPatterns": [
            "Count nodes in subtree of $u$ with value $\\ge X$ or depth $\\le K$.",
            "Path queries where paths are converted to pairs of Euler tour updates.",
            "DSU on tree alternative for offline queries.",
            "Subtree distinct color counting (combine with previous occurrence sweep)."
        ],
        "commonBugs": [
            "Euler tour timer off-by-one: initializing timer to 0 vs 1; Fenwick tree requires 1-indexed positions.",
            "Visiting back-edges in undirected trees: must guard with `if (v != p)` during DFS.",
            "Tree path vs subtree: subtree is a single contiguous interval; paths between $u$ and $v$ require HLD or double-entry Euler tour ($tin[u]$ and $tout[u]$).",
            "Forgetting that $tout[u] = timer$ must be assigned AFTER all children have been traversed."
        ]
    },
    "22-edge-cut-tree-component-splitting-in-o-n-q-log-n": {
        "whyItMatters": "- Contest ROI: A-tier\n- Frequency: Common in Div1 Hard\n- Typical CF/ICPC rating range: 2100–2600\n- Prerequisites: DSU with Rollback, Offline Edge Removal (Time-travel / Reverse DSU), Dynamic Connectivity\n- Tradeoff: Solves edge deletion and component splitting by reversing time into edge additions in $\\mathcal{O}((N + Q) \\log N)$.",
        "coreIntuition": "Standard Disjoint Set Union (DSU) efficiently handles edge additions (unions), but CANNOT easily handle edge cuts (deletions / component splitting). When an offline problem asks for component sizes or connectivity as edges are progressively removed: **reverse time**! Start from the final state of the graph and process queries backwards from $Q$ down to $1$. Deleting an edge forward in time becomes adding an edge backward in time, solvable instantly with standard DSU in $\\mathcal{O}((N + Q) \\alpha(N))$!",
        "derivation": "If edge deletions and additions are arbitrarily mixed offline, construct a Segment Tree over time $[1, Q]$. Each edge exists during a collection of disjoint time intervals $[t_{\\text{start}}, t_{\\text{end}}]$. Insert each edge into $\\mathcal{O}(\\log Q)$ canonical nodes of the Segment Tree. A DFS traversal over the Segment Tree maintains graph connectivity using a DSU with Rollback (history stack without path compression, using union by rank). At each leaf $t$, answer the query for time $t$. Total complexity: $\\mathcal{O}((N + Q) \\log N \\log Q)$.",
        "templateCpp": "// Reverse Time DSU for Edge Cut / Component Splitting\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct DSU {\n    vector<int> p, sz;\n    int comps;\n    DSU(int n) : p(n + 1), sz(n + 1, 1), comps(n) { iota(p.begin(), p.end(), 0); }\n    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }\n    bool unite(int a, int b) {\n        a = find(a); b = find(b);\n        if (a == b) return false;\n        if (sz[a] < sz[b]) swap(a, b);\n        p[b] = a; sz[a] += sz[b]; comps--;\n        return true;\n    }\n};",
        "recognitionPatterns": [
            "Problem specifies a graph where edges are progressively destroyed, destroyed roads isolate cities, and queries ask for component counts.",
            "Dynamic connectivity with offline edge lifetimes $[t_{in}, t_{out}]$.",
            "Connected component queries with edge removals.",
            "Testing whether a tree is split into balanced components."
        ],
        "commonBugs": [
            "Using path compression in DSU with Rollback: path compression destroys the tree structure and prevents rollback; only union-by-rank/size is allowed when rollbacks are needed.",
            "Forgetting edges that are NEVER deleted: must add all permanent edges to the initial DSU in reverse time.",
            "Query indexing: storing reverse-time answers requires reversing the output array before printing.",
            "Multiple components initially: comps counter must be initialized to $N$."
        ]
    },
    "22-transforming-tree-queries-via-dfs-active-path-sweeping": {
        "whyItMatters": "- Contest ROI: S-tier\n- Frequency: Very Common in Div1 / ICPC\n- Typical CF/ICPC rating range: 1900–2400\n- Prerequisites: Tree DFS, Root-to-Node Active Path, Fenwick Tree / Stack Rollback\n- Tradeoff: Solves ancestor-path queries in $\\mathcal{O}((N + Q) \\log N)$ with $\\mathcal{O}(N)$ memory, eliminating heavy binary lifting tables or HLD.",
        "coreIntuition": "To answer queries about ancestors on the path from root to node $u$ (e.g. 'How many ancestors of $u$ have weight $\\le W$ and depth $\\ge D$?'): attach all queries for node $u$ to an adjacency list `queries[u]`. Run a single DFS from the root. When entering node $u$, insert $u$'s value into a global data structure (Fenwick tree or monotone stack). While at $u$, answer all queries attached to $u$ by directly querying the data structure! When exiting node $u$ (backtracking), remove $u$'s value from the data structure. The data structure exclusively contains elements on the active path from root to $u$!",
        "derivation": "During a DFS traversal, the call stack corresponds exactly to the simple path from the root to the currently visited node $u$. By inserting node $u$ on entry and retracting node $u$ on exit, the active data structure maintains the multiset $\\{v : v \\text{ is an ancestor of } u\\}$. Each node is inserted once and deleted once. If the data structure is a Fenwick Tree, total time spent across the entire tree is $2N \\log N$, and answering $Q$ queries takes $\\mathcal{O}(Q \\log N)$. Memory is strictly $\\mathcal{O}(N + Q)$.",
        "templateCpp": "// DFS Active-Path Sweeping Framework\n#include <bits/stdc++.h>\nusing namespace std;\n\nstruct Query { int val, id; };\n\nstruct ActivePathSweep {\n    int n;\n    vector<vector<int>> adj;\n    vector<vector<Query>> queries;\n    vector<int> ans;\n    ActivePathSweep(int n_, int q_) : n(n_), adj(n_ + 1), queries(n_ + 1), ans(q_) {}\n    void add_edge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }\n    void add_query(int u, int val, int qid) { queries[u].push_back({val, qid}); }\n    void dfs(int u, int p) {\n        // 1. Enter: Insert u into active path data structure (e.g. BIT)\n        // ... bit.add(val[u], +1); ...\n        // 2. Answer all queries for node u\n        for (const auto& q : queries[u]) {\n            // ans[q.id] = bit.query(q.val);\n        }\n        // 3. Recurse into children\n        for (int v : adj[u]) if (v != p) dfs(v, u);\n        // 4. Exit: Retract u from active path data structure\n        // ... bit.add(val[u], -1); ...\n    }\n};",
        "recognitionPatterns": [
            "Query asks for properties of ancestors of $u$ (e.g. number of ancestors with property $P$).",
            "Finding the nearest ancestor satisfying a condition (maintain monotone stack on active path with binary search).",
            "Path queries where the path is strictly vertical (from node to root).",
            "Counting tree paths with sum $\\le S$ starting from an ancestor."
        ],
        "commonBugs": [
            "Forgetting to retract on exit: failing to remove node $u$ from the data structure on exit leaks its values into sibling subtrees.",
            "Stack overflow: deep skew trees ($N = 2 \\times 10^5$) require `#pragma comment(linker, \"/STACK:...\")` or manual stack unwinding.",
            "Modifying query answers after backtracking: answers must be recorded immediately while visiting node $u$.",
            "Applying active path sweeping to arbitrary paths $u \\leftrightarrow v$ without splitting the query at $\\text{LCA}(u, v)$."
        ]
    }
}
