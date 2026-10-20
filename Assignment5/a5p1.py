#!/usr/bin/env python3

#---------------------------------------------------------------
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
#---------------------------------------------------------------

"""
CMPUT 331 Assignment 5 Problem 1 Student Solution
Author: Chitkarsh Rathi
"""
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
from sys import flags
from collections import Counter # Helpful class, see documentation or help(Counter)

def freqDict(ciphertext: str) -> dict:
    """
    Analyze the frequency of the letters
    """

    counts = Counter(c for c in ciphertext.upper() if c.isalpha())
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    mapping = {}
    for i in range(len(sorted_counts)):
        letter = sorted_counts[i][0]
        mapping[letter] = ETAOIN[i]
    return mapping

def freqDecrypt(mapping: dict, ciphertext: str) -> str:
    """
    Apply the mapping to ciphertext
    """

    decrypted = []
    for c in ciphertext:
        if c.isalpha():
            upper_c = c.upper()
            decrypted.append(mapping.get(upper_c, upper_c))
        else:
            decrypted.append(c)

    return ''.join(decrypted)

def test():
    "Run tests"
    assert type(freqDict("A")) is dict
    assert freqDict("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")["A"] == "E"
    assert freqDict("AABBA")['B'] == "T"
    assert freqDict("-: AB CD AH")['A'] == "E"
    assert freqDecrypt({"A": "E", "Z": "L", "T": "H", "F": "O", "U": "W", "I": "R", "Q": "D"}, "TAZZF UFIZQ!") == "HELLO WORLD!"


# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
