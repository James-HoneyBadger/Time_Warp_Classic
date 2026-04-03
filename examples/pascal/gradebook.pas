PROGRAM StudentGradeBook;

{ ═══════════════════════════════════════════════════ }
{ STUDENT GRADE BOOK                                 }
{ Weighted grade calculator with class-wide analysis }
{ ═══════════════════════════════════════════════════ }

CONST HONOR_THRESHOLD = 90;
CONST MERIT_THRESHOLD = 80;
CONST PASS_THRESHOLD = 60;
CONST MATH_WEIGHT = 30;
CONST SCIENCE_WEIGHT = 25;
CONST ENGLISH_WEIGHT = 25;
CONST HISTORY_WEIGHT = 20;

{ ─── Student 1: Alice ─── }
VAR S1_NAME : STRING;
VAR S1_MATH : REAL;
VAR S1_SCI : REAL;
VAR S1_ENG : REAL;
VAR S1_HIST : REAL;
VAR S1_WAVG : REAL;
VAR S1_AVG : REAL;

S1_NAME := 'Alice Johnson';
S1_MATH := 95;
S1_SCI := 92;
S1_ENG := 88;
S1_HIST := 91;
S1_AVG := (S1_MATH + S1_SCI + S1_ENG + S1_HIST) / 4;
S1_WAVG := (S1_MATH * MATH_WEIGHT + S1_SCI * SCIENCE_WEIGHT + S1_ENG * ENGLISH_WEIGHT + S1_HIST * HISTORY_WEIGHT) / 100;

{ ─── Student 2: Bob ─── }
VAR S2_NAME : STRING;
VAR S2_MATH : REAL;
VAR S2_SCI : REAL;
VAR S2_ENG : REAL;
VAR S2_HIST : REAL;
VAR S2_WAVG : REAL;
VAR S2_AVG : REAL;

S2_NAME := 'Bob Martinez';
S2_MATH := 78;
S2_SCI := 85;
S2_ENG := 92;
S2_HIST := 88;
S2_AVG := (S2_MATH + S2_SCI + S2_ENG + S2_HIST) / 4;
S2_WAVG := (S2_MATH * MATH_WEIGHT + S2_SCI * SCIENCE_WEIGHT + S2_ENG * ENGLISH_WEIGHT + S2_HIST * HISTORY_WEIGHT) / 100;

{ ─── Student 3: Carol ─── }
VAR S3_NAME : STRING;
VAR S3_MATH : REAL;
VAR S3_SCI : REAL;
VAR S3_ENG : REAL;
VAR S3_HIST : REAL;
VAR S3_WAVG : REAL;
VAR S3_AVG : REAL;

S3_NAME := 'Carol Chen';
S3_MATH := 100;
S3_SCI := 97;
S3_ENG := 95;
S3_HIST := 98;
S3_AVG := (S3_MATH + S3_SCI + S3_ENG + S3_HIST) / 4;
S3_WAVG := (S3_MATH * MATH_WEIGHT + S3_SCI * SCIENCE_WEIGHT + S3_ENG * ENGLISH_WEIGHT + S3_HIST * HISTORY_WEIGHT) / 100;

{ ─── Student 4: David ─── }
VAR S4_NAME : STRING;
VAR S4_MATH : REAL;
VAR S4_SCI : REAL;
VAR S4_ENG : REAL;
VAR S4_HIST : REAL;
VAR S4_WAVG : REAL;
VAR S4_AVG : REAL;

S4_NAME := 'David Park';
S4_MATH := 65;
S4_SCI := 72;
S4_ENG := 58;
S4_HIST := 70;
S4_AVG := (S4_MATH + S4_SCI + S4_ENG + S4_HIST) / 4;
S4_WAVG := (S4_MATH * MATH_WEIGHT + S4_SCI * SCIENCE_WEIGHT + S4_ENG * ENGLISH_WEIGHT + S4_HIST * HISTORY_WEIGHT) / 100;

{ ─── Student 5: Eva ─── }
VAR S5_NAME : STRING;
VAR S5_MATH : REAL;
VAR S5_SCI : REAL;
VAR S5_ENG : REAL;
VAR S5_HIST : REAL;
VAR S5_WAVG : REAL;
VAR S5_AVG : REAL;

S5_NAME := 'Eva Williams';
S5_MATH := 82;
S5_SCI := 79;
S5_ENG := 91;
S5_HIST := 85;
S5_AVG := (S5_MATH + S5_SCI + S5_ENG + S5_HIST) / 4;
S5_WAVG := (S5_MATH * MATH_WEIGHT + S5_SCI * SCIENCE_WEIGHT + S5_ENG * ENGLISH_WEIGHT + S5_HIST * HISTORY_WEIGHT) / 100;

{ ═══════════════════════════════════════════════════ }
{ REPORT OUTPUT                                      }
{ ═══════════════════════════════════════════════════ }

WRITELN('════════════════════════════════════════════════════════════');
WRITELN('                 STUDENT GRADE BOOK v1.0');
WRITELN('         Weighted Grade Calculator & Analysis');
WRITELN('════════════════════════════════════════════════════════════');
WRITELN('');
WRITELN('  Weights: Math=30%  Science=25%  English=25%  History=20%');
WRITELN('');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  INDIVIDUAL STUDENT REPORTS');
WRITELN('────────────────────────────────────────────────────────────');

WRITELN('');
WRITELN('  1. ', S1_NAME);
WRITELN('     Math: ', S1_MATH, '   Science: ', S1_SCI, '   English: ', S1_ENG, '   History: ', S1_HIST);
WRITELN('     Simple Average: ', S1_AVG, '   Weighted Average: ', S1_WAVG);
IF S1_WAVG >= 90 THEN WRITELN('     Classification: HONOR ROLL');
IF (S1_WAVG >= 80) AND (S1_WAVG < 90) THEN WRITELN('     Classification: MERIT');
IF (S1_WAVG >= 60) AND (S1_WAVG < 80) THEN WRITELN('     Classification: PASS');
IF S1_WAVG < 60 THEN WRITELN('     Classification: NEEDS IMPROVEMENT');

WRITELN('');
WRITELN('  2. ', S2_NAME);
WRITELN('     Math: ', S2_MATH, '   Science: ', S2_SCI, '   English: ', S2_ENG, '   History: ', S2_HIST);
WRITELN('     Simple Average: ', S2_AVG, '   Weighted Average: ', S2_WAVG);
IF S2_WAVG >= 90 THEN WRITELN('     Classification: HONOR ROLL');
IF (S2_WAVG >= 80) AND (S2_WAVG < 90) THEN WRITELN('     Classification: MERIT');
IF (S2_WAVG >= 60) AND (S2_WAVG < 80) THEN WRITELN('     Classification: PASS');
IF S2_WAVG < 60 THEN WRITELN('     Classification: NEEDS IMPROVEMENT');

WRITELN('');
WRITELN('  3. ', S3_NAME);
WRITELN('     Math: ', S3_MATH, '   Science: ', S3_SCI, '   English: ', S3_ENG, '   History: ', S3_HIST);
WRITELN('     Simple Average: ', S3_AVG, '   Weighted Average: ', S3_WAVG);
IF S3_WAVG >= 90 THEN WRITELN('     Classification: HONOR ROLL');
IF (S3_WAVG >= 80) AND (S3_WAVG < 90) THEN WRITELN('     Classification: MERIT');
IF (S3_WAVG >= 60) AND (S3_WAVG < 80) THEN WRITELN('     Classification: PASS');
IF S3_WAVG < 60 THEN WRITELN('     Classification: NEEDS IMPROVEMENT');

WRITELN('');
WRITELN('  4. ', S4_NAME);
WRITELN('     Math: ', S4_MATH, '   Science: ', S4_SCI, '   English: ', S4_ENG, '   History: ', S4_HIST);
WRITELN('     Simple Average: ', S4_AVG, '   Weighted Average: ', S4_WAVG);
IF S4_WAVG >= 90 THEN WRITELN('     Classification: HONOR ROLL');
IF (S4_WAVG >= 80) AND (S4_WAVG < 90) THEN WRITELN('     Classification: MERIT');
IF (S4_WAVG >= 60) AND (S4_WAVG < 80) THEN WRITELN('     Classification: PASS');
IF S4_WAVG < 60 THEN WRITELN('     Classification: NEEDS IMPROVEMENT');

WRITELN('');
WRITELN('  5. ', S5_NAME);
WRITELN('     Math: ', S5_MATH, '   Science: ', S5_SCI, '   English: ', S5_ENG, '   History: ', S5_HIST);
WRITELN('     Simple Average: ', S5_AVG, '   Weighted Average: ', S5_WAVG);
IF S5_WAVG >= 90 THEN WRITELN('     Classification: HONOR ROLL');
IF (S5_WAVG >= 80) AND (S5_WAVG < 90) THEN WRITELN('     Classification: MERIT');
IF (S5_WAVG >= 60) AND (S5_WAVG < 80) THEN WRITELN('     Classification: PASS');
IF S5_WAVG < 60 THEN WRITELN('     Classification: NEEDS IMPROVEMENT');

{ ─── Class-wide Statistics ─── }
VAR CLASS_MATH : REAL;
VAR CLASS_SCI : REAL;
VAR CLASS_ENG : REAL;
VAR CLASS_HIST : REAL;
VAR CLASS_OVERALL : REAL;
VAR HIGHEST : REAL;
VAR LOWEST : REAL;

CLASS_MATH := (S1_MATH + S2_MATH + S3_MATH + S4_MATH + S5_MATH) / 5;
CLASS_SCI := (S1_SCI + S2_SCI + S3_SCI + S4_SCI + S5_SCI) / 5;
CLASS_ENG := (S1_ENG + S2_ENG + S3_ENG + S4_ENG + S5_ENG) / 5;
CLASS_HIST := (S1_HIST + S2_HIST + S3_HIST + S4_HIST + S5_HIST) / 5;
CLASS_OVERALL := (S1_WAVG + S2_WAVG + S3_WAVG + S4_WAVG + S5_WAVG) / 5;

HIGHEST := MAX(MAX(MAX(S1_WAVG, S2_WAVG), MAX(S3_WAVG, S4_WAVG)), S5_WAVG);
LOWEST := MIN(MIN(MIN(S1_WAVG, S2_WAVG), MIN(S3_WAVG, S4_WAVG)), S5_WAVG);

WRITELN('');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  CLASS-WIDE STATISTICS');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Subject Averages:');
WRITELN('    Mathematics:  ', CLASS_MATH);
WRITELN('    Science:      ', CLASS_SCI);
WRITELN('    English:      ', CLASS_ENG);
WRITELN('    History:      ', CLASS_HIST);
WRITELN('');
WRITELN('  Overall Weighted Class Average: ', CLASS_OVERALL);
WRITELN('  Highest Weighted Average:       ', HIGHEST);
WRITELN('  Lowest Weighted Average:        ', LOWEST);
WRITELN('  Spread (High - Low):            ', HIGHEST - LOWEST);

{ ─── Standard Deviation ─── }
VAR VARIANCE : REAL;
VAR STDDEV : REAL;

VARIANCE := ((S1_WAVG - CLASS_OVERALL) * (S1_WAVG - CLASS_OVERALL) + (S2_WAVG - CLASS_OVERALL) * (S2_WAVG - CLASS_OVERALL) + (S3_WAVG - CLASS_OVERALL) * (S3_WAVG - CLASS_OVERALL) + (S4_WAVG - CLASS_OVERALL) * (S4_WAVG - CLASS_OVERALL) + (S5_WAVG - CLASS_OVERALL) * (S5_WAVG - CLASS_OVERALL)) / 5;
STDDEV := SQRT(VARIANCE);

WRITELN('  Variance:                       ', VARIANCE);
WRITELN('  Standard Deviation:             ', STDDEV);

WRITELN('');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  HONOR ROLL');
WRITELN('────────────────────────────────────────────────────────────');
IF S1_WAVG >= 90 THEN WRITELN('    ', S1_NAME, '  (', S1_WAVG, ')');
IF S2_WAVG >= 90 THEN WRITELN('    ', S2_NAME, '  (', S2_WAVG, ')');
IF S3_WAVG >= 90 THEN WRITELN('    ', S3_NAME, '  (', S3_WAVG, ')');
IF S4_WAVG >= 90 THEN WRITELN('    ', S4_NAME, '  (', S4_WAVG, ')');
IF S5_WAVG >= 90 THEN WRITELN('    ', S5_NAME, '  (', S5_WAVG, ')');

WRITELN('');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  NEEDS ATTENTION (Below ', PASS_THRESHOLD, ')');
WRITELN('────────────────────────────────────────────────────────────');
IF S1_WAVG < 60 THEN WRITELN('    ', S1_NAME, '  (', S1_WAVG, ')');
IF S2_WAVG < 60 THEN WRITELN('    ', S2_NAME, '  (', S2_WAVG, ')');
IF S3_WAVG < 60 THEN WRITELN('    ', S3_NAME, '  (', S3_WAVG, ')');
IF S4_WAVG < 60 THEN WRITELN('    ', S4_NAME, '  (', S4_WAVG, ')');
IF S5_WAVG < 60 THEN WRITELN('    ', S5_NAME, '  (', S5_WAVG, ')');

WRITELN('');
WRITELN('════════════════════════════════════════════════════════════');
WRITELN('  Grade Book Report Complete');
WRITELN('════════════════════════════════════════════════════════════');

END.
