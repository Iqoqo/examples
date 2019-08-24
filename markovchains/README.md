# markovchains

This example is a simple NLP experiment for generating text that is almost intelligible,
still mostly nonsense, and in a style based on the input text.

There are more advanced methods for generating text in a given style, but this toy
example is very simple.

- Parse an input file containing a number of sentences.
- Using these sentences, build a dictionary mapping n-grams to next word frequency distributions.
Here we are using n=2 for bigrams.
- Using this frequency distribution map, generate new sentences.

## Data

The data is taken from [State of the Union Addresses made available from UCSB](https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union).

Each file contains the addresses of a single president.  Blank lines are ignored,
as are comments (starting with #) which are used to provide url sources.

Each file is included as an input in the DISCO platform.

## Technical notes

While the NLTK module is included in the default environment (at the moment at least),
the data for sentence and word parsers is not. In order to get this data downloaded,
we had to do a few workarounds to get NLTK to read and write from a location the process
had read/write access to.
