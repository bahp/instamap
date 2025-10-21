#
from src.utils import ner

DEFAULT_TAGGERS = {
    'rule': ner.NERRule(),
    'flair': ner.NERFlair(),
    'spacy': ner.NERSpacy(),
    'spacy-sm': ner.NERSpacy(model='en_core_web_sm'),
    'spacy-lg': ner.NERSpacy(model='en_core_web_lg'),
    'spacy-trf': ner.NERSpacy(model='en_core_web_trf'),
    'bard': ner.NERBard()
}


