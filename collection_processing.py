from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer, word_tokenize

from data_processing import load_data, load_stop_words, pickle_save_data_to_file, pickle_load_from_file
from config import CORPUS_DIRECTORY_PATH, STOP_WORDS_FILE_PATH, COLLECTION_FILE_PATH


def tokenize_simple(text):
    """
    Separates text into tokens with space as separator.

    :param text: input text (string)
    :return: tokens (list of string)
    """
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = text.split(" ")
        return tokens


def tokenize_regex(text):
    """
    Separates text into tokens using a RegexpTokenizer.

    :param text: input text (string)
    :return: tokens (list of string)
    """
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        # Extract abbreviations
        tokenizer = RegexpTokenizer('[a-zA-Z]\.[a-zA-Z]')
        tokens = tokenizer.tokenize(text)

        # Extract words and numbers
        tokenizer = RegexpTokenizer('[a-zA-Z]{2,}|\d+\S?\d*')
        word_tokens = tokenizer.tokenize(text)
        return tokens + word_tokens


def remove_stop_words(text_tokens, stop_words):
    """
    Removes words in stop_words from text_tokens.

    :param text_tokens: (list of string)
    :param stop_words: (list of string)
    :return: tokens (list of string)
    """
    for word in stop_words:
        text_tokens = list(filter(lambda a: a != word, text_tokens))

    return text_tokens


def lemmatize(tokens):
    """Lemmatize list of tokens"""
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def stemming(tokens):
    """Stem list of tokens"""
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def process_text(text, stop_words, rm_stop_words=True):
    """
    Split the text into tokens, remove the stop words unless specified not to, lemmatize and stem tokens.

    :param text: (string)
    :param stop_words: (list of string)
    :param rm_stop_words: (bool)
    :return: stemmed_words (list of string)
    """
    words = tokenize_simple(text)
    if rm_stop_words:
        words = remove_stop_words(words, stop_words)
    lemmatized_words = lemmatize(words)
    stemmed_words = stemming(lemmatized_words)
    return stemmed_words


def get_collection_from_corpus(corpus, stop_words):
    """
    Creates a collection dictionary from a given corpus and a list of stop_words.

    :param corpus: (dict) A dictionary with filenames as keys and file content as values
    :param stop_words: (list) List of stopwords
    :return: (dict)
    """
    collection = {}
    print("start building collection")
    for key in corpus:
        print(f"processing {key}")
        collection[key] = process_text(corpus[key], stop_words)
    print("done building collection")
    return collection


def remove_query_from_stop_words(query, stop_words):
    """Returns a copy of the stop words after having removed the words used in the query"""
    query_words = query.split()
    return [sw for sw in stop_words if sw not in query_words]


def check_only_stop_words(query, stop_words):
    """Checks whether the query contains only stop words"""
    for word in query.split():
        if word not in stop_words:
            return False
    return True


def main():
    corpus = load_data(CORPUS_DIRECTORY_PATH)
    stop_words = load_stop_words(STOP_WORDS_FILE_PATH)

    collection = get_collection_from_corpus(corpus, stop_words)

    pickle_save_data_to_file(collection, COLLECTION_FILE_PATH)

    # This tests whether the save and load are done correctly
    collection_loaded = pickle_load_from_file(COLLECTION_FILE_PATH)

    for term in collection:
        if term not in collection_loaded or collection[term] != collection_loaded[term]:
            raise Exception(
                "There is a discrepancy between the collection and the loaded data")


if __name__ == "__main__":
    main()
