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
Problem 3
"""

from sys import flags
import a6p2


'''
Use this section to import your code from A6P2 
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''

def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:
    return a6p2.keyScore(mapping, ciphertext, frequencies, n)



def bestSuccessor(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> dict:
    og_score = keyScore(mapping, ciphertext, frequencies, n)
    highest_score = og_score
    best_mapping = 0

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for i in range(len(letters)):
        for j in range(i + 1, len(letters)):
            k1 = letters[i]
            k2 = letters[j]

            new_mapping = mapping.copy()
            new_mapping[k1], new_mapping[k2] = new_mapping[k2], new_mapping[k1]
            new_score = keyScore(new_mapping, ciphertext, frequencies, n)

            if new_score > highest_score:
                highest_score = new_score
                best_mapping = new_mapping
            elif new_score == highest_score and best_mapping != 0:
                best_mapping = breakKeyScoreTie(mapping, best_mapping, new_mapping)

    return best_mapping if best_mapping != 0 else mapping



def breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB):
    """
    Break the tie between two successor mappings that have the same keyscore

    originalMapping: mapping the the other parameters are successors to
    successorMappingA: mapping that has had two keys swapped
    successorMappingB: mapping that has had two other keys swapped

    Example usage:
    originalMapping = {"A": "A", "B": "B", "C": "C"}
    # Mapping with B and C switched
    successorMappingA = {"A": "A", "B": "C", "C": "B"}
    # Mapping with A and C switched
    successorMappingB = {"A": "C", "B": "B", "C": "A"}

    # AC < BC so this function will return successorMappingB
    assert breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB) == successorMappingB
    """
    aSwapped = "".join(sorted(k for k, v in (
        set(successorMappingA.items()) - set(originalMapping.items()))))
    bSwapped = "".join(sorted(k for k, v in (
        set(successorMappingB.items()) - set(originalMapping.items()))))
    return successorMappingA if aSwapped < bSwapped else successorMappingB

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C"}, {"A": "A", "B": "C", "C": "B"}, {
                            "A": "C", "B": "B", "C": "A"}) == {"A": "C", "B": "B", "C": "A"}
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C", "D": "D"}, {
                            "A": "B", "B": "A", "C": "C", "D": "D"}, {"A": "A", "B": "B", "C": "D", "D": "C"}) == {"A": "B", "B": "A", "C": "C", "D": "D"}

    mapping = {chr(i): chr(i) for i in range(65, 91)}
    mapping[' '] = ' '


    # --- Edge Cases ---
    
    # Test 3: Empty Ciphertext
    # An empty string cannot be scored, so no successor can beat the original 0.0 score.
    assert bestSuccessor(mapping, "", {'AA': 1.0}, 2) == mapping
    print("Test 3 passed: Empty ciphertext returns original mapping")

    # Test 4: Empty Frequency Dictionary
    # With no known frequencies, every decipherment scores 0.0. No strict improvement possible.
    assert bestSuccessor(mapping, "HELLO", {}, 2) == mapping
    print("Test 4 passed: Empty frequencies dictionary returns original mapping")

    # Test 5: Out of bounds 'n'
    # n is larger than the ciphertext. Score is 0.0, no improvement possible.
    assert bestSuccessor(mapping, "HI", {'HI ': 1.0}, 5) == mapping
    print("Test 5 passed: n > len(ciphertext) returns original mapping")

    # Test 6: Same Score Swap (No Strict Improvement)
    # Original decipherment is "AB" (score 1.0). Swapping A and B gives "BA" (also score 1.0).
    # Since it is a tie with the *original* mapping, it must return the original mapping.
    freqs_tie_orig = {'AB': 1.0, 'BA': 1.0}
    assert bestSuccessor(mapping, "AB", freqs_tie_orig, 2) == mapping
    print("Test 6 passed: Equal score to original returns original mapping")

    # Test 7: Strict Improvement (Basic)
    # Ciphertext "XX" has score 0.0. Swapping X with A creates "AA", boosting score to 1.0.
    freqs_single = {'AA': 1.0, 'XX': 0.0}
    expected_map7 = mapping.copy()
    expected_map7['X'], expected_map7['A'] = 'A', 'X'
    assert bestSuccessor(mapping, "XX", freqs_single, 2) == expected_map7
    print("Test 7 passed: Finds single strict improvement")

    # Test 8: Successor Tie-Breaking Scenario
    # Ciphertext is "XY" (score 0.0).
    # Swap X and A -> "AY" (score 1.0). Swap X and B -> "BY" (score 1.0).
    # Both are strict improvements, so they tie for best. 
    # breakKeyScoreTie must resolve this. Swapped keys are 'AX' vs 'BX'. 'AX' wins.
    freqs_tie_succ = {'AY': 1.0, 'BY': 1.0, 'XY': 0.0}
    expected_map8 = mapping.copy()
    expected_map8['X'], expected_map8['A'] = 'A', 'X'
    assert bestSuccessor(mapping, "XY", freqs_tie_succ, 2) == expected_map8
    print("Test 8 passed: Correctly breaks ties between two equally improved successors")

    # Test 9: Shifted/Randomized Initial Mapping
    # The starting mapping isn't identity. A maps to B, B maps to C, etc.
    shifted_map = {chr(i): chr(i+1) for i in range(65, 90)}
    shifted_map['Z'] = 'A'
    shifted_map[' '] = ' '
    
    # Ciphertext "Z " decodes to "A ". 
    # If we swap Z's mapping ('A') with Q's mapping ('R'), it will decode to "R ".
    freqs_shifted = {"A ": 0.0, "R ": 5.0}
    expected_map9 = shifted_map.copy()
    expected_map9['Z'] = 'R'
    expected_map9['Q'] = 'A' # Because Q originally mapped to R, now maps to A
    
    assert bestSuccessor(shifted_map, "Z ", freqs_shifted, 2) == expected_map9
    print("Test 9 passed: Handles randomized/non-identity initial mappings")

    # Test 10: Unigram (n=1) Improvement
    # Decipherment of "X X" gives two 'X's (score 0.0). Swap X->E gives two 'E's (score 2.0).
    freqs_unigram = {'E': 1.0, ' ': 0.0}
    expected_map10 = mapping.copy()
    expected_map10['X'], expected_map10['E'] = 'E', 'X'
    assert bestSuccessor(mapping, "X X", freqs_unigram, 1) == expected_map10
    print("Test 10 passed: Works correctly with unigrams (n=1)")

    print("------------------------------")
    print("All 10 extreme tests passed successfully!")
    print("All tests passed successfully!")

if __name__ == "__main__" and not flags.interactive:
    test()