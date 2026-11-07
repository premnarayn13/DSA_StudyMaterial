# 15. Hashing Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly matching problem statements to optimal Hashing design patterns during a technical coding interview enables solving complex search, sequence, and system partition problems in **$O(1)$ Average Constant Time** or **$O(N)$ Linear Time**. Hashing problems resolve into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal data structure strategies, along with copy-paste production Java templates.

> **Important:** Master the primary selection rules:
> 1. **Prefix Sum + HashMap**: Use for sub-array sum, divisibility, or zero-one balance queries.
> 2. **Frequency Array / Map**: Use for character counts, anagrams, and top K frequencies.
> 3. **HashSet Boundary Exploration**: Use for longest consecutive sequence queries.
> 4. **Canonical Key Formatting**: Use for grouping anagrams or isomorphic pattern matching.

---

## 2. Master Hashing Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER HASHING PROBLEM DECISION MATRIX                                                            |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Find number of sub-arrays with sum equal to K"   | Prefix Sum + HashMap  | `map.containsKey(s-K)`|
| "Find top K most frequent elements in O(N) time"  | Frequency Bucket Sort | Bucket index = freq   |
| "Find longest consecutive sequence in O(N) time"  | HashSet Boundary      | `!set.contains(n - 1)`|
| "Group words that are anagrams of each other"     | Canonical Key HashMap | Frequency key `#1#0#2`|
| "Check if string P pattern matches string S 1-to-1"| Bijective Dual Mapping| Dual Map / Array index|
| "Slide string window for sub-pattern matching"    | Rolling Hash (Rabin)  | $O(1)$ Hash Update    |
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Subarray Sum Equals K Template
* **Signal**: Finding continuous sub-array count with sum $K$ or divisible by $K$ (560, 974).

```java
public static int subarraySumTemplate(int[] nums, int k) {
    Map<Integer, Integer> prefixMap = new HashMap<>();
    prefixMap.put(0, 1); // Base sentinel
    int currSum = 0, count = 0;

    for (int num : nums) {
        currSum += num;
        if (prefixMap.containsKey(currSum - k)) {
            count += prefixMap.get(currSum - k);
        }
        prefixMap.put(currSum, prefixMap.getOrDefault(currSum, 0) + 1);
    }
    return count;
}
```

---

## 4. Pattern 2: Top K Frequency Bucket Sort Template
* **Signal**: Finding $K$ most frequent elements in $O(N)$ linear time (347).

```java
@SuppressWarnings("unchecked")
public static int[] topKFrequentTemplate(int[] nums, int k) {
    Map<Integer, Integer> freqMap = new HashMap<>();
    for (int num : nums) freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);

    int n = nums.length;
    List<Integer>[] buckets = new List[n + 1];
    for (int key : freqMap.keySet()) {
        int freq = freqMap.get(key);
        if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
        buckets[freq].add(key);
    }

    int[] result = new int[k]; int p = 0;
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
```

---

## 5. Pattern 3: Longest Consecutive Sequence Template
* **Signal**: Finding longest consecutive numbers sequence in $O(N)$ time (128).

```java
public static int longestConsecutiveTemplate(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) set.add(num);

    int maxLen = 0;
    for (int num : set) {
        if (!set.contains(num - 1)) { // Sequence Start Check!
            int curr = num, streak = 1;
            while (set.contains(curr + 1)) { curr++; streak++; }
            maxLen = Math.max(maxLen, streak);
        }
    }
    return maxLen;
}
```

---

## 6. Pattern 4: Group Anagrams Canonical Key Template
* **Signal**: Grouping anagram strings in $O(N \cdot K)$ time (49).

```java
public static List<List<String>> groupAnagramsTemplate(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) count[c - 'a']++;
        StringBuilder sb = new StringBuilder();
        for (int c : count) sb.append('#').append(c);
        String key = sb.toString();
        map.putIfAbsent(key, new ArrayList<>());
        map.get(key).add(s);
    }
    return new ArrayList<>(map.values());
}
```

---

## 7. Pattern 5: Bijective Mapping Template
* **Signal**: 1-to-1 character or word pattern matching (205, 290).

```java
public static boolean isIsomorphicTemplate(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] mapS = new int[256], mapT = new int[256];
    for (int i = 0; i < s.length(); i++) {
        if (mapS[s.charAt(i)] != mapT[t.charAt(i)]) return false;
        mapS[s.charAt(i)] = i + 1; // 1-based index marker
        mapT[t.charAt(i)] = i + 1;
    }
    return true;
}
```

---

## 8. Pattern 6: Rolling Hash Template
* **Signal**: Substring pattern matching in $O(N)$ time (28, 187).

```java
public static int strStrRollingHashTemplate(String haystack, String needle) {
    int n = haystack.length(), m = needle.length();
    if (m > n) return -1;
    long P = 31, M = 1_000_000_007L, power = 1;
    for (int i = 0; i < m - 1; i++) power = (power * P) % M;

    long tHash = 0, wHash = 0;
    for (int i = 0; i < m; i++) {
        tHash = (tHash * P + needle.charAt(i)) % M;
        wHash = (wHash * P + haystack.charAt(i)) % M;
    }
    if (wHash == tHash && haystack.substring(0, m).equals(needle)) return 0;

    for (int i = 1; i <= n - m; i++) {
        long out = (haystack.charAt(i - 1) * power) % M;
        wHash = (wHash - out + M) % M;
        wHash = (wHash * P + haystack.charAt(i + m - 1)) % M;
        if (wHash == tHash && haystack.substring(i, i + m).equals(needle)) return i;
    }
    return -1;
}
```

---

## 9. Edge Case & Trap Checklist
* **Base Sentinel in Prefix Sum**: Always initialize `prefixMap.put(0, 1)`.
* **Delimiters in Canonical Keys**: Always add `#` between frequency counts.
* **Negative Modulo Normalization**: Always add `+ K` before modulo: `((currSum % K) + K) % K`.
* **Pre-sizing HashMaps**: Pre-size HashMaps with `(expectedEntries / 0.75f) + 1`.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: HASHING PATTERN RECOGNITION                          |
+-----------------------------------------------------------------------+
| 1. Subarray Sum Equals K (560): prefixMap.put(0, 1) base sentinel     |
| 2. Top K Bucket Sort (347): Bucket index = frequency; scan N down to 1|
| 3. Consecutive Sequence (128): Explore ONLY if !set.contains(num - 1) |
| 4. Group Anagrams (49): Frequency string key "#1#0#2" with '#' delim  |
| 5. Bijective Isomorphic (205): Compare last seen 1-based index arrays |
| 6. Rolling Hash (28): H_new = (((H - out*P^(L-1)) % M + M)%M * P + in)%M|
| 7. Pre-sizing Rule: initialCapacity = (expectedItems / 0.75f) + 1     |
| 8. Java 8 Rehash Rule: (hash & oldCap) == 0 splits low/high bins      |
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why `prefixMap.put(0, 1)` base sentinel is required.
- [ ] I know how `(hash & oldCap) == 0` determines new bucket index.
- [ ] I can explain why Bucket Sort achieves $O(N)$ time for Top K elements.
