#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright <<Current Year>> <<Insert your name here>>
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
    raise NotImplementedError()


def subseqIC(ciphertext: str, keylen: int) -> float:
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    raise NotImplementedError()


def keyLengthIC(ciphertext: str, n: int) -> list:
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    raise NotImplementedError()


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


# Invoke test() if called via `python3 avigp234.py`
# but not if `python3 -i avigp234.py` or `from avigp234 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
