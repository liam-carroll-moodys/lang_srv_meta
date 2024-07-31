from flask import Flask, request, jsonify
import nltk
nltk.download('punkt', quiet=True)
import ctranslate2
import sentencepiece as spm
import os

app = Flask(__name__)
ct_model_path = os.path.join(os.path.dirname(__file__), "..", "models", "m2m100_418m")
sp_model_path = os.path.join(ct_model_path, "sentencepiece.model")

# Set the device and beam size
device = "cpu"  # Change to "cuda" if GPU is available
beam_size = 1

# Load the source SentencePiece model
sp = spm.SentencePieceProcessor()
sp.load(sp_model_path)

# Initialize the translator
translator = ctranslate2.Translator(ct_model_path, device=device)

def translate(text, src_p, tgt_p):
    src_prefix = "__" + src_p + "__"
    tgt_prefix = "__" + tgt_p + "__"
    source_sents = nltk.sent_tokenize(text)
    target_prefix = [[tgt_prefix]] * len(source_sents)
    source_sents_subworded = sp.encode(source_sents, out_type=str)
    source_sents_subworded = [[src_prefix] + sent for sent in source_sents_subworded]

    # Translate the source sentences
    translations = translator.translate_batch(source_sents_subworded, batch_type="tokens",
                                              max_batch_size=2024, beam_size=beam_size,
                                              target_prefix=target_prefix)
    translations = [translation[0]['tokens'] for translation in translations]

    # Desubword the target sentences
    translations_desubword = sp.decode(translations)
    translations_desubword = [sent[len(tgt_prefix):] for sent in translations_desubword]
    translated_text = " ".join(translations_desubword)
    return translated_text

@app.route("/")
def hello_world():
    return "Translation service is running\n"

@app.route("/query", methods=['GET', 'POST'])
def query_endpoint():
    if request.method == 'POST':
        data = request.json
    else:  # GET method
        data = request.args

    text = data.get('text')
    src_p = data.get('src_p')
    tgt_p = data.get('tgt_p')

    if not all([text, src_p, tgt_p]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        translated_text = translate(text, src_p, tgt_p)
        return translated_text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5007)