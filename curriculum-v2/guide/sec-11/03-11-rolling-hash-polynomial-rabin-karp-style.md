# 3. Rolling Hash (Polynomial / Rabin–Karp style)

> **Section:** §11 String Algorithms & Automata  
> **Phase:** Phase 6 — String Algorithms  
> **Contest ROI:** S-tier | **Rating Range:** 1400–2200 | **Frequency:** Very Common  
> **Prerequisites:** modular arithmetic, prefix arrays; anti-hash awareness  

---

## 1. Contest Payoff & Why It Matters

- Contest ROI: S-tier
- Frequency: Very Common
- Typical CF/ICPC rating range: 1400–2200
- Prerequisites: modular arithmetic, prefix arrays; anti-hash awareness

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

Map a string to an integer (or pair of integers) so that equality of substrings becomes equality of hashes in O(1) after O(n) prefix prep:  
`H(s[l..r]) = (pref[r+1] - pref[l] * base^{len}) mod M`.

You trade determinism for speed and flexibility: any substring comparison, LCP via binary search + hash, lexicographic compare, distinct substring counting approximations, 2D hashes, etc.

**Collisions are real.** On CF, single mod `1e9+7` with fixed base is attackable. Prefer: double hash (two mods), random base at runtime, or `mod = 2^64` natural overflow **plus** awareness that it is also breakable in theory—still widely used with random odd base.

---

## 4. Proof Sketches & Recurrences

Fix base `b` and modulus `M`.  
`pref[0] = 0`, `pref[i+1] = pref[i]*b + s[i]` (map char to 1..σ to avoid leading-zero issues).  
`powb[0] = 1`, `powb[i+1] = powb[i]*b`.

Then `hash(l,r) = pref[r+1] - pref[l]*powb[r-l+1]` (mod M, bring to [0,M)).

**LCP of two suffixes i,j:** binary search maximal L with `hash(i,i+L-1)==hash(j,j+L-1)`.

**Collision probability:** for random hashes, ≈ `#comparisons / M`. Double hash ≈ product of moduli. Adversarial inputs need random base or cryptographic thinking—contests usually stop at double + random base.

---

## 5. Contest-Ready Implementation Templates

**Operational Complexity:** `- Preprocessing: O(n)
- Per-query / per-operation: O(1) substring hash; O(log n) LCP via binary search
- Total: depends on queries; typically O((n+q) log n) for many LCP compares
- Memory: O(n) per hash stream`

### C++17 Template

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

### Python 3 Template

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

## 6. Recognition Trigger Signals & Heuristics

- Substring equality / lexicographic compare under many queries
- Binary search on string length + equality checks (LCP, distinct count, matching)
- Palindrome checks without Manacher: hash(s[l..r]) == hash(reverse[n-1-r..n-1-l])
- “Sort all substrings” / compare cyclic shifts
- When SA/SAM would work but hash is enough and easier to code under time pressure
- Grid / path hashing; tree path hashes with binary lifting

---

## 7. Contest WA / TLE / RE Traps

- Mapping `'a'→0` causing leading-zero collisions on different lengths (use +1)
- Negative mod after subtraction without fixing
- Same base every run → hackable; forget second modulus
- Comparing hashes of different lengths without length check
- Building `pow` wrong for large n (overflow before mod)
- Using hash as “proof” of inequality direction for sorting without tie-break by real chars when hashes equal

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

- **Reverse hash** for palindromes
- **2D rolling hash** on matrices
- **Hash of multiset** (xor of random per value, or sorted polynomial)—different problem
- **Incremental hash** for sliding window anagrams / Rabin–Karp search
- **Tree / path hash** with binary lifting: hash down + hash up
- **Natural overflow `uint64_t`** single stream (fast; still randomize base)

---

## 11. Typical Problem Archetypes

1. Standard application: Rabin–Karp find pattern; substring equality queries
2. Slightly disguised: number of distinct substrings O(n²) loop with set of hashes (n≤5e3) or smarter
3. Difficult: lex smallest rotation; compare versions; binary search answer on string score
4. Very difficult / advanced: anti-hash resistant constructions; geometric hashing; heavy double/triple schemes under adversarial judges

---

## 12. Recognition & Identification Drills

1. q queries: given (l1,r1,l2,r2), test equality of two substrings.
2. Find longest substring that appears at least twice (non-overlapping or overlapping—variants).
3. Count palindromic substrings of even length only, using hashes (no Manacher).

---

## 13. Fast-Lookup Cheat Sheet

- When to use: default hammer for substring equality / lex compare under time pressure
- Key invariant: polynomial prefix structure enables O(1) range hash
- Key formula: `H(l,r) = pref[r+1] - pref[l]*b^{len}`
- Complexity: O(n) prep, O(1) get
- Template to remember: double hash + random base + 1-indexed char map

---

## 4. Manacher

---
