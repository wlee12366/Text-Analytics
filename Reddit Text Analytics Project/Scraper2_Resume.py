# -*- coding: utf-8 -*-

# https://www.reddit.com/r/redditdev/comments/8suiqu/scrape_all_submissions_and_comments_made_by_a/
# https://www.reddit.com/r/pushshift/comments/89pxra/pushshift_api_with_large_amounts_of_data/
# https://api.pushshift.io/reddit/comment/search?subreddit=gamereviews&limit=1000&sort=desc

import pandas as pd
import json
import requests
import re


def pushShifter(link, df, before = None):

    if (before is not None):
        suffix = '&before=' + str(before)
    
    print(suffix)
    link = link + suffix
        
    request = requests.get(link)

    json_dic = []

    json_dic = request.json()
    
    comment_dict= {'author': [], 
                'body': [],
                'created_utc': [], 'id': [], 
                'score': []}
    
    print (json_dic['data'][0]['author'])
    print (len(json_dic['data'][0]))

    for comment in json_dic['data']:
        comment_dict["author"].append(comment["author"])
        comment_dict["score"].append(comment["score"])
        comment_dict["id"].append(comment["id"])
        # comment_dict["permalink"].append(comment["permalink"])
        comment_dict["created_utc"].append(comment["created_utc"])
        comment_dict["body"].append(comment["body"])
        
    length = len(comment_dict['author'])
    
    data = pd.DataFrame(comment_dict)
    df = df.append(data)

    before = df.iloc[-1][2]
    return before, df, length


link = "https://api.pushshift.io/reddit/comment/search?limit=1000&sort=desc"


count = 0

before = df.iloc[-1][2]  

while len(df) < 2000000:
    before, df, length = pushShifter(link, df, before)
    count += 1
    print ("Iteration:", count)
    print (length)
    if (length < 1000):
        break

df = df.reset_index(drop=True)
     
 
