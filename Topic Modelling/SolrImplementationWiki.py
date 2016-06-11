import solr
import re
import os
import WikiAPI
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def genXmlFileWiki(__list,pathFolder):
    counter = 0
    add = etree.Element("add")
    for article_file in __list:
        # print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile('<doc.*>')
            endlinePattern = re.compile('</doc>')
            documentIdPattern = re.compile('<doc id="([^"]*)".*');
            documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
            #documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')
            if startLinePattern.match(line):
                # self.listIDs.append(re.search(documentIdPattern, line).group(1))
                title = re.search(documentTitlePattern, line).group(1)
                id = re.search(documentIdPattern, line).group(1)
                url = WikiAPI.get_fullurl_from_pageid("en",id)
                line = f.readline()

                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()

                location = article_file.split("/")[-2] + "/" + article_file.split("/")[-1]

                doc = etree.SubElement(add,"doc")
                '''
                etree.SubElement(doc,"field", title=unicode(title, "utf-8"))
                etree.SubElement(doc, "field", article_id=id)
                etree.SubElement(doc, "field", corpus_id=str(reverse_binding[id]))
                etree.SubElement(doc, "field", url=url)
                etree.SubElement(doc, "field", location=location)
                etree.SubElement(doc, "field", text=unicode(text, "utf-8"))
                '''

                doc_id = etree.SubElement(doc, "field", name='id')
                doc_id.text = str(counter)
                counter+=1

                doc_title = etree.SubElement(doc,"field", name='title')
                doc_title.text = unicode(title, "utf-8")
                print str(title)
                doc_article_id = etree.SubElement(doc, "field", name='article_id')
                doc_article_id.text = str(id)
                #print str(id)
                doc_corpus_id = etree.SubElement(doc, "field", name='corpus_id')
                doc_corpus_id.text = str(reverse_binding[id])
                #print str(reverse_binding[id])
                doc_url = etree.SubElement(doc, "field", name='url')
                doc_url.text = url
                #print url
                doc_location = etree.SubElement(doc, "field", name='location')
                doc_location.text = location
                #print location
                #doc_text = etree.SubElement(doc, "field", name='text')
                #doc_text.text = unicode(text, "utf-8")
                #print ""

            else:
                line = f.readline()
        # s.commit()
        f.close()
    et = etree.ElementTree(add)
    with open(pathFolder+'/output-fix-id.xml', 'w') as output_file:
        output_file.write(etree.tostring(et, pretty_print=True))

def genXmlFileMR(__list,pathFolder):
    counter = 0
    add = etree.Element("add")
    for article_file in __list:
        # print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile('<doc.*>')
            endlinePattern = re.compile('</doc>')
            documentIdPattern = re.compile('<doc id="([^"]*)".*');
            documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
            #documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')
            if startLinePattern.match(line):
                # self.listIDs.append(re.search(documentIdPattern, line).group(1))
                title = re.search(documentTitlePattern, line).group(1)
                id = re.search(documentIdPattern, line).group(1)
                url = WikiAPI.get_fullurl_from_pageid("en",id)
                line = f.readline()

                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()

                location = article_file.split("/")[-2] + "/" + article_file.split("/")[-1]

                doc = etree.SubElement(add,"doc")
                '''
                etree.SubElement(doc,"field", title=unicode(title, "utf-8"))
                etree.SubElement(doc, "field", article_id=id)
                etree.SubElement(doc, "field", corpus_id=str(reverse_binding[id]))
                etree.SubElement(doc, "field", url=url)
                etree.SubElement(doc, "field", location=location)
                etree.SubElement(doc, "field", text=unicode(text, "utf-8"))
                '''
                doc_title = etree.SubElement(doc,"field", name='title')
                doc_title.text = unicode(title, "utf-8")
                print str(title)
                doc_id = etree.SubElement(doc, "field", name='id')
                doc_id.text = str(id)
                #print str(id)
                doc_corpus_id = etree.SubElement(doc, "field", name='corpus_id')
                doc_corpus_id.text = str(reverse_binding[id])
                #print str(reverse_binding[id])
                doc_url = etree.SubElement(doc, "field", name='url')
                doc_url.text = url
                #print url
                doc_location = etree.SubElement(doc, "field", name='location')
                doc_location.text = location
                #print location
                #doc_text = etree.SubElement(doc, "field", name='text')
                #doc_text.text = unicode(text, "utf-8")
                #print ""

            else:
                line = f.readline()
        # s.commit()
        f.close()
    et = etree.ElementTree(add)
    with open(pathFolder+'/output-no-text-correct-url.xml', 'w') as output_file:
        output_file.write(etree.tostring(et, pretty_print=True))


def genSolrIndex(__list):
    counter = 0
    for article_file in __list:
        #print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile('<doc.*>')
            endlinePattern = re.compile('</doc>')
            documentIdPattern = re.compile('<doc id="([^"]*)".*');
            documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
            documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')
            if startLinePattern.match(line):
                #self.listIDs.append(re.search(documentIdPattern, line).group(1))
                title = re.search(documentTitlePattern, line).group(1)
                id = re.search(documentIdPattern,line).group(1)
                url = re.search(documentUrlPattern,line).group(1)
                line = f.readline()


                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()

                location = article_file.split("/")[-2]+"/"+article_file.split("/")[-1]

                doc = dict(
                    id=id,
                    title=title,
                    url=url,
                    location=location
                )


                counter+=1

                try:
                    s.add(doc).commit()
                except:
                    print "error "+str(counter)+" "+title

                '''s.add(doc)'''
                #counter+=1
                print "Added "+str(counter)+" "+title

            else:
                line = f.readline()
        #s.commit()
        f.close()

def returnArticlePaths():
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



if sys.argv.__len__() == 3:
    pathFolder = sys.argv[1]
    pathBinding = sys.argv[1] + "/corpus-docs.binding"
    pathDoc = sys.argv[2]
else:
    print "pathFolder pathDoc"
    quit()


import pickle
print "Loading binding"
binding = pickle.load(open(pathBinding,'r'))
print "Creating reverse_binding"
reverse_binding = {}
for i in range(0,len(binding)):
    reverse_binding.update({binding[i][0]:i})


files = returnArticlePaths()
genXmlFileWiki(files, pathFolder)

#s = solr.SolrConnection('http://localhost:8983/solr/simplewiki')






#files = returnArticlePaths()
#genSolrIndex(files)

#response = s.query('title:"Ocean"')
#hit = response.results[0]['title']
