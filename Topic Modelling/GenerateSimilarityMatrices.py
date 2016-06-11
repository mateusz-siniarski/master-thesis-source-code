import re
import logging
from time import time
import sys
import os
from gensim import corpora, models, similarities





def returnModelsWithEnding(ending):
    articles = []
    if os.path.isdir(pathModel):
        for (path, dirs, files) in os.walk(pathModel):
            for fil in files:
                if(not str(fil).startswith('.') and str(fil).endswith(ending)):
                    articles.append(str(path)+'/'+str(fil))
        return articles
    else:
        articles.append(pathModel)
        return articles



def genLsiIndex():
    for lsi_model in lsi_models:
        file_name = re.match(".*\/(.*)",lsi_model).group(1)
        print "Started "+file_name
        tStart = time()
        lsi = models.LsiModel.load(lsi_model)
        index = similarities.MatrixSimilarity(lsi[corpus])
        tStop = time()

        print "Running time "+file_name+": %f" % (tStop - tStart)
        pathLsiIndex = pathIndex +"/"+file_name+".index"
        index.save(pathLsiIndex)

def genLdaIndex():
    for lda_model in lda_models:
        file_name = re.match(".*\/(.*)",lda_model).group(1)
        print "Started "+file_name
        tStart = time()
        lda = models.LdaModel.load(lda_model)
        index = similarities.MatrixSimilarity(lda[corpus])
        tStop = time()

        print "Running time "+file_name+": %f" % (tStop - tStart)
        pathLdaIndex = pathIndex +"/"+file_name+".index"
        index.save(pathLdaIndex)

def genHdpIndex():
    for hdp_model in hdp_models:
        file_name = re.match(".*\/(.*)",hdp_model).group(1)
        print "Started "+file_name
        tStart = time()
        hdp = models.HdpModel.load(hdp_model)
        index = similarities.MatrixSimilarity(hdp[corpus])
        tStop = time()

        print "Running time "+file_name+": %f" % (tStop - tStart)
        pathHdpIndex = pathIndex +"/"+file_name+".index"
        index.save(pathHdpIndex)

def genRpIndex():
    for rp_model in rp_models:
        file_name = re.match(".*\/(.*)",rp_model).group(1)
        print "Started "+file_name
        try:
            tStart = time()
            rp = models.RpModel.load(rp_model)
            index = similarities.MatrixSimilarity(rp[corpus])
            tStop = time()

            print "Running time "+file_name+": %f" % (tStop - tStart)
            pathRpIndex = pathIndex +"/"+file_name+".index"
            index.save(pathRpIndex)
        except:
            print "error " +rp_model

def genLsiIndexFile(lsi_model):
    file_name = re.match(".*\/(.*)",lsi_model).group(1)
    print "Started "+file_name
    tStart = time()
    lsi = models.LsiModel.load(lsi_model)
    index = similarities.MatrixSimilarity(lsi[corpus])
    tStop = time()
    print "Running time "+file_name+": %f" % (tStop - tStart)
    pathLsiIndex = pathIndex +"/"+file_name+".index"
    index.save(pathLsiIndex)

def genLdaIndexFile(lda_model):
    file_name = re.match(".*\/(.*)",lda_model).group(1)
    print "Started "+file_name
    tStart = time()
    lda = models.LdaModel.load(lda_model)
    index = similarities.MatrixSimilarity(lda[corpus])
    tStop = time()
    print "Running time "+file_name+": %f" % (tStop - tStart)
    pathLdaIndex = pathIndex +"/"+file_name+".index"
    index.save(pathLdaIndex)

def genHdpIndexFile(hdp_model):
    file_name = re.match(".*\/(.*)",hdp_model).group(1)
    print "Started "+file_name
    tStart = time()
    hdp = models.HdpModel.load(hdp_model)
    index = similarities.MatrixSimilarity(hdp[corpus])
    tStop = time()
    print "Running time "+file_name+": %f" % (tStop - tStart)
    pathHdpIndex = pathIndex +"/"+file_name+".index"
    index.save(pathHdpIndex)

def genRpIndexFile(rp_model):
    file_name = re.match(".*\/(.*)",rp_model).group(1)
    print "Started "+file_name
    try:
        tStart = time()
        rp = models.RpModel.load(rp_model)
        index = similarities.MatrixSimilarity(rp[corpus])
        tStop = time()
        print "Running time "+file_name+": %f" % (tStop - tStart)
        pathRpIndex = pathIndex +"/"+file_name+".index"
        index.save(pathRpIndex)
    except:
        print "error " +rp_model



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if sys.argv.__len__() == 2:
     pathDictionary =    sys.argv[1] +"/dictionary.dict"
     pathCorpus =        sys.argv[1] +"/corpus.mm"
     pathIndex =         sys.argv[1] +"/index"
     pathModel =         sys.argv[1] +"/models"
     pathTemp =            sys.argv[1] +"/tmp"
     pathTFIDF =         sys.argv[1] +"/models/model.tfidf"
     #pathLsi =           sys.argv[1] +"/models/model-tfidf-50.lsi"
     #pathLda =           sys.argv[1] +"/models/model-tfidf-50.lda"
     pathBinding =       sys.argv[1] +"/corpus-docs.binding"
else:
     print "pathFolder"
     quit()


corpus = corpora.MmCorpus(pathCorpus)
dictionary = corpora.Dictionary.load(pathDictionary)
'''

#endings = [".lsi",".lda",".rp",".hdp"]
#endings = [".lsi"]
lsi_models= returnModelsWithEnding(".lsi")
lda_models= returnModelsWithEnding(".lda")
hdp_models= returnModelsWithEnding(".hdp")
rp_models= returnModelsWithEnding(".rp")

genRpIndex()
genLsiIndex()
genLdaIndex()
genHdpIndex()



'''
import multiprocessing as mp

if __name__ == '__main__':
    pool = mp.Pool(processes=8)

    lsi_models= returnModelsWithEnding(".lsi")
    lda_models= returnModelsWithEnding(".lda")
    hdp_models= returnModelsWithEnding(".hdp")
    rp_models= returnModelsWithEnding(".rp")

    for model in lsi_models:
        pool.apply_async(genLsiIndexFile, (model,))

    for model in lda_models:
        pool.apply_async(genLdaIndexFile, (model,))

    for model in hdp_models:
        pool.apply_async(genHdpIndexFile, (model,))

    for model in rp_models:
        pool.apply_async(genRpIndexFile, (model,))

    pool.close()
    pool.join()



