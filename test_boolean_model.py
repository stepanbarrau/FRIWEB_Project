from config_utils import load_config
from data_processing import load_stop_words, pickle_load_from_file, pickle_save_data_to_file
from boolean_model import process_query_boolean

if __name__ == "__main__":
    config = load_config()
    stop_words = load_stop_words(config.get(
        'stop_words_path', 'stop_words_path'))
    inv_index = pickle_load_from_file(config.get('index_path', 'index_path'))
    query2 = "stanford class"
    query3 = "stanford students"
    query4 = "very cool"
    query8 = "stanford computer science"
    result2 = process_query_boolean(query2, inv_index, stop_words)
    result3 = process_query_boolean(query3, inv_index, stop_words)
    result4 = process_query_boolean(query4, inv_index, stop_words)
    result8 = process_query_boolean(query8, inv_index, stop_words)
    pickle_save_data_to_file(result2, "data/boolean_results/result2")
    pickle_save_data_to_file(result3, "data/boolean_results/result3")
    pickle_save_data_to_file(result4, "data/boolean_results/result4")
    pickle_save_data_to_file(result8, "data/boolean_results/result8")
