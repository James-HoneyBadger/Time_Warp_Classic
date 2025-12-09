#!/usr/bin/env python3
"""
Code Templates System for Time_Warp IDE
Provides organized code templates by language and category
"""


class CodeTemplates:
    """Manages code templates organized by language and category"""

    def __init__(self):
        """Initialize the code templates system"""
        self.templates = self._load_templates()

    def _load_templates(self):
        """Load all code templates"""
        return {
            "TW PILOT": {
                "Basic": {
                    "Hello World": """T:Hello, World!
T:Welcome to PILOT programming!
END""",
                    "User Input": """T:What's your name?
A:
T:Hello, $INPUT!
END""",
                    "Simple Quiz": """T:What's 2 + 2?
A:
M:4
Y:T:Correct!
N:T:Try again!
END""",
                },
                "Loops": {
                    "Counting Loop": """C:COUNT = 1
*LOOP
T:Count: $COUNT
C:COUNT + 1
Y(LOOP):COUNT <= 10
END""",
                    "Menu System": """*MENU
T:Choose: 1) Start 2) Help 3) Exit
A:
M:1
Y:J(START)
M:2
Y:J(HELP)
M:3
Y:J(EXIT)
J(MENU)
*START
T:Let's begin!
END""",
                },
                "Graphics": {
                    "Simple Drawing": """PENDOWN
FORWARD 100
RIGHT 90
FORWARD 100
PENUP
END""",
                    "Square Pattern": """REPEAT 4
  FORWARD 100
  RIGHT 90
END
END""",
                    "Spiral": """C:SIZE = 10
*SPIRAL
FORWARD $SIZE
RIGHT 91
C:SIZE + 5
Y(SPIRAL):SIZE < 200
END""",
                },
                "Games": {
                    "Number Guessing": """C:NUMBER = RND(100) + 1
C:TRIES = 0
*GUESS
T:Guess my number (1-100):
A:
C:TRIES + 1
Y(HIGH):INPUT > NUMBER
Y(LOW):INPUT < NUMBER
T:Correct in $TRIES tries!
E:
*HIGH
T:Too high!
J(GUESS)
*LOW
T:Too low!
J(GUESS)
END"""
                },
                "Math": {
                    "Calculator": """T:Enter first number:
A:
C:NUM1 = INPUT
T:Enter second number:
A:
C:NUM2 = INPUT
T:Sum: $NUM1 + $NUM2 = $(NUM1 + NUM2)
END"""
                },
            },
            "TW BASIC": {
                "Basic": {
                    "Hello World": """10 PRINT "Hello, World!"
20 PRINT "Welcome to BASIC programming!"
30 END""",
                    "User Input": """10 PRINT "What's your name?"
20 INPUT NAME$
30 PRINT "Hello, "; NAME$; "!"
40 END""",
                    "Simple Math": """10 LET A = 5
20 LET B = 3
30 PRINT "Sum:"; A + B
40 PRINT "Product:"; A * B
50 END""",
                },
                "Loops": {
                    "FOR Loop": """10 FOR I = 1 TO 10
20 PRINT "Count:"; I
30 NEXT I
40 END""",
                    "WHILE Loop": """10 LET COUNT = 1
20 WHILE COUNT <= 10
30 PRINT "Count:"; COUNT
40 LET COUNT = COUNT + 1
50 WEND
60 END""",
                },
                "Graphics": {
                    "Simple Graphics": """10 SCREEN 12
20 LINE (100,100)-(200,200)
30 CIRCLE (150,150), 50
40 END""",
                    "Color Demo": """10 FOR I = 1 TO 15
20 COLOR I
30 PRINT "Color"; I
40 NEXT I
50 END""",
                },
                "Games": {
                    "Guess Number": """10 RANDOMIZE TIMER
20 SECRET = INT(RND * 100) + 1
30 PRINT "Guess my number (1-100):"
40 INPUT GUESS
50 IF GUESS = SECRET THEN PRINT "Correct!": END
60 IF GUESS < SECRET THEN PRINT "Too low!"
70 IF GUESS > SECRET THEN PRINT "Too high!"
80 GOTO 30"""
                },
                "Math": {
                    "Factorial": """10 PRINT "Enter a number:"
20 INPUT N
30 LET FACT = 1
40 FOR I = 1 TO N
50 LET FACT = FACT * I
60 NEXT I
70 PRINT "Factorial:"; FACT
80 END"""
                },
            },
            "TW Logo": {
                "Basic": {
                    "Hello World": """print [Hello World]
print [Welcome to Logo]
bye""",
                    "Simple Movement": """forward 100
right 90
forward 100
bye""",
                },
                "Loops": {
                    "Repeat Square": """repeat 4 [forward 100 right 90]
bye""",
                    "Spiral": """for [size 10 200 10] [forward :size right 91]
bye""",
                },
                "Graphics": {
                    "Color Square": """setpencolor [255 0 0]
repeat 4 [forward 100 right 90]
setpencolor [0 255 0]
forward 50
repeat 4 [forward 50 right 90]
bye""",
                    "Flower": """repeat 6 [repeat 4 [forward 50 right 90] right 60]
bye""",
                },
                "Games": {
                    "Simple Game": """to guess
  make "secret random 100
  make "tries 0
  ask "Guess my number (1-100):
  while [not equalp :guess :secret] [
    make "tries :tries + 1
    if :guess < :secret [print [Too low!]]
    if :guess > :secret [print [Too high!]]
    ask "Try again:
  ]
  print sentence [Correct in] word :tries [tries!]
end
guess
bye"""
                },
                "Math": {
                    "Multiplication Table": """to table :n
  for [i 1 10] [print (sentence :i "* :n =) i * :n]
end
table 5
bye"""
                },
            },
            "Python": {
                "Basic": {
                    "Hello World": """print("Hello, World!")
print("Welcome to Python programming!")""",
                    "User Input": """name = input("What's your name? ")
print(f"Hello, {name}!")""",
                    "Variables": """# Variable examples
name = "Alice"
age = 25
height = 5.6

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")""",
                },
                "Loops": {
                    "For Loop": """for i in range(1, 11):
    print(f"Count: {i}")""",
                    "While Loop": """count = 1
while count <= 10:
    print(f"Count: {count}")
    count += 1""",
                    "List Comprehension": """numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)""",
                },
                "Functions": {
                    "Simple Function": """def greet(name):
    return f"Hello, {name}!"

result = greet("World")
print(result)""",
                    "Recursive Function": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))""",
                },
                "Graphics": {
                    "Turtle Graphics": """import turtle

t = turtle.Turtle()
for _ in range(4):
    t.forward(100)
    t.right(90)

turtle.done()""",
                    "Pygame Basic": """import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()""",
                },
                "Games": {
                    "Number Guessing": """import random

secret = random.randint(1, 100)
tries = 0

while True:
    guess = int(input("Guess (1-100): "))
    tries += 1
    if guess == secret:
        print(f"Correct in {tries} tries!")
        break
    elif guess < secret:
        print("Too low!")
    else:
        print("Too high!")"""
                },
                "Math": {
                    "Calculator": """def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x + y

def divide(x, y):
    if y != 0:
        return x / y
    return "Cannot divide by zero"

print("Select operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")

choice = input("Enter choice (1/2/3/4): ")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if choice == '1':
    print(add(num1, num2))
elif choice == '2':
    print(subtract(num1, num2))
elif choice == '3':
    print(multiply(num1, num2))
elif choice == '4':
    print(divide(num1, num2))
else:
    print("Invalid input")"""
                },
            },
            "JavaScript": {
                "Basic": {
                    "Hello World": """console.log("Hello, World!");
console.log("Welcome to JavaScript!");""",
                    "User Input": """const name = prompt("What's your name?");
console.log(`Hello, ${name}!`);""",
                    "Variables": """let name = "Alice";
const age = 25;
var height = 5.6;

console.log(`Name: ${name}`);
console.log(`Age: ${age}`);
console.log(`Height: ${height}`);""",
                },
                "Loops": {
                    "For Loop": """for (let i = 1; i <= 10; i++) {
    console.log(`Count: ${i}`);
}""",
                    "While Loop": """let count = 1;
while (count <= 10) {
    console.log(`Count: ${count}`);
    count++;
}""",
                    "Array Methods": """const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(x => x ** 2);
console.log(squares);""",
                },
                "Functions": {
                    "Arrow Function": """const greet = (name) => `Hello, ${name}!`;

console.log(greet("World"));""",
                    "Async Function": """async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

fetchData();""",
                },
                "DOM": {
                    "Button Click": """<button id="myButton">Click me</button>
<p id="output"></p>

<script>
document.getElementById('myButton').addEventListener('click', function() {
    document.getElementById('output').textContent = 'Button clicked!';
});
</script>""",
                    "Form Validation": """<form id="myForm">
    <input type="email" id="email" required>
    <button type="submit">Submit</button>
</form>

<script>
document.getElementById('myForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    if (email.includes('@')) {
        alert('Valid email!');
    } else {
        alert('Invalid email!');
    }
});
</script>""",
                },
                "Games": {
                    "Rock Paper Scissors": """function getComputerChoice() {
    const choices = ['rock', 'paper', 'scissors'];
    return choices[Math.floor(Math.random() * choices.length)];
}

function playGame(playerChoice) {
    const computerChoice = getComputerChoice();
    console.log(`You: ${playerChoice}, Computer: ${computerChoice}`);

    if (playerChoice === computerChoice) {
        console.log("It's a tie!");
    } else if (
        (playerChoice === 'rock' && computerChoice === 'scissors') ||
        (playerChoice === 'paper' && computerChoice === 'rock') ||
        (playerChoice === 'scissors' && computerChoice === 'paper')
    ) {
        console.log("You win!");
    } else {
        console.log("Computer wins!");
    }
}

// Example usage
playGame('rock');"""
                },
                "Math": {
                    "Calculator": """function add(x, y) { return x + y; }
function subtract(x, y) { return x - y; }
function multiply(x, y) { return x * y; }
function divide(x, y) { return y !== 0 ? x / y : 'Cannot divide by zero'; }

const operation = prompt("Choose operation (add/subtract/multiply/divide):");
const num1 = parseFloat(prompt("Enter first number:"));
const num2 = parseFloat(prompt("Enter second number:"));

let result;
switch (operation) {
    case 'add':
        result = add(num1, num2);
        break;
    case 'subtract':
        result = subtract(num1, num2);
        break;
    case 'multiply':
        result = multiply(num1, num2);
        break;
    case 'divide':
        result = divide(num1, num2);
        break;
    default:
        result = 'Invalid operation';
}

console.log(`Result: ${result}`);"""
                },
            },
            "TW Pascal": {
                "Basic": {
                    "Hello World": """program HelloWorld;
begin
  writeln('Hello, World!');
end.""",
                    "User Input": """program UserInput;
var
  name: string;
begin
  write('What is your name? ');
  readln(name);
  writeln('Hello, ', name, '!');
end.""",
                    "Variables Demo": """program VariablesDemo;
const
  PI = 3.14159;
var
  radius, area: real;
begin
  radius := 5.0;
  area := PI * radius * radius;
  writeln('Area of circle: ', area:0:2);
end.""",
                    "Conditional Demo": """program ConditionalDemo;
var
  number: integer;
begin
  write('Enter a number: ');
  readln(number);
  if number > 0 then
    writeln('Positive number')
  else if number < 0 then
    writeln('Negative number')
  else
    writeln('Zero');
end.""",
                },
                "Loops": {
                    "For Loop": """program ForLoopDemo;
var
  i: integer;
begin
  for i := 1 to 10 do
    writeln('Count: ', i);
end.""",
                    "While Loop": """program WhileLoopDemo;
var
  count: integer;
begin
  count := 1;
  while count <= 10 do
  begin
    writeln('Count: ', count);
    count := count + 1;
  end;
end.""",
                    "Repeat Loop": """program RepeatLoopDemo;
var
  num: integer;
begin
  repeat
    write('Enter a positive number: ');
    readln(num);
  until num > 0;
  writeln('You entered: ', num);
end.""",
                },
                "Graphics": {
                    "Simple Drawing": """program SimpleDrawing;
uses
  Graph;
var
  gd, gm: integer;
begin
  gd := Detect;
  InitGraph(gd, gm, '');
  if GraphResult <> grOk then
    Halt(1);

  { Draw a circle }
  Circle(320, 240, 100);

  { Draw a rectangle }
  Rectangle(200, 150, 440, 330);

  Readln;
  CloseGraph;
end.""",
                    "Turtle Graphics": """program TurtleGraphics;
var
  x, y, angle: real;
begin
  x := 320;
  y := 240;
  angle := 0;

  { Move forward }
  x := x + 50 * cos(angle * PI / 180);
  y := y + 50 * sin(angle * PI / 180);

  { Turn right }
  angle := angle + 90;

  writeln('New position: (', x:0:0, ', ', y:0:0, ')');
end.""",
                },
                "Games": {
                    "Number Guessing": """program GuessingGame;
var
  secret, guess: integer;
begin
  randomize;
  secret := random(100) + 1;
  writeln('I am thinking of a number between 1 and 100.');

  repeat
    write('Guess: ');
    readln(guess);
    if guess < secret then
      writeln('Too low!')
    else if guess > secret then
      writeln('Too high!')
    else
      writeln('Correct!');
  until guess = secret;
end.""",
                    "Calculator": """program Calculator;
var
  num1, num2, result: real;
  op: char;
begin
  write('Enter first number: ');
  readln(num1);
  write('Enter operator (+, -, *, /): ');
  readln(op);
  write('Enter second number: ');
  readln(num2);

  case op of
    '+': result := num1 + num2;
    '-': result := num1 - num2;
    '*': result := num1 * num2;
    '/': if num2 <> 0 then result := num1 / num2 else result := 0;
  end;

  writeln('Result: ', result:0:2);
end.""",
                },
                "Math": {
                    "Factorial": """program FactorialDemo;
function Factorial(n: integer): longint;
begin
  if n <= 1 then
    Factorial := 1
  else
    Factorial := n * Factorial(n - 1);
end;

var
  num: integer;
begin
  write('Enter a number: ');
  readln(num);
  writeln(num, '! = ', Factorial(num));
end.""",
                    "Prime Check": """program PrimeCheck;
function IsPrime(n: integer): boolean;
var
  i: integer;
begin
  if n < 2 then
    IsPrime := false
  else
  begin
    IsPrime := true;
    for i := 2 to trunc(sqrt(n)) do
      if n mod i = 0 then
        IsPrime := false;
  end;
end;

var
  num: integer;
begin
  write('Enter a number: ');
  readln(num);
  if IsPrime(num) then
    writeln(num, ' is prime')
  else
    writeln(num, ' is not prime');
end.""",
                    "Fibonacci": """program FibonacciDemo;
function Fibonacci(n: integer): longint;
begin
  if n <= 1 then
    Fibonacci := n
  else
    Fibonacci := Fibonacci(n - 1) + Fibonacci(n - 2);
end;

var
  i: integer;
begin
  for i := 0 to 10 do
    write(Fibonacci(i), ' ');
  writeln;
end.""",
                },
            },
            "TW Prolog": {
                "Basic": {
                    "Hello World": """Hello Prolog""",
                },
            },
            "TW Forth": {
                "Basic": {
                    "Hello World": """Hello Forth""",
                },
            },
            "Perl": {
                "Basic": {
                    "Hello World": """print "Hello, World!\\n";""",
                },
            },
        }

    def get_languages(self):
        """Get all available languages"""
        return list(self.templates.keys())

    def get_categories(self, language):
        """Get categories for a language"""
        if language in self.templates:
            return list(self.templates[language].keys())
        return []

    def get_templates(self, language, category):
        """Get templates for a language and category"""
        if language in self.templates and category in self.templates[language]:
            return list(self.templates[language][category].keys())
        return []

    def get_template_code(self, language, category, template_name):
        """Get the code for a specific template"""
        if (
            language in self.templates
            and category in self.templates[language]
            and template_name in self.templates[language][category]
        ):
            return self.templates[language][category][template_name]
        return ""

    def get_template_info(self, language, category, template_name):
        """Get template information including code and metadata"""
        code = self.get_template_code(language, category, template_name)
        if code:
            return {
                "name": template_name,
                "language": language,
                "category": category,
                "code": code,
                "lines": len(code.split("\n")),
            }
        return None
