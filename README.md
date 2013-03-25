unsupervised_sentiment
======================

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
tokenizers/punkt/english, wordnet, brown, conll2000 and treebank. 

Lastly, pyml library is needed for the SVM classifier that is used currently in our code. <br />
Download http://pyml.sourceforge.net/  <br />
```bash 
 $ tar zxvf PyML-0.7.11.tar.gz
 $ cd PyML-0.7.11
 $ python setup.py build
 $ python setup.py install 
```


Current pipeline
----------------
- Subjectivity classification
  * bootstrapping with pattern-based learner
- Polarity classification
  * bootstrapping with self-trained SVM (optional)

Examples
--------
```bash
$ python sentiment.py "I have to give much love and respect to Rony. Your work is Amazing\!"

[*] Checking block of text:
[1] I have to give much love and respect to Rony.
[2] Your work is Amazing\!

 subjective-----> 100.00%
 objective------> 0.00%
 
 positive-------> 100.00%
 neutral--------> 0.00%
 negative-------> 0.00%

[x] positive (7.00, 0.96)
```

```bash
$ python sentiment.py "I was blown away by some of the comments here posted by people who is either uneducated, ignorant, self-righteous or al-of-the-above. I'm irritated and saddened as I read these finger-pointing\"g or \"i'm right and you're wrong\" type of posts\!"

[*] Checking block of text:
[1] I was blown away by some of the comments here posted by people who is either uneducated, ignorant, self-righteous or al-of-the-above.
[2] I'm irritated and saddened as I read these finger-pointing"g or "i'm right and you're wrong" type of posts!

 subjective-----> 100.00%
 objective------> 0.00%

 positive-------> 0.00%
 neutral--------> 0.00%
 negative-------> 100.00%

[x] negative (-8.00, -0.32)
```

```bash
$ python sentiment.py "I found your presentation amazing! However, some of your results are misleading,  unjustified and irrational."

[*] Checking block of text:
[1] I found your presentation amazing!
[2] However, some of your results are misleading, unjustified and irrational.

 subjective-----> 100.00%
 objective------> 0.00%

 positive-------> 50.00%
 neutral--------> 0.00%
 negative-------> 50.00%

[x] negative (-4.00, 0.23)
```



