import numpy as np
import time
from nltk.corpus import stopwords

#from LinearInformationPropagation import LIP
from KeywordExtractionModule import LIPGreedy
from EmbeddingModule import EmbeddingsReader
from ArxivDataModule import ArxivReader
from ArxivDataModule import ArxivManager
import pprint
import platform

from collections import Counter

lambda_ = .3

#Clock in time
start = time.time()
if(platform.system() == 'Windows'):
	common_words_path = 'C:\\Users\\Jona Q\\Documents\\Embeddings\\20k.txt'
	text_data_path = "C:\\Users\\Jona Q\\Documents\GitHub\\Arxiv\\Data\\Text\\voxelHashing.txt"

else:
	common_words_path = '/home/jonathan/Documents/WordEmbedding/20Newsgroups/Data/20k.txt'
	text_data_path = "/home/jonathan/Documents/WordEmbedding/Arxiv/Data/Text/donQuixote.txt"


#Get embeddings
embObj = EmbeddingsReader()
normalize = True
embeddings = embObj.readEmbeddings(normalize)
#Store arrays with all embedding values
values_array = embObj.valuesArray()
print(type(values_array))
keys_array = embObj.keysArray()
print(values_array[0])


#Create stopwords set
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
common_words_file = open(common_words_path, 'r')
common_words_list = [word for line in common_words_file for word in line.split()]
common_words_file.close()
#Select the top num_common_words words to remove from vocabulary
num_common_words = 600
#Update stopwrd set with common words
stop_words.update(common_words_list[0:num_common_words])
#Convert to unicode
if(platform.system() == 'Windows'):
	stop_words = [word for word in stop_words]
else:
    stop_words = [unicode(word) for word in stop_words]


arxivReader = ArxivReader()
text_data = arxivReader.readFileSplitByParagraphs(text_data_path)
print(len(text_data), ' paragraphs\n')
results = []
for i in range(len(text_data)):
	print('Paragraph ', i, '\n')
	message = text_data[i]
	#print message
	#Map all words to their embeddings
	message = [[embeddings.get(word) for word in sentences if word not in stop_words and embeddings.get(word) is not None] for sentences in message]
	#Check for empty sentences (after common and stop word removal)
	message = [sen for sen in message if len(sen) > 0]

	lip = LIPGreedy(message, embObj.embeddingSize(), lambda_, 'euclidean')
	lip.computeBoundary()
	lip.selectKeywords()
	r = lip.getResults(values_array, keys_array)
	results += r

results.sort()
print(results)
cnt = Counter(results)
print('Extracted keywords')
k = 1
if(platform.system() == 'Windows'):
	print([word for word, occur in iter(cnt.items()) if occur > k])
else:
    print([word for word, occur in cnt.iteritems() if occur > k])



"""arxivManager = ArxivManager()
for c in arxivManager.categories():
	text_data = arxivManager.read(c)
	for i, message in enumerate(text_data):
		print 'Message ', i+1
		#Map all words to their embeddings
		message = [[embeddings.get(word) for word in sentences if word not in stop_words and embeddings.get(word) is not None] for sentences in message]
		#Check for empty sentences (after common and stop word removal)
		message = [sen for sen in message if len(sen) > 0]

		#message = embObj.mapWords(message)
		lip = LIPGreedy(message, embObj.embeddingSize(), lambda_)
		lip.computeBoundary()
		lip.selectKeywords()
		lip.printResults(values_array, keys_array)"""
