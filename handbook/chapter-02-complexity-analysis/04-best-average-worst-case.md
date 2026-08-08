# 04. Best, Average & Worst Case Analysis

## 1. Introduction
Algorithmic performance varies dynamically depending on input configuration, ordering, and data distribution. Evaluating an algorithm requires understanding three distinct operational cases: Best Case (optimistic scenario), Worst Case (pessimistic scenario), and Average Case (expected statistical scenario).

> **Important:** Technical interviewers prioritize **Worst-Case Analysis** to guarantee system stability under maximum load, followed by **Average-Case Analysis** for practical performance expectations.

## 2. Core Concepts
* **Best Case**: The input configuration that requires the minimum possible steps for input size $n$. Represented by $\Omega(g(n))$.
* **Worst Case**: The input configuration that requires the maximum possible steps for input size $n$. Represented by $O(g(n))$.
* **Average Case**: The expected step count over all possible input permutations of size $n$, assuming a uniform probability distribution. Represented by $\Theta(g(n))$ when tightly bounded.

> **Memory Trick:** **"Best = First Try, Worst = Last Try, Average = Random Expectations"**.

## 3. Characteristics / Properties
* **Input-Dependent Variability**:
  * Linear Search: Target at index `0` $\rightarrow$ Best $O(1)$; Target absent $\rightarrow$ Worst $O(n)$; Random index $\rightarrow$ Avg $O(n/2) = O(n)$.
* **Pivot Vulnerability (Quick Sort)**:
  * Best/Avg Case: Balanced partition splits array in half $\rightarrow O(n \log n)$.
  * Worst Case: Unbalanced partition (already sorted array with first element as pivot) $\rightarrow O(n^2)$.
* **Inherent Stability (Merge Sort)**:
  * Best = Worst = Average = $\Theta(n \log n)$ (Input distribution does NOT change execution steps).

## 4. Internal Working
Execution tree comparison between Quick Sort Average Case vs Worst Case:

```
[ Balanced Partition (Average Case: O(n log n)) ]
                    [ N ]
                  /       \
             [ N/2 ]     [ N/2 ]           <-- Log₂ N levels of recursion
             /     \     /     \
         [ N/4 ] [N/4] [N/4]  [N/4]

[ Unbalanced Partition (Worst Case: O(n²)) ]
                    [ N ]
                   /     \
                 [1]   [ N-1 ]
                       /     \             <-- N levels of recursion!
                     [1]   [ N-2 ]
```

## 5. Visual Diagram
Input State Spectrum:

```
   BEST CASE                     AVERAGE CASE                     WORST CASE
  (Optimistic)                    (Expected)                     (Pessimistic)
-------|------------------------------|-------------------------------|------->
  Linear Search:                Linear Search:                  Linear Search:
  Target at index 0             Target at index n/2             Target at index n-1
  (1 comparison)                (n/2 comparisons)               (n comparisons)
```

## 6. Operations / Algorithms
Analyzing input cases systematically:
1. **Identify Best Case**: Find the input layout that triggers early loops, hits cached values, or exits immediately.
2. **Identify Worst Case**: Construct an adversarial input that forces all conditional checks to fail or loops to complete fully.
3. **Calculate Average Case**: Sum step counts across all $P$ valid input permutations and divide by $P$: $T_{avg}(n) = \sum \frac{P_i \cdot T(P_i)}{P}$.

> **Quick Syntax:**
```java
// Quick Sort Randomized Pivot Selection (Mitigates Worst-Case O(n^2))
int randomIndex = left + random.nextInt(right - left + 1);
swap(arr, left, randomIndex); // Converts Worst-Case input into Average Case O(n log n)
```

## 7. Examples
* **Linear Search**: Best $\Omega(1)$, Average $\Theta(n)$, Worst $O(n)$.
* **Quick Sort**: Best $\Omega(n \log n)$, Average $\Theta(n \log n)$, Worst $O(n^2)$.
* **Insertion Sort**: Best $\Omega(n)$ (already sorted), Average $\Theta(n^2)$, Worst $O(n^2)$ (reverse sorted).
* **Hash Table Lookup**: Best $\Omega(1)$, Average $\Theta(1)$, Worst $O(n)$ (all keys collide into same bucket).

## 8. Java Code
Demonstrating input configuration impacts on Insertion Sort performance:

```java
public class InputCaseAnalysisDemo {

    // Insertion Sort demonstrating Best-Case O(n) vs Worst-Case O(n^2)
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        long comparisons = 0;

        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && arr[j] > key) {
                comparisons++;
                arr[j + 1] = arr[j];
                j--;
            }
            if (j >= 0) comparisons++; // Count final failed check
            arr[j + 1] = key;
        }

        System.out.println("Sorted " + n + " elements with " + comparisons + " comparisons.");
    }

    public static void main(String[] args) {
        int[] bestCase = {1, 2, 3, 4, 5, 6, 7, 8};  // Already sorted -> Best Case
        int[] worstCase = {8, 7, 6, 5, 4, 3, 2, 1}; // Reverse sorted -> Worst Case

        System.out.print("BEST CASE: ");
        insertionSort(bestCase);

        System.out.print("WORST CASE: ");
        insertionSort(worstCase);
    }
}
```

## 9. Complexity Analysis
| Algorithm | Best Case ($\Omega$) | Average Case ($\Theta$) | Worst Case ($O$) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| **Binary Search** | $\Omega(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Insertion Sort** | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Quick Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n^2)$ | $O(\log n)$ call stack |
| **Merge Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n \log n)$ | $O(n)$ auxiliary |
| **HashMap Lookup** | $\Omega(1)$ | $\Theta(1)$ | $O(n)$ | $O(n)$ space |

## 10. Edge Cases
* **Adversarial Inputs**: Input arrays sorted in reverse order trigger worst-case $O(n^2)$ in naive Quick Sort or Insertion Sort.
* **Hash Collision Attacks**: Crafting keys with matching hash codes forces Java `HashMap` buckets to degrade from $O(1)$ to $O(n)$ (mitigated to $O(\log n)$ in Java 8+ via Red-Black Trees).

## 11. Common Mistakes
* Assuming Average-Case time complexity is simply $\frac{\text{Best} + \text{Worst}}{2}$. (Average case requires rigorous probability expectation over all permutations!).
* Stating Quick Sort is always $O(n \log n)$ without acknowledging its $O(n^2)$ worst case.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** In Java 8+, `HashMap` mitigates worst-case hash collisions! When a single bucket exceeds 8 nodes (`TREEIFY_THRESHOLD`), Java converts the bucket from a Singly Linked List ($O(n)$ worst-case) into a Red-Black Tree ($O(\log n)$ worst-case).

> **Memory Trick:** **"Randomize to Avoid Worst Case"**. Randomly shuffling the input array or choosing a random pivot eliminates adversarial worst-case inputs in Quick Sort.

## 13. Comparisons
| Feature | Best Case | Average Case | Worst Case |
| :--- | :--- | :--- | :--- |
| **Notation** | Big-Omega ($\Omega$) | Big-Theta ($\Theta$) / Big-O ($O$) | Big-O ($O$) |
| **Utility** | Ideal conditions | Real-world expectation | Safety guarantee / SLA |
| **Primary Use** | Theoretical proof | Performance benchmarking | Production system design |

## 14. How to Recognize This in Questions
* **"Guarantee performance regardless of initial order"** $\rightarrow$ Choose Merge Sort ($O(n \log n)$ worst case) over Quick Sort.
* **"Optimized for nearly sorted arrays"** $\rightarrow$ Choose Insertion Sort ($\Omega(n)$ best case).

## 15. Frequently Asked Interview Questions
* **Q: Why does Java use Dual-Pivot Quicksort for primitives but Timsort for Objects?**  
  *A:* Primitives don't require stability, and Dual-Pivot Quicksort provides outstanding average-case speed with cache locality. Object sorting requires **stability** (preserving equal item order), which Timsort guarantees in $O(n \log n)$ time and $O(n)$ best-case time.
* **Q: What is the worst-case space complexity of Quick Sort?**  
  *A:* $O(n)$ call stack depth when partitions are completely unbalanced ($n-1$ recursive calls). Average stack depth is $O(\log n)$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BEST, AVERAGE & WORST CASE                            |
+-----------------------------------------------------------------------+
| • Best Case = Ω(n) Optimistic | Worst Case = O(n) Pessimistic Guarantee|
| • Quick Sort: Best/Avg O(n log n) | Worst O(n²) on sorted array        |
| • Java 8 HashMap Treeification: Bucket > 8 nodes converts List->RB Tree|
| • Timsort: O(n log n) worst-case stable sort used for Java Objects     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can define Best, Average, and Worst case complexities with example inputs.
- [ ] I know why naive Quick Sort degrades to $O(n^2)$ on sorted arrays.
- [ ] I know how Java 8 handles HashMap bucket collisions using Red-Black Trees.
- [ ] I understand why Timsort is used for sorting Java objects instead of Quick Sort.
- [ ] I can explain the role of randomized pivot selection in Quick Sort.
