import pytest

"""
def capital_case(x):
    return x.capitalize()

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'

def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        capital_case(9)

@pytest.fixture
    return Wallet()

@pytest.fixture
def wallet():
    return Wallet(20)

def test_default_initial_amount(empty_wallet):
    assert empty_wallet.balance == 0

def test_setting_initial_amount(wallet):
    assert wallet.balance == 20

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])
def test_transactions(earned, spent, expected):
    my_wallet = Wallet()
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected

@pytest.fixture
def my_wallet():
    return Wallet()

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])
def test_transactions(my_wallet, earned, spent, expected):
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected
"""

@pytest.fixture
def icons():
    text = """
        🌍 Madrid
        🌏 Kuala Lumpur
        🌐🚩 Guatemala
        Hatchard's library 📚
        📍 London, United Kingdom
        📌Manchester, United Kingdom 
    """
    return [
        ('🌍 Lugano', 'Lugano'),
        ('🌏 Maldives', 'Maldives'),
        ('🌐 Florence', 'Florence'),
        ('🚩 Cambodia', 'Cambodia'),
        ('📍 Madrid', 'Madrid'),
        ('📌 Salamanca', 'Salamanca'),
        ('📚 Hatchards', 'Hatchards'),
        #('Hatchards📚', 'Hatchards'),
        (text, 5)
    ]

@pytest.fixture
def bulletpoints():
    """"""
    text = """
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
    return [
        #(text, 9)
    ]

@pytest.fixture
def country_flags():
    return [
        ('🇲🇪', 'Montenegro')
    ]

@pytest.fixture
def country_texts():
    return [
        #('Spain', 'Spain'),
        #('MoNtEnEGrO', 'Montenegro')
    ]

@pytest.fixture
def captions():
    return [
        ('CvE3TlxLgKU', [
            {'rule':'bulletpoint', 'method':'inline', 'text':'Magome Juku'},
            {'rule':'bulletpoint', 'method':'inline', 'text':'Takayama'},
            {'rule':'bulletpoint', 'method':'inline', 'text':'Nakano'},
            {'rule':'bulletpoint', 'method':'inline', 'text':'Konkaikomyo-ji'}
        ]),
        ('Cy-hYVzPemK', []),
        ('CxQ1tJ8rV9w', [
            {'rule': 'country', 'attr': 'flag', 'text': '🇮🇹'},
            {'rule': 'icon', 'text': '🌍'}
        ]),
        ('CzBYpc5ocQb', [
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Camden'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Richmond'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Notting Hill'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Hampstead'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'City of London'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Chelsea'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Greenwich'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Fitzrovia'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Belgravia'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Primrose Hill'},
        ]),
        ('CyRLr01sj8i', [
            {'rule':'icon', 'text':'Vienna'},
            {'rule':'country', 'attr':'text', 'text':'Austria'},
            {'rule':'country', 'attr':'flag', 'text':'🇦🇹'},
        ]),
        ('CysEVwgqeS8', [
            {'rule':'country', 'attr':'flag', 'text':'🇰🇿'},
        ]),
        ('Cy6EgYltiFv', [
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Brussels'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Ghent'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Brugge'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Mechelen'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Leuven'}
        ]),
        ('B5ewgDhKQth', [
            {'rule':'country', 'attr':'text', 'text':'Italy'},
        ]),
        ('B5NqBLMJGZM', [
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Brugge'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Gent'},
            {'rule':'bulletpoint', 'method':'multiline', 'text':'Brussels'},
        ])
    ]



def test_regexp_icon_location(icons):
    """"""
    from src.utils.ner import regexp_icon_location
    for text,label in icons:
        result = regexp_icon_location(text)
        #with pytest.raises(TypeError):
        #    assert len(result) == 0
        if isinstance(label, str):
            assert label in result[0]['text']
        else:
            assert len(result) == label

def test_regexp_bulletpoint_location(bulletpoints):
    """"""
    from src.utils.ner import regexp_bulletpoint_location
    for text, label in bulletpoints:
        print(text, label)
        result = regexp_bulletpoint_location(text)
        print(result)
        #assert len(result) == 1

def test_regexp_country_flag(country_flags):
    """"""
    from src.utils.ner import regexp_country_flag
    for text,label in country_flags:
        result = regexp_country_flag(text)
        assert len(result) == 1

def test_regexp_country_text(country_texts):
    """"""
    from src.utils.ner import regexp_country_text
    for text,label in country_texts:
        result = regexp_country_text(text)
        print(result)
        print("AAA")
        assert len(result) == 1



def check_caption_regexp(label, result):
    """"""
    for l in label:
        matched = False
        for r in result:
            if (l['rule'].lower() == r['rule'].lower()) and \
               (l['text'].lower() in r['text'].lower()):
               matched = True
        if matched is False:
            return False, l
    return True, ''


def test_regexp_all(captions):
    """"""

    def load_caption(shortcode):
        fullpath = path / shortcode / 'caption.txt'
        with open(fullpath, 'r') as f:
            text = f.read()
        return text

    from pathlib import Path
    from src.utils.ner import NERRule
    tagger = NERRule()
    path = Path('./data/bernardhp/posts')

    # Capture all shortcodes for those in which the
    # information extracted from the caption does not
    # match the predefined labels.
    capture = {}

    for shortcode, label in captions:
        caption = load_caption(shortcode)
        result = tagger.predict(caption)
        matched, message = check_caption_regexp(label, result)
        if not matched:
            capture[shortcode] = message

        # Show
        print(shortcode)
        print(caption)
        print(result)

    # Return
    if len(capture) > 0:
        assert False, capture
    assert True, ''

