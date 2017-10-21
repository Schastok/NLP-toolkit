# -*- coding: utf-8 -*-
'''
Created on Jan 31, 2015

@author: robin
'''
import re
from nltk.stem.isri import ISRIStemmer


class ArabicTokenizer():
    '''
    The Tokenizer gets trained using a stopwordlist and a trainingset(= [[rawsentences: string1,string2,string3,etc],[tokenized sentences: [token1, token2, token3], [token1, etc], etc]]
    '''
    def __init__(self, stopwordlist, trainingdata):
        self.stopwordlist = stopwordlist
        self.trainingdata = trainingdata
        test = []
        gold = []
        self.trainset = []
        for phrase in trainingdata[0]:
            test.append(word for word in self.tokenize(phrase))
        for phrase in trainingdata[1]:
            for word in phrase:
                gold.append(word)
        testset = set(test)
        goldset = set(gold)
        self.trainset = goldset.difference(testset)
        
    def tokenize(self, data):

        st = ISRIStemmer()
        pre_enclitics_1 = [u"ب", u"ل", u"ك", u"و", u"ف"]
        pre_enclitics_2 = [u"بال", u"كال"]
        post_enclitics_1 = [u"ي", u"ك", u"ه"]
        post_enclitics_2 = [u"ها", u"هم", u"هن", u"نا", u"ني", u"كم", u"وا", u"ون"]
        tokens= []
        tokenlist= []
        nodots = re.sub("([!،﴾٪﴿٫؛٬.؟])", " \g<1>", data)
        simple = nodots.split("  ")
        justsplit = []
        for token in simple:
            token = token.replace(" ", "")
            token = token.decode("utf-8")
            justsplit.append(token)
            if token in self.stopwordlist or token in self.trainset:
                tokens.append(token)
            else:                               
                if token[0:2] == u"ال":   #Artikel
                    tokens.append(u"ال")
                    tokens.append(token[2:])                        
                elif token[0:2] ==  u"لل":  #Präposition li + Artikel
                        tokens.append(token[0])
                        tokens.append(u"ال")
                        tokens.append(token[2:])                                   
                elif token[0:3] in pre_enclitics_2: #andere Präpos + Artikel
                        tokens.append(token[0])
                        tokens.append(u"ال")
                        tokens.append(token[3:])                       
                elif token[0] in pre_enclitics_1:   #Präpositionen 
                    if token[-2:] in post_enclitics_2: #mit enklitischen PersPron
                            tokens.append(token[0])
                            tokens.append(token[1:-2])
                            tokens.append(token[-2:])   
                    elif token[-1] in post_enclitics_1: #mit langen enklitischen Perspron
                            tokens.append(token[0])
                            tokens.append(token[1:-1])
                            tokens.append(token[-1])      
                    else:                               #ohne Perspron
                            tokens.append(token[0])
                            tokens.append(token[1:])                                  
                elif token[-2:] in post_enclitics_2: #lange enklitische Perspron
                            tokens.append(token[:-2])
                            tokens.append(token[-2:])                   
                elif token[-1] in post_enclitics_1: #kurze enklitische Perspron
                            tokens.append(token[:-1])
                            tokens.append(token[-1])   
                else:
                    tokens.append(token)  
        for i in tokens:
            try:
                if i[-1] == u"ت" and st.stem(token)[-1] != token[-1]: #ta-marbuta
                    i = i.replace(i[-1], u"ة")
                else:
                    pass
            except:
                pass
            tokenlist.append(i)
        return tokenlist



            
#________________________________________-Data-________________________________________

import cPickle
import nltk

stopwords = open("stopwords_ar.txt", "r")
quran = open ("quran-simple-clean.txt", "r")
finaldata = cPickle.load(open("finaldata", "rb"))

def readin(text):
    list = []
    for line in text:
        list.append(line)
    return list

def notag(list):
    gold = []
    for sentence in list:
        phrase = []
        for (word, tag) in sentence:
            phrase.append(word)
        gold.append(phrase)
    return gold


mytest = readin(quran)
mygold = notag(finaldata)


mytrainingdata = []
mytrainingdata.append(mytest[:5000])
mytrainingdata.append(mygold[:5000])

stop  = readin(stopwords)
mystopwords = []
for i in stop:
    mystopwords.append(i[:-2].decode("utf-8"))

#___________________________________________________Initialisation___________________________________________

mytokenizer = ArabicTokenizer(mystopwords, mytrainingdata)


