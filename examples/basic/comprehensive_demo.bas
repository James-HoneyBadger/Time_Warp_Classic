REM =========================================================
REM COMPREHENSIVE BASIC DEMO - Time Warp Classic IDE
REM Demonstrates all major BASIC language features
REM =========================================================

REM --- VARIABLES AND DATA TYPES ---
PRINT "=== VARIABLES AND ASSIGNMENT ==="
LET x = 42
LET name$ = "Time Warp"
LET pi = 3.14159
PRINT "Integer: "; x
PRINT "String: "; name$
PRINT "Float: "; pi
PRINT

REM --- ARITHMETIC OPERATIONS ---
PRINT "=== ARITHMETIC OPERATIONS ==="
LET a = 10
LET b = 3
PRINT "Addition: "; a + b
PRINT "Subtraction: "; a - b
PRINT "Multiplication: "; a * b
PRINT "Division: "; a / b
PRINT "Modulo: "; a MOD b
PRINT "Power: "; a ^ 2
PRINT

REM --- MATHEMATICAL FUNCTIONS ---
PRINT "=== MATHEMATICAL FUNCTIONS ==="
PRINT "SIN(1): "; SIN(1)
PRINT "COS(0): "; COS(0)
PRINT "TAN(1): "; TAN(1)
PRINT "SQRT(16): "; SQRT(16)
PRINT "ABS(-42): "; ABS(-42)
PRINT "INT(3.7): "; INT(3.7)
PRINT "RND(100): "; RND(100)
PRINT

REM --- STRING OPERATIONS ---
PRINT "=== STRING OPERATIONS ==="
LET msg = "BASIC Programming"
PRINT "LEN(msg): "; LEN(msg)
PRINT "LEFT(msg, 5): "; LEFT(msg, 5)
PRINT "RIGHT(msg, 11): "; RIGHT(msg, 11)
PRINT "MID(msg, 7, 11): "; MID(msg, 7, 11)
PRINT "INSTR(msg, 'P'): "; INSTR(msg, "P")
PRINT "UPPER: "; UPPER(msg)
PRINT "LOWER: "; LOWER(msg)
PRINT

REM --- ARRAYS ---
PRINT "=== ARRAY OPERATIONS ==="
DIM numbers(5)
LET numbers(1) = 10
LET numbers(2) = 20
LET numbers(3) = 30
LET numbers(4) = 40
LET numbers(5) = 50
PRINT "Array[1]: "; numbers(1)
PRINT "Array[3]: "; numbers(3)
PRINT "SORT array..."
SORT numbers
PRINT "Sorted array[1]: "; numbers(1)
PRINT "SUM: "; SUM(numbers)
PRINT "AVG: "; AVG(numbers)
PRINT "MIN: "; MIN(numbers)
PRINT "MAX: "; MAX(numbers)
PRINT

REM --- CONDITIONAL STATEMENTS ---
PRINT "=== IF/THEN/ELSE STATEMENTS ==="
LET age = 25
IF age >= 18 THEN
    PRINT "You are an adult"
ELSE
    PRINT "You are a minor"
END IF

LET score = 85
IF score >= 90 THEN
    PRINT "Grade: A"
ELSE IF score >= 80 THEN
    PRINT "Grade: B"
ELSE IF score >= 70 THEN
    PRINT "Grade: C"
ELSE
    PRINT "Grade: F"
END IF
PRINT

REM --- FOR LOOPS ---
PRINT "=== FOR LOOPS ==="
PRINT "Counting from 1 to 5:"
FOR i = 1 TO 5
    PRINT "  "; i; " squared = "; i * i
NEXT i
PRINT

PRINT "Counting backwards:"
FOR j = 5 TO 1 STEP -1
    PRINT "  "; j
NEXT j
PRINT

REM --- WHILE LOOPS ---
PRINT "=== WHILE LOOPS ==="
LET counter = 1
WHILE counter <= 3
    PRINT "  Counter: "; counter
    LET counter = counter + 1
END WHILE
PRINT

REM --- SUBROUTINES ---
PRINT "=== SUBROUTINES (GOSUB) ==="
FOR n = 1 TO 3
    GOSUB PrintGreeting
NEXT n
PRINT
GOTO SkipSub

PrintGreeting:
    PRINT "  Hello from subroutine!"
    RETURN

SkipSub:

REM --- TYPE CONVERSION ---
PRINT "=== TYPE CONVERSION ==="
LET numStr = "123"
LET num = VAL(numStr)
PRINT "VAL('123'): "; num
PRINT "STR$(456): "; STR$(456)
PRINT

REM --- COMPARISON OPERATORS ---
PRINT "=== COMPARISON OPERATORS ==="
IF 5 > 3 THEN PRINT "5 > 3: TRUE"
IF 5 = 5 THEN PRINT "5 = 5: TRUE"
IF 5 < 10 THEN PRINT "5 < 10: TRUE"
IF 5 >= 5 THEN PRINT "5 >= 5: TRUE"
IF 5 <= 10 THEN PRINT "5 <= 10: TRUE"
IF 5 <> 3 THEN PRINT "5 <> 3: TRUE"
PRINT

REM --- LOGICAL OPERATORS ---
PRINT "=== LOGICAL OPERATORS ==="
IF 5 > 3 AND 10 > 5 THEN PRINT "AND: TRUE"
IF 5 > 3 OR 10 < 5 THEN PRINT "OR: TRUE"
IF NOT (5 < 3) THEN PRINT "NOT: TRUE"
PRINT

REM --- STRING CONCATENATION ---
PRINT "=== STRING CONCATENATION ==="
LET first = "Hello"
LET last = "World"
LET greeting = first + " " + last
PRINT greeting
PRINT

REM --- FINAL MESSAGE ---
PRINT "=== DEMO COMPLETE ==="
PRINT "Basic programming language features demonstrated!"
END
