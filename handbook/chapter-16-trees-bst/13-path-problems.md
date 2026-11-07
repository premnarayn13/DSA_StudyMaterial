# 13. Binary Tree Path Problems, Global Max Traversal & Prefix Sum Trees

## 1. Introduction
**Binary Tree Path Problems** represent a foundational class of tree algorithms where values are accumulated along parent-child paths or arbitrary node-to-node paths. Algorithms like **Binary Tree Maximum Path Sum (LeetCode 124)**, **Path Sum III (LeetCode 437)**, **Path Sum II (LeetCode 113)**, and **Diameter of Binary Tree (LeetCode 543)** solve complex path optimization problems in **$O(N)$ linear time and $O(H)$ auxiliary space** using global variables, prefix sum maps, and backtracking path lists.

> **Important:** In **Binary Tree Maximum Path Sum (LeetCode 124)**, there is a fundamental distinction between what a helper function **RETURNS** vs what it **UPDATES**:
> * **Helper Return Value**: Returns the maximum path sum starting at current node extending down ONE branch (`node.val + max(0, leftGain, rightGain)`), because a path cannot split upward into two branches!
> * **Global Max Update**: Updates global maximum with the local arch sum (`node.val + max(0, leftGain) + max(0, rightGain)`), connecting left and right subtrees through `node`! ⚡

```
Maximum Path Sum Arch vs Single-Branch Extension Topology:
                      [ Current Node (10) ]
                       /                 \
        [ Left Gain (+15) ]           [ Right Gain (+20) ]

Local Arch Sum (Global Max Update) : 10 + 15 + 20 = 45! (Connects Left, Node, Right)
Single Branch Return (Helper Return): 10 + max(15, 20) = 30! (Extends upward to parent!) ⚡
```

---

## 2. Core Concepts & Maximum Path Sum Mechanics (LeetCode 124)

### 2.1 Binary Tree Maximum Path Sum (LeetCode 124)
A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. A node can only appear in the sequence at most once. The path does NOT need to pass through the root!

#### Algorithmic Strategy ($O(N)$ Time, $O(H)$ Space):
1. Maintain global variable `int maxSum = Integer.MIN_VALUE`.
2. Define helper DFS `maxGain(node)`:
   - Base Case: If `node == null`, return `0`.
   - Compute left subtree max gain (clamp negative gains to 0!):
     `leftGain = Math.max(0, maxGain(node.left))`
   - Compute right subtree max gain:
     `rightGain = Math.max(0, maxGain(node.right))`
   - Compute local arch path sum through current node:
     `priceNewPath = node.val + leftGain + rightGain`
   - Update global maximum: `maxSum = Math.max(maxSum, priceNewPath)`.
   - **Return Single Branch Max**: `return node.val + Math.max(leftGain, rightGain)`.
3. Return `maxSum`.

```
Negative Gain Clamping Rule (Math.max(0, gain)):
If a subtree yields a NEGATIVE total gain (e.g. -5), including it in the path reduces total sum!
Clamping negative gains to 0 effectively prunes bad subtrees from the maximum path! ⚡
```

> **Memory Trick:** **"Max Path Sum: Clamp child gains to Math.max(0, gain)! Update global max with arch sum; Return single branch max!"**

---

## 3. Characteristics & Path Sum III Prefix Sum Mapping (LeetCode 437)

### 3.1 Path Sum III (LeetCode 437 - Prefix Sum Map on Trees)
Given a binary tree and `targetSum`, return the number of paths where the sum of values along the path equals `targetSum`. The path does NOT need to start at root or end at leaf, but MUST go downwards!
* **Prefix Sum HashMap Strategy ($O(N)$ Time, $O(H)$ Auxiliary Space)**:
  - Identical to array Subarray Sum Equals K (LeetCode 560)!
  - Maintain `Map<Long, Integer> prefixMap` storing prefix sums down the current DFS path.
  - Base Sentinel: `prefixMap.put(0L, 1)`.
  - **Backtracking Rule**: When returning up from a node's DFS call, decrement its prefix sum frequency in `prefixMap` (`prefixMap.put(currSum, prefixMap.get(currSum) - 1)`), preventing prefix sums from one branch from corrupting parallel branches!

---

## 4. Internal Working Mechanics
Tracing Path Sum II (LeetCode 113 - Root-to-Leaf Path Target) Backtracking:

```
Target Sum = 22. Tree: [5, 4, 8, 11, null, 13, 4, 7, 2]

DFS Path: [5] -> [5, 4] -> [5, 4, 11] -> [5, 4, 11, 7]
  - Leaf 7: Sum = 27 != 22.
  - Backtrack: Remove 7 from path list.

DFS Path: [5, 4, 11] -> [5, 4, 11, 2]
  - Leaf 2: Sum = 22 == 22! MATCH FOUND!
  - Add copy of path [5, 4, 11, 2] to result!
  - Backtrack: Remove 2 from path list.

Backtracking preserves O(H) space for path state! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Diameter of Binary Tree (LeetCode 543) Subtree Height Arch Topography:

```
                  [ Node (1) ]
                 /            \
        Left Height (2)     Right Height (2)
               /                    \
            (Node)                (Node)

Local Arch Diameter at Node 1 = Left Height + Right Height = 2 + 2 = 4 Edges! ⚡
Helper Returns Tree Height    = 1 + max(Left, Right) = 3 Nodes!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Maximum Path Sum (LeetCode 124), Path Sum II (LeetCode 113), Path Sum III (LeetCode 437), and Diameter of Binary Tree (LeetCode 543):

```java
import java.util.*;

public class PathProblemsMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // 1. Binary Tree Maximum Path Sum (LeetCode 124) O(N) Time, O(H) Space
    private static int globalMaxPathSum;

    public static int maxPathSum(TreeNode root) {
        globalMaxPathSum = Integer.MIN_VALUE;
        maxGainDFS(root);
        return globalMaxPathSum;
    }

    private static int maxGainDFS(TreeNode node) {
        if (node == null) return 0;

        // Clamp negative subtree gains to 0
        int leftGain = Math.max(0, maxGainDFS(node.left));
        int rightGain = Math.max(0, maxGainDFS(node.right));

        // Local Arch Sum connecting left, node, and right
        int currentArchSum = node.val + leftGain + rightGain;
        globalMaxPathSum = Math.max(globalMaxPathSum, currentArchSum);

        // Return single branch maximum extending up to parent
        return node.val + Math.max(leftGain, rightGain);
    }

    // 2. Path Sum II Root-to-Leaf Paths (LeetCode 113) O(N) Time, O(H) Space
    public static List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentPath = new ArrayList<>();
        dfsPathSum2(root, targetSum, currentPath, result);
        return result;
    }

    private static void dfsPathSum2(TreeNode node, int remainingSum, List<Integer> currentPath, List<List<Integer>> result) {
        if (node == null) return;

        currentPath.add(node.val);

        // Leaf node check
        if (node.left == null && node.right == null && remainingSum == node.val) {
            result.add(new ArrayList<>(currentPath)); // Record path copy
        } else {
            dfsPathSum2(node.left, remainingSum - node.val, currentPath, result);
            dfsPathSum2(node.right, remainingSum - node.val, currentPath, result);
        }

        currentPath.remove(currentPath.size() - 1); // Backtrack!
    }

    // 3. Path Sum III Prefix Sum Map on Tree (LeetCode 437) O(N) Time, O(H) Space
    public static int pathSum3(TreeNode root, int targetSum) {
        Map<Long, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0L, 1); // Base sentinel
        return dfsPrefixPath(root, 0L, targetSum, prefixMap);
    }

    private static int dfsPrefixPath(TreeNode node, long currentSum, int targetSum, Map<Long, Integer> prefixMap) {
        if (node == null) return 0;

        currentSum += node.val;
        int count = prefixMap.getOrDefault(currentSum - targetSum, 0);

        prefixMap.put(currentSum, prefixMap.getOrDefault(currentSum, 0) + 1);

        count += dfsPrefixPath(node.left, currentSum, targetSum, prefixMap);
        count += dfsPrefixPath(node.right, currentSum, targetSum, prefixMap);

        // Backtrack: Remove prefix sum frequency when exiting subtree!
        prefixMap.put(currentSum, prefixMap.get(currentSum) - 1);

        return count;
    }

    // 4. Diameter of Binary Tree (LeetCode 543) O(N) Time, O(H) Space
    private static int maxDiameter;

    public static int diameterOfBinaryTree(TreeNode root) {
        maxDiameter = 0;
        depthDFS(root);
        return maxDiameter;
    }

    private static int depthDFS(TreeNode node) {
        if (node == null) return 0;

        int leftDepth = depthDFS(node.left);
        int rightDepth = depthDFS(node.right);

        // Diameter is max edge count connecting left and right subtrees
        maxDiameter = Math.max(maxDiameter, leftDepth + rightDepth);

        return 1 + Math.max(leftDepth, rightDepth);
    }
}
```

> **Quick Syntax:**
```java
// Path Sum III Prefix Backtracking Line
prefixMap.put(currSum, prefixMap.get(currSum) - 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 124 - Binary Tree Maximum Path Sum**: Arch sum vs single branch return.
* **LeetCode 437 - Path Sum III**: Prefix sum HashMap on tree with backtracking.
* **LeetCode 543 - Diameter of Binary Tree**: Local height sum diameter.
* **LeetCode 113 - Path Sum II**: Backtracking path list.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Maximum Path Sum and Path Sum III:

```java
public class PathProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Maximum Path Sum (LeetCode 124) ===");
        // Build Tree with negative values:
        //       -10
        //       /  \
        //      9   20
        //         /  \
        //        15   7
        PathProblemsMaster.TreeNode root = new PathProblemsMaster.TreeNode(-10);
        root.left = new PathProblemsMaster.TreeNode(9);
        root.right = new PathProblemsMaster.TreeNode(20, 
            new PathProblemsMaster.TreeNode(15), new PathProblemsMaster.TreeNode(7));

        int maxPath = PathProblemsMaster.maxPathSum(root);
        System.out.println("Max Path Sum: " + maxPath); // Output: 42 (Path: 15 -> 20 -> 7)

        System.out.println("\n=== 2. Diameter of Binary Tree (LeetCode 543) ===");
        int diameter = PathProblemsMaster.diameterOfBinaryTree(root);
        System.out.println("Tree Diameter: " + diameter); // Output: 3 edges (Path: 15 -> 20 -> -10 -> 9) ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Max Path Sum (124)** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Clamp negative gains to 0 |
| **Path Sum II (113)** | **$O(N)$ Linear ⚡** | $O(H)$ Backtrack List| Leaf node target sum match |
| **Path Sum III (437)**| **$O(N)$ Linear ⚡** | $O(H)$ Map Space | Prefix sum HashMap + backtracking |
| **Diameter (543)** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Max `leftDepth + rightDepth` |

---

## 10. Edge Cases & Boundary Handling
* **All Negative Values in Tree (`[-3]` or `[-2, -1]`)**: Handled by initializing `globalMaxPathSum = Integer.MIN_VALUE`; returns `-1`.
* **64-Bit Prefix Sum Overflow in 437**: Using `long currentSum` prevents 32-bit integer overflow on deep trees with large values.

---

## 11. Common Mistakes & Anti-Patterns
* **Returning Arch Sum in Helper Function for LeetCode 124**:
  - Returning `node.val + leftGain + rightGain` up to parent creates an invalid bifurcated path (a path cannot branch into 2 subtrees AND extend to parent!).
  - **Return single branch extension `node.val + Math.max(leftGain, rightGain)`**.
* **Forgetting Prefix Map Backtracking in Path Sum III**:
  - Leaving prefix sum entries in `prefixMap` when exiting a subtree allows path counts from left subtrees to falsely match right subtrees!
  - **Always decrement prefix sum frequency when exiting subtree (`prefixMap.put(sum, count - 1)`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Backtracking is Mandatory for Path Sum III (LeetCode 437):
> Unlike 1D arrays where prefix sums process sequentially, trees branch into left and right subtrees!
> A prefix sum accumulated down the LEFT subtree does NOT exist along paths in the RIGHT subtree!
> Decrementing `prefixMap` frequency when exiting a node's DFS call ensures the map contains ONLY prefix sums along the CURRENT active root-to-node path!

> **Memory Trick:** **"Always decrement prefixMap count when exiting a DFS subtree call!"**

---

## 13. System & Implementation Comparisons

| Feature | Prefix HashMap Path Sum III | Naive Double DFS Path Sum III |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | $O(H)$ Prefix Map Space | **$O(H)$ Stack Space** |
| **Execution Speed** | **Fastest (Single Pass) ⚡** | Slower |

---

## 14. How to Recognize This in Questions
* **"Find maximum path sum where path can start and end at any node"** $\rightarrow$ LeetCode 124 (Clamp negative gains to 0).
* **"Find number of paths that sum to target value going downwards"** $\rightarrow$ LeetCode 437 (Prefix Sum HashMap with backtracking).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `Math.max(0, gain)` clamp subtree gains in LeetCode 124?**  
  *A:* If a subtree yields a negative sum (e.g. -10), incorporating it into the path sum would reduce the overall total. Clamping negative gains to 0 simulates choosing NOT to extend the path into that negative subtree.
* **Q: What is the difference between Tree Height and Tree Diameter?**  
  *A:* Height is the maximum node depth from root to leaf. Diameter is the maximum edge count between ANY two leaf nodes in the tree (which may or may not pass through the root).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY TREE PATH PROBLEMS                             |
+-----------------------------------------------------------------------+
| • Max Path Sum (124): Clamp child gains with Math.max(0, gain)        |
| • Local Arch Sum    : node.val + leftGain + rightGain (Update global) |
| • Single Branch Return: node.val + Math.max(leftGain, rightGain)      |
| • Path Sum III (437): Prefix map + backtrack (decrement sum on exit!) |
| • Tree Diameter(543): Global max of (leftDepth + rightDepth)          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Binary Tree Maximum Path Sum (LeetCode 124).
- [ ] I can write Path Sum III (LeetCode 437) in $O(N)$ time with prefix map.
- [ ] I can write Diameter of Binary Tree (LeetCode 543).
- [ ] I know why single branch max must be returned to parent in 124.
- [ ] I know why prefix map backtracking is mandatory in 437.
