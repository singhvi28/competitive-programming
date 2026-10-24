# 6. Suffix Array

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** A-tier | **Rating Range:** 1900–2600 | **Frequency:** Occasional  
> **Prerequisites:** sorting, radix / pairwise ranking; string comparisons; preferably LCP (next section)  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: A-tier
- Frequency: Occasional
- Typical CF/ICPC rating range: 1900–2600
- Prerequisites: sorting, radix / pairwise ranking; string comparisons; preferably LCP (next section)

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

The **suffix array** `sa[0..n-1]` is the list of starting indices of all suffixes of `s` in lexicographic order. Often append a sentinel `$` smaller than every alphabet character so no suffix is a prefix of another.

Once you have SA, binary search finds any pattern in O(|P| log n) character compares (or O(|P| + log n) with LCP + RMQ). With LCP, you unlock distinct substrings, number of occurrences, longest repeated substring, string matching statistics—the “heavy” string toolkit without building an explicit suffix tree.

**Construction choice for contests:**
- **Doubling (prefix-doubling):** clean, O(n log² n) with `std::sort` or O(n log n) with radix on ranks. Easy to remember and debug.
- **SA-IS:** O(n), excellent constants in good implementations; harder to write from scratch under pressure. Sketch below; ship a trusted snippet if you rely on it.
- **DC3 / skew:** O(n), rarely hand-coded in contests now.

Prefer **doubling with radix** as your default “I can rewrite it” code; keep SA-IS in a library if you have one.

---

## 4. Proof Sketches & Recurrences

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

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n log² n) sort-doubling; O(n log n) radix-doubling; O(n) SA-IS
- Per-query / per-operation: O(|P| log n) pattern binary search without LCP acceleration
- Total: construction + queries
- Memory: O(n)`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- All suffixes sorted / lex compare many suffixes
- Longest repeated substring; number of distinct substrings
- Pattern matching when many queries or need occurrence ranges on SA
- Lex smallest rotation (SA of `s+s` or min among first n cyclic)
- Comparing two strings’ substring structures; LCS of two strings via SA of concat

---

## 7. Contest WA / TLE / RE Traps

- Forgetting sentinel → ties when one suffix is prefix of another
- Erasing wrong SA entry after sentinel
- Rank update: must use old ranks for both keys in the same round
- Alphabet / signed char: cast to `unsigned char`
- Pattern search bounds: occurrence range is contiguous on SA but need LCP to count fast
- Off-by-one on string length after appending sentinel

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

- **Cyclic shifts / necklace:** SA on `s+s`, restrict starts `< n`
- **Two strings:** concat `A + '#' + B + '$'`, SA+LCP for LCS
- **Sparse SA / only needed suffixes**
- **SA + segment tree on LCP** for rich queries

---

## 11. Typical Problem Archetypes

1. Standard application: construct SA; find any occurrence of P
2. Slightly disguised: lex smallest rotation; sort all cyclic shifts
3. Difficult: distinct substrings count (needs LCP); k-th substring
4. Very difficult / advanced: multi-string problems; SA + persistent segtree on ranks

---

## 12. Recognition & Identification Drills

1. Output the suffix array of a given string.
2. Find the lexicographically smallest rotation of s.
3. Given many patterns, find for each whether it is a substring of s (n, sum|P| large).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: need global order of suffixes / repeated substring statistics
- Key invariant: doubling ranks by length 2^k pairs
- Key formula: sort by `(rank[i], rank[i+k])`
- Complexity: O(n log² n) fine for n≤4e5 usually
- Template to remember: doubling + sort + re-rank until unique

---

## 7. LCP

---
