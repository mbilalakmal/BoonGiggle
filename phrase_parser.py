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
# -----------------------------------------------------------

import filing
import token_normalizer


def _query_to_terms(query):
    '''
    Convert `query` to list of terms.
    '''
    tokens = query.split()
    terms = token_normalizer.normalize_tokens(tokens)

    return terms


def _evaluate_phrase_query(terms, inverted_index):
    '''
    Return a set containing relevant doc_ids.
    '''
    # if one of the terms is not indexed return an empty set.
    if not set.issubset(
        set(terms),
        set(inverted_index.keys())
    ):
        return set()

    # a list of sets where each set is documents containing one of the terms.
    seperate_documents = [set(inverted_index[term].keys()) for term in terms]
    # a single set of documents that contain all the terms
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

    terms = _query_to_terms(query)

    result = _evaluate_phrase_query(terms, inverted_index)

    if len(result) == 0:
        return None
    else:
        documents = [doc_ids[doc_id] for doc_id in result]
        return (result, documents)


if __name__ == '__main__':
    
    # Ask for phrase query
    query = input('Enter a phrase query: ')

    result = retreive_documents(query)

    if result == None:
        print('No relevant speeches.')
    else:
        print(result)
