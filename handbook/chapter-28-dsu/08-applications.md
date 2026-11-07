# 08. System Applications: Network Connectivity, Social Graphs & Accounts Merge

## 1. Introduction
**Disjoint Set Union (DSU)** powers modern cloud networking infrastructure, social media graph analytics, computer vision image segmentation engines, and user data deduplication systems. From **Cloud VPC Network Connectivity Monitors** (checking whether microservice pods can communicate in $O(1)$ time) to **Social Network Friend Circle Engines**, **Computer Vision Connected Component Labeling**, and **Accounts Merge (LeetCode 721 - Identity Resolution)**, DSU provides deterministic, sub-millisecond execution across distributed platforms.

> **Important:** Core Industrial DSU Application Domains:
> 1. **Accounts Merge / Identity Resolution (LeetCode 721)**: Merges user accounts that share at least one email address. Emails are mapped to a DSU, grouping all linked emails into common component accounts in **$O(N \log N)$ Time**!
> 2. **Network Connectivity & Cloud VPC Routing**: Dynamic link state updates (cable additions/breakages) and reachability tests (`connected(podA, podB)`) executed in **$\alpha(N) \approx O(1)$ Constant Time**! ⚡

```
Accounts Merge Identity Resolution Topology (LeetCode 721):
User Account 1: ["John", "john1@mail.com", "john2@mail.com"]
User Account 2: ["John", "john2@mail.com", "john3@mail.com"]  <--- Shared Email "john2@mail.com"!

DSU Merges Component:
       ("john1@mail.com") <--- Root
           /          \
  ("john2@mail.com")  ("john3@mail.com")

All 3 emails merged into 1 single unified John account! ⚡
```

---

## 2. Core Concepts & LeetCode 721 Accounts Merge Engine

### 2.1 LeetCode 721 Accounts Merge Algorithm
Given a list of `accounts` where `account[0]` is a name and remaining elements are emails:
1. Map each unique email `String` to an integer ID using `Map<String, Integer> emailToId`.
2. Map each email ID to the account owner name `emailToName`.
3. For each account:
   - First email `firstEmail = account[1]`.
   - For all subsequent emails `email` in account:
     - `dsu.union(firstEmail, email)` (Connects all emails in the same account!).
4. Group emails by component root: `Map<Integer, List<String>> components`.
5. Sort emails in each component list lexicographically and prepend the account name to produce result!

```
DSU System Application Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Production System     | Set Element       | Merge Trigger     | Performance Goal  |
+-----------------------+-------------------+-------------------+-------------------+
| **Accounts Merge (721)**| User Email String | Shared Email Match| **$O(N \log N)$ Deduplication ⚡**|
| **Cloud VPC Router**  | Network Pod / IP  | Active Cable Link | **$\alpha(N) \approx O(1)$ Reachability ⚡**|
| **Image Segmentation**| Pixel Intensity   | Adjacent Similar  | **$O(Pixels)$ Labeling ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Accounts Merge: Connect all emails in an account to the first email! DSU automatically merges shared accounts!"**

---

## 3. Characteristics & Computer Vision Connected Component Labeling

### 3.1 Computer Vision Image Component Labeling
In digital image processing (e.g. medical MRI analysis or autonomous vehicle object detection):
* Binary image pixels ($0$ for background, $1$ for object).
* DSU unions adjacent 8-connected foreground pixels in **$O(\text{Pixels})$ Time**.
* Instantly counts and extracts total distinct physical objects in the image! ⚡

---

## 4. Internal Working Mechanics
Tracing Accounts Merge for `Account 1: [John, a@mail, b@mail]` and `Account 2: [John, b@mail, c@mail]`:

```
Step 1: Process Account 1:
- First email: a@mail. Next email: b@mail.
- union("a@mail", "b@mail") -> Component: {a@mail, b@mail}.

Step 2: Process Account 2:
- First email: b@mail. Next email: c@mail.
- union("b@mail", "c@mail") -> Component: {a@mail, b@mail, c@mail}.

Step 3: Group & Sort:
- Root find("a@mail") = Root find("b@mail") = Root find("c@mail").
- Collected emails: ["a@mail", "b@mail", "c@mail"].
- Prepend "John": ["John", "a@mail", "b@mail", "c@mail"].

Merged 2 accounts into 1 deduplicated profile! ✅
```

---

## 5. Visual Diagram
Accounts Merge Identity Resolution Topography:

```
Account 1 Emails: (a@mail) ---- (b@mail)
                                   |
Account 2 Emails:               (c@mail)
                                   |
               Merged Component Root: (a@mail)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 721 (Accounts Merge using DSU identity resolution):

```java
import java.util.*;

// LeetCode 721: Accounts Merge Master
public class DSUApplicationsMaster {

    private static class DSU {
        private final int[] parent;

        public DSU(int n) {
            this.parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX != rootY) {
                parent[rootY] = rootX;
            }
        }
    }

    // LeetCode 721 Solution O(N log N) Time, O(N) Space
    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        Map<String, Integer> emailToId = new HashMap<>();
        Map<String, String> emailToName = new HashMap<>();
        int emailCount = 0;

        // Step 1: Assign unique integer IDs to all emails
        for (List<String> account : accounts) {
            String name = account.get(0);
            for (int i = 1; i < account.size(); i++) {
                String email = account.get(i);
                if (!emailToId.containsKey(email)) {
                    emailToId.put(email, emailCount++);
                    emailToName.put(email, name);
                }
            }
        }

        DSU dsu = new DSU(emailCount);

        // Step 2: Union all emails in the same account to the first email
        for (List<String> account : accounts) {
            String firstEmail = account.get(1);
            int firstId = emailToId.get(firstEmail);

            for (int i = 2; i < account.size(); i++) {
                String nextEmail = account.get(i);
                int nextId = emailToId.get(nextEmail);
                dsu.union(firstId, nextId); // Merge emails into same set
            }
        }

        // Step 3: Group emails by their component root ID
        Map<Integer, List<String>> rootToEmails = new HashMap<>();
        for (String email : emailToId.keySet()) {
            int rootId = dsu.find(emailToId.get(email));
            rootToEmails.putIfAbsent(rootId, new ArrayList<>());
            rootToEmails.get(rootId).add(email);
        }

        // Step 4: Sort emails in each component & build final result list
        List<List<String>> mergedAccounts = new ArrayList<>();
        for (List<String> emails : rootToEmails.values()) {
            Collections.sort(emails); // Lexicographical sort
            String name = emailToName.get(emails.get(0));

            List<String> mergedAccount = new ArrayList<>();
            mergedAccount.add(name); // Prepend name
            mergedAccount.addAll(emails);
            mergedAccounts.add(mergedAccount);
        }

        return mergedAccounts;
    }
}
```

> **Quick Syntax:**
```java
// Accounts Merge Primary Loop Line
for (int i = 2; i < account.size(); i++) dsu.union(firstId, emailToId.get(account.get(i)));
```

---

## 7. Concrete Problem Examples
* **LeetCode 721 - Accounts Merge**: Core identity resolution problem.
* **Network Pod Connectivity**: Reachability testing in distributed systems.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 721 `accountsMerge`:

```java
public class DSUApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 721 Accounts Merge Test ===");
        DSUApplicationsMaster solver = new DSUApplicationsMaster();

        List<List<String>> accounts = Arrays.asList(
            Arrays.asList("John", "johnsmith@mail.com", "john_newyork@mail.com"),
            Arrays.asList("John", "johnsmith@mail.com", "john00@mail.com"),
            Arrays.asList("Mary", "mary@mail.com"),
            Arrays.asList("John", "johnnybravo@mail.com")
        );

        List<List<String>> merged = solver.accountsMerge(accounts);

        System.out.println("Merged Accounts:");
        for (List<String> acc : merged) {
            System.out.println(acc);
        }
        // Output:
        // [John, john00@mail.com, john_newyork@mail.com, johnsmith@mail.com]
        // [Mary, mary@mail.com]
        // [John, johnnybravo@mail.com] ✅
    }
}
```

---

## 9. Complexity Analysis

| Production System | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Accounts Merge (721)**| **$O(N \log N)$ Sorting ⚡**| **$O(N)$ Hash Map Space**| DSU email union + email sort |
| **Network Reachability**| **$\alpha(V) \approx O(1)$ Instant ⚡**| **$O(V)$ DSU Array** | Dynamic cable edge additions |

---

## 10. Edge Cases & Boundary Handling
* **Accounts with Same Name but No Shared Emails**: Kept cleanly as separate disconnected accounts.
* **Single Email Accounts**: Handled safely, returning account as-is.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Account Names as DSU Keys**:
  - Multiple distinct people can share the same name (e.g. two different people named `"John"`).
  - **NEVER use names as DSU keys; map unique EMAILS to DSU keys instead**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Accounts Merge Uses Emails as DSU Keys:
> An email address is a globally unique identifier (UUID) belonging to 1 physical entity. Names are non-unique string labels.
> By performing `union()` on email IDs, DSU correctly links accounts that share emails without incorrectly merging different individuals who happen to share the same name! ⚡

> **Memory Trick:** **"Map emails to DSU IDs, NOT names! Emails are unique identifiers!"**

---

## 13. System & Implementation Comparisons

| Feature | DSU Identity Resolution | Pairwise Graph BFS |
| :--- | :--- | :--- |
| **Implementation** | **Clean Hash Map + DSU ⚡** | Complex Graph Building |
| **Time Complexity** | **$O(N \log N)$ Optimal ⚡** | $O(N^2)$ Pairwise Comparisons |
| **Scalability** | **Scales to 10,000,000 emails ⚡**| TLEs on large account sets |

---

## 14. How to Recognize This in Questions
* **"Merge user records or account profiles that share at least one common identifier"** $\rightarrow$ LeetCode 721 (DSU Accounts Merge).

---

## 15. Frequently Asked Interview Questions
* **Q: Why are emails in each merged account sorted lexicographically in LeetCode 721?**  
  *A:* Because LeetCode problem specifications explicitly require sorted output format for test assertions.
* **Q: How does DSU handle cloud VPC microservice network reachability testing?**  
  *A:* By calling `dsu.connected(podA, podB)` in $O(1)$ time to check if a valid routing path exists between two microservices.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DSU SYSTEM APPLICATIONS (LEETCODE 721)                |
+-----------------------------------------------------------------------+
| • Step 1: Map unique emails to integer IDs (emailToId)                |
| • Step 2: For each account, call dsu.union(firstEmail, otherEmail)    |
| • Step 3: Group emails by root ID: rootId = dsu.find(emailToId.get(e))|
| • Step 4: Sort email lists lexicographically and prepend name         |
| • Performance: $O(N \log N)$ Total Time | $O(N)$ Space ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 721 (`Accounts Merge`) in Java.
- [ ] I know why emails MUST be used as DSU keys instead of names.
- [ ] I can map generic string emails to integer DSU IDs.
- [ ] I can group merged elements by component root ID.
- [ ] I can trace identity resolution step by step.
