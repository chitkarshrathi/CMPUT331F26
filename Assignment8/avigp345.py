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
Assignment Vigenère Problems 3, 4, and 5
"""

import re
from sys import flags


def numbersClose(a, b):
    return abs(a - b) < 0.000001

def stringIC(text: str) -> float:
    """
    Compute the index of coincidence (IC) for text
    """

    n = len(text)
    if n <= 1:
        return 0.0

    counts = {}
    for ch in text:
        if ch in counts:
            counts[ch] = counts[ch] + 1
        else:
            counts[ch] = 1

    numerator = 0
    for letter in counts:
        freq = counts[letter]
        numerator = numerator + freq * (freq - 1)

    denominator = n * (n - 1)
    return numerator / denominator


def subseqIC(ciphertext: str, keylen: int) -> float:
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """

    if keylen <= 0:
        return 0.0

    total_ic = 0.0
    for i in range(1, keylen + 1):
        subseq = getNthSubkeysLetters(i, keylen, ciphertext)
        ic = stringIC(subseq)
        total_ic = total_ic + ic

    average_ic = total_ic / keylen
    return average_ic


def keyLengthIC(ciphertext: str, n: int) -> list:
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    scores = []
    for keylen in range(1, 21):
        avg_ic = subseqIC(ciphertext, keylen)
        scores.append((-avg_ic, keylen))

    scores.sort()

    top_lengths = []
    for i in range(n):
        top_lengths.append(scores[i][1])

    return top_lengths


def getNthSubkeysLetters(nth: int, keyLength: int, message: str):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    message = re.compile('[^A-Z]').sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def test():
    "Run tests"
    assert numbersClose(stringIC("ABA"), 1 / 3)
    assert numbersClose(subseqIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 3), 0.03882783882783883)
    assert numbersClose(subseqIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 4), 0.0601010101010101)
    assert numbersClose(subseqIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 5), 0.012698412698412698)
    expected = [8, 16, 4, 12, 6]
    assert keyLengthIC("PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU", 5) == expected
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

    # 2. Empty string and single character (avoid division by zero)
    ic = stringIC("")
    assert numbersClose(ic, 0.0), f"Got {ic}, expected 0.0"

    ic = stringIC("A")
    assert numbersClose(ic, 0.0), f"Got {ic}, expected 0.0"

    # 3. All identical letters (maximum IC = 1.0)
    ic = stringIC("AAAA")
    assert numbersClose(ic, 1.0), f"Got {ic}, expected 1.0"

    # 4. All distinct letters (minimum IC = 0.0)
    ic = stringIC("ABCDEF")
    assert numbersClose(ic, 0.0), f"Got {ic}, expected 0.0"

    # 5. Multiple repeated letters ("AABB" -> (2 + 2) / 12 = 1/3)
    ic = stringIC("AABB")
    assert numbersClose(ic, 1 / 3), f"Got {ic}, expected {1 / 3}"

    # 6. Mixed frequencies ("MISSISSIPPI" -> (12 + 12 + 2) / 110 = 26/110)
    ic = stringIC("MISSISSIPPI")
    assert numbersClose(ic, 26 / 110), f"Got {ic}, expected {26 / 110}"



    avg_ic = subseqIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 4)
    assert numbersClose(avg_ic, 0.0601010101010101), f"Got {avg_ic}, expected 0.0601010101010101"

    avg_ic = subseqIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 5)
    assert numbersClose(avg_ic, 0.012698412698412698), f"Got {avg_ic}, expected 0.012698412698412698"

    # 2. Key length of 1 (should match stringIC directly)
    avg_ic = subseqIC("ABA", 1)
    assert numbersClose(avg_ic, 1 / 3), f"Got {avg_ic}, expected {1 / 3}"

    # 3. Perfectly periodic text ("AA", "BB", "CC" -> average IC = 1.0)
    avg_ic = subseqIC("ABCABC", 3)
    assert numbersClose(avg_ic, 1.0), f"Got {avg_ic}, expected 1.0"

    # 4. All distinct letters in every subsequence ("ABC", "ABC" -> 0.0)
    avg_ic = subseqIC("AABBCC", 2)
    assert numbersClose(avg_ic, 0.0), f"Got {avg_ic}, expected 0.0"

    # 5. Uneven subsequence lengths ("ABA" -> 1/3, "AB" -> 0.0; avg = 1/6)
    avg_ic = subseqIC("AABBA", 2)
    assert numbersClose(avg_ic, 1 / 6), f"Got {avg_ic}, expected {1 / 6}"

    # 6. Key length larger than ciphertext length
    avg_ic = subseqIC("ABCD", 5)
    assert numbersClose(avg_ic, 0.0), f"Got {avg_ic}, expected 0.0"



    ct = "PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU"
    res = keyLengthIC(ct, 1)
    assert res == [8], f"Got {res}, expected [8]"

    # 3. Boundary n = 20 (returns all key lengths 1..20 with no duplicates)
    res = keyLengthIC(ct, 20)
    assert len(res) == 20 and sorted(res) == list(range(1, 21)), f"Invalid n=20 result: {res}"

    # 4. Empty string (all ICs are 0.0 -> tie-breaker picks lowest key lengths)
    res = keyLengthIC("", 5)
    assert res == [1, 2, 3, 4, 5], f"Got {res}, expected [1, 2, 3, 4, 5]"

    # 5. All distinct letters (all ICs are 0.0 -> tie-breaker picks lowest)
    res = keyLengthIC("ABCDEFGHIJ", 5)
    assert res == [1, 2, 3, 4, 5], f"Got {res}, expected [1, 2, 3, 4, 5]"

    # 6. All identical letters (all ICs are 1.0 -> tie-breaker picks lowest)
    res = keyLengthIC("A" * 40, 5)
    assert res == [1, 2, 3, 4, 5], f"Got {res}, expected [1, 2, 3, 4, 5]"

    # 7. Exact period 3 ("ABCABC" -> k=3 is 1.0, k=1 is 0.2, rest 0.0)
    res = keyLengthIC("ABCABC", 5)
    assert res == [3, 1, 2, 4, 5], f"Got {res}, expected [3, 1, 2, 4, 5]"

    # 8. Exact period 2 ("ABABABAB" -> k=2,4 tie at 1.0; then k=1, k=6, k=3)
    res = keyLengthIC("ABABABAB", 5)
    assert res == [2, 4, 1, 6, 3], f"Got {res}, expected [2, 4, 1, 6, 3]"

    # 9. Exact period 5 ("ABCDEABCDE" -> k=5 is 1.0, k=1 is 1/9, rest 0.0)
    res = keyLengthIC("ABCDEABCDE", 4)
    assert res == [5, 1, 2, 3], f"Got {res}, expected [5, 1, 2, 3]"

# Invoke test() if called via `python3 avigp234.py`
# but not if `python3 -i avigp234.py` or `from avigp234 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
