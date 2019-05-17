import os
from datetime import datetime
from uuid import UUID

import pytest
import pytz

from envprops import EnvProps


dir_ = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session', autouse=True)
def environment():
    """ confirm all required enviornment variables exist """
    env_keys = list(os.environ.keys())
    try:
        assert 'PYTEST_ENV_STRING1' in env_keys
        assert 'PYTEST_ENV_STRING2' in env_keys
        assert 'PYTEST_ENV_STRING3' in env_keys
        assert 'PYTEST_ENV_INT1' in env_keys
        assert 'PYTEST_ENV_INT2' in env_keys
        assert 'PYTEST_ENV_INT3' in env_keys
        assert 'PYTEST_ENV_BOOL1' in env_keys
        assert 'PYTEST_ENV_BOOL2' in env_keys
        assert 'PYTEST_ENV_BOOL3' in env_keys
        assert 'PYTEST_ENV_BOOL4' in env_keys
        assert 'PYTEST_ENV_UUID1' in env_keys
        assert 'PYTEST_ENV_DATE1' in env_keys
        assert 'PYTEST_ENV_DATE2' in env_keys
    except Exception:
        raise RuntimeError('please source files/pytest.env before running tests')


def test_parser():
    conf = EnvProps(filename='not_a_file.nul')
    # str
    assert conf.parse('abc', 'str') == 'abc'
    assert conf.parse('UxCcY-264RD_#aHPJNqLxkeS-_c^NydY', 'str') == 'UxCcY-264RD_#aHPJNqLxkeS-_c^NydY'
    assert conf.parse('1985019923', 'str') == '1985019923'
    assert conf.parse('base64:a0hEISMzJmNMbX4iJFFoQ1Y2dXlIVEw3VCM9TlJLcDQ=', 'str') == 'kHD!#3&cLm~"$QhCV6uyHTL7T#=NRKp4'
    assert conf.parse('base64:PWZCY0U2SmoqYmhqIUMjM0pjUkFtQDN2YUhWIUNiVyY=', 'str') == '=fBcE6Jj*bhj!C#3JcRAm@3vaHV!CbW&'
    assert conf.parse('base64:fF89QCQmJCsjPStAI3wtISEhJiYmIyNfLSNeXz0qPSY=', 'str') == '|_=@$&$+#=+@#|-!!!&&&##_-#^_=*=&'
    # bytes
    assert conf.parse('UxCcY-264RD_#aHPJNqLxkeS-_c^NydY', 'bytes') == b'UxCcY-264RD_#aHPJNqLxkeS-_c^NydY'
    assert conf.parse(1985019923, 'bytes') == b'1985019923'
    assert conf.parse('base64:VU6ODsAuKYRMV+Xgs+GuBRX5Rgtv9NUgMQKl2MILNEU=', 'bytes') == b'UN\x8e\x0e\xc0.)\x84LW\xe5\xe0\xb3\xe1\xae\x05\x15\xf9F\x0bo\xf4\xd5 1\x02\xa5\xd8\xc2\x0b4E'
    assert conf.parse('base64:vZGWzhiQUW1eGOTjOtoWtb/zaEyD2an2KXrfxH/bXl0=', 'bytes') == b'\xbd\x91\x96\xce\x18\x90Qm^\x18\xe4\xe3:\xda\x16\xb5\xbf\xf3hL\x83\xd9\xa9\xf6)z\xdf\xc4\x7f\xdb^]'
    # int
    assert conf.parse('1', 'int') == 1
    assert conf.parse('999', 'int') == 999
    assert conf.parse('1985019923', 'int') == 1985019923
    # float
    assert conf.parse('0.123', 'float') == 0.123
    assert conf.parse('123.123', 'float') == 123.123
    assert conf.parse('5123.1255622124', 'float') == 5123.1255622124
    # bool
    assert conf.parse('yes', 'bool') is True
    assert conf.parse('1', 'bool') is True
    assert conf.parse('true', 'bool') is True
    assert conf.parse('NO', 'bool') is False
    assert conf.parse('0', 'bool') is False
    assert conf.parse('FALSE', 'bool') is False
    # uuid
    assert conf.parse('a0063d99-62b2-4c8f-82b2-bd6bd64b8e8d', 'uuid') == UUID('a0063d99-62b2-4c8f-82b2-bd6bd64b8e8d')
    assert conf.parse('d66fc5a6-be43-47ac-b743-4501d6d0e918', 'uuid') == UUID('d66fc5a6-be43-47ac-b743-4501d6d0e918')
    assert conf.parse('5711923d-9fe5-4464-9891-351421ecf728', 'uuid') == UUID('5711923d-9fe5-4464-9891-351421ecf728')
    # date
    assert conf.parse('2018-01-01', 'date') == datetime(2018, 1, 1, 0, 0, 0)
    assert conf.parse('1994-11-05T08:15:30.123456-05:00', 'date') == datetime(1994, 11, 5, 8, 15, 30, 123456, tzinfo=pytz.timezone('Etc/GMT+5'))

    # test bad type
    with pytest.raises(ValueError) as excinfo:
        conf.parse('bad value', 'strr')
    assert str(excinfo.value) == 'datatype not supported: strr [supported=str,bytes,int,float,bool,uuid,date]'


def test_values():
    conf = EnvProps(filename='not_a_file.nul')
    assert conf.value('PYTEST_ENV_STRING1', {'type': 'str'}) == 'abc'
    assert conf.value('PYTEST_ENV_STRINGZ', {'type': 'str', 'default': 'abc'}) == 'abc'
    with pytest.raises(ValueError) as excinfo:
        assert conf.value('PYTEST_ENV_STRING_DOESNOTEXIST', {'type': 'str'}) == 'abc'
    assert str(excinfo.value) == 'no config value has been defined for "PYTEST_ENV_STRING_DOESNOTEXIST"'


@pytest.mark.parametrize('filename', [
    f'{dir_}/files/properties.json',
    f'{dir_}/files/properties.yaml'
])
def test_envconfig(filename):
    conf = EnvProps(filename)
    conf_dict = conf.read()
    assert isinstance(conf_dict, dict)
    for name, definition in conf_dict.items():
        assert type(name) is str
        assert isinstance(definition, dict)
        assert 'type' in definition


@pytest.mark.parametrize('filename', [
    f'{dir_}/files/properties.json',
    f'{dir_}/files/properties.yaml'
])
def test_envconfig(filename):
    conf = EnvProps(filename).asdict()
    assert conf['PYTEST_ENV_STRING1'] == 'abc'
    assert conf['PYTEST_ENV_STRING2'] == 'UxCcY-264RD_#aHPJNqLxkeS-_c^NydY'
    assert conf['PYTEST_ENV_STRING3'] == '74f4fae1-855d-49be-863e-c1d5050af630'
    assert conf['PYTEST_ENV_STRING4'] == 'testing123'
    assert conf['PYTEST_ENV_BYTES1'] == b'1\xb3\xbf\xdd\xe5\xae\x92\x85\x92+\xa4.\x0b\xe6\x7f\xbc\xf4\xb5o\xa0n\xf8(\x17T&\xa6r\x0bF\x92\xfe'
    assert conf['PYTEST_ENV_BYTES2'] == b'\xcb#\xa8U\x80\xdf9\xd2\x87\x8f\x89\x8e\x1b\x0c\xcf\x99\xd4p\xb8\xfa\x8c\x9c\xb2=\xf6\xa3\xaa\xda\xfd\x1cd\x06'
    assert conf['PYTEST_ENV_BYTES3'] == b'testing123'
    assert conf['PYTEST_ENV_INT1'] == 1
    assert conf['PYTEST_ENV_INT2'] == 99
    assert conf['PYTEST_ENV_INT3'] == 1563234
    assert conf['PYTEST_ENV_INT4'] == 123
    assert conf['PYTEST_ENV_BOOL1'] is True
    assert conf['PYTEST_ENV_BOOL2'] is False
    assert conf['PYTEST_ENV_BOOL3'] is True
    assert conf['PYTEST_ENV_BOOL4'] is False
    assert conf['PYTEST_ENV_BOOL5'] is True
    assert conf['PYTEST_ENV_UUID1'] == UUID('340ab29e-7df0-4f63-bd61-31efcb1c2dcf')
    assert conf['PYTEST_ENV_DATE1'] == datetime(1999, 10, 20, 0, 0)
    assert conf['PYTEST_ENV_DATE2'] == datetime(2015, 1, 1, 12, tzinfo=pytz.timezone('Etc/GMT+5'))
