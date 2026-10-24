# 4. Manacher’s Algorithm

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** B-tier | **Rating Range:** 1700–2300 | **Frequency:** Occasional  
> **Prerequisites:** strings, palindrome definition; hashing alternative often enough  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: B-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1700–2300
- Prerequisites: strings, palindrome definition; hashing alternative often enough

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

Manacher computes, for every center, the radius of the longest palindrome in **linear time**, by recycling mirrors inside a known palindrome—exactly the Z-box idea applied to palindromic radius.

Transform trick: insert sentinels `^#a#b#c#$` so odd/even palindromes unify into odd centers on the transformed string. Array `p[i]` = radius in transformed coordinates (how many steps you can expand).

Inside the current rightmost palindrome centered at `c` with right edge `r`, the mirror of `i` is `2c-i`. You can start radius at `min(p[mirror], r-i)` and expand only when you hit the boundary.

**When hashing is enough:** count/check palindromes with binary search + forward/reverse hash is often shorter to code and O(n log n). Use Manacher when you need **all radii**, O(n) guaranteed, or tight constraints.

**vs eertree:** Manacher gives radii / all maximal palindromes around centers. Eertree builds a tree of *distinct* palindromes with suffix links—richer structure, rarer need (see 03b).

---

## 4. Proof Sketches & Recurrences

Let `t` be transformed string length `m`. Maintain `c,r`. For each `i`:
- `mirror = 2c - i`
- `p[i] = i < r ? min(r - i, p[mirror]) : 0`
- while `t[i + p[i] + 1] == t[i - p[i] - 1]`, `p[i]++`
- if `i + p[i] > r`, update `c,r`

Original-string odd palindrome at center `i` corresponds to transformed center `2i+2` (depends on exact transform). Even palindrome between `i` and `i+1` maps to the `#` between them.

Number of palindromic substrings = sum over centers of number of expansions (each radius step adds one palindrome), carefully mapped back—or sum `(p[i]+1)/2` style formulas on transformed `p` (verify on `"aaa"`).

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n)
- Per-query / per-operation: O(1) per center radius
- Total: O(n)
- Memory: O(n)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Explicitly ask for longest palindromic substring
- Count palindromic substrings (sum of radii)
- For each center, need exact max odd/even palindrome length
- Problems that then DP on palindrome radii
- “Palindrome around every position” tables

---

## 7. Contest WA / TLE / RE Traps

- Confusing odd/even radius definitions (`d1` vs `d2`) when extracting substring indices
- Off-by-one when converting radius → start index
- Expanding without mirror initialization → O(n²)
- Counting palindromes: each distinct *occurrence* vs distinct *string*—Manacher counts occurrences by center; distinct needs hash set / eertree / SA
- Empty string / n=1 edge cases in longest-palindrome extract

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

- **Transformed `#` version** single array (classic CP-algorithms style)
- **Count all palindromic substrings:** sum of radii with correct formula
- **Longest palindrome in range** → needs sparse table on radii or different tools
- **Manacher + DP:** dp on ends of palindromes

---

## 11. Typical Problem Archetypes

1. Standard application: longest palindromic substring
2. Slightly disguised: count palindromic substrings
3. Difficult: minimum characters to append to make palindrome (related to borders of s + '#' + rev); hybrid with KMP
4. Very difficult / advanced: palindrome partitioning optimizations; interact with eertree for distinct

---

## 12. Recognition & Identification Drills

1. Return the length of the longest palindromic substring.
2. Count how many substrings are palindromes (occurrences, not distinct).
3. For each index i, find the longest palindrome starting at i (not necessarily centered at i).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need all palindrome radii in O(n); else hash+binsearch often fine
- Key invariant: mirror radii inside current rightmost palindrome
- Key formula: start from `min(p[mirror], r-i)`, then expand
- Complexity: O(n)
- Template to remember: separate odd/even loops with `[l,r]` boxes

---

## 5. Aho-Corasick

---
