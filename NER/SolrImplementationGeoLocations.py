import re
import os
import MarineRegionsAPI
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


def genXmlFileMR(abs_matches, destination):
    s = SolrAPI.SolrAPI()
    add = etree.Element("add")

    # print(article_file)
    f = open(abs_matches)
    line = f.readline()
    i = 0
    last_article_id = 0
    checked_locations = {}
    while line:
        # assume there's one document per line, tokens separated by whitespace
        # yield dictionary.doc2bow(line.lower().split())

        # doc_path   char_start  char_end    ids     location_name

        values = line.split("\t")
        doc_path = values[0]
        #word_start = values[1]
        #word_end = values[2]
        geo_ids = values[3].split(',')
        geo_id = geo_ids[0]

        mr = MarineRegionsAPI.getDataFromLocationId(geo_id)




        geo_lat = mr.get_latitude()
        geo_lng = mr.get_longitude()
        geo_name = mr.get_name()



        if not str(geo_name).isdigit() and str(geo_lat) != 'None' and str(geo_lng) != 'None':




            if not geo_id in checked_locations:
                try:
                    print str(geo_id) + " " +unicode(geo_name) + " " + str(geo_lat) + " " + str(geo_lng)
                except:
                    print "not printable id:" + str(i)

                #checked_locations.update({geo_id:geo_name})
                checked_locations[geo_id] = geo_name
                doc = etree.SubElement(add, "doc")
                doc_id = etree.SubElement(doc, "field", name='id')
                doc_id.text = str(i)
                i += 1

                doc_geo_id = etree.SubElement(doc, "field", name='geo_id')
                doc_geo_id.text = geo_id

                doc_geo_name = etree.SubElement(doc, "field", name='geo_name')
                doc_geo_name.text = unicode(geo_name)

                doc_geo_lat = etree.SubElement(doc, "field", name='geo_lat')
                doc_geo_lat.text = str(geo_lat)

                doc_geo_lng = etree.SubElement(doc, "field", name='geo_lng')
                doc_geo_lng.text = str(geo_lng)



        line = f.readline()

    f.close()
    et = etree.ElementTree(add)
    with open(destination + '/output-geo-locs.xml', 'w') as output_file:
        output_file.write(etree.tostring(et, pretty_print=True))

if sys.argv.__len__() == 4:
    abs_matches = sys.argv[1]
    destination = sys.argv[2]
    docs_parent = sys.argv[3]
else:
    print "abs_matches destination docs_parent/ "
    quit()



genXmlFileMR(abs_matches, destination)








# files = returnArticlePaths()
# genSolrIndex(files)

# response = s.query('title:"Ocean"')
# hit = response.results[0]['title']
