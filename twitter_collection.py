#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:33:09 2023

@author: fnurakeshwer
"""

def fetch_sentiment_using_SIA(text):
    sid = SentimentIntensityAnalyzer()
    polarity_scores = sid.polarity_scores(text)
    return 'neg' if polarity_scores['neg'] > polarity_scores['pos'] else 'pos'

def remove_pattern(text, pattern_regex):
    r = re.findall(pattern_regex, text)
    for i in r:
        text = re.sub(i, '', text)
    
    return text 


import numpy as np 
import pandas as pd 
# =============================================================================
# import matplotlib.pyplot as plt 
# =============================================================================
# =============================================================================
# import seaborn as sns
# =============================================================================
import re
# =============================================================================
# import time
# =============================================================================
# =============================================================================
# import string
# =============================================================================
import warnings
# =============================================================================
# import yfinance as yf
# import pandas as pd 
# import pandas_ta as pta
# import requests
# import statistics as st
# # for all NLP related operations on text
# =============================================================================
import nltk
from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# =============================================================================
# from nltk.stem import WordNetLemmatizer
# from nltk.stem.porter import *
# from nltk.classify import NaiveBayesClassifier
# from wordcloud import WordCloud
# 
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import f1_score, confusion_matrix, accuracy_score
# from sklearn.svm import SVC
# from sklearn.naive_bayes import GaussianNB
# 
# =============================================================================
#from reading_database import read_database

import reading_database

# To consume Twitter's API
import tweepy
from tweepy import OAuthHandler 
import random
# To identify the sentiment of text
# from textblob import TextBlob
# from textblob.sentiments import NaiveBayesAnalyzer
# from textblob.np_extractors import ConllExtractor

# For Deploy
# =============================================================================
# import pickle
# from sklearn.feature_extraction.text import CountVectorizer 
# from sklearn.pipeline import make_pipeline
# from nltk.tokenize import RegexpTokenizer
# from dash import dash_table, Dash 
# import pandas as pd
# 
# =============================================================================
# ignoring all the warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# downloading stopwords corpus
nltk.download('stopwords')
nltk.download('wordnet')    
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('movie_reviews')
nltk.download('punkt')
nltk.download('conll2000')
nltk.download('brown')
stopwords = set(stopwords.words("english"))

# for showing all the plots inline


# consumer_key = 'gqW9birtLMLNRTjgv1BOre61N'
# consumer_secret = 'vnKkNrt8BOoAHqSeKPYxQ698e2vYCuAFzgSexBmZ7ZCjHl0LKq'
# access_token = '3349806612-rV18nciBtRlU5L9b19YjKJuZVtqK1fqgbgGimg0'
# access_token_secret = 'zEPMLK1l7pq8S6TWnkM4a6udCkIB77YjKeK3R6UduhRwq'


keys=[{"CONSUMER_KEY":'NnNfUZ3hhjHviw2rYQMThKGoj',
     "CONSUMER_SECRET":'WGeCxoYVtljpp0cvaqQGLhoKXZGZ9WjmJUTW0exfvSJq5OUAZd',
     "ACCESS_TOKEN":'3349806612-YqG9wIpFjr2rEIytz01ZW7FuRzYCmcSjbPTwjrC',
     "ACCESS_SECRET":'FOBlKfawUAEvL5cHZRbkSnIEAVbWjcu949yXb52gN0aiv'
     },
     {"CONSUMER_KEY":'FCyrBzfEDuRaIhNj5ajzb5UIZ',
     "CONSUMER_SECRET":'s6sgFNhmUtsB1wCPx87fRVQeSeJX5fvRnzT9M0trtMq1nI1Cy0',
     "ACCESS_TOKEN":'3349806612-XZ1Mi4Q5EVi4IHY5gvHUArSuJyukt5cFtkEMqLr',
     "ACCESS_SECRET":'ocW3tgOWDX11uy357kounrlq08qqe3Ryk5bCHy64W02Ja'
     },
     
     {"CONSUMER_KEY":'6QQrFvMOp6bdecTst8NZxLtwY',
     "CONSUMER_SECRET":'qe2yMsGa6DGdRIG5dbgNn1vCBMTcjmkBEaLap165wzXlEEdTBP',
     "ACCESS_TOKEN":'3349806612-dtI4E9XOPv3dkwoga11Skaz6NFda3butD3uvkqX',
     "ACCESS_SECRET":'JE1kBSFpPgd3x6QRPNuFs7yngUyWUsn3mUWOsj8BabNnH'
     },
     
     
     {"CONSUMER_KEY":'AJivM0VJ8G8F8ofqhuOWMWQzW',
     "CONSUMER_SECRET":'30q2CvgobQc0ysymGSGlxfXhV60Rx3PpabdtieMQ8s6uJN2AXY',
     "ACCESS_TOKEN":'3349806612-1TTwdHjTFxZBjMaNMUD7RXM65EISr5iVfNABhyA',
     "ACCESS_SECRET":'Fex1MSmSbxNXGRZovJS0MO0gd16rmItxs9uwW0gMjYlzt'
     },
     
     {"CONSUMER_KEY":'tvCUDiQfPAfkuijonMCvxqRjQ',
     "CONSUMER_SECRET":'JmpBlQIleMn2Vcj6JMxx6e2V06kAdvPY1cgEjpY0RscBl64nAR',
     "ACCESS_TOKEN":'3349806612-ZzhZqnRQqOU8eaRHgtnMx2hUGXn0bSUahfst4Vz',
     "ACCESS_SECRET":'xlxFIec64gHJKsDEBgL4qqc5DQWq9O7tDUQSi0C0xY2Lz'
     },
     
     {"CONSUMER_KEY":'ZJjp0jOe8O2dUduD3HJGTylEJ',
     "CONSUMER_SECRET":'FxfxfDIWM4Wy1jOTLY3PpBXS9FZuuoILEov4IP4SxDb41DS2ZE',
     "ACCESS_TOKEN":'3349806612-IJLKk9PJICLvtB6knDE5W4UJmanribDEqdSP053',
     "ACCESS_SECRET":'4Oo0pTFW4CM95dMbLK1UckBouYfa3nCY6ZGhoaPVhMUhU'
     },
     
     
     ]



# consumer_key= 'dlzVloCpxvjxddNsNgnl706TJ'
# consumer_secret= 'askzY1OdHCst7ueFN6SOrlf9t3asizBT3avjJFjZAQyCiMPZyK'
# access_token = '3349806612-TFobMhpe7TOnTfxrkGM5kKr2FlsQ0VPLg7mzit9'
# access_token_secret = 'ZdGi6eKbewLzD87NmD82FxrcPSiUG1jBvOwdMCQLgS1V7'
class TwitterClient(object): 
    def __init__(self): 
        #Initialization method. 
        try:
            random_index = random.randint(0,len(keys)-1)
            auth = tweepy.OAuthHandler(keys[random_index]["CONSUMER_KEY"], keys[random_index]["CONSUMER_SECRET"])
            auth.set_access_token(keys[random_index]["ACCESS_TOKEN"], keys[random_index]["ACCESS_SECRET"])
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
        except tweepy.errors.TweepyException as e:
            print(f"Error: Tweeter Authentication Failed - \n{str(e)}")
            
        except tweepy.errors.TweepyException as e:
            print(f"Error: Tweeter Authentication Failed - \n{str(e)}")

    def get_tweets(self, query, maxTweets = 1000):
        #Function to fetch tweets. 
        # empty list to store parsed tweets 
        tweets = [] 
        sinceId = None
        max_id = -1
        tweetCount = 0
        tweetsPerQry = 100

        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry)
                    else:
                        new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    parsed_tweet = {} 
                    parsed_tweet['tweets'] = tweet.text 

                    # appending parsed tweet to tweets list 
                    if tweet.retweet_count > 0: 
                        # if tweet has retweets, ensure that it is appended only once 
                        if parsed_tweet not in tweets: 
                            tweets.append(parsed_tweet) 
                    else: 
                        tweets.append(parsed_tweet) 
                        
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id

            except tweepy.errors.TweepyException as e:
                # Just exit if any error
                print("Tweepy error : " + str(e))
                break
        
        return pd.DataFrame(tweets)



def reading_tweets(df_m1):
    sentiment_results_of_companies = []
    for i in df_m1['stockname']: 
        print(i, "company is searching on twitter")
    
        twitter_client = TwitterClient()
    
        # calling function to get tweets
        tweets_df = twitter_client.get_tweets(i, maxTweets=10)
        print(f'tweets_df Shape - {tweets_df.shape}')
        if (tweets_df.shape[1]==0):
            tweets_df["tweets"] = ["No_tweet_for_this_company"]
    
    
        sentiments_using_SIA = tweets_df.tweets.apply(lambda tweet: fetch_sentiment_using_SIA(tweet))
        pd.DataFrame(sentiments_using_SIA.value_counts())
    
        tweets_df['sentiment'] = sentiments_using_SIA
        #tweets_df.head()
    
        tweets_df['tidy_tweets'] = np.vectorize(remove_pattern)(tweets_df['tweets'], "@[\w]*: | *RT*")
        #tweets_df.head(10)
    
        cleaned_tweets = []
    
        for index, row in tweets_df.iterrows():
            # Here we are filtering out all the words that contains link
            words_without_links = [word for word in row.tidy_tweets.split() if 'http' not in word]
            cleaned_tweets.append(' '.join(words_without_links))
    
        tweets_df['tidy_tweets'] = cleaned_tweets
        tweets_df = tweets_df.dropna()
        #tweets_df.head(10)
        sentiments_using_SIA2 = tweets_df.tidy_tweets.apply(lambda tweet: fetch_sentiment_using_SIA(tweet))
        pd.DataFrame(sentiments_using_SIA2.value_counts())
        
        positive_tweets = []
        negative_tweets = []
        for j in sentiments_using_SIA2:
            if j == 'pos':
                positive_tweets.append(j)
            else:
                negative_tweets.append(j)
        
        ng_tweets = len(negative_tweets)
        if (ng_tweets == 0):
            ng_tweets = ng_tweets+1 
        if (len(positive_tweets)*0.80)/(ng_tweets) > 0:
            result ='postive'
        else:
            result ='negative'
        
        sentiment_results_of_companies.append(result)
       
            
    df_sentiment = pd.DataFrame(sentiment_results_of_companies)
    df_sentiment['sentiment'] = df_sentiment
    df_sentiment = df_sentiment.iloc[: , 1:]
    df_m1['Sentiments'] = sentiment_results_of_companies

    return df_m1

