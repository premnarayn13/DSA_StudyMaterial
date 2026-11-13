# Master's DSA Study Material & Interactive Problem Tracker

[![Deploy to GitHub Pages](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml/badge.svg)](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml)
[![Live Web Application](https://img.shields.io/badge/Live%20App-GitHub%20Pages-brightgreen?style=flat&logo=github)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Curated Problems](https://img.shields.io/badge/Curated%20Problems-486%20Problems-blue)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Modules Covered](https://img.shields.io/badge/Modules-20%20Topics-blueviolet)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Theoretical Handbook](https://img.shields.io/badge/Handbook-30%20Chapters-orange)](./handbook/)
[![Practice Sheet](https://img.shields.io/badge/Workbook-GFG%20450%20Excel-success)](./MY_GFG-450.xlsx)

A production-grade, all-in-one Data Structures & Algorithms ecosystem. This repository pairs **Master's DSA Sheet**—a dependency-free, high-speed interactive tracker—with a comprehensive **30-chapter DSA handbook** and structured revision workbooks for interview preparation.

🌐 **Live Web Application:** [https://premnarayn13.github.io/DSA_StudyMaterial/](https://premnarayn13.github.io/DSA_StudyMaterial/)

---

## 🎯 Master's DSA Sheet (Interactive Tracker)

The repository hosts a client-side single-page application engineered for focused problem solving and progress tracking:

* **486 Curated Problems across 20 Modules:** Thoroughly audited syllabus covering foundational mathematics, arrays, strings, binary search, trees, graphs, dynamic programming, heaps, and advanced algorithmic patterns.
* **Smart Platform Routing:** Verified direct links to **LeetCode** (primary), **GeeksforGeeks**, and **TakeUForward** practice pages, with alternate mirrors available for each problem.
* **Zero Backend, Local Persistence:** Problem completion statuses, starred items, and theme preferences reside solely in browser `localStorage`. No accounts, no telemetry, and complete privacy.
* **Multi-Dimensional Filtering & Search:** Instant sub-millisecond search across problem titles, subtopics, and module tags. Filter concurrently by difficulty (*Easy*, *Medium*, *Hard*), platform, tier (*Basic*, *Core*, *Pro*), and status.
* **Keyboard-First Workflow:**
  * `/` : Jump immediately to search
  * `j` / `k` : Navigate problems down and up
  * `s` : Toggle solved status for active problem
  * `Esc` : Clear search and close modal views
* **Progress Portability:** Built-in JSON export and import to backup, transfer, or sync progress between devices without external servers.

---

## 📚 Complete DSA Theoretical Handbook

Located in the [`handbook/`](./handbook/) directory, this 30-chapter guide provides rigorous explanations of core algorithmic principles:

* **Foundational Analysis:** Time and space asymptotic complexity, Big-O/Big-Ω/Big-Θ proofs, and recursion call stack mechanics.
* **Linear & Non-Linear Structures:** Detailed memory layouts and pointer mechanics for Arrays, Strings, Linked Lists, Stacks, Queues, Binary Trees, and BSTs.
* **Advanced & Competitive Structures:** Implementation breakdowns for Heaps, Tries, Disjoint Set Union (DSU), Segment Trees, Fenwick Trees (BIT), AVL Trees, and Red-Black Trees.
* **Algorithmic Paradigms:** In-depth blueprints for Divide & Conquer, Backtracking, Greedy Optimization, Dynamic Programming (1D, 2D, Grids, Subsequences, MCM), and Graph Algorithms (BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, Kosaraju's SCC, Topological Sort).

---

## 📊 Offline Practice Workbook

The repository includes [`MY_GFG-450.xlsx`](./MY_GFG-450.xlsx), a dedicated offline milestone and revision tracking spreadsheet tailored for interview schedules and daily problem-solving targets.

---

## 📂 Repository Architecture

```text
DSA_StudyMaterial/
├── .github/workflows/
│   └── deploy.yml              # Automated build, validation & GitHub Pages deployment
├── handbook/                   # 30 Comprehensive theory chapters with code & proofs
│   ├── chapter-01-introduction-to-dsa/
│   ├── chapter-03-arrays/
│   ├── chapter-19-graphs/
│   └── ...
├── Problems_List/
│   ├── scripts/                # Data validation and integrity verification tooling
│   └── site/                   # Web app frontend (Vanilla HTML5, CSS3, ES6 JS)
│       ├── index.html          # Application layout
│       ├── styles.css          # Design system & dark/light theme tokens
│       ├── app.js              # Client-side state, filtering & keyboard engine
│       └── data.json           # 486 Curated problems & platform metadata
├── MY_GFG-450.xlsx             # Offline revision tracking workbook
└── README.md                   # Repository documentation
```

---

## 💻 Local Development & Offline Access

The interactive tracker requires no build tools, compilers, or third-party package dependencies:

```bash
# Clone the repository
git clone https://github.com/premnarayn13/DSA_StudyMaterial.git
cd DSA_StudyMaterial

# Start any standard local HTTP server
python -m http.server 8000
```

Navigate to `http://localhost:8000/Problems_List/site/` in any modern web browser.

---

## 🚀 Continuous Deployment

Every commit pushed to the `master` branch triggers the GitHub Actions CI/CD pipeline (`.github/workflows/deploy.yml`):
1. **Validation:** Checks dataset consistency and validates problem link integrity (`verify_site_data.py`).
2. **Metadata Sync:** Ensures documentation metrics match dataset values (`check_readme.py`).
3. **Cache Stamping:** Injects cache-busting version identifiers for static assets.
4. **Publishing:** Deploys the production bundle automatically to the `gh-pages` branch.
