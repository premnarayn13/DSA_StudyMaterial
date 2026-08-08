# 05. Amortized Analysis

## 1. Introduction
Amortized analysis evaluates the average time required per operation over a sequence of $N$ operations, guaranteeing an upper bound even when occasional individual operations are expensive. In technical interviews, amortized bounds explain why dynamic data structures like Java's `ArrayList` offer constant-time performance overall despite occasional array copy reallocations.

> **Important:** Amortized complexity is NOT Average-Case complexity! Amortized analysis guarantees a deterministic worst-case average over a sequence of operations without making probabilistic assumptions about input distribution.

## 2. Core Concepts
* **Amortized Bound Formula**: Amortized Cost = $\frac{\text{Total Cost of } N \text{ Sequential Operations}}{N}$.
* **Dynamic Array Growth**: When a Java `ArrayList` fills up, it creates a new backing array of size $1.5 \times \text{capacity}$ (or $2 \times$), copies all elements over ($O(n)$ work), and inserts the new item.
* **Cost Spreading**: The heavy $O(n)$ cost of array copying occurs so infrequently that spreading it over all prior $O(1)$ insertions yields an **Amortized $O(1)$** cost per insertion.

> **Memory Trick:** **"Pay a Small Tax Early to Cover Rare Large Costs"**. Think of amortized analysis like paying a annual subscription fee in tiny monthly installments.

## 3. Characteristics / Properties
* **Three Analysis Methods**:
  1. **Aggregate Method**: Calculate total time $T(n)$ for $n$ operations and compute $T(n)/n$.
  2. **Accounting (Banker's) Method**: Charge higher virtual "credits" on cheap operations to pay for future expensive operations.
  3. **Potential Method**: Define a potential function $\Phi(S)$ representing energy stored in data structure state.
* **Deterministic Guarantee**: Applies to worst-case sequence execution—no random probability required.

## 4. Internal Working
Tracing `ArrayList` dynamic resizing behavior with doubling factor:

```
Insert 1..4  : [X][X][X][X]                 (Capacity = 4, Cost per push = 1)
Insert 5     : [X][X][X][X][X][_][_][_]     (Array DOUBLES to 8! Cost = 4 copies + 1 push = 5)
Insert 6..8  : [X][X][X][X][X][X][X][X]     (Capacity = 8, Cost per push = 1)
Insert 9     : Array DOUBLES to 16!         (Cost = 8 copies + 1 push = 9)

Total Cost for N pushes = N + (1 + 2 + 4 + 8 + ... + N) <= N + 2N = 3N operations.
Amortized Cost per Push = 3N / N = O(1) constant time!
```

## 5. Visual Diagram
Cost Spike Spreading Visualization:

```
  Operation Cost
    ^
 O(n)|                  | (Array Doubling Reallocation Spike)
     |                  |
 O(1)|  _  _  _  _  _  _| _  _  _  _  _  _  _
     +-----------------------------------------> Operation Sequence (1..N)
        [ Spreading the Spike over N steps gives Amortized O(1) Ceiling ]
```

## 6. Operations / Algorithms
Proving Amortized $O(1)$ using the Aggregate Method:
1. Let $c_i = 1$ if index $i$ is not a power of 2.
2. Let $c_i = i$ if index $i$ is a power of 2 (triggers capacity doubling).
3. Total cost $T(N) = \sum_{i=1}^{N} c_i = N + \sum_{k=0}^{\lfloor\log_2 N\rfloor} 2^k < N + 2N = 3N$.
4. Amortized cost = $\frac{T(N)}{N} = \frac{3N}{N} = O(1)$.

> **Quick Syntax:**
```java
// Java ArrayList resizing factor proof (JDK 8+ uses newCapacity = oldCapacity + (oldCapacity >> 1))
int oldCapacity = elementData.length;
int newCapacity = oldCapacity + (oldCapacity >> 1); // 1.5x expansion growth factor
```

## 7. Examples
* **`ArrayList.add(element)`**: Amortized $O(1)$ time (Worst case single operation is $O(n)$).
* **Dynamic Table Insertion**: Amortized $O(1)$ space/time.
* **Monotonic Queue / Stack Operations**: Amortized $O(1)$ per push/pop despite nested loops popping elements.
* **Disjoint Set Union (DSU) with Path Compression**: Amortized $O(\alpha(n))$ time per operation (where $\alpha$ is Inverse Ackermann function $\le 4$).

## 8. Java Code
Demonstrating dynamic array reallocation cost and proving amortized $O(1)$ execution:

```java
import java.util.Arrays;

public class AmortizedAnalysisDemo {

    static class CustomDynamicArray {
        private int[] data;
        private int size;
        private int capacity;
        private long totalOpsCount;

        public CustomDynamicArray() {
            this.capacity = 2; // Initial capacity
            this.data = new int[capacity];
            this.size = 0;
            this.totalOpsCount = 0;
        }

        public void add(int element) {
            totalOpsCount++; // Cost of insert
            if (size == capacity) {
                // Reallocate & copy
                capacity *= 2;
                int[] newData = new int[capacity];
                for (int i = 0; i < size; i++) {
                    newData[i] = data[i];
                    totalOpsCount++; // Cost of copying each element
                }
                data = newData;
            }
            data[size++] = element;
        }

        public double getAmortizedCost() {
            return (double) totalOpsCount / size;
        }
    }

    public static void main(String[] args) {
        CustomDynamicArray array = new CustomDynamicArray();
        int N = 1000000; // 1 Million inserts

        for (int i = 1; i <= N; i++) {
            array.add(i);
        }

        System.out.println("Pushed " + N + " elements.");
        System.out.println("Total operations executed (Includes copying): " + array.totalOpsCount);
        System.out.println("Amortized cost per push: " + array.getAmortizedCost() + " (Constant O(1))");
    }
}
```

## 9. Complexity Analysis
| Operation | Worst-Case Single Op | Amortized Complexity | Reason |
| :--- | :--- | :--- | :--- |
| **`ArrayList.add()`** | $O(n)$ | **Amortized $O(1)$** | Array reallocation occurs exponentially infrequently |
| **Monotonic Stack Push** | $O(n)$ | **Amortized $O(1)$** | Each element is pushed and popped at most ONCE |
| **DSU Find with Path Compression**| $O(n)$ | **Amortized $O(\alpha(n))$**| Pointer paths flatten permanently on search |
| **KMP String Matching Loop** | $O(n)$ | **Amortized $O(1)$ per char**| Pattern index fallback steps bounded by string length |

## 10. Edge Cases
* **Shrinking Dynamic Arrays (Thrashing Risk)**: If an array halves capacity as soon as it drops below 50% utilization, alternating `add()` and `delete()` at the boundary triggers $O(n)$ copy operations on EVERY operation!
  * **Solution**: Shrink capacity to half ONLY when array drops to **25% utilization** (Quarter-full rule).

## 11. Common Mistakes
* Confusing Amortized $O(1)$ with Average-Case $O(1)$. (Average case relies on input randomness; Amortized case holds even for worst-case input sequences).
* Stating that `ArrayList.add()` is strictly $O(1)$ without mentioning the word **Amortized**.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why does Java's `ArrayList` grow by $1.5\times$ instead of $2\times$? Growing by $1.5\times$ (via `oldCapacity + (oldCapacity >> 1)`) allows the memory manager to reuse previously deallocated memory blocks in future reallocations, improving memory fragmentation behavior.

> **Memory Trick:** **"Monotonic Stack = Amortized O(1)"**. Even if a `while` loop inside a `for` loop pops elements, each element enters the stack once and leaves once $\implies$ Total pops across $N$ iterations $\le N \implies$ Amortized $O(1)$.

## 13. Comparisons
| Metric | Worst-Case Single Op | Average-Case | Amortized Case |
| :--- | :--- | :--- | :--- |
| **Assumption** | Worst input possible | Random uniform input distribution | Sequence of $N$ ops on worst input |
| **ArrayList `add()`** | $O(n)$ | $O(1)$ | **Amortized $O(1)$** |
| **Deterministic?** | Yes | No (Statistical) | **Yes (Guaranteed over sequence)** |

## 14. How to Recognize This in Questions
* **"Explain complexity of building a stack with dynamic array"** $\rightarrow$ Highlight **Amortized $O(1)$**.
* **"Loop contains inner while loop popping elements"** $\rightarrow$ Check if total pops over all iterations are bounded by $N$ $\rightarrow$ **Amortized $O(1)$**.

## 15. Frequently Asked Interview Questions
* **Q: What is the difference between Amortized Time and Average-Case Time?**  
  *A:* Average-case depends on the probability distribution of inputs. Amortized time guarantees an average performance per operation over ANY sequence of operations, independent of input randomness.
* **Q: What is the Inverse Ackermann Function $\alpha(n)$?**  
  *A:* $\alpha(n)$ is a extremely slow-growing function. For all practical physical universe values of $n$ (up to $10^{80}$ atoms), $\alpha(n) \le 4$. Thus, Amortized $O(\alpha(n))$ is functionally constant time $O(1)$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: AMORTIZED ANALYSIS                                    |
+-----------------------------------------------------------------------+
| • Amortized Complexity = Total Cost of N Operations / N               |
| • ArrayList.add() = Amortized O(1) [Worst-case single push = O(n)]    |
| • Java ArrayList Growth Factor = 1.5x (oldCapacity + (oldCapacity>>1))|
| • Prevents Thrashing: Shrink array at 25% capacity, NOT 50%           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can state the formal mathematical definition of Amortized Analysis.
- [ ] I can prove why dynamic array doubling yields Amortized $O(1)$ insertion.
- [ ] I know why Java uses $1.5\times$ growth factor instead of $2\times$.
- [ ] I can explain the difference between Amortized $O(1)$ and Average-Case $O(1)$.
- [ ] I know how to avoid thrashing during dynamic array shrinking.
