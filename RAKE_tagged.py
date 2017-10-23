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
        all_words = []
        for sentence in document_sents:
            words = map(lambda x: "#" if x in self.stopwords else x, self.tagging(self.tokenizer(sentence.lower())))
            for w in words:
                all_words.append(w)
        phrase = []
        candidates =[]
        for (word, tag) in all_words:
            if word == "#" or self.isPunct(word):
                if len(phrase) > 0:
                    phrase_list.append(phrase)
                    phrase = []
            else:
                if self.pos != None:
                    phrase.append(word)
                    for t in self.pos:
                        if tag.startswith(t):
                            candidates.append(self.lemma(word, t[0].lower()))
                                #print(self.lemma(word, t.lower()))
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
            print(len(word_scores))
            phrase_scores = self.calculate_phrase_scores(phrase_list, word_scores, candidate_list)
            if output_type == "s":
                sorted_scores = sorted(phrase_scores.items(),key=operator.itemgetter(1), reverse=True)
            else:
                sorted_scores = sorted(word_scores.items(),key=operator.itemgetter(1), reverse=True)           
            print(len(sorted_scores))
            keyword_results.append([k[0] for k in sorted_scores[0:self.nkey]])
        return keyword_results




'''
sample text from wikipedia
'''
text = "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that can later be released to fuel the organisms' activities (energy transformation). This chemical energy is stored in carbohydrate molecules, such as sugars, which are synthesized from carbon dioxide and water – hence the name photosynthesis, from the Greek φῶς, phōs, light, and σύνθεσις, synthesis, putting together. In most cases, oxygen is also released as a waste product. Most plants, most algae, and cyanobacteria perform photosynthesis; such organisms are called photoautotrophs. Photosynthesis is largely responsible for producing and maintaining the oxygen content of the Earth's atmosphere, and supplies all of the organic compounds and most of the energy necessary for life on Earth. Although photosynthesis is performed differently by different species, the process always begins when energy from light is absorbed by proteins called reaction centres that contain green chlorophyll pigments. In plants, these proteins are held inside organelles called chloroplasts, which are most abundant in leaf cells, while in bacteria they are embedded in the plasma membrane. In these light-dependent reactions, some energy is used to strip electrons from suitable substances, such as water, producing oxygen gas. The hydrogen freed by the splitting of water is used in the creation of two further compounds that act as an immediate energy storage means: reduced nicotinamide adenine dinucleotide phosphate (NADPH) and adenosine triphosphate (ATP), the energy currency of cells. In plants, algae and cyanobacteria, long-term energy storage in the form of sugars is produced by a subsequent sequence of light-independent reactions called the Calvin cycle; some bacteria use different mechanisms, such as the reverse Krebs cycle, to achieve the same end. In the Calvin cycle, atmospheric carbon dioxide is incorporated into already existing organic carbon compounds, such as ribulose bisphosphate (RuBP). Using the ATP and NADPH produced by the light-dependent reactions, the resulting compounds are then reduced and removed to form further carbohydrates, such as glucose. The first photosynthetic organisms probably evolved early in the evolutionary history of life and most likely used reducing agents such as hydrogen or hydrogen sulfide, rather than water, as sources of electrons. Cyanobacteria appeared later; the excess oxygen they produced contributed directly to the oxygenation of the Earth, which rendered the evolution of complex life possible. Today, the average rate of energy capture by photosynthesis globally is approximately 130 terawatts, which is about three times the current power consumption of human civilization. Photosynthetic organisms also convert around 100–115 thousand million metric tonnes of carbon into biomass per year."
text2 = "The Americas (also collectively called America) comprise the totality of the continents of North and South America. Together, they make up most of the land in Earth's western hemisphere and comprise the New World. Along with their associated islands, they cover 8% of Earth's total surface area and 28.4% of its land area. The topography is dominated by the American Cordillera, a long chain of mountains that runs the length of the west coast. The flatter eastern side of the Americas is dominated by large river basins, such as the Amazon, St. Lawrence River / Great Lakes basin, Mississippi, and La Plata. Since the Americas extend 14,000 km (8,700 mi) from north to south, the climate and ecology vary widely, from the arctic tundra of Northern Canada, Greenland, and Alaska, to the tropical rain forests in Central America and South America. Humans first settled the Americas from Asia between 42,000 and 17,000 years ago. A second migration of Na-Dene speakers followed later from Asia. The subsequent migration of the Inuit into the neoarctic around 3500 BCE completed what is generally regarded as the settlement by the indigenous peoples of the Americas. The first known European settlement in the Americas was by the Norse explorer Leif Ericson. However, the colonization never became permanent and was later abandoned. The voyages of Christopher Columbus from 1492 to 1502 resulted in permanent contact with European (and subsequently, other Old World) powers, which led to the Columbian exchange. Diseases introduced from Europe and West Africa devastated the indigenous peoples, and the European powers colonized the Americas. Mass emigration from Europe, including large numbers of indentured servants, and importation of African slaves largely replaced the indigenous peoples. Decolonization of the Americas began with the American Revolution in 1776 and Haitian Revolution in 1791. Currently, almost all of the population of the Americas resides in independent countries; however, the legacy of the colonization and settlement by Europeans is that the Americas share many common cultural traits, most notably Christianity and the use of Indo-European languages: primarily Spanish, English, Portuguese, French, and to a lesser extent Dutch. The population is over 1 billion, with over 65% of them living in one of the three most populous countries (the United States, Brazil, and Mexico). As of the beginning of the 2010s, the most populous urban agglomerations are Mexico City (Mexico), New York (U.S.), Sao Paulo (Brazil), Los Angeles (U.S.), Buenos Aires (Argentina) and Rio de Janeiro (Brazil), all of them megacities (metropolitan areas with ten million inhabitants or more)."
sample=[text2]



myRE = RAKE_tagged(5, stopwords='auto', pos=["NNS", "VB"])
print(myRE.transform(sample, output_type="s"))



