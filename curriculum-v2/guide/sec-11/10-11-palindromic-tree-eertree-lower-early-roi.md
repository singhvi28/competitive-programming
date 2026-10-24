# 10. Palindromic Tree (Eertree) — Lower Early ROI

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** palindrome radii intuition (Manacher); automata/suffix-link comfort  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: palindrome radii intuition (Manacher); automata/suffix-link comfort

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

The **eertree** stores all **distinct** palindromic substrings of s in O(n) nodes. Two roots: even empty palindrome (length 0) and odd “−1” imaginary. Each node is a distinct palindrome; edges add a character on both sides; **suffix link** points to the longest proper palindromic suffix.

Online: when appending `s[i]`, start from the node of the longest palindromic suffix of `s[0..i-1]`, walk suffix links until `s[i - len - 1] == s[i]`, then possibly create a new node.

**Manacher vs eertree:**
- Manacher: all centers’ radii (occurrences / geometry of palindromes), O(n)
- Eertree: **distinct** palindromes as nodes + links; occurrence counts; DP on palindromes
- If you only need longest or count occurrences of palindromic substrings, Manacher (or hash) wins on ROI
- If you need “how many distinct palindromes” or DP over distinct palindrome nodes, eertree shines

**Early ROI:** skip until Manacher/hash/SAM are solid. Marked **lower early ROI** on purpose.

---

## 4. Proof Sketches & Recurrences

Nodes ≤ n + 2. For append at i:
- Let `v` be last = longest palindromic suffix before add.
- While `i - st[v].len - 1 < 0` or `s[i - st[v].len - 1] != s[i]`, `v = link[v]`.
- If transition `s[i]` from `v` exists, last = that child (palindrome already known); else create node with `len = st[v].len + 2`, set suffix link by continuing from `link[v]`, etc.

Occurrence: increment count on `last` each time; propagate via suffix links or as needed.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing / build: O(n) amortized
- Per-query / per-operation: O(1) amortized per append
- Total: O(n)
- Memory: O(n · σ)`

### C++17 Template

```cpp
namespace eertree {
struct Eertree {
    static constexpr int SIG = 26;
    struct Node {
        int next[SIG];
        int link = 0, len = 0;
        long long cnt = 0;
        Node() { fill(next, next + SIG, -1); }
    };
    vector<Node> st;
    string s;
    int last = 0;

    Eertree() {
        st.push_back(Node()); // 0: len 0 even root, link 1
        st.push_back(Node()); // 1: len -1 odd root, link 1
        st[0].link = 1;
        st[1].link = 1;
        st[0].len = 0;
        st[1].len = -1;
        last = 0;
    }

    void add(char ch) {
        int c = ch - 'a';
        int pos = (int)s.size();
        s.push_back(ch);
        int p = last;
        while (true) {
            int L = st[p].len;
            if (pos - L - 1 >= 0 && s[pos - L - 1] == ch) break;
            p = st[p].link;
        }
        if (st[p].next[c] != -1) {
            last = st[p].next[c];
            st[last].cnt++;
            return;
        }
        int cur = (int)st.size();
        st.push_back(Node());
        st[cur].len = st[p].len + 2;
        st[p].next[c] = cur;
        if (st[cur].len == 1) {
            st[cur].link = 0;
        } else {
            int q = st[p].link;
            while (true) {
                int L = st[q].len;
                if (pos - L - 1 >= 0 && s[pos - L - 1] == ch) break;
                q = st[q].link;
            }
            st[cur].link = st[q].next[c];
        }
        last = cur;
        st[cur].cnt = 1;
    }

    long long distinct_palindromes() const {
        return (long long)st.size() - 2;
    }
};
} // namespace eertree
```

### Python 3 Template

```python
# OK for learning / n ≤ ~1e5 if careful; still niche. Prefer C++ when TL tight.

class Eertree:
    def __init__(self, sigma: int = 26):
        self.sigma = sigma
        self.next = [[-1] * sigma for _ in range(2)]
        self.link = [1, 1]
        self.length = [0, -1]
        self.cnt = [0, 0]
        self.last = 0
        self.s = []

    def add(self, ch: str) -> None:
        c = ord(ch) - 97
        pos = len(self.s)
        self.s.append(ch)
        p = self.last
        while True:
            L = self.length[p]
            if pos - L - 1 >= 0 and self.s[pos - L - 1] == ch:
                break
            p = self.link[p]
        if self.next[p][c] != -1:
            self.last = self.next[p][c]
            self.cnt[self.last] += 1
            return
        cur = len(self.next)
        self.next.append([-1] * self.sigma)
        self.link.append(0)
        self.length.append(self.length[p] + 2)
        self.cnt.append(1)
        self.next[p][c] = cur
        if self.length[cur] == 1:
            self.link[cur] = 0
        else:
            q = self.link[p]
            while True:
                L = self.length[q]
                if pos - L - 1 >= 0 and self.s[pos - L - 1] == ch:
                    break
                q = self.link[q]
            self.link[cur] = self.next[q][c]
        self.last = cur
```

---

## 6. Recognition Trigger Signals & Heuristics

- Count **distinct** palindromic substrings
- DP where states are distinct palindromes
- Problems explicitly mentioning palindromic tree / eertree in blogs
- Frequency of each distinct palindrome

---

## 7. Contest WA / TLE / RE Traps

- Wrong odd/even roots (`len = -1` node essential)
- Suffix link for length-1 must go to even root 0
- Forgetting to increment cnt on already-existing node
- Walking links without bounds check on `pos - L - 1`
- Confusing distinct count with Manacher occurrence count

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

- **Series links / quick links** for faster DP (advanced)
- **Eertree + DP** on last palindrome suffix partitions
- **Count occurrences** via cnt propagate along links

---

## 11. Typical Problem Archetypes

1. Standard application: number of distinct palindromic substrings
2. Slightly disguised: sum of frequencies of distinct palindromes
3. Difficult: palindrome partition DP accelerated by eertree links
4. Very difficult / advanced: series links, digraph of palindromes

---

## 12. Recognition & Identification Drills

1. Count distinct palindromic substrings of s (n ≤ 1e5).
2. Compare your answer to Manacher-based occurrence count on `"aaa"` vs `"aba"` — explain the difference.
3. Maintain distinct palindrome count online under append-only.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: distinct palindromes / DP on palindrome nodes — else Manacher/hash
- Key invariant: ≤ n distinct palindromes; suffix = longest palindromic suffix link
- Key formula: nodes = distinct pals; online append with link walks
- Complexity: O(n)
- Template to remember: two roots (−1 and 0), create node len+2, set link

---

## 11. Which Problems Each Algorithm Solves — Synthesis

---
