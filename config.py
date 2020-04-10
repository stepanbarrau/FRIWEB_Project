import os
import configparser

# Paths
DIRECTORY_PATH = os.getcwd()
# Data path
DATA_DIRECTORY_PATH = os.path.join(DIRECTORY_PATH, "data")
# Corpus path
CORPUS_DIRECTORY_PATH = os.path.join(DATA_DIRECTORY_PATH, "pa1-data")
# Stop words file path
STOP_WORDS_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "stop_words.txt")
# Queries paths
QUERIES_PATH = os.path.join(DATA_DIRECTORY_PATH, "queries")
QUERIES_INPUT_PATH = os.path.join(QUERIES_PATH, "dev_queries")
QUERIES_OUTPUT_PATH = os.path.join(QUERIES_PATH, "dev_output")
# Collection file path
COLLECTION_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, "collection.pkl")
# Index files path
INDEX_DIRECTORY_PATH = os.path.join(DATA_DIRECTORY_PATH, "index")
SIMPLE_INDEX_FILE_PATH = os.path.join(INDEX_DIRECTORY_PATH, "simple_index.pkl")
FREQUENCY_INDEX_FILE_PATH = os.path.join(INDEX_DIRECTORY_PATH, "frequency_index.pkl")
DF_FILE_PATH = os.path.join(INDEX_DIRECTORY_PATH, "df_file.pkl")
# Test output paths
VECTORIAL_RESULTS_DIRECTORY_PATH = os.path.join(DATA_DIRECTORY_PATH, "vectorial_results")
BOOLEAN_RESULTS_DIRECTORY_PATH = os.path.join(DATA_DIRECTORY_PATH, "boolean_results")