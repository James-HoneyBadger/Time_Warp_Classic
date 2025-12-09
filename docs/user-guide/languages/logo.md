# Logo Language Reference

## Overview

Logo is an educational programming language famous for its turtle graphics. Programs control a virtual turtle that draws on the screen using simple movement commands. Time_Warp implements a comprehensive Logo dialect with modern enhancements and **full UCBLogo (Berkeley Logo) compatibility**.

## UCBLogo Compatibility

Time_Warp Logo is fully compatible with UCBLogo (Berkeley Logo), supporting:

- **Advanced Data Structures**: Arrays, multi-dimensional arrays, property lists
- **Advanced Control Structures**: APPLY, INVOKE, FOREACH, CASCADE, CASE, COND, WHILE, UNTIL, DO.WHILE, DO.UNTIL, FOR loops
- **Advanced Turtle Graphics**: SETHEADING, TOWARDS, SCRUNCH, multiple turtle support
- **Error Handling**: ERRACT, ERROR commands
- **Advanced Arithmetic**: Bitwise operations (BITAND, BITOR, BITXOR, BITNOT, ASHIFT, LSHIFT)
- **Macros**: .MACRO, .DEFMACRO for defining parameterized macros
- **Special Variables**: ALLOWGETSET, CASEIGNOREDP, FULLPRINTP, PRINTDEPTHLIMIT, PRINTWIDTHLIMIT

## Basic Concepts

### The Turtle
- An invisible cursor that moves around the screen
- Can draw lines as it moves
- Has a position (X, Y coordinates)
- Has a heading (direction in degrees)
- Can have its pen up or down

### Coordinate System
- Origin (0, 0) is the center of the screen
- Positive X is right, positive Y is up
- Angles measured counterclockwise from positive X axis
- Screen bounds: -200 to 200 in both X and Y

## Commands

### Movement

#### FORWARD / FD
Move turtle forward by specified distance:
```
FORWARD 100
FD 50
```

#### BACK / BK
Move turtle backward by specified distance:
```
BACK 50
BK 25
```

#### LEFT / LT
Turn turtle left by specified angle in degrees:
```
LEFT 90
LT 45
```

#### RIGHT / RT
Turn turtle right by specified angle in degrees:
```
RIGHT 90
RT 45
```

### Pen Control

#### PENDOWN / PD
Put the pen down to draw lines:
```
PENDOWN
PD
```

#### PENUP / PU
Lift the pen up to move without drawing:
```
PENUP
PU
```

#### SETPENCOLOR / SETPC
Set the pen color (0-15):
```
SETPENCOLOR 1
SETPC 15
```

### Position and Heading

#### SETXY
Move turtle to absolute coordinates:
```
SETXY 100 50
SETXY -50 -25
```

#### SETX
Set X coordinate, keep Y the same:
```
SETX 100
```

#### SETY
Set Y coordinate, keep X the same:
```
SETY 50
```

#### SETHEADING / SETH
Set turtle heading in degrees:
```
SETHEADING 0    ; Point right
SETH 90         ; Point up
SETH 180        ; Point left
SETH 270        ; Point down
```

### Information

#### XCOR
Get current X coordinate:
```
PRINT XCOR
```

#### YCOR
Get current Y coordinate:
```
PRINT YCOR
```

#### HEADING
Get current heading in degrees:
```
PRINT HEADING
```

#### PENCOLOR
Get current pen color:
```
PRINT PENCOLOR
```

## Procedures

### Defining Procedures

#### TO ... END
Define a reusable procedure:
```
TO SQUARE :SIZE
  REPEAT 4 [FORWARD :SIZE RIGHT 90]
END
```

#### Calling Procedures
Execute a defined procedure:
```
SQUARE 100
SQUARE 50
```

### Parameters
Procedures can accept parameters (prefixed with colon):
```
TO TRIANGLE :SIZE :ANGLE
  REPEAT 3 [FORWARD :SIZE RIGHT :ANGLE]
END

TRIANGLE 100 120
```

## Control Structures

### REPEAT
Execute commands multiple times:
```
REPEAT 4 [FORWARD 50 RIGHT 90]  ; Square
REPEAT 3 [FORWARD 60 RIGHT 120] ; Triangle
```

### IF
Conditional execution:
```
IF :SIZE > 10 [FORWARD :SIZE]
IF color = "red [SETPENCOLOR 1]
```

### WHILE
Loop while condition is true:
```
WHILE :count < 10 [
  FORWARD 10
  MAKE "count :count + 1
]
```

### FOR
Counted loop:
```
FOR [i 1 10] [PRINT :i]
FOR [x 0 100 10] [FORWARD :x RIGHT 90]
```

## Variables

### MAKE
Create or change a variable:
```
MAKE "size 100
MAKE "color "red
MAKE "count 0
```

### Variable Access
Access variables with colon prefix:
```
MAKE "length 50
FORWARD :length
```

### Local Variables
Variables in procedures are local by default:
```
TO DRAWBOX :size
  MAKE "half :size / 2
  FORWARD :half
  RIGHT 90
  ; half is only available in this procedure
END
```

## Mathematical Operations

### Basic Arithmetic
```
MAKE "a 10
MAKE "b 20
MAKE "sum :a + :b
MAKE "diff :a - :b
MAKE "prod :a * :b
MAKE "quot :a / :b
```

### Advanced Math
```
MAKE "result SIN 45    ; Sine (degrees)
MAKE "root SQRT 16     ; Square root
MAKE "power 2 ^ 3      ; Exponentiation
MAKE "abs ABS -5       ; Absolute value
MAKE "round ROUND 3.7  ; Round to nearest integer
```

## Lists

### Creating Lists
```
MAKE "numbers [1 2 3 4 5]
MAKE "colors [red green blue]
```

### List Operations
```
MAKE "first FIRST :numbers    ; Get first item
MAKE "rest BUTFIRST :numbers  ; Remove first item
MAKE "count COUNT :numbers    ; Get length
MAKE "item ITEM 3 :numbers    ; Get nth item
```

## Examples

### Basic Shapes

#### Square
```
TO SQUARE :size
  REPEAT 4 [FORWARD :size RIGHT 90]
END

SQUARE 100
```

#### Circle
```
TO CIRCLE :radius
  REPEAT 36 [FORWARD (2 * 3.14159 * :radius / 36) RIGHT 10]
END

CIRCLE 50
```

#### Triangle
```
TO TRIANGLE :size
  REPEAT 3 [FORWARD :size RIGHT 120]
END

TRIANGLE 80
```

### Complex Drawings

#### Flower
```
TO PETAL :size
  REPEAT 2 [
    FORWARD :size
    RIGHT 60
    FORWARD :size
    RIGHT 120
  ]
END

TO FLOWER
  REPEAT 6 [
    PETAL 50
    RIGHT 60
  ]
END

FLOWER
```

#### Spiral
```
TO SPIRAL :size :angle :steps
  REPEAT :steps [
    FORWARD :size
    RIGHT :angle
    MAKE "size :size + 2
  ]
END

SPIRAL 5 20 50
```

#### Star
```
TO STAR :size
  REPEAT 5 [
    FORWARD :size
    RIGHT 144
  ]
END

STAR 100
```

### Fractals

#### Tree
```
TO TREE :size
  IF :size < 5 [STOP]
  FORWARD :size
  RIGHT 25
  TREE :size * 0.7
  LEFT 50
  TREE :size * 0.7
  RIGHT 25
  BACK :size
END

TREE 100
```

#### Snowflake
```
TO SIDE :size :level
  IF :level = 0 [FORWARD :size] [
    SIDE :size/3 :level-1
    LEFT 60
    SIDE :size/3 :level-1
    RIGHT 120
    SIDE :size/3 :level-1
    LEFT 60
    SIDE :size/3 :level-1
  ]
END

TO SNOWFLAKE :size
  REPEAT 3 [
    SIDE :size 3
    RIGHT 120
  ]
END

SNOWFLAKE 150
```

### Interactive Programs

#### Drawing Program
```
TO DRAW
  PENDOWN
  WHILE [TRUE] [
    IF MOUSEPRESSED [
      SETXY MOUSEX MOUSEY
    ]
  ]
END

DRAW
```

#### Color Changer
```
TO COLORCYCLE
  MAKE "color 0
  WHILE [TRUE] [
    SETPENCOLOR :color
    MAKE "color MODULO (:color + 1) 16
    WAIT 10
  ]
END

COLORCYCLE
```

## Color Reference

| Number | Color    | Number | Color     |
|--------|----------|--------|-----------|
| 0      | Black    | 8      | Gray      |
| 1      | Blue     | 9      | Light Blue|
| 2      | Green    | 10     | Light Green|
| 3      | Cyan     | 11     | Light Cyan|
| 4      | Red      | 12     | Light Red |
| 5      | Magenta  | 13     | Light Magenta|
| 6      | Yellow   | 14     | Light Yellow|
| 7      | White    | 15     | Bright White|

## Best Practices

1. **Use procedures** to organize code
2. **Choose meaningful names** for procedures and variables
3. **Use parameters** to make procedures flexible
4. **Start simple** and build complexity gradually
5. **Test procedures** individually before combining
6. **Use comments** to explain complex logic

## Error Handling

Logo programs handle errors gracefully:
- Invalid coordinates are clamped to screen bounds
- Division by zero returns infinity
- Missing procedures show error messages
- Type mismatches are converted automatically

## Advanced Features

### UCBLogo Data Structures

#### Arrays
Create and manipulate arrays:
```
ARRAY "MYARRAY 10 0        ; Create array with 10 elements, default value 0
SETITEM "MYARRAY 5 42      ; Set element at index 5 to 42
PRINT ITEM 5 "MYARRAY      ; Print element at index 5
```

#### Multi-dimensional Arrays
```
MDARRAY "MATRIX [3 3]       ; Create 3x3 array
MDSETITEM "MATRIX [1 2] 99 ; Set element at [1,2] to 99
```

#### Property Lists
Store key-value pairs:
```
PPROP "PERSON "NAME "John    ; Set property
PPROP "PERSON "AGE 25
PRINT GPROP "PERSON "NAME   ; Get property value
PRINT PLIST "PERSON         ; List all properties
REMPROP "PERSON "AGE        ; Remove property
```

### UCBLogo Control Structures

#### FOREACH Loop
Iterate over list elements:
```
FOREACH "item [1 2 3 4 5] [
  PRINT :item
]
```

#### WHILE and UNTIL Loops
```
WHILE [:count < 10] [
  PRINT :count
  MAKE "count :count + 1
]

UNTIL [:count = 0] [
  PRINT :count
  MAKE "count :count - 1
]
```

#### FOR Loop
```
FOR [i 1 10 1] [
  PRINT :i
]
```

#### CASE Selection
```
CASE :value [
  [1] [PRINT "One"]
  [2] [PRINT "Two"]
  [ELSE] [PRINT "Other"]
]
```

#### APPLY and INVOKE
Apply procedures to arguments:
```
APPLY "PRINT [1 2 3]
INVOKE "SUM [10 20 30]
```

### UCBLogo Advanced Turtle Graphics

#### SETHEADING
Set turtle direction directly:
```
SETHEADING 90    ; Face north
SETHEADING 0     ; Face east
```

#### TOWARDS
Point turtle towards coordinates:
```
TOWARDS 100 100   ; Point towards (100, 100)
```

#### SCRUNCH
Adjust coordinate scaling:
```
SCRUNCH 2 2       ; Double the scale in both directions
```

### UCBLogo Error Handling

#### ERRACT
Set error handler:
```
ERRACT [PRINT "Error occurred"]
```

#### ERROR
Generate custom errors:
```
IF :value < 0 [ERROR "Value must be positive"]
```

### UCBLogo Bitwise Operations

```
PRINT BITAND 12 10    ; 8 (1100 & 1010 = 1000)
PRINT BITOR 12 10     ; 14 (1100 | 1010 = 1110)
PRINT BITXOR 12 10    ; 6 (1100 ^ 1010 = 0110)
PRINT BITNOT 12       ; -13 (bitwise NOT)
PRINT ASHIFT 1 3      ; 8 (1 << 3)
PRINT LSHIFT 16 2     ; 4 (16 >> 2)
```

### UCBLogo Macros

#### .MACRO
Define simple macros:
```
.MACRO SQUARE :size [
  REPEAT 4 [FORWARD :size RIGHT 90]
]
SQUARE 50
```

#### .DEFMACRO
Define parameterized macros:
```
.DEFMACRO POLYGON :sides :size [
  REPEAT :sides [FORWARD :size RIGHT 360/:sides]
]
POLYGON 6 30    ; Draw hexagon
```

### Recursion
Procedures can call themselves:
```
TO COUNTDOWN :n
  IF :n > 0 [
    PRINT :n
    COUNTDOWN :n - 1
  ]
END

COUNTDOWN 10
```

### Higher-Order Functions
```
TO APPLY :func :list
  IF NOT EMPTY? :list [
    RUN (SENTENCE :func FIRST :list)
    APPLY :func BUTFIRST :list
  ]
END

APPLY [PRINT] [1 2 3 4 5]
```

### Dynamic Procedure Creation
```
MAKE "procname "MYPROC
DEFINE :procname [[x] [PRINT :x * 2]]
MYPROC 21  ; Prints 42
```

## Compatibility

Time_Warp Logo extends classic Logo with:
- Enhanced graphics capabilities
- Better error handling
- Modern programming constructs
- Improved performance
- Additional mathematical functions

## See Also

- [Logo Sample Programs](../../samples/logo/)
- [Time_Warp User Guide](../user_guide.md)
- [Compiler Documentation](../compiler.md)