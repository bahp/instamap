"""

"""
# Libraries
from nested_lookup import nested_lookup

#
document = [
    { 'taco' : 42 } ,
    { 'salsa' : [
        { 'burrito' : { 'taco' : 69 } },
        { 'guacamole' : { 'taco' : 72 } },
        { 'paella' : {
            'taco' : {
                'large': 2 ,
                'medium': 3,
                'small': 4
            }
        } },
    ] }
]

# Show
print(nested_lookup('taco', document))
