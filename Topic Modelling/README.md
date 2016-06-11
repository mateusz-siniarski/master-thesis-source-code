#Topic modelling

##FileBrowser.py
Functions for browsing file system

##gen_qrel_res_excel.py
Exports results from Trec Eval to an excel spreadsheet
Input: folder with Trec Eval results, extracted from gen_qrel.py
Output: excel spreadsheet

##gen_qrel.py
Performes TrecEval measures for each topic model.
Input: gold standard spreadsheet, folder with the extracted similar docs for each model, destination path, TrecEval path
Output: folder with Trec Eval results for each topic model

##GenerateSimilarityMatrices.py
Generates the multiple variants of topic models using multiprocessing
Input: Folder with data generated from GenerateWikiCorpus.py
Output: Topic models stored in the input folder

##GenerateWikiCorpus.py
Generates the Wiki corpus and dictionary, nessesary for creating topic models.
Input: WikiExtractor articles, destination path
Output: Folder with the corpus, dictionary and a "binding" file containing reference of the corpus_id, article_id, and relative path to the article in WikiExtractor. 

##SimilarityMeasure.py
Script for retrieving similar documents from an input text.

##SimilarityMeasureAPI.py
Script containing functions for retrieving document title and text

##SimilarityMeasureExport.py
Exports results from similarity measure to excel spreadsheets
Input: Folder with data generated from GenerateWikiCorpus.py, articles from WikiExtractor
Output: Similar docs spreadsheets in the input folder


##SimilarityMeasureExportRelevanceTest.py
Prepares spreadsheet for generating Google Form. Uses pooled relevant documents from all topic models
Input: Folder with data generated from GenerateWikiCorpus.py, articles from WikiExtractor
Output: excel spreadsheet in the input folder

##SolrAPI.py
Set of functions for accessing Solr

##SolrImplementationWiki.py
Script for exporting Wikipedia articles to Solr
Input: Folder with data generated from GenerateWikiCorpus.py, articles from WikiExtractor
Output: Solr index in xml file format stored in the input folder 

##WikiAPI.py
Set of functions for accessing WikipediaAPI

##xlAPI.py
Set of functions for accessing Excel files
