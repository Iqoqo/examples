"""
Solve a Spelling Bee puzzle.


"""
from pathlib import Path
import requests
import sys


def get_allowed_words(to_lower=True):
    """Return a list of words to use as allowable words."""
    try:
        words = get_allowed_words_from_filesystem(to_lower=to_lower)
    except FileNotFoundError as e:
        print('Unable to find a dictionary on the file system.  Trying online dictionaries.')
        words = get_allowed_words_from_web(to_lower=to_lower)
    return words


def get_allowed_words_from_filesystem(to_lower=True):
    """Get a list of allowed words from the filesystem.

    If a word list cannot be found in the standard locations, raise `FileNotFoundError`.
    """
    filepaths = [
        Path('/usr/dict/words'),
        Path('/usr/share/dict/words'),
    ]
    word_filepath = None
    for filepath in filepaths:
        print('trying {}'.format(filepath))
        if filepath.exists():
            print('found word list: {}'.format(filepath))
            word_filepath = filepath
            break
    if word_filepath is None:
        raise FileNotFoundError('Unable to find a word list on this platform')
    with word_filepath.open(mode='r') as f:
        words = f.readlines()
    if to_lower is True:
        words = [word.strip().lower() for word in words]
    return words


def get_allowed_words_from_web(to_lower=True):
    """Get a list of allowed words from a url.

    """
    url = 'https://users.cs.duke.edu/~ola/ap/linuxwords'
    print('trying {}'.format(url))
    r = requests.get(url)
    words = r.content.decode('utf-8').split()
    if to_lower is True:
        words = [word.strip().lower() for word in words]
    return words


def get_matching_words(center_letter, other_letters, allowed_words, min_word_length=5):
    """Return a list of words from `allowed words` that fit the criteria.
        - Includes `center_letter` at least once.
        - Includes only letters from `other_letters` and `center_letter`.
        - Contains at least `min_word_length` letters.
    """
    words = []
    allowed_letters = set(center_letter).union(set(other_letters))
    for word in allowed_words:
        if len(word) < min_word_length:
            continue
        if center_letter not in word:
            continue
        if set(word).difference(allowed_letters):
            # the word contains letters other than the allowed letters
            continue
        words.append(word)
    return words


def main():
    data_file = Path(sys.argv[1])
    allowed_words = get_allowed_words()
    with data_file.open(mode='r') as f:
        for line in f.readlines():
            letters = line.strip().split(',')
            center_letter = letters[0]
            other_letters = letters[1:]
            matching_words = get_matching_words(center_letter, other_letters, allowed_words=allowed_words)
            print(center_letter, other_letters, len(matching_words), matching_words)


if __name__ == '__main__':
    main()

