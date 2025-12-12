# lang_detection.py
import os
import requests
import pycountry
import regex
import collections

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def split_and_pad(text):
    """
    Take a long string, extract word-like tokens, one per line, all lowercase.
    """
    tokens = regex.findall(r"\b\p{L}+\'*\p{L}*\b",text,flags=regex.UNICODE)
    padded_tokens = [token.lower() + '\n' for token in tokens]
    return padded_tokens

def data_cleaning(raw_text):
    """
    Remove punctuation, digits etc. Keep mostly letters/whitespace.
    """
    regex_pattern = r"[，!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~0-9]"
    return regex.sub(regex_pattern, "", raw_text)

def skip_template_text(text):
    """
    Strip Project Gutenberg header/footer, then clean.
    """
    start_phrase = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_phrase_1 = "*** END OF THE PROJECT GUTENBERG EBOOK"
    end_phrase_2 = "End of Project Gutenbergs"

    pattern = regex.compile(
        f'{regex.escape(start_phrase)}(.*?){regex.escape(end_phrase_1)}|'
        f'{regex.escape(end_phrase_2)}',
        regex.DOTALL
    )
    match = pattern.search(text)
    if match:
        start_idx = match.start() + len(start_phrase)
        end_idx = match.end() - 50
        intermediate_stage = text[start_idx:end_idx]
        index = intermediate_stage.find("***")
        if index != -1:
            text = intermediate_stage[index + 600 + len("***"):].strip()
    return data_cleaning(text)

def get_books_text(output_directory=BASE_DIR, language_codes=None):
    if language_codes is None:
        language_codes = ['fra', 'deu', 'eng', 'spa', 'zho', 'jpn']

    # List of lists of URLs for each language (same as your code)
    urls = [
        [  # French
            "https://www.gutenberg.org/cache/epub/51709/pg51709.txt",
            "https://www.gutenberg.org/cache/epub/18092/pg18092.txt",
            "https://www.gutenberg.org/cache/epub/13704/pg13704.txt",
            "https://www.gutenberg.org/cache/epub/16901/pg16901.txt",
            "https://www.gutenberg.org/cache/epub/44715/pg44715.txt",
            "https://www.gutenberg.org/cache/epub/11049/pg11049.txt",
            "https://www.gutenberg.org/cache/epub/14536/pg14536.txt",
            "https://www.gutenberg.org/cache/epub/51826/pg51826.txt",
            "https://www.gutenberg.org/cache/epub/50435/pg50435.txt",
            "https://www.gutenberg.org/cache/epub/28523/pg28523.txt",
        ],
        [  # German
            "https://www.gutenberg.org/cache/epub/15787/pg15787.txt",
            "https://www.gutenberg.org/cache/epub/16264/pg16264.txt",
            "https://www.gutenberg.org/cache/epub/19755/pg19755.txt",
            "https://www.gutenberg.org/cache/epub/14075/pg14075.txt",
            "https://www.gutenberg.org/cache/epub/22492/pg22492.txt",
            "https://www.gutenberg.org/cache/epub/17379/pg17379.txt",
            "https://www.gutenberg.org/cache/epub/19460/pg19460.txt",
            "https://www.gutenberg.org/cache/epub/20613/pg20613.txt",
            "https://www.gutenberg.org/cache/epub/6343/pg6343.txt",
            "https://www.gutenberg.org/cache/epub/6342/pg6342.txt",
        ],
        [  # English
            "https://www.gutenberg.org/cache/epub/20724/pg20724.txt",
            "https://www.gutenberg.org/cache/epub/19238/pg19238.txt",
            "https://www.gutenberg.org/cache/epub/19291/pg19291.txt",
            "https://www.gutenberg.org/cache/epub/19285/pg19285.txt",
            "https://www.gutenberg.org/cache/epub/19296/pg19296.txt",
            "https://www.gutenberg.org/cache/epub/19300/pg19300.txt",
            "https://www.gutenberg.org/cache/epub/48916/pg48916.txt",
            "https://www.gutenberg.org/cache/epub/22600/pg22600.txt",
            "https://www.gutenberg.org/cache/epub/29107/pg29107.txt",
            "https://www.gutenberg.org/cache/epub/21993/pg21993.txt",
        ],
        [  # Spanish
            "https://www.gutenberg.org/cache/epub/33461/pg33461.txt",
            "https://www.gutenberg.org/cache/epub/36986/pg36986.txt",
            "https://www.gutenberg.org/cache/epub/16109/pg16109.txt",
            "https://www.gutenberg.org/cache/epub/20099/pg20099.txt",
            "https://www.gutenberg.org/cache/epub/46201/pg46201.txt",
            "https://www.gutenberg.org/cache/epub/68443/pg68443.txt",
            "https://www.gutenberg.org/cache/epub/13608/pg13608.txt",
            "https://www.gutenberg.org/cache/epub/43017/pg43017.txt",
            "https://www.gutenberg.org/cache/epub/55038/pg55038.txt",
            "https://www.gutenberg.org/cache/epub/63509/pg63509.txt",
        ],
        [  # Chinese
            "https://www.gutenberg.org/cache/epub/24225/pg24225.txt",
            "https://www.gutenberg.org/cache/epub/25328/pg25328.txt",
            "https://www.gutenberg.org/cache/epub/27119/pg27119.txt",
            "https://www.gutenberg.org/cache/epub/24185/pg24185.txt",
            "https://www.gutenberg.org/cache/epub/24051/pg24051.txt",
            "https://www.gutenberg.org/cache/epub/23841/pg23841.txt",
            "https://www.gutenberg.org/cache/epub/24041/pg24041.txt",
            "https://www.gutenberg.org/cache/epub/27329/pg27329.txt",
            "https://www.gutenberg.org/cache/epub/24058/pg24058.txt",
            "https://www.gutenberg.org/cache/epub/23948/pg23948.txt",
        ],
        [  # Japanese
            "https://www.gutenberg.org/cache/epub/1982/pg1982.txt",
            "https://www.gutenberg.org/cache/epub/34013/pg34013.txt",
            "https://www.gutenberg.org/cache/epub/39287/pg39287.txt",
            "https://www.gutenberg.org/cache/epub/35018/pg35018.txt",
            "https://www.gutenberg.org/cache/epub/34158/pg34158.txt",
            "https://www.gutenberg.org/cache/epub/41325/pg41325.txt",
            "https://www.gutenberg.org/cache/epub/36358/pg36358.txt",
            "https://www.gutenberg.org/cache/epub/35018/pg35018.txt",
            "https://www.gutenberg.org/cache/epub/32978/pg32978.txt",
        ],
    ]

    for index, url_list in enumerate(urls):
        language = pycountry.languages.get(alpha_3=language_codes[index]).name
        print("Getting data for", language)

        books_text = []
        cleaned_text = ""
        tokens = []

        for _, url in enumerate(url_list):
            try:
                response = requests.get(url)
                response.raise_for_status()

                raw_text = response.content.decode("utf-8", errors="ignore").strip()

                cleaned_text += skip_template_text(raw_text)
                tokens = split_and_pad(cleaned_text)

                books_text.append(raw_text)
            except requests.exceptions.RequestException as e:
                print(f"Error downloading book from {url}: {e}")

        # Save ONE combined file per language (this is like the course)
        dataset_path = os.path.join(output_directory, "dataset", f"{language}.txt")
        with open(dataset_path, "w", encoding="utf-8") as f:
            f.write(books_text[0])

        tokenized_path = os.path.join(output_directory, "tokenized", f"{language}.int1.txt")
        with open(tokenized_path, "w", encoding="utf-8") as f:
            for item in tokens:
                f.write(item)

def generate_ngrams(line):
    """
    Character ngrams of length 1..5 from a string.
    """
    ngrams = []
    n = len(line)
    for i in range(n):
        for j in range(1, min(n - i, 6)):
            ngrams.append(line[i:i + j])
    return ngrams


def count_ngram_frequency(ngrams):
    return collections.Counter(ngrams)


def sort_ngrams_by_frequency(ngram_counter):
    # Sort primarily by descending frequency, then alphabetically
    return sorted(ngram_counter.items(), key=lambda x: (-x[1], x[0]))

def generate_and_count_ngrams(input_file_path, output_file_path, frequency_file_path):
    n_gram_counts = collections.Counter()

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            ngrams = generate_ngrams(line)
            n_gram_counts += count_ngram_frequency(ngrams)

    sorted_ngrams = sort_ngrams_by_frequency(n_gram_counts)

    with open(output_file_path, 'w', encoding='utf-8') as output_file, \
         open(frequency_file_path, 'w', encoding='utf-8') as frequency_file:

        for n_gram, count in sorted_ngrams:
            output_file.write(f"{n_gram}\n")
            frequency_file.write(f"{n_gram}: {count}\n")

def preprocess_file(file_name):
    """
    Preprocess user input in the SAME WAY as training data.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    cleaned = data_cleaning(raw_text)
    tokens = split_and_pad(cleaned)
    return tokens

def test_language(file_name):
    """
    Compute ranking of ngrams in the test text, then compare
    with each language's ranking and pick the closest.
    """
    directory = os.path.join(BASE_DIR, "nGrams")
    trained_languages = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith('.nGrams.txt')
    ]
    print("Trained language files:", trained_languages)

    tokenized_lines = preprocess_file(file_name)
    n_gram_counts = collections.Counter()

    for line in tokenized_lines:
        ngrams = generate_ngrams(line)
        n_gram_counts += count_ngram_frequency(ngrams)

    sorted_ngrams = sort_ngrams_by_frequency(n_gram_counts)

    out_of_order_scores = []

    for language_file in trained_languages:
        with open(language_file, 'r', encoding='utf-8') as f:
            train_ngrams = [line.strip() for line in f]

        rank_table = {ngram: rank for rank, ngram in enumerate(train_ngrams, start=1)}

        # distance = how much the ranking of each ngram differs
        score = 0
        for rank, (ngram, _) in enumerate(sorted_ngrams, start=1):
            score += abs(rank_table.get(ngram, 50000) - rank)
        out_of_order_scores.append(score)

    min_index = out_of_order_scores.index(min(out_of_order_scores))
    identified_language_file = trained_languages[min_index]
    result = os.path.basename(identified_language_file)[:-10]  # strip ".nGrams.txt"
    return result
