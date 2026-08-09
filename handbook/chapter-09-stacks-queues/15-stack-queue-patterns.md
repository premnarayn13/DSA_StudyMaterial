# 15. Stack & Queue Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly matching problem statements to optimal Stack and Queue design patterns during a technical coding interview enables solving complex sequence, range, and cache problems in **$O(N)$ linear time**. Stack and Queue problems resolve into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal data structure strategies, along with copy-paste production Java templates.

> **Important:** Master the primary selection rules:
> 1. **Monotonic Stack (Decreasing/Increasing)**: Use for Next/Previous Greater/Smaller element range queries.
> 2. **Monotonic Queue (Double-Ended)**: Use for Sliding Window Max/Min queries.
> 3. **Index Sentinel Stack**: Use for Histogram areas and parenthesis substring length bounds.
> 4. **LRU Cache Hybrid**: Use HashMap + Doubly LinkedList for $O(1)$ read/write/eviction caches.

---

## 2. Master Stack & Queue Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER STACK & QUEUE PROBLEM DECISION MATRIX                                                      |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Find next greater / smaller element to right"    | Monotonic Stack (R-L) | `while(peek()<=v)pop()`|
| "Find max/min element in sliding window size K"   | Monotonic Queue       | Deque storing indices |
| "Find largest rectangle area in 1D histogram"     | Histogram Index Stack | Virtual sentinel height 0|
| "Check valid nested brackets / evaluate math expr"| LIFO Matching Stack   | Push expected closing |
| "Design cache with O(1) get, put, and eviction"   | LRU Cache Hybrid      | HashMap + Doubly List |
| "Implement FIFO Queue using 2 Stacks"             | Dual-Stack Lazy Move  | Transfer on out.empty()|
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Monotonic Stack (Next Greater Element) Template
* **Signal**: Finding nearest greater element to the right (739, 496, 503).

```java
public static int[] nextGreaterElementTemplate(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = n - 1; i >= 0; i--) {
        while (!stack.isEmpty() && stack.peek() <= nums[i]) {
            stack.pop();
        }
        result[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(nums[i]);
    }

    return result;
}
```

---

## 4. Pattern 2: Monotonic Queue (Sliding Window Max) Template
* **Signal**: Finding max/min element in every sliding window of size $K$ (239).

```java
public static int[] maxSlidingWindowTemplate(int[] nums, int k) {
    int n = nums.length, p = 0;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>();

    for (int right = 0; right < n; right++) {
        if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) deque.pollFirst();
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) deque.pollLast();
        deque.offerLast(right);
        if (right >= k - 1) result[p++] = nums[deque.peekFirst()];
    }

    return result;
}
```

---

## 5. Pattern 3: Largest Rectangle Histogram Area Template
* **Signal**: Largest rectangle area in 1D histogram or 2D binary matrix (84, 85).

```java
public static int largestRectangleAreaTemplate(int[] heights) {
    int n = heights.length, maxArea = 0;
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i <= n; i++) {
        int currH = (i == n) ? 0 : heights[i];
        while (!stack.isEmpty() && heights[stack.peek()] >= currH) {
            int h = heights[stack.pop()];
            int w = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, h * w);
        }
        stack.push(i);
    }

    return maxArea;
}
```

---

## 6. Pattern 4: Valid Parentheses Match Template
* **Signal**: Matching nested brackets and parentheses strings (20).

```java
public static boolean isValidParenthesesTemplate(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(') stack.push(')');
        else if (c == '{') stack.push('}');
        else if (c == '[') stack.push(']');
        else if (stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}
```

---

## 7. Pattern 5: LRU Cache Hybrid Template
* **Signal**: $O(1)$ read, write, and least recently used eviction cache (146).

```java
public static class LRUCacheTemplate {
    private static class Node { int k, v; Node prev, next; Node(int k, int v) { this.k = k; this.v = v; } }
    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(-1, -1), tail = new Node(-1, -1);

    public LRUCacheTemplate(int cap) { this.cap = cap; head.next = tail; tail.prev = head; }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node n = map.get(key); remove(n); addHead(n); return n.v;
    }

    public void put(int key, int val) {
        if (map.containsKey(key)) { Node n = map.get(key); n.v = val; remove(n); addHead(n); }
        else {
            if (map.size() == cap) { Node lru = tail.prev; remove(lru); map.remove(lru.k); }
            Node n = new Node(key, val); addHead(n); map.put(key, n);
        }
    }
    private void addHead(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }
    private void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
}
```

---

## 8. Pattern 6: Dual-Stack Queue Adaptation Template
* **Signal**: Building a FIFO Queue using LIFO Stacks (232).

```java
public static class QueueViaStacksTemplate {
    private final Deque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();

    public void push(int x) { in.push(x); }
    public int pop() { transfer(); return out.pop(); }
    public int peek() { transfer(); return out.peek(); }
    public boolean empty() { return in.isEmpty() && out.isEmpty(); }
    private void transfer() { if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop()); }
}
```

---

## 9. Edge Case & Trap Checklist
* **Virtual Sentinel Height 0 at Index $N$ in Histogram**: Always flush remaining stack elements at $i = N$.
* **Negative Modulo in Circular Deque**: Always add `+ capacity` before modulo when moving backward.
* **`java.util.Stack` Anti-Pattern**: Never use legacy `java.util.Stack`. Always use `ArrayDeque`.
* **LRU Sentinel Nodes**: Always use dummy `head` and `tail` nodes to eliminate null checks.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: STACK & QUEUE PATTERN RECOGNITION                    |
+-----------------------------------------------------------------------+
| 1. Monotonic Stack (NGE): Right-to-Left pass; purge stack.peek() <= val|
| 2. Monotonic Queue (Max): Deque storing indices; max at peekFirst()   |
| 3. Histogram Area (84): Monotonic increasing stack; w = i - peek() - 1|
| 4. Parentheses Match (20): Push expected closing bracket directly!     |
| 5. LRU Cache (146): HashMap + Doubly LinkedList with dummy sentinels  |
| 6. Queue via 2 Stacks (232): Transfer inStack to outStack when empty  |
| 7. Min Stack (155): Push onto minStack if val <= minStack.peek()      |
| 8. Circular Deque (641): front = (front - 1 + capacity) % capacity    |
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why `ArrayDeque` is superior to `java.util.Stack`.
- [ ] I know how dummy sentinels simplify LRU Cache implementation.
- [ ] I can write Monotonic Stack Next Greater Element (LeetCode 739).
