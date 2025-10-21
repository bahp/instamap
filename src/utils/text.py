# Libraries
import re
import json
import string
import pandas as pd

# Key spaces before and after since duplicate spaces
# will be removed in one of the final steps of the
# caption processing pipeline.
TAG1 = ' The city of '

def new_line_to_end_sentence(text, sep='.'):
    return text.replace("\n", ".")

def remove_multiple_spaces(text):
    return re.sub(' +', ' ', text)

def bulletpoints_to_location(text):
    """
    What about a list with dots.. or with letters..

    careful that they do not start with \@

    Cy8pUc0M8y8

    1 - @dralbarias
    2 - @francescolp4
    3 - @fnc_86
    4 - @davide_losapio

    """
    "\W"
    return re.sub(r"(\s)?(\d)+\W", TAG1, text)

def icon_to_location(text):
    icons = ["📍", "🌍"]
    for i in icons:
        text = text.replace(i, TAG1)
    return text

def manual_replace(text):
    l = ['LOC :']
    for e in l:
        text = text.replace(e, TAG1)
    return text


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)

    return result

def format_text_chain(text, chain=[]):
    edited = text
    for f, args in chain:
        edited = f(edited, **args)
    return edited

def show(i, post_id, text1, text2=None, result=None):
    """Display the post

    Parameters
    ----------

    Returns
    --------
    """
    # Show
    print("=" * 80)
    print("%3d. %s" % (i, post_id))
    print("-" * 80)
    print(text1)
    print("-" * 80)
    if text2 is not None:
        print(text2)
        print("-" * 80)
    if result is not None:
        for e in result:
            print(e)
    print("\n\n")