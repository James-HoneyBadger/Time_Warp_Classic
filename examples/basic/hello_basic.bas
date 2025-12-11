10 REM ====================================
20 REM    BASIC Demo - Hello World & Graphics
30 REM ====================================
40 CLS
50 PRINT "Welcome to Time Warp BASIC!"
60 PRINT ""
70 PRINT "Drawing a square..."
80 PENDOWN
90 FORWARD 100
100 RIGHT 90
110 FORWARD 100
120 RIGHT 90
130 FORWARD 100
140 RIGHT 90
150 FORWARD 100
160 RIGHT 90
170 PENUP
180 PRINT ""
190 PRINT "Now drawing a growing spiral..."
200 LET D = 5
210 PENDOWN
220 FOR I = 1 TO 36
230   FORWARD D
240   RIGHT 10
250   LET D = D + 2
260 NEXT I
270 PENUP
280 PRINT ""
290 PRINT "BASIC graphics demo complete!"
300 END
