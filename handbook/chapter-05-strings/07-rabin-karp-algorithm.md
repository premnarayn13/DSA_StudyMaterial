# 07. Rabin-Karp Algorithm & Rolling Hash

## 1. Introduction
The **Rabin-Karp Algorithm** is a string-matching algorithm that uses **Rolling Hash** functions to achieve average-case **$O(N + M)$ time complexity and $O(1)$ auxiliary space**. Instead of comparing characters one by one at every text alignment, Rabin-Karp computes a numerical hash of pattern $P$ and compares it against the rolling hash of text windows in $O(1)$ time per shift. Rabin-Karp is especially powerful for **Multi-Pattern Searching** and detecting duplicate substrings.

> **Important:** When window hash equals pattern hash, Rabin-Karp MUST perform an explicit character-by-character verification pass to rule out **Hash Collisions**!

## 2. Core Concepts
* **Polynomial Rolling Hash**: Representing a string as an integer polynomial using base $B$ (e.g., $B = 31$ or $256$) modulo a large prime $MOD$ (e.g., $10^9 + 7$):
  $$\text{Hash}(S) = (S[0] \cdot B^{M-1} + S[1] \cdot B^{M-2} + \dots + S[M-1] \cdot B^0) \pmod{MOD}$$
* **$O(1)$ Rolling Hash Update Rule**: Shifting window from index $i$ to $i+1$ (removing old char $T[i]$ and adding new char $T[i+M]$):
  $$\text{newHash} = ((\text{oldHash} - T[i] \cdot B^{M-1}) \cdot B + T[i+M]) \pmod{MOD}$$
* **Spurious Hit / Hash Collision**: Occurs when two distinct string windows produce identical numerical hash values. Handled via explicit character checks.
* **Double Hashing**: Using two independent prime moduli ($MOD_1$ and $MOD_2$) simultaneously to make hash collisions practically impossible ($1 / 10^{18}$).

> **Memory Trick:** **"Subtract Old High-Order Term -> Multiply by Base -> Add New Low-Order Term -> Modulo!"**

## 3. Characteristics / Properties
* **Multi-Pattern Searching Advantage**: Can search for $K$ different patterns of length $M$ simultaneously by storing pattern hashes in a `HashSet` ($O(N + K \cdot M)$ time).
* **Modular Arithmetic Safety**: Intermediate hash multiplications must prevent 64-bit integer overflow using `long` types and adding $MOD$ before taking `% MOD` when subtracting terms.

```
Rabin-Karp Performance Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric                | Best / Avg Case   | Worst Case        | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| Single Pattern Search | O(N + M)          | O(N * M) (Collisions)| O(1) Constant    |
| Multi-Pattern Search  | O(N + K * M)      | O(N * K * M)      | O(K) Hash Set     |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing $O(1)$ Rolling Hash Window Shift:

```
Text T = "code", Base B = 10, MOD = 101, Pattern Length M = 3
Window 0: "cod" (values 3, 14, 3) -> Hash = (3*10² + 14*10¹ + 3*10⁰) % 101 = 443 % 101 = 39

Shift Window to "ode" (Remove 'c'=3, Add 'e'=4):
Step 1: Subtract old high-order term (3 * 10² = 300): 39 - 300 = -261
Step 2: Multiply by Base 10: -261 * 10 = -2610
Step 3: Add new char ('e'=4): -2610 + 4 = -2606
Step 4: Take Modulo 101 (handling negatives): (-2606 % 101 + 101) % 101 = 20 ✅ (O(1) time!)
```

## 5. Visual Diagram
Rolling Hash Window Slide Mechanics:

```
Text Window:  [ c ][ o ][ d ] e
               |-----------|   (Old Hash: 39)
               
Subtract 'c'  --------------> Remove 3 * 10²
Shift Left    --------------> Multiply by Base 10
Add 'e'       --------------> Add 4

New Window:     c [ o ][ d ][ e ]
                  |-----------| (New Hash: 20 in O(1) time!)
```

## 6. Operations / Algorithms
Rabin-Karp Master Implementation:

```java
public class RabinKarp {
    private static final int BASE = 256;
    private static final long MOD = 1_000_000_007L;

    public int search(String text, String pattern) {
        int N = text.length(), M = pattern.length();
        if (M > N) return -1;

        long patternHash = 0, textHash = 0, power = 1;

        // Precompute BASE^(M-1) % MOD
        for (int i = 0; i < M - 1; i++) {
            power = (power * BASE) % MOD;
        }

        // Compute initial hash for pattern and first window of text
        for (int i = 0; i < M; i++) {
            patternHash = (patternHash * BASE + pattern.charAt(i)) % MOD;
            textHash = (textHash * BASE + text.charAt(i)) % MOD;
        }

        // Slide window over text
        for (int i = 0; i <= N - M; i++) {
            if (patternHash == textHash) {
                // Character verification pass to eliminate spurious hits
                if (text.substring(i, i + M).equals(pattern)) {
                    return i; // Match found at index i
                }
            }

            // Rolling hash update for next window
            if (i < N - M) {
                textHash = (textHash - (text.charAt(i) * power) % MOD + MOD) % MOD;
                textHash = (textHash * BASE + text.charAt(i + M)) % MOD;
            }
        }
        return -1;
    }
}
```

> **Quick Syntax:**
```java
// Modular Arithmetic Subtraction Guard
long updatedHash = (oldHash - (outgoingChar * power) % MOD + MOD) % MOD;
updatedHash = (updatedHash * BASE + incomingChar) % MOD;
```

## 7. Examples
* **LeetCode 28 - Find the Index of the First Occurrence in a String**: Rabin-Karp $O(N + M)$ search.
* **LeetCode 1044 - Longest Duplicate Substring**: Binary Search on Substring Length + Rabin-Karp Rolling Hash in $O(N \log N)$ time.
* **Repeated DNA Sequences (LeetCode 187)**: Rolling hash on 10-letter DNA sequences.

## 8. Java Code
Complete interview-ready Java suite implementing Rabin-Karp Search, Hash Collision Verification, and Longest Duplicate Substring detection:

```java
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class RabinKarpMaster {

    private static final int BASE = 31;
    private static final long MOD = 1_000_000_007L;

    // 1. Rabin-Karp Substring Search O(N + M) Avg Time, O(1) Space
    public static List<Integer> searchAll(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;
        int N = text.length(), M = pattern.length();

        if (M == 0 || M > N) return matches;

        long patternHash = 0, textHash = 0, power = 1;

        // Precompute BASE^(M-1) % MOD
        for (int i = 0; i < M - 1; i++) {
            power = (power * BASE) % MOD;
        }

        // Initial hash values for pattern and window 0
        for (int i = 0; i < M; i++) {
            patternHash = (patternHash * BASE + text.charAt(i)) % MOD; // Note: pattern hash
        }
        patternHash = 0;
        for (int i = 0; i < M; i++) {
            patternHash = (patternHash * BASE + pattern.charAt(i)) % MOD;
            textHash = (textHash * BASE + text.charAt(i)) % MOD;
        }

        // Slide window across text
        for (int i = 0; i <= N - M; i++) {
            if (patternHash == textHash) {
                // Verification pass to eliminate spurious hits
                if (text.regionMatches(i, pattern, 0, M)) {
                    matches.add(i);
                }
            }

            // Calculate rolling hash for next window
            if (i < N - M) {
                textHash = (textHash - (text.charAt(i) * power) % MOD + MOD) % MOD;
                textHash = (textHash * BASE + text.charAt(i + M)) % MOD;
            }
        }

        return matches;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String text = "AABAACAADAABAABA";
        String pattern = "AABA";

        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);

        List<Integer> matches = searchAll(text, pattern);
        System.out.println("Rabin-Karp Match Indices Found: " + matches); // Output: [0, 9, 12]
    }
}
```

## 9. Complexity Analysis
| Scenario | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Average Case** | **$O(N + M)$** | **$O(1)$** | Rare hash collisions |
| **Worst Case (Poor Modulus)**| $O(N \cdot M)$ | $O(1)$ | Spurious hits on every shift |
| **Multi-Pattern Search ($K$)**| $O(N + K \cdot M)$ | $O(K)$ HashSet | Hash set lookup in $O(1)$ |

## 10. Edge Cases
* **Negative Modular Remainder**: Java `%` operator can return negative values for negative numbers. Always add `+ MOD` before taking `% MOD`: `(hash - val + MOD) % MOD`.
* **Pattern Length $M > N$**: Return empty list immediately.
* **Hash Overflow**: Use `long` variables for all intermediate rolling hash calculations.

## 11. Common Mistakes
* Omitting the character verification pass `text.regionMatches(...)` when `textHash == patternHash` (accepts false positive spurious hits!).
* Forgetting to add `MOD` before taking `% MOD` when subtracting the outgoing character term (causes negative array index / hash bugs).
* Recalculating $B^{M-1} \pmod{MOD}$ inside the sliding window loop instead of precomputing it once upfront.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never forget: **Hash Equality DOES NOT Guarantee String Equality!**
> Always explain to the interviewer: *"When the rolling hash matches, I perform a secondary character verification pass to guard against hash collisions (spurious hits)."*

> **Memory Trick:** **"Rolling Hash Subtraction: Always add + MOD before taking % MOD!"**

## 13. Comparisons
| Feature | Rabin-Karp Algorithm | KMP Algorithm |
| :--- | :--- | :--- |
| **Core Mechanism** | Rolling Numerical Hash | Longest Prefix Suffix (LPS) Array |
| **Single Pattern Search** | $O(N + M)$ Avg / $O(N \cdot M)$ Worst | **$O(N + M)$ Guaranteed Worst-case** |
| **Multi-Pattern Search** | **EXCELLENT ($O(N)$ with HashSet)**| Complex (Requires Aho-Corasick Automaton) |
| **Auxiliary Space** | **$O(1)$** | $O(M)$ |

## 14. How to Recognize This in Questions
* **"Search for multiple patterns of same length M in text"** $\rightarrow$ Rabin-Karp + HashSet ($O(N)$).
* **"Find longest repeated / duplicate substring in string"** $\rightarrow$ Binary Search on Length + Rabin-Karp.

## 15. Frequently Asked Interview Questions
* **Q: What is a Spurious Hit in Rabin-Karp?**  
  *A:* A spurious hit occurs when two distinct string windows produce the same numerical hash modulo $MOD$. It is resolved by performing an explicit character comparison.
* **Q: Why is Rabin-Karp preferred for multi-pattern searching over KMP?**  
  *A:* Rabin-Karp can hash $K$ different patterns into a `HashSet` in $O(K \cdot M)$ time. As the text window slides, its rolling hash is checked against the `HashSet` in $O(1)$ time, finding any pattern match in $O(N + K \cdot M)$ total time.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RABIN-KARP & ROLLING HASH                             |
+-----------------------------------------------------------------------+
| • Hash Formula: (ch0 * B^(M-1) + ch1 * B^(M-2) + ... + chM-1) % MOD   |
| • O(1) Roll Update: ((oldHash - outChar * power) % MOD + MOD) % MOD   |
|                     newHash = (newHash * BASE + inChar) % MOD         |
| • Spurious Hit Guard: Always verify characters when hashes match!    |
| • Multi-Pattern Search: Hash set of K patterns => O(N + K*M) time     |
| • Complexity: O(N + M) Avg Time | O(1) Auxiliary Space                |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the $O(1)$ Rolling Hash update formula from memory.
- [ ] I know why adding `+ MOD` before `% MOD` is required for subtractions.
- [ ] I can explain what a Spurious Hit is and how to handle it.
- [ ] I can explain why Rabin-Karp is optimal for Multi-Pattern search.
- [ ] I can solve LeetCode 187 (Repeated DNA Sequences) using rolling hash.
