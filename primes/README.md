# primes

This script finds all prime numbers within a specified range.

## Data

Input for this script is a file that has two numbers on its first line &mdash; a lower and upper boundary.

Some pre-generated range files can be found under the `data` sub-directory. 
We also supply an offline script that helps you generate 100 random ranges. Note that it will overwrite the files already in `data`.

```
$ python range_generator.py
```

Please note that the generator is not intended to run as an DISCO job.

## Output

The scripts generates 'output.txt' file that lists all the primes found in a given range. 
The same information is also written to `stdout`.