# Suffix Tree (Conceptual — Lower Early ROI)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** suffix array + LCP, or Ukkonen intuition; most contest tasks solvable without explicit tree  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: suffix array + LCP, or Ukkonen intuition; most contest tasks solvable without explicit tree

---

## 2. Theoretical Deep-Dive & Mathematical Mechanics

### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

## 3. Core Intuition & Problem Framing

A **suffix tree** is a compressed trie of all suffixes: edges labeled with substrings (or `(l,r)` index pairs into s), internal nodes = branching, O(n) nodes/edges with compression.

**Contest reality:** building Ukkonen correctly under time pressure is high-variance. Almost every CF/ICPC use-case is covered by:
- **SA + LCP (+ RMQ)** ≈ suffix tree’s lexicographic and LCP structure
- **SAM** ≈ suffix tree’s “substring automaton / endpos” view (SAM is the compressed DAWG; suffix tree is the tree)

Learn **concepts** so papers/editorials make sense; implement tree only when an editorial forces node-explicit DP that is painful on SA.

**Useful mental maps:**
- LCP-adjacent values ↔ depths of LCA-like structure between consecutive leaves in SA order
- Suffix link in tree: from node for `cX` to node for `X`
- Explicit tree DP: sometimes cleaner for “path labeled queries” but rare

---

## 4. Proof Sketches & Recurrences

**From SA+LCP (cartesian / stack construction):** process SA left to right; maintain stack of LCP depths to build a tree whose leaves are suffixes in order and internal node depths are LCPs—this is the **suffix tree / LCP tree** in O(n). This is the practical “construction” if you truly need nodes.

**Ukkonen (sketch):** online, all suffixes implicit via active point; open transitions; suffix links between internal nodes; O(n) with careful edge representation. Easy to get wrong.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) Ukkonen / O(n) from SA+LCP
- Per-query / per-operation: O(|P|) walk
- Total: O(n + queries)
- Memory: O(n)`

### C++17 Template

```cpp
namespace suffix_tree_from_lcp {
// Build explicit tree from SA + LCP (parent[leaf], depth). Enough for many "tree DP" needs.
struct Node {
    int parent = -1;
    int depth = 0;   // string depth
    int l = -1, r = -1; // optional edge label s[l..r)
    vector<int> child;
};
// Stack construction of LCP cartesian tree over SA order — sketch:
vector<Node> build(const string& s, const vector<int>& sa, const vector<int>& lcp) {
    // Full robust implementations are long; prefer SA/SAM for contests.
    // If needed: create leaves for each sa[i], create internal nodes when lcp decreases,
    // using a stack of (node, depth). See competitive programming literature "suffix tree via SA".
    return {};
}
} // namespace suffix_tree_from_lcp
```

---

## 6. Recognition Trigger Signals & Heuristics

- Editorial mentions Ukkonen / “build suffix tree”
- Need explicit branching nodes with edge labels as intervals
- Research-olympiad stringology; rarely modern CF Div.1 easy/medium

---

## 7. Contest WA / TLE / RE Traps

- Edge label index errors; off-by-one on half-open intervals
- Missing suffix links in Ukkonen
- Treating uncompressed trie as tree → O(n²) memory

---

## 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

## 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

## 10. Algorithmic Variants & Advanced Extensions

- **Generalized suffix tree** for multiple strings
- **Compact vs Patricia**
- **Suffix link tree vs transition DAG (SAM)**

---

## 11. Typical Problem Archetypes

1. Standard application: textbook pattern matching via tree walk
2. Slightly disguised: longest repeated via deepest internal node
3. Difficult: tree DP on explicit nodes
4. Very difficult / advanced: research-level stringology

---

## 12. Recognition & Identification Drills

1. Explain how max LCP relates to deepest internal node in the suffix tree.
2. Given SA and LCP, describe how to build the compressed trie structure with a stack.
3. Name two contest problems usually solved with SAM/SA that textbooks solve with suffix trees.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: rarely; prefer SA+LCP or SAM
- Key invariant: compressed trie of suffixes; O(n) size
- Key formula: internal node string-depth ↔ LCP structure
- Complexity: O(n) build in theory
- Template to remember: “don’t implement Ukkonen unless necessary; map to SA/SAM”

---

## 10. Palindromic Tree / Eertree

---
