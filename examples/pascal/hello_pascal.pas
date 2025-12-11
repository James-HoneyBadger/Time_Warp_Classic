{ ====================================
    Pascal Demo - Structured Programming
  ==================================== }

PROGRAM HelloPascal;

VAR
  i, sum: INTEGER;
  name: STRING;

{ Function to calculate factorial }
FUNCTION Factorial(n: INTEGER): INTEGER;
VAR
  result, j: INTEGER;
BEGIN
  result := 1;
  FOR j := 2 TO n DO
    result := result * j;
  Factorial := result;
END;

{ Main program }
BEGIN
  WRITELN('Welcome to Time Warp Pascal!');
  WRITELN('');
  WRITELN('Pascal is a structured programming language');
  WRITELN('designed by Niklaus Wirth in 1970.');
  WRITELN('');
  
  { Simple loop demonstration }
  WRITELN('Counting from 1 to 5:');
  FOR i := 1 TO 5 DO
    WRITELN('  ', i);
  
  WRITELN('');
  
  { Calculate some factorials }
  WRITELN('Factorial calculations:');
  FOR i := 1 TO 5 DO
    WRITELN('  ', i, '! = ', Factorial(i));
  
  WRITELN('');
  
  { Sum calculation }
  sum := 0;
  FOR i := 1 TO 10 DO
    sum := sum + i;
  WRITELN('Sum of 1 to 10 = ', sum);
  
  WRITELN('');
  WRITELN('Pascal demo complete!');
END.
