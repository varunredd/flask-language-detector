# Flask Language Detector

A character n-gram-based language detection system built with Python and Flask.  
The project downloads books in multiple languages from Project Gutenberg, builds
language models from character n-gram statistics, and exposes a simple web UI
to detect the language of an input paragraph.

## ✨ Features

- Supports multiple languages (French, German, English, Spanish, Chinese, Japanese)
- Character-level n-gram model (1–5 characters)
- Rank-based distance metric for language detection
- Flask web interface with a clean, minimal UI
- Modular training pipeline script to rebuild models

---

## 🧱 Project Structure

```text
language_detector/
  app.py                  # Flask web server
  lang_detection.py       # Core language detection logic (training + testing)
  prepare_models.py       # Script to run the training pipeline once
  test.txt                # Temporary file used when testing user input
  templates/
    index.html            # Main page with form
    result.html           # Page that shows “Detected Language: ...”
  static/
    style.css             # CSS styling
  dataset/                # Raw or representative text per language (generated)
  tokenized/              # Tokenized and cleaned text (generated)
  nGrams/                 # Ranked n-gram lists per language (generated)
  processed/              # n-gram frequency files per language (generated)

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/flask-language-detector.git
cd flask-language-detector
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate.bat   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, you can generate one with:

```bash
pip freeze > requirements.txt
```

---

## 🧪 Training the Language Models

Before running the web app, you need to download training data and build
n-gram models. This is done once (or whenever you want to retrain) via:

```bash
python prepare_models.py
```

This script will:

* Download books from Project Gutenberg for each supported language.
* Clean and tokenize them.
* Generate character n-gram statistics.
* Save ranked n-gram lists into `nGrams/Language.nGrams.txt`.

> **Note:** This can take a few minutes depending on your connection.

---

## 🚀 Running the Flask App

After training models, start the web app:

```bash
python app.py
```

The app will start on:

```text
http://127.0.0.1:5000
```

Open this URL in your browser.

---

## 💡 Usage

1. Open the web page.
2. Type or paste a paragraph of text in one of the supported languages.
3. Click **“Detect Language”**.
4. The result page will display:

```text
Detected Language: <LanguageName>
```

---

## 🧰 Implementation Details

### Text preprocessing

* Uses `regex` to extract word-like tokens.
* Strips punctuation and digits.
* Lowercases everything to focus on character patterns rather than formatting.

### N-gram model

For each language, the training pipeline:

* Builds a frequency table of all character n-grams of length 1–5.
* Sorts them by frequency to obtain a **ranking** for that language.

### Language detection

For an input paragraph, the app:

1. Applies the same preprocessing as during training.
2. Builds its own ranked list of n-grams.
3. Compares this ranking against each language model using the sum of absolute
   rank differences (with a large penalty for n-grams not present in a model).
4. Chooses the language with the **smallest distance score**.

> Matching the preprocessing between training and testing is crucial.
> If the test pipeline used different rules, the n-grams would not align and the
> detector might always predict the same language.

---

## 🛠 Troubleshooting

### Always predicts the same language

* Ensure you ran:

  ```bash
  python prepare_models.py
  ```

* Confirm that `nGrams/` contains **non-empty** `.nGrams.txt` files for all languages.

* Make sure the test preprocessing uses the same `data_cleaning` and
  `split_and_pad` functions as the training pipeline.

### Books fail to download

* Check your internet connection.
* Project Gutenberg links occasionally change; update URLs in `get_books_text`
  if needed.

---

## 🔮 Possible Extensions

* Add more languages and training corpora.
* Expose a JSON API endpoint for programmatic access.
* Provide top-K predictions with scores.
* Experiment with different distance metrics or ML models (fastText, neural nets).
* Containerize the app with Docker for easier deployment.
