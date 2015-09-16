import nltk
import rhymes

execfile("../markov_chains/markov_chains.py")
execfile("rhymes.py")

marks = set(['?', '.', '!', ',', ';', ':', '`', '``', '-', '--', "''"])

def only_words(tokenized_content):
    ret = []
    for w in tokenized_content:
        if w not in marks:
            ret.append(w)
    return ret


f = open('emma.txt', 'r')
corpus = nltk.word_tokenize(f.read().lower())
corpus = only_words(corpus)

try:
    markov.chain
except NameError:
    markov = create(corpus, 3)
    rev_markov = create_reverse(corpus, 3)

print len(corpus)

line1 = generate_line(markov, "emma", 7)
line2 = generate_rhyming_line(rev_markov, line1, 7)
line3 = generate_line(markov, "she", 5)
line4 = generate_rhyming_line(rev_markov, line3, 5)
line5 = generate_rhyming_line(rev_markov, line2, 7)

print ' '.join(line1) + '\n' + ' '.join(line2)+ '\n' + ' '.join(line3)+ '\n' + ' '.join(line4)+ '\n' + ' '.join(line5)
