# 09. Frequency Counting Algorithms, Top K Bucket Sort & Substring Windows

## 1. Introduction
**Frequency Counting** is one of the most fundamental applications of Hash Maps and Fixed-Size Frequency Arrays (`int[26]` or `int[128]`). By recording item frequencies in $O(1)$ constant time per item, algorithms like **First Unique Character in a String (LeetCode 387)**, **Top K Frequent Elements (LeetCode 347)**, **Valid Anagram (LeetCode 242)**, and **Minimum Window Substring (LeetCode 76)** solve sequence analytics in **$O(N)$ linear time and $O(U)$ space** (where $U$ is unique element count).

> **Important:** For **Top K Frequent Elements (LeetCode 347)**, using a **Bucket Sort Strategy** (where bucket index represents element frequency $1 \dots N$) reduces time complexity from $O(N \log K)$ (PriorityQueue) down to **$O(N)$ Strict Linear Time**!

```
Frequency Bucket Sort Topology (LeetCode 347):
Input Array : [ 1, 1, 1, 2, 2, 3 ] (Element Frequencies: 1->3, 2->2, 3->1)
Bucket Index:  0       1          2          3
Buckets     : [ ] | [ Val 3 ] | [ Val 2 ] | [ Val 1 ]
                    ^ (Freq 1)  ^ (Freq 2)  ^ (Freq 3 - Top 1!)
Scan buckets right-to-left to retrieve Top K elements in O(N) Time! ⚡
```

---

## 2. Core Concepts & Frequency Counting Mechanics

### 2.1 First Unique Character in a String (LeetCode 387)
Given a string `s`, find the first non-repeating character and return its index. If it does not exist, return `-1`:
1. Use frequency array `int[] count = new int[26]`.
2. First Pass: Compute character frequencies for all characters in `s`.
3. Second Pass: Iterate `s` from `i = 0` to $N-1$. The first character with `count[c - 'a'] == 1` is the answer!
4. Time Complexity: **$O(N)$ Linear Time**, Space: **$O(1)$ Fixed Array Space**.

### 2.2 Top K Frequent Elements (LeetCode 347 - Bucket Sort Strategy)
Given an integer array `nums` and integer $K$, return the $K$ most frequent elements:
1. Count frequencies using `Map<Integer, Integer> freqMap = new HashMap<>()`.
2. Create bucket array `List<Integer>[] buckets = new List[N + 1]`.
3. For each key `num` in `freqMap`:
   - `freq = freqMap.get(num)`.
   - If `buckets[freq] == null`, allocate `new ArrayList<>()`.
   - `buckets[freq].add(num)`.
4. Iterate buckets from **`i = N` down to `1`**:
   - Collect elements until $K$ elements are accumulated.
5. Return result array. Time Complexity: **$O(N)$ Linear Time**!

```
Bucket Array Frequency Bounds:
The maximum frequency any element can achieve in an array of size N is N!
Therefore, creating a bucket array of size N + 1 guarantees an O(1) direct bucket lookup for any frequency! ⚡
```

> **Memory Trick:** **"Top K Frequent Elements: Bucket index = Frequency! Scan buckets from N down to 1 for O(N) time!"**

---

## 3. Characteristics & Minimum Window Substring (LeetCode 76)

### 3.1 Minimum Window Substring (LeetCode 76 - Sliding Window + Frequency Hashing)
Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included:
* **`targetMap`**: Stores character frequencies of `t`.
* **`matched`**: Tracks count of unique characters satisfying target frequency requirements.
* **Sliding Window Algorithm**:
  1. Expand `right` pointer, updating `windowMap`.
  2. When character frequency meets target (`windowMap == targetMap`), increment `matched++`.
  3. While `matched == targetMap.size()` (Valid Window):
     - Record minimum window bounds `[left, right]`.
     - Contract `left` pointer, updating `windowMap` and decrementing `matched` when valid state is broken.

---

## 4. Internal Working Mechanics
Tracing Top K Frequent Elements (LeetCode 347) on `nums = [1, 1, 1, 2, 2, 3]`, $K = 2$:

```
Step 1: Map Frequencies -> {1: 3, 2: 2, 3: 1}
Step 2: Create Buckets array of size 7 (Indices 0..6):
  Buckets[1] = [3]  (Frequency 1)
  Buckets[2] = [2]  (Frequency 2)
  Buckets[3] = [1]  (Frequency 3)

Step 3: Collect Top K (K = 2) from right to left (Index 6 down to 1):
  - Index 6..4: Empty
  - Index 3: Add 1 (K remaining = 1)
  - Index 2: Add 2 (K remaining = 0 -> STOP!)

Result Array = [1, 2] ✅ (Executed in O(N) Time!)
```

---

## 5. Visual Diagram
Frequency Counting Bucket Sort Topography:

```
Bucket Array Index (Represents Frequency):
Index 0 : [ ]
Index 1 : [ 3 ]  (Character '3' appears 1 time)
Index 2 : [ 2 ]  (Character '2' appears 2 times)
Index 3 : [ 1 ]  (Character '1' appears 3 times)  <--- Top 1 Most Frequent!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing First Unique Character (LeetCode 387), Top K Frequent Elements (LeetCode 347), and Minimum Window Substring (LeetCode 76):

```java
import java.util.*;

public class FrequencyCountingMaster {

    // 1. First Unique Character in String (LeetCode 387) O(N) Time, O(1) Space
    public static int firstUniqChar(String s) {
        if (s == null || s.length() == 0) return -1;

        int[] count = new int[26];
        int n = s.length();

        for (int i = 0; i < n; i++) {
            count[s.charAt(i) - 'a']++;
        }

        for (int i = 0; i < n; i++) {
            if (count[s.charAt(i) - 'a'] == 1) {
                return i;
            }
        }

        return -1;
    }

    // 2. Top K Frequent Elements (LeetCode 347 - Bucket Sort Strategy) O(N) Time, O(N) Space
    @SuppressWarnings("unchecked")
    public static int[] topKFrequent(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];

        // Step 1: Map frequencies
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);
        }

        // Step 2: Bucket array where index represents frequency
        int n = nums.length;
        List<Integer>[] buckets = new List[n + 1];

        for (int key : freqMap.keySet()) {
            int freq = freqMap.get(key);
            if (buckets[freq] == null) {
                buckets[freq] = new ArrayList<>();
            }
            buckets[freq].add(key);
        }

        // Step 3: Collect top K elements from right to left
        int[] result = new int[k];
        int p = 0;

        for (int i = n; i >= 1 && p < k; i--) {
            if (buckets[i] != null) {
                for (int num : buckets[i]) {
                    result[p++] = num;
                    if (p == k) break;
                }
            }
        }

        return result;
    }

    // 3. Minimum Window Substring (LeetCode 76) O(N) Time, O(U) Space
    public static String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) return "";

        Map<Character, Integer> targetMap = new HashMap<>();
        for (char c : t.toCharArray()) {
            targetMap.put(c, targetMap.getOrDefault(c, 0) + 1);
        }

        Map<Character, Integer> windowMap = new HashMap<>();
        int matched = 0;
        int minLen = Integer.MAX_VALUE;
        int start = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (targetMap.containsKey(c)) {
                windowMap.put(c, windowMap.getOrDefault(c, 0) + 1);
                if (windowMap.get(c).equals(targetMap.get(c))) {
                    matched++;
                }
            }

            while (matched == targetMap.size()) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    start = left;
                }

                char leftChar = s.charAt(left);
                if (targetMap.containsKey(leftChar)) {
                    if (windowMap.get(leftChar).equals(targetMap.get(leftChar))) {
                        matched--;
                    }
                    windowMap.put(leftChar, windowMap.get(leftChar) - 1);
                }
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
    }
}
```

> **Quick Syntax:**
```java
// Frequency Counter Line
map.put(key, map.getOrDefault(key, 0) + 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 387 - First Unique Character**: 2-pass frequency array.
* **LeetCode 347 - Top K Frequent Elements**: Frequency bucket sort.
* **LeetCode 76 - Minimum Window Substring**: Sliding window frequency map.
* **LeetCode 242 - Valid Anagram**: Character frequency match.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing First Unique Character, Top K Frequent, and Minimum Window Substring:

```java
public class FrequencyCountingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. First Unique Character (LeetCode 387) ===");
        String s1 = "leetcode";
        System.out.println("First Unique Index in \"leetcode\": " + 
            FrequencyCountingMaster.firstUniqChar(s1)); // Output: 0 ('l')

        System.out.println("\n=== 2. Top K Frequent Elements (LeetCode 347) ===");
        int[] nums2 = {1, 1, 1, 2, 2, 3};
        int[] topK = FrequencyCountingMaster.topKFrequent(nums2, 2);
        System.out.println("Top 2 Frequent Elements: " + Arrays.toString(topK)); // Output: [1, 2]

        System.out.println("\n=== 3. Minimum Window Substring (LeetCode 76) ===");
        String s3 = "ADOBECODEBANC", t3 = "ABC";
        String minWin = FrequencyCountingMaster.minWindow(s3, t3);
        System.out.println("Min Window Substring: \"" + minWin + "\""); // Output: "BANC"
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **First Unique Char (387)**| **$O(N)$ Linear ⚡** | **$O(1)$ Array Space ⚡**| 2-pass fixed frequency array |
| **Top K Frequent (347)** | **$O(N)$ Linear ⚡** | $O(N)$ Bucket Space | Frequency index bucket sort |
| **Min Window Substring (76)**| **$O(N)$ Linear ⚡**| $O(U)$ Map Space | Sliding window + frequency map |

---

## 10. Edge Cases & Boundary Handling
* **$K > \text{Unique Elements}$ in Top K**: `p < k` condition guards against index out of bounds.
* **No Valid Window in LeetCode 76**: Returns `""` when `minLen == Integer.MAX_VALUE`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Min Heap ($O(N \log K)$ Time Penalty) for Top K**:
  - Using `PriorityQueue` takes $O(N \log K)$ time.
  - **Use Bucket Sort (where index = frequency) for $O(N)$ strict linear time**.
* **Using `==` Integer Object Comparison in Frequency Maps**:
  - `windowMap.get(c) == targetMap.get(c)` fails for counts $> 127$ due to Object caching bounds!
  - **Always use `windowMap.get(c).equals(targetMap.get(c))`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** PriorityQueue vs Bucket Sort for Top K Frequent Elements:
> * **PriorityQueue (Min Heap)**: $O(N \log K)$ Time, $O(N)$ Space. Good for streaming data.
> * **Bucket Sort**: **$O(N)$ Linear Time**, $O(N)$ Space. Optimal when full array is available in memory.

> **Memory Trick:** **"Bucket sort achieves O(N) time for Top K by mapping frequency to array indices!"**

---

## 13. System & Implementation Comparisons

| Feature | Bucket Sort Top K | PriorityQueue (Min Heap) Top K |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡** | $O(N \log K)$ Logarithmic |
| **Streaming Support** | No (Requires full array) | **Yes (Supports continuous streams) ⚡**|
| **Code Footprint** | ~15 Lines | ~10 Lines |

---

## 14. How to Recognize This in Questions
* **"Find first non-repeating character in string"** $\rightarrow$ Fixed frequency array `int[26]`.
* **"Find K most frequent elements in O(N) time"** $\rightarrow$ Frequency bucket sort (LeetCode 347).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Bucket Sort solve Top K Frequent Elements in $O(N)$ time?**  
  *A:* Because the maximum possible frequency of any item is $N$. Creating a bucket array of size $N+1$ allows placing elements into frequency buckets in $O(1)$ time and scanning frequencies from $N$ down to 1 in $O(N)$ total time.
* **Q: Why should `int[26]` array be used instead of `HashMap` for lowercase ASCII strings?**  
  *A:* Fixed-size array `int[26]` allocates zero heap objects, runs in constant memory ($O(1)$ space), and executes faster due to direct CPU array indexing.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FREQUENCY COUNTING ALGORITHMS                        |
+-----------------------------------------------------------------------+
| • Frequency Increment: map.put(k, map.getOrDefault(k, 0) + 1)         |
| • ASCII Optimization: Use int[26] or int[128] for character counts    |
| • Top K Bucket Sort: Bucket index = frequency; scan N down to 1 (O(N))|
| • Object Equality Rule: Use .equals() when comparing Integer map values|
| • Min Window (76): Expand right for valid; contract left for minimum  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write First Unique Character (LeetCode 387) using `int[26]`.
- [ ] I can write Top K Frequent Elements (LeetCode 347) using Bucket Sort in $O(N)$ time.
- [ ] I can write Minimum Window Substring (LeetCode 76) using sliding window.
- [ ] I know why `.equals()` must be used for `Integer` value comparisons.
- [ ] I know when to use Bucket Sort vs Min Heap.
