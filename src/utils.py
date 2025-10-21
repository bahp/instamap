# Libraries
import pandas as pd

"""
class AttrDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __dir__(self):
        return list(self) + dir(type(self))
"""

class AttrDict(dict):
    """Dictionary subclass whose entries can be accessed by attributes"""
    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """ Construct nested AttrDicts from nested dictionaries. """
            if not isinstance(data, dict):
                return data
            else:
                return AttrDict({key: from_nested_dict(data[key])
                                    for key in data})

        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])



class Fetch:
    """"""
    def __init__(self, json, attrdict=False, prefix=''):
        self.attrdict = attrdict
        if self.attrdict:
            self._json = AttrDict(json)
        else:
            self._json = json

    def find_locations(self):
        nested = self.find_nested_location()
        nested.append(self.find_node_location())
        nested.append(self.find_user_location())
        return nested

        node = self.find_node_location()
        user = self.find_user_location()
        text = self.find_text_location()
        return None

    def get(self):
        pass

    def shortcode(self):
        if self.attrdict:
            return self._json._node.shortcode
        return self._json['node']['shortcode']

    def display_url(self):
        if self.attrdict:
            return self._json._node.display_url
        return self._json['node']['display_url']

    def location(self):
        location = self.find_node_location()
        print(location)
        if location:
            return location
        return {}
        #location = self.find_nested_location()
        #location = location[0] if location else {}
        #return location

    def caption(self):
        pass
    
    def find_node_location(self):
        try:
            if self.attrdict:
                return self._json._node.location
            return self._json['node']['location']
        except (AttributeError, KeyError) as e:
            return []

    def find_user_location(self):
        try:
            #iphone_struct (or sometimes _node)
            if self.attrdict:
                return self._json.node.iphone_struct.location
            return self._json['node']['iphone_struct']['location']
        except (AttributeError, KeyError) as e:
            return []


    def find_nested_location(self):
        # Library
        from nested_lookup import nested_lookup
        return nested_lookup("location", self._json)

    def find_text_location(self):
        pass

    def json_normalize(self, raw=False):
        if raw:
            return pd.json_normalize(self._json)
        return pd.json_normalize({
            'shortcode': self.shortcode(),
            'location': self.location(),
            'display_url': self.display_url()
        }, sep='_')




if __name__ == '__main__':

    # Sample
    d = {
        'name': 'Bernard',
        'surname': 'Hernandez',
        'location': {
            'lat': 1,
            'lon': 2
        }
    }

    # Dictionary
    m = AttrDict(d)

    # Show
    print(m)
    print(m.name)
    print(m.surname)
    print(m.location.lat)