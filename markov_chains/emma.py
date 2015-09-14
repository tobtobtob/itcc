import urllib2
import nltk
import markov_chains
import json
import random
            

content = open('emma.txt', 'r').read()
tokens = nltk.word_tokenize(content)
model = create(tokens, 5)

print model.generate(100)

