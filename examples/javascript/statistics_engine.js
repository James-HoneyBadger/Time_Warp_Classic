// ═══════════════════════════════════════════════════════
// STATISTICAL ANALYSIS ENGINE
// Comprehensive statistics library with descriptive
// stats, correlation, regression, and probability
// calculations with formatted report output
// ═══════════════════════════════════════════════════════

"use strict";

// ═══════════════════════════════════════
// STATISTICS LIBRARY
// ═══════════════════════════════════════

function sum(arr) {
    let s = 0;
    for (let i = 0; i < arr.length; i++) s += arr[i];
    return s;
}

function mean(arr) {
    return sum(arr) / arr.length;
}

function median(arr) {
    const sorted = arr.slice().sort(function(a, b) { return a - b; });
    const mid = Math.floor(sorted.length / 2);
    if (sorted.length % 2 === 0) {
        return (sorted[mid - 1] + sorted[mid]) / 2;
    }
    return sorted[mid];
}

function mode(arr) {
    const freq = {};
    let maxFreq = 0;
    let modes = [];
    for (let i = 0; i < arr.length; i++) {
        freq[arr[i]] = (freq[arr[i]] || 0) + 1;
        if (freq[arr[i]] > maxFreq) maxFreq = freq[arr[i]];
    }
    for (const key in freq) {
        if (freq[key] === maxFreq) modes.push(Number(key));
    }
    return modes;
}

function variance(arr) {
    const m = mean(arr);
    let sumSq = 0;
    for (let i = 0; i < arr.length; i++) {
        sumSq += (arr[i] - m) * (arr[i] - m);
    }
    return sumSq / arr.length;
}

function stdDev(arr) {
    return Math.sqrt(variance(arr));
}

function sampleVariance(arr) {
    const m = mean(arr);
    let sumSq = 0;
    for (let i = 0; i < arr.length; i++) {
        sumSq += (arr[i] - m) * (arr[i] - m);
    }
    return sumSq / (arr.length - 1);
}

function skewness(arr) {
    const m = mean(arr);
    const sd = stdDev(arr);
    const n = arr.length;
    let sumCubed = 0;
    for (let i = 0; i < n; i++) {
        sumCubed += Math.pow((arr[i] - m) / sd, 3);
    }
    return sumCubed / n;
}

function kurtosis(arr) {
    const m = mean(arr);
    const sd = stdDev(arr);
    const n = arr.length;
    let sumFourth = 0;
    for (let i = 0; i < n; i++) {
        sumFourth += Math.pow((arr[i] - m) / sd, 4);
    }
    return sumFourth / n - 3; // Excess kurtosis
}

function percentile(arr, p) {
    const sorted = arr.slice().sort(function(a, b) { return a - b; });
    const index = (p / 100) * (sorted.length - 1);
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    if (lower === upper) return sorted[lower];
    return sorted[lower] * (upper - index) + sorted[upper] * (index - lower);
}

function iqr(arr) {
    return percentile(arr, 75) - percentile(arr, 25);
}

// ─── Correlation and Regression ───

function correlation(x, y) {
    const n = x.length;
    const mx = mean(x);
    const my = mean(y);
    let sumXY = 0, sumX2 = 0, sumY2 = 0;
    for (let i = 0; i < n; i++) {
        sumXY += (x[i] - mx) * (y[i] - my);
        sumX2 += (x[i] - mx) * (x[i] - mx);
        sumY2 += (y[i] - my) * (y[i] - my);
    }
    return sumXY / Math.sqrt(sumX2 * sumY2);
}

function linearRegression(x, y) {
    const n = x.length;
    const mx = mean(x);
    const my = mean(y);
    let sumXY = 0, sumX2 = 0;
    for (let i = 0; i < n; i++) {
        sumXY += (x[i] - mx) * (y[i] - my);
        sumX2 += (x[i] - mx) * (x[i] - mx);
    }
    const slope = sumXY / sumX2;
    const intercept = my - slope * mx;
    const r = correlation(x, y);
    return { slope: slope, intercept: intercept, r: r, rSquared: r * r };
}

// ─── Z-Score and Outlier Detection ───

function zScores(arr) {
    const m = mean(arr);
    const sd = stdDev(arr);
    return arr.map(function(x) { return (x - m) / sd; });
}

function findOutliers(arr, threshold) {
    threshold = threshold || 2;
    const z = zScores(arr);
    const outliers = [];
    for (let i = 0; i < arr.length; i++) {
        if (Math.abs(z[i]) > threshold) {
            outliers.push({ index: i, value: arr[i], zScore: z[i] });
        }
    }
    return outliers;
}

// ─── Histogram ───

function histogram(arr, bins) {
    const min = Math.min.apply(null, arr);
    const max = Math.max.apply(null, arr);
    const range = max - min;
    const binWidth = range / bins;
    const counts = new Array(bins).fill(0);
    const edges = [];

    for (let i = 0; i <= bins; i++) {
        edges.push(min + i * binWidth);
    }

    for (let i = 0; i < arr.length; i++) {
        let bin = Math.floor((arr[i] - min) / binWidth);
        if (bin >= bins) bin = bins - 1;
        counts[bin]++;
    }

    return { counts: counts, edges: edges, binWidth: binWidth };
}

// ═══════════════════════════════════════
// DATA SETS AND ANALYSIS
// ═══════════════════════════════════════

console.log("═".repeat(62));
console.log("         STATISTICAL ANALYSIS ENGINE v1.0");
console.log("═".repeat(62));
console.log();

// ─── Dataset 1: Student Test Scores ───
const scores = [72, 85, 90, 68, 74, 92, 88, 76, 95, 83,
                67, 79, 91, 86, 73, 88, 94, 71, 82, 87,
                78, 93, 69, 84, 81, 77, 89, 75, 96, 80];

console.log("─".repeat(62));
console.log("  DATASET 1: Student Test Scores (n=" + scores.length + ")");
console.log("─".repeat(62));
console.log();

console.log("  Descriptive Statistics:");
console.log("    Mean:             " + mean(scores).toFixed(2));
console.log("    Median:           " + median(scores).toFixed(2));
console.log("    Mode:             " + mode(scores).join(", "));
console.log("    Std Deviation:    " + stdDev(scores).toFixed(2));
console.log("    Variance:         " + variance(scores).toFixed(2));
console.log("    Skewness:         " + skewness(scores).toFixed(4));
console.log("    Kurtosis:         " + kurtosis(scores).toFixed(4));
console.log("    Min:              " + Math.min.apply(null, scores));
console.log("    Max:              " + Math.max.apply(null, scores));
console.log("    Range:            " + (Math.max.apply(null, scores) - Math.min.apply(null, scores)));
console.log();

console.log("  Percentiles:");
console.log("    25th (Q1):        " + percentile(scores, 25).toFixed(2));
console.log("    50th (Median):    " + percentile(scores, 50).toFixed(2));
console.log("    75th (Q3):        " + percentile(scores, 75).toFixed(2));
console.log("    90th:             " + percentile(scores, 90).toFixed(2));
console.log("    IQR:              " + iqr(scores).toFixed(2));
console.log();

// Histogram
console.log("  Score Distribution (Histogram):");
const hist = histogram(scores, 6);
const maxCount = Math.max.apply(null, hist.counts);
for (let i = 0; i < hist.counts.length; i++) {
    const lo = hist.edges[i].toFixed(0);
    const hi = hist.edges[i + 1].toFixed(0);
    const bar = "#".repeat(Math.round(hist.counts[i] / maxCount * 30));
    const label = (lo + "-" + hi).padEnd(10);
    console.log("    " + label + " " + String(hist.counts[i]).padStart(3) + " " + bar);
}
console.log();

// ─── Dataset 2: Correlation Analysis ───
console.log("─".repeat(62));
console.log("  DATASET 2: Study Hours vs Test Scores");
console.log("─".repeat(62));
console.log();

const studyHours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 4, 6, 8, 3, 5, 7, 9, 10];
const testScores = [55, 62, 68, 72, 78, 82, 88, 91, 95, 93, 97, 45, 65, 75, 85, 58, 70, 80, 90, 92];

console.log("  Study Hours: " + studyHours.join(", "));
console.log("  Test Scores: " + testScores.join(", "));
console.log();

const reg = linearRegression(studyHours, testScores);
console.log("  Correlation Analysis:");
console.log("    Pearson r:        " + reg.r.toFixed(4));
console.log("    R-squared:        " + reg.rSquared.toFixed(4) + " (" + (reg.rSquared * 100).toFixed(1) + "% variance explained)");
console.log("    Regression:       y = " + reg.slope.toFixed(2) + "x + " + reg.intercept.toFixed(2));
console.log();

const strength = Math.abs(reg.r);
const corrLabel = strength > 0.9 ? "Very Strong" :
                  strength > 0.7 ? "Strong" :
                  strength > 0.5 ? "Moderate" :
                  strength > 0.3 ? "Weak" : "Very Weak";
console.log("    Correlation Strength: " + corrLabel + " " + (reg.r > 0 ? "Positive" : "Negative"));
console.log();

console.log("  Predictions (from regression):");
console.log("    5 hours study  -> Score: " + (reg.slope * 5 + reg.intercept).toFixed(1));
console.log("    8 hours study  -> Score: " + (reg.slope * 8 + reg.intercept).toFixed(1));
console.log("    12 hours study -> Score: " + (reg.slope * 12 + reg.intercept).toFixed(1));
console.log();

// ─── Dataset 3: Outlier Detection ───
console.log("─".repeat(62));
console.log("  DATASET 3: Outlier Detection");
console.log("─".repeat(62));
console.log();

const salesData = [120, 135, 128, 142, 130, 125, 290, 131, 127, 138,
                   133, 18, 136, 129, 140, 134, 126, 137, 132, 141];

console.log("  Monthly Sales: " + salesData.join(", "));
console.log("  Mean: " + mean(salesData).toFixed(2) + "  StdDev: " + stdDev(salesData).toFixed(2));
console.log();

const outliers = findOutliers(salesData, 1.5);
if (outliers.length > 0) {
    console.log("  Outliers Detected (|z| > 1.5):");
    for (let i = 0; i < outliers.length; i++) {
        const o = outliers[i];
        const direction = o.zScore > 0 ? "above" : "below";
        console.log("    Index " + o.index + ": value=" + o.value +
                    " (z=" + o.zScore.toFixed(2) + ", " + direction + " mean)");
    }
} else {
    console.log("  No outliers detected.");
}
console.log();

// Remove outliers and recalculate
const cleanData = salesData.filter(function(val, idx) {
    return !outliers.some(function(o) { return o.index === idx; });
});
console.log("  After removing outliers:");
console.log("    New Mean:    " + mean(cleanData).toFixed(2) + " (was " + mean(salesData).toFixed(2) + ")");
console.log("    New StdDev:  " + stdDev(cleanData).toFixed(2) + " (was " + stdDev(salesData).toFixed(2) + ")");
console.log();

// ─── Dataset 4: Multi-variable comparison ───
console.log("─".repeat(62));
console.log("  DATASET 4: Department Performance Comparison");
console.log("─".repeat(62));
console.log();

const departments = {
    Engineering: [92, 88, 95, 91, 87, 93, 89, 94, 90, 96],
    Marketing:   [78, 82, 75, 80, 85, 77, 83, 79, 81, 76],
    Sales:       [88, 92, 85, 90, 87, 93, 89, 91, 86, 94],
    Support:     [70, 75, 72, 68, 74, 71, 77, 73, 69, 76]
};

console.log("  Department     Mean    Median  StdDev  Min   Max   Range");
console.log("  " + "-".repeat(56));

for (const dept in departments) {
    const d = departments[dept];
    console.log("  " + dept.padEnd(15) +
                mean(d).toFixed(1).padStart(6) + "   " +
                median(d).toFixed(1).padStart(6) + "  " +
                stdDev(d).toFixed(1).padStart(6) + "  " +
                String(Math.min.apply(null, d)).padStart(4) + "  " +
                String(Math.max.apply(null, d)).padStart(4) + "   " +
                String(Math.max.apply(null, d) - Math.min.apply(null, d)).padStart(4));
}
console.log();

// Bar chart comparison
console.log("  Mean Performance Bar Chart:");
for (const dept in departments) {
    const m = mean(departments[dept]);
    const bar = "#".repeat(Math.round(m / 2));
    console.log("    " + dept.padEnd(15) + bar + " " + m.toFixed(1));
}
console.log();

// ─── Probability ───
console.log("─".repeat(62));
console.log("  PROBABILITY CALCULATIONS");
console.log("─".repeat(62));
console.log();

console.log("  Normal Distribution Z-Score Table:");
console.log("  z       P(Z<z)    P(Z>z)");
console.log("  " + "-".repeat(35));

// Approximate CDF using error function approximation
function normalCDF(z) {
    const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
    const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    const sign = z < 0 ? -1 : 1;
    z = Math.abs(z) / Math.sqrt(2);
    const t = 1.0 / (1.0 + p * z);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-z * z);
    return 0.5 * (1.0 + sign * y);
}

const zValues = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3];
for (let i = 0; i < zValues.length; i++) {
    const z = zValues[i];
    const pLess = normalCDF(z);
    console.log("  " + (z >= 0 ? " " : "") + z.toFixed(1) + "     " +
                pLess.toFixed(4) + "    " + (1 - pLess).toFixed(4));
}

console.log();
console.log("═".repeat(62));
console.log("  Statistical Analysis Engine Complete");
console.log("  Modules: Descriptive, Correlation, Outlier, Probability");
console.log("═".repeat(62));
