# 1. KMP / Prefix Function

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** strings, arrays, basic loops; no automata theory required  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: strings, arrays, basic loops; no automata theory required

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

The **prefix function** `π[i]` for string `s` (0-indexed) is the longest proper prefix of `s[0..i]` that is also a suffix of `s[0..i]`. “Proper” means strictly shorter than `i+1`.

KMP is not “search with a DFA you build by hand.” It is: compute how much of the pattern you have matched so far; on a mismatch, jump to the longest border that could still be valid, without re-examining characters you already know match.

Borders compose: if `π[i] = k` and you mismatch at `i+1`, the next candidate border length is `π[k-1]` (then `π[π[k-1]-1]`, …). That chain is why the amortized cost is linear: each index of the text is advanced at most once, and the border pointer only decreases.

Classic pattern search builds `π` on `pattern + '#' + text` (or runs the automaton online): occurrences are positions where the matched length equals `|pattern|`.

---

## 4. Proof Sketches & Recurrences

Define `π[0] = 0`. For `i ≥ 1`, let `j = π[i-1]`. While `j > 0` and `s[i] ≠ s[j]`, set `j = π[j-1]`. Then `π[i] = j+1` if `s[i] == s[j]`, else `0`.

**Amortized O(n):** consider potential `Φ = j` (current border length). Each successful match increments `i` and increases `j` by 1. Each failed comparison strictly decreases `j` along the π-chain. Over the whole run, total decreases ≤ total increases ≤ n, so total while-loop iterations are O(n).

**Period fact:** the smallest period of `s[0..i]` is `i+1 - π[i]` if that divides the length appropriately; for the whole string `s` of length `n`, if `n % (n - π[n-1]) == 0`, then the minimal period is `n - π[n-1]`.

**KMP automaton:** states `0..m` (matched length). Transition `δ(j, c)` = length after reading `c` from state `j`. Can be precomputed in O(m·Σ) or computed on the fly with π.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(|P|) for π on pattern; O(|P|+|T|) for concatenate method
- Per-query / per-operation: O(1) amortized per character online
- Total: O(|P|+|T|) time
- Memory: O(|P|) or O(|P|+|T|)`

### C++17 Template

```cpp
// C++17, namespace-safe, contest-ready
namespace kmp {
vector<int> prefix_function(const string& s) {
    int n = (int)s.size();
    vector<int> pi(n);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

// all start indices of pattern in text
vector<int> find_occurrences(const string& text, const string& pat) {
    if (pat.empty()) return {};
    string cur = pat + '#' + text; // '#' must not appear in alphabet; use '\0' carefully
    auto pi = prefix_function(cur);
    vector<int> occ;
    int m = (int)pat.size();
    for (int i = m + 1; i < (int)cur.size(); i++)
        if (pi[i] == m) occ.push_back(i - 2 * m);
    return occ;
}

// online automaton: after building pi on pattern only
int go(const vector<int>& pi, const string& pat, int j, char c) {
    while (j > 0 && (j == (int)pat.size() || c != pat[j])) j = pi[j - 1];
    if (j < (int)pat.size() && c == pat[j]) j++;
    return j;
}
} // namespace kmp
```

### Python 3 Template

```python
def prefix_function(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def find_occurrences(text: str, pat: str) -> list[int]:
    if not pat:
        return []
    cur = pat + "#" + text
    pi = prefix_function(cur)
    m = len(pat)
    return [i - 2 * m for i in range(m + 1, len(cur)) if pi[i] == m]
```

---

## 6. Recognition Trigger Signals & Heuristics

- “Find all occurrences of pattern in text” with `|P|+|T| ≤ 1e6–1e7` and exact match
- “Shortest period / border / cyclic shift” of a string
- “String is periodic with period `p`” ↔ `n % p == 0` and `π[n-1] == n-p` (for the full string)
- Compress / count distinct borders; longest proper border chain
- Match with “failure links” without building a full Aho trie (single pattern)
- Offline: concatenate with separators and read `π` peaks

---

## 7. Contest WA / TLE / RE Traps

- Using a separator that appears in the alphabet → false matches across the join
- Off-by-one on occurrence index (`i - 2*m` vs `i - m - m`)
- Forgetting “proper” prefix: π[i] < i+1 always; do not allow full-string self-match as border incorrectly in period checks
- Building O(m·Σ) automaton with wrong failure fallback (must follow π, not reset to 0 blindly when Σ transitions missing)
- Assuming π gives *minimal* period without the divisibility check

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

- **Count occurrences / first only:** stop at first `pi[i]==m` or count peaks
- **Border set:** repeatedly `j = pi[j-1]` from `pi[n-1]` lists all border lengths
- **Cyclic matching:** search `P` in `T+T` (length 2n−1) for rotations
- **KMP on integers / tokens:** same code; equality on alphabet symbols
- **Autocorrelation / string covering:** periods from π; Z-function often cleaner for “match at every offset”

---

## 11. Typical Problem Archetypes

1. Standard application: find all occurrences of P in T
2. Slightly disguised: shortest string with given π, or reconstruct from π constraints
3. Difficult: count distinct substrings via borders; string compression by period; match with wildcards reduced to two KMPs / hashes
4. Very difficult / advanced: multiple patterns still forced into KMP+trie ideas → usually Aho; π on huge concatenations with careful separators

---

## 12. Recognition & Identification Drills

1. Given s, find the shortest string t such that s is a prefix of t+t+… (minimal period cover).
2. You are given π for an unknown string over {a,b}; decide if any string realizes it.
3. Count how many prefixes of s are also suffixes of s (including the full string or excluding—read carefully).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: single-pattern exact match; periods/borders; linear string scanning with failure links
- Key invariant: π[i] = longest border of prefix i+1; mismatches jump via π
- Key formula: minimal period candidate `p = n - π[n-1]`; period iff `n % p == 0`
- Complexity: O(n) preprocess / search
- Template to remember: while-shrink `j = pi[j-1]`, then extend if equal

---

## 2. Z-function

---
