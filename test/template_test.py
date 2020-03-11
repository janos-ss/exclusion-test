import template.handler.handlerFactory
import pytest
from template.template import Template

# TODO template class is off and should be redecouped


class mockHandler:

    def __init__(*arg, **args):
        pass

    def getValues(self):
        return ['TEST', 'TEST2']

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
    assert template1.getValuesMono(('key1', None), {}) == ['TEST', 'TEST2']


def test_getAllValues():
    assert template1.getAllValues({}) == ['TEST', 'TEST2']
    assert template2.getAllValues({}) == ['TEST', 'TEST2', 'TEST', 'TEST2']


def test_replace():
    templateTest = Template([('key1', None)])
    res = templateTest.replace()

    assert (res == 'TEST2') or (res == 'TEST')
