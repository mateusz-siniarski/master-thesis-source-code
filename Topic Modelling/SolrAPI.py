import solr

class SolrAPI:

    def __init__(self,core="enwiki-20160113_no-text",server="localhost",port=8984):
        url = 'http://'+server+':'+str(port)+'/solr/'+core
        self.s = solr.SolrConnection(url)

    def query(self,query,field='*'):
        return self.s.query(field+':'+query)

    def get_id_from_title(self,title):
        response = self.query('"'+title+'"','title')
        return response.results[0]['id']

    def get_id_from_corpus_id(self,corpus_id):
        response = self.query('"' + str(corpus_id) + '"', 'corpus_id')
        return response.results[0]['corpus_id'][0]

    def get_title_from_id(self,id):
        response = self.query('"' + str(id) + '"', 'id')
        return response.results[0]['title'][0]

    def get_url_from_id(self,id):
        response = self.query('"' + str(id) + '"', 'id')
        return response.results[0]['url'][0]
    def get_location_from_id(self,id):
        response = self.query('"' + str(id) + '"', 'id')
        return response.results[0]['location'][0]
    def get_corpus_id_from_id(self,id):
        response = self.query('"' + str(id) + '"', 'id')
        return response.results[0]['corpus_id'][0]


'''
response = s.query('title:"Ocean"')

print "title " +str(response.results[0]['title'][0])
print "id " +str(response.results[0]['id'])
print "corpus_id " +str(response.results[0]['corpus_id'][0])
location = response.results[0]['location'][0]
print "location " +str(location)
print "url " +str(response.results[0]['url'][0])

'''