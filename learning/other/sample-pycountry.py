""""""
# Libraries
import re
import time
import pycountry

# ---------------------------------
# Basic
# ---------------------------------
# Text
text1 = "United States (New York), United kingdom (London)"
text2 = "I am in 🇺🇸"
text3 = "🇼🇫 🇼🇸 🇾🇪🇿🇦 🇿🇲🇿🇼"

# Find countries
for country in pycountry.countries:
    if country.name.lower() in text1.lower():
        print(country)

# Find flags
for country in pycountry.countries:
    if country.flag in text2.lower():
        print(country)

# ---------------------------------
# Efficiency
# ---------------------------------

def find_countries(txt):
    """"""
    return [country
        for country in pycountry.countries
            if country.flag in txt.lower()]

def regexp_country_flag_v1(txt):
    """Find country flags."""
    countries = find_countries(txt)
    flags = [c.flag for c in countries]
    regexp = '(%s)' % '|'.join(flags)
    result = list(re.finditer(regexp, txt, re.MULTILINE))
    return result

def regexp_country_flag_v2(txt):
    pass

# Longer text
text4 = """
    A paragraph is defined 🇼🇫 🇼🇸 as “a group of sentences or a single sentence 
    that forms a unit” (Lunsford and Connors 116). Length and appearance 
    do not determine 🇾🇪🇿🇦 whether a section in a paper is a paragraph. For 
    instance, in some styles of writing, particularly journalistic styles, 
    a paragraph can be just one sentence long. 🇿🇲🇿🇼
"""

# Query
query = text3


# ---------
# Method 1
# ---------
# Get all flags
flags = [ country.flag for country in pycountry.countries ]

# Get regular expression
regexp = '(%s)' % '|'.join(flags)

# Compute
t0 = time.time()
r1 = list(re.finditer(regexp, str(query), re.MULTILINE))
t1 = time.time()

# ---------
# Method 2
# ---------
# Compute
t2 = time.time()
r2 = regexp_country_flag_v1(query)
t3 = time.time()

# Show
print("\n\n\n")
print(r1)
print(r2)

print("Method 1: %s" % (t1-t0))
print("Method 2: %s" % (t3-t2))