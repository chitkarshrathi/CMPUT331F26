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
#----------------------------------------------------------------

#-------------------- START ASSIGNMENT HERE ---------------------
"""
General decryption program
Author: <<Insert your name here>>
"""

from detectEnglish import isEnglish
from itertools import permutations

from typing import List

def hack(ciphertype: str, ciphertext: str):
    """
    Decrypt a given ciphertext with either of these algorithm: caesar, transposition, or affine.
        Input: a line from `ciphers.txt`.
        Output: the decrypted message (or plaintext).
    """
    
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Code referenced and used from a1p1.py and a1p3.py submission for CMPUT331 Assignment 1 by Chitkarsh Rathi on 9/21/2026. Some modiciations made to the code to fit the requirements of this assignment.
    if ciphertype == 'C':
        output = []
        
        char_to_index = {char: idx for idx, char in enumerate(LETTERS)}
        index_to_char = {idx: char for idx, char in enumerate(LETTERS)}

        for ch in LETTERS:
            message = ciphertext.upper()
            key = ch.upper()
            translated = ''

            for i in message:
                if i in char_to_index:
                    shift = char_to_index[key[0]]
                    index = (char_to_index[i] - shift) % len(LETTERS)
                    translated += index_to_char[index]
                else:
                    translated += i
                    
            decrypted_text = translated

            count  = 0
            for k in decrypted_text.split():
                cleaned_word = ''

                for c in k.upper():
                    if c in LETTERS:
                        cleaned_word += c

                if isEnglish(cleaned_word):
                    count += 1

            output.append((decrypted_text, ch, count))

        # sorts output by highest count, then uses a tie-breaker by alphabets 
        output.sort(key=lambda x: (-x[2], x[0]))
        return output[0][0]

    # Code referenced and used from a1p1.py and a2p3.py submission for CMPUT331 Assignment 2 by Chitkarsh Rathi on 9/28/2026. Some modiciations made to the code to fit the requirements of this assignment.
    elif ciphertype == 'T':
        for col_length in range(1, 10):
            for key_tuple in permutations(range(1, col_length + 1)):
                key = list(key_tuple)
                message = ciphertext

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

                if isEnglish(plaintext):
                    return plaintext

    elif ciphertype == 'A':
        output = []
        
        char_to_index = {char: idx for idx, char in enumerate(LETTERS)}
        index_to_char = {idx: char for idx, char in enumerate(LETTERS)}
        
        valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        
        for key_a in valid_a:
            mod_inv_a = -1
            for x in range(1, len(LETTERS)):
                if (key_a * x) % len(LETTERS) == 1:
                    mod_inv_a = x
                    break
                    
            if mod_inv_a == -1:
                continue
                
            for key_b in range(len(LETTERS)):
                message = ciphertext.upper()
                translated = ''
                
                for i in message:
                    if i in char_to_index:
                        y = char_to_index[i]
                        index = (mod_inv_a * (y - key_b)) % len(LETTERS)
                        translated += index_to_char[index]
                    else:
                        translated += i
                        
                decrypted_text = translated
                
                count = 0
                for k in decrypted_text.split():
                    cleaned_word = ''
                    
                    for c in k.upper():
                        if c in LETTERS:
                            cleaned_word += c
                            
                    if isEnglish(cleaned_word):
                        count += 1
                        
                output.append((decrypted_text, key_b, count))
                
        output.sort(key=lambda x: (-x[2], x[1]))
        return output[0][0]

def processing():
    # Add the processing steps here like reading form ciphers.txt, calling the hack function, writing to decrypted.txt, etc.
    decrypted_messages = []
    
    with open('ciphers.txt', 'r') as f:
        for line in f:
            line = line.strip()
            
            if line:
                parts = line.split(';')
                ciphertype = parts[0]
                ciphertext = parts[1]
                
                plaintext = hack(ciphertype, ciphertext)
                
                if plaintext:
                    decrypted_messages.append(plaintext)
                else:
                    decrypted_messages.append("FAILED TO DECRYPT")
                    
    with open('decrypted.txt', 'w') as f:
        for msg in decrypted_messages:
            f.write(msg + '\n')

def test():
    # Test cases for the hack function. You can add more tests as needed.
    assert hack("C", "GHGIQ") == "ABACK", "Caesar hack failed"
    assert hack("T", "IS HAUCREERNP F") == "CIPHERS ARE FUN", "Transposition hack failed"
    assert hack("A", "IHHWVC SWFRCP") == "AFFINE CIPHER", "Affine hack failed"
    assert hack("A", "XBQUVSQVFRUVLE FVSOTG") == "MULTIPLICATION CIPHER", "Affine hack failed"

if __name__ == '__main__':
    test()