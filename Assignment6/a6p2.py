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
Problem 2
"""

from sys import flags

def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:

    if n <= 0 or n > len(ciphertext):
        return 0.0

    decrypted_text = ''.join(mapping.get(c, c) for c in ciphertext)

    ngram_counts = {}

    for i in range(len(decrypted_text) - n + 1):
        ngram = decrypted_text[i:i+n]
        ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1

    score = 0.0

    for ngram, count in ngram_counts.items():
        frequency = frequencies.get(ngram, 0.0)
        score += count * frequency

    return score    
    
  

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

    mapping = {chr(i): chr(i) for i in range(65, 91)}
    mapping[' '] = ' '
    
    ciphertext = "EEFFFEEF"
    frequencies = {'EE': 0.5, 'EF': 0.2, 'FE': 0.3}
    n = 2
    
    res1 = keyScore(mapping, ciphertext, frequencies, n)
    # Expected: (2 * 0.5) + (2 * 0.2) + (2 * 0) + (1 * 0.3) = 1.0 + 0.4 + 0 + 0.3 = 1.7
    assert abs(res1 - 1.7) < 1e-6, f"Failed Test 1: {res1}"
    print("Test 1 passed: Given assignment example")

    # Test 2: Edge case where no n-grams are in the frequency dictionary
    res2 = keyScore(mapping, "AAAAA", frequencies, 2)
    assert res2 == 0.0, f"Failed Test 2: {res2}"
    print("Test 2 passed: No matching n-grams")

    # Test 3: Actual mapping translation test
    # Ciphertext "XXYYY" translated with X->E, Y->F becomes "EEFFF"
    test_mapping = mapping.copy()
    test_mapping['X'] = 'E'
    test_mapping['Y'] = 'F'
    
    # Decipherment will be "EEFFF"
    # Bigrams: EE, EF, FF, FF
    # Counts: EE:1, EF:1, FF:2
    # Score: (1 * 0.5) + (1 * 0.2) + (2 * 0.0) = 0.7
    res3 = keyScore(test_mapping, "XXYYY", frequencies, 2)
    assert abs(res3 - 0.7) < 1e-6, f"Failed Test 3: {res3}"
    print("Test 3 passed: Mapping translation")

    # Test 4: Out of bounds n
    assert keyScore(mapping, "TEXT", frequencies, 0) == 0.0, "Failed Test 4a"
    assert keyScore(mapping, "TEXT", frequencies, 5) == 0.0, "Failed Test 4b"
    print("Test 4 passed: Out of bounds n values")

    # Test 5: Empty ciphertext
    assert keyScore(mapping, "", frequencies, 2) == 0.0, "Failed Test 5"
    print("Test 5 passed: Empty ciphertext")

    # Test 6: Empty frequencies dictionary
    # Even with a valid string, if we have no known frequencies, score must be 0.0
    assert keyScore(mapping, "EEFFFEEF", {}, 2) == 0.0, "Failed Test 6"
    print("Test 6 passed: Empty frequencies dictionary")

    # Test 7: Unigrams (n = 1)
    unigram_freqs = {'E': 0.5, 'F': 0.1}
    # Ciphertext "EF E" -> Maps to "EF E"
    # Counts: E:2, F:1, ' ':1
    # Score: (2 * 0.5) + (1 * 0.1) + (1 * 0.0) = 1.1
    res7 = keyScore(mapping, "EF E", unigram_freqs, 1)
    assert abs(res7 - 1.1) < 1e-6, f"Failed Test 7: {res7}"
    print("Test 7 passed: Unigram scoring (n=1)")

    # Test 8: Mapping spaces correctly
    space_mapping = mapping.copy()
    space_mapping['X'] = 'E'
    space_mapping['Y'] = 'F'
    space_mapping['Z'] = ' ' # Suppose Z maps to space just for a strict test
    # Cipher: "XZY" -> Deciphered: "E F"
    # n = 2. Bigrams in "E F": "E ", " F"
    freq_space = {"E ": 0.8, " F": 0.2}
    res8 = keyScore(space_mapping, "XZY", freq_space, 2)
    # Score: (1 * 0.8) + (1 * 0.2) = 1.0
    assert abs(res8 - 1.0) < 1e-6, f"Failed Test 8: {res8}"
    print("Test 8 passed: Correctly scoring spaces in decipherment")

    print("------------------------------")
    print("All tests passed successfully!")

if __name__ == "__main__" and not flags.interactive:
    test()





