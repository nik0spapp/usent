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

import sys
import nltk
from lexicon import Lexicon    
from stemming.porter2 import stem

class HpSubj:
    """
        High precision subjective sentence classifier which uses an annotated 
        lexicon of words as features. It classifies a sentence as subjective 
        if it contains two or more of the strong subjective clues.
    """

    def __init__(self, debug=False): 
        self.dictionary = Lexicon().words
        self.debug = debug
        
    def classify(self, sentence):
        wdict = self.dictionary
        words = nltk.word_tokenize(sentence)
        strong_subjective_words_count = 0
        subjective = False
        for word in words: 
            word = word.lower()
            check = [word, stem(word)]
            for w in check: 
                if wdict.has_key(w) and wdict[w]['type'] == 'strongsubj':
                    strong_subjective_words_count += 1
                    if strong_subjective_words_count >= 2:
                        subjective = True
                        break
        return subjective
    

class HpObj:
    """
        High precision objective sentence classifier which uses an annotated 
        lexicon as training data. It classifies a sentence as objective if it
        doesn't contain along with its previous and next sentence, not even 
        one strong subjective clue and at most one weak subjective clue.
    """
    
    def __init__(self, debug=False): 
    
        self.lexicon = Lexicon()
        self.dictionary = self.lexicon.words
        self.debug = debug
    
    def classify(self, current, previous="", next=""):
        if self.debug:
            print 
            print "current:", current
            print "previous:", previous 
            print "next:", next
            print
        wdict = self.dictionary
        words = nltk.word_tokenize(current)
        prev_words = nltk.word_tokenize(previous)
        next_words = nltk.word_tokenize(next)
        words += prev_words + next_words
        strong_subjective_words_count = 0
        weak_subjective_words_count = 0 
        objective = True
        
        for word in words: 
            word = word.lower()
            check = [word, stem(word)]
            for w in check: 
                if wdict.has_key(w):
                    if wdict[w]['type'] == 'strongsubj':
                        strong_subjective_words_count += 1
                        if strong_subjective_words_count > 0:
                            objective = False
                            break
                    elif wdict[w]['type'] == 'weaksubj':
                        weak_subjective_words_count += 1
                        if weak_subjective_words_count > 1:
                            objective = False
                            break
        return objective
 

if __name__ == '__main__': 
    hpo = HpObj()
    hps = HpSubj()
    print "Objective: " + (str)(hpo.classify(sys.argv[1]))
    print "Subjective: " + (str)(hps.classify(sys.argv[1]))
    
    
    
    
    
    
    
    
    
    
