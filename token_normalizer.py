# -----------------------------------------------------------
# This module performs text normalization.
# Currently it applies case-folding and stemming (Porter)
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

from nltk import PorterStemmer


def normalize_tokens(tokens):
    '''
    Return case-folded and stemmed `tokens`.

    Normalization and Lemmatization can be added.
    '''
    folded_tokens = [token.lower() for token in tokens]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in folded_tokens]

    return stemmed_tokens
