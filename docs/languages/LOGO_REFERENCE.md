# Logo Language Reference

Complete reference for Logo turtle graphics in Time Warp Classic.

## Turtle Basics

Logo uses a virtual "turtle" that draws on the screen:
- **Turtle position:** X, Y coordinates
- **Turtle direction:** Angle in degrees (0=up, 90=right, 180=down, 270=left)
- **Pen state:** Up (no draw) or down (drawing)

## Movement

### Basic Movement

```logo
FORWARD 100         FD 100      Move forward 100 units
BACK 50             BK 50       Move backward 50 units
RIGHT 90            RT 90       Turn right 90 degrees
LEFT 45             LT 45       Turn left 45 degrees
```

### Examples

```logo
FD 100
RT 90
FD 100
RT 90
FD 100
RT 90
FD 100              \ Draws a square
```

## Pen Control

### Pen State

```logo
PENDOWN             PD          Lower pen (drawing)
PENUP               PU          Raise pen (not drawing)
```

### Pen Attributes

```logo
PENSIZE 3           Set pen thickness
SETPENCOLOR 1       Set pen color (1=red, 2=green, etc.)
SETPENCOLOR [255 0 0]  Set RGB color
```

## Graphics Commands

### Shapes

```logo
CIRCLE 50           Draw circle with radius 50
```

### Clear

```logo
CLEARSCREEN         CS          Clear entire screen
HOME                            Go to center, face up
```

## Turtle State

### Position & Direction

```logo
XCOR                Get X coordinate
YCOR                Get Y coordinate
HEADING             Get current direction (0-359)
SETPOSITION [50 100] SETPOS [50 100]  Go to position
SETHEADING 0        SETH 0      Set direction (0=up)
```

### Pen State Query

```logo
PENDOWNP                        Check if pen is down
PENSTATE                        Get pen state
```

## Loops & Repetition

### Repeat Loop

```logo
REPEAT 4 [
    FORWARD 100
    RIGHT 90
]                   \ Draws a square

REPEAT 360 [
    FORWARD 1
    RIGHT 1
]                   \ Draws a circle
```

### For Loop (Logo 2)

```logo
FOR [I 1 4] [
    FORWARD 100
    RIGHT 90
]
```

## Variables

### Variable Definition

```logo
MAKE "size 50
FORWARD :size       \ Use variable with :

MAKE "x 10
MAKE "y 20
SETPOSITION [list :x :y]
```

## Procedures (Custom Commands)

### Define Procedure

```logo
TO SQUARE :size
    REPEAT 4 [
        FORWARD :size
        RIGHT 90
    ]
END

SQUARE 100          \ Call procedure
```

### Nested Procedures

```logo
TO TRIANGLE :size
    REPEAT 3 [
        FORWARD :size
        RIGHT 120
    ]
END

TO STAR :size
    REPEAT 5 [
        FORWARD :size
        RIGHT 144
    ]
END

STAR 100
```

## Advanced Features

### Recursion

```logo
TO SPIRAL :size :angle
    IF :size < 1
        STOP
    END
    FORWARD :size
    RIGHT :angle
    SPIRAL :size + 2 :angle
END

SPIRAL 1 15
```

### Nested Patterns

```logo
TO PATTERN :count :size
    IF :count = 0
        STOP
    END
    REPEAT 4 [
        FORWARD :size
        RIGHT 90
    ]
    RIGHT 30
    PATTERN :count - 1 :size - 5
END

PATTERN 10 100
```

## Complete Examples

### Square

```logo
TO SQUARE :size
    REPEAT 4 [
        FORWARD :size
        RIGHT 90
    ]
END

SQUARE 100
```

### Regular Polygon

```logo
TO POLYGON :sides :size
    REPEAT :sides [
        FORWARD :size
        RIGHT 360 / :sides
    ]
END

POLYGON 6 80       \ Hexagon
POLYGON 8 60       \ Octagon
```

### Spiral

```logo
TO SPIRAL :size
    REPEAT 100 [
        FORWARD :size
        RIGHT 10
        MAKE "size :size + 1
    ]
END

SPIRAL 1
```

### Fractal Tree

```logo
TO TREE :size
    IF :size < 5
        STOP
    END
    FORWARD :size
    RIGHT 30
    TREE :size / 2
    LEFT 60
    TREE :size / 2
    RIGHT 30
    BACK :size
END

TREE 100
```

### Star

```logo
TO STAR :size :points
    REPEAT :points [
        FORWARD :size
        RIGHT 360 / :points
    ]
END

STAR 100 5         \ 5-pointed star
```

### Geometric Design

```logo
TO DESIGN :count :size
    REPEAT :count [
        REPEAT 4 [
            FORWARD :size
            RIGHT 90
        ]
        RIGHT 30
    ]
END

DESIGN 12 50       \ Rotating squares pattern
```

## Color System

### Colors (1-8)

```logo
1   - Black
2   - Red
3   - Green
4   - Blue
5   - Magenta
6   - Cyan
7   - Yellow
8   - White
```

### Set Colors

```logo
SETPENCOLOR 2      \ Red
SETPENCOLOR 3      \ Green
SETPENCOLOR [255 128 0]  \ RGB colors
```

## Tips & Best Practices

1. **Use procedures** for repeated patterns
2. **Build complex from simple** pieces
3. **Test each shape independently**
4. **Use appropriate scale** for drawings
5. **Comment your code** explaining design
6. **Experiment with colors** and patterns
7. **Combine multiple shapes** creatively

## Common Patterns

### Sunburst
```logo
REPEAT 12 [
    FORWARD 100
    BACK 100
    RIGHT 30
]
```

### Flower
```logo
REPEAT 6 [
    CIRCLE 50
    RIGHT 60
]
```

### Maze-like
```logo
REPEAT 4 [
    FORWARD 100
    RIGHT 90
    FORWARD 50
    RIGHT 90
]
```

## Debugging

```logo
CLEARSCREEN        \ Start fresh
HOME               \ Return to center
```

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/logo/](../../examples/logo/)

---

**Last Updated:** 2024
