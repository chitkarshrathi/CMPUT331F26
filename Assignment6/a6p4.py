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
Problem 4
"""

from sys import flags
import a6p1, a6p2, a6p3


ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # This is the true English letter frequency


def breakSub(cipherFile: str, textFile: str) -> None:
    """
    Inputs:
        cipherFile:
            'text_finnegan_cipher.txt' for testing
            'text_cipher.txt' for submission
            Path to the ciphertext file.

        textFile:
            'wells.txt'
            Path to the English reference text file.

    Outputs:
        Save deciphered text to the address 'text_plain.txt'
    """
    n = 2  # Use bigrams as required by the assignment

    with open(cipherFile, 'r') as f:
        ciphertext = f.read()

    with open(textFile, 'r') as f:
        reference_text = f.read()

    frequencies = a6p1.ngramsFreqs(reference_text, n)

    counts = {chr(i): 0 for i in range(65, 91)}

    for char in ciphertext:
        if char in counts:
            counts[char] += 1

    sorted_letters = sorted(counts.keys(), key=lambda x: (-counts[x], x))

    mapping = {' ' : ' '}

    for i, j in enumerate(sorted_letters):
        mapping[j] = ETAOIN[i]

    current_mapping = mapping

    while True:
        new_mapping = a6p3.bestSuccessor(current_mapping, ciphertext, frequencies, n)

        if new_mapping == current_mapping:
            break

        current_mapping = new_mapping

    decrypted_chars = []

    for char in ciphertext:
        decrypted_chars.append(current_mapping.get(char, char))

    decrypted_text = ''.join(decrypted_chars)

    with open('text_plain.txt', 'w') as f:
        f.write(decrypted_text)


'''
Use this section to import your code from A6P1, A6P2, A6P3
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''
        
def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

    print("Testing Finnegan cipher...")
    try:
        breakSub("text_finnegan_cipher.txt", "wells.txt")
        print("Finnegan cipher decrypted.")
        
        with open('text_plain.txt', 'r') as f1, open('text_finnegan_plain.txt', 'r') as f2:
            my_output = f1.read()
            expected_output = f2.read()
            
        if my_output == expected_output:
            print("SUCCESS: Deciphered text matches the reference file.")
        else:
            print("FAILURE: Deciphered text does not match the reference file.")
            
        print("-" * 40)
        
        # Final submission run
        breakSub("text_cipher.txt", "wells.txt")
        print("Final submission cipher decrypted and saved.")
        
    except FileNotFoundError as e:
        print(f"Test skipped: A required file was not found - {e}")
    
if __name__ == "__main__" and not flags.interactive:
    test()