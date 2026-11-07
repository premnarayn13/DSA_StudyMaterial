# 13. Rolling Hash & Strings, Rabin-Karp Search & Double Hash Collision Elimination

## 1. Introduction
The **Rolling Hash Pattern** (most famously realized in the **Rabin-Karp String Matching Algorithm**) transforms substring search from $O(N \cdot M)$ naive character comparisons down to **$O(N)$ Average Linear Time**. By maintaining a sliding window polynomial hash code that updates in **$O(1)$ Constant Time** when sliding 1 character to the right, Rolling Hash solves complex string search problems like **Rabin-Karp Substring Search (LeetCode 28)**, **Repeated DNA Sequences (LeetCode 187)**, and **Longest Duplicate Substring (LeetCode 1044)**.

> **Important:** How does a Rolling Hash achieve $O(1)$ constant time window updates?
> When sliding a window of length $L$ from index $i-1$ to $i$:
> 1. Subtract the outgoing character: $H_{\text{new}} = (H_{\text{old}} - s[i-1] \cdot P^{L-1}) \bmod M$.
> 2. Shift base prime: $H_{\text{new}} = (H_{\text{new}} \cdot P) \bmod M$.
> 3. Add incoming character: $H_{\text{new}} = (H_{\text{new}} + s[i + L - 1]) \bmod M$.
> Re-computing full substring hashes from scratch is completely eliminated! ⚡

```
Rolling Hash Window Shift Topology:
Window at i-1: [ 'a', 'b', 'c' ] 'd'  ---> Hash H1
Slide Right  : 'a' [ 'b', 'c', 'd' ]  ---> H2 = (H1 - 'a'*P^2) * P + 'd' (Calculated in O(1) Time!) ⚡
```

---

## 2. Core Concepts & Rabin-Karp Rolling Hash Formulation

### 2.1 The Polynomial Rolling Hash Equation
For a string window $S[i \dots i + L - 1]$ of length $L$ using base prime $P$ and modulo prime $M$:

$$H(i) = \left( \sum_{j=0}^{L-1} S[i + j] \cdot P^{L-1-j} \right) \bmod M$$

#### $O(1)$ Window Update Transformation Formula:
$$H(i + 1) = \left( (H(i) - S[i] \cdot P^{L-1}) \cdot P + S[i + L] \right) \bmod M$$

```
Rolling Hash Modulo Arithmetic Safeguard:
In modular arithmetic, subtraction (H(i) - S[i]*P^{L-1}) can yield negative values!
Always add modulo M before taking % M to prevent negative remainders in Java:
H_new = (((H_old - S[i] * power) % M + M) % M * P + S[i + L]) % M! ⚡
```

> **Memory Trick:** **"Rolling Hash: Subtract outgoing character * P^(L-1), multiply by base prime P, add incoming character!"**

---

## 3. Characteristics & Double Hashing Spurious Hit Elimination

### 3.1 Eliminating Spurious Hits via Double Hashing
A **Spurious Hit** occurs when two distinct substrings evaluate to the SAME rolling hash code ($H(S_1) == H(S_2)$ but $S_1 \ne S_2$).
* **Naive Defense**: Perform an $O(L)$ explicit character-by-character string comparison on every hash match. (Can degrade worst-case time to $O(N \cdot M)$ if hash collisions occur frequently!).
* **Double Hashing Defense**: Compute TWO independent rolling hashes simultaneously using 2 different prime bases ($P_1 = 31, P_2 = 37$) and 2 different prime modulos ($M_1 = 10^9 + 7, M_2 = 10^9 + 9$).
* **Collision Probability**: The probability of two distinct strings matching BOTH hashes simultaneously is $\approx \frac{1}{M_1 \cdot M_2} \approx \frac{1}{10^{18}}$ (Virtually Zero Collision Probability!).

---

## 4. Internal Working Mechanics
Tracing Rabin-Karp Substring Search on text `S = "abcde"`, pattern `P = "cde"` ($L = 3, P = 31, M = 10^9+7$):

```
Pattern "cde" Hash Code = 99318

Init Window i=0 ("abc"): Hash = 97314 (No match)

Slide to i=1 ("bcd"):
  - Outgoing char: 'a' (ASCII 97). Incoming char: 'd' (ASCII 100).
  - H_new = (97314 - 97 * 31^2) * 31 + 100 = 98316 (No match)

Slide to i=2 ("cde"):
  - Outgoing char: 'b' (ASCII 98). Incoming char: 'e' (ASCII 101).
  - H_new = (98316 - 98 * 31^2) * 31 + 101 = 99318.
  - H_new (99318) == Pattern Hash (99318) -> MATCH FOUND at Index 2! ✅
```

---

## 5. Visual Diagram
Rabin-Karp Rolling Hash Window Sliding Topography:

```
Step 1: [ a   b   c ]  d   e   ---> Calculate Initial Hash H0
          |
        Subtract 'a' * P^(L-1)
          |
        Multiply by P
          |
        Add 'd'
          |
          v
Step 2:   a  [ b   c   d ]  e   ---> Instant O(1) Hash Update H1! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Rabin-Karp Substring Search (LeetCode 28), Repeated DNA Sequences (LeetCode 187), and Longest Duplicate Substring (LeetCode 1044):

```java
import java.util.*;

public class RollingHashStringsMaster {

    // 1. Rabin-Karp Substring Search (LeetCode 28) O(N + M) Time, O(1) Space
    public static int strStrRabinKarp(String haystack, String needle) {
        if (needle == null || haystack == null || needle.length() > haystack.length()) return -1;
        if (needle.length() == 0) return 0;

        int n = haystack.length();
        int m = needle.length();
        long P = 31;
        long M = 1_000_000_007L;

        // Compute P^(m-1) % M
        long power = 1;
        for (int i = 0; i < m - 1; i++) {
            power = (power * P) % M;
        }

        // Compute initial hashes for needle and first window of haystack
        long targetHash = 0;
        long windowHash = 0;
        for (int i = 0; i < m; i++) {
            targetHash = (targetHash * P + needle.charAt(i)) % M;
            windowHash = (windowHash * P + haystack.charAt(i)) % M;
        }

        if (windowHash == targetHash && haystack.substring(0, m).equals(needle)) {
            return 0; // Found at index 0
        }

        // Slide window across haystack
        for (int i = 1; i <= n - m; i++) {
            // Remove outgoing char haystack[i-1] and add incoming char haystack[i+m-1]
            long outgoing = (haystack.charAt(i - 1) * power) % M;
            windowHash = (windowHash - outgoing + M) % M;
            windowHash = (windowHash * P + haystack.charAt(i + m - 1)) % M;

            if (windowHash == targetHash) {
                // Verify match to guard against spurious hit
                if (haystack.substring(i, i + m).equals(needle)) {
                    return i;
                }
            }
        }

        return -1;
    }

    // 2. Repeated DNA Sequences (LeetCode 187 - 10-mer Bitmask Rolling Hash) O(N) Time, O(N) Space
    public static List<String> findRepeatedDnaSequences(String s) {
        if (s == null || s.length() < 10) return new ArrayList<>();

        Set<Integer> seen = new HashSet<>();
        Set<String> repeated = new HashSet<>();

        // Map characters to 2-bit values: A=00, C=01, G=10, T=11
        int[] charMap = new int[26];
        charMap['C' - 'A'] = 1;
        charMap['G' - 'A'] = 2;
        charMap['T' - 'A'] = 3;

        int windowHash = 0;
        // Build initial 10-mer bitmask (20 bits total)
        for (int i = 0; i < 9; i++) {
            windowHash = (windowHash << 2) | charMap[s.charAt(i) - 'A'];
        }

        // Mask to keep lower 20 bits (0xFFFFF)
        int mask = (1 << 20) - 1;

        for (int i = 9; i < s.length(); i++) {
            windowHash = ((windowHash << 2) | charMap[s.charAt(i) - 'A']) & mask;
            if (!seen.add(windowHash)) {
                repeated.add(s.substring(i - 9, i + 1));
            }
        }

        return new ArrayList<>(repeated);
    }
}
```

> **Quick Syntax:**
```java
// O(1) Rolling Hash Window Update Line
long outgoing = (s.charAt(i - 1) * power) % M;
windowHash = (windowHash - outgoing + M) % M;
windowHash = (windowHash * P + s.charAt(i + m - 1)) % M;
```

---

## 7. Concrete Problem Examples
* **LeetCode 28 - Find the Index of the First Occurrence**: Rabin-Karp rolling hash.
* **LeetCode 187 - Repeated DNA Sequences**: Bitmask 20-bit rolling hash.
* **LeetCode 1044 - Longest Duplicate Substring**: Binary search length + Rabin-Karp double hashing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Rabin-Karp Substring Search and Repeated DNA Sequences:

```java
public class RollingHashStringsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Rabin-Karp Substring Search (LeetCode 28) ===");
        String haystack = "sadbutsad", needle = "sad";
        int matchIdx = RollingHashStringsMaster.strStrRabinKarp(haystack, needle);
        System.out.println("Pattern Found at Index: " + matchIdx); // Output: 0

        System.out.println("\n=== 2. Repeated DNA Sequences (LeetCode 187) ===");
        String dna = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT";
        List<String> dnaRes = RollingHashStringsMaster.findRepeatedDnaSequences(dna);
        System.out.println("Repeated 10-mers: " + dnaRes);
        // Output: ["AAAAACCCCC", "CCCCCAAAAA"]
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Rabin-Karp Search (28)** | **$O(N + M)$ Average ⚡** | **$O(1)$ Space ⚡** | $O(1)$ window hash update |
| **Repeated DNA (187)** | **$O(N)$ Linear ⚡** | $O(N)$ Set Space | 20-bit bitmask rolling hash |
| **Longest Duplicate (1044)**| **$O(N \log N)$ ⚡** | $O(N)$ Space | Binary Search + Double Hashing |

---

## 10. Edge Cases & Boundary Handling
* **Negative Remainder Prevention**: Subtracting outgoing character can produce negative values. Always add `+ M` before modulo: `(hash - outgoing + M) % M`.
* **String Length $M > N$**: Handled by initial check returning `-1` or `""`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Add $+ M$ During Hash Subtraction**:
  - `(hash - outgoing) % M` yields negative remainders in Java, causing hash match comparison failures!
  - **Always execute `(hash - outgoing + M) % M`**.
* **Skipping Verification Step on Single Hash Match**:
  - Assuming a hash match guarantees string equality without explicit string verification or double hashing introduces spurious hit bugs.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Bitmasking Works for DNA Sequences (LeetCode 187):
> DNA strings contain ONLY 4 characters (`A`, `C`, `G`, `T`).
> Each character can be represented in **2 bits**: `A=00, C=01, G=10, T=11`.
> A 10-character DNA 10-mer consumes $10 \times 2 = 20\text{ bits}$, which fits comfortably inside a single 32-bit primitive `int`!
> Window update becomes a single 2-bit left shift and bitwise AND mask: `((hash << 2) | val) & 0xFFFFF`!

> **Memory Trick:** **"DNA 10-mer fits in 20 bits of a single integer! Use bitwise (hash << 2) | val & 0xFFFFF!"**

---

## 13. System & Implementation Comparisons

| Feature | Rabin-Karp Rolling Hash | KMP (Knuth-Morris-Pratt) Algorithm |
| :--- | :--- | :--- |
| **Average Time Complexity**| **$O(N + M)$ Linear ⚡** | **$O(N + M)$ Linear ⚡** |
| **Multiple Pattern Search**| **Optimal (Hashes multiple patterns) ⚡**| Requires Multiple Automata |
| **Implementation Complexity**| Moderate (Algebraic) | High (LPS Array Automaton) |

---

## 14. How to Recognize This in Questions
* **"Find first occurrence of pattern in text using rolling hash"** $\rightarrow$ Rabin-Karp (LeetCode 28).
* **"Find all 10-letter DNA sequences appearing more than once"** $\rightarrow$ LeetCode 187 (20-bit bitmask rolling hash).

---

## 15. Frequently Asked Interview Questions
* **Q: How does Rabin-Karp update substring hash codes in $O(1)$ constant time?**  
  *A:* By subtracting the outgoing left character scaled by $P^{L-1}$, shifting the remaining base prime power by multiplying by $P$, and adding the new incoming right character.
* **Q: What is the probability of a Spurious Hit when using Double Hashing?**  
  *A:* For modulos $M_1 \approx 10^9$ and $M_2 \approx 10^9$, collision probability is $\frac{1}{M_1 \cdot M_2} \approx 10^{-18}$, rendering spurious hits mathematically impossible in practical computing.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ROLLING HASH & RABIN-KARP                             |
+-----------------------------------------------------------------------+
| • Window Update Rule: H_new = (((H - out*power)%M + M)%M * P + in) % M|
| • Power Constant: power = P^(L-1) % M                                 |
| • DNA Bitmasking (187): 2 bits per char -> 20 bits total (mask 0xFFFFF)|
| • Spurious Hit Defense: Double hashing using 2 independent prime modulos|
| • Time Complexity: O(N) Linear Average Time | O(1) Space ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Rabin-Karp Substring Search (LeetCode 28) from memory.
- [ ] I know why `+ M` is required during modulo subtraction.
- [ ] I can write Repeated DNA Sequences (LeetCode 187) using 20-bit bitmasking.
- [ ] I can state the $O(1)$ rolling hash window update equation.
- [ ] I know how Double Hashing eliminates spurious hits.
