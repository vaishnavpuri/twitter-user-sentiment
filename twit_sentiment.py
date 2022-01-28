from twit_cleaning import *
from twit_data import *
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
nltk.download('vader_lexicon')

def tweet_sentiment(tweet):
    tb = TextBlob(str(tweet))
    score = tb.sentiment.polarity
    #print(score)
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
        
tweets_df['tweet_sentiment'] = tweets_df['content'].apply(lambda tweet: tweet_sentiment(tweet))

#graphic
plt.clf()
tweets_df['tweet_sentiment'].value_counts().plot(kind= 'barh')
plt.title('Sentiment of @'+handles+' Tweets')
plt.xlabel('Frequencey of Tweet Sentiment')
plt.show()



