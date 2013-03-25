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
import pickle
import nltk.corpus, nltk.tag, itertools  
from terminal_colors import Tcolors

class SequentialTagger:
    """
        Sequential tagger: It uses a sequential tagging method for tagging
        untagged sentences. Three tag classifiers are used in sequential 
        order (Unigram, Bigram and Trigram) that are trained with brown
        corpus. Experiments have been made to select this specific UBT 
        sequence that seems to have better precision than the other 
        combinations.
    """
    def __init__(self): 
    
        self.filename = "stored/ubt_tagger.classifier"
        try: 
            self.ubt_tagger = pickle.load(open(self.filename)) 
            print Tcolors.ADD + Tcolors.OKBLUE + " Loaded existing UBT tagger!" + Tcolors.ENDC 
        except:
            print Tcolors.ACT + Tcolors.RED + " Existing UBT tagger not found." + Tcolors.ENDC
            print "Path:",  "stored/ubt_tagger.classifier"
            print "Training..."
            brown_review_all = nltk.corpus.brown.tagged_sents()
            brown_review_sents = nltk.corpus.brown.tagged_sents(categories=['reviews'])
            brown_lore_sents = nltk.corpus.brown.tagged_sents(categories=['lore'])
            brown_romance_sents = nltk.corpus.brown.tagged_sents(categories=['romance'])
            
            brown_train = list(itertools.chain(brown_review_sents[:1000], 
                                               brown_lore_sents[:1000], 
                                               brown_romance_sents[:1000]))
            brown_test = list(itertools.chain(brown_review_sents[1000:2000], 
                                              brown_lore_sents[1000:2000], 
                                              brown_romance_sents[1000:2000]))
            
            conll_sents = nltk.corpus.conll2000.tagged_sents()
            conll2_sents = nltk.corpus.conll2002.tagged_sents()
            conll_train = list(conll_sents[:4000])
            conll_test = list(conll_sents[4000:8000])
     
            treebank_sents = nltk.corpus.treebank.tagged_sents()
            treebank_train = list(treebank_sents[:1500])
            treebank_test = list(treebank_sents[1500:3000]) 
            train_sents = conll_sents + conll2_sents + treebank_sents + brown_train
            test_sents = conll_test
            
            ubt_tagger = self.backoff_tagger(train_sents, [nltk.tag.UnigramTagger, 
                                                           nltk.tag.BigramTagger, 
                                                           nltk.tag.TrigramTagger])
            self.ubt_tagger = ubt_tagger
            output = open(self.filename,'wb')
            pickle.dump(self.ubt_tagger,output)
            output.close()
            
    def backoff_tagger(self, tagged_sents, tagger_classes, backoff=None):
        """
            Creation the sequential tagger
        """
        if not backoff:
            backoff = tagger_classes[0](tagged_sents)
            del tagger_classes[0]
     
        for cls in tagger_classes:
            tagger = cls(tagged_sents, backoff=backoff)
            backoff = tagger
     
        return backoff
     
    def tag(self, sentence):
        """
            Method for tagging untagged sentences.
        """
        words = nltk.word_tokenize(sentence)
        return self.ubt_tagger.tag(words)
