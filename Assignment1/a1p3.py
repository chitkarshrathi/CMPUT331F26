#!/usr/bin/python3

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
CMPUT 331 Assignment 1 Student Solution
September 2026
Author: Chitkarsh Rathi
"""


from sys import flags
from a1p1 import encrypt, decrypt

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def crack_caesar(ciphertext, val_words):
    output = []

    for ch in LETTERS:
        decrypted_text = decrypt(ciphertext, ch)
        count  = 0

        for k in decrypted_text.split():
            cleaned_word = ''

            for c in k.upper():
                if c in LETTERS:
                    cleaned_word += c

            if cleaned_word in val_words:
                count += 1

        output.append((decrypted_text, ch, count))

    # sorts output by highest count, then uses a tie-breaker by alphabets 
    output.sort(key=lambda x: (-x[2], x[0]))
    return output[0][0], output[0][1]


def form_dictionary(text_address='carroll-alice.txt'):
    val_words = set()

    with open(text_address, 'r') as f:
        for line in f:
            for word in line.split():
                cleaned_word = ''

                for c in word.upper():
                    if c in LETTERS:
                        cleaned_word += c

                if cleaned_word:
                    val_words.add(cleaned_word)

    return val_words



def test():
    assert crack_caesar('TBIZLJB QL TLKABOIXKA', form_dictionary()) == ('WELCOME TO WONDERLAND', 'X')


if __name__ == "__main__" and not flags.interactive:
    test()