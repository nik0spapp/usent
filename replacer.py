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
from nltk.corpus import wordnet

class RepeatReplacer(object):
    """
    RepeatReplacer: Replaces letters that appear in irregular 
    repetition inside words.
    """

    def __init__(self, lexicon):
       self.lexicon = lexicon.words
       self.repeat_regexp = re.compile(r'(.*)(.)\2(.*)')
       self.repl = r'\1\2\3'
     
    def replace(self, word):
       check = re.sub(r'\!|;|\||\.|\?|,|:|"|\)|\(','',word)
       if self.lexicon.has_key(word) and self.lexicon[word].has_key('emoticon'):
          return word
       if wordnet.synsets(check):  
         if word == check:
            return word
         else:  
            return check + "".join(set(word[len(check):]))
       repl_word = self.repeat_regexp.sub(self.repl, word)
       if repl_word != word:
         return self.replace(repl_word)
       else:
         return repl_word 
     

if __name__ == '__main__': 
    rr = RepeatReplacer()
    example = "sorrryyyyyyyyyyy"
    print "Before: " + example
    rr.replace(example)
    print "After: " + example
