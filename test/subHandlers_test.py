
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
    handler = BasicHandler('test', None, {'test': ["res"]})
    assert handler.getValues().sort() == ['res'].sort()


def test_file():
    handler = FileHandler('testData/testKey1.val', None)
    assert handler.getValues().sort() == ['TEST1', 'TEST2'].sort()

    handler = FileHandler('testData/testKey2.val', {'sep': ':'})
    assert handler.getValues().sort() == ['TEST3', 'TEST4'].sort()


def test_dir():
    handler = DirectoryHandler(
        'testData/unifiedsep', None)
    assert handler.getValues().sort() == [
        'TEST3', 'TEST4', 'TEST1', 'TEST2'].sort()


def test_command():
    handler = CommandHandler('echo "test1\ntest2"', None)
    assert handler.getValues().sort() == ['test1', 'test2'].sort()
