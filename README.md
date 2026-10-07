# Competitive Programming & Interview Mastery Portal

A modern, high-yield multi-track training portal designed for competitive programming mastery, contest simulations, and top-tier technical interview preparation. Built with **React + TypeScript + Tailwind CSS + Vite + KaTeX**.

🌐 **Live Website**: [https://singhvi28.github.io/competitive-programming/](https://singhvi28.github.io/competitive-programming/)

---

## 🎯 Tracks

### 1. [Codeforces Candidate Master Curriculum](https://singhvi28.github.io/competitive-programming/curriculum/)
- **Target Audience**: Expert (1600–1899) transitioning to Candidate Master (1900–2300).
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

### 2. [LeetCode Classified Hards Track](https://singhvi28.github.io/competitive-programming/leetcode-hards/)
- **Target Audience**: Top-tier tech interview candidates (Google, Meta, Citadel, Hudson River Trading, Jane Street, Databricks).
- **Curated Dataset**: **301 classified Hard problems** grouped into 3 signal tiers:
  - **Category 1 (Direct Interview Classics - 44 Problems)**: High ROI, frequently tested in tier-1 interviews (Company tagged).
  - **Category 2 (Niche Transferable Concepts - 128 Problems)**: High-concept patterns that unlock entire subcategories of tricky problems.
  - **Category 3 (CP-Tier & Exotic Hards - 129 Problems)**: Boundary-pushing competitive programming problems for high-frequency trading and maximum signal.
- **Extras**: Signal tier filtering, company tag search, concept filtering, checklist tracking.

### 3. [Codeforces Virtual Contests Library](https://singhvi28.github.io/competitive-programming/virtual-contests/)
- **Target Audience**: Competitive programmers drilling speed, consistency, and timed virtual contests.
- **Curated Dataset**: **237 modern Codeforces rounds** (Contest IDs 1315–2258):
  - **Div. 2 Rounds (154 Contests)**: Standard 2-hour rating battles.
  - **Educational Rounds (49 Contests)**: Standard concept-heavy practice rounds.
  - **Combined / Global Rounds (34 Contests)**: High-difficulty Div 1+2 & Global contests.
- **Extras**: 1-click virtual launch, problems & standings shortcuts, ID/Name search, type filters, and progress tracking.

### 4. [Codeforces Master Mirror](https://singhvi28.github.io/competitive-programming/mirror/)
- **Target Audience**: Serious competitors mirroring real training portfolios of top masters.
- **Curated Dataset**: **321 modern problems** (Contest ID $> 1300$, ratings $1900–2300$) solved by `a.out` and/or `Queue`:
  - **Solved by Both (21 Problems)**: Ultra high-consensus transition problems.
  - **Solved by `a.out` (204 Problems)**: Mastered by `a.out` with direct AC submission links.
  - **Solved by `Queue` (138 Problems)**: Mastered by `Queue` with direct AC submission links.
- **Extras**: Live Codeforces API solve synchronization for user handles (`akkisinghvi28` & `akshitsinghvi28`), solver filter tabs (Both, a.out, Queue), official tag filters, direct AC code shortcuts, and JSON progress backup.

---

## ⚡ Interactive Web Features
- **React + TypeScript + Vite** for component modularity and blazing fast client-side routing.
- **Dark Glassmorphic UI** with Tailwind CSS, Lucide icons, Inter & JetBrains Mono typography.
- **Pure KaTeX Math Rendering** for math formulas and complexity bounds without DOM race conditions.
- **Independent Progress Tracking** persisted via `localStorage` with JSON export/import.
- **Codeforces Live API Sync** on the Master Mirror page for automatic solve status tracking.
- **Instant Search & Multi-Filters** (`/` keyboard shortcut to focus search bar across all pages).

---

## 🛠️ Development & Build

```bash
# Install dependencies
npm install

# Start local dev server
npm run dev

# Type check & production build
npm run build
```

---

## 📂 Repository Structure
```
├── src/
│   ├── components/              # Reusable UI components
│   │   ├── common/              # Navbar, SearchBar, MathRenderer
│   │   ├── curriculum/          # ProblemCard, ModuleSection, Roadmap, GeometryCheatSheet
│   │   ├── leetcode/            # LeetCodeCard, CategorySection
│   │   ├── virtual/             # ContestCard
│   │   └── mirror/              # MirrorProblemCard
│   ├── context/                 # Global ToastContext & notifications
│   ├── data/                    # Curriculum, LeetCode, Virtuals, & Mirror JSON data
│   ├── hooks/                   # useLocalStorageSet hook
│   ├── pages/                   # HomePage, CurriculumPage, LeetCodeHardsPage, VirtualContestsPage, MirrorPage
│   ├── types/                   # TypeScript interfaces & types
│   ├── App.tsx                  # Root application router & layout
│   ├── main.tsx                 # React DOM mount point
│   └── index.css                # Tailwind CSS & global styles
├── .github/workflows/deploy.yml # Automated GitHub Pages CI/CD workflow
├── vite.config.ts               # Vite configuration with base path /competitive-programming/
├── tailwind.config.js           # Custom dark theme configuration
└── package.json                 # Project dependencies & scripts
```
