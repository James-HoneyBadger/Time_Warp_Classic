# JavaScript Language Reference

Complete reference for JavaScript syntax in Time Warp Classic.

> **Note:** JavaScript runs via Node.js subprocess with a 30-second timeout. All modern ES6+ features are supported.

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variables | `let`/`const`/`var` | `let x = 10` |
| Console | `console.log(expr)` | `console.log("Hello")` |
| Operators | `+ - * / % **` | `5 + 3` |
| If/Else | `if (cond) { ... }` | `if (x > 5) { ... }` |
| For Loop | `for (let i=0; i<n; i++)` | `for (let i=0; i<10; i++)` |
| While Loop | `while (cond) { ... }` | `while (x < 100) { ... }` |
| Function | `function name(args) { }` | `function add(a,b) { return a+b }` |
| Arrow | `(args) => expr` | `const sq = x => x * x` |
| Class | `class Name { ... }` | `class Dog { bark() {} }` |
| Template | `` `${expr}` `` | `` `Hello ${name}` `` |
| Destruct | `const {a, b} = obj` | `const [x, y] = [1, 2]` |
| Spread | `...array` | `[...arr1, ...arr2]` |
| Array | `[value, value, ...]` | `[1, 2, 3]` |
| Object | `{key: value, ...}` | `{name: "Alice"}` |

## Variables & Data Types

### Variable Declaration

```javascript
// ES6+ (preferred)
let x = 10;                // Block-scoped, reassignable
const name = "Alice";      // Block-scoped, constant
const PI = 3.14159;        // Cannot be reassigned

// Legacy
var count = 0;             // Function-scoped (avoid in new code)

// Multiple declarations
let a = 1, b = 2, c = 3;
const [first, second] = [10, 20];  // Destructuring
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

## Arrow Functions

```javascript
// Arrow function syntax
const square = (x) => x * x;
const add = (a, b) => a + b;

// Single parameter (parentheses optional)
const double = x => x * 2;

// Multi-line body
const greet = (name) => {
    const msg = `Hello, ${name}!`;
    return msg;
};

// With array methods
const numbers = [1, 2, 3, 4, 5];
const evens = numbers.filter(n => n % 2 === 0);
const doubled = numbers.map(n => n * 2);
const sum = numbers.reduce((acc, n) => acc + n, 0);
```

## Template Literals

```javascript
const name = "Alice";
const age = 30;

// String interpolation
console.log(`Hello, ${name}!`);
console.log(`${name} is ${age} years old`);

// Multi-line strings
const html = `
  <div>
    <h1>${name}</h1>
    <p>Age: ${age}</p>
  </div>
`;

// Expressions in templates
console.log(`2 + 3 = ${2 + 3}`);
console.log(`${name.toUpperCase()} is ${age >= 18 ? 'adult' : 'minor'}`);
```

## Destructuring

### Array Destructuring

```javascript
const [a, b, c] = [1, 2, 3];
const [first, ...rest] = [10, 20, 30, 40];
// first = 10, rest = [20, 30, 40]

// Skip elements
const [, second, , fourth] = [1, 2, 3, 4];

// Default values
const [x = 0, y = 0] = [5];  // x = 5, y = 0
```

### Object Destructuring

```javascript
const person = { name: "Alice", age: 30, city: "NYC" };
const { name, age } = person;

// Rename
const { name: firstName, age: years } = person;

// Default values
const { name, email = "N/A" } = person;

// Nested
const { address: { street, zip } } = complexObj;
```

## Spread & Rest Operators

```javascript
// Spread arrays
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];  // [1, 2, 3, 4, 5, 6]

// Spread objects
const defaults = { color: "red", size: 10 };
const custom = { ...defaults, size: 20 };  // { color: "red", size: 20 }

// Rest parameters
function sum(...numbers) {
    return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4);  // 10
```

## Classes

```javascript
class Animal {
    constructor(name, sound) {
        this.name = name;
        this.sound = sound;
    }

    speak() {
        console.log(`${this.name} says ${this.sound}`);
    }

    toString() {
        return `Animal(${this.name})`;
    }
}

// Inheritance
class Dog extends Animal {
    constructor(name) {
        super(name, "Woof");
        this.tricks = [];
    }

    learn(trick) {
        this.tricks.push(trick);
    }

    showTricks() {
        console.log(`${this.name} knows: ${this.tricks.join(", ")}`);
    }
}

const dog = new Dog("Rex");
dog.speak();             // Rex says Woof
dog.learn("sit");
dog.showTricks();        // Rex knows: sit
```

### Static Methods & Getters

```javascript
class Circle {
    constructor(radius) {
        this._radius = radius;
    }

    get area() {
        return Math.PI * this._radius ** 2;
    }

    get circumference() {
        return 2 * Math.PI * this._radius;
    }

    static fromDiameter(d) {
        return new Circle(d / 2);
    }
}

const c = new Circle(5);
console.log(c.area);            // ~78.54
const c2 = Circle.fromDiameter(10);
```

## Promises & Async/Await

### Promises

```javascript
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const fetchData = () => {
    return new Promise((resolve, reject) => {
        const data = { name: "Alice", age: 30 };
        resolve(data);
    });
};

fetchData()
    .then(data => console.log(data.name))
    .catch(err => console.error(err));
```

### Async/Await

```javascript
async function getData() {
    try {
        const data = await fetchData();
        console.log(data.name);
    } catch (err) {
        console.error("Error:", err);
    }
}
```

## Closures

```javascript
function makeCounter() {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

const counter = makeCounter();
counter.increment();     // 1
counter.increment();     // 2
counter.decrement();     // 1
console.log(counter.getCount());  // 1
```

## Error Handling

```javascript
try {
    const result = riskyOperation();
    console.log(result);
} catch (error) {
    console.error("Error:", error.message);
} finally {
    console.log("Cleanup complete");
}

// Custom errors
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}
```

## Regular Expressions

```javascript
const text = "Hello World 123";

// Test
/World/.test(text);              // true

// Match
text.match(/\d+/);              // ["123"]
text.match(/[A-Z]/g);           // ["H", "W"]

// Replace
text.replace(/World/, "JS");    // "Hello JS 123"
text.replace(/\d/g, "#");       // "Hello World ###"

// Split
"a,b,c".split(/,/);             // ["a", "b", "c"]
```

## Iterators & Generators

```javascript
// Generator function
function* fibonacci() {
    let a = 0, b = 1;
    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

const fib = fibonacci();
for (let i = 0; i < 8; i++) {
    console.log(fib.next().value);
}

// for...of
for (const val of [10, 20, 30]) {
    console.log(val);
}
```

## Map & Set

```javascript
// Map (key-value pairs, any key type)
const map = new Map();
map.set("name", "Alice");
map.set(42, "answer");
console.log(map.get("name"));   // "Alice"
console.log(map.size);          // 2

// Set (unique values)
const set = new Set([1, 2, 2, 3, 3]);
console.log(set.size);          // 3
set.add(4);
set.has(2);                     // true
```

## Tips & Tricks

1. **Use `let`/`const`** instead of `var`
2. **Use `===`** for strict comparison (not `==`)
3. **Use arrow functions** for short callbacks
4. **Use template literals** for string formatting
5. **Use destructuring** to extract values cleanly
6. **Use `console.log()`** for debugging
7. **Use `try/catch`** for error handling
8. **Execution timeout:** 30 seconds for all JavaScript programs

## Common Gotchas

```javascript
// Type coercion
"5" + 3                // "53" (string concatenation)
"5" - 3                // 2 (numeric subtraction)

// Loose equality
0 == false             // true
0 === false            // false

// let vs var scope
for (let i = 0; i < 3; i++) {}
// console.log(i);    // ReferenceError (let is block-scoped)
```

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/javascript/](../../examples/javascript/)

---

**Last Updated:** 2025
