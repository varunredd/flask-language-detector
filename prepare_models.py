# prepare_models.py
from lang_detection import (
    get_books_text,
    generate_and_count_ngrams,
    BASE_DIR,
    pycountry
)
import os

if __name__ == "__main__":
    # Step 1: download & tokenize
    get_books_text()

    # Step 2: generate ngrams per language
    language_codes = ['fra', 'deu', 'eng', 'spa', 'zho', 'jpn']
    for code in language_codes:
        language_name = pycountry.languages.get(alpha_3=code).name
        input_file_path = os.path.join(BASE_DIR, "tokenized", f"{language_name}.int1.txt")
        n_gram_file_path = os.path.join(BASE_DIR, "nGrams", f"{language_name}.nGrams.txt")
        frequency_file_path = os.path.join(BASE_DIR, "processed", f"{language_name}.nGramsFrequency.txt")

        print("Processing", language_name, "for nGrams!")
        generate_and_count_ngrams(input_file_path, n_gram_file_path, frequency_file_path)
