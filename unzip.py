
import os
import json
import glob
import instaloader
from pathlib import Path


# Path
path = ':saved'
path = 'test'

# Instagram session
username = "bernardhp"
L = instaloader.Instaloader()
L.load_session_from_file(username)

# Loop finding all xz files but excluding the
# file if it starts with the word iterator.
for f in glob.glob('%s/[!iterator]**/*.xz' % path, recursive=True):
    print(f)
    p = instaloader.load_structure_from_file(
        filename=f, context=L.context)

    # Delete context because it is a complex type defined
    # by instaloader and json loads does not know how to
    # dump it.
    aux = p.__dict__
    context = aux.pop('_context')
    aux['node'] = aux.pop('_node', {})

    # Save
    with open('%s/item.json' % Path(f).parent, 'w') as json_file:
        json_file.write(json.dumps(aux, indent=2))


# Can it be done without using instaloader?

"""
for competitors in os.listdir(path):
    for f in os.listdir(path+competitors):
        if f.endswith('.xz'):
            with lzma.open(path+competitors+'/'+f) as f:
                json_bytes = f.read()
                stri = json_bytes.decode('utf-8')
                data = json.loads(stri)

                print(data)
"""