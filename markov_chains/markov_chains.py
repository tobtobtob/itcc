
import random


def create(content, order):
    chain = {}
    chaintop = chain
    for i in range(0,len(content)-order-1):
        
        #first traverse throug the dictionary structure,
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


class Markov_chain:
    order = 0
    chain = {}

    def generate(self, nwords):
        
        random.seed()
        result = ['']*(nwords)       
        #first generate a random order-length sequence from the seed
        curr_dict = self.chain
        for i in range(0, self.order):
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
                
                
        return ' '.join(result)
            
