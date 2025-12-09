REM Turbo BASIC Features Demo
REM Showcasing advanced BASIC commands

10 PRINT "Turbo BASIC Features Demo"
20 PRINT

REM Variables and direct assignment
30 X = 10
40 Y = 20
50 PRINT "Initial values: X="; X; ", Y="; Y

REM SWAP command
60 SWAP X, Y
70 PRINT "After SWAP: X="; X; ", Y="; Y

REM INCR and DECR commands
80 INCR X
90 DECR Y, 2
100 PRINT "After INCR X and DECR Y,2: X="; X; ", Y="; Y
110 PRINT

REM DO LOOP with EXIT
120 PRINT "DO LOOP demonstration:"
130 COUNT = 0
140 DO
150   PRINT "Iteration: "; COUNT
160   INCR COUNT
170   IF COUNT >= 5 THEN EXIT DO
180 LOOP
190 PRINT "DO LOOP completed"
200 PRINT

REM WHILE WEND
210 PRINT "WHILE WEND demonstration:"
220 VALUE = 1
230 WHILE VALUE <= 3
240   PRINT "Value: "; VALUE
250   INCR VALUE
260 WEND
270 PRINT "WHILE WEND completed"
280 PRINT

REM SELECT CASE
290 PRINT "SELECT CASE demonstration:"
300 SCORE = 85
310 SELECT CASE SCORE
320   CASE 90 TO 100
330     PRINT "Grade: A"
340   CASE 80 TO 89
350     PRINT "Grade: B"
360   CASE 70 TO 79
370     PRINT "Grade: C"
380   CASE ELSE
390     PRINT "Grade: F"
400 END SELECT

410 PRINT
420 PRINT "Turbo BASIC demo complete!"