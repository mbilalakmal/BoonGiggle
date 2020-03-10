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
# -----------------------------------------------------------

from collections import deque

import filing
import token_normalizer


def _query_to_infix(query):
    '''
    Convert `query` to an infix boolean expression.

    AND, OR, NOT are replaced with *, +, ~.
    Whitespaces are added for further processing.
    '''
    expression = (
        query
        .replace('(', ' ( ')
        .replace(')', ' ) ')
        .replace('AND', ' * ')
        .replace('OR', ' + ')
        .replace('NOT', ' ~ ')
    )
    tokens = expression.split()

    infix = token_normalizer.normalize_tokens(tokens)
    return infix


def _infix_to_postfix(infix):
    '''
    Return a postfix expression from an `infix` expression.

    Shunting-yard algorithm is employed.
    '''
    stack = deque()
    postfix = []

    for token in infix:
        if token == '(':
            stack.append(token)

        elif token == ')':
            while True:
                if not stack:
                    # wrong infix
                    print('INCORRECT EQUATION FOOL')
                    return None
                if stack[-1] == '(':
                    stack.pop()
                    break
                postfix.append( stack.pop() )
        
        elif token in ['*', '+', '~']:
            stack.append(token) #precedence not implemented
        else:
            postfix.append(token) #operand

    stack.reverse()
    postfix.extend(stack) #empty the stack

    return postfix


def _evaluate_postfix(postfix, inverted_index, doc_ids):
    '''
    Evaluate the `postfix` expression.

    Returns a set containing relevant doc_ids.
    '''
    if len(postfix) == 1: # short circuit single-term queries
        docs = set(inverted_index[postfix[0]].keys())
        return docs

    stack = deque()
    for symbol in postfix:
        if symbol not in ['*', '+', '~', '%']:
            stack.append(symbol)

        elif symbol == '*':
            _intersection(stack, inverted_index)

        elif symbol == '+':
            _union(stack, inverted_index)

        elif symbol == '~':
            _negation(stack, inverted_index, doc_ids)
    
    return stack[0]


def _intersection(stack, inverted_index):
    '''
    Perform intersection (AND) operation.

    Pops two operands and pushes their result on `stack`.
    '''
    operand1 = stack.pop()
    operand2 = stack.pop()

    if type(operand1) is str:
        if operand1 in inverted_index:
            operand1 = set(inverted_index[operand1].keys())
        else: #if term does not exist, intersection will be empty
            stack.append(set())
            return

    if type(operand2) is str:
        if operand2 in inverted_index:
            operand2 = set(inverted_index[operand2].keys())
        else: #if term does not exist, intersection will be empty
            stack.append(set())
            return

    result = set.intersection(operand1, operand2)
    stack.append(result)


def _union(stack, inverted_index):
    '''
    Perform union (OR) operation.

    Pops two operands and pushes their result on `stack`.
    '''
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


def _negation(stack, inverted_index, doc_ids):
    '''
    Perform complement (NOT) operation.

    Pops one operand and pushes the result on `stack`.
    '''
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
    '''
    Retreive documents relevant to the boolean `query`.

    Returns a tuple of sets containing doc_ids and filenames.
    `None` if no relevant documents are found.
    '''
    filename = r'resources\inverted_index'
    inverted_index = filing.load_python_object(filename)

    filename = r'resources\doc_ids'
    doc_ids = filing.load_python_object(filename)

    infix = _query_to_infix(query)

    postfix = _infix_to_postfix(infix)

    # Evaluate postfix expression
    result = _evaluate_postfix(postfix, inverted_index, doc_ids)

    if len(result) == 0:
        return None
    else:
        documents = [doc_ids[doc_id] for doc_id in result]
        return (result, documents)


if __name__ == '__main__':

    # Ask for boolean query
    query = input('Enter a boolean query: ')

    result = retreive_documents(query)

    if result == None:
        print('No relevant speeches.')
    else:
        print(result)