import collections


def article_tokenize_simple(text):
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


def article_remove_stop_words(text_tokens,stop_word_file):
    """
    removes words in stop_word_file from text_tokens
    :param text_tokens: (list of string)
    :param stop_word_file: (list of string)
    :return: tokens (list of string)
    """
    for word in stop_word_file:
        text_tokens = list(filter(lambda a: a != word, text_tokens))

    return(text_tokens)


print(article_tokenize_simple("lala lulu lolo"))