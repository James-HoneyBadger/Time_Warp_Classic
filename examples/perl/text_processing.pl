#!/usr/bin/perl
# Perl Text Processing Demo
# Demonstrates Perl's powerful text manipulation capabilities

use strict;
use warnings;

print "Perl Text Processing Demo\n";
print "=" x 30 . "\n\n";

# Sample text data
my $text = "The quick brown fox jumps over the lazy dog. Perl is a powerful programming language for text processing and system administration.";

print "Original text:\n$text\n\n";

# Word count
my @words = split /\s+/, $text;
my $word_count = scalar @words;
print "Word count: $word_count\n\n";

# Find words starting with vowels
my @vowel_words = grep { /^[aeiou]/i } @words;
print "Words starting with vowels: " . join(", ", @vowel_words) . "\n\n";

# Replace words
my $modified_text = $text;
$modified_text =~ s/quick/fast/g;
$modified_text =~ s/lazy/sleepy/g;
print "Modified text:\n$modified_text\n\n";

# Extract sentences
my @sentences = split /\.\s*/, $text;
print "Sentences found:\n";
for my $i (0 .. $#sentences) {
    print "  " . ($i + 1) . ". $sentences[$i].\n";
}
print "\n";

# Pattern matching demo
print "Pattern matching results:\n";
if ($text =~ /powerful/) {
    print "✓ Found 'powerful' in the text\n";
}
if ($text =~ /programming/) {
    print "✓ Found 'programming' in the text\n";
}
if ($text =~ /python/i) {
    print "✓ Found 'python' (case insensitive) in the text\n";
} else {
    print "✗ Did not find 'python' in the text\n";
}

print "\nText processing demo complete!\n";