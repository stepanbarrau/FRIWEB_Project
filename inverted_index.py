import collections
from extraction_vocabulaire import article_tokenize_simple
from load_documents import load_data

def build_index(corpus, type):
    """
    builds inverted index from corpus (dict:name->text) of texts
    :param corpus: dict string -> string
    :param type: type of the index : type = 0 -> document index (simple)
                                     type  = 1 -> frequency index
                                     type = 3 -> position index (not yet implemented)
    :return: index (dict: term(string) -> list of text names (string) + frequency/position (optional)
    """

    if type not in [0, 1]:
        raise Exception("type of inverted index not implemented")

    index = {}
    for text_name in corpus:
        print(index)

        raw_words = article_tokenize_simple(corpus[text_name])
        term_counter = collections.Counter(raw_words)

        for term in term_counter:
            if term in index:
                if type == 0:
                    index[term].append(text_name)
                elif type == 1:
                    index[term].append((text_name, term_counter[term]))
            else:
                if type == 0:
                    index[term] = [text_name]
                elif type == 1:
                    index[term] = [(text_name, term_counter[term])]

    return index


def save_index_to_file(index, filename, type):
    """
    saves index to a text file, under the format:
    Term1, df_1 | doc_1, doc_4                                   if it is a type 1
    or
    Term1, df_1 | (doc_1, tf_doc1_Term1) (doc_4, tf_doc_4_Term1) if it is a type 2
    :param index:
    :param filename:
    :return:
    """
    # TODO finish
    with open(filename, "w+") as f:
        for term in index:
            pass
        f.close()



def main():
    corpus = load_data()
    index = build_index(corpus, 0)
    print(index)


main()