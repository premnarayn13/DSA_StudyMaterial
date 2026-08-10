# 04. Rabin-Karp Algorithm: Rolling Hash, Modular Arithmetic & Multi-Pattern Search

## 1. Introduction
The **Rabin-Karp Algorithm** is a probabilistic string-searching algorithm created by Michael O. Rabin and Richard M. Karp in 1987. Unlike Naive or KMP algorithms that compare characters directly, Rabin-Karp maps substrings to integer values using a **Polynomial Rolling Hash Function** over a large prime modulus $Q$. By sliding a fixed-length window of size $M$ over text $T$ of size $N$, Rabin-Karp updates the rolling hash in **$O(1)$ Constant Time** per shift. When text hash equals pattern hash, Rabin-Karp performs a character-by-character verification to handle **Spurious Hits (Hash Collisions)**. Rabin-Karp achieves **$O(N + M)$ Average Time Complexity** and excels at **Multi-Pattern Searching**.

> **Important:** Core Invariants of the Rabin-Karp Algorithm:
> 1. **Polynomial Hash Formula**:
>    $$H(S) = \left( \sum_{i=0}^{M-1} S[i] \cdot B^{M-1-i} \right) \pmod Q$$
>    where $B$ is the radix base (e.g. $B = 256$) and $Q$ is a large prime (e.g. $Q = 10^9 + 7$ or $101$).
> 2. **$O(1)$ Rolling Hash Update Equation**:
>    $$H_{i+1} = \left( B \cdot (H_i - T[i] \cdot h) + T[i + M] \right) \pmod Q$$
>    where $h = B^{M-1} \pmod Q$. Computes the next window hash in 1 step!
> 3. **Spurious Hit Verification Invariant**:
>    - If $H(T[i \dots i+M-1]) \neq H(P) \implies$ Guaranteed NOT a match!
>    - If $H(T[i \dots i+M-1]) == H(P) \implies$ Candidate match! Must verify characters to rule out hash collisions.
> 4. **Multi-Pattern Advantage**: Can search $K$ patterns of length $M$ simultaneously by storing pattern hashes in a Hash Set, matching any of $K$ patterns in **$O(N + K \cdot M)$ Time**! ⚡

```
Rabin-Karp Rolling Hash Window Topology (Base B=256, Prime Q=101):
Pattern P: "CDE" -> Hash H(P) = 54

Text Window 0: "ABC" -> Hash H("ABC") = 32 != 54 -> No Match!
Roll Hash to Window 1: Subtract 'A', Shift B, Add 'D' -> Hash H("BCD") = 41 != 54 -> No Match!
Roll Hash to Window 2: Subtract 'B', Shift B, Add 'E' -> Hash H("CDE") = 54 == H(P)!
  - Hash Equal -> Verify "CDE" == "CDE" -> MATCH FOUND AT INDEX 2! ⚡
```

---

## 2. Core Concepts & Rabin-Karp Strategy Matrix

### 2.1 Rabin-Karp Strategy Matrix
```
Rabin-Karp Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Hashing Method    | Average Time      | Worst Case Time   |
+-----------------------+-------------------+-------------------+-------------------+
| **Single Pattern**    | Rolling Hash (B,Q)| **$O(N + M)$ ⚡** | $O(N \cdot M)$ (Collisions) |
| **Multi-Pattern (K)** | Set Hash Lookup   | **$O(N + K \cdot M)$⚡**| $O(N \cdot K \cdot M)$|
| **2D Matrix Matching**| 2D Rolling Hash   | **$O(N^2)$ ⚡**   | $O(N^2 \cdot M^2)$ |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Rabin-Karp: Roll window hash in O(1) time! If hashes match, verify characters to rule out spurious hits!"**

---

## 3. Characteristics & $O(1)$ Rolling Hash Math Proof

### 3.1 Mathematical Proof of $O(1)$ Rolling Hash Window Shift
* Let window $i$ cover characters $T[i \dots i+M-1]$ with hash:
  $$H_i = \left( T[i] \cdot B^{M-1} + T[i+1] \cdot B^{M-2} + \dots + T[i+M-1] \cdot B^0 \right) \pmod Q$$
* To transition to window $i+1$ covering $T[i+1 \dots i+M]$:
  1. Remove leading char $T[i]$: $H_i - T[i] \cdot B^{M-1}$
  2. Multiply remainder by base $B$: $\left( H_i - T[i] \cdot B^{M-1} \right) \cdot B$
  3. Add trailing char $T[i+M]$: $\left( H_i - T[i] \cdot B^{M-1} \right) \cdot B + T[i+M]$
* Applying modular arithmetic to prevent overflow:
  $$H_{i+1} = \left( B \cdot (H_i - T[i] \cdot h) + T[i + M] \right) \pmod Q$$
* Since $h = B^{M-1} \pmod Q$ is precomputed in $O(M)$ time, updating $H_{i+1}$ takes **$O(1)$ Constant Operations**! ⚡

---

## 4. Internal Working Mechanics: Modular Negative Remainder Handling

In Java, the modulo operator `%` can return negative results when subtracting $T[i] \cdot h$. Handling negative modular remainders properly is essential to prevent hash mismatches:

```
Handling Negative Modulo Remainder in Java:

// BAD: (H - T[i] * h) can be negative -> (negative % Q) returns negative integer!
int newHash = (base * (currHash - text.charAt(i) * h) + text.charAt(i + m)) % Q;

// GOOD: Add Q before modulo to ensure non-negative result! ⚡
int newHash = (base * (currHash - text.charAt(i) * h) + text.charAt(i + m)) % Q;
if (newHash < 0) {
    newHash = (newHash + Q) % Q; // Wrap around to valid range [0 ... Q-1]!
}
```

---

## 5. Visual Diagram: Rolling Hash Window Mechanics

```
Text:     [ T[i] | T[i+1] | T[i+2] | ... | T[i+M-1] ] | T[i+M]
           └───── Subtract T[i] * B^(M-1) ──────────┘
                  └───────── Multiply by Base B ────┘
                         └────────────── Add T[i+M] ──┘

Result: Compute H(i+1) in 1 Step without re-hashing full window! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Rabin-Karp Single Pattern Search, Multi-Pattern Searching via Hash Sets, and Modular Arithmetic Guards.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Rabin-Karp Algorithm,
 * Rolling Hash Updates, Spurious Hit Verification, and Multi-Pattern Searching.
 */
public class RabinKarpMaster {

    private static final int BASE = 256;               // Radix Base B (Extended ASCII)
    private static final int PRIME = 1_000_000_007;   // Prime Modulus Q (Prevents Overflows)

    // =========================================================================
    // 1. RABIN-KARP SINGLE PATTERN SEARCH (O(N + M) Average Time, O(1) Space)
    // =========================================================================
    /**
     * Searches all 0-based occurrences of pattern P in text T using Rabin-Karp.
     *
     * @param text input text string T
     * @param pattern search pattern P
     * @return list of starting match indices
     */
    public List<Integer> search(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();

        if (m == 0 || m > n) return matches;

        // Step 1: Precompute h = B^(M-1) % Q
        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * BASE) % PRIME;
        }

        long patternHash = 0;
        long textHash = 0;

        // Step 2: Compute initial hash for pattern and first window of text
        for (int i = 0; i < m; i++) {
            patternHash = (BASE * patternHash + pattern.charAt(i)) % PRIME;
            textHash = (BASE * textHash + text.charAt(i)) % PRIME;
        }

        // Step 3: Slide rolling hash window over text
        for (int i = 0; i <= n - m; i++) {
            // Check if hash matches
            if (patternHash == textHash) {
                // Candidate match! Perform character-by-character verification to rule out spurious hits
                if (checkCharacters(text, pattern, i)) {
                    matches.add(i); // True Match Found! ⚡
                }
            }

            // Calculate rolling hash for next window (if not at end of text)
            if (i < n - m) {
                textHash = (BASE * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;

                // Handle negative modulo remainders
                if (textHash < 0) {
                    textHash = (textHash + PRIME) % PRIME;
                }
            }
        }

        return matches;
    }

    private boolean checkCharacters(String text, String pattern, int startIdx) {
        for (int j = 0; j < pattern.length(); j++) {
            if (text.charAt(startIdx + j) != pattern.charAt(j)) {
                return false; // Spurious hit detected! Hash collision occurred.
            }
        }
        return true;
    }

    // =========================================================================
    // 2. RABIN-KARP MULTI-PATTERN SEARCH ENGINE (O(N + K * M) Time)
    // =========================================================================
    /**
     * Searches multiple patterns of equal length M in text T simultaneously.
     */
    public Map<String, List<Integer>> searchMultiplePatterns(String text, List<String> patterns) {
        Map<String, List<Integer>> resultMap = new HashMap<>();
        if (text == null || patterns == null || patterns.isEmpty()) return resultMap;

        int m = patterns.get(0).length();
        int n = text.length();

        if (m > n) return resultMap;

        // Store pattern hashes in a map for O(1) lookup
        Map<Long, List<String>> hashToPatterns = new HashMap<>();

        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * BASE) % PRIME;
        }

        for (String p : patterns) {
            resultMap.put(p, new ArrayList<>());
            long pHash = 0;
            for (int i = 0; i < m; i++) {
                pHash = (BASE * pHash + p.charAt(i)) % PRIME;
            }
            hashToPatterns.computeIfAbsent(pHash, k -> new ArrayList<>()).add(p);
        }

        long textHash = 0;
        for (int i = 0; i < m; i++) {
            textHash = (BASE * textHash + text.charAt(i)) % PRIME;
        }

        for (int i = 0; i <= n - m; i++) {
            if (hashToPatterns.containsKey(textHash)) {
                for (String p : hashToPatterns.get(textHash)) {
                    if (checkCharacters(text, p, i)) {
                        resultMap.get(p).add(i);
                    }
                }
            }

            if (i < n - m) {
                textHash = (BASE * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
                if (textHash < 0) textHash = (textHash + PRIME) % PRIME;
            }
        }

        return resultMap;
    }
}
```

> **Quick Syntax:**
```java
// Rolling Hash Update Line
textHash = (BASE * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
if (textHash < 0) textHash += PRIME;
```

---

## 7. Concrete Problem Examples & Applications

1. **Plagiarism Detection Engines**:
   - Rabin-Karp searches thousands of document sentences (multi-patterns) against a master corpus in linear time.

2. **LeetCode 1044 - Longest Duplicate Substring**:
   - Uses Binary Search on Substring Length + Rabin-Karp Rolling Hash to find longest duplicate substring in $O(N \log N)$ time.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;
import java.util.Map;

public class RabinKarpDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   RABIN-KARP ROLLING HASH MATCHING DEMO         ");
        System.out.println("=================================================\n");

        RabinKarpMaster master = new RabinKarpMaster();

        // 1. Single Pattern Search Test
        String text = "GEEKS FOR GEEKS";
        String pattern = "GEEK";
        List<Integer> matches = master.search(text, pattern);
        System.out.println("1. Text   : \"" + text + "\"");
        System.out.println("   Pattern: \"" + pattern + "\"");
        System.out.println("   Rabin-Karp Matches Found at Indices: " + matches);
        System.out.println("-------------------------------------------------");

        // 2. Multi-Pattern Search Test
        List<String> patterns = List.of("GEEK", "FOR ");
        Map<String, List<Integer>> multiMatches = master.searchMultiplePatterns(text, patterns);
        System.out.println("2. Multi-Pattern Search Results: " + multiMatches);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Rabin-Karp Mode | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Single Pattern** | $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(N + M)}$ ⚡| $O(N \cdot M)$ (Collisions) | $\mathbf{O(1)}$ Space ⚡| Rolling Hash $O(1)$ |
| **Multi-Pattern (K)**| $\mathbf{O(N + K \cdot M)}$⚡| $\mathbf{O(N + K \cdot M)}$⚡| $O(N \cdot K \cdot M)$ | $O(K)$ Hash Map | Hash Set Lookup |

---

## 10. Edge Cases & Boundary Handling

1. **Hash Collisions (Spurious Hits)**:
   - Handled cleanly by character-by-character verification when hashes match.

2. **Negative Modulo Remainder**:
   - Corrected using `if (textHash < 0) textHash += PRIME`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Omitting Character Verification on Hash Match**:
  - Assuming equal hashes implies equal strings causes false positive matches due to hash collisions. ALWAYS verify characters when hashes match!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Rabin-Karp Outperforms KMP for Multi-Pattern Search:
> KMP requires running separate search passes per pattern ($K \times O(N)$).
> Rabin-Karp computes pattern hashes upfront and checks text window hashes against a **Hash Set** in $O(1)$ time, searching $K$ patterns in a **Single Forward Pass**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Rabin-Karp Algorithm | KMP Algorithm | Naive Search |
| :--- | :--- | :--- | :--- |
| **Multi-Pattern Support**| **Extremely High (Single Pass)⚡**| Low (Requires Aho-Corasick)| Low |
| **Average Time** | **$O(N + M)$ Linear ⚡** | **$O(N + M)$ Linear ⚡** | $O(N)$ Average |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| $O(M)$ LPS Table | $O(1)$ Constant Space |

---

## 14. How to Recognize This in Questions

* **"Search multiple patterns of same length in text simultaneously"** $\rightarrow$ Rabin-Karp Multi-Pattern Search.
* **"Find duplicate substrings of fixed length L using rolling hash"** $\rightarrow$ Rabin-Karp Rolling Hash.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Rabin-Karp achieve $O(1)$ hash rolling updates?**  
  *A:* By subtracting the high-order term $T[i] \cdot B^{M-1}$, multiplying the remaining value by base $B$, and adding the new low-order character $T[i+M]$ modulo prime $Q$.

* **Q: What is a Spurious Hit in Rabin-Karp?**  
  *A:* A situation where two different substrings produce identical hash values due to modular arithmetic hash collision.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RABIN-KARP ALGORITHM                                  |
+-----------------------------------------------------------------------+
| • Rolling Hash  : H(i+1) = (B * (H(i) - T[i]*h) + T[i+m]) % PRIME     |
| • Modulo Guard  : If textHash < 0 -> textHash += PRIME                |
| • Spurious Hit  : Verify characters when textHash == patternHash      |
| • Multi-Pattern : Search K patterns in single pass using Hash Set     |
| • Performance   : O(N + M) Average Time | O(1) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the Rabin-Karp rolling hash update equation in Java.
- [ ] I can handle negative modulo remainders cleanly.
- [ ] I can write character-by-character verification for spurious hits.
- [ ] I can write Rabin-Karp Multi-Pattern search using a Hash Set.
- [ ] I can state why Rabin-Karp excels at multi-pattern searching.
