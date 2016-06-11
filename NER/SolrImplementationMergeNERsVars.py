import re
import os
import MarineRegionsAPI
import WikiAPI
import SimilarityMeasureAPI
import solr
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
    # article_file = pathDoc + "/" + location
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
            # print str(sentence_end) + " " + str(len(tokens))
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

    # print sentence
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
            #print name
            if hierarchy == "":
                hierarchy = unicode(name)
            else:
                hierarchy = unicode(name) + '/' + hierarchy

            geo_id = parent.get_parent_id()
    return hierarchy


def genXmlFileMR(all_entities, destination):
    
    add = etree.Element("add")
    #path to Solr index with variable-changes
    s = solr.SolrConnection('http://ocean.idi.ntnu.no:8984/solr/variable-changes')


    i = 0
    last_article_id = 0
    for entity in all_entities:
     





        line = entity[2]
        type = entity[1]

        values = line.split("\t")

        doc_path = values[0]


        article_id = re.match('.*/(.*)\s-\s(.*).txt', doc_path).group(1)
        article_title = re.match('.*/(.*)\s-\s(.*).txt', doc_path).group(2)



        if type == 'mrner':

            geo_ids = values[3].split(',')
            geo_id = geo_ids[0]
            mr = MarineRegionsAPI.getDataFromLocationId(geo_id)
            geo_placetype = mr.get_placeType()
            geo_name = mr.get_name()
            try:
                print str(i) + " " +str(article_id)+" "+unicode(article_title) + " " + unicode(geo_placetype) + " " + unicode(geo_name)
            except:
                print "not printable id:" + str(i)

        if type == 'wormsner':
            species_ids = values[3].split(',')
            species_id = species_ids[0]
            species_ranks = values[4].split(',')
            species_rank = species_ranks[0]
            species_name = values[5].strip()
            try:
                print str(i) + " " +str(article_id)+" "+unicode(article_title) + " " + unicode(species_rank)+ " " + unicode(species_name)
            except:
                print "not printable id:" + str(i)



        i += 1
        if not last_article_id == article_id:
            article_url = WikiAPI.get_fullurl_from_pageid("en", article_id)

            location_text = reverse_binding[article_id]
            text = SimilarityMeasureAPI.getText(path_wikipedia, location_text, article_id)





            last_article_id = article_id
            doc = etree.SubElement(add, "doc")
            doc_id = etree.SubElement(doc, "field", name='id')
            doc_id.text = str(i)



            doc_article_id = etree.SubElement(doc, "field", name='article_id')
            doc_article_id.text = str(article_id)




            doc_article_title = etree.SubElement(doc, "field", name='article_title')
            doc_article_title.text = unicode(article_title)

            doc_article_url = etree.SubElement(doc, "field", name='article_url')
            doc_article_url.text = str(article_url)

            # doc_word_start = etree.SubElement(doc, "field", name='word_start')
            # doc_word_start.text = str(word_start)

            # doc_word_end = etree.SubElement(doc, "field", name='word_end')
            # doc_word_end.text = str(word_end)

            doc_text = etree.SubElement(doc, "field", name='text')
            doc_text.text = unicode(text)

            # doc_article_snippet = etree.SubElement(doc, "field", name='article_snippet')
            # doc_article_snippet.text = unicode(article_snippet)

            response = s.query('article_id:"' + article_id + '"')
            for data in response.results:
                doc_variable_text = etree.SubElement(doc, "field", name='variable_text')
                doc_variable_text.text = unicode(data['subStr'])

                doc_variable_label = etree.SubElement(doc, "field", name='variable_label')
                doc_variable_label.text = unicode(data['label'])

                doc_variable_hierarchy = etree.SubElement(doc, "field", name='variable_hierarchy')
                doc_variable_hierarchy.text = unicode(data['label']+'/'+data['subStr'])


        if type == 'mrner':
            doc_geo_id = etree.SubElement(doc, "field", name='geo_id')
            doc_geo_id.text = geo_id

            doc_geo_name = etree.SubElement(doc, "field", name='geo_name')
            doc_geo_name.text = unicode(geo_name)

            doc_geo_placetype = etree.SubElement(doc, "field", name='geo_placetype')
            doc_geo_placetype.text = geo_placetype

        if type == 'wormsner':
            doc_species_id = etree.SubElement(doc, "field", name='species_id')
            doc_species_id.text = species_id

            doc_species_name = etree.SubElement(doc, "field", name='species_name')
            doc_species_name.text = species_name

            doc_species_rank = etree.SubElement(doc, "field", name='species_rank')
            doc_species_rank.text = species_rank

    et = etree.ElementTree(add)
    with open(destination + '/output-merged-ners-vars-hierarchy.xml', 'w') as output_file:
        output_file.write(etree.tostring(et, pretty_print=True))

        


def listAllPageIDs(all_entities, matches):
    for match in matches:
        f = open(match)
        line = f.readline()
        i = 0
        while line:
            values = line.split("\t")
            doc_path = values[0]
            article_id = re.match('.*/(.*)\s-\s(.*).txt', doc_path).group(1)
            if len(values) == 5:
                type_ner = 'mrner'
            elif len(values) == 6:
                type_ner = 'wormsner'

            array = [int(article_id), type_ner, line]

            all_entities.append(array)
            line = f.readline()
    return sorted(all_entities, key=lambda x: x[0])


# SolrImplementationMR.py.. / mrner - master / data - yes / abs_matches.txt.. / mrner - master / data - yes.. / mrner - master / data - yes /../ gensim - enwiki - 20160113 / corpus - docs.binding.. / enwiki - 20160113
if sys.argv.__len__() == 6:
    mrner_matches = sys.argv[1]
    wormsner_matches = sys.argv[2]
    destination = sys.argv[3]
    pathBinding = sys.argv[4]
    path_wikipedia = sys.argv[5]
else:
    print "mrner_matches wormsner_matches destination binding path_wikipedia"
    quit()

import pickle

print "Loading binding"
binding = pickle.load(open(pathBinding, 'r'))
print "Creating reverse_binding"
reverse_binding = {}
for i in range(0, len(binding)):
    reverse_binding.update({binding[i][0]: binding[i][1]})

all_entities = []

all_entities = listAllPageIDs(all_entities, [mrner_matches, wormsner_matches])
print len(all_entities)
genXmlFileMR(all_entities, destination)








# files = returnArticlePaths()
# genSolrIndex(files)

# response = s.query('title:"Ocean"')
# hit = response.results[0]['title']
