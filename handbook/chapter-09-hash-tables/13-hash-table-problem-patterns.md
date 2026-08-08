# 13. Hash Table Problem Recognition Patterns & Strategy Selection

## 1. Introduction
Solving hashing and associative map problems in technical coding interviews requires rapid pattern recognition. Identifying problem signals—such as pairwise sum targets, contiguous subarray sum constraints over arrays containing negative numbers, anagram clustering, string isomorphism, sequence boundary detection, or dynamic LRU caching—dictates the optimal algorithmic pattern: Single-Pass Complement Lookup, Prefix Sum Complement Mapping, Canonical Frequency Key Generator, Bijective Dual Mapping, Set Boundary Filter, or LinkedHashMap Access-Ordering.

> **Important:** Recognizing whether a problem requires **Prefix Sum Frequency Mapping** ($O(N)$ for negative numbers) vs **Sliding Window** ($O(N)$ for positive numbers only) is a critical decision point in coding interviews.

```
Hash Pattern Decision Matrix:
+-----------------------------------------------------------------------------------+
| 1. Complement Search  : Target - nums[i] -> Single-Pass HashMap (Check First!)    |
| 2. Range Sum Query    : PrefixSum[j] - K -> Prefix Sum HashMap (map.put(0,1)!)    |
| 3. String Clustering  : Anagrams / Shifts -> Canonical Key Format (#1#0#1...)     |
| 4. Sequence Boundary  : Longest Consecutive -> Set Filter (!set.contains(num-1))  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Decision Matrix

### 2.1 The 6 Core Hash Table Problem Patterns
1. **Pattern 1: Single-Pass Complement Lookup (`target - nums[i]`)**:
   - *Signal*: "Find two numbers in an unsorted array that add up to target".
   - *Idiom*: Check `map.containsKey(complement)` BEFORE calling `map.put(nums[i], i)`.
2. **Pattern 2: Prefix Sum Complement Hash (`P[j] - K`)**:
   - *Signal*: "Find contiguous subarrays with sum equal to K (array contains negative numbers)".
   - *Idiom*: Initialize `map.put(0, 1)`, check `map.get(P[j] - K)`.
3. **Pattern 3: Canonical Key Generation (`#1#0#1...`)**:
   - *Signal*: "Group anagrams or strings under equivalence transformations".
   - *Idiom*: Format 26-character frequency array with `#` delimiters as map key.
4. **Pattern 4: Set Boundary Scan Filter (`!set.contains(n - 1)`)**:
   - *Signal*: "Find longest consecutive sequence of numbers in $O(N)$ time".
   - *Idiom*: Insert all items into `HashSet`, expand ONLY if `num - 1` is absent.
5. **Pattern 5: Bijective Dual Mapping (`mapST` & `mapTS` / `int[256]`)**:
   - *Signal*: "Check if two strings are isomorphic or follow word pattern 'abba'".
   - *Idiom*: Enforce 1-to-1 mappings in BOTH directions using `lastSeenS[s[i]] == lastSeenT[t[i]]`.
6. **Pattern 6: Access-Order LinkedHashMap (`removeEldestEntry`)**:
   - *Signal*: "Design an LRU Cache with $O(1)$ get and put".
   - *Idiom*: Extend `LinkedHashMap` with `accessOrder = true` and override `removeEldestEntry()`.

```
Comprehensive Pattern Decision Matrix:
+------------------------------------+------------------------------+--------------------+
| Problem Phrasing / Signal          | Optimal Hash Pattern         | Target Complexity  |
+------------------------------------+------------------------------+--------------------+
| Pair sum equals target             | Single-Pass Complement Map   | O(N) Time, O(N) Space ⚡|
| Subarray sum equals K (Negative OK)| Prefix Sum HashMap           | O(N) Time, O(N) Space ⚡|
| Group anagrams together            | Canonical Frequency Key Map  | O(N*L) Time, O(N*L) Space⚡|
| Longest consecutive sequence       | HashSet Sequence Start Filter| O(N) Time, O(N) Space ⚡|
| Isomorphic strings / Word pattern  | Bijective Dual Map / Array   | O(N) Time, O(1) Space ⚡|
| Design LRU Cache with O(1) ops     | LinkedHashMap Access-Order   | O(1) Time, O(N) Space ⚡|
+------------------------------------+------------------------------+--------------------+
```

---

## 3. Internal Working Mechanics
Pattern Selection Flowchart:

```
                    [ HASH TABLE PROBLEM STATEMENT ]
                                  |
            +---------------------+---------------------+
            |                                           |
   [ Range / Array Queries ]                  [ String / State Queries ]
            |                                           |
   +--------+--------+                         +--------+--------+
   |                 |                         |                 |
[Pair Target]   [Subarray Sum]             [Grouping]       [Bijective Match]
   |                 |                         |                 |
(Complement Map) (Prefix Sum Map)         (Canonical Key)   (Dual Maps / Array)
```

---

## 4. Visual Diagram
Summary of Key Hash Table Idioms & Templates:

```
[ PATTERN 1: SINGLE-PASS COMPLEMENT ]
int comp = target - nums[i];
if (map.containsKey(comp)) return new int[]{map.get(comp), i};
map.put(nums[i], i);

[ PATTERN 2: PREFIX SUM COMPLEMENT ]
map.put(0, 1);
runningSum += num;
if (map.containsKey(runningSum - k)) count += map.get(runningSum - k);
map.put(runningSum, map.getOrDefault(runningSum, 0) + 1);

[ PATTERN 4: SET BOUNDARY SCAN ]
if (!set.contains(num - 1)) {
    while (set.contains(curr + 1)) { curr++; streak++; }
}
```

---

## 5. Operations & Complete Java Code Templates
Master Code Templates for all 6 Hash Table Patterns:

```java
import java.util.*;

public class HashTablePatternRecognitionMaster {

    // Pattern 1: Single-Pass Complement Map (LeetCode 1)
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) return new int[]{map.get(comp), i};
            map.put(nums[i], i);
        }
        return new int[0];
    }

    // Pattern 2: Prefix Sum HashMap (LeetCode 560)
    public static int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        int sum = 0, count = 0;
        for (int n : nums) {
            sum += n;
            if (map.containsKey(sum - k)) count += map.get(sum - k);
            map.put(sum, map.getOrDefault(sum, 0) + 1);
        }
        return count;
    }

    // Pattern 3: Canonical Frequency Key (LeetCode 49)
    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) count[c - 'a']++;
            StringBuilder sb = new StringBuilder();
            for (int c : count) sb.append('#').append(c);
            String key = sb.toString();
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }

    // Pattern 4: Set Boundary Scan (LeetCode 128)
    public static int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int n : nums) set.add(n);
        int maxLen = 0;
        for (int num : set) {
            if (!set.contains(num - 1)) {
                int curr = num, streak = 1;
                while (set.contains(curr + 1)) { curr++; streak++; }
                maxLen = Math.max(maxLen, streak);
            }
        }
        return maxLen;
    }

    // Pattern 5: Bijective Last-Seen Array (LeetCode 205)
    public static boolean isIsomorphic(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] sSeen = new int[256], tSeen = new int[256];
        for (int i = 0; i < s.length(); i++) {
            if (sSeen[s.charAt(i)] != tSeen[t.charAt(i)]) return false;
            sSeen[s.charAt(i)] = i + 1;
            tSeen[t.charAt(i)] = i + 1;
        }
        return true;
    }

    // Pattern 6: Access-Order LinkedHashMap LRU (LeetCode 146)
    public static class LRUCache<K, V> extends LinkedHashMap<K, V> {
        private final int cap;
        public LRUCache(int cap) { super(cap, 0.75f, true); this.cap = cap; }
        @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() > cap;
        }
    }
}
```

---

## 6. Java Code Demonstration & Dry Run
Demonstration executing pattern selection across representative problems:

```java
public class HashTablePatternDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Two Sum Complement ===");
        System.out.println("Two Sum [2,7,11,15] target 9: " + 
            Arrays.toString(HashTablePatternRecognitionMaster.twoSum(new int[]{2, 7, 11, 15}, 9)));

        System.out.println("\n=== 2. Testing Prefix Sum HashMap ===");
        System.out.println("Subarray Sum [1,1,1] K=2: " + 
            HashTablePatternRecognitionMaster.subarraySum(new int[]{1, 1, 1}, 2));

        System.out.println("\n=== 3. Testing Set Boundary Scan ===");
        System.out.println("Longest Consecutive [100,4,200,1,3,2]: " + 
            HashTablePatternRecognitionMaster.longestConsecutive(new int[]{100, 4, 200, 1, 3, 2}));
    }
}
```

---

## 7. Complexity Analysis

| Pattern | Time Complexity | Auxiliary Space | Optimal Indicator |
| :--- | :--- | :--- | :--- |
| **Single-Pass Complement** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Check BEFORE `put()` |
| **Prefix Sum HashMap** | **$O(N)$ Linear ⚡** | $O(N)$ Space | `map.put(0, 1)` base rule |
| **Canonical Frequency Key** | **$O(N \cdot L)$ Linear ⚡**| $O(N \cdot L)$ Space | `#` delimiters formatted key |
| **Set Boundary Filter** | **$O(N)$ Linear ⚡** | $O(N)$ Space | `!set.contains(n - 1)` start filter |
| **Bijective Last-Seen** | **$O(N)$ Linear ⚡** | **$O(1)$ Space ⚡**| `sSeen[s[i]] == tSeen[t[i]]` |
| **LinkedHashMap LRU** | **Strict $O(1)$ ⚡** | $O(\text{Cap})$ Space | `accessOrder = true` |

---

## 8. Edge Cases & Trap Summary
* **Trap 1: Self-Pairing Bug**: Using two-pass complement map without checking `map.get(comp) != i`. Fixed by single-pass check-first logic.
* **Trap 2: Missing Base Prefix `map.put(0, 1)`**: Misses all valid subarrays starting at index 0!
* **Trap 3: Sliding Window on Negative Numbers**: Fails on non-monotonic sums. Must use Prefix Sum HashMap.
* **Trap 4: Missing Delimiters in Frequency Keys**: Causes false collisions between `[1, 11]` and `[11, 1]`. Use `#`.
* **Trap 5: Expanding Non-Start Set Sequences**: Expanding from every set element degrades to $O(N^2)$. Use `!contains(n-1)`.

---

## 9. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASH TABLE PROBLEM PATTERNS                           |
+-----------------------------------------------------------------------+
| 1. Complement: Check map.containsKey(target - nums[i]) BEFORE put()   |
| 2. Prefix Sum: ALWAYS initialize map.put(0, 1)! Target = P[j] - K     |
| 3. Anagram Grouping: Use StringBuilder with '#' delimiter for freq key|
| 4. Consecutive Sequence: Filter with (!set.contains(num - 1))         |
| 5. Isomorphic: Enforce bidirectional 1-to-1 match (sSeen[s] == tSeen[t])|
| 6. LRU Cache: LinkedHashMap(cap, 0.75f, true) + removeEldestEntry()   |
+-----------------------------------------------------------------------+
```

---

## 10. Practice Checklist
- [ ] I can match any hash-related interview question to its core pattern within 30 seconds.
- [ ] I know why single-pass complement lookup prevents self-pairing bugs.
- [ ] I always initialize `map.put(0, 1)` for prefix sum subarray counting.
- [ ] I use `#` delimiters in canonical frequency key strings.
- [ ] I can write the `!set.contains(num - 1)` sequence boundary filter.
- [ ] I know how to implement an LRU cache using `LinkedHashMap`.
