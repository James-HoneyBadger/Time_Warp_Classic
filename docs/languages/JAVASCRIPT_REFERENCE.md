# JavaScript Language Reference

Complete reference for JavaScript (ES5) syntax in Time Warp Classic.

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variables | `var name = value` | `var x = 10` |
| Console | `console.log(expr)` | `console.log("Hello")` |
| Operators | `+ - * / % ^` | `5 + 3` |
| If/Else | `if (cond) { ... }` | `if (x > 5) { ... }` |
| For Loop | `for (i=0; i<n; i++)` | `for (i=0; i<10; i++)` |
| While Loop | `while (cond) { ... }` | `while (x < 100) { ... }` |
| Function | `function name(args) { ... }` | `function add(a,b) { return a+b }` |
| Array | `[value, value, ...]` | `[1, 2, 3]` |
| Object | `{key: value, ...}` | `{name: "Alice"}` |

## Variables & Data Types

### Variable Declaration

```javascript
var x = 10;               // Number
var name = "Alice";       // String
var height = 5.7;         // Number (float)
var isActive = true;      // Boolean
var items = [1, 2, 3];    // Array
var person = {name: "Alice"};  // Object
```

### Data Types

```javascript
typeof 42              // "number"
typeof "hello"         // "string"
typeof 3.14            // "number"
typeof true            // "boolean"
typeof [1, 2]          // "object"
typeof {a: 1}          // "object"
typeof undefined       // "undefined"
typeof function(){}    // "function"
```

### Type Coercion

```javascript
Number("42")           // 42
String(42)             // "42"
Boolean(1)             // true
parseInt("42")         // 42
parseFloat("3.14")     // 3.14
```

## Operators

### Arithmetic

```javascript
+       Addition         5 + 3 = 8
-       Subtraction      5 - 3 = 2
*       Multiplication   5 * 3 = 15
/       Division         6 / 2 = 3
%       Modulo           7 % 3 = 1
++      Increment        x++
--      Decrement        x--
```

### Assignment

```javascript
x = 5;
x += 3;    // x = x + 3
x -= 2;    // x = x - 2
x *= 2;    // x = x * 2
x /= 4;    // x = x / 4
x %= 2;    // x = x % 2
```

### Comparison

```javascript
==      Equal value       5 == 5
===     Strict equal      5 === 5
!=      Not equal         5 != 3
!==     Strict not equal  5 !== 3
<       Less than         3 < 5
>       Greater than      5 > 3
<=      Less or equal     5 <= 5
>=      Greater or equal  5 >= 5
```

### Logical

```javascript
&&      AND               x > 5 && y < 10
||      OR                x == 1 || x == 2
!       NOT               !done
```

## Control Structures

### If/Else

```javascript
if (condition) {
    statements;
} else if (condition) {
    statements;
} else {
    statements;
}

if (age >= 18) {
    console.log("Adult");
} else {
    console.log("Minor");
}
```

### Switch

```javascript
switch (value) {
    case 1:
        console.log("One");
        break;
    case 2:
        console.log("Two");
        break;
    default:
        console.log("Other");
}
```

### For Loop

```javascript
for (var i = 0; i < 5; i++) {
    console.log(i);  // 0, 1, 2, 3, 4
}

for (var i = 0; i < 10; i += 2) {
    console.log(i);  // 0, 2, 4, 6, 8
}
```

### While Loop

```javascript
var count = 0;
while (count < 5) {
    console.log(count);
    count++;
}

var i = 5;
do {
    console.log(i);
    i--;
} while (i > 0);
```

### Break & Continue

```javascript
for (var i = 0; i < 10; i++) {
    if (i == 5) break;        // Exit loop
    if (i == 2) continue;     // Skip iteration
    console.log(i);
}
```

## Arrays

### Array Basics

```javascript
var numbers = [1, 2, 3, 4, 5];
var mixed = [1, "hello", true];

// Access
numbers[0]             // 1
numbers[numbers.length - 1]  // 5

// Length
numbers.length         // 5

// Modify
numbers[0] = 10;
```

### Array Methods

```javascript
numbers.push(6)        // Add to end -> [1,2,3,4,5,6]
numbers.pop()          // Remove from end -> 6
numbers.unshift(0)     // Add to beginning -> [0,1,2,3,4,5]
numbers.shift()        // Remove from beginning -> 0
numbers.join(", ")     // "1, 2, 3, 4, 5"
numbers.reverse()      // [5, 4, 3, 2, 1]
numbers.sort()         // [1, 2, 3, 4, 5]
numbers.indexOf(3)     // 2
```

### Array Iteration

```javascript
// For loop
for (var i = 0; i < numbers.length; i++) {
    console.log(numbers[i]);
}

// For..in loop
for (var i in numbers) {
    console.log(numbers[i]);
}
```

## Objects

### Object Basics

```javascript
var person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

// Access
person.name            // "Alice"
person["age"]          // 30

// Modify
person.email = "alice@example.com";
person["phone"] = "555-1234";

// Delete
delete person.city;
```

### Object Methods

```javascript
var person = {name: "Alice", age: 30};

Object.keys(person)    // ["name", "age"]
Object.values(person)  // ["Alice", 30]

// Iteration
for (var key in person) {
    console.log(key + ": " + person[key]);
}
```

## Functions

### Function Definition

```javascript
function greet(name) {
    return "Hello, " + name;
}

function add(a, b) {
    return a + b;
}

function printMessage(msg) {
    console.log(msg);
}

// Calling
greet("Alice")         // "Hello, Alice"
add(5, 3)              // 8
printMessage("Hi")
```

### Anonymous Functions

```javascript
var square = function(x) {
    return x * x;
};

square(5);             // 25
```

### Function Parameters

```javascript
function introduce(name, age) {
    console.log(name + " is " + age);
}

// Default parameters
function greet(name) {
    name = name || "Guest";  // Default to "Guest"
    return "Hello, " + name;
}

// Variable arguments
function sum() {
    var total = 0;
    for (var i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

sum(1, 2, 3, 4, 5);    // 15
```

### Recursion

```javascript
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

factorial(5);          // 120

function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fibonacci(6);          // 8
```

## String Operations

### String Basics

```javascript
var msg = "Hello, World!";

// Length
msg.length             // 13

// Access characters
msg[0]                 // "H"
msg.charAt(0)          // "H"

// Case conversion
msg.toUpperCase()      // "HELLO, WORLD!"
msg.toLowerCase()      // "hello, world!"
```

### String Methods

```javascript
var str = "Hello World";

str.length             // 11
str.substring(0, 5)    // "Hello"
str.slice(0, 5)        // "Hello"
str.indexOf("World")   // 6
str.lastIndexOf("o")   // 7
str.replace("World", "JavaScript")
str.split(" ")         // ["Hello", "World"]
str.trim()             // Remove whitespace
str.startsWith("Hello") // true
str.endsWith("World")  // true
```

### String Concatenation

```javascript
"Hello" + " " + "World"       // "Hello World"
var msg = "Hello";
msg += " World";              // "Hello World"
```

## Math Object

```javascript
Math.abs(-5)           // 5
Math.max(3, 5, 2)      // 5
Math.min(3, 5, 2)      // 2
Math.round(4.7)        // 5
Math.floor(4.7)        // 4
Math.ceil(4.2)         // 5
Math.sqrt(16)          // 4
Math.pow(2, 3)         // 8
Math.random()          // 0.something
Math.sin(0)            // 0
Math.cos(0)            // 1
Math.PI                // 3.14159...
Math.E                 // 2.71828...
```

## Complete Examples

### Temperature Converter

```javascript
var celsius = 25;
var fahrenheit = (celsius * 9/5) + 32;
console.log(celsius + "C = " + fahrenheit + "F");
```

### Sum of Array

```javascript
var numbers = [1, 2, 3, 4, 5];
var sum = 0;
for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
console.log("Sum: " + sum);
```

### Fibonacci Sequence

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

for (var i = 0; i < 8; i++) {
    console.log(fibonacci(i));
}
```

### Word Counter

```javascript
var text = "hello world hello javascript";
var words = text.split(" ");
var count = {};

for (var i = 0; i < words.length; i++) {
    var word = words[i];
    count[word] = (count[word] || 0) + 1;
}

for (var word in count) {
    console.log(word + ": " + count[word]);
}
```

## Tips & Tricks

1. **Use console.log()** for debugging
2. **Always declare variables** with var
3. **Use === for comparison** (not ==)
4. **Avoid global variables** when possible
5. **Test with boundary values** for functions
6. **Break complex code** into smaller functions
7. **Use meaningful names** for clarity

## Common Gotchas

```javascript
// Type coercion
"5" + 3                // "53" (string concatenation)
"5" - 3                // 2 (numeric subtraction)

// Loose equality
0 == false             // true
0 === false            // false

// Global variables
function test() {
    x = 5;             // Creates global variable
}
```

## See Also

- [USER_GUIDE.md](../user/USER_GUIDE.md)
- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/javascript/](../../examples/javascript/)

---

**Last Updated:** 2024
