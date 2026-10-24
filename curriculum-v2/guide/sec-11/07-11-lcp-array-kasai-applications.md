# LCP Array (Kasai) + Applications

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** suffix array  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: suffix array

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

`lcp[i]` = length of longest common prefix of suffixes `sa[i]` and `sa[i-1]` (define `lcp[0] = 0`). Adjacent-in-SA LCP is enough because for any two suffixes, LCP equals the **minimum** LCP on the SA-interval between them (RMQ).

**Kasai’s algorithm** computes LCP in O(n) given SA and the inverse `rank[sa[i]] = i`: walk suffixes in text order `i = 0..n-1`; the LCP of suffix `i` with its SA-predecessor is at least `h-1` if suffix `i-1` had height `h`—so decrement `h` at most once per step and extend.

**Why LCP unlocks SA power:**
- Number of distinct substrings = `n(n+1)/2 - Σ lcp[i]`
- Longest repeated substring = max `lcp[i]`
- Occurrence count of a pattern = size of SA range where suffixes share prefix |P|
- LCS of two strings = max LCP among adjacent SA pairs that come from different strings

---

## 4. Proof Sketches & Recurrences

Let `rank[sa[i]] = i`.  
Set `k = 0`. For `i = 0..n-1`:
- If `rank[i] == 0`, `lcp[0] = 0`, continue (or set and skip).
- `j = sa[rank[i] - 1]`
- While `i+k < n && j+k < n && s[i+k] == s[j+k]`: `k++`
- `lcp[rank[i]] = k`
- If `k > 0`: `k--`

**Amortized O(n):** `k` increases ≤ n times total; decreases ≤ n times.

**RMQ:** sparse table on `lcp` → LCP of any two suffixes in O(1).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) Kasai + O(n log n) sparse table
- Per-query / per-operation: O(1) LCP of any two suffixes with RMQ
- Total: O(n) after SA
- Memory: O(n)`

### C++17 Template

```cpp
namespace lcp {
vector<int> kasai(const string& s, const vector<int>& sa) {
    int n = (int)s.size();
    vector<int> rankv(n), lcp(n);
    for (int i = 0; i < n; i++) rankv[sa[i]] = i;
    for (int i = 0, k = 0; i < n; i++) {
        if (rankv[i] == 0) { k = 0; continue; }
        int j = sa[rankv[i] - 1];
        while (i + k < n && j + k < n && s[i + k] == s[j + k]) k++;
        lcp[rankv[i]] = k;
        if (k) k--;
    }
    return lcp; // lcp[i] = LCP(sa[i], sa[i-1])
}

long long count_distinct_substrings(int n, const vector<int>& lcp) {
    long long total = 1LL * n * (n + 1) / 2;
    for (int i = 1; i < n; i++) total -= lcp[i];
    return total;
}

int longest_repeated_substring_len(const vector<int>& lcp) {
    return lcp.empty() ? 0 : *max_element(lcp.begin(), lcp.end());
}
} // namespace lcp
```

### Python 3 Template

```python
# Practical only with small n, or if SA already built and n moderate.

def kasai(s: str, sa: list[int]) -> list[int]:
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    k = 0
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue
        j = sa[rank[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1
    return lcp
```

---

## 6. Recognition Trigger Signals & Heuristics

- Anything “count distinct substrings / unique occurrences”
- Longest duplicated substring
- k-th lexicographic substring (walk SA accumulating `n - sa[i] - lcp[i]` new strings)
- Match statistics needing RMQ on LCP
- After you built SA, almost always build LCP next

---

## 7. Contest WA / TLE / RE Traps

- `lcp` indexing: some codes store `lcp[i] = LCP(sa[i], sa[i+1])` — pick a convention
- Forgetting `k--` → still correct but O(n²)
- Distinct substring formula wrong if sentinel still in SA
- RMQ off-by-one: LCP(sa[a], sa[b]) = min on `(min(a,b)+1 .. max(a,b))` under `lcp[i]=LCP(sa[i],sa[i-1])`
- Mixing lengths of A and B in concat LCS problems (ignore LCP across separator only… actually take max where owners differ)

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

- **Phi / PLCP** variants of Kasai
- **LCP of pattern vs SA range** during binary search (accelerated matching)
- **Histogram / stack on LCP** for “number of substrings appearing ≥ k times”
- **Diff array on SA ranges** for occurrence tagging

---

## 11. Typical Problem Archetypes

1. Standard application: distinct substrings; longest repeated substring
2. Slightly disguised: k-th lex substring; shared substrings of two strings
3. Difficult: count pairs of substrings with LCP constraints; stack on LCP histogram
4. Very difficult / advanced: string borders statistics; match to multiple texts with color on SA

---

## 12. Recognition & Identification Drills

1. Count distinct substrings of s.
2. Find any longest substring that occurs at least twice.
3. Find LCS length of two strings via SA+LCP of a concatenation.

---

## 13. Fast-Lookup Cheat Sheet

- When to use: always pair with SA for counting / repeated / LCS-of-two
- Key invariant: Kasai height decreases by at most 1 when moving to next text position
- Key formula: distinct = n(n+1)/2 − Σ lcp
- Complexity: O(n) LCP
- Template to remember: `rank`, walk i in text order, extend, `k--`

---

## 8. Suffix Automaton

---
