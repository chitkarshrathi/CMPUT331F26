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
Nomenclator cipher
Author: <<Insert your name here>>
"""

import random


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def translateMessage(key: str, message: str, codebook: dict, mode: str):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    """

    cb_encrypt = {}
    for k, v in codebook.items():
        cb_encrypt[k.lower()] = v
        
    cb_decrypt = {}
    for k, v in codebook.items():
        for symbol in v:
            cb_decrypt[symbol] = k

    char_to_sub = {}
    if mode == 'encrypt':
        for i in range(len(LETTERS)):
            char_to_sub[LETTERS[i]] = key[i]
            char_to_sub[LETTERS[i].lower()] = key[i].lower()
    else:
        for i in range(len(LETTERS)):
            char_to_sub[key[i]] = LETTERS[i]
            char_to_sub[key[i].lower()] = LETTERS[i].lower()

    parts = []
    current_part = ''
    for char in message:
        if char.isspace():
            if current_part and not current_part[-1].isspace():
                parts.append(current_part)
                current_part = ''
            current_part += char
        else:
            if current_part and current_part[-1].isspace():
                parts.append(current_part)
                current_part = ''
            current_part += char
    if current_part:
        parts.append(current_part)

    translated = ''

    for part in parts:
        if part and part[0].isspace():
            translated += part
        else:
            start_idx = 0
            end_idx = len(part) - 1
            
            while start_idx <= end_idx:
                c = part[start_idx]
                if mode == 'encrypt':
                    is_target = c.upper() in LETTERS
                else:
                    is_target = c.upper() in LETTERS or c.isdigit()
                
                if is_target:
                    break
                start_idx += 1
                
            while end_idx >= start_idx:
                c = part[end_idx]
                if mode == 'encrypt':
                    is_target = c.upper() in LETTERS
                else:
                    is_target = c.upper() in LETTERS or c.isdigit()
                    
                if is_target:
                    break
                end_idx -= 1
                
            if start_idx > end_idx:
                for c in part:
                    if c in char_to_sub:
                        translated += char_to_sub[c]
                    else:
                        translated += c
            else:
                prefix = part[:start_idx]
                core = part[start_idx:end_idx + 1]
                suffix = part[end_idx + 1:]
                
                if mode == 'encrypt':
                    if core.lower() in cb_encrypt:
                        symbol = random.choice(cb_encrypt[core.lower()])
                        translated += prefix + symbol + suffix
                    else:
                        for c in part:
                            if c in char_to_sub:
                                translated += char_to_sub[c]
                            else:
                                translated += c
                else:
                    if core in cb_decrypt:
                        original_word = cb_decrypt[core]
                        translated += prefix + original_word + suffix
                    else:
                        for c in part:
                            if c in char_to_sub:
                                translated += char_to_sub[c]
                            else:
                                translated += c

    return translated


def encryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'encrypt')


def decryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'decrypt')


def test():
    # Provided tests.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    plaintext = "X-ray machines cannot be brought here, as -ray* are very dangerous. Hello;ray! ray;"
    codebook = {'ray':['1']}
    ciphertext = encryptMessage(key, plaintext, codebook)
    assert ciphertext=="G-clh nlwisxar wlxxpj fa fcptuij iaca, lr -1* lca qach olxuacptr. Iammp;clh! 1;"
    # End of provided tests.

if __name__ == '__main__':
    test()
