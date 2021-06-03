import json
import csv
import tweepy
import re


""""
AIM: TO WRITE A GENERAL TWEET MINING SCRIPT, IRRESPECTIVE OF HASHTAGS
INPUTS: consumer key and secret, access token and secret

RESULT: saves the information in a csv file
"""

def search_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    #creating an authentication method, for accessing twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #initialize tweepy API
    api = tweepy.API(auth)
    
    #next we get the name of the file we want to copy to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
    print(fname)
    
    #open the spreadsheet file we want to write to
    with open(f"{fname}.csv", 'w') as file:
        
        hashtagfile = csv.writer(file) 
        #The csv. writer() method returns a writer object 
        #which converts the user's data into delimited strings 
        #on the given file-like object.
        
        #now we write the header row into the spreadsheet file
        hashtagfile.writerow(['tweetID','timestamp','tweet_text','user_name''retweet_count','like_count','hashtag','followers_count'])
        
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+'-filter:retweets AND -filter:replies',
                                  lang="en", tweet_mode='extended').items(500):
            hashtagfile.writerow([tweet.id,tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), tweet.retweet_count, tweet.favorite_count, [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])


consumer_key = '############' #input('Consumer Key: ')
consumer_secret = '##################' #input('Consumer Secret: ')
access_token = '##############' #input('Access Token: ')
access_token_secret = '##############' #input('Acess Token Secret: ')

hashtag_phrase = input('Hashtag Phrase: ')

if __name__ == '__main__':
    search_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
