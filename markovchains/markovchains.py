"""
Parse a corpus as example text then create new sentences using a Markov n-gram model.
"""
from collections import defaultdict
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.probability import MLEProbDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
import os
from pathlib import Path
import sys

NLTK_DATA_DIR = '/tmp/nltk_data/'
TOKEN_EOL = '<EOL>'


def get_args():
    """
    Return input filepath.

    These are retrieved from the command line in the order expected by the DISCO platform.
    If not provided, the value will be None.
    """
    try:
        input_filepath = Path(sys.argv[1])
    except IndexError:
        input_filepath = None

    return input_filepath


def get_sentences(input_filepath):
    if input_filepath is None:
        input_filepath = Path('data/sotu_george_washington.txt')
    sentences = []
    with input_filepath.open(mode='r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                # ignore blank lines
                continue
            if line.startswith('#'):
                # ignore comments
                continue
            for s in sent_tokenize(line):
                sentences.append(s)
    return sentences


def get_ngram_frequency_distribution_map(input_filepath, ngram_length=1):
    print('Creating word frequency distribution map from {}'.format(input_filepath))
    sentences = get_sentences(input_filepath)
    ngram_freq_dist = defaultdict(nltk.FreqDist)
    for sentence in sentences:
        previous_words = [None] * ngram_length
        for token in word_tokenize(sentence):
            token = token.lower()
            ngram_freq_dist[tuple(previous_words)][token] += 1
            # add the new word to the end and remove the word at the front
            previous_words.append(token)
            previous_words.pop(0)
        ngram_freq_dist[tuple(previous_words)][TOKEN_EOL] += 1
    return ngram_freq_dist


def get_probability_distribution_map(frequency_distribution_map):
    prob_dist_map = {}
    for pos, freq_dist in frequency_distribution_map.items():
        prob_dist_map[pos] = MLEProbDist(freq_dist)
    return prob_dist_map


def get_generated_sentence(ngram_freq_dist_map, probability_distribution_map):
    ngram_length = len(list(ngram_freq_dist_map.keys())[0])
    token_list = [None] * ngram_length
    token = None
    selected_tokens = []
    while token != TOKEN_EOL:
        # token = ngram_freq_dist_map[ngram]
        token = probability_distribution_map[tuple(token_list)].generate()
        selected_tokens.append(token)
        # add the selected token to the end and remove the token at the front
        token_list.append(token)
        token_list.pop(0)
    # remove the final EOL
    selected_tokens.pop()
    d = TreebankWordDetokenizer()
    s = d.detokenize(selected_tokens)
    return s

def get_generated_sentences(ngram_freq_dist_map, n_sentences=10):
    probability_distribution_map = get_probability_distribution_map(ngram_freq_dist_map)
    sentences = []
    for i in range(n_sentences):
        sentences.append(get_generated_sentence(ngram_freq_dist_map, probability_distribution_map))
    return sentences


def init():
    # set the NLTK data directory to a writable location - does this do anything?
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    # give NLTK another hint
    nltk.data.path.append(NLTK_DATA_DIR)
    # download necessary packages
    nltk.download('punkt', download_dir=NLTK_DATA_DIR)


def main():
    input_filepath = get_args()
    init()
    ngram_length = 2
    n_sentences = 20
    ngram_freq_dist_map = get_ngram_frequency_distribution_map(input_filepath, ngram_length=ngram_length)
    # for token_list, freq_dist in ngram_freq_dist_map.items():
    #     print('ngram:', token_list)
    #     print(freq_dist.tabulate())
    sentences = get_generated_sentences(ngram_freq_dist_map, n_sentences=n_sentences)
    for sentence in sentences:
        print(sentence)


if __name__ == '__main__':
    main()
