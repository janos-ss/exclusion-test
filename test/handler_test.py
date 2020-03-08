from template.handler.handler import Handler
from template.handler.fileHandler import FileHandler
from template.handler.basicHandler import BasicHandler
from template.handler.directoryHandler import DirectoryHandler
from template.handler.commandHandler import CommandHandler

import os
from os.path import abspath



def test_getHandler():

    # Basic
    keys ={'test':['lala','lolo']}
    handler= Handler.getHandler('test', None, keys, '/', True )
    assert type(handler) == BasicHandler


    # Files
    valeFile='testData/testKey.val'

    handler= Handler.getHandler(valeFile, None, {}, '/', True )
    assert type(handler) == FileHandler
    
    handler= Handler.getHandler(valeFile, None, {}, ['/','/zarfsdgdg'], True )
    assert type(handler)== FileHandler

    # Feed with abspath
    abspathFile= abspath(valeFile) 
    handler= Handler.getHandler(abspathFile, None, {}, '/', True )
    assert type(handler) == FileHandler

    # Directory
    handler= Handler.getHandler('testData', None, {}, ['/','/zarfsdgdg'], False )
    assert type(handler) == DirectoryHandler

    # CMD
    handler= Handler.getHandler('echo TEST', None, {}, [], True )
    assert type(handler) == CommandHandler

    # priority
    keys2= {'testData':['test']}
    handler= Handler.getHandler('testData', None, keys2, ['/','/zarfsdgdg'], False )
    assert type(handler) == BasicHandler

    keys3= {valeFile:['test']}
    handler= Handler.getHandler(valeFile, None, keys3, ['/','/zarfsdgdg'], False )
    assert type(handler) == BasicHandler


def test_parseOptions():
    expected = {'type': 'file', 'opt': 'tr'}
    assert Handler.parseOptionsString('type   =  file, opt=tr') == expected
    assert Handler.parseOptionsString('') == {}

def test_checkFileAccess():
    assert Handler.checkFileAccess('/tete/tata.file', ['/tete'] )
    assert not Handler.checkFileAccess('/tete/tata.file', ['/te'] )
    assert Handler.checkFileAccess('/tete/tata.file', ['/etc', '/tete'] )
    assert not Handler.checkFileAccess('/tete/tata.file', ['/etc', '/tetaz'] )
    afile= '/opt/toto.py'
    assert Handler.checkFileAccess(afile, [afile] )

    assert Handler.checkFileAccess('testData/testKey.val', ['testData'] )
    assert Handler.checkFileAccess('./testData/testKey.val', ['./testData'] )

