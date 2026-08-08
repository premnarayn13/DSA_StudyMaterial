# 02. Character Encoding, ASCII & Unicode in Java

## 1. Introduction
Character encoding defines how human characters (letters, numbers, symbols, emojis) are represented as binary bit patterns in computer memory. In Java, character processing relies on **ASCII (American Standard Code for Information Interchange)** and **Unicode (UTF-16)** representations. In technical coding interviews, understanding character integer values, ASCII offset arithmetic (`ch - 'a'`), uppercase/lowercase conversions, and digit parsing without built-in libraries is essential for string manipulation.

> **Important:** In Java, `char` is a 16-bit unsigned integer type representing UTF-16 code units (range $0$ to $65,535$). Because `char` is internally an integer, you can perform direct mathematical operations on characters!

## 2. Core Concepts
* **ASCII Code Table**: Standard 7-bit / 8-bit character set mapping $128$ characters to integers $0 \dots 127$:
  * `'0'` to `'9'` $\to$ ASCII values **$48$ to $57$**
  * `'A'` to `'Z'` $\to$ ASCII values **$65$ to $90$**
  * `'a'` to `'z'` $\to$ ASCII values **$97$ to $122$**
* **ASCII Distance / Offset**:
  * Distance between `'a'` and `'z'` is $25$ ($122 - 97 = 25$).
  * Case difference: `'a' - 'A' = 32` ($97 - 65 = 32$).
* **Digit Character to Integer Conversion**: Subtracting ASCII `'0'`:
  $$\text{intValue} = \text{charVal} - \text{'0'}$$
* **Unicode (UTF-8 / UTF-16)**: Universal character encoding standard accommodating international scripts, symbols, and Emojis (which consume 2 Java `char` surrogate pairs!).

> **Memory Trick:** **"48 is '0', 65 is 'A', 97 is 'a'. Difference between 'a' and 'A' is 32!"**

## 3. Characteristics / Properties
* **Character Arithmetic**:
  * Convert digit char to int: `int num = ch - '0';` (e.g., `'7' - '0' = 55 - 48 = 7`).
  * Convert int to digit char: `char ch = (char)(num + '0');`.
  * Convert uppercase to lowercase: `char lower = (char)(ch + 32);` or `(char)(ch | 32)`.
  * Convert lowercase to uppercase: `char upper = (char)(ch - 32);` or `(char)(ch & ~32)`.
* **Bitwise Case Conversion**:
  * Toggle Case: `ch ^ 32` (`'A' ^ 32 = 'a'`, `'a' ^ 32 = 'A'`).

```
ASCII Reference Table Quick View:
+-------------------+-------------------+-------------------+-------------------+
| Character Category| Char Representation| ASCII Decimal Range| Key Offset Formula|
+-------------------+-------------------+-------------------+-------------------+
| Digits            | '0' ... '9'       | 48 ... 57         | val = ch - '0'    |
| Uppercase Letters | 'A' ... 'Z'       | 65 ... 90         | index = ch - 'A'  |
| Lowercase Letters | 'a' ... 'z'       | 97 ... 122        | index = ch - 'a'  |
| Case Difference   | 'a' - 'A'         | 32                | lower = ch | 32   |
+-------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Character Arithmetic & Case Transformations:

```
Char '5': ASCII 53 -> '5' - '0' = 53 - 48 = 5 (Numeric integer value!)
Char 'C': ASCII 67 -> 'C' - 'A' = 67 - 65 = 2 (0-based uppercase index!)
Char 'c': ASCII 99 -> 'c' - 'a' = 99 - 97 = 2 (0-based lowercase index!)

Bitwise Case Manipulation:
'A' (Binary 01000001 = 65)
 32 (Binary 00100000 = 32)
--------------------------
 OR | =    01100001 = 97 ('a' Lowercase!)
```

## 5. Visual Diagram
ASCII Offset Mapping & Bitwise Case Conversion:

```
Uppercase 'A' (65):  0 1 0 0 0 0 0 1
Bitwise OR 32:       0 0 1 0 0 0 0 0  (Set 6th bit)
------------------------------------
Lowercase 'a' (97):  0 1 1 0 0 0 0 1

Uppercase 'B' (66):  0 1 0 0 0 0 1 0
Bitwise OR 32:       0 0 1 0 0 0 0 0
------------------------------------
Lowercase 'b' (98):  0 1 1 0 0 0 1 0
```

## 6. Operations / Algorithms
Essential Character Conversion Idioms in Java:

### 1. Manual String to Integer Parsing (`atoi` - LeetCode 8)
```java
public int myAtoi(String str) {
    int i = 0, n = str.length(), sign = 1;
    long result = 0;

    // Skip whitespace
    while (i < n && str.charAt(i) == ' ') i++;

    // Check sign
    if (i < n && (str.charAt(i) == '+' || str.charAt(i) == '-')) {
        sign = (str.charAt(i) == '-') ? -1 : 1;
        i++;
    }

    // Convert digits
    while (i < n && Character.isDigit(str.charAt(i))) {
        int digit = str.charAt(i) - '0';
        result = result * 10 + digit;

        // Check overflow
        if (sign * result > Integer.MAX_VALUE) return Integer.MAX_VALUE;
        if (sign * result < Integer.MIN_VALUE) return Integer.MIN_VALUE;
        i++;
    }

    return (int) (sign * result);
}
```

> **Quick Syntax:**
```java
// Fast Character Properties using Character Class
boolean isLetter = Character.isLetter(ch);
boolean isDigit  = Character.isDigit(ch);
boolean isAlnum  = Character.isLetterOrDigit(ch);
char toLower     = Character.toLowerCase(ch);
```

## 7. Examples
* **LeetCode 8 - String to Integer (atoi)**: Parsing string digits manually using `ch - '0'`.
* **LeetCode 125 - Valid Palindrome**: Filtering alphanumeric characters using `Character.isLetterOrDigit()`.
* **LeetCode 43 - Multiply Strings**: Multiplying large numeric strings digit-by-digit using ASCII character math.

## 8. Java Code
Complete interview-ready Java suite implementing ASCII arithmetic, Manual String-to-Int parsing, Character Frequency Counting, and Bitwise Case Conversion:

```java
public class CharacterEncodingMaster {

    // 1. Convert Digit String to Int manually (atoi implementation)
    public static int parseStringToInt(String s) {
        if (s == null || s.isEmpty()) return 0;

        int i = 0;
        int n = s.length();
        int sign = 1;
        long result = 0;

        // Skip leading spaces
        while (i < n && s.charAt(i) == ' ') i++;

        // Handle sign
        if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
            sign = (s.charAt(i) == '-') ? -1 : 1;
            i++;
        }

        // Process digits using ASCII subtraction (ch - '0')
        while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
            int digit = s.charAt(i) - '0';
            result = result * 10 + digit;

            // Overflow protection
            if (sign == 1 && result > Integer.MAX_VALUE) return Integer.MAX_VALUE;
            if (sign == -1 && -result < Integer.MIN_VALUE) return Integer.MIN_VALUE;

            i++;
        }

        return (int) (sign * result);
    }

    // 2. Fast Case Conversion using ASCII / Bitwise Manipulation
    public static String toLowerCaseFast(String s) {
        char[] chars = s.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            if (chars[i] >= 'A' && chars[i] <= 'Z') {
                chars[i] = (char) (chars[i] | 32); // Bitwise OR set 6th bit
            }
        }
        return new String(chars);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test ASCII Math
        char digitChar = '7';
        int numericVal = digitChar - '0';
        System.out.println("Char '7' -> Int Value: " + numericVal); // Output: 7

        // Test Manual atoi
        System.out.println("Parsed '-42': " + parseStringToInt("   -42")); // Output: -42
        System.out.println("Parsed with overflow: " + parseStringToInt("999999999999")); // Output: 2147483647

        // Test Bitwise Case Conversion
        System.out.println("Fast Lowercase 'HELLO WORLD': " + toLowerCaseFast("HELLO WORLD")); // hello world
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **`ch - '0'` (Digit Parse)** | **$O(1)$** | **$O(1)$** | Direct ASCII integer subtraction |
| **`ch \| 32` (To Lowercase)**| **$O(1)$** | **$O(1)$** | Bitwise OR operation |
| **`ch & ~32` (To Uppercase)**| **$O(1)$** | **$O(1)$** | Bitwise AND clear bit operation |
| **Manual `atoi` Parsing** | **$O(N)$** | **$O(1)$** | Single linear pass over string |

## 10. Edge Cases
* **Integer Overflow in String Digits**: Strings like `"999999999999999"` overflow 32-bit signed `int`. Always use `long result` during digit accumulation and check bounds against `Integer.MAX_VALUE`.
* **Unicode Emojis / Surrogate Pairs**: Emojis (like 😀 `\uD83D\uDE00`) consume 2 `char` code units in Java (`s.length()` returns 2!). Standard `s.charAt(i)` splits the surrogate pair.
* **Non-ASCII Characters**: International characters (e.g., `'é'`, `'ñ'`) have ASCII values $> 127$. Direct subtraction `ch - 'a'` will produce negative indices!

## 11. Common Mistakes
* Assuming `char` in Java is strictly 8-bit (Java `char` is 16-bit UTF-16!).
* Using `ch - 'a'` when the input string contains uppercase letters or non-alphabetic characters (causes `ArrayIndexOutOfBoundsException`).
* Forgetting to multiply by 10 when accumulating parsed digits: `result = result * 10 + digit`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Remember the bitwise case tricks for fast character manipulation:
> * **To Lowercase**: `ch | 32` or `ch | ' '` (Sets 6th bit).
> * **To Uppercase**: `ch & ~32` or `ch & '_'` (Clears 6th bit).
> * **Toggle Case**: `ch ^ 32` or `ch ^ ' '` (Flips 6th bit).

> **Memory Trick:** **"Digit value = ch - '0'; Letter offset = ch - 'a'"**.

## 13. Comparisons
| Feature | `ch - '0'` ASCII Math | `Character.getNumericValue(ch)` |
| :--- | :--- | :--- |
| **Speed** | **Fastest (Single CPU subtract instruction)** | Slower (Method call overhead) |
| **Input Restriction**| Basic ASCII digits `'0'...'9'` | Handles Unicode / Roman numerals |
| **Interview Recommendation** | **PREFERRED FOR DSA** | General application code |

## 14. How to Recognize This in Questions
* **"Parse string into integer without using Integer.parseInt()"** $\rightarrow$ Manual Digit Accumulation `result = result * 10 + (ch - '0')`.
* **"Check valid palindrome ignoring case and non-alphanumeric chars"** $\rightarrow$ ASCII offset check or `Character.isLetterOrDigit()`.

## 15. Frequently Asked Interview Questions
* **Q: Why does `'7' - '0'` evaluate to integer `7`?**  
  *A:* Because ASCII values of consecutive digits are sequential: `'0'` is 48, `'1'` is 49, ..., `'7'` is 55. Subtracting $55 - 48$ yields $7$.
* **Q: What is a Surrogate Pair in Java Strings?**  
  *A:* Characters outside the Basic Multilingual Plane (like Emojis) cannot fit into a single 16-bit `char`. Java encodes them using a pair of two 16-bit `char` code units called a Surrogate Pair.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CHARACTER ENCODING, ASCII & UNICODE                   |
+-----------------------------------------------------------------------+
| • ASCII Values: '0'=48, 'A'=65, 'a'=97 | 'a' - 'A' = 32               |
| • Digit to Int: int val = ch - '0' | Int to Digit: char ch = val + '0'|
| • Char Indexing: Lowercase = ch - 'a' | Uppercase = ch - 'A'          |
| • Bitwise Lowercase: ch | 32 | Bitwise Uppercase: ch & ~32            |
| • Manual Atoi Formula: result = result * 10 + (ch - '0')              |
| • Java `char` is 16-bit unsigned (0 to 65,535) UTF-16 code unit       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can state the ASCII integer values for `'0'`, `'A'`, and `'a'`.
- [ ] I can convert digit characters to integer values using `ch - '0'`.
- [ ] I can write manual string-to-int parsing (`atoi`) with overflow checks.
- [ ] I know the bitwise case manipulation tricks (`| 32`, `& ~32`).
- [ ] I understand how Java handles 16-bit UTF-16 characters and surrogate pairs.
