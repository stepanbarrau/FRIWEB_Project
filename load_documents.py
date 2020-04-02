from pathlib import Path
import os


def load_data(data_path):
    """
    browses directory path in data_location.config:data_path
    :return: a dictionary with keys as filenames (string) and content as file content (string)
    """
    corpus = {}
    parse_file_tree(data_path, corpus)
    print("done")

    return corpus


def load_stop_words(filename):
    with open(filename, 'r') as f:
        maj_stop_words = filter(lambda s: s != "", f.read().split("\n\n"))
        return [s.lower() for s in maj_stop_words]


def parse_file_tree(path_name, corpus):
    """
    recursively adds texts to corpus
    :param path_name: starting path (string)
    :param corpus: dictionary of texts
    :return: None
    """
    path = Path(path_name)
    print(path.name)
    for p in path.glob('*'):
        if p.is_dir():
            parse_file_tree(os.path.join(path_name, p.name), corpus)
        else:
            load_file_to_corpus(os.path.join(path_name, p.name), corpus)


def load_file_to_corpus(filename, corpus):
    with open(filename, 'r') as f:
        corpus[filename] = f.read()

