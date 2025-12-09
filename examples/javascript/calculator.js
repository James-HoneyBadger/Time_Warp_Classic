#!/usr/bin/env node
/**
 * JavaScript Interactive Calculator Demo
 * Demonstrates basic JavaScript operations and user interaction
 */

const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function askQuestion(question) {
    return new Promise((resolve) => {
        rl.question(question, resolve);
    });
}

async function calculator() {
    console.log("JavaScript Interactive Calculator");
    console.log("=================================");
    console.log();

    while (true) {
        console.log("Available operations:");
        console.log("1. Addition (+)");
        console.log("2. Subtraction (-)");
        console.log("3. Multiplication (*)");
        console.log("4. Division (/)");
        console.log("5. Exit");
        console.log();

        const choice = await askQuestion("Choose an operation (1-5): ");

        if (choice === '5') {
            console.log("Thanks for using the calculator!");
            break;
        }

        const num1 = parseFloat(await askQuestion("Enter first number: "));
        const num2 = parseFloat(await askQuestion("Enter second number: "));

        if (isNaN(num1) || isNaN(num2)) {
            console.log("❌ Please enter valid numbers!");
            console.log();
            continue;
        }

        let result;
        let operation;

        switch (choice) {
            case '1':
                result = num1 + num2;
                operation = '+';
                break;
            case '2':
                result = num1 - num2;
                operation = '-';
                break;
            case '3':
                result = num1 * num2;
                operation = '*';
                break;
            case '4':
                if (num2 === 0) {
                    console.log("❌ Cannot divide by zero!");
                    console.log();
                    continue;
                }
                result = num1 / num2;
                operation = '/';
                break;
            default:
                console.log("❌ Invalid choice!");
                console.log();
                continue;
        }

        console.log(`Result: ${num1} ${operation} ${num2} = ${result}`);
        console.log();
    }

    rl.close();
}

// Run the calculator
calculator();