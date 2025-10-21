"""

See:
https://www.assemblyai.com/blog/6-best-named-entity-recognition-apis-entity-detection/
https://journal.code4lib.org/articles/15405
"""
# Libraries
import glob
import json
import spacy
import pandas as pd


def create_dataframe_from_docs(docs):
    """Create a csv file with the entities

    Parameters
    ----------

    """
    # Get entities
    entities = []
    for doc in docs:
        for ent in doc.ents:
            entities.extend([[
                doc._.shortcode,
                ent.text, ent.label_, ent.label,
                ent.start, ent.end]])

    # Create DataFrame
    df_entities = pd.DataFrame(
        data=entities,
        columns=['file', 'text', 'label_',
                 'label_id', 'start', 'end']
    )

    # Return
    return df_entities


def compute_NER(text_tuples):
    """Extracts the entities from the text

    .. note: Disable all that is needed.

    .. note: The trf finds only few very accurate entities.
        $ python -m spacy download en_core_web_trf

    .. note: It uses as tuples to include document metadata.
        # Allow to include params in pipe (required)
        from spacy.tokens import Doc
        if not Doc.has_extension("text_id"):
            Doc.set_extension("text_id", default=None)

    .. see: https://spacy.io/usage/processing-pipelines

    .. warning: From the metadata only the text_id is being included.

    Parameters
    ----------
    ext_tuples: The tuples where the first element is the text and
        the second element is a dictionary with the metadata.
        [(text, {text_id: 1}), (text, {text_id: 2})

    """
    # Allow to include params in pipe (required)
    from spacy.tokens import Doc
    if not Doc.has_extension("shortcode"):
        Doc.set_extension("shortcode", default=None)

    # Load model
    #nlp = spacy.load("en_core_web_lg")
    nlp = spacy.load("en_core_web_sm")
    #nlp = spacy.load("en_core_web_trf")

    # Compute pipeline
    doc_tuples = list(nlp.pipe(text_tuples,
        as_tuples=True,
        disable=["tok2vec",
                 "tagger",
                 "parser",
                 "attribute_ruler",
                 "lemmatizer"]))

    # Get docs
    docs = []
    for doc, context in doc_tuples:
        doc._.shortcode = context["shortcode"]
        docs.append(doc)

    # Return
    return docs


# Create the docs
docs = [
    {
        "text": "The big ben is in London.",
        "shortcode": 123456
    },
    {
        "text": "My brother was born in Taiwan.",
        "shortcode": 555555
    },
    {
        "text": "Please, wait for me in the church.",
        "shortcode": 999999
    }
]


# Create text tuples
doc_tuples = [
    (d['text'], {'shortcode': d['shortcode']}) for d in docs
]

# Compute entities
docs = compute_NER(doc_tuples)

# Store them in a DataFrame
df_entities = create_dataframe_from_docs(docs)
df_entities['description'] = \
    df_entities['label_'].apply(lambda x: spacy.explain(x))

# Show
print("Entities:")
print(df_entities)

# Display in server
spacy.displacy.serve(docs, style="ent", port=8777)
