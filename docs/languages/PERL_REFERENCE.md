# Perl in Time Warp Classic

Time Warp does not reimplement Perl. It saves your program to a temporary
`.pl` file and runs it with the system `perl` in a separate process. Text
munging, regular expressions, hashes, CPAN modules you have installed: it
is all real Perl 5.

This page covers what is different inside Time Warp: how `perl` is found,
how output and input travel, time limits, and error reporting. For the
language itself, see [perldoc](#further-reading).

## At a glance

| Topic | Behaviour |
|-------|-----------|
| Runtime | `perl` on `PATH`, then `perl5`; must be installed separately |
| Output | stdout and stderr merged, shown line by line as the program prints |
| Input | The console bar feeds `STDIN`, one line per Enter |
| Time limit | 30 s in the desktop IDE and `timewarp --run`; 10 s by default in the web IDE |
| Stop | Ctrl+. (desktop) or the Stop button (web); the console shows `BREAK` |
| Errors | `?ERROR IN n: ...` naming the editor line, sometimes followed by a `?HINT:` line |
| Turtle graphics | Not available |
| Console REPL | Each line runs in a fresh process; nothing carries over |

## Which Perl runs

Time Warp looks for `perl`, then `perl5`, on `PATH` and uses the first one
whose `perl --version` succeeds. Most Linux and macOS systems already have
one; on Windows install [Strawberry Perl](https://strawberryperl.com/). To
check the version, run `print "$^V\n";` from the console bar.

### When Perl is missing

The language menu shows Perl as "(runtime missing)" (in the web IDE the
status bar also says "Perl needs its runtime installed on the server").
Running anyway prints:

```text
?PERL NOT FOUND - install it to run these scripts (install Perl (apt install perl, brew install perl, or strawberryperl.com))
```

Install Perl and restart Time Warp.

## How a run works

1. Time Warp puts `$| = 1; ` at the very start of line 1 (autoflush, so
   output is not held back) and writes the program to a temporary file
   such as `/tmp/tmp0u0tho6x.pl`. Nothing is inserted as a new line, so
   line numbers in messages match the editor.
2. Time Warp starts `perl <file>`. On Linux and macOS the command is
   wrapped in `stdbuf -oL -eL` when `stdbuf` exists.
3. The working directory is the directory Time Warp was started from, not
   the folder your file is saved in. Relative paths in `open` resolve from
   there.
4. `.` is not in `@INC`, and the temporary file lives elsewhere anyway, so
   `use MyModule;` does not find a `MyModule.pm` next to your saved file.
   Set `PERL5LIB` before starting Time Warp, or use
   `use lib '/full/path';`.
5. When the program ends, the temporary file is deleted.

Because the prefix shares line 1, a `#!` line there turns into a plain
comment (harmless; you do not need one), and `use v5.36;` on line 1
still works.

## Output

- `print`, `printf`, `say` (with `use feature 'say';`) and `warn` all go
  to the console, in order.
- A line is shown when its newline arrives. `print "Working..."` without
  `\n` stays invisible until a later newline or the end of the program.
- Warnings appear in the console but do not fail the run. With
  `use warnings;`, an undefined value in a string shows up as
  `Use of uninitialized value $u in concatenation (.) or string at /tmp/....pl line 2.`
- The web IDE stops a run after 20,000 lines of output
  (`Stopped: output limit of 20000 lines reached`).

## Input

While a program is running, the console bar sends what you type to
`STDIN`, one line per Enter, echoed in the console.

```perl
print "Name?\n";
chomp(my $name = <STDIN>);
print "Age?\n";
chomp(my $age = <STDIN>);
printf "Hello, %s. Next year you will be %d.\n", $name, $age + 1;
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

- **End prompts with `\n`.** A prompt without one does not appear until
  the next newline.
- **Typing ahead works.** Lines typed early wait in the pipe.
- **There is no end-of-file.** `STDIN` stays open, so
  `while (my $line = <STDIN>)` and `my @all = <STDIN>` wait until the time
  limit. Stop at a known count or a sentinel such as an empty line:
  `last if $line eq '';` after `chomp`.
- **Waiting counts toward the time limit.** The built-in languages pause
  the clock at `INPUT`; Perl programs do not. In the web IDE the default
  limit is 10 seconds; raise it with `timewarp --web --timeout N`.
- **The web IDE cannot tell that the program is waiting.** Type anyway.

## Time limits and stopping

| Where | Limit | What you see |
|-------|-------|--------------|
| Desktop IDE, `timewarp --run` | 30 s | `?ERROR: Perl script timed out after 30s` and a `?HINT:` |
| Web IDE | 10 s (set with `--timeout`) | `Stopped: time limit of 10s reached`, then `BREAK` |

The 30-second limit belongs to the Perl runner itself, so it also caps web
runs whose `--timeout` is higher.

To stop a program early, press Ctrl+. in the desktop IDE or the Stop
button in the browser. The process is killed and the console prints
`BREAK`.

## Errors and hints

When Perl exits with an error, Time Warp shows Perl's message, then a
summary line naming the editor line and, when it recognises the error, a
hint:

```perl
my $n = 0;
print 10 / $n, "\n";
```

```text
Illegal division by zero at /tmp/tmp0u0tho6x.pl line 2.
?ERROR IN 2: Illegal division by zero
?HINT: a value in the expression is 0 - check the divisor before dividing. See docs/languages/PERL_REFERENCE.md.
```

- The line number comes from Perl's `at ... line N`. In the desktop IDE,
  click the `?ERROR IN` line to jump to it.
- Hints are matched against the summary line. Runtime errors such as
  division by zero, and time-outs, get one.
- **Compile errors** (strict violations, syntax errors, missing modules)
  are summarised unhelpfully, as
  `?ERROR IN n: Execution of /tmp/....pl aborted due to compilation errors.`
  or `?ERROR IN 1: BEGIN failed--compilation aborted`, and get no hint.
  The real message is in the lines above, for example
  `Global symbol "$y" requires explicit package name ... line 4.` or
  `Can't locate Foo/Bar.pm in @INC ...`.
- `die "Out of coffee\n";` prints the message and is summarised as
  `?ERROR: Perl script exited with code 255`. A `die` message without a
  trailing `\n` includes `at ... line N`, so the summary names the line.
- `exit 3;` is reported as `?ERROR: Perl script exited with code 3`.

Start programs with `use strict;` and `use warnings;`. Most Perl
surprises turn into a message with a line number.

## The console REPL

When no program is running, a line typed in the console bar is run as a
complete, one-line program in a brand-new `perl` process:

```text
>print join(",", map { $_ * $_ } 1..5), "\n";
1,4,9,16,25
```

Nothing persists between lines. Each line has a 2-second limit, after
which it is stopped without a message. For anything longer, use the
editor and Run.

## Turtle graphics

Not available. The Time Warp canvas is driven only by the built-in
languages. Use Logo for turtle work.

## Cheat sheet

| Task | Perl |
|------|------|
| Pragmas | `use strict; use warnings;` |
| Print | `print "x = $x\n";`, `printf "%.2f\n", $x;` |
| Read a line | `chomp(my $s = <STDIN>);` |
| Scalars | `my $n = 10; my $name = "Ada";` |
| Arrays | `my @xs = (1, 2, 3); push @xs, 4; $xs[0]; $xs[-1]; scalar @xs` |
| Hashes | `my %age = (ada => 41); $age{bob} = 30; exists $age{ada}; keys %age` |
| Arithmetic | `+ - * / %`, `**` power, `int($a / $b)` integer division |
| Compare numbers | `== != < <= > >=` |
| Compare strings | `eq ne lt le gt ge`; join with `.`, repeat with `x` |
| If | `if ($x > 0) { ... } elsif ($x == 0) { ... } else { ... }` |
| Counted loop | `for my $i (1 .. 10) { ... }` |
| Loop over array | `for my $x (@xs) { ... }`; hash: `for my $k (sort keys %h) { ... }` |
| Loop control | `next`, `last` |
| Subroutine | `sub area { my ($w, $h) = @_; return $w * $h; }` |
| Match | `if ($s =~ /(\d+)/) { print "found $1\n"; }` |
| Substitute | `(my $t = $s) =~ s/old/new/g;` |
| Split / join | `my @w = split /\s+/, $s; join(", ", @w)` |
| List tools | `grep { $_ > 2 } @xs`, `map { $_ * 2 } @xs`, `sort { $a <=> $b } @xs` |
| Errors | `eval { ...; 1 } or print "failed: $@";` |
| Comment | `# like this` |

A complete program:

```perl
use strict;
use warnings;

my $text = "the quick brown fox jumps over the lazy dog the end";
my %count;
$count{$_}++ for split /\s+/, $text;

for my $word (sort { $count{$b} <=> $count{$a} || $a cmp $b } keys %count) {
    printf "%-6s %d\n", $word, $count{$word};
    last if $word eq 'dog';
}
```

```text
the    3
brown  1
dog    1
```

## Known limitations (1.6.0)

- `timewarp --run file.pl --language perl` does not pass the terminal's
  stdin to the program.
- Compile errors get a poor `?ERROR` summary line (see above).
- A REPL line that runs past 2 seconds is stopped silently.

## Further reading

- [perldoc.perl.org](https://perldoc.perl.org/) - the official
  documentation; also `perldoc` on the command line
- [perlintro](https://perldoc.perl.org/perlintro) - a quick tour of the
  language
- [perlretut](https://perldoc.perl.org/perlretut) - regular expressions
- Examples: [examples/perl/](../../examples/perl/)
- [Language tutorials](../user/LANGUAGE_TUTORIALS.md#perl)
