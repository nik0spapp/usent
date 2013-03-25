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

p_flag = False
n_flag = False
b_flag = False

positives = {} #{"word1":{"typ":"", "pos1":"", "priorpolarity":}}
negatives = {} #{"word1":{"type":"", "pos1":"", "priorpolarity":}} 
emoticons_file = open("datasets/emoticons.data","r")
lines = emoticons_file.readlines()

def patch_emoticons():
    global p_flag, n_flag, b_flag
    
    for line in lines:
        if line.startswith("positive"):
            print "Parsing Positives...." 
            p_flag = True    
            n_flag = False
            
        elif line.startswith("negative"):
            print "Parsing Negatives...."
            n_flag = True
            p_flag = False
            
        elif line.startswith("bad_words"):
            n_flag = False
            p_flag = False
            b_flag = True
            
        if p_flag and not line.startswith("positive"):
            p_data = line.split(" ")
            for data in p_data:
                positives[data] = {"type":"strongsub", "emoticon" : True, "pos1":"anypos", "priorpolarity":"positive"}   
        
        if n_flag and not line.startswith("negative"):
            n_data = line.split(" ")
            for data in n_data:
                negatives[data] = {"type":"strongsub", "emoticon" : True, "pos1":"anypos", "priorpolarity":"negative"}
                        
        if b_flag and not line.startswith("bad_words"):
            word = line.replace("\n", "")
            negatives[word] = {"type":"strongsub", "pos1":"anypos", "priorpolarity":"negative"}
    totals = dict(positives, **negatives) 
    return totals
    
def parse_dataset(filename):    
    parsed_data = []
    dataset = open(os.path.abspath("") +"/"+ filename,"r")
    lines = dataset.readlines()
    
    for line in lines:
        parsed_data.append(line.replace("\n", ""))
    return parsed_data

                
    
        
        
        


