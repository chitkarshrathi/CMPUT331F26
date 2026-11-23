#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Chitkarsh Rathi
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------

"""
Assignment Vigenère Problem 1
"""

from sys import flags


def antiKasiski(key: str, plaintext: str) -> str:
    """
    Thwart Kasiski examination 
    """

    modified_text = plaintext
    key_length = len(key)

    cipher_chars = []
    for i in range(len(modified_text)):
        p_num = ord(modified_text[i]) - ord("A")
        k_num = ord(key[i % key_length]) - ord("A")
        c_char = chr((p_num + k_num) % 26 + ord("A"))
        cipher_chars.append(c_char)

    ciphertext = "".join(cipher_chars)

    has_repeat = True
    while has_repeat:
        has_repeat = False
        i = 0

        while i < len(ciphertext) - 2:
            trigram = ciphertext[i : i + 3]

            if ciphertext.find(trigram, i + 1) != -1:
                insert_pos = i + 3
                modified_text = (
                    modified_text[:insert_pos] + "X" + modified_text[insert_pos:]
                )

                new_tail = []
                for j in range(insert_pos, len(modified_text)):
                    p_num = ord(modified_text[j]) - ord("A")
                    k_num = ord(key[j % key_length]) - ord("A")
                    c_char = chr((p_num + k_num) % 26 + ord("A"))
                    new_tail.append(c_char)

                ciphertext = ciphertext[:insert_pos] + "".join(new_tail)
                has_repeat = True

            i += 1

    return ciphertext


def test():
    "Run tests"
    ciphertext = antiKasiski("WICK", "THOSEPOLICEOFFICERSOFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY")
    expected = "PPQCAXQVEKGYBNZSYMTCTWHPAZGNDMTKNQFODWOOPPGHUBGVHBJOTUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

    ciphertext = antiKasiski("ABC", "THETESTCASETHATHASTHEREPEAT")
    expected = "TIGXUGSUEATGTICXUJATVHFTEQGAU"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 3. PDF Example 2 (cascading insert requiring consecutive Xs)
    ciphertext = antiKasiski("ABC", "THECATTHEMOUSETHEDOG")
    expected = "TIGXYEAUVHFOOVUEUJEEQG"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 4. Empty plaintext
    ciphertext = antiKasiski("KEY", "")
    expected = ""
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 5. Plaintext shorter than a trigram
    ciphertext = antiKasiski("KEY", "HI")
    expected = "RM"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 6. Repeated plaintext trigram that does NOT repeat in ciphertext
    ciphertext = antiKasiski("ABC", "THEATHE")
    expected = "TIGAUJE"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 7. Minimum length for a non-overlapping repeated trigram (length 6)
    ciphertext = antiKasiski("DEF", "ABCABC")
    expected = "DFHAEGF"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 8. Accidental ciphertext collision from different plaintext trigrams
    ciphertext = antiKasiski("BA", "AAABZB")
    expected = "BABXCZC"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 9. Overlapping repeated trigrams ("ABABA")
    ciphertext = antiKasiski("AB", "AAAAA")
    expected = "ABAYAB"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 10. Plaintext already containing 'X' characters
    ciphertext = antiKasiski("ABC", "XABXAB")
    expected = "XBDXYCB"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 11. Alphabet wrap-around at Z (25)
    ciphertext = antiKasiski("ZY", "ZAZAZA")
    expected = "YYYVZXZ"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"

    # 12. Key longer than plaintext
    ciphertext = antiKasiski("SUPERLONGKEY", "HELLO")
    expected = "ZYAPF"
    assert ciphertext == expected, f"\nGot:      {ciphertext}\nExpected: {expected}"


# Invoke test() if called via `python3 avigp1.py`
# but not if `python3 -i avigp1.py` or `from avigp1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
