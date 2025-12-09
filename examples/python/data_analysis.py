#!/usr/bin/env python3
"""
Python Data Analysis Demo
Demonstrates basic data processing and visualization concepts
"""

# Sample data
scores = [85, 92, 78, 96, 88, 73, 89, 91, 84, 87]

print("Python Data Analysis Demo")
print("=" * 30)
print()

print("Student Scores:", scores)
print()

# Calculate statistics
total = sum(scores)
average = total / len(scores)
maximum = max(scores)
minimum = min(scores)

print(f"Total students: {len(scores)}")
print(f"Average score: {average:.1f}")
print(f"Highest score: {maximum}")
print(f"Lowest score: {minimum}")
print()

# Count grades
grades = {"A": 0, "B": 0, "C": 0, "F": 0}
for score in scores:
    if score >= 90:
        grades["A"] += 1
    elif score >= 80:
        grades["B"] += 1
    elif score >= 70:
        grades["C"] += 1
    else:
        grades["F"] += 1

print("Grade Distribution:")
for grade, count in grades.items():
    print(f"  {grade}: {count} students")

print()
print("Analysis complete!")
