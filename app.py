# app.py
from flask import Flask, render_template, request
from lang_detection import test_language, BASE_DIR
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/detect_language', methods=['POST'])
def detect_language_route():
    paragraph = request.form['paragraph']

    # Save paragraph to test.txt
    test_path = os.path.join(BASE_DIR, "test.txt")
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(paragraph)

    language = test_language(test_path)
    return render_template('result.html', language=language)

if __name__ == "__main__":
    app.run(debug=True)
