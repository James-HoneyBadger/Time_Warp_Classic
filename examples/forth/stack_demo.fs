\ Forth Stack Programming Demo
\ Demonstrates stack operations and word definitions

: HELLO ( -- )
    ." Forth Stack Programming Demo" CR
    ." =============================" CR CR ;

: SQUARE ( n -- n^2 )
    DUP * ;

: CUBE ( n -- n^3 )
    DUP DUP * * ;

: DISPLAY-NUMBERS ( -- )
    ." Numbers and their squares/cubes:" CR
    5 0 DO
        I 1+ DUP ." Number: " . ."  Square: " SQUARE . ."  Cube: " CUBE . CR
    LOOP ;

: FIBONACCI ( n -- fib_n )
    DUP 2 < IF DROP 1 EXIT THEN
    DUP 1- RECURSE
    SWAP 2- RECURSE + ;

: DISPLAY-FIB ( -- )
    ." First 10 Fibonacci numbers:" CR
    10 1 DO
        I FIBONACCI ." Fib(" I . ." ) = " . CR
    LOOP ;

: FACTORIAL ( n -- n! )
    DUP 0= IF DROP 1 EXIT THEN
    DUP 1- RECURSE * ;

: DISPLAY-FACT ( -- )
    ." Factorials:" CR
    6 1 DO
        I ." " I . ." ! = " I FACTORIAL . CR
    LOOP ;

: STACK-DEMO ( -- )
    ." Stack manipulation demo:" CR
    10 20 30 ." Original stack: " .S CR
    SWAP ." After SWAP: " .S CR
    DUP ." After DUP: " .S CR
    DROP ." After DROP: " .S CR
    ROT ." After ROT: " .S CR ;

HELLO

DISPLAY-NUMBERS CR

DISPLAY-FIB CR

DISPLAY-FACT CR

STACK-DEMO CR

." Forth demo complete!" CR