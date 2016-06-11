import os
import sys
import re
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

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
            if startLinePattern.match(line):
                if re.search(documentIdPattern, line).group(1) == id:
                    return re.search(documentTitlePattern, line).group(1)
                else:
                    line = f.readline()

            else:
                line = f.readline()
        f.close()

def getText(pathDoc,location, id):
    id = str(id)
    article_file = pathDoc+"/"+location
    f = open(article_file)
    line = f.readline()
    while line:
        if startLinePattern.match(line):
            document_id = re.search(documentIdPattern, line).group(1)
            if document_id == id:
                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()
                    # print text
                return text
            else:
                line = f.readline()

        else:
            line = f.readline()
    f.close()




def returnArticlePaths(pathDoc):
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