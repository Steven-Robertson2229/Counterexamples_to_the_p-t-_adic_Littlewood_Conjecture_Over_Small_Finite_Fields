# Main_Code.py:
This code is used to prove Theorems 1.5 and 1.9 from the paper _Counterexamples to the p(t)-adic Littlewood Conjecture Over Small Finite Fields_. The code runs on Python 3.7.9. When using the code, make sure the file TileObject.py is in the same folder as Main_Code.py. The code is currently set up to run Algorithms 1.1, 1.2, 2.1, and 2.2 over F3 using the First-Level Paperfolding Sequence. This should take under a second to run, returning the information found in Section 4.1 of the paper. 

To change the finite field, replace prime=3 two lines above "def main(step):" to your chosen prime. For prime=3,7 and 11, you can now run the code. If you want to run the code over F5, you will neeed to also change "TO.Tile.tile_length=8" to be "TO.Tile.tile_length=16" and "input_generator(paperfolding(1,10000), write_output)" to be "input_generator(adapted_paperfolding(1,10000), write_output)".

# Save_and_Quit.py
Proof of Theorem 1.5 and the F11 case of Theorem 1.9 required the use of a super computer, as large amounts of RAM were required. We had the constraint that the supercomputer would kill any code running longer than a week. Therefore, a version of Main_Code was written that saved its progress to a txt file after 6 days. It can then be run again, recreating its progress by reading the txt files. The instructions for use are provided as comments in the file. If the user does not have this time constraint, then this version of the code is not needed. 

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

