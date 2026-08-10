# 14. Tree DP: Subtree Aggregations, Post-Order Traversals & Path Optimization

## 1. Introduction
**Tree Dynamic Programming** extends dynamic programming state transitions to hierarchical tree structures $T = (V, E)$. Because a tree with $N$ nodes has no cycles and contains exactly $N - 1$ edges, every node $u$ defines a unique **Subtree $T_u$ Rooted at $u$**. Tree DP operates via **Post-Order Bottom-Up Traversal (DFS)**: a parent node $u$ aggregates DP state vectors returned by its children $v \in \text{children}(u)$ to form its own optimal subtree state $DP[u]$. Key benchmark problems include **House Robber III (LeetCode 337)** (Non-adjacent node choice via `[rob_u, skip_u]` pairs), **Binary Tree Maximum Path Sum (LeetCode 124)** (Path passing through $u$ vs straight branch returning to parent), **Diameter of Binary Tree (LeetCode 543)**, and **Binary Tree Cameras (LeetCode 968)**. Tree DP executes in **$O(N)$ Strict Linear Time Complexity** and **$O(H)$ Auxiliary Space** (where $H$ is tree height).

> **Important:** Core Structural Invariants of Tree DP:
> 1. **Post-Order Traversal Invariant**:
>    - Subtree DP states for all children $v \in \text{children}(u)$ MUST be fully computed BEFORE computing state $DP[u]$ for parent $u$.
> 2. **State Tuple Return Pattern (`[option1, option2]`)**:
>    - Functions return an array/tuple representing choices at node $u$ (e.g. `int[] {rob_u, skip_u}`).
> 3. **House Robber III State Recurrence (LeetCode 337)**:
>    - If node $u$ is ROBBED: Children CANNOT be robbed.
>      $$\text{rob}_u = u.\text{val} + \text{skip}_{\text{left}} + \text{skip}_{\text{right}}$$
>    - If node $u$ is SKIPPED: Children can either be robbed or skipped!
>      $$\text{skip}_u = \max(\text{rob}_{\text{left}}, \text{skip}_{\text{left}}) + \max(\text{rob}_{\text{right}}, \text{skip}_{\text{right}})$$
> 4. **Max Path Sum Branch vs Arch Rule (LeetCode 124)**:
>    - **Arch Path through $u$** (cannot be extended to parent): $u.\text{val} + \max(0, \text{left}) + \max(0, \text{right})$ $\to$ Updates Global Max!
>    - **Single Branch returned to parent**: $u.\text{val} + \max(0, \max(\text{left}, \text{right}))$ $\to$ Returned value! ⚡

```
Tree DP Post-Order Aggregation Topology (House Robber III):

                   [ Node u (val = 3) ]
                     /              \
         Left Child (v1)          Right Child (v2)
          [rob=4, skip=2]          [rob=5, skip=1]

Parent Calculation:
- Rob Node u  = val + skip_v1 + skip_v2 = 3 + 2 + 1 = 6
- Skip Node u = max(rob_v1, skip_v1) + max(rob_v2, skip_v2) = max(4,2) + max(5,1) = 4 + 5 = 9!

Returns [rob_u=6, skip_u=9] to grandparent in O(N) Linear Time! ⚡
```

---

## 2. Core Concepts & Tree DP Strategy Matrix

### 2.1 Tree DP Strategy Matrix
```
Tree DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | State Tuple Return| Branch Return Value| Global Update Value| Space Complexity |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **House Robber III**  | `[rob_u, skip_u]` | State Pair Array  | $\max(\text{rob}, \text{skip})$| **$O(H)$ Stack ⚡**|
| **Max Path Sum (124)**| Max Single Branch | $v + \max(L, R)$  | $v + \max(0,L) + \max(0,R)$| **$O(H)$ Stack ⚡**|
| **Tree Diameter (543)**| Depth $1 + \max(L, R)$| Depth to Parent | $L + R$ Depth Sum | **$O(H)$ Stack ⚡**|
| **Tree Cameras (968)**| State $0, 1, 2$   | Camera Status     | Increment Camera Count| **$O(H)$ Stack ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"House Robber III returns [rob, skip]; Max Path Sum returns single branch to parent, but updates global max with Arch (val + left + right)!"**

---

## 3. Characteristics & Max Path Sum Mathematical Proof

### 3.1 Mathematical Derivation of LeetCode 124 (Binary Tree Max Path Sum)
* A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. Path can start and end at ANY node.
* Let $u$ be the highest node (LCA arch) of a candidate path.
* **Two Distinct Path Configurations at Node $u$**:
  1. **Subtree Arch Path through $u$**:
     Path starts in left subtree, ascends to $u$, and descends into right subtree.
     $$\text{ArchSum}(u) = u.\text{val} + \max(0, \text{Gain}_{\text{left}}) + \max(0, \text{Gain}_{\text{right}})$$
     This path cannot be extended further up to $u$'s parent! It updates `globalMax`.
  2. **Extendable Single Branch Path to Parent**:
     Path starts in either left or right subtree and extends UP through $u$ to $u$'s parent.
     $$\text{BranchGain}(u) = u.\text{val} + \max(0, \, \max(\text{Gain}_{\text{left}}, \text{Gain}_{\text{right}}))$$
     This single branch value is returned by the DFS function to $u$'s parent!
* Post-Order DFS evaluates every node as potential Arch LCA in **$O(N)$ Time and $O(H)$ Space**! ⚡

---

## 4. Internal Working Mechanics: Binary Tree Cameras State Machine

Tracing LeetCode 968 (Binary Tree Cameras):

```
State Definitions returned by Subtree DFS:
- State 0: Node HAS NO CAMERA and is NOT COVERED by any camera. (Needs parent camera!)
- State 1: Node HAS A CAMERA installed.
- State 2: Node HAS NO CAMERA, but IS COVERED by child's camera.

Greedy Tree DP State Machine Transitions at Parent u:
1. If ANY child is in State 0 (Uncovered):
   - Parent u MUST install a camera! Set cameras++, Return State 1! ⚡
2. If ANY child is in State 1 (Has Camera):
   - Parent u is covered by child's camera! Return State 2! ⚡
3. Else (All children in State 2 - Covered without cameras):
   - Parent u is currently uncovered. Return State 0! (Defer camera to grandparent!) ⚡

Solves Minimum Cameras in O(N) Linear Time! ✅ ⚡
```

---

## 5. Visual Diagram: Arch Path vs Single Branch Path

```
Tree Node u Path Bifurcation (LeetCode 124):

                    [ Parent Node ]
                          │
                   Single Branch Path (Returned to Parent!)
                          │
                          ▼
                  [ Arch LCA Node u ]
                     /           \
                    /             \
        Left Subtree               Right Subtree
       (Gain_left)                  (Gain_right)

Arch Path Sum = u.val + max(0, Gain_left) + max(0, Gain_right) ──► Updates Global Max! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing House Robber III (LeetCode 337), Binary Tree Maximum Path Sum (LeetCode 124), Diameter of Binary Tree (LeetCode 543), and Binary Tree Cameras (LeetCode 968).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Tree Dynamic Programming Algorithms:
 * House Robber III, Binary Tree Max Path Sum, Tree Diameter, and Tree Cameras.
 */
public class TreeDPProblemsMaster {

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

    // =========================================================================
    // 1. LEETCODE 337: HOUSE ROBBER III (O(N) Time, O(H) Space)
    // =========================================================================
    /**
     * Calculates maximum loot from binary tree without robbing adjacent nodes.
     *
     * @param root root of binary tree
     * @return maximum loot amount
     */
    public int robTree(TreeNode root) {
        int[] res = robTreeDFS(root);
        return Math.max(res[0], res[1]); // max(rob_root, skip_root) ⚡
    }

    /**
     * Post-Order DFS returning int[] {rob_u, skip_u}.
     */
    private int[] robTreeDFS(TreeNode u) {
        if (u == null) return new int[]{0, 0};

        int[] left = robTreeDFS(u.left);   // [rob_left, skip_left]
        int[] right = robTreeDFS(u.right); // [rob_right, skip_right]

        // Option A: Rob current node u (Children CANNOT be robbed!)
        int robU = u.val + left[1] + right[1];

        // Option B: Skip current node u (Children CAN be robbed or skipped!)
        int skipU = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);

        return new int[]{robU, skipU};
    }

    // =========================================================================
    // 2. LEETCODE 124: BINARY TREE MAXIMUM PATH SUM (O(N) Time, O(H) Space)
    // =========================================================================
    private int maxPathSumGlobal = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        maxPathSumGlobal = Integer.MIN_VALUE;
        maxPathSumDFS(root);
        return maxPathSumGlobal;
    }

    private int maxPathSumDFS(TreeNode u) {
        if (u == null) return 0;

        // Post-order subtree gains (ignore negative gains)
        int leftGain = Math.max(0, maxPathSumDFS(u.left));
        int rightGain = Math.max(0, maxPathSumDFS(u.right));

        // Arch path passing through u as LCA
        int currentArchSum = u.val + leftGain + rightGain;
        maxPathSumGlobal = Math.max(maxPathSumGlobal, currentArchSum); // Global update! ⚡

        // Single branch gain returned to parent
        return u.val + Math.max(leftGain, rightGain);
    }

    // =========================================================================
    // 3. LEETCODE 543: DIAMETER OF BINARY TREE (O(N) Time, O(H) Space)
    // =========================================================================
    private int maxDiameterGlobal = 0;

    public int diameterOfBinaryTree(TreeNode root) {
        maxDiameterGlobal = 0;
        diameterDFS(root);
        return maxDiameterGlobal;
    }

    private int diameterDFS(TreeNode u) {
        if (u == null) return 0;

        int leftDepth = diameterDFS(u.left);
        int rightDepth = diameterDFS(u.right);

        maxDiameterGlobal = Math.max(maxDiameterGlobal, leftDepth + rightDepth);
        return 1 + Math.max(leftDepth, rightDepth);
    }

    // =========================================================================
    // 4. LEETCODE 968: BINARY TREE CAMERAS (O(N) Time, O(H) Space)
    // =========================================================================
    private int cameraCount = 0;

    public int minCameraCover(TreeNode root) {
        cameraCount = 0;
        // If root is left uncovered (State 0), root MUST install a camera!
        if (cameraDFS(root) == 0) {
            cameraCount++;
        }
        return cameraCount;
    }

    /**
     * Return States:
     * 0: Uncovered (Needs camera)
     * 1: Has Camera
     * 2: Covered (No camera)
     */
    private int cameraDFS(TreeNode u) {
        if (u == null) return 2; // Null nodes are covered!

        int leftState = cameraDFS(u.left);
        int rightState = cameraDFS(u.right);

        if (leftState == 0 || rightState == 0) {
            cameraCount++;
            return 1; // Install camera! ⚡
        }

        if (leftState == 1 || rightState == 1) {
            return 2; // Covered by child camera!
        }

        return 0; // Uncovered
    }
}
```

> **Quick Syntax:**
```java
// House Robber III Post-Order Line
int robU = u.val + left[1] + right[1]; int skipU = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 337 - House Robber III**:
   - Non-adjacent node robbing benchmark ($O(N)$ time, `[rob, skip]` tuple).

2. **LeetCode 124 - Binary Tree Maximum Path Sum**:
   - Tree path optimization benchmark ($O(N)$ time).

3. **LeetCode 968 - Binary Tree Cameras**:
   - Minimum vertex cover tree state machine ($O(N)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class TreeDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   TREE DYNAMIC PROGRAMMING BENCHMARK DEMO       ");
        System.out.println("=================================================\n");

        TreeDPProblemsMaster master = new TreeDPProblemsMaster();

        // Build Test Tree: [3, 2, 3, null, 3, null, 1]
        TreeDPProblemsMaster.TreeNode root = new TreeDPProblemsMaster.TreeNode(
            3,
            new TreeDPProblemsMaster.TreeNode(2, null, new TreeDPProblemsMaster.TreeNode(3)),
            new TreeDPProblemsMaster.TreeNode(3, null, new TreeDPProblemsMaster.TreeNode(1))
        );

        // 1. House Robber III Test
        int maxLoot = master.robTree(root);
        System.out.println("1. LeetCode 337 House Robber III for Test Tree:");
        System.out.println("   Max Loot (Post-Order Tree DP): " + maxLoot + " Loot (Optimal = 7)");
        System.out.println("-------------------------------------------------");

        // 2. Max Path Sum Test (LeetCode 124)
        int maxPath = master.maxPathSum(root);
        System.out.println("2. LeetCode 124 Binary Tree Max Path Sum:");
        System.out.println("   Max Path Sum (Arch vs Branch): " + maxPath);
        System.out.println("-------------------------------------------------");

        // 3. Tree Diameter Test (LeetCode 543)
        int diameter = master.diameterOfBinaryTree(root);
        System.out.println("3. LeetCode 543 Diameter of Binary Tree:");
        System.out.println("   Tree Diameter: " + diameter + " Edges");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Tree DP Problem | Time Complexity | Auxiliary Stack Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **House Robber III (337)**| $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(H)}$ Stack ⚡| `[rob_u, skip_u]` tuple return |
| **Max Path Sum (124)**  | $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(H)}$ Stack ⚡| Arch path vs Single branch |
| **Tree Diameter (543)** | $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(H)}$ Stack ⚡| $L + R$ depth sum |
| **Tree Cameras (968)**  | $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(H)}$ Stack ⚡| State machine $0, 1, 2$ |

---

## 10. Edge Cases & Boundary Handling

1. **All Negative Node Values in Max Path Sum (`root.val = -3`)**:
   - `Math.max(0, gain)` ignores negative subtrees, returning `-3` correctly.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Returning Arch Path Sum to Parent in Max Path Sum**:
  - Returning `u.val + leftGain + rightGain` to parent forms an invalid branching tree path (a node cannot connect to two children AND a parent simultaneously). ALWAYS return `u.val + max(leftGain, rightGain)` to parent!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Tree DP Execution Model:
> Tree DP MUST execute in **Post-Order Traversal** (Left, Right, Node) so that child subtree states are fully resolved before evaluating parent node $u$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Sequence DP | Tree DP |
| :--- | :--- | :--- |
| **State Dependencies** | Linear ($i-1, i-2$) | Hierarchical Subtrees ($v \in \text{children}$) |
| **Traversal Order** | Iterative Loop ($0 \dots N$) | **Post-Order DFS (Bottom-Up) ⚡** |
| **Time Complexity** | $O(N)$ Linear | **$O(N)$ Strict Linear ⚡** |

---

## 14. How to Recognize This in Questions

* **"Maximize profit picking non-adjacent nodes in binary tree"** $\rightarrow$ LeetCode 337 (House Robber III).
* **"Find maximum path sum between any two nodes in binary tree"** $\rightarrow$ LeetCode 124.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does House Robber III return an array `int[] {rob, skip}`?**  
  *A:* To pass two DP subproblem choices back to the parent in a single $O(1)$ post-order return, eliminating redundant tree traversals.

* **Q: What is the difference between an Arch Path and a Single Branch Path in LeetCode 124?**  
  *A:* An Arch Path ($u.\text{val} + \text{left} + \text{right}$) bridges left and right subtrees through $u$ and updates global max; a Single Branch ($u.\text{val} + \max(\text{left}, \text{right})$) extends upward to $u$'s parent.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE DP                                               |
+-----------------------------------------------------------------------+
| • Traversal Invariant: MUST use Post-Order DFS (Bottom-Up from leaves)|
| • House Robber III   : Return [rob, skip] -> rob = val + skipL + skipR|
| • Max Path Sum 124   : Global max = val + max(0,L) + max(0,R)          |
| • Branch Return 124  : Return val + max(0, max(L, R)) to parent!       |
| • Performance        : O(N) Strict Linear Time | O(H) Stack Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 337 (`House Robber III`) in $O(N)$ time in Java.
- [ ] I can write LeetCode 124 (`Binary Tree Maximum Path Sum`).
- [ ] I can write LeetCode 543 (`Diameter of Binary Tree`).
- [ ] I can write LeetCode 968 (`Binary Tree Cameras`) using state machine DFS.
- [ ] I can explain why Max Path Sum returns a single branch to its parent.
