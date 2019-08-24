#!/usr/bin/env python

"""Simulates a long-running task by generating simple stdout output at a one-second interval, for 1000 seconds.
"""
import time

for i in range(1, 1000):
    print(str(i))
    time.sleep(1)
    
print("Done")
