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
# -----------------------------------------------------------

import re

import filing
import token_normalizer


def _build_positional_index(documents, stop_words):
    '''
    Build a positional index by extracting terms from `documents`.

    `stop_words` are excluded from indexing.
    '''
    inverted_index = {} # terms mapped to posting lists

    for item in documents.items():

        doc_id, document = item
        pattern = r'\W+'
        tokens = re.split(pattern, document)
        sanitized_tokens = token_normalizer.normalize_tokens(tokens)

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


def generate_index_file():
    '''
    Create index file from the corpus.
    '''
    # Read all the document files
    pathname = r'resources\corpus\*.txt'
    doc_ids, documents = filing.read_docs_files(pathname)

    # Store doc_ids->filename dictionary
    filename = r'resources\doc_ids'
    filing.store_python_object(doc_ids, filename)

    # Read the stop words
    filename = r'resources\stopwords.txt'
    stop_words = filing.read_stop_words(filename)

    # Create the inverted index
    inverted_index = _build_positional_index(documents, stop_words)

    # Store the inverted index
    filename = r'resources\inverted_index'
    filing.store_python_object(inverted_index, filename)


if __name__ == '__main__':
    generate_index_file()