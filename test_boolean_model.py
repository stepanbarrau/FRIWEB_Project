from config_utils import load_config
from data_processing import load_stop_words, pickle_load_from_file
from boolean_model import process_query_boolean

if __name__ == "__main__":
    config = load_config()
    stop_words = load_stop_words(config.get(
        'stop_words_path', 'stop_words_path'))
    inv_index = pickle_load_from_file(config.get('index_path', 'index_path'))
    query1 = "stanford"
    query2 = "stanford class avm"
    query3 = "class"
    result1 = process_query_boolean(query1, inv_index, stop_words)
    result2 = process_query_boolean(query2, inv_index, stop_words)
    result3 = process_query_boolean(query3, inv_index, stop_words)
    print(result1)
    print(result2)
    print(result3)
