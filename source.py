import os
import tweepy
from pypexels import PyPexels
import random
import pandas as pd
import regex as re
import requests


#Your pexels API key
api_key = ''

#Your Twitter keys
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

py_pexel = PyPexels(api_key = api_key)

search_terms = ['nature','life','water','fire']
selected=[]
sources=[]
photogpher=[]

def load_ids():
    with open('ids.txt','a+') as used:
        used_ids = used.read().split()
     return used_ids   

def select(search_term):
    results = py_pexel.search(query = search_term,page=1,per_page=25)
    pid=[]
    photographer=[]
    photo_url=[]
    for img in results.entries:
        pid.append(img.id)
        photographer.append(img.photographer)
        photo_url.append(img.src.get('medium'))
        used_ids = load_ids()
    x = random.randint(0,25)
    if x<len(pid) and pid[x] not in used_ids:
        selected.append(pid[x])
        sources.append(photo_url[x])
        photogpher.append(photographer[x])
    else:
        while(x-1>0 and pid[x-1] in used_ids):
            x-=1
        selected.append(pid[x])

def select_photos():
    for search_term in search_terms:
        select(search_term)
    print('Pexels stuff done!') 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

replies_tmp=[]
replies=[]
#non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
for full_tweets in tweepy.Cursor(api.user_timeline,screen_name='Draw_This_',timeout=999999).items(7):
    for tweet in tweepy.Cursor(api.search,q='to:'+'Draw_This_',result_type='recent',timeout=999999).items(10):
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
    if k>=4:    
        for i in range(0,k):
            selected.append(reply_df['text'][i])
        select_photos()
    else:
        print("not enough words,selecting random")


def create_message():
    message="*test run*Today's words:"+', '.join(search_terms)
    message+="\nPhotos provided by pexels\n" 
    for photographer in photogpher:
        message+=photographer+'\n'
    print(message)
    return message

filenames=[]


def get_images(sources):
    for index in range(len(sources)):        
        filename = 'photo'+str(index)+'.jpg'
        request = requests.get(sources[index], stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            filenames.append(filename)        
        else:
            print("Unable to download image")


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
