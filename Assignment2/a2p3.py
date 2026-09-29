#!/usr/bin/python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 <<Insert your name here>>
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
CMPUT 331 Assignment 2 Student Solution
September 2026
Author: <Your name here>
"""

from typing import List

def decipherMessage(key: List[int], message: str) -> str:
    length  = len(message)
    num_cols = len(key)

    rows = length // num_cols
    if length % num_cols != 0:
        rows += 1

    space = (rows * num_cols) - length

    cols = [''] * num_cols
    idx = 0

    for i in key:
        col_idx = i - 1

        if col_idx < num_cols - space:
            col_len = rows
        else:
            col_len = rows - 1

        cols[col_idx] = message[idx:idx + col_len]
        idx += col_len

    plaintext = ''
    for i in range(rows):
        for c in cols:
            if i < len(c):
                plaintext += c[i]

    return plaintext

def test():
    assert decipherMessage([2, 4, 1, 5, 3], "IS HAUCREERNP F") == "CIPHERS ARE FUN"

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
