#!/usr/bin/env python

"""This example illustrates passing a file as an argument. 
It echoes the file's content to stdout.
"""
import sys
import shutil


for path in sys.argv[1:]:
    print(path)
    with open(path, "r") as f:
        shutil.copyfileobj(f, sys.stdout)
        print
