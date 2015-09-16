
import random
import json
from hyphen import Hyphenator, dict_info
from hyphen.dictools import *


def create(content, order):
    bads = set(["'", "--", "-", "_", ";", ":"])
    chain = {}
    chaintop = chain
    for i in range(0,len(content)-order-1):
        
        #first traverse through the dictionary structure,
        #and create the new dictionaries needed
        
        for j in range(0, order):
            if chain.has_key(content[i+j]):
               chain = chain[content[i+j]]
            else:
                chain[content[i+j]] = {}
                chain = chain[content[i+j]]

        #increase the counter that the word precedes the n-gram
            
        if(chain.has_key(content[i+order])):
            chain[content[i+order]] = chain[content[i+order]]+1
        else:
            chain[content[i+order]] = 1
        chain = chaintop
        

    markov = Markov_chain()
    markov.order = order
    markov.chain = chain
    markov.h = Hyphenator('en_US')
    return markov

def create_reverse(content, order):
    return create(list(reversed(content)), order)


class Markov_chain:
    order = 0
    chain = {}
    h = 0

    def generate(self, nwords, seed):

        random.seed()

        if not self.chain.has_key(seed):
            print "NICK CAVE's BAND"
            return
        
        result = [seed] + (['']*(nwords-1))     
        #first generate a random order-length sequence from the seed
        curr_dict = self.chain[seed]
        
        for i in range(1, self.order):
            key_list = curr_dict.keys()
            result[i] = key_list[random.randint(0, len(key_list)-1)]
            curr_dict = curr_dict[result[i]]
            
       
        
        for i in range(0, nwords-self.order):
            curr_dict = self.chain
            
            for j in range(0, self.order):
                curr_dict = curr_dict[result[i+j]]
                
            total = sum(curr_dict.values())
            randval = random.randint(1, total)
            accum = 0
            for k in curr_dict.keys():
                accum += curr_dict[k]
                if accum >= randval:
                    result[i+self.order] = k
                    break
                
                
        return result
    
    def count_syllables(self,text):
        temp = map(unicode, text)
        counter = 0
        for w in temp:
            counter += len(self.h.syllables(w))
        return counter

    def generate_nsyllables(self, nsyllables, seed):

        random.seed()

        if not self.chain.has_key(seed):
            print "NICK CAVE's BAND"
            return
        while True:
            result = [seed]    
            #first generate a random order-length sequence from the seed
            curr_dict = self.chain[seed]
        
            for i in range(1, self.order):
                key_list = curr_dict.keys()
                result.append(key_list[random.randint(0, len(key_list)-1)])
                curr_dict = curr_dict[result[i]]
                
                if self.count_syllables(result) == nsyllables:
                    return result
                if self.count_syllables(result) > nsyllables:
                    return self.generate_nsyllables(nsyllables, seed)
            
       
        
            for i in range(0, 1000):
                curr_dict = self.chain
            
                for j in range(0, self.order):
                    curr_dict = curr_dict[result[i+j]]
                
                total = sum(curr_dict.values())
                randval = random.randint(1, total)
                accum = 0
                for k in curr_dict.keys():
                    accum += curr_dict[k]
                    if accum >= randval:
                        result.append(k)
                        break
                if self.count_syllables(result) == nsyllables:
                    return result
                if self.count_syllables(result) > nsyllables:
                    return self.generate_nsyllables(nsyllables, seed)
                
                
        return result
            
