# FRIWEB Project

This is a search engine made for a course at CentraleSupélec.
We are working with a dataset from Stanford, available [here](http://web.stanford.edu/class/cs276/pa/pa1-data.zip).

The search engine takes text queries (exemples provided in the data folder) and answers with the id of relevant documents. We do not sort the documents by importance.

## Set up

This project is written with **Python 3**. All the following commands using python are implicitly using Python 3.

Download the full dataset [here](https://drive.google.com/open?id=1zLPHK_Wv3WFsC5Zww2EEvW_7Yt1Djvhj).
It contains the corpus, queries, stop words, pre-computed collection and indexes.

Put it at the root of this repository.
Check that it matches the paths in `config.py`.

Run the following command to install requirements (it is recommanded to use a virtual env):

```
pip install -r requirements.txt
```

### Generate collection and inverted index

_Note: Skip this section if you have downloaded the full dataset, with corpus, queries, stop words and pre-computed collection and index._

Requirements (all these files and folders should be under the `data/` directory):

- [Stanford corpus](http://web.stanford.edu/class/cs276/pa/pa1-data.zip) as `pa1-data`
- [Queries](https://drive.google.com/open?id=1B5flJ48VN2x5XNXRJ1zWpEyopoxrvrCT) as `queries`
- [TIME.STP](http://ir.dcs.gla.ac.uk/resources/test_collections/time/) as `stop_words.txt`

To generate the collection, run:

```
python collection_processing.py
```

This will load the raw texts from the dataset, process them into the usable format described below, and write the collection to `data/collection.pkl`.

Then build the inverted indexes (`simple` and `frequency`) with the following command:

```
python inverted_index.py
```

### Test the models

To test the model, run the script `test_model.py`.
You have to use the following options to specify what type of model you would like to use:

```
python test_model.py boolean
```

```
python test_model.py vectorial --weight-query    {boolean, frequency}
                               --weight-document {boolean, frequency, tf_idf_normalize,
                                                  tf_idf_logarithmic, tf_idf_logarithmic_normalize}
```

## Method

### Processing Inputs

We process all text inputs, that is, the texts from the corpus and
the queries. This gives us usable representations of the given texts.

Here are the steps we take to process texts:

#### Tokenization

This step takes a raw text and transforms it into words. We do this by simply
splitting the original text with the _space_ as a separator character. We therefore get
a collection of **terms**.

#### Stop words

Many terms in a text of a request are not useful for categorizing their
content, such as "the" or "are". Removing stop words is especially useful
because they are present in virtually all texts in the corpus, and so,
they increase the size of the inverted index significantly.

In order to determine which terms are stop words, we first try to use a list of pre-defines stop words extracted from the [TIME](http://ir.dcs.gla.ac.uk/resources/test_collections/time/) collection.

But we realized that some queries were only made of stop words, so we couldn't just remove every single word in them. We finally decided to keep stop words in the index and to remove them from queries only if they have non stop words. Doing so, we get the same results on queries with non stop words, but we are also able to answer queries only made of stop words.
For exemple:

- The query `a student class` becomes `student class` because it has at least one word that isn't stop word.
- We leave the query `the the` as it is since it is only made of stop words.

The drawback of this approach is that the index is larger and may take longer to compute on very big datasets. But it didn't have much impact for our scope.

#### Stemming and Lemmatization

Once relevant words have been extracted from a text, they can take several forms, which
we would like to be able to link back together. For example, "paste", "pasting" and "pastes" are
different forms of the same concept, but with different spelling.

For this purpose, _stemming_ is a technique which removes the prefixes and suffixes a word can have
For example, the words "paste", "pasting" and "pastes" will all be reduced to "past", which
is their common radical. For this work, we use Porter's Stemming algorithm.

Lemmatization allows to group together words that, despite being variations of one another,
are morphologically different. For example, "be", "is" and "are" are all conjugations of the verb "to be"
and would therefore all be transformed into "be".

This addresses the inherent difficulty that English has subtle variations of words of similar
meaning but different form.

The text corpus we are using contains an additional hardship. Many of them contain
typos, such as "campsit"; abbreviations, such as "rd", "qtr", or "csl tr"; file
names such as "06obasketballboy".

#### Aggregating and Counting Duplicate Words

The words have been grouped by meaning. We now aggregate duplicate words to count them.
This allows us to estimate how important a certain term is in a text.

The output of all the above steps is a _bag of words_. In our representation of the text, the frequency of the terms is important, but not their order.

### Statistics on the Collection

Once we have processed the texts from the corpus, we run a few statistics on the resulting collection. For exemple the most frequent word and its number of occurences, the average frequence of words, ...

These statisticts are used to compute the frequency inverted index, as explained below.

### Building an Inverted Index

The inverted index allows to link a term back to all the texts in the corpus that contain
it. It is implemented as a dictionary, where the keys are the terms present in the collection,
and the values are a list of the id of all the documents that contain the term.

This allows the search engine to take terms as an input, and output document names.
The index may come with statistics which allow for better performances.
In the _frequency inverted index_, we added the possibility to know how many occurrences of the term
used as a key there are in the documents pointed to by that key. This statistic is called term frequency (_tf_)
and is used in the _tf/idf_ metric.

This step takes a long time to compute (a few hours on this dataset), since we need to go through
each document for each term. After computation, the resulting index is stored in a file (using _pickle_).
When processing queries, we are loading the index from the file to avoid computing it again.

### Boolean Model

Boolean models is a simple way to find relevant document. The idea is to transform the query in a boolean query by adding boolean operators between words. For exemple, `students class` can become `students AND class` or `students OR class`. Then, we are looking for all documents that satisfy the boolean query, using the inverted index.

We have decided to keep our boolean model simple by only adding `AND` operators betweens words. Which means that we are looking for the documents that contains all the query terms.
For exemple, with the `students class` query, we are looking for all documents that contains `student` and `class`.

Our boolean model is defined in `boolean_model.py`.

### Vectorial Model

Our vectorial model is defined in `vectorial_model.py`.

### Performance Evaluation

To measure performances, we are using `test_model.py`, a script that is processing all queries, and comparing the predictions with the expected output given with the dataset.
The script allows to test both models.

The results for the boolean model are:

```
query 'the the': expected 81770 elements - got 81769 - 1 elements different
query 'stanford computer science': expected 4232 elements - got 813 - 3839 elements different
query 'we are': expected 12409 elements - got 6111 - 6306 elements different
query 'a': expected 66675 elements - got 68966 - 2295 elements different
query 'stanford students': expected 22335 elements - got 12605 - 14340 elements different
query 'very cool': expected 63 elements - got 777 - 716 elements different
query 'the': expected 81770 elements - got 81769 - 1 elements different
query 'stanford class': expected 6094 elements - got 2414 - 5126 elements different
```

And the results for the vectorial model are:

```
query 'the the': expected 81770 elements - got 81769 - 1 elements different
query 'stanford computer science': expected 4232 elements - got 74658 - 70426 elements different
query 'we are': expected 12409 elements - got 45490 - 33081 elements different
query 'a': expected 66675 elements - got 68966 - 2295 elements different
query 'stanford students': expected 22335 elements - got 72921 - 50586 elements different
query 'very cool': expected 63 elements - got 777 - 716 elements different
query 'the': expected 81770 elements - got 81769 - 1 elements different
query 'stanford class': expected 6094 elements - got 73118 - 67024 elements different
```

Our boolean model seems to return less accurate documents that what is expected. On the other side, our vectorial model is predicting much more accurate document than expected. This is understandable: since the boolean model is only keeping documents that contains **all** the terms, it is likely to be more restrictive.

We notice that performances are good on queries containing only stop words. However, performances aren't very good on the other queries. The boolean model still seems to have better performances than the vectorial, because the later is returning too much documents.
