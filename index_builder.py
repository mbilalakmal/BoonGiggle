# -----------------------------------------------------------
# This module performs indexing of the documents.
# The steps performed are summarized below:
# (1) Read each document
# (2) Create tokens from the document
# (3) Case-fold each token
# (4) Stem each token
# (5) Store the term along with document and
# position. Skipping over stop words.
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# email k173669@nu.edu.pk
# -----------------------------------------------------------

from glob import glob
import re
import json
from nltk import PorterStemmer
import time

print('Start')
a = time.time()

with open(r'resources\stopwords.txt', 'r') as txt_file:
    stop_words = set(txt_file.read().split())


documents = {}

for file_name in glob(r'resources\corpus\*.txt'):
    
    with open(file_name, 'r', encoding='utf-8') as txt_file:
        document = txt_file.read()
        documents[file_name] = document


inverted_index = {}

for doc_id in documents.keys():

    document = documents[doc_id]

    tokens = re.split(r'\W+', document)
    folded_tokens = [token.lower() for token in tokens]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in folded_tokens]

    for position, term in enumerate(stemmed_tokens):

        if term in stop_words:
            continue

        if term not in inverted_index.keys():
            inverted_index[term] = {}

        if doc_id not in inverted_index[term].keys():
            inverted_index[term][doc_id] = set()

        inverted_index[term][doc_id].add(position)
        # print(term, doc_id, position)
        # input()

# for term in inverted_index:
#     print(term, len(inverted_index[term]))
#     input()
print('End')
b = time.time()

print(f'Time: {b-a} seconds')

# store in json