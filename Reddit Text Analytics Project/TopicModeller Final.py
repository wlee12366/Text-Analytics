# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:08:57 2018
"""
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized
    

for key in ["NHL", "Destiny"]:
    doc_complete = []
    print (key)
    
    if len(dfColl[key]) == 0:
        continue;
    
    for j in range(0, len(dfColl[key])):
        if  not np.isnan(dfColl[key].iloc[j][8]): # Instead of looking at all body, see if we extracted from it first to see if compound is nan
            doc_complete.append(dfColl[key].iloc[j][1].rstrip("]").lstrip("[").strip("'").strip())
        # https://stackoverflow.com/questions/3704918/python-way-to-restart-a-for-loop-similar-to-continue-for-while-loops
        else:
            continue
        
    if j == len(dfColl[key]) - 1 and len(doc_complete) == 0:
            continue;
        
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    
    doc_clean = [clean(doc).split() for doc in doc_complete]  
    
    removeKey = [clean(key).split()]  
    removeKey = removeKey[0]
    
    """
    Doesn't remove the second word in a title for some reason with "remove"
    # https://stackoverflow.com/questions/29771168/how-to-remove-words-from-a-list-in-python
    for i in range(0, len(doc_clean)):
        for word in doc_clean[i]:
            if word in removeKey:
                doc_clean[i].remove(word)
    """
    
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    # Replace is an important function
    for i in range(0, len(doc_clean)):
        for j, word in enumerate(doc_clean[i]):
            if word in removeKey:
                doc_clean[i][j] = word.replace(word, "")
        doc_clean[i] = list(filter(None, doc_clean[i]))
            
    
    # for i in range(0, len(doc_clean)):
    #    doc_clean[i].remove("".join(key.split()).lower())
    
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    
    # Running and Trainign LDA model on the document term matrix.
    if len(doc_clean) <= 100:
        ldamodel = Lda(doc_term_matrix, num_topics=4, id2word = dictionary, passes = 50)
        print(ldamodel.print_topics(num_topics=4, num_words= 5))
    elif len(doc_clean) > 100 and len(doc_clean) <= 400: 
        ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes = 50)
        print(ldamodel.print_topics(num_topics= 5, num_words= 5))
    elif len(doc_clean) > 400 and len(doc_clean) < 700: 
        ldamodel = Lda(doc_term_matrix, num_topics = 6, id2word = dictionary, passes = 50)
        print(ldamodel.print_topics(num_topics= 6, num_words= 5))
    else:
        ldamodel = Lda(doc_term_matrix, num_topics = 6, id2word = dictionary, passes = 50)
        print(ldamodel.print_topics(num_topics = 6, num_words= 5))
    
# http://miriamposner.com/blog/very-basic-strategies-for-interpreting-results-from-the-topic-modeling-tool/
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda

    