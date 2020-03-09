# -----------------------------------------------------------
# This module parses a boolean query.
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
import re
import string
from collections import deque
from nltk import PorterStemmer

def load_python_object(filename):
    with open(filename, 'rb') as object_file:
        python_object = pickle.load(object_file)
    return python_object


def query_to_infix(query):

    expression = (
        query
        .replace('(', ' ( ')
        .replace(')', ' ) ')
        .replace('AND', ' * ')
        .replace('OR', ' + ')
        .replace('NOT', ' ~ ')
    )

    # tokenize -> list
    infix = expression.split()

    stemmer = PorterStemmer()
    infix = [ stemmer.stem(token.lower()) for token in infix ]

    return infix


def infix_to_postfix(infix):

    stack = deque()
    postfix = []

    for token in infix:
        if token == '(':
            stack.append(token)

        elif token == ')':
            while True:
                if not stack:
                    # wrong infix
                    print('WRONG EQUATION FOOL')
                    return None
                if stack[-1] == '(':
                    stack.pop()
                    break
                postfix.append( stack.pop() )
        
        elif token in ['*', '+', '~']:
            stack.append(token) #precedence not implemented
        else:
            postfix.append(token)   #operand

    stack.reverse()
    postfix.extend(stack)   #empty the stack

    return postfix


def evaluate_postfix(postfix, inverted_index, doc_ids):

    # check if expression contains a single term only
    if len(postfix) == 1:
        docs = set(inverted_index[postfix[0]].keys())
        return docs

    stack = deque()

    for symbol in postfix:
        if symbol not in ['*', '+', '~', '%']:
            stack.append(symbol)
        elif symbol == '*':
            intersection(stack, inverted_index)
        elif symbol == '+':
            union(stack, inverted_index)
        elif symbol == '~':
            negation(stack, inverted_index, doc_ids)
    
    return stack[0]


def intersection(stack, inverted_index):
    operand1 = stack.pop()
    operand2 = stack.pop()

    if type(operand1) is str:
        if operand1 in inverted_index:
            operand1 = set(inverted_index[operand1].keys())
        else:
            operand1 = set()

    if type(operand2) is str:
        if operand2 in inverted_index:
            operand2 = set(inverted_index[operand2].keys())
        else:
            operand2 = set()

    result = set.intersection(operand1, operand2)
    stack.append(result)


def union(stack, inverted_index):
    operand1 = stack.pop()
    operand2 = stack.pop()

    if type(operand1) is str:
        if operand1 in inverted_index:
            operand1 = set(inverted_index[operand1].keys())
        else:
            operand1 = set()

    if type(operand2) is str:
        if operand2 in inverted_index:
            operand2 = set(inverted_index[operand2].keys())
        else:
            operand2 = set()

    result = set.union(operand1, operand2)
    stack.append(result)


def negation(stack, inverted_index, doc_ids):
    operand = stack.pop()

    if type(operand) is str:
        if operand in inverted_index:
            operand = set(inverted_index[operand].keys())
        else:
            operand = set()

    total = set(doc_ids.keys())
    result = set.difference(total, operand)
    stack.append(result)


def retreive_documents(query):
    
    filename = r'resources\inverted_index'
    inverted_index = load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = load_python_object(filename)

    infix = query_to_infix(query)

    postfix = infix_to_postfix(infix)

    # Evaluate postfix expression
    result = evaluate_postfix(postfix, inverted_index, doc_ids)

    if len(result) == 0:
        return None
    else:
        documents = [doc_ids[doc_id] for doc_id in result]
        return (result, documents)


if __name__ == '__main__':
    
    #  Load Inverted Index and Doc IDs
    filename = r'resources\inverted_index'
    inverted_index = load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = load_python_object(filename)

    # Ask for boolean query
    query = input('Enter a boolean query: ')

    # Convert to infix expression
    infix = query_to_infix(query)

    # Convert to postfix expression
    postfix = infix_to_postfix(infix)

    print(postfix)

    # Evaluate postfix expression
    result = evaluate_postfix(postfix, inverted_index, doc_ids)

    if len(result) == 0:
        print('No relevant speeches.')
    else:
        print(result)