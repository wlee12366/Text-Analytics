# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 00:14:18 2018
"""

import pandas as pd
import json
import requests
import re

# Back up to Sept 1

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

def keyword(df):
    return (len(re.findall(notSet + game + notSet, df,re.IGNORECASE)) > 0)


listGames = ["Dark Souls", "Madden", "Skyrim", "Oblivion", "ARMA", "Skylines", "Overcooked",
             "Dishonored", "Rimworld", "Dying Light", "God of War", "Black Ops", "Papers Please", "NHL", "Destiny", "Zelda", 
             "The Last of Us", "Halo", "Borderlands", "Saints Row", "The Division", "Hellblade", "Burnout",
             "Just Cause", "Stardew", "MvC Infinite", "Shadow of War", "Dead Rising", "Cuphead", "Overwatch",
             "Papers Please", "The Witness", "Metal Gear Survive", "Firewatch", "Skater", "No Man's Sky",
             "Sunset Overdrive", "Quantum Break", "Riptide", "Viva Pinata"]
listSubreddits = ["https://api.pushshift.io/reddit/comment/search?subreddit=gamereviews&limit=1000&sort=desc",
                  "https://api.pushshift.io/reddit/comment/search?subreddit=games&limit=1000&sort=desc"]
notSet = "[^a-zA-Z]"

dfColl = {}

count = 1 # Initialize


for link in listSubreddits:
    print (link)
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
    
    df = pd.DataFrame(comment_dict)
    
    before = df.iloc[-1][2]
    
    while len(df) < 1000000:
        before, df, length = pushShifter(link, df, before)
        count += 1
        print ("Iteration:", count)
        print (length)
        if (length < 1000):
            break


df = df.reset_index(drop=True)


count = 0

for game in listGames:
    count += 1
    print ("Game:", game)
    print ("Iteration:", count)
    mask = df['body'].map(keyword)
    dfColl[game] = df[mask]
  
