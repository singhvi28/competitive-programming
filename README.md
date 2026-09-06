# Competitive Programming & Interview Mastery Portal

A curated, high-yield dual-track training portal designed for competitive programming mastery and top-tier technical interview preparation.

🌐 **Live Website**: [https://singhvi28.github.io/competitive-programming/](https://singhvi28.github.io/competitive-programming/)

---

## 🎯 Tracks

### 1. [Codeforces Master Transition Curriculum](https://singhvi28.github.io/competitive-programming/curriculum)
- **Target Audience**: Expert (1600–1899) transitioning to Candidate Master / Master (1900–2300).
- **Curated Dataset**: **144 verified modern problems** (Contest ID $\ge 1300$, ratings $1900–2300$).
- **Modules**:
  1. Tree Decompositions, HLD & Centroid Decomposition
  2. Cartesian Trees, Monotonic Stacks & Offline Reductions
  3. Randomization, 64-bit Polynomial Hashing & Implicit Treaps
  4. Advanced DP Optimizations (Fenwick DP, Quotient Splitting, Monotonic Transitions)
  5. Graph Structure, Tarjan Bridges & 2-SAT Implication Graphs
  6. Network Flow, Dinic's Algorithm, Hall's Condition & Min-Cost Flow
  7. Computational Geometry (Chebyshev Rotations, Angular Sweeps, Pick's Theorem)
  8. Linear Basis ($\mathbb{F}_2$), Bit-Trie D&C & Number Theory
- **Extras**: 6-Week Structured Training Roadmap, Geometry Cheat Sheet, Problem Search & Filters.

### 2. [LeetCode Classified Hards Track](https://singhvi28.github.io/competitive-programming/leetcode-hards)
- **Target Audience**: Top-tier tech interview candidates (Google, Meta, Citadel, Hudson River Trading, Jane Street, Databricks).
- **Curated Dataset**: **301 classified Hard problems** grouped into 3 signal tiers:
  - **Category 1 (Direct Interview Classics - 44 Problems)**: High ROI, frequently tested in tier-1 interviews (Company tagged).
  - **Category 2 (Niche Transferable Concepts - 128 Problems)**: High-concept patterns that unlock entire subcategories of tricky problems.
  - **Category 3 (CP-Tier & Exotic Hards - 129 Problems)**: Boundary-pushing competitive programming problems for high-frequency trading and maximum signal.
- **Extras**: Signal tier filtering, company tag search, concept filtering, checklist tracking.

---

## ⚡ Interactive Web Features
- **Dark Cyberpunk UI** with Tailwind CSS & Glassmorphism
- **Independent Progress Tracking** persisted via `localStorage`
- **Instant Search & Multi-Filters** (Rating, Category, Topic, Company, Status)
- **Mathematical Formula Rendering** with KaTeX
- **Progress Export & Import** (JSON backups)
- **Responsive Navigation** across all portal sub-routes

---

## 📂 Repository Structure
```
├── index.html                   # Central Portal Landing Page
├── curriculum/
│   └── index.html               # Codeforces Master Curriculum Page
├── curriculum.html              # Fallback / Direct Link
├── leetcode-hards/
│   └── index.html               # LeetCode Classified Hards Page
├── leetcode-hards.html          # Fallback / Direct Link
├── data.json                    # Codeforces 144 Problems & Schedule Data
├── leetcode_data.json           # LeetCode 301 Classified Problems Data
└── .nojekyll                    # Disable Jekyll for raw static asset serving
```
