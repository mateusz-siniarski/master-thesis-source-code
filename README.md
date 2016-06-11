#The source code from my master's thesis: "Knowledge discovery from large collections of unstructured information"
This repository contains the source code created during my master's thesis.

##Topic modelling
The code contains a [Gensim](https://github.com/piskvorky/gensim) implementation for the following parts of generating and evaluating the topic models:
* Generating corpus and dictionary from Wikipedia articles (dumpfiles extracted from [WikiExtractor] (https://github.com/attardi/wikiextractor))
* Generating multiple topic models variants using multiprocessing
* Export similar documents from a list of seed documents
* Generate input data for Google Form
* Generate index of selected Wikipedia articles for Solr

##Named entity recognition
* Processes abs_matches output files from MRNER and WoRMSNER
* Processes output from extracted variable changes
* Generate index of Wikipedia articles referenced in NERs
* Generate separate index for each NER

##Google Forms generator
Uses a Google Spreadsheet as input for generating form. The added features include:
* Introduction page with description and personal data survey
* 20 pages containing 10 questions about the relevance level of the Wikipedia articles
* The WikiAPI is used for extracting summaries of Wikipedia articles.

##Ocean Wiki search engine
Contains a modified version of [SolrStrap](https://github.com/fergiemcdowall/solrstrap). The features include:
* Instant search
* Infinite scrolling
* Facets for filtering results
* Map displaying geographical facets
* Text snippets displaying the direction change of the variables
