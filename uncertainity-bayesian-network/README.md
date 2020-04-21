# Bayesian Network - Uncertainity

Implemented Variable Elimination for Bayes Net.

## Tests Results

Test 1 ....passed.
P(s|g) = 1.0 P(-s|g) = 0.0
Test 2 ....passed.
P(w|b,-e) = 0.68 P(-w|b,-e) = 0.32
Test 3 ....passed.
P(g|s) = 0.5 P(-g|s) = 0.5 P(g|-s) = 0.0 P(-g|-s) = 1.0
Test 4 ....passed.
P(g|s,w) = 0.5 P(-g|s,w) = 0.5 P(g|s,-w) = 0.5 P(-g|s,-w) = 0.5
Test 5 ....passed.
P(g|-s,w) = 0.0 P(-g|-s,w) = 1.0 P(g|-s,-w) = 0.0 P(-g|-s,-w) = 1.0
Test 6 ....passed.
P(g|w) = 0.15265998457979954 P(-g|w) = 0.8473400154202004 P(g|-w) = 0.01336753983256819 P(-g|-w) = 0.9866324601674318
Test 7 ....passed.
P(g) = 0.04950000000000001 P(-g) = 0.9505
Test 8 ....passed.
P(e) = 0.1 P(-e) = 0.9