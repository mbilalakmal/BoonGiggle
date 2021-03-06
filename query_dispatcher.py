# -----------------------------------------------------------
# This module determines the type of query and dispatches
# the appropriate parser.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import re

import boolean_parser
import phrase_parser
import proximity_parser


def dispatch_query(query):
    '''
    Determine the type of query and call the parser.

    Uses regular expressions to detect boolean and proximity queries.
    '''
    bool_regex = r'AND|OR|NOT'
    prox_regex = r'/\d+'

    if re.search(bool_regex, query) != None:
        return boolean_parser.retreive_documents(query)

    if re.search(prox_regex, query) != None:
        return proximity_parser.retreive_documents(query)

    return phrase_parser.retreive_documents(query)


if __name__ == '__main__':

    # Ask for query
    query = input('Enter a query: ')
    result = dispatch_query(query)

    if result == None:
        print('No relevant speeches.')
    else:
        print(result)
