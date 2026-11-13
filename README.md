<div align="center">

# Master's DSA Sheet & Study Ecosystem

[![Deploy to GitHub Pages](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml/badge.svg)](https://github.com/premnarayn13/DSA_StudyMaterial/actions/workflows/deploy.yml)
[![Live Web Application](https://img.shields.io/badge/Live%20App-GitHub%20Pages-00c853?style=for-the-badge&logo=github)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Curated Problems](https://img.shields.io/badge/Curated%20Problems-486%20Problems-007acc?style=for-the-badge&logo=leetcode)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Curriculum Modules](https://img.shields.io/badge/Curriculum-20%20Modules-7952b3?style=for-the-badge)](https://premnarayn13.github.io/DSA_StudyMaterial/)
[![Theoretical Handbook](https://img.shields.io/badge/Handbook-30%20Chapters-ff6f00?style=for-the-badge&logo=gitbook)](./handbook/)
[![Offline Workbook](https://img.shields.io/badge/Workbook-GFG%20450%20Excel-2e7d32?style=for-the-badge&logo=microsoftexcel)](./MY_GFG-450.xlsx)

<br/>

</div>

> ### 🚀 [**Launch Live Tracker: https://premnarayn13.github.io/DSA_StudyMaterial/**](https://premnarayn13.github.io/DSA_StudyMaterial/)
> **Instant interactive progress tracker with verified LeetCode & GFG links, one-click checkboxes, instant search, and zero backend tracking.**

<div align="center">

| 🎯 Curated Problems | 🗂️ Curriculum Modules | 📖 Handbook Chapters | 💻 LeetCode Direct | 🟢 GeeksforGeeks | 💾 Data Privacy |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **486 Problems** | **20 Modules** | **30 Chapters** | **255 Verified** | **198 Verified** | **100% LocalStorage** |

</div>

---

## Direct Navigation Links

Access the primary components of this ecosystem immediately:

* 🚀 **[Live Web Application](https://premnarayn13.github.io/DSA_StudyMaterial/):** Interactive tracker with checkboxes, search, filters, and keyboard navigation.
* 📚 **[Theory Handbook Directory](./handbook/):** 30 deep-dive chapters with mathematical proofs, memory diagrams, and code.
* 📊 **[Offline Revision Workbook](./MY_GFG-450.xlsx):** Excel spreadsheet for offline milestone and revision tracking.
* 🛠️ **[Automated Deploy Workflow](./.github/workflows/deploy.yml):** GitHub Actions CI/CD pipeline for GitHub Pages deployment.

---

## Ecosystem Architecture

This repository unites three foundational tools into one cohesive preparation platform:

1. **Interactive Web Tracker:** A lightweight client-side application hosting **486 curated problems** across **20 modules** with instant search, multi-criteria filtering, and local persistence.
2. **Theoretical Handbook:** A **30-chapter guide** delivering asymptotic complexity derivations, low-level memory representation diagrams, and interview pattern blueprints.
3. **Offline Milestone Workbook:** An integrated spreadsheet ([`MY_GFG-450.xlsx`](./MY_GFG-450.xlsx)) equipped with revision flags, attempt logs, and progress formulas.

---

## Interactive Tracker Features

Built with pure vanilla HTML5, CSS3, and ES6 JavaScript, the web tracker runs instantly in any browser with zero installation:

* 🔗 **Deterministic Link Precedence:** Direct links route to **LeetCode** as primary. If unavailable, they resolve to verified **GeeksforGeeks** problem pages or **TakeUForward** mirrors.
* 💾 **100% Client-Side Privacy:** Checkboxes, starred bookmarks, notes, and theme preferences reside solely in browser `localStorage`. No accounts, no credentials, and no external tracking.
* ⚡ **Instant Search Engine:** Sub-millisecond substring queries across problem titles, topic tags, and module names without page reloads.
* 🎯 **Multi-Criteria Filtering:** Filter concurrently by difficulty (*Easy*, *Medium*, *Hard*), problem tier (*Basic*, *Core*, *Pro*), platform source, and solved status.
* 🌗 **Theme Engine:** Built-in Light and Dark themes with automated system preference detection.
* 📦 **Data Backup & Portability:** Single-click JSON export and import to backup progress or transfer seamlessly between machines.

### Difficulty & Tier Classification

Problems are classified across two complementary dimensions to guide your preparation trajectory:

| Classification | Dimension | Description & Target Audience | Target Standard |
|:---|:---:|:---|:---|
| **Easy** | Difficulty | Direct fundamental questions testing baseline syntax and data structure awareness | Solve in < 15 mins |
| **Medium** | Difficulty | Core interview standard questions combining multiple techniques (majority of FAANG rounds) | Solve in < 25 mins |
| **Hard** | Difficulty | Advanced algorithmic puzzles requiring optimal space-time tradeoffs and rigorous invariants | Solve in < 45 mins |
| **Basic** | Progression Tier | Foundation builder: elementary traversal, basic hashing, and brute-force implementations | 100% mastery |
| **Core** | Progression Tier | Standard interview benchmarks: optimal two-pointer, dynamic programming, and graph BFS/DFS | Essential focus |
| **Pro** | Progression Tier | Competitive-tier challenges: segment trees, complex DP on trees, and advanced string hashing | Differentiation |

### Keyboard Shortcuts

| Key | Operation | Action Description |
|:---:|:---|:---|
| <kbd>/</kbd> | **Focus Search** | Highlights global search bar instantly from anywhere on the page |
| <kbd>j</kbd> | **Next Problem** | Moves cursor highlight downward to the next problem row |
| <kbd>k</kbd> | **Previous Problem** | Moves cursor highlight upward to the previous problem row |
| <kbd>s</kbd> | **Toggle Solved** | Toggles completion checkbox of the highlighted problem |
| <kbd>Esc</kbd> | **Clear / Close** | Clears active search filter or closes the active details drawer |

### Client-Side State Management

The application operates without backend servers or user authentication. All progress is isolated to your browser via Web Storage APIs:

| Storage Key | Data Format | Content Stored |
|:---|:---|:---|
| `a2z.solved` | `localStorage` JSON Array | List of unique problem IDs marked as completed |
| `a2z.starred` | `localStorage` JSON Array | List of unique problem IDs flagged for revision or follow-up |
| `a2z.theme` | `localStorage` String | Active UI theme setting (`light` or `dark`) |

---

## Curriculum Syllabus

The curriculum organizes **486 problems** across **20 modules** covering all high-frequency interview patterns:

| # | Module | Problems | Core Patterns & Landmark Problems |
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
| **—** | **Total Master's Curriculum** | **486** | **Production-Grade Technical Interview Benchmark** |

---

## Technical Interview Pattern Matrix

Mastering DSA requires recognizing underlying algorithmic paradigms across problem statements:

| Algorithmic Pattern | Core Mechanism | High-Yield Application Areas |
|:---|:---|:---|
| **Two Pointers & Sliding Window** | Left/Right pointers, expanding & shrinking window | Substring problems, 3-Sum, Container With Most Water, Trapping Rainwater |
| **Monotonic Stack / Deque** | Stack maintaining strictly ascending or descending order | Next Greater Element, Largest Rectangle in Histogram, Sliding Window Maximum |
| **Binary Search on Answer Space** | Monotonic predicate testing range $[L, R]$ | Koko Eating Bananas, Capacity to Ship Packages, Book Allocation Problem |
| **Fast & Slow Pointers** | Floyd's cycle finding algorithm with differing velocities | Linked list loop detection, middle of linked list, duplicate number in array |
| **State-Space Backtracking** | Depth-first search with pruning and backtracking | N-Queens, Sudoku Solver, Palindrome Partitioning, Word Search in Grid |
| **Multi-Source BFS** | Queue initialized with multiple starting coordinates | Rotting Oranges, Distance of nearest cell having 1, Walls and Gates |
| **Topological Ordering** | In-degree queue reduction (Kahn's algorithm) | Course Schedule I & II, Alien Dictionary, Build Order resolution |
| **Shortest Paths & Disjoint Sets** | Greedy edge relaxation & Union-Find with path compression | Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal's MST, Accounts Merge |
| **Dynamic Programming State Reductions**| Optimal substructure and overlapping subproblems | 0/1 Knapsack, Coin Change, Longest Increasing Subsequence, Edit Distance |

---

## 12-Week Master Study Plan

A structured, week-by-week preparation roadmap tailored for technical interviews:

| Week | Focus Topic & Modules | Primary Learning Objectives | Weekly Target |
|:---:|:---|:---|:---:|
| **Week 01** | **Beginner Math & Sorting** (Mod 01–02) | Euclidean GCD, prime tests, divisor logic, Merge Sort & Quick Sort | **21 problems** |
| **Week 02** | **Arrays & 2D Matrices** (Mod 03) | Kadane's algorithm, Dutch National Flag, Next Permutation, Spiral Matrix | **25 problems** |
| **Week 03** | **Strings & Hashing** (Mod 04–05) | Palindrome expansion, Roman conversions, Prefix-Sum Hashing, XOR subarrays | **25 problems** |
| **Week 04** | **Binary Search Mastery** (Mod 06) | Lower/Upper bound, search on answers (Koko Bananas), Median of 2 arrays | **30 problems** |
| **Week 05** | **Recursion & Backtracking** (Mod 07) | State-space trees, Subsets, Combination Sum, N-Queens, Sudoku Solver | **25 problems** |
| **Week 06** | **Linked Lists & Bit Manipulation** (Mod 08–09) | Fast-slow pointers, Reverse in K-groups, Clone LL, Bitmask power sets | **25 problems** |
| **Week 07** | **Greedy & Sliding Window** (Mod 10–11) | Interval scheduling, Candy, Minimum Window Substring & Subsequence | **28 problems** |
| **Week 08** | **Stacks, Queues & Monotonicity** (Mod 12) | Next Greater Element, Trapping Rainwater, Histogram Area, LRU/LFU Cache | **31 problems** |
| **Week 09** | **Binary Trees & BSTs** (Mod 13–14) | Morris traversal, LCA, diameter, tree serialisation, BST validation | **35 problems** |
| **Week 10** | **Heaps & Priority Queues** (Mod 15) | Min/Max Heaps, Task Scheduler, Design Twitter, Median in Data Stream | **22 problems** |
| **Week 11** | **Graph Theory & Traversals** (Mod 16) | BFS/DFS cycles, Kahn's topological sort, Dijkstra, Bellman-Ford, Kosaraju | **35 problems** |
| **Week 12** | **Dynamic Programming & Tries** (Mod 17–20) | 0/1 Knapsack, LCS/LIS variants, MCM partitioning, Trie prefixes, KMP | **40 problems** |

---

## Theoretical Handbook Highlights

The [`handbook/`](./handbook/) directory contains 30 dedicated chapters organized into 6 core technical domains:

| Domain | Chapter Scope | Key Algorithmic Principles & Theorems |
|:---|:---:|:---|
| **Mathematical Foundations** | Ch 01–02, 23–24 | Asymptotic derivations, Master Theorem, number theory, Java memory model |
| **Linear Data Structures** | Ch 03–04, 10, 13–15 | Memory alignment, sliding window templates, two pointers, monotonic queues |
| **Hierarchical Structures** | Ch 16–18, 25–26 | Tree traversals, LCA, Morris traversal, BST properties, AVL & Red-Black trees |
| **Graph Networks** | Ch 19, 28 | BFS/DFS, topological order, Dijkstra, Bellman-Ford, Floyd-Warshall, DSU |
| **Algorithmic Paradigms** | Ch 05–09, 11–12 | Divide & conquer, recursion stack, state-space pruning, greedy choice |
| **Advanced DP & Strings** | Ch 20–22, 27, 29–30 | 1D/2D DP, MCM, KMP string matching, Segment Trees, Fenwick Trees, Branch & Bound |

---

## Offline Practice Tracking Workbook

For engineers who track progress via spreadsheets or offline workbooks, the repository includes [`MY_GFG-450.xlsx`](./MY_GFG-450.xlsx):

* 📋 **Pre-Populated Problem Inventory:** Categorized by topic, algorithmic pattern, and technical difficulty.
* ⏱️ **Attempt & Timing Logs:** Dedicated columns to record problem-solving duration and repeat attempts.
* 🏷️ **Review Status Flags:** Tag problems as **Needs Review**, **Tricky Edge-Case**, or **Mastered**.
* 📈 **Formula-Driven Progress:** Automated completion percentages and daily milestone velocity trackers.

---

## Local Development & Setup

The web application is pure static web technology. It requires no complex build tools or runtime compilers:

```bash
# 1. Clone the repository
git clone https://github.com/premnarayn13/DSA_StudyMaterial.git

# 2. Navigate to the project root
cd DSA_StudyMaterial

# 3. Start a local HTTP server using Python or Node.js
# Option A: Python 3
python -m http.server 8000

# Option B: Node.js (via npx serve)
npx serve Problems_List/site -l 8000
```

Open your browser and navigate to:
```text
http://localhost:8000/Problems_List/site/
```

> **Note:** Running through an HTTP server (rather than double-clicking `index.html`) avoids browser CORS restrictions when fetching `data.json` over the `file://` protocol.

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

---

## Interactive Preparation Checklist

Test your readiness across standard interview competencies:

- [ ] **Arrays & Matrices:** Implemented Kadane's algorithm, Next Permutation & Spiral Matrix
- [ ] **Two Pointers & Sliding Window:** Solved Minimum Window Substring & 3-Sum in $O(N^2)$
- [ ] **Monotonic Stack:** Solved Next Greater Element, Trapping Rainwater & Largest Histogram
- [ ] **Binary Search:** Implemented Search in Rotated Array & Median of Two Sorted Arrays
- [ ] **Recursion & Backtracking:** Implemented N-Queens, Sudoku Solver & Palindrome Partitioning
- [ ] **Linked Lists:** Reversed in K-Groups, detected cycles with Floyd's algorithm & cloned random lists
- [ ] **Trees & BST:** Traversed trees using Morris Inorder & verified BST properties
- [ ] **Heaps & Priority Queues:** Constructed Two-Heaps for Median Stream & solved Task Scheduler
- [ ] **Graphs:** Implemented Dijkstra's shortest path, Kahn's Topological Sort & Kosaraju SCC
- [ ] **Dynamic Programming:** Solved 0/1 Knapsack, Longest Increasing Subsequence & Matrix Chain Multiplication
- [ ] **Tries & Advanced Strings:** Constructed prefix trees & implemented KMP / Rabin-Karp pattern search
- [ ] **System Design Data Structures:** Designed LRU Cache & LFU Cache with $O(1)$ operations

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

---

<div align="center">

> *"Simplicity is prerequisite for reliability."*  
> — **Edsger W. Dijkstra**

> *"Premature optimization is the root of all evil in programming."*  
> — **Donald E. Knuth**

> *"Talk is cheap. Show me the code."*  
> — **Linus Torvalds**

<br/>

**Master's DSA Sheet & Study Ecosystem**  
*Built for Engineers Mastering Problem-Solving and Technical Interviews.*

⭐ **Found this helpful? Consider starring the repository to support the project!** ⭐

</div>
