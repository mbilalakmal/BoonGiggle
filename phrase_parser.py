# -----------------------------------------------------------
# This module parses a general phrase query.
#
# The steps performed are summarized below:
# (1) Load inverted_index from file
# (2) Prompt user for query and parse it
# (3) Perform boolean retreival to obtain relevant doc_ids
# (4) Display doc_ids to user
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# email k173669@nu.edu.pk
# -----------------------------------------------------------

import pickle
from nltk import PorterStemmer

def load_python_object(filename):
    with open(filename, 'rb') as object_file:
        python_object = pickle.load(object_file)
    return python_object


def query_to_terms(query):
    tokens = query.split()
    stemmer = PorterStemmer()
    terms = [stemmer.stem(token.lower()) for token in tokens]

    return terms

def evaluate_phrase_query(terms, inverted_index):
    seperate_documents = [set(inverted_index[term].keys()) for term in terms]
    common_documents = set.intersection(*seperate_documents)

    result = set()
    for document_id in common_documents:

        posting_lists = set()

        for index, term in enumerate(terms):
            term_positions = inverted_index[term][document_id]
            posting_list = set( [position-index for position in term_positions] )

            if index == 0:
                posting_lists.update(posting_list)
                continue
            if posting_lists.isdisjoint(posting_list):
                posting_lists.clear()
                break
            posting_lists.intersection_update(posting_list)

        if posting_lists:
            result.add(document_id)
        
    return result

if __name__ == '__main__':
    
    #  Load Inverted Index and Doc IDs
    filename = r'resources\inverted_index'
    inverted_index = load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = load_python_object(filename)

    # Ask for boolean query
    query = input('Enter a phrase query: ')

    # Convert to phrase terms
    terms = query_to_terms(query)

    # Evaluate phrase query
    result = evaluate_phrase_query(terms, inverted_index)

    if len(result) == 0:
        print('No relevant speeches.')
    else:
        print(result)
        documents = [doc_ids[doc_id] for doc_id in result]
        print(documents)
        print(len(result))