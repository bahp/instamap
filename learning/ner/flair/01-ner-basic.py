"""
Description: Playing around with flair for named entity recognition

Other pontential things that might be interesting are sentiment analysis
and extracting keywords (maybe not in this case since we already have
hashtags?). Anyways, links below.

See:
  1. Sentiment with vader on instagram captions
  https://medium.com/analytics-vidhya/sentiment-analysis-on-instagram-captions-in-under-80-lines-of-code-b429c8193a4a

  2. Extracting keywords.
  https://www.analyticsvidhya.com/blog/2022/01/four-of-the-easiest-and-most-effective-methods-of-keyword-extraction-from-a-single-text-using-python/
"""

# Libraries
import re
import json
import pandas as pd

from pathlib import Path
from flair.data import Sentence
from flair.nn import Classifier


"""
# Define path
path = Path("../../../data/nlp/s1.txt")

# Load data
with open(path, "r") as f:
    data = f.read()
"""

data = '''
    This is a sample text created by Alfredo.
    Alfredo was born in Paris, France on the 3rd of November.
    He works for an american tech company, Google.
    '''

def display_example_header(i):
    print("\n\n" + "="*80)
    print(i)
    print("=" * 80)

def format_text(txt):
    """
    .. note: Not removing spaces if tabular.
    """
    # Clean text
    text = txt
    text = text.strip()
    text = text.replace("#", '')
    text = text.replace(".", ". ")
    text = text.replace(",", ", ")
    return text

def split_sentences(txt):
    """
    .. note: Not filtering if tabular or spaces.
    """
    return list(filter(None, txt.split("\n")))

def flatten_flair_entities(d):
    """The input is the entities dict."""
    if not d:
        return pd.DataFrame()
    df1 = pd.json_normalize(d, sep='.').explode('labels')
    df2 = pd.json_normalize(df1.labels)
    r = pd.concat([df1, df2], axis=1).drop(columns='labels')
    return r

def fair_nlp_entities_dataframe(r):
    """
    .. note: Very dirty dont use it.
    """
    aux = pd.DataFrame()
    entities = r['entities']
    for e in entities:
        lbl = pd.DataFrame(e['labels'])
        lbl['text'] = e['text']
        aux = pd.concat([aux, lbl])
    return aux


def process_sentences(sentences, tagger):
    """

    :param sentences:
    :param tagger:
    :return:
    """
    # Create empty results
    results = []

    # Loop for each sentences
    for i, s in enumerate(sentences):
        print("%s. Computing sentence... <%s>" % (i, s))

        # Extract entities
        edited = format_text(s)
        sentence = Sentence(edited)
        tagger.predict(sentence)
        r = sentence.to_dict(tag_type='ner')

        # Append
        results.append(r)

    # Return
    return results



# -------------------------------------
# Example 0: Named entity recognition
# -------------------------------------
display_example_header(i='0. Named Entity Recognition (NER)')

# make a sentence
sentence = Sentence('I love Berlin and London.')
# load the NER tagger
tagger = Classifier.load('ner')
# run NER over sentence
tagger.predict(sentence)
# Show
print(sentence)

# Show probabilities
for entity in sentence.get_labels():
    print(entity)

    #print(dir(entity))
    #print(entity.value)
    #print(entity.score)
    #print(entity.shortstring)



# -------------------------------------
# Example 1: Sentiment analysis
# -------------------------------------
display_example_header(i='1. Sentiment Analysis')

# make a sentence
sentence = Sentence('I love Berlin and London.')
# load the NER tagger
tagger = Classifier.load('sentiment')
# run NER over sentence
tagger.predict(sentence)
# print the sentence with all annotations
print(sentence)



# --------------------------------------
# Example 2: As a whole
# --------------------------------------
# In this example we will consider that the text s a single sentence.
# Although in reality it is composed of three. This approach might word
# for text in captions (e.g. Instagram) but for longer texts might be better
# to divide it in sentences.

display_example_header("2. NER Loop (full text as sentence)")

# Create sentences
sentences = [data]
# Create classifier
tagger = Classifier.load('ner')
# Loop
results = process_sentences(sentences, tagger)
# Show DataFrame
df = flatten_flair_entities(results[0]['entities'])

# Show
print("Sentences:")
print(sentences)
print("Results:")
print(df)
#print("Full:")
#print(json.dumps(results, indent=4))


# --------------------------------------
# Example 4: Divide it in sentences
# --------------------------------------
display_example_header("2. NER Loop (split sentences)")

# Create sentences
sentences = split_sentences(data)
# Process sentences
results = process_sentences(sentences, tagger)
# Create DataFrame
df = flatten_flair_entities(results[0]['entities'])

# Show
for s,e in zip(sentences, results):
    df = flatten_flair_entities(e['entities'])
    print(s)
    print(df)
    print("\n")
