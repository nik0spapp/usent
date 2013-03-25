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

import os
import sys
import nltk
import random
import datetime
from terminal_colors import Tcolors
sys.path.append(os.path.abspath("") + "/../")

class PbSubj:
    """
        PbSubj: Pattern-Based subjective sentence classifier which classifies a 
        sentence as subjective with a probability of the top-matched 
        pattern among a list of strongly associated with subjectivity
        patterns. The selection of these patterns is made using two thresholds
        t1 and t2. The patterns whom frequency is greater than t1 and the 
        subjective frequency greater than t2 are selected.
    """
    
    def __init__(self, tagger, debug=False):
        self.tagger = tagger
        # Patterns learned from the pattern learner
        self.learned_patterns = {}
        # Strong subjective patterns
        self.ss_patterns = {} 
        self.sorted_ss_patterns = None
        self.t1_threshold = 5 # 3
        self.t2_threshold = 1 # 0.9
        self.pl_threshold = 25
        self.limit = 1
        self.debug = debug
        
    def classify(self, sentence):
        """
            Classify sentence based on the probabilities of the strongly 
            associated patterns with subjectivity.
        """
        found = False
        matched_pattern = None
        # POS tagging
        tagged_sentence = self.tagger.tag(sentence)
        words = []
        tags = []
        for (word, tag) in tagged_sentence:
            words.append(word)
            if tag is None:
                tag = ""
            tags.append(tag)
            
        for (pattern, value) in self.sorted_ss_patterns:
            display = value['display']
            pattern_type = value['type']
            try:
            	pos_in_sentence = sentence.find(display)
            except:
            	pos_in_sentence = -1
            	
            if pos_in_sentence > -1:
                matched_pattern = value
                if pattern_type == "subj": 
                    found = self.search_for_subject(display, words, tags)
                elif pattern_type in ["dobj", "np"]:
                    remaining_sentence = sentence[pos_in_sentence:]
                    found = self.search_for_object(display, words, tags)
            if found: 
                break
        if not found:      
            objective = False
            subjective = False  
        else:
            if self.debug: print matched_pattern
            random.seed()
            if random.uniform(0,1) <= matched_pattern['prob']:
                subjective = True
                objective = False
                if self.debug: print "Probability: " + (str)(matched_pattern['prob'])
            else:
                objective = True
                subjective = False 
                if self.debug: print "Probability: " + (str)(1 - matched_pattern['prob'])
        return found, subjective, objective
        
        
    def find_needle_in_haystack(self, needle, haystack):
        """
            This method finds the position of the intersection on 
            the haystack array (if there is one).
        """                                                         
        r = [] 
        L = len(needle) 
        for i in range(len(haystack)): 
           if haystack[i:i+L] == needle: 
               r.append(i)
        return r 

    
    def search_for_object(self, pattern, words, tags):
        pattern_words = pattern.split()
        position = self.find_needle_in_haystack(pattern_words, words)
        if len(position) > 0:
            position = position[0] + len(pattern_words)
            for i, tag in enumerate(tags[position:]): 
                if i < self.limit and (tag.find("NN") > -1 or tag.find("NP") > -1\
                   or tag.find("PR") > -1):
                   return True
        return False
    
    
    def search_for_subject(self, pattern, words, tags):
        pattern_words = pattern.split()
        position = self.find_needle_in_haystack(pattern_words, words)
        if len(position) > 0:
            position = position[0] - 1
            for i, tag in enumerate(tags[position:]): 
                if i < self.limit and (tag.find("NN") > -1 or tag.find("NP") > -1\
                   or tag.find("PR") > -1):
                   return True
        return False          
    
            
    def select_strong_subjective_patterns(self):
        """
            Selection of the strongly associated with subjectivity patterns
            using the thresholds t1 and t2.
        """
        self.ss_patterns = {}
        for pattern in self.learned_patterns.keys():
            freq = self.learned_patterns[pattern]['freq']
            prob = self.learned_patterns[pattern]['prob']
            if freq >= self.t1_threshold and prob >= self.t2_threshold: 
                self.ss_patterns[pattern] = self.learned_patterns[pattern]
            # delete some patterns with low frequency and probability for efficiency
            elif freq > 5 and freq < ((self.t1_threshold*3) / 4):
            	del(self.learned_patterns[pattern])
            
        sorted_ss = sorted(self.ss_patterns.iteritems(),key=lambda x: x[1]['prob'], reverse=True)
        self.sorted_ss_patterns = sorted_ss 
        for (s,v) in sorted_ss:
            title = (Tcolors.OKGREEN+s+Tcolors.ENDC+" ").ljust(70,'-') 
            pbs = (str)(v['freq'])+"/" + Tcolors.CYAN + (str)(v['prob']) + Tcolors.ENDC
            if self.debug: print title + "------------> " + pbs
        if self.debug: print
        if len(sorted_ss) > self.pl_threshold:
        	self.t1_threshold += 1
        
    def train(self, learned_patterns):
        """
            Train classifier with the learned patterns derived from
            the pattern learner.
        """
        self.learned_patterns = learned_patterns
        self.select_strong_subjective_patterns()
        
        
