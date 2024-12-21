from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def vader_sentiment(self, text: str):
        score = self.analyzer.polarity_scores(text)
        return score

    def textblob_sentiment(self, text: str):
        blob = TextBlob(text)
        return blob.sentiment
