# Perl Language Reference

Complete reference for Perl syntax in Time Warp Classic.

## Program Structure

```perl
#!/usr/bin/perl
use strict;
use warnings;

# Your code here
```

## Variables

### Scalars ($)

```perl
$x = 10;
$name = "Alice";
$pi = 3.14159;
$active = 1;        # Boolean
```

### Arrays (@)

```perl
@numbers = (1, 2, 3, 4, 5);
@colors = qw(red green blue);
@mixed = (1, "hello", 3.14);

# Access
$numbers[0]         # 1
$numbers[-1]        # 5 (last element)
```

### Hashes (%)

```perl
%person = (
    'name' => 'Alice',
    'age' => 30,
    'city' => 'New York'
);

# Access
$person{'name'}     # Alice
```

## Operators

### Arithmetic

```perl
+       Addition
-       Subtraction
*       Multiplication
/       Division
%       Modulo
**      Power
```

### String Operations

```perl
.       Concatenation    "Hello" . " World"
x       Repetition       "ab" x 3 = "ababab"
```

### Comparison (Numeric)

```perl
==      Equal
!=      Not equal
<       Less than
>       Greater than
<=      Less or equal
>=      Greater or equal
<=>     Spaceship (compare)
```

### Comparison (String)

```perl
eq      Equal
ne      Not equal
lt      Less than
gt      Greater than
le      Less or equal
ge      Greater or equal
cmp     Compare
```

### Logical

```perl
&&      AND
||      OR
!       NOT
and     AND (lower precedence)
or      OR (lower precedence)
not     NOT (lower precedence)
```

## Control Structures

### If/Elsif/Else

```perl
if ($x > 5) {
    print "Greater";
} elsif ($x == 5) {
    print "Equal";
} else {
    print "Less";
}
```

### Unless (Opposite of If)

```perl
unless ($x == 0) {
    print "Not zero";
}
```

### For Loop

```perl
for (my $i = 0; $i < 10; $i++) {
    print $i;
}

for my $i (1..10) {
    print $i;
}
```

### Foreach Loop

```perl
foreach my $num (@numbers) {
    print $num;
}

for my $color (@colors) {
    print $color;
}
```

### While Loop

```perl
while ($count < 10) {
    print $count;
    $count++;
}

until ($count == 10) {
    print $count;
    $count++;
}
```

### Last & Next (Break/Continue)

```perl
for my $i (1..10) {
    if ($i == 5) { last; }      # Break
    if ($i == 2) { next; }      # Continue
    print $i;
}
```

## Arrays

### Array Operations

```perl
@array = (1, 2, 3);
push(@array, 4);            # Add to end
$elem = pop(@array);        # Remove from end
unshift(@array, 0);         # Add to beginning
shift(@array);              # Remove from beginning

# Length
$len = scalar @array;
$last_index = $#array;

# Join
$str = join(", ", @array);

# Split
@words = split(/\s+/, $text);
```

### Array Slices

```perl
@numbers = (1, 2, 3, 4, 5);
@slice = @numbers[1, 3];    # (2, 4)
```

### Array Range

```perl
@range = (1..10);           # (1, 2, 3, ..., 10)
@letters = ('a'..'z');
```

## Hashes

### Hash Operations

```perl
%hash = ('key1' => 'value1', 'key2' => 'value2');

# Access
$hash{'key1'}

# Add/modify
$hash{'key3'} = 'value3';

# Delete
delete $hash{'key1'};

# Keys and values
@keys = keys %hash;
@values = values %hash;

# Check existence
if (exists $hash{'key'}) { ... }
```

### Hash Iteration

```perl
while (my ($key, $value) = each %hash) {
    print "$key => $value\n";
}

foreach my $key (keys %hash) {
    print "$key => $hash{$key}\n";
}
```

## Strings

### String Basics

```perl
$str = "Hello";
$len = length($str);
$upper = uc($str);          # Uppercase
$lower = lc($str);          # Lowercase
$cap = ucfirst($str);       # Capitalize
```

### String Methods

```perl
substr($str, 0, 2)          # First 2 chars
index($str, "ell")          # Find position
rindex($str, "l")           # Find from right
uc($str)                    # Uppercase
lc($str)                    # Lowercase
reverse($str)               # Reverse
```

### String Interpolation

```perl
$name = "Alice";
print "Hello, $name!";      # "Hello, Alice!"
print 'Hello, $name!';      # 'Hello, $name!' (literal)
print qq(Hello, $name!);    # "Hello, Alice!"
```

### Regular Expressions

```perl
$text = "Hello World";

# Match
if ($text =~ /World/) { print "Found"; }
if ($text !~ /xyz/) { print "Not found"; }

# Substitution
$text =~ s/World/Perl/;     # "Hello Perl"
$text =~ s/o/0/g;          # Replace all

# Split
@words = split(/\s+/, $text);

# Patterns
/^start/                    # Start of string
/end$/                      # End of string
/[aeiou]/                   # Character class
/[^aeiou]/                  # Negated class
/a+/                        # One or more
/a*/                        # Zero or more
/a?/                        # Zero or one
```

## Functions/Subroutines

### Subroutine Definition

```perl
sub greet {
    my ($name) = @_;
    print "Hello, $name!";
}

greet("Alice");

sub add {
    my ($a, $b) = @_;
    return $a + $b;
}

$sum = add(5, 3);
```

### Return Values

```perl
sub get_multiple {
    return (1, 2, 3);
}

my ($a, $b, $c) = get_multiple();
```

### Lexical Variables (my)

```perl
sub function {
    my $local_var = 10;     # Local to function
    our $global_var;        # Package variable
}
```

## References

### Creating References

```perl
$scalar_ref = \$scalar;
$array_ref = \@array;
$hash_ref = \%hash;
$code_ref = \&subroutine;

$array_ref = [1, 2, 3];    # Anonymous array
$hash_ref = {a => 1, b => 2};  # Anonymous hash
```

### Dereferencing

```perl
$$scalar_ref                # Dereference scalar
@$array_ref                 # Dereference array
$array_ref->[0]             # Array element
%$hash_ref                  # Dereference hash
$hash_ref->{key}            # Hash element
&$code_ref                  # Call function
```

## Map and Grep

### Map (Transform)

```perl
@numbers = (1, 2, 3, 4, 5);
@squared = map { $_ * $_ } @numbers;  # (1, 4, 9, 16, 25)

@words = qw(hello world);
@lengths = map { length($_) } @words;  # (5, 5)
```

### Grep (Filter)

```perl
@numbers = (1, 2, 3, 4, 5);
@even = grep { $_ % 2 == 0 } @numbers;  # (2, 4)

@words = qw(apple banana apricot);
@awords = grep { /^a/ } @words;  # (apple, apricot)
```

## File I/O

### Reading Files

```perl
open(my $fh, '<', 'file.txt') or die "Cannot open file";
while (my $line = <$fh>) {
    print $line;
}
close($fh);
```

### Writing Files

```perl
open(my $fh, '>', 'output.txt') or die "Cannot open";
print $fh "Hello, World!\n";
close($fh);
```

### Appending

```perl
open(my $fh, '>>', 'file.txt') or die "Cannot open";
print $fh "New line\n";
close($fh);
```

## Useful Built-in Functions

```perl
abs($x)                 # Absolute value
int($x)                 # Integer part
sqrt($x)                # Square root
sin($x), cos($x)        # Trigonometry
exp($x), log($x)        # Exponential, logarithm
rand()                  # Random 0..1
int(rand(100))          # Random 0..99
sort(@array)            # Sort array
reverse(@array)         # Reverse
scalar @array           # Array length
chomp($str)             # Remove newline
chop($str)              # Remove last character
```

## Complete Examples

### Count Word Frequency

```perl
use strict;
use warnings;

my $text = "hello world hello perl hello";
my %freq;

for my $word (split /\s+/, $text) {
    $freq{$word}++;
}

for my $word (sort keys %freq) {
    print "$word: $freq{$word}\n";
}
```

### Process Text

```perl
my @lines = (
    "apple 100",
    "banana 50",
    "cherry 75"
);

my $total = 0;
for my $line (@lines) {
    my ($fruit, $price) = split /\s+/, $line;
    $total += $price;
    print "$fruit costs $price\n";
}
print "Total: $total\n";
```

## Tips & Best Practices

1. **Use strict & warnings** always
2. **Use lexical variables** (my)
3. **Test regex separately** before using
4. **Use meaningful variable names**
5. **Avoid globals** when possible
6. **Use references** for complex data
7. **Check return values** (especially file I/O)

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/perl/](../../examples/perl/)

---

**Last Updated:** 2024
