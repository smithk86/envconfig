import os
from datetime import datetime
from uuid import UUID

import pytest
import pytz

from envconfig import EnvConfig


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
    except:
        raise RuntimeError('please source files/pytest.env before running tests')


def test_parser():
    conf = EnvConfig(filename='not_a_file.nul')
    # str
    assert conf.parse('abc', 'str') == 'abc'
    assert conf.parse('UxCcY-264RD_#aHPJNqLxkeS-_c^NydY', 'str') == 'UxCcY-264RD_#aHPJNqLxkeS-_c^NydY'
    assert conf.parse('1985019923', 'str') == '1985019923'
    # int
    assert conf.parse('1', 'int') == 1
    assert conf.parse('999', 'int') == 999
    assert conf.parse('1985019923', 'int') == 1985019923
    # float
    assert conf.parse('0.123', 'float') == 0.123
    assert conf.parse('123.123', 'float') == 123.123
    assert conf.parse('5123.1255622124', 'float') == 5123.1255622124
    # bool
    assert conf.parse('yes', 'bool') == True
    assert conf.parse('1', 'bool') == True
    assert conf.parse('true', 'bool') == True
    assert conf.parse('NO', 'bool') == False
    assert conf.parse('0', 'bool') == False
    assert conf.parse('FALSE', 'bool') == False
    # uuid
    assert conf.parse('a0063d99-62b2-4c8f-82b2-bd6bd64b8e8d', 'uuid') == UUID('a0063d99-62b2-4c8f-82b2-bd6bd64b8e8d')
    assert conf.parse('d66fc5a6-be43-47ac-b743-4501d6d0e918', 'uuid') == UUID('d66fc5a6-be43-47ac-b743-4501d6d0e918')
    assert conf.parse('5711923d-9fe5-4464-9891-351421ecf728', 'uuid') == UUID('5711923d-9fe5-4464-9891-351421ecf728')
    # date
    assert conf.parse('2018-01-01', 'date') == datetime(2018, 1, 1, 0, 0, 0)
    assert conf.parse('1994-11-05T08:15:30.123456-05:00', 'date') == datetime(1994, 11, 5, 8, 15, 30, 123456, tzinfo=pytz.timezone('Etc/GMT+5'))


def test_values():
    conf = EnvConfig(filename='not_a_file.nul')
    assert conf.value('PYTEST_ENV_STRING1', {'type': 'str'}) == 'abc'
    assert conf.value('PYTEST_ENV_STRINGZ', {'type': 'str', 'default': 'abc'}) == 'abc'
    with pytest.raises(ValueError, message='no config value has been defined for "PYTEST_ENV_STRING_DOESNOTEXIST"'):
        assert conf.value('PYTEST_ENV_STRING_DOESNOTEXIST', {'type': 'str'}) == 'abc'


@pytest.mark.parametrize('filename', [
    f'{dir_}/files/envconfig.json',
    f'{dir_}/files/envconfig.yaml'
])
def test_envconfig(filename):
    conf = EnvConfig(filename)
    conf_dict = conf.read()
    assert isinstance(conf_dict, dict)
    for name, definition in conf_dict.items():
        assert type(name) is str
        assert isinstance(definition, dict)
        assert 'type' in definition


@pytest.mark.parametrize('filename', [
    f'{dir_}/files/envconfig.json',
    f'{dir_}/files/envconfig.yaml'
])
def test_envconfig(filename):
    conf = EnvConfig(filename).to_dict()
    assert conf['PYTEST_ENV_STRING1'] == 'abc'
    assert conf['PYTEST_ENV_STRING2'] == 'UxCcY-264RD_#aHPJNqLxkeS-_c^NydY'
    assert conf['PYTEST_ENV_STRING3'] == '74f4fae1-855d-49be-863e-c1d5050af630'
    assert conf['PYTEST_ENV_STRING4'] == 'testing123'
    assert conf['PYTEST_ENV_INT1'] == 1
    assert conf['PYTEST_ENV_INT2'] == 99
    assert conf['PYTEST_ENV_INT3'] == 1563234
    assert conf['PYTEST_ENV_INT4'] == 123
    assert conf['PYTEST_ENV_BOOL1'] == True
    assert conf['PYTEST_ENV_BOOL2'] == False
    assert conf['PYTEST_ENV_BOOL3'] == True
    assert conf['PYTEST_ENV_BOOL4'] == False
    assert conf['PYTEST_ENV_BOOL5'] == True
    assert conf['PYTEST_ENV_UUID1'] == UUID('340ab29e-7df0-4f63-bd61-31efcb1c2dcf')
    assert conf['PYTEST_ENV_DATE1'] == datetime(1999, 10, 20, 0, 0)
