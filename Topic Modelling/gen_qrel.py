import WikiAPI
import xlAPI
import re
import FileBrowser
import sys
import os

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def getBinaryRelevance(rel):
    if rel == "Yes":
        return 1
    else:
        return 0
def getTernaryRelevance(rel):
    if rel == "Yes":
        return 2
    elif rel == "Maybe":
        return 1
    else:
        return 0

def getRelevantDocs(rel_docs_ss_path):
    relevant_docs_list = []

    sheet = xlAPI.getSpreadsheetFile(rel_docs_ss_path)
    start_col = 0
    title = sheet.cell(0, start_col).value
    while re.match("(.*(Timestamp|Name|Age|Degree|Profession).*)", title):
        start_col += 1
        title = sheet.cell(0, start_col).value
    for i in range(start_col, sheet.ncols):
        title = sheet.cell(0, i).value
        if re.match("^(.*)\s-\shttps://", title):
            title = re.match("^(.*)\s-\shttps://", title).group(1)
            id = WikiAPI.get_pageid_from_article_title("en", title)

            scores = [ ['Yes', 0], ['Maybe', 0], ['No', 0]]
            for j in range(1, sheet.nrows):
                for s in scores:
                    if sheet.cell(j, i).value == s[0]:
                        s[1] += 1
            #relevance = getTernaryRelevance(max(scores, key=lambda x: x[1])[0])
            relevance = int(round(float(3*scores[0][1]+2*scores[1][1]+scores[2][1])/(scores[0][1]+scores[1][1]+scores[2][1])-1))
            array = [id, relevance]
            relevant_docs_list.append(array)



            #print title+"\t"+str(relevance)
            '''
            print scores[0]
            print scores[1]
            print scores[2]
            print "Max: "+str(max(scores, key=lambda x: x[1])[0])
            avg = float(3*scores[0][1]+2*scores[1][1]+scores[2][1])/(scores[0][1]+scores[1][1]+scores[2][1])-1
            print "Score: "+str(avg)
            print "Rounded: "+str(int(round(avg)))
            print ""
            '''
    return relevant_docs_list


'''
    relevant_docs_list = []

    sheet = xlAPI.getSpreadsheetFile(rel_docs_ss_path)

    row_title = 0
    row_rel = 2

    for col in range(1, sheet.ncols):
        full_title = sheet.cell(row_title, col).value
        relevance = getTernaryRelevance(sheet.cell(row_rel, col).value)
        try:
            title = re.match("(.*)\s-", full_title).group(1)
            id = WikiAPI.get_pageid_from_article_title("en", title)

            array = [id, relevance]
            relevant_docs_list.append(array)
        except:
            continue
    return relevant_docs_list

'''



def getSimModels(sim_model_folder_path):
    return FileBrowser.returnFilePathsFromDirectory(sim_model_folder_path)


def getSimModelRes(sim_model_path):
    sim_docs_list = []

    sheet = xlAPI.getSpreadsheetFile(sim_model_path)

    col_title = 0
    col_id = 1
    col_sim = 3

    for row in range(1, sheet.nrows):
        title = sheet.cell(row, col_title).value
        id = sheet.cell(row, col_id).value
        sim = sheet.cell(row, col_sim).value

        array = [id, title, sim]
        sim_docs_list.append(array)
    return sim_docs_list


def checkIfRelevant(similar_doc_id, rel_docs):
    for doc in rel_docs:
        if int(similar_doc_id) == int(doc[0]):
            print "found rel"
            return doc[1]
    return 0


def gen_qrel(sim_model_folder_path, rel_docs, qrel_file_path, result_file_path):

    sim_models_paths = getSimModels(sim_model_folder_path)

    qrel_file = open(qrel_file_path,"w")
    result_file = open(result_file_path,"w")
    for sim_model_path in sim_models_paths:
        article_id = re.match(".*/(.*)-.*.xls",sim_model_path).group(1)
        sim_model_res = getSimModelRes(sim_model_path)

        for res in sim_model_res:
            similar_doc_id = res[0]
            rel = checkIfRelevant(similar_doc_id,rel_docs)
            sim = res[2]
            if rel != -1:
                qrel_file.write(str(article_id)+" "+str(0)+" "+str(similar_doc_id)+" "+str(rel)+"\n")
                result_file.write(str(article_id)+" "+str(0)+" "+str(similar_doc_id)+" "+str(0)+" "+str(sim)+" "+str(0)+"\n")
                print str(article_id)+" "+str(similar_doc_id)+" "+str(sim)+" "+str(rel)
                #print WikiAPI.get_title_from_pageid("en",article_id)+" "+WikiAPI.get_title_from_pageid("en",similar_doc_id)+" "+str(rel)+" "+str(sim)
    qrel_file.close()
    result_file.close()


if sys.argv.__len__() == 5:
    rel_docs_ss_path = sys.argv[1]
    sim_models_folders_path = sys.argv[2]
    qrel_dest_folder_path = sys.argv[3]
    trec_eval_loc = sys.argv[4]
else:
    print "rel_docs_ss_path sim_models_folders_path qrel_folder_path trec_eval_loc"
    quit()

rel_docs = getRelevantDocs(rel_docs_ss_path)

for sim_model_folder_path in FileBrowser.returnAllDirs(sim_models_folders_path):
    print sim_model_folder_path

    file_name = re.match(".*\/(.*)",sim_model_folder_path).group(1)
    qrel_folder_path = qrel_dest_folder_path + "/" + file_name
    FileBrowser.create_folder_if_not_exists(qrel_folder_path)
    qrel_file_path = qrel_folder_path +"/qrel.txt"
    result_file_path = qrel_folder_path +"/qrel-res.txt"
    output_file_path = qrel_folder_path +"/output.txt"
    gen_qrel(sim_model_folder_path, rel_docs, qrel_file_path, result_file_path)
    system_command = trec_eval_loc +" -q -m all_trec "+ qrel_file_path+" "+result_file_path +" > " +output_file_path
    print system_command
    os.system(system_command)


#"/Users/Mateusz/Desktop/spreadsheets-en-improved/ternary/qrel.txt"
#"/Users/Mateusz/Desktop/spreadsheets-en-improved/ternary/qrel-res.txt"