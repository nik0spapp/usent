####################################################################
# Licence:    Creative Commons (see COPYRIGHT)                     #
# Authors:    Nikolaos Pappas, Georgios Katsimpras                 #
#             {nik0spapp, gkatsimpras}@gmail.com                   # 
# Supervisor: Efstathios stamatatos                                #
#             stamatatos@aegean.gr                                 #
# University of the Aegean                                         #
# Department of Information and Communication Systems Engineering  #
# Information Management Track (MSc)                               #
# Karlovasi, Samos                                                 #
# Greece                                                           #
####################################################################

from __future__ import division
import nltk
import string
import sys
from terminal_colors import Tcolors
from stemming.porter2 import stem 
sys.path.append(sys.path[0] + "/../")


class PolarityClassifier:
    """
    PolarityClassifier: Rule-based polarity classification of sentences 
    according to the following paper:

    T. Wilson, J. Wiebe, and P. Hoffmann. Recognizing contextual polarity 
    in phrase-level sentiment analysis. In Proceedings of the conference 
    on Human Language Technology and Empirical Methods in Natural Language 
    Processing, HLT '05, pages 347--354, 2005.

    Enhancements: We have incorporated emoticons and slung dictionary 
    apart from the MPQA lexicon that is used in the paper.
    """
    
    def __init__(self, tagger, lexicon, debug=False):
        self.lexicon = lexicon.words
        self.sentence = None
        self.words = []
        self.feature_words = {}
        self.polar_expressions = []
        self.polar_with_tags = {}
        self.polar_with_score = {}
        self.strong_polar_expressions = []
        self.negation_words = ["not", "no", "but"]
        self.tagger = tagger
        self.words_pos_tags = []
        self.stokens = []
        self.emotions_score = []
        self.emoticons = []
        self.debug = debug
        
    def apply_emotions(self):
        """
            Compute emotion scores based on emoticon list.
        """
        score = 0
        for token in self.stokens:
            if self.lexicon.has_key(token) \
               and self.lexicon[token].has_key('emoticon'):
               if self.lexicon[token]['priorpolarity'] == "negative":
                    score = -2
               else:
                    score = 2
               self.emoticons.append(token)
               self.emotions_score.append(score)
           
    def apply_weights(self):
        """
        Adjust (2*n times) scores for polar expressions.
        """ 
        # Strong emotion heuristic based on punctuation
        strong_emotion = 1 
        if self.sentence.endswith("!"):
            strong_emotion = 1.5
        elif self.sentence.endswith("?"):
            strong_emotion = 0.5 
            
        for i,polar in enumerate(self.polar_expressions):
            #first rule: if strong double score
            if polar in self.strong_polar_expressions:
                self.polar_with_score[polar] *= 2
            #second rule: if intensified polar double score
            if self.intensified_polar(polar):
                self.polar_with_score[polar] *= 2
            #third rule: if polar expr is adjective double score
            if self.polar_with_tags[polar] == "adj":
                self.polar_with_score[polar] *= 2
             
            if i + 1 == len(self.polar_expressions):
                self.polar_with_score[polar] *= strong_emotion
                
    def check_precedings(self, polar, words):
        """
        Find the indexes of polar words and 5 preceding of it.
        """
        if words.index(polar) >= 6:
            return True
        else:
            return False
    
    def classify(self, sentence):
        """
        Sum up the contextual scores of polar expressions and classify the sentence.
        """
        self.sentence = sentence
        # Extracting Features from sentence
        self.extract_features() 
        # Performing Word Sense Disambiguation
        # Extracting Polar Expressions
        self.word_sense_disambiguation()
        # Checking for negation words
        self.negation_modeling()
        # Adjusting weights to Polar Expressions
        self.apply_weights() 
        self.apply_emotions()
        # Performing polarity classification
        [prediction, score] = self.predict_class()
        
        
        if self.debug:
            print "\n[*] --------------------RESULTS----------------------"
            print Tcolors.ADD + " FEATURE WORDS:", self.feature_words        
            print Tcolors.ADD + " POLAR EXPRESSIONS FOUND:", self.polar_expressions
            print Tcolors.ADD + " POLAR WEIGHTS:", self.polar_with_score
            print Tcolors.ADD + " EMOTICONS:", self.emoticons
            print Tcolors.ADD + " EMOTION WEIGHTS:", self.emotions_score
            print Tcolors.ADD + " PREDICTION: ", prediction, ", WITH CONFIDENCE: ", score
            print Tcolors.ADD + " NORMALIZED CONFIDENCE: ", score/len(self.words)
        
        self.words = [w for w in self.words if w != '']
        return prediction, score, score/len(self.words) #normalizedScore
      
    def extract_features(self):
        """
        Match positive and negative words of a sentence with a score of +1 or -1
        respectively, if found in the lexicon.
        """        
        self.words = self.tokenize_words(self.sentence)        
        words = self.words                       
        for word in words:
            word = word.lower()
            if word in self.lexicon:
                if self.lexicon[word]['priorpolarity'] == "positive":
                    if not self.feature_words.has_key(word):                        
                        self.feature_words[word] = 1
                    else:
                        self.feature_words[word] += 1
                elif self.lexicon[word]['priorpolarity'] == "negative":
                    if not self.feature_words.has_key(word):                        
                        self.feature_words[word] = -1
                    else:
                        self.feature_words[word] -= 1
                else:
                    self.feature_words[word] = 0
            
    def intensified_polar(self, polar):
        if self.words.index(polar) > 0:
            previous_word = self.words[self.words.index(polar) - 1]
            
            if self.lexicon.has_key(previous_word) and self.lexicon[previous_word]["type"]=="strongsubj" \
               and 'adj' in self.lexicon[previous_word]["pos1"]:
                return True
        return False
    
    def match_tags(self, pos_tag):
        if pos_tag:
            if pos_tag.startswith("VB"):
                return "verb"
            elif pos_tag.startswith("JJ"):
                return "adj"
            elif pos_tag.startswith("NN"):
                return "noun"
            elif pos_tag.startswith("RB"):
                return "adverb"
            else:
                return 'anypos'
        else:
            return "anypos"
    
    def negation_modeling(self):
        """
        Examine negation words and reassign polarity.
        """
        for polar in self.polar_expressions:
            has_precedings = self.check_precedings(polar, self.words)
            for neg in self.negation_words:
                if has_precedings: 
                    if (neg in self.words[(self.words.index(polar)-5):self.words.index(polar)])\
                       or self.polarity_shifting(polar, self.words[(self.words.index(polar)-5):self.words.index(polar)]):
                        self.polar_with_score[polar] = self.polar_with_score[polar]*(-1)
                        break
                else:
                    if neg in self.words[0:self.words.index(polar)] or \
                       self.polarity_shifting(polar, self.words[0:self.words.index(polar)]):
                        self.polar_with_score[polar] = self.polar_with_score[polar]*(-1)
                          
    def predict_class(self):
        summary = 0
        summary = sum([value for value in self.polar_with_score.values()])
        summary += sum(self.emotions_score)
        
        if summary > 0:
            return "positive", summary
        elif summary < 0:
            return "negative", summary
        else:
            return "neutral", summary
    
    def polarity_shifting(self, polar, words):
        for word in words:
            if (self.lexicon.has_key(word) and self.lexicon[word]["type"]=="strongsubj" \
               and self.lexicon[word]["priorpolarity"] != self.lexicon[polar]["priorpolarity"] \
               and self.lexicon[word]["priorpolarity"]!="neutral") or \
               word.endswith("n't"):
                # reverse polarity of polar
                if self.debug:
                    print "[!] NEGATION WORD FOUND: ",word
                return True
        
        return False                   
    
    def tokenize_words(self, sentence):
        words = nltk.word_tokenize(sentence.lower())
        self.stokens = sentence.split()
        for i,word in enumerate(words):
            if word[len(word)-1] in string.punctuation: 
                words[words.index(word)] = word[0:(len(word)-1)]
                
        self.words_pos_tags = self.tagger.tag(sentence)
        for (word, TAG) in self.words_pos_tags:  
            word = word.lower() 
            # Handle punctuation in word_tokenization
            if TAG and TAG.startswith("VB"):   
            	if word in words:      
                	words[words.index(word)] = stem(word)
        return words
    
    def word_sense_disambiguation(self):
        """
        Disambiguate words in a sentence if only if the POS tag of the word matches
        the POS tag in the lexicon
        """ 
        for (word, TAG) in self.words_pos_tags:   
            # Handle punctuation in word_tokenization
            if word[len(word)-1] in string.punctuation:                
                word = word[0:(len(word)-1)]
            matched_tag = self.match_tags(TAG)
            word = word.lower()
            words = [word, stem(word)]
            for w in words: 
                if self.feature_words.has_key(w) and (matched_tag in self.lexicon[w]["pos1"] \
                                                         or self.lexicon[w]["pos1"][0] == "anypos" \
                                                         or matched_tag == "anypos"): 
                    self.polar_expressions.append(w)
                    self.polar_with_score[w] = self.feature_words[w]
                    self.polar_with_tags[w] = matched_tag
                    if self.lexicon[w]['type'] == "strongsubj":
                        self.strong_polar_expressions.append(w)
                    
        self.polar_expressions = list(set(self.polar_expressions))

      
if __name__ == '__main__': 
    polarity = PolarityClassifier(sys.argv[1])
    polarity.classify()

    
        
        
