#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright <<Insert the date here>> <<Insert your name here>>
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
Author: <<Insert your name here>>
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

    partial_hack = ssh.hackSimpleSub(message)
    
    cipher_to_plain = {c: None for c in LETTERS}
    plain_to_cipher = {c: None for c in LETTERS}
    
    for c, p in zip(message, partial_hack):
        if c.upper() in LETTERS and p.upper() in LETTERS:
            cipher_to_plain[c.upper()] = p.upper()
            plain_to_cipher[p.upper()] = c.upper()
            
    dict_words = {}
    with open('dictionary.txt', 'r') as f:
        for line in f:
            w = line.strip().upper()
            if w.isalpha():
                if len(w) not in dict_words:
                    dict_words[len(w)] = []
                dict_words[len(w)].append(w)
                

    cipher_words = list(set(re.findall(r'[A-Za-z]+', message.upper())))
    
    changed = True
    while changed:
        changed = False
        
        for c_word in cipher_words:
            if all(cipher_to_plain[c] is not None for c in c_word):
                continue
                
            candidates = []
            for w in dict_words.get(len(c_word), []):
                valid = True
                temp_c_to_p = {}
                temp_p_to_c = {}
                
                for i in range(len(c_word)):
                    c = c_word[i]
                    p = w[i]
                    
                    if cipher_to_plain[c] is not None and cipher_to_plain[c] != p:
                        valid = False
                        break
                    if plain_to_cipher[p] is not None and plain_to_cipher[p] != c:
                        valid = False
                        break
                        
                    if c in temp_c_to_p and temp_c_to_p[c] != p:
                        valid = False
                        break
                    if p in temp_p_to_c and temp_p_to_c[p] != c:
                        valid = False
                        break
                        
                    temp_c_to_p[c] = p
                    temp_p_to_c[p] = c
                    
                if valid:
                    candidates.append(w)
                    
            if candidates:
                unmapped_chars = set(c for c in c_word if cipher_to_plain[c] is None)
                for c in unmapped_chars:
                    idx = c_word.index(c)
                    
                    possible_p = set(cand[idx] for cand in candidates)
                    
                    if len(possible_p) == 1:
                        p = possible_p.pop()
                        cipher_to_plain[c] = p
                        plain_to_cipher[p] = c
                        changed = True
                        
    final_message = ''
    for char in message:
        if char.upper() in LETTERS:
            p = cipher_to_plain[char.upper()]
            if p is None:
                final_message += char 
            else:
                if char.isupper():
                    final_message += p
                else:
                    final_message += p.lower()
        else:
            final_message += char
            
    return final_message


def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
    # End of provided test.
    

if __name__ == '__main__':
    test()
