import re
import os
import MarineRegionsAPI
import json
import WikiAPI
import SimilarityMeasureAPI
import SolrAPI
from lxml import etree

import sys

reload(sys)
sys.setdefaultencoding("utf-8")




def tokenize(text):
    # TODO: lousy tokenization
    return [token for token in text.split()]


def getSentence(article_file, wordstart, wordend):
    wordstart = int(wordstart)
    wordend = int(wordend)
    #article_file = pathDoc + "/" + location
    # print(article_file)
    file = open(article_file).read()
    tokens = tokenize(file)
    sentence_tokenized = [];

    # find begining
    sentence_start = wordstart
    sentence_left_limit = 1
    sentence_left = 0
    while sentence_left < sentence_left_limit and sentence_start > 0:
        sentence_start -= 1
        if tokens[sentence_start].endswith('.'):
            sentence_left += 1

    # find end
    sentence_end = wordend - 1
    sentence_right_limit = 1
    sentence_right = 0
    if not tokens[sentence_end].endswith('.'):
        while sentence_right < sentence_right_limit and sentence_end < len(tokens) - 1:
            sentence_end += 1
            #print str(sentence_end) + " " + str(len(tokens))
            if tokens[sentence_end].endswith('.'):
                sentence_right += 1

    sentence = ""
    for i in range(sentence_start + 1, sentence_end + 1):
        if sentence == "":
            sentence = tokens[i]
        elif i == wordstart and (wordend - wordstart) == 1:
            sentence = sentence + " <b>" + tokens[i] + "</b>"
        elif i == wordstart:
            sentence = sentence + " <b>" + tokens[i]
        elif i == (wordend - 1):
            sentence = sentence + " " + tokens[i] + "</b>"
        else:
            sentence = sentence + " " + tokens[i]

    #print sentence
    return sentence


def getNameHierarchy(geo_id):
        hierarchy = ""
        run = True
        while run:
            parent = MarineRegionsAPI.getParentFromLocationId(geo_id)
            if parent.data is None:
                run = False
            else:
                name = parent.get_name()
                print name
                if hierarchy == "":
                    hierarchy = unicode(name)
                else:
                    hierarchy = unicode(name) + '/' + hierarchy

                geo_id = parent.get_parent_id()
        return hierarchy


def genXmlFileVariable(json_data, destination):
    json_data = open(json_data).read()

    data = json.loads(json_data)



    add = etree.Element("add")

    i = 0
    for d in data:

        filename = d['filename']
        subStr = d['subStr']
        label = d['label']
        charOffsetBegin = d['charOffsetBegin']
        charOffsetEnd = d['charOffsetEnd']

        pattern = '^(.*)\s-\s(.*)#'

        article_id = int(re.match(pattern,filename).group(1))
        title = re.match(pattern,filename).group(2)






        try:
            print str(i) + " "+str(article_id) + " " +unicode(title) + " " + str(subStr) + " " + str(label)
        except:
            print "not printable id:" + str(i)


        doc = etree.SubElement(add, "doc")
        doc_id = etree.SubElement(doc, "field", name='id')
        doc_id.text = str(i)
        i += 1

        doc_article_id = etree.SubElement(doc, "field", name='article_id')
        doc_article_id.text = str(article_id)

        doc_title = etree.SubElement(doc, "field", name='title')
        doc_title.text = unicode(title)

        doc_subStr = etree.SubElement(doc, "field", name='subStr')
        doc_subStr.text = unicode(subStr)

        doc_label = etree.SubElement(doc, "field", name='label')
        doc_label.text = str(label)

        doc_charOffsetBegin = etree.SubElement(doc, "field", name='charOffsetBegin')
        doc_charOffsetBegin.text = str(charOffsetBegin)

        doc_charOffsetEnd = etree.SubElement(doc, "field", name='charOffsetEnd')
        doc_charOffsetEnd.text = str(charOffsetEnd)



    et = etree.ElementTree(add)
    with open(destination + '/output-variables.xml', 'w') as output_file:
        output_file.write(etree.tostring(et, pretty_print=True))

if sys.argv.__len__() == 3:
    json_data = sys.argv[1]
    destination = sys.argv[2]
else:
    print "json_data destination"
    quit()



genXmlFileVariable(json_data, destination)








# files = returnArticlePaths()
# genSolrIndex(files)

# response = s.query('title:"Ocean"')
# hit = response.results[0]['title']
