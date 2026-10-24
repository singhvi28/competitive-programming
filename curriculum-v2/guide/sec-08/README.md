# Section §08: Advanced Graphs (Shortest Paths, MST, Euler)

> **Module ID:** `sec-08`  
> **Phase:** Phase 4 — Graph Algorithms & Network Flow  
> **Topic Count:** 19  

**Module Summary:** Dijkstra variants, 0-1 BFS, Floyd-Warshall, DAG paths, Functional graphs, Kruskal reconstruction tree, and Eulerian path construction.

---

## Topics in this Section

| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |
|---|---|---|---|---|---|
| 1 | Dijkstra Variants | `S-tier` | 1400–2100 (variants to 2500+) | Very Common | [01-08-dijkstra-variants.md](./01-08-dijkstra-variants.md) |
| 2 | 0-1 BFS | `A-tier` | 1500–2100 | Common | [02-08-0-1-bfs.md](./02-08-0-1-bfs.md) |
| 3 | Bellman–Ford | `A-tier` | 1500–2100 | Occasional | [03-08-bellman-ford.md](./03-08-bellman-ford.md) |
| 4 | SPFA (Including Why It Is Dangerous) | `C-tier` | 1600–2200 (avoid) | Rare (as a *good* choice); historically overused | [04-08-spfa-including-why-it-is-dangerous.md](./04-08-spfa-including-why-it-is-dangerous.md) |
| 5 | Floyd–Warshall | `A-tier` | 1400–2000 | Common | [05-08-floyd-warshall.md](./05-08-floyd-warshall.md) |
| 6 | DAG Shortest Paths | `A-tier` | 1500–2000 | Common | [06-08-dag-shortest-paths.md](./06-08-dag-shortest-paths.md) |
| 7 | Multi-Source Shortest Paths | `A-tier` | 1500–2100 | Common | [07-08-multi-source-shortest-paths.md](./07-08-multi-source-shortest-paths.md) |
| 8 | Johnson’s Algorithm | `C-tier` | 2200–2700 | Rare | [08-08-johnson-s-algorithm.md](./08-08-johnson-s-algorithm.md) |
| 9 | Dijkstra vs 0-1 BFS vs Bellman–Ford | `B-tier` | 1600–2200 | Common | [09-08-dijkstra-vs-0-1-bfs-vs-bellman-ford.md](./09-08-dijkstra-vs-0-1-bfs-vs-bellman-ford.md) |
| 10 | Why SPFA Is Dangerous | `B-tier` | 1600–2200 | Common | [10-08-why-spfa-is-dangerous.md](./10-08-why-spfa-is-dangerous.md) |
| 11 | Kruskal Reconstruction vs HLD for Path Max | `B-tier` | 1600–2200 | Common | [11-08-kruskal-reconstruction-vs-hld-for-path-max.md](./11-08-kruskal-reconstruction-vs-hld-for-path-max.md) |
| 12 | Borůvka Niche | `B-tier` | 1600–2200 | Common | [12-08-bor-vka-niche.md](./12-08-bor-vka-niche.md) |
| 13 | Part A — [08-a-shortest-paths.md](08-a-shortest-paths.md) | `B-tier` | 1600–2200 | Common | [13-08-part-a-08-a-shortest-paths-md-08-a-shortest-paths-md.md](./13-08-part-a-08-a-shortest-paths-md-08-a-shortest-paths-md.md) |
| 14 | Part B — [08-b-mst-euler-functional.md](08-b-mst-euler-functional.md) | `B-tier` | 1600–2200 | Common | [14-08-part-b-08-b-mst-euler-functional-md-08-b-mst-euler-functional-md.md](./14-08-part-b-08-b-mst-euler-functional-md-08-b-mst-euler-functional-md.md) |
| 15 | Minimum Spanning Tree Variants | `A-tier` | 1400–2200 | Common | [15-08-minimum-spanning-tree-variants.md](./15-08-minimum-spanning-tree-variants.md) |
| 16 | Kruskal Reconstruction Tree | `B-tier` | 2100–2700 | Occasional | [16-08-kruskal-reconstruction-tree.md](./16-08-kruskal-reconstruction-tree.md) |
| 17 | Borůvka | `C-tier` | 2000–2600 | Rare | [17-08-bor-vka.md](./17-08-bor-vka.md) |
| 18 | Eulerian Paths / Circuits | `A-tier` | 1700–2300 | Occasional | [18-08-eulerian-paths-circuits.md](./18-08-eulerian-paths-circuits.md) |
| 19 | Functional Graphs | `A-tier` | 1600–2200 | Common | [19-08-functional-graphs.md](./19-08-functional-graphs.md) |
