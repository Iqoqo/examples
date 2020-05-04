#!/usr/bin/env python

"""Finds all primary numbers within a specified range.

The range will be given as a pair of numbers separated with a single space (' '),
written on the first line of a file passed in the argument.

For example, if the file 'data/range0.txt' contains '6072173 6756677' on the first line, type 'python prime_finder.py data/range0.txt' to run the script.

The script prints every prime it finds to the standard output stream, as well as to 'output.txt' file.
"""
import sys
from math import sqrt
from itertools import count, islice

outputfile = open("output.txt", "w")

def isPrime(n):
    return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

with open(sys.argv[1], 'r') as file:
    line = file.readline()
    splitted = line.split(' ')
    startRange = int(splitted[0])
    endRange = int(splitted[1])

    print(f"Data file: {sys.argv[1]}\n")
    print(f"Primes between {startRange} to {endRange}:\n")
    outputfile.write(f"Data file: {sys.argv[1]}\n")
    outputfile.write(f"Primes between {startRange} to {endRange}:\n")

    for i in range(startRange, endRange):
        if isPrime(i):
            outputfile.write(str(i) + " is a prime!\n")
            print(str(i) + " is a prime!\n")
