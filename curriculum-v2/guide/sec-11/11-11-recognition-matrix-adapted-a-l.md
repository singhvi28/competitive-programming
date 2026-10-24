# Recognition Matrix + Adapted A–L

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier (meta-skill) | **Rating Range:** 1400–2700 (depends on tool) | **Frequency:** Very Common (decides tool choice)  
> **Prerequisites:** sections 1–10 at least at recognition level  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier (meta-skill)
- Frequency: Very Common (decides tool choice)
- Typical CF/ICPC rating range: 1400–2700 (depends on tool)
- Prerequisites: sections 1–10 at least at recognition level

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

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: tool-dependent (see each section)
- Per-query / per-operation: tool-dependent
- Total: prefer O(n) / O(n log n) string scans at n≤1e6 (C++)
- Memory: watch O(nσ) automata`

### C++17 Template

```cpp
// No single template — keep a personal library:
// kmp::, zfunc::, rhash::, manacher::, aho::, sa::, lcp::, sam::
// Load the namespace that matches the recognition matrix row.
```

### Python 3 Template

```python
# Practical in Python: KMP, Z, hashing, Manacher, light Aho.
# Impractical / risky at CF scale: suffix array, SAM, heavy Aho, eertree on tight TL.
```

---

## 6. Recognition Trigger Signals & Heuristics

- Keyword “period / border / prefix function” → KMP
- “Match lengths with prefix” → Z
- “Are these two substrings equal?” → hash (or SA LCP)
- “Forbidden dictionary / many needles” → Aho
- “Longest palindromic substring / count pals” → Manacher
- “Distinct substrings” → SAM or SA+LCP
- “k-th substring / suffix order” → SA+LCP
- “Distinct palindromes” → eertree

---

## 7. Contest WA / TLE / RE Traps

- Using SA when hash suffices (time sink)
- Using eertree for longest palindrome (overkill)
- Single hash on CF without randomization
- Python SA/SAM on n=1e5
- Wrong tool: counting distinct pals with Manacher sum of radii

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

- Hybrid: hash + SA verify; Aho + DP; SAM of reverse; KMP for period after Manacher
- Multi-string: concat with unique separators for SA; generalized SAM; AC for dictionary

---

## 11. Typical Problem Archetypes

1. Standard application: map statement → matrix row → code library
2. Slightly disguised: period hiding inside DP; equality hiding inside binary search on answer
3. Difficult: need two structures (e.g. Aho + segtree on fail tree)
4. Very difficult / advanced: stringology stacks (runs, Lyndon) beyond this section

---

## 12. Recognition & Identification Drills

1. “Count distinct substrings” — which two tools work, and which is shorter?
2. “q substring equality queries” — hash or SA?
3. “k patterns, one text, then DP avoid them” — why Aho beat multi-KMP?

---

## 13. Fast-Lookup Cheat Sheet

- When to use: always, before coding strings
- Key invariant: match the *question about substrings* to the *structure that materializes it*
- Key formula: see matrix in B
- Complexity: pick O(n)–O(n log n) C++ tools first
- Template to remember: Hash → KMP/Z → Aho → Manacher → SA/LCP ↔ SAM → (tree/eertree niche)

---
