Dictionary-based sentiment detection
======================
The attached code is an implementation of an unsupervised sentiment classification procedure that was used originally for an opinion mining
and retrieval system (1st paper below) and for improving one-class collaborative filtering (2nd paper below). For the 2nd paper
I have included a folder called "TED_comment_annotations" that contains the files of the human study we conducted on TED 
comment sentiment classification (with 6 human annotators). In case you use the code or the human annotations of TED 
comments for your research please cite the following papers:
<ul>
<li>
Nikolaos Pappas, Georgios Katsimpras, Efstathios Stamatatos, <i>Distinguishing the Popularity Between Topics: A System for Up-to-date Opinion Retrieval and Mining in the Web</i>, 14th International Conference on Intelligent Text Processing and Computational Linguistics, Samos, Greece, LNCS, Springer, 2013 <br /> 
<a href="http://publications.idiap.ch/downloads/papers/2013/Pappas_CICLING_2013.pdf" target="_blank">http://publications.idiap.ch/downloads/papers/2013/Pappas_CICLING_2013.pdf</a>
</li> 
<li>
Nikolaos Pappas, Andrei Popescu-Belis, <i>Sentiment Analysis of User Comments for One-Class Collaborative Filtering over TED Talks, 36th ACM SIGIR Conference on Research and Development in Information Retrieval, Short papers, Dublin, Ireland, ACM, 2013 <br /> 
<a href="http://publications.idiap.ch/downloads/papers/2013/Pappas_SIGIR_2013.pdf" target="_blank">http://publications.idiap.ch/downloads/papers/2013/Pappas_SIGIR_2013.pdf</a>
</li>
</ul>

The method combines two different bootstrapping procedures, namely for subjectivity and polarity detection (1st
and 2nd paper accordingly). The rule-based polarity classifier is an extension of the one that was presented in 
the 3rd paper listed below.

- E. Riloff and J. Wiebe. Learning extraction patterns for subjective expressions.
In Proceedings of the 2003 conference on Empirical methods in natural language
processing, EMNLP ’03, 2003.  <br />
<a href="http://www.cs.utah.edu/~riloff/pdfs/emnlp03.pdf" target="_blank">http://www.cs.utah.edu/~riloff/pdfs/emnlp03.pdf</a>
- D. K. M Wiegand. Bootstrapping supervised machine-learning polarity classifiers with rule-based classification. 
In Proceedings of the ECAI-Workshop on Computational Approaches to Subjectivity and Sentiment Analysis (WASSA), 2009.  <br />
<a href="http://www.lsv.uni-saarland.de/wassa.pdf" target="_blank">http://www.lsv.uni-saarland.de/wassa.pdf</a>
- T. Wilson, J. Wiebe, and P. Hoffmann. Recognizing contextual polarity in phrase-level sentiment 
analysis. In Proceedings of the conference on Human Language Technology and Empirical Methods in 
Natural Language Processing, HLT ’05, 2005. <br />
<a href="http://people.cs.pitt.edu/~wiebe/pubs/papers/emnlp05polarity.pdf" target="_blank">http://people.cs.pitt.edu/~wiebe/pubs/papers/emnlp05polarity.pdf</a>

Dependencies
------------
The available code for unsupervised sentiment classification requires Python programming 
language and pip package manager to run. For detailed installing instructions please refer to 
the following links: <br />
http://www.python.org/getit/ <br />
http://www.pip-installer.org/en/latest/

After installing them, you should be able to install the following packages: <br />
```bash
$ pip install nltk  
$ pip install stemmer 
$ pip install numpy
$ pip install pickle 
```

After you install nltk you will need some corpora to train the sequential POS tagger (pos.py) and the nltk tokenizer.
```bash
$ python 
```
```python
import nltk 
nltk.download() 
```  
The issue of the above command will load a graphical interface that lets you manage several corpora
related to nltk library. From the list select and download the following corpora: 
*tokenizers/punkt/english*, *wordnet*, *brown*, *conll2000* and *treebank*. 

Lastly, pyml library is needed for the SVM classifier that is used currently in our code. <br />
Download http://pyml.sourceforge.net/ and then issue: <br />
```bash 
 $ tar zxvf PyML-0.7.11.tar.gz
 $ cd PyML-0.7.11
 $ python setup.py build
 $ python setup.py install 
```


Processing pipeline
-------------------
The current pipline that is implemented in sentiment.py is depicted in the following diagram. Initially,
the input text is split into sentences and each sentence is fed to a high precision subjectivity classifier.
If the sentence is classified as subjective then syntactic patterns are learned from this instance. In case 
that the sentence is not detected as such then it is fed to the pattern-based classifier. The pattern-based
classifier outputs the class of the sentence based on the learned patterns so far. If the instance is subjective
then again more patterns are learned from it, otherwise it is fed to a high precision objectivity classifier.
If the sentence is classified as objective, then it is ignored, otherwise it is fed to the polarity classifier.

Finally, the polarity classifier estimates the numerical sentiment and normalized sentiment values and outputs
the result. The instances with high confidence from the polarity classifier can be further used to train an SVM 
classifier to improve further the classification performance (see paper for further details). At the current version
this option is disabled, but you can easily enable it. Similarly, you can remove some of the components from the 
pipeline according to your needs (e.g. skip subjectivity classification).


![ScreenShot](https://raw.github.com/nik0spapp/unsupervised_sentiment/master/examples/bootstrap.png)

Examples
--------
To estimate the total sentiment and total normalized sentiment (as described in the papers), 
you can simply execute the sentiment.py file and give the desired block of text as an argument.
Make sure that you escape symbols such as '"' and '!'. Apart from the command line execution you 
can integrate the library to your code and use directly the returned results. Below you can 
find two simple examples for demonstrating purposes:

```bash
$ python sentiment.py "I have to give much love and respect to Rony. Your work is Amazing\!"
```
![ScreenShot](https://raw.github.com/nik0spapp/unsupervised_sentiment/master/examples/1.png)



```bash
$ python sentiment.py "I was blown away by some of the comments here posted by people who is either 
uneducated, ignorant, self-righteous or al-of-the-above. I'm irritated and saddened as I read these 
finger-pointing \"i'm right and you're wrong\" type of posts\!"
```
![ScreenShot](https://raw.github.com/nik0spapp/unsupervised_sentiment/master/examples/2.png)


