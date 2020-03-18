import template.handler.handlerFactory
import pytest
from template.template import Template

# TODO template class is off and should be redecouped


class mockHandler:

    def __init__(*arg, **args):
        pass

    def getValues(self):
        return ([('TEST', 1), ('TEST2', 2)], 3, False)

    def getHandler(*arg, **args):
        return mockHandler()


# see https://github.com/pytest-dev/pytest/issues/363 to see why we dont
# bother having per module fixture
@pytest.fixture(autouse=True)
def mockHandle(monkeypatch):
    # Before test
    monkeypatch.setattr(Template, 'handlerFactory', mockHandler)


template1 = Template([('key1', None)])
template2 = Template([('key2', None), ('key1', None)])


def test_getValuesMono():
    values, pond, alleq = template1.getValuesMono(('key1', None), {})
    assert values == [('TEST', 1), ('TEST2', 2)]
    assert pond == 3
    assert alleq == False


def test_getAllValues():
    values, pond, alleq = template1.getAllValues({})
    assert values == [('TEST', 1), ('TEST2', 2)]
    assert pond == 3
    assert alleq == False

    values, pond, alleq = template2.getAllValues({})
    assert values == [('TEST', 1), ('TEST2', 2), ('TEST', 1), ('TEST2', 2)]
    assert pond == 6
    assert alleq == False


def test_replace():
    templateTest = Template([('key1', None)])
    res = templateTest.replace()
    assert (res == 'TEST2') or (res == 'TEST')

import random


def biaisedRand():
    return 0.5


def test_inequalWeightReplace(monkeypatch):
    monkeypatch.setattr(random, 'random', biaisedRand)
    values = [('tiger', 5), ('cow', 1), ('elephant', 5)]
    assert Template.inequalWeightReplace(values, 11) == 'cow'


def test_equalweight(monkeypatch):
    monkeypatch.setattr(random, 'random', biaisedRand)
    values = [('tiger', 1), ('cow', 1), ('elephant', 1)]
    assert Template.equalWeightReplace(values) == 'cow'
