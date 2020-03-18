
import os
import pytest
from os.path import abspath


from template.handler.handlerFactory import HandlerFactory
from template.handler.fileHandler import FileHandler
from template.handler.basicHandler import BasicHandler
from template.handler.directoryHandler import DirectoryHandler
from template.handler.commandHandler import CommandHandler


def mockParseOptions(string):
    # for this test we use raw option transmission
    return string

# see https://github.com/pytest-dev/pytest/issues/363 to see why we dont
# bother having per module fixture


@pytest.fixture(autouse=True)
def mockHandle(monkeypatch):
    # Before test
    monkeypatch.setattr(HandlerFactory, 'parseOptionsString', mockParseOptions)


def test_basic():
    handler = BasicHandler('test', None, {'test': ["res", ('tamere', 18)]})
    values, ponderation, allEqual = handler.getValues()
    assert sorted(values) == sorted([('res', 1.0), ('tamere', 18)])
    assert ponderation == 19
    assert not allEqual


def test_file():
    handler = FileHandler('testData/testKey1.val', None)

    values, ponderation, allEqual = handler.getValues()
    # User need to watch to not put the separator for no reason (really watch
    # out for the last \n)
    assert sorted(values) == sorted([('TEST1', 1), ('TEST2', 1)])
    assert ponderation == 2
    assert allEqual

    handler = FileHandler('testData/testKey2.val', {'sep': ':'})

    values, ponderation, allEqual = handler.getValues()
    assert sorted(values) == sorted([('TEST3', 1), ('TEST4', 1)])
    assert ponderation == 2
    assert allEqual

    handler = FileHandler('testData/ponderated', {})

    values, ponderation, allEqual = handler.getValues()
    assert sorted(values) == sorted([('tiger', 8), ('cow', 1), ('chicken', 7)])
    assert ponderation == 16
    assert not allEqual


def test_dir():
    handler = DirectoryHandler(
        'testData/unifiedsep', None)
    values, ponderation, allEqual = handler.getValues()

    assert sorted(values) == sorted([
        ('TEST3', 1), ('TEST4', 1), ('TEST1', 1), ('TEST2', 1)])
    assert ponderation == 4
    assert allEqual


def test_command():
    handler = CommandHandler('echo "test1\ntest2"', None)
    values, ponderation, allEqual = handler.getValues()
    assert sorted(values) == sorted([('test1', 1), ('test2', 1)])
    assert ponderation == 2
    assert allEqual
