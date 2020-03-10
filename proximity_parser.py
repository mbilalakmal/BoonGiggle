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
# -----------------------------------------------------------

import re

import filing
import token_normalizer


def _query_to_terms(query):
    '''
    Convert `query` to terms.

    Returns the terms and the proximity as a tuple.
    '''
    tokens = query.split()
    terms = token_normalizer.normalize_tokens(tokens)

    proximity = int(re.search(r'\d+', query).group(0)) + 1
    return (terms[0], terms[1], proximity)


def _is_proximity_in_doc(doc, term1, term2, proximity, inverted_index):
    '''
    Return `True` if two terms are `proximity` words apart in `doc`.

    `False` otherwise.
    '''
    for position1 in inverted_index[term1][doc]:
        for position2 in inverted_index[term2][doc]:
            if abs(position2 - position1) == proximity:
                return True
    return False


def _evaluate_proximity_query(term1, term2, proximity, inverted_index):
    '''
    Return a set containing relevant doc_ids.
    '''
    # if one of the terms is not indexed return an empty set.
    if not set.issubset(
        set([term1, term2]),
        set(inverted_index.keys())
    ):
        return set()

    result = set()
    doc_ids1 = set(inverted_index[term1].keys())
    doc_ids2 = set(inverted_index[term2].keys())

    for doc_id in doc_ids1:
        if doc_id not in doc_ids2:
            continue

        if _is_proximity_in_doc(
            doc_id, term1, term2, proximity, inverted_index
            ):
            result.add(doc_id)
        
    return result


def retreive_documents(query):
    '''
    Retreive documents relevant to the proximity `query`.

    Returns a tuple of sets containing doc_ids and filenames.
    `None` if no relevant documents are found.
    '''
    filename = r'resources\inverted_index'
    inverted_index = filing.load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = filing.load_python_object(filename)

    term1, term2, proximity = _query_to_terms(query)

    result = _evaluate_proximity_query(term1, term2, proximity, inverted_index)

    if len(result) == 0:
        return None
    else:
        documents = [doc_ids[doc_id] for doc_id in result]
        return (result, documents)


if __name__ == '__main__':
    
    # Ask for proximity query
    query = input('Enter a proximity query: ')

    result = retreive_documents(query)

    if result == None:
        print('No relevant speeches.')
    else:
        print(result)
