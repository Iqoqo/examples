#!/usr/bin/env python

import sys

HEADER_FILE = "constant.txt"

"""Reads space-separated values from a file, row by row, 
and applies a conversion function to each. 
The conversion function must accept exactly one string parameter.
"""
def read_values(filename, conversion):
    with open(filename, 'r') as file_handle:
        lines = file_handle.readlines()
        return [[conversion(val) for val in line.split()] for line in lines]

with open(HEADER_FILE, "r") as constants_file_handler:
    const_data = constants_file_handler.read()
    print(const_data)

data_filename = sys.argv[1]

data = read_values(data_filename, float)

factor = -2 
power = 2 

for row in data:

    output = []
    for column in row:
        output.append((column * factor) ** power)

    print(output)
