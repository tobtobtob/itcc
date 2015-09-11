import urllib2
import nltk
import markov_chains
import json
import random


def create(content, order):
    chain = {}
    chaintop = chain
    print len(content)
    for i in range(0,len(content)-order-1):
        print "JEE"
        #first traverse throug the dictionary structure,
        #and create the new dictionaries needed
        for j in range(0, order):
            if chain.has_key(content[i+j]):
               chain = chain[content[i+j]]
            else:
                chain[content[i+j]] = {}
                chain = chain[content[i+j]]

        #increase the counter for sum of amounts of successors

        #if(chain.has_key('COUNTER')):
        #    chain['COUNTER'] = chain['COUNTER']+1
        #else:
        #    chain['COUNTER'] = 1

        #increase the counter that the word precedes the n-gram
            
        if(chain.has_key(content[i+order])):
            chain[content[i+order]] = chain[content[i+order]]+1
        else:
            chain[content[i+order]] = 1
        chain = chaintop
        print json.dumps(chain)

    markov = Markov_chain()
    markov.order = order
    markov.chain = chain
    
    return markov


class Markov_chain:
    order = 0
    chain = {}

    def generate(self, nwords):
        random.seed()
        result = ['']*(nwords)
        #first generate a random order-length sequence from the seed
        curr_dict = self.chain
        for i in range(0,self.order):
            key_list = curr_dict.keys()
            result[i] = key_list[random.randint(0, len(key_list)-1)]
            curr_dict = curr_dict[result[i]]
        print ' '.join(result[0:self.order])
        
            
                                


text_source = "http://www.gutenberg.org/cache/epub/158/pg158.txt"
data = urllib2.urlopen(text_source)
content_text = data.read()

#this is to omit the non-fiction parts of the text
start = content_text.find("*** START OF THIS PROJECT GUTENBERG")
end = content_text.rfind("End of the Project Gutenberg")

con = content_text[start:(start+1000)]


tokens = nltk.word_tokenize(con)
#model = nltk.NgramModel(6, tokens)
#generated_content = model.generate(50, ['Emma']);

model = create(tokens, 2)
print json.dumps(model.chain)
model.generate(10)
#print ' '.join(generated_content)



