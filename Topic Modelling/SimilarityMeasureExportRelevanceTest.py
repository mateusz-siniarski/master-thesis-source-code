import re
import logging
import FileBrowser
from gensim import corpora, models, similarities
import WikiAPI
import xlrd
import multiprocessing as mp


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



def mergeSims(model_type, index, corpus_type, articles):
    tot_sims = []
    for article in articles:
        query_id = WikiAPI.get_pageid_from_article_title("en", article)
        query_id = str(query_id)
        # print query_id
        title_query = WikiAPI.get_title_from_pageid("en", query_id)
        article_paths = returnArticlePaths(pathDoc)


        location = getLocation(query_id)
        if location == None:
            continue
        article_text, index_query = getText(location, query_id)

        text_query = dictionary.doc2bow(article_text.lower().split())
        if corpus_type == "tfidf":
            text_query = tfidf[text_query]

        model_query = model_type[text_query]

        sims = index[model_query]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tot_sims.extend(sims)
        #sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # print(sims)
    return tot_sims




def mergeFromEachTopicModel(model):
    model_type = re.match(".*\.(.*)", model).group(1)
    try:
        corpus_type = re.match(".*model-(tfidf|bow)", model).group(1)
    except:
        return None
    file_name = re.match(".*\/(.*)", model).group(1)
    pathCurrentIndex = pathIndex + "/" + file_name + ".index"
    index = similarities.Similarity.load(pathCurrentIndex)

    print file_name

    if model_type == "lsi":
        lsi = models.LsiModel.load(model)
        return mergeSims(lsi, index, corpus_type, articles)
    elif model_type == "lda":
        lda = models.LdaModel.load(model)
        return mergeSims(lda, index, corpus_type, articles)
    elif model_type == "rp":
        rp = models.RpModel.load(model)
        return mergeSims(rp, index, corpus_type, articles)
    elif model_type == "hdp":
        hdp = models.HdpModel.load(model)
        return mergeSims(hdp, index, corpus_type, articles)




def gen_spreadsheet(doc_ids,save_location,file_name, limit=200):
    import xlwt


    excel_workbook = xlwt.Workbook(encoding='utf8')
    excel_sheet = excel_workbook.add_sheet("test")

    if len(doc_ids) < limit:
        limit = len(doc_ids)

    for i in range(0, limit):
        doc_id = doc_ids[i]
        id_article = doc_id[0]
        similarity_rate = doc_id[1]

        title = WikiAPI.get_title_from_pageid("en",id_article)
        url = WikiAPI.get_fullurl_from_pageid("en",id_article)

        print "{0}\t{1}\t{2}\t{3}".format(title, id_article, url, similarity_rate)

        excel_sheet.write(i, 0, title)
        excel_sheet.write(i, 1, id_article)
        excel_sheet.write(i, 2, url)
        excel_sheet.write(i, 3, float(similarity_rate))
    excel_workbook.save(save_location+"/"+file_name+".xls")










def groupDocs(tot_sims,t=0):
    seen = {}
    doc_ids = []
    for sim in tot_sims:
        doc_id = binding[sim[0]][0]
        doc_sim = sim[1]

        if doc_id in seen and doc_sim >= t:
            seen[doc_id] += doc_sim
            continue
        if doc_sim >= t:
            seen[doc_id] = doc_sim
            doc_ids.append(doc_id)

    result = []
    for doc_id in doc_ids:
        doc_sim = seen[doc_id]
        result.append([doc_id, doc_sim])
    return sorted(result, key=lambda item: -item[1])

def groupDocsFromSpreadsheets(tot_sims, t=0):
    seen = {}
    doc_ids = []
    for sim in tot_sims:
        #doc_title = sim[0]
        doc_id = sim[1]
        #doc_url = sim[2]
        doc_sim = sim[3]

        if doc_id in seen and doc_sim >= t:
            seen[doc_id] += doc_sim
            continue
        if doc_sim >= t:
            seen[doc_id] = doc_sim
            doc_ids.append(doc_id)

    result = []
    for doc_id in doc_ids:
        doc_sim = seen[doc_id]
        result.append([doc_id, doc_sim])
    return sorted(result, key=lambda item: -item[1])

def groupArticlesFromSpreadsheets(articles, spreadsheets):



    #seen = articles
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





    '''
        #doc_title = sim[0]
        doc_id = sim[1]
        #doc_url = sim[2]
        doc_sim = sim[3]

        if doc_id in seen and doc_sim >= t:
            seen[doc_id] += doc_sim
            continue
        if doc_sim >= t:
            seen[doc_id] = doc_sim
            doc_ids.append(doc_id)

    result = []
    for doc_id in doc_ids:
        doc_sim = seen[doc_id]
        result.append([doc_id, doc_sim])
    return sorted(result, key=lambda item: -item[1])

    '''
    return sorted(set(articles))

def printRangeOfDocs(doc_ids, limit=200):
    for i in range(0,limit):
        doc_id = doc_ids[i]
        title = WikiAPI.get_title_from_pageid("en",doc_id[0])
        if title == None:
            title = "None"
        print title +" - "+ str(doc_id[0]) +" - "+str(doc_id[1])

def get_pre_sheets(workbooks_paths):
    pre_sheets = []
    for path in workbooks_paths:
        pre_workbook = xlrd.open_workbook(path)
        pre_sheet = pre_workbook.sheet_by_index(0)
        pre_sheets.append(pre_sheet)
    return pre_sheets

def get_pre_sheets_and_path(workbooks_paths):
    pre_sheets = []
    for path in workbooks_paths:
        pre_workbook = xlrd.open_workbook(path)
        pre_sheet = pre_workbook.sheet_by_index(0)
        model_name = re.match(".*(model-.*).xls",path).group(1)
        pre_sheets.append([model_name, pre_sheet])
    return pre_sheets

def list_all_from_spreadsheet(workbook_folder, file_name_contains=None):
    merged_spreadsheets = []

    workbooks_paths = []
    if file_name_contains == None:
        workbooks_paths.extend(FileBrowser.returnFilePathsFromDirectory(workbook_folder))
    else:
        for e in file_name_contains:
            workbooks_paths.extend(FileBrowser.returnFilesWithEnding(workbook_folder, str(e + ".xls")))

    pre_sheets = get_pre_sheets(workbooks_paths)

    for pre_sheet in pre_sheets:
        pre_sheet_rows = pre_sheet.nrows
        for r in range(1, pre_sheet_rows):
            pre_row = pre_sheet.row_values(r)
            row = [pre_row[0],int(pre_row[1]),pre_row[2],float(pre_row[3])]
            merged_spreadsheets.append(row)

    return merged_spreadsheets

def find_min_max(pre_sheet):
    score_max = float("-inf")
    score_min = float("inf")
    pre_sheet_rows = pre_sheet.nrows
    for r in range(1, pre_sheet_rows):
        pre_row = pre_sheet.row_values(r)
        test_score = float(pre_row[3])
        if test_score > score_max:
            score_max = test_score
        if test_score < score_min:
            score_min = test_score
    return score_max, score_min

def normalize(x, x_max, x_min):
    return float((x-x_min)/(x_max-x_min))

def list_all_from_spreadsheet_normalized(workbook_folder, file_name_contains=None):
    merged_spreadsheets = []

    workbooks_paths = []
    if file_name_contains == None:
        workbooks_paths.extend(FileBrowser.returnFilePathsFromDirectory(workbook_folder))
    else:
        for e in file_name_contains:
            workbooks_paths.extend(FileBrowser.returnFilesWithEnding(workbook_folder, str(e + ".xls")))

    pre_sheets = get_pre_sheets(workbooks_paths)

    for pre_sheet in pre_sheets:
        score_max, score_min = find_min_max(pre_sheet)
        pre_sheet_rows = pre_sheet.nrows
        for r in range(1, pre_sheet_rows):
            pre_row = pre_sheet.row_values(r)
            row = [pre_row[0],int(pre_row[1]),pre_row[2],normalize(float(pre_row[3]),score_max,score_min)]
            merged_spreadsheets.append(row)

    return merged_spreadsheets

def list_all_from_spreadsheet(workbook_folder, file_name_contains=None):
    merged_spreadsheets = []

    workbooks_paths = []
    if file_name_contains == None:
        workbooks_paths.extend(FileBrowser.returnFilePathsFromDirectory(workbook_folder))
    else:
        for e in file_name_contains:
            workbooks_paths.extend(FileBrowser.returnFilesWithEnding(workbook_folder, str(e + ".xls")))

    pre_sheets = get_pre_sheets(workbooks_paths)

    for pre_sheet in pre_sheets:
        pre_sheet_rows = pre_sheet.nrows
        for r in range(1, pre_sheet_rows):
            pre_row = pre_sheet.row_values(r)
            row = [pre_row[0],int(pre_row[1]),pre_row[2],float(pre_row[3])]
            merged_spreadsheets.append(row)

    return merged_spreadsheets

def generate_similar_document_spreadsheets(topic_models, save_location):
    for model in topic_models:
        print model
        file_name = re.match(".*\/(.*)", model).group(1)
        save_path = save_location + "/" + file_name + ".xls"
        index_path = pathIndex + "/" + file_name + ".index"
        if not FileBrowser.file_exists(save_path) and FileBrowser.file_exists(index_path):
            current_sim = mergeFromEachTopicModel(model)
            if current_sim != None:
                doc_ids = groupDocs(current_sim)
            # printRangeOfDocs(doc_ids)
            gen_spreadsheet(doc_ids, save_location, file_name)
            # tot_sims.extend(current_sim)



def print_sum_of_each_sheet(workbook_folder, file_name_contains=None, normalized = False):


    workbooks_paths = []
    if file_name_contains == None:
        workbooks_paths.extend(FileBrowser.returnFilePathsFromDirectory(workbook_folder))
    else:
        for e in file_name_contains:
            workbooks_paths.extend(FileBrowser.returnFilesWithEnding(workbook_folder, str(e + ".xls")))

    pre_sheets = get_pre_sheets_and_path(workbooks_paths)
    '''
    for path, pre_sheet in pre_sheets:
        pre_sheet_rows = pre_sheet.nrows
        sum = 0
        for r in range(1, pre_sheet_rows):
            pre_row = pre_sheet.row_values(r)
            sum += float(pre_row[3])
        print path + " = "+sum
    '''
    for path, pre_sheet in pre_sheets:
        if normalized:
            score_max, score_min = find_min_max(pre_sheet)
        pre_sheet_rows = pre_sheet.nrows
        sum = 0
        for r in range(1, pre_sheet_rows):
            pre_row = pre_sheet.row_values(r)
            if normalized:
                score = normalize(float(pre_row[3]), score_max, score_min)
            else:
                score = float(pre_row[3])
            sum += score
        print path + "\t" + str(sum)

def gen_grouped_spreadsheet(save_location):
    merged_models = list_all_from_spreadsheet_normalized(save_location,["lda","lsi","rp"])
    grouped_models = groupDocsFromSpreadsheets(merged_models)
    gen_spreadsheet(grouped_models,save_location,"normalized_total")



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


##Generates the spreadsheet
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


tot_sims = []

topic_models = []
topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"lda"))
topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"lsi"))
topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"rp"))
topic_models.extend(FileBrowser.returnFilesWithEnding(pathModel,"hdp"))



result_location = pathFolder + "/relevant-docs"
save_location = pathFolder + "/relevant-docs"
#spreadsheets_paths = [str(result_location+"/relevant-docs-test (Responses).xlsx"),str(result_location+"/relevant-docs-normalized (Responses).xlsx")]
#articles = groupArticlesFromSpreadsheets(articles, get_pre_sheets(spreadsheets_paths))


generate_similar_document_spreadsheets(topic_models, save_location)


#FileBrowser.create_folder_if_not_exists(save_location)


#gen_grouped_spreadsheet(save_location)

#print_sum_of_each_sheet(save_location,["lda","lsi","rp"],normalized=True)




#print "total"
#doc_ids = groupDocs(tot_sims)
#printRangeOfDocs(doc_ids)
#gen_spreadsheet(doc_ids, save_location, "total")


