"""

"""
# Libraries
import os
import json
import time

import bardapi
from bardapi import Bard
from dotenv import load_dotenv

# Load
load_dotenv()


# .. note: Depending on the country, it might be that a
#          single cookie works. However, in many countries
#          more than one cookie is required.

# Setting cookie manually
#token = 'dAhSrS8RLHFSgdqcWCiC50xeaRB3tFY0962GZIYPI7gRkiNcA3ECMhSBfmf3fynhgBFx2w.'
#os.environ['_BARD_API_KEY'] =token


text = """
Which image is your favourite ??
Quale immagine è la tua preferita ??
Scegli il tuo scatto preferito tagga un amico e condividi sul tuo story...!!
1- Forcella Denti Di Terrarossa @artur.alla
2- Laghi di San Giuliano @explorewithartur
3- Lago Nambino @arturlandscapes
4- Lago Di Antermoia @trekwithartur
5- Rifugio Brentei @artur.alla
6- Lagorai @explorewithartur
7- Molveno @arturlandscapes
8- Cornetto, Bondone @trekwithartur
9- Panarotta @artur.alla
10- Le Odle @arturlandscapes
"""

query1 = """
Could you extract the locations from the caption below and let me know 
the district, city and country they are in. Please can you put that 
information into a json file where each item has the following 
information: address, image_link, source favicon url and the position
in which it was found in the text. 

\n\n
The caption is:\n '%s'.
"""

query2 = """Please construct a json file extracting for each of the 
locations in the following caption the name, the full address, image 
link, favicon url, the latitude, the longitude, the type of location, 
and the position in which it was found in the text.

The caption is: %s
"""

def call_bard(query):
    bard = Bard()
    answer = bard.get_answer(query)
    return answer



#bard = Bard(timeout=10) # Set timeout in seconds

# Load session from cookies
from bardapi import BardCookies
bard = BardCookies(token_from_browser=True, timeout=40)
response = bard.get_answer(query1 % text)

# Query
response = bard.get_answer(query1 % text)

# Save
with open('bard.json', 'w') as f:
    json.dump(response, f, indent=4)

# Show
print(json.dumps(response, indent=4))