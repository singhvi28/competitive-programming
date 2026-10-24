# Section §11: String Algorithms & Automata

> **Module ID:** `sec-11`  
> **Phase:** Phase 6 — String Algorithms  
> **Topic Count:** 15  

**Module Summary:** Rolling hash with anti-hash hygiene, KMP pi-table, Z-algorithm, Manacher palindrome radius, Aho-Corasick automaton, Suffix Array + LCP, and Suffix Automaton (SAM).

---

## Table of Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Individual Guide |
|---|---|---|---|---|---|
| 1 | [KMP / Prefix Function](#topic-1) | `S-tier` | 1400–2000 | Common | [01-11-kmp-prefix-function.md](./01-11-kmp-prefix-function.md) |
| 2 | [Z-function](#topic-2) | `A-tier` | 1400–2000 | Common | [02-11-z-function.md](./02-11-z-function.md) |
| 3 | [Rolling Hash (Polynomial / Rabin–Karp style)](#topic-3) | `S-tier` | 1400–2200 | Very Common | [03-11-rolling-hash-polynomial-rabin-karp-style.md](./03-11-rolling-hash-polynomial-rabin-karp-style.md) |
| 4 | [Manacher’s Algorithm](#topic-4) | `B-tier` | 1700–2300 | Occasional | [04-11-manacher-s-algorithm.md](./04-11-manacher-s-algorithm.md) |
| 5 | [Aho-Corasick Automaton](#topic-5) | `A-tier` | 1800–2400 | Occasional | [05-11-aho-corasick-automaton.md](./05-11-aho-corasick-automaton.md) |
| 6 | [Suffix Array](#topic-6) | `A-tier` | 1900–2600 | Occasional | [06-11-suffix-array.md](./06-11-suffix-array.md) |
| 7 | [LCP Array (Kasai) + Applications](#topic-7) | `A-tier` | 1900–2600 | Occasional | [07-11-lcp-array-kasai-applications.md](./07-11-lcp-array-kasai-applications.md) |
| 8 | [Suffix Automaton (SAM)](#topic-8) | `A-tier` | 2000–2700 | Occasional | [08-11-suffix-automaton-sam.md](./08-11-suffix-automaton-sam.md) |
| 9 | [Suffix Tree (Conceptual — Lower Early ROI)](#topic-9) | `C-tier` | 2200–2800 | Rare | [09-11-suffix-tree-conceptual-lower-early-roi.md](./09-11-suffix-tree-conceptual-lower-early-roi.md) |
| 10 | [Palindromic Tree (Eertree) — Lower Early ROI](#topic-10) | `C-tier` | 2200–2800 | Rare | [10-11-palindromic-tree-eertree-lower-early-roi.md](./10-11-palindromic-tree-eertree-lower-early-roi.md) |
| 11 | [Recognition Matrix + Adapted A–L](#topic-11) | `S-tier (meta-skill)` | 1400–2700 (depends on tool) | Very Common (decides tool choice) | [11-11-recognition-matrix-adapted-a-l.md](./11-11-recognition-matrix-adapted-a-l.md) |
| 12 | [Quick Reference — Algorithm → Problem Class](#topic-12) | `B-tier` | 1600–2200 | Common | [12-11-quick-reference-algorithm-problem-class.md](./12-11-quick-reference-algorithm-problem-class.md) |
| 13 | [High-ROI (drill first)](#topic-13) | `B-tier` | 1600–2200 | Common | [13-11-high-roi-drill-first.md](./13-11-high-roi-drill-first.md) |
| 14 | [Situational (Medium / B-tier)](#topic-14) | `B-tier` | 1600–2200 | Common | [14-11-situational-medium-b-tier.md](./14-11-situational-medium-b-tier.md) |
| 15 | [Rarely worth early / Niche (C-tier)](#topic-15) | `B-tier` | 1600–2200 | Common | [15-11-rarely-worth-early-niche-c-tier.md](./15-11-rarely-worth-early-niche-c-tier.md) |

---

## Complete Section Content Deep-Dives

<a id="topic-1"></a>
### 1. KMP / Prefix Function

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** strings, arrays, basic loops; no automata theory required  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: strings, arrays, basic loops; no automata theory required

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

The **prefix function** `π[i]` for string `s` (0-indexed) is the longest proper prefix of `s[0..i]` that is also a suffix of `s[0..i]`. “Proper” means strictly shorter than `i+1`.

KMP is not “search with a DFA you build by hand.” It is: compute how much of the pattern you have matched so far; on a mismatch, jump to the longest border that could still be valid, without re-examining characters you already know match.

Borders compose: if `π[i] = k` and you mismatch at `i+1`, the next candidate border length is `π[k-1]` (then `π[π[k-1]-1]`, …). That chain is why the amortized cost is linear: each index of the text is advanced at most once, and the border pointer only decreases.

Classic pattern search builds `π` on `pattern + '#' + text` (or runs the automaton online): occurrences are positions where the matched length equals `|pattern|`.

---

#### 4. Proof Sketches & Recurrences

Define `π[0] = 0`. For `i ≥ 1`, let `j = π[i-1]`. While `j > 0` and `s[i] ≠ s[j]`, set `j = π[j-1]`. Then `π[i] = j+1` if `s[i] == s[j]`, else `0`.

**Amortized O(n):** consider potential `Φ = j` (current border length). Each successful match increments `i` and increases `j` by 1. Each failed comparison strictly decreases `j` along the π-chain. Over the whole run, total decreases ≤ total increases ≤ n, so total while-loop iterations are O(n).

**Period fact:** the smallest period of `s[0..i]` is `i+1 - π[i]` if that divides the length appropriately; for the whole string `s` of length `n`, if `n % (n - π[n-1]) == 0`, then the minimal period is `n - π[n-1]`.

**KMP automaton:** states `0..m` (matched length). Transition `δ(j, c)` = length after reading `c` from state `j`. Can be precomputed in O(m·Σ) or computed on the fly with π.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(|P|) for π on pattern; O(|P|+|T|) for concatenate method
- Per-query / per-operation: O(1) amortized per character online
- Total: O(|P|+|T|) time
- Memory: O(|P|) or O(|P|+|T|)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- “Find all occurrences of pattern in text” with `|P|+|T| ≤ 1e6–1e7` and exact match
- “Shortest period / border / cyclic shift” of a string
- “String is periodic with period `p`” ↔ `n % p == 0` and `π[n-1] == n-p` (for the full string)
- Compress / count distinct borders; longest proper border chain
- Match with “failure links” without building a full Aho trie (single pattern)
- Offline: concatenate with separators and read `π` peaks

---

#### 7. Contest WA / TLE / RE Traps

- Using a separator that appears in the alphabet → false matches across the join
- Off-by-one on occurrence index (`i - 2*m` vs `i - m - m`)
- Forgetting “proper” prefix: π[i] < i+1 always; do not allow full-string self-match as border incorrectly in period checks
- Building O(m·Σ) automaton with wrong failure fallback (must follow π, not reset to 0 blindly when Σ transitions missing)
- Assuming π gives *minimal* period without the divisibility check

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Count occurrences / first only:** stop at first `pi[i]==m` or count peaks
- **Border set:** repeatedly `j = pi[j-1]` from `pi[n-1]` lists all border lengths
- **Cyclic matching:** search `P` in `T+T` (length 2n−1) for rotations
- **KMP on integers / tokens:** same code; equality on alphabet symbols
- **Autocorrelation / string covering:** periods from π; Z-function often cleaner for “match at every offset”

---

#### 11. Typical Problem Archetypes

1. Standard application: find all occurrences of P in T
2. Slightly disguised: shortest string with given π, or reconstruct from π constraints
3. Difficult: count distinct substrings via borders; string compression by period; match with wildcards reduced to two KMPs / hashes
4. Very difficult / advanced: multiple patterns still forced into KMP+trie ideas → usually Aho; π on huge concatenations with careful separators

---

#### 12. Recognition & Identification Drills

1. Given s, find the shortest string t such that s is a prefix of t+t+… (minimal period cover).
2. You are given π for an unknown string over {a,b}; decide if any string realizes it.
3. Count how many prefixes of s are also suffixes of s (including the full string or excluding—read carefully).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: single-pattern exact match; periods/borders; linear string scanning with failure links
- Key invariant: π[i] = longest border of prefix i+1; mismatches jump via π
- Key formula: minimal period candidate `p = n - π[n-1]`; period iff `n % p == 0`
- Complexity: O(n) preprocess / search
- Template to remember: while-shrink `j = pi[j-1]`, then extend if equal

---

## 2. Z-function

---


---

<a id="topic-2"></a>
### 2. Z-function

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1400–2000 | **Frequency:** Common  
> **Prerequisites:** strings; optional familiarity with KMP borders  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: strings; optional familiarity with KMP borders

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

`Z[i]` = length of the longest substring starting at `i` that matches a prefix of `s`. `Z[0]` is usually left unused or defined as 0 / n by convention—pick one and stick to it (contest code often sets `Z[0] = 0` and never reads it).

Maintain the rightmost Z-box `[l, r]` (substring `s[l..r]` matches `s[0..r-l]`). For `i ≤ r`, you already know `Z[i-l]` from the prefix mirror; you can copy `min(Z[i-l], r-i+1)` and only extend past `r` when needed. That is the same “don’t re-compare known matches” idea as KMP, but the array answers a different question: **match length at every alignment with the prefix**, not border of every prefix.

KMP π answers “border of prefix ending at i.” Z answers “how much prefix matches starting at i.” Many period / occurrence problems are one line with Z and awkward with π (and vice versa).

---

#### 4. Proof Sketches & Recurrences

Initialize `l = r = 0`. For `i = 1..n-1`:
- If `i ≤ r`, set `Z[i] = min(r - i + 1, Z[i - l])`.
- While `i + Z[i] < n` and `s[Z[i]] == s[i + Z[i]]`, increment `Z[i]`.
- If `i + Z[i] - 1 > r`, set `l = i`, `r = i + Z[i] - 1`.

**Correctness of the copy:** `s[l..r] = s[0..r-l]`, so `s[i..r] = s[i-l..r-l]`. The known match length from the prefix at offset `i-l` is `Z[i-l]`, but you cannot claim past `r`, hence the `min`.

**Amortized O(n):** each successful character comparison advances `r`. `r` never decreases; failed comparisons are O(1) per i outside extensions. Total O(n).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) to compute Z
- Per-query / per-operation: O(1) read of Z[i]
- Total: O(|P|+|T|) for search via concatenation
- Memory: O(n)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Occurrences of pattern: build `P + '#' + T`, then `Z[i] == |P|` for matches
- “String matches its prefix at position i” / self-matches / autocorrelation
- Cubes, squares, runs often start from Z-boxes or Z on carefully built strings
- Compare “is T[i..] prefix-related to P” without hashing
- When you need **all** prefix-match lengths, Z is more direct than π

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting separator in `P+'#'+T` → Z runs across the boundary
- Using `Z[0] = n` accidentally in sums (double-count / overflow); many problems want `Z[0]` excluded
- Off-by-one: occurrence start is `i - |P| - 1` for concat form
- Extending while-loop without updating `[l,r]` → TLE (loses linear guarantee)
- Confusing Z with π: `π[i]` is about prefix *ending* at i; `Z[i]` about prefix *starting* at i

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Z on integers:** same
- **Reverse Z:** Z on `reverse(s)` for suffix–prefix style facts
- **Two strings:** Z on `A+'#'+B` gives, for each start in B, LCP with A
- **Minimal period:** smallest `p` with `Z[p] = n-p` (and related checks)
- **Excludant / match tables** for stringology olympiad problems

---

#### 11. Typical Problem Archetypes

1. Standard application: pattern matching via Z
2. Slightly disguised: number of distinct prefixes that occur at position i; compressibility
3. Difficult: count pairs (i,j) with s[i..]==s[j..] prefix constraints; squares via Z
4. Very difficult / advanced: run enumeration / Lyndon-related tools (often beyond CF Div.2)

---

#### 12. Recognition & Identification Drills

1. Find all starting positions where the suffix equals a prefix of length ≥ k.
2. Check whether s is a power t^k for k≥2.
3. For each prefix length L, count how many times that prefix occurs in s as a substring (overlapping allowed).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need match lengths of the prefix at every index; often cleaner than KMP for “how much matches here”
- Key invariant: Z-box `[l,r]` is the rightmost known prefix match
- Key formula: inside box, `Z[i] ≥ min(Z[i-l], r-i+1)` before extending
- Complexity: O(n)
- Template to remember: copy from box, extend, update `[l,r]`

---

## 3. Rolling Hash

---


---

<a id="topic-3"></a>
### 3. Rolling Hash (Polynomial / Rabin–Karp style)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2200 | **Frequency:** Very Common  
> **Prerequisites:** modular arithmetic, prefix arrays; anti-hash awareness  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2200
- Prerequisites: modular arithmetic, prefix arrays; anti-hash awareness

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Map a string to an integer (or pair of integers) so that equality of substrings becomes equality of hashes in O(1) after O(n) prefix prep:  
`H(s[l..r]) = (pref[r+1] - pref[l] * base^{len}) mod M`.

You trade determinism for speed and flexibility: any substring comparison, LCP via binary search + hash, lexicographic compare, distinct substring counting approximations, 2D hashes, etc.

**Collisions are real.** On CF, single mod `1e9+7` with fixed base is attackable. Prefer: double hash (two mods), random base at runtime, or `mod = 2^64` natural overflow **plus** awareness that it is also breakable in theory—still widely used with random odd base.

---

#### 4. Proof Sketches & Recurrences

Fix base `b` and modulus `M`.  
`pref[0] = 0`, `pref[i+1] = pref[i]*b + s[i]` (map char to 1..σ to avoid leading-zero issues).  
`powb[0] = 1`, `powb[i+1] = powb[i]*b`.

Then `hash(l,r) = pref[r+1] - pref[l]*powb[r-l+1]` (mod M, bring to [0,M)).

**LCP of two suffixes i,j:** binary search maximal L with `hash(i,i+L-1)==hash(j,j+L-1)`.

**Collision probability:** for random hashes, ≈ `#comparisons / M`. Double hash ≈ product of moduli. Adversarial inputs need random base or cryptographic thinking—contests usually stop at double + random base.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n)
- Per-query / per-operation: O(1) substring hash; O(log n) LCP via binary search
- Total: depends on queries; typically O((n+q) log n) for many LCP compares
- Memory: O(n) per hash stream`

##### C++17 Template

```cpp
namespace rhash {
using ull = uint64_t;
// splitmix-ish random base; two 64-bit mods via __int128, or ull overflow + second mod

struct Hashing {
    static constexpr ull mod = (1ull << 61) - 1; // fast prime
    ull base;
    vector<ull> pref, pb;
    static ull add(ull a, ull b) { a += b; if (a >= mod) a -= mod; return a; }
    static ull sub(ull a, ull b) { return a >= b ? a - b : a + mod - b; }
    static ull mul(ull a, ull b) {
        __int128 t = (__int128)a * b;
        t = (t >> 61) + (t & mod);
        if (t >= mod) t -= mod;
        return (ull)t;
    }
    Hashing() {}
    Hashing(const string& s, ull base_ = 0) { init(s, base_); }
    void init(const string& s, ull base_ = 0) {
        mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());
        base = base_ ? base_ : (rng() % (mod - 3) + 2);
        int n = (int)s.size();
        pref.assign(n + 1, 0);
        pb.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            pref[i + 1] = add(mul(pref[i], base), (ull)(s[i] - 'a' + 1));
            pb[i + 1] = mul(pb[i], base);
        }
    }
    ull get(int l, int r) const { // inclusive
        return sub(pref[r + 1], mul(pref[l], pb[r - l + 1]));
    }
};

// double hash for safer equality
struct Hash2 {
    Hashing h1, h2;
    Hash2(const string& s) {
        h1.init(s);
        h2.init(s);
    }
    pair<ull, ull> get(int l, int r) const { return {h1.get(l, r), h2.get(l, r)}; }
};
} // namespace rhash
```

##### Python 3 Template

```python
# Python is OK for n ≤ ~2e5 with simple ops; tight TL / many queries → prefer C++.

class Hashing:
    def __init__(self, s: str, base: int = 911382323, mod: int = 10**9 + 7):
        self.mod = mod
        self.base = base
        n = len(s)
        self.pref = [0] * (n + 1)
        self.pb = [1] * (n + 1)
        for i, ch in enumerate(s):
            self.pref[i + 1] = (self.pref[i] * base + (ord(ch) - 96)) % mod
            self.pb[i + 1] = self.pb[i] * base % mod

    def get(self, l: int, r: int) -> int:  # inclusive
        mod = self.mod
        return (self.pref[r + 1] - self.pref[l] * self.pb[r - l + 1]) % mod

# Prefer two independent (base, mod) pairs in contests.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Substring equality / lexicographic compare under many queries
- Binary search on string length + equality checks (LCP, distinct count, matching)
- Palindrome checks without Manacher: hash(s[l..r]) == hash(reverse[n-1-r..n-1-l])
- “Sort all substrings” / compare cyclic shifts
- When SA/SAM would work but hash is enough and easier to code under time pressure
- Grid / path hashing; tree path hashes with binary lifting

---

#### 7. Contest WA / TLE / RE Traps

- Mapping `'a'→0` causing leading-zero collisions on different lengths (use +1)
- Negative mod after subtraction without fixing
- Same base every run → hackable; forget second modulus
- Comparing hashes of different lengths without length check
- Building `pow` wrong for large n (overflow before mod)
- Using hash as “proof” of inequality direction for sorting without tie-break by real chars when hashes equal

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Reverse hash** for palindromes
- **2D rolling hash** on matrices
- **Hash of multiset** (xor of random per value, or sorted polynomial)—different problem
- **Incremental hash** for sliding window anagrams / Rabin–Karp search
- **Tree / path hash** with binary lifting: hash down + hash up
- **Natural overflow `uint64_t`** single stream (fast; still randomize base)

---

#### 11. Typical Problem Archetypes

1. Standard application: Rabin–Karp find pattern; substring equality queries
2. Slightly disguised: number of distinct substrings O(n²) loop with set of hashes (n≤5e3) or smarter
3. Difficult: lex smallest rotation; compare versions; binary search answer on string score
4. Very difficult / advanced: anti-hash resistant constructions; geometric hashing; heavy double/triple schemes under adversarial judges

---

#### 12. Recognition & Identification Drills

1. q queries: given (l1,r1,l2,r2), test equality of two substrings.
2. Find longest substring that appears at least twice (non-overlapping or overlapping—variants).
3. Count palindromic substrings of even length only, using hashes (no Manacher).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: default hammer for substring equality / lex compare under time pressure
- Key invariant: polynomial prefix structure enables O(1) range hash
- Key formula: `H(l,r) = pref[r+1] - pref[l]*b^{len}`
- Complexity: O(n) prep, O(1) get
- Template to remember: double hash + random base + 1-indexed char map

---

## 4. Manacher

---


---

<a id="topic-4"></a>
### 4. Manacher’s Algorithm

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** strings, palindrome definition; hashing alternative often enough  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: strings, palindrome definition; hashing alternative often enough

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Manacher computes, for every center, the radius of the longest palindrome in **linear time**, by recycling mirrors inside a known palindrome—exactly the Z-box idea applied to palindromic radius.

Transform trick: insert sentinels `^#a#b#c#$` so odd/even palindromes unify into odd centers on the transformed string. Array `p[i]` = radius in transformed coordinates (how many steps you can expand).

Inside the current rightmost palindrome centered at `c` with right edge `r`, the mirror of `i` is `2c-i`. You can start radius at `min(p[mirror], r-i)` and expand only when you hit the boundary.

**When hashing is enough:** count/check palindromes with binary search + forward/reverse hash is often shorter to code and O(n log n). Use Manacher when you need **all radii**, O(n) guaranteed, or tight constraints.

**vs eertree:** Manacher gives radii / all maximal palindromes around centers. Eertree builds a tree of *distinct* palindromes with suffix links—richer structure, rarer need (see 03b).

---

#### 4. Proof Sketches & Recurrences

Let `t` be transformed string length `m`. Maintain `c,r`. For each `i`:
- `mirror = 2c - i`
- `p[i] = i < r ? min(r - i, p[mirror]) : 0`
- while `t[i + p[i] + 1] == t[i - p[i] - 1]`, `p[i]++`
- if `i + p[i] > r`, update `c,r`

Original-string odd palindrome at center `i` corresponds to transformed center `2i+2` (depends on exact transform). Even palindrome between `i` and `i+1` maps to the `#` between them.

Number of palindromic substrings = sum over centers of number of expansions (each radius step adds one palindrome), carefully mapped back—or sum `(p[i]+1)/2` style formulas on transformed `p` (verify on `"aaa"`).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n)
- Per-query / per-operation: O(1) per center radius
- Total: O(n)
- Memory: O(n)`

##### C++17 Template

```cpp
namespace manacher {
// returns vector d for original string:
// d1[i] = radius of odd palindrome centered at i (length 2*d1[i]-1)
// d2[i] = radius of even palindrome with right center i (between i-1 and i), length 2*d2[i]
pair<vector<int>, vector<int>> manacher(const string& s) {
    int n = (int)s.size();
    vector<int> d1(n), d2(n);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) k++;
        d1[i] = k--;
        if (i + k > r) l = i - k, r = i + k;
    }
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k--;
        if (i + k > r) l = i - k - 1, r = i + k;
    }
    return {d1, d2};
}

string longest_palindrome(const string& s) {
    auto [d1, d2] = manacher(s);
    int best = 0, st = 0;
    int n = (int)s.size();
    for (int i = 0; i < n; i++) {
        if (2 * d1[i] - 1 > best) best = 2 * d1[i] - 1, st = i - d1[i] + 1;
        if (2 * d2[i] > best) best = 2 * d2[i], st = i - d2[i];
    }
    return s.substr(st, best);
}
} // namespace manacher
```

##### Python 3 Template

```python
def manacher(s: str) -> tuple[list[int], list[int]]:
    n = len(s)
    d1 = [0] * n
    l = 0
    r = -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k, i + k
    d2 = [0] * n
    l = 0
    r = -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k - 1, i + k
    return d1, d2
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Explicitly ask for longest palindromic substring
- Count palindromic substrings (sum of radii)
- For each center, need exact max odd/even palindrome length
- Problems that then DP on palindrome radii
- “Palindrome around every position” tables

---

#### 7. Contest WA / TLE / RE Traps

- Confusing odd/even radius definitions (`d1` vs `d2`) when extracting substring indices
- Off-by-one when converting radius → start index
- Expanding without mirror initialization → O(n²)
- Counting palindromes: each distinct *occurrence* vs distinct *string*—Manacher counts occurrences by center; distinct needs hash set / eertree / SA
- Empty string / n=1 edge cases in longest-palindrome extract

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Transformed `#` version** single array (classic CP-algorithms style)
- **Count all palindromic substrings:** sum of radii with correct formula
- **Longest palindrome in range** → needs sparse table on radii or different tools
- **Manacher + DP:** dp on ends of palindromes

---

#### 11. Typical Problem Archetypes

1. Standard application: longest palindromic substring
2. Slightly disguised: count palindromic substrings
3. Difficult: minimum characters to append to make palindrome (related to borders of s + '#' + rev); hybrid with KMP
4. Very difficult / advanced: palindrome partitioning optimizations; interact with eertree for distinct

---

#### 12. Recognition & Identification Drills

1. Return the length of the longest palindromic substring.
2. Count how many substrings are palindromes (occurrences, not distinct).
3. For each index i, find the longest palindrome starting at i (not necessarily centered at i).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need all palindrome radii in O(n); else hash+binsearch often fine
- Key invariant: mirror radii inside current rightmost palindrome
- Key formula: start from `min(p[mirror], r-i)`, then expand
- Complexity: O(n)
- Template to remember: separate odd/even loops with `[l,r]` boxes

---

## 5. Aho-Corasick

---


---

<a id="topic-5"></a>
### 5. Aho-Corasick Automaton

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1800–2400 | **Frequency:** Occasional  
> **Prerequisites:** trie, KMP failure links intuition  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: trie, KMP failure links intuition

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Aho-Corasick = **trie of all patterns** + **failure links** (KMP-style borders on the trie) + **output/dictionary links**.

Failure link of node `v` points to the longest proper suffix of the string represented by `v` that is still a trie node (prefix of some pattern). Output link jumps to the next node that corresponds to an actual pattern end (skipping empty fail chain).

Reading the text once: from state `u`, on char `c` follow transition (build via BFS: missing edges go to `fail`’s transition). At each state, report all patterns ending here by walking output links.

**vs multi KMP:** |patterns| separate KMPs is O(|T|·Σ patterns) worst in naive multi-scan, or awkward. AC is O(|T| + sum |P_i| + occurrences) with careful output handling.

**vs SA:** SA can find all pattern occurrences via binary search per pattern; AC is better when many patterns stream online or you need automaton DP (“how many ways to build string avoiding patterns”).

---

#### 4. Proof Sketches & Recurrences

1. Insert all patterns into a trie; mark `out[v]` with pattern indices ending at `v`.
2. BFS from root: for root’s children, `fail = root`. For node `v` with parent edge `c`, `fail[v] = go(fail[parent], c)` (KMP jump).
3. `go(v,c)`: if transition exists use it; else follow fail until possible (memoize as full transitions during BFS).
4. `dict_link[v] = out[fail[v]] ? fail[v] : dict_link[fail[v]]` (skip to next output).

**Complexity:** building O(Σ |P_i| · σ) if you fill all alphabet transitions, or alphabet-map / dynamic. Matching O(|T| + total reported occurrences) if you walk dict links carefully (can be O(|T|·answers)).

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(Σ|P_i| · σ) with filled transitions
- Per-query / per-operation: O(|T|) transitions + O(occurrences) reporting
- Total: linear in input + outputs (watch output merging)
- Memory: O(Σ|P_i| · σ)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Multiple pattern matching in one text
- “Forbidden words” / virus detection / dictionary hits
- DP on automaton: count strings of length n that avoid a set of patterns
- Replace all dictionary words; highlight matches
- Online streaming match as characters arrive

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to BFS-build fail links before search
- Not filling missing transitions → TLE from fail-walking each step
- Reporting: infinite loop on dict links; missing overlapping matches
- Alphabet assumptions (`'a'..'z'` only) when digits/uppercase appear
- Cloning entire output lists to every fail child → exponential memory
- Root transitions: missing char at root must go to root, not −1

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **DP on AC:** `dp[i][state]` after i chars; forbidden if output nonempty
- **Online AC** with incremental pattern adds (harder; usually rebuild)
- **Bitset of matched patterns** per node for small pattern counts
- **Fail tree** as graph: subtree problems on pattern occurrences
- **Binary alphabet / large alphabet:** map / dynamic next

---

#### 11. Typical Problem Archetypes

1. Standard application: find which patterns occur in text
2. Slightly disguised: shortest superstring-ish / cover text with dictionary words (DP on AC)
3. Difficult: count distinct matched patterns; minimum deletions to avoid viruses
4. Very difficult / advanced: AC + segment tree on fail tree; dynamic patterns

---

#### 12. Recognition & Identification Drills

1. Given k ≤ 1e5 total pattern length and text length 1e6, report for each pattern whether it occurs.
2. Count binary strings of length n that contain none of given forbidden words.
3. Replace every occurrence of any dictionary word by `*` (non-overlapping leftmost longest—policy matters).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: many patterns, one text; automaton DP with dictionary
- Key invariant: fail link = border in the trie; dict link skips to next pattern end
- Key formula: build fails in BFS order; missing edge `next[v][c] = next[fail[v]][c]`
- Complexity: O(|text| + sum |patterns| + occ)
- Template to remember: trie + BFS fail + output/dict links

---

[Back to Section 11 hub](11-string-algorithms.md) · [Continue to 03b](11-b-string-algorithms.md)

---


---

<a id="topic-6"></a>
### 6. Suffix Array

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** sorting, radix / pairwise ranking; string comparisons; preferably LCP (next section)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: sorting, radix / pairwise ranking; string comparisons; preferably LCP (next section)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

The **suffix array** `sa[0..n-1]` is the list of starting indices of all suffixes of `s` in lexicographic order. Often append a sentinel `$` smaller than every alphabet character so no suffix is a prefix of another.

Once you have SA, binary search finds any pattern in O(|P| log n) character compares (or O(|P| + log n) with LCP + RMQ). With LCP, you unlock distinct substrings, number of occurrences, longest repeated substring, string matching statistics—the “heavy” string toolkit without building an explicit suffix tree.

**Construction choice for contests:**
- **Doubling (prefix-doubling):** clean, O(n log² n) with `std::sort` or O(n log n) with radix on ranks. Easy to remember and debug.
- **SA-IS:** O(n), excellent constants in good implementations; harder to write from scratch under pressure. Sketch below; ship a trusted snippet if you rely on it.
- **DC3 / skew:** O(n), rarely hand-coded in contests now.

Prefer **doubling with radix** as your default “I can rewrite it” code; keep SA-IS in a library if you have one.

---

#### 4. Proof Sketches & Recurrences

Let `r_k[i]` be the rank of substring `s[i..i+2^k)`.  
Base: sort characters → `r_0`.  
Transition: pair `(r_k[i], r_k[i+2^k])` (use −1 / sentinel if out of range). Sort suffixes by these pairs → new ranks `r_{k+1}`.  
After `⌈log n⌉` steps, ranks are unique; `sa[rank[i]] = i`.

With comparison sort: O(n log n) steps × O(n log n) sort = O(n log² n).  
With counting sort on ranks: O(n) per level → O(n log n).

**SA-IS sketch (induced sorting):**
1. Classify suffixes L/S (s[i] > s[i+1] → L, else S); LMS = leftmost S of a run.
2. Name LMS substrings by induced sort using buckets; recurse on LMS name string.
3. Induce full SA from sorted LMS order via L then S bucket scans.

You need careful bucket pointers; wrong L/S → silent WA. Use only if practiced.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n log² n) sort-doubling; O(n log n) radix-doubling; O(n) SA-IS
- Per-query / per-operation: O(|P| log n) pattern binary search without LCP acceleration
- Total: construction + queries
- Memory: O(n)`

##### C++17 Template

```cpp
namespace sa {
// Primary: doubling + std::sort — O(n log^2 n), clear and contest-ready.
// Append sentinel 0; input chars should be > 0 (e.g. 'a'..'z').
vector<int> build(string s) {
    s += char(0);
    int n = (int)s.size();
    vector<int> sa(n), r(n), tmp(n);
    iota(sa.begin(), sa.end(), 0);
    for (int i = 0; i < n; i++) r[i] = (unsigned char)s[i];
    for (int k = 0; k < n; k = k ? k * 2 : 1) {
        auto cmp = [&](int i, int j) {
            if (r[i] != r[j]) return r[i] < r[j];
            int a = i + k < n ? r[i + k] : -1;
            int b = j + k < n ? r[j + k] : -1;
            return a < b;
        };
        sort(sa.begin(), sa.end(), cmp);
        tmp[sa[0]] = 0;
        for (int i = 1; i < n; i++)
            tmp[sa[i]] = tmp[sa[i - 1]] + (cmp(sa[i - 1], sa[i]) ? 1 : 0);
        r.swap(tmp);
        if (r[sa.back()] == n - 1) break;
    }
    sa.erase(sa.begin()); // drop sentinel suffix (smallest)
    return sa;
}

// Faster doubling + radix / counting sort — O(n log n).
vector<int> build_radix(string s) {
    s += char(0);
    int n = (int)s.size();
    vector<int> sa(n), r(n), nr(n);
    int alphabet = max(n, 256);
    vector<int> cnt(alphabet + 2, 0);
    for (int i = 0; i < n; i++) {
        sa[i] = i;
        r[i] = (unsigned char)s[i];
        cnt[r[i] + 1]++;
    }
    for (int i = 1; i < (int)cnt.size(); i++) cnt[i] += cnt[i - 1];
    // initial sort by character already via ranks; full loop:
    iota(sa.begin(), sa.end(), 0);
    sort(sa.begin(), sa.end(), [&](int i, int j) { return r[i] < r[j]; });
    for (int k = 1; k < n; k <<= 1) {
        auto second = [&](int i) -> int { return i + k < n ? r[i + k] + 1 : 0; };
        // sort by second key
        fill(cnt.begin(), cnt.end(), 0);
        for (int i = 0; i < n; i++) cnt[second(i)]++;
        for (int i = 1; i < (int)cnt.size(); i++) cnt[i] += cnt[i - 1];
        vector<int> by2(n);
        for (int i = n - 1; i >= 0; i--) by2[--cnt[second(sa[i])]] = sa[i];
        // sort by first key (stable via previous order)
        fill(cnt.begin(), cnt.end(), 0);
        for (int i = 0; i < n; i++) cnt[r[i]]++;
        for (int i = 1; i < (int)cnt.size(); i++) cnt[i] += cnt[i - 1];
        for (int i = n - 1; i >= 0; i--) sa[--cnt[r[by2[i]]]] = by2[i];
        nr[sa[0]] = 0;
        for (int i = 1; i < n; i++) {
            int a = sa[i - 1], b = sa[i];
            nr[b] = nr[a] + (r[a] != r[b] || second(a) != second(b));
        }
        r.swap(nr);
        if (r[sa[n - 1]] == n - 1) break;
        alphabet = n;
        if ((int)cnt.size() < alphabet + 2) cnt.assign(alphabet + 2, 0);
    }
    sa.erase(sa.begin());
    return sa;
}

// SA-IS sketch (O(n)) — use a trusted library implementation in contest;
// induced sorting outline:
// 1) Classify L/S; mark LMS positions.
// 2) Bucket-sort LMS substrings via induce L then S; name LMS; recurse.
// 3) Induce full SA from sorted LMS order.
// Wrong L/S or bucket heads → silent WA; prefer build() / build_radix() unless practiced.
} // namespace sa
```

##### Python 3 Template

```python
# Python impractical for large CF tests (n ≥ 1e5 often TLE).
# Useful remnant: the interface and Kasai LCP once SA is known; or n ≤ 2e4.

def suffix_array(s: str) -> list[int]:
    s = s + "\0"
    n = len(s)
    sa = list(range(n))
    r = [ord(c) for c in s]
    k = 1
    while True:
        sa.sort(key=lambda i: (r[i], r[i + k] if i + k < n else -1))
        tmp = [0] * n
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (
                (r[sa[i - 1]], r[sa[i - 1] + k] if sa[i - 1] + k < n else -1)
                < (r[sa[i]], r[sa[i] + k] if sa[i] + k < n else -1)
            )
        r = tmp
        if r[sa[-1]] == n - 1:
            break
        k *= 2
    return sa[1:]  # drop sentinel
```

---

#### 6. Recognition Trigger Signals & Heuristics

- All suffixes sorted / lex compare many suffixes
- Longest repeated substring; number of distinct substrings
- Pattern matching when many queries or need occurrence ranges on SA
- Lex smallest rotation (SA of `s+s` or min among first n cyclic)
- Comparing two strings’ substring structures; LCS of two strings via SA of concat

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting sentinel → ties when one suffix is prefix of another
- Erasing wrong SA entry after sentinel
- Rank update: must use old ranks for both keys in the same round
- Alphabet / signed char: cast to `unsigned char`
- Pattern search bounds: occurrence range is contiguous on SA but need LCP to count fast
- Off-by-one on string length after appending sentinel

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Cyclic shifts / necklace:** SA on `s+s`, restrict starts `< n`
- **Two strings:** concat `A + '#' + B + '$'`, SA+LCP for LCS
- **Sparse SA / only needed suffixes**
- **SA + segment tree on LCP** for rich queries

---

#### 11. Typical Problem Archetypes

1. Standard application: construct SA; find any occurrence of P
2. Slightly disguised: lex smallest rotation; sort all cyclic shifts
3. Difficult: distinct substrings count (needs LCP); k-th substring
4. Very difficult / advanced: multi-string problems; SA + persistent segtree on ranks

---

#### 12. Recognition & Identification Drills

1. Output the suffix array of a given string.
2. Find the lexicographically smallest rotation of s.
3. Given many patterns, find for each whether it is a substring of s (n, sum|P| large).

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: need global order of suffixes / repeated substring statistics
- Key invariant: doubling ranks by length 2^k pairs
- Key formula: sort by `(rank[i], rank[i+k])`
- Complexity: O(n log² n) fine for n≤4e5 usually
- Template to remember: doubling + sort + re-rank until unique

---

## 7. LCP

---


---

<a id="topic-7"></a>
### 7. LCP Array (Kasai) + Applications

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** suffix array  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: suffix array

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

`lcp[i]` = length of longest common prefix of suffixes `sa[i]` and `sa[i-1]` (define `lcp[0] = 0`). Adjacent-in-SA LCP is enough because for any two suffixes, LCP equals the **minimum** LCP on the SA-interval between them (RMQ).

**Kasai’s algorithm** computes LCP in O(n) given SA and the inverse `rank[sa[i]] = i`: walk suffixes in text order `i = 0..n-1`; the LCP of suffix `i` with its SA-predecessor is at least `h-1` if suffix `i-1` had height `h`—so decrement `h` at most once per step and extend.

**Why LCP unlocks SA power:**
- Number of distinct substrings = `n(n+1)/2 - Σ lcp[i]`
- Longest repeated substring = max `lcp[i]`
- Occurrence count of a pattern = size of SA range where suffixes share prefix |P|
- LCS of two strings = max LCP among adjacent SA pairs that come from different strings

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) Kasai + O(n log n) sparse table
- Per-query / per-operation: O(1) LCP of any two suffixes with RMQ
- Total: O(n) after SA
- Memory: O(n)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Anything “count distinct substrings / unique occurrences”
- Longest duplicated substring
- k-th lexicographic substring (walk SA accumulating `n - sa[i] - lcp[i]` new strings)
- Match statistics needing RMQ on LCP
- After you built SA, almost always build LCP next

---

#### 7. Contest WA / TLE / RE Traps

- `lcp` indexing: some codes store `lcp[i] = LCP(sa[i], sa[i+1])` — pick a convention
- Forgetting `k--` → still correct but O(n²)
- Distinct substring formula wrong if sentinel still in SA
- RMQ off-by-one: LCP(sa[a], sa[b]) = min on `(min(a,b)+1 .. max(a,b))` under `lcp[i]=LCP(sa[i],sa[i-1])`
- Mixing lengths of A and B in concat LCS problems (ignore LCP across separator only… actually take max where owners differ)

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Phi / PLCP** variants of Kasai
- **LCP of pattern vs SA range** during binary search (accelerated matching)
- **Histogram / stack on LCP** for “number of substrings appearing ≥ k times”
- **Diff array on SA ranges** for occurrence tagging

---

#### 11. Typical Problem Archetypes

1. Standard application: distinct substrings; longest repeated substring
2. Slightly disguised: k-th lex substring; shared substrings of two strings
3. Difficult: count pairs of substrings with LCP constraints; stack on LCP histogram
4. Very difficult / advanced: string borders statistics; match to multiple texts with color on SA

---

#### 12. Recognition & Identification Drills

1. Count distinct substrings of s.
2. Find any longest substring that occurs at least twice.
3. Find LCS length of two strings via SA+LCP of a concatenation.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: always pair with SA for counting / repeated / LCS-of-two
- Key invariant: Kasai height decreases by at most 1 when moving to next text position
- Key formula: distinct = n(n+1)/2 − Σ lcp
- Complexity: O(n) LCP
- Template to remember: `rank`, walk i in text order, extend, `k--`

---

## 8. Suffix Automaton

---


---

<a id="topic-8"></a>
### 8. Suffix Automaton (SAM)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 2000–2700 | **Frequency:** Occasional  
> **Prerequisites:** automata intuition; optional SA familiarity (different model)  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 2000–2700
- Prerequisites: automata intuition; optional SA familiarity (different model)

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

The **suffix automaton** of s is the minimal DFA that recognizes exactly the set of suffixes of s (and as a byproduct, all substrings are paths from the start state). It has ≤ 2n−1 states and ≤ 3n−4 transitions for length n ≥ 3.

Each state represents an **endpos-equivalence class**: set of substrings that end at the same set of positions. A state stores `len` (longest string in the class) and `link` (suffix link) to the state of the longest proper suffix in a different class. Strings in a state have lengths `(len(link)+1 .. len)`.

**Online construction:** append characters one by one; clone states when needed (the famous “clone” step). This is why SAM is so contest-friendly for “all substrings” problems: after build, DP on DAG of transitions or on suffix-link tree.

**SAM vs SA:**
- SAM: excellent for “number of distinct substrings”, “first occurrence”, “continue reading online”, automaton DP, endpos sizes
- SA+LCP: excellent for lex order, k-th substring, RMQ between suffixes, some occurrence-interval problems
- Overlap large; pick the structure that matches the query shape

---

#### 4. Proof Sketches & Recurrences

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

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n · σ) time with arrays; O(n) amortized with maps (worse constants)
- Per-query / per-operation: O(|P|) run pattern; O(#states) DP
- Total: linear in practice for fixed σ
- Memory: O(n · σ)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Number of distinct substrings (Σ over states `len - len(link)`)
- Occurrences of each substring / endpos size DP
- Longest substring occurring ≥ k times
- Shortest non-appearing string over alphabet
- Online: process stream, maintain SAM of text so far
- Pattern matching: run pattern on SAM of text
- Multiple strings: generalized SAM / trie of SAMs / concat with separators carefully

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting `occ[clone] = 0` and `occ[cur] = 1` → wrong occurrence counts
- Propagating occ without sorting by decreasing length
- Distinct substrings: starting from state 0 incorrectly; use `len - len(link)` for v≥1
- Redirect loop must only rewrite transitions that still point to `q`
- Using SAM of reverse string when problem wants prefixes vs suffixes—check direction
- Alphabet compression forgotten for large char sets

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **SAM of reverse** for prefix structure / palindromes hybrids
- **Generalized SAM** for multiple words
- **DP on DAG:** longest path, count paths = substrings through states
- **Fail/suffix-link tree** as real tree for subtree occ sums
- **Minimum cyclic shift** via SAM tricks / Duval; often Lyndon or SA simpler

---

#### 11. Typical Problem Archetypes

1. Standard application: count distinct substrings
2. Slightly disguised: total length of distinct substrings; first occurrence position
3. Difficult: lexicographic DFS on SAM for k-th substring; occurrence ≥ k longest
4. Very difficult / advanced: SAM + segtree on endpos; dynamic strings; matching statistics

---

#### 12. Recognition & Identification Drills

1. Compute the number of distinct substrings of s.
2. Find the longest substring that appears at least twice.
3. Find the shortest string over `{a,b}` that is not a substring of s.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: substring set as automaton; distinct count; occurrence via endpos; online append
- Key invariant: endpos equivalence; suffix links
- Key formula: distinct += len[v] − len[link[v]]
- Complexity: O(n) states/transitions order
- Template to remember: extend with possible clone + redirect

---

## 9. Suffix Tree Concepts

---


---

<a id="topic-9"></a>
### 9. Suffix Tree (Conceptual — Lower Early ROI)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** suffix array + LCP, or Ukkonen intuition; most contest tasks solvable without explicit tree  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: suffix array + LCP, or Ukkonen intuition; most contest tasks solvable without explicit tree

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

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

#### 4. Proof Sketches & Recurrences

**From SA+LCP (cartesian / stack construction):** process SA left to right; maintain stack of LCP depths to build a tree whose leaves are suffixes in order and internal node depths are LCPs—this is the **suffix tree / LCP tree** in O(n). This is the practical “construction” if you truly need nodes.

**Ukkonen (sketch):** online, all suffixes implicit via active point; open transitions; suffix links between internal nodes; O(n) with careful edge representation. Easy to get wrong.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n) Ukkonen / O(n) from SA+LCP
- Per-query / per-operation: O(|P|) walk
- Total: O(n + queries)
- Memory: O(n)`

##### C++17 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Editorial mentions Ukkonen / “build suffix tree”
- Need explicit branching nodes with edge labels as intervals
- Research-olympiad stringology; rarely modern CF Div.1 easy/medium

---

#### 7. Contest WA / TLE / RE Traps

- Edge label index errors; off-by-one on half-open intervals
- Missing suffix links in Ukkonen
- Treating uncompressed trie as tree → O(n²) memory

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Generalized suffix tree** for multiple strings
- **Compact vs Patricia**
- **Suffix link tree vs transition DAG (SAM)**

---

#### 11. Typical Problem Archetypes

1. Standard application: textbook pattern matching via tree walk
2. Slightly disguised: longest repeated via deepest internal node
3. Difficult: tree DP on explicit nodes
4. Very difficult / advanced: research-level stringology

---

#### 12. Recognition & Identification Drills

1. Explain how max LCP relates to deepest internal node in the suffix tree.
2. Given SA and LCP, describe how to build the compressed trie structure with a stack.
3. Name two contest problems usually solved with SAM/SA that textbooks solve with suffix trees.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: rarely; prefer SA+LCP or SAM
- Key invariant: compressed trie of suffixes; O(n) size
- Key formula: internal node string-depth ↔ LCP structure
- Complexity: O(n) build in theory
- Template to remember: “don’t implement Ukkonen unless necessary; map to SA/SAM”

---

## 10. Palindromic Tree / Eertree

---


---

<a id="topic-10"></a>
### 10. Palindromic Tree (Eertree) — Lower Early ROI

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** C-tier | **Rating Range:** 2200–2800 | **Frequency:** Rare  
> **Prerequisites:** palindrome radii intuition (Manacher); automata/suffix-link comfort  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2200–2800
- Prerequisites: palindrome radii intuition (Manacher); automata/suffix-link comfort

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

The **eertree** stores all **distinct** palindromic substrings of s in O(n) nodes. Two roots: even empty palindrome (length 0) and odd “−1” imaginary. Each node is a distinct palindrome; edges add a character on both sides; **suffix link** points to the longest proper palindromic suffix.

Online: when appending `s[i]`, start from the node of the longest palindromic suffix of `s[0..i-1]`, walk suffix links until `s[i - len - 1] == s[i]`, then possibly create a new node.

**Manacher vs eertree:**
- Manacher: all centers’ radii (occurrences / geometry of palindromes), O(n)
- Eertree: **distinct** palindromes as nodes + links; occurrence counts; DP on palindromes
- If you only need longest or count occurrences of palindromic substrings, Manacher (or hash) wins on ROI
- If you need “how many distinct palindromes” or DP over distinct palindrome nodes, eertree shines

**Early ROI:** skip until Manacher/hash/SAM are solid. Marked **lower early ROI** on purpose.

---

#### 4. Proof Sketches & Recurrences

Nodes ≤ n + 2. For append at i:
- Let `v` be last = longest palindromic suffix before add.
- While `i - st[v].len - 1 < 0` or `s[i - st[v].len - 1] != s[i]`, `v = link[v]`.
- If transition `s[i]` from `v` exists, last = that child (palindrome already known); else create node with `len = st[v].len + 2`, set suffix link by continuing from `link[v]`, etc.

Occurrence: increment count on `last` each time; propagate via suffix links or as needed.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing / build: O(n) amortized
- Per-query / per-operation: O(1) amortized per append
- Total: O(n)
- Memory: O(n · σ)`

##### C++17 Template

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

##### Python 3 Template

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

#### 6. Recognition Trigger Signals & Heuristics

- Count **distinct** palindromic substrings
- DP where states are distinct palindromes
- Problems explicitly mentioning palindromic tree / eertree in blogs
- Frequency of each distinct palindrome

---

#### 7. Contest WA / TLE / RE Traps

- Wrong odd/even roots (`len = -1` node essential)
- Suffix link for length-1 must go to even root 0
- Forgetting to increment cnt on already-existing node
- Walking links without bounds check on `pos - L - 1`
- Confusing distinct count with Manacher occurrence count

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- **Series links / quick links** for faster DP (advanced)
- **Eertree + DP** on last palindrome suffix partitions
- **Count occurrences** via cnt propagate along links

---

#### 11. Typical Problem Archetypes

1. Standard application: number of distinct palindromic substrings
2. Slightly disguised: sum of frequencies of distinct palindromes
3. Difficult: palindrome partition DP accelerated by eertree links
4. Very difficult / advanced: series links, digraph of palindromes

---

#### 12. Recognition & Identification Drills

1. Count distinct palindromic substrings of s (n ≤ 1e5).
2. Compare your answer to Manacher-based occurrence count on `"aaa"` vs `"aba"` — explain the difference.
3. Maintain distinct palindrome count online under append-only.

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: distinct palindromes / DP on palindrome nodes — else Manacher/hash
- Key invariant: ≤ n distinct palindromes; suffix = longest palindromic suffix link
- Key formula: nodes = distinct pals; online append with link walks
- Complexity: O(n)
- Template to remember: two roots (−1 and 0), create node len+2, set link

---

## 11. Which Problems Each Algorithm Solves — Synthesis

---


---

<a id="topic-11"></a>
### 11. Recognition Matrix + Adapted A–L

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier (meta-skill) | **Rating Range:** 1400–2700 (depends on tool) | **Frequency:** Very Common (decides tool choice)  
> **Prerequisites:** sections 1–10 at least at recognition level  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (meta-skill)
- Frequency: Very Common (decides tool choice)
- Typical CF/ICPC rating range: 1400–2700 (depends on tool)
- Prerequisites: sections 1–10 at least at recognition level

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

String problems are usually **not** “implement a named algorithm.” They are “which string view fits?”:

| Need | First tool |
|------|------------|
| One pattern in text | KMP or Z or hash |
| Prefix-match lengths at every index | Z |
| Borders / periods / failure function | KMP π |
| Substring equality / lex compare / flexible queries | Rolling hash |
| Many patterns in one text / dictionary DP | Aho-Corasick |
| All radii / count palindrome *occurrences* | Manacher (or hash) |
| Distinct palindromes / palindrome-node DP | Eertree (niche) |
| Lex order of suffixes, k-th substring, LCS of 2 via concat | SA + LCP |
| Distinct substrings, endpos, online substrings automaton | SAM |
| Explicit compressed trie nodes | Suffix tree (rare; use SA/SAM) |

**Hash vs SA:** hash wins for speed of coding and pairwise equality; SA wins when you need global order, deterministic heavy counting, or LCP RMQ structure.

**SA vs SAM:** SA = sorted suffixes; SAM = automaton of substrings / endpos. Distinct count: both. k-th lex substring: SA+LCP natural. Online append / run automaton: SAM.

**Manacher vs eertree:** geometry of centers vs set of distinct pals.

**Aho vs multi-KMP:** Aho for dictionary + automaton DP; KMP only if one pattern or few.

---

#### 4. Proof Sketches & Recurrences

Decision flow (contest):
1. If only equality / binary search on strings → **hash** (double).
2. Else if single pattern / period → **KMP/Z**.
3. Else if many patterns → **Aho**.
4. Else if palindromes:
   - occurrences / longest → **Manacher** or hash;
   - distinct / node DP → **eertree** (if known).
5. Else if substring set / counts / occurrences of all:
   - lex / k-th / LCS two strings → **SA+LCP**;
   - automaton / distinct / endpos → **SAM**.
6. Explicit suffix tree → only if forced; else map to SA/SAM.

---

#### 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: tool-dependent (see each section)
- Per-query / per-operation: tool-dependent
- Total: prefer O(n) / O(n log n) string scans at n≤1e6 (C++)
- Memory: watch O(nσ) automata`

##### C++17 Template

```cpp
// No single template — keep a personal library:
// kmp::, zfunc::, rhash::, manacher::, aho::, sa::, lcp::, sam::
// Load the namespace that matches the recognition matrix row.
```

##### Python 3 Template

```python
# Practical in Python: KMP, Z, hashing, Manacher, light Aho.
# Impractical / risky at CF scale: suffix array, SAM, heavy Aho, eertree on tight TL.
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Keyword “period / border / prefix function” → KMP
- “Match lengths with prefix” → Z
- “Are these two substrings equal?” → hash (or SA LCP)
- “Forbidden dictionary / many needles” → Aho
- “Longest palindromic substring / count pals” → Manacher
- “Distinct substrings” → SAM or SA+LCP
- “k-th substring / suffix order” → SA+LCP
- “Distinct palindromes” → eertree

---

#### 7. Contest WA / TLE / RE Traps

- Using SA when hash suffices (time sink)
- Using eertree for longest palindrome (overkill)
- Single hash on CF without randomization
- Python SA/SAM on n=1e5
- Wrong tool: counting distinct pals with Manacher sum of radii

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---

#### 10. Algorithmic Variants & Advanced Extensions

- Hybrid: hash + SA verify; Aho + DP; SAM of reverse; KMP for period after Manacher
- Multi-string: concat with unique separators for SA; generalized SAM; AC for dictionary

---

#### 11. Typical Problem Archetypes

1. Standard application: map statement → matrix row → code library
2. Slightly disguised: period hiding inside DP; equality hiding inside binary search on answer
3. Difficult: need two structures (e.g. Aho + segtree on fail tree)
4. Very difficult / advanced: stringology stacks (runs, Lyndon) beyond this section

---

#### 12. Recognition & Identification Drills

1. “Count distinct substrings” — which two tools work, and which is shorter?
2. “q substring equality queries” — hash or SA?
3. “k patterns, one text, then DP avoid them” — why Aho beat multi-KMP?

---

#### 13. Fast-Lookup Cheat Sheet

- When to use: always, before coding strings
- Key invariant: match the *question about substrings* to the *structure that materializes it*
- Key formula: see matrix in B
- Complexity: pick O(n)–O(n log n) C++ tools first
- Template to remember: Hash → KMP/Z → Aho → Manacher → SA/LCP ↔ SAM → (tree/eertree niche)

---


---

<a id="topic-12"></a>
### 12. Quick Reference — Algorithm → Problem Class

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2400
- Prerequisites: String matching basics

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

String algorithm matching matrix: Single pattern matching $\to$ KMP / Z-algorithm $\mathcal{O}(N + M)$; Multiple pattern matching $\to$ Aho-Corasick Automaton; Palindrome enumeration $\to$ Manacher $\mathcal{O}(N)$; Lexicographical queries / LCP $\to$ Suffix Array + LCP; All substring transitions $\to$ Suffix Automaton (SAM) $\mathcal{O}(N)$.

---

#### 4. Proof Sketches & Recurrences

KMP computes prefix failure links $\pi[i] = \max \{ k < i : s[0..k-1] = s[i-k..i-1] \}$. Suffix Automaton constructs the minimal DFA recognizing all substrings with at most $2N-1$ states and $3N-4$ transitions.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// String Quick Reference Matrix Implementation Check
#include <bits/stdc++.h>
using namespace std;

vector<int> prefix_function(const string& s) {
    int n = s.size();
    vector<int> pi(n);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Pattern search, periodic string prefixes, substring count, longest common substring.

---

#### 7. Contest WA / TLE / RE Traps

- Off-by-one in string length comparisons and prefix function transitions.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---


---

<a id="topic-13"></a>
### 13. High-ROI (drill first)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2000
- Prerequisites: Arrays, modulo arithmetic

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Start with Polynomial Rolling Hashing with double 64-bit moduli ($10^9+7$ and $10^9+9$) and base $B = 313$ or random odd integer, followed by KMP and Z-algorithm. These solve 70% of contest string tasks.

---

#### 4. Proof Sketches & Recurrences

Hash invariant: $H(s[0..i]) = (H(s[0..i-1]) \cdot B + s[i]) \pmod M$. Substring hash in $\mathcal{O}(1)$: $H(s[l..r]) = (H[r+1] - H[l] \cdot B^{r - l + 1}) \pmod M$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Double Polynomial Rolling Hash Template
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct StringHash {
    int n;
    ll B1 = 313, M1 = 1e9 + 7;
    ll B2 = 317, M2 = 1e9 + 9;
    vector<ll> h1, h2, p1, p2;
    StringHash(const string& s) : n(s.size()), h1(n + 1), h2(n + 1), p1(n + 1, 1), p2(n + 1, 1) {
        for (int i = 0; i < n; ++i) {
            h1[i + 1] = (h1[i] * B1 + s[i]) % M1;
            h2[i + 1] = (h2[i] * B2 + s[i]) % M2;
            p1[i + 1] = (p1[i] * B1) % M1;
            p2[i + 1] = (p2[i] * B2) % M2;
        }
    }
    pair<ll, ll> get_hash(int l, int r) {
        ll a = (h1[r + 1] - h1[l] * p1[r - l + 1]) % M1; if (a < 0) a += M1;
        ll b = (h2[r + 1] - h2[l] * p2[r - l + 1]) % M2; if (b < 0) b += M2;
        return {a, b};
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Checking if two substrings are equal in $O(1)$.
- Longest common prefix via binary search on hash values.

---

#### 7. Contest WA / TLE / RE Traps

- Single modulo hash hacked by anti-hash test cases; always use double hash with random base.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---


---

<a id="topic-14"></a>
### 14. Situational (Medium / B-tier)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Common
- Typical CF/ICPC rating range: 1800–2400
- Prerequisites: KMP, Trie, BFS

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Aho-Corasick builds a Trie over a dictionary of patterns and connects failure links via BFS, mimicking KMP on a tree. Manacher finds all maximal palindromic radii centered at each character/interstice in linear $\mathcal{O}(N)$ time.

---

#### 4. Proof Sketches & Recurrences

Failure link of node $u$ points to the longest proper suffix of $u$ present in the Trie. Manacher reuses the palindromic symmetry around the current rightmost boundary $R$.

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Aho-Corasick Multi-Pattern Automaton
#include <bits/stdc++.h>
using namespace std;

struct AhoCorasick {
    struct Node { int next[26] = {0}; int link = 0; int cnt = 0; };
    vector<Node> t = {Node()};
    void insert(const string& s) {
        int v = 0;
        for (char c : s) {
            int idx = c - 'a';
            if (!t[v].next[idx]) { t[v].next[idx] = t.size(); t.emplace_back(); }
            v = t[v].next[idx];
        }
        t[v].cnt++;
    }
    void build() {
        queue<int> q;
        for (int c = 0; c < 26; ++c) if (t[0].next[c]) q.push(t[0].next[c]);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (int c = 0; c < 26; ++c) {
                int u = t[v].next[c];
                if (u) { t[u].link = t[t[v].link].next[c]; q.push(u); }
                else { t[v].next[c] = t[t[v].link].next[c]; }
            }
        }
    }
};
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Given text $T$ and $K$ patterns, count occurrences of each pattern in $T$.
- Longest palindromic substring or palindromic prefix factorization.

---

#### 7. Contest WA / TLE / RE Traps

- Forgetting to propagate pattern counts along failure links in Aho-Corasick.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---


---

<a id="topic-15"></a>
### 15. Rarely worth early / Niche (C-tier)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1600–2200 | **Frequency:** Common  

---

#### 1. Contest Payoff & Why It Matters

- Contest ROI: C-tier
- Frequency: Rare
- Typical CF/ICPC rating range: 2400–3000
- Prerequisites: Suffix Automaton, Palindromic Tree

---

#### 2. Theoretical Deep-Dive & Mathematical Mechanics

##### Overview

String Algorithms solve pattern matching, periodic structure analysis, and dictionary search in linear time: Rolling Hash with randomized bases, KMP Prefix Function $\pi$, Z-Algorithm, Manacher's Algorithm, Aho-Corasick Automata, and Suffix Automata (SAM).

##### Fundamental Theorems & Invariants

- **Polynomial Rolling Hash Invariant:** $H(S) = \sum_{i=0}^{n-1} S[i] \cdot B^{n-1-i} \pmod M$. Substring hashes $H(S[l \dots r]) = (H(r) - H(l-1) \cdot B^{r-l+1}) \pmod M$ evaluate in $\mathcal{O}(1)$.
- **KMP Periodicity Lemma:** A string $S$ has a period of length $p$ if and only if $n - p = \pi[n-1]$ and $n \pmod p = 0$.
- **Suffix Automaton (SAM) Linear State Bound:** A Suffix Automaton is the minimal Deterministic Finite Automaton (DFA) accepting all suffixes of string $S$. For a string of length $N$, SAM has at most $2N-1$ states and $3N-4$ transitions, constructed in strictly $\mathcal{O}(N)$ time.
- **Aho-Corasick Dictionary Invariant:** Constructs a trie with KMP-style failure links and dictionary output links, processing multiple pattern searches over a text of length $T$ in $\mathcal{O}(|T| + \sum |P_i|)$ time.

##### Algorithmic Execution Blueprint

1. **Anti-Hash Hygiene:** Always pick base $B \in [10^8, 10^9]$ uniformly at random at runtime using `std::chrono::high_resolution_clock` to thwart anti-hash contest test cases.
2. **KMP Prefix Function:** Maintain pointer $j = \pi[i-1]$; while $j > 0$ and $S[i] \neq S[j]$, step $j = \pi[j-1]$. If $S[i] == S[j]$, $j++$; set $\pi[i] = j$.
3. **Suffix Automaton Extension:** For new character $c$, create state $cur$. Trace parent links from $last$, adding transitions to $cur$. If a state with existing transition is found, split clone state if necessary.

##### Closed-Form Invariant Equations

$$H(S[l \dots r]) = \Big(H[r] - H[l-1] \cdot B^{r-l+1} \pmod M + M\Big) \pmod M, \quad |\text{States}(\text{SAM})| \le 2N - 1$$

##### Structural Edge Cases & Assumptions

- Never use single 32-bit modulo (e.g. $10^9+7$) for rolling hashes on strings of length $> 10^5$; collision probability by Birthday Paradox exceeds $99\%$. Use double 64-bit hashing or 128-bit modulo.
- In Aho-Corasick, traverse the failure link DAG in topological order or use output link optimization to avoid quadratic match enumeration on repeated prefixes.
- Manacher's algorithm requires inserting separator tokens (e.g. `#`) to unify odd and even palindrome radius evaluations.

---

#### 3. Core Intuition & Problem Framing

Eertree (Palindromic Automaton) and Lyndon Factorization (Duval's algorithm) are specialized string constructs. Master Suffix Automaton and Aho-Corasick before investing time here.

---

#### 4. Proof Sketches & Recurrences

Eertree maintains directed transitions on characters between palindromic states with two roots (lengths $-1$ and $0$).

---

#### 5. Contest-Ready Implementation Templates

##### C++17 Template

```cpp
// Palindromic Tree (Eertree) outline
```

---

#### 6. Recognition Trigger Signals & Heuristics

- Number of distinct palindromic substrings in each prefix dynamically.

---

#### 7. Contest WA / TLE / RE Traps

- Incorrect initialization of length -1 imaginary root.

---

#### 8. Curated Practice Problem Bank

| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |
|---|---|---|---|---|---|---|
| Codeforces | CF-1200E | Compress Words | 1600 | KMP, Rolling Hash, Strings | KMP prefix function on merged boundary strings to find maximum overlap prefix-suffix. | [Solve Problem](https://codeforces.com/contest/1200/problem/E) |
| Codeforces | CF-432D | Prefixes and Suffixes | 2000 | Z-Algorithm, KMP, DP | Z-algorithm + prefix function DP to count occurrences of all matching prefixes. | [Solve Problem](https://codeforces.com/contest/432/problem/D) |
| Codeforces | CF-963D | Frequency of String | 2400 | Aho-Corasick, Trie, Strings | Aho-Corasick multi-pattern matching tracks occurrence position queues. | [Solve Problem](https://codeforces.com/contest/963/problem/D) |
| Codeforces | CF-1037H | Security | 2800 | Suffix Automaton, Persistent SegTree | Suffix Automaton + Persistent SegTree on endpos sets to greedily match next char. | [Solve Problem](https://codeforces.com/contest/1037/problem/H) |
| CSES | CSES-1753 | String Matching | 1400 | KMP, Z-Algorithm | Classic KMP pattern search / Z-algorithm linear scan. | [Solve Problem](https://cses.fi/problemset/task/1753) |

---

#### 9. External Theory & Deep-Dive References

- **[CP-Algorithms]** [CP-Algorithms: String Hashing & Randomized Anti-Hash](https://cp-algorithms.com/string/string-hashing.html)
- **[CP-Algorithms]** [CP-Algorithms: Prefix Function & KMP](https://cp-algorithms.com/string/prefix-function.html)
- **[CP-Algorithms]** [CP-Algorithms: Aho-Corasick Automaton](https://cp-algorithms.com/string/aho_corasick.html)
- **[CP-Algorithms]** [CP-Algorithms: Suffix Automaton (SAM)](https://cp-algorithms.com/string/suffix-automaton.html)

---


---
