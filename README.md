# Main_Code.py:
This code is used to prove Theorems 1.5 and 1.9 from the paper _Counterexamples to the p(t)-adic Littlewood Conjecture Over Small Finite Fields_. The code runs on Python 3.7.9. When using the code, make sure the file TileObject.py is in the same folder as Main_Code.py. The code is currently set up to run Algorithms 1.1, 1.2, 2.1, and 2.2 over F3 using the First-Level Paperfolding Sequence. This should take under a second to run, returning the information found in Section 4.1 of the paper. 

To change the finite field, replace prime=3 two lines above "def main(step):" to your chosen prime. For prime=3,7 and 11, you can now run the code. If you want to run the code over F5, you will neeed to also change "TO.Tile.tile_length=8" to be "TO.Tile.tile_length=16" and "input_generator(paperfolding(1,10000), write_output)" to be "input_generator(adapted_paperfolding(1,10000), write_output)".

# Save_and_Quit.py
Proof of Theorem 1.5 and the F11 case of Theorem 1.9 required the use of a super computer, as large amounts of RAM were required. We had the constraint that the supercomputer would kill any code running longer than a week. Therefore, a version of Main_Code was written that saved its progress to a txt file after 6 days. It can then be run again, recreating its progress by reading the txt files. The instructions for use are provided as comments in the file. If the user does not have this time constraint, then this version of the code is not needed. 


