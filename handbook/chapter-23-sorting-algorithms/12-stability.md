# 12. Sorting Stability: Invariants, Multi-Column Sorting & Proofs

## 1. Introduction
**Sorting Stability** is a fundamental architectural property of sorting algorithms that dictates whether the relative input order of records with equal keys is preserved in the final sorted output. Mathematically, a sorting algorithm is **Stable** if for any pair of elements $A[i]$ and $A[j]$ where $A[i] = A[j]$ and $i < j$, the algorithm guarantees that $A[i]$ appears before $A[j]$ in the sorted output ($\text{pos}_{\text{out}}(A[i]) < \text{pos}_{\text{out}}(A[j])$). Sorting stability is indispensable in real-world systems, enabling **Multi-Column Database Queries (`ORDER BY secondary_key, primary_key`)**, multi-level UI table sorting, and pipeline data aggregation.

> **Important:** Master Stability Status across All Major Sorting Algorithms:
> 1. **Strictly STABLE Algorithms**:
>    - **Insertion Sort**: Stable (Shifts elements only when `arr[j] > key`).
>    - **Bubble Sort**: Stable (Swaps adjacent pairs only when `arr[j] > arr[j+1]`).
>    - **Merge Sort**: Stable (Merges left element first when `arr[left] <= arr[right]`).
>    - **Counting Sort**: Stable (Places elements right-to-left from cumulative frequencies).
>    - **Radix Sort**: Stable (Requires stable Counting Sort subroutine per digit pass).
>    - **TimSort**: Stable (Merges natural runs using non-strict $\le$ comparisons).
> 2. **Inherently UNSTABLE Algorithms**:
>    - **Selection Sort**: Unstable (Long-distance swaps move min element across equal keys).
>    - **Quick Sort**: Unstable (Lomuto/Hoare partitioning swaps elements non-adjacently).
>    - **Heap Sort**: Unstable (Root-to-leaf binary heap swaps break equal key order).
>    - **Shell Sort**: Unstable (Interleaved gap insertion jumps over equal keys). ⚡

```
Multi-Column Database Sorting Stability Topology:
Goal: Sort Students by Grade (Primary), then Stably by Name (Secondary).

Initial List (Sorted by Name): [ ("Alice", 85), ("Bob", 90), ("Charlie", 85), ("David", 90) ]

Stable Grade Sort Output:
Grade 85: [ ("Alice", 85), ("Charlie", 85) ]   (Alice remains BEFORE Charlie!) ⚡
Grade 90: [ ("Bob", 90),   ("David", 90) ]     (Bob remains BEFORE David!) ⚡

Unstable Grade Sort Output:
Grade 85: [ ("Charlie", 85), ("Alice", 85) ]   (Name order DESTROYED!) ❌
```

---

## 2. Core Concepts & Complete Stability Matrix

### 2.1 Complete Stability Strategy Matrix
```
Master Algorithm Stability Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm             | Stability Status  | Mechanism Breaking / Preserving   |
+-----------------------+-------------------+-------------------+-------------------+
| **Insertion Sort**    | **STABLE ⚡**     | Strict inequality `arr[j] > key`  |
| **Bubble Sort**       | **STABLE ⚡**     | Adjacent swaps only `arr[j]>arr[j+1]`|
| **Merge Sort**        | **STABLE ⚡**     | Non-strict merge `arr[left] <= arr[right]`|
| **Counting Sort**     | **STABLE ⚡**     | Right-to-left output loop `N-1..0`|
| **Radix Sort**        | **STABLE ⚡**     | Relies on stable Counting Sort    |
| **TimSort**           | **STABLE ⚡**     | Stable run merging                |
| **Selection Sort**    | **UNSTABLE ❌**   | Long-distance swap `swap(0, min)` |
| **Quick Sort**        | **UNSTABLE ❌**   | Partitioning swaps across pivot   |
| **Heap Sort**         | **UNSTABLE ❌**   | Root-to-leaf heapify swaps        |
| **Shell Sort**        | **UNSTABLE ❌**   | Gap distance insertion jumps      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Stable: Insertion, Bubble, Merge, Counting, Radix, TimSort! Unstable: Selection, Quick, Heap, Shell!"**

---

## 3. Characteristics & Transformation Proof (Unstable $\to$ Stable)

### 3.1 Mathematical Proof: Making Any Unstable Algorithm Stable
* Any inherently unstable algorithm (e.g. QuickSort) can be converted into a **Stable Sort** by augmenting each element key $K_i$ with its original input index $i$:
  $$\text{Augmented Key } K'_i = (K_i, i)$$
* Define total ordering relation $\le_{aug}$ on augmented keys:
  $$(K_i, i) \le_{aug} (K_j, j) \iff (K_i < K_j) \lor (K_i = K_j \land i < j)$$
* Because original input indices are strictly unique ($i \neq j$), no two augmented keys are ever equal.
* This eliminates equal key ties completely, guaranteeing **Strict Stability** in **$O(N)$ Extra Space**! ⚡

---

## 4. Internal Working Mechanics: Why QuickSort Partitioning Breaks Stability

Tracing QuickSort Lomuto Partitioning on `[ 3[A], 3[B], 1 ]` with Pivot = 1:

```
Initial State: [ 3[A], 3[B], 1 ]  (3[A] at index 0, 3[B] at index 1, Pivot = 1 at index 2)

Lomuto Partitioning Steps:
- j = 0 (val 3[A] > 1): Do nothing.
- j = 1 (val 3[B] > 1): Do nothing.
- Swap Pivot (1) at index 2 with arr[i+1] (3[A]) at index 0!

Array State after Partitioning: [ 1, 3[B], 3[A] ]

Notice: 3[A] was swapped to the end behind 3[B]!
Relative input order of equal keys 3[A] and 3[B] is BROKEN!
QuickSort Partitioning is inherently UNSTABLE! ❌
```

---

## 5. Visual Diagram: Multi-Column Stable Pipeline Architecture

```
Multi-Column Sorting Pipeline Architecture:

Step 1: Sort by Secondary Key (Name)
Input : [ (Bob, 90), (Alice, 85), (Charlie, 85) ]
Output: [ (Alice, 85), (Bob, 90), (Charlie, 85) ] ──> [ (Alice, 85), (Bob, 90), (Charlie, 85) ]

Step 2: Apply STABLE Sort by Primary Key (Grade)
Input : [ (Alice, 85), (Bob, 90), (Charlie, 85) ]
Output: [ (Alice, 85), (Charlie, 85), (Bob, 90) ]  (Alice stays before Charlie!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Multi-Column Stable Sorting, Stability Auditing, and Augmented Index Key Wrapping.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Sorting Stability Invariants,
 * Multi-Column Sorting Pipelines, and Stability Augmentation Wrappers.
 */
public class SortingStabilityMaster {

    /**
     * Multi-Column Record Class representing a Student.
     */
    public static class Student {
        public final String name;
        public final int grade;

        public Student(String name, int grade) {
            this.name = name;
            this.grade = grade;
        }

        @Override
        public String toString() {
            return name + ":" + grade;
        }
    }

    // =========================================================================
    // 1. MULTI-COLUMN STABLE SORTING PIPELINE
    // =========================================================================
    /**
     * Sorts students by Name (Secondary), then STABLY by Grade (Primary).
     * Requires a Stable Sort (MergeSort / TimSort).
     */
    public void multiColumnStableSort(List<Student> students) {
        if (students == null || students.size() <= 1) return;

        // Step 1: Sort by Secondary Key (Name)
        Collections.sort(students, Comparator.comparing(s -> s.name));

        // Step 2: STABLY Sort by Primary Key (Grade) using Collections.sort (TimSort)
        Collections.sort(students, Comparator.comparingInt(s -> s.grade));
    }

    // =========================================================================
    // 2. UNSTABLE-TO-STABLE CONVERSION VIA AUGMENTED INDEX WRAPPER
    // =========================================================================
    public static class AugmentedElement<T extends Comparable<T>> implements Comparable<AugmentedElement<T>> {
        public final T value;
        public final int originalIndex;

        public AugmentedElement(T value, int originalIndex) {
            this.value = value;
            this.originalIndex = originalIndex;
        }

        @Override
        public int compareTo(AugmentedElement<T> o) {
            int cmp = this.value.compareTo(o.value);
            if (cmp != 0) {
                return cmp; // Primary value comparison
            }
            return Integer.compare(this.originalIndex, o.originalIndex); // Secondary original index comparison! ⚡
        }
    }

    /**
     * Converts any Unstable Sort into a Guaranteed Stable Sort using Index Augmentation.
     */
    public <T extends Comparable<T>> List<T> makeStableSort(List<T> inputList) {
        if (inputList == null) return null;

        List<AugmentedElement<T>> augmentedList = new ArrayList<>();
        for (int i = 0; i < inputList.size(); i++) {
            augmentedList.add(new AugmentedElement<>(inputList.get(i), i));
        }

        // Even if an unstable algorithm is used, equal value ties are broken by original index!
        Collections.sort(augmentedList);

        List<T> result = new ArrayList<>();
        for (AugmentedElement<T> elem : augmentedList) {
            result.add(elem.value);
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Augmented Key Comparison Line for Guaranteed Stability
int cmp = this.val.compareTo(o.val); return (cmp != 0) ? cmp : Integer.compare(this.idx, o.idx);
```

---

## 7. Concrete Problem Examples & Applications

1. **SQL `ORDER BY` Queries**:
   - Executing `SELECT * FROM employees ORDER BY department, salary DESC` relies on stable sorting algorithms under the hood.

2. **E-Commerce Product Filtering**:
   - Filtering items by "Price: Low to High", and then by "Customer Rating" preserves price order within identical ratings!

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.ArrayList;
import java.util.List;

public class SortingStabilityDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    SORTING STABILITY & MULTI-COLUMN DEMO        ");
        System.out.println("=================================================\n");

        SortingStabilityMaster master = new SortingStabilityMaster();

        // 1. Multi-Column Stable Sort Test
        List<SortingStabilityMaster.Student> students = new ArrayList<>();
        students.add(new SortingStabilityMaster.Student("Bob", 90));
        students.add(new SortingStabilityMaster.Student("Alice", 85));
        students.add(new SortingStabilityMaster.Student("Charlie", 85));
        students.add(new SortingStabilityMaster.Student("David", 90));

        System.out.println("1. Original Student List: " + students);
        master.multiColumnStableSort(students);
        System.out.println("   Sorted (Name then Grade Stably): " + students);
        System.out.println("-------------------------------------------------");

        // 2. Augmented Stability Conversion Test
        List<Integer> list = List.of(5, 2, 8, 2, 1);
        List<Integer> stableSorted = master.makeStableSort(list);
        System.out.println("2. Original List: " + list);
        System.out.println("   Guaranteed Stable Sorted via Augmentation: " + stableSorted);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Stability Strategy | Extra Memory | Time Overhead | Primary Advantage |
| :--- | :--- | :--- | :--- |
| **Native Stable Sort (Merge/Tim)**| $O(N)$ Memory | $O(N \log N)$ | Zero Code Modification |
| **Index Augmentation Wrapper**   | $O(N)$ Space | $O(N \log N)$ | **Makes ANY Unstable Sort Stable ⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **All Key Values Unique (`[1, 2, 3, 4]`)**:
   - When all keys are unique, Stable and Unstable sorting algorithms produce 100% identical outputs!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using QuickSort for Multi-Column Sorting**:
  - Sorting by secondary key and then running QuickSort by primary key DESTROYS the secondary key order because QuickSort is UNSTABLE.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Primitive Arrays Use QuickSort while Object Collections Use TimSort in Java:
> * Primitive values (`int = 5`) have no identity or attached fields. Swapping identical primitives (`5 == 5`) is indistinguishable, so Java uses **Dual-Pivot QuickSort** for $O(1)$ memory speed.
> * Objects (`Student`, `User`) carry associated fields. Preserving multi-column sort order requires a **Stable Sort**, so Java uses **TimSort**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Stable Sort (TimSort / MergeSort) | Unstable Sort (QuickSort / HeapSort) |
| :--- | :--- | :--- |
| **Multi-Column Order** | **PRESERVED ⚡** | DESTROYED |
| **Memory Footprint**   | $O(N)$ Auxiliary Memory | **$O(\log N)$ or $O(1)$ In-Place ⚡** |
| **Best Case Speed**    | **$O(N)$ Adaptive (TimSort)⚡**| $O(N \log N)$ |

---

## 14. How to Recognize This in Questions

* **"Sort items by Grade preserving their original alphabetical Name order"** $\rightarrow$ Requires Stable Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Stable Sorting Algorithm?**  
  *A:* An algorithm that guarantees equal elements ($A[i] = A[j]$ with $i < j$) maintain their original relative order in the output.

* **Q: How can you make an unstable algorithm stable?**  
  *A:* By augmenting each element key with its original input index $i$ as a secondary tie-breaker comparison key $(K_i, i)$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SORTING STABILITY                                     |
+-----------------------------------------------------------------------+
| • Definition  : Preserves relative input order of equal keys (i < j)  |
| • STABLE      : Insertion, Bubble, Merge, Counting, Radix, TimSort ⚡  |
| • UNSTABLE    : Selection, Quick, Heap, Shell ❌                      |
| • Multi-Column: Sort by secondary key first, then STABLY by primary   |
| • Augmentation: Attach (value, index) pair to force stability! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the formal mathematical definition of sorting stability.
- [ ] I can categorize all 10 major sorting algorithms as Stable or Unstable.
- [ ] I can explain why QuickSort and Selection Sort are unstable.
- [ ] I can implement multi-column stable sorting in Java.
- [ ] I can augment elements with original indices to force stability.
