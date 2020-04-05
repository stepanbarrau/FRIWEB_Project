from tt import BooleanExpression
from collections import Counter
from collection_processing import process_text


def processed_query_to_and_boolean(query_tokens):
    """
    transform query tokens to boolean query tokens
    :param query_tokens: query words (list of string)
    :return: query tokens with "and" between (list of string)
    """
    # Copy query
    boolean_query = [token for token in query_tokens]
    for _ in range(len(query_tokens) - 1):
        # Reverse Polish notation
        boolean_query.append('and')
    return boolean_query


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
        if term not in boolean_operators:
            if term not in inverted_index.keys():
                raise Exception("One term is not in the index")
            else:
                evaluation_stack.append(inverted_index[term])
        else:
            if term == "not":
                operande = evaluation_stack.pop()
                eval_prop = boolean_operator_processing_with_inverted_index(
                    term, evaluation_stack.pop(), operande)
                evaluation_stack.append(eval_prop[0])
                evaluation_stack.append(eval_prop[0])
            else:
                operator = term
                eval_prop = boolean_operator_processing_with_inverted_index(
                    operator, evaluation_stack.pop(), evaluation_stack.pop())
                evaluation_stack.append(eval_prop[0])
    return evaluation_stack.pop()


def process_query_boolean(query, inverted_index, stop_words):
    """
    find relevant documents for given query using boolean model on inverted_index
    :param query: (string)
    :param inverted_index: (dict string -> string)
    :param stop_words: to filter stop words in query (list of string)
    :return: documents relevant for the query (list of string)
    """
    processed_query = process_text(query, stop_words)
    # Filter off words that are not in the index
    processed_query = list(filter(
        lambda token: token in inverted_index.keys(), processed_query))
    boolean_query = processed_query_to_and_boolean(processed_query)
    if (len(boolean_query) > 0):
        return process_boolean_query_with_inverted_index(boolean_query, inverted_index)
    else:
        print("boolean query is empty: returning empty result")
        return []


if __name__ == "__main__":
    query = ["we", "are"]
    boolean_query = processed_query_to_and_boolean(query)
    print(boolean_query)
