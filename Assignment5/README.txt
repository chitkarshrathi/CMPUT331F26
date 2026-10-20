# CMPUT 331: Assignment 5

## Student Details
- **Full Name:** `Chitkarsh Rathi`
- **CCID:** `chitkars`

## References and Resources
    http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
    https://cipherregister.com/learn/frequency-analysis
    https://www.geeksforgeeks.org/dsa/program-to-perform-a-letter-frequency-attack-on-a-monoalphabetic-substitution-cipher/
    TA intro video on Canvas


The structure/format of this README was adapted from the CMPUT 301 Labs README.md template and sample README template on CMPUT 331 Canvas Page.

## Manual Decryption Process
    1. Initial Mapping
        Used my code from a5p1.py and a5p3.py to map the cipher's letter counts to standard English frequencies (ETAOIN). This established a statistical baseline, though the output was largely inaccurate due to the short length of the ciphertext.

    2. Identifying Key Letters
        Matched the top two highest-frequency cipher letters to 'E' and 'T'. Located the single-letter words in the text to lock in 'A' and 'I'. Identified the most frequent 3-letter word to map the characters for "THE".

    3. Iterative Refinement
        Used context clues from the partially formed words to deduce the remaining characters (e.g., mapping letters to complete words like "NATURE" and "BOOK"). Updated the dictionary mapping iteratively and ran it through the freqDecrypt function until the exact plaintext was fully resolved.


## Verbal Collaboration
N/A 

## AI Use Declaration
Google Gemini was used to generate test cases for all problems and generating readme.txt.

## Prerequisites
Python 3.8.10 (Standard LIbrary only)

## Usage
Run any problem script from the root directory, for example:
    python3 a5p1.py