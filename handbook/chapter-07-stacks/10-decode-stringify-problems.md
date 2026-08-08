# 10. String Decoding, Unpacking & Encoding Stacks

## 1. Introduction
String decoding, bracket expansion, and run-length string parsing (LeetCode 394 - Decode String, LeetCode 726 - Number of Atoms, LeetCode 1087 - Brace Expansion) represent an essential class of stack parsing problems in technical coding interviews. These problems evaluate multi-stack state framing (`countStack` + `stringStack`), nested bracket depth management, digit accumulation, and string builder manipulation in **$O(N \cdot \text{maxK})$ time**.

> **Important:** In string decoding problems (e.g. `3[a2[c]]`), encountering an opening bracket **`[`** signals the start of a nested frame. We MUST push current multiplier `k` onto `countStack`, push accumulated prefix onto `stringStack`, and **reset state variables (`k = 0, currString = new StringBuilder()`)**!

## 2. Core Concepts
* **Dual Stack Frame Architecture**:
  * **`countStack` (`Deque<Integer>`)**: Stores repetition counts $K$ preceding `[`.
  * **`stringStack` (`Deque<StringBuilder>`)**: Stores prefix strings accumulated prior to entering `[`.
* **4-State Character Stream Parser**:
  1. **Digit (`isDigit(c)`)**: Multi-digit accumulation: `k = k * 10 + (c - '0')`.
  2. **Opening Bracket (`'['`)**: Push state frames (`countStack.push(k)`, `stringStack.push(currString)`). Reset `k = 0, currString = new StringBuilder()`.
  3. **Closing Bracket (`']'`)**: Pop count $K$ and prefix string. Append `currString` repeated $K$ times to prefix, and set `currString = prefix`.
  4. **Letter (`isLetter(c)`)**: Append character to `currString`.

> **Memory Trick:** **"On '[': Push k & prefix string, reset state! On ']': Pop count & prefix string, repeat & append!"**

## 3. Characteristics / Properties
* **Nested Frame Isolation**: Dual stacks isolate inner bracket expansions (e.g. `2[c]` inside `3[a2[c]]`), guaranteeing correct inner-to-outer expansion order.
* **StringBuilder Performance**: Using `StringBuilder` for string concatenation avoids intermediate string allocations, achieving optimal execution speed.

```
String Decoding Parsing State Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Input Character       | Action            | Stack Operation   | State Reset       |
+-----------------------+-------------------+-------------------+-------------------+
| Digit `'0'..'9'`      | Accumulate `k`    | None              | None              |
| Opening Bracket `'['` | Save State Frame  | Push `k` & `prefix`| `k=0, curr=""`    |
| Closing Bracket `']'` | Expand Segment    | Pop `count` & `prev`| `curr = expanded` |
| Letter `'a'..'z'`     | Append to current | None              | None              |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Decode String (LeetCode 394) on `"3[a2[c]]"`:

```
Read "3": k = 3
Read "[": countStack.push(3), stringStack.push(""), reset k=0, curr=""
Read "a": curr = "a"
Read "2": k = 2
Read "[": countStack.push(2), stringStack.push("a"), reset k=0, curr=""
Read "c": curr = "c"

Read "]": (Inner Frame Completed)
- Pop count = 2, Pop prev = "a"
- Expanded = "a" + ("c" * 2) = "acc"
- Set curr = "acc"

Read "]": (Outer Frame Completed)
- Pop count = 3, Pop prev = ""
- Expanded = "" + ("acc" * 3) = "accaccacc"
- Set curr = "accaccacc" ✅ (Output: "accaccacc")
```

## 5. Visual Diagram
Dual Stack Frame Pushing & Popping Architecture:

```
Reading "3[a2[c]]":

On 1st '[':   countStack: [ 3 ]             stringStack: [ "" ]
On 2nd '[':   countStack: [ 3, 2 ]          stringStack: [ "", "a" ]

On 1st ']':   Pop count 2, prev "a"  -> Result: "acc"
On 2nd ']':   Pop count 3, prev ""   -> Result: "accaccacc"
```

## 6. Operations / Algorithms
LeetCode 394 Master Implementation:

```java
public String decodeString(String s) {
    Deque<Integer> countStack = new ArrayDeque<>();
    Deque<StringBuilder> stringStack = new ArrayDeque<>();
    StringBuilder currString = new StringBuilder();
    int k = 0;

    for (char ch : s.toCharArray()) {
        if (Character.isDigit(ch)) {
            k = k * 10 + (ch - '0');
        } else if (ch == '[') {
            countStack.push(k);
            stringStack.push(currString);
            currString = new StringBuilder(); // Reset current string frame
            k = 0;                            // Reset count
        } else if (ch == ']') {
            StringBuilder decodedString = stringStack.pop();
            int count = countStack.pop();

            for (int i = 0; i < count; i++) {
                decodedString.append(currString);
            }
            currString = decodedString; // Update currString to expanded result
        } else {
            currString.append(ch);
        }
    }

    return currString.toString();
}
```

> **Quick Syntax:**
```java
// Frame Push on '['
countStack.push(k);
stringStack.push(currString);
currString = new StringBuilder();
k = 0;
```

## 7. Examples
* **LeetCode 394 - Decode String**: Nested bracket decoding.
* **LeetCode 726 - Number of Atoms**: Chemical formula parsing with atomic element multiplier brackets (e.g. `K4(ON(SO3)2)2`).
* **LeetCode 1087 - Brace Expansion**: Permutations of bracket options.

## 8. Java Code
Complete interview-ready Java suite implementing Decode String (LeetCode 394) and String Unpacking with dry runs:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class DecodeStringifyMaster {

    // LeetCode 394: Decode String O(N * maxK) Time, O(N) Space
    public static String decodeString(String s) {
        Deque<Integer> countStack = new ArrayDeque<>();
        Deque<StringBuilder> stringStack = new ArrayDeque<>();
        StringBuilder currString = new StringBuilder();
        int k = 0;

        for (char ch : s.toCharArray()) {
            if (Character.isDigit(ch)) {
                k = k * 10 + (ch - '0');
            } else if (ch == '[') {
                countStack.push(k);
                stringStack.push(currString);
                currString = new StringBuilder();
                k = 0;
            } else if (ch == ']') {
                StringBuilder decodedString = stringStack.pop();
                int count = countStack.pop();
                for (int i = 0; i < count; i++) {
                    decodedString.append(currString);
                }
                currString = decodedString;
            } else {
                currString.append(ch);
            }
        }

        return currString.toString();
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String s1 = "3[a]2[bc]";
        System.out.println("Decode '" + s1 + "': " + decodeString(s1)); // Output: aaabcbc

        String s2 = "3[a2[c]]";
        System.out.println("Decode '" + s2 + "': " + decodeString(s2)); // Output: accaccacc

        String s3 = "2[abc]3[cd]ef";
        System.out.println("Decode '" + s3 + "': " + decodeString(s3)); // Output: abcabccdcdcdef
    }
}
```

## 9. Complexity Analysis
| Input Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Decode String** | **$O(N \cdot \text{maxK})$** | $O(N)$ Dual Stacks | String segment repetition length |
| **Chemical Atom Parsing** | **$O(N \log N)$** | $O(N)$ Map Stack | TreeMap element name sorting |

## 10. Edge Cases
* **Multi-Digit Multipliers (`100[leetcode]`)**: Multi-digit accumulation `k = k * 10 + (ch - '0')` handles numbers $> 9$.
* **Unbracketed Characters (`2[a]bc`)**: Trailing characters outside brackets append to `currString` directly.
* **Deeply Nested Brackets (`2[2[2[a]]]`)**: Dual stacks handle arbitrary nesting depths cleanly.

## 11. Common Mistakes
* Forgetting to reset `k = 0` and `currString = new StringBuilder()` after pushing onto stacks on `[`.
* Using `String` concatenation `+` inside repetition loops (causes $O(K^2)$ memory copying slowdown!). Always use `StringBuilder.append()`.
* Omitting multi-digit `k = k * 10 + (ch - '0')` logic, assuming multipliers are always single digits `0..9`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** State Reset Rule on Opening Bracket `[`:
> When `ch == '['`:
> 1. Push `k` onto `countStack`.
> 2. Push `currString` onto `stringStack`.
> 3. **Reset `currString = new StringBuilder();`**
> 4. **Reset `k = 0;`**
> Forgetting to reset both state variables corrupts subsequent string frame accumulation!

> **Memory Trick:** **"Push on '[', then RESET k = 0 and currString = new StringBuilder()!"**

## 13. Comparisons
| Feature | Single Stack String Parsing | Dual Stack (`countStack` + `stringStack`) |
| :--- | :--- | :--- |
| **Stack Content** | Mixed Object / Char Stack | Typed Dual Stacks (`Integer` & `StringBuilder`) |
| **Casting Requirement** | Heavy casting `(String) obj` | **Type Safe (Zero casting)** |
| **Code Readability** | Low | **High (Clean & Modern)** |

## 14. How to Recognize This in Questions
* **"Decode string formatted as k[encoded_string]"** $\rightarrow$ Dual Stack Decoding (LeetCode 394).
* **"Parse nested chemical formula multipliers"** $\rightarrow$ HashMap Stack parsing (LeetCode 726).

## 15. Frequently Asked Interview Questions
* **Q: Why are two separate stacks (`countStack` and `stringStack`) preferred over a single unified stack?**  
  *A:* Two typed stacks eliminate object casting and variant type wrappers in Java, providing strict type safety, cleaner code, and superior execution speed.
* **Q: How does `k = k * 10 + (ch - '0')` parse multi-digit counts?**  
  *A:* When encountering consecutive digit characters (e.g. `'1'`, `'0'`, `'0'`), multiplying the previous accumulated value by 10 shifts existing digits left by one decimal place, allowing the new digit `(ch - '0')` to be added at the units position.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING DECODING & BRACKET UNPACKING                  |
+-----------------------------------------------------------------------+
| • Digit: k = k * 10 + (ch - '0')                                      |
| • Open '[': countStack.push(k); stringStack.push(currString);         |
|             currString = new StringBuilder(); k = 0;                  |
| • Close ']': prev = stringStack.pop(); count = countStack.pop();       |
|              for (0..count) prev.append(currString); currString = prev; |
| • Letter: currString.append(ch)                                       |
| • Complexity: O(N * maxK) Time | O(N) Space                           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the multi-digit parsing formula `k = k * 10 + (ch - '0')`.
- [ ] I can write the 4-step state reset sequence on `[`.
- [ ] I can write the frame expansion and popping logic on `]`.
- [ ] I can implement Decode String (LeetCode 394) in under 5 minutes.
- [ ] I know why dual typed stacks are preferred over a single mixed object stack.
