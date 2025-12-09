#!/usr/bin/env node
/**
 * JavaScript Data Structures Demo
 * Demonstrates arrays, objects, and modern JavaScript features
 */

// Sample data
const students = [
    { name: "Alice", age: 20, grade: "A", scores: [85, 92, 88] },
    { name: "Bob", age: 19, grade: "B", scores: [78, 81, 85] },
    { name: "Charlie", age: 21, grade: "A", scores: [96, 89, 94] },
    { name: "Diana", age: 20, grade: "C", scores: [72, 75, 78] }
];

console.log("JavaScript Data Structures Demo");
console.log("=================================");
console.log();

// Display all students
console.log("Student Records:");
students.forEach((student, index) => {
    console.log(`${index + 1}. ${student.name} (Age: ${student.age}, Grade: ${student.grade})`);
});
console.log();

// Calculate average scores
console.log("Average Scores:");
students.forEach(student => {
    const avgScore = student.scores.reduce((sum, score) => sum + score, 0) / student.scores.length;
    console.log(`${student.name}: ${avgScore.toFixed(1)}`);
});
console.log();

// Filter high performers
const highPerformers = students.filter(student => {
    const avgScore = student.scores.reduce((sum, score) => sum + score, 0) / student.scores.length;
    return avgScore >= 85;
});

console.log("High Performers (Average ≥ 85):");
highPerformers.forEach(student => {
    console.log(`- ${student.name}`);
});
console.log();

// Sort by age
const sortedByAge = [...students].sort((a, b) => a.age - b.age);
console.log("Students Sorted by Age:");
sortedByAge.forEach(student => {
    console.log(`- ${student.name}: ${student.age} years old`);
});
console.log();

// Grade distribution
const gradeCount = students.reduce((acc, student) => {
    acc[student.grade] = (acc[student.grade] || 0) + 1;
    return acc;
}, {});

console.log("Grade Distribution:");
Object.entries(gradeCount).forEach(([grade, count]) => {
    console.log(`${grade}: ${count} student(s)`);
});

console.log();
console.log("Data structures demo complete!");