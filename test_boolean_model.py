from config_utils import load_config
from data_processing import load_stop_words, pickle_load_from_file, save_results, load_results
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
    save_results(result2, "data/boolean_results/result2.txt")
    save_results(result3, "data/boolean_results/result3.txt")
    save_results(result4, "data/boolean_results/result4.txt")
    save_results(result8, "data/boolean_results/result8.txt")
    load_result2 = load_results("data/queries/dev_output/2.out")
    load_result3 = load_results("data/queries/dev_output/3.out")
    load_result4 = load_results("data/queries/dev_output/4.out")
    load_result8 = load_results("data/queries/dev_output/8.out")
    result2_difference = len(list(
        set(load_result2).symmetric_difference(set(result2))))
    result3_difference = len(list(
        set(load_result3).symmetric_difference(set(result3))))
    result4_difference = len(list(
        set(load_result4).symmetric_difference(set(result4))))
    result8_difference = len(list(
        set(load_result8).symmetric_difference(set(result8))))
    print(
        f"results 2: expected {len(load_result2)} elements - got {len(result2)} - {result2_difference} elements different")
    print(
        f"results 3: expected {len(load_result3)} elements - got {len(result3)} - {result3_difference} elements different")
    print(
        f"results 4: expected {len(load_result4)} elements - got {len(result4)} - {result4_difference} elements different")
    print(
        f"results 8: expected {len(load_result8)} elements - got {len(result8)} - {result8_difference} elements different")
