# 02. Coloring Rules, The 5 Structural Invariants & Black-Height Proofs

## 1. Introduction
The self-balancing guarantee of a **Red-Black Tree** is governed by **5 Strict Coloring Rules (Structural Invariants)**. By ensuring that no path contains consecutive RED nodes and that every path from root to leaf contains the exact same number of BLACK nodes, these 5 rules guarantee that the longest simple path from root to leaf is **at most twice as long as the shortest simple path**.

> **Important:** The 5 Canonical Invariant Rules of Red-Black Trees:
> 1. **Rule 1 (Node Color Rule)**: Every node is either **RED** or **BLACK**.
> 2. **Rule 2 (Root Color Rule)**: The **ROOT NODE IS ALWAYS BLACK**.
> 3. **Rule 3 (Leaf Color Rule)**: Every leaf node (**NIL / null**) is **BLACK**.
> 4. **Rule 4 (No Consecutive Red Rule / Red Property)**: If a node is **RED**, both of its children **MUST BE BLACK** (No double-RED parent-child pair allowed!).
> 5. **Rule 5 (Black-Height Uniformity Rule / Black Property)**: For each node, **EVERY simple path from that node to descendant NIL leaves contains the EXACT SAME NUMBER of BLACK nodes**! ⚡

```
Red-Black Tree 5-Rule Structural Invariant Spectrum:
                     [ 20 (BLACK) ]  <--- Rule 2: Root is BLACK!
                    /              \
        [ 10 (RED) ]                [ 30 (BLACK) ]
       /            \              /              \
[ NIL (BLACK) ] [ NIL (BLACK) ] [ NIL (BLACK) ] [ NIL (BLACK) ]  <--- Rule 3: NIL is BLACK!

Path 20 -> 10 -> NIL: Black Count = 2 (20 B, NIL B).
Path 20 -> 30 -> NIL: Black Count = 2 (20 B, 30 B). -> Rule 5 Satisfied! ⚡
```

---

## 2. Core Concepts & Maximum Height Bound Proof ($H \le 2 \log_2(N + 1)$)

### 2.1 Why the 5 Rules Limit Height to $H \le 2 \log_2(N + 1)$
Let $bh(X)$ be the **Black-Height** of node $X$ (the number of black nodes on any path from $X$ to a descendant NIL leaf, excluding $X$):
1. **Shortest Path**: Consists of ONLY Black nodes $\implies \text{Length} = bh(\text{root})$.
2. **Longest Path**: Alternates between Black and Red nodes (due to Rule 4: No double Red nodes!) $\implies \text{Length} \le 2 \cdot bh(\text{root})$.
3. Therefore: $\text{Longest Path} \le 2 \times \text{Shortest Path}$!

#### Mathematical Induction Proof:
* A subtree rooted at node $X$ contains at least $2^{bh(X)} - 1$ internal nodes.
* For a tree of height $H$, the black height $bh(\text{root}) \ge H / 2$.
* Thus: $N \ge 2^{H/2} - 1 \implies N + 1 \ge 2^{H/2}$.
* Taking base-2 logarithms: $\log_2(N + 1) \ge H / 2 \implies \mathbf{H \le 2 \log_2(N + 1)}$! ⚡

```
Rule Verification Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Rule Name             | Invariant Requirement| Violation Trigger | Recovery Action   |
+-----------------------+-------------------+-------------------+-------------------+
| **Rule 2: Root**      | Root MUST be BLACK| Insertion recolors| Set `root.color = BLACK`|
| **Rule 4: Red Rule**  | Red parent -> Black kids| RED node inserted under RED parent| Recolor uncle OR Rotate|
| **Rule 5: Black-Height**| Equal black count | Deletion removes black node| Double-Black balance|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Red-Black Rules: Root is Black! NIL is Black! No Double RED! Equal Black-Height on all paths!"**

---

## 3. Characteristics & Double-RED Violation Scenarios

### 3.1 Resolving Rule 4 Violations (Double-RED Conflicts)
When a new RED node is inserted under a RED parent:
* **Uncle is RED**: Recolor Parent and Uncle to BLACK, recolor Grandparent to RED! (Push violation up).
* **Uncle is BLACK**: Perform Rotation (Single or Double) and Recolor Parent/Grandparent! (Fixes violation locally in $O(1)$ time).

---

## 4. Internal Working Mechanics
Tracing Full 5-Rule Verification on an Arbitrary Binary Search Tree:

```
Check Tree: Root 10 (RED). Left 5 (BLACK). Right 15 (RED, right=20 RED).

1. Rule 1 Check: All nodes RED or BLACK -> PASS.
2. Rule 2 Check: Root 10 is RED -> VIOLATION of Rule 2! (Fix: color 10 BLACK).
3. Rule 3 Check: NIL leaves are BLACK -> PASS.
4. Rule 4 Check: Node 15 is RED, right child 20 is RED -> VIOLATION of Rule 4! (Double-RED conflict!).
5. Rule 5 Check: Left path black count = 2 (10, 5). Right path black count = 1 (10). -> VIOLATION of Rule 5!

Tree fails 3 of 5 rules! Must execute recoloring and rotations! ❌
```

---

## 5. Visual Diagram
Double-RED Violation vs Recolored State Topography:

```
Double-RED Violation (Rule 4 Fail):          Recolored Valid State:
        [ Grandparent (BLACK) ]                    [ Grandparent (RED) ]
       /                       \                  /                     \
  [ Parent (RED) ]         [ Uncle (RED) ]   [ Parent (BLACK) ]    [ Uncle (BLACK) ]
     /                                          /
[ New (RED) ] <--- Violation!             [ New (RED) ] <--- Valid!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a comprehensive 5-Rule Red-Black Tree Invariant Verifier:

```java
import java.util.*;

public class RBColoringRulesMaster {

    public static final boolean RED = false;
    public static final boolean BLACK = true;

    public static class RBNode {
        public int val;
        public boolean color;
        public RBNode left;
        public RBNode right;
        public RBNode parent;

        public RBNode(int val, boolean color) {
            this.val = val;
            this.color = color;
        }
    }

    public static boolean getColor(RBNode node) {
        return (node == null) ? BLACK : node.color;
    }

    // Full 5-Rule Verification Engine O(N) Time
    public static boolean verifyAllRules(RBNode root) {
        if (root == null) return true;

        // Rule 2 Verification: Root MUST be BLACK
        if (getColor(root) != BLACK) {
            System.err.println("Rule 2 Violation: Root is RED!");
            return false;
        }

        // Verify Rule 4 (No Double RED) and Rule 5 (Equal Black Height)
        return verifySubtreeRules(root) && verifyBlackHeight(root) != -1;
    }

    // Verify Rule 4: No Consecutive RED Nodes
    private static boolean verifySubtreeRules(RBNode node) {
        if (node == null) return true;

        // Rule 4 Check: If node is RED, both children MUST be BLACK
        if (node.color == RED) {
            if (getColor(node.left) == RED || getColor(node.right) == RED) {
                System.err.println("Rule 4 Violation: Double RED at Node " + node.val);
                return false;
            }
        }

        return verifySubtreeRules(node.left) && verifySubtreeRules(node.right);
    }

    // Verify Rule 5: Uniform Black Height Across All Paths
    private static int verifyBlackHeight(RBNode node) {
        if (node == null) return 1; // NIL leaf counts as 1 BLACK node

        int leftBH = verifyBlackHeight(node.left);
        if (leftBH == -1) return -1;

        int rightBH = verifyBlackHeight(node.right);
        if (rightBH == -1) return -1;

        if (leftBH != rightBH) {
            System.err.println("Rule 5 Violation: Mismatched Black Height at Node " + node.val);
            return -1;
        }

        return leftBH + (node.color == BLACK ? 1 : 0);
    }
}
```

> **Quick Syntax:**
```java
// Rule 4 Check Line
if (node.color == RED && (getColor(node.left) == RED || getColor(node.right) == RED)) return false;
```

---

## 7. Concrete Problem Examples
* **Red-Black Tree Invariant Audit**: Validating custom RB-Tree implementations.
* **LeetCode 110 Variant**: Checking black-height balance invariants.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing 5-Rule Verification across valid and invalid Red-Black trees:

```java
public class RBColoringRulesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black 5-Rule Verification Test ===");
        // Build Valid Tree:
        //       20 (BLACK)
        //      /          \
        //   10 (RED)     30 (BLACK)
        RBColoringRulesMaster.RBNode root = 
            new RBColoringRulesMaster.RBNode(20, RBColoringRulesMaster.BLACK);
        root.left = new RBColoringRulesMaster.RBNode(10, RBColoringRulesMaster.RED);
        root.right = new RBColoringRulesMaster.RBNode(30, RBColoringRulesMaster.BLACK);

        System.out.println("Is Valid Red-Black Tree? " + 
            RBColoringRulesMaster.verifyAllRules(root)); // Output: true ✅

        System.out.println("\n=== 2. Testing Rule 4 Violation (Double RED) ===");
        root.left.left = new RBColoringRulesMaster.RBNode(5, RBColoringRulesMaster.RED); // Double RED!

        System.out.println("Is Valid After Adding Red Child under Red 10? " + 
            RBColoringRulesMaster.verifyAllRules(root)); // Output: false (Rule 4 Violation!)
    }
}
```

---

## 9. Complexity Analysis

| Rule Verification | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Rule 2 (Root Black)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | Single boolean check |
| **Rule 4 (No Double RED)**| **$O(N)$ Linear ⚡** | $O(H)$ Call Stack Space | Full DFS traversal |
| **Rule 5 (Black Height)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack Space | Post-order path check |

---

## 10. Edge Cases & Boundary Handling
* **Empty Tree (`root == null`)**: Returns `true` (valid empty RB-tree).
* **Single Node Tree**: Must be BLACK (Rule 2), satisfies all 5 rules.

---

## 11. Common Mistakes & Anti-Patterns
* **Allowing Root to Remain RED**:
  - Forgetting to explicitly enforce `root.color = BLACK` after insertion/recoloring violates Rule 2.
  - **Always execute `root.color = BLACK` at the end of insertion**.
* **Counting RED Nodes in Black Height**:
  - Black height counts ONLY BLACK nodes (including NIL leaves).
  - **NEVER count RED nodes when calculating black height**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The Core Structural Result of the 5 Rules:
> Because Rule 4 prevents two RED nodes from being adjacent, the maximum possible path consists of alternating BLACK and RED nodes.
> Because Rule 5 forces every path to have the EXACT SAME number of BLACK nodes ($bh$), the longest path can be at most $2 \times bh$, and the shortest path is $bh$.
> This guarantees that no path is more than twice as long as any other path, ensuring **$H \le 2 \log_2(N + 1)$**!

> **Memory Trick:** **"Longest path <= 2 * Shortest path because RED nodes cannot be adjacent!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Tree Rules | AVL Tree Rules |
| :--- | :--- | :--- |
| **Primary Invariant Metric**| 5 Color Rules (No double RED, Equal BH) | Balance Factor $|\text{BF}| \le 1$ |
| **Height Bound** | $H \le 2.0 \log_2 N$ | **$H \le 1.44 \log_2 N$ (Tighter) ⚡**|
| **Structural Enforcement** | Recolor + At most 2-3 Rotations | Height update + Rotations |

---

## 14. How to Recognize This in Questions
* **"Verify if binary search tree obeys Red-Black color properties"** $\rightarrow$ Check all 5 coloring rules.

---

## 15. Frequently Asked Interview Questions
* **Q: What are the 5 rules of a Red-Black Tree?**  
  *A:* 1. Node is Red/Black. 2. Root is Black. 3. NIL leaves are Black. 4. No double Red nodes. 5. Equal black height on all paths.
* **Q: Why does inserting a new node as RED minimize invariant violations?**  
  *A:* Inserting a RED node preserves Rule 5 (Black-Height invariant) completely, risking ONLY Rule 4 (Double-RED conflict), which is easy to resolve via local recoloring or rotation.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: THE 5 RED-BLACK COLORING RULES                        |
+-----------------------------------------------------------------------+
| • Rule 1: Every node is either RED or BLACK                           |
| • Rule 2: Root is ALWAYS BLACK                                        |
| • Rule 3: NIL leaves are ALWAYS BLACK                                 |
| • Rule 4: RED nodes MUST have BLACK children (No Double RED!)         |
| • Rule 5: EVERY path to NIL leaves has the EXACT SAME Black-Height    |
| • Height Bound: H <= 2 log2(N + 1) (Longest path <= 2 * Shortest path) |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can list all 5 Red-Black tree coloring rules from memory.
- [ ] I can write the 5-rule verifier in Java in $O(N)$ time.
- [ ] I can prove why height $H \le 2 \log_2(N + 1)$.
- [ ] I know why new nodes are inserted as RED.
- [ ] I can state why NIL leaves are always BLACK.
