from nltk.corpus import cmudict

execfile("../markov_chains/markov_chains.py")

def rhymes(word1, word2, prondict):
    try:
        pron1 = prondict[word1][0]
        pron2 = prondict[word2][0]

        len1 = len(pron1)
        len2 = len(pron2)
    except KeyError:
        return False

    return (pron1[len1-1] == pron2[len2-1]) and  (pron1[len1-2] == pron2[len2-2])

def alliterate(word1, word2):
    prondict = cmudict.dict()
    pron1 = prondict[word1][0]
    pron2 = prondict[word2][0]
    
    return pron1[0] == pron2[0]


def rhyming_list(word, all_words):
    prondict = cmudict.dict()
    result = []
    for w in all_words:
        if rhymes(word, w, prondict):
            result.append(w)
    return result


def rhyminglines(markov, re_markov, length, seed):
    while True:
        first_line = markov.generate(length, seed)    
        random.seed()
        rhymes = rhyming_list(first_line[len(first_line)-1], markov.chain.keys())
        if rhymes == []:
            continue
        rhyming_word = rhymes[random.randint(0, len(rhymes)-1)]
        second_line = reversed(re_markov.generate(length, rhyming_word))
        return ' '.join(first_line) + '\n' + ' '.join(second_line)
    
def generate_line(markov, seed, syllablecount):
    return markov.generate_nsyllables(syllablecount, seed)

def generate_rhyming_line(rev_markov, line1, syllablecount):
    
    while True:   
        random.seed()
        rhymes = rhyming_list(line1[len(line1)-1], rev_markov.chain.keys())
        if rhymes == []:
            continue
        rhyming_word = rhymes[random.randint(0, len(rhymes)-1)]
        second_line = list(reversed(rev_markov.generate_nsyllables(syllablecount, rhyming_word)))
        return second_line



