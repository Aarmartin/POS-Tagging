# Part of Speech Tagging
This data is taken from the POS tagged portion of the Penn 
Treebank WSJ corpus. 

This program is designed to identify the relevant part of speech of individual words within a body of text. There are three stages to this development
* tagger-train.py
  * This script takes in a corpus of words and their associated parts of speech to determine POS probabilities for each word
* tagger-test.py
  * This takes in a body of text and calculates their most probable POS tag based on the probabilities found in the previous program
* tagger-eval.py
  * This final program grades the accuracy of each tag

There are also two separate modes that can be used
* Mode 0
  * This mode simply takes the most frequent associated tag for each word
* Mode 1
  * This mode is the frequency with enhanced measures taken, such as context clues and grammatical POS rules

# Running the program
This program is in three parts, and is run in the format
```
python3 tagger-train.py pos-train.txt > tagger-train-prob.txt
python3 tagger-test.py <MODE> tagger-train-prob.txt pos-test.txt > pos-test-<MODE>.txt
python3 tagger-eval.py pos-test-key.txt pos-test-<MODE>.txt > pos-test-<MODE>-eval.txt
```
Where \<MODE\> is the associated algorithm chosen
