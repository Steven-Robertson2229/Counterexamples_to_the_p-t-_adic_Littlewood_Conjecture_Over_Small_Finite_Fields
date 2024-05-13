# Collab_Number_Wall
This project is looking to investigate generating Number Walls primarily using
the Paper Folding sequence and Adapted Paper Folding sequence, looking to find a complete set of tiling for mod 7 and mod 11 (for Paper Folding), and mod 5 (for Adapted Paper Folding).

## Quickstart Testing
TODO

## Expected Outputs
Below is a list of the expected outputs from core functions for common/expected
input parameters. This will allow you to quickly verify that the code has run correctly,
which is useful when altering functionality or improving computational complexity.

For an exact image of the output for any fully computed prime inputs, please see the
`Results-Images` directory in this repository.

All input and time to process values are based on our V3.0 functions.

### Tiling Function
Input:
- prime_input=3
- sequence=paper_folding_seq (pap_f)
- tile_length=8

Output= **211 unique tiles** after approx 200 slices, and **837 total tiles processed (out of 21735)**

Input:
- prime_input=3
- sequence=pagoda_seq (pagoda)
- tile_length=16

Output= **197 unique tiles** after approx 184 slices, and **779 total tiles processed (out of ??)**

Input:
- prime_input=5
- sequence=adapted_paper_folding_seq (pap_f5)
- tile_length=16

Output= **?? unique tiles** after approx ?? slices, and **?? total tiles processed (out of ??)**

Input:
- prime_input=7
- sequence=paper_folding_seq (pap_f)
- tile_length=8

Output= **302,835 unique tiles** after approx 15,000 slices (stabilising at 7500 slices)
and **1,211,333 total tiles processed (out of 112,147,775)**

Input:
- prime_input=11
- sequence=paper_folding_seq (pap_f)
- tile_length=8

Output= **7,864,003 unique tiles** after approx 184,200 slices (stabilising at 92,100 slices)
and **31,456,005 total tiles processed (out of ???)**

### Four Tuples Function
Input (*paper folding sequence*):
- list of unique tile mappings generated from **prime 3**

Output= **681 unique four-tuples**

Input (*pagoda sequence*):
- list of unique tile mappings generated from **prime 3**

Output= **573 unique four-tuples**

Input (*adapted paper folding sequence*):
- list of unique tile mappings generated from **prime 5**

Output= **?? unique four-tuples**

Input (*paper folding sequence*):
- list of unique tile mappings generated from **prime 7**

Output= **1,575,729 unique four-tuples**

Input (*paper folding sequence*):
- list of unique tile mappings generated from **prime 11**

Output= **42,736,009 unique four-tuples**

## External links
You can find several papers discussing the background to this work below:
- [link_text1](https://<add a link here>)
- [link_text2](https://<add another link here>)

