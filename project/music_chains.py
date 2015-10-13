
import random
import json


def create(content, order):
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
    return markov

def create_reverse(content, order):
    return create(list(reversed(content)), order)

def smooth(chain, f):
    if isinstance(chain.values()[0], int):
        for k in chain.keys():
            chain[k] = f(chain[k])
    else:
        for k in chain.keys():
            smooth(chain[k], f)


class Markov_chain:
    order = 0
    chain = {}
    def get_chain(self):
        return chain

    def evaluate(self, individual):
        counter = 0
        for i in range(len(individual)-self.order-1):
            chain = self.chain
            for j in range(self.order):
                if not chain.has_key(individual[i+j]):
                    break
                chain = chain[individual[i+j]]
                if j == self.order-1:
                    if chain.has_key(individual[i+j+1]):
                        counter = counter+chain[individual[i+j+1]]
        return counter      
            

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
   
            
