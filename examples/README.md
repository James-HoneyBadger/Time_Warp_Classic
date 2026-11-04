# Example Programs

Two programs per language, plus a BASIC index. Each one finishes with exit
code 0 under `--run`, so together they make a quick smoke test of the
interpreters.

## Files

```
examples/
├── README.md                     this file
├── __init__.py                   lets the examples ship inside the pip package
├── basic/
│   ├── INDEX.bas                 prints a menu of all the examples
│   ├── finance_calculator.bas    compound interest, loans, savings
│   └── sales_dashboard.bas       quarterly sales report with ASCII charts
├── forth/
│   ├── engineering_calc.fth      unit conversions and Ohm's law
│   └── number_theory.fth         primes, GCD/LCM, Fibonacci, Collatz
├── javascript/
│   ├── sorting_showcase.js       five sorts, with operation counts
│   └── statistics_engine.js      descriptive stats, regression, histograms
├── logo/
│   ├── mandala_art.logo          layered mandala in RGB colours
│   └── spirograph_art.logo       spirograph-style patterns
├── pascal/
│   ├── gradebook.pas             weighted grades and class statistics
│   └── physics_calculator.pas    physics formula tables
├── perl/
│   ├── cipher_toolkit.pl         classical ciphers and frequency analysis
│   └── log_analyzer.pl           web server log report
├── pilot/
│   ├── math_tutor.pilot          15 arithmetic questions, scored
│   └── science_quiz.pilot        15 science questions, scored
├── prolog/
│   ├── expert_system.pro         animal classification rules
│   └── geography_db.pro          countries, capitals and populations
└── python/
    ├── crypto_toolkit.py         cipher classes, hashing, cryptanalysis
    └── data_pipeline.py          a small DataTable class and sales analysis
```

## Running them

**Desktop IDE.** **Program → Load Example** lists every file above by
language and switches the language selector for you. **File → Open File...**
(Ctrl+O) works too. Press **Run** or F5.

**Web IDE.** Start `python3 Time_Warp.py --web`, open
<http://127.0.0.1:8000/> and pick from the examples drop-down in the header.

**Command line.** `--run` needs `--language` for a plain source file:

```bash
python3 Time_Warp.py --run examples/basic/finance_calculator.bas --language basic
python3 Time_Warp.py --run examples/forth/number_theory.fth -l forth
```

The PILOT programs ask questions. In the IDEs, type answers into the console
bar and press Enter. On the command line they read from stdin, so you can pipe
answers in: `yes 5 | python3 Time_Warp.py --run examples/pilot/math_tutor.pilot -l pilot`.

The JavaScript and Perl examples need `node` and `perl` on your `PATH`. Python
examples use the same Python that runs Time Warp.

## What each one shows

### BASIC

| File | What it does | Language features |
|------|--------------|-------------------|
| `finance_calculator.bas` | Compound interest, loan amortisation, investment growth, savings goals, retirement projection | Unnumbered lines, `LET`, `FOR`/`NEXT`, `WHILE`/`WEND`, `DIM`, `INT` |
| `sales_dashboard.bas` | Five product lines over four quarters: totals, bar charts, statistics, a forecast | `DIM` arrays with `SUM`, `AVG`, `MAX`, `MIN`; `SQRT`; block `IF`/`ELSE`/`END IF` |
| `INDEX.bas` | Prints the list of examples | Classic numbered lines, `CLS` |

### Forth

| File | What it does | Language features |
|------|--------------|-------------------|
| `engineering_calc.fth` | Temperature, distance, weight, electrical, energy and speed conversions | Colon definitions, `VARIABLE`, stack words (`DUP`, `SWAP`, `OVER`, `ROT`, `DROP`), `."` |
| `number_theory.fth` | Primes, GCD/LCM, Fibonacci and the golden ratio, factorials, Collatz, perfect numbers, Pythagorean triples | `DO`...`LOOP`, `BEGIN`...`WHILE`...`REPEAT`, `IF`/`ELSE`/`THEN`, `MOD` |

### JavaScript

| File | What it does | Language features |
|------|--------------|-------------------|
| `sorting_showcase.js` | Bubble, selection, insertion, merge and quick sort side by side, counting comparisons and swaps | Functions, recursion, arrays, `while` loops |
| `statistics_engine.js` | Mean, median, mode, standard deviation, skewness, kurtosis, percentiles, correlation, linear regression, outliers, histograms | `const`/`let`, `Math`, `map`/`filter` |

### Logo

| File | What it does | Language features |
|------|--------------|-------------------|
| `mandala_art.logo` | Starbursts, petals, diamonds and circles in six colour layers | `TO`...`END` procedures, `REPEAT`, `MAKE`, `SETPENCOLOR [r g b]`, `SETPENSIZE`, `CIRCLE`, `PU`/`PD`, `HOME`, `HT` |
| `spirograph_art.logo` | Spiral, rose, triangular web, pentagon flower, hexagonal lace and diamond frame | Nested `REPEAT`, angle offsets, colour and pen-width changes |

The Logo examples print almost nothing; the result is on the turtle canvas.
In the web IDE use **Save PNG** to keep it.

### Pascal

| File | What it does | Language features |
|------|--------------|-------------------|
| `gradebook.pas` | Five students, four weighted subjects, letter grades, class mean and standard deviation, honour roll | `CONST`, `VAR`, `Real`/`String`, `IF` with `AND`, `WRITELN` |
| `physics_calculator.pas` | Projectile motion, free fall, waves, kinetic energy, pendulums, orbital velocity, a trig table | `FOR` loops, `SIN`, `COS`, `SQRT`, `ROUND` |

### Perl

| File | What it does | Language features |
|------|--------------|-------------------|
| `cipher_toolkit.pl` | Caesar, ROT13, Atbash, Vigenere and Rail Fence ciphers, a brute-force attack on Caesar, letter frequencies | `sub`, hashes, `ord`/`chr`, `sort`, `printf` |
| `log_analyzer.pl` | Parses Apache-style log lines: status codes, top URLs, user agents, failed logins, a health rating | Regex captures with `=~`, hashes of counts, `split`, references |

### PILOT

| File | What it does | Language features |
|------|--------------|-------------------|
| `math_tutor.pilot` | 15 mental-arithmetic questions with scoring | `T:`, `A:`, `C:`, `M:`, `MT:`, `J:`, conditional `J(...)`, `U:`/`E:` subroutines, `R:`, `{VAR}` interpolation |
| `science_quiz.pilot` | 15 questions across physics, chemistry, biology, earth science and astronomy | `M:` with alternatives (`M:ohm\|ohms`), `MT:` feedback, `U:`/`E:` subroutines |

### Prolog

| File | What it does | Language features |
|------|--------------|-------------------|
| `expert_system.pro` | Classifies 20 animals by features, diet and habitat | Facts, rules with `:-`, `?-` queries, backtracking |
| `geography_db.pro` | 21 countries with capitals, populations and currencies; regional queries | Facts, rules, shared variables across goals, `>`/`<` comparisons |

### Python

| File | What it does | Language features |
|------|--------------|-------------------|
| `crypto_toolkit.py` | Caesar, Vigenere, substitution and Playfair cipher classes; MD5/SHA hashes; avalanche effect; chi-squared cracking; password strength | Classes, comprehensions, f-strings, `hashlib`, `collections` |
| `data_pipeline.py` | A `DataTable` with filter, sort and group-by over a retail dataset; correlation; trend forecast | Classes, `lambda`, `sorted` with keys, `zip`, `enumerate` |

## Where to start

- New to all of it: `INDEX.bas`, then `mandala_art.logo`, then `math_tutor.pilot`.
- Know a modern language: compare `cipher_toolkit.pl` with `crypto_toolkit.py`.
- Want to think differently: `number_theory.fth` (stack) and `expert_system.pro` (logic).

Language references live in [../docs/languages/](../docs/languages/).
