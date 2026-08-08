# 08. Binary Tree Path Problems: Root-to-Leaf, Any-to-Any & Maximum Path Sum

## 1. Introduction
Solving path problems on Binary Trees is one of the highest-yield problem domains in technical coding interviews. Path problems range from **Root-to-Leaf Path Sums (LeetCode 112, 113)**, **Subpath Sum Equals K (LeetCode 437)** using Prefix Sum Hash Maps, to **Any-Node to Any-Node Maximum Path Sum (LeetCode 124)**. These problems evaluate recursive state tracking, backtracking, post-order subtree contribution return values, and global variable optimization.

> **Important:** In Binary Tree Maximum Path Sum (LeetCode 124), a node's recursive function returns the **Maximum Single-Branch Path Sum** (`val + max(leftBranch, rightBranch)`), while updating a global maximum with the **Full Arch Path Sum** (`val + leftBranch + rightBranch`)!

```
Tree Path Types Spectrum:
+-----------------------------------------------------------------------------------+
| Root-to-Leaf Path   : Must start at Root and terminate at a Leaf node (112, 113)  |
| Downward Subpath    : Begins at any node, moves downward to any descendant (437)  |
| Any-to-Any Path     : Connects any two nodes along parent-child edges (124) ⚡    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Patterns

### 2.1 Pattern 1: Root-to-Leaf Backtracking (LeetCode 113)
* **Goal**: Find all root-to-leaf paths where node values sum to `targetSum`.
* **Mechanism**: Top-Down DFS with Backtracking.
  - Maintain `currentPath` list.
  - At node `curr`: `currentPath.add(curr.val)`.
  - If `curr` is a **Leaf Node** (`left == null && right == null`) and `targetSum == curr.val`:
    - Add a copy of `currentPath` to `result`: `result.add(new ArrayList<>(currentPath))`.
  - Recurse left and right with `targetSum - curr.val`.
  - **Backtrack**: `currentPath.remove(currentPath.size() - 1)`.

### 2.2 Pattern 2: Downward Subpath Prefix Sum HashMap (LeetCode 437)
* **Goal**: Find number of downward paths summing to `targetSum` starting and ending at any nodes.
* **Mechanism**: Prefix Sum Hash Map on Trees (Adapted from Array Subarray Sum Equals K!).
  - Maintain `runningSum` and `prefixMap<Long, Integer>`.
  - Search `complement = runningSum - targetSum` in `prefixMap`.
  - Recurse left and right.
  - **Backtrack**: Decrement `prefixMap.put(runningSum, prefixMap.get(runningSum) - 1)` before returning!

### 2.3 Pattern 3: Any-to-Any Maximum Path Sum (LeetCode 124)
* **Goal**: Find maximum path sum connecting ANY two nodes in the tree.
* **Mechanism**: Post-Order Bottom-Up DFS.
  - At node `curr`:
    - `leftMax = Math.max(0, maxGain(curr.left))` (Prune negative contributions with `Math.max(0, ...)`!).
    - `rightMax = Math.max(0, maxGain(curr.right))`.
    - **Arch Path Sum through `curr`**: `priceNewPath = curr.val + leftMax + rightMax`.
    - Update global maximum: `maxSum = Math.max(maxSum, priceNewPath)`.
    - **Return to Parent**: Return single branch max contribution `curr.val + Math.max(leftMax, rightMax)`.

```
Path Return vs Global Update Paradox (LeetCode 124):
                       ( Node X )
                      /          \
            [ Left Branch ]   [ Right Branch ]

Arch Path (Global Max Update)  : Left Branch + Node X + Right Branch  (Cannot extend up!)
Single Branch (Returned Value) : Node X + max(Left Branch, Right Branch) (Extends to Parent!)
```

> **Memory Trick:** **"LeetCode 124: Prune negative subtrees with Math.max(0, gain)! Global update = val + left + right; Return to parent = val + max(left, right)!"**

---

## 3. Characteristics & Problem Variations

```
Tree Path Problem Patterns Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Path Constraint   | Traversal Pattern | Key Return / State|
+-----------------------+-------------------+-------------------+-------------------+
| Path Sum I (112)      | Root to Leaf      | Top-Down DFS      | `boolean` match   |
| Path Sum II (113)     | Root to Leaf      | DFS + Backtrack   | `List<List<Int>>` |
| Path Sum III (437)    | Downward Subpath  | Prefix Sum Map    | `prefixMap.put(0,1)`|
| Max Path Sum (124)    | Any-to-Any        | Post-Order DFS    | `val + max(L, R)` |
| Longest Univalue (687)| Same Value Nodes  | Post-Order DFS    | `max(L_len, R_len)`|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Binary Tree Maximum Path Sum (LeetCode 124) on `[-10, 9, 20, null, null, 15, 7]`:

```
          ( -10 )
         /       \
       ( 9 )     ( 20 )
                /      \
              ( 15 )   ( 7 )

1. Leaf Node 9: left=0, right=0. Arch = 9. Max = 9. Return to parent: 9.
2. Leaf Node 15: Arch = 15. Max = 15. Return: 15.
3. Leaf Node 7: Arch = 7. Max = 15. Return: 7.
4. Node 20: leftGain = 15, rightGain = 7.
   - Arch Path through 20 = 20 + 15 + 7 = 42. Update global Max = 42.
   - Return to parent (-10) = 20 + max(15, 7) = 35.
5. Root Node -10: leftGain = 9, rightGain = 35.
   - Arch Path through -10 = -10 + 9 + 35 = 34.
   - Global Max remains 42!

Result: Max Path Sum = 42 (Path: 15 -> 20 -> 7) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Maximum Path Sum Arch vs Single Branch Path Topology:

```
                  ( -10 )
                 /       \
               ( 9 )     ( 20 )  <-- Node 20
                        /      \
                      ( 15 )   ( 7 )

Global Arch Path (42) : [15] ---> (20) ---> [7]   (Cannot be extended to -10!)
Returned Branch (35)  : (20) ---> [15]            (Passed to -10 to build larger paths!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Path Sum II (LeetCode 113), Path Sum III (LeetCode 437), Maximum Path Sum (LeetCode 124), and Longest Univalue Path (LeetCode 687):

```java
import java.util.*;

public class TreePathMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Path Sum II (LeetCode 113) O(N) Time, O(H) Space
    public static List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentPath = new ArrayList<>();
        pathSumHelper(root, targetSum, currentPath, result);
        return result;
    }

    private static void pathSumHelper(TreeNode node, int targetSum, 
                                     List<Integer> currentPath, List<List<Integer>> result) {
        if (node == null) return;

        currentPath.add(node.val);

        // Check if Root-to-Leaf path sum matches
        if (node.left == null && node.right == null && targetSum == node.val) {
            result.add(new ArrayList<>(currentPath));
        } else {
            pathSumHelper(node.left, targetSum - node.val, currentPath, result);
            pathSumHelper(node.right, targetSum - node.val, currentPath, result);
        }

        // Backtrack
        currentPath.remove(currentPath.size() - 1);
    }

    // 2. Path Sum III (LeetCode 437) O(N) Time, O(H) Space - Prefix Sum Map
    public static int pathSumIII(TreeNode root, int targetSum) {
        Map<Long, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0L, 1); // Base Rule: Empty path sum 0
        return prefixSumDFS(root, 0L, targetSum, prefixMap);
    }

    private static int prefixSumDFS(TreeNode node, long runningSum, int targetSum, 
                                    Map<Long, Integer> prefixMap) {
        if (node == null) return 0;

        runningSum += node.val;
        int count = prefixMap.getOrDefault(runningSum - targetSum, 0);

        prefixMap.put(runningSum, prefixMap.getOrDefault(runningSum, 0) + 1);

        count += prefixSumDFS(node.left, runningSum, targetSum, prefixMap);
        count += prefixSumDFS(node.right, runningSum, targetSum, prefixMap);

        // Backtrack: Remove running sum count before returning up call stack
        prefixMap.put(runningSum, prefixMap.get(runningSum) - 1);

        return count;
    }

    // 3. Binary Tree Maximum Path Sum (LeetCode 124) O(N) Time, O(H) Space
    private static int maxPathSumGlobal = Integer.MIN_VALUE;

    public static int maxPathSum(TreeNode root) {
        maxPathSumGlobal = Integer.MIN_VALUE;
        maxGain(root);
        return maxPathSumGlobal;
    }

    private static int maxGain(TreeNode node) {
        if (node == null) return 0;

        // Prune negative branch contributions using Math.max(0, ...)
        int leftGain = Math.max(0, maxGain(node.left));
        int rightGain = Math.max(0, maxGain(node.right));

        // Arch Path Sum through current node
        int archPathSum = node.val + leftGain + rightGain;

        // Update global maximum path sum
        maxPathSumGlobal = Math.max(maxPathSumGlobal, archPathSum);

        // Return max single-branch gain extending to parent
        return node.val + Math.max(leftGain, rightGain);
    }

    // 4. Longest Univalue Path (LeetCode 687) O(N) Time, O(H) Space
    private static int maxUnivaluePathGlobal = 0;

    public static int longestUnivaluePath(TreeNode root) {
        maxUnivaluePathGlobal = 0;
        univalueDFS(root);
        return maxUnivaluePathGlobal;
    }

    private static int univalueDFS(TreeNode node) {
        if (node == null) return 0;

        int left = univalueDFS(node.left);
        int right = univalueDFS(node.right);

        int leftPath = 0, rightPath = 0;

        if (node.left != null && node.left.val == node.val) {
            leftPath = left + 1;
        }
        if (node.right != null && node.right.val == node.val) {
            rightPath = right + 1;
        }

        maxUnivaluePathGlobal = Math.max(maxUnivaluePathGlobal, leftPath + rightPath);

        return Math.max(leftPath, rightPath);
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 124 Max Gain Subtree Return Formula
int leftGain = Math.max(0, maxGain(node.left));
int rightGain = Math.max(0, maxGain(node.right));
maxSum = Math.max(maxSum, node.val + leftGain + rightGain);
return node.val + Math.max(leftGain, rightGain);
```

---

## 7. Concrete Problem Examples
* **LeetCode 113 - Path Sum II**: Root-to-leaf DFS backtracking.
* **LeetCode 437 - Path Sum III**: Prefix sum HashMap on trees.
* **LeetCode 124 - Binary Tree Maximum Path Sum**: Any-to-any post-order DFS.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Path Sum II, Path Sum III, and Maximum Path Sum:

```java
public class TreePathDemo {

    public static void main(String[] args) {
        // Build Tree: [-10, 9, 20, null, null, 15, 7]
        TreePathMaster.TreeNode root = new TreePathMaster.TreeNode(-10);
        root.left = new TreePathMaster.TreeNode(9);
        root.right = new TreePathMaster.TreeNode(20);
        root.right.left = new TreePathMaster.TreeNode(15);
        root.right.right = new TreePathMaster.TreeNode(7);

        System.out.println("=== 1. Binary Tree Maximum Path Sum (LeetCode 124) ===");
        System.out.println("Max Path Sum: " + TreePathMaster.maxPathSum(root)); // Output: 42

        // Build Tree for Path Sum II: [5, 4, 8, 11, null, 13, 4]
        TreePathMaster.TreeNode root2 = new TreePathMaster.TreeNode(5);
        root2.left = new TreePathMaster.TreeNode(4);
        root2.right = new TreePathMaster.TreeNode(8);
        root2.left.left = new TreePathMaster.TreeNode(11);
        root2.right.left = new TreePathMaster.TreeNode(13);
        root2.right.right = new TreePathMaster.TreeNode(4);

        System.out.println("\n=== 2. Path Sum II (Target = 20) ===");
        System.out.println("Paths matching 20: " + TreePathMaster.pathSum(root2, 20));
    }
}
```

---

## 9. Complexity Analysis

| Problem Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Path Sum II (113)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Root-to-Leaf Backtracking |
| **Path Sum III (437)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Prefix Sum HashMap Backtracking |
| **Max Path Sum (124)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Single Branch Return vs Arch Update |

---

## 10. Edge Cases & Boundary Handling
* **All Negative Node Values in Tree (e.g. `root = [-3]`)**:
  - Initializing `maxPathSumGlobal = 0` produces WRONG answer `0`!
  - **Always initialize `maxPathSumGlobal = Integer.MIN_VALUE`**!
  - `Math.max(0, maxGain(...))` ensures negative subtrees return `0` gain to avoid reducing parent sums.
* **Large Node Values Overflowing Integer Range**: In Path Sum III (LeetCode 437), running sums can exceed 32-bit `Integer.MAX_VALUE`. **Use `long` for running sums**!

---

## 11. Common Mistakes & Anti-Patterns
* **Returning Arch Path Sum to Parent in LeetCode 124**:
  - Returning `node.val + leftGain + rightGain` to parent forms an invalid branching path!
  - A valid path can enter a node from one child and leave to the parent, but CANNOT branch to both children AND parent! **Return ONLY single branch gain `node.val + max(left, right)`**.
* **Forgetting to Backtrack Prefix Sum Map in LeetCode 437**:
  - Failing to decrement `prefixMap` on exiting a node allows left subtree prefix sums to pollute right subtree lookup queries!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Returning Value vs Global Update Rule (LeetCode 124):
> * **Global Update**: `maxSum = Math.max(maxSum, node.val + leftGain + rightGain)` (Evaluates full arch path through `node`).
> * **Return Value**: `return node.val + Math.max(leftGain, rightGain)` (Returns maximum single branch extending to parent).

> **Memory Trick:** **"Arch path updates global max; Single branch returns to parent!"**

---

## 13. System & Implementation Comparisons

| Feature | Root-to-Leaf Paths (113) | Subpath Sum (437) | Max Path Sum (124) |
| :--- | :--- | :--- | :--- |
| **Start Node** | Must be Root | Any Node | Any Node |
| **End Node** | Must be Leaf | Any Descendant | Any Node |
| **Mechanism** | Backtracking List | Prefix Sum Map | Post-Order DFS Max Gain |

---

## 14. How to Recognize This in Questions
* **"Find maximum path sum connecting any two nodes in a binary tree"** $\rightarrow$ LeetCode 124 (Post-order DFS with global max update).
* **"Find number of downward paths that sum to target"** $\rightarrow$ LeetCode 437 (Prefix sum HashMap + backtracking).

---

## 15. Frequently Asked Interview Questions
* **Q: Why do we use `Math.max(0, maxGain(child))` in LeetCode 124?**  
  *A:* If a child subtree produces a negative path sum (e.g. `-5`), including it in the path reduces the total sum. `Math.max(0, gain)` prunes negative subtrees by treating their contribution as `0`.
* **Q: Why is backtracking mandatory in Path Sum III (LeetCode 437)?**  
  *A:* Because we are exploring downward paths. When DFS backtracks up from the left subtree to process the right subtree, prefix sums from the left subtree are no longer in the active path. Decrementing the frequency in `prefixMap` removes stale prefix sums.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY TREE PATH PROBLEMS                             |
+-----------------------------------------------------------------------+
| • Path Sum II (113): Root-to-Leaf DFS + Backtracking                  |
| • Path Sum III (437): Prefix Sum HashMap + Backtracking               |
| • Max Path Sum (124): Post-Order DFS with Math.max(0, gain) pruning   |
| • Arch Path Update: maxSum = max(maxSum, val + leftGain + rightGain)  |
| • Subtree Return: return val + max(leftGain, rightGain)               |
| • Integer Overflow Guard: Use long runningSum in Path Sum III         |
| • Complexity: All path algorithms run in O(N) Linear Time             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Path Sum II (LeetCode 113) with list backtracking.
- [ ] I can write Path Sum III (LeetCode 437) with prefix sum map backtracking.
- [ ] I can write Binary Tree Maximum Path Sum (LeetCode 124) in under 5 minutes.
- [ ] I know why `Math.max(0, gain)` prunes negative subtrees.
- [ ] I know the difference between Arch Path Update and Subtree Return Value.
