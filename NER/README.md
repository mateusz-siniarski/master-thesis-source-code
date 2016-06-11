#Named entity recognition

##MarineRegionsAPI.py
Extraction of additional metadata for geolocation entities:
* Placetype
* Coordinates

##prepareMRNER.py
Prepares relevant articles to NER processing by storing in individual text files.

Input: XLS excel file with relevant articles, articles from WikiExtractor, destination path

Output: Folder containing text files of relevant articles.

##SolrImplementationGeoLocations.py
Creates index with the geographical locations.

Input: abs_matches from MRNER, destination path, 

Output: XML index for Solr

##SolrImplementationMergeNERsVars
Creates index with Wikipedia articles and references to extracted entities and variables.

Input: abs_matches from MRNER, abs_matches from WoRMSNER, destination path, binding file, articles from WikiExtractor

Output: XML index for Solr

##SolrImplementationVariableChange.py
Creates index with the extracted variable changes.

Input: matches from the extracted variables, destination path 

Output: XML index for Solr


##StatisticsNER.py
Calculates average entities per articles

Input: abs_matches file
