from pathlib import Path
import configparser
import os


def load_data():
    """
    browses directory path in data_location.config:data_path
    :return: a dictionary with keys as filenames (string) and content as file content (string)
    """
    config = configparser.ConfigParser()
    config.readfp(open(r'data_location.config'))
    data_path = config.get('data_path', 'data_path')

    corpus = {}
    parse_file_tree(data_path, corpus)
    print("done")

    return corpus


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
        f.close()


