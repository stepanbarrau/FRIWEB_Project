from argparse import ArgumentParser
import  os

import config
from data_processing import load_stop_words, pickle_load_from_file, pickle_save_data_to_file, load_queries_and_output,\
    save_strings_as_text_file
from boolean_model import process_query_boolean
from vectorial_model import process_vectorial_query, get_stats_collection

if __name__ == "__main__":
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="model")
    boolean = subparser.add_parser("boolean")
    vectorial = subparser.add_parser("vectorial")

    vectorial.add_argument("--weight-query", type=str, default="frequency", choices=("boolean", "frequency"))
    vectorial.add_argument("--weight-document", type=str, default="tf_idf_normalize",
                           choices=("boolean", "frequency", "tf_idf_normalize", "tf_idf_logarithmic",
                                    "tf_idf_logarithmic_normalize"))
    args = parser.parse_args()

    stop_words_path = config.STOP_WORDS_FILE_PATH
    queries_path = config.QUERIES_INPUT_PATH
    queries_output_path = config.QUERIES_OUTPUT_PATH
    simple_index_path = config.SIMPLE_INDEX_FILE_PATH
    frequency_index_path = config.FREQUENCY_INDEX_FILE_PATH
    collection_path = config.COLLECTION_FILE_PATH
    boolean_results_directory_path = config.BOOLEAN_RESULTS_DIRECTORY_PATH
    vectorial_results_directory_path = config.VECTORIAL_RESULTS_DIRECTORY_PATH

    stop_words = load_stop_words(stop_words_path)
    queries_and_output = load_queries_and_output(queries_path, queries_output_path)

    if args.model == "boolean":
        inv_index = pickle_load_from_file(simple_index_path)
        for i, query in enumerate(queries_and_output):
            prediction = process_query_boolean(query, inv_index, stop_words)
            output = queries_and_output[query]
            difference = list(
                set(prediction).symmetric_difference(set(output)))
            print(
                f"query '{query}': expected {len(output)} elements - got {len(prediction)} - {len(difference)} elements different")
            save_strings_as_text_file(prediction, os.path.join(boolean_results_directory_path, f"results_{i}"))
    elif args.model == "vectorial":
        collection = pickle_load_from_file(collection_path)
        frequency_index = pickle_load_from_file(frequency_index_path)
        stats_collection = get_stats_collection(collection)
        for i, query in enumerate(queries_and_output):
            prediction = process_vectorial_query(query, frequency_index, stop_words, stats_collection,
                                                 args.weight_document, args.weight_query)
            output = queries_and_output[query]
            difference = list(
                set(prediction).symmetric_difference(set(output)))
            print(
                f"query '{query}': expected {len(output)} elements - got {len(prediction)} - {len(difference)} elements different")
            save_strings_as_text_file(prediction, os.path.join(vectorial_results_directory_path, f"results_{i}")