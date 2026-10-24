# Section §09: Network Flow & Matchings

> **Module ID:** `sec-09`  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Topic Count:** 20  

**Module Summary:** Dinic's blocking flow algorithm, Min-Cut theorem & project selection closures, Bipartite matching (Kuhn / Hopcroft-Karp), MCMF with SPFA/Potentials, and Demands.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | Max Flow (Ford–Fulkerson / Edmonds–Karp) | `A-tier` | 1800–2400 | Occasional | [01-09-max-flow-ford-fulkerson-edmonds-karp.md](./01-09-max-flow-ford-fulkerson-edmonds-karp.md) |
| 2 | Dinic’s Algorithm | `A-tier` | 1900–2500 | Occasional | [02-09-dinic-s-algorithm.md](./02-09-dinic-s-algorithm.md) |
| 3 | \(s\)–\(t\) Min Cut | `A-tier` | 1900–2500 | Occasional | [03-09-s-t-min-cut.md](./03-09-s-t-min-cut.md) |
| 4 | Bipartite Cardinality Matching (Kuhn) | `S-tier` | 1600–2200 | Common | [04-09-bipartite-cardinality-matching-kuhn.md](./04-09-bipartite-cardinality-matching-kuhn.md) |
| 5 | Hopcroft–Karp | `B-tier` | 2000–2500 | Occasional | [05-09-hopcroft-karp.md](./05-09-hopcroft-karp.md) |
| 6 | Min-Cost Max-Flow (MCMF) | `B-tier` | 2100–2700 | Occasional | [06-09-min-cost-max-flow-mcmf.md](./06-09-min-cost-max-flow-mcmf.md) |
| 7 | Flows with Lower Bounds on Edges | `C-tier` | 2300–2900 | Rare | [07-09-flows-with-lower-bounds-on-edges.md](./07-09-flows-with-lower-bounds-on-edges.md) |
| 8 | Circulation (Feasibility / Balances) | `C-tier` | 2300–2900 | Rare | [08-09-circulation-feasibility-balances.md](./08-09-circulation-feasibility-balances.md) |
| 9 | Vertex Capacities (Node Split) | `B-tier` | 2000–2500 | Occasional | [09-09-vertex-capacities-node-split.md](./09-09-vertex-capacities-node-split.md) |
| 10 | Edge-Disjoint & Vertex-Disjoint Paths | `A-tier` | 1800–2400 | Occasional | [10-09-edge-disjoint-vertex-disjoint-paths.md](./10-09-edge-disjoint-vertex-disjoint-paths.md) |
| 11 | Flow Modeling Recognition (Meta-Skill) | `S-tier` | 1800–2500 | Common | [11-09-flow-modeling-recognition-meta-skill.md](./11-09-flow-modeling-recognition-meta-skill.md) |
| 12 | What to drill this week | `B-tier` | 1600–2200 | Common | [12-09-what-to-drill-this-week.md](./12-09-what-to-drill-this-week.md) |
| 13 | Hungarian Algorithm (Kuhn-Munkres) | `B-tier` | 2100–2600 | Occasional | [13-09-hungarian-algorithm-kuhn-munkres.md](./13-09-hungarian-algorithm-kuhn-munkres.md) |
| 14 | Dinic vs Edmonds–Karp | `B-tier` | 1600–2200 | Common | [14-09-dinic-vs-edmonds-karp.md](./14-09-dinic-vs-edmonds-karp.md) |
| 15 | Dinic vs Hopcroft–Karp | `B-tier` | 1600–2200 | Common | [15-09-dinic-vs-hopcroft-karp.md](./15-09-dinic-vs-hopcroft-karp.md) |
| 16 | Matching vs General Flow | `B-tier` | 1600–2200 | Common | [16-09-matching-vs-general-flow.md](./16-09-matching-vs-general-flow.md) |
| 17 | MCMF vs Greedy | `B-tier` | 1600–2200 | Common | [17-09-mcmf-vs-greedy.md](./17-09-mcmf-vs-greedy.md) |
| 18 | High-ROI (master first) | `B-tier` | 1600–2200 | Common | [18-09-high-roi-master-first.md](./18-09-high-roi-master-first.md) |
| 19 | Situational (learn when patterns appear) | `B-tier` | 1600–2200 | Common | [19-09-situational-learn-when-patterns-appear.md](./19-09-situational-learn-when-patterns-appear.md) |
| 20 | Rarely worth early / Niche | `B-tier` | 1600–2200 | Common | [20-09-rarely-worth-early-niche.md](./20-09-rarely-worth-early-niche.md) |
