# FRIWEB Project

Search engine
talk about the specificities here : no pagerank, pure text, waht kinds of queries we work with
etc

## Set up

Download the dataset [here](http://web.stanford.edu/class/cs276/pa/pa1-data.zip).

Put it at the root of this repository.

Duplicate the `data_location.template.config`, renaming it as `data_location.config` and change the data path if needed.


If you wish to filter stop words, add a file named `stop_words.txt` 
at the root of this repository. The format must be one stop word per line.

## Structure of the project

## Method

### Processing Inputs

We process all text inputs, that is, the texts from the corpus and
the queries. This gives us usable representations of the given texts.

Here are the steps we take to process texts:
#### Tokenization
This step takes a raw text and transforms it into words. We do this by simply
splitting the original text with the _space_ as a separator character. We therefore get
a collection of __terms__.

#### Removing stop words
Many terms in a text of a request are not useful for categorizing their
content, such as "the" or "are". Removing stop words is especially useful
because they are present in virtually all texts in the corpus, and so,
they increase the size of the inverted index significantly.

In order to determine which terms are stop words, we use a list of pre-defines stop words
which one can find in the TIME series under TIME.STP.

#### Stemming and Lemmatization
Once relevant words have been extracted from a text, they can take several forms, which
we would like to be able to link back together. For example, "paste", "pasting" and "pastes" are 
different forms of the same concept, but look very different.

For this purpose, Stemming is a technique which removes the prefixes and suffixes a word can have
For example, the words "paste", "pasting" and "pastes" will all be reduced to "past", which
is their common radical. For this work, we use Porter's Stemming algorithm.

Lemmatization allows to group together words that, despite being variations of one another,
are morphologically different. For example, "be", "is" and "are" are all conjugations of the verb "to be"
and would therefore all be transformed into "be".

This addresses the inherent difficulty that English has subtle variations of words of similar
meaning but different form.

The text corpus we are to study contain an additional hardship. Many of them contain 
typos, such as "campsit"; abbreviations, such as "rd",  "qtr", or "csl tr"; file 
names such as "06obasketballboy".

#### Removal and Counting of Duplicate Words
The words have been grouped by meaning,so we can now remove duplicate words in a text and count them.
This allows us to estimate how important a certain term is in a text.

Once we have processed a text following the above steps, we can represent it as 
a "bag of words". That is because all that is important, are the terms and their frequencies,
but not their order, in our representation of the text.

### Statistics of the Text Corpus
Once we have processed the texts from the corpus, we ran a few statistics.

### Building an Inverted Index
The inverted index allows to link a term back to all the texts in the corpus that contain 
it. It is implemented as a dictionary, where the keys are the terms present in the collection, 
and are linked to a list of all the titles of the documents that they are a part of. 
This then allows the search algorithms to take terms as an input, and output document names.
The index may come with statistics which allow for getter search algorithms. 
In this implementation, we added the possibility to know how many occurrences of the term 
used as a key there are in the texts pointed to by that key. This statistic is called _tf_
and is used in the _tf/idf_ criterion.

This step takes a very long time (a few hours on this dataset) since we need to go through
each document for each term, and there are X terms and X documents. Therefore, the index can be stored 
in a file, and then loaded, so it only has to be calculated once. 
### Boolean Queries
Boolean Queries are a simple type of query, whereby we wish to get all the documents that 
satisfy a boolean expression for containing or not containing the terms of the query.

For example, if we wish to look for documents  

### Vector Queries

### Performance Evaluation
