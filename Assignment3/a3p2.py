#!/usr/bin/python3

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
CMPUT 331 Assignment 3 Student Solution
Author: Chitkarsh Rathi
"""

from sys import flags


def affine_key_count(m):
    if m < 2:
        return 0

    count = m
    n = m 

    if n % 2 == 0:
        while n % 2 == 0:
            n //= 2
        count -= count // 2

    p = 3
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            count -= count // p
        p += 2

    if n > 1:
        count -= count // n

    return (count * m) - 1


def test():
    assert affine_key_count(65) == 3119


if __name__ == "__main__" and not flags.interactive:
    test()
