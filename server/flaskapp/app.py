from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/analyze', methods=['POST'])
@app.route('/api/analyze-review/', methods=['POST'])
@app.route('/analyze/<text>', methods=['GET'])
def analyze_sentiment(text=None):
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        text_to_analyze = data.get('text', '') or request.form.get('text', '')
    else:
        text_to_analyze = text or ""

    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400

    scores = analyzer.polarity_scores(text_to_analyze)
    compound = scores.get('compound', 0)
    
    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return jsonify({
        "text": text_to_analyze,
        "sentiment": sentiment,
        "compound": compound
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "sentiment-analysis"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
