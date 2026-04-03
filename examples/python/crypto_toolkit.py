#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════
CRYPTOGRAPHY TOOLKIT
Classical and modern cipher implementations with
encryption, decryption, hashing, and analysis tools
═══════════════════════════════════════════════════════
"""

import string
import hashlib
import math
from collections import Counter

# ═══════════════════════════════════════
# CIPHER IMPLEMENTATIONS
# ═══════════════════════════════════════

class CaesarCipher:
    """Shift cipher - each letter shifted by fixed amount"""

    @staticmethod
    def encrypt(text, shift):
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text, shift):
        return CaesarCipher.encrypt(text, 26 - (shift % 26))

    @staticmethod
    def brute_force(ciphertext):
        """Try all 26 shifts and return results"""
        results = []
        for shift in range(26):
            results.append((shift, CaesarCipher.decrypt(ciphertext, shift)))
        return results


class VigenereCipher:
    """Polyalphabetic cipher using keyword"""

    @staticmethod
    def encrypt(text, key):
        key = key.upper()
        result = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                shift = ord(key[ki % len(key)]) - ord('A')
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base + shift) % 26 + base))
                ki += 1
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text, key):
        key = key.upper()
        result = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                shift = ord(key[ki % len(key)]) - ord('A')
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base - shift) % 26 + base))
                ki += 1
            else:
                result.append(ch)
        return ''.join(result)


class SubstitutionCipher:
    """Monoalphabetic substitution cipher"""

    @staticmethod
    def generate_key(seed_word):
        """Generate alphabet key from seed word"""
        seen = set()
        key = []
        for ch in seed_word.upper():
            if ch.isalpha() and ch not in seen:
                key.append(ch)
                seen.add(ch)
        for ch in string.ascii_uppercase:
            if ch not in seen:
                key.append(ch)
                seen.add(ch)
        return ''.join(key)

    @staticmethod
    def encrypt(text, key):
        table = str.maketrans(string.ascii_uppercase + string.ascii_lowercase,
                              key + key.lower())
        return text.translate(table)

    @staticmethod
    def decrypt(text, key):
        table = str.maketrans(key + key.lower(),
                              string.ascii_uppercase + string.ascii_lowercase)
        return text.translate(table)


class PlayfairCipher:
    """Digraph substitution cipher"""

    @staticmethod
    def generate_grid(key):
        seen = set()
        grid = []
        for ch in (key.upper() + string.ascii_uppercase):
            ch = 'I' if ch == 'J' else ch
            if ch.isalpha() and ch not in seen:
                grid.append(ch)
                seen.add(ch)
        return [grid[i:i+5] for i in range(0, 25, 5)]

    @staticmethod
    def find_pos(grid, ch):
        ch = 'I' if ch == 'J' else ch
        for r in range(5):
            for c in range(5):
                if grid[r][c] == ch:
                    return r, c
        return 0, 0

    @staticmethod
    def encrypt(text, key):
        grid = PlayfairCipher.generate_grid(key)
        text = text.upper().replace('J', 'I')
        text = ''.join(ch for ch in text if ch.isalpha())

        # Create digraphs
        digraphs = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else 'X'
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
            digraphs.append((a, b))

        result = []
        for a, b in digraphs:
            r1, c1 = PlayfairCipher.find_pos(grid, a)
            r2, c2 = PlayfairCipher.find_pos(grid, b)
            if r1 == r2:
                result.append(grid[r1][(c1 + 1) % 5] + grid[r2][(c2 + 1) % 5])
            elif c1 == c2:
                result.append(grid[(r1 + 1) % 5][c1] + grid[(r2 + 1) % 5][c2])
            else:
                result.append(grid[r1][c2] + grid[r2][c1])

        return ' '.join(result)


# ═══════════════════════════════════════
# ANALYSIS TOOLS
# ═══════════════════════════════════════

def frequency_analysis(text):
    """Analyze letter frequency"""
    letters = [ch.upper() for ch in text if ch.isalpha()]
    total = len(letters)
    if total == 0:
        return {}
    freq = Counter(letters)
    return {ch: (count / total) * 100 for ch, count in freq.most_common()}

def index_of_coincidence(text):
    """Calculate Index of Coincidence"""
    letters = [ch.upper() for ch in text if ch.isalpha()]
    n = len(letters)
    if n <= 1:
        return 0
    freq = Counter(letters)
    numerator = sum(f * (f - 1) for f in freq.values())
    return numerator / (n * (n - 1))

def chi_squared_score(text, shift):
    """Score a Caesar shift by chi-squared against English"""
    english_freq = {
        'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7,
        'F': 2.2, 'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.2,
        'K': 0.8, 'L': 4.0, 'M': 2.4, 'N': 6.7, 'O': 7.5,
        'P': 1.9, 'Q': 0.1, 'R': 6.0, 'S': 6.3, 'T': 9.1,
        'U': 2.8, 'V': 1.0, 'W': 2.4, 'X': 0.2, 'Y': 2.0,
        'Z': 0.1
    }
    decrypted = CaesarCipher.decrypt(text, shift)
    freq = frequency_analysis(decrypted)
    score = sum((freq.get(ch, 0) - ef) ** 2 / ef
                for ch, ef in english_freq.items())
    return score

def password_strength(password):
    """Analyze password strength"""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32

    entropy = length * math.log2(charset_size) if charset_size > 0 else 0
    combinations = charset_size ** length if charset_size > 0 else 0

    score = 0
    score += min(length * 4, 40)
    if has_upper: score += 10
    if has_lower: score += 10
    if has_digit: score += 10
    if has_special: score += 15
    if length >= 12: score += 15

    if score >= 80: rating = "STRONG"
    elif score >= 60: rating = "GOOD"
    elif score >= 40: rating = "FAIR"
    else: rating = "WEAK"

    return {
        'length': length,
        'entropy': entropy,
        'combinations': combinations,
        'score': score,
        'rating': rating,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_special': has_special,
    }


# ═══════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════

def main():
    plaintext = "The art of cryptography is as ancient as writing itself"

    print("=" * 62)
    print("          CRYPTOGRAPHY TOOLKIT v1.0")
    print("=" * 62)
    print()
    print(f"  Original: {plaintext}")
    print()

    # ─── Caesar Cipher ───
    print("-" * 62)
    print("  CAESAR CIPHER")
    print("-" * 62)
    for shift in [3, 7, 13, 21]:
        enc = CaesarCipher.encrypt(plaintext, shift)
        dec = CaesarCipher.decrypt(enc, shift)
        ok = "PASS" if dec == plaintext else "FAIL"
        print(f"  Shift {shift:2d}: {enc}")
        print(f"  Verify:  {ok}")
    print()

    # ─── Vigenere Cipher ───
    print("-" * 62)
    print("  VIGENERE CIPHER")
    print("-" * 62)
    for key in ["PYTHON", "CRYPTO", "TIMEWARP"]:
        enc = VigenereCipher.encrypt(plaintext, key)
        dec = VigenereCipher.decrypt(enc, key)
        ok = "PASS" if dec == plaintext else "FAIL"
        print(f"  Key={key:8s}  Encrypted: {enc}")
        print(f"  {'':14s}  Decrypted: {dec}  [{ok}]")
    print()

    # ─── Substitution Cipher ───
    print("-" * 62)
    print("  SUBSTITUTION CIPHER")
    print("-" * 62)
    sub_key = SubstitutionCipher.generate_key("CRYPTOGRAPHY")
    print(f"  Key alphabet:  {sub_key}")
    print(f"  Plain alpha:   {string.ascii_uppercase}")
    enc = SubstitutionCipher.encrypt(plaintext, sub_key)
    dec = SubstitutionCipher.decrypt(enc, sub_key)
    ok = "PASS" if dec == plaintext else "FAIL"
    print(f"  Encrypted:     {enc}")
    print(f"  Decrypted:     {dec}  [{ok}]")
    print()

    # ─── Playfair Cipher ───
    print("-" * 62)
    print("  PLAYFAIR CIPHER")
    print("-" * 62)
    pf_key = "MONARCHY"
    grid = PlayfairCipher.generate_grid(pf_key)
    print(f"  Key: {pf_key}")
    print("  Grid:")
    for row in grid:
        print(f"    {' '.join(row)}")
    enc = PlayfairCipher.encrypt("ATTACK AT DAWN", pf_key)
    print(f"  Plain:  ATTACK AT DAWN")
    print(f"  Cipher: {enc}")
    print()

    # ─── Hash Functions ───
    print("-" * 62)
    print("  CRYPTOGRAPHIC HASHES")
    print("-" * 62)
    test_str = "Time Warp Classic"
    print(f"  Input: \"{test_str}\"")
    print(f"  MD5:    {hashlib.md5(test_str.encode()).hexdigest()}")
    print(f"  SHA-1:  {hashlib.sha1(test_str.encode()).hexdigest()}")
    print(f"  SHA-256:{hashlib.sha256(test_str.encode()).hexdigest()}")
    print()
    print("  Avalanche Effect (changing 1 character):")
    test_str2 = "Time Warp Classid"
    h1 = hashlib.sha256(test_str.encode()).hexdigest()
    h2 = hashlib.sha256(test_str2.encode()).hexdigest()
    diff_bits = sum(bin(int(a, 16) ^ int(b, 16)).count('1')
                    for a, b in zip(h1, h2))
    print(f"  Original:  {h1}")
    print(f"  Modified:  {h2}")
    print(f"  Bits changed: {diff_bits}/256 ({diff_bits/256*100:.1f}%)")
    print()

    # ─── Caesar Brute Force ───
    print("-" * 62)
    print("  AUTOMATED CAESAR ATTACK")
    print("-" * 62)
    secret = CaesarCipher.encrypt("Send reinforcements immediately", 19)
    print(f"  Ciphertext: {secret}")
    print()
    scores = [(s, chi_squared_score(secret, s)) for s in range(26)]
    scores.sort(key=lambda x: x[1])
    print("  Top 5 candidates (chi-squared ranking):")
    for shift, score in scores[:5]:
        dec = CaesarCipher.decrypt(secret, shift)
        marker = " <-- BEST" if shift == scores[0][0] else ""
        print(f"    Shift {shift:2d}: {dec} (score: {score:.1f}){marker}")
    print()

    # ─── Frequency Analysis ───
    print("-" * 62)
    print("  FREQUENCY ANALYSIS")
    print("-" * 62)
    long_text = ("to be or not to be that is the question whether tis nobler "
                 "in the mind to suffer the slings and arrows of outrageous "
                 "fortune or to take arms against a sea of troubles")
    enc_text = CaesarCipher.encrypt(long_text, 5)

    print("  Index of Coincidence:")
    print(f"    English text:   {index_of_coincidence(long_text):.4f} (expected ~0.0667)")
    print(f"    Caesar (mono):  {index_of_coincidence(enc_text):.4f} (preserved)")
    random_text = "xkqwzptmflbhcnaoeisudvjgryx" * 5
    print(f"    Random text:    {index_of_coincidence(random_text):.4f} (expected ~0.0385)")
    print()

    freq = frequency_analysis(long_text)
    print("  Top 10 letter frequencies (English text):")
    for ch, pct in list(freq.items())[:10]:
        bar = "#" * int(pct)
        print(f"    {ch}: {pct:5.1f}% {bar}")
    print()

    # ─── Password Strength ───
    print("-" * 62)
    print("  PASSWORD STRENGTH ANALYZER")
    print("-" * 62)
    passwords = [
        "password",
        "P@ssw0rd",
        "MyD0g$Name!2024",
        "correct-horse-battery-staple",
        "Tr0ub4dor&3",
    ]
    print(f"  {'Password':<32s} Score  Rating   Entropy")
    print("  " + "-" * 56)
    for pw in passwords:
        result = password_strength(pw)
        print(f"  {pw:<32s} {result['score']:>3d}    {result['rating']:<8s} {result['entropy']:.1f} bits")
    print()

    print("=" * 62)
    print("  Cryptography Toolkit Complete")
    print("  Ciphers: Caesar, Vigenere, Substitution, Playfair")
    print("  Analysis: Frequency, Chi-squared, IoC, Password Strength")
    print("=" * 62)


if __name__ == "__main__":
    main()
