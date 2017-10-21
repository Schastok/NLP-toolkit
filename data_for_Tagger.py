# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2014

@author: robin
'''

import codecs
import cPickle
import re


def sentencer(l): # Uses the Verse numbers to set the sentence borders
    counter = 1
    phrase = []
    result = []
    for [x, y, z] in l[:-1]:  
        if int(x) == counter:
            phrase.append((y, z))
        else:
            result.append(phrase)
            phrase = phrase[:]
            phrase = []
            phrase.append((y,z))
            counter = int(x)
    return result



def transcriptor(phrase): # transcripts the words using a dictionary with encodings
    codingtab = codecs.open("encoding.txt", "r", encoding="utf-8")
    codetext = codingtab.read()
    codetext = codetext.replace(" + ", "")
    cwords = codetext.split()
    codedict = {}
    for i in range(0,len(cwords)):
        if i%4 == 1:
            codedict[cwords[i+1]]= unichr(int(cwords[i-1]))
    resultlist = []
    errorlist = []
    for (word, tag) in phrase:
        for char in word:
            try:
                word = word.replace(char, codedict[char])
            except:
                tag = "$"+tag  
        if tag[0] != "$":
            resultlist.append((word, tag))
        else: 
            errorlist.append((word, tag))
#    print u"{} : {}".format(word, tag)
    return resultlist


def devok(taggedlist): #removes the "harakat" (short vowel marks)
    novok = []
    for (word, tag) in taggedlist:
        for char in word:
            if char == unichr(1648):
                word = word.replace(char, "")
            elif char == unichr(1656):
                word = word.replace(char, "")
            elif char == unichr(1649):
                word = word.replace(char, unichr(1575))
            for i in range(1611, 1620):
                if char == unichr(i):
                    word = word.replace(char, "")
            for i in range(1659, 1773):
                if char == unichr(i):
                    word = word.replace(char, "")  
        novok.append((word, tag))
    return novok


def replacer(list): #sets only one tag for the conjunction "fa"
    final = []
    for sentence in list:
        phrase = []
        for (word, tag) in sentence:
            if tag == "REM" or tag =="RSLT":
                tag = "CONJ"
            phrase.append((word, tag))
        final.append(phrase)
    return final


if __name__ == "__main__":
    
    # creating a file with only words, tags and verse numbers
    file = open("quran.txt", "r")
    neu = open("tags.txt", "w")
    for line in file:
        if re.match("\(.+\)\s(.+?)\s(.+?)\s.*", line):
            neu.write(re.sub("\(\d+:(\d+).+?\)\s(.+?)\s(.+?)\s.*", "\g<1> \g<2> \g<3>", line))
        

    # reading in the data and creating the needed nested lists
    file = open("tags.txt", "r")
    tagged = []
    for line in file:
        tagged.append(line.split())
    phrase = []

    sentenced = sentencer(tagged)    

    # transcription, de-vocalisation and replacement of unnecessary tags
    unicodelist = []
    for i in sentenced:
        unicodelist.append(transcriptor(i))
    unvokalized = []
    for i in unicodelist:
        unvokalized.append(devok(i))
    finaldata = replacer(unvokalized)

    # creating training and testdata
    print len(finaldata)
    trainingdata = finaldata[1001:]
    testdata = finaldata[:1000]
    cPickle.dump(testdata, open("testdata", "wb"), protocol=1)
    cPickle.dump(trainingdata, open("trainingdata", "wb"), protocol=1)
    cPickle.dump(finaldata, open("finaldata", "wb"), protocol=1)
