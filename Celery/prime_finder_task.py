from celery import Celery
from math import sqrt
from itertools import count, islice

"""
This module holds the Celery task
The task accepts two numbers and finds all the primes numbers between the two numbers
"""

# Defining the celery app, using RabbitMQ as the message broker and RPC as backend for getting the results
app = Celery('prime_finder_task', backend='rpc://', broker='amqp://guest:guest@localhost//')


# A function for checking if a number is prime
def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))


# Defining this function as a celery task
@app.task
def find_primes(start_range, end_range):
    return [n for n in range(start_range, end_range) if is_prime(n)]
