import sys
import re

def listAllPageIDs(match):
    all_entities = {}
    f = open(match)
    line = f.readline()
    entities = 0
    docs = 0
    last_id = 0
    while line:
        values = line.split("\t")
        doc_path = values[0]
        article_id = re.match('.*/(.*)\s-\s(.*).txt', doc_path).group(1)
        if not last_id == article_id:
            docs = docs + 1
            last_id == article_id
        entities = entities +1

    avg = entities/docs
    print avg


if sys.argv.__len__() == 2:
    match = sys.argv[1]
else:
    print "ner"
    quit()


listAllPageIDs(match)