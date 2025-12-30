#!/usr/bin/perl
# =========================================================
# COMPREHENSIVE PERL DEMO - Time Warp Classic IDE
# Demonstrates all major Perl language features
# =========================================================

use strict;
use warnings;

print "==================================================\n";
print "COMPREHENSIVE PERL DEMO\n";
print "==================================================\n\n";

# --- VARIABLES AND DATA TYPES ---
print "=== VARIABLES AND DATA TYPES ===\n";
my $integer = 42;
my $float = 3.14159;
my $string = "Time Warp";
my $bool = 1;

print "Integer: $integer\n";
print "Float: $float\n";
print "String: $string\n";
print "Boolean: $bool\n";
print "\n";

# --- ARITHMETIC OPERATIONS ---
print "=== ARITHMETIC OPERATIONS ===\n";
my $a = 10;
my $b = 3;
print "Addition: ", $a + $b, "\n";
print "Subtraction: ", $a - $b, "\n";
print "Multiplication: ", $a * $b, "\n";
print "Division: ", $a / $b, "\n";
print "Modulo: ", $a % $b, "\n";
print "Exponentiation: ", $a ** 2, "\n";
print "\n";

# --- STRING OPERATIONS ---
print "=== STRING OPERATIONS ===\n";
my $msg = "Perl Programming";
print "Original: $msg\n";
print "Length: ", length($msg), "\n";
print "Uppercase: ", uc($msg), "\n";
print "Lowercase: ", lc($msg), "\n";
print "Substring: ", substr($msg, 0, 4), "\n";
print "Index of 'Pro': ", index($msg, "Pro"), "\n";
print "Replace: ", $msg =~ s/Perl/Perl/r, "\n";
print "Split: ", join(", ", split(/ /, $msg)), "\n";
print "Reverse: ", reverse($msg), "\n";
print "Repeat: ", "x" x 5, "\n";
print "\n";

# --- ARRAYS ---
print "=== ARRAYS ===\n";
my @numbers = (10, 20, 30, 40, 50);
print "Array: ", join(", ", @numbers), "\n";
print "Length: ", scalar(@numbers), "\n";
print "First element: $numbers[0]\n";
print "Last element: $numbers[$#numbers]\n";

push(@numbers, 60);
print "After push(60): ", join(", ", @numbers), "\n";

my $popped = pop(@numbers);
print "Popped: $popped\n";

unshift(@numbers, 5);
print "After unshift(5): ", join(", ", @numbers), "\n";

shift(@numbers);
print "After shift(): ", join(", ", @numbers), "\n";

# Calculate sum
my $sum = 0;
foreach my $num (@numbers) {
    $sum += $num;
}
print "Sum: $sum\n";

# Sort
my @sorted = sort { $a <=> $b } @numbers;
print "Sorted: ", join(", ", @sorted), "\n";
print "\n";

# --- HASHES ---
print "=== HASHES ===\n";
my %person = (
    name => "Alice",
    age => 30,
    city => "New York",
    occupation => "Developer"
);
print "Name: $person{name}\n";
print "Age: $person{age}\n";
print "City: $person{city}\n";
print "Keys: ", join(", ", keys %person), "\n";
print "Values: ", join(", ", values %person), "\n";
print "\n";

# --- CONDITIONAL STATEMENTS ---
print "=== IF/ELSIF/ELSE STATEMENTS ===\n";
my $age = 25;
if ($age >= 18) {
    print "You are an adult\n";
} else {
    print "You are a minor\n";
}

my $score = 85;
if ($score >= 90) {
    print "Grade: A\n";
} elsif ($score >= 80) {
    print "Grade: B\n";
} elsif ($score >= 70) {
    print "Grade: C\n";
} else {
    print "Grade: F\n";
}
print "\n";

# --- UNLESS ---
print "=== UNLESS STATEMENT ===\n";
my $is_adult = 1;
unless ($is_adult == 0) {
    print "Person is an adult\n";
}
print "\n";

# --- FOR LOOPS ---
print "=== FOR LOOPS ===\n";
print "Counting 1 to 5:\n";
for (my $i = 1; $i <= 5; $i++) {
    print "  $i squared = ", $i * $i, "\n";
}
print "\n";

# --- FOREACH LOOPS ---
print "=== FOREACH LOOPS ===\n";
my @colors = qw(red green blue yellow);
foreach my $color (@colors) {
    print "  Color: $color\n";
}
print "\n";

# --- WHILE LOOPS ---
print "=== WHILE LOOPS ===\n";
my $counter = 1;
while ($counter <= 3) {
    print "  Counter: $counter\n";
    $counter++;
}
print "\n";

# --- DO-WHILE LOOPS ---
print "=== DO-WHILE LOOPS ===\n";
my $num = 1;
do {
    print "  Num: $num\n";
    $num++;
} while ($num <= 3);
print "\n";

# --- SUBROUTINES ---
print "=== SUBROUTINES ===\n";

sub greet {
    my ($name) = @_;
    return "Hello, $name!";
}

sub add {
    my ($a, $b) = @_;
    return $a + $b;
}

sub factorial {
    my ($n) = @_;
    return 1 if $n <= 1;
    return $n * factorial($n - 1);
}

print greet("Alice"), "\n";
print "5 + 3 = ", add(5, 3), "\n";
print "5! = ", factorial(5), "\n";
print "\n";

# --- REGULAR EXPRESSIONS ---
print "=== REGULAR EXPRESSIONS ===\n";
my $text = "The Time Warp Classic IDE";
if ($text =~ /Time/) {
    print "Text contains 'Time'\n";
}
my $replaced = $text;
$replaced =~ s/Time Warp/Perl/;
print "After replace: $replaced\n";

if ($text =~ /(\w+) (\w+) (\w+)/) {
    print "Captured words: $1, $2, $3\n";
}
print "\n";

# --- COMPARISON OPERATORS ---
print "=== COMPARISON OPERATORS ===\n";
if (5 > 3) { print "5 > 3: true\n"; }
if (5 == 5) { print "5 == 5: true\n"; }
if (5 < 10) { print "5 < 10: true\n"; }
if (5 >= 5) { print "5 >= 5: true\n"; }
if (5 <= 10) { print "5 <= 10: true\n"; }
if (5 != 3) { print "5 != 3: true\n"; }
print "\n";

# --- STRING COMPARISON ---
print "=== STRING COMPARISON ===\n";
if ("abc" eq "abc") { print "'abc' eq 'abc': true\n"; }
if ("abc" ne "def") { print "'abc' ne 'def': true\n"; }
if ("abc" lt "def") { print "'abc' lt 'def': true\n"; }
if ("def" gt "abc") { print "'def' gt 'abc': true\n"; }
print "\n";

# --- LOGICAL OPERATORS ---
print "=== LOGICAL OPERATORS ===\n";
if (5 > 3 && 10 > 5) { print "AND: true\n"; }
if (5 > 3 || 10 < 5) { print "OR: true\n"; }
if (!(5 < 3)) { print "NOT: true\n"; }
print "\n";

# --- TERNARY OPERATOR ---
print "=== TERNARY OPERATOR ===\n";
my $num_val = 7;
my $result = ($num_val % 2 == 0) ? "even" : "odd";
print "$num_val is $result\n";
print "\n";

# --- TYPE CONVERSION ---
print "=== TYPE CONVERSION ===\n";
my $str_num = "123";
my $num_val2 = 0 + $str_num;
print "String to number: '123' -> $num_val2\n";
my $num_to_str = "" . 456;
print "Number to string: 456 -> '$num_to_str'\n";
print "\n";

# --- MAP AND GREP ---
print "=== MAP AND GREP ===\n";
my @nums = (1, 2, 3, 4, 5);
my @squared = map { $_ * $_ } @nums;
print "Squared: ", join(", ", @squared), "\n";
my @evens = grep { $_ % 2 == 0 } @nums;
print "Evens: ", join(", ", @evens), "\n";
print "\n";

# --- REFERENCES ---
print "=== REFERENCES ===\n";
my $arr_ref = \@numbers;
print "Array reference first element: ", $arr_ref->[0], "\n";
my $hash_ref = \%person;
print "Hash reference name: ", $hash_ref->{name}, "\n";
print "\n";

# --- FINAL MESSAGE ---
print "==================================================\n";
print "PERL DEMO COMPLETE!\n";
print "All major Perl features demonstrated!\n";
print "==================================================\n";
