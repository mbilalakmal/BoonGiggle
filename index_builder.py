# -----------------------------------------------------------
# This module creates an inverted index from the documents.
#
# The steps performed are summarized below:
# (1) Read all the documents.
# (2) Store Document IDs against their file names.
# (3) Create tokens from each document.
# (4) Preprocess (case-fold and stem) tokens.
# (5) Store each term along with document ID and position.
# (6) Store the inverted index dictionary as a binary file.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# email k173669@nu.edu.pk
# -----------------------------------------------------------

import pickle           # dump  | storing to file
import re               # split | tokenizing of documents' body
from glob import glob   # glob  | discover names of all txt files
from nltk import PorterStemmer  # stem  | stemming of tokens


def read_txt_files(pathname, encoding = 'utf=8'):
    '''
    Return txt documents discovered in `pathname`.
    '''
    documents   = {}    # numeric ID mapped to document body
    doc_ids     = {}    # numeric ID mapped to file name

    # discover txt files in pathname
    # and load into documents dictionary
    for file_name in glob(pathname):

        #get numeric ID from file name
        doc_id = re.search(r'\d+', file_name).group(0)
        doc_ids[doc_id] = file_name

        with open(file_name, 'r', encoding=encoding) as txt_file:
            _ = txt_file.readline()     #discard title
            document = txt_file.read()
            documents[doc_id] = document

    return (doc_ids, documents)


def read_stop_words(filename):
    '''
    Return stop words present in `filename`.
    '''
    with open(filename, 'r') as txt_file:
        stop_words = set( txt_file.read().split() )
    return stop_words


def sanitize_tokens(tokens):
    '''
    Return case-folded and stemmed `tokens`.
    '''
    folded_tokens = [token.lower() for token in tokens]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in folded_tokens]

    return stemmed_tokens


def build_positional_index(documents, stop_words):
    '''
    Build a positional index by extracting terms from `documents`.

    `stop_words` are excluded from indexing.
    '''
    inverted_index = {} # terms mapped to posting lists

    for item in documents.items():

        doc_id, document = item
        pattern = r'\W+'
        tokens = re.split(pattern, document)
        sanitized_tokens = sanitize_tokens(tokens)

        for position, term in enumerate(sanitized_tokens):

            if term in stop_words:
                continue    #skip stop words

            # create term dict
            if term not in inverted_index.keys():
                inverted_index[term] = {}

            # create doc_id set inside term dict
            if doc_id not in inverted_index[term].keys():
                inverted_index[term][doc_id] = set()

            inverted_index[term][doc_id].add(position)

    return inverted_index


def store_python_object(python_object, filename):
    '''
    Store `python_object` in `filename`.

    If `filename` exists, it will be overwritten.
    '''
    with open(filename, 'wb') as bin_file:
        pickle.dump(python_object, bin_file)


def generate_index():
    
    pathname = r'resources\corpus\*.txt'
    doc_ids, documents = read_txt_files(pathname)

    filename = r'resources\doc_ids'
    store_python_object(doc_ids, filename)

    filename = r'resources\stopwords.txt'
    stop_words = read_stop_words(filename)

    inverted_index = build_positional_index(documents, stop_words)

    filename = r'resources\inverted_index'
    store_python_object(inverted_index, filename)


if __name__ == '__main__':

    # Read all the documents
    pathname = r'resources\corpus\*.txt'
    doc_ids, documents = read_txt_files(pathname)

    # Store doc_ids
    filename = r'resources\doc_ids'
    store_python_object(doc_ids, filename)

    #Read the stop words
    filename = r'resources\stopwords.txt'
    stop_words = read_stop_words(filename)

    # Create the inverted index
    inverted_index = build_positional_index(documents, stop_words)

    # Store the inverted index
    filename = r'resources\inverted_index'
    store_python_object(inverted_index, filename)