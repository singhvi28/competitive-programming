# Suffix Automaton (SAM)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** automata intuition; optional SA familiarity (different model)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: automata intuition; optional SA familiarity (different model)

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

The **suffix automaton** of s is the minimal DFA that recognizes exactly the set of suffixes of s (and as a byproduct, all substrings are paths from the start state). It has ≤ 2n−1 states and ≤ 3n−4 transitions for length n ≥ 3.

Each state represents an **endpos-equivalence class**: set of substrings that end at the same set of positions. A state stores `len` (longest string in the class) and `link` (suffix link) to the state of the longest proper suffix in a different class. Strings in a state have lengths `(len(link)+1 .. len)`.

**Online construction:** append characters one by one; clone states when needed (the famous “clone” step). This is why SAM is so contest-friendly for “all substrings” problems: after build, DP on DAG of transitions or on suffix-link tree.

**SAM vs SA:**
- SAM: excellent for “number of distinct substrings”, “first occurrence”, “continue reading online”, automaton DP, endpos sizes
- SA+LCP: excellent for lex order, k-th substring, RMQ between suffixes, some occurrence-interval problems
- Overlap large; pick the structure that matches the query shape

---

## 4. Proof Sketches & Recurrences

States: `0` = initial. For each state: `next[c]`, `link`, `len`.

`extend(c)` with `last` = state of whole current string:
1. Create `cur` with `len = len[last]+1`.
2. From `p = last`, while `p ≠ -1` and no `next[p][c]`, set `next[p][c] = cur`, `p = link[p]`.
3. If `p == -1`: `link[cur] = 0`.
4. Else `q = next[p][c]`. If `len[p]+1 == len[q]`: `link[cur] = q`.
5. Else clone `q` into `clone` with `len = len[p]+1`, copy transitions & link; set `link[q] = link[cur] = clone`; while `p ≠ -1` and `next[p][c] == q`, redirect to `clone`.

**Distinct substrings:** each state contributes `len[v] - len[link[v]]` distinct strings.

**Occurrences:** let `cnt[v]` = 1 for non-clone created as `cur` when extending (endpos grows); 0 for clone. Propagate `cnt` up suffix links in decreasing `len` order: `cnt[link[v]] += cnt[v]`. Then occurrences of strings represented by `v` = `cnt[v]`.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n · σ) time with arrays; O(n) amortized with maps (worse constants)
- Per-query / per-operation: O(|P|) run pattern; O(#states) DP
- Total: linear in practice for fixed σ
- Memory: O(n · σ)`

### C++17 Template

```cpp
namespace sam {
struct SAM {
    static constexpr int SIG = 26;
    struct State {
        int next[SIG];
        int link = -1, len = 0;
        long long occ = 0; // endpos size after propagate
        State() { fill(next, next + SIG, -1); }
    };
    vector<State> st;
    int last = 0;

    SAM(int maxlen = 0) {
        st.reserve(2 * maxlen + 5);
        st.push_back(State());
    }

    void extend(int c) {
        int cur = (int)st.size();
        st.push_back(State());
        st[cur].len = st[last].len + 1;
        st[cur].occ = 1; // real end
        int p = last;
        while (p != -1 && st[p].next[c] == -1) {
            st[p].next[c] = cur;
            p = st[p].link;
        }
        if (p == -1) {
            st[cur].link = 0;
        } else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) {
                st[cur].link = q;
            } else {
                int cl = (int)st.size();
                st.push_back(st[q]); // copy transitions, link
                st[cl].len = st[p].len + 1;
                st[cl].occ = 0; // clone
                while (p != -1 && st[p].next[c] == q) {
                    st[p].next[c] = cl;
                    p = st[p].link;
                }
                st[q].link = st[cur].link = cl;
            }
        }
        last = cur;
    }

    void build(const string& s) {
        for (char ch : s) extend(ch - 'a');
    }

    void propagate_occ() {
        vector<int> order(st.size());
        iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b) { return st[a].len > st[b].len; });
        for (int v : order)
            if (st[v].link >= 0) st[st[v].link].occ += st[v].occ;
    }

    long long distinct_substrings() const {
        long long ans = 0;
        for (int v = 1; v < (int)st.size(); v++)
            ans += st[v].len - st[st[v].link].len;
        return ans;
    }
};
} // namespace sam
```

### Python 3 Template

```python
# Python often TLE for n ≥ 1e5 (constant-heavy). Prefer C++ in contests.

class SAM:
    __slots__ = ("next", "link", "length", "occ", "last")

    def __init__(self, sigma: int = 26):
        self.next = [{}]  # list of dicts for flexible alphabet
        self.link = [-1]
        self.length = [0]
        self.occ = [0]
        self.last = 0

    def extend(self, c: int) -> None:
        cur = len(self.next)
        self.next.append({})
        self.link.append(-1)
        self.length.append(self.length[self.last] + 1)
        self.occ.append(1)
        p = self.last
        while p != -1 and c not in self.next[p]:
            self.next[p][c] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                cl = len(self.next)
                self.next.append(self.next[q].copy())
                self.link.append(self.link[q])
                self.length.append(self.length[p] + 1)
                self.occ.append(0)
                while p != -1 and self.next[p].get(c) == q:
                    self.next[p][c] = cl
                    p = self.link[p]
                self.link[q] = self.link[cur] = cl
        self.last = cur
```

---

## 6. Recognition Trigger Signals & Heuristics

- Number of distinct substrings (Σ over states `len - len(link)`)
- Occurrences of each substring / endpos size DP
- Longest substring occurring ≥ k times
- Shortest non-appearing string over alphabet
- Online: process stream, maintain SAM of text so far
- Pattern matching: run pattern on SAM of text
- Multiple strings: generalized SAM / trie of SAMs / concat with separators carefully

---

## 7. Contest WA / TLE / RE Traps

- Forgetting `occ[clone] = 0` and `occ[cur] = 1` → wrong occurrence counts
- Propagating occ without sorting by decreasing length
- Distinct substrings: starting from state 0 incorrectly; use `len - len(link)` for v≥1
- Redirect loop must only rewrite transitions that still point to `q`
- Using SAM of reverse string when problem wants prefixes vs suffixes—check direction
- Alphabet compression forgotten for large char sets

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

- **SAM of reverse** for prefix structure / palindromes hybrids
- **Generalized SAM** for multiple words
- **DP on DAG:** longest path, count paths = substrings through states
- **Fail/suffix-link tree** as real tree for subtree occ sums
- **Minimum cyclic shift** via SAM tricks / Duval; often Lyndon or SA simpler

---

## 11. Typical Problem Archetypes

1. Standard application: count distinct substrings
2. Slightly disguised: total length of distinct substrings; first occurrence position
3. Difficult: lexicographic DFS on SAM for k-th substring; occurrence ≥ k longest
4. Very difficult / advanced: SAM + segtree on endpos; dynamic strings; matching statistics

---

## 12. Recognition & Identification Drills

1. Compute the number of distinct substrings of s.
2. Find the longest substring that appears at least twice.
3. Find the shortest string over `{a,b}` that is not a substring of s.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: substring set as automaton; distinct count; occurrence via endpos; online append
- Key invariant: endpos equivalence; suffix links
- Key formula: distinct += len[v] − len[link[v]]
- Complexity: O(n) states/transitions order
- Template to remember: extend with possible clone + redirect

---

## 9. Suffix Tree Concepts

---
