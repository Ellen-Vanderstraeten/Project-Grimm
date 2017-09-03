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

'''Create a dictionary in order to access the name of fairy tales and their respective place.'''
PlaceDict_Name_to_Place = {} #dictionary for place of file and its indexnumber
i = 0 #counter

for file in file_place:
    PlaceDict_Name_to_Place[file.split("\\")[-1]] = i
    i += 1
    with io.open(file, "r", encoding="utf-8") as fairy_tale:
        corpus.append(fairy_tale.read())

'''Create a dictionary in order to access the place of a fairy tale and give the name. Reverse of the dict above.'''
PlaceDict_Place_to_Name = dict((value, key) for key, value in PlaceDict_Name_to_Place.items())

def RemovePunctDigits(text):
    punctList = "“„‘‚" + string.punctuation + string.digits
    output =""
    for i in text:
        if not (i in punctList):
            output = output + i
    return output

stoplist = ['er', 'sie', 'es', 'und', 'in', 'der', 'da', 'das', 'die', 'den']

Fairy_Tale_TestCorpus = []

for fairy_tale in corpus:
	fairy_tale_Sentences = []
	for sentence in re.split("[.|!|?]", fairy_tale.lower()):
		clean_line = RemovePunctDigits(sentence)
		fairy_tale_sentence_words = []
		for word in clean_line.split():
			if word not in stoplist:
				fairy_tale_sentence_words.append(word)
		fairy_tale_Sentences.append(fairy_tale_sentence_words)
	Fairy_Tale_TestCorpus.append(fairy_tale_Sentences)


def GetSameFairyTales(name):
    NameList =[]
    for key, value in PlaceDict_Name_to_Place.items():
        if name in key:
            NameList.append(key)
    return NameList


FairyTale1 = GetSameFairyTales("H%C3%A4nsel_und_")
FairyTale2 = GetSameFairyTales("Aschenputtel_")


FairyTale1_Sentences = []
for fairy_tale in FairyTale1:
	for sentence in Fairy_Tale_TestCorpus[PlaceDict_Name_to_Place[fairy_tale]]:
		FairyTale1_Sentences.append(sentence)

FairyTale2_Sentences = []
for fairy_tale in FairyTale2:
	for sentences in Fairy_Tale_TestCorpus[PlaceDict_Name_to_Place[fairy_tale]]:
		FairyTale2_Sentences.append(sentences)

model1 = models.Word2Vec(FairyTale1_Sentences, min_count=1) 
model2 = models.Word2Vec(FairyTale2_Sentences, min_count=1) 

java_path = r"C:\Program Files\Java\jre1.8.0_111\bin\java.exe"
os.environ['JAVAHOME'] = java_path

jar = r'C:\Users\Ellen\Desktop\projectGrimm\projectGrimm\projectGrimm\stanford-postagger-full-2017-06-09\stanford-postagger-full-2017-06-09\stanford-postagger.jar'
modelMap = r'C:\Users\Ellen\Desktop\projectGrimm\projectGrimm\projectGrimm\stanford-postagger-full-2017-06-09\stanford-postagger-full-2017-06-09\models\german-fast-caseless.tagger'

pos_tagger = StanfordPOSTagger(modelMap, jar)


def fairytaleContainsWord(word, fairyTale):
	for sentence in fairyTale:
		if word in sentence:
			return True
	return False

UniqueWordList = set()
for fairy_tale in Fairy_Tale_TestCorpus:
	for sentence in fairy_tale:
		for word in sentence:
			if fairytaleContainsWord(word, FairyTale1_Sentences) and fairytaleContainsWord(word,FairyTale2_Sentences) and (word not in UniqueWordList):
				UniqueWordList.add(word)


Only_ADJD = []
Speech_Type_Word = pos_tagger.tag(UniqueWordList)
for words in Speech_Type_Word:
	if words[1] == "ADJD": #only want nouns and adjectives
		Only_ADJD.append(words[0])


def CompareWordSimilarity(term, number_of_topwords, model):
	WordSimilarity = []
	for word in Only_ADJD:
		WordSimilarity.append((word, model.similarity(term, word)))
	return sorted(WordSimilarity,key=operator.itemgetter(1), reverse=True)[:number_of_topwords]

TestWordsList = ["stiefmutter", "vater"]
Output_FairyTale1 = []
for word in TestWordsList:
	Output_FairyTale1.append((word, CompareWordSimilarity(word, 10, model1)))
pprint(Output_FairyTale1)

Output_FairyTale2 = []
for word in TestWordsList:
	Output_FairyTale2.append((word, CompareWordSimilarity(word, 10, model2)))
pprint(Output_FairyTale2)

