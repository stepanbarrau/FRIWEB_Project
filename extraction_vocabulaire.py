import collections
import configparser
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from load_documents import load_data, load_stop_words


def article_tokenize_simple(text):
    """
    separates text into tokens with space as separator
    :param text: input text (string)
    :return: tokens (list of string)
    """
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = word_tokenize(text)
        return tokens


def article_remove_stop_words(text_tokens, stop_words):
    """
    removes words in stop_words from text_tokens
    :param text_tokens: (list of string)
    :param stop_words: (list of string)
    :return: tokens (list of string)
    """
    for word in stop_words:
        text_tokens = list(filter(lambda a: a != word, text_tokens))

    return(text_tokens)


def article_lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def article_stemming(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def main():
    config = configparser.ConfigParser()
    config.read_file(open(r'data_location.config'))
    data_path = config.get('data_path', 'data_path')
    stop_words_path = config.get('stop_words_path', 'stop_words_path')

    corpus = load_data(data_path)
    stop_words = load_stop_words(stop_words_path)
    for key in corpus:
        raw_words = article_tokenize_simple(corpus[key])
        print(collections.Counter(raw_words))
        filtered_words = article_remove_stop_words(raw_words, stop_words)
        print(len(raw_words) - len(filtered_words), "stop word removed")
        lemmatized_words = article_lemmatize(filtered_words)
        stemmed_words = article_stemming(lemmatized_words)
        print(collections.Counter(stemmed_words))
        break


if __name__ == "__main__":
    main()
