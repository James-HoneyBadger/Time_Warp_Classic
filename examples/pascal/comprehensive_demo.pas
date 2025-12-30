PROGRAM ComprehensiveDemo;
{========================================================}
{ COMPREHENSIVE PASCAL DEMO - Time Warp Classic IDE      }
{ Demonstrates all major Pascal language features        }
{========================================================}

CONST
    PI = 3.14159;
    MAX_SIZE = 10;

TYPE
    IntArray = ARRAY[1..10] OF INTEGER;

VAR
    intVar : INTEGER;
    realVar : REAL;
    strVar : STRING;
    boolVar : BOOLEAN;
    charVar : CHAR;
    numbers : IntArray;
    i, j : INTEGER;
    sum, avg : REAL;

{=== PROCEDURES ===}
PROCEDURE PrintHeader(title : STRING);
BEGIN
    WriteLn;
    WriteLn('=== ', title, ' ===');
END;

PROCEDURE PrintLine(text : STRING);
BEGIN
    WriteLn(text);
END;

FUNCTION Add(a, b : INTEGER) : INTEGER;
BEGIN
    Add := a + b;
END;

FUNCTION Multiply(a, b : REAL) : REAL;
BEGIN
    Multiply := a * b;
END;

FUNCTION Factorial(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN
        Factorial := 1
    ELSE
        Factorial := n * Factorial(n - 1);
END;

FUNCTION IsEven(n : INTEGER) : BOOLEAN;
BEGIN
    IsEven := (n MOD 2) = 0;
END;

FUNCTION Power(base, exponent : INTEGER) : INTEGER;
VAR
    result, i : INTEGER;
BEGIN
    result := 1;
    FOR i := 1 TO exponent DO
        result := result * base;
    Power := result;
END;

PROCEDURE PrintArray(arr : IntArray; size : INTEGER);
VAR
    i : INTEGER;
BEGIN
    FOR i := 1 TO size DO
        WriteLn('  [', i, '] = ', arr[i]);
END;

BEGIN
    WriteLn('==================================================');
    WriteLn('COMPREHENSIVE PASCAL DEMO');
    WriteLn('==================================================');

    { --- VARIABLES AND DATA TYPES --- }
    PrintHeader('VARIABLES AND DATA TYPES');
    intVar := 42;
    realVar := 3.14159;
    strVar := 'Time Warp';
    boolVar := TRUE;
    charVar := 'A';
    WriteLn('Integer: ', intVar);
    WriteLn('Real: ', realVar:0:5);
    WriteLn('String: ', strVar);
    WriteLn('Boolean: ', boolVar);
    WriteLn('Char: ', charVar);

    { --- ARITHMETIC OPERATIONS --- }
    PrintHeader('ARITHMETIC OPERATIONS');
    WriteLn('Addition (10 + 3): ', 10 + 3);
    WriteLn('Subtraction (10 - 3): ', 10 - 3);
    WriteLn('Multiplication (10 * 3): ', 10 * 3);
    WriteLn('Division (10 / 3): ', 10 / 3:0:2);
    WriteLn('Integer Division (10 DIV 3): ', 10 DIV 3);
    WriteLn('Modulo (10 MOD 3): ', 10 MOD 3);

    { --- FUNCTION CALLS --- }
    PrintHeader('FUNCTIONS');
    WriteLn('Add(5, 3) = ', Add(5, 3));
    WriteLn('Multiply(4.5, 2.0) = ', Multiply(4.5, 2.0):0:2);
    WriteLn('Factorial(5) = ', Factorial(5));
    WriteLn('Power(2, 8) = ', Power(2, 8));

    { --- CONDITIONAL STATEMENTS --- }
    PrintHeader('IF/ELSE STATEMENTS');
    intVar := 25;
    IF intVar >= 18 THEN
        WriteLn('You are an adult')
    ELSE
        WriteLn('You are a minor');

    intVar := 85;
    IF intVar >= 90 THEN
        WriteLn('Grade: A')
    ELSE IF intVar >= 80 THEN
        WriteLn('Grade: B')
    ELSE IF intVar >= 70 THEN
        WriteLn('Grade: C')
    ELSE
        WriteLn('Grade: F');

    { --- CASE STATEMENT --- }
    PrintHeader('CASE STATEMENT');
    intVar := 2;
    CASE intVar OF
        1: WriteLn('One');
        2: WriteLn('Two');
        3: WriteLn('Three');
    END;

    { --- FOR LOOPS --- }
    PrintHeader('FOR LOOPS');
    WriteLn('Counting 1 to 5:');
    FOR i := 1 TO 5 DO
        WriteLn('  ', i, ' squared = ', i * i);

    WriteLn;
    WriteLn('Counting backwards:');
    FOR i := 5 DOWNTO 1 DO
        WriteLn('  ', i);

    { --- WHILE LOOPS --- }
    PrintHeader('WHILE LOOPS');
    i := 1;
    WHILE i <= 3 DO
    BEGIN
        WriteLn('  Counter: ', i);
        i := i + 1;
    END;

    { --- REPEAT-UNTIL LOOPS --- }
    PrintHeader('REPEAT-UNTIL LOOPS');
    i := 1;
    REPEAT
        WriteLn('  Iteration: ', i);
        i := i + 1;
    UNTIL i > 3;

    { --- ARRAYS --- }
    PrintHeader('ARRAY OPERATIONS');
    WriteLn('Initializing array [1..5]:');
    numbers[1] := 10;
    numbers[2] := 20;
    numbers[3] := 30;
    numbers[4] := 40;
    numbers[5] := 50;

    WriteLn('Array elements:');
    PrintArray(numbers, 5);

    WriteLn;
    sum := 0;
    FOR i := 1 TO 5 DO
        sum := sum + numbers[i];
    WriteLn('Sum: ', sum:0:0);
    WriteLn('Average: ', sum / 5:0:2);

    { --- STRING OPERATIONS --- }
    PrintHeader('STRING OPERATIONS');
    strVar := 'Pascal Programming';
    WriteLn('String: ', strVar);
    WriteLn('Length: ', Length(strVar));
    WriteLn('Uppercase: ', UpCase(charVar));
    WriteLn('First 6 chars: ', Copy(strVar, 1, 6));

    { --- BOOLEAN LOGIC --- }
    PrintHeader('BOOLEAN OPERATIONS');
    IF IsEven(4) THEN
        WriteLn('4 is even');
    IF IsEven(5) THEN
        WriteLn('5 is even')
    ELSE
        WriteLn('5 is odd');

    { --- LOGICAL OPERATORS --- }
    PrintHeader('LOGICAL OPERATORS');
    IF (5 > 3) AND (10 > 5) THEN
        WriteLn('AND: true');
    IF (5 > 3) OR (10 < 5) THEN
        WriteLn('OR: true');
    IF NOT (5 < 3) THEN
        WriteLn('NOT: true');

    { --- COMPARISON OPERATORS --- }
    PrintHeader('COMPARISON OPERATORS');
    IF 5 > 3 THEN WriteLn('5 > 3: true');
    IF 5 = 5 THEN WriteLn('5 = 5: true');
    IF 5 < 10 THEN WriteLn('5 < 10: true');
    IF 5 >= 5 THEN WriteLn('5 >= 5: true');
    IF 5 <= 10 THEN WriteLn('5 <= 10: true');
    IF 5 <> 3 THEN WriteLn('5 <> 3: true');

    { --- FINAL MESSAGE --- }
    WriteLn;
    WriteLn('==================================================');
    WriteLn('PASCAL DEMO COMPLETE!');
    WriteLn('All major Pascal features demonstrated!');
    WriteLn('==================================================');
END.
