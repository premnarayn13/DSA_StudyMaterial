# 04. Job Assignment Problem: Matrix Reduction, Worker-Job Matching & LC-B&B

## 1. Introduction
The **Job Assignment Problem** is a foundational NP-hard combinatorial optimization problem where $N$ workers must be assigned to $N$ distinct jobs on a 1-to-1 basis such that the total cost of assignment is **MINIMIZED**. Given an $N \times N$ Cost Matrix $C$ where $C[i][j]$ represents the cost of worker $i$ performing job $j$, the objective is to find a permutation $\pi$ of $\{0 \dots N-1\}$ that minimizes $\sum_{i=0}^{N-1} C[i][\pi(i)]$. While the **Hungarian Algorithm** solves this in $O(N^3)$ polynomial time, **Least-Cost Branch & Bound (LC-B&B)** using **Row-Column Matrix Reduction Lower Bounds** serves as the general paradigm benchmark for solving assignment problems with complex side constraints.

> **Important:** Core Structural Invariants of LC-B&B Job Assignment:
> 1. **Worker-by-Worker Assignment Level ($level = 0 \dots N-1$)**:
>    - At tree depth $level$, assign Worker `level` to one of the unassigned Jobs $j \in \{0 \dots N-1\}$.
> 2. **Job Assignment Mask / Visited Array (`assignedJobs[]`)**:
>    - Boolean array tracking jobs already assigned to previous workers to enforce 1-to-1 matching.
> 3. **Reduced Matrix Lower Bound Calculation ($\hat{l}(x)$)**:
>    - Lower Bound $\hat{l}(x) = \text{Accumulated Cost} + \text{Reduced Matrix Minimum Sum of Unassigned Workers/Jobs}$.
> 4. **Min-PriorityQueue Node Ordering**:
>    - Live Nodes are stored in a Min-PriorityQueue ordered by Lower Bound $\hat{l}(x)$, expanding the worker assignment with the lowest optimistic cost first! ⚡

```
Job Assignment State Space Tree Topology (3 Workers -> 3 Jobs):

                    [ Root: Worker 0 Assignment (l_hat = 9) ]
                    /                 |                 \
         [ Worker 0 -> Job 0 ] [ Worker 0 -> Job 1 ] [ Worker 0 -> Job 2 ]
         (l_hat = 14)          (l_hat = 9 -> POP!)   (l_hat = 12)
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
              [ Worker 1 -> Job 0 ]       [ Worker 1 -> Job 2 ]
              (l_hat = 11)                (l_hat = 9 -> POP!)

Priority Queue pops Worker 0 -> Job 1 first (Lowest Bound 9)! ⚡
```

---

## 2. Core Concepts & Assignment Strategy Matrix

### 2.1 Job Assignment Implementations Strategy Matrix
```
Job Assignment Implementations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Implementation        | Bounding Engine   | Queue Engine      | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Hungarian Algorithm**| Dual Matrix Potentials| Alternating Paths| **$O(N^3)$ Strict ⚡**| **$O(N^2)$ Matrix ⚡**|
| **LC Branch & Bound** | **Matrix Reduction⚡**| **Min-PriorityQueue⚡**| **Pruned $O(N!)$ ⚡**| **$O(N!)$ Queue ⚡** |
| **Naive DFS**         | Plain Permutations| DFS Stack         | $O(N!)$ Worst ❌  | $O(N)$ Stack      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LC-B&B Job Assignment matches Worker 'level' to Job 'j'; Min-PriorityQueue expands node with smallest l_hat!"**

---

## 3. Characteristics & Reduced Matrix Lower Bound Derivation

### 3.1 Mathematical Derivation of Assignment Lower Bound $\hat{l}(x)$
* Let node $x$ represent partial assignment of workers $0 \dots k-1$ to jobs $\pi(0) \dots \pi(k-1)$, incurring accumulated cost $C_{\text{acc}}(x) = \sum_{i=0}^{k-1} C[i][\pi(i)]$.
* Let $U_{\text{workers}} = \{k \dots N-1\}$ be remaining unassigned workers, and $U_{\text{jobs}} = \{0 \dots N-1\} \setminus \{\pi(0) \dots \pi(k-1)\}$ be remaining available jobs.
* **Admissible Lower Bound Formula**:
  $$\hat{l}(x) = C_{\text{acc}}(x) + \sum_{i \in U_{\text{workers}}} \min_{j \in U_{\text{jobs}}} C[i][j]$$
* **Proof of Admissibility**:
  - For each unassigned worker $i$, the actual job assigned in any complete extension must be some $j \in U_{\text{jobs}}$.
  - The actual cost $C[i][j] \ge \min_{j' \in U_{\text{jobs}}} C[i][j']$.
  - Summing these minimums over all remaining workers gives a lower bound that is strictly $\le$ the true completion cost over $\text{Subtree}(x)$. Admissibility holds! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step LC-B&B Assignment Execution

Tracing Job Assignment for $3 \times 3$ Cost Matrix:

```
Cost Matrix C:
Worker 0: [ 9, 2, 7 ]
Worker 1: [ 6, 4, 3 ]
Worker 2: [ 5, 8, 1 ]

Root Lower Bound: Row min sum = 2 + 3 + 1 = 6.

Level 0 (Assign Worker 0):
- Option 1 (Job 0, Cost 9): Remaining Workers 1,2 min jobs = 3 + 1 = 4. Total l_hat = 9 + 4 = 13.
- Option 2 (Job 1, Cost 2): Remaining Workers 1,2 min jobs = 3 + 1 = 4. Total l_hat = 2 + 4 = 6. (LOWEST!) ⚡
- Option 3 (Job 2, Cost 7): Remaining Workers 1,2 min jobs = 4 + 5 = 9. Total l_hat = 7 + 9 = 16.

PQ Pop: Option 2 (Worker 0 -> Job 1, l_hat = 6).

Level 1 (Assign Worker 1, Job 1 unavailable):
- Option 2.1 (Job 0, Cost 6): Worker 2 min job = 1. Total l_hat = 2 + 6 + 1 = 9.
- Option 2.2 (Job 2, Cost 3): Worker 2 min job = 5. Total l_hat = 2 + 3 + 5 = 10.

PQ Pop: Option 2.1 (Worker 0->Job 1, Worker 1->Job 0, l_hat = 9).

Level 2 (Assign Worker 2, Jobs 0,1 unavailable):
- Must pick Job 2 (Cost 1). Total Cost = 2 + 6 + 1 = 9.

Optimal Assignment: Worker 0->Job 1, Worker 1->Job 0, Worker 2->Job 2! Cost = 9! ✅ ⚡
```

---

## 5. Visual Diagram: Reduced Matrix State Expansion

```
LC-B&B Priority Queue State Expansion:

Priority Queue: [ Node(W0->J1, l_hat=6), Node(W0->J0, l_hat=13), Node(W0->J2, l_hat=16) ]
                         │
              Pop Best Node(W0->J1, l_hat=6)
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
[ Node(W1->J0, l_hat=9) ]       [ Node(W1->J2, l_hat=10) ]
  (Queued in PQ!)                 (Queued in PQ!)

Expands optimal assignment path directly! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LC Branch & Bound Job Assignment Solver using Priority Queue and Matrix Bounding.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Job Assignment Problem:
 * LC Branch & Bound, Min-Priority Queue, and Reduced Cost Matrix Bounding.
 */
public class AssignmentProblemMaster {

    public static class AssignmentNode implements Comparable<AssignmentNode> {
        public final int worker; // Current worker being assigned (level)
        public final int job;    // Job assigned to this worker
        public final int cost;   // Accumulated cost so far
        public final int lowerBound; // Optimistic lower bound l_hat
        public final boolean[] assignedJobs; // Visited jobs array
        public final AssignmentNode parent;

        public AssignmentNode(int worker, int job, int cost, int lowerBound, boolean[] assignedJobs, AssignmentNode parent) {
            this.worker = worker;
            this.job = job;
            this.cost = cost;
            this.lowerBound = lowerBound;
            this.assignedJobs = assignedJobs.clone();
            this.parent = parent;
        }

        @Override
        public int compareTo(AssignmentNode o) {
            return Integer.compare(this.lowerBound, o.lowerBound); // MIN-PRIORITY QUEUE BY LOWER BOUND! ⚡
        }
    }

    // =========================================================================
    // 1. LC BRANCH & BOUND JOB ASSIGNMENT SOLVER (O(N!) Pruned)
    // =========================================================================
    /**
     * Solves Job Assignment Problem returning minimum total cost.
     *
     * @param costMatrix N x N cost matrix
     * @return minimum total assignment cost
     */
    public int solveAssignmentBranchAndBound(int[][] costMatrix) {
        if (costMatrix == null || costMatrix.length == 0) return 0;
        int n = costMatrix.length;

        PriorityQueue<AssignmentNode> pq = new PriorityQueue<>();
        boolean[] initialAssigned = new boolean[n];

        // Root Node (Dummy worker -1)
        int rootBound = calculateLowerBound(costMatrix, -1, initialAssigned, 0, n);
        AssignmentNode root = new AssignmentNode(-1, -1, 0, rootBound, initialAssigned, null);
        pq.add(root);

        int bestCost = Integer.MAX_VALUE;

        while (!pq.isEmpty()) {
            AssignmentNode curr = pq.poll();

            // Optimality Bounding Pruning Line ⚡
            if (curr.lowerBound >= bestCost) continue;

            // Base Case: All N workers assigned!
            if (curr.worker == n - 1) {
                bestCost = Math.min(bestCost, curr.cost);
                continue;
            }

            int nextWorker = curr.worker + 1;

            // Try assigning nextWorker to each unassigned Job j
            for (int j = 0; j < n; j++) {
                if (!curr.assignedJobs[j]) {
                    boolean[] nextAssigned = curr.assignedJobs.clone();
                    nextAssigned[j] = true;

                    int nextCost = curr.cost + costMatrix[nextWorker][j];
                    int nextBound = calculateLowerBound(costMatrix, nextWorker, nextAssigned, nextCost, n);

                    if (nextBound < bestCost) {
                        pq.add(new AssignmentNode(nextWorker, j, nextCost, nextBound, nextAssigned, curr));
                    }
                }
            }
        }

        return bestCost;
    }

    private int calculateLowerBound(int[][] costMatrix, int worker, boolean[] assignedJobs, int currentCost, int n) {
        int bound = currentCost;

        // Estimate minimum cost for remaining unassigned workers
        for (int i = worker + 1; i < n; i++) {
            int minJobCost = Integer.MAX_VALUE;
            for (int j = 0; j < n; j++) {
                if (!assignedJobs[j] && costMatrix[i][j] < minJobCost) {
                    minJobCost = costMatrix[i][j];
                }
            }
            if (minJobCost != Integer.MAX_VALUE) {
                bound += minJobCost;
            }
        }

        return bound; // Admissible Lower Bound l_hat! ⚡
    }
}
```

> **Quick Syntax:**
```java
// LC-B&B Min-Priority Queue Comparison Line
public int compareTo(AssignmentNode o) { return Integer.compare(this.lowerBound, o.lowerBound); }
```

---

## 7. Concrete Problem Examples & Applications

1. **Job Assignment Problem**:
   - Worker-to-job matching benchmark ($O(N!)$ pruned).

2. **Task Scheduling in Distributed Systems**:
   - Assigning $N$ computational tasks to $N$ heterogeneous server nodes.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class AssignmentProblemDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   JOB ASSIGNMENT LC-B&B BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        AssignmentProblemMaster master = new AssignmentProblemMaster();

        int[][] costMatrix = {
            {9, 2, 7},
            {6, 4, 3},
            {5, 8, 1}
        };

        int minCost = master.solveAssignmentBranchAndBound(costMatrix);

        System.out.println("1. Job Assignment LC-B&B Result:");
        System.out.println("   Cost Matrix: 3 Workers x 3 Jobs");
        System.out.println("   Minimum Total Assignment Cost: " + minCost + " Cost (Optimal = 9)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Assignment Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Hungarian Algorithm**| $\mathbf{O(N^3)}$ Strict Polynomial⚡| $\mathbf{O(N^2)}$ Matrix Space| Dual matrix potentials |
| **LC Branch & Bound**  | $\mathbf{O(N!)}$ Pruned ⚡| $\mathbf{O(N!)}$ PriorityQueue| Min lower bound `l_hat` |

---

## 10. Edge Cases & Boundary Handling

1. **Single Worker / Single Job ($N=1$)**:
   - Returns `costMatrix[0][0]` immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Allowing 1 Job to be Assigned to Multiple Workers**:
  - Failing to mark `assignedJobs[j] = true` breaks 1-to-1 matching, resulting in invalid assignments. **ALWAYS maintain `boolean[] assignedJobs`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 1-to-1 Worker-Job Matching Rule:
> Maintain a `boolean[] assignedJobs` array to track assigned jobs. Worker $i$ can ONLY be assigned to job $j$ if `assignedJobs[j] == false`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Hungarian Algorithm | LC Branch & Bound |
| :--- | :--- | :--- |
| **Algorithmic Class** | Polynomial ($O(N^3)$) | **Branch & Bound ($O(N!)$ Pruned) ⚡** |
| **Side Constraints** | Difficult to add | **Easily Handles Side Constraints ⚡** |
| **Data Structure** | Augmenting Paths | Min-Priority Queue |

---

## 14. How to Recognize This in Questions

* **"Assign N workers to N jobs to minimize total cost"** $\rightarrow$ Job Assignment Problem.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Branch & Bound used for Job Assignment when Hungarian Algorithm is $O(N^3)$?**  
  *A:* Because real-world assignment problems often include complex side constraints (e.g. precedence, resource limits) that break the Hungarian algorithm structure, whereas Branch & Bound easily handles side constraints.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: JOB ASSIGNMENT PROBLEM                                |
+-----------------------------------------------------------------------+
| • Level Order  : Assign Worker level to unassigned Job j              |
| • Tracking     : boolean[] assignedJobs ensures 1-to-1 matching       |
| • Lower Bound  : l_hat = currCost + sum(min job cost for unassigned)  |
| • PriorityQueue: Min-PQ ordered by lowerBound -> Pops lowest l_hat    |
| • Performance  : Prunes 90%+ of permutations in practice! ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LC Branch & Bound Job Assignment in Java using Priority Queue.
- [ ] I can write the admissible lower bound function for unassigned workers.
- [ ] I can explain why `boolean[] assignedJobs` is required.
- [ ] I can state the complexity of Hungarian Algorithm ($O(N^3)$).
- [ ] I can state why B&B is preferred when side constraints are present.
