import json
import logging
import os
import sys
from base64 import b64decode
from distutils.util import strtobool
from uuid import UUID


__version__ = '0.2.0'


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


class EnvProps(object):
    supported_datatypes = [
        'str',
        'bytes',
        'int',
        'float',
        'bool',
        'uuid',
        'date'
    ]

    def __init__(self, filename, encoding='utf-8', yaml_loader='SafeLoader'):
        self.filename = filename
        self.encoding = encoding
        self.yaml_loader = yaml_loader

    def __iter__(self):
        data = self.read()
        if 'properties' not in data:
            raise ValueError('the "properties" key is missing')
        for config_name, definition in data['properties'].items():
            yield (config_name, self.value(config_name, definition))

    def asdict(self):
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
            return EnvProps._parse_string(strvalue, encoding=self.encoding)
        elif type_ == 'bytes':
            return EnvProps._parse_bytes(strvalue, encoding=self.encoding)
        elif type_ == 'int':
            return EnvProps._parse_int(strvalue)
        elif type_ == 'float':
            return EnvProps._parse_float(strvalue)
        if type_ == 'bool':
            return EnvProps._parse_bool(strvalue)
        elif type_ == 'uuid':
            return EnvProps._parse_uuid(strvalue)
        elif type_ == 'date':
            return EnvProps._parse_date(strvalue)
        else:
            raise ValueError(f"datatype not supported: {type_} [supported={','.join(EnvProps.supported_datatypes)}]")

    @staticmethod
    def _parse_string(strvalue, encoding='utf-8'):
        strvalue = str(strvalue)
        if strvalue.startswith('base64:'):
            return b64decode(strvalue[7:]).decode(encoding)
        else:
            return strvalue

    @staticmethod
    def _parse_bytes(strvalue, encoding='utf-8'):
        strvalue = str(strvalue)
        if strvalue.startswith('base64:'):
            return b64decode(strvalue[7:])
        else:
            return strvalue.encode(encoding)

    @staticmethod
    def _parse_int(strvalue):
        return int(strvalue)

    @staticmethod
    def _parse_float(strvalue):
        return float(strvalue)

    @staticmethod
    def _parse_bool(strvalue):
        if type(strvalue) is str:
            return bool(strtobool(strvalue))
        else:
            return bool(strvalue)

    @staticmethod
    def _parse_uuid(strvalue):
        return UUID(strvalue)

    @staticmethod
    def _parse_date(strvalue):
        if date_supported is False:
            raise ValueError('dateparser is not available; please run "pip install dateparser"')
        return dateparser.parse(strvalue)

    def read(self):
        with open(self.filename, 'r') as fh:
            data = fh.read()

        if self.filename.endswith('.yaml'):
            if yaml_supported is False:
                raise ValueError('pyyaml is not available; please run "pip install pyyaml"')
            yaml_loader = getattr(yaml, self.yaml_loader) if self.yaml_loader else None
            return yaml.load(data, Loader=yaml_loader)
        elif self.filename.endswith('.json'):
            return json.loads(data)
        else:
            raise ValueError('supported file types are json and yaml')