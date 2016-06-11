import SimilarityMeasureAPI
import FileBrowser
import SolrAPI
import xlAPI
import sys

if sys.argv.__len__() == 4:
    pathXml = sys.argv[1]
    pathDoc = sys.argv[2]
    pathMRNER = sys.argv[3]
    pathTextDocsFolder = sys.argv[3]+"/docs"
else:
    print "pathXml pathDoc pathMRNER"
    quit()


FileBrowser.create_folder_if_not_exists(pathTextDocsFolder)
s = SolrAPI.SolrAPI('enwiki-20160113_no-text')

sheet = xlAPI.getSpreadsheetFile(pathXml)
col_ID = 1

for i in range(0,sheet.nrows):
    article_id = int(sheet.cell(i,col_ID).value)
    title = s.get_title_from_id(article_id).replace("/","_")
    location = s.get_location_from_id(article_id)
    text = SimilarityMeasureAPI.getText(pathDoc,location,article_id)
    file_name = "/"+str(article_id)+" - "+str(title)+".txt"
    print str(title)
    file = open(str(pathTextDocsFolder+file_name),"w")
    file.write(text)
    file.close()
