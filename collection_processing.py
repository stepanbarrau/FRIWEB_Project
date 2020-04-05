import collections
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from data_processing import load_data, load_stop_words, pickle_save_data_to_file, pickle_load_from_file
from config_utils import load_config


def tokenize_simple(text):
    """
    separates text into tokens with space as separator
    :param text: input text (string)
    :return: tokens (list of string)
    """
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = text.split(" ")
        return tokens


def remove_stop_words(text_tokens, stop_words):
    """
    removes words in stop_words from text_tokens
    :param text_tokens: (list of string)
    :param stop_words: (list of string)
    :return: tokens (list of string)
    """
    for word in stop_words:
        text_tokens = list(filter(lambda a: a != word, text_tokens))

    return(text_tokens)


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def stemming(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def process_text(text, stop_words):
    """
    split the text into tokens, remove the stop words, lemmatize and stem tokens.
    :param text: (string)
    :param stop_words: (list of string)
    :return: stemmed_words (list of string)
    """
    raw_words = tokenize_simple(text)
    filtered_words = remove_stop_words(raw_words, stop_words)
    lemmatized_words = lemmatize(filtered_words)
    stemmed_words = stemming(lemmatized_words)
    return stemmed_words


def get_collection_from_corpus(corpus, stop_words):
    collection = {}
    print("start building collection")
    for key in corpus:
        print(f"processing {key}")
        collection[key] = process_text(corpus[key], stop_words)
    print("done building collection")
    return collection


def main():
    config = load_config()
    data_path = config.get('data_path', 'data_path')
    stop_words_path = config.get('stop_words_path', 'stop_words_path')

    corpus = load_data(data_path)
    stop_words = load_stop_words(stop_words_path)

    collection = get_collection_from_corpus(corpus, stop_words)

    pickle_save_data_to_file(
        collection, config.get('collection_path', 'collection_path'))
    collection_loaded = pickle_load_from_file(
        config.get('collection_path', 'collection_path'))

    for term in collection:
        if term not in collection_loaded or collection[term] != collection_loaded[term]:
            raise Exception(
                "There is a discrepancy between the collection and the loaded data")


if __name__ == "__main__":
    main()
