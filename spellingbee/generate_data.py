"""
Create a data file to be used by the puzzle solver.

The format is a line for each puzzle, where each line is a comma separated list of letters.
The first letter in the list is assumed to be in the center, and all other letters surrounding the center.

Usage:
generate.py [--lines=<lines>] [--files=<files>] [--dirpath=<dirpath>]

Options:
  --lines=<lines>           Number of lines to generate. [default: 1000]
  --files=<files>           Number of files to generate. [default: 10]
  --dirpath=<dirpath>       Path of the data data directory to write. [default: ./data]
"""
from docopt import docopt
import numpy as np
from pathlib import Path
import string


def get_letter_weights():
    """Return an `np.array` with the frequencies of the letters a-z.

    Source: https://gist.github.com/evilpacket/5973230
    """
    # Assume ordered dictionary as the default since Python 3.6
    letter_dct = {
        "a": 8.167,
        "b": 1.492,
        "c": 2.782,
        "d": 4.253,
        "e": 12.702,
        "f": 2.228,
        "g": 2.015,
        "h": 6.094,
        "i": 6.966,
        "j": 0.153,
        "k": 0.772,
        "l": 4.025,
        "m": 2.406,
        "n": 6.749,
        "o": 7.507,
        "p": 1.929,
        "q": 0.095,
        "r": 5.987,
        "s": 6.327,
        "t": 9.056,
        "u": 2.758,
        "v": 0.978,
        "w": 2.360,
        "x": 0.150,
        "y": 1.974,
        "z": 0.074,
    }
    values = np.array(list(letter_dct.values()))
    return values / values.sum()


def generate_datafile(output_filepath, n_lines, letters=None, weights=None):
    print('generating {}'.format(output_filepath))
    if letters is None:
        letters = list(string.ascii_lowercase)
    with output_filepath.open(mode='w') as f:
        for i in range(n_lines):
            s = np.random.choice(letters, size=7, replace=False, p=weights)
            # print(','.join(s))
            f.write(','.join(s) + '\n')


def main():
    arguments = docopt(__doc__)
    dirpath = Path(arguments['--dirpath'])
    n_lines = int(arguments['--lines'])
    n_files = int(arguments['--files'])
    letters = list(string.ascii_lowercase)
    weights = get_letter_weights()
    # print({l: w for l, w in zip(letters, weights)})
    dirpath.mkdir(exist_ok=True)
    for i in range(n_files):
        output_filepath = dirpath / 'data-{idx:0>4}.csv'.format(idx=i)
        generate_datafile(output_filepath, n_lines, letters, weights)


if __name__ == '__main__':
    main()
