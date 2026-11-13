<div align="center">

# Master's DSA Sheet & Study Ecosystem

**A production-grade curriculum, interactive tracker, and comprehensive theoretical handbook for technical interviews.**

[![Deploy to GitHub Pages](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml/badge.svg)](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml)
[![Live Web Application](https://img.shields.io/badge/Live%20App-GitHub%20Pages-00c853?style=flat&logo=github)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Curated Problems](https://img.shields.io/badge/Curated%20Problems-486%20Problems-007acc?style=flat&logo=leetcode)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Curriculum Modules](https://img.shields.io/badge/Curriculum-20%20Modules-7952b3?style=flat)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Theoretical Handbook](https://img.shields.io/badge/Handbook-30%20Chapters-ff6f00?style=flat&logo=gitbook)](./handbook/)
[![Offline Workbook](https://img.shields.io/badge/Workbook-GFG%20450%20Excel-2e7d32?style=flat&logo=microsoftexcel)](./MY_GFG-450.xlsx)

[**Launch Live Tracker**](https://premnarayn13.github.io/DSA_StudyMaterial/) &nbsp;•&nbsp; [**Handbook Documentation**](./handbook/) &nbsp;•&nbsp; [**Offline Workbook**](./MY_GFG-450.xlsx) &nbsp;•&nbsp; [**Report an Issue**](https://github.com/premnarayn13/DSA_StudyMaterial/issues)

</div>

---

## Ecosystem Overview

This repository provides a unified, end-to-end preparation platform designed for software engineers preparing for competitive programming and technical interviews. The material combines three distinct pillars:

1. **Interactive Web Tracker:** A zero-dependency, client-side web application hosting **486 vetted problems** across **20 modules** with real-time multi-filtering, local progress persistence, and sub-millisecond search.
2. **Theoretical Handbook:** A **30-chapter deep dive** covering asymptotic analysis, low-level memory representation, pointer mechanics, and advanced algorithmic design patterns.
3. **Offline Milestone Workbook:** An integrated Excel workbook ([`MY_GFG-450.xlsx`](./MY_GFG-450.xlsx)) equipped with milestone formulas, revision tags, and attempt metrics for offline study.

| Metric | Specification | Engineering Details |
|:---|:---|:---|
| **Total Curated Problems** | **486 Problems** | Strict deduplication, standard interview variations only |
| **Curriculum Coverage** | **20 Structured Modules** | From foundational math and bit manipulation to advanced DP and graphs |
| **Handbook Scope** | **30 Deep Chapters** | Formal proofs, complexity bounds, and multi-language implementations |
| **Primary Platform Routing** | **255 LeetCode Links** | Direct access to official LeetCode problems |
| **Secondary Platform Routing** | **198 GeeksforGeeks Links** | Verified practice problem mirrors |
| **Data Privacy & Storage** | **100% Client-Side** | Zero remote tracking, powered by browser `localStorage` |

---

## Interactive Tracker Features

The web tracker is engineered with vanilla HTML5, CSS3, and ES6 JavaScript, eliminating build steps, framework bloat, and runtime overhead.

* **Deterministic Link Precedence:** Every problem directs to **LeetCode** as primary. If unavailable, it resolves to a verified **GeeksforGeeks** problem page, followed by **TakeUForward** practice mirrors.
* **Persistent Local State:** Marked checkmarks, starred bookmarks, and custom notes reside exclusively within browser `localStorage` (`a2z.solved`, `a2z.starred`, `a2z.theme`). Your data stays on your machine.
* **Instant Search Engine:** Sub-millisecond substring queries across problem titles, topic categories, and module names without DOM rebuilds.
* **Granular Multi-Filtering:** Intersect filters by difficulty level, problem tier, platform source, and solved status simultaneously.
* **Responsive Theming:** Native Light and Dark themes with automated system preference detection.
* **Data Portability:** Single-click JSON export and import for seamless progress backup or migration across devices.

### Filter Specifications

| Filter Type | Options | Purpose |
|:---|:---|:---|
| **Difficulty** | **All**, **Easy**, **Medium**, **Hard** | Target problems matching your current preparation phase |
| **Problem Tier** | **Basic**, **Core**, **Pro** | Differentiate fundamental concepts from advanced interview challenges |
| **Platform** | **LeetCode**, **GeeksforGeeks**, **TakeUForward** | Focus practice on your preferred coding environment |
| **Status** | **All**, **Solved**, **Unsolved**, **Starred** | Manage backlogs, revision targets, and bookmarked problems |

### Keyboard Shortcuts

| Key | Operation | Action Description |
|:---:|:---|:---|
| <kbd>/</kbd> | **Focus Search** | Highlights global search bar from anywhere on the page |
| <kbd>j</kbd> | **Navigate Down** | Moves the cursor highlight down to the next problem row |
| <kbd>k</kbd> | **Navigate Up** | Moves the cursor highlight up to the previous problem row |
| <kbd>s</kbd> | **Toggle Solved** | Inverts the completion checkbox of the highlighted problem |
| <kbd>Esc</kbd> | **Clear / Close** | Resets active search filter or closes the active details drawer |

### Client-Side State Management

The application operates without backend servers or user authentication. All progress is isolated to your browser via Web Storage APIs:

| Key Name | Storage Type | Content Stored |
|:---|:---|:---|
| `a2z.solved` | `localStorage` JSON String | Set of unique problem IDs marked as completed by the user |
| `a2z.starred` | `localStorage` JSON String | Set of unique problem IDs flagged for revision or follow-up |
| `a2z.theme` | `localStorage` String | Active UI theme setting (`light` or `dark`) |

---

## Curriculum Syllabus

The curriculum organizes **486 problems** across **20 modules**, ensuring comprehensive coverage from fundamental data manipulation to advanced graph and dynamic programming theorems.

| # | Module | Problems | Key Algorithms & Landmark Problems |
|:---:|:---|:---:|:---|
| **01** | **Beginner Problems** | `16` | Armstrong check, prime testing, Euclidean GCD, divisor enumeration |
| **02** | **Sorting Algorithms** | `5` | Bubble, Selection, Insertion, Merge Sort, Quick Sort divide & conquer |
| **03** | **Arrays** | `42` | Kadane's algorithm, Dutch National Flag, Next Permutation, Spiral Matrix |
| **04** | **Strings** | `20` | Palindromic substrings, Roman conversions, bracket balancing, expand center |
| **05** | **Hashing** | `5` | Prefix sum hash maps, longest consecutive sequence, XOR subarray counting |
| **06** | **Binary Search** | `45` | Lower/Upper bound, Rotated search, Koko Bananas, Median of sorted arrays |
| **07** | **Recursion & Backtracking** | `29` | Subsets, Combination Sum, N-Queens, Sudoku Solver, Expression Add Operators |
| **08** | **Linked-List** | `27` | Tortoise & Hare cycle detection, reverse in K-groups, copy random list |
| **09** | **Bit Manipulation** | `7` | Single number variations, bitmask subsets, range XOR properties |
| **10** | **Greedy Algorithms** | `16` | N-Meetings, Job sequencing, Jump Game I & II, Fractional Knapsack, Candy |
| **11** | **Sliding Window / 2 Pointer** | `12` | Longest substring with K distinct, Min Window Substring & Subsequence |
| **12** | **Stack / Queues** | `31` | Monotonic Stack, Next Greater Element, Trapping Rainwater, LRU/LFU Cache |
| **13** | **Binary Trees** | `41` | Vertical/Spiral order, Diameter, LCA, Morris Traversal, Tree Serialisation |
| **14** | **Binary Search Trees** | `18` | BST validation, Inorder predecessor/successor, Two Sum in BST, Largest BST |
| **15** | **Heaps & Priority Queues** | `22` | Kth Largest, Task Scheduler, Design Twitter, Merge K Lists, Median Stream |
| **16** | **Graphs** | `51` | Multi-source BFS, Kahn's Algo, Dijkstra, Bellman-Ford, Floyd-Warshall, Kosaraju |
| **17** | **Dynamic Programming** | `54` | Grid paths, 0/1 & Unbounded Knapsack, LCS, LIS variants, MCM partitioning |
| **18** | **Tries** | `6` | Prefix trees, longest word with all prefixes, maximum XOR queries |
| **19** | **Strings (Advanced Algo)** | `36` | KMP pattern matcher, Rabin-Karp rolling hash, Z-algorithm, Word Wrap |
| **20** | **Maths & Number Theory** | `3` | Sieve of Eratosthenes, Prime factorisation, Prime range counting |
| **—** | **Complete Curriculum** | **486** | **Standard Technical Interview Standard** |

### Problem Tier Stratification

To help engineers prioritize study time efficiently, every problem is classified into one of three distinct tiers:

* **Basic Tier:** Foundational syntax, boundary checks, and standard implementation patterns required for baseline technical literacy.
* **Core Tier:** Landmark interview questions and recurring canonical patterns asked in 80%+ of top-tier software engineering assessments.
* **Pro Tier:** High-complexity challenges requiring multi-paradigm combinations, optimal state reductions, and advanced tree/graph theorems.

---

## Theoretical Handbook Structure

The [`handbook/`](./handbook/) contains 30 dedicated chapters organized into 6 progressive study phases. Each chapter provides mathematical proofs, memory layout representations, and code implementations:

| Phase | Focus Domain | Chapters | Core Topics & Algorithmic Principles |
|:---|:---|:---:|:---|
| **Phase 1** | **Foundations & Complexity** | `01–02, 23–24` | Big-O/Big-Ω/Big-Θ proofs, Master Theorem, number theory, Java memory model |
| **Phase 2** | **Linear Structures** | `03–04, 10, 13–15` | Memory alignment, sliding window templates, two pointers, monotonic queues |
| **Phase 3** | **Tree Hierarchies** | `16–18, 25–26` | Tree traversals, LCA, Morris traversal, BST properties, AVL & Red-Black trees |
| **Phase 4** | **Graph Networks** | `19, 28` | BFS/DFS, topological sort, Dijkstra, Bellman-Ford, Floyd-Warshall, DSU |
| **Phase 5** | **Algorithmic Paradigms** | `05–09, 11–12` | Divide & conquer, state-space recursion, pruning, greedy choice property |
| **Phase 6** | **Dynamic Programming & Advanced** | `20–22, 27, 29–30` | 1D/2D DP, MCM, KMP string matching, Segment Trees, Fenwick Trees, Branch & Bound |

### Core Handbook Tenets

* **Mathematical Rigor:** Derivations of worst-case, average-case, and amortized complexity bounds.
* **Low-Level Memory Architecture:** Contrast between contiguous cache-friendly arrays and pointer-linked node structures.
* **Edge-Case Checklists:** Explicit coverage of off-by-one errors, recursion depth limits, integer overflow, and empty collections.
* **Implementation Blueprints:** Idiomatic implementations in **C++** and **Java** accompanied by step-by-step trace tables.

---

## Structured Preparation Blueprint

A phased study trajectory designed to optimize problem retention and interview readiness over a 12-to-16 week preparation window:

| Preparation Stage | Target Modules | Primary Objectives | Recommended Target |
|:---|:---|:---|:---:|
| **Stage 1: Core Fundamentals** | Modules 01 – 05 | Asymptotic bounds, array operations, prefix hashing, string manipulation | **4 – 5 problems / day** |
| **Stage 2: Linear & Hierarchical** | Modules 06 – 14 | Binary search spaces, recursion trees, linked lists, stacks, and tree views | **3 – 4 problems / day** |
| **Stage 3: Advanced Optimization** | Modules 15 – 16 | Priority queue construction, graph traversals, shortest path algorithms | **3 – 4 problems / day** |
| **Stage 4: Dynamic Programming** | Modules 17 – 20 | Subsequence DP, grid optimization, MCM partitioning, Trie lookups | **2 – 3 problems / day** |

---

## Offline Practice Workbook

For engineers who track progress via spreadsheets or offline workbooks, the repository includes [`MY_GFG-450.xlsx`](./MY_GFG-450.xlsx):

* **Pre-Populated Problem Inventory:** Categorized by topic, algorithmic pattern, and technical difficulty.
* **Attempt & Timing Logs:** Columns dedicated to recording problem-solving time and repeat attempt counts.
* **Review Status Flags:** Tag problems as **Needs Review**, **Tricky Edge-Case**, or **Mastered**.
* **Formula-Driven Progress:** Automated completion percentages and daily milestone velocity trackers.

---

## Local Development & Setup

The web application is pure static web technology. It requires no Node.js runtime, npm dependencies, or compilation steps.

### Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/premnarayn13/DSA_StudyMaterial.git

# 2. Navigate to the project root
cd DSA_StudyMaterial

# 3. Start a local HTTP server
python -m http.server 8000
```

Open your browser and navigate to:

```text
http://localhost:8000/Problems_List/site/
```

> **Important:** Running through an HTTP server (rather than double-clicking `index.html`) avoids browser CORS restrictions when fetching `data.json` over the `file://` protocol.

### Alternative Static Servers

```bash
# Using Node.js npx
npx serve Problems_List/site

# Using PHP built-in server
php -S localhost:8000 -t Problems_List/site
```

---

## Repository Architecture

```text
DSA_StudyMaterial/
├── .github/workflows/
│   └── deploy.yml              # CI/CD validation, asset versioning & GitHub Pages release
├── handbook/                   # 30 Theoretical chapters with proofs, layouts & code
│   ├── chapter-01-introduction-to-dsa/
│   ├── chapter-03-arrays/
│   ├── chapter-19-graphs/
│   ├── chapter-20-dynamic-programming/
│   └── ...
├── Problems_List/
│   ├── scripts/                # Data integrity validation and statistics checking tools
│   │   ├── verify_site_data.py # Validates problem counts, sequence, and URLs
│   │   └── check_readme.py     # Ensures README metrics match data.json exactly
│   └── site/                   # Web application frontend
│       ├── index.html          # Semantic HTML5 layout
│       ├── styles.css          # Design tokens and theme definitions
│       ├── app.js              # State management, filter engine & keyboard handlers
│       └── data.json           # 486 Curated problem entries and metadata
├── MY_GFG-450.xlsx             # Offline revision tracking workbook
└── README.md                   # Repository documentation
```

---

## Automated Deployment Pipeline

All updates committed to the `master` branch trigger the GitHub Actions workflow located at [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml):

```text
[ Push to master branch ]
            │
            ▼
[ Step 1: verify_site_data.py ] ──► Validates 486 problems, IDs, sequential order & URLs
            │
            ▼
[ Step 2: check_readme.py ]     ──► Validates that documentation metrics match data.json
            │
            ▼
[ Step 3: Asset Stamping ]      ──► Injects cache-busting hashes into script and CSS tags
            │
            ▼
[ Step 4: Publish to gh-pages ] ──► Deploys production bundle to premnarayn13.github.io
```

| Pipeline Stage | Executed Command | Quality Assurance Gate |
|:---|:---|:---|
| **Data Integrity Verification** | `python Problems_List/scripts/verify_site_data.py` | Confirms all 486 problems have valid URLs, sequential IDs, and valid platforms |
| **Metric Consistency Guard** | `python Problems_List/scripts/check_readme.py` | Recomputes 12 metadata statistics and halts build if numbers disagree |
| **Asset Cache Stamping** | `python Problems_List/scripts/stamp_assets.py` | Injects SHA hashes into `styles.css` and `app.js` to eliminate stale browser caches |
| **Production Publication** | `actions/deploy-pages` | Publishes static bundle directly to the `gh-pages` deployment branch |

---

## Frequently Asked Questions

<details>
<summary><b>1. Where is my practice progress stored?</b></summary>
<br/>
Progress is stored 100% locally within your browser's <code>localStorage</code> under isolated keys (<code>a2z.solved</code>, <code>a2z.starred</code>, <code>a2z.theme</code>). It persists permanently across browser restarts, updates, and machine reboots.
</details>

<details>
<summary><b>2. Will other visitors opening the hosted link affect my checklist?</b></summary>
<br/>
No. Because progress is stored entirely client-side in your own browser, every visitor maintains an isolated, independent checklist. No data is transmitted to or shared across remote devices.
</details>

<details>
<summary><b>3. How can I transfer my solved problems to another device?</b></summary>
<br/>
Click the <b>•••</b> menu button in the top-right navbar, select <b>Export progress</b> to download a compact <code>.json</code> state file, and click <b>Import progress</b> on your secondary computer to restore or merge your records.
</details>

<details>
<summary><b>4. How were duplicate and trivial problems handled?</b></summary>
<br/>
The curriculum underwent strict deduplication. Elementary syntax tutorials (such as hello-world style loops and redundant wrappers) were removed, while all standard, high-frequency interview problems across LeetCode and GeeksforGeeks were preserved and expanded.
</details>

<details>
<summary><b>5. Can I use the application completely offline?</b></summary>
<br/>
Yes. Once cloned locally, running <code>python -m http.server 8000</code> gives you complete access to the problem directory, search engine, filter matrix, and progress tracking with zero internet connectivity required.
</details>

<details>
<summary><b>6. What distinguishes this tracker from static PDF or markdown sheets?</b></summary>
<br/>
Static sheets rot quickly when links break or problems are re-categorized. This ecosystem enforces automated CI/CD link validation, multi-platform mirrors, instant sub-millisecond filtering by tier and difficulty, and local progress tracking without requiring account logins.
</details>

---

<div align="center">

**Master's DSA Sheet & Study Ecosystem** • Maintained for Engineers Preparing for High-Bar Technical Interviews.

</div>
