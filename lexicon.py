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

import pickle 
import os
import sys 
from datasets.emoticons_patch import patch_emoticons 

class Lexicon:
    """
        Lexicon class loads an annotated dataset of words
        that have strong/weak subjectivity and is used to 
        train the high precision objective and subjective 
        classifiers.
    """
       
    def __init__(self):
        self.filename =  "stored/lexicon"
        try:
            self.words = pickle.load(open(self.filename))
        except:
            self.words = {}
            self.load()
            output = open(self.filename, 'wb')
            pickle.dump(self.words, output)
        
    def load(self):
        """
            The method loads the annotated corpus and extracts the structure
            with easy access for the classifiers.
        """
        dictionary_file = open("datasets/subjclueslen1-HLTEMNLP05.tff","r")
        lines = dictionary_file.readlines()

        for line in lines:
            attributes = line.split(" ")
            for index,attr in enumerate(attributes):
                if attr.find('word1') > -1:
                    word_value = attr.split("=")[1]
                    attributes[index] = []
                    break
            if self.words.has_key(word_value):
                for attr in attributes:
                    if attr != []:
                        arr = attr.split("=")
                        key = arr[0]
                        if key == "pos1":  
                            pos = self.words[word_value][key]
                            self.words[word_value][key].append(arr[1])
                            break
            else:
                self.words[word_value] = {}
                for attr in attributes:
                    if attr != []:
                        arr = attr.split("=")
                        key = arr[0]
                        if len(arr) > 1:
                            value = arr[1]
                        if key == "pos1":
                            self.words[word_value][key] = [value.replace("\n", "")]
                        else:
                            self.words[word_value][key] = value.replace("\n", "") 
        
        self.words = dict(patch_emoticons(), **self.words)        
        
                            
                            
        
