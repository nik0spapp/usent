unsupervised_sentiment
======================

Dependencies
------------
Install Python
Install pip

$ pip install nltk
$ pip install stemmer
$ pip install numpy
$ pip install pickle

Download http://pyml.sourceforge.net/
tar zxvf PyML-0.7.11.tar.gz
cd PyML-0.7.11
python setup.py build
python setup.py install


Current pipeline
----------------
- Subjectivity classification
  * bootstrapping with pattern-based learner
- Polarity classification
  * bootstrapping with self-trained SVM (optional)

Examples
--------
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


