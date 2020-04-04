import collections
import pickle
from enum import Enum
from collection_processing import get_collection_from_corpus
from data_processing import load_data, load_stop_words
from config_utils import load_config


class IndexType(Enum):
    SIMPLE = 0
    FREQUENCY = 1


def build_index(collection, type):
    """
    builds inverted index from a collection of stemmed words (dict:name->text) of texts
    :param collection: dict string -> string
    :param type: type of the index : type = 0 -> document index (simple)
                                     type  = 1 -> frequency index
                                     type = 3 -> position index (not yet implemented)
    :return: index (dict: term(string) -> list of text names (string) + frequency/position (optional)
             df (dict term(string) -> frequency (int)
    """

    index = {}
    df = {}
    for text_name in collection:
        term_counter = collections.Counter(collection[text_name])

        if type == IndexType.SIMPLE:
            for term in term_counter:
                index[term] = index.setdefault(term, [])
                df[term] = df.setdefault(term, 0)

                index[term].append(text_name)
                df[term] += 1

        if type == IndexType.FREQUENCY:
            for term in term_counter:
                index[term] = index.setdefault(term, [])
                df[term] = df.setdefault(term, 0)

                index[term].append((text_name, term_counter[term]))
                df[term] += 1

    return index, df


def save_index_to_file(inverted_index, filename):
    with open(filename, "wb") as f:
        pickle.dump(inverted_index, f)
        f.close()


def load_index_from_file(filename):
    with open(filename, 'rb') as f:
        index = pickle.load(f)
        return index


def save_df_to_file(df, filename):
    with open(filename, "wb") as f:
        pickle.dump(df, f)
        f.close()


def load_df_from_file(filename):
    with open(filename, 'rb') as f:
        df = pickle.load(f)
        return df


def test():
    config = load_config()
    data_path = config.get('data_path', 'data_path')
    stop_words_path = config.get('stop_words_path', 'stop_words_path')

    corpus = load_data(data_path)
    stop_words = load_stop_words(stop_words_path)

    collection = get_collection_from_corpus(corpus, stop_words)
    index, df = build_index(collection, IndexType.SIMPLE)

    save_index_to_file(index, "test_index_file4.txt")
    index_loaded = load_index_from_file("test_index_file4.txt")

    save_df_to_file(df, "test_df_file4.txt")
    df_loaded = load_df_from_file("test_df_file4.txt")

    no_error = True
    for term in index:
        if df[term] != df_loaded[term]:
            no_error = False
        for doc_name in index[term]:
            if doc_name not in index_loaded[term]:
                no_error = False

    print(f"no_error : {no_error}")


test()
