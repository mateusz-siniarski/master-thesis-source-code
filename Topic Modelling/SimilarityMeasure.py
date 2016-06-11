import re
import logging
import nltk
import sys
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import sys

startLinePattern = re.compile('<doc.*>')
endlinePattern = re.compile('</doc>')
documentIdPattern = re.compile('<doc id="([^"]*)".*');
documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')





def getTitle(__list, id):

    for article_file in __list:
        #print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            if startLinePattern.match(line):
                if re.search(documentIdPattern, line).group(1) == id:
                    return re.search(documentTitlePattern, line).group(1)
                else:
                    line = f.readline()

            else:
                line = f.readline()
        f.close()

def getText(__list, id):

    for article_file in __list:
        #print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            if startLinePattern.match(line):
                document_id = re.search(documentIdPattern, line).group(1)
                if document_id == id:
                    text = ""
                    line = f.readline()
                    while line and not endlinePattern.match(line):
                        text += line
                        line = f.readline()
                        # print text
                    return text, document_id
                else:
                    line = f.readline()

            else:
                line = f.readline()
        f.close()




def returnArticlePaths():
    # pathDoc = "/Volumes/My Passport/wiki_ensimple-20160111/"
    articles = []
    if os.path.isdir(pathDoc):
        for (path, dirs, files) in os.walk(pathDoc):
            for fil in files:
                if(not str(fil).startswith('.')):
                    articles.append(str(path)+'/'+str(fil))
        return sorted(articles)
    else:
        articles.append(pathDoc)
        return articles

if sys.argv.__len__() == 4:
     pathDictionary =    sys.argv[1] +"/dictionary.dict"
     pathCorpus =        sys.argv[1] +"/corpus.mm"
     pathIndex =         sys.argv[1] +"/index/model-bow.hdp.index"
     pathTFIDF =         sys.argv[1] +"/models/model.tfidf"
     pathLsi =           sys.argv[1] +"/models/model-bow-500.lsi"
     pathLda =           sys.argv[1] +"/models/model-bow-200.lda"
     pathRp =            sys.argv[1] +"/models/model-bow-20.rp"
     pathHdp =           sys.argv[1] +"/models/model-bow.hdp"
     pathBinding =       sys.argv[1] +"/corpus-docs.binding"
     query =             sys.argv[3]
     pathDoc =           sys.argv[2]
else:
     print "pathFolder pathDoc query"
     quit()
############################################################################################



#pathTFIDF = '/media/mateusz/My Passport/gensim-small-sample/models/model.tfidf'
#
#pathDictionary = '/media/mateusz/My Passport/gensim-small-sample/dictionary.dict'
#pathCorpus = '/media/mateusz/My Passport/gensim-small-sample/corpus.mm'
#pathIndex = '/media/mateusz/My Passport/gensim-small-sample/index.index'
#
#pathLsi = '/media/mateusz/My Passport/gensim-small-sample/models/model.lsi'
#pathLda = '/media/mateusz/My Passport/gensim-small-sample/models/model.lda'
#
#pathBinding = '/media/mateusz/My Passport/gensim-small-sample/corpus-docs.binding'

######################################################################################
#pathTFIDF = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.tfidf'
#pathTFIDF = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.tfidf'

#pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/dictionary.dict'
#pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/corpus.mm'
#pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/index.index'




#pathLsi = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.lsi'
#pathLda = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.lda'
########################################################################################
# pathLsi = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi'
# pathLsi2 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model2.lsi'
# pathLsi3 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model3.lsi'
# pathLsi100 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100.lsi'
#
# pathLsi10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lsi'
# pathLsi50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lsi'
# pathLsi100_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100_tf.lsi'
# pathLsi300_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model300_tf.lsi'
#
# pathLda10 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10.lda'
# pathLda10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lda'
# pathLda50 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50.lda'
# pathLda50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lda'
#
# pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
# pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'
# pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple/index.index'
################################################################################
#query = "Australia"


createIndex = False
import pickle
binding = pickle.load(open(pathBinding,'r'))
files = returnArticlePaths()

corpus = corpora.MmCorpus(pathCorpus)
dictionary = corpora.Dictionary.load(pathDictionary)
tfidf = models.TfidfModel.load(pathTFIDF)

#lsi = models.LsiModel.load(pathLsi)

corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel.load(pathLsi)
lda = models.LdaModel.load(pathLda)
rp  = models.RpModel.load(pathRp)
hdp = models.HdpModel.load(pathHdp)

import random

#Other with interesting results
#27 - Australia
#383240 - Boeing 737 Classic
#262895 - David Bruce (ice hockey) - results hockey and football players

#Ocean related
#103595 - Ocean
#33466 - Plankton
#9067 - Shark
#285 - Fish
#30975 - Porpoise - mammals living in the ocean
#Salmon (20095)
#Teleost (230189) - the dominant fish of present day.

#query, index_query = getText(files,random.choice(binding))
query, index_query = getText(files,"312485")
query_bow = dictionary.doc2bow(query.lower().split())
query_tfidf = tfidf[query_bow]

query_lsi = lsi[query_bow]
query_lda = lda[query_bow]
query_rp = rp[query_bow]
query_hdp = hdp[query_bow]

index = similarities.Similarity.load(pathIndex)
print ' '

sims = index[query_hdp] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
#print(sims)



print "Similarity to query "+index_query+"\n"+query
for i in range(0,len(sims)):
    #i index of corpus
    id_article = binding[sims[i][0]][0]
    similarity_rate = sims[i][1]
    title = getTitle(files,id_article)
    #print "{0} -> {1} -> {2}".format(sims[i], id_article, title)
    print "{0} ({1}) - {2}".format(title,id_article,similarity_rate)

#for i in range(0,len(binding)):
#    print "{0}\t{1}".format(i,binding[i])



#topics =lsi.show_topics(num_topics=-1, num_words=-1, log=False, formatted=True)
#topics_lsi = lsi.print_topics(-1)
print ' '
#topics_lda = lda.print_topics(-1)
