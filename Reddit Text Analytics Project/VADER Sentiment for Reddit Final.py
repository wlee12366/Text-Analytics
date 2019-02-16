# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 23:41:24 2018

Note to Self: Optimize for faster processing. Whenever I'm not so squeezed for time, I should better document
what the code does. I can also probably organize it better when I come back to optimize.

IMPORTANT:
    
Make sure to create a dictionary for all dfs. Each df should hold reviews or comments for one game.

Have a unique df for each game contained which will be aggregrated into a dictionary. We can iterate through the dictionary
in order to access through each df, thereby automating the entire process. See the GroupMe message I wrote earlier
for more details.

"""

import pandas as pd
import numpy as np
import json
import math
import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_scores(sentence):
   snt = analyser.polarity_scores(sentence)
   print("{:-<40} {}".format(sentence, str(snt)))
   
   return snt
   

def keepSplit(inString, delimiters = ['.', '?', '!']):
    outStrings = []
    strBuffer = ""
    for c in inString:
        strBuffer += c;
        if c in delimiters:
            outStrings.append(strBuffer)
            strBuffer = ""
    if len(strBuffer) > 0:
        outStrings.append(strBuffer)
    return outStrings
   

notSet = "[^a-zA-Z]"


for key in dfColl.keys():

    dfColl[key]["pos"] = np.nan
    dfColl[key]["neu"] = np.nan
    dfColl[key]["neg"] = np.nan
    dfColl[key]["compound"] = np.nan
    dfColl[key]["sentiment"] = np.nan
    dfColl[key]["examined string"] = np.nan
    
    for j in range(0, len(dfColl[key])):
        propCheck = True
        stringExam = []
        stringPos = []
        stringCom = (dfColl[key].iloc[j][1]) #
        
        stringSep = keepSplit(stringCom)
            
        strExValid = [] # Valid, extra non-keyword containing strings to extract with keyword containing strings

        if len(stringSep[-1]) == 0:
            stringSep.pop()
            
        for i, sentence in enumerate(stringSep):
            if len(re.findall(notSet + key + notSet, sentence,re.IGNORECASE)) > 0:
                stringExam.append(sentence)
                stringPos.append(i)

        
        if len(stringCom) / len(stringSep) < math.floor((math.sqrt(len(stringSep)) - 1) * 10) / 10 and len(stringSep) <= 10:
            propCheck = False
            snt = sentiment_scores("")
        elif len(stringCom) == 2 and len(stringSep) > 10 and len(stringSep) < 20:
            propCheck = False
            snt = sentiment_scores("")
        elif len(stringCom) / len(stringSep) < .1 and len(stringSep) >= 20:
            propCheck = False
            snt = sentiment_scores("")

        
        if propCheck:
            for i in stringPos:
                if i != 0:
                    if not(i - 1 in strExValid):
                        strExValid.append(stringSep[i - 1])
                      
                if not(i in strExValid):
                    strExValid.append(stringSep[i])
                    
                if not (i >= len(stringSep) - 1):
                    if not(i + 1 in strExValid):
                        strExValid.append(stringSep[i + 1])
                        
            if len(stringSep) <= 3:
                dfColl[key]["examined string"].iloc[j]  =  str(stringExam).rstrip("]").lstrip("[").strip("'").strip()
                snt = sentiment_scores(str(stringExam))
            else:
                strExValid = str(". ".join(strExValid))
                dfColl[key]["examined string"].iloc[j]  =  strExValid
                snt = sentiment_scores(strExValid)     
        

        # Access game DF, column, and iterates through all rows of game DF
        if snt["compound"] != 0.0: # if compound = 0, it's a trash post. Ex: "&gt;Dark Souls Chest ahead"
            # Ex: But Dark Souls isn't Assassin's Creed They're not the same game
            # {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
            dfColl[key]["pos"].iloc[j] = snt["pos"]
            dfColl[key]["neu"].iloc[j] = snt["neu"]
            dfColl[key]["neg"].iloc[j] = snt["neg"]
            dfColl[key]["compound"].iloc[j] = snt["compound"]
        else:
            dfColl[key]["pos"].iloc[j] = np.nan
            dfColl[key]["neu"].iloc[j] = np.nan
            dfColl[key]["neg"].iloc[j] = np.nan
            dfColl[key]["compound"].iloc[j] = np.nan
            snt["compound"] = np.nan
        
        if  np.isnan(snt["compound"]):
            dfColl[key]["sentiment"].iloc[j] = np.nan
        elif snt["compound"] < -.1:
            dfColl[key]["sentiment"].iloc[j] = "neg"
        elif snt["compound"] > .1:
            dfColl[key]["sentiment"].iloc[j] = "pos"
        else:
            dfColl[key]["sentiment"].iloc[j] = "neu"        
    

    

print_sentiment_scores()



"""
https://www.reddit.com/r/MachineLearning/comments/8uuoc8/d_dont_common_sentiment_analysis_strategies_seem/

Solved Issues:
    
print (len(re.findall("ARMA",
               "I might be weird about this but I also like how rarity has little to do with ship usefulness, even the lowest rarity units are useful for something and some of the strongest high rarity ships are farmable at low rates from maps.", re.IGNORECASE)) > 0)

Matchall finds "ARMA" in "fARMAble"


 "have you tried BR in arma?  its really bad.
 i did it for alittle awhile but all those milsim restrictions put such a huge ceiling on how you can play the game. 
 sitting in a bush was a million times more effective than any other playstyle just because of how janky the movement was. 
 pubg is definitely a mix of realism and game mechanics to encourage a more aggressive playstyle. 
 i definitely wouldnt call pubg "milsim", but it is definitely drawing elements from the genre."
 {'neg': 0.048, 'neu': 0.694, 'pos': 0.259, 'compound': 0.9719}
 
to
 
 "have you tried BR in arma?  its really bad.
 i did it for alittle awhile but all those milsim restrictions put such a huge ceiling on how you can play the game"
 {'neg': 0.068, 'neu': 0.762, 'pos': 0.171, 'compound': 0.5652}
 
  It's account for it here and strip out the part that's relevant but even then, sentiment analysis isn't perfect,
 even though to a human it's clear it's a negative comment. Overall compound score decreases but it's classified as positive
 still
 
 How do I pull out a limited amount of text to capture only the relevant parts?
 
 1. Go by proportion for full-on critic reviews.
 2. Go by before and after for smaller reviews and comments.
 3. If less than or equal to 3 sentences, pick only one sentence.

"""
