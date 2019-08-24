# spellingbee

This script is a solver for the New York Times Spelling Bee.  The puzzle has one letter
in the center, surrounded by six other letters.  The object is to find as many words
as possible that fit the criteria:

- The word must contain the center letter at least once.
- The word can contain any number of the outer letters.
- Letters can be used more than once.
- Words must be at least five letters long.
- No proper nouns or hyphenated words.

## Data

Here we generate the data using the script `generate_data.py`.  This file is used to
generate data offline.  It is not run on the DISCO platform.

By default the program will create 10 files in the `data/` directory with 1000 puzzles
in each file.  To get the options available, use `--help`:

```
$ python generate_data.py --help
Create a data file to be used by the puzzle solver.

The format is a line for each puzzle, where each line is a comma separated list of letters.
The first letter in the list is assumed to be in the center, and all other letters surrounding the center.

Usage:
generate.py [--lines=<lines>] [--files=<files>] [--dirpath=<dirpath>]

Options:
  --lines=<lines>           Number of lines to generate. [default: 1000]
  --files=<files>           Number of files to generate. [default: 10]
  --dirpath=<dirpath>       Path of the data data directory to write. [default: ./data]

```

This uses the [docopt module](https://github.com/docopt/docopt) to generate options 
from doc strings.  It is not included in the standard modules, unfortunately, so it
will require a pip or conda install.

## Technical notes

This is a brute force solution, where we just iterate through every word in the
dictionary and perform a few tests.  It is likely that a more efficient approach
would be graph based, where we do a graph search through the available letters
(based on the puzzle) and terminate when there are no available words that start 
with these letters.  This would require our available words be parsed into a data 
structure that supports fast queries for words starting with some sequence.

This example is a "fast enough" approach.

TODO: The next refinement should be to find a better list of allowed words.  This could
be done by providing a constants file.
