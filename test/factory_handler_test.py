import os
import pytest
from os.path import abspath


from template.handler.handlerFactory import HandlerFactory
from template.handler.fileHandler import FileHandler
from template.handler.basicHandler import BasicHandler
from template.handler.directoryHandler import DirectoryHandler
from template.handler.commandHandler import CommandHandler

factoryInvalidFileConstraint = [HandlerFactory(['/zarfsdgdg'])]
factoryInvalidFileConstraint.append(HandlerFactory('/zarfsdgdg'))
basicFactory = HandlerFactory()
commandFactory = HandlerFactory(allowCommand=True)

valeFile = 'testData/testKey1.val'
fileFactory = [HandlerFactory('.')]  # singleton
fileFactory.append(HandlerFactory(['.']))  # List notation
fileFactory.append(HandlerFactory(['/azfsdfsdgd', '.']))  # invalid and valid
fileFactory.append(HandlerFactory(abspath(valeFile)))  # using absolutepath
fileFactory.append(HandlerFactory(valeFile))  # constraint = file

dirValue = 'testData'
dirFactory = [HandlerFactory('.')]  # singleton
dirFactory.append(HandlerFactory(['.']))  # List notation
dirFactory.append(HandlerFactory(['/azfsdfsdgd', '.']))  # invalid and valid
dirFactory.append(HandlerFactory(abspath(dirValue)))  # using absolutepath
dirFactory.append(HandlerFactory(dirValue))  # constraint = file


everythingFactory = HandlerFactory('/', True)


def test_guessHandler():

    # Basic
    keys = {'test': ['lala', 'lolo']}
    handler = everythingFactory.guessHandler('test', None, keys)
    assert type(handler) == BasicHandler

    # Files
    valeFile = 'testData/testKey1.val'
    for fileFactoryN in fileFactory:
        handler = fileFactoryN.guessHandler(valeFile, None, {})
        assert type(handler) == FileHandler

    for dirFactoryN in dirFactory:
        # Directory
        handler = dirFactoryN.guessHandler(
            dirValue, None, {})
        assert type(handler) == DirectoryHandler

    # CMD
    handler = commandFactory.guessHandler('echo TEST', None, {})
    assert type(handler) == CommandHandler

    # priority
    keys2 = {'testData': ['test']}
    handler = fileFactory[0].guessHandler(
        'testData', None, keys2)
    assert type(handler) == BasicHandler

    keys3 = {valeFile: ['test']}
    handler = fileFactory[0].guessHandler(
        'testData', None, keys2)
    assert type(handler) == BasicHandler

    # must fail
    with pytest.raises(PermissionError):
        handler = fileFactory[0].getHandler(
            'echo remote exec', None, keys3)

    with pytest.raises(PermissionError):
        handler = fileFactory[0].getHandler(
            '/etc/passwd', None, {})


def test_getHandler():
    # force with type option
    keys3 = {valeFile: ['test']}
    handler = everythingFactory.getHandler(
        valeFile, 'type=file', keys3)
    assert type(handler) == FileHandler

    with pytest.raises(ValueError):
        keys3 = {valeFile: ['test']}
        handler = everythingFactory.guessHandler(
            valeFile, 'type=fiagsd', keys3)


def test_parseOptions():
    expected = {'type': 'file', 'opt': 'tr'}
    assert HandlerFactory.parseOptionsString(
        'type   =  file, opt=tr') == expected
    assert HandlerFactory.parseOptionsString('') == {}


def test_checkFileAccess():
    for factory in fileFactory:
        assert factory.checkFileAccess(valeFile)

    for factory in factoryInvalidFileConstraint:
        assert not factory.checkFileAccess(valeFile)

# Same for directory


def test_get_file():
    with pytest.raises(PermissionError):
        factoryInvalidFileConstraint[0].getFile(valeFile, {})
    assert type(fileFactory[0].getFile(valeFile, {})) == FileHandler

# Same for directory


def test_get_Directory():
    with pytest.raises(PermissionError):
        factoryInvalidFileConstraint[0].getDirectory(valeFile, {})
    assert type(fileFactory[0].getDirectory(valeFile, {})) == DirectoryHandler


def test_get_Command():
    with pytest.raises(PermissionError):
        fileFactory[0].getCommand(valeFile, {})
    assert type(commandFactory.getCommand(valeFile, {})) == CommandHandler
