import nltk
import cPickle
import re


class ArabicTagger(trainingdata):
    def __init__:
        self.trainingdata = trainingdata
        self.pattern = [
           (u"(أ|ي|ت|ن).?..((و|ي)ن)?", "V"),  #Verben Praesens Stamm 1, 2 und 4
           (u"(أست|يست|تست|نست).?..((و|ي)ن)?", "V"), #Verben, Praesens Stamm 10
           (u"(أ|ي|ت|ن).?ت..((و|ي)ن)?", "V"), # Verben, Praesens Stamm 8
           (u"(أ|ي|ت|ن)ن...((و|ي)ن)?", "V"), #Verben, Praesens Stamm 9
           (u"(أ|ي|ت|ن)ت...((و|ي)ن)?", "V"), #Verben, Praesens Stamm 5
           (u"(أ|ي|ت|ن)ت?.ا..((و|ي)ن)?", "V"),#Verben, Praesens Stamm 3,6
           (u"...(ت|نا|تا|تما|وا|ن|تم|تن)", "V"),#Verben Prät Stamm 1
           (u"(ت|أ|ا|ان|است).?..(ت|نا|تا|تما|وا|ن|تم|تن)?", "V"), #Verben Praeteritum alle Stämme ohne 3, 5, 6 und 8
           (u"ت?.ا..(ت|نا|تا|تما|وا|ن|تم|تن)", "V"), #Verben Präteritum Staemme 3 und 6
           (u"ا.ت..(ت|نا|تا|تما|وا|ن|تم|تن)", "V"),#Verben Präteritum Stamm 8
           (u"([!،﴾٪﴿٫؛٬.؟])", "-")] 

        
        self.default_tagger = nltk.DefaultTagger('N')
        self.regexp_tagger = nltk.RegexpTagger(pattern, backoff=default_tagger)
        self.uni=nltk.UnigramTagger(self.trainingdata, backoff=regexp_tagger)
        self.bigr=nltk.BigramTagger(self.trainingdata, backoff=uni)
        self.trigr = nltk.TrigramTagger(self.trainingdata, backoff=bigr)
        self.transform = train_brill(self.trainingdata, trigr)
        pass
    
    def train_brill(traindata, backoff): #function to train the transformation based brill-tagger. if the template collection "fntbl37" is not working, find its content in the comment block 
    templ = nltk.tag.brill.fntbl37()
    
    #additional templates i found useful for arabic:
    templ.append(nltk.tag.brill.Template(nltk.tag.brill.Pos([-3, -2, -1]), nltk.tag.brill.Word([0])))
    templ.append(nltk.tag.brill.Template(nltk.tag.brill.Pos([-3, -2, -1]), nltk.tag.brill.Word([-1])))
    templ.append(nltk.tag.brill.Template(nltk.tag.brill.Pos([1, 2, 3, 4])))
    
    trainer = nltk.tag.brill_trainer.BrillTaggerTrainer(initial_tagger = backoff, templates = templ, trace=0, deterministic=None)
    brill_tagger = trainer.train(traindata)
    return brill_tagger  


    def tag(self, word):
        return self.transform.tag(word)









'''templ = [
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Word([1]), nltk.tag.brill.Word([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([-1]), nltk.tag.brill.Word([0]), nltk.tag.brill.Word([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Word([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Word([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Word([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Word([-2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([1, 2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([-2, -1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([1, 2, 3])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([-3, -2, -1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Pos([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Pos([-2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Pos([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0]), nltk.tag.brill.Pos([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([0])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([-2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Word([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-1]), nltk.tag.brill.Pos([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1]), nltk.tag.brill.Pos([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-1]), nltk.tag.brill.Pos([-2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1, 2, 3])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1, 2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-3, -2, -1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-2, -1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1]), nltk.tag.brill.Word([0]), nltk.tag.brill.Word([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1]), nltk.tag.brill.Word([0]), nltk.tag.brill.Word([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-1]), nltk.tag.brill.Word([-1]), nltk.tag.brill.Word([0])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-1]), nltk.tag.brill.Word([0]), nltk.tag.brill.Word([1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([-2]), nltk.tag.brill.Pos([-1])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1]), nltk.tag.brill.Pos([2])),
            nltk.tag.brill.Template(nltk.tag.brill.Pos([1]), nltk.tag.brill.Pos([2]), nltk.tag.brill.Word([1]))]'''
