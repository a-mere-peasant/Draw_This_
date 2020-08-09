import tweepy
import pexels
import random
import pandas as pd
import regex as re
import requests


search_terms = ['nature','life','water','fire']
selected = []
sources = []
photographer = []

def load_ids():
    with open('ids.txt','a+') as used:
        used_ids = used.read().split()
    return used_ids   

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

replies_tmp=[]
replies=[]
def get_replies():   
    for full_tweets in tweepy.Cursor(api.user_timeline,screen_name='Draw_This_',timeout=999999).items(1):
        for tweet in tweepy.Cursor(api.search,q='to:'+'Draw_This_',result_type='recent',timeout=999999).items(100):
            if (hasattr(tweet, 'in_reply_to_status_id_str') and tweet.favorite_count>0):
                if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
                    replies.append(tweet.id)
                #print("Tweet :",full_tweets.text.translate(non_bmp_map))
                for ids in replies_tmp:
                    print(ids)
                    replies.append(ids)
                replies_tmp.clear()

def get_words():
    cols=['id','text','favorite_count']
    all_reps=[]
    for ids in replies:
        reply_data={}
        reply=dict(vars(api.get_status(ids)))
        if (len(re.findall(r'\w+', reply['text'])) == 1):
                reply_data[col]=reply[col]
        all_reps.append(reply_data)
    reply_df = pd.DataFrame(all_reps,columns=cols)
    reply_df.sort_values(by=['favorite_count'],inplace=True,ascending=False)
    k=len(reply_df)
    if  4-k > 0:
         for i in range(0,k):
            search_terms.append(reply_df['text'][i])
         select_photos()
         for i in range(k,4):
            random_photos = py_pexel.random(per_page = 4-k)
            for random_photo in random_photos.entries:
                selected.append(random_photo.id)
    else:    
        for i in range(0,4):
            search_terms.append(reply_df['text'][i])
        select_photos()

def create_message():
    message="*test run*Today's words:"+', '.join(search_terms)
    message+="\nPhotos provided by pexels\n" 
    for photographer in photogpher:
        message+=photographer+'\n'
    print(message)
    return message

def tweet_message():
    get_words()
    select_photos()
    message = create_message()
    get_images(sources)
    media_ids = []
    for filename in filenames:
         res = api.media_upload(filename)
         media_ids.append(res.media_id)

    api.update_status(status=message, media_ids=media_ids)
    print("Updated Status!")
    for filename in filenames:   
        os.remove(filename)
    print("Removed photos from local storage!")    

tweet_message()
