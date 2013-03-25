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

import nltk
import sys
import os
import pickle
import numpy as np
from PyML import svm, ker, featsel
from PyML.containers.vectorDatasets import SparseDataSet, VectorDataSet
from PyML.classifiers.composite import Chain, FeatureSelect 
from scrapy.conf import settings
from terminal_colors import Tcolors
from PyML.classifiers.svm import loadSVM

class SvmClassifier:
    """
    SVM classifier: Performing training and prediction of sentiment class.
    """
    def __init__(self, lexicon, C=1, num_features=100):
        self.training_set = None
        self.classes = None 
        self.test_set = None
        self.results = None
        self.kernel = ker.Linear()
        self.C = C  
        self.feature_data = PATH + "/learning/stored/feature.data"
        self.label_data = PATH + "/learning/stored/svm_label.data"
        self.lexicon = lexicon
        self.num_features = len(self.lexicon.words.keys())
        try:
            print "Loading existing SVM..."
            features = pickle.load(open(self.feature_data))
            labels = pickle.load(open(self.label_data))
            sparsedata = SparseDataSet(features, L=labels) 
            self.svm_classifier = loadSVM(PATH + "/learning/stored/svm.classifier",sparsedata)
        except Exception as e:
            print e
            print "Existing SVM not found!"
            self.svm_classifier = svm.SVM(self.kernel)
        self.accuracy = None
        self.predicted_labels = None
        score = featsel.FeatureScore('golub')
        self.filter = featsel.Filter(score)
        self.feature_selector = FeatureSelect(self.svm_classifier, self.filter)
        self.chain = Chain([self.feature_selector, self.svm_classifier])
        
    def classify(self, sentences, labels):
        self.test_set = self.compute_features(sentences)
        print
        print Tcolors.ACT + " Classifying instance with SVM: " + Tcolors.RED + sentences[0] + Tcolors.C
        print Tcolors.HEADER
        test_data = SparseDataSet(self.test_set, L=labels)
        self.results = self.svm_classifier.test(test_data)
        print Tcolors.C 
        return self.results
    
    def compute_features(self, sentences): 
        features = [] 
        for i,sent in enumerate(sentences):
            sent = sent.lower()
            words = nltk.word_tokenize(sent)     
            feature = np.zeros(self.num_features) 
            for word in words:
                if word.lower() in self.lexicon.words.keys():
                    feature[self.lexicon.words.keys().index(word)] = 1
            features.append(feature) 
        return features  
    
    def initialize_lexicon(self):
        pass
    
    def print_stats(self): 
        print "[*] SVM Classifier ACCURACY: ", self.accuracy
        print "[*] SVM Classifier PREDICTED_LABEL: ", self.predicted_labels[0]
    
    def stats(self):
        self.accuracy = self.results.getSuccessRate()
        self.predicted_labels = self.results.getPredictedLabels()        
    
    def save(self,data,features,labels):
        output = open(self.feature_data ,'wb')
        pickle.dump(features,output)
        output.close()
        output = open(self.label_data,'wb')
        pickle.dump(labels,output)
        output.close()
        self.svm_classifier.save(PATH + "/learning/stored/svm.classifier")
        
    def train(self, training_set, labels):
        print Tcolors.ACT + " Training SVM with chaining..."
        features = self.compute_features(training_set) 
        data = SparseDataSet(features, L=labels) 
        print Tcolors.CYAN
        self.training_set = data 
        self.svm_classifier.train(data)     
        self.save(data,features,labels)
        print Tcolors.C
     
        
