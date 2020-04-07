from argparse import ArgumentParser

from config_utils import load_config
from collection_processing import remove_query_from_stop_words
from data_processing import load_stop_words, pickle_load_from_file, pickle_save_data_to_file, load_queries_and_output
from boolean_model import process_query_boolean
from vectorial_model import process_vectorial_query, get_stats_collection

if __name__ == "__main__":
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="model")
    boolean = subparser.add_parser("boolean")
    vectorial = subparser.add_parser("vectorial")

    vectorial.add_argument("--weight-query", type=str, default="frequercy", choices=("boolean", "frequency"))
    vectorial.add_argument("--weight-document", type=str, default="tf_idf_normalize",
                           choices=("boolean", "frequency", "tf_idf_normalize", "tf_idf_logarithmic",
                                    "tf_idf_logarithmic_normalize"))
    args = parser.parse_args()
    config = load_config()
    stop_words_path = config.get("stop_words_path", "stop_words_path")
    queries_path = config.get("queries_path", "queries_path")
    queries_output_path = config.get("queries_output_path", "queries_output_path")
    simple_index_path = config.get("simple_index_path", "simple_index_path")
    collection_path = config.get("collection_path", "collection_path")
    frequency_index_path = config.get("frequency_index_path", "frequency_index_path")

    stop_words = load_stop_words(stop_words_path)
    queries_and_output = load_queries_and_output(queries_path, queries_output_path)

    if args.model == "boolean":
        inv_index = pickle_load_from_file(simple_index_path)
        for query in queries_and_output:
            stop_words_not_in_query = remove_query_from_stop_words(query, stop_words)
            prediction = process_query_boolean(query, inv_index, stop_words_not_in_query)
            output = queries_and_output[query]
            difference = list(
                set(prediction).symmetric_difference(set(output)))
            print(
                f"query '{query}': expected {len(output)} elements - got {len(prediction)} - {len(difference)} elements different")
    elif args.model == "vectorial":
        collection = pickle_load_from_file(collection_path)
        frequency_index = pickle_load_from_file(frequency_index_path)
        stats_collection = get_stats_collection(collection)
        for query in queries_and_output:
            stop_words_not_in_query = remove_query_from_stop_words(query, stop_words)
            prediction = process_vectorial_query(query, frequency_index, stop_words_not_in_query, stats_collection,
                                                 args.weight_document, args.weight_query)
            output = queries_and_output[query]
            difference = list(
                set(prediction).symmetric_difference(set(output)))
            print(
                f"query '{query}': expected {len(output)} elements - got {len(prediction)} - {len(difference)} elements different")
