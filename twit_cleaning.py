import twit_api
from twit_data import *
import string
import re as re
import nltk
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
data = tweets_df['content']
punctuation = string.punctuation
punct_list = punctuation
#removes all punctuation from the tweet
def remove_punctuation(tweet):
    translator = str.maketrans('','', punct_list)
    return tweet.translate(translator)

#remove all stopwords from the tweet
def remove_sw(tweet):
    sw = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
    'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
    'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
    'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
    'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
    'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
    'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
    'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
    'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
    't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
    'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
    'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
    'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
    'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
    "youve", 'your', 'yours', 'yourself', 'yourselves']
    STOPWORDS = set(sw)
    tweet = tweet.lower()
    tweet = " ".join([w for w in str(tweet).split() if w not in STOPWORDS])
    return tweet

#removing repeated characters
def remove_repeated_characters(tweet):
    return re.sub(r'(.)1+', r'1', tweet)

#remove numbers
def remove_numbers(data):
    return re.sub('[0-9]+','', data)

#removing URLs
def remove_URL(data):
    return re.sub('((www.[^s]+)|(https?://[^s]+))',' ',data)

#stemming
st = nltk.PorterStemmer()
def stemming(data):
    tweet = [st.stem(w) for w in data]
    return tweet

#lemmatizing
lm = nltk.WordNetLemmatizer()
def lemmatizing(data):
    tweet = [lm.lemmatize(w) for w in data]
    return tweet


tweets_df['content'] = tweets_df['content'].apply(lambda tweet: remove_sw(tweet))
tweets_df['content'] = tweets_df['content'].apply(lambda x: remove_punctuation(x))
tweets_df['content'] = tweets_df['content'].apply(lambda y: remove_repeated_characters(y))
tweets_df['content'] = tweets_df['content'].apply(lambda z: remove_URL(z))
tweets_df['content'] = tweets_df['content'].apply(lambda a: remove_numbers(a))
tweets_df['content'] = tweets_df['content'].apply(tokenizer.tokenize)
tweets_df['content'] = tweets_df['content'].apply(lambda lemm: lemmatizing(lemm))
tweets_df['content'] = tweets_df['content'].apply(lambda stem: stemming(stem))
print(tweets_df['content'])

