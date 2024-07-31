from flask import Flask, request, render_template
import sentiment_analysis as sa

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        review = request.form['review']
        print(f"Review: {review}")  # Debugging output
        sentiment = sa.predict_sentiment(review)
        print(f"Predicted Sentiment: {sentiment}")  # Debugging output
        return render_template('index.html', prediction=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
