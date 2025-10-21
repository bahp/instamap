"""
https://spotintelligence.com/2022/12/06/named-entity-recognition-ner/
"""

# Libraries
import re
import json
import functools
import pandas as pd

from pathlib import Path
from src.utils import text
from collections.abc import Iterable


def clean_text(text):
    """Do we really want to remove punctuation?"""
    edited = re.sub(r',', ', ', text)
    edited = re.sub(r'[^\w\s]', '', edited)
    edited = re.sub(r"\s+", " ", edited)
    edited = edited.strip()
    edited = edited.lower()
    return edited

def add_metadata(**d):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)
            if isinstance(r, dict):
                return r | d
            if isinstance(r, Iterable):
                return [e | d if isinstance(e, dict) else e for e in r]
            return r
        return wrapper
    return decorator






class NERBase:
    """Basic NER class.

    .. note: Should I make this abstract?
    """
    FILENAME = None
    RENAME = {}
    tagger = None

    def get_path(self, p):
        """Get path with filename."""
        return Path(p) / self.FILENAME

    def exists(self, path):
        """Check if file already exists."""
        return (Path(path) / self.FILENAME).exists()

    def predict(self, txt):
        """Extract entities from text."""
        pass

    def format_text(self, txt, chain=None):
        """Formats the text."""
        return txt

    def select_entities(self, df, **kwargs):
        df = df.rename(columns=self.RENAME)
        return select_entities_from_df(df, **kwargs)

    def from_json(self, filepath, as_frame=False):
        """Loads file from json."""
        with open(filepath, 'r') as file:
            r = json.load(file)
        if as_frame:
            r = self.to_frame(r)
        return r

    def to_frame(self, records):
        """Converts records to DataFrame."""
        return pd.DataFrame.from_records(records)

    def to_json(self, path):
        pass

    def save(self, r, path):
        """Save result as json."""
        with open(Path(path) / self.FILENAME, 'w') as f:
            json.dump(r, f, indent=4)



#
# Dynamic creation of regular expressions.
#
def create_regexp_country_flag(countries):
    """Example: (🇿🇦|🇿🇲|🇿🇼)"""
    return '(%s)' % '|'.join([c.flag for c in countries])

def create_regexp_country_text(countries, attr='name'):
    """Example: (japan|united kingdom)"""
    names = [ getattr(c, attr).lower() for c in countries ]
    #names = ['(?<=\W)%s(?=\W)' % getattr(c, attr).lower() for c in countries]
    return '(?<=\W)(%s)(?=\W)' % '|'.join(names)




def find_countries_v2(txt, attrs=None):
    """"""
    import pycountry
    #if not attr in ['name', 'flag', 'alpha_2', 'alpha_3']:
    #    attr = 'name'
    if attrs is None:
        attrs = ['name', 'flag']
    edited = txt.lower()
    countries = set()
    for country in pycountry.countries:
        for attr in attrs:
            if getattr(country, attr).lower() in edited:
                countries.add(country)
    return countries


def find_countries(txt, attr='name'):
    """Find countries in text.
    """
    import pycountry
    if not attr in ['name', 'flag', 'alpha_2', 'alpha_3']:
        attr = 'name'
    countries = set()
    for country in pycountry.countries:
        if getattr(country, attr).lower() in txt.lower():
            countries.add(country)
    return countries



def re_match_to_dict(m, extra={}):
    d = {'text': m.group(0),
         'start': m.start(),
         'end': m.end(),
         'groupdict': m.groupdict()}
    return {**d, **extra}


def re_finditer(regexp, string, to_dict=True, **kwargs):
    """Executes finditer and r"""
    search = re.finditer(regexp, string,
        flags=re.MULTILINE | re.IGNORECASE)
    if not to_dict:
        return search
    return [re_match_to_dict(m, **kwargs) for m in list(search)]

@add_metadata(method='rule', rule='location')
def regexp_tag_location(txt):
    """Finds the tag location in the text.

    Examples that should be matched:
      Location: Madrid
      Location : Madrid
      Locations : Madrid
      Locations: Madrid
      LOC: Madrid
      LOC : Madrid

    Parameters
    ----------
    txt: string
        The text to match

    Returns
    -------
    List with matches.
    """
    return [{}]

@add_metadata(method='rule', rule='icon')
def regexp_icon_location(txt, icons=None):
    """Return matches with locations based on icons.

    Extracts those matches that...
        a. start with an icon
        b. has at least a word
        b. has anything else but \n or .

    .. note: Enable both start and/or end?
    .. note: ?: is to avoid matching just the icon.
    .. note: <Location> only should be ignored? Thus if the
             pin only contains the word location but no location
             words after removing location, there is no location
             to use. What if too many words, like a sentence, then
             it is probably not a location.

    Possible regular expressions:
    regexp_s1 = '(?:' + s + ')+[^\n\.]*'               # starts with icon
    regexp_s2 = '(?:' + s + ')+[^\n\.]*(?:\w)+[^\n\.]' # starts with icon
    regexp_s3 = '[^\n\.]*(?:\w)+[^\n\.](?:' + s + ')+' # ends with icon
    regexp = '('+ regexp_s2 + ',' + regexp_s3 + ')+'   # combine
    """
    # Default icons that indicate location
    DEFAULT_ICONS_LOC = [
        '🌍', '🌏', '🌐', '🚩', '📍', '📌', '📚'
    ]
    # Check icons
    icons = DEFAULT_ICONS_LOC if icons is None else icons
    s = '|'.join(icons)
    regexp = '(?P<icon>' + s + ')+(?P<location>[^\n\.]*(?:\w)+[^\n\.])'
    return re_finditer(regexp, txt)


@add_metadata(method='rule',
              rule='bullet',
              type='multiline')
def regexp_bullet_location(txt, sep=None):
    """Matches with locations based on bullet points.

    .. note: Maybe it is better to be quite specific with the
             bullet points, specially including the inlines
             introduces a lot of issues as a paragraph might
             have numbers followed by elements.
    .. note: remove @words
    .. note: To improve it create two regexp. The first will
             match common bullet points which are often included
             in new lines. If non found, then we will look for
             inline bullet points.
    .. note: what happens if finding bulling points the result
             is just a single value? Then probably it was not
             a bullet point.

    There should be a .,:|) or something but only a space it
    could be just a number within a frase?

    Explanation
        1. (?<=\W) -> to look back no letters.
        2. (?:\d+)(\s)*(,|\.|\)|-|[A-Z]) -> bulletpoint.
        3. [^\d\n]+ -> anything but another digit or \n

    Regular expression bullet points

    Regular expression for inlines

    Regular expression for multilines
    '^(?P<order>\d+)(?P<sep>(,|\.|\)|-)+)\s*(?P<location>\w\w[^\n\.\d]+)$'

    """
    # Regular expression to find bullet.
    #regexp_bullet =
    # Regular expression for inline bullet points.
    #regexp_inline
    # Regular expression for multiline bullet points
    #regexp_multi

    sep = '|'.join(['\s', '.', ',', ')', '-' ])
    #regexp_s1 = '^(?:\d)+(\s|,|\.|\))[^\n\.]*(?:\w)+[^\n\.]'
    #regexp_v2 = '(?:\d)?' + sep + (,|\.|\))[^\n\.]*(?:\w)+[^\n\.]'
    regexp = '(?:\d+)(\s)*(,|\.|\)|-|[A-Z])[^\n\.](?:\w)+[^\n\.]'
    regexp = '(?<=\W)(?:\d+)(\s)*(,|\.|\)|-|[A-Z])[^\d\n\.]+'
    # To broad gives many issues..
    #regexp = '(?<=\W)(?:\d+)(?!\n)(\s|,|\.|\)|-)+(?=\w)[^\d\n]+'
    multiline = '^(?:\d+)(?!\n)(\s|,|\.|\)|-)+(?=\w)[^\d\n]+'


    # Multiline bullet points
    regexp = '^(\d+)(\s|,|\.|\)|-)*(\w)+[^\n\.]+'
    regexp = '^(\d+)(\s|,|\.|\)|-)*\w\w[^\n\.\d]+$'
    regexp = '^(?P<order>\d+)(?P<sep>(,|\.|\)|-)+)\s*(?P<location>\w\w[^\n\.\d]+)$'

    multiline = re_finditer(regexp, txt)
    # Inline bullet points
    regexp = '(?<=\s)(?:\d+)(\s)*(,|\.|\)|-)+(?=\w)[^\d\n]+'
    singleline = re_finditer(regexp, txt)

    # Return
    return multiline# + singleline


@add_metadata(method='rule', rule='country', attr='flag')
def regexp_country_flag(txt, countries=None):
    """Matches with country flags.

    Parameters
    ----------
    txt: string
        The text to match
    countries: list
        List of country objects (pycountry).

    Returns
    -------
    List with matches.
    """
    if countries is None:
        countries = find_countries_v2(txt, attrs=['flag'])
    regexp = '(?P<flag>%s)' % '|'.join([c.flag for c in countries])
    return re_finditer(regexp, txt)

@add_metadata(method='rule', rule='country', attr='text')
def regexp_country_text(txt, countries=None):
    """Matches with country names.

    Parameters
    ----------
    txt: string
        The text to match
    countries: list
        List of pycountry country objects.

    Returns
    -------
    List with matches.
    """
    if countries is None:
        countries = find_countries_v2(txt, attrs=['name'])
    names = [getattr(c, 'name').lower() for c in countries]
    regexp = '(?<=\W)(?P<name>%s)(?=\W)' % '|'.join(names)
    return re_finditer(regexp, txt)

def regexp_contains_country(txt, attrs=None, countries=None):
    """Matches country flag or name."""
    # Libraries
    import pycountry
    # Basic check
    attrs = ['flag', 'name'] if attrs is None else attrs
    # Get countries
    countries = find_countries_v2(txt, attrs=attrs)
    if not countries:
        return []
    # Get matches
    r1 = regexp_country_flag(txt, countries=countries)
    r2 = regexp_country_text(txt, countries=countries)

    # Add location key to flag regexps.
    for entry in r1:
        entry['groupdict']['location'] = pycountry \
            .countries.get(flag=entry['text']).name

    # Add location key to text regexps.
    for entry in r2:
        entry['groupdict']['location'] = entry['text']

    # Return
    return r1 + r2


class NERRule(NERBase):
    """https://stackoverflow.com/questions/68590366/python-regex-including-comma-and-dot

    Steps:
    1. There are no bullet points
    2. Starts with icon
    3. There are letters at some point.
    3. Ends in . or \n

    The results returned from predict look as follows:

        [
        {
            'text': '🇮🇹',
            'start': 36,
            'end': 38,
            'groupdict': {'flag': '🇮🇹'},
            'method': 'rule',
            'rule': 'country',
            'attr': 'flag'
        },
        {
            'text': 'Italy',
            'start': 30,
            'end': 35,
            'groupdict': {'name': 'Italy'},
            'method': 'rule',
            'rule': 'country',
            'attr': 'text'
        },
        {
            'text': '🌍Duomo di Milano',
            'start': 0,
            'end': 20,
            'groupdict': {
                'icon': '🌍',
                'location': '🇮🇹 Duomo di Milano'
            },
            'method': 'rule',
            'rule': 'icon'
        },
        {
            'text': '1. Brussels by @lorigavalda',
            'start': 206, 'end': 233,
            'groupdict': {
                'order': '1',
                'sep': '.',
                'location': 'Brussels by @lorigavalda'
            },
            'method': 'rule',
            'rule': 'bullet',
            'type': 'multiline'
        }]

    """
    FILENAME = 'ner_rule.json'

    def predict(self, text):
        """Extracts the locations.

        .. note: Remove numbers from bullet points?
        .. note: Remove @username (done)
        .. note: Remove #hashtags (done but reconsider)

        Parameters
        ----------
        text: String
            The text fro which to extract the locations.

        Returns
        --------
        Regular expression results
        """
        # Maybe thy should only be removed when doing
        # the bullet points. There might be some captions
        # in which the location is with a hashtag.
        # Remove user names (@) and hashtags (#)
        #text = re.sub('@(\S)+', '', text)
        #text = re.sub('#(\S)+', '', text)

        # Extract locations from regular expressions
        r_bullet = regexp_bullet_location(text)
        r_icons = regexp_icon_location(text)
        r_countries = regexp_contains_country(text)
        #r_tags =

        # Return
        return r_bullet + r_icons + r_countries

    def to_frame(self, json_result):
        """Load DataFrame from json.

        Parameters
        ----------

        Returns
        --------
        """
        if not json_result:
            return pd.DataFrame()
        df1 = pd.DataFrame(json_result)
        df2 = pd.json_normalize(df1.groupdict)
        r = df1.drop(columns='groupdict').join(df2)
        return r










class NERFlair(NERBase):
    """Extract entities using the flair python package.

    Ref: https://github.com/flairNLP/flair

    .. note: Include other extractors to see if there is one
             good enough to extract full locations, and no need
             for bard.

             https://medium.com/@b.terryjack/nlp-pretrained-named-entity-recognition-7caa5cd28d7b#:~:text=(document).entities-,Flair,train%20each%20classifier%20was%20different%20).


    """

    # Attributes
    FILENAME = 'ner_flair.json'
    RENAME = {
        'text': 'text',
        'value': 'label',
        'start': 'start',
        'end': 'end'
    }
    sentence = None

    def __init__(self):
        """"""
        pass

    @add_metadata(method='flair')
    def predict(self, txt):
        """Extracts the entities."""
        # Create tagger on first predict
        if self.tagger is None:
            # Libraries
            from flair.nn import Classifier
            # Tagger
            self.tagger = Classifier.load('ner')

        # Library
        from flair.data import Sentence
        # Make prediction
        self.sentence = Sentence(txt)
        self.tagger.predict(self.sentence)
        return self.sentence.to_dict(tag_type='ner')


    def format_text(self, txt, chain=None):
        """Format the text.

        .. note: This formatting was mostly a hack to include
                 information that would help the model to identify
                 the locations. Since they are now extracted with
                 the NERRule, it is not needed.

        .. note: The caption should not be modified to ensure that
                 the start and end positions are with respect to the
                 original caption.

        """
        return txt
        """
        if chain is not None:
            return text.format_text_chain(text=txt, chain=chain)

        # Default formatting
        edited = text.format_text_chain(text=txt,
            chain=[
                (text.bulletpoints_to_location, {}),
                (text.icon_to_location, {}),
                (text.new_line_to_end_sentence, {}),
                (text.remove_multiple_spaces, {})
            ])
        # Return
        return edited
        """

    def to_json(self, r):
        return self.sentence.to_dict(tag_type='ner')

    def to_frame(self, json_result):
        """Load DataFrame from json.

        Parameters
        ----------

        Returns
        --------
        """
        if not 'entities' in json_result:
            return pd.DataFrame()
        if not len(json_result['entities']):
            return pd.DataFrame()

        df1 = pd.DataFrame(json_result['entities'])
        df1 = df1.explode('labels')
        df2 = pd.json_normalize(df1.labels)
        r = df1.drop(columns='labels').join(df2)
        r = r.rename(columns={
            'start_pos': 'start',
            'end_pos': 'end'
        })
        return r






















class NERBard(NERBase):
    """"""
    FILENAME = 'ner_bard.json'
    RENAME = {
        'name': 'text'
    }

    # Query
    QUERY1 = """Please construct a json file extracting for each of 
        the locations in the following caption the name (name), the 
        full address (full_address) and the order (order) in which 
        it was found in the text.

        The caption is: %s
    """

    QUERY2 = """Please construct a json file extracting for each of 
        the locations in the following caption the name, the named 
        entities (e.g. person and location) with their start, end and 
        confidence, and the order in which it was found in the text.
        
        The caption is: %s
    """

    def __init__(self, query=QUERY1):
        """"""
        self.query = query

    def exists(self, path):
        """Check if file already exists.

        .. note: There might be files that do not contain a
                 JSON just because a location was no identified
                 in the content. It would be querying them over
                 and over if using that condition.
        """
        filepath = (Path(path) / self.FILENAME)
        file_exists = filepath.exists()
        with open(filepath, 'r') as f:
            content = json.load(f)['content']
        file_is_json = self.response_extract_json(content) is not None
        file_is_error = content.startswith('Response Error:')
        return file_exists and not file_is_error #file_is_json

    def predict(self, text):
        """Extract the entities."""
        # Create tagger if it is the first query.
        if self.tagger is None:
            # Libraries
            from bardapi import BardCookies
            from dotenv import load_dotenv

            # Create tagger on first predict.
            self.tagger = BardCookies(
                token_from_browser=True, timeout=40
            )

        # Return answer
        return self.tagger.get_answer(self.query % text)

    def to_json(self):
        pass

    def from_json(self, filepath, as_dataframe=False):
        """"""
        import json
        with open(filepath, 'r') as file:
            r = json.load(file)
        r = self.response_extract_json(r['content'])
        if r is None:
            print(filepath)
            return None

        # Sometimes the result has an attribute locations
        # with the array of locations. However, sometimes
        # the array is inserted directly.
        if 'locations' in r:
            r = r['locations']

        if as_dataframe:
            r = pd.DataFrame.from_records(r)
        return r

    def response_extract_json(self, content):
        """"""
        # Libraries
        import re
        # Get response
        # Use regular expression to find the JSON string
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)

        if json_match:
            json_string = json_match.group(1)
            try:
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No JSON found in the response.")
            return None



class NERSpacy(NERBase):
    """Extract entities using the spacy python package.

    The possible options are:
     - "en_core_web_sm"
     - "en_core_web_md"
     - "en_core_web_lg"
     - "en_core_web_trf"

    """
    FILENAME = 'ner_spacy.json'
    RENAME = {
        'text': 'text',
        'label': 'label',
        'label_': 'label_',
        'start': 'start',
        'end': 'end'
    }

    def __init__(self, model="en_core_web_sm"):
        """"""
        self.model = model
        self.FILENAME = self.FILENAME \
            .replace('.json', '-%s.json' % model)

    def predict(self, text):
        """Extracts the entities."""
        if self.tagger is None:
            # Library
            import spacy
            # Create tagger on first predict
            self.tagger = spacy.load(self.model)

        # Find entities
        doc = self.tagger(text)
        # Return
        return self.to_dict(doc)


        # How to convert results to dict automatically.
        #return doc.to_dict()



        """
        entities = []
        for ent in doc.ents:
            entities.extend([[
                ent.text, ent.label_, ent.label,
                ent.start, ent.end]])

        # Convert text to tuples
        text_tuples = [(text, {})]

        #
        doc_tuples = list(self.tagger.pipe(text_tuples,
                      as_tuples=True,
                      disable=["tok2vec",
                               "tagger",
                               "parser",
                               "attribute_ruler",
                               "lemmatizer"]))

        # Create list
        from collections import defaultdict

        #print(entities)
        ents = self.to_json(doc)
        docs = self.get_docs_from_tuples(doc_tuples)
        ents = self.to_json(docs)
        """
        
    def format_text(self, txt, chain=None):
        """Format the text.

        .. note: This formatting might different depending
                 on the algorithm to make it pick up more
                 elements (in particular locations)
        """
        if chain is not None:
            return text.format_text_chain(text=txt, chain=chain)

        # Default formatting
        edited = text.format_text_chain(text=txt,
            chain=[
                #(text.bulletpoints_to_location, {}),
                #(text.icon_to_location, {}),
                (text.new_line_to_end_sentence, {}),
                (text.remove_multiple_spaces, {})
            ])

        # Return
        return edited

    def to_dict(self, doc):
        """Formats the doc to a dictionary of entities"""
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'label_': ent.label,
                'start': ent.start,
                'end' : ent.end
            })
        return entities


    def filter(self, df):
        """"""


    def to_json(self, docs):
        """
        """
        entities = []
        for doc in docs:
            for ent in doc.ents:
                entities.extend([[
                    # doc._.text_id,
                    ent.text, ent.label_, ent.label,
                    ent.start, ent.end]])

    def get_docs_from_tuples(self, doc_tuples):
        # Get docs
        docs = []
        for doc, context in doc_tuples:
            # doc._.text_id = context["text_id"]
            docs.append(doc)
        return docs

    def to_dataframe(self, docs):
        """"""
        lists = self.to_list(docs)
        df_entities = pd.DataFrame(
            data=docs,
            columns=['text', 'label_', 'label_id', 'start', 'end']
        )

    def to_list(self, docs):
        entities = []
        for doc in docs:
            for ent in doc.ents:
                entities.extend([[
                    # doc._.text_id,
                    ent.text, ent.label_, ent.label,
                    ent.start, ent.end]])
        return entities




class NERNLTK:
    TAG = 'nltk'

    def save(self, filepath):
        pass






class NERBert:
    TAG = 'bert'

    def save(self, filepath):
        pass




def select_geolocation_query(df):
    """"""
    #if not matches:
    #    return None

    # Create DataFrame
    #df = pd.DataFrame(matches)
    df['query'] = df['query'].str.lower()
    df = df.drop_duplicates(subset=['query'])

    # Count types of regexp
    counts = df.rule.value_counts()

    # Keep bullets
    if 'bullets' in counts:
        df = df[~df.rule.isin(['country'])]
    if 'icon' in counts:
        df = df[~df.rule.isin(['country'])]

    return df



# I get many repeated
# I get issues with punctuation
def select_entities_from_df(df,
        rename={}, entity_types=None,
        min_confidence=0, top_n=None):
    """"""
    # Basic formatting
    df = df.reset_index()
    df = df.rename(columns=rename)
    #df.text = df.text.str.lower()

    df = select_geolocation_query(df)

    #if 'groupdict' in df:
    #    aux = pd.json_normalize(df['groupdict'])
    #    df = pd.concat([df, aux], axis=1)


    if 'label' in df:
        if entity_types is not None:
            if isinstance(entity_types, str):
                entity_types = [entity_types]
            df = df[df.label.isin(entity_types)]

    if 'confidence' in  df:
        df = df[df.confidence >= min_confidence]
        df = df.sort_values(by=['confidence'], ascending=False)

    if top_n is not None:
        df = df.head(top_n)
        #df = df.groupby(by='shortcode').head(top_n)


    # Drop any duplicates
    #df = df.drop_duplicates(subset=['text'])
    df = df.drop_duplicates(subset=['query'])

    return df



def select_entities_flair(df,
                          entity_types=['LOC'],
                          min_confidence=0,
                          top_confidence=None):
    """
    The columns are:
           text
           start_pos
           end_pos
           value
           confidence

    :param df:
    :param entity_types:
    :param min_confidence:
    :param top_confidence:
    :return:
    """
    # Libraries
    from src.utils.text import remove_punctuation

    # Define which entities to keep
    df = df[df.value.isin(entity_types)]
    df = df[df.confidence >= min_confidence]
    df.text = df.text.str.lower()
    df = df.drop_duplicates(subset=['text'])

    # Filter by confidence
    if top_confidence is not None:
        df = df.sort_values(by=['confidence'], ascending=False)
        df = df.groupby(by='shortcode').head(top_confidence)

    df['text'] = df.text.str.lower()
    df = df.drop_duplicates(subset=['text'])
    # df = df.head(30)
    # df = df.reset_index(drop=True)
    # df = df.set_index('text')

    # Return
    return df

def select_entities_bard(df):
    df = df.rename(columns={
        'name': 'text'
    })
    df.text = df.text.str.lower()
    df = df.drop_duplicates(subset=['text'])
    return df