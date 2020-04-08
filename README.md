# FRIWEB Project

Search engine

## Set up

Download the dataset [here](http://web.stanford.edu/class/cs276/pa/pa1-data.zip).

Put it at the root of this repository.

Duplicate the `data_location.template.config`, renaming it as `data_location.config` and change the data path if needed.

If you wish to filter stop words, add a file named `stop_words.txt` 
at the root of this repository. The format must be one stop word per line.

## Structure of the project

## Method

### Statistics of the Text Corpus
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
we would like to be able to link back together. For example, "be", "is" and "are" are 
different forms of the same concept, but look very different.



### Building an Inverted Index
The inverted index allows to link a term back to all the texts in the corpus that contain 
it.
### Boolean Queries
### Vector Queries
### Performance Evaluation
