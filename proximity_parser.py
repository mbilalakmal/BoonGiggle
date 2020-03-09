# -----------------------------------------------------------
# This module parses a binary proximity query.
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

    proximity = int(terms[-1][-1]) + 1
    print(proximity)

    return (terms[0], terms[1], proximity)


def is_proximity_in_doc(doc, term1, term2, proximity, inverted_index):

    for position1 in inverted_index[term1][doc]:
        for position2 in inverted_index[term2][doc]:
            if abs(position2 - position1) == proximity:
                return True
    return False


def evaluate_proximity_query(term1, term2, proximity, inverted_index):
    
    result = set()

    doc_ids1 = set(inverted_index[term1].keys())
    doc_ids2 = set(inverted_index[term2].keys())

    for doc_id in doc_ids1:
        if doc_id not in doc_ids2:
            continue

        if is_proximity_in_doc(
            doc_id, term1, term2, proximity, inverted_index
            ):
            result.add(doc_id)
        
    return result

if __name__ == '__main__':
    
    #  Load Inverted Index and Doc IDs
    filename = r'resources\inverted_index'
    inverted_index = load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = load_python_object(filename)

    # Ask for proximity query
    query = input('Enter a proximity query: ')

    # Convert to proximity terms
    term1, term2, proximity = query_to_terms(query)

    # Evaluate proximity query
    result = evaluate_proximity_query(term1, term2, proximity, inverted_index)

    if len(result) == 0:
        print('No relevant speeches.')
    else:
        print(result)
        documents = [doc_ids[doc_id] for doc_id in result]
        print(documents)
        print(len(result))