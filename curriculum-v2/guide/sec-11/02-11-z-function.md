# Z-function

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** strings; optional familiarity with KMP borders  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: strings; optional familiarity with KMP borders

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

`Z[i]` = length of the longest substring starting at `i` that matches a prefix of `s`. `Z[0]` is usually left unused or defined as 0 / n by convention—pick one and stick to it (contest code often sets `Z[0] = 0` and never reads it).

Maintain the rightmost Z-box `[l, r]` (substring `s[l..r]` matches `s[0..r-l]`). For `i ≤ r`, you already know `Z[i-l]` from the prefix mirror; you can copy `min(Z[i-l], r-i+1)` and only extend past `r` when needed. That is the same “don’t re-compare known matches” idea as KMP, but the array answers a different question: **match length at every alignment with the prefix**, not border of every prefix.

KMP π answers “border of prefix ending at i.” Z answers “how much prefix matches starting at i.” Many period / occurrence problems are one line with Z and awkward with π (and vice versa).

---

## 4. Proof Sketches & Recurrences

Initialize `l = r = 0`. For `i = 1..n-1`:
- If `i ≤ r`, set `Z[i] = min(r - i + 1, Z[i - l])`.
- While `i + Z[i] < n` and `s[Z[i]] == s[i + Z[i]]`, increment `Z[i]`.
- If `i + Z[i] - 1 > r`, set `l = i`, `r = i + Z[i] - 1`.

**Correctness of the copy:** `s[l..r] = s[0..r-l]`, so `s[i..r] = s[i-l..r-l]`. The known match length from the prefix at offset `i-l` is `Z[i-l]`, but you cannot claim past `r`, hence the `min`.

**Amortized O(n):** each successful character comparison advances `r`. `r` never decreases; failed comparisons are O(1) per i outside extensions. Total O(n).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) to compute Z
- Per-query / per-operation: O(1) read of Z[i]
- Total: O(|P|+|T|) for search via concatenation
- Memory: O(n)`

### C++17 Template

```cpp
namespace zfunc {
vector<int> z_function(const string& s) {
    int n = (int)s.size();
    vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) l = i, r = i + z[i] - 1;
    }
    return z;
}

vector<int> find_occurrences(const string& text, const string& pat) {
    if (pat.empty()) return {};
    string cur = pat + '#' + text;
    auto z = z_function(cur);
    vector<int> occ;
    int m = (int)pat.size();
    for (int i = m + 1; i < (int)cur.size(); i++)
        if (z[i] == m) occ.push_back(i - m - 1);
    return occ;
}
} // namespace zfunc
```

### Python 3 Template

```python
def z_function(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z
```

---

## 6. Recognition Trigger Signals & Heuristics

- Occurrences of pattern: build `P + '#' + T`, then `Z[i] == |P|` for matches
- “String matches its prefix at position i” / self-matches / autocorrelation
- Cubes, squares, runs often start from Z-boxes or Z on carefully built strings
- Compare “is T[i..] prefix-related to P” without hashing
- When you need **all** prefix-match lengths, Z is more direct than π

---

## 7. Contest WA / TLE / RE Traps

- Forgetting separator in `P+'#'+T` → Z runs across the boundary
- Using `Z[0] = n` accidentally in sums (double-count / overflow); many problems want `Z[0]` excluded
- Off-by-one: occurrence start is `i - |P| - 1` for concat form
- Extending while-loop without updating `[l,r]` → TLE (loses linear guarantee)
- Confusing Z with π: `π[i]` is about prefix *ending* at i; `Z[i]` about prefix *starting* at i

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

- **Z on integers:** same
- **Reverse Z:** Z on `reverse(s)` for suffix–prefix style facts
- **Two strings:** Z on `A+'#'+B` gives, for each start in B, LCP with A
- **Minimal period:** smallest `p` with `Z[p] = n-p` (and related checks)
- **Excludant / match tables** for stringology olympiad problems

---

## 11. Typical Problem Archetypes

1. Standard application: pattern matching via Z
2. Slightly disguised: number of distinct prefixes that occur at position i; compressibility
3. Difficult: count pairs (i,j) with s[i..]==s[j..] prefix constraints; squares via Z
4. Very difficult / advanced: run enumeration / Lyndon-related tools (often beyond CF Div.2)

---

## 12. Recognition & Identification Drills

1. Find all starting positions where the suffix equals a prefix of length ≥ k.
2. Check whether s is a power t^k for k≥2.
3. For each prefix length L, count how many times that prefix occurs in s as a substring (overlapping allowed).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need match lengths of the prefix at every index; often cleaner than KMP for “how much matches here”
- Key invariant: Z-box `[l,r]` is the rightmost known prefix match
- Key formula: inside box, `Z[i] ≥ min(Z[i-l], r-i+1)` before extending
- Complexity: O(n)
- Template to remember: copy from box, extend, update `[l,r]`

---

## 3. Rolling Hash

---
