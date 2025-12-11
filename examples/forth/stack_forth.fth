\ ====================================
\    Forth Demo - Stack-Based Programming
\ ====================================

\ Forth uses Reverse Polish Notation (RPN)
\ and a stack-based architecture

: GREET ( -- )
    ." Welcome to Time Warp Forth!" CR
    ." Forth is a stack-based language created by Charles Moore." CR
    CR
;

: PRINT-STARS ( n -- )
    0 DO
        ." *"
    LOOP
    CR
;

: SQUARE ( n -- n*n )
    DUP *
;

: CUBE ( n -- n*n*n )
    DUP DUP * *
;

: DEMO-MATH ( -- )
    ." Math demonstrations:" CR
    ." 5 squared = " 5 SQUARE . CR
    ." 3 cubed = " 3 CUBE . CR
    ." 10 + 20 = " 10 20 + . CR
    ." 50 - 15 = " 50 15 - . CR
    CR
;

: DEMO-STARS ( -- )
    ." Printing star patterns:" CR
    5 0 DO
        I 1+ PRINT-STARS
    LOOP
    CR
;

: COUNTDOWN ( n -- )
    BEGIN
        DUP 0 >
    WHILE
        DUP . ." " 
        1-
    REPEAT
    DROP
    ." Liftoff!" CR
;

: MAIN ( -- )
    GREET
    DEMO-MATH
    DEMO-STARS
    ." Countdown: " 5 COUNTDOWN
    CR
    ." Forth demo complete!" CR
;

\ Run the main program
MAIN
