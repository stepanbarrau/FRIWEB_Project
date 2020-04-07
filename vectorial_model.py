import math
from collections import Counter
from collections import OrderedDict

from collection_processing import article_tokenize_other, lemmatize, remove_stop_words


def remove_non_index_term(query, inverted_index):
    """"Remove tokens that are not in index from query."""
    query_filtered = []
    for token in query:
        if token in inverted_index:
            query_filtered.append(token)
    return query_filtered


def pre_processed_query(query, inverted_index, stop_words):
    """
    Process raw query for vectorial vectorial query.

    Tokenize, filter stop words and lemmatize query.
    :param query: (string) query
    :param inverted_index:
    :return:
    """
    tokenized_query = article_tokenize_other(query)
    filtered_query = remove_non_index_term(tokenized_query, inverted_index)
    filtered_query = remove_stop_words(filtered_query, stop_words)
    normalized_query = lemmatize(filtered_query)
    return normalized_query


def get_term_frequency(term, doc_id, index_frequency):
    """Get the frequency of a term in a document of the collection."""
    return index_frequency[term][doc_id]


def get_logarithmic_term_frequency(term, doc_id, index_frequency):
    """
    Get logarithmic frequency of term in a document of the collection.

    Equal to 0 if the term is not in the document, otherwise 1 + log(term_frequency).
    """
    tf = get_term_frequency(term, doc_id, index_frequency)
    if tf > 0:
        return 1 + math.log(tf)
    else:
        return 0


def get_normalized_term_frequency(term, doc_id, index_frequency, stats_collection):
    """Get normalized term frequency"""
    term_frequency = get_term_frequency(term, doc_id, index_frequency)
    normalized_term_frequency = 0.5 + 0.5 * (term_frequency / stats_collection[doc_id]["max_frequency"])
    return normalized_term_frequency


def get_normalized_logarithmic_term_frequency(term, doc_id, index_frequency, stats_collection):
    """Get normalized logarithmic term frequency"""
    term_frequency = get_term_frequency(term, doc_id, index_frequency)
    normalized_logarithmic_term_frequency = (1 + math.log(term_frequency)) / (1 + math.log(
        stats_collection[doc_id]["average_frequency"]))
    return normalized_logarithmic_term_frequency


def get_idf(term, index_frequency, nb_doc):
    """Gets idf of term in collection"""
    return math.log(nb_doc / len(index_frequency[term].keys()))


def get_stats_document(document):
    """
    Get statistics on the document.

    Calculates the frequency of most common term, the number of unique terms, and the average frequency of terms.
    :param document: Document to get statistics on
    :return: (dict) stats
    """
    counter = Counter()
    for term in document:
        counter.update([term])
    stats = dict()
    stats["max_frequency"] = counter.most_common(1)[0][1]
    stats["number_unique_terms"] = len(counter.items())
    tf_moy = sum(counter.values())
    stats["average_frequency"] = tf_moy / len(counter.items())
    return stats


def get_stats_collection(collection):
    """Get statistics on all the documents in the collection """
    stats = dict()
    stats["nb_docs"] = len(collection.keys())
    for doc in collection:
        stats[doc] = get_stats_document(collection[doc])
    return stats


def process_vectorial_query(query, frequency_index, stop_words, stats_collection, weighting_scheme_document,
                            weighting_scheme_query):
    # Set weighting schemes if not specified
    if weighting_scheme_document is None:
        weighting_scheme_document = "tf_idf_normalize"
    if weighting_scheme_query is None:
        weighting_scheme_query = "frequency"

    relevant_docs = {}
    counter_query = Counter()
    # Preprocess query
    query_pre_processed = pre_processed_query(query, frequency_index, stop_words)

    nb_doc = stats_collection["nb_docs"]
    norm_query = 0.
    for term in query_pre_processed:
        if term in frequency_index:
            w_term_query = 0.
            counter_query.update([term])
            if weighting_scheme_query == "binary":
                w_term_query = 1
            if weighting_scheme_query == "frequency":
                w_term_query = counter_query[term]
            norm_query = norm_query + w_term_query * w_term_query
            for doc in frequency_index[term]:
                w_term_doc = 0.
                relevant_docs[doc] = 0.
                if weighting_scheme_document == "binary":
                    w_term_doc = 1
                if weighting_scheme_document == "frequency":
                    w_term_doc = get_term_frequency(term, doc, frequency_index)
                if weighting_scheme_document == "tf_idf_normalize":
                    w_term_doc = get_normalized_term_frequency(term, doc, frequency_index, stats_collection
                                                               ) * get_idf(term, frequency_index, nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic":
                    w_term_doc = get_logarithmic_term_frequency(term, doc, frequency_index
                                                                ) * get_idf(term, frequency_index, nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic_normalize":
                    w_term_doc = get_normalized_logarithmic_term_frequency(term, doc, frequency_index, stats_collection
                                                                           ) * get_idf(term, frequency_index, nb_doc)
                relevant_docs[doc] = relevant_docs[doc] + w_term_doc * w_term_query
    ordered_relevant_docs = OrderedDict(sorted(relevant_docs.items(), key=lambda t: t[1], reverse=True))
    return ordered_relevant_docs
