import json
import logging
import os
import sys
from distutils.util import strtobool
from uuid import UUID

try:
    import yaml
    yaml_supported = True
except ModuleNotFoundError:
    yaml_supported = False


try:
    import dateparser
    date_supported = True
except ModuleNotFoundError:
    date_supported = False


supported_datatypes = [
    'str',
    'int',
    'float',
    'bool',
    'uuid'
]


class EnvConfig(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for config_name, definition in self.read().items():
            yield (config_name, self.value(config_name, definition))

    def to_dict(self):
        return dict(self)

    def value(self, config_name, definition):
        # set default value
        strvalue = definition.get('default')
        # attempt to get value from environment but default to the default value
        strvalue = os.environ.get(config_name, strvalue)
        if strvalue is None:
            raise ValueError(f'no config value has been defined for "{config_name}"')
        else:
            return self.parse(strvalue, definition['type'])

    def parse(self, strvalue, type_):
        if type_ == 'str':
            return strvalue
        elif type_ == 'int':
            return int(strvalue)
        elif type_ == 'float':
            return float(strvalue)   
        if type_ == 'bool':
            if type(strvalue) is str:
                return bool(strtobool(strvalue))
            else:
                return bool(strvalue)
        elif type_ == 'uuid':
            return UUID(strvalue)
        elif type_ == 'date':
            if date_supported is False:
                raise ValueError('dateparser is not available; please run "pip install dateparser"')
            return dateparser.parse(strvalue)
        else:
            raise ValueError(f"datatype not supported: {type_} [supported={','.join(supported_datatypes)}")

    def read(self):
        with open(self.filename, 'r') as fh:
            data = fh.read()

        if self.filename.endswith('.yaml'):
            if yaml_supported is False:
                raise ValueError('pyyaml is not available; please run "pip install pyyaml"')
            return yaml.load(data)
        elif self.filename.endswith('.json'):
            return json.loads(data)
        else:
            raise ValueError('supported file types are json and yaml')
