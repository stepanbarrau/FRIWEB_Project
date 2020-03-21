from pathlib import Path
import configparser


def load_data():
    """
    browses directory path in data_location.config:data_path
    :return: a dictionary with keys as filenames (string) and content as file content (string)
    """
    config = configparser.ConfigParser()
    config.readfp(open(r'data_location.config'))
    data_path = config.get('data_path', 'data_path')
    path = Path(data_path)

    corpus = {}

    for p in path.rglob('*'):
        if not p.is_dir():
            load_file_to_corpus(p.name, corpus)

    return corpus


def load_file_to_corpus(filename, corpus):
    with open(filename, 'r') as f:
        corpus[filename] = f.read()


