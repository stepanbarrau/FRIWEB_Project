import os
import pickle
from pathlib import Path


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


def load_file_to_corpus(filepath, corpus):
    with open(filepath, 'r') as f:
        path, filename = os.path.split(filepath)
        _, folder = os.path.split(path)
        key = os.path.join(folder, filename)
        corpus[key] = f.read()


def pickle_save_data_to_file(data, path):
    dir, _ = os.path.split(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, "wb") as f:
        pickle.dump(data, f)
        f.close()


def pickle_load_from_file(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        return data


def save_results(results, path):
    """
    save a list of document names to a text file
    :param results: (list of string)
    :param path: path (string)
    :return: None
    """
    with open(path, "a") as f:
        results = map(lambda s: s + "\n", results)
        f.writelines(results)
        f.close()


def load_results(path):
    """
    load document names from a text file to a list
    :param path: path (string)
    :return results: (list of string)
    """
    results = []
    with open(path, "r") as f:
        results = f.readlines()
        results = map(lambda s: s[:-2] if s.endswith("\n") else s, results)
        f.close()
    return results
