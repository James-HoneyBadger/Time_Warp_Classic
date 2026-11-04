# JavaScript in Time Warp Classic

Time Warp does not reimplement JavaScript. It saves your program to a
temporary `.js` file and runs it with [Node.js](https://nodejs.org/) in a
separate process. This is server-side JavaScript: there is no browser, no
DOM, no `alert()` and no `document`, even in the web IDE.

This page covers what is different inside Time Warp: how Node is found, how
output and input travel, time limits, and error reporting. For the language
itself, see the [official documentation](#further-reading).

## At a glance

| Topic | Behaviour |
|-------|-----------|
| Runtime | `node` on `PATH`, then `nodejs`; must be installed separately |
| Output | stdout and stderr merged, shown line by line as the program prints |
| Input | The console bar feeds the program's stdin; read it with `readline` |
| Time limit | 30 s in the desktop IDE and `timewarp --run`; 10 s by default in the web IDE |
| Stop | Ctrl+. (desktop) or the Stop button (web); the console shows `BREAK` |
| Errors | `?ERROR IN n: ...` naming the editor line, often followed by a `?HINT:` line |
| Turtle graphics | Not available |
| Console REPL | Each line runs in a fresh process; nothing carries over |

## Which Node runs

Time Warp looks for `node`, then `nodejs`, on `PATH`, and uses the first
one whose `node --version` succeeds. It does not bundle Node. Install it
from [nodejs.org](https://nodejs.org/) or your package manager
(`apt install nodejs`, `brew install node`).

The version matters. Language features, and whether `import` statements
work in a plain `.js` file, depend on the Node you have. Node 20.19 and
later detect ES module syntax automatically; older versions need
`require()`. To check, run `console.log(process.version)` from the console
bar.

The web container image (`Dockerfile.web`) does not install Node by
default (the lines are there, commented out), so JavaScript is
unavailable there until you enable them.

### When Node is missing

The language menu shows JavaScript as "(runtime missing)" (in the web IDE
the status bar also says "JavaScript needs its runtime installed on the
server"). Running anyway prints:

```text
?JAVASCRIPT NOT FOUND - install it to run these scripts (install Node.js from nodejs.org)
```

Install Node and restart Time Warp.

## How a run works

1. The editor text is written to a temporary file such as
   `/tmp/tmpdffr8nwp.js`. That name appears in stack traces; the line
   numbers match the editor.
2. Time Warp starts `node <file>`. On Linux and macOS the command is
   wrapped in `stdbuf -oL -eL` when `stdbuf` exists.
3. The working directory is the directory Time Warp was started from, not
   the folder your file is saved in. Relative paths in `fs` calls resolve
   from there.
4. `require()` and `import` look for packages relative to the temporary
   file, so a `node_modules` folder next to your saved file is **not**
   found. Globally installed modules are not found either. Point
   `NODE_PATH` at a `node_modules` folder before starting Time Warp:

   ```bash
   NODE_PATH=$HOME/myproject/node_modules timewarp
   ```

   Built-in modules (`fs`, `path`, `readline`, `os`, ...) always work.
5. When the program ends, the temporary file is deleted.

Node exits when there is nothing left to do: no pending timers, promises
or open streams. A program that leaves a `readline` interface open keeps
running until the time limit, so close it when you are done.

## Output

- `console.log`, `console.error` and `process.stdout.write` all go to the
  console, in order.
- A line is shown when its newline arrives. `process.stdout.write("...")`
  without `\n` stays invisible until a later newline or the end of the
  program.
- Objects and arrays print in Node's inspect format:
  `console.log([3, 1, 2], {k: 1})` shows `[ 3, 1, 2 ] { k: 1 }`.
- The web IDE stops a run after 20,000 lines of output
  (`Stopped: output limit of 20000 lines reached`).

## Input

While a program is running, the console bar sends what you type to the
program's stdin, one line per Enter, echoed in the console. Node has no
built-in `input()`; this small helper does the job:

```javascript
const readline = require("readline");
const rl = readline.createInterface({ input: process.stdin });
const lines = rl[Symbol.asyncIterator]();
async function ask(question) {
  console.log(question);
  return (await lines.next()).value;
}

async function main() {
  const name = await ask("Name?");
  const age = Number(await ask("Age?"));
  console.log(`Hello, ${name}. Next year you will be ${age + 1}.`);
  rl.close();
}
main();
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

- **Print prompts with `console.log`.** A prompt written without a newline
  (`rl.question("Name? ", ...)`) does not appear until the next newline.
- **Typing ahead works.** Lines typed early wait in the pipe.
- **There is no end-of-file.** stdin stays open, so a `rl.on("close")`
  handler never fires and `for await (const line of rl)` never finishes on
  its own. Stop at a known count or a sentinel line, then call
  `rl.close()`.
- **Waiting counts toward the time limit.** The built-in languages pause
  the clock at `INPUT`; Node programs do not. In the web IDE the default
  limit is 10 seconds; raise it with `timewarp --web --timeout N`.
- **The web IDE cannot tell that the program is waiting.** Type anyway.

## Time limits and stopping

| Where | Limit | What you see |
|-------|-------|--------------|
| Desktop IDE, `timewarp --run` | 30 s | `?ERROR: JavaScript script timed out after 30s` and a `?HINT:` |
| Web IDE | 10 s (set with `--timeout`) | `Stopped: time limit of 10s reached`, then `BREAK` |

The 30-second limit belongs to the JavaScript runner itself, so it also
caps web runs whose `--timeout` is higher. A `setInterval` that is never
cleared keeps Node alive until one of these limits ends it.

To stop a program early, press Ctrl+. in the desktop IDE or the Stop
button in the browser. The process is killed and the console prints
`BREAK`.

## Errors and hints

When Node exits with an error, Time Warp shows Node's message and stack
trace, then a summary line and, when it recognises the error, a hint:

```javascript
const total = 10;
console.log(totl);
```

```text
/tmp/tmpdffr8nwp.js:2
console.log(totl);
            ^

ReferenceError: totl is not defined
    at Object.<anonymous> (/tmp/tmpdffr8nwp.js:2:13)
    ...
Node.js v20.20.2
?ERROR IN 2: ReferenceError: totl is not defined
?HINT: give the name a value before using it - check the spelling too. See docs/languages/JAVASCRIPT_REFERENCE.md.
```

- The line number comes from the stack trace. In the desktop IDE, click
  the `?ERROR IN` line to jump to it.
- Hints exist for undefined names, syntax errors and time-outs. Other
  errors, such as `TypeError: Cannot read properties of null`, get the
  `?ERROR` line only. Dividing by zero is not an error in JavaScript;
  it gives `Infinity` or `NaN`.
- Syntax errors are reported as `?ERROR:` without a line number. The line
  is in Node's first output line (`/tmp/....js:3`).
- A missing module currently produces an unhelpful summary
  (`?ERROR IN 1: requireStack: [...]`). Read the `Error: Cannot find
  module 'name'` line above it.
- Unhandled promise rejections are errors too and are reported the same
  way.
- `process.exit(3)` is reported as
  `?ERROR: JavaScript script exited with code 3`.

## The console REPL

When no program is running, a line typed in the console bar is run as a
complete, one-line program in a brand-new Node process:

```text
>console.log([1, 2, 3].map(x => x * 2))
[ 2, 4, 6 ]
```

Nothing persists between lines, and a bare expression such as `2 + 2`
prints nothing: wrap it in `console.log()`. Each line has a 2-second
limit, after which it is stopped without a message.

## Turtle graphics

Not available. The Time Warp canvas is driven only by the built-in
languages. Use Logo for turtle work.

## Cheat sheet

| Task | JavaScript |
|------|-----------|
| Print | `console.log("x =", x)`, `` console.log(`${x.toFixed(2)}`) `` |
| Variables | `const pi = 3.14;` `let n = 0;` (avoid `var`) |
| Arithmetic | `+ - * / %`, `**` power, `Math.floor(a / b)` integer division |
| Compare / logic | `=== !== < <= > >=`, `&& \|\| !` (prefer `===` to `==`) |
| If | `if (x > 0) { ... } else if (x === 0) { ... } else { ... }` |
| Counted loop | `for (let i = 1; i <= 10; i++) { ... }` |
| Loop over array | `for (const x of xs) { ... }` |
| Function | `function area(w, h) { return w * h; }` or `const area = (w, h) => w * h;` |
| Array | `const xs = [1, 2, 3]; xs.push(4); xs.length; xs.at(-1)` |
| Array methods | `xs.map(f)`, `xs.filter(f)`, `xs.reduce((a, b) => a + b, 0)` |
| Sort numbers | `xs.sort((a, b) => a - b)` (the default sort is by string) |
| Object | `const p = { name: "Ada", age: 41 }; p.name; Object.keys(p)` |
| Map | `const m = new Map(); m.set("a", 1); m.get("a")` |
| Strings | `s.toUpperCase()`, `s.split(" ")`, `parts.join(", ")`, `s.slice(1, 4)` |
| Numbers | `Number("42")`, `parseInt(s, 10)`, `Math.round(x)`, `Math.random()` |
| Errors | `try { ... } catch (e) { console.log(e.message); }` |
| Async | `await new Promise(r => setTimeout(r, 500));` inside an `async` function |
| Comment | `// line` or `/* block */` |

A complete program:

```javascript
function isPrime(n) {
  if (n < 2) return false;
  for (let d = 2; d * d <= n; d++) {
    if (n % d === 0) return false;
  }
  return true;
}

const primes = [];
for (let n = 0; n < 50; n++) {
  if (isPrime(n)) primes.push(n);
}
console.log(`${primes.length} primes below 50:`);
console.log(primes.join(" "));
```

```text
15 primes below 50:
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
```

## Known limitations (1.6.0)

- `timewarp --run file.js --language javascript` does not pass the
  terminal's stdin to the program.
- Syntax errors and missing modules get poor `?ERROR` summary lines (see
  above).
- A REPL line that runs past 2 seconds is stopped silently.

## Further reading

- [Node.js documentation](https://nodejs.org/docs/latest/api/) - use the
  version matching your `node --version`
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [MDN JavaScript Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)
- Examples: [examples/javascript/](../../examples/javascript/)
- [Language tutorials](../user/LANGUAGE_TUTORIALS.md#javascript)
