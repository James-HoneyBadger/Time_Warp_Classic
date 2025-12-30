// COMPREHENSIVE JAVASCRIPT DEMO - Time Warp Classic IDE
// Demonstrates all major JavaScript ES5 features

console.log("==================================================");
console.log("COMPREHENSIVE JAVASCRIPT DEMO");
console.log("==================================================");
console.log("");

// --- VARIABLES AND DATA TYPES ---
console.log("=== VARIABLES AND DATA TYPES ===");
var intVar = 42;
var floatVar = 3.14159;
var stringVar = "Time Warp";
var boolVar = true;
var nullVar = null;
var undefinedVar = undefined;

console.log("Integer: " + intVar);
console.log("Float: " + floatVar);
console.log("String: " + stringVar);
console.log("Boolean: " + boolVar);
console.log("Null: " + nullVar);
console.log("Undefined: " + undefinedVar);
console.log("");

// --- ARITHMETIC OPERATIONS ---
console.log("=== ARITHMETIC OPERATIONS ===");
var a = 10;
var b = 3;
console.log("Addition: " + (a + b));
console.log("Subtraction: " + (a - b));
console.log("Multiplication: " + (a * b));
console.log("Division: " + (a / b));
console.log("Modulo: " + (a % b));
console.log("Exponentiation: " + Math.pow(a, 2));
console.log("");

// --- STRING OPERATIONS ---
console.log("=== STRING OPERATIONS ===");
var msg = "JavaScript Programming";
console.log("Original: " + msg);
console.log("Length: " + msg.length);
console.log("Uppercase: " + msg.toUpperCase());
console.log("Lowercase: " + msg.toLowerCase());
console.log("charAt(0): " + msg.charAt(0));
console.log("charCodeAt(0): " + msg.charCodeAt(0));
console.log("indexOf('Script'): " + msg.indexOf("Script"));
console.log("substring(0, 10): " + msg.substring(0, 10));
console.log("slice(0, 4): " + msg.slice(0, 4));
console.log("split(' '): " + msg.split(" "));
console.log("replace('JavaScript', 'Time Warp'): " + msg.replace("JavaScript", "Time Warp"));
console.log("concat(' Language'): " + msg.concat(" Language"));
console.log("");

// --- ARRAYS ---
console.log("=== ARRAYS ===");
var numbers = [10, 20, 30, 40, 50];
console.log("Array: " + numbers);
console.log("First element: " + numbers[0]);
console.log("Last element: " + numbers[numbers.length - 1]);
console.log("Length: " + numbers.length);

var sum = 0;
for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
console.log("Sum: " + sum);

numbers.push(60);
console.log("After push(60): " + numbers);

var popped = numbers.pop();
console.log("Popped: " + popped);

numbers.unshift(5);
console.log("After unshift(5): " + numbers);

numbers.shift();
console.log("After shift(): " + numbers);

console.log("indexOf(30): " + numbers.indexOf(30));
console.log("");

// --- OBJECTS ---
console.log("=== OBJECTS ===");
var person = {
    name: "Alice",
    age: 30,
    city: "New York",
    occupation: "Developer"
};
console.log("Object: " + JSON.stringify(person));
console.log("Name: " + person.name);
console.log("Age: " + person["age"]);
person.email = "alice@example.com";
console.log("After adding email: " + JSON.stringify(person));
console.log("");

// --- CONDITIONAL STATEMENTS ---
console.log("=== IF/ELSE STATEMENTS ===");
var age = 25;
if (age >= 18) {
    console.log("You are an adult");
} else {
    console.log("You are a minor");
}

var score = 85;
if (score >= 90) {
    console.log("Grade: A");
} else if (score >= 80) {
    console.log("Grade: B");
} else if (score >= 70) {
    console.log("Grade: C");
} else {
    console.log("Grade: F");
}
console.log("");

// --- SWITCH STATEMENT ---
console.log("=== SWITCH STATEMENT ===");
var day = 3;
switch (day) {
    case 1:
        console.log("Monday");
        break;
    case 2:
        console.log("Tuesday");
        break;
    case 3:
        console.log("Wednesday");
        break;
    default:
        console.log("Unknown day");
}
console.log("");

// --- FOR LOOPS ---
console.log("=== FOR LOOPS ===");
console.log("Counting 1 to 5:");
for (var i = 1; i <= 5; i++) {
    console.log("  " + i + " squared = " + (i * i));
}
console.log("");

// --- WHILE LOOPS ---
console.log("=== WHILE LOOPS ===");
var counter = 1;
while (counter <= 3) {
    console.log("  Counter: " + counter);
    counter++;
}
console.log("");

// --- DO-WHILE LOOPS ---
console.log("=== DO-WHILE LOOPS ===");
var x = 1;
do {
    console.log("  x = " + x);
    x++;
} while (x <= 3);
console.log("");

// --- FUNCTIONS ---
console.log("=== FUNCTIONS ===");
function greet(name) {
    return "Hello, " + name + "!";
}

function add(a, b) {
    return a + b;
}

function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(greet("Alice"));
console.log("5 + 3 = " + add(5, 3));
console.log("5! = " + factorial(5));
console.log("");

// --- ANONYMOUS FUNCTIONS ---
console.log("=== ANONYMOUS FUNCTIONS ===");
var multiply = function(a, b) {
    return a * b;
};
console.log("Multiply 4 * 5 = " + multiply(4, 5));
console.log("");

// --- MATHEMATICAL OPERATIONS ---
console.log("=== MATHEMATICAL OPERATIONS ===");
console.log("Math.sqrt(16): " + Math.sqrt(16));
console.log("Math.abs(-42): " + Math.abs(-42));
console.log("Math.floor(3.7): " + Math.floor(3.7));
console.log("Math.ceil(3.2): " + Math.ceil(3.2));
console.log("Math.round(3.5): " + Math.round(3.5));
console.log("Math.sin(0): " + Math.sin(0));
console.log("Math.cos(0): " + Math.cos(0));
console.log("Math.tan(0): " + Math.tan(0));
console.log("Math.pow(2, 8): " + Math.pow(2, 8));
console.log("Math.min(5, 2, 8): " + Math.min(5, 2, 8));
console.log("Math.max(5, 2, 8): " + Math.max(5, 2, 8));
console.log("Math.random(): " + Math.random());
console.log("Math.PI: " + Math.PI);
console.log("Math.E: " + Math.E);
console.log("");

// --- COMPARISON OPERATORS ---
console.log("=== COMPARISON OPERATORS ===");
if (5 > 3) console.log("5 > 3: true");
if (5 == 5) console.log("5 == 5: true");
if (5 === 5) console.log("5 === 5: true");
if (5 < 10) console.log("5 < 10: true");
if (5 >= 5) console.log("5 >= 5: true");
if (5 <= 10) console.log("5 <= 10: true");
if (5 != 3) console.log("5 != 3: true");
if (5 !== 3) console.log("5 !== 3: true");
console.log("");

// --- LOGICAL OPERATORS ---
console.log("=== LOGICAL OPERATORS ===");
if (5 > 3 && 10 > 5) console.log("AND: true");
if (5 > 3 || 10 < 5) console.log("OR: true");
if (!(5 < 3)) console.log("NOT: true");
console.log("");

// --- TERNARY OPERATOR ---
console.log("=== TERNARY OPERATOR ===");
var num = 7;
var result = num % 2 == 0 ? "even" : "odd";
console.log(num + " is " + result);
console.log("");

// --- TYPE CONVERSION ---
console.log("=== TYPE CONVERSION ===");
console.log("parseInt('123'): " + parseInt("123"));
console.log("parseFloat('3.14'): " + parseFloat("3.14"));
console.log("String(42): " + String(42));
console.log("Number('123'): " + Number("123"));
console.log("Boolean(1): " + Boolean(1));
console.log("typeof 42: " + typeof 42);
console.log("typeof 'hello': " + typeof "hello");
console.log("");

// --- FINAL MESSAGE ---
console.log("==================================================");
console.log("JAVASCRIPT DEMO COMPLETE!");
console.log("All major JavaScript features demonstrated!");
console.log("==================================================");
