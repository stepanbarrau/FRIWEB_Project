import collections
import os
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
             df (dict term(string) -> frequency (int)
    """

    if type not in [0, 1]:
        raise Exception("type of inverted index not implemented")

    index = {}
    df = {}
    for text_name in corpus:
        print(index)

        raw_words = article_tokenize_simple(corpus[text_name])
        term_counter = collections.Counter(raw_words)

        if type == 0:
            for term in term_counter:
                if term in index:
                    index[term].append(text_name)
                    df[term] += 1
                else:
                    index[term] = [text_name]
                    df[term] = 1

        if type == 1:
            for term in term_counter:
                if term in index:
                    index[term].append((text_name, term_counter[term]))
                    df[term] += 1
                else:
                    index[term] = [(text_name, term_counter[term])]
                    df[term] = 1

    return index, df


def save_index_to_file(index, df, filename, type):
    """
    WARNING: terms, or document names must NOT contain linebreaks, spaces, or the cheracters | and §
    saves index to a text file, under the format:
    Term1 df_1|doc_1 doc_4                              if it is a type 1
    or
    Term1 df_1|doc_1 tf_doc1_Term1§doc_4 tf_doc_4_Term1 if it is a type 2
    :param index:
    :param filename:
    :return:
    """
    if type not in [0, 1]:
        raise Exception("type of inverted index not implemented")

    with open(filename, "w+") as f:

        if type == 0:
            for term in index:
                line = ""
                line += f"{term} {df[term]}|"
                for doc_name in index[term]:
                    line += f"{doc_name} "
                line += "\n"
                f.write(line)

        if type == 1:
            for term in index:
                f.write(f"{term} {df[term]}|")
                for doc in index[term]:
                    doc_name, doc_tf = doc
                    f.write(f"{doc_name} {doc_tf}§")
                f.write(os.linesep)

        f.close()


def load_index_from_file(filename, type):
    """
    WARNING: terms, or document names must NOT contain linebreaks, spaces, or the cheracters | and §
    loads index and df from file, under the above format
    :param filename: string
    :param type: int
    :return: index, df
    """
    if type not in [0, 1]:
        raise Exception("type of inverted index not implemented")

    index = {}
    df = {}

    if type == 0:
        with open(filename, "r") as f:
            for line in f:
                tokens = line.split("|")
                print(tokens)
                header = tokens[0]
                body = tokens[1]
                header_tokens = header.split(" ")
                body_tokens = body.split(" ")
                term = header_tokens[0]
                df_value = header_tokens[1]
                df[term] = df_value
                index[term] = []
                for doc_name in body_tokens:
                    index[term].append(doc_name)

    if type == 1:
        with open(filename, "r") as f:
            for line in f:
                tokens = line.split("|")
                header = tokens[0]
                body = tokens[1]
                header_tokens = header.split(" ")
                body_tokens = body.split("§")
                term = header_tokens[0]
                df_value = header_tokens[1]
                df[term] = df_value
                index[term] = []
                for doc in body_tokens:
                    doc_tokens = doc.split(" ")
                    doc_name = doc_tokens[0]
                    doc_tf = doc_tokens[1]
                    index[term].append((doc_name, doc_tf))

    return index, df


def test():
    corpus = load_data()
    index, df = build_index(corpus, 0)
    save_index_to_file(index, df, "test_index_file3.txt", 0)
    index_loaded, df_loaded = load_index_from_file("test_index_file3.txt", 0)
    print(index_loaded)
    print(df_loaded)
    no_error = True
    for term in index:
        if df[term] != df_loaded[term]:
            no_error = False
        for doc_name in index[term]:
            if not doc_name in index_loaded[term]:
                no_error = False

    print(f"no_error : {no_error}")


test()
