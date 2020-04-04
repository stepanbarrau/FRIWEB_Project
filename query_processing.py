from collection_processing import tokenize_simple, remove_stop_words, lemmatize, stemming


def process_query(query, stop_words):
    raw_words = tokenize_simple(query)
    filtered_words = remove_stop_words(raw_words, stop_words)
    lemmatized_words = lemmatize(filtered_words)
    stemmed_words = stemming(lemmatized_words)
    return stemmed_words
