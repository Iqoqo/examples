from celery import Celery, group
from prime_finder_task import find_primes

"""
This is the main method and should be run as script

This script demonstrates the use of group and task signature

The task is defined in prime_finder_task.py
"""


def find_primes_in_range(start, end):
    step = 100000
    # Creating ranges to run on
    ranges = [(n, min(n + step, end)) for n in range(start, end, step)]
    # Generate task signatures for the above ranges
    tasks = [find_primes.s(r[0], r[1]) for r in ranges]
    # Create a group of all the tasks to be run in parallel
    job = group(tasks)
    # Run the group
    results = job.apply_async()
    return results.get(timeout=100)


if __name__ == "__main__":
    results = find_primes_in_range(0, 1000000)
    print(results)
