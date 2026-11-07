# 11. Probability in Algorithms: Linearity of Expectation, Reservoir Sampling & Monte Carlo vs Las Vegas

## 1. Introduction
**Probability & Expected Value in Algorithms** is a core subfield of computer science that powers streaming data sampling, randomized algorithms, game theory, load balancing, and probabilistic data structures. By incorporating randomness into algorithmic design, developers achieve algorithms that are simpler, faster, and immune to worst-case adversarial inputs. Core probabilistic paradigms include **Linearity of Expectation ($E[X + Y] = E[X] + E[Y]$)**, **Reservoir Sampling (LeetCode 382 & 398)** (which samples $K$ items uniformly from an infinite stream in $O(N)$ time and $O(K)$ space), and the distinction between **Las Vegas Algorithms** (always correct, random time) and **Monte Carlo Algorithms** (deterministic time, probabilistic correctness).

> **Important:** Core Structural Properties of Probabilistic Algorithms:
> 1. **Linearity of Expectation Principle**:
>    $$E[X_1 + X_2 + \dots + X_n] = E[X_1] + E[X_2] + \dots + E[X_n]$$
>    - **CRITICAL**: Linearity of expectation holds EVEN IF random variables $X_i$ are DEPENDENT! ⚡
> 2. **Reservoir Sampling Invariant (LeetCode 382 / 398)**:
>    - For a stream of size $N$, item $i$ (1-indexed) is selected with probability $P = \frac{1}{i}$.
>    - Proof of Uniformity: At stream end, every item $i \in \{1 \dots N\}$ has EXACT probability $P = \frac{1}{N}$ of being selected! ⚡
> 3. **Las Vegas vs Monte Carlo Categorization**:
>    - **Las Vegas**: Always correct (100% deterministic correctness), random runtime (e.g. QuickSelect, Randomized QuickSort).
>    - **Monte Carlo**: Deterministic runtime, probabilistic correctness with bounded error $\epsilon$ (e.g. Miller-Rabin Primality Test, Monte Carlo Tree Search).
> 4. **Coupon Collector Expected Time**:
>    $$E[T] = N \times H_N = N \sum_{i=1}^N \frac{1}{i} \approx N \ln N + \gamma N$$ ⚡

```
Reservoir Sampling Stream Invariant Topology (Stream size N unknown):

Stream Element i Arrival (1-indexed):
- Generate random integer rand ∈ [0 ... i-1].
- If rand == 0 (Probability 1/i):
  Replace current reservoir item with Element i!

Proof that Element i is selected at end of stream N:
P(Selected at step i) = 1/i
P(NOT replaced at step i+1) = i / (i + 1)
P(NOT replaced at step i+2) = (i + 1) / (i + 2)
...
P(Final) = (1/i) * (i / (i+1)) * ((i+1) / (i+2)) ... * ((N-1) / N) = 1 / N!

Guarantees 100% Uniform Probability (1/N) for all stream elements! ⚡
```

---

## 2. Core Concepts & Probabilistic Algorithms Strategy Matrix

### 2.1 Probabilistic Algorithms Strategy Matrix
```
Probabilistic Algorithms Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Probabilistic Paradigm| Target Problem    | Time Complexity   | Auxiliary Space   | Key Guarantees    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Reservoir Sampling**| Infinite Stream $N$| **$O(N)$ Single Pass⚡**| **$O(K)$ Memory ⚡**| Exact $1/N$ Uniform|
| **Las Vegas (Quick)** | Selection / Sort  | **$O(N)$ Expected ⚡**| $O(\log N)$ Stack | 100% Correctness  |
| **Monte Carlo (MR)**  | Huge Primality    | **$O(K \log^3 N)$ ⚡**| **$O(1)$ Memory ⚡**| Error $< (1/4)^K$  |
| **Coupon Collector**  | Full Set Coverage | **$O(N \log N)$ ⚡**| $O(N)$ Tracker    | $E[T] = N \ln N$   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Reservoir sampling: for element i, pick with probability 1/i (rand.nextInt(i) == 0); Las Vegas = always correct, random time; Monte Carlo = fixed time, random correctness!"**

---

## 3. Characteristics & Reservoir Sampling Mathematical Proof

### 3.1 Mathematical Proof of Reservoir Sampling Uniformity ($P = \frac{1}{N}$)
* **Goal**: Select 1 random element from an unknown streaming sequence of $N$ elements such that every element has probability $\frac{1}{N}$.
* **Algorithm**:
  - For element $i$ (1-indexed):
    - Pick random integer $R \in [0, i-1]$.
    - If $R = 0$ (probability $\frac{1}{i}$), replace reservoir value with element $i$.
* **Proof by Induction**:
  - **Base Case ($N = 1$)**: Element 1 is picked with probability $\frac{1}{1} = 1$. Correct.
  - **Inductive Hypothesis**: Assume after $k$ elements, every element $j \in \{1 \dots k\}$ in the reservoir has probability $\frac{1}{k}$.
  - **Inductive Step ($N = k + 1$)**:
    - Element $k+1$ is chosen with probability $\frac{1}{k+1}$.
    - For any existing element $j \le k$ to remain in the reservoir, two independent events must occur:
      1. Element $j$ was in the reservoir after step $k$ (Probability = $\frac{1}{k}$).
      2. Element $k+1$ DOES NOT replace element $j$ at step $k+1$ (Probability = $1 - \frac{1}{k+1} = \frac{k}{k+1}$).
    - Probability that element $j$ remains in the reservoir at step $k+1$:
      $$P(j \text{ in reservoir}) = \frac{1}{k} \times \left(1 - \frac{1}{k+1}\right) = \frac{1}{k} \times \frac{k}{k+1} = \frac{1}{k+1}$$
* Proves by induction that every element $i \in \{1 \dots N\}$ has EXACT probability $\frac{1}{N}$ of being selected! ⚡

---

## 4. Internal Working Mechanics: Las Vegas vs Monte Carlo Classification

Tracing QuickSelect (Las Vegas) vs Miller-Rabin (Monte Carlo):

```
1. QuickSelect (Las Vegas Algorithm):
   - Runtime: Random (Best O(N), Worst O(N^2) dependent on pivot choice).
   - Output : ALWAYS 100% CORRECT (Guaranteed exact K-th smallest element!).
   - Re-runs until correct result is achieved. ✅ ⚡

2. Miller-Rabin Primality Test (Monte Carlo Algorithm):
   - Runtime: Deterministic fixed bound O(K log^3 N).
   - Output : Probabilistic correctness.
     - If outputs "Composite": 100% GUARANTEED COMPOSITE!
     - If outputs "Prime": Probabilistic (Error probability < (1/4)^K).
   - Increasing K iterations shrinks error rate exponentially to zero! ✅ ⚡
```

---

## 5. Visual Diagram: Reservoir Sampling Stream Execution

```
Stream Inspection Window (Reservoir Size K = 1):

Element 1: Selected (P = 1/1 = 100%)    ──► Reservoir = [Elem 1]
Element 2: rand(2) == 0 (P = 1/2 = 50%) ──► Replaced! Reservoir = [Elem 2]
Element 3: rand(3) == 0 (P = 1/3 = 33%) ──► Kept Elem 2! Reservoir = [Elem 2]
Element 4: rand(4) == 0 (P = 1/4 = 25%) ──► Kept Elem 2! Reservoir = [Elem 2]

Final Result: Every element 1..4 had EXACT 25% (1/4) chance of surviving! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Reservoir Sampling (LeetCode 382 & 398), Linearity of Expectation Simulator, and Las Vegas QuickSelect Engine.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Probabilistic Algorithms:
 * Reservoir Sampling (LeetCode 382/398), Linearity of Expectation, and Las Vegas QuickSelect.
 */
public class ProbabilityAlgorithmsMaster {

    private final Random random = new Random();

    // =========================================================================
    // 1. LEETCODE 382 / 398: RESERVOIR SAMPLING (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Uniformly samples 1 random element from an unknown input stream in O(N) single pass.
     *
     * @param stream iterator over streaming data elements
     * @return 1 uniformly chosen element from stream
     */
    public int reservoirSampleStream(Iterator<Integer> stream) {
        if (stream == null || !stream.hasNext()) return -1;

        int reservoir = stream.next(); // 1st element selected with P = 1 ⚡
        int count = 1;

        while (stream.hasNext()) {
            count++;
            int currentVal = stream.next();

            // Select current element with probability 1 / count ⚡
            if (random.nextInt(count) == 0) {
                reservoir = currentVal; // Replace reservoir item! ⚡
            }
        }

        return reservoir; // 100% Uniform Probability 1/N ⚡
    }

    /**
     * Uniformly samples K random elements from a stream in O(N) time and O(K) space.
     */
    public int[] reservoirSampleK(Iterator<Integer> stream, int k) {
        if (stream == null || k <= 0) return new int[0];

        int[] reservoir = new int[k];
        int count = 0;

        // Fill first K elements
        while (stream.hasNext() && count < k) {
            reservoir[count] = stream.next();
            count++;
        }

        // Process remaining elements from k+1 to N
        while (stream.hasNext()) {
            count++;
            int currentVal = stream.next();
            int randIdx = random.nextInt(count);

            // Replace element at randIdx if randIdx < k ⚡
            if (randIdx < k) {
                reservoir[randIdx] = currentVal;
            }
        }

        return reservoir;
    }

    // =========================================================================
    // 2. LAS VEGAS RANDOMIZED QUICKSELECT (O(N) Expected Time, O(1) Space)
    // =========================================================================
    /**
     * Finds K-th smallest element in array in expected O(N) time (Las Vegas Algorithm).
     */
    public int quickSelectLasVegas(int[] nums, int k) {
        if (nums == null || k < 1 || k > nums.length) return -1;
        return quickSelect(nums, 0, nums.length - 1, k - 1);
    }

    private int quickSelect(int[] nums, int left, int right, int kIdx) {
        if (left == right) return nums[left];

        // Randomized pivot selection (Las Vegas Property!) ⚡
        int pivotIdx = left + random.nextInt(right - left + 1);
        pivotIdx = partition(nums, left, right, pivotIdx);

        if (kIdx == pivotIdx) {
            return nums[kIdx]; // Always 100% Correct! ⚡
        } else if (kIdx < pivotIdx) {
            return quickSelect(nums, left, pivotIdx - 1, kIdx);
        } else {
            return quickSelect(nums, pivotIdx + 1, right, kIdx);
        }
    }

    private int partition(int[] nums, int left, int right, int pivotIdx) {
        int pivotVal = nums[pivotIdx];
        swap(nums, pivotIdx, right);
        int storeIdx = left;

        for (int i = left; i < right; i++) {
            if (nums[i] < pivotVal) {
                swap(nums, i, storeIdx);
                storeIdx++;
            }
        }

        swap(nums, storeIdx, right);
        return storeIdx;
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Reservoir Sampling Core Line
if (random.nextInt(count) == 0) reservoir = currentVal; // Selects item with exact P = 1 / count
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 382 - Linked List Random Node**:
   - Random node sampling from linked list of unknown length using Reservoir Sampling ($O(N)$ time, $O(1)$ space).

2. **LeetCode 398 - Random Pick Index**:
   - Random index sampling for target value occurrences.

3. **Randomized QuickSelect (LeetCode 215)**:
   - Las Vegas randomized $O(N)$ expected selection engine.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class ProbabilityAlgorithmsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   PROBABILISTIC ALGORITHMS BENCHMARK DEMO       ");
        System.out.println("=================================================\n");

        ProbabilityAlgorithmsMaster master = new ProbabilityAlgorithmsMaster();

        // 1. Reservoir Sampling Single Item Test
        List<Integer> stream = List.of(10, 20, 30, 40, 50, 60, 70, 80, 90, 100);
        int sampledVal = master.reservoirSampleStream(stream.iterator());

        System.out.println("1. Reservoir Sampling 1 Item from Stream of 10 Elements:");
        System.out.println("   Sampled Element: " + sampledVal + " (Uniform Probability P = 1/10)");
        System.out.println("-------------------------------------------------");

        // 2. Reservoir Sampling K Items (K = 3)
        int[] sampledK = master.reservoirSampleK(stream.iterator(), 3);
        System.out.println("2. Reservoir Sampling K = 3 Items from Stream of 10 Elements:");
        System.out.println("   Sampled Array K=3: " + Arrays.toString(sampledK));
        System.out.println("-------------------------------------------------");

        // 3. Las Vegas QuickSelect Test
        int[] nums = {7, 10, 4, 3, 20, 15};
        int k = 3; // 3rd smallest (Optimal = 7)
        int selected = master.quickSelectLasVegas(nums.clone(), k);

        System.out.println("3. Las Vegas Randomized QuickSelect (3rd Smallest in [7, 10, 4, 3, 20, 15]):");
        System.out.println("   3rd Smallest Element: " + selected + " (Optimal = 7)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Probabilistic Algorithm | Paradigm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Reservoir Sampling** | Streaming Uniform | $\mathbf{O(N)}$ Single Pass⚡| $\mathbf{O(1)}$ Memory ⚡| `rand.nextInt(count)==0` |
| **QuickSelect** | Las Vegas | $\mathbf{O(N)}$ Expected ⚡| $O(\log N)$ Stack | Always 100% correct |
| **Miller-Rabin** | Monte Carlo | $\mathbf{O(K \log^3 N)}$ ⚡| $\mathbf{O(1)}$ Memory ⚡| Error $< (1/4)^K$ |

---

## 10. Edge Cases & Boundary Handling

1. **Empty Input Stream**:
   - Returns `-1` or empty array `[]`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Loading Full Streaming Dataset into RAM Array for Sampling**:
  - Loading an unknown infinite stream of $10^9$ items into an `ArrayList` causes `OutOfMemoryError`. **ALWAYS use Reservoir Sampling to sample in $O(N)$ single pass using $O(1)$ memory!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Reservoir Sampling Rule:
> For a stream of unknown size $N$, sample the $i$-th element with probability **$P = \frac{1}{i}$** (`random.nextInt(i) == 0`), guaranteeing every item has exact uniform probability **$\frac{1}{N}$**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Full Array In-Memory Shuffle | Reservoir Sampling |
| :--- | :--- | :--- |
| **Memory Footprint** | $O(N)$ Memory Array (OOM Risk) | **$O(1)$ Strict Memory ⚡** |
| **Stream Capability**| Requires Known Size $N$ | **Unknown Infinite Stream $N$ ⚡** |
| **Uniformity** | 100% Uniform | **100% Guaranteed Uniform ⚡** |

---

## 14. How to Recognize This in Questions

* **"Randomly pick a node from linked list of unknown length in O(1) space"** $\rightarrow$ LeetCode 382 (Reservoir Sampling).
* **"Randomly pick an index for target value in O(1) extra space"** $\rightarrow$ LeetCode 398.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Reservoir Sampling guarantee equal probability $\frac{1}{N}$ for all elements?**  
  *A:* By selecting element $i$ with probability $\frac{1}{i}$ and keeping it through subsequent steps $(1 - \frac{1}{i+1}) \times (1 - \frac{1}{i+2}) \dots (1 - \frac{1}{N}) = \frac{i}{N}$. Multiplying $\frac{1}{i} \times \frac{i}{N}$ yields exact probability $\frac{1}{N}$.

* **Q: What is the difference between Las Vegas and Monte Carlo algorithms?**  
  *A:* Las Vegas algorithms ALWAYS produce 100% correct outputs with random runtime (e.g. QuickSelect). Monte Carlo algorithms run in deterministic fixed time with probabilistic correctness (e.g. Miller-Rabin).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PROBABILITY IN ALGORITHMS                             |
+-----------------------------------------------------------------------+
| • Reservoir Sampling: for item i, select if (random.nextInt(i) == 0)   |
| • Uniformity Proof  : P(Selected) = (1/i) * (i/(i+1)) ... = 1/N ⚡    |
| • Linearity of Exp  : E[X + Y] = E[X] + E[Y] (Holds even if dependent!)|
| • Las Vegas         : 100% Correct Output, Random Runtime (QuickSelect)|
| • Monte Carlo       : Fixed Runtime, Probabilistic Correctness (Miller)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Reservoir Sampling for 1 item in Java (LeetCode 382).
- [ ] I can write Reservoir Sampling for $K$ items in Java.
- [ ] I can write Las Vegas Randomized QuickSelect in Java.
- [ ] I can prove why Reservoir Sampling produces uniform $\frac{1}{N}$ probability.
- [ ] I can state the difference between Las Vegas and Monte Carlo algorithms.
