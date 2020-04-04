from tt import BooleanExpression
from collections import Counter
from query import process_query


def query_to_postfixe(query):
    b = BooleanExpression(query)
    return b.postfix_tokens


def query_to_and_boolean(processed_query):
    boolean_query = []
    for token in processed_query:
        boolean_query.append(token)
        boolean_query.append('and')
    boolean_query.pop()
    return query_to_postfixe(boolean_query)


def merge_and_postings_list(posting_term1, posting_term2):
    result = []
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            result.append(posting_term1[i])
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                i = i+1
            else:
                j = j+1
    return result


def merge_or_postings_list(posting_term1, posting_term2):
    result = []
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            result.append(posting_term1[i])
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                result.append(posting_term1[i])
                i = i+1
            else:
                result.append(posting_term2[j])
                j = j+1
    return result


def merge_and_not_postings_list(posting_term1, posting_term2):
    result = []
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                result.append(posting_term1[i])
                i = i+1
            else:
                j = j+1
    return result


def boolean_operator_processing_with_inverted_index(boolean_operator, posting_term1, posting_term2):
    result = []
    if boolean_operator == "and":
        result.append(merge_and_postings_list(posting_term1, posting_term2))
    elif boolean_operator == "or":
        result.append(merge_or_postings_list(posting_term1, posting_term2))
    elif boolean_operator == "not":
        result.append(merge_and_not_postings_list(
            posting_term1, posting_term2))
    return result


def process_boolean_query_with_inverted_index(query, inverted_index, boolean_operators=["and", "or", "not"]):
    evaluation_stack = []
    for term in query:
        if term.upper() not in boolean_operators:
            evaluation_stack.append(inverted_index[term.upper()])
        else:
            if term.upper() == "not":
                operande = evaluation_stack.pop()
                eval_prop = boolean_operator_processing_with_inverted_index(
                    term.upper(), evaluation_stack.pop(), operande)
                evaluation_stack.append(eval_prop[0])
                evaluation_stack.append(eval_prop[0])
            else:
                operator = term.upper()
                eval_prop = boolean_operator_processing_with_inverted_index(
                    operator, evaluation_stack.pop(), evaluation_stack.pop())
                evaluation_stack.append(eval_prop[0])
    return evaluation_stack.pop()


def process_query_boolean(query, inverted_index):
    boolean_query = query_to_and_boolean(query)
    return process_boolean_query_with_inverted_index(boolean_query, inverted_index)