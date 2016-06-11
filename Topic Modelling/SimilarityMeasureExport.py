import re
import logging
import FileBrowser
from gensim import corpora, models, similarities
import WikiAPI
import multiprocessing as mp
import xlrd


import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
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

def getText(location, id):
    article_file = pathDoc+"/"+location
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




def returnArticlePaths(pathDoc):

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

def getLocation(query_id):
    for b in binding:
        if int(b[0]) == int(query_id):
            return b[1]


def generateResults(model_type, index, corpus_type, articles, save_location):
    for article in articles:
        query_id = WikiAPI.get_pageid_from_article_title("en",article)
        query_id = str(query_id)
        #print query_id
        title_query = WikiAPI.get_title_from_pageid("en",query_id)
        article_paths = returnArticlePaths(pathDoc)
        spreadsheet_location = save_location+"/"+query_id+'-'+str(title_query)+".xls"
        if not FileBrowser.file_exists(spreadsheet_location):
            print str(article) + " - generating sim docs"
            location = getLocation(query_id)
            if location == None:
                print("\tArticle " + str(title_query) + " not found")
                continue
            article_text, index_query = getText(location, query_id)

            text_query = dictionary.doc2bow(article_text.lower().split())
            if corpus_type == "tfidf":
                text_query = tfidf[text_query]


            model_query = model_type[text_query]


            sims = index[model_query] # perform a similarity query against the corpus
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            #print(sims)

            import xlwt

            #print "title\tid\turl\tsimilarity"
            #print "\n\n"
            #print "Similarity to query "+index_query+"\n"
            #print article_text
            excel_workbook = xlwt.Workbook(encoding='utf8')
            excel_sheet = excel_workbook.add_sheet("test")
            #excel.
            #excel.add_sheet("test")
            #limit = 101
            limit = 1000
            pos_diff = 0
            i = 0

            while i != limit:
                id_article = binding[sims[i][0]][0]
                #if id_article == query_id:
                #    limit+=1
                #    pos_diff+=1
                #else:
                similarity_rate = sims[i][1]
                #solr_query = s.query('id:"'+id_article+'"')

                title = WikiAPI.get_title_from_pageid("en",id_article)
                #title = str(solr_query.results[0]['title'][0])
                #location = str(solr_query.results[0]['location'][0])
                url = WikiAPI.get_fullurl_from_pageid("en",id_article)
                #print "{0} -> {1} -> {2}".format(sims[i], id_article, title)
                #print "{0}\t{1}\t{2}\t{3}".format(title, id_article, url, similarity_rate)
                #print WikiAPI.get_summary_from_pageid("en",id_article)+'\n\n'
                #text = getText(location,id_article)[0]

                excel_sheet.write(i-pos_diff, 0, title)
                excel_sheet.write(i-pos_diff, 1, id_article)
                excel_sheet.write(i-pos_diff, 2, url)
                excel_sheet.write(i-pos_diff, 3, float(similarity_rate))
                i+=1
            excel_workbook.save(save_location+"/"+query_id+'-'+str(title_query)+".xls")
        else:
            print str(article) + " exists"




def generateFromEachTopicModel(model):
    model_type = re.match(".*\.(.*)",model).group(1)
    corpus_type = re.match(".*model-(tfidf|bow)",model).group(1)
    file_name = re.match(".*\/(.*)",model).group(1)
    pathCurrentIndex = pathIndex+"/"+file_name+".index"
    index = similarities.Similarity.load(pathCurrentIndex)
    save_location = pathFolder+"/spreadsheets-simple/"+file_name
    FileBrowser.create_folder_if_not_exists(save_location)
    print file_name
    if model_type == "lsi":
        lsi = models.LsiModel.load(model)
        generateResults(lsi,index,corpus_type,articles,save_location)
    elif model_type == "lda":
        lda = models.LdaModel.load(model)
        generateResults(lda,index,corpus_type,articles,save_location)
    elif model_type == "rp":
        rp = models.RpModel.load(model)
        generateResults(rp,index,corpus_type,articles,save_location)
    elif model_type == "hdp":
        hdp = models.HdpModel.load(model)
        generateResults(hdp,index,corpus_type,articles,save_location)

def get_pre_sheets(workbooks_paths):
    pre_sheets = []
    for path in workbooks_paths:
        pre_workbook = xlrd.open_workbook(path)
        pre_sheet = pre_workbook.sheet_by_index(0)
        pre_sheets.append(pre_sheet)
    return pre_sheets

def groupArticlesFromSpreadsheets(articles, spreadsheets):

    for sheet in spreadsheets:
        start_col = 0
        title = sheet.cell(0,start_col).value
        while re.match("(.*(Timestamp|Name|Age|Degree|Profession).*)",title):
            start_col += 1
            title = sheet.cell(0, start_col).value
        for i in range(start_col,sheet.ncols):
            title = sheet.cell(0, i).value
            if re.match("^(.*)\s-\shttps://",title):
                title = re.match("^(.*)\s-\shttps://",title).group(1)
                for j in range(1, sheet.nrows):
                    if sheet.cell(j,i).value == "Yes":
                        articles.append(title)
                        continue


    return sorted(set(articles))











if sys.argv.__len__() == 3:
     pathFolder =        sys.argv[1]
     pathDictionary =    sys.argv[1] +"/dictionary.dict"
     pathCorpus =        sys.argv[1] +"/corpus.mm"
     pathModel =         sys.argv[1] +"/models"
     pathIndex =         sys.argv[1] +"/index"
     pathTFIDF =         sys.argv[1] +"/models/model.tfidf"
     pathBinding =       sys.argv[1] +"/corpus-docs.binding"
     pathDoc =             sys.argv[2]
else:
     print "pathFolder pathDoc"
     quit()



import pickle
binding = pickle.load(open(pathBinding,'r'))

corpus = corpora.MmCorpus(pathCorpus)
dictionary = corpora.Dictionary.load(pathDictionary)
tfidf = models.TfidfModel.load(pathTFIDF)

corpus_tfidf = tfidf[corpus]


articles = [
    "Dissolved organic carbon",
    "Algal bloom",
    "Biological pump",
    "Ocean fertilization",
    "Trophic state index",
    "Phytoplankton",
    "Zooplankton",
    "Plankton",
    "Cyanobacteria",
    "Limiting factor",
    "Iron fertilization",
    "Carbon cycle",
    "Carbon sink",
    "Oceanography",
    "Ocean chemistry",
    "Global warming",
    "Ocean acidification",
    "Oxygen minimum zone",
    "Marine ecosystem",
    "Aquatic ecosystem",
    "Biomass (ecology)",
    "Blue carbon"
]

topic_models = []
topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"model-tfidf-500.lsi"))

#topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"lda"))
#topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"lsi"))
#topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"rp"))
#topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"hdp"))

#for model in topic_models:
#    generateFromEachTopicModel(model)


result_location = pathFolder + "/relevant-docs"
save_location = pathFolder + "/relevant-docs-extended"
spreadsheets_paths = [str(result_location+"/relevant-docs-test (Responses).xlsx"),str(result_location+"/relevant-docs-normalized (Responses).xlsx")]
articles = groupArticlesFromSpreadsheets(articles, get_pre_sheets(spreadsheets_paths))

generateFromEachTopicModel(topic_models[0])


'