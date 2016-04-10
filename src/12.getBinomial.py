import os
import sys
import csv
import scipy.stats

# This script finds the probability of obtaining n significant correlations by chance.

# The input parameters are:
# 	1) p = the hypothesised probability of one success, given the null hypothesis (e.g. 0.05)
#	2) n = no. of successes (significant p results < 0.05)


# The outputs are:
#   The binomial probability of n joint successes, given the null hypothesis.


# Initialization
successProb = float(raw_input("Significance level: "))
noSuccesses = raw_input("No. of significant p values at this level: ")			
noTrials = 132					# No. of non-training tasks. (12 speakers x 12 tasks) - 12 training tasks.


# Calculate and Output
print scipy.stats.binom_test(noSuccesses, noTrials, successProb)		# Two-tailed binomial test.

# (NB: This is not the cumulative probability)