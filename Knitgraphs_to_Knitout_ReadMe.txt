Submission for HW2: KnitGraphs to Knitout

Method documentation can be found as in-line comments.

Knitout output files produced by my implementations can be found in the my_results\knitout directory.

I added a main method to test_knitgraph_to_knitout.py to run the tests. I additionally changed the default yarn carrier
for the stockinette method from 4 to 3 in order to match the test outputs. Running each test in
test_knitgraph_to_knitout.py individually produces the expected knitout file, which was checked against the provided
test knitout files using a diffchecker. The only difference is a trivial knitout comment diff in test_twists.k. The
actual knitout instructions match exactly.