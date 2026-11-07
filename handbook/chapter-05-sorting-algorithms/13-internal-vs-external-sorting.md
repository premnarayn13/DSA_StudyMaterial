# 13. Internal vs External Sorting: RAM Limits, Disk I/O & K-Way External Merge

## 1. Introduction
**Internal Sorting** refers to sorting algorithms that operate entirely within a system's Main Random Access Memory (RAM), accessing any memory address in $O(1)$ constant time. However, when processing massive datasets (e.g. 500GB log files or multi-terabyte database tables) that far exceed available system RAM capacity ($M \ll N$), algorithms must transition to **External Sorting**. External Sorting minimizes high-latency **Disk / Storage I/O Pass Count** by dividing the input file into $M$-sized RAM chunks, sorting each chunk internally, writing sorted chunk files to disk, and merging them using a **Priority Queue K-Way External Merge Routine** in **$O(N \log_K (N/M))$ Disk I/O Time**.

> **Important:** Core Invariants of Internal vs External Sorting:
> 1. **Internal Sorting Limit**: Assumes $O(1)$ random memory access. Performance is bottlenecked by CPU comparisons and L1/L2 cache locality.
> 2. **External Sorting Bottleneck**: Bottlenecked by Disk I/O Read/Write operations. 1 disk block access ($\approx 5\text{ms}$) costs 10,000,000 CPU clock cycles!
> 3. **Chunk Creation Phase**: Reads $M$ bytes into RAM buffer, sorts internally using QuickSort/TimSort, and writes sorted run file $R_i$ to disk.
> 4. **K-Way Priority Queue Merge Phase**: Opens $K$ sorted run files concurrently, reads 1 block per run into RAM, and uses a Min-Heap Priority Queue of size $K$ to merge all runs into a single sorted output file in **$O(N \log K)$ Time**. ⚡

```
External Sorting 2-Phase Pipeline Topology (File Size = 100GB, RAM M = 10GB):
Phase 1: Chunk Creation (Read 10GB -> Internal Sort -> Write Run File)
  - Output: 10 Sorted Temp Run Files [Run_1, Run_2 ... Run_10] (10GB each)

Phase 2: K-Way External Merge (K = 10 Run Files in Min-Heap)
  - Min-Heap Priority Queue (Size 10) streams minimum key to Output File!
  - 100GB File Fully Sorted in 2 Total Disk Passes! ⚡
```

---

## 2. Core Concepts & Internal vs External Strategy Matrix

### 2.1 Internal vs External Strategy Matrix
```
Internal vs External Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric / Dimension    | Internal Sorting  | External Sorting  | K-Way External Merge|
+-----------------------+-------------------+-------------------+-------------------+
| **Memory Limit**      | Fits in RAM ($N \le M$)| Exceeds RAM ($N \gg M$)| RAM $M$ Buffers  |
| **Bottleneck**        | CPU Clock / Cache | **Disk I/O Latency ⚡**| Priority Queue Merge|
| **Algorithm**         | QuickSort / TimSort| Multi-Way Merge   | **Min-Heap (Size K)⚡**|
| **Pass Complexity**   | $O(N \log N)$ CPU | **$O(\log_K(N/M))$ Disk Passes ⚡**| $O(N \log K)$ CPU |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Internal = RAM bound; External = Multi-Way Merge Sort using Min-Heap to minimize disk passes!"**

---

## 3. Characteristics & Disk I/O Pass Complexity Proof

### 3.1 Mathematical Proof of $O(\log_K (N/M))$ Disk Passes
* Let $N$ be total dataset size, $M$ be available RAM size, and $K$ be maximum concurrent merge streams ($K = M / \text{BlockSize}$).
* Phase 1 (Chunk Creation): Creates $R = \lceil N / M \rceil$ initial sorted run files. Consumes 1 Read pass and 1 Write pass ($2 N$ I/O).
* Phase 2 (K-Way Merging): Each merge pass reduces the number of run files by a factor of $K$:
  $$R \to R/K \to R/K^2 \dots 1$$
* Total Merge Passes required:
  $$P = \mathbf{\lceil \log_K (N/M) \rceil \text{ Total Disk Merge Passes}}$$
* Total Disk I/O Work: $2 N \cdot (1 + \log_K (N/M)) = \mathbf{O(N \log_K (N/M)) \text{ Disk I/O Volume}}$. ⚡

---

## 4. Internal Working Mechanics: Priority Queue K-Way Merge Stream

How does K-Way External Merging stream data through RAM without overflowing memory?

```
Tracing K-Way Merge Stream (K = 3 Run Files):

Run 1 File Buffer: [ 3, 10, 15 ]
Run 2 File Buffer: [ 2, 9, 20 ]
Run 3 File Buffer: [ 5, 8, 12 ]

Min-Heap Priority Queue (Size K = 3):
Initial Heap Push: (2, Run2), (3, Run1), (5, Run3)

Step 1: Extract Min (2, Run2) -> Write 2 to Output File.
        Fetch next element from Run 2 Buffer (val 9).
        Heap Push: (9, Run2). Heap becomes: [ (3, Run1), (5, Run3), (9, Run2) ].

Step 2: Extract Min (3, Run1) -> Write 3 to Output File.
        Fetch next element from Run 1 Buffer (val 10).
        Heap Push: (10, Run1). Heap becomes: [ (5, Run3), (9, Run2), (10, Run1) ].

Streams multi-terabyte data using ONLY O(K) RAM memory! ✅
```

---

## 5. Visual Diagram: External Merge Sort Architecture

```
Massive Disk File (100GB)
         │
         ▼ (Phase 1: Read M=10GB Chunks -> Internal QuickSort -> Write Runs)
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Run File 1  │ │  Run File 2  │ │  Run File 3  │ (Sorted 10GB Runs on Disk)
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
   [Buf 1]          [Buf 2]          [Buf 3]    (RAM Buffers)
       │                │                │
       └───────────┬────┴────────────────┘
                   ▼
       [ Min-Heap (Size K=3) ] ──> Output Stream File (100GB Sorted) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing a complete External Merge Sort Engine, Chunk Division Generator, and K-Way Min-Heap Stream Merging.

```java
import java.io.*;
import java.util.*;

/**
 * Production-Grade Master Suite Implementing External Merge Sort,
 * Chunk Generator Runs, and K-Way Min-Heap Priority Queue Merging.
 */
public class ExternalSortingMaster {

    /**
     * Node wrapper tracking element value and source run index in Min-Heap.
     */
    public static class HeapNode implements Comparable<HeapNode> {
        public final int val;
        public final int runIndex;

        public HeapNode(int val, int runIndex) {
            this.val = val;
            this.runIndex = runIndex;
        }

        @Override
        public int compareTo(HeapNode o) {
            return Integer.compare(this.val, o.val);
        }
    }

    // =========================================================================
    // 1. K-WAY EXTERNAL MERGE STREAM (O(N log K) Time, O(K) RAM Space)
    // =========================================================================
    /**
     * Merges K sorted run files into a single sorted output file using K-Way Min-Heap.
     *
     * @param runFiles list of temporary sorted run files
     * @param outputFile final output file destination
     */
    public void mergeKSortedRuns(List<File> runFiles, File outputFile) throws IOException {
        int k = runFiles.size();
        BufferedReader[] readers = new BufferedReader[k];
        PriorityQueue<HeapNode> minHeap = new PriorityQueue<>(k);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))) {
            // Step 1: Open readers for all K run files and push first element into Min-Heap
            for (int i = 0; i < k; i++) {
                readers[i] = new BufferedReader(new FileReader(runFiles.get(i)));
                String line = readers[i].readLine();
                if (line != null) {
                    minHeap.add(new HeapNode(Integer.parseInt(line), i));
                }
            }

            // Step 2: Stream minimum elements to output file
            while (!minHeap.isEmpty()) {
                HeapNode minNode = minHeap.poll();

                // Write minimum value to output file
                writer.write(minNode.val + "\n");

                // Read next element from the same run file that produced the min value
                String nextLine = readers[minNode.runIndex].readLine();
                if (nextLine != null) {
                    minHeap.add(new HeapNode(Integer.parseInt(nextLine), minNode.runIndex));
                }
            }
        } finally {
            // Step 3: Close all readers and delete temporary run files
            for (int i = 0; i < k; i++) {
                if (readers[i] != null) readers[i].close();
                runFiles.get(i).delete(); // Cleanup temp files! ⚡
            }
        }
    }

    // =========================================================================
    // 2. CHUNK CREATION PHASE (Splits large data into M-sized sorted runs)
    // =========================================================================
    /**
     * Creates M-sized sorted temp run files from input stream.
     */
    public List<File> createInitialRuns(BufferedReader reader, int chunkSize) throws IOException {
        List<File> runFiles = new ArrayList<>();
        List<Integer> buffer = new ArrayList<>(chunkSize);

        String line;
        while ((line = reader.readLine()) != null) {
            buffer.add(Integer.parseInt(line));

            if (buffer.size() == chunkSize) {
                runFiles.add(writeSortedRun(buffer));
                buffer.clear();
            }
        }

        if (!buffer.isEmpty()) {
            runFiles.add(writeSortedRun(buffer));
        }

        return runFiles;
    }

    private File writeSortedRun(List<Integer> buffer) throws IOException {
        Collections.sort(buffer); // Internal QuickSort / TimSort in RAM

        File tempFile = File.createTempFile("external_run_", ".tmp");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(tempFile))) {
            for (int val : buffer) {
                writer.write(val + "\n");
            }
        }
        return tempFile;
    }
}
```

> **Quick Syntax:**
```java
// K-Way Min-Heap Stream Fetch Line
HeapNode minNode = minHeap.poll(); writer.write(minNode.val + "\n");
```

---

## 7. Concrete Problem Examples & Applications

1. **Big Data Processing (Apache Spark / Hadoop MapReduce)**:
   - External Merge Sort forms the core of MapReduce Shuffle & Sort passes.

2. **Database Engines (PostgreSQL / MySQL InnoDB External Sort)**:
   - Queries returning millions of un-indexed rows (`ORDER BY`) execute External Sort when `work_mem` is exceeded.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.io.*;
import java.util.*;

public class ExternalSortingDemo {

    public static void main(String[] args) throws IOException {
        System.out.println("=================================================");
        System.out.println("   EXTERNAL MERGE SORT DISK ENGINE DEMO          ");
        System.out.println("=================================================\n");

        ExternalSortingMaster master = new ExternalSortingMaster();

        // 1. Simulate Input File Generation
        File inputFile = File.createTempFile("large_input_", ".txt");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(inputFile))) {
            int[] data = {50, 10, 80, 20, 90, 30, 70, 40, 60, 100};
            for (int val : data) writer.write(val + "\n");
        }

        // 2. Phase 1: Chunk Creation (Chunk size M = 3 items)
        List<File> runFiles;
        try (BufferedReader reader = new BufferedReader(new FileReader(inputFile))) {
            runFiles = master.createInitialRuns(reader, 3);
        }
        System.out.println("1. Created " + runFiles.size() + " Sorted Run Files on Disk.");

        // 3. Phase 2: K-Way External Merge Stream
        File outputFile = File.createTempFile("sorted_output_", ".txt");
        master.mergeKSortedRuns(runFiles, outputFile);

        // 4. Verify Sorted Output Stream
        System.out.println("2. Verified Sorted Output File Contents:");
        try (BufferedReader reader = new BufferedReader(new FileReader(outputFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.print(line + " ");
            }
            System.out.println();
        }

        // Cleanup
        inputFile.delete();
        outputFile.delete();
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Sorting Paradigm | Primary Bottleneck | Time Complexity | Auxiliary Space | Disk I/O Pass Count |
| :--- | :--- | :--- | :--- | :--- |
| **Internal Sorting** | CPU Clock Cycles | $\mathbf{O(N \log N)}$ CPU ⚡| $O(1)$ to $O(N)$ RAM | 0 Disk Passes |
| **External Sorting** | **Disk Storage I/O ⚡**| $\mathbf{O(N \log_K (N/M))}$| $O(M)$ RAM Buffers | $\mathbf{\lceil \log_K(N/M) \rceil}$ Passes ⚡|

---

## 10. Edge Cases & Boundary Handling

1. **Memory Allocation Limit Exceeded (`OutOfMemoryError`)**:
   - Set chunk size $M$ to at most $70\%$ of available heap space (`Runtime.getRuntime().maxMemory()`) to account for Java object overhead.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Opening All Run Files Without Heap Bounds**:
  - If $K$ (number of run files) is extremely large ($K > 10,000$), opening $K$ file descriptors simultaneously causes `Too many open files` OS crashes.
  - **Fix**: Perform Multi-Pass Cascading Merges when $K > 1,000$.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Golden Rules of External Sorting:
> 1. **Phase 1 (Chunk Creation)**: Maximizes RAM utilization to create as FEW initial run files as possible ($R = N/M$).
> 2. **Phase 2 (K-Way Merge)**: Maximizes $K$ (Min-Heap size) to reduce total disk merge passes to $\lceil \log_K R \rceil$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Internal Sorting (QuickSort) | External Sorting (Multi-Way Merge) |
| :--- | :--- | :--- |
| **Data Location** | Main Memory (RAM) | Secondary Storage (SSD / Hard Disk) |
| **Access Latency**| ~100 Nanoseconds | ~5 Milliseconds (50,000x Slower!) |
| **Merge Engine** | Sub-array Pointers | **Min-Heap Stream Buffers (Size K)⚡**|

---

## 14. How to Recognize This in Questions

* **"Sort 500GB file when available RAM is only 4GB"** $\rightarrow$ External Multi-Way Merge Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does External Sort use Multi-Way Merge instead of 2-Way Merge?**  
  *A:* Because 2-Way Merge requires $\log_2(N/M)$ disk passes, whereas K-Way Merge requires only $\log_K(N/M)$ passes, reducing expensive disk I/O volume by $O(\log_2 K)$ times.

* **Q: What is Replacement Selection in External Sorting?**  
  *A:* An optimization that uses a Min-Heap during Phase 1 chunk creation to produce initial sorted runs that are, on average, $2M$ in length (twice the RAM size $M$), cutting the initial run count in half!

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: INTERNAL VS EXTERNAL SORTING                          |
+-----------------------------------------------------------------------+
| • Internal Sort : Fits in RAM (N <= M) | CPU & Cache bound            |
| • External Sort : Exceeds RAM (N >> M) | Disk I/O bound               |
| • Phase 1       : Create M-sized sorted run files via internal sort   |
| • Phase 2       : Merge K run streams using Min-Heap (Size K) Priority Q|
| • Disk Passes   : log_K(N/M) Total Disk Read/Write Passes ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can explain the difference between Internal and External Sorting.
- [ ] I can write a K-Way Min-Heap stream merge engine in Java.
- [ ] I can prove why K-Way Merge requires $\lceil \log_K (N/M) \rceil$ disk passes.
- [ ] I can write the chunk creation phase to generate temp run files.
- [ ] I can explain Replacement Selection optimization ($2M$ average run length).
