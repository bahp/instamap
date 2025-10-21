
SHORTCODE_CLASSES = {
    'bulletpoints': [
        'CzBYpc5ocQb', 'CvE3TlxLgKU', '11111111'
    ],
    'icons': [
        'CxQ1tJ8rV9w', 'CytHvWGIh8M', 'CnUFPmav67B', 'CvIEfZVNIDm',
        'CylhhZXM5mO', 'Cy6EgYltiFv', 'CyubKljvvNy', 'CytMiMBtB6c',
        'CwsXj8kNSQh', 'Cyxz2rhNscp', 'CyknIJtI2k6', 'CylDyTNtVZc',
        'CykUIy8oIrw', 'CyTf-iOIWjq', 'CwcLq14s4Mk', 'CyQWtpzru19',
        'CyQnvkOtqzx', 'CyEJ3mLIUV1', 'CyLtbl6twpu', 'Ct6C0desz3b',
        'CyGDGR3sv7z', 'CxRC5lZoKHm', 'Cx3yIHTocBA', 'CxNzc1IIitt',
        'Cql5SkNrB_I', 'CxL0HHYIfb5', 'CxXX44btaHb'
    ],
    'flags': [
        'CvE3TlxLgKU', 'Cy-hYVzPemK', 'CxQ1tJ8rV9w', 'CzBYpc5ocQb',
        'CyRLr01sj8i', 'CysEVwgqeS8', 'Cy6EgYltiFv'
    ],
    'todo': [
        'B5ewgDhKQth', #Location: ITALY CALABRIA
        'B5NqBLMJGZM' #Belgium / bullet!
    ],
    'hashtags': [
        'Cy3hRvYoEQt', 'Cym0t2ftWMN'
    ],
    'address': [
        'Ct6C0desz3b'
    ]
}





if __name__ == '__main__':


    # https://regex101.com/r/6Y1X1k/3

    import re
    import sys

    from pathlib import Path

    # Libraries
    from src.utils.ner import re_match_to_dict
    from src.utils.ner import regexp_icon_location
    from src.utils.ner import regexp_bullet_location
    from src.utils.ner import regexp_country_flag
    from src.utils.ner import regexp_country_text
    from src.utils.ner import regexp_contains_country
    from src.utils.ner import NERRule


    def show_header(i):
        print("\n")
        print("="*80)
        print("Example %s" % i)
        print("="*80)

    def show_result(text, results):
        print("="*80)
        print(text)
        print("\n")
        for r in results:
            print(r)
        print("\n\n")

    def load_post(path, shortcode):
        fullpath = path / shortcode / 'caption.txt'
        with open(fullpath, 'r') as f:
            return f.read()

    def run(text, regexp):
        search = re.finditer(regexp, text, re.MULTILINE)
        r = [re_match_to_dict(m) for m in search]
        show_result(text, r)


    # Define path
    PATH = Path('./data/bernardhp/posts/')

    # Create some samples
    text1 = """
        🌍 Madrid
        🌏 Kuala Lumpur
        🌐🚩 Guatemala
        Hatchard's library 📚
        📍 London, United Kingdom
        📌Manchester, United Kingdom 
    """

    text2 = """
        1 Sample
        01 Sample
        1. Sample
        1) Sample
        1- Sample
        1, Sample
        1 , Sample
        1 - Sample
        1. NaMme: Description
    """

    text3 =  """
        A paragraph is defined 🇼🇫 🇼🇸 as “a group of sentences or a single sentence 
        that forms a unit” (Lunsford and Connors 116). Length and appearance 
        do not determine 🇾🇪🇿🇦 whether a section in a paper is a paragraph. For 
        instance, in some styles of writing, particularly journalistic styles, 
        a paragraph can be just one sentence long. 🇿🇲🇿🇼 
    """

    text7 =  """
        A paragraph is defined 🇼🇫 🇼🇸 as “a group of sentences or a single sentence 
        that forms a unit” (Lunsford and Connors 116). Length and appearance 
        do not determine 🇾🇪🇿🇦 whether a section in a paper is a paragraph. For 
        instance, in some styles of writing, particularly journalistic styles, 
        a paragraph can be just one sentence long. 🇿🇲🇿🇼 Spain France
    """

    text4 = load_post(PATH, shortcode='CzBYpc5ocQb')
    text5 = load_post(PATH, shortcode='CvE3TlxLgKU')
    text6 = load_post(PATH, shortcode='CzD6fazOqTe')

    MANUAL = False


    if MANUAL:

        # ---------------------------------
        # Icon indicating location
        # ---------------------------------
        r = regexp_icon_location(text1)
        show_header(i="icon")
        show_result(text1, r)

        # ---------------------------------
        # Bullet points
        # ---------------------------------
        r = regexp_bullet_location(text2)
        show_header(i="bulletpoint")
        show_result(text2, r)

        r = regexp_bullet_location(text3)
        show_header(i="bulletpoint")
        show_result(text3, r)

        r = regexp_bullet_location(text4)
        show_header(i="bulletpoint")
        show_result(text4, r)

        # ---------------------------------
        # Country flag and/or text
        # ---------------------------------
        r = regexp_contains_country(text3, attrs=['name'])
        show_header(i="Country name")
        show_result(text3, r)

        r = regexp_contains_country(text7, attrs=['flag'])
        show_header(i="Country flag")
        show_result(text7, r)

        r = regexp_contains_country(text7, attrs=['name'])
        show_header(i="Country name")
        show_result(text7, r)

        r = regexp_contains_country(text7)
        show_header(i="Country flag and name")
        show_result(text7, r)



    # ---------------------------------
    # Refining regular expressions
    # ---------------------------------
    # Define interesting codes.
    shortcodes = [
        'CzBYpc5ocQb', 'CvE3TlxLgKU', 'CzD6fazOqTe', 'Cy-OtEUMuZd',
        'CstVx6CP_kO', 'CyQW2D2IL6U', 'Cy-vFBSyIuA', 'Cy8pUc0M8y8'
    ]

    # ---------------------------------
    #
    # ---------------------------------
    sep = '(%s)' % '|'.join(['.', ',', ')', '-'])
    regexp = '(?:\d)+(\s)*(\s|,|\.|\)|-)'
    #regexp = '^(?:\d)+(\s|,|\.|\))[^\n\.]*(?:\w)+[^\n\.]'         # bahp v1
    #regexp = '(\d+)(\s)*(,|\.|\)|-|[A-Z])[^\n\.]*(?:\w)+[^\n\.]'  # bahp v2
    #regexp = '(?:\d+)(\s)*(,|\.|\)|-|[A-Z])[^\n\.](?:\w)+[^\n\.]' # bahp v3
    regexp = '(?<=\W)(?:\d+)(\s)*(,|\.|\)|-|[A-Z])[^\d\n]+'        # bahp v4
    #regexp = '(?:^|(?<=\s))\d\.?(?:\d+)?(?=\s)|\*(?=\s)'          # online 1
    #regexp = '\((\d+)\)\s+(.*?)(?=/(?:\(\d+\)))'                  # online 2
    # Regexp just bullet
    regexp = '(?<=\W)(?:\d+)(?!\n)(\s)*(,|\.|\)|-|[A-Z])(?<=\w)[^\d\n]+'
    regexp = '(?<=\W)(?:\d+)(?!\n)(\s|,|\.|\)|-)+(?=\w)[^\d\n]+'
    regexp = '^(?:\d+)(?!\n)(\s|,|\.|\)|-)+(?=\w)[^\d\n]+'

    import string
    #string.punctuation

    bullet = '(?<=\W)(?:\d+)(\s|,|\.|\)|-)*(?=\w)[^\n]+'

    multiline = '^(\d+)(\s|,|\.|\)|-)*(\w)+[^\n\.]+'
    inline = '(?<=\s)(?:\d+)(\s)*(,|\.|\)|-)+(?=\w)[^\d\n]+'

    regexp = '^(\d+)(\s|-)+(\w+)(?:\n+)'
    regexp = '^(\d+)(\s|,|\.|\)|-)*(\w|\s|,)+(?:(\n|\.|$)+)'
    #regexp = '(?<=\s)(?:\d+)(\s)*(,|\.|\)|-)+(?=\w)[^\d\n]+'
    regexp = '^(\d+)(\s|,|\.|\)|-)*\w\w[^\n\.\d]+$'


    # Match only uppercase if space only?

    regexp = '^(?P<order>\d+)(?P<sep>(,|\.|\)|-)+)\s*(?P<location>\w\w[^\n\.\d]+)$'
    for s in shortcodes:
        text = load_post(PATH, shortcode=s)
        text = re.sub('@(\S)+', '', text)

        run(text, regexp)


    # ---------------------------------
    # All the captions
    # ---------------------------------
    # Get all shortcodes
    shortcodes  = sorted({
        x for v in SHORTCODE_CLASSES.values()
            for x in v})

    # Create tagger
    tagger = NERRule()
    for code in shortcodes:
        try:
            text = load_post(PATH, code)
            r = tagger.predict(text)
            show_result(text, r)
        except OSError as e:
            print(f"\n==> Unable to open {PATH}: {e}\n",
                  file=sys.stderr)

    import pycountry
    country = pycountry.countries.get(flag='🇬🇧')
    #print(country)


    from src.utils.ner import add_metadata

    @add_metadata(rule='country')
    @add_metadata(attr='flag')
    def regexp_v1():
        return {'text': 'Text1'}


    @add_metadata(rule='country', attr='flag')
    def regexp_v2():
        return [{'text': 'Text1'}]


    r1 = regexp_v1()
    r2 = regexp_v2()

    print(r1)
    print(r2)


    import re
    import string

    aux = "  Where  is the other . Percent 01 Half. "
    aux2 = aux.strip()
    aux3 = re.sub(r"\s+", "", aux)
    aux4 = " ".join(aux.split())
    aux5 = aux.translate({ord(c): None for c in string.whitespace})

    print(aux)
    print(aux2)
    print(aux3)
    print(aux4)
    print(aux5)

    res1 = re.sub(r'[^\w\s]', '', aux)
    res2 = aux.translate(str.maketrans('', '', string.punctuation))
    res3 = aux.translate(str.maketrans('', '', string.whitespace))
    print(res1)
    print(res2)
    print(res3)
    print("aaa")

    final = re.sub(r'[^\w\s]', '', aux)
    final = re.sub(r"\s+"," ", final)
    final = final.strip()
    print(final)

    import sys
    sys.exit()

    # ---------------------------------
    # All
    # ---------------------------------
    # Create tagger
    tagger = NERRule()
    for code in shortcodes:
        try:
            text = load_post(PATH, code)
            r = tagger.predict(text)
            show_result(text, r)
        except FileNotFoundError as e:
            print("File %s not found!" % code)
    #r = regexp_country_text(text3)
    #show_header(i="text")
    #show_result(r)


    def test_sum():
        assert sum([1, 2, 3]) == 6, "Should be 6"