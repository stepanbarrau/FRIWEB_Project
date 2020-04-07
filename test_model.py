from argparse import ArgumentParser

from config_utils import load_config
from data_processing import load_stop_words, pickle_load_from_file, load_queries_and_output
from boolean_model import process_query_boolean

if __name__ == "__main__":




    config = load_config()
    stop_words = load_stop_words(config.get(
        'stop_words_path', 'stop_words_path'))
    inv_index = pickle_load_from_file(config.get(
        'simple_index_path', 'simple_index_path'))
    queries_and_output = load_queries_and_output(config.get('queries_path', 'queries_path'), config.get(
        'queries_output_path', 'queries_output_path'))
    for query in queries_and_output:
        prediction = process_query_boolean(query, inv_index, stop_words)
        output = queries_and_output[query]
        difference = list(
            set(prediction).symmetric_difference(set(output)))
        print(
            f"query '{query}': expected {len(output)} elements - got {len(prediction)} - {len(difference)} elements different")
