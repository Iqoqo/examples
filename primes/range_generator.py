#!/usr/bin/env python

"""An auxiliary script that generates ranges (pairs of numbers) to be used as input to 'prime_finder.py'.
The generated files will be saved into the 'data' directory.

NOTE: This script should not be run as a job.
"""
from random import randint
import os

OUTPUT_DIRECTORY = "data"
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

for i in range(1, 100):
    start = randint(1, 10000000)
    end = start + randint(1000, 1000000)
    file = open(OUTPUT_DIRECTORY + "/range" + str(i) + ".txt", "w")
    file.write(str(start) + " " + str(end))
