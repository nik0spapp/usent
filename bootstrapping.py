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

import re
import sys  
import pickle 
from terminal_colors import Tcolors
from pb_classifiers import PbSubj

class Bootstrapping:
    """
        Bootstrapping: Class performing the bootstrapping process for 
        subjectivity and objectivity classification of  sentences. The 
        method learns linguistically rich extraction patterns for subjective 
        (opinionated) expressions from unannotated data. The learned
        patterns are used to identify more subjective sentences that simple 
        high precision classifiers can't recall.

        Related paper:
        E. Riloff and J. Wiebe. Learning extraction patterns for subjective 
        expressions. In Proceedings of the 2003 conference on Empirical methods 
        in natural language processing, EMNLP '03, pages 105--112, 2003. ACL.
        
        Learned patterns structure
        e.g. {"<subj> was killed" : {'type' : 'subj',
                                     'display' : 'was killed',
                                     'subj_freq' : 10,
                                     'freq' : 20,
                                     'prob' : 0.5}}
         
    """
    
    def __init__(self, hp_obj, hp_subj, tagger, debug=False):
        # Syntactic forms for pattern extraction
        self.syntactic_forms = {"subj" : [["BE","VBN*|VBD*"],
                                          ["HAVE","BE","VB*"],
                                          ["VB*"],
                                          ["VB*","*","NN*|NP*|NC*"], 
                                          ["VB*","TO","VB*"],
                                          ["HAVE","TO","BE"],
                                          ["HAVE","NN*"]],
                                "dobj" : [["VB*"],
                                          ["TO","VB*"],
                                          ["VB*","TO","VB*"]],  
                                "np"   : [["NN","IN"],
                                          ["VB*","NN","IN"],
                                          ["BE","VBN","IN"],
                                          ["TO","VB","TO"]]
                                }
        self.filename = "stored/learned_patterns"
        try:
            self.learned_patterns = pickle.load(open(self.filename))
            print Tcolors.ADD + Tcolors.OKBLUE + " Loaded existing pattern knowledge!" + Tcolors.ENDC 
        except:
            print Tcolors.ACT + Tcolors.RED + " Existing pattern knowledge not found." + Tcolors.ENDC
            self.learned_patterns = {}
             
        # Part Of Speech Sequential Tagger (Unigram->Bigram->Trigram) 
        self.tagger = tagger
        # Sentence to be classified
        self.subjective = False
        self.objective = False
        # High precision objective classifier
        self.hp_obj = hp_obj
        # High precision subjective classifier
        self.hp_subj = hp_subj
        # Pattern-Based Subjective Classifier
        self.pb_subj = PbSubj(self.tagger, debug=debug)
        # Learned patterns
        self.patterns = {}
        self.debug = debug
            
    def classify(self, sentence, previous="", next=""):
        """
            Subjectivity classification using boostrapping method.
        """
        # STEP 1: Classify sentence with HP Subjective classifier
        self.subjective = self.hp_subj.classify(sentence) 
        # STEP 1: Get help from learned patterns
        if not self.subjective:
            if self.debug: print Tcolors.ACT + " Training pattern based classifier...\n"
            self.pb_subj.train(self.learned_patterns)
            found, self.subjective, obj = self.pb_subj.classify(sentence)
        
        if not self.subjective and not self.objective:
            # STEP 2: Classify sentence with HP Objective classifier
            self.objective = self.hp_obj.classify(sentence, previous, next)
        
        if self.subjective or self.objective:
            # STEP 3: Learn 
            self.learn_patterns_from(sentence) 
        else:
            # STEP 4: Classify based on learned patterns
            found, self.subjective, self.objective = self.pb_subj.classify(sentence)
            # Uncomment the two following to bootstrap further the subjective
            # sentences detected from the pattern-based classifier.
            # if self.subjective:
            #    self.learn_patterns_from(sentence)
        if self.subjective:
            return 'subjective'
        elif self.objective:
            return 'objective'
        else:
            return None
    
    def learn_patterns_from(self, sentence):
        """
            Learns extraction patterns associated with subjectivity
            from a given sentence.
        """
        tagged_sentence = self.tagger.tag(sentence)
        tags = []
        words = []
        if self.debug:
            print Tcolors.ACT + " Performing part of speech (POS) tagging..." + Tcolors.WARNING 
            print tagged_sentence
            print Tcolors.ENDC
        for (w,tag) in tagged_sentence:
            if tag is None:
                tag = ""
            tags.append(tag)
            words.append(w)

        self.trigger_patterns(tags, words)
                
    def match_until_next_nn(self, i, tags, words, form, key):
        """
            The hard job for triggering the syntactic forms :-)
        """
        LIMITER = 4
        BE = ['was','were','be','being','am','been','are','is']
        HAVE = ['has','have','had']
        matched = 0
        prev_matched = 0 
        positions_matched = []
        learned_pattern = []
        star = False 

        for j,ctag in enumerate(form):
            next = i + j + 1
            inner = 0 
            found = False
            while(not found and next < len(tags)):
                next += inner
                if next < len(words) and ctag == "VB*" and words[next] in HAVE:
                    next += 1
                    if next < len(words) and ctag == "VB*" and words[next] in BE:
                        next += 1
                elif next < len(words) and ctag == "VB*" and words[next] in BE:
                    next += 1
                if ctag == "*":
                    star = True  
                elif ctag.find("*") > -1:
                    ortags = ctag.split("|")
                    for ortag in ortags:
                        if next < len(tags) and tags[next].find(ortag.replace("*","")) > -1\
                           and next not in positions_matched: 
                            if star and inner < 2: 
                                matched += 1
                            matched += 1 
                            positions_matched.append(next) 
                            found = True
                elif ctag == "BE":  
                    if next < len(tags) and (tags[next].find("VB") > -1 or tags[next].find("BE") > -1) \
                       and words[next] in BE and next not in positions_matched: 
                        matched += 1 
                        positions_matched.append(next)
                        found = True
                elif ctag == "HAVE":
                    if next < len(tags) and (tags[next].find("VB") > -1 or tags[next].find("HV") > -1)\
                       and words[next] in HAVE and next not in positions_matched:
                            matched += 1 
                            positions_matched.append(next)  
                            found = True                 
                elif next < len(tags) and tags[next].find(ctag) > -1\
                     and next not in positions_matched: 
                    matched += 1
                    positions_matched.append(next)
                    found = True
                else:
                    found = True
                inner += 1
                
        if key == "subj":
            learned_pattern = ["<subj>"] 
        for pos in positions_matched:
            learned_pattern.append(words[pos])
        if key != "subj":
            learned_pattern.append("<" + key +">")
        
        learned_pattern = " ".join(learned_pattern)    
         
        if matched == len(form):
            if self.debug:
                print Tcolors.ACT + Tcolors.RED + " Form triggered: ", form, Tcolors.ENDC
                print "Pattern learned:", learned_pattern
            return True, learned_pattern
        else:
            return False, None
                
    def proccess_learned_pattern(self, pattern):
        """
            Add pattern to learned patterns if it doesn't exist else
            update its probability.
        """ 
        if pattern.find("subj") > -1:
            key = "subj"
        elif pattern.find("dobj") > -1:
            key = "dobj"
        else:
            key = "np"
        cur_subj_freq = 0
        if self.subjective:
            cur_subj_freq = 1 
        pkey = pattern
        pkey = re.sub(r"<subj> | <np>| <dobj>","",pkey) 
        if self.learned_patterns.has_key(pattern):
            subj_freq = self.learned_patterns[pattern]['subj_freq'] + cur_subj_freq
            freq = self.learned_patterns[pattern]['freq'] + 1
            prob = (float)(subj_freq)/(float)(freq)
            self.learned_patterns[pattern]['prob'] = prob
            self.learned_patterns[pattern]['subj_freq'] = subj_freq
            self.learned_patterns[pattern]['freq'] = freq
            if self.debug: print Tcolors.ADD + Tcolors.HEADER + " Updating pattern:", pattern, Tcolors.ENDC  
        else:
            subj_freq = 0
            freq = 1
            subj_freq += cur_subj_freq
            prob = (float)(subj_freq)/(float)(freq)
            self.learned_patterns[pattern] = {'type': key,
                                           'display': pkey,
                                           'freq' : freq,
                                           'subj_freq' : subj_freq,
                                           'prob' : prob}  
            if self.debug: print Tcolors.ADD + Tcolors.CYAN + " Learning pattern:", pattern, Tcolors.ENDC  
            
    def store_knowledge(self): 
        """
            Stored learned patterns for future usage.
        """
        output = open(self.filename, 'wb')
        pickle.dump(self.learned_patterns, output)
        
        
    def trigger_patterns(self, tags, words):
        """
            Method that triggers syntactic forms and returns the learned 
            patterns from the triggering.
        """   
        patterns = []
        if self.debug: print Tcolors.ACT + " Triggering subjective syntactic forms..." 
        for key in self.syntactic_forms.keys():
            syntactic_forms = self.syntactic_forms[key]
            if self.debug: print Tcolors.PROC + Tcolors.GRAY + " Checking form group " + key + "..." + Tcolors.ENDC
            
            for form in syntactic_forms:  
                for i,tag in enumerate(tags): 
                    if tag.find("NN") > -1 or tag.find("NP") > -1 \
                       or tag.find("PR") > -1: 
                        triggered, pattern = self.match_until_next_nn(i, tags, words, form, key) 
                        if pattern is not None and pattern not in patterns:
                            if self.debug: print Tcolors.ACT + Tcolors.RED + " Form triggered: ", form, Tcolors.ENDC
                            patterns.append(pattern)
        for pattern in patterns:
            self.proccess_learned_pattern(pattern)
        if self.debug:
            print Tcolors.OKBLUE
            print self.learned_patterns    
            print Tcolors.ENDC
        self.store_knowledge()

    def train(self, data):
        """
            Method to train the pattern-based classifier
        """
        for sentence in data:
            self.classify(sentence)  
    
    def clear_learned_data(self):
        self.learned_patterns = {}

                  
if __name__ == "__main__":
    from hp_classifiers import HpObj, HpSubj
    from pos import SequentialTagger
    hp_obj = HpObj()
    hp_subj = HpSubj()  
    tagger = SequentialTagger()
    bootstrapping = Bootstrapping(hp_obj, hp_subj, tagger)
    if self.debug:
        print bootstrapping.classify(sys.argv[1])
        
        
