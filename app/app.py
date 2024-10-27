# from flask import Flask, render_template, request, redirect, url_for
# from pymongo import MongoClient
# from bson import ObjectId
# from transformers import pipeline

# app = Flask(__name__)

# # MongoDB setup
# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
# db = client['sentiment_db']  # Replace with your database name
# collection = db['sentiments']  # Replace with your collection name

# # Load pre-trained BERT model for sentiment analysis
# classifier = pipeline('sentiment-analysis')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         text = request.form['text']
#         if not text.strip():
#             return render_template('index.html', error="Please enter valid text.")
        
#         # BERT-based sentiment analysis
#         result = classifier(text)[0]
#         sentiment_label = result['label']
#         sentiment_score = result['score']

#         # Mapping BERT labels to simpler sentiments
#         sentiment = 'Positive' if sentiment_label == 'POSITIVE' else 'Negative' if sentiment_label == 'NEGATIVE' else 'Neutral'
        
#         # Store in MongoDB
#         collection.insert_one({'text': text, 'sentiment': sentiment, 'score': sentiment_score})
        
#         return redirect(url_for('results'))

#     return render_template('index.html')

# @app.route('/results', methods=['GET'])
# def results():
#     sentiments = list(collection.find())
    
#     # Add emojis based on the sentiment
#     for sentiment in sentiments:
#         if sentiment['sentiment'] == 'Positive':
#             sentiment['emoji'] = '😊'
#         elif sentiment['sentiment'] == 'Negative':
#             sentiment['emoji'] = '😞'
#         else:
#             sentiment['emoji'] = '😐'
    
#     sentiment_counts = {
#         'Positive': sum(1 for s in sentiments if s['sentiment'] == 'Positive'),
#         'Negative': sum(1 for s in sentiments if s['sentiment'] == 'Negative'),
#         'Neutral': sum(1 for s in sentiments if s['sentiment'] == 'Neutral'),
#     }

#     return render_template('results.html', sentiments=sentiments, sentiment_counts=sentiment_counts)

# @app.route('/delete/<id>', methods=['POST'])
# def delete(id):
#     collection.delete_one({'_id': ObjectId(id)})  # Convert id to ObjectId
#     return redirect(url_for('results'))

# @app.route('/clear', methods=['POST'])
# def clear():
#     collection.delete_many({})  # This will delete all records in the collection
#     return redirect(url_for('results'))

# if __name__ == '__main__':
#     app.run(debug=True)

# import os
# from flask import Flask, render_template, request, redirect, url_for
# from pymongo import MongoClient
# from bson import ObjectId
# from transformers import pipeline
# from dotenv import load_dotenv

# # Load environment variables from a .env file if available
# load_dotenv()

# app = Flask(__name__)

# # MongoDB setup using environment variable for the URI
# mongo_uri = os.getenv('MONGODB_URI')
# client = MongoClient(mongo_uri)
# db = client['sentiment_db']  # Replace with your database name if different
# collection = db['sentiments']  # Replace with your collection name if different

# # Load pre-trained BERT model for sentiment analysis
# classifier = pipeline('sentiment-analysis')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         text = request.form['text']
#         if not text.strip():
#             return render_template('index.html', error="Please enter valid text.")
        
#         # Perform sentiment analysis
#         result = classifier(text)[0]
#         sentiment_label = result['label']
#         sentiment_score = result['score']

#         # Mapping BERT labels to simpler sentiments
#         sentiment = 'Positive' if sentiment_label == 'POSITIVE' else 'Negative' if sentiment_label == 'NEGATIVE' else 'Neutral'
        
#         # Store in MongoDB
#         collection.insert_one({'text': text, 'sentiment': sentiment, 'score': sentiment_score})
        
#         return redirect(url_for('results'))

#     return render_template('index.html')

# @app.route('/results', methods=['GET'])
# def results():
#     sentiments = list(collection.find())
    
#     # Add emojis based on the sentiment
#     for sentiment in sentiments:
#         if sentiment['sentiment'] == 'Positive':
#             sentiment['emoji'] = '😊'
#         elif sentiment['sentiment'] == 'Negative':
#             sentiment['emoji'] = '😞'
#         else:
#             sentiment['emoji'] = '😐'
    
#     sentiment_counts = {
#         'Positive': sum(1 for s in sentiments if s['sentiment'] == 'Positive'),
#         'Negative': sum(1 for s in sentiments if s['sentiment'] == 'Negative'),
#         'Neutral': sum(1 for s in sentiments if s['sentiment'] == 'Neutral'),
#     }

#     return render_template('results.html', sentiments=sentiments, sentiment_counts=sentiment_counts)

# @app.route('/delete/<id>', methods=['POST'])
# def delete(id):
#     collection.delete_one({'_id': ObjectId(id)})  # Convert id to ObjectId
#     return redirect(url_for('results'))

# @app.route('/clear', methods=['POST'])
# def clear():
#     collection.delete_many({})  # This will delete all records in the collection
#     return redirect(url_for('results'))

# if __name__ == '__main__':
#     app.run(debug=True)
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

app = Flask(__name__)

# MongoDB setup using environment variable for the URI
mongo_uri = os.getenv('MONGODB_URI')
if not mongo_uri:
    raise ValueError("MongoDB URI is not set. Please set the MONGODB_URI environment variable.")
client = MongoClient(mongo_uri)
db = client['sentiment_db']  # Replace with your database name if different
collection = db['sentiments']  # Replace with your collection name if different

# Lazy-load pre-trained BERT model for sentiment analysis
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        classifier = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")
    return classifier

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        if not text.strip():
            return render_template('index.html', error="Please enter valid text.")
        
        # Perform sentiment analysis
        classifier = get_classifier()
        result = classifier(text)[0]
        sentiment_label = result['label']
        sentiment_score = result['score']

        # Mapping BERT labels to simpler sentiments
        sentiment = 'Positive' if sentiment_label == 'POSITIVE' else 'Negative' if sentiment_label == 'NEGATIVE' else 'Neutral'
        
        # Store in MongoDB
        collection.insert_one({'text': text, 'sentiment': sentiment, 'score': sentiment_score})
        
        return redirect(url_for('results'))

    return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():
    sentiments = list(collection.find())
    
    # Add emojis based on the sentiment
    for sentiment in sentiments:
        if sentiment['sentiment'] == 'Positive':
            sentiment['emoji'] = '😊'
        elif sentiment['sentiment'] == 'Negative':
            sentiment['emoji'] = '😞'
        else:
            sentiment['emoji'] = '😐'
    
    sentiment_counts = {
        'Positive': sum(1 for s in sentiments if s['sentiment'] == 'Positive'),
        'Negative': sum(1 for s in sentiments if s['sentiment'] == 'Negative'),
        'Neutral': sum(1 for s in sentiments if s['sentiment'] == 'Neutral'),
    }

    return render_template('results.html', sentiments=sentiments, sentiment_counts=sentiment_counts)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})  # Convert id to ObjectId
    return redirect(url_for('results'))

@app.route('/clear', methods=['POST'])
def clear():
    collection.delete_many({})  # This will delete all records in the collection
    return redirect(url_for('results'))

if __name__ == '__main__':
    # This line will only run locally
    app.run(debug=True)
