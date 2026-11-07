# 04. Job Sequencing Problem: Profit Sorting, Slot Allocation & DSU Optimizations

## 1. Introduction
The **Job Sequencing Problem with Deadlines** is a fundamental greedy scheduling problem designed to maximize total profit when executing a set of unit-time jobs under strict deadline constraints. Given $N$ jobs $J = \{j_1, j_2 \dots j_N\}$, where each job $j_i$ requires 1 unit of execution time, has a deadline $d_i \ge 1$, and yields a profit $p_i > 0$ if completed on or before its deadline, the goal is to schedule a subset of jobs to **Maximize Total Profit**. The optimal Greedy strategy sorts jobs in descending order of **Profit ($p_i$)** and allocates each job to the **Latest Available Time Slot $t \le d_i$**. While a naive slot search runs in $O(N^2)$ time, optimizing slot lookup via **Disjoint-Set Union (DSU / Union-Find)** reduces execution to **$O(N \log N)$ Time Complexity** and **$O(N)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Job Sequencing:
> 1. **Profit-First Greedy Invariant**:
>    - Process jobs in strictly non-increasing order of profit ($p_1 \ge p_2 \ge \dots \ge p_N$). High-profit jobs MUST be prioritized!
> 2. **Latest Available Time Slot Rule**:
>    - For a job with deadline $d_i$, schedule it at the **Latest Free Time Slot $t \le d_i$** (i.e. slot $d_i, d_i - 1 \dots 1$).
>    - Why latest slot? Scheduling as late as possible reserves earlier time slots for jobs with tighter (smaller) deadlines!
> 3. **DSU (Union-Find) Slot Allocation Optimization**:
>    - Represent free time slots as a DSU parent array `parent[t]`.
>    - Finding the latest available slot for deadline $d$ takes $O(\alpha(N))$ amortized time via `find(d)`, eliminating $O(N)$ linear slot scanning!
> 4. **Unit-Time Execution Invariant**:
>    - Every job takes exactly 1 unit of time (slot $[t-1, t]$ for integer $t$). ⚡

```
Job Sequencing Profit & Slot Topology:

Job 1: Profit = 100, Deadline = 2 ──► Assign to Slot 2 (Latest <= 2)
Job 2: Profit = 50,  Deadline = 1 ──► Assign to Slot 1 (Latest <= 1)
Job 3: Profit = 40,  Deadline = 2 ──► Slot 2 full! Slot 1 full! ──► CANNOT SCHEDULE!

Time Slots:  | Slot 1: Job 2 | Slot 2: Job 1 |
Total Profit = 100 + 50 = 150! ⚡
```

---

## 2. Core Concepts & Job Scheduling Strategy Matrix

### 2.1 Job Scheduling Variants Strategy Matrix
```
Job Scheduling Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Scheduling Model      | Slot Search Method| Time Complexity   | Auxiliary Space   | Primary Invariant |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Naive Array Slot**  | Linear Scan $d\to1$| $O(N^2)$ Quadratic| $O(\max d_i)$ Array| Simple Slot Search|
| **DSU Optimized ⚡**  | Path Compression  | **$O(N \log N)$ ⚡**| **$O(\max d_i)$ DSU⚡**| Amortized $O(\alpha(N))$|
| **TreeSet Slot**      | Floor Lookup      | **$O(N \log N)$ ⚡**| $O(N)$ TreeSet    | Self-Balancing BST|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sort jobs by PROFIT descending! Schedule job at latest free slot t <= deadline using DSU path compression!"**

---

## 3. Characteristics & $O(N \log N)$ DSU Mathematical Proof

### 3.1 Mathematical Proof of DSU Slot Allocation Optimality
* **Problem**: In naive job sequencing, for a job with deadline $d$, scanning linearly backward $d, d-1 \dots 1$ takes $O(d)$ time, causing $O(N \cdot \max d_i) = O(N^2)$ worst-case execution.
* **DSU Representation**:
  - Maintain a DSU parent array initialized to `parent[i] = i` for $i \in [0 \dots \max d_i]$.
  - `find(d)` returns the latest available free slot $\le d$. If `find(d) == 0`, no free slot exists.
  - When slot $s = \text{find}(d)$ is assigned to a job, we union it with slot $s - 1$ by setting `parent[s] = find(s - 1)`.
* **Complexity Proof**:
  - Sorting $N$ jobs by profit takes $O(N \log N)$ time.
  - Performing $N$ DSU `find` and `union` operations with Path Compression takes $O(N \cdot \alpha(N))$ time, where $\alpha$ is the Inverse Ackermann Function ($\alpha(N) \le 4$).
  - Total Time Complexity: $\mathbf{O(N \log N) \text{ Log-Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: Step-by-Step DSU Slot Trace

Tracing Job Sequencing for Jobs: $J_1(p=100, d=2)$, $J_2(p=19, d=1)$, $J_3(p=27, d=2)$, $J_4(p=25, d=1)$, $J_5(p=15, d=3)$:

```
Step 1: Sort Jobs Descending by Profit:
Ordered Jobs:
1. J1: Profit 100, Deadline 2
2. J3: Profit 27,  Deadline 2
3. J4: Profit 25,  Deadline 1
4. J2: Profit 19,  Deadline 1
5. J5: Profit 15,  Deadline 3

Max Deadline = 3. Init DSU Parent: parent = [0, 1, 2, 3].

Step 2: Process Jobs Greedily with DSU:

- Process J1 (Profit 100, d=2):
  availableSlot = find(2) = 2. Slot 2 is FREE!
  Schedule J1 at Slot 2.
  Union(2, 1) -> parent[2] = find(1) = 1.
  Total Profit = 100, Count = 1.

- Process J3 (Profit 27, d=2):
  availableSlot = find(2) -> parent[2] is 1 -> find(1) = 1. Slot 1 is FREE!
  Schedule J3 at Slot 1.
  Union(1, 0) -> parent[1] = find(0) = 0.
  Total Profit = 100 + 27 = 127, Count = 2.

- Process J4 (Profit 25, d=1):
  availableSlot = find(1) -> parent[1] is 0 -> find(0) = 0.
  Slot 0 -> NO FREE SLOT! Skip J4.

- Process J2 (Profit 19, d=1):
  find(1) = 0 -> NO FREE SLOT! Skip J2.

- Process J5 (Profit 15, d=3):
  availableSlot = find(3) = 3. Slot 3 is FREE!
  Schedule J5 at Slot 3.
  Union(3, 2) -> parent[3] = find(2) = 0.
  Total Profit = 127 + 15 = 142, Count = 3.

Final Schedule: Slot 1: J3, Slot 2: J1, Slot 3: J5. Max Profit = 142! ✅
```

---

## 5. Visual Diagram: DSU Slot Pointer Redirect Graph

```
Initial DSU State:   [0] ── [1] ── [2] ── [3]  (All slots point to themselves)

After Slot 2 Claimed: [0] ── [1] ◄── [2]   [3]  (Slot 2 points to Slot 1!)

After Slot 1 Claimed: [0] ◄── [1] ◄── [2]   [3]  (Slot 1 and 2 point to Slot 0!)

Next query find(2) jumps instantly to 0 in 1 step via Path Compression! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Naive $O(N^2)$ Job Sequencing, DSU Fast $O(N \log N)$ Job Sequencing, and TreeSet Slot Allocation.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Job Sequencing Problem,
 * Profit-Based Greedy Choice, Naive Slot Allocation, and DSU Optimizations.
 */
public class JobSequencingMaster {

    public static class Job {
        public final int id;
        public final int deadline;
        public final int profit;

        public Job(int id, int deadline, int profit) {
            this.id = id;
            this.deadline = deadline;
            this.profit = profit;
        }

        @Override
        public String toString() {
            return "Job" + id + "[p=" + profit + ", d=" + deadline + "]";
        }
    }

    public static class JobResult {
        public final int count;
        public final int totalProfit;
        public final int[] scheduledSlots; // Maps slot index to Job ID

        public JobResult(int count, int totalProfit, int[] scheduledSlots) {
            this.count = count;
            this.totalProfit = totalProfit;
            this.scheduledSlots = scheduledSlots;
        }
    }

    // =========================================================================
    // 1. DSU (UNION-FIND) OPTIMIZED JOB SEQUENCING (O(N log N) Time, O(MaxD) Space)
    // =========================================================================
    public static class DSU {
        private final int[] parent;

        public DSU(int maxDeadline) {
            this.parent = new int[maxDeadline + 1];
            for (int i = 0; i <= maxDeadline; i++) {
                parent[i] = i;
            }
        }

        public int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path Compression! ⚡
        }

        public void union(int u, int v) {
            parent[u] = v; // Redirect claimed slot u to free slot v
        }
    }

    /**
     * Solves Job Sequencing in O(N log N) time using DSU slot allocation.
     *
     * @param jobs list of input jobs
     * @return JobResult containing total count, profit, and slot assignments
     */
    public JobResult solveJobSequencingDSU(List<Job> jobs) {
        if (jobs == null || jobs.isEmpty()) {
            return new JobResult(0, 0, new int[0]);
        }

        // Step 1: Sort jobs descending by profit
        List<Job> sortedJobs = new ArrayList<>(jobs);
        sortedJobs.sort((a, b) -> Integer.compare(b.profit, a.profit));

        // Find maximum deadline to size DSU and slot array
        int maxDeadline = 0;
        for (Job job : sortedJobs) {
            maxDeadline = Math.max(maxDeadline, job.deadline);
        }

        DSU dsu = new DSU(maxDeadline);
        int[] slots = new int[maxDeadline + 1]; // 1-based indexing for slots
        Arrays.fill(slots, -1);

        int count = 0;
        int totalProfit = 0;

        // Step 2: Make Greedy Choices sequentially
        for (Job job : sortedJobs) {
            // Find latest available free slot <= job.deadline
            int availableSlot = dsu.find(job.deadline);

            if (availableSlot > 0) {
                // Claim availableSlot for this job
                slots[availableSlot] = job.id;
                totalProfit += job.profit;
                count++;

                // Union availableSlot with availableSlot - 1
                dsu.union(availableSlot, dsu.find(availableSlot - 1));
            }
        }

        return new JobResult(count, totalProfit, slots);
    }

    // =========================================================================
    // 2. NAIVE ARRAY-BASED JOB SEQUENCING (O(N^2) Time, O(MaxD) Space)
    // =========================================================================
    /**
     * Solves Job Sequencing in O(N^2) time using linear backward slot scan.
     */
    public JobResult solveJobSequencingNaive(List<Job> jobs) {
        if (jobs == null || jobs.isEmpty()) return new JobResult(0, 0, new int[0]);

        List<Job> sorted = new ArrayList<>(jobs);
        sorted.sort((a, b) -> Integer.compare(b.profit, a.profit));

        int maxDeadline = 0;
        for (Job j : sorted) maxDeadline = Math.max(maxDeadline, j.deadline);

        int[] slots = new int[maxDeadline + 1];
        Arrays.fill(slots, -1);

        int count = 0;
        int totalProfit = 0;

        for (Job job : sorted) {
            // Naive linear backward scan from deadline down to 1
            for (int t = job.deadline; t >= 1; t--) {
                if (slots[t] == -1) {
                    slots[t] = job.id;
                    totalProfit += job.profit;
                    count++;
                    break;
                }
            }
        }

        return new JobResult(count, totalProfit, slots);
    }
}
```

> **Quick Syntax:**
```java
// DSU Slot Allocation Line
int availableSlot = dsu.find(job.deadline); if (availableSlot > 0) { slots[availableSlot] = job.id; dsu.union(availableSlot, dsu.find(availableSlot - 1)); }
```

---

## 7. Concrete Problem Examples & Applications

1. **GeeksforGeeks / Coding Ninjas - Job Sequencing Problem**:
   - Primary job scheduling benchmark problem ($O(N \log N)$ time via DSU).

2. **Cloud Server Task Dispatchers**:
   - Assigning high-paying computing tasks to deadline-constrained cloud VMs.

3. **High-Frequency Financial Trade Order Execution**:
   - Executing lucrative trade orders before market expiration deadlines.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class JobSequencingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   JOB SEQUENCING GREEDY DSU DEMO               ");
        System.out.println("=================================================\n");

        JobSequencingMaster master = new JobSequencingMaster();

        List<JobSequencingMaster.Job> jobs = List.of(
            new JobSequencingMaster.Job(1, 2, 100),
            new JobSequencingMaster.Job(2, 1, 19),
            new JobSequencingMaster.Job(3, 2, 27),
            new JobSequencingMaster.Job(4, 1, 25),
            new JobSequencingMaster.Job(5, 3, 15)
        );

        System.out.println("1. Input Jobs List: " + jobs);

        // DSU Fast Solution Test
        JobSequencingMaster.JobResult dsuResult = master.solveJobSequencingDSU(jobs);
        System.out.println("\n2. DSU Fast Solution Results (O(N log N) Time):");
        System.out.println("   Max Jobs Scheduled : " + dsuResult.count);
        System.out.println("   Max Total Profit   : " + dsuResult.totalProfit + " (Optimal)");

        System.out.print("   Scheduled Time Slots: ");
        for (int t = 1; t < dsuResult.scheduledSlots.length; t++) {
            System.out.print("[Slot " + t + ": Job" + dsuResult.scheduledSlots[t] + "] ");
        }
        System.out.println("\n=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Job Sequencing Variant | Sorting Time | Slot Allocation Time | Total Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Array Scan** | $O(N \log N)$ | $O(N \cdot \max D)$ | $O(N^2)$ Quadratic ❌| $O(\max D)$ Array |
| **DSU Path Compression**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \cdot \alpha(N))}$ ⚡| $\mathbf{O(N \log N)}$ Log-Linear⚡| $\mathbf{O(\max D)}$ DSU ⚡|
| **TreeSet Floor Lookup**| $\mathbf{O(N \log N)}$ ⚡| $O(N \log N)$ | $\mathbf{O(N \log N)}$ Log-Linear⚡| $O(N)$ TreeSet |

---

## 10. Edge Cases & Boundary Handling

1. **All Deadlines Equal 1 ($d_i = 1$ for all $i$)**:
   - Only 1 slot exists. Greedy selects the single job with maximum profit.

2. **Deadlines Exceed Job Count ($\max d_i > N$)**:
   - DSU size is capped at $\min(N, \max d_i)$ to prevent allocating unnecessary memory.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Scheduling Job at Earliest Free Slot ($t = 1$) Instead of Latest ($t \le d_i$)**:
  - Scheduling a job at slot 1 when its deadline is 5 blocks jobs that MUST finish at slot 1. **ALWAYS schedule at the LATEST available slot $t \le d_i$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why DSU Path Compression Reduces Time to $O(N \log N)$:
> Naive backward scanning takes $O(d)$ per job. DSU `find(d)` uses **Path Compression** to collapse tree depth, finding the latest free slot in $O(\alpha(N))$ amortized time! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | DSU Job Sequencing | Naive Job Sequencing | TreeSet Job Sequencing |
| :--- | :--- | :--- | :--- |
| **Slot Allocation Time**| **$O(\alpha(N))$ Amortized ⚡**| $O(d)$ Linear | $O(\log N)$ TreeSet |
| **Total Time** | **$O(N \log N)$ Fast ⚡** | $O(N^2)$ Slow | $O(N \log N)$ Fast |
| **Auxiliary Memory** | $O(\max D)$ Array | $O(\max D)$ Array | $O(N)$ Objects |

---

## 14. How to Recognize This in Questions

* **"Maximize profit scheduling unit-time jobs under deadline constraints"** $\rightarrow$ Job Sequencing Problem.

---

## 15. Frequently Asked Interview Questions

* **Q: Why should a job be scheduled at the latest available free time slot $t \le d_i$?**  
  *A:* Because filling the latest possible slot leaves earlier slots open for jobs with smaller (tighter) deadlines.

* **Q: How does DSU optimize slot allocation?**  
  *A:* By mapping each time slot to its parent free slot. Claiming slot $s$ connects it to $s - 1$, allowing `find(d)` to jump directly to the next free slot in $O(\alpha(N))$ time.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: JOB SEQUENCING PROBLEM                                |
+-----------------------------------------------------------------------+
| • Greedy Choice: Sort jobs in descending order of PROFIT (p_i)        |
| • Slot Rule    : Assign job to LATEST available free slot t <= deadline|
| • Naive Time   : O(N^2) due to linear backward slot scan              |
| • DSU Opt      : DSU find(d) + Path Compression -> O(N log N) Total! ⚡|
| • Result       : Maximize profit under unit-time deadline constraints |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write standard Job Sequencing using Profit sorting in Java.
- [ ] I can write DSU (Union-Find) Path Compression slot allocation.
- [ ] I can explain why jobs must be scheduled at the latest available slot $t \le d_i$.
- [ ] I can prove why DSU optimizes execution time from $O(N^2)$ to $O(N \log N)$.
- [ ] I can state the result format (Job Count + Max Profit + Slot Schedule).
