// ====================================
//    JavaScript Demo - Modern Web Language
// ====================================

console.log("Welcome to Time Warp JavaScript!");
console.log("JavaScript is the language of the web.\n");

// === Variables and Constants ===
console.log("=== Variables and Constants ===");
const PI = 3.14159;
let counter = 0;
var oldStyle = "still works but let/const preferred";

console.log(`PI = ${PI}`);
console.log(`Counter = ${counter}\n`);

// === Arrays and Methods ===
console.log("=== Array Operations ===");
const languages = ['BASIC', 'Logo', 'Pascal', 'Python', 'JavaScript'];

console.log(`Languages: ${languages.join(', ')}`);
console.log(`Total: ${languages.length} languages`);

// Array methods
const upperLanguages = languages.map(lang => lang.toUpperCase());
console.log(`Uppercase: ${upperLanguages.join(', ')}`);

const shortNames = languages.filter(lang => lang.length <= 5);
console.log(`Short names: ${shortNames.join(', ')}\n`);

// === Objects ===
console.log("=== Object Demonstration ===");
const language = {
    name: 'JavaScript',
    year: 1995,
    creator: 'Brendan Eich',
    paradigm: 'Multi-paradigm',
    
    describe() {
        return `${this.name} was created by ${this.creator} in ${this.year}`;
    }
};

console.log(language.describe());
console.log(`Paradigm: ${language.paradigm}\n`);

// === Functions ===
console.log("=== Function Demonstrations ===");

// Traditional function
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(`5! = ${factorial(5)}`);

// Arrow function
const square = x => x * x;
console.log(`Square of 7 = ${square(7)}`);

// Function with multiple parameters
const greet = (name, time = 'day') => `Good ${time}, ${name}!`;
console.log(greet('User'));
console.log(greet('Programmer', 'evening'));
console.log();

// === Classes (ES6+) ===
console.log("=== Class Example ===");

class ProgrammingLanguage {
    constructor(name, year, paradigm) {
        this.name = name;
        this.year = year;
        this.paradigm = paradigm;
    }
    
    isVintage() {
        return this.year < 1980;
    }
    
    toString() {
        const age = new Date().getFullYear() - this.year;
        return `${this.name} (${this.year}, ${age} years old): ${this.paradigm}`;
    }
}

const langs = [
    new ProgrammingLanguage('JavaScript', 1995, 'Multi-paradigm'),
    new ProgrammingLanguage('Logo', 1967, 'Educational'),
    new ProgrammingLanguage('Python', 1991, 'Multi-paradigm')
];

langs.forEach(lang => {
    const vintage = lang.isVintage() ? 'vintage' : 'modern';
    console.log(`${lang.toString()} - ${vintage}`);
});
console.log();

// === Promises (Async) ===
console.log("=== Async Programming ===");

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function countdown() {
    console.log("Countdown starting...");
    for (let i = 5; i > 0; i--) {
        console.log(i);
        await delay(100);  // Simulated delay
    }
    console.log("Liftoff!");
}

// Note: In actual async execution, this would wait
console.log("(Async countdown would execute here)");
console.log();

// === Template Literals and String Methods ===
console.log("=== String Operations ===");
const text = "The Quick Brown Fox Jumps Over The Lazy Dog";
console.log(`Original: ${text}`);
console.log(`Lowercase: ${text.toLowerCase()}`);
console.log(`Word count: ${text.split(' ').length}`);
console.log(`Contains 'Fox': ${text.includes('Fox')}`);
console.log();

// === Spread Operator and Destructuring ===
console.log("=== Modern JS Features ===");
const numbers = [1, 2, 3];
const moreNumbers = [...numbers, 4, 5, 6];
console.log(`Spread: ${moreNumbers.join(', ')}`);

const [first, second, ...rest] = moreNumbers;
console.log(`First: ${first}, Second: ${second}, Rest: ${rest.join(', ')}`);

const { name, year } = language;
console.log(`Destructured: ${name}, ${year}`);
console.log();

console.log("JavaScript demo complete!");
