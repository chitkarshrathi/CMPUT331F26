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
Assignment Vigenère Problem 1
"""

from sys import flags


def antiKasiski(key: str, plaintext: str) -> str:
    """
    Thwart Kasiski examination 
    """
    raise NotImplementedError()


def test():
    "Run tests"
    ciphertext = antiKasiski("WICK", "THOSEPOLICEOFFICERSOFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY")
    expected = "PPQCAXQVEKGYBNZSYMTCTWHPAZGNDMTKNQFODWOOPPGHUBGVHBJOTUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU"
    assert ciphertext == expected
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking


# Invoke test() if called via `python3 avigp1.py`
# but not if `python3 -i avigp1.py` or `from avigp1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
