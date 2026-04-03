\ ═══════════════════════════════════════════════════════
\ NUMBER THEORY TOOLKIT
\ Practical number theory computations demonstrating
\ Forth's power for mathematical algorithms:
\ primes, GCD, Fibonacci, Collatz, and more
\ ═══════════════════════════════════════════════════════

: HEADER ." ═══════════════════════════════════════════" CR ;
: DIVIDER ."  ─────────────────────────────────────────" CR ;

HEADER
."  NUMBER THEORY TOOLKIT v1.0" CR
HEADER
CR

\ ═══════════════════════════════════════
\ PRIME NUMBERS
\ ═══════════════════════════════════════

VARIABLE p-n
VARIABLE p-flag

: IS-PRIME? ( n -- flag )
    p-n ! 1 p-flag !
    p-n @ 2 < IF 0 p-flag ! THEN
    p-n @ 2 > IF p-n @ 2 MOD 0 = IF 0 p-flag ! THEN THEN
    p-flag @ 1 = p-n @ 2 > AND IF
        3 BEGIN
            DUP DUP * p-n @ <= p-flag @ 1 = AND WHILE
            p-n @ OVER MOD 0 = IF 0 p-flag ! THEN
            2 +
        REPEAT DROP
    THEN
    p-flag @ ;

."  PRIME NUMBERS" CR
DIVIDER

: SHOW-PRIMES-100 ( -- )
    ."   " 
    101 2 DO
        I DUP IS-PRIME? IF . ELSE DROP THEN
    LOOP ;

."   Primes up to 100:" CR
SHOW-PRIMES-100
CR CR

."   Counting primes up to various limits:" CR
VARIABLE prime-count

: COUNT-PRIMES ( limit -- count )
    0 prime-count !
    2 DO
        I IS-PRIME? IF prime-count @ 1 + prime-count ! THEN
    LOOP
    prime-count @ ;

."   Primes up to 50:  " 51 COUNT-PRIMES . CR
."   Primes up to 100: " 101 COUNT-PRIMES . CR
."   Primes up to 200: " 201 COUNT-PRIMES . CR
CR

\ ═══════════════════════════════════════
\ GREATEST COMMON DIVISOR
\ ═══════════════════════════════════════

: GCD ( a b -- gcd )
    BEGIN DUP WHILE
        SWAP OVER MOD
    REPEAT DROP ;

: LCM ( a b -- lcm )
    2DUP GCD / * ;

."  GREATEST COMMON DIVISOR (Euclid's Algorithm)" CR
DIVIDER

."   GCD(48, 18) = " 48 18 GCD . CR
."   GCD(100, 75) = " 100 75 GCD . CR
."   GCD(252, 105) = " 252 105 GCD . CR
."   GCD(17, 13) = " 17 13 GCD . ."  (coprime)" CR
CR

."   LEAST COMMON MULTIPLE" CR
."   LCM(12, 18) = " 12 18 LCM . CR
."   LCM(7, 5) = " 7 5 LCM . CR
."   LCM(15, 20) = " 15 20 LCM . CR
CR

\ ═══════════════════════════════════════
\ FIBONACCI SEQUENCE
\ ═══════════════════════════════════════

: FIB ( n -- fib )
    DUP 1 <= IF
    ELSE
        0 1 ROT 1 DO
            SWAP OVER +
        LOOP
        SWAP DROP
    THEN ;

: SHOW-FIB ( -- )
    ."   "
    20 0 DO I FIB . LOOP ;

: SHOW-FIB-RATIOS ( -- )
    15 10 DO
        ."   F(" I . ." ) / F(" I 1 - . ." ) = "
        I FIB . ."  / " I 1 - FIB .
        ."  ratio*1000 = " I FIB 1000 * I 1 - FIB / . CR
    LOOP ;

."  FIBONACCI SEQUENCE" CR
DIVIDER
."   First 20 Fibonacci numbers:" CR
SHOW-FIB
CR CR

."   Fibonacci ratios (approaching Golden Ratio ~1.618):" CR
SHOW-FIB-RATIOS
CR

\ ═══════════════════════════════════════
\ FACTORIALS
\ ═══════════════════════════════════════

: FACTORIAL ( n -- n! )
    DUP 1 <= IF DROP 1 ELSE
        1 SWAP 1+ 2 DO
            I *
        LOOP
    THEN ;

: SHOW-FACTORIALS ( -- )
    13 1 DO
        ."   " I . ." ! = " I FACTORIAL . CR
    LOOP ;

."  FACTORIALS" CR
DIVIDER
SHOW-FACTORIALS
CR

\ ═══════════════════════════════════════
\ COLLATZ CONJECTURE
\ ═══════════════════════════════════════

: COLLATZ-STEPS ( n -- steps )
    0 SWAP
    BEGIN DUP 1 > WHILE
        DUP 2 MOD 0 = IF
            2 /
        ELSE
            3 * 1 +
        THEN
        SWAP 1 + SWAP
    REPEAT
    DROP ;

: COLLATZ-SEQUENCE ( n -- )
    BEGIN
        DUP .
        DUP 1 > WHILE
        DUP 2 MOD 0 = IF 2 / ELSE 3 * 1 + THEN
    REPEAT
    DROP ;

."  COLLATZ CONJECTURE (3n+1 Problem)" CR
DIVIDER
."   Starting Number  ->  Steps to reach 1" CR

."   7  -> " 7 COLLATZ-STEPS . ."  steps" CR
."   15 -> " 15 COLLATZ-STEPS . ."  steps" CR
."   27 -> " 27 COLLATZ-STEPS . ."  steps" CR
."   97 -> " 97 COLLATZ-STEPS . ."  steps" CR

CR
."   Sequence for n=27:" CR
."   " 27 COLLATZ-SEQUENCE
CR CR

\ ═══════════════════════════════════════
\ PERFECT NUMBERS
\ ═══════════════════════════════════════

: SUM-DIVISORS ( n -- sum )
    0 SWAP
    DUP 2 / 1+ 1 DO
        DUP I MOD 0 = IF
            SWAP I + SWAP
        THEN
    LOOP DROP ;

: PERFECT? ( n -- flag )
    DUP SUM-DIVISORS = ;

: FIND-PERFECT ( limit -- )
    ."   "
    1 DO
        I DUP PERFECT? IF . ELSE DROP THEN
    LOOP ;

."  PERFECT NUMBERS" CR
DIVIDER
."   A perfect number equals the sum of its divisors." CR
."   Checking 1-500:" CR
500 FIND-PERFECT
CR CR

."   Divisor analysis:" CR
."   6:  divisors sum = " 6 SUM-DIVISORS . ."  (perfect)" CR
."   12: divisors sum = " 12 SUM-DIVISORS . ."  (abundant)" CR
."   8:  divisors sum = " 8 SUM-DIVISORS . ."  (deficient)" CR
."   28: divisors sum = " 28 SUM-DIVISORS . ."  (perfect)" CR
CR

\ ═══════════════════════════════════════
\ TRIANGULAR NUMBERS
\ ═══════════════════════════════════════

: TRIANGULAR ( n -- tri )
    DUP 1 + * 2 / ;

: SHOW-TRIANGULAR ( -- )
    ."   "
    15 1 DO I TRIANGULAR . LOOP ;

."  TRIANGULAR NUMBERS" CR
DIVIDER
."   T(n) = n(n+1)/2" CR
SHOW-TRIANGULAR
CR CR

\ ═══════════════════════════════════════
\ POWER FUNCTION
\ ═══════════════════════════════════════

: POWER ( base exp -- result )
    1 SWAP 0 DO
        OVER *
    LOOP
    SWAP DROP ;

: SHOW-POWERS-OF ( base limit -- )
    ."   "
    0 DO
        OVER I POWER .
    LOOP DROP ;

."  POWERS" CR
DIVIDER
."   Powers of 2:" CR
2 16 SHOW-POWERS-OF
CR
."   Powers of 3:" CR
3 10 SHOW-POWERS-OF
CR CR

\ ═══════════════════════════════════════
\ PYTHAGOREAN TRIPLES
\ ═══════════════════════════════════════

VARIABLE pyth-a
VARIABLE pyth-b

: FIND-TRIPLES ( maxc -- )
    1 DO
        I 1 DO
            I 1 DO
                I I * J J * + K K * = IF
                    I J < IF
                        I pyth-a !
                        J pyth-b !
                        ."   " pyth-a @ . ."  " pyth-b @ . ."  " K . CR
                    THEN
                THEN
            LOOP
        LOOP
    LOOP ;

."  PYTHAGOREAN TRIPLES (a b c where a^2 + b^2 = c^2)" CR
DIVIDER
."   Triples with hypotenuse <= 30:" CR
31 FIND-TRIPLES
CR

\ ═══════════════════════════════════════
\ SUMMARY
\ ═══════════════════════════════════════

HEADER
."  Number Theory Toolkit Complete" CR
."  Demonstrated: Primes, GCD/LCM, Fibonacci," CR
."  Factorials, Collatz, Perfect Numbers," CR
."  Triangular Numbers, Powers, Pythagorean Triples" CR
HEADER
