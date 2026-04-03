// ═══════════════════════════════════════════════════════
// SORTING ALGORITHM SHOWCASE
// Implements and benchmarks 5 sorting algorithms with
// visual step tracking and performance comparison
// ═══════════════════════════════════════════════════════

"use strict";

// ─── Utility Functions ───

function generateArray(size, maxVal) {
    const arr = [];
    let seed = 42;
    for (let i = 0; i < size; i++) {
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        arr.push(seed % maxVal);
    }
    return arr;
}

function isSorted(arr) {
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] < arr[i - 1]) return false;
    }
    return true;
}

function formatArray(arr, maxShow) {
    maxShow = maxShow || 20;
    if (arr.length <= maxShow) return "[" + arr.join(", ") + "]";
    const first = arr.slice(0, 10).join(", ");
    const last = arr.slice(-5).join(", ");
    return "[" + first + ", ... , " + last + "] (" + arr.length + " elements)";
}

// ═══════════════════════════════════════
// SORTING ALGORITHMS
// ═══════════════════════════════════════

// ─── Bubble Sort ───
function bubbleSort(arr) {
    const a = arr.slice();
    let comparisons = 0, swaps = 0;
    const n = a.length;
    for (let i = 0; i < n - 1; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            comparisons++;
            if (a[j] > a[j + 1]) {
                const tmp = a[j]; a[j] = a[j + 1]; a[j + 1] = tmp;
                swaps++;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return { sorted: a, comparisons: comparisons, swaps: swaps, name: "Bubble Sort" };
}

// ─── Selection Sort ───
function selectionSort(arr) {
    const a = arr.slice();
    let comparisons = 0, swaps = 0;
    const n = a.length;
    for (let i = 0; i < n - 1; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            comparisons++;
            if (a[j] < a[minIdx]) minIdx = j;
        }
        if (minIdx !== i) {
            const tmp = a[i]; a[i] = a[minIdx]; a[minIdx] = tmp;
            swaps++;
        }
    }
    return { sorted: a, comparisons: comparisons, swaps: swaps, name: "Selection Sort" };
}

// ─── Insertion Sort ───
function insertionSort(arr) {
    const a = arr.slice();
    let comparisons = 0, swaps = 0;
    const n = a.length;
    for (let i = 1; i < n; i++) {
        const key = a[i];
        let j = i - 1;
        while (j >= 0) {
            comparisons++;
            if (a[j] > key) {
                a[j + 1] = a[j];
                swaps++;
                j--;
            } else {
                break;
            }
        }
        a[j + 1] = key;
    }
    return { sorted: a, comparisons: comparisons, swaps: swaps, name: "Insertion Sort" };
}

// ─── Merge Sort ───
function mergeSort(arr) {
    let comparisons = 0, swaps = 0;

    function merge(left, right) {
        const result = [];
        let li = 0, ri = 0;
        while (li < left.length && ri < right.length) {
            comparisons++;
            if (left[li] <= right[ri]) {
                result.push(left[li++]);
            } else {
                result.push(right[ri++]);
                swaps++;
            }
        }
        while (li < left.length) result.push(left[li++]);
        while (ri < right.length) result.push(right[ri++]);
        return result;
    }

    function sort(a) {
        if (a.length <= 1) return a;
        const mid = Math.floor(a.length / 2);
        const left = sort(a.slice(0, mid));
        const right = sort(a.slice(mid));
        return merge(left, right);
    }

    const sorted = sort(arr.slice());
    return { sorted: sorted, comparisons: comparisons, swaps: swaps, name: "Merge Sort" };
}

// ─── Quick Sort ───
function quickSort(arr) {
    let comparisons = 0, swaps = 0;

    function sort(a, lo, hi) {
        if (lo >= hi) return;
        const pivot = a[Math.floor((lo + hi) / 2)];
        let i = lo, j = hi;
        while (i <= j) {
            while (a[i] < pivot) { comparisons++; i++; }
            while (a[j] > pivot) { comparisons++; j--; }
            comparisons += 2;
            if (i <= j) {
                const tmp = a[i]; a[i] = a[j]; a[j] = tmp;
                swaps++;
                i++; j--;
            }
        }
        if (lo < j) sort(a, lo, j);
        if (i < hi) sort(a, i, hi);
    }

    const a = arr.slice();
    sort(a, 0, a.length - 1);
    return { sorted: a, comparisons: comparisons, swaps: swaps, name: "Quick Sort" };
}

// ═══════════════════════════════════════
// REPORT GENERATION
// ═══════════════════════════════════════

console.log("═".repeat(62));
console.log("         SORTING ALGORITHM SHOWCASE v1.0");
console.log("═".repeat(62));
console.log();

// ─── Small Array Demo with Step Tracking ───
console.log("─".repeat(62));
console.log("  SMALL ARRAY DEMONSTRATION");
console.log("─".repeat(62));
const smallArr = [64, 25, 12, 22, 11, 90, 45, 33];
console.log("  Input: " + formatArray(smallArr));
console.log();

const smallResults = [
    bubbleSort(smallArr),
    selectionSort(smallArr),
    insertionSort(smallArr),
    mergeSort(smallArr),
    quickSort(smallArr),
];

for (const r of smallResults) {
    console.log("  " + r.name + ":");
    console.log("    Result:      " + formatArray(r.sorted));
    console.log("    Comparisons: " + r.comparisons);
    console.log("    Swaps:       " + r.swaps);
    console.log("    Correct:     " + (isSorted(r.sorted) ? "YES" : "NO"));
    console.log();
}

// ─── Performance Comparison at Different Sizes ───
console.log("─".repeat(62));
console.log("  PERFORMANCE COMPARISON");
console.log("─".repeat(62));
console.log();

const sizes = [50, 100, 200, 500];
const algorithms = [bubbleSort, selectionSort, insertionSort, mergeSort, quickSort];
const algoNames = ["Bubble", "Selection", "Insertion", "Merge", "Quick"];

console.log("  Comparisons by Array Size:");
console.log("  " + "-".repeat(58));
let header = "  Size    ";
for (const name of algoNames) {
    header += name.padEnd(12);
}
console.log(header);
console.log("  " + "-".repeat(58));

for (const size of sizes) {
    const testArr = generateArray(size, 1000);
    let row = "  " + String(size).padEnd(10);
    for (const algo of algorithms) {
        const result = algo(testArr);
        row += String(result.comparisons).padEnd(12);
    }
    console.log(row);
}
console.log();

console.log("  Swaps by Array Size:");
console.log("  " + "-".repeat(58));
header = "  Size    ";
for (const name of algoNames) {
    header += name.padEnd(12);
}
console.log(header);
console.log("  " + "-".repeat(58));

for (const size of sizes) {
    const testArr = generateArray(size, 1000);
    let row = "  " + String(size).padEnd(10);
    for (const algo of algorithms) {
        const result = algo(testArr);
        row += String(result.swaps).padEnd(12);
    }
    console.log(row);
}
console.log();

// ─── Best/Worst Case Analysis ───
console.log("─".repeat(62));
console.log("  BEST & WORST CASE ANALYSIS (n=100)");
console.log("─".repeat(62));
console.log();

// Already sorted (best case for some)
const sortedArr = [];
for (let i = 0; i < 100; i++) sortedArr.push(i);

// Reverse sorted (worst case for some)
const reverseArr = sortedArr.slice().reverse();

// Random
const randomArr = generateArray(100, 1000);

const scenarios = [
    { name: "Already Sorted", data: sortedArr },
    { name: "Reverse Sorted", data: reverseArr },
    { name: "Random Data   ", data: randomArr },
];

for (const scenario of scenarios) {
    console.log("  " + scenario.name + ":");
    for (let ai = 0; ai < algorithms.length; ai++) {
        const result = algorithms[ai](scenario.data);
        const bar = "#".repeat(Math.min(Math.floor(result.comparisons / 100), 40));
        console.log("    " + algoNames[ai].padEnd(12) + String(result.comparisons).padEnd(8) + "comps  " + bar);
    }
    console.log();
}

// ─── Efficiency Rankings ───
console.log("─".repeat(62));
console.log("  ALGORITHM EFFICIENCY RANKINGS (n=500, random)");
console.log("─".repeat(62));
console.log();

const benchArr = generateArray(500, 10000);
const benchResults = algorithms.map(function(algo, i) {
    const r = algo(benchArr);
    return { name: algoNames[i], comparisons: r.comparisons, swaps: r.swaps,
             total: r.comparisons + r.swaps };
});

benchResults.sort(function(x, y) { return x.total - y.total; });

console.log("  Rank  Algorithm     Comparisons  Swaps      Total Ops");
console.log("  " + "-".repeat(56));

for (let i = 0; i < benchResults.length; i++) {
    const br = benchResults[i];
    const medal = i === 0 ? " *** WINNER" : "";
    console.log("  " + String(i + 1).padEnd(6) +
                br.name.padEnd(14) +
                String(br.comparisons).padEnd(13) +
                String(br.swaps).padEnd(11) +
                String(br.total) + medal);
}

console.log();
console.log("  Theoretical Complexity:");
console.log("    Bubble Sort:    O(n^2)   - Simple but slow");
console.log("    Selection Sort: O(n^2)   - Fewer swaps than bubble");
console.log("    Insertion Sort: O(n^2)   - Fast on nearly-sorted data");
console.log("    Merge Sort:     O(n lgn) - Consistent, stable sort");
console.log("    Quick Sort:     O(n lgn) - Usually fastest in practice");

console.log();
console.log("═".repeat(62));
console.log("  Sorting Algorithm Showcase Complete");
console.log("═".repeat(62));
