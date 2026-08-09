# 09. Reorganize String, Character Frequency Heap Interleaving & Even/Odd Placement

## 1. Introduction
**Reorganize String (LeetCode 767)** requires rearranging characters in a string such that no two adjacent characters are identical. If any character appears with a frequency strictly greater than $\lfloor (N + 1) / 2 \rfloor$ (where $N$ is string length), reorganization is mathematically IMPOSSIBLE, and the algorithm returns `""`. By using a **Max-Heap PriorityQueue** ordered by character frequency or a **Linear Even/Odd Index Placement Algorithm**, Reorganize String executes in **$O(N)$ Linear Time and $O(1)$ Auxiliary Space** (for fixed 26-character alphabets).

> **Important:** The Two Solution Strategies for Reorganize String (LeetCode 767):
> 1. **Max-Heap Interleaving Strategy ($O(N \log 26) = O(N)$ Time)**:
>    - Poll top 2 most frequent characters `(first, second)` from Max-Heap.
>    - Append both to `StringBuilder`!
>    - Decrement frequencies and re-offer to Max-Heap if frequency $> 0$.
> 2. **Even/Odd Index Placement Strategy ($O(N)$ Time - Optimal)**:
>    - Place the most frequent character in **EVEN indices (`0, 2, 4, ...`)**.
>    - Fill remaining characters in remaining even indices, then odd indices (`1, 3, 5, ...`). ⚡

```
Reorganize String Even/Odd Placement Topology (Input: "aab"):
Max Freq Char : 'a' (freq 2), String Length N = 3.
Feasibility   : maxFreq (2) <= (3 + 1) / 2 (2) -> VALID!

Even Placement: Result Array: [ 'a',  _ , 'a' ] (Indices 0, 2)
Odd Placement : Result Array: [ 'a', 'b', 'a' ] (Index 1 filled with 'b')
Output = "aba" (No adjacent duplicates!) ⚡
```

---

## 2. Core Concepts & Mathematical Feasibility Check

### 2.1 The Pigeonhole Feasibility Check
Why does $\text{maxFreq} > \lfloor (N + 1) / 2 \rfloor$ prove impossible reorganization?
* **Even Length $N$** (e.g. $N = 4$): Max allowed frequency of any character is $4/2 = 2$. If a char appears 3 times (`"aaab"`), at least two `'a'`s MUST be adjacent!
* **Odd Length $N$** (e.g. $N = 5$): Max allowed frequency is $(5+1)/2 = 3$. If a char appears 4 times (`"aaaab"`), adjacency is unavoidable!

$$\mathbf{\text{If } \text{maxFreq} > \frac{N + 1}{2} \implies \text{Return } ""}$$

```
Reorganize String Strategy Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Strategy Variant      | Time Complexity   | Auxiliary Space   | Key Advantage     |
+-----------------------+-------------------+-------------------+-------------------+
| **Max-Heap Interleave**| **$O(N)$ Linear ⚡**| $O(26)$ Heap Space | Generalizable to $K$-Distance|
| **Even/Odd Placement**| **$O(N)$ Linear ⚡**| **$O(N)$ Array ⚡**| Zero Heap Allocation Overhead|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"If maxFreq > (N + 1) / 2, return empty string! Place most frequent char at EVEN indices 0, 2, 4!"**

---

## 3. Characteristics & Max-Heap Pairwise Interleaving

### 3.1 Pairwise Interleaving Mechanics
Polling 2 items `(first, second)` simultaneously from a Max-Heap guarantees that `first` and `second` are distinct characters!
1. Poll `first = maxHeap.poll()`. Append `first.ch`.
2. Poll `second = maxHeap.poll()`. Append `second.ch`.
3. Decrement `first.freq--` and `second.freq--`.
4. Re-offer both if their remaining frequencies are $> 0$.

---

## 4. Internal Working Mechanics
Tracing Reorganize String (LeetCode 767) on `s = "aab"`:

```
Freq Map: {'a': 2, 'b': 1}. Length N = 3.
Max Freq = 2 <= (3+1)/2 = 2 -> Feasible!

Even/Odd Placement Algorithm:
1. Most Frequent Char: 'a' (freq 2).
   - Place 'a' at idx 0 -> res = ['a', _, _], idx = 2.
   - Place 'a' at idx 2 -> res = ['a', _, 'a'], idx = 4 (>= N -> switch to idx 1!).

2. Next Char: 'b' (freq 1).
   - Place 'b' at idx 1 -> res = ['a', 'b', 'a'].

Final String = "aba"! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Max-Heap Pairwise Interleaving Topography:

```
Heap State: [ ('a', freq 3) | ('b', freq 2) | ('c', freq 1) ]

Step 1: Poll 'a' & 'b' -> SB: "ab" -> Re-offer ('a', 2) & ('b', 1)
Heap State: [ ('a', freq 2) | ('b', freq 1) | ('c', freq 1) ]

Step 2: Poll 'a' & 'b' -> SB: "abab" -> Re-offer ('a', 1)
Heap State: [ ('a', freq 1) | ('c', freq 1) ]

Step 3: Poll 'a' & 'c' -> SB: "abacac" -> Complete! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Reorganize String using Max-Heap Interleaving and Even/Odd Index Placement (LeetCode 767):

```java
import java.util.*;

public class ReorganizeStringMaster {

    // 1. Reorganize String using Even/Odd Index Placement (Optimal O(N) Time, O(N) Space)
    public static String reorganizeStringEvenOdd(String s) {
        if (s == null || s.length() == 0) return "";

        int[] counts = new int[26];
        int maxCount = 0;
        char maxChar = 'a';

        for (char c : s.toCharArray()) {
            counts[c - 'a']++;
            if (counts[c - 'a'] > maxCount) {
                maxCount = counts[c - 'a'];
                maxChar = c;
            }
        }

        // Pigeonhole Feasibility Check
        if (maxCount > (s.length() + 1) / 2) {
            return ""; // Impossible to reorganize!
        }

        char[] result = new char[s.length()];
        int idx = 0;

        // Step 1: Fill most frequent character in EVEN indices (0, 2, 4, ...)
        while (counts[maxChar - 'a'] > 0) {
            result[idx] = maxChar;
            idx += 2;
            counts[maxChar - 'a']--;
        }

        // Step 2: Fill remaining characters in remaining even, then odd indices
        for (int i = 0; i < 26; i++) {
            while (counts[i] > 0) {
                if (idx >= s.length()) {
                    idx = 1; // Switch to ODD indices!
                }
                result[idx] = (char) (i + 'a');
                idx += 2;
                counts[i]--;
            }
        }

        return new String(result);
    }

    // 2. Reorganize String using Max-Heap Pair Interleaving O(N log 26) = O(N) Time
    public static String reorganizeStringHeap(String s) {
        if (s == null || s.length() == 0) return "";

        int[] counts = new int[26];
        for (char c : s.toCharArray()) {
            counts[c - 'a']++;
        }

        // Max-Heap ordered by character frequency
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(b[1], a[1])
        );

        for (int i = 0; i < 26; i++) {
            if (counts[i] > 0) {
                if (counts[i] > (s.length() + 1) / 2) return ""; // Feasibility check
                maxHeap.offer(new int[]{i + 'a', counts[i]});
            }
        }

        StringBuilder sb = new StringBuilder();

        // Pairwise polling from Max-Heap
        while (maxHeap.size() >= 2) {
            int[] first = maxHeap.poll();
            int[] second = maxHeap.poll();

            sb.append((char) first[0]);
            sb.append((char) second[0]);

            first[1]--;
            second[1]--;

            if (first[1] > 0) maxHeap.offer(first);
            if (second[1] > 0) maxHeap.offer(second);
        }

        // Process leftover single character
        if (!maxHeap.isEmpty()) {
            int[] last = maxHeap.poll();
            if (last[1] > 1) return ""; // Extra check
            sb.append((char) last[0]);
        }

        return sb.toString();
    }
}
```

> **Quick Syntax:**
```java
// Pigeonhole Feasibility Check Line
if (maxCount > (s.length() + 1) / 2) return "";
```

---

## 7. Concrete Problem Examples
* **LeetCode 767 - Reorganize String**: Adjacent character separation.
* **LeetCode 1054 - Distant Barcodes**: Array barcode reorganization.
* **LeetCode 358 - Rearrange String k Distance Apart**: $K$-distance separation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `reorganizeStringEvenOdd` and `reorganizeStringHeap`:

```java
public class ReorganizeStringDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Valid Input Test (\"aab\") ===");
        String s1 = "aab";
        System.out.println("Even/Odd Result: \"" + ReorganizeStringMaster.reorganizeStringEvenOdd(s1) + "\""); // "aba"
        System.out.println("Heap Result:     \"" + ReorganizeStringMaster.reorganizeStringHeap(s1) + "\"");    // "aba" ✅

        System.out.println("\n=== 2. Impossible Input Test (\"aaab\") ===");
        String s2 = "aaab";
        System.out.println("Result: \"" + ReorganizeStringMaster.reorganizeStringEvenOdd(s2) + "\""); // "" (Impossible!) ✅
    }
}
```

---

## 9. Complexity Analysis

| Implementation Strategy | Time Complexity | Auxiliary Space | Key Optimization |
| :--- | :--- | :--- | :--- |
| **Even/Odd Placement** | **$O(N)$ Linear ⚡** | **$O(N)$ Array ⚡** | Direct array stride `idx += 2` |
| **Max-Heap Interleaving**| **$O(N \log 26) = O(N)$ ⚡**| $O(26) = O(1)$ Heap Space| Pairwise heap polling |

---

## 10. Edge Cases & Boundary Handling
* **Single Character String (`"a"`)**: Returns `"a"` immediately.
* **All Identical Characters (`"aaaa"`)**: Fails feasibility check and returns `""`.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting the Pigeonhole Feasibility Check**:
  - Attempting to reorganize an impossible string (`"aaab"`) without checking `maxCount > (N + 1) / 2` leads to infinite loops or incorrect adjacencies.
  - **ALWAYS perform `if (maxCount > (N + 1) / 2) return ""` FIRST**.
* **Interleaving Only 1 Character at a Time in Heap**:
  - Polling only 1 item from the heap requires storing a `prev` reference to avoid re-inserting it immediately.
  - **Poll 2 items `(first, second)` simultaneously for clean, bug-free code**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Even/Odd Placement Guarantees Non-Adjacency:
> Because the most frequent character `maxChar` has frequency $\le \lceil N / 2 \rceil$, placing `maxChar` at even indices `0, 2, 4, ...` separates every instance by at least 1 slot!
> Filling remaining characters in remaining even indices and then odd indices guarantees no identical characters touch!

> **Memory Trick:** **"Place most frequent char at even indices 0, 2, 4; then fill remaining slots!"**

---

## 13. System & Implementation Comparisons

| Feature | Even/Odd Array Placement | Max-Heap Pair Interleaving |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Code Size** | **Compact (1 Pass) ⚡** | Moderate (Heap structures) |
| **Flexibility** | Tailored for Adjacent ($K=2$) | Easily generalizes to any distance $K$ |

---

## 14. How to Recognize This in Questions
* **"Rearrange string so no two adjacent characters are identical"** $\rightarrow$ Reorganize String (LeetCode 767).
* **"Rearrange barcodes so no two adjacent codes are equal"** $\rightarrow$ Distant Barcodes (LeetCode 1054).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `maxCount > (N + 1) / 2` prove impossible reorganization?**  
  *A:* By the Pigeonhole Principle, placing a character $M$ times into an array of size $N$ leaves $N - M$ non-matching slots. To prevent adjacency, we require $N - M \ge M - 1 \implies M \le (N + 1) / 2$.
* **Q: How can this algorithm be extended to distance $K > 2$?**  
  *A:* Use a Max-Heap combined with a Cooldown Queue of size $K$ (LeetCode 358).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: REORGANIZE STRING & CHARACTER FREQUENCY               |
+-----------------------------------------------------------------------+
| • Feasibility Check: If maxCount > (N + 1) / 2 -> Return ""           |
| • Optimal Strategy : Fill maxChar at EVEN indices 0, 2, 4, ...        |
| • Remaining Filling: Fill remaining chars at remaining even/odd slots |
| • Heap Strategy    : Poll 2 items (first, second) from Max-Heap       |
| • Complexity       : O(N) Linear Time | O(N) Auxiliary Space ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Reorganize String (LeetCode 767) using Even/Odd placement.
- [ ] I can write Reorganize String using Max-Heap pair interleaving.
- [ ] I know why `maxCount > (N + 1) / 2` proves reorganization impossible.
- [ ] I know how to fill even indices first to prevent adjacent duplicates.
- [ ] I can extend this pattern to Distant Barcodes (LeetCode 1054).
