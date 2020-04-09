import collections
from enum import Enum
from collection_processing import get_collection_from_corpus
from data_processing import load_data, load_stop_words, pickle_save_data_to_file, pickle_load_from_file
from config import CORPUS_DIRECTORY_PATH, SIMPLE_INDEX_FILE_PATH, FREQUENCY_INDEX_FILE_PATH, DF_FILE_PATH


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
    print(f"start building index (type: {type})")
    for text_name in collection:
        print(f"build index for {text_name}")
        term_counter = collections.Counter(collection[text_name])

        if type == IndexType.SIMPLE:
            for term in term_counter:
                index[term] = index.setdefault(term, [])
                df[term] = df.setdefault(term, 0)

                index[term].append(text_name)
                df[term] += 1

        if type == IndexType.FREQUENCY:
            for term in term_counter:
                index[term] = index.setdefault(term, {})
                df[term] = df.setdefault(term, 0)

                index[term].update({text_name: term_counter[term]})
                df[term] += 1
    print("done building index")
    return index, df


def main():
    data_path = CORPUS_DIRECTORY_PATH
    simple_index_path = SIMPLE_INDEX_FILE_PATH
    frequency_index_path = FREQUENCY_INDEX_FILE_PATH
    df_path = DF_FILE_PATH

    corpus = load_data(data_path)
    # Testing not removing stop words from index
    stop_words = []

    collection = get_collection_from_corpus(corpus, stop_words)

    simple_index, simple_df = build_index(collection, IndexType.SIMPLE)

    pickle_save_data_to_file(simple_index, simple_index_path)
    pickle_save_data_to_file(simple_df, df_path)

    # df is the same than simple_df
    frequency_index, _ = build_index(collection, IndexType.FREQUENCY)

    pickle_save_data_to_file(frequency_index, frequency_index_path)

    simple_index_loaded = pickle_load_from_file(simple_index_path)

    frequency_index_loaded = pickle_load_from_file(frequency_index_path)

    df_loaded = pickle_load_from_file(df_path)

    no_error = True
    for term in simple_index:
        if simple_df[term] != df_loaded[term]:
            no_error = False
        for doc_name in simple_index[term]:
            if doc_name not in simple_index_loaded[term]:
                no_error = False
        for doc_name in frequency_index[term]:
            if doc_name not in frequency_index_loaded[term]:
                no_error = False

    print(f"no_error : {no_error}")


if __name__ == "__main__":
    main()
