import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim') # to filter out the warning

import os, string, re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from gensim import corpora, models, similarities
import glob
from collections import Counter, defaultdict
import io
import operator
from pprint import pprint
import numpy as np
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize

'''Load multiple files from the Versions folder into a list in order to access all the files.'''
file_place = glob.glob(os.path.join(os.getcwd(), "Versions", "*.txt"))
corpus = []

for file in file_place:
    with io.open(file, "r", encoding="utf-8") as fairy_tale:
        corpus.append(fairy_tale.read())

def RemovePunctDigits(text):
    punctList = "“„‘‚" + string.punctuation + string.digits
    output =""
    for i in text:
        if not (i in punctList):
            output = output + i
    return output

stoplist = ['er', 'sie', 'es', 'und', 'in', 'der', 'da', 'das', 'die', 'den']

Sentence_Corpus = []

for fairy_tale in corpus:
	for sentence in re.split("[.|!|?]", fairy_tale.lower()):
		clean_line = RemovePunctDigits(sentence)
		fairy_tale_sentence_words = []
		for word in clean_line.split():
			if word not in stoplist:
				fairy_tale_sentence_words.append(word)
		Sentence_Corpus.append(fairy_tale_sentence_words)
#pprint(Sentence_Corpus[0])

model = models.Word2Vec(Sentence_Corpus, min_count=1) 

'''Import speech tagger so that only adjectives remain'''
java_path = r"C:\Program Files\Java\jre1.8.0_111\bin\java.exe"
os.environ['JAVAHOME'] = java_path

jar = r'C:\Users\Ellen\Desktop\projectGrimm\projectGrimm\projectGrimm\stanford-postagger-full-2017-06-09\stanford-postagger-full-2017-06-09\stanford-postagger.jar'
modelMap = r'C:\Users\Ellen\Desktop\projectGrimm\projectGrimm\projectGrimm\stanford-postagger-full-2017-06-09\stanford-postagger-full-2017-06-09\models\german-fast-caseless.tagger'

pos_tagger = StanfordPOSTagger(modelMap, jar)

UniqueWordList = set()
for sentence in Sentence_Corpus:
	for word in sentence:
		if word not in UniqueWordList:
			UniqueWordList.add(word)

Only_ADJD = []
Speech_Type_Word = pos_tagger.tag(UniqueWordList)
for words in Speech_Type_Word:
	if words[1] == "ADJD": #only want nouns and adjectives
		Only_ADJD.append(words[0])


def CompareWordSimilarity(term, number_of_topwords):
	WordSimilarity = []
	for word in Only_NN_and_ADJD:
		WordSimilarity.append((word, model.similarity(term, word)))
	return sorted(WordSimilarity,key=operator.itemgetter(1), reverse=True)[:number_of_topwords]

'''Test function'''
TestWordsList = ["stiefmutter", "vater", "kind", "hänsel", "gretel"]
OutputList = []
for word in TestWordsList:
	OutputList.append((word, CompareWordSimilarity(word, 10)))
pprint(OutputList)
