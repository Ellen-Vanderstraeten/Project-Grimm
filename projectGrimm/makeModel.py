import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim') # to filter out the warning

import os, heapq, string, re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from gensim import corpora, models, similarities
import glob
from collections import Counter, defaultdict
import io
import operator
from pprint import pprint
import numpy as np

'''Load multiple files from the 'Versions' folder into a list in order to access all the fairy tales.'''
file_place = glob.glob(os.path.join(os.getcwd(), "Versions", "*.txt"))

corpus = []

def RemovePunctDigits(text):
    punctList = "“„‘‚" + string.punctuation + string.digits
    output =""
    for i in text:
        if not (i in punctList):
            output = output + i
    return output

'''Create a dictionary in order to access the name of fairy tales and their respective place.'''
PlaceDict_Name_to_Place = {} #dictionary for place of file and its indexnumber
i = 0 #counter

for file in file_place:
    PlaceDict_Name_to_Place[file.split("\\")[-1]] = i
    i += 1
    with io.open(file, "r", encoding="utf-8") as fairy_tale:
        corpus.append(RemovePunctDigits(fairy_tale.read()))
#print("Number of Grimm fairy tales:" , len(corpus))
#print(corpus[0])

'''Create a dictionary in order to access the place of a fairy tale and give the name. Reverse of the dictionary above.'''
PlaceDict_Place_to_Name = dict((value, key) for key, value in PlaceDict_Name_to_Place.items())


''' Create Stoplist: first filter out punctuation and then common words. Gensim provides the most commom words for the English language but not for German.'''
WordCount = {}
for fairy_tale in corpus:
    words = fairy_tale.lower().split()
    for word in words:
        if word not in WordCount:
            WordCount[word] = 1
        else:
            WordCount[word] += 1

Highest_values = dict(sorted(WordCount.items(),key=operator.itemgetter(1), reverse=True)[:10]) #reverse want we willen de hoogste cijfers.
#print(Highest_values)

Lowest_values = dict(sorted(WordCount.items(),key=operator.itemgetter(1), reverse=False)[:30])
#print(Lowest_values)

def tokenize(docs, stoplist):
    texts = []
    for doc in docs:
        t = [word for word in doc.lower().split() if word not in stoplist]
        texts.append(t)
    return texts 

'''Eliminate those words that only occur once in the corpus'''
stoplist = list(Highest_values.keys())
texts = tokenize(corpus, stoplist)
print(stoplist)

def RemoveOccurencesOfOne(texts):
    output = []
    for text in texts:
        t = []
        for token in text:
            if WordCount[token] > 1:
                t.append(token)
        output.append(t)
    return output

texts = RemoveOccurencesOfOne(texts)
#pprint(texts)

dictionary = corpora.Dictionary(texts)
#print(dictionary.token2id)

VectorizedTexts = []

for text in texts:
    VectorizedTexts.append(dictionary.doc2bow(text))
#print(VectorizedTexts)

tfidf = models.TfidfModel(VectorizedTexts) #make tfidf for all fairy tales in vectorized texts; making the model
SimilaritiesMAtrix = similarities.SparseMatrixSimilarity(tfidf[VectorizedTexts], num_features=len(dictionary)) #applying the model on the fairy tales.
'''num_features = aantal unieke woorden in het corpus'''


'''Application of model on corpus by creating functions'''
def SimilarityDegreeFairyTales(NameFairyTale, SimilarityPercentage):
    WordSims = SimilaritiesMAtrix[tfidf[VectorizedTexts[PlaceDict_Name_to_Place[NameFairyTale]]]]
    Similarity_degree_documents = list(enumerate(WordSims))
    '''Filter out those fairy tales with a low similarity by creating a list for those fairy tales with a large similarity.'''
    Large_Similarity_Degree = []
    for fairy_tale in Similarity_degree_documents:
        if fairy_tale[1] > SimilarityPercentage/100: 
            Large_Similarity_Degree.append((PlaceDict_Place_to_Name[fairy_tale[0]], fairy_tale[1])) 
            '''Call place of fairy and put in PlaceDict_Place_to_Name which returns the name of the fairy tale.'''
    return Large_Similarity_Degree
#print(SimilarityDegreeFairyTales("H%C3%A4nsel_und_Grethel_(1857).txt", 50))

def GetSameFairyTales(name):
    NameList =[]
    for key, value in PlaceDict_Name_to_Place.items():
        if name in key:
            NameList.append(key)
    return NameList
#pprint(GetSameFairyTales("Rapunzel"))

'''Test functions: Example'''
Test_Corpus = GetSameFairyTales("Rapunzel")
Similarities_Test_Corpus = []
for fairy_tale in Test_Corpus:
    Similarities_Test_Corpus.append((fairy_tale, SimilarityDegreeFairyTales(fairy_tale, 50)))
#pprint(Similarities_Test_Corpus)


'''Visualization of word frequency in different versions of a fairy tale'''
Same_FairyTales = []
Name_of_FairyTale = GetSameFairyTales("Rapunzel")
for fairy_tale in Name_of_FairyTale:
    Same_FairyTales.append(VectorizedTexts[PlaceDict_Name_to_Place[fairy_tale]])

colors = cm.rainbow(np.linspace(0, 1, len(Name_of_FairyTale)))

counter = 0
docs = tfidf[Same_FairyTales]
Most_Used_Words_in_docs = {}
Most_Used_Words_for_each_doc = []

'''Dictionary with all the words which we're going to plot and respective place of word.'''
for doc in docs:
    Highest_FrequencyWords = heapq.nlargest(10, doc, key=operator.itemgetter(1))
    for word in Highest_FrequencyWords:
        if word[0] not in Most_Used_Words_in_docs:
            Most_Used_Words_in_docs[word[0]] = len(Most_Used_Words_in_docs)
    Most_Used_Words_for_each_doc.append(Highest_FrequencyWords)

'''List which contains place and name of word.'''
for doc in Most_Used_Words_for_each_doc:
    Place_of_Word = []
    Frequency_of_Word = []    
    for word in doc:
        Place_of_Word.append(Most_Used_Words_in_docs[word[0]]) #id woord
        Frequency_of_Word.append(word[1])#frequency woord
    plt.scatter(Place_of_Word, Frequency_of_Word, color=colors[counter], label=Name_of_FairyTale[counter])
    plt.legend(bbox_to_anchor=(1.09, 0.9), loc=counter + 1, borderaxespad=0.)# locatie begint van 1 te tellen en niet van 0
    counter +=1

WordNames = []
for word in sorted(Most_Used_Words_in_docs.items(),key=operator.itemgetter(1), reverse=False):
    WordNames.append(dictionary[word[0]])

plt.xticks(range(0,len(Most_Used_Words_in_docs)), WordNames, rotation=90)
#plt.show()
