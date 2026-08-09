# 16. Master Reference — Stacks & Queues

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 9: Stacks & Queues**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh LIFO vs FIFO semantics, ArrayDeque cache locality, Monotonic Stack Next Greater Element rules, Monotonic Queue Sliding Window Max indexing, Histogram width formula $w = i - \text{stack.peek()} - 1$, LRU Cache HashMap + Doubly LinkedList sentinels, Min Stack $2*val - minVal$ encoding, and Circular Deque negative modulo arithmetic!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **LIFO Stack Operational Invariant**: Mutations occur exclusively at Top of Stack (`top`). Time Complexity: $O(1)$ Constant.
* **FIFO Queue Operational Invariant**: Enqueue at Rear (`rear`), Dequeue from Front (`front`). Time Complexity: $O(1)$ Constant.
* **Histogram Area Width Formula (LeetCode 84)**:
  - $w = \text{stack.isEmpty()} ? i : i - \text{stack.peek()} - 1$.
* **Min Stack Difference Encoding Restoration (LeetCode 155)**:
  - Encoded Push (`val < min`): $\text{encoded} = 2 \times \text{val} - \text{min}$; set $\text{min} = \text{val}$.
  - Decoded Pop (`top < min`): Restore $\text{prevMin} = 2 \times \text{min} - \text{top}$.
* **Circular Array Wraparound Equations**:
  - Moving Forward : $\text{idx} = (\text{idx} + 1) \bmod K$
  - Moving Backward: $\text{idx} = (\text{idx} - 1 + K) \bmod K$
  - Power-of-2 Bitwise Masking: $\text{idx} = (\text{idx} + 1) \ \& \ (K - 1)$
* **Dual-Stack Queue Amortized Time**: Transfer `inStack` to `outStack` ONLY when `outStack.isEmpty()`. Each element is moved at most once $\implies O(1)$ Amortized Time!

```
Stacks & Queues Invariants & Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Monotonic Stack (Next Greater)    | Right-to-Left pass; purge stack.peek() <= val     |
| Monotonic Queue (Sliding Max)     | Deque storing INDICES; max at peekFirst()         |
| Histogram Area Calculation        | h = heights[pop()], w = isEmpty() ? i : i-peek()-1|
| Parentheses Closing Push          | If c == '(' stack.push(')'); check pop() == c     |
| Min Stack Dual Strategy           | Push minStack if val <= minStack.peek()           |
| LRU Cache Node Promotion          | removeNode(node) -> addHead(node)                 |
| Circular Deque Front Insert       | front = (front - 1 + capacity) % capacity         |
| Bitwise Masking Ring Buffer       | idx = (idx + 1) & (capacity - 1) for 2^k capacity |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ArrayStack Push/Pop** | **$O(1)$ Amortized ⚡** | **$O(1)$ Amortized ⚡** | $O(N)$ (On Resize) | $O(N)$ Space | Dynamic array resizing ($2\times$) |
| **LinkedListStack Push/Pop**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Heap Nodes | Node pointer re-linking |
| **Circular Array Queue** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Space | Modulo index wrap `(idx+1)%K` |
| **Daily Temperatures (739)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Monotonic stack storing indices |
| **Sliding Window Max (239)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(K)$ Deque Space | Monotonic Deque index storage |
| **Valid Parentheses (20)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Expected closing bracket push |
| **Longest Valid Paren (32)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | `-1` sentinel index stack |
| **Evaluate RPN (150)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Single pass postfix evaluation |
| **Calculator II (227)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Immediate `*` and `/` evaluation |
| **Circular NGE II (503)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Virtual 2N loop with `i % N` |
| **Next Permutation (556)** | **$O(D)$ Linear ⚡** | **$O(D)$ Linear ⚡** | **$O(D)$ Linear ⚡** | $O(D)$ Digit Array | 4-step pivot-successor swap-reverse |
| **Histogram Area (84)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Monotonic increasing index stack |
| **Maximal Rectangle (85)**| **$O(R \cdot C)$ Linear ⚡**| **$O(R \cdot C)$ Linear ⚡**| **$O(R \cdot C)$ Linear ⚡**| $O(C)$ Aux Array | 2D matrix reduction to 1D histogram |
| **Min Stack (155)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Space | Dual stack `minStack.peek()` |
| **Queue via 2 Stacks (232)**| **$O(1)$ Constant ⚡** | **$O(1)$ Amortized ⚡**| $O(N)$ (On Transfer) | $O(N)$ Space | Lazy inStack to outStack transfer |
| **Circular Deque (641)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(K)$ Array Space | 4-boundary modulo wraparound |
| **LRU Cache (146)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(\text{Capacity})$ Space | HashMap + Doubly LinkedList |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Stack and Queue Implementations                              |
+-----------------------------------------------------------------------------------+
| Array-backed Stack/Queue (ArrayDeque) : Contiguous Memory (Best CPU Cache Hit Rate)⚡|
| Node-backed Stack/Queue (LinkedList)  : 24 Bytes Node Header + Pointers per Elem  |
| Dual Stack LRU Cache Hybrid           : 32B Map Entry + 24B Node Header per Elem  |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Production Stack & Queue Creation (Always prefer ArrayDeque!)
Deque<Integer> stack = new ArrayDeque<>();
Queue<Integer> queue = new ArrayDeque<>();

// 2. Monotonic Stack Next Greater Pattern
while (!stack.isEmpty() && arr[stack.peek()] <= arr[i]) stack.pop();
result[i] = stack.isEmpty() ? -1 : stack.peek();
stack.push(i);

// 3. Monotonic Queue Window Max Pattern
if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) deque.pollFirst();
while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) deque.pollLast();
deque.offerLast(right);

// 4. Histogram Area Calculation
int h = heights[stack.pop()];
int w = stack.isEmpty() ? i : i - stack.peek() - 1;
maxArea = Math.max(maxArea, h * w);

// 5. Circular Deque Wraparound
front = (front - 1 + capacity) % capacity; // Insert Front
rear  = (rear - 1 + capacity) % capacity;  // Delete Last
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using Legacy `java.util.Stack`**: `java.util.Stack` is synchronized (adds lock overhead) and inherits from `Vector`. Always use `ArrayDeque`.
* **Pitfall 2: Forgetting Virtual Height 0 at Index $N$ in Histogram**: Leaves elements in stack, missing rectangles extended to the right edge.
* **Pitfall 3: Negative Modulo in Java (`(front - 1) % K`)**: Evaluates to `-1` in Java, throwing index out of bounds. Always add `+ capacity` before modulo: `(front - 1 + capacity) % capacity`.
* **Pitfall 4: Non-Commutative Operand Order in RPN Evaluation**: `b = stack.pop()`, `a = stack.pop()`; result is `a - b` or `a / b` (NOT `b - a`).
* **Pitfall 5: Using `Integer` `==` Comparison in Min Stack**: Values outside `-128 ... 127` cache range fail `==`. Always use `.equals()` or unbox primitives.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 9 (STACKS & QUEUES)              |
+-----------------------------------------------------------------------+
| 1. Operational API: Prefer ArrayDeque over Stack and LinkedList       |
| 2. Monotonic Stack: Next Greater = Right-to-Left, purge <= val        |
| 3. Monotonic Queue: Window Max = Deque storing indices; max at head   |
| 4. Histogram Area: w = stack.isEmpty() ? i : i - stack.peek() - 1     |
| 5. Parentheses Trick: Push expected closing bracket directly          |
| 6. Longest Valid Paren: Push -1 sentinel; validLen = i - stack.peek() |
| 7. RPN Evaluation: b = pop(); a = pop(); calculate a op b             |
| 8. Calculator II: Immediate evaluation for * and / on stack top       |
| 9. Circular NGE II: Virtual 2N loop 2N-1 down to 0 using nums[i % N]  |
| 10. Next Permutation: Pivot (a[i]<a[i+1]) -> Succ (a[j]>a[i]) -> Swap -> Reverse|
| 11. Min Stack: Push minStack if val <= minStack.peek()                |
| 12. Queue via 2 Stacks: Transfer inStack to outStack when empty       |
| 13. Circular Deque: Add +capacity before modulo when moving backward  |
| 14. LRU Cache: HashMap + Doubly LinkedList with dummy sentinels       |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write custom ArrayStack and LinkedListStack implementations.
- [ ] I can write Daily Temperatures (LeetCode 739) using Monotonic Stack.
- [ ] I can write Sliding Window Maximum (LeetCode 239) using Monotonic Queue.
- [ ] I can write Largest Rectangle in Histogram (LeetCode 84) in $O(N)$ time.
- [ ] I can write Maximal Rectangle in 2D Binary Matrix (LeetCode 85).
- [ ] I can write Valid Parentheses (LeetCode 20) in 4 lines.
- [ ] I can write Longest Valid Parentheses (LeetCode 32) using `-1` sentinel stack.
- [ ] I can write Evaluate Reverse Polish Notation (LeetCode 150).
- [ ] I can write Basic Calculator II (LeetCode 227).
- [ ] I can write Next Greater Element II (LeetCode 503) for circular arrays.
- [ ] I can write Next Greater Element III (LeetCode 556) next permutation.
- [ ] I can write Min Stack (LeetCode 155) using Dual Stack Strategy.
- [ ] I can write Implement Queue using Stacks (LeetCode 232).
- [ ] I can write Design Circular Deque (LeetCode 641).
- [ ] I can write LRU Cache (LeetCode 146) from scratch.
- [ ] I can write Task Scheduler (LeetCode 621).
