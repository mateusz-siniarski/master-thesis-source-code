import nltk
import re
import logging
import FileBrowser
import sys


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def GenerateWikiCorpus(list, dictionary):
    for text in ParseWikiText(list):
        yield dictionary.doc2bow(text.lower().split())

listIDs = []
def ParseWikiText(list):
    for article_file in list:
        print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile('<doc.*>')
            endlinePattern = re.compile('</doc>')
            documentIdPattern = re.compile('<doc id="([^"]*)".*');
            if startLinePattern.match(line):
                elementid = re.search(documentIdPattern, line).group(1)
                location = article_file.split("/")[-2]+"/"+article_file.split("/")[-1]
                array = [elementid, location]
                listIDs.append(array)
                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()
                # print text
                yield text
            else:
                line = f.readline()
        f.close()

def getIDs():
    return listIDs

def generate(path_location, path_doc):

    pathDictionary = path_location + "/dictionary.dict"
    pathCorpus = path_location + "/corpus.mm"
    pathDoc = path_doc
    pathBinding = path_location + "/corpus-docs.binding"

    FileBrowser.create_folder_if_not_exists(path_location)

    from gensim import corpora

    # pathDictionary = '/Volumes/My Passport/gensim-wiki/dictionary.dict'
    # pathCorpus = '/Volumes/My Passport/gensim-wiki/corpus.mm'


    from time import time

    tStart = time()

    # Generate a list of files
    listFiles = FileBrowser.returnFilePathsFromDirectory(pathDoc)

    iterText = ParseWikiText(listFiles)
    dictionary = corpora.Dictionary(text.lower().split() for text in iterText)


    # remove stop words and words that appear only once
    stoplist = set(nltk.corpus.stopwords.words("english"))
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
    dictionary.compactify()
    dictionary.save(pathDictionary)

    corpus = GenerateWikiCorpus(listFiles, dictionary)
    corpora.MmCorpus.serialize(pathCorpus, corpus)

    # Save index to file

    import pickle
    pickle.dump(listIDs, open(pathBinding, 'w'));

    # for i in range(0,len(IDs)):
    #    print "{0}\t{1}".format(i,IDs[i])

    tEnd = time()

    print "Running time: %f" % (tEnd - tStart)

#Generates the Wiki corpus to pathFolder. input is the hierarchy structure from WikiExtractor
if sys.argv.__len__() == 2:
    pathFolder = sys.argv[1]
    pathDocs = sys.argv[2]
else:
    print "pathFolder, pathDocs"
    quit()

generate(pathFolder,pathDocs)