#Author: Devi Mahajan
#Date: 7.7.25

"""
Create a program, called score_headlines.py
This program should accept an input text file which will contain one headline per line
This program should also accept a parameter describing the source of the headlines (example: chicagotribune, nyt)
If the client does not provide these two parameters, the program should give an appropriate and friendly error message
This program should output a new file, called headline_scores_source_year_month_day.txt (example: headline_scores_nyt_2025_01_15.txt)
"""

#IMPORTS

import sys
import os
from datetime import datetime
import joblib
from sentence_transformers import SentenceTransformer

MODEL_FILENAME = "svm.joblib"
#EMBEDDING_MODEL_PATH = "/opt/huggingface_models/all-MiniLM-L6-v2"
EMBEDDING_MODEL_PATH = "all-MiniLM-L6-v2"

#FUNCTIONS 

def validate_args():
    #Ensure correct num arguments.
    if len(sys.argv) != 3:
        print("Usage: python score_headlines.py <input_file.txt> <news_source>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def read_headline_file(filepath):
    #Read headlines from text file (ignore blank lines)
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[Error] File not found: {filepath}")
        sys.exit(1)

def embed_texts(text_list):
    #Convert text to vector embeddings
    embedder = SentenceTransformer(EMBEDDING_MODEL_PATH)
    return embedder.encode(text_list)

def load_classifier(path=MODEL_FILENAME):
    #Load scikit-learn SVM classifier
    return joblib.load(path)

def predict_sentiments(classifier, vectorized_headlines):
    #Assign sentiment labels to each headline
    return classifier.predict(vectorized_headlines)

def generate_output_filename(source_name):
    #Create output file name using source + today's date
    today = datetime.today()
    return f"headline_scores_{source_name}_{today.strftime('%Y_%m_%d')}.txt"

def write_predictions(out_path, headlines, sentiments):
    #Write sentiment + headline pairs to file
    with open(out_path, "w", encoding="utf-8") as f:
        for sentiment, line in zip(sentiments, headlines):
            f.write(f"{sentiment}, {line}\n")
    print(f"[✓] Results saved to: {out_path}")

def run_pipeline():
    #Pipeline flow
    input_path, source = validate_args()
    raw_headlines = read_headline_file(input_path)
    embeddings = embed_texts(raw_headlines)
    classifier = load_classifier()
    results = predict_sentiments(classifier, embeddings)
    output_file = generate_output_filename(source)
    write_predictions(output_file, raw_headlines, results)

#RUN MAIN

if __name__ == "__main__":
    run_pipeline()