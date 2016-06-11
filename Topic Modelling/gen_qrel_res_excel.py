import xlwt
import FileBrowser
import sys
import re


if sys.argv.__len__() == 2:
    qrel_models_folder = sys.argv[1]
else:
    print "qrel_models_folder"
    quit()

folders = FileBrowser.returnAllDirs(qrel_models_folder)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Results")
row = 0
sheet.write(row,0,"Model type")
sheet.write(row,1,"Corpus type")
sheet.write(row,2,"Topics")
sheet.write(row,3,"MAP")
sheet.write(row,4,"NDCG")

for folder in folders:
    '''
    if ending hdp
        get bow/tfidf and topics "-"
    else:
        get bow/tfidf and topics

    '''


    print folder

    row += 1
    file_name = re.match(".*\/(.*)", folder).group(1)
    if re.match(".*(hdp)", file_name) and re.match(".*model-(tfidf|bow)\..*", file_name):
        model_type = re.match(".*(hdp)", file_name).group(1)
        sheet.write(row, 0, model_type)
        corpus_type = re.match(".*model-(tfidf|bow)\..*", file_name).group(1)
        sheet.write(row, 1, corpus_type)
        sheet.write(row, 2, "-")

    elif re.match(".*(lda|lsi|rp)", file_name) and re.match(".*model-(tfidf|bow)-(.*)\..*", file_name):
        model_type = re.match(".*(lda|lsi|rp)", file_name).group(1)
        sheet.write(row, 0, model_type)
        corpus_type = re.match(".*model-(tfidf|bow)-(.*)\..*", file_name).group(1)
        sheet.write(row, 1, corpus_type)
        topics = re.match(".*model-(tfidf|bow)-(.*)\..*", file_name).group(2)
        sheet.write(row, 2, int(topics))
    else:
        row-=1
        continue



    output_path = folder + "/output.txt"
    output_file = open(output_path,'r')
    for line in output_file:
        #^(map|ndcg)\s.*all\s*(.*)

        if re.match("^map\s.*all\s*(.*)",line):
            #print line
            map = re.match("^map\s.*all\s*(.*)",line).group(1)
            sheet.write(row, 3, float(map))
        if re.match("^ndcg\s.*all\s*(.*)", line):
            #print line
            ndcg = re.match("^ndcg\s.*all\s*(.*)", line).group(1)
            sheet.write(row, 4, float(ndcg))

save_path = qrel_models_folder +"/results-normalized.xls"
workbook.save(save_path)


