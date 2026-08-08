# 09. Frequency Array & Counting Techniques

## 1. Introduction
The **Frequency Array** (or Counting Array) technique maps element values directly to array indices to record occurrence counts, state flags, or distribution frequencies. In technical coding interviews, frequency arrays replace hash tables when element value ranges are known and bounded (e.g., lowercase characters `a-z`, digits `0-9`, or numbers $0 \le \text{val} \le K$), operating in **$O(n)$ time and $O(1)$ auxiliary space** with zero object allocation overhead.

> **Important:** Using an `int[26]` primitive frequency array for lowercase ASCII character counts is over **10x faster** and consumes **95% less memory** than a `HashMap<Character, Integer>` because it avoids autoboxing, object headers, and hash collision checks!

## 2. Core Concepts
* **Direct Index Mapping**: Value $V$ maps directly to array index $V$ (or $V - \text{minVal}$). `freq[V]++` increments the occurrence count of $V$ in $O(1)$ time.
* **ASCII Offset Mapping**: For lowercase English letters `'a'` through `'z'`, character $C$ maps to index `C - 'a'` (range 0 to 25).
* **Boyer-Moore Majority Voting Algorithm**: A specialized $O(n)$ time and $O(1)$ space frequency algorithm that finds the majority element (appearing $> n/2$ times) without allocating any frequency array or hash map.
* **Bucket Sort / Counting Sort Connection**: Using frequency arrays to achieve linear-time $O(n)$ sorting when element ranges are small.

> **Memory Trick:** **"Index = Element Value, Content = Element Frequency"**. For characters, index = `char - 'a'`.

## 3. Characteristics / Properties
* **Range Dependence**: Frequency arrays require element values to sit within a reasonable, bounded integer range (e.g., $\text{maxVal} \le 10^6$). If element values are huge ($10^9$) or negative, HashMaps or Coordinate Compression must be used.
* **$O(1)$ Auxiliary Space**: Primitive fixed-size frequency arrays (`int[26]`, `int[256]`, `int[1000]`) occupy constant space independent of input size $N$.

```
Frequency Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Frequency Strategy    | Time Complexity   | Space Complexity  | Best Used When    |
+-----------------------+-------------------+-------------------+-------------------+
| Primitive Frequency Array| O(n)           | O(1) (Fixed Range)| Value range bounded (e.g. 26, 256)|
| HashMap<K, V>         | O(n)              | O(n)              | Unbounded / Huge values |
| Boyer-Moore Voting    | O(n)              | O(1)              | Majority Element (> n/2) |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Boyer-Moore Majority Voting Algorithm on `nums = [2, 2, 1, 1, 1, 2, 2]` ($N = 7$):

```
Initialization: candidate = 0, count = 0

i = 0 (val 2): count == 0 -> candidate = 2, count = 1
i = 1 (val 2): val == candidate -> count = 2
i = 2 (val 1): val != candidate -> count = 1
i = 3 (val 1): val != candidate -> count = 0 (Reset trigger!)
i = 4 (val 1): count == 0 -> candidate = 1, count = 1
i = 5 (val 2): val != candidate -> count = 0 (Reset trigger!)
i = 6 (val 2): count == 0 -> candidate = 2, count = 1

Surviving Candidate: 2 (Majority Element appearing > 7/2 = 3 times) ✅
```

## 5. Visual Diagram
ASCII Offset Mapping (`char - 'a'`) Layout:

```
Character:   'a'    'b'    'c'   ...   'z'
Index Math:  'a'-'a' 'b'-'a' 'c'-'a'   'z'-'a'
Index:        0      1      2    ...   25
           +------+------+------+-----+------+
freq[]:    |  3   |  0   |  5   | ... |  1   |
           +------+------+------+-----+------+
```

## 6. Operations / Algorithms
Core Frequency Array Algorithms:

### 1. Character Frequency Array (`int[26]`)
```java
int[] freq = new int[26];
for (char c : str.toCharArray()) {
    freq[c - 'a']++;
}
```

### 2. Valid Anagram Check (LeetCode 242)
```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] freq = new int[26];
    for (int i = 0; i < s.length(); i++) {
        freq[s.charAt(i) - 'a']++;
        freq[t.charAt(i) - 'a']--;
    }
    for (int count : freq) {
        if (count != 0) return false;
    }
    return true;
}
```

### 3. Boyer-Moore Majority Element (LeetCode 169)
```java
public int majorityElement(int[] nums) {
    int candidate = 0;
    int count = 0;
    for (int num : nums) {
        if (count == 0) {
            candidate = num;
        }
        count += (num == candidate) ? 1 : -1;
    }
    return candidate; // O(n) time, O(1) space!
}
```

> **Quick Syntax:**
```java
// Lowercase Char Offset Indexing
int index = ch - 'a'; // 'a' -> 0, 'b' -> 1, ..., 'z' -> 25

// Uppercase Char Offset Indexing
int indexUpper = ch - 'A'; // 'A' -> 0, 'B' -> 1, ..., 'Z' -> 25
```

## 7. Examples
* **LeetCode 242 - Valid Anagram**: Checking if two strings have identical character frequencies using `int[26]`.
* **LeetCode 387 - First Unique Character in a String**: Two-pass traversal using `int[26]` frequency array.
* **LeetCode 169 - Majority Element**: Finding element appearing $> n/2$ times using Boyer-Moore Voting Algorithm in $O(1)$ space.

## 8. Java Code
Complete interview-ready Java suite implementing Character Frequency Analysis, Valid Anagram, First Unique Character, and Boyer-Moore Majority Voting:

```java
public class FrequencyTechniquesMaster {

    // 1. Valid Anagram Check O(N) Time, O(1) Space (int[26])
    public static boolean isAnagram(String s, String t) {
        if (s == null || t == null || s.length() != t.length()) return false;

        int[] freq = new int[26];
        int n = s.length();

        for (int i = 0; i < n; i++) {
            freq[s.charAt(i) - 'a']++;
            freq[t.charAt(i) - 'a']--;
        }

        for (int count : freq) {
            if (count != 0) return false;
        }

        return true;
    }

    // 2. First Unique Character in String O(N) Time, O(1) Space
    public static int firstUniqChar(String s) {
        if (s == null || s.length() == 0) return -1;

        int[] freq = new int[26];

        // Pass 1: Build frequency map
        for (int i = 0; i < s.length(); i++) {
            freq[s.charAt(i) - 'a']++;
        }

        // Pass 2: Find first character with frequency 1
        for (int i = 0; i < s.length(); i++) {
            if (freq[s.charAt(i) - 'a'] == 1) {
                return i;
            }
        }

        return -1; // No unique character found
    }

    // 3. Boyer-Moore Majority Element Algorithm O(N) Time, O(1) Space
    public static int majorityElement(int[] nums) {
        if (nums == null || nums.length == 0) return -1;

        int candidate = 0;
        int count = 0;

        // Step 1: Find candidate
        for (int num : nums) {
            if (count == 0) {
                candidate = num;
            }
            count += (num == candidate) ? 1 : -1;
        }

        // Step 2: Verification pass (optional if majority element is guaranteed)
        int verifyCount = 0;
        for (int num : nums) {
            if (num == candidate) verifyCount++;
        }

        return (verifyCount > nums.length / 2) ? candidate : -1;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Anagram Test
        System.out.println("Is 'anagram' & 'nagaram' Anagram? " + isAnagram("anagram", "nagaram")); // true

        // First Unique Char Test
        System.out.println("First Unique Char in 'leetcode': Index " + firstUniqChar("leetcode")); // Output: 0 ('l')
        System.out.println("First Unique Char in 'loveleetcode': Index " + firstUniqChar("loveleetcode")); // Output: 2 ('v')

        // Boyer-Moore Majority Test
        int[] nums = {2, 2, 1, 1, 1, 2, 2};
        System.out.println("Majority Element in {2,2,1,1,1,2,2}: " + majorityElement(nums)); // Output: 2
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Valid Anagram (`int[26]`)** | $O(N)$ | $O(1)$ fixed 26 ints | Zero heap object allocations |
| **First Unique Char (`int[26]`)**| $O(N)$ | $O(1)$ fixed 26 ints | Fast two-pass indexing |
| **Boyer-Moore Majority Vote** | $O(N)$ | $O(1)$ constant | Zero frequency storage required |
| **Counting Sort** | $O(N + K)$ | $O(K)$ range space | Sorts bounded integers in linear time |

## 10. Edge Cases
* **Negative Integer Values**: If array elements can be negative (e.g., values from $-100$ to $+100$), add an offset constant `offset = 100` so `freq[val + offset]` maps to non-negative index ranges $0 \dots 200$.
* **Full ASCII (Extended)**: If string contains spaces, punctuation, or unicode, `int[26]` will crash! Use `int[256]` for full ASCII or `HashMap<Character, Integer>` for Unicode.
* **No Majority Element Exists**: If problem does NOT guarantee a majority element ($> n/2$), Boyer-Moore requires a mandatory second verification pass to count candidate occurrences.

## 11. Common Mistakes
* Out of bounds error by using `c - 'a'` on uppercase letters or special characters (causes `ArrayIndexOutOfBoundsException`).
* Allocating a massive array `int[1_000_000_000]` when element values are huge ($10^9$) (causes `OutOfMemoryError`!). Use `HashMap` or Coordinate Compression instead.
* Assuming Boyer-Moore works for finding elements appearing $> n/3$ times without extending the algorithm to 2 candidates (Boyer-Moore for $> n/3$ requires 2 candidates and 2 counters!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Prefer primitive frequency arrays (`int[26]`) over `HashMap<Character, Integer>` whenever character inputs are restricted to lowercase English letters. Mention to the interviewer: *"Since the character set is restricted to lowercase English letters, I am using a fixed-size `int[26]` frequency array to achieve $O(1)$ space and eliminate object overhead."*

> **Memory Trick:** **"Candidate counter increment/decrement cancels non-majority elements in Boyer-Moore"**.

## 13. Comparisons
| Metric | Primitive Frequency Array (`int[26]`) | HashMap (`HashMap<Character, Integer>`) |
| :--- | :--- | :--- |
| **Lookup Speed** | $O(1)$ direct array index lookup | $O(1)$ avg (hash computation + bucket traversal) |
| **Memory Footprint**| 104 bytes total (26 ints) | $\approx 1.5$ KB (Object headers, Map Entries, Nodes) |
| **Input Restriction**| Fixed/Bounded ranges only | Accepts any unbounded / object key types |
| **GC Overhead** | Zero | High garbage collection pressure |

## 14. How to Recognize This in Questions
* **"Check if two strings are anagrams or permutations of each other"** $\rightarrow$ `int[26]` Frequency Array.
* **"Find element appearing more than N/2 times in O(1) space"** $\rightarrow$ Boyer-Moore Majority Voting Algorithm.

## 15. Frequently Asked Interview Questions
* **Q: Why does Boyer-Moore Voting Algorithm guarantee finding the majority element if it exists?**  
  *A:* Because the majority element appears more than $N/2$ times. Even if all other elements ($< N/2$) pair up to decrement the majority element's count, the majority element will still have a net positive count at the end of the array pass.
* **Q: How do you handle uppercase AND lowercase letters in a frequency array?**  
  *A:* Allocate `int[52]` where $0 \dots 25$ maps lowercase (`c - 'a'`) and $26 \dots 51$ maps uppercase (`c - 'A' + 26`), or use `int[128]` / `int[256]` for standard ASCII offsets.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FREQUENCY & COUNTING TECHNIQUES                       |
+-----------------------------------------------------------------------+
| • Lowercase Index Mapping: index = char - 'a' (Range 0..25)           |
| • Anagram Trick: Single freq[26] array; ++ for string1, -- for string2|
| • Prefer int[26] over HashMap for 10x faster execution & zero GC      |
| • Boyer-Moore Voting: Majority (>N/2) candidate count += (num==cand)?1:-1|
| • Negative Values: Use offset index = val + MIN_VALUE_OFFSET          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement `int[26]` frequency mapping from memory.
- [ ] I can write the single-array Valid Anagram check (`++` and `--`).
- [ ] I can implement Boyer-Moore Majority Voting Algorithm in $O(1)$ space.
- [ ] I know how to handle negative number ranges using index offsets.
- [ ] I understand why `int[26]` is preferred over `HashMap` for string problems.
