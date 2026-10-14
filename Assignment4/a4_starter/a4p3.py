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
Enhanced substitution cipher solver
Author: Chitkarsh Rathi
"""

import re
import simpleSubHacker as ssh

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hackSimpleSub(message: str):
    """
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
    """

    mapping = ssh.hackSimpleSub(message)
    
    with open('dictionary.txt', 'r') as f:
        dict_words = [line.strip().upper() for line in f if line.strip().isalpha()]
        
    clean_msg = re.sub(r'[^A-Z\s]', '', message.upper())
    cipher_words = list(set(clean_msg.split()))
    
    changed = True
    while changed:
        changed = False
        
        known_p = set(mapping[c][0] for c in LETTERS if len(mapping[c]) == 1)
        
        for c in LETTERS:
            if len(mapping[c]) != 1:
                if len(mapping[c]) == 0:
                    mapping[c] = list(LETTERS)
                
                original_len = len(mapping[c])
                mapping[c] = [p for p in mapping[c] if p not in known_p]
                
                if len(mapping[c]) == 1 and original_len != 1:
                    changed = True
                    
        mapping = ssh.removeSolvedLettersFromMapping(mapping)
        known_p = set(mapping[c][0] for c in LETTERS if len(mapping[c]) == 1)
        unknown_regex = '[^' + ''.join(known_p) + ']' if known_p else '.'

        for cw in cipher_words:
            if all(len(mapping[c]) == 1 for c in cw):
                continue
                
            pattern_str = '^'
            for c in cw:
                if len(mapping[c]) == 1:
                    pattern_str += mapping[c][0]
                elif len(mapping[c]) > 1:
                    pattern_str += '[' + ''.join(mapping[c]) + ']'
                else:
                    pattern_str += unknown_regex
            pattern_str += '$'
            
            pattern = re.compile(pattern_str)
            candidates = [w for w in dict_words if pattern.match(w)]
            
            if candidates:
                unresolved_chars = set(c for c in cw if len(mapping[c]) != 1)
                for c in unresolved_chars:
                    indices = [i for i, char in enumerate(cw) if char == c]
                    
                    possible_p_for_c = set()
                    for cand in candidates:
                        p_chars = set(cand[i] for i in indices)
                        if len(p_chars) == 1:
                            possible_p_for_c.add(cand[indices[0]])
                            
                    if len(possible_p_for_c) == 1:
                        solved_p = possible_p_for_c.pop()
                        mapping[c] = [solved_p]
                        changed = True
                        
        if changed:
            mapping = ssh.removeSolvedLettersFromMapping(mapping)

    return ssh.decryptWithCipherletterMapping(message, mapping)


def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
    # End of provided test.
    

if __name__ == '__main__':
    test()
