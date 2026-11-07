# 05. Boyer-Moore Algorithm: Bad Character Rule, Good Suffix Heuristic & Sub-Linear Bounds

## 1. Introduction
The **Boyer-Moore Algorithm** is a sub-linear string-searching algorithm created by Robert S. Boyer and J. Strother Moore in 1977. Operating on a **Right-to-Left Pattern Comparison Paradigm**, Boyer-Moore compares pattern characters with text characters starting from the end of the pattern ($j = M - 1$ down to $0$). When a character mismatch occurs, Boyer-Moore applies two precomputed heuristics—the **Bad Character Heuristic** and the **Good Suffix Heuristic**—to compute alignment shifts. Boyer-Moore achieves **Sub-Linear Best-Case Time Complexity $O(N / M)$** (skipping up to $M$ text characters in a single step) and **$O(N + M)$ Average Time Complexity** in **$O(M + |\Sigma|)$ Auxiliary Space**.

> **Important:** Core Invariants of the Boyer-Moore Algorithm:
> 1. **Right-to-Left Comparison Invariant**: Compares pattern characters $P[j]$ with text characters $T[i + j]$ starting from pattern tail $j = M - 1$ down to $0$.
> 2. **Bad Character Heuristic**:
>    - Upon mismatch at $T[i + j] = c$:
>      - If mismatch char $c$ exists in pattern $P$ at last occurrence index $\text{badChar}[c]$: Shift alignment $i \leftarrow i + \max(1, j - \text{badChar}[c])$.
>      - If mismatch char $c$ is ABSENT in pattern $P$: Shift alignment $i \leftarrow i + (j + 1)$ (jumps entire pattern past character $c$!).
> 3. **Good Suffix Heuristic**:
>    - If a suffix of $P$ matched before mismatch at $j$, shift pattern right to align matched suffix with its previous occurrence in $P$.
> 4. **Combined Maximum Shift Rule**:
>    $$\text{shift} = \max(\text{shift}_{\text{badChar}}, \text{shift}_{\text{goodSuffix}})$$
>    Guarantees maximum safe rightward alignment shift at every mismatch step! ⚡

```
Boyer-Moore Bad Character Shift Topology (Text T = "GCAATGCCTATGA", Pattern P = "TATGA"):
Align Offset 0: Compare P "TATGA" with T[0..4] "GCAAT" from RIGHT to LEFT:
- Compare P[4] 'A' with T[4] 'T' -> MISMATCH at j=4!
- Bad Character 'T': Last occurrence of 'T' in P "TATGA" is index 2.
- Shift = j - badChar['T'] = 4 - 2 = 2 positions right!

Align Offset 2: Compare P "TATGA" with T[2..6] "AATGC":
- Compare P[4] 'A' with T[6] 'C' -> MISMATCH at j=4!
- Bad Character 'C': 'C' is ABSENT in pattern P!
- Shift = j + 1 = 4 + 1 = 5 positions right! (Sub-Linear Skip!) ⚡
```

---

## 2. Core Concepts & Boyer-Moore Strategy Matrix

### 2.1 Boyer-Moore Strategy Matrix
```
Boyer-Moore Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Heuristic Component   | Primary Function  | Best Case Impact  | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Bad Character Rule**| Shift by char match| **$O(N / M)$ Sub-Linear⚡**| $O(|\Sigma|)$ Array|
| **Good Suffix Rule**  | Shift by suffix   | $O(N + M)$ Bounds | $O(M)$ Array      |
| **Horspool Variant**  | Simplified Bad Char| **Fastest in Practice⚡**| $O(|\Sigma|)$ Array|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Boyer-Moore compares right-to-left! Absent bad char allows sub-linear jumps of M positions O(N / M)!"**

---

## 3. Characteristics & $O(N / M)$ Sub-Linear Best-Case Proof

### 3.1 Mathematical Proof of $O(N / M)$ Sub-Linear Best-Case Time
* Consider Text $T = \text{"ZZZZZZZZZZZZZZZZ"}$ ($N$ 'Z's) and Pattern $P = \text{"ABCDE"}$ ($M = 5$).
* Align $P$ at $i = 0$. Compare rightmost character $P[4]$ ('E') with $T[4]$ ('Z').
* Mismatch at $j = 4$. Mismatch character 'Z' is ABSENT in $P$.
* Bad Character Rule shifts alignment $i \leftarrow i + M = i + 5$.
* Next comparison evaluates $T[9]$ ('Z').
* Number of comparisons executed across text of length $N$:
  $$\text{Comparisons} = \frac{N}{M} = \mathbf{O(N / M) \text{ Sub-Linear Time Complexity}}$$
* Demonstrates why Boyer-Moore runs faster as pattern length $M$ INCREASES! ⚡

---

## 4. Internal Working Mechanics: Horspool Variant (Simplified Bad Char)

Boyer-Moore-Horspool simplifies the standard algorithm by computing bad character shifts based ONLY on the rightmost text character $T[i + M - 1]$:

```
Horspool Bad Character Shift Table Construction for P = "NEEDLE":

Alphabet Size |Sigma| = 256. Default shift for all chars = M = 6.

Populate Bad Char Shift Table for pattern chars P[0 ... M-2]:
- 'N' (Index 0): shift['N'] = 6 - 1 - 0 = 5
- 'E' (Index 1): shift['E'] = 6 - 1 - 1 = 4
- 'E' (Index 2): shift['E'] = 6 - 1 - 2 = 3 (Overwrites 'E')
- 'D' (Index 3): shift['D'] = 6 - 1 - 3 = 2
- 'L' (Index 4): shift['L'] = 6 - 1 - 4 = 1
- 'E' (Index 5): Last char skipped in precomputation!

Horspool Shift = shift[ T[i + M - 1] ]! Simple, fast, and sub-linear! ✅
```

---

## 5. Visual Diagram: Bad Character Absent Jump Mechanics

```
Text T:     [ G | C | A | A | T | G | C | C | T | A | T | G | A ]
              │   │   │   │   │
Pattern P:  [ T | A | T | G | A ]   (Compare Right-to-Left from Index 4!)
                                ▲
                                Mismatch at j=4 ('T' != 'A')

Bad Char 'T' is at index 2 in P ──> Shift pattern right by 4 - 2 = 2 positions! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Boyer-Moore Bad Character Heuristic Search and Boyer-Moore-Horspool Fast Search.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Boyer-Moore Algorithm,
 * Bad Character Heuristics, and Horspool Fast Sub-Linear Matching.
 */
public class BoyerMooreMaster {

    private static final int ALPHABET_SIZE = 256; // Extended ASCII Alphabet Size |Sigma|

    // =========================================================================
    // 1. BOYER-MOORE BAD CHARACTER SEARCH (O(N / M) Best Time, O(M + |Sigma|) Space)
    // =========================================================================
    /**
     * Finds all 0-based starting indices of pattern P in text T using Boyer-Moore Bad Character Rule.
     *
     * @param text input text string T
     * @param pattern search pattern P
     * @return list of starting match indices
     */
    public List<Integer> searchBadCharacter(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();

        if (m == 0 || m > n) return matches;

        // Step 1: Precompute Bad Character Heuristic Array in O(M + |Sigma|) Time
        int[] badChar = buildBadCharacterTable(pattern);

        int s = 0; // s is the alignment shift offset of pattern relative to text

        while (s <= n - m) {
            int j = m - 1; // Start comparing from RIGHT to LEFT!

            // Compare pattern characters right-to-left
            while (j >= 0 && pattern.charAt(j) == text.charAt(s + j)) {
                j--;
            }

            if (j < 0) {
                // Match Found! Record starting index s
                matches.add(s);

                // Shift pattern so next char aligns with last occurrence in pattern
                s += (s + m < n) ? m - badChar[text.charAt(s + m)] : 1;
            } else {
                // Mismatch encountered at j
                char mismatchChar = text.charAt(s + j);

                // Calculate Bad Character Shift: max(1, j - badChar[mismatchChar])
                int shift = Math.max(1, j - badChar[mismatchChar]);
                s += shift; // Jump alignment offset rightward! ⚡
            }
        }

        return matches;
    }

    private int[] buildBadCharacterTable(String pattern) {
        int[] badChar = new int[ALPHABET_SIZE];

        // Initialize all characters as -1 (absent in pattern)
        Arrays.fill(badChar, -1);

        // Record last occurrence index of each character in pattern
        for (int i = 0; i < pattern.length(); i++) {
            badChar[pattern.charAt(i)] = i;
        }

        return badChar;
    }

    // =========================================================================
    // 2. BOYER-MOORE-HORSPOOL FAST SEARCH (O(N / M) Best Time - Simplest Code)
    // =========================================================================
    /**
     * Performs Boyer-Moore-Horspool Fast Search.
     * Uses rightmost text character T[s + m - 1] for bad character shift lookup.
     */
    public List<Integer> searchHorspool(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();
        if (m == 0 || m > n) return matches;

        // Precompute Horspool Shift Table
        int[] shiftTable = new int[ALPHABET_SIZE];
        Arrays.fill(shiftTable, m); // Default shift = M

        for (int i = 0; i < m - 1; i++) {
            shiftTable[pattern.charAt(i)] = m - 1 - i;
        }

        int s = 0;
        while (s <= n - m) {
            int j = m - 1;

            while (j >= 0 && pattern.charAt(j) == text.charAt(s + j)) {
                j--;
            }

            if (j < 0) {
                matches.add(s); // Match found!
            }

            // Horspool Shift based on rightmost character T[s + m - 1]
            s += shiftTable[text.charAt(s + m - 1)];
        }

        return matches;
    }
}
```

> **Quick Syntax:**
```java
// Boyer-Moore Bad Character Shift Line
int shift = Math.max(1, j - badChar[text.charAt(s + j)]); s += shift;
```

---

## 7. Concrete Problem Examples & Applications

1. **Text Editors & IDE Search Tools (ctrl+F)**:
   - Boyer-Moore is the standard engine powering search features in text editors (e.g. GNU grep, VS Code) due to its sub-linear speed on long patterns.

2. **DNA Genomic Sequence Matching**:
   - Matching long DNA sequences ($|\Sigma|=4$) where sub-linear jumps skip thousands of characters.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class BoyerMooreDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BOYER-MOORE SUB-LINEAR SEARCHING DEMO         ");
        System.out.println("=================================================\n");

        BoyerMooreMaster master = new BoyerMooreMaster();

        // 1. Bad Character Boyer-Moore Test
        String text1 = "GCAATGCCTATGA";
        String pattern1 = "TATGA";
        List<Integer> matches1 = master.searchBadCharacter(text1, pattern1);
        System.out.println("1. Text   : \"" + text1 + "\"");
        System.out.println("   Pattern: \"" + pattern1 + "\"");
        System.out.println("   Boyer-Moore Bad Char Matches: " + matches1);
        System.out.println("-------------------------------------------------");

        // 2. Horspool Fast Search Test
        String text2 = "HERE IS A SIMPLE EXAMPLE";
        String pattern2 = "EXAMPLE";
        List<Integer> matches2 = master.searchHorspool(text2, pattern2);
        System.out.println("2. Text (Horspool Search): \"" + text2 + "\"");
        System.out.println("   Pattern               : \"" + pattern2 + "\"");
        System.out.println("   Matches Found at      : " + matches2);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Boyer-Moore Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Feature |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bad Character Rule** | $\mathbf{O(N / M)}$ Sub-Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $O(N \cdot M)$ Worst | $O(|\Sigma|)$ Table | Right-to-Left Scan |
| **Horspool Variant**   | $\mathbf{O(N / M)}$ Sub-Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $O(N \cdot M)$ Worst | $O(|\Sigma|)$ Table | Shift on $T[s+m-1]$ |
| **Full Boyer-Moore**   | $\mathbf{O(N / M)}$ Sub-Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N + M)}$ Strict ⚡| $O(M + |\Sigma|)$ | Combined Max Shift |

---

## 10. Edge Cases & Boundary Handling

1. **Negative Bad Character Shifts (`j - badChar[c] < 0`)**:
   - Handled cleanly by `Math.max(1, j - badChar[c])` to guarantee alignment shift $s$ always moves strictly forward by at least 1 position.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Comparing Left-to-Right in Boyer-Moore**:
  - Boyer-Moore MUST compare characters from **RIGHT to LEFT** ($j = M - 1$ down to $0$) to enable bad character sub-linear jumps.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Boyer-Moore Gets FASTER as Pattern Length $M$ Increases:
> In Naive/KMP algorithms, a longer pattern increases work.
> In Boyer-Moore, a longer pattern $M$ increases bad character jump distances ($i \leftarrow i + M$), reducing the total number of text comparisons down to $O(N / M)$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Boyer-Moore Algorithm | KMP Algorithm | Naive Search |
| :--- | :--- | :--- | :--- |
| **Best Case Time** | **$O(N / M)$ Sub-Linear ⚡**| $O(N)$ Linear | $O(N)$ Linear |
| **Comparison Order**| **Right-to-Left (M-1..0)⚡**| Left-to-Right (0..N) | Left-to-Right (0..N) |
| **Pattern Length Trend**| **FASTER as M grows ⚡**| Slower as M grows | Slower as M grows |

---

## 14. How to Recognize This in Questions

* **"Search long pattern in large text file with maximum speed (grep / text editor engine)"** $\rightarrow$ Boyer-Moore Algorithm.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Boyer-Moore compare characters right-to-left?**  
  *A:* Because comparing from right-to-left aligns the pattern's tail with text. If a mismatch occurs at the pattern tail on an absent character, the entire pattern can skip $M$ positions rightward.

* **Q: What is the Bad Character Rule?**  
  *A:* A heuristic that shifts the pattern rightward until the text mismatch character aligns with its last occurrence in the pattern, or shifts past the mismatch character completely if absent.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BOYER-MOORE ALGORITHM                                 |
+-----------------------------------------------------------------------+
| • Direction     : Compares pattern right-to-left (j = M - 1 down to 0)|
| • Bad Char Shift: shift = max(1, j - badChar[mismatchChar])           |
| • Absent Shift  : If bad char absent in P -> Jump full M positions!   |
| • Best Case     : O(N / M) Sub-Linear Time (FASTER for longer M!) ⚡    |
| • Horspool Variant: Uses shiftTable[ T[s + m - 1] ] for simple speed |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the Bad Character Table precomputation routine in Java.
- [ ] I can write Boyer-Moore right-to-left pattern matching.
- [ ] I can write Boyer-Moore-Horspool Fast Search.
- [ ] I can prove why Boyer-Moore runs in $O(N / M)$ sub-linear time in best case.
- [ ] I can explain why `Math.max(1, j - badChar[c])` is necessary to prevent negative shifts.
