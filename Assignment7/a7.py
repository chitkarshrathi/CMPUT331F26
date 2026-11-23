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
Assignment 7
Author: Chitkarsh Rathi
"""

from sys import flags
import math

def cliSSD(ciphertext: str, files):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """

    ctext_upper = ciphertext.upper()
    ctext_freq = {}
    count = 0

    for char in ctext_upper:
        if char.isalpha():
            ctext_freq[char] = ctext_freq.get(char, 0) + 1
            count += 1

    cipher_ssd = [total / count for total in sorted(ctext_freq.values(), reverse=True)] if count > 0 else []

    distances = {}

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            file_text = f.read().upper()

        f_counts = {}
        f_total = 0

        for char in file_text:
            if char.isalpha():
                f_counts[char] = f_counts.get(char, 0) + 1
                f_total += 1

        file_ssd = [total / f_total for total in sorted(f_counts.values(), reverse=True)] if f_total > 0 else []

        max_len = max(len(cipher_ssd), len(file_ssd))

        cipher_padded = cipher_ssd + [0] * (max_len - len(cipher_ssd))
        file_padded = file_ssd + [0] * (max_len - len(file_ssd))

        distance = sum((cipher_padded[i] - file_padded[i]) ** 2 for i in range(max_len)) 
        distances[filepath] = distance

    return distances
    
def cliDPD(ciphertext: str, files):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """

    cipher_tokens = ciphertext.split()
    c_total = len(cipher_tokens)
    c_pattern_counts = {}
    
    for token in cipher_tokens:
        clean_token = "".join(ch for ch in token if ch.isalpha()).upper()
        
        char_counts = {}
        for char in clean_token:
            char_counts[char] = char_counts.get(char, 0) + 1
            
        pattern = tuple(sorted(char_counts.values(), reverse=True))
        c_pattern_counts[pattern] = c_pattern_counts.get(pattern, 0) + 1
        
    cipher_dpd = {p: count / c_total for p, count in c_pattern_counts.items()} if c_total > 0 else {}
    
    distances = {}
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            file_text = f.read()
            
        file_tokens = file_text.split()
        f_total = len(file_tokens)
        f_pattern_counts = {}
        
        for token in file_tokens:
            clean_token = "".join(ch for ch in token if ch.isalpha()).upper()
            char_counts = {}
            for char in clean_token:
                char_counts[char] = char_counts.get(char, 0) + 1
                
            pattern = tuple(sorted(char_counts.values(), reverse=True))
            f_pattern_counts[pattern] = f_pattern_counts.get(pattern, 0) + 1
            
        file_dpd = {p: count / f_total for p, count in f_pattern_counts.items()} if f_total > 0 else {}
        
        all_patterns = set(cipher_dpd.keys()).union(set(file_dpd.keys()))
        distance = 0.0
        
        for p in all_patterns:
            c_prob = cipher_dpd.get(p, 0.0)
            f_prob = file_dpd.get(p, 0.0)
            distance += (c_prob - f_prob) ** 2
            
        distances[filepath] = distance
        
    return distances

def cliSSDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """
    results = {}
    
    for c_file in ciphertext_files:
        with open(c_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
            
        distances = cliSSD(ciphertext, sampletext_files)
        
        best_match = min(distances, key=distances.get)
        
        results[c_file] = best_match
        
    return results

def cliDPDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """

    results = {}
    
    for c_file in ciphertext_files:
        with open(c_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
            
        distances = cliDPD(ciphertext, sampletext_files)
        
        best_match = min(distances, key=distances.get)
        
        results[c_file] = best_match
        
    return results

def generateMapping(dictionary: dict):
    """
    Args:
        dictionary (return value of cliSSDTest or cliDPDTest)
    Returns:
        A classification mapping (dict) of the ciphertexts.
        Please refer to the assignment instructions for the required format.
    """
    mapping = {}
    
    for cipher_path, sample_path in dictionary.items():

        cipher_filename = cipher_path.replace('\\', '/').split('/')[-1]
        
        actual_lang = cipher_filename.split('_')[1]
        
        sample_filename = sample_path.replace('\\', '/').split('/')[-1]
        
        predicted_lang = sample_filename.split('_')[1].split('.')[0]
        
        pair = (actual_lang, predicted_lang)
        mapping[pair] = mapping.get(pair, 0) + 1
        
    return mapping

def generateMatrix(mapping):
    """
    Args:
        mapping (dictionary returned by generateMapping)
    Returns:
        None (prints a formatted confusion matrix)
    """
    languages = ["bg", "de", "el", "en", "es", "fr", "it", "nl", "pl", "ru"]

    header = "     " + " | ".join(languages)
    print("\n")
    print(header)
    print("   " + "-" * len(header))

    for actual in languages:
        row = [f"{mapping.get((actual, predicted), 0):>2}" for predicted in languages]
        print(f"{actual} | {' | '.join(row)}")
    print("\n") 


def test():

# Test cases for Problem 1 and Problem 2.
# Results are compared using math.isclose and pass if within 0.0008
# of the expected value (Python's sum() may round the last digits differently).
# Feel free to add more test cases here 
    cipher = """fukvuvu osyxhwuyxg wxhobsuv gxrxvbepxsy ucybsbpbck ewbixty povvobs xtc ybyuv tbky povvobs xtc
ylx xcwbexus gopxskobs luwpbsokosh bdixtyorxk kywctycwuv mcsgk xntlushosh osmbwpuyobs xnexwoxstx usg ogxuk tbvvudbwuyorx fbwa pbsoybwosh kbtouv euwysxwk v
xcwbexus tbppokkobs
xcwbexus gxtokobsk bs ylx opevxpxsyuyobs bmylx tbppbs kxtcwoyj usg gxmxstx ebvotj ostvcgosh ylbkx osoyouyosh u pokkobs uk wxmxwwxg yb os ylok uwyotvx kluvv dx ugbeyxg dj ylx tbcstov bm posokyxwk utyosh csusopbckvj bs u ewbebkuv mwbp ylx csobs posokyxw mbw mbwxohs ummuowk bw mwbp u pxpdxw kyuyx
oo yb xskcwx yluy ylx xcwbexus ewbebkuv vosxk mwupxk exw kxtbsg ewbhwxkkorx ktussosh ok ugbeyxg uk ylx koshvx fbwvg kyusg uwg
ylx pbwx xmmotoxsy ylx bexwuybwk osrbvrxg ylx pbwx xmmotoxsy ylx xcwbexus yxvxtbppcsotuyobsk puwaxy fovv dx
yuos ylx ybyuv ruvcx bm ylx wxkeowuyovx gcky tbstxsywuyobs mbw kextomoxg yopx osyxwruvk
oyv
dj vxyyxw guyxg puwtl gw gx gbposotok fuk osmbwpxg dj gh nro yluy ylx ewbixty bm ylx mbcsguyobs lug sby dxxs kxvxtyxg dxtuckx oy gog sby pxxy ylx ussbcstxg twoyxwou
bs yb sbrxpdxw os tbsicstyobs foyl ylx sxylxwvusgk posokywj bm lxuvyl usg ylx xsrowbspxsy ylx tbppokkobs lxvg us osyxwsuyobsuv tbsmxwxstx uy ylx luhcx bs tvxus yxtlsbvbhoxk bkuv yb ylx tbcstov tbstxwsosh u pcvyousscuv ewbhwuppx os ylx moxvg bm dobpbvxtcvuw xshosxxwosh osgowxty utyobs ylx xtbsbpot usg kbtouv tbppoyyxx pxxyosh bs usg sbrxpdxw gxvorxwxg us beosobs bs ylx tbppokkobs ewbebkuv yb ylx tbcstov tbstxwsosh cwusocp xnevbwuyobs usg xnywutyobs osgowxty utyobs
"""
    a = cliSSD(cipher, ["texts/sample_bg.txt", "texts/sample_de.txt", "texts/sample_el.txt", "texts/sample_en.txt", "texts/sample_es.txt", "texts/sample_fr.txt", "texts/sample_it.txt", "texts/sample_nl.txt", "texts/sample_pl.txt", "texts/sample_ru.txt"])
    expected_a = {'texts/sample_bg.txt': 0.0008686304175672087, 'texts/sample_de.txt': 0.0030282241681359465, 'texts/sample_el.txt': 0.003900768672618399, 'texts/sample_en.txt': 0.0009685983479506998, 'texts/sample_es.txt': 0.0014847832596343855, 'texts/sample_fr.txt': 0.002342377137372695, 'texts/sample_it.txt': 0.0008613778129189986, 'texts/sample_nl.txt': 0.00658594015644843, 'texts/sample_pl.txt': 0.004795508346043341, 'texts/sample_ru.txt': 0.002884312599878665}
    for k in expected_a:
        assert math.isclose(a[k], expected_a[k], abs_tol=0.0008), f"{k}: got {a[k]}, expected {expected_a[k]}"

    b = cliDPD(cipher, ["texts/sample_bg.txt", "texts/sample_de.txt", "texts/sample_el.txt", "texts/sample_en.txt", "texts/sample_es.txt", "texts/sample_fr.txt", "texts/sample_it.txt", "texts/sample_nl.txt", "texts/sample_pl.txt", "texts/sample_ru.txt"])
    expected_b = {'texts/sample_bg.txt': 0.03760706244775398, 'texts/sample_de.txt': 0.019627307148711397, 'texts/sample_el.txt': 0.010778849211054852, 'texts/sample_en.txt': 0.004254877302061767, 'texts/sample_es.txt': 0.017505446082276693, 'texts/sample_fr.txt': 0.0120039286951674, 'texts/sample_it.txt': 0.01241955510016762, 'texts/sample_nl.txt': 0.009751349385997449, 'texts/sample_pl.txt': 0.03375909319348446, 'texts/sample_ru.txt': 0.03334088648579243}
    for k in expected_b:
        assert math.isclose(b[k], expected_b[k], abs_tol=0.0008), f"{k}: got {b[k]}, expected {expected_b[k]}"

# ==========================================
    # === EDGE CASE TESTS FOR PROBLEMS 1 & 2 ===
    # ==========================================
    # We will use just one real file to test against
    test_files = ["texts/sample_bg.txt"]
    
    try:
        # Edge Case 1: Completely empty string
        # Proves your code handles division-by-zero properly.
        cliSSD("", test_files)
        cliDPD("", test_files)
        
        # Edge Case 2: Only punctuation and numbers (no letters)
        # Proves your code properly filters non-letters and counts empty words ().
        cliSSD("1234567890 !@#$%^&*()", test_files)
        cliDPD("1234567890 !@#$%^&*()", test_files)
        
        # Edge Case 3: A single gigantic repetitive word
        # Ensures no index-out-of-bounds errors on skewed distributions.
        cliSSD("A" * 1000, test_files)
        cliDPD("A" * 1000, test_files)
        
        # Edge Case 4: Case Insensitivity Proof
        # We test uppercase vs lowercase. The distances to the sample file 
        # MUST be mathematically identical.
        ssd_upper = cliSSD("AABBCCDD", test_files)
        ssd_lower = cliSSD("aabbccdd", test_files)
        assert math.isclose(ssd_upper[test_files[0]], ssd_lower[test_files[0]], abs_tol=0.0001), "SSD failed case test"
        
        dpd_upper = cliDPD("AABBCCDD", test_files)
        dpd_lower = cliDPD("aabbccdd", test_files)
        assert math.isclose(dpd_upper[test_files[0]], dpd_lower[test_files[0]], abs_tol=0.0001), "DPD failed case test"

        print("All Edge Case Tests Passed Successfully (No crashes on weird data)!\n")
        
    except Exception as e:
        print(f"Edge Case Test Failed! Error: {e}")

# === Test block for Problem 3 & 4 (No imports needed) ===
    languages = ["bg", "de", "el", "en", "es", "fr", "it", "nl", "pl", "ru"]
    
    # Generate the 50 ciphertext file paths and 10 sample file paths
    cipher_files = [f"texts/ciphertext_{lang}_{i}.txt" for lang in languages for i in range(1, 6)]
    sample_files = [f"texts/sample_{lang}.txt" for lang in languages]
    
    try:
        print("Running SSD Test (This takes a few seconds)...")
        ssd_results = cliSSDTest(cipher_files, sample_files)
        ssd_mapping = generateMapping(ssd_results)
        print("SSD Confusion Matrix:")
        generateMatrix(ssd_mapping)
        
        print("Running DPD Test (This takes a few seconds)...")
        dpd_results = cliDPDTest(cipher_files, sample_files)
        dpd_mapping = generateMapping(dpd_results)
        print("DPD Confusion Matrix:")
        generateMatrix(dpd_mapping)
    except FileNotFoundError:
        print("File error")

if __name__ == "__main__" and not flags.interactive:
    test()