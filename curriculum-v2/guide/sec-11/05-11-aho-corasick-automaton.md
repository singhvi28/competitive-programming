# Aho-Corasick Automaton

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** trie, KMP failure links intuition  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: trie, KMP failure links intuition

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

Aho-Corasick = **trie of all patterns** + **failure links** (KMP-style borders on the trie) + **output/dictionary links**.

Failure link of node `v` points to the longest proper suffix of the string represented by `v` that is still a trie node (prefix of some pattern). Output link jumps to the next node that corresponds to an actual pattern end (skipping empty fail chain).

Reading the text once: from state `u`, on char `c` follow transition (build via BFS: missing edges go to `fail`’s transition). At each state, report all patterns ending here by walking output links.

**vs multi KMP:** |patterns| separate KMPs is O(|T|·Σ patterns) worst in naive multi-scan, or awkward. AC is O(|T| + sum |P_i| + occurrences) with careful output handling.

**vs SA:** SA can find all pattern occurrences via binary search per pattern; AC is better when many patterns stream online or you need automaton DP (“how many ways to build string avoiding patterns”).

---

## 4. Proof Sketches & Recurrences

1. Insert all patterns into a trie; mark `out[v]` with pattern indices ending at `v`.
2. BFS from root: for root’s children, `fail = root`. For node `v` with parent edge `c`, `fail[v] = go(fail[parent], c)` (KMP jump).
3. `go(v,c)`: if transition exists use it; else follow fail until possible (memoize as full transitions during BFS).
4. `dict_link[v] = out[fail[v]] ? fail[v] : dict_link[fail[v]]` (skip to next output).

**Complexity:** building O(Σ |P_i| · σ) if you fill all alphabet transitions, or alphabet-map / dynamic. Matching O(|T| + total reported occurrences) if you walk dict links carefully (can be O(|T|·answers)).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(Σ|P_i| · σ) with filled transitions
- Per-query / per-operation: O(|T|) transitions + O(occurrences) reporting
- Total: linear in input + outputs (watch output merging)
- Memory: O(Σ|P_i| · σ)`

### C++17 Template

```cpp
namespace aho {
struct AC {
    static constexpr int SIG = 26;
    struct Node {
        int next[SIG];
        int link = 0;
        int out = -1;      // last pattern index ending here, or -1
        int dict = -1;     // next output node
        int pch = 0;
        int p = -1;
        Node() { fill(next, next + SIG, -1); }
    };
    vector<Node> t;
    vector<vector<int>> pats_at; // all pattern ids at node

    AC() { t.push_back(Node()); pats_at.push_back({}); }

    int add(const string& s, int id) {
        int v = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (t[v].next[c] < 0) {
                t[v].next[c] = (int)t.size();
                t.push_back(Node());
                pats_at.push_back({});
                t.back().p = v;
                t.back().pch = c;
            }
            v = t[v].next[c];
        }
        pats_at[v].push_back(id);
        t[v].out = id;
        return v;
    }

    void build() {
        queue<int> q;
        for (int c = 0; c < SIG; c++) {
            int u = t[0].next[c];
            if (u >= 0) {
                t[u].link = 0;
                q.push(u);
            } else t[0].next[c] = 0; // missing → stay/root sink
        }
        while (!q.empty()) {
            int v = q.front(); q.pop();
            int f = t[v].link;
            t[v].dict = !pats_at[f].empty() ? f : t[f].dict;
            for (int c = 0; c < SIG; c++) {
                int u = t[v].next[c];
                if (u >= 0) {
                    t[u].link = t[f].next[c];
                    q.push(u);
                } else {
                    t[v].next[c] = t[f].next[c];
                }
            }
        }
    }

    // returns list of (pattern_id, end_position_in_text_inclusive)
    vector<pair<int,int>> search(const string& text) {
        vector<pair<int,int>> res;
        int v = 0;
        for (int i = 0; i < (int)text.size(); i++) {
            int c = text[i] - 'a';
            v = t[v].next[c];
            for (int u = v; u != -1; u = t[u].dict)
                for (int id : pats_at[u]) res.push_back({id, i});
        }
        return res;
    }
};
} // namespace aho
```

### Python 3 Template

```python
# Usable for moderate sizes; large σ·states or huge occurrence dumps → prefer C++.

from collections import deque

class AhoCorasick:
    def __init__(self, sigma: int = 26):
        self.sigma = sigma
        self.next = [[-1] * sigma]
        self.link = [0]
        self.out = [[]]  # pattern ids

    def add(self, s: str, idx: int) -> None:
        v = 0
        for ch in s:
            c = ord(ch) - 97
            if self.next[v][c] < 0:
                self.next[v][c] = len(self.next)
                self.next.append([-1] * self.sigma)
                self.link.append(0)
                self.out.append([])
            v = self.next[v][c]
        self.out[v].append(idx)

    def build(self) -> None:
        q = deque()
        for c in range(self.sigma):
            u = self.next[0][c]
            if u >= 0:
                self.link[u] = 0
                q.append(u)
            else:
                self.next[0][c] = 0
        while q:
            v = q.popleft()
            for c in range(self.sigma):
                u = self.next[v][c]
                if u >= 0:
                    self.link[u] = self.next[self.link[v]][c]
                    self.out[u] += self.out[self.link[u]]  # merge outputs
                    q.append(u)
                else:
                    self.next[v][c] = self.next[self.link[v]][c]
```

---

## 6. Recognition Trigger Signals & Heuristics

- Multiple pattern matching in one text
- “Forbidden words” / virus detection / dictionary hits
- DP on automaton: count strings of length n that avoid a set of patterns
- Replace all dictionary words; highlight matches
- Online streaming match as characters arrive

---

## 7. Contest WA / TLE / RE Traps

- Forgetting to BFS-build fail links before search
- Not filling missing transitions → TLE from fail-walking each step
- Reporting: infinite loop on dict links; missing overlapping matches
- Alphabet assumptions (`'a'..'z'` only) when digits/uppercase appear
- Cloning entire output lists to every fail child → exponential memory
- Root transitions: missing char at root must go to root, not −1

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

- **DP on AC:** `dp[i][state]` after i chars; forbidden if output nonempty
- **Online AC** with incremental pattern adds (harder; usually rebuild)
- **Bitset of matched patterns** per node for small pattern counts
- **Fail tree** as graph: subtree problems on pattern occurrences
- **Binary alphabet / large alphabet:** map / dynamic next

---

## 11. Typical Problem Archetypes

1. Standard application: find which patterns occur in text
2. Slightly disguised: shortest superstring-ish / cover text with dictionary words (DP on AC)
3. Difficult: count distinct matched patterns; minimum deletions to avoid viruses
4. Very difficult / advanced: AC + segment tree on fail tree; dynamic patterns

---

## 12. Recognition & Identification Drills

1. Given k ≤ 1e5 total pattern length and text length 1e6, report for each pattern whether it occurs.
2. Count binary strings of length n that contain none of given forbidden words.
3. Replace every occurrence of any dictionary word by `*` (non-overlapping leftmost longest—policy matters).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: many patterns, one text; automaton DP with dictionary
- Key invariant: fail link = border in the trie; dict link skips to next pattern end
- Key formula: build fails in BFS order; missing edge `next[v][c] = next[fail[v]][c]`
- Complexity: O(|text| + sum |patterns| + occ)
- Template to remember: trie + BFS fail + output/dict links

---

[Back to Section 11 hub](11-string-algorithms.md) · [Continue to 03b](11-b-string-algorithms.md)

---
