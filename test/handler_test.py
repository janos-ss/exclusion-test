import template.handler.handlerFactory
import pytest
from template.handler.handler import Handler


def test_createOptions():
    handler = Handler('placeholder', {})
    assert handler.createOptions(
        {}) == {'equalweight': False, 'sep': '\n', 'sep2': ' '}
    assert handler.createOptions({'tata': 'toto'}) == {
        'equalweight': False, 'tata': 'toto', 'sep': '\n', 'sep2': ' '}
    assert handler.createOptions(
        {'sep': 18}) == {'equalweight': False, 'sep': 18, 'sep2': ' '}

    class HHandler(Handler):
        default = {'sep': 'customSep'}

    handler = HHandler('placeHolder', {})
    assert handler.createOptions(
        {}) == {'equalweight': False, 'sep': 'customSep', 'sep2': ' '}
    assert handler.createOptions(
        {'sep': 20}) == {'equalweight': False, 'sep': 20, 'sep2': ' '}


def test_parseRow():
    handler = Handler('placeholder', {})
    assert handler.parseRow('toto') == ('toto', 1.0)
    assert handler.parseRow('toto 18') == ('toto', 18.0)
    assert handler.parseRow('toto 18msfjdpsf 45') == ('toto', 18.0)
    handler = Handler('placeholder', {'sep2': 'tata'})


def test_parseData():
    handler = Handler('placeholder', {})
    testData = """tiger 2
cow 4
tiger 1Mo22
monkey"""
    parsed, pond, allequal = handler.parseData(testData)
    assert sorted(parsed) == sorted(
        [('tiger', 2.0), ('cow', 4.0), ('tiger', 1.0), ('monkey', 1.0)])
    assert pond == 8
    assert not allequal

    handler = Handler('placeholder', {'equalweight': True})
    testData = """tiger 2
cow 4
tiger 1Mo22
monkey"""
    parsed, pond, allEq = handler.parseData(testData)
    assert sorted(parsed) == sorted(
        [('tiger', 1), ('cow', 1), ('tiger', 1), ('monkey', 1)])
    assert pond == 4

    handler = Handler('placeholder', {})
    testData = """tiger
cow 4
tiger 1Mo22
monkey"""
    parsed, pond, allEq = handler.parseData(testData)
    assert sorted(parsed) == sorted(
        [('tiger', 1), ('cow', 4), ('tiger', 1), ('monkey', 1)])
    assert pond == 7
