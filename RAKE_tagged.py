
import numpy as np
import nltk
import string
import operator
from nltk.stem import WordNetLemmatizer


class RAKE_tagged():
    '''
    This class applies the RAKE (Rapid Automatic Keyword Extraction) algorithm after filtering and stemming the possible candidates.
    it can be used for any language by passing the taggers, tokenizers and stemmers to the initialisation
    '''
    def __init__(self, no_of_keywords, stopwords='auto', pos =['N'], tokenizer='auto', tagging='auto', stemming='auto'):
        self.pos = pos
        self.nkey = no_of_keywords
        self.stopwords = stopwords
        self.tokenizer = tokenizer
        self.tagging = tagging
        self.lemma = stemming


        pass
    
    def isPunct(self, word):
        return len(word) == 1 and word in string.punctuation

    def isNumeric(self, word):
        try:
            float(word) if '.' in word else int(word)
            return True
        except ValueError:
            return False
            
    def manage_params(self):
        if type(self.stopwords) == list:
            pass
        elif self.stopwords == "auto":
            self.stopwords = set(nltk.corpus.stopwords.words())
        else:
            self.stopwords = []
            
        if self.tokenizer == 'auto':
            self.tokenizer = nltk.word_tokenize
        else:
            pass
        
        if self.tagging == 'auto':
            self.tagging = nltk.pos_tag
        else:
            pass
        
        if self.lemma == 'auto':
            lemmatizer = WordNetLemmatizer()
            self.lemma = lemmatizer.lemmatize
        else:
            pass
    
    def candidate_keywords(self, document_sents):
        '''
        Finding the possible candidates for keywords, by removing stopwords and filtering by POS tag
        '''
        phrase_list = []
        for sentence in document_sents:
            words = map(lambda x: "#" if x in self.stopwords else x, self.tagging(self.tokenizer(sentence.lower())))
            phrase = []
            candidates =[]
            
            for (word, tag) in words:
                if word == "#" or self.isPunct(word):
                  if len(phrase) > 0:
                    phrase_list.append(phrase)
                    phrase = []
                else:
                    if self.pos != None:
                        phrase.append(word)
                        for t in self.pos:
                            if tag.startswith(t):
                                candidates.append(self.lemma(word, t.lower()))
                            else:
                                pass
                    else:
                        phrase.append(word)
                        candidates.append(word)
        return phrase_list, candidates
    
    def calculate_word_scores(self, phrase_list, candidates):
        word_freq = nltk.FreqDist()
        word_degree = nltk.FreqDist()
        for phrase in phrase_list:
          degree = len(list(filter(lambda x: not self.isNumeric(x), phrase))) - 1
          for word in phrase:
            word_freq[word] += 1
            word_degree[word] += degree
        for word in word_freq.keys():
          word_degree[word] = word_degree[word] + word_freq[word]
        word_scores = {}
        for word in word_freq.keys():
            if word in candidates:
                word_scores[word] = word_degree[word] / word_freq[word]
        return word_scores
    
    def calculate_phrase_scores(self, phrase_list, word_scores, candidates):
        phrase_scores = {}
        for phrase in phrase_list:
          phrase_score = 0
          for word in phrase:
              if word in candidates:
                phrase_score += word_scores[word]
          phrase_scores[" ".join(phrase)] = phrase_score
        return phrase_scores
    
    def fit(self):
        #might be useful for piping
        pass

    def transform(self, corpus, output_type="w"):
        keyword_results = []
        self.manage_params()
        for document in corpus:
            sentences = nltk.sent_tokenize(document)
            phrase_list, candidate_list = self.candidate_keywords(sentences)
            word_scores = self.calculate_word_scores(phrase_list, candidate_list)
            phrase_scores = self.calculate_phrase_scores(phrase_list, word_scores, candidate_list)
            if output_type == "s":
                sorted_scores = sorted(phrase_scores.items(),key=operator.itemgetter(1), reverse=True)
            else:
                sorted_scores = sorted(word_scores.items(),key=operator.itemgetter(1), reverse=True)           
            keyword_results.append([k[0] for k in sorted_scores[0:self.nkey]])
        return keyword_results




'''
sample text from wikipedia
'''
text = "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that can later be released to fuel the organisms' activities (energy transformation). This chemical energy is stored in carbohydrate molecules, such as sugars, which are synthesized from carbon dioxide and water – hence the name photosynthesis, from the Greek φῶς, phōs, light, and σύνθεσις, synthesis, putting together. In most cases, oxygen is also released as a waste product. Most plants, most algae, and cyanobacteria perform photosynthesis; such organisms are called photoautotrophs. Photosynthesis is largely responsible for producing and maintaining the oxygen content of the Earth's atmosphere, and supplies all of the organic compounds and most of the energy necessary for life on Earth. Although photosynthesis is performed differently by different species, the process always begins when energy from light is absorbed by proteins called reaction centres that contain green chlorophyll pigments. In plants, these proteins are held inside organelles called chloroplasts, which are most abundant in leaf cells, while in bacteria they are embedded in the plasma membrane. In these light-dependent reactions, some energy is used to strip electrons from suitable substances, such as water, producing oxygen gas. The hydrogen freed by the splitting of water is used in the creation of two further compounds that act as an immediate energy storage means: reduced nicotinamide adenine dinucleotide phosphate (NADPH) and adenosine triphosphate (ATP), the energy currency of cells. In plants, algae and cyanobacteria, long-term energy storage in the form of sugars is produced by a subsequent sequence of light-independent reactions called the Calvin cycle; some bacteria use different mechanisms, such as the reverse Krebs cycle, to achieve the same end. In the Calvin cycle, atmospheric carbon dioxide is incorporated into already existing organic carbon compounds, such as ribulose bisphosphate (RuBP). Using the ATP and NADPH produced by the light-dependent reactions, the resulting compounds are then reduced and removed to form further carbohydrates, such as glucose. The first photosynthetic organisms probably evolved early in the evolutionary history of life and most likely used reducing agents such as hydrogen or hydrogen sulfide, rather than water, as sources of electrons. Cyanobacteria appeared later; the excess oxygen they produced contributed directly to the oxygenation of the Earth, which rendered the evolution of complex life possible. Today, the average rate of energy capture by photosynthesis globally is approximately 130 terawatts, which is about three times the current power consumption of human civilization. Photosynthetic organisms also convert around 100–115 thousand million metric tonnes of carbon into biomass per year."

sample=[text]


myRE = RAKE_tagged(10, stopwords='auto', pos=["N", "V", "R"])
print(myRE.transform(df_txt.values[:2], output_type="w"))

for catchphrase in myRE.transform(sample, output_type="s")[0]:
    print (catchphrase)


