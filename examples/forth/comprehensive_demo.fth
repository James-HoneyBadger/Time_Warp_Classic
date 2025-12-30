% =========================================================
% COMPREHENSIVE FORTH DEMO - Time Warp Classic IDE
% Demonstrates all major Forth language features
% =========================================================

\ --- STACK OPERATIONS AND PRINTING ---
: HEADER ." ===================================================" CR ." COMPREHENSIVE FORTH DEMO" CR ." ===================================================" CR CR ;

HEADER

\ --- BASIC ARITHMETIC ---
." === BASIC ARITHMETIC ===" CR
10 5 + .  ." (10 + 5)" CR
10 5 - .  ." (10 - 5)" CR
10 5 * .  ." (10 * 5)" CR
10 5 / .  ." (10 / 5)" CR
17 5 MOD .  ." (17 mod 5)" CR
2 8 ** .  ." (2 ^ 8)" CR
CR

\ --- STACK MANIPULATION ---
." === STACK MANIPULATION ===" CR
5 DUP . . ." (DUP: 5 duplicated)" CR
10 20 SWAP . . ." (SWAP: 10 20 swapped)" CR
1 2 3 ROT . . . ." (ROT: 1 2 3 rotated)" CR
1 2 OVER . . . . ." (OVER: 1 2 1 2)" CR
CR

\ --- VARIABLES AND MEMORY ---
." === VARIABLES ===" CR
VARIABLE x
42 x !
x @ . ." (Variable x = 42)" CR
VARIABLE y
100 y !
y @ . ." (Variable y = 100)" CR
CR

\ --- WORD DEFINITIONS ---
: SQUARE DUP * ;
: CUBE DUP DUP * * ;
: DOUBLE 2 * ;
: HALVE 2 / ;
: THIRD 3 / ;

." === WORD DEFINITIONS ===" CR
5 SQUARE . ." (5 squared)" CR
3 CUBE . ." (3 cubed)" CR
7 DOUBLE . ." (7 doubled)" CR
20 HALVE . ." (20 halved)" CR
15 THIRD . ." (15 / 3)" CR
CR

\ --- CONDITIONAL LOGIC ---
." === CONDITIONAL LOGIC ===" CR
: CHECK_POSITIVE ( n -- ) DUP 0 > IF ." positive" ELSE ." not positive" THEN DROP CR ;
5 CHECK_POSITIVE
-3 CHECK_POSITIVE
0 CHECK_POSITIVE

: GRADE ( score -- ) 
    DUP 90 >= IF ." Grade: A" ELSE
    DUP 80 >= IF ." Grade: B" ELSE
    DUP 70 >= IF ." Grade: C" ELSE
    ." Grade: F" THEN THEN THEN DROP CR ;
95 GRADE
85 GRADE
75 GRADE
65 GRADE
CR

\ --- LOOPS ---
." === LOOPS ===" CR
." Counting 1 to 5:" CR
: COUNT_UP ( n -- ) 1 DO I . LOOP ;
5 COUNT_UP CR

." Counting backwards:" CR
: COUNT_DOWN ( n -- ) DO I . -1 +LOOP ;
5 1 COUNT_DOWN CR

." Multiplication table (3x):" CR
: MULT_TABLE ( n -- )
    1 DO
        1 DO
            J I * .
        LOOP CR
    LOOP ;
CR

\ --- ARRAY/TABLE OPERATIONS ---
." === ARRAYS (TABLES) ===" CR
CREATE numbers 5 CELLS ALLOT
: SET_ARRAY ( value index -- ) CELLS numbers + ! ;
: GET_ARRAY ( index -- value ) CELLS numbers + @ ;

10 0 SET_ARRAY
20 1 SET_ARRAY
30 2 SET_ARRAY
40 3 SET_ARRAY
50 4 SET_ARRAY

." Array values:" CR
0 GET_ARRAY . ." (index 0)" CR
1 GET_ARRAY . ." (index 1)" CR
2 GET_ARRAY . ." (index 2)" CR
3 GET_ARRAY . ." (index 3)" CR
4 GET_ARRAY . ." (index 4)" CR
CR

\ --- SUM AND AVERAGE ---
." === SUM AND AVERAGE ===" CR
: SUM_ARRAY ( -- sum )
    0
    5 0 DO I GET_ARRAY + LOOP ;

: AVG_ARRAY ( -- avg )
    SUM_ARRAY 5 / ;

SUM_ARRAY . ." (sum of array)" CR
AVG_ARRAY . ." (average of array)" CR
CR

\ --- RECURSION ---
." === RECURSION ===" CR
: FACTORIAL ( n -- factorial )
    DUP 1 > IF
        DUP 1 - RECURSE *
    ELSE
        DROP 1
    THEN ;

5 FACTORIAL . ." (5!)" CR
6 FACTORIAL . ." (6!)" CR
CR

\ --- COMPARISON ---
." === COMPARISON ===" CR
: COMPARE ( a b -- )
    2DUP > IF ." first is greater" ELSE
    2DUP < IF ." second is greater" ELSE
    ." they are equal" THEN THEN 2DROP CR ;

10 5 COMPARE
5 10 COMPARE
5 5 COMPARE
CR

\ --- NUMBER PROPERTIES ---
." === NUMBER PROPERTIES ===" CR
: IS_EVEN ( n -- flag ) 2 MOD 0 = ;
: IS_ODD ( n -- flag ) 2 MOD 0 <> ;

: PRINT_PARITY ( n -- )
    DUP IS_EVEN IF ." is even" ELSE ." is odd" THEN DROP CR ;

4 PRINT_PARITY
7 PRINT_PARITY
10 PRINT_PARITY
CR

\ --- STRING OPERATIONS ---
." === STRING OPERATIONS ===" CR
: PRINT_STRING ( -- ) ." Hello from Forth!" ;
PRINT_STRING CR
: REPEAT_CHAR ( char count -- ) 0 DO DUP EMIT LOOP DROP ;
42 5 REPEAT_CHAR CR
CR

\ --- FLOATING POINT ---
." === FLOATING POINT ===" CR
3.14159E0 F. ." (PI)" CR
2.71828E0 F. ." (E)" CR
10E0 2E0 F/ F. ." (10 / 2)" CR
CR

\ --- MATHEMATICAL FUNCTIONS ---
." === MATHEMATICAL FUNCTIONS ===" CR
: SQUARE-ROOT ( x -- sqrt )
    S" SQRT" EVALUATE ;

100 SQUARE-ROOT F. ." (sqrt(100))" CR
CR

\ --- DEFINITIONS WITH MULTIPLE OUTPUTS ---
." === MULTI-OUTPUT WORDS ===" CR
: DIVIDE-WITH-REMAINDER ( a b -- quotient remainder )
    2DUP MOD ROT ROT / ;

17 5 DIVIDE-WITH-REMAINDER
. . ." (17 ÷ 5)" CR
CR

\ --- FINAL MESSAGE ---
." ===================================================" CR
." FORTH DEMO COMPLETE!" CR
." All major Forth features demonstrated!" CR
." ===================================================" CR
