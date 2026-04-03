# Time Warp Classic - Example Programs

Full-featured, practical programs for all 9 supported languages.
Each program is a standalone application that demonstrates real-world
use of the language while exercising its full capabilities.

---

## Directory Structure

```
examples/
├── README.md                        # This file
├── basic/
│   ├── finance_calculator.bas       # Personal finance calculator
│   ├── sales_dashboard.bas          # Sales analytics dashboard
│   └── INDEX.bas                    # Index of all examples
├── forth/
│   ├── engineering_calc.fth         # Engineering unit converter
│   └── number_theory.fth           # Number theory toolkit
├── javascript/
│   ├── sorting_showcase.js          # Sorting algorithm comparison
│   └── statistics_engine.js         # Statistical analysis engine
├── logo/
│   ├── mandala_art.logo             # Multi-layered mandala generator
│   └── spirograph_art.logo          # Spirograph pattern collection
├── pascal/
│   ├── gradebook.pas                # Student grade book system
│   └── physics_calculator.pas       # Physics formula calculator
├── perl/
│   ├── log_analyzer.pl              # Server log analyzer
│   └── cipher_toolkit.pl            # Cryptographic cipher toolkit
├── pilot/
│   ├── science_quiz.pilot           # Interactive science quiz
│   └── math_tutor.pilot             # Mental math trainer
├── prolog/
│   ├── expert_system.pro            # Animal classification expert system
│   └── geography_db.pro             # World geography knowledge base
└── python/
    ├── crypto_toolkit.py            # Cryptography toolkit
    └── data_pipeline.py             # Data analysis pipeline
```

---

## Programs by Language

### BASIC

| Program | Description |
|---------|-------------|
| `finance_calculator.bas` | Compound interest, loan amortization, investment growth projections, savings goals, and retirement planning with formatted tables |
| `sales_dashboard.bas` | Sales analytics with 5 product lines, quarterly data, ASCII bar charts, statistical analysis, and revenue forecasting |

**Features used:** Variables, arrays (DIM/SUM/AVG), FOR/NEXT loops, GOSUB/RETURN subroutines, IF/THEN/ELSE, string formatting, math functions (SQR, INT, RND), PRINT TAB

---

### Forth

| Program | Description |
|---------|-------------|
| `engineering_calc.fth` | Temperature, distance, weight, electrical (Ohm's law), energy, and speed unit conversions with formatted output |
| `number_theory.fth` | Prime numbers (sieve/counting), GCD/LCM (Euclid's algorithm), Fibonacci with golden ratio, factorials, Collatz conjecture, perfect numbers, Pythagorean triples |

**Features used:** Stack manipulation (DUP, SWAP, OVER, ROT, DROP), colon definitions, variables, DO...LOOP, BEGIN...UNTIL, IF/ELSE/THEN, MOD, nested word calls, formatted output (.  ." )

---

### JavaScript

| Program | Description |
|---------|-------------|
| `sorting_showcase.js` | Side-by-side comparison of 5 sorting algorithms (bubble, selection, insertion, merge, quick) with operation counting and performance analysis |
| `statistics_engine.js` | Full statistical analysis: mean, median, mode, standard deviation, skewness, kurtosis, percentiles, correlation, linear regression, outlier detection, histograms |

**Features used:** Functions, arrays, objects, Math library, loops (for/while), conditionals, string methods, template literals, closures, higher-order functions (map/filter/reduce), recursion

---

### Logo

| Program | Description |
|---------|-------------|
| `mandala_art.logo` | Six-layered mandala with color-coded geometric elements: starbursts, petals, diamonds, and concentric circles using procedures and RGB colors |
| `spirograph_art.logo` | Six distinct spirograph patterns: growing spiral, rose, triangular web, pentagon flower, hexagonal lace, and diamond frame |

**Features used:** TO/END procedures, REPEAT loops, MAKE variables, SETPENCOLOR (RGB), SETPENSIZE, FORWARD/BACKWARD, RIGHT/LEFT, PENUP/PENDOWN, CIRCLE, CLEARSCREEN, HOME

---

### Pascal

| Program | Description |
|---------|-------------|
| `gradebook.pas` | Student grade management for 5 students across 4 subjects with weighted averages, letter grades, class statistics (mean, variance, standard deviation), and honor roll |
| `physics_calculator.pas` | Physics formula tables: projectile motion, free fall, electromagnetic spectrum, kinetic energy, pendulum periods, orbital mechanics, and trigonometry |

**Features used:** VAR/CONST declarations, typed variables (Integer, Real, String), FOR loops, IF/THEN with AND/OR, WRITELN with expressions, math functions (SIN, COS, SQRT, SQR, POWER, LN), string operations

---

### Perl

| Program | Description |
|---------|-------------|
| `log_analyzer.pl` | Apache access log parser: IP tracking, status code analysis, URL frequency, user agent detection, brute force attempt identification, and server health rating |
| `cipher_toolkit.pl` | Five classical ciphers (Caesar, ROT13, Atbash, Vigenere, Rail Fence) with encryption, decryption, brute force attack, and frequency analysis |

**Features used:** Scalars, arrays, hashes, regular expressions (captures, character classes), subroutines, foreach/for/while loops, if/elsif/else, string manipulation (uc, lc, substr, chr, ord), sort, printf formatting, references

---

### PILOT

| Program | Description |
|---------|-------------|
| `science_quiz.pilot` | 15-question science quiz across physics, chemistry, biology, earth science, and astronomy with pattern matching and educational explanations |
| `math_tutor.pilot` | 15 mental arithmetic problems (addition, subtraction, multiplication, division, mixed) with automatic answer checking and score tracking |

**Features used:** T: text output, A: input, C: computation, M: pattern matching, MT: conditional text, Y:/N: conditions, L: labels, J: jumps, J(condition): conditional jumps, U:/E: subroutines, R: runtime commands, {VAR} interpolation

---

### Prolog

| Program | Description |
|---------|-------------|
| `expert_system.pro` | Animal classification with 20 animals, physical characteristics, habitat/diet facts, and inference rules for species identification, danger assessment, and ecological queries |
| `geography_db.pro` | World geography knowledge base with 21 countries, capitals, populations, languages, currencies, and inference rules for regional analysis and cross-country comparisons |

**Features used:** Facts, rules with :- operator, ?- queries, unification, backtracking, variables (uppercase), comma-separated goals, write/1, member/2, arithmetic comparisons, LISTING

---

### Python

| Program | Description |
|---------|-------------|
| `crypto_toolkit.py` | Four cipher implementations (Caesar, Vigenere, Substitution, Playfair) as classes, SHA/MD5 hashing, avalanche effect demonstration, chi-squared cryptanalysis, password strength analyzer |
| `data_pipeline.py` | DataTable class with filter/sort/group_by operations, Stats class for statistical analysis, 24-row retail sales dataset, regional/product analysis, correlation matrix, trend forecasting |

**Features used:** Classes (OOP), inheritance, list/dict comprehensions, f-strings, lambda functions, math/hashlib modules, exception handling, string methods, enumerate, zip, sorted with key functions, formatted output

---

## How to Use

1. **Launch Time Warp Classic:**
   ```bash
   python3 run.py
   ```

2. **Select a language** from the dropdown menu

3. **Open a program:** File → Open → navigate to `examples/[language]/`

4. **Run:** Click the Run button

5. **View results** in the output panel (and turtle canvas for Logo)

> **Note:** PILOT programs with `A:` commands will prompt for input via dialog boxes. The science quiz accepts text answers; the math tutor accepts numeric answers.

---

## Learning Path

| Level | Recommended Programs |
|-------|---------------------|
| **Beginner** | BASIC `finance_calculator`, Logo `mandala_art`, PILOT `science_quiz` |
| **Intermediate** | Pascal `gradebook`, Python `data_pipeline`, Perl `cipher_toolkit` |
| **Advanced** | Prolog `expert_system`, Forth `number_theory`, JavaScript `statistics_engine` |

---

© 2025–2026 Honey Badger Universe | Example Programs
