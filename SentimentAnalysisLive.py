import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class Twitter(object): 

	def __init__(self): 
		API_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		API_secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		try: 
			self.auth = OAuthHandler(API_key, API_secret_key) 
			self.auth.set_access_token(access_token, access_token_secret) 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(w+:S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 5,lang = 'en'): 
		tweets = [] 

		try:  
			fetched_tweets = self.api.search(q = query, count = count, lang = 'en') 
			for tweet in fetched_tweets: 
				parsed_tweet = {} 
				parsed_tweet['text'] = tweet.text 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
				if tweet.retweet_count > 0: 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet)  
			return tweets 
		except tweepy.TweepError as e: 
			
			print("Error : " + str(e)) 

def main():
    api = Twitter() 
    keyword=input("Enter the Search keyword:\t")
    keyvalue=input("Enter the number of tweets:\t")
    tweets = api.get_tweets(query = keyword, count = keyvalue, lang = 'en')
    if len(tweets) > 0 :
        positiveTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        print("Percentage of Positive tweets: {} %".format(100*len(positiveTweets)/len(tweets))) 
        negativeTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        print("Percentage of Negative tweets: {} %".format(100*len(negativeTweets)/len(tweets)))
        print("Percentage of Neutral tweets: {} % ".format(100*(len(tweets) - len(negativeTweets) - len(positiveTweets))/len(tweets)))
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%") 
        print("\nPRINTING FIVE POSITIVE TWEETS:\n") 
        for tweet in positiveTweets[:5]:
            print(tweet['text'])

        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("\nPRINTING FIVE NEGATIVE TWEETS:\n") 
        for tweet in negativeTweets[:5]: 
            print(tweet['text']) 
		
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("\nPRINTING FIVE NEUTRAL TWEETS:\n") 
        for tweet in tweets[:5]: 
            print(tweet['text'])

    else:
        print(" No tweets on your given keyword")   
    
if __name__ == "__main__": 
	 
	main() 
