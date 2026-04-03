#!/usr/bin/perl
# ═══════════════════════════════════════════════════════
# CRYPTOGRAPHIC TEXT TOOLKIT
# Classical cipher implementation with encryption,
# decryption, and frequency analysis capabilities
# Demonstrates Perl's text processing power
# ═══════════════════════════════════════════════════════

use strict;
use warnings;

# ═══════════════════════════════════════
# CIPHER IMPLEMENTATIONS
# ═══════════════════════════════════════

sub caesar_encrypt {
    my ($text, $shift) = @_;
    $shift = $shift % 26;
    my $result = '';
    for my $ch (split //, $text) {
        if ($ch =~ /[A-Z]/) {
            $result .= chr((ord($ch) - ord('A') + $shift) % 26 + ord('A'));
        } elsif ($ch =~ /[a-z]/) {
            $result .= chr((ord($ch) - ord('a') + $shift) % 26 + ord('a'));
        } else {
            $result .= $ch;
        }
    }
    return $result;
}

sub caesar_decrypt {
    my ($text, $shift) = @_;
    return caesar_encrypt($text, 26 - ($shift % 26));
}

sub vigenere_encrypt {
    my ($text, $key) = @_;
    $key = uc($key);
    my $result = '';
    my $ki = 0;
    for my $ch (split //, $text) {
        if ($ch =~ /[A-Za-z]/) {
            my $shift = ord(substr($key, $ki % length($key), 1)) - ord('A');
            if ($ch =~ /[A-Z]/) {
                $result .= chr((ord($ch) - ord('A') + $shift) % 26 + ord('A'));
            } else {
                $result .= chr((ord($ch) - ord('a') + $shift) % 26 + ord('a'));
            }
            $ki++;
        } else {
            $result .= $ch;
        }
    }
    return $result;
}

sub vigenere_decrypt {
    my ($text, $key) = @_;
    $key = uc($key);
    my $result = '';
    my $ki = 0;
    for my $ch (split //, $text) {
        if ($ch =~ /[A-Za-z]/) {
            my $shift = ord(substr($key, $ki % length($key), 1)) - ord('A');
            if ($ch =~ /[A-Z]/) {
                $result .= chr((ord($ch) - ord('A') - $shift + 26) % 26 + ord('A'));
            } else {
                $result .= chr((ord($ch) - ord('a') - $shift + 26) % 26 + ord('a'));
            }
            $ki++;
        } else {
            $result .= $ch;
        }
    }
    return $result;
}

sub rot13 {
    my ($text) = @_;
    return caesar_encrypt($text, 13);
}

sub atbash {
    my ($text) = @_;
    my $result = '';
    for my $ch (split //, $text) {
        if ($ch =~ /[A-Z]/) {
            $result .= chr(ord('Z') - (ord($ch) - ord('A')));
        } elsif ($ch =~ /[a-z]/) {
            $result .= chr(ord('z') - (ord($ch) - ord('a')));
        } else {
            $result .= $ch;
        }
    }
    return $result;
}

sub rail_fence_encrypt {
    my ($text, $rails) = @_;
    my @fence;
    for my $r (0..$rails-1) {
        $fence[$r] = [];
    }
    my $rail = 0;
    my $dir = 1;
    for my $ch (split //, $text) {
        push @{$fence[$rail]}, $ch;
        $rail += $dir;
        if ($rail >= $rails) { $dir = -1; $rail = $rails - 2; }
        if ($rail < 0) { $dir = 1; $rail = 1; }
    }
    my $result = '';
    for my $r (0..$rails-1) {
        $result .= join('', @{$fence[$r]});
    }
    return $result;
}

# ═══════════════════════════════════════
# FREQUENCY ANALYSIS
# ═══════════════════════════════════════

sub frequency_analysis {
    my ($text) = @_;
    my %freq;
    my $total = 0;
    for my $ch (split //, uc($text)) {
        if ($ch =~ /[A-Z]/) {
            $freq{$ch}++;
            $total++;
        }
    }
    return (\%freq, $total);
}

sub print_frequency {
    my ($text, $label) = @_;
    my ($freq_ref, $total) = frequency_analysis($text);
    my %freq = %$freq_ref;

    print "  Frequency Analysis: $label\n";
    print "  " . "-" x 50 . "\n";

    # English letter frequency for comparison
    my %english_freq = (
        E => 12.7, T => 9.1, A => 8.2, O => 7.5, I => 7.0,
        N => 6.7, S => 6.3, H => 6.1, R => 6.0, D => 4.3,
        L => 4.0, C => 2.8, U => 2.8, M => 2.4, W => 2.4,
        F => 2.2, G => 2.0, Y => 2.0, P => 1.9, B => 1.5,
        V => 1.0, K => 0.8, J => 0.2, X => 0.2, Q => 0.1,
        Z => 0.1,
    );

    for my $ch (sort { ($freq{$b} || 0) <=> ($freq{$a} || 0) } 'A'..'Z') {
        next unless exists $freq{$ch};
        my $count = $freq{$ch};
        my $pct = ($count / $total) * 100;
        my $eng = $english_freq{$ch} || 0;
        my $bar = "#" x int($pct);
        printf "    %s: %5.1f%% (eng: %4.1f%%) %s\n", $ch, $pct, $eng, $bar;
    }
    print "\n";
}

# ═══════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════

my $plaintext = "The quick brown fox jumps over the lazy dog near the quiet stream";

print "=" x 62, "\n";
print "          CRYPTOGRAPHIC TEXT TOOLKIT v1.0\n";
print "=" x 62, "\n\n";

print "-" x 62, "\n";
print "  ORIGINAL TEXT\n";
print "-" x 62, "\n";
print "  $plaintext\n\n";

# ─── Caesar Cipher ───
print "-" x 62, "\n";
print "  CAESAR CIPHER (Shift Cipher)\n";
print "-" x 62, "\n";
for my $shift (3, 7, 13, 19) {
    my $encrypted = caesar_encrypt($plaintext, $shift);
    my $decrypted = caesar_decrypt($encrypted, $shift);
    printf "  Shift %2d encrypt: %s\n", $shift, $encrypted;
    printf "  Shift %2d decrypt: %s\n", $shift, $decrypted;
    my $ok = $decrypted eq $plaintext ? "PASS" : "FAIL";
    print "  Verify: $ok\n\n";
}

# ─── ROT13 ───
print "-" x 62, "\n";
print "  ROT13 (Self-Inverting Cipher)\n";
print "-" x 62, "\n";
my $rot13_enc = rot13($plaintext);
my $rot13_dec = rot13($rot13_enc);
print "  Encrypted: $rot13_enc\n";
print "  Decrypted: $rot13_dec\n";
my $rot13_ok = $rot13_dec eq $plaintext ? "PASS" : "FAIL";
print "  Self-inverse verify: $rot13_ok\n\n";

# ─── Atbash Cipher ───
print "-" x 62, "\n";
print "  ATBASH CIPHER (Mirror Alphabet)\n";
print "-" x 62, "\n";
my $atbash_enc = atbash($plaintext);
my $atbash_dec = atbash($atbash_enc);
print "  Encrypted: $atbash_enc\n";
print "  Decrypted: $atbash_dec\n";
my $atbash_ok = $atbash_dec eq $plaintext ? "PASS" : "FAIL";
print "  Self-inverse verify: $atbash_ok\n\n";

# ─── Vigenere Cipher ───
print "-" x 62, "\n";
print "  VIGENERE CIPHER (Polyalphabetic)\n";
print "-" x 62, "\n";
for my $key ("SECRET", "CIPHER", "PERL") {
    my $encrypted = vigenere_encrypt($plaintext, $key);
    my $decrypted = vigenere_decrypt($encrypted, $key);
    printf "  Key: %-8s Encrypted: %s\n", $key, $encrypted;
    printf "  Key: %-8s Decrypted: %s\n", $key, $decrypted;
    my $ok = $decrypted eq $plaintext ? "PASS" : "FAIL";
    print "  Verify: $ok\n\n";
}

# ─── Rail Fence Cipher ───
print "-" x 62, "\n";
print "  RAIL FENCE CIPHER (Transposition)\n";
print "-" x 62, "\n";
for my $rails (2, 3, 4) {
    my $encrypted = rail_fence_encrypt($plaintext, $rails);
    printf "  %d rails: %s\n", $rails, $encrypted;
}
print "\n";

# ─── Brute Force Caesar ───
print "-" x 62, "\n";
print "  BRUTE FORCE CAESAR ATTACK\n";
print "-" x 62, "\n";
my $mystery = caesar_encrypt("Attack at dawn", 17);
print "  Ciphertext: $mystery\n";
print "  Trying all 26 shifts:\n";
for my $try_shift (0..25) {
    my $attempt = caesar_decrypt($mystery, $try_shift);
    my $marker = ($attempt =~ /[Aa]ttack/) ? " <-- FOUND!" : "";
    printf "    Shift %2d: %s%s\n", $try_shift, $attempt, $marker;
}
print "\n";

# ─── Frequency Analysis ───
print "-" x 62, "\n";
print "  FREQUENCY ANALYSIS\n";
print "-" x 62, "\n\n";

my $long_text = "To be or not to be that is the question whether tis nobler " .
    "in the mind to suffer the slings and arrows of outrageous fortune " .
    "or to take arms against a sea of troubles and by opposing end them";

print_frequency($long_text, "English plaintext (Shakespeare)");

my $caesar_long = caesar_encrypt($long_text, 7);
print_frequency($caesar_long, "Caesar-encrypted (shift 7)");

print "  Note: In the encrypted text, the most frequent letter\n";
print "  should be shifted 7 positions from E (i.e., L).\n\n";

print "=" x 62, "\n";
print "  Cryptographic Toolkit Complete\n";
print "  Ciphers: Caesar, ROT13, Atbash, Vigenere, Rail Fence\n";
print "  Analysis: Frequency counting, brute force attack\n";
print "=" x 62, "\n";
