# -----------------------------------------------------------
# This module creates an inverted index from the documents.
#
# The steps performed are summarized below:
# (1) Read all the documents
# (2) Create tokens from each document
# (3) Preprocess (case-fold and stem) tokens
# (4) Store each term along with document ID and position
# (5) Store the inverted index dictionary as a binary file
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# email k173669@nu.edu.pk
# -----------------------------------------------------------

import pickle           # dump and load | filing
import re               # split | tokenizing
import time             # time | timing the whole preprocessing
from glob import glob   # | file names of all txt files

from nltk import PorterStemmer  # stem | stemming

# with open(r'resources\inverted_index', 'rb') as index_file:
#     inverted_index_2 = pickle.load(index_file)


def read_txt_files(pathname, encoding = 'utf=8'):
    '''
    Return txt documents discovered in `pathname`.
    '''
    documents = {}  # key = filename, value = document

    # discover txt files in pathname
    # and load into documents dictionary
    for file_name in glob(pathname):
        with open(file_name, 'r', encoding=encoding) as txt_file:
            document = txt_file.read()
            documents[file_name] = document

    return documents


def read_stop_words(filename):
    '''
    Return stop words present in `filename`.
    '''
    with open(filename, 'r') as txt_file:
        stop_words = set(txt_file.read().split())
    return stop_words


def sanitize_tokens(tokens):
    '''
    Return case-folded and stemmed `tokens`.
    '''
    # case-fold tokens
    folded_tokens = [token.lower() for token in tokens]

    # stem tokens
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in folded_tokens]

    return stemmed_tokens


def build_positional_index(documents, stop_words):
    '''
    Build a positional index by extracting terms from `documents`.

    `stop_words` are excluded from indexing.
    '''
    inverted_index = {} #[term][doc_id] = set(pos1, pos2)

    for item in documents.items():

        doc_id, document = item
        pattern = r'\W+'
        tokens = re.split(pattern, document)
        sanitized_tokens = sanitize_tokens(tokens)

        for position, term in enumerate(sanitized_tokens):

            if term in stop_words:  # skip stop words
                continue

            # create term dict
            if term not in inverted_index.keys():
                inverted_index[term] = {}

            # create doc_id set inside term dict
            if doc_id not in inverted_index[term].keys():
                inverted_index[term][doc_id] = set()

            inverted_index[term][doc_id].add(position)

    return inverted_index


def store_inverted_index(inverted_index, filename):
    '''
    Store `inverted_index` Python object in `filename`.

    If `filename` exists, it will be overwritten.
    '''
    with open(filename, 'wb') as index_file:
        pickle.dump(inverted_index, index_file)


if __name__ == '__main__':

    # Read all the documents
    pathname = r'resources\corpus\*.txt'
    documents = read_txt_files(pathname)

    #Read the stop words
    filename = r'resources\stopwords.txt'
    stop_words = read_stop_words(filename)

    # Create the inverted index
    inverted_index = build_positional_index(documents, stop_words)

    # Store the inverted index
    filename = r'resources\inverted_index'
    store_inverted_index(inverted_index, filename)
