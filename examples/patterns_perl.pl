#!/usr/bin/env perl
# ====================================
#    Perl Demo - Text Processing
# ====================================

use strict;
use warnings;

print "Welcome to Time Warp Perl!\n";
print "Perl is excellent for text processing and pattern matching.\n\n";

# Array demonstration
print "=== Array Operations ===\n";
my @languages = ('BASIC', 'Logo', 'Pascal', 'Prolog', 'Forth', 'Perl');
print "Supported languages: " . join(', ', @languages) . "\n";
print "Total: " . scalar(@languages) . " languages\n\n";

# Hash demonstration
print "=== Hash (Dictionary) Operations ===\n";
my %years = (
    'BASIC'  => 1964,
    'Logo'   => 1967,
    'Pascal' => 1970,
    'Prolog' => 1972,
    'Forth'  => 1970,
    'Perl'   => 1987
);

foreach my $lang (sort keys %years) {
    print "$lang was created in $years{$lang}\n";
}
print "\n";

# Pattern matching
print "=== Regular Expression Demo ===\n";
my $text = "The Quick Brown Fox Jumps Over The Lazy Dog";
print "Original: $text\n";

# Count words
my @words = split(/\s+/, $text);
print "Word count: " . scalar(@words) . "\n";

# Find words with 'o'
my @words_with_o = grep { /o/i } @words;
print "Words with 'o': " . join(', ', @words_with_o) . "\n";

# Transform text
$text =~ s/\b(\w)/\U$1/g;  # Uppercase first letter of each word
print "Capitalized: $text\n\n";

# Subroutine demonstration
sub fibonacci {
    my ($n) = @_;
    return $n if $n < 2;
    return fibonacci($n-1) + fibonacci($n-2);
}

print "=== Fibonacci Sequence ===\n";
for my $i (0..10) {
    print "F($i) = " . fibonacci($i) . "\n";
}

print "\nPerl demo complete!\n";
