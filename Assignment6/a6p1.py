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
Problem 1
"""

from sys import flags

def ngramsFreqs(text: str, n: int) -> dict:
    """
    text: the content string
    n: the size of the n-grams
    """

    if n <= 0 or n > len(text):
        return {}

    counts = {}
    total_ngrams = 0

    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        counts[ngram] = counts.get(ngram, 0) + 1
        total_ngrams += 1

    frequencies = {}

    for ngram, count in counts.items():
        frequencies[ngram] = count / total_ngrams

    return frequencies
    

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests

    res1 = ngramsFreqs("ABABA", 2)
    assert res1 == {'AB': 0.5, 'BA': 0.5}, f"Failed Test 1: {res1}"
    print("Test 1 passed: Given example")

    # Test 2: Unigrams (1-grams)
    res2 = ngramsFreqs("AABB", 1)
    assert res2 == {'A': 0.5, 'B': 0.5}, f"Failed Test 2: {res2}"
    print("Test 2 passed: Unigrams")

    # Test 3: Trigrams with spaces
    # "A B A" length is 5. 3-grams: "A B", " B ", "B A". Total = 3. Each is 1/3.
    res3 = ngramsFreqs("A B A", 3)
    assert abs(res3['A B'] - 1/3) < 1e-6, f"Failed Test 3a: {res3}"
    assert abs(res3[' B '] - 1/3) < 1e-6, f"Failed Test 3b: {res3}"
    assert abs(res3['B A'] - 1/3) < 1e-6, f"Failed Test 3c: {res3}"
    print("Test 3 passed: Trigrams with spaces")

    # Test 4: n equals the length of the string
    res4 = ngramsFreqs("HELLO", 5)
    assert res4 == {'HELLO': 1.0}, f"Failed Test 4: {res4}"
    print("Test 4 passed: n equals string length")

    # Test 5: Edge cases (n <= 0 or n > len(text))
    assert ngramsFreqs("TEXT", 0) == {}, "Failed Test 5a"
    assert ngramsFreqs("TEXT", -1) == {}, "Failed Test 5b"
    assert ngramsFreqs("TEXT", 5) == {}, "Failed Test 5c"
    print("Test 5 passed: Out of bounds n values")

    # Test 6: Empty string input
    assert ngramsFreqs("", 1) == {}, "Failed Test 6"
    print("Test 6 passed: Empty string input")

    # Test 7: String with all identical characters
    res7 = ngramsFreqs("AAAAA", 2)
    assert res7 == {'AA': 1.0}, f"Failed Test 7: {res7}"
    print("Test 7 passed: Identical characters")

    # Test 8: String with only spaces
    res8 = ngramsFreqs("   ", 2)
    assert res8 == {'  ': 1.0}, f"Failed Test 8: {res8}"
    print("Test 8 passed: String with only spaces")

    print("------------------------------")
    print("All tests passed successfully!")
if __name__ == "__main__" and not flags.interactive:
    test()
