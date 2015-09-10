
def create(content, order):
    chain = {}
    for i in range(0,len(content)-order-1):
        
        tempchain = chain

        #first traverse throug the dictionary structure,
        #and create the new dictionaries needed
        for j in range(0, order):
            if tempchain.has_key(content[i+j]):
               tempchain = tempchain[content[i+j]]
            else:
                tempchain[content[i+j]] = {}
                tempchain = tempchain[content[i+j]]

        #increase the counter for sum of amounts of successors

        if(tempchain.has_key('COUNTER')):
            tempchain['COUNTER'] = tempchain['COUNTER']+1
        else:
            tempchain['COUNTER'] = 1

        #increase the counter that the word precedes the n-gram
            
        if(tempchain.has_key(content[i+order])):
            tempchain[content[i+order]] = tempchain[content[i+order]]+1
        else:
            tempchain[content[i+order]] = 1

    markov = Markov_chain()
    markov.order = order
    markov.chain = chain
    
    return markov


class Markov_chain:
    order = 0
    chain = {}

    def generate(seed, length):
        result = ['']*length

    
    

                                 





