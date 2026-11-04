# Python in Time Warp Classic

Time Warp does not reimplement Python. It saves your program to a temporary
`.py` file and runs it with a real Python 3 interpreter in a separate
process. Anything that works in Python will work here, within the limits
below.

This page covers what is different inside Time Warp: which interpreter
runs, how output and input travel, time limits, and error reporting. For
the language itself, the [official Python documentation](#further-reading)
is the reference.

## At a glance

| Topic | Behaviour |
|-------|-----------|
| Runtime | The Python that runs Time Warp itself (`sys.executable`); `python3`, then `python`, as fallbacks |
| Output | stdout and stderr merged, shown line by line as the program prints |
| Input | The console bar feeds the program's stdin, one line per Enter |
| Time limit | 30 s in the desktop IDE and `timewarp --run`; 10 s by default in the web IDE |
| Stop | Ctrl+. (desktop) or the Stop button (web); the console shows `BREAK` |
| Errors | `?ERROR IN n: ...` naming the editor line, often followed by a `?HINT:` line |
| Turtle graphics | Not available |
| Console REPL | Each line runs in a fresh process; nothing carries over |

## Which Python runs

Time Warp runs your program with the same interpreter that started the IDE
or the web server (Time Warp needs Python 3.9 or later). To see which one,
run `import sys; print(sys.version)` from the console bar. Two
consequences:

- Packages installed in that environment (for example, the virtualenv you
  installed Time Warp into) are importable. Packages installed elsewhere are
  not.
- The web container image is built on Python 3.12, so programs there run
  on 3.12.

If that interpreter somehow cannot be started, Time Warp tries `python3`
and then `python` on `PATH`. When none work, a run prints:

```text
?PYTHON NOT FOUND - install it to run these scripts
```

In practice this does not happen: if Time Warp is running, so is a
Python.

## How a run works

1. The editor text is written to a temporary file such as
   `/tmp/tmpk3x9q1ab.py`. That name appears in tracebacks; the line numbers
   match the editor.
2. Time Warp starts `python -u <file>`. The `-u` flag and the environment
   variables `PYTHONUNBUFFERED=1` and `PYTHONIOENCODING=utf-8` (set only if
   not already set) keep output unbuffered and UTF-8. On Linux and macOS
   the command is also wrapped in `stdbuf -oL -eL` when `stdbuf` exists.
3. The working directory is the directory Time Warp was started from, not
   the folder your file is saved in. Relative paths in `open()` resolve
   from there.
4. `sys.path[0]` is the temporary directory, so modules sitting next to
   your saved file cannot be imported by name. Use absolute paths, or add
   the folder to `sys.path` yourself.
5. When the program ends, the temporary file is deleted.

Your program runs in its own process. It cannot reach the IDE's variables,
canvas or editor, and a crash in your program cannot take the IDE down.

## Output

- Output appears line by line while the program runs, so progress
  messages show up as they are printed.
- A line is shown when its newline arrives. `print("Working", end="")`
  stays invisible until a later newline or the end of the program.
- stderr is merged into the same stream, so warnings and tracebacks
  appear in order with normal output.
- The web IDE stops a run after 20,000 lines of output
  (`Stopped: output limit of 20000 lines reached`).

## Input

While a program is running, the console bar sends what you type to the
program's stdin. Each Enter sends one line, which is also echoed in the
console. `input()` reads it as usual.

```python
print("Name?")
name = input()
print("Age?")
age = int(input())
print(f"Hello, {name}. Next year you will be {age + 1}.")
```

Typing `Ada` and then `41` gives:

```text
Name?
Ada
Age?
41
Hello, Ada. Next year you will be 42.
```

Things to know:

- **Put prompts on their own line.** `input("Name? ")` writes the prompt
  without a newline, so it does not appear until the next newline and then
  shows up glued to later output. `print("Name?")` followed by `input()`
  avoids this.
- **Typing ahead works.** Lines typed before the program asks for them
  wait in the pipe.
- **There is no end-of-file.** stdin stays open for the whole run, so
  `sys.stdin.read()` or `for line in sys.stdin:` waits until the time limit
  ends the program. Read a known number of lines with `input()`, or stop
  at a sentinel such as an empty line.
- **Waiting counts toward the time limit.** For Python, JavaScript and
  Perl the clock keeps running while the program waits for you. (The
  built-in languages pause it at `INPUT`.) In the web IDE the default
  limit is 10 seconds, so answer promptly or raise it with
  `timewarp --web --timeout N`.
- **The web IDE cannot tell that the program is waiting.** The console bar
  reads "Input for the running program" rather than a prompt. Type anyway.

## Time limits and stopping

| Where | Limit | What you see |
|-------|-------|--------------|
| Desktop IDE, `timewarp --run` | 30 s | `?ERROR: Python script timed out after 30s` and a `?HINT:` |
| Web IDE | 10 s (set with `--timeout`) | `Stopped: time limit of 10s reached`, then `BREAK` |

The 30-second limit belongs to the Python runner itself, so it also caps
web runs: setting `--timeout 60` still ends a Python program after 30
seconds.

To stop a program early, press Ctrl+. in the desktop IDE or the Stop
button in the browser. The process is killed and the console prints
`BREAK`.

## Errors and hints

When Python exits with an error, Time Warp shows the traceback, then a
summary line naming the editor line, and a hint when it recognises the
error:

```python
print("hi")
x = 1
y = x / 0
```

```text
hi
Traceback (most recent call last):
  File "/tmp/tmpdkihht94.py", line 3, in <module>
    y = x / 0
        ~~^~~
ZeroDivisionError: division by zero
?ERROR IN 3: ZeroDivisionError: division by zero
?HINT: a value in the expression is 0 - check the divisor before dividing. See docs/languages/PYTHON_REFERENCE.md.
```

- The line number comes from the last traceback frame inside your file.
  In the desktop IDE, click the `?ERROR IN` line to jump to it.
- Hints exist for division by zero, undefined names (`NameError`),
  indentation errors, missing modules, syntax errors, type mix-ups
  (`can only concatenate`, `unsupported operand`) and time-outs. Other
  errors get no hint.
- A non-zero exit without a traceback, such as `sys.exit(3)`, is reported
  as `?ERROR: Python script exited with code 3`.

## The console REPL

When no program is running, a line typed in the console bar is run as a
complete, one-line program in a brand-new Python process:

```text
>print(2 ** 10)
1024
>x = 5
>print(x)
...
NameError: name 'x' is not defined
```

Nothing persists between lines: no variables, no imports. Each line also
has a 2-second limit, after which it is stopped without a message, and
`input()` cannot be answered from the REPL. For anything longer than a
one-liner, use the editor and Run.

## Turtle graphics

Not available. The Time Warp canvas is driven only by the built-in
languages (Logo, BASIC, PILOT and friends). A Python program cannot draw
on it.

Python's own `turtle` module is a separate thing: in the desktop IDE it
tries to open its own Tk window from the child process, and in the web
IDE there is no display for it. Use Logo for turtle work.

## Cheat sheet

Enough Python to read the examples. The [tutorial](#further-reading)
covers the rest.

| Task | Python |
|------|--------|
| Print | `print("x =", x)`, `print(f"{x:.2f}")` |
| Read a line | `s = input()`; number: `n = int(input())` |
| Variables | `x = 10`, `name = "Ada"`, `ok = True` |
| Arithmetic | `+ - * /` (true division), `//` floor, `%` mod, `**` power |
| Compare / logic | `== != < <= > >=`, `and or not` |
| If | `if x > 0:` / `elif x == 0:` / `else:` (indent the body) |
| Counted loop | `for i in range(1, 11):` |
| While | `while n > 0:` |
| Function | `def area(w, h): return w * h` |
| List | `xs = [1, 2, 3]`, `xs.append(4)`, `xs[0]`, `xs[-1]`, `len(xs)` |
| Dict | `d = {"a": 1}`, `d["b"] = 2`, `d.get("c", 0)` |
| Loop with index | `for i, x in enumerate(xs):` |
| Comprehension | `[x * x for x in xs if x % 2]` |
| Strings | `s.upper()`, `s.split()`, `", ".join(parts)`, `s[1:4]` |
| Errors | `try:` / `except ValueError as e:` / `finally:` |
| Modules | `import math`, `from random import randint` |
| Comment | `# like this` |

A complete program:

```python
def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))

primes = [n for n in range(50) if is_prime(n)]
print(len(primes), "primes below 50:")
print(primes)
```

```text
15 primes below 50:
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

## Known limitations (1.6.0)

- `timewarp --run file.py --language python` does not pass the terminal's
  stdin to the program, so `input()` waits until the 30-second limit.
- A REPL line that runs past 2 seconds is stopped silently.

## Further reading

- [Python documentation](https://docs.python.org/3/) - match the version
  your Time Warp runs on
- [The Python Tutorial](https://docs.python.org/3/tutorial/)
- [Library reference](https://docs.python.org/3/library/)
- Examples: [examples/python/](../../examples/python/)
- [Language tutorials](../user/LANGUAGE_TUTORIALS.md#python)
