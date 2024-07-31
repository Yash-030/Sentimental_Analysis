import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Preprocessing steps
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Reconstruct the text
    return ' '.join(tokens)

def load_data():
    data = pd.read_csv('Reviews.csv')
    # Apply preprocessing to the review column
    data['Review'] = data['Review'].apply(preprocess_text)
    return data

def train_model():
    data = load_data()
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(data['Review'])
    y = data['Sentiment']
    model = LogisticRegression()
    model.fit(X, y)
    with open('model.pkl', 'wb') as f:
        pickle.dump((tfidf, model), f)

def predict_sentiment(review):
    # Preprocess the review
    review = preprocess_text(review)
    with open('model.pkl', 'rb') as f:
        tfidf, model = pickle.load(f)
    review_tfidf = tfidf.transform([review])
    prediction = model.predict(review_tfidf)
    return prediction[0]

if __name__ == "__main__":
    train_model()  # Train the model
    # Test the predict function
    print(predict_sentiment("The food was amazing and the service was excellent!"))  # Expected: Positive
    print(predict_sentiment("The food was terrible and the service was awful!"))  # Expected: Negative
