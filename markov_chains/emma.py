import urllib2
import nltk


text_source = "http://www.gutenberg.org/cache/epub/158/pg158.txt"
data = urllib2.urlopen(text_source)
content_text = data.read()

#this is to omit the non-fiction parts of the text
start = content_text.find("*** START OF THIS PROJECT GUTENBERG")
end = content_text.rfind("End of the Project Gutenberg")

content = content_text[start:end]


tokens = nltk.word_tokenize(content)
model = nltk.NgramModel(6, tokens)

generated_content = model.generate(50, ['Emma']);
print ' '.join(generated_content)

